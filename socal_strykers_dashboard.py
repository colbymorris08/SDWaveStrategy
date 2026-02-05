#!/usr/bin/env python3
"""
SoCal Strykers Revenue Analysis Dashboard Generator
Generates a comprehensive HTML dashboard with regression model, visualizations, and revenue initiatives
"""

import pandas as pd
import base64
from pathlib import Path
import os

# Load data
print("Loading data from data.csv...")
print(f"Current directory: {os.getcwd()}")

# Try to find data.csv
if os.path.exists('data.csv'):
    df = pd.read_csv('data.csv')
elif os.path.exists('/mnt/user-data/uploads/SoCal_Strykers_Secondary_Ticket_Sales_Secondary_Tix_Transaction_Data_.csv'):
    print("Note: Using full dataset path")
    df = pd.read_csv('/mnt/user-data/uploads/SoCal_Strykers_Secondary_Ticket_Sales_Secondary_Tix_Transaction_Data_.csv')
else:
    raise FileNotFoundError("Could not find data.csv. Please run this script from the directory containing data.csv")

# Clean data
df['Total_Revenue'] = df['Total Block Price'].str.replace('$', '', regex=False).str.replace(',', '').astype(float)
df['Seats'] = df['Number of Seats']
df['Event_Date'] = pd.to_datetime(df['Event Date'], format='%m/%d/%Y', errors='coerce')
df['Sale_Date'] = pd.to_datetime(df['Sale Date'], format='%m/%d/%Y', errors='coerce')
df['Days_Before_Game'] = (df['Event_Date'] - df['Sale_Date']).dt.days

def categorize_customer(days):
    if pd.isna(days):
        return 'Unknown'
    if days >= 15:
        return 'Planner'
    elif days >= 3:
        return 'In-Between'
    else:
        return 'Last-Minute'

df['Customer_Type'] = df['Days_Before_Game'].apply(categorize_customer)

# Calculate metrics
baseline_revenue = df['Total_Revenue'].sum()
baseline_seats = df['Seats'].sum()
baseline_atp = baseline_revenue / baseline_seats
total_games = 31

# Filter for known customer types
known_df = df[df['Customer_Type'] != 'Unknown']

# Calculate customer type ATPs
planner_data = known_df[known_df['Customer_Type'] == 'Planner']
planner_atp = planner_data['Total_Revenue'].sum() / planner_data['Seats'].sum()
planner_seats = planner_data['Seats'].sum()

inbetween_data = known_df[known_df['Customer_Type'] == 'In-Between']
inbetween_atp = inbetween_data['Total_Revenue'].sum() / inbetween_data['Seats'].sum()
inbetween_seats = inbetween_data['Seats'].sum()

lastmin_data = known_df[known_df['Customer_Type'] == 'Last-Minute']
lastmin_atp = lastmin_data['Total_Revenue'].sum() / lastmin_data['Seats'].sum()
lastmin_seats = lastmin_data['Seats'].sum()
lastmin_revenue = lastmin_data['Total_Revenue'].sum()

# Initiative calculations
# Initiative 1
target_lastmin_atp = planner_atp * 0.75
retention = 0.90
new_lastmin_seats = lastmin_seats * retention
new_lastmin_revenue = new_lastmin_seats * target_lastmin_atp
revenue_change_1 = new_lastmin_revenue - lastmin_revenue

# Initiative 2
seats_converting_a = inbetween_seats * 0.20
atp_increase_a = planner_atp - inbetween_atp
revenue_increase_a = seats_converting_a * atp_increase_a

seats_converting_b = lastmin_seats * 0.20
atp_increase_b = inbetween_atp - lastmin_atp
revenue_increase_b = seats_converting_b * atp_increase_b
revenue_change_2 = revenue_increase_a + revenue_increase_b

# Initiative 3
avg_attendance = 1922
eligible_pct = 0.798
take_rate = 1/3
upgrade_price = 10
eligible_per_game = avg_attendance * eligible_pct
upgrades_per_game = eligible_per_game * take_rate
revenue_per_game = upgrades_per_game * upgrade_price
revenue_change_3 = revenue_per_game * total_games

# Total
total_increase = revenue_change_1 + revenue_change_2 + revenue_change_3
new_revenue = baseline_revenue + total_increase

print(f"Baseline Revenue: ${baseline_revenue:,.2f}")
print(f"Total Increase: ${total_increase:,.2f}")
print(f"New Revenue: ${new_revenue:,.2f}")

# Function to encode image to base64
def encode_image(image_path):
    """Encode image file to base64 string"""
    # Try multiple possible locations
    possible_paths = [
        image_path,  # Direct path
        f'outputs/{image_path}',  # outputs subdirectory
        f'/mnt/user-data/outputs/{image_path}',  # Full path
    ]
    
    for path in possible_paths:
        try:
            with open(path, 'rb') as img_file:
                return base64.b64encode(img_file.read()).decode()
        except FileNotFoundError:
            continue
    
    print(f"Warning: Could not find {image_path} in any location")
    return None

# List of figures to include
figures = [
    ('figure_00_summary_stats.png', 'Summary Statistics Dashboard'),
    ('figure_05_atp_by_customer_type.png', 'ATP by Customer Type'),
    ('figure_06_atp_by_seating.png', 'ATP by Seating Category'),
    ('figure_10_promotion_comparison.png', 'ATP by Promotion Status'),
    ('figure_03_days_before_game.png', 'Purchase Timing Distribution'),
    ('figure_04_atp_by_season.png', 'ATP by Season'),
    ('figure_07_atp_by_promotion_type.png', 'ATP by Promotion Type'),
    ('figure_08_opponents_by_atp.png', 'ATP by Opponent'),
    ('figure_09_atp_by_day_of_week.png', 'ATP by Day of Week'),
]

# Encode all images
encoded_images = {}
for fig_name, fig_title in figures:
    encoded = encode_image(fig_name)
    if encoded:
        encoded_images[fig_name] = encoded
        print(f"✓ Encoded: {fig_name}")
    else:
        print(f"✗ Missing: {fig_name}")

# Generate HTML
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SoCal Strykers Revenue Analysis Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #ffffff;
            line-height: 1.6;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }}
        
        header {{
            text-align: center;
            margin-bottom: 50px;
            padding-bottom: 30px;
            border-bottom: 2px solid rgba(255, 255, 255, 0.2);
        }}
        
        h1 {{
            font-size: 3em;
            font-weight: 700;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #00d9ff, #ffd700);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .subtitle {{
            font-size: 1.2em;
            color: rgba(255, 255, 255, 0.8);
            margin-top: 10px;
        }}
        
        .section {{
            background: rgba(255, 255, 255, 0.08);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        h2 {{
            font-size: 2em;
            margin-bottom: 20px;
            color: #00d9ff;
            border-left: 5px solid #ffd700;
            padding-left: 15px;
        }}
        
        h3 {{
            font-size: 1.5em;
            margin: 25px 0 15px 0;
            color: #ffd700;
        }}
        
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, rgba(0, 217, 255, 0.2), rgba(255, 215, 0, 0.2));
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .metric-label {{
            font-size: 0.9em;
            color: rgba(255, 255, 255, 0.7);
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .metric-value {{
            font-size: 2em;
            font-weight: 700;
            color: #ffffff;
        }}
        
        .calculation-box {{
            background: rgba(0, 0, 0, 0.3);
            border-left: 4px solid #00d9ff;
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
        }}
        
        .calculation-box pre {{
            color: #ffffff;
            font-size: 0.95em;
            line-height: 1.8;
            white-space: pre-wrap;
        }}
        
        .initiative-card {{
            background: linear-gradient(135deg, rgba(255, 107, 107, 0.15), rgba(255, 215, 0, 0.15));
            border-radius: 12px;
            padding: 25px;
            margin: 20px 0;
            border: 2px solid rgba(255, 215, 0, 0.3);
        }}
        
        .initiative-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .initiative-title {{
            font-size: 1.3em;
            font-weight: 600;
            color: #ffd700;
        }}
        
        .initiative-impact {{
            font-size: 1.5em;
            font-weight: 700;
            color: #00ff88;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 8px;
            overflow: hidden;
        }}
        
        th {{
            background: rgba(0, 217, 255, 0.3);
            padding: 15px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.9em;
            letter-spacing: 1px;
        }}
        
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        tr:hover {{
            background: rgba(255, 255, 255, 0.05);
        }}
        
        .model-equation {{
            background: rgba(0, 0, 0, 0.4);
            padding: 25px;
            border-radius: 10px;
            margin: 20px 0;
            border: 2px solid #00d9ff;
        }}
        
        .equation {{
            font-family: 'Courier New', monospace;
            font-size: 1em;
            line-height: 1.8;
            color: #ffffff;
        }}
        
        .stat-badge {{
            display: inline-block;
            background: rgba(0, 217, 255, 0.3);
            padding: 5px 15px;
            border-radius: 20px;
            margin: 5px;
            font-size: 0.9em;
            border: 1px solid rgba(0, 217, 255, 0.5);
        }}
        
        .total-impact {{
            background: linear-gradient(135deg, rgba(0, 255, 136, 0.2), rgba(255, 215, 0, 0.2));
            border: 3px solid #00ff88;
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            margin: 30px 0;
        }}
        
        .total-impact .amount {{
            font-size: 3em;
            font-weight: 700;
            color: #00ff88;
            margin: 10px 0;
        }}
        
        .total-impact .percentage {{
            font-size: 1.5em;
            color: #ffd700;
        }}
        
        .image-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
            margin: 30px 0;
        }}
        
        .image-card {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .image-card img {{
            width: 100%;
            border-radius: 8px;
            margin-bottom: 10px;
        }}
        
        .image-title {{
            text-align: center;
            font-size: 1.1em;
            color: #ffd700;
            margin-top: 10px;
        }}
        
        .highlight {{
            color: #00ff88;
            font-weight: 600;
        }}
        
        .note {{
            background: rgba(255, 215, 0, 0.1);
            border-left: 4px solid #ffd700;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
            font-size: 0.95em;
        }}
        
        footer {{
            text-align: center;
            margin-top: 50px;
            padding-top: 30px;
            border-top: 2px solid rgba(255, 255, 255, 0.2);
            color: rgba(255, 255, 255, 0.6);
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 20px;
            }}
            
            h1 {{
                font-size: 2em;
            }}
            
            .metric-grid {{
                grid-template-columns: 1fr;
            }}
            
            .image-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎫 SoCal Strykers Revenue Analysis</h1>
            <div class="subtitle">Statistical Model & Strategic Revenue Optimization</div>
            <div class="subtitle" style="font-size: 0.9em; margin-top: 5px;">Colby Morris | colby.morris08@gmail.com</div>
            <div class="subtitle" style="font-size: 0.85em; margin-top: 3px;">San Diego Wave Questionnaire</div>
        </header>

        <!-- Executive Summary -->
        <div class="section">
            <h2>📊 Executive Summary</h2>
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-label">Current Revenue</div>
                    <div class="metric-value">${baseline_revenue:,.0f}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Total Seats Sold</div>
                    <div class="metric-value">{int(baseline_seats):,}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Overall ATP</div>
                    <div class="metric-value">${baseline_atp:.2f}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Total Games</div>
                    <div class="metric-value">{total_games}</div>
                </div>
            </div>
        </div>

        <!-- Regression Model Analysis -->
        <div class="section">
            <h2>🔬 Regression Analysis</h2>
            
            <div class="note">
                <strong>Key Finding:</strong> Customer purchase timing affects pricing differently by seat location. Premium seats lose significantly more value when sold last-minute.
            </div>
            
            <h3>Model Performance</h3>
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-label">R-squared</div>
                    <div class="metric-value">19.84%</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">F-statistic</div>
                    <div class="metric-value">474.30</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">p-value</div>
                    <div class="metric-value">< 0.001</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Sample Size</div>
                    <div class="metric-value">23,006</div>
                </div>
            </div>
            
            <h3>Regression Equation</h3>
            <div class="model-equation">
                <div class="equation">
Price = 79.12 (Intercept)<br>
        &nbsp;&nbsp;&nbsp;&nbsp;- 21.41 × In-Between<br>
        &nbsp;&nbsp;&nbsp;&nbsp;- 49.04 × Last-Minute<br>
        &nbsp;&nbsp;&nbsp;&nbsp;+ 45.03 × Lower_Goal_Line<br>
        &nbsp;&nbsp;&nbsp;&nbsp;+ 226.67 × Lower_Sideline<br>
        &nbsp;&nbsp;&nbsp;&nbsp;+ 723.96 × Pitchside<br>
        &nbsp;&nbsp;&nbsp;&nbsp;+ 81.35 × Promotion<br>
        &nbsp;&nbsp;&nbsp;&nbsp;- 134.95 × (Last-Minute × Lower_Sideline)<br>
        &nbsp;&nbsp;&nbsp;&nbsp;- 613.24 × (Last-Minute × Pitchside)<br>
        &nbsp;&nbsp;&nbsp;&nbsp;+ 124.45 × (In-Between × Pitchside)
                </div>
            </div>
            
            <h3>Critical Interaction Effects</h3>
            <table>
                <thead>
                    <tr>
                        <th>Interaction Term</th>
                        <th>Coefficient</th>
                        <th>p-value</th>
                        <th>Interpretation</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Last-Minute × Pitchside</td>
                        <td class="highlight">-$613.24</td>
                        <td>< 0.001 ***</td>
                        <td>Pitchside loses 59% of value for last-minute buyers</td>
                    </tr>
                    <tr>
                        <td>Last-Minute × Lower Sideline</td>
                        <td class="highlight">-$134.95</td>
                        <td>< 0.001 ***</td>
                        <td>Extra discount on premium sideline seats</td>
                    </tr>
                    <tr>
                        <td>In-Between × Pitchside</td>
                        <td class="highlight">+$124.45</td>
                        <td>0.018 *</td>
                        <td>Sweet spot: 3-14 days before game</td>
                    </tr>
                </tbody>
            </table>
            
            <div class="note">
                <strong>Business Implication:</strong> Hold premium inventory (Pitchside, Lower Sideline) for early buyers. Target Pitchside sales to In-Between customers (3-14 days), not Last-Minute buyers.
            </div>
        </div>

        <!-- Revenue Initiatives -->
        <div class="section">
            <h2>💰 Strategic Revenue Initiatives</h2>
            
            <!-- Initiative 1 -->
            <div class="initiative-card">
                <div class="initiative-header">
                    <div class="initiative-title">Initiative 1: Last-Minute Discount Reduction</div>
                    <div class="initiative-impact">+${revenue_change_1:,.0f}</div>
                </div>
                
                <p><strong>Problem:</strong> Current discount of 38.9% exceeds industry standard (20-30%)</p>
                
                <div class="calculation-box">
                    <pre>Current seats:         {int(lastmin_seats):,}
× Current ATP:         × ${lastmin_atp:.2f}
= Current revenue:     = ${lastmin_revenue:,.2f}

Retained seats (90%):  {int(new_lastmin_seats):,}
× New ATP:             × ${target_lastmin_atp:.2f}
= New revenue:         = ${new_lastmin_revenue:,.2f}

Revenue change:        +${revenue_change_1:,.2f}</pre>
                </div>
                
                <div class="stat-badge">90% retention assumed</div>
                <div class="stat-badge">Break-even: 81.5%</div>
                <div class="stat-badge">Margin of safety: 8.5 pts</div>
            </div>
            
            <!-- Initiative 2 -->
            <div class="initiative-card">
                <div class="initiative-header">
                    <div class="initiative-title">Initiative 2: Customer Conversion Program</div>
                    <div class="initiative-impact">+${revenue_change_2:,.0f}</div>
                </div>
                
                <p><strong>Strategy:</strong> Move customers to earlier purchase timing through targeted campaigns</p>
                
                <h4 style="margin-top: 20px; color: #ffffff;">Scenario A: In-Between → Planner</h4>
                <div class="calculation-box">
                    <pre>In-Between seats:      {int(inbetween_seats):,}
× 20% converting:      × 0.20
= Seats converting:    = {int(seats_converting_a):,}
× ATP increase:        × ${atp_increase_a:.2f}
= Revenue gain:        = ${revenue_increase_a:,.2f}</pre>
                </div>
                
                <h4 style="margin-top: 15px; color: #ffffff;">Scenario B: Last-Minute → In-Between</h4>
                <div class="calculation-box">
                    <pre>Last-Minute seats:     {int(lastmin_seats):,}
× 20% converting:      × 0.20
= Seats converting:    = {int(seats_converting_b):,}
× ATP increase:        × ${atp_increase_b:.2f}
= Revenue gain:        = ${revenue_increase_b:,.2f}

Combined total:        ${revenue_change_2:,.2f}</pre>
                </div>
                
                <div class="stat-badge">Early-bird campaigns</div>
                <div class="stat-badge">Urgency messaging</div>
                <div class="stat-badge">Loyalty rewards</div>
            </div>
            
            <!-- Initiative 3 -->
            <div class="initiative-card">
                <div class="initiative-header">
                    <div class="initiative-title">Initiative 3: Halftime Seat Upgrades</div>
                    <div class="initiative-impact">+${revenue_change_3:,.0f}</div>
                </div>
                
                <p><strong>Concept:</strong> $10 in-game upgrades from Upper Level → Lower Level at halftime</p>
                
                <div class="calculation-box">
                    <pre>Avg attendance:        {int(avg_attendance):,} seats/game
× 79.8% eligible:      × 0.798
= Eligible Upper:      = {int(eligible_per_game):,} seats
× 33.3% take rate:     × 0.333
= Upgrades/game:       = {int(upgrades_per_game):,} upgrades
× $10 price:           × ${upgrade_price:.2f}
= Revenue/game:        = ${revenue_per_game:,.2f}
× 31 games:            × {total_games}
= Season revenue:      = ${revenue_change_3:,.2f}</pre>
                </div>
                
                <div class="stat-badge">Mobile app delivery</div>
                <div class="stat-badge">Halftime push notifications</div>
                <div class="stat-badge">Limited availability</div>
            </div>
        </div>

        <!-- Total Impact -->
        <div class="total-impact">
            <h2 style="color: #ffffff; border: none; margin-bottom: 20px;">📈 Total Revenue Impact</h2>
            <div style="font-size: 1.2em; color: rgba(255, 255, 255, 0.8);">Current Revenue: ${baseline_revenue:,.0f}</div>
            <div class="amount">+${total_increase:,.0f}</div>
            <div class="percentage">+{total_increase/baseline_revenue*100:.2f}%</div>
            <div style="font-size: 1.3em; margin-top: 20px; color: #ffffff;">New Revenue: ${new_revenue:,.0f}</div>
            <div style="font-size: 1em; margin-top: 10px; color: rgba(255, 255, 255, 0.7);">Per Game Increase: +${total_increase/total_games:,.0f}/game</div>
        </div>

        <!-- Summary Table -->
        <div class="section">
            <h2>📋 Initiative Summary</h2>
            <table>
                <thead>
                    <tr>
                        <th>Initiative</th>
                        <th>Revenue Impact</th>
                        <th>% of Total</th>
                        <th>Key Metric</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Last-Minute Discount Reduction</td>
                        <td class="highlight">${revenue_change_1:,.0f}</td>
                        <td>{revenue_change_1/baseline_revenue*100:.2f}%</td>
                        <td>90% retention</td>
                    </tr>
                    <tr>
                        <td>Customer Conversion Program</td>
                        <td class="highlight">${revenue_change_2:,.0f}</td>
                        <td>{revenue_change_2/baseline_revenue*100:.2f}%</td>
                        <td>20% convert each tier</td>
                    </tr>
                    <tr>
                        <td>Halftime Seat Upgrades</td>
                        <td class="highlight">${revenue_change_3:,.0f}</td>
                        <td>{revenue_change_3/baseline_revenue*100:.2f}%</td>
                        <td>79.8% eligible, 33% take</td>
                    </tr>
                    <tr style="background: rgba(0, 255, 136, 0.2); font-weight: 700;">
                        <td>TOTAL IMPACT</td>
                        <td class="highlight">${total_increase:,.0f}</td>
                        <td>{total_increase/baseline_revenue*100:.2f}%</td>
                        <td>${total_increase/total_games:,.0f}/game</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Data Visualizations -->
        <div class="section">
            <h2>📊 Data Visualizations</h2>
            <div class="image-grid">
"""

# Add all images
for fig_name, fig_title in figures:
    if fig_name in encoded_images:
        html_content += f"""
                <div class="image-card">
                    <img src="data:image/png;base64,{encoded_images[fig_name]}" alt="{fig_title}">
                    <div class="image-title">{fig_title}</div>
                </div>
"""

html_content += """
            </div>
        </div>

        <!-- Customer Type Breakdown -->
        <div class="section">
            <h2>👥 Customer Type Analysis</h2>
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-label">Planner (15+ days)</div>
                    <div class="metric-value">$""" + f"{planner_atp:.2f}" + """</div>
                    <div style="font-size: 0.9em; margin-top: 10px;">""" + f"{int(planner_seats):,} seats" + """</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">In-Between (3-14 days)</div>
                    <div class="metric-value">$""" + f"{inbetween_atp:.2f}" + """</div>
                    <div style="font-size: 0.9em; margin-top: 10px;">""" + f"{int(inbetween_seats):,} seats" + """</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Last-Minute (0-2 days)</div>
                    <div class="metric-value">$""" + f"{lastmin_atp:.2f}" + """</div>
                    <div style="font-size: 0.9em; margin-top: 10px;">""" + f"{int(lastmin_seats):,} seats" + """</div>
                </div>
            </div>
            
            <div class="note" style="margin-top: 20px;">
                <strong>Note:</strong> ATPs calculated using Total Revenue ÷ Total Seats methodology (not average of individual prices)
            </div>
        </div>

        <!-- Implementation Timeline -->
        <div class="section">
            <h2>⏱️ Implementation Timeline</h2>
            <table>
                <thead>
                    <tr>
                        <th>Phase</th>
                        <th>Timeline</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Phase 1</strong></td>
                        <td>Days 0-30</td>
                        <td>Implement Last-Minute pricing floor (25% max discount)</td>
                    </tr>
                    <tr>
                        <td><strong>Phase 2</strong></td>
                        <td>Days 30-60</td>
                        <td>Launch customer conversion campaigns (email, retargeting)</td>
                    </tr>
                    <tr>
                        <td><strong>Phase 3</strong></td>
                        <td>Days 60-90</td>
                        <td>Roll out halftime upgrade program via mobile app</td>
                    </tr>
                </tbody>
            </table>
            
            <div class="note">
                <strong>Risk Assessment:</strong> LOW - All initiatives have positive break-even margins with 4-8 percentage point safety buffers
            </div>
        </div>

        <footer>
            <p>SoCal Strykers Revenue Analysis Dashboard</p>
            <p>Statistical Model & Strategic Revenue Optimization</p>
            <p style="margin-top: 10px;">Colby Morris | colby.morris08@gmail.com</p>
            <p style="font-size: 0.9em;">San Diego Wave Questionnaire</p>
        </footer>
    </div>
</body>
</html>
"""

# Write HTML file
output_file = 'socal_strykers_dashboard.html'
with open(output_file, 'w') as f:
    f.write(html_content)

print(f"\n{'='*80}")
print(f"✅ Dashboard generated successfully!")
print(f"{'='*80}")
print(f"Output file: {output_file}")
print(f"\nTo view the dashboard:")
print(f"  1. Open {output_file} in your web browser")
print(f"  2. Or run: python -m http.server 8000")
print(f"     Then navigate to http://localhost:8000/{output_file}")
print(f"\n{'='*80}")
