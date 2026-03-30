import streamlit as st
import plotly.express as px
from utils.styles import premium_card
from utils.data_manager import get_demo_metrics
from utils.db_utils import load_user_apps

def show_dashboard():
    # Load Real Data from Supabase
    df = load_user_apps()
    
    if df is None or df.empty:
        st.info("No data found. Please complete the onboarding process first.")
        return
        
    metrics = get_demo_metrics(df)
    
    st.markdown('<h1 class="header-title">TechVista Solutions Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle">Real-time SaaS spend and optimization overview</p>', unsafe_allow_html=True)
    
    # Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        premium_card("Monthly Spend", f"\u20b9{metrics['total_spend']:,.0f}", "+2.4%", "normal")
    with col2:
        premium_card("Active Apps", f"{metrics['active_apps']}", "0", "normal")
    with col3:
        premium_card("Wasted Seats", f"{metrics['wasted_seats']}", "-12", "danger")
    with col4:
        premium_card("Potential Savings", f"\u20b9{metrics['potential_savings']:,.0f}", "Priority", "danger")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.write("### Spend by Department")
        dept_spend = df.groupby("Department")["Monthly Cost (\u20b9)"].sum().reset_index()
        fig = px.pie(dept_spend, values="Monthly Cost (\u20b9)", names="Department", hole=0.6,
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(showlegend=True, margin=dict(t=0, b=0, l=0, r=0), height=300)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.write("### Top 5 Tools by Waste")
        waste_tools = df.sort_values(by="Potential Savings (\u20b9)", ascending=False).head(5)
        fig = px.bar(waste_tools, x="Tool Name", y="Potential Savings (\u20b9)", 
                     color_discrete_sequence=['#0EA5E9'])
        fig.update_layout(margin=dict(t=20, b=0, l=0, r=0), height=300, 
                          xaxis_title=None, yaxis_title="Potential Savings (\u20b9)")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Renewals
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.write("### Upcoming Renewals")
    renewals = df.sort_values(by="Renewal Date").head(3)
    for _, row in renewals.iterrows():
        col_a, col_b, col_c = st.columns([2, 2, 1])
        col_a.write(f"**{row['Tool Name']}**")
        col_b.write(f"Next Bill: {row['Renewal Date']}")
        col_c.write(f"\u20b9{row['Monthly Cost (\u20b9)']:,.0f}")
        st.divider()
    
    if st.button("Analyze All Waste \u2192"):
        st.info("Directing to Waste Detector...")
    st.markdown('</div>', unsafe_allow_html=True)
