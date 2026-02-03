"""
SoCal Strykers Secondary Ticket Sales Analysis
Executive Dashboard for Data Innovation & Strategy Team
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from scipy import stats

# Page Configuration
st.set_page_config(
    page_title="SoCal Strykers | Ticket Analytics",
    page_icon="SS",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling - ALL TEXT WHITE ON DARK BACKGROUNDS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Global dark background */
    .main, .stApp {
        background: linear-gradient(135deg, #0a0e17 0%, #1a1f2e 100%);
        color: #ffffff !important;
    }
    
    /* ALL TEXT WHITE */
    h1, h2, h3, h4, h5, h6, p, span, div, label, .stMarkdown, .stText {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3 {
        font-weight: 700;
    }
    
    /* Hero header styling */
    .hero-header {
        background: linear-gradient(135deg, #1e2a3a 0%, #0a1628 100%);
        border-radius: 20px;
        padding: 40px;
        margin-bottom: 30px;
        border: 2px solid #00d4aa;
        text-align: center;
    }
    
    .team-name {
        font-size: 4.5rem !important;
        font-weight: 900 !important;
        color: #ffffff !important;
        text-transform: uppercase;
        letter-spacing: 8px;
        margin-bottom: 0;
        text-shadow: 0 0 40px rgba(0, 212, 170, 0.5);
    }
    
    .team-subtitle {
        font-size: 1.2rem;
        color: #00d4aa !important;
        text-transform: uppercase;
        letter-spacing: 4px;
        margin-top: 10px;
    }
    
    .dashboard-title {
        font-size: 1.5rem;
        color: #8892a0 !important;
        font-weight: 400;
        margin-top: 20px;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #1e2a3a 0%, #2d3748 100%);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #00d4aa !important;
        font-family: 'Inter', sans-serif;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #ffffff !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Insight and recommendation boxes */
    .insight-box {
        background: linear-gradient(135deg, #1a2332 0%, #243447 100%);
        border-left: 4px solid #00d4aa;
        padding: 16px 20px;
        border-radius: 0 12px 12px 0;
        margin: 16px 0;
        color: #ffffff !important;
    }
    
    .insight-box strong, .insight-box b {
        color: #00d4aa !important;
    }
    
    .recommendation-box {
        background: linear-gradient(135deg, #2d1f3d 0%, #3d2a52 100%);
        border-left: 4px solid #9f7aea;
        padding: 16px 20px;
        border-radius: 0 12px 12px 0;
        margin: 16px 0;
        color: #ffffff !important;
    }
    
    .recommendation-box strong, .recommendation-box b {
        color: #9f7aea !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1e2a3a;
        border-radius: 8px;
        padding: 10px 20px;
        color: #ffffff !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #00d4aa !important;
        color: #0a0e17 !important;
    }
    
    /* Metrics */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e2a3a 0%, #2d3748 100%);
        border-radius: 12px;
        padding: 16px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    div[data-testid="stMetric"] label {
        color: #ffffff !important;
    }
    
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #00d4aa !important;
    }
    
    div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: #8892a0 !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1628 0%, #1a1f2e 100%);
        color: #ffffff !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    /* Selectbox and multiselect */
    .stSelectbox label, .stMultiSelect label {
        color: #ffffff !important;
    }
    
    /* Stadium map container */
    .stadium-map-container {
        background: #ffffff;
        border-radius: 12px;
        padding: 10px;
        margin: 20px 0;
    }
    
    /* Table styling */
    .dataframe {
        color: #ffffff !important;
    }
    
    /* Links */
    a {
        color: #00d4aa !important;
    }
</style>
""", unsafe_allow_html=True)

# Load and process data
@st.cache_data
def load_data():
    # Try multiple possible file paths
    possible_paths = [
        'SoCal_Strykers_Secondary_Ticket_Sales_SecondaryTix_Transaction_Data.csv',  # User's local filename
        'SoCal_Strykers_Secondary_Ticket_Sales_Secondary_Tix_Transaction_Data_.csv',  # Alternate
        'SoCal Strykers Secondary Ticket Sales(Secondary Tix Transaction Data).csv',  # Original filename
        'data.csv',  # Simple fallback
        '/mnt/user-data/uploads/SoCal_Strykers_Secondary_Ticket_Sales_Secondary_Tix_Transaction_Data_.csv'  # Cloud environment
    ]
    
    df = None
    for path in possible_paths:
        try:
            df = pd.read_csv(path)
            break
        except FileNotFoundError:
            continue
    
    if df is None:
        st.error("❌ Could not find the CSV file. Please place your ticket data CSV in the same folder as this script and name it 'data.csv'")
        st.stop()
    df.columns = df.columns.str.strip()
    
    # Clean price columns
    df['Ticket_Price'] = df['Ticket Price'].replace(r'[\$,]', '', regex=True).astype(float)
    df['Total_Revenue'] = df['Total Block Price'].replace(r'[\$,]', '', regex=True).astype(float)
    
    # Parse dates
    df['Event_Date'] = pd.to_datetime(df['Event Date'], errors='coerce')
    df['Sale_Date'] = pd.to_datetime(df['Sale Date'], errors='coerce')
    df = df.dropna(subset=['Event_Date', 'Sale_Date'])
    
    # Calculate days before game
    df['Days_Before'] = (df['Event_Date'] - df['Sale_Date']).dt.days
    
    # Categorize sections
    def categorize_section(section):
        section_str = str(section).strip()
        if section_str.startswith('Upper'):
            return 'Upper Level GA'
        elif section_str.startswith('Lower'):
            letter = section_str.replace('Lower ', '').strip()
            if letter in ['M', 'N', 'O', 'L', 'P']:
                return 'Club'
            elif letter in ['H', 'J', 'K', 'G', 'F', 'Q', 'R', 'S', 'T']:
                return 'Lower Level GA'
            elif letter in ['A', 'B', 'C', 'D', 'E']:
                return 'Pitchside'
            return 'Lower Level GA'
        elif 'Pitchside' in section_str:
            return 'Pitchside'
        return 'Other'
    
    df['Seating_Category'] = df['Section'].apply(categorize_section)
    
    # Create timing buckets
    def timing_bucket(days):
        if days <= 0: return '0. Game Day'
        elif days <= 3: return '1. 1-3 Days'
        elif days <= 7: return '2. 4-7 Days'
        elif days <= 14: return '3. 8-14 Days'
        elif days <= 30: return '4. 15-30 Days'
        elif days <= 60: return '5. 31-60 Days'
        else: return '6. 60+ Days'
    
    df['Timing_Bucket'] = df['Days_Before'].apply(timing_bucket)
    
    # Add day of week and month
    df['Day_of_Week'] = df['Event_Date'].dt.day_name()
    df['Month'] = df['Event_Date'].dt.month_name()
    
    return df

# Load data
df = load_data()

# Primary pricing reference (from Exhibit A)
PRIMARY_PRICES = {
    'Upper Level GA': 75,
    'Lower Level GA': 125,
    'Club': 120,
    'Pitchside': 250
}

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <div style="font-size: 1.5rem; font-weight: 900; color: #ffffff; letter-spacing: 2px;">SOCAL</div>
        <div style="font-size: 2rem; font-weight: 900; color: #00d4aa; letter-spacing: 3px;">STRYKERS</div>
        <div style="font-size: 0.8rem; color: #8892a0; margin-top: 5px;">TICKET ANALYTICS</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### Data Overview")
    st.metric("Total Transactions", f"{len(df):,}")
    st.metric("Total Tickets Sold", f"{df['Number of Seats'].sum():,}")
    st.metric("Total Revenue", f"${df['Total_Revenue'].sum():,.0f}")
    st.metric("Avg Ticket Price", f"${df['Ticket_Price'].mean():.2f}")
    
    st.markdown("---")
    st.markdown("### Filters")
    
    selected_categories = st.multiselect(
        "Seating Category",
        options=sorted(df['Seating_Category'].unique()),
        default=sorted(df['Seating_Category'].unique())
    )
    
    selected_opponents = st.multiselect(
        "Opponents",
        options=sorted(df['Away Team'].unique()),
        default=sorted(df['Away Team'].unique())
    )

# Filter data
filtered_df = df[
    (df['Seating_Category'].isin(selected_categories)) &
    (df['Away Team'].isin(selected_opponents))
]

# Header - PROMINENT SOCAL STRYKERS BRANDING
st.markdown("""
<div class="hero-header">
    <div style="font-size: 0.9rem; color: #8892a0; margin-bottom: 10px;">Analysis by <strong style="color: #00d4aa;">Colby Morris</strong></div>
    <div class="team-name">SOCAL STRYKERS</div>
    <div class="team-subtitle">Stryker Stadium | Southern California</div>
    <div class="dashboard-title">Secondary Ticket Market Analysis | Executive Dashboard</div>
</div>
""", unsafe_allow_html=True)

# Key Metrics Row
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Overall ATP",
        f"${filtered_df['Ticket_Price'].mean():.2f}",
        f"{((filtered_df['Ticket_Price'].mean() / df['Ticket_Price'].mean()) - 1) * 100:+.1f}% vs all"
    )

with col2:
    st.metric(
        "Tickets Analyzed",
        f"{filtered_df['Number of Seats'].sum():,}",
        f"{len(filtered_df):,} transactions"
    )

with col3:
    st.metric(
        "Total Revenue",
        f"${filtered_df['Total_Revenue'].sum()/1000:.0f}K",
        "Secondary market"
    )

with col4:
    avg_days = filtered_df['Days_Before'].mean()
    st.metric(
        "Avg Purchase Lead",
        f"{avg_days:.0f} days",
        "Before event"
    )

with col5:
    top_opponent = filtered_df.groupby('Away Team')['Ticket_Price'].mean().idxmax()
    top_price = filtered_df.groupby('Away Team')['Ticket_Price'].mean().max()
    st.metric(
        "Highest ATP Opponent",
        f"{top_opponent}",
        f"${top_price:.0f} ATP"
    )

st.markdown("---")

# Main Content Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "ATP by Seating", 
    "Purchase Timing", 
    "Opponent Analysis",
    "Statistical Validation",
    "Revenue Opportunities",
    "Strategic Recommendations"
])

# ===========================================
# TAB 1: ATP BY SEATING AREA
# ===========================================
with tab1:
    st.markdown("## Average Ticket Price by Seating Area")
    st.markdown("*Comparing secondary market prices to primary pricing strategy*")
    
    # Stadium Map Section
    st.markdown("### Stryker Stadium Seating Map & Primary Pricing")
    
    # Try to load stadium map image
    import os
    stadium_map_paths = [
        'stadium_map.png',
        '/mnt/user-data/outputs/stadium_map.png'
    ]
    
    stadium_map_found = False
    for map_path in stadium_map_paths:
        if os.path.exists(map_path):
            st.image(map_path, use_container_width=True)
            stadium_map_found = True
            break
    
    if not stadium_map_found:
        st.markdown("""
        <div style="background: #1e2a3a; padding: 20px; border-radius: 12px; text-align: center;">
            <p style="color: #8892a0;">Stadium map not found. Place 'stadium_map.png' in the same folder as this script.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # ATP by Category Chart
        atp_by_cat = filtered_df.groupby('Seating_Category').agg({
            'Ticket_Price': ['mean', 'median', 'std', 'count'],
            'Number of Seats': 'sum'
        }).round(2)
        atp_by_cat.columns = ['ATP_Mean', 'ATP_Median', 'ATP_Std', 'Transactions', 'Tickets_Sold']
        atp_by_cat = atp_by_cat.reset_index()
        
        # Add primary price comparison
        atp_by_cat['Primary_Price'] = atp_by_cat['Seating_Category'].map(PRIMARY_PRICES)
        atp_by_cat['Premium_Pct'] = ((atp_by_cat['ATP_Mean'] - atp_by_cat['Primary_Price']) / atp_by_cat['Primary_Price'] * 100).round(1)
        
        fig = make_subplots(
            rows=1, cols=1,
            specs=[[{"secondary_y": True}]]
        )
        
        # Secondary ATP bars
        fig.add_trace(
            go.Bar(
                name='Secondary ATP',
                x=atp_by_cat['Seating_Category'],
                y=atp_by_cat['ATP_Mean'],
                marker_color='#00d4aa',
                text=[f'${x:.0f}' for x in atp_by_cat['ATP_Mean']],
                textposition='outside',
                textfont=dict(size=14, color='white')
            )
        )
        
        # Primary price line
        fig.add_trace(
            go.Scatter(
                name='Primary Price',
                x=atp_by_cat['Seating_Category'],
                y=atp_by_cat['Primary_Price'],
                mode='lines+markers',
                line=dict(color='#ff6b6b', width=3, dash='dash'),
                marker=dict(size=12, symbol='diamond')
            )
        )
        
        fig.update_layout(
            title=dict(text="Secondary vs Primary Pricing by Seating Category", font=dict(size=18, color='white')),
            xaxis_title="Seating Category",
            yaxis_title="Average Ticket Price ($)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=500,
            bargap=0.3,
            margin=dict(t=80, b=60, l=60, r=40),
            yaxis=dict(range=[0, atp_by_cat['ATP_Mean'].max() * 1.25])  # Add 25% headroom for labels
        )
        
        fig.update_xaxes(gridcolor='rgba(255,255,255,0.1)')
        fig.update_yaxes(gridcolor='rgba(255,255,255,0.1)')
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Secondary vs Primary Premium")
        for _, row in atp_by_cat.iterrows():
            premium = row['Premium_Pct']
            color = "#00d4aa" if premium > 0 else "#ff6b6b"
            arrow = "▲" if premium > 0 else "▼"
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1e2a3a 0%, #2d3748 100%); 
                        padding: 16px; border-radius: 12px; margin-bottom: 12px;
                        border-left: 4px solid {color};">
                <div style="font-weight: 600; color: white;">{arrow} {row['Seating_Category']}</div>
                <div style="color: {color}; font-size: 1.5rem; font-weight: 700;">{premium:+.1f}%</div>
                <div style="color: #8892a0; font-size: 0.8rem;">
                    Primary: ${row['Primary_Price']:.0f} → Secondary: ${row['ATP_Mean']:.0f}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box">
        <strong>Key Insight:</strong> Club seats show a <strong style="color: #00d4aa;">+69% premium</strong> 
        on the secondary market, indicating significant underpricing in primary sales. 
        Consider raising Club section prices by 30-40% to capture more value while still maintaining secondary market demand.
    </div>
    """, unsafe_allow_html=True)

# ===========================================
# TAB 2: PURCHASE TIMING
# ===========================================
with tab2:
    st.markdown("## ATP by Purchase Timing")
    st.markdown("*Understanding when fans buy and what they pay*")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # ATP by timing
        timing_stats = filtered_df.groupby('Timing_Bucket').agg({
            'Ticket_Price': 'mean',
            'Number of Seats': 'sum'
        }).reset_index()
        timing_stats.columns = ['Timing', 'ATP', 'Tickets']
        timing_stats['Pct_of_Total'] = (timing_stats['Tickets'] / timing_stats['Tickets'].sum() * 100).round(1)
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Bar(
                name='Average Ticket Price',
                x=timing_stats['Timing'],
                y=timing_stats['ATP'],
                marker_color='#00d4aa',
                text=[f'${x:.0f}' for x in timing_stats['ATP']],
                textposition='outside'
            ),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(
                name='% of Total Tickets',
                x=timing_stats['Timing'],
                y=timing_stats['Pct_of_Total'],
                mode='lines+markers+text',
                line=dict(color='#ffd93d', width=3),
                marker=dict(size=10),
                text=[f'{x:.0f}%' for x in timing_stats['Pct_of_Total']],
                textposition='top center'
            ),
            secondary_y=True
        )
        
        fig.update_layout(
            title="ATP and Sales Volume by Purchase Timing",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=450,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        fig.update_yaxes(title_text="Average Ticket Price ($)", secondary_y=False, gridcolor='rgba(255,255,255,0.1)')
        fig.update_yaxes(title_text="% of Total Tickets Sold", secondary_y=True, gridcolor='rgba(255,255,255,0.1)')
        fig.update_xaxes(gridcolor='rgba(255,255,255,0.1)')
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Timing Distribution")
        
        fig_pie = px.pie(
            timing_stats, 
            values='Tickets', 
            names='Timing',
            color_discrete_sequence=['#00d4aa', '#00a3ff', '#9f7aea', '#ffd93d', '#ff6b6b', '#ff9f43', '#a55eea']
        )
        fig_pie.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown("""
        <div class="insight-box">
            <strong>Key Finding:</strong><br>
            <strong style="color: #ffd93d;">33% of tickets</strong> are sold 
            within 3 days of the game, but at the <strong>lowest prices</strong>.
            <br><br>
            Early planners (60+ days out) pay <strong style="color: #00d4aa;">$152 avg</strong> 
            vs <strong style="color: #ff6b6b;">$64 avg</strong> for game-day purchases.
        </div>
        """, unsafe_allow_html=True)

# ===========================================
# TAB 3: OPPONENT ANALYSIS
# ===========================================
with tab3:
    st.markdown("## Opponent-Based Demand Analysis")
    st.markdown("*Identifying premium matchups and pricing opportunities*")
    
    # Opponent ATP analysis
    opponent_stats = filtered_df.groupby('Away Team').agg({
        'Ticket_Price': ['mean', 'median'],
        'Number of Seats': 'sum',
        'Days_Before': 'mean'
    }).round(2)
    opponent_stats.columns = ['ATP_Mean', 'ATP_Median', 'Tickets_Sold', 'Avg_Lead_Time']
    opponent_stats = opponent_stats.reset_index().sort_values('ATP_Mean', ascending=False)
    
    overall_atp = filtered_df['Ticket_Price'].mean()
    opponent_stats['Premium'] = ((opponent_stats['ATP_Mean'] - overall_atp) / overall_atp * 100).round(1)
    opponent_stats['Tier'] = opponent_stats['Premium'].apply(
        lambda x: 'Premium' if x > 10 else ('Standard' if x > -10 else 'Value')
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Horizontal bar chart
        fig = go.Figure()
        
        colors = ['#00d4aa' if x > overall_atp * 1.1 else ('#ffd93d' if x > overall_atp * 0.9 else '#ff6b6b') 
                  for x in opponent_stats['ATP_Mean']]
        
        fig.add_trace(go.Bar(
            y=opponent_stats['Away Team'],
            x=opponent_stats['ATP_Mean'],
            orientation='h',
            marker_color=colors,
            text=[f'${x:.0f}' for x in opponent_stats['ATP_Mean']],
            textposition='outside'
        ))
        
        # Add average line
        fig.add_vline(
            x=overall_atp, 
            line_dash="dash", 
            line_color="#ffffff",
            annotation_text=f"Avg: ${overall_atp:.0f}",
            annotation_position="top"
        )
        
        fig.update_layout(
            title="ATP by Opponent (Ranked)",
            xaxis_title="Average Ticket Price ($)",
            yaxis_title="",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=700,
            yaxis=dict(autorange="reversed")
        )
        
        fig.update_xaxes(gridcolor='rgba(255,255,255,0.1)')
        fig.update_yaxes(gridcolor='rgba(255,255,255,0.1)')
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Game Tier Classification")
        
        premium_games = opponent_stats[opponent_stats['Tier'] == 'Premium']
        standard_games = opponent_stats[opponent_stats['Tier'] == 'Standard']
        value_games = opponent_stats[opponent_stats['Tier'] == 'Value']
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a3a2e 0%, #2d4a3e 100%); 
                    padding: 16px; border-radius: 12px; margin-bottom: 12px;">
            <div style="color: #00d4aa; font-weight: 700; font-size: 1.2rem;">PREMIUM TIER</div>
            <div style="color: white; font-size: 0.9rem;">ATP > ${overall_atp * 1.1:.0f}</div>
            <div style="color: #8892a0; margin-top: 8px;">
                {', '.join(premium_games['Away Team'].tolist())}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #3a3a1a 0%, #4a4a2d 100%); 
                    padding: 16px; border-radius: 12px; margin-bottom: 12px;">
            <div style="color: #ffd93d; font-weight: 700; font-size: 1.2rem;">STANDARD TIER</div>
            <div style="color: white; font-size: 0.9rem;">ATP ${overall_atp * 0.9:.0f} - ${overall_atp * 1.1:.0f}</div>
            <div style="color: #8892a0; margin-top: 8px;">
                {', '.join(standard_games['Away Team'].tolist()[:5])}...
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #3a1a1a 0%, #4a2d2d 100%); 
                    padding: 16px; border-radius: 12px; margin-bottom: 12px;">
            <div style="color: #ff6b6b; font-weight: 700; font-size: 1.2rem;">VALUE TIER</div>
            <div style="color: white; font-size: 0.9rem;">ATP < ${overall_atp * 0.9:.0f}</div>
            <div style="color: #8892a0; margin-top: 8px;">
                {', '.join(value_games['Away Team'].tolist()[:5])}...
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="recommendation-box">
            <strong>Recommendation:</strong><br>
            Implement <strong>dynamic pricing tiers</strong>:
            <ul>
                <li>Premium: +25-40% over base</li>
                <li>Standard: Base price</li>
                <li>Value: -10-15% with promotions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ===========================================
# TAB 4: STATISTICAL VALIDATION
# ===========================================
with tab4:
    st.markdown("## Statistical Validation & Predictive Modeling")
    st.markdown("*Applying rigorous statistical methods to validate findings and build predictive models*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Hypothesis Testing: Seating Premium")
        st.markdown("**Question:** Is the Club section secondary premium statistically significant?")
        
        # T-test: Club vs Upper Level GA prices
        club_prices = filtered_df[filtered_df['Seating_Category'] == 'Club']['Ticket_Price']
        upper_prices = filtered_df[filtered_df['Seating_Category'] == 'Upper Level GA']['Ticket_Price']
        
        if len(club_prices) > 0 and len(upper_prices) > 0:
            t_stat, p_value = stats.ttest_ind(club_prices, upper_prices)
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1e2a3a 0%, #2d3748 100%); 
                        padding: 20px; border-radius: 12px; margin: 16px 0;">
                <div style="color: #ffffff; font-weight: 600; margin-bottom: 10px;">T-Test Results: Club vs Upper Level GA</div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="color: #8892a0;">Club Mean ATP:</span>
                    <span style="color: #00d4aa; font-weight: 600;">${club_prices.mean():.2f}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="color: #8892a0;">Upper Level Mean ATP:</span>
                    <span style="color: #00d4aa; font-weight: 600;">${upper_prices.mean():.2f}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="color: #8892a0;">T-Statistic:</span>
                    <span style="color: #ffffff; font-weight: 600;">{t_stat:.4f}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="color: #8892a0;">P-Value:</span>
                    <span style="color: {'#00d4aa' if p_value < 0.05 else '#ff6b6b'}; font-weight: 600;">{p_value:.2e}</span>
                </div>
                <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.1);">
                    <span style="color: #ffffff;">Conclusion: </span>
                    <span style="color: #00d4aa; font-weight: 600;">{'Statistically Significant (p < 0.05)' if p_value < 0.05 else 'Not Statistically Significant'}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # T-test: Early vs Late purchase timing
        st.markdown("**Question:** Do early planners pay significantly more than last-minute buyers?")
        
        early_prices = filtered_df[filtered_df['Days_Before'] > 30]['Ticket_Price']
        late_prices = filtered_df[filtered_df['Days_Before'] <= 3]['Ticket_Price']
        
        if len(early_prices) > 0 and len(late_prices) > 0:
            t_stat2, p_value2 = stats.ttest_ind(early_prices, late_prices)
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1e2a3a 0%, #2d3748 100%); 
                        padding: 20px; border-radius: 12px; margin: 16px 0;">
                <div style="color: #ffffff; font-weight: 600; margin-bottom: 10px;">T-Test Results: Early (30+ days) vs Late (0-3 days)</div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="color: #8892a0;">Early Planners Mean ATP:</span>
                    <span style="color: #00d4aa; font-weight: 600;">${early_prices.mean():.2f}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="color: #8892a0;">Last-Minute Mean ATP:</span>
                    <span style="color: #00d4aa; font-weight: 600;">${late_prices.mean():.2f}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="color: #8892a0;">P-Value:</span>
                    <span style="color: {'#00d4aa' if p_value2 < 0.05 else '#ff6b6b'}; font-weight: 600;">{p_value2:.2e}</span>
                </div>
                <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.1);">
                    <span style="color: #ffffff;">Conclusion: </span>
                    <span style="color: #00d4aa; font-weight: 600;">{'Statistically Significant (p < 0.05)' if p_value2 < 0.05 else 'Not Statistically Significant'}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Ticket Timing Classification Model")
        st.markdown("*Fan segmentation model for targeted marketing strategies*")
        
        # Create customer type classification
        def classify_buyer(days):
            if days <= 2:
                return 'Last-Minute'
            elif days > 14:
                return 'Planner'
            else:
                return 'In-Between'
        
        filtered_df_copy = filtered_df.copy()
        filtered_df_copy['Buyer_Type'] = filtered_df_copy['Days_Before'].apply(classify_buyer)
        
        buyer_dist = filtered_df_copy.groupby('Buyer_Type').agg({
            'Ticket_Price': ['mean', 'count'],
            'Number of Seats': 'sum'
        }).round(2)
        buyer_dist.columns = ['ATP', 'Transactions', 'Tickets']
        buyer_dist = buyer_dist.reset_index()
        
        # Order correctly
        buyer_order = ['Last-Minute', 'In-Between', 'Planner']
        buyer_dist['Buyer_Type'] = pd.Categorical(buyer_dist['Buyer_Type'], categories=buyer_order, ordered=True)
        buyer_dist = buyer_dist.sort_values('Buyer_Type')
        
        fig = px.bar(
            buyer_dist,
            x='Buyer_Type',
            y='Transactions',
            color='ATP',
            color_continuous_scale=['#ff6b6b', '#ffd93d', '#00d4aa'],
            text=[f'{x:,}' for x in buyer_dist['Transactions']]
        )
        
        fig.update_layout(
            title="Customer Segmentation by Purchase Timing",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=300,
            showlegend=False,
            margin=dict(t=60, b=40, l=40, r=40)
        )
        fig.update_traces(textposition='outside')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show breakdown
        st.markdown("**Segment Definitions:**")
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e2a3a 0%, #2d3748 100%); 
                    padding: 16px; border-radius: 12px;">
            <div style="margin-bottom: 8px;"><strong style="color: #ff6b6b;">Last-Minute:</strong> <span style="color: #8892a0;">Purchases within 2 days of game</span></div>
            <div style="margin-bottom: 8px;"><strong style="color: #ffd93d;">In-Between:</strong> <span style="color: #8892a0;">Purchases 3-14 days before game</span></div>
            <div><strong style="color: #00d4aa;">Planner:</strong> <span style="color: #8892a0;">Purchases 15+ days before game</span></div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # A/B Testing Recommendations
    st.markdown("### Recommended A/B Testing Framework")
    st.markdown("*Before full deployment of pricing changes, validate with controlled experiments*")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a3a2e 0%, #2d4a3e 100%); 
                    padding: 20px; border-radius: 12px; height: 100%;">
            <div style="color: #00d4aa; font-weight: 700; font-size: 1.1rem; margin-bottom: 12px;">Test 1: Club Pricing</div>
            <div style="color: #ffffff; font-size: 0.9rem; margin-bottom: 8px;"><strong>Hypothesis:</strong> Raising Club prices by 25% will not significantly reduce demand</div>
            <div style="color: #8892a0; font-size: 0.85rem; margin-bottom: 8px;"><strong>Control:</strong> Current $120/game pricing</div>
            <div style="color: #8892a0; font-size: 0.85rem; margin-bottom: 8px;"><strong>Treatment:</strong> $150/game pricing</div>
            <div style="color: #8892a0; font-size: 0.85rem;"><strong>Metric:</strong> Conversion rate, total revenue</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #3a3a1a 0%, #4a4a2d 100%); 
                    padding: 20px; border-radius: 12px; height: 100%;">
            <div style="color: #ffd93d; font-weight: 700; font-size: 1.1rem; margin-bottom: 12px;">Test 2: Early-Bird Incentive</div>
            <div style="color: #ffffff; font-size: 0.9rem; margin-bottom: 8px;"><strong>Hypothesis:</strong> 10% discount for 30+ day purchases will shift demand earlier</div>
            <div style="color: #8892a0; font-size: 0.85rem; margin-bottom: 8px;"><strong>Control:</strong> Standard pricing timeline</div>
            <div style="color: #8892a0; font-size: 0.85rem; margin-bottom: 8px;"><strong>Treatment:</strong> 10% early-bird discount</div>
            <div style="color: #8892a0; font-size: 0.85rem;"><strong>Metric:</strong> % sales 30+ days out</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #3a1a3a 0%, #4a2d4a 100%); 
                    padding: 20px; border-radius: 12px; height: 100%;">
            <div style="color: #9f7aea; font-weight: 700; font-size: 1.1rem; margin-bottom: 12px;">Test 3: Personalized Timing</div>
            <div style="color: #ffffff; font-size: 0.9rem; margin-bottom: 8px;"><strong>Hypothesis:</strong> Sending promos aligned with buyer type increases conversion</div>
            <div style="color: #8892a0; font-size: 0.85rem; margin-bottom: 8px;"><strong>Control:</strong> Generic email blast to all</div>
            <div style="color: #8892a0; font-size: 0.85rem; margin-bottom: 8px;"><strong>Treatment:</strong> Targeted emails by segment</div>
            <div style="color: #8892a0; font-size: 0.85rem;"><strong>Metric:</strong> Open rate, click rate, conversion</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box" style="margin-top: 20px;">
        <strong>Why A/B Test First?</strong><br>
        While immediate deployment of pricing changes captures revenue faster, A/B testing ensures 
        the model works in real-world conditions and builds organizational confidence in data-driven decisions.
        <br><br>
        <strong>Recommendation:</strong> Run Tests 1 and 2 for the first half of next season, then full deployment if successful.
    </div>
    """, unsafe_allow_html=True)

# ===========================================
# TAB 5: REVENUE OPPORTUNITIES
# ===========================================
with tab5:
    st.markdown("## Revenue Optimization Opportunities")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Day of Week Analysis")
        dow_stats = filtered_df.groupby('Day_of_Week').agg({
            'Ticket_Price': 'mean',
            'Number of Seats': 'sum'
        }).reset_index()
        
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_stats['Day_of_Week'] = pd.Categorical(dow_stats['Day_of_Week'], categories=day_order, ordered=True)
        dow_stats = dow_stats.sort_values('Day_of_Week')
        
        fig = px.bar(
            dow_stats,
            x='Day_of_Week',
            y='Ticket_Price',
            color='Ticket_Price',
            color_continuous_scale=['#ff6b6b', '#ffd93d', '#00d4aa'],
            text=[f'${x:.0f}' for x in dow_stats['Ticket_Price']]
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=350,
            showlegend=False,
            xaxis_title="",
            yaxis_title="Average Ticket Price ($)"
        )
        fig.update_traces(textposition='outside')
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class="insight-box">
            <strong>Insight:</strong> Sunday games command <strong style="color: #00d4aa;">170% higher ATP</strong> 
            than Friday games. Consider premium pricing for weekend matchups.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Monthly Trends")
        month_stats = filtered_df.groupby('Month').agg({
            'Ticket_Price': 'mean',
            'Number of Seats': 'sum'
        }).reset_index()
        
        fig = px.bar(
            month_stats,
            x='Month',
            y='Ticket_Price',
            color='Ticket_Price',
            color_continuous_scale=['#ff6b6b', '#ffd93d', '#00d4aa'],
            text=[f'${x:.0f}' for x in month_stats['Ticket_Price']]
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=350,
            showlegend=False,
            xaxis_title="",
            yaxis_title="Average Ticket Price ($)"
        )
        fig.update_traces(textposition='outside')
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class="insight-box">
            <strong>Insight:</strong> February shows <strong style="color: #00d4aa;">$192 ATP</strong> - 
            likely playoff push timing. Early season (November) shows lowest demand.
        </div>
        """, unsafe_allow_html=True)
    
    # Revenue Capture Analysis
    st.markdown("### Revenue Capture Analysis")
    st.markdown("*Estimated revenue left on table due to primary pricing gaps*")
    
    col1, col2, col3 = st.columns(3)
    
    # Calculate revenue gap
    revenue_analysis = []
    for cat in ['Club', 'Pitchside', 'Upper Level GA', 'Lower Level GA']:
        cat_data = filtered_df[filtered_df['Seating_Category'] == cat]
        if len(cat_data) > 0 and cat in PRIMARY_PRICES:
            secondary_atp = cat_data['Ticket_Price'].mean()
            primary_price = PRIMARY_PRICES[cat]
            tickets_sold = cat_data['Number of Seats'].sum()
            gap = max(0, secondary_atp - primary_price)
            lost_revenue = gap * tickets_sold
            revenue_analysis.append({
                'Category': cat,
                'Gap': gap,
                'Lost_Revenue': lost_revenue,
                'Tickets': tickets_sold
            })
    
    rev_df = pd.DataFrame(revenue_analysis)
    total_lost = rev_df['Lost_Revenue'].sum()
    
    with col1:
        st.metric("Club Section Gap", f"${rev_df[rev_df['Category']=='Club']['Gap'].values[0]:.0f}/ticket")
    with col2:
        st.metric("Pitchside Gap", f"${rev_df[rev_df['Category']=='Pitchside']['Gap'].values[0]:.0f}/ticket" if len(rev_df[rev_df['Category']=='Pitchside']) > 0 else "N/A")
    with col3:
        st.metric("💵 Total Est. Lost Revenue", f"${total_lost/1000:.0f}K", "Annually at current volume")

# ===========================================
# TAB 6: STRATEGIC RECOMMENDATIONS
# ===========================================
with tab6:
    st.markdown("## Strategic Recommendations")
    st.markdown("*Data-driven actions to grow revenue and improve fan experience*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Pricing Strategy
        
        <div class="recommendation-box">
            <strong>1. Implement Dynamic Tiered Pricing</strong>
            <ul>
                <li>Create 3 pricing tiers based on opponent demand</li>
                <li>Premium games (WSH, BAL, MEM, NY): +25-40%</li>
                <li>Standard games: Base price</li>
                <li>Value games (STL, SD, IND, MIL): Promotional pricing</li>
            </ul>
        </div>
        
        <div class="recommendation-box">
            <strong>2. Adjust Club Section Pricing</strong>
            <ul>
                <li>Current: $120/game primary</li>
                <li>Recommended: $160-$180/game</li>
                <li>Secondary market shows 69% premium - significant value capture opportunity</li>
            </ul>
        </div>
        
        <div class="recommendation-box">
            <strong>3. Day-of-Week Premium</strong>
            <ul>
                <li>Sunday games: +15-20% premium</li>
                <li>Friday games: Consider promotional discounts</li>
                <li>Weekend packages for families</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        ### 🎪 Fan Experience & Marketing
        
        <div class="recommendation-box">
            <strong>4. Early Purchase Incentives</strong>
            <ul>
                <li>33% of sales happen within 3 days - shift demand earlier</li>
                <li>Offer early-bird discounts (10-15% off 30+ days out)</li>
                <li>Exclusive experiences for early purchasers</li>
            </ul>
        </div>
        
        <div class="recommendation-box">
            <strong>5. Value Game Activation</strong>
            <ul>
                <li>Theme nights for low-demand opponents</li>
                <li>Group discount programs</li>
                <li>Youth soccer partnerships</li>
                <li>Community giveaway nights</li>
            </ul>
        </div>
        
        <div class="recommendation-box">
            <strong>6. Additional Data Needs</strong>
            <ul>
                <li>Primary sales data for comparison</li>
                <li>Fan demographics and preferences</li>
                <li>Concession/merchandise tie-in data</li>
                <li>Weather impact analysis</li>
                <li>Social media engagement metrics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Summary KPIs
    st.markdown("### Projected Impact Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Club Price Adjustment", "+$40-60/game", "Captures secondary premium")
    with col2:
        st.metric("Dynamic Pricing Lift", "+15-25%", "On premium games")
    with col3:
        st.metric("Est. Annual Revenue Gain", "$200-400K", "From pricing optimization")
    with col4:
        st.metric("Early Purchase Shift", "+20%", "Move to 30+ days out")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #8892a0; padding: 20px;">
    <p style="font-size: 1.1rem; color: #ffffff;">SoCal Strykers Ticket Analytics Dashboard</p>
    <p style="font-size: 0.9rem;">Analysis by <strong style="color: #00d4aa;">Colby Morris</strong></p>
    <p style="font-size: 0.8rem;">Based on secondary ticket transaction data | Prepared for Executive Review</p>
</div>
""", unsafe_allow_html=True)
