import streamlit as st
import pandas as pd
import plotly.express as px
from utils.pdf_generator import create_pdf_report
from utils.db_utils import load_user_apps

def show_alerts():
    st.markdown('<h1 class="header-title">Security & Cost Alerts</h1>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle">Real-time notifications about your SaaS ecosystem</p>', unsafe_allow_html=True)
    
    # Generic realistic alerts
    alerts = [
        {"type": "Cost Spike", "tool": "AWS", "msg": "Unexpected 15% increase in compute costs.", "time": "2 hours ago", "color": "#EF4444"},
        {"type": "Inactive Users", "tool": "Salesforce", "msg": "5 users haven't logged in for 45+ days.", "time": "1 day ago", "color": "#F59E0B"},
        {"type": "Renewal Ahead", "tool": "Zoom", "msg": "Annual renewal (₹2.4L) in 10 days.", "time": "2 days ago", "color": "#0EA5E9"},
    ]
    
    for alert in alerts:
        st.markdown(
            f"""
            <div class="premium-card" style="border-left: 5px solid {alert['color']};">
                <div style="display: flex; justify-content: space-between;">
                    <span style="font-weight: 700; color: {alert['color']};">{alert['type']}</span>
                    <span style="color: #9CA3AF; font-size: 12px;">{alert['time']}</span>
                </div>
                <h4 style="margin: 8px 0;">{alert['tool']}</h4>
                <p style="color: #6B7280; font-size: 14px;">{alert['msg']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button(f"Act on {alert['tool']} Alert", key=f"alert_{alert['tool']}"):
            st.info(f"Analysis triggered for {alert['tool']}...")

def show_reports():
    # Load Real Data
    df = load_user_apps()
    
    if df is None or df.empty:
        st.info("No data found to generate reports.")
        return
        
    st.markdown('<h1 class="header-title">Savings Report</h1>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle">Detailed breakdown of optimization trends and savings</p>', unsafe_allow_html=True)
    
    # Savings Breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.write("### Cumulative Savings (\u20b9)")
        # Demo trend data for time series (realistic for a growing company)
        history = pd.DataFrame({
            "Month": ["Jan", "Feb", "Mar", "Apr"],
            "Savings": [12000, 24000, 38000, 48000]
        })
        fig = px.line(history, x="Month", y="Savings", markers=True, color_discrete_sequence=['#10B981'])
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.write("### Spend Optimization Trend")
        total_spend = df["Monthly Cost (\u20b9)"].sum()
        potential_savings = df["Potential Savings (\u20b9)"].sum()
        trend = pd.DataFrame({
            "Category": ["Before Optimization", "Current Forecast"],
            "Spend": [total_spend + potential_savings, total_spend]
        })
        fig = px.bar(trend, x="Category", y="Spend", color="Category", 
                     color_discrete_map={"Before Optimization": "#EF4444", "Current Forecast": "#10B981"})
        fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), height=300)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.write("### Generate Executive Report")
    st.markdown("Download a professional PDF summary of your SaaS footprint and savings.")
    
    if st.button("Generate & Download PDF"):
        with st.spinner("Generating PDF from Supabase data..."):
            pdf_bytes = create_pdf_report(df)
            st.download_button(
                label="Click here to download PDF",
                data=pdf_bytes,
                file_name="CloudCull_Executive_Report.pdf",
                mime="application/pdf"
            )
    st.markdown('</div>', unsafe_allow_html=True)
