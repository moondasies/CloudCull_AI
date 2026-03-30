import streamlit as st
from utils.styles import apply_custom_styles
from utils.db_utils import init_db_session
from pages_content.auth_page import show_auth_page
from pages_content.onboarding_page import show_onboarding_page
from pages_content.dashboard import show_dashboard
from pages_content.apps_table import show_apps_table
from pages_content.waste_detector import show_waste_detector
from pages_content.ai_optimizer import show_ai_optimizer
from pages_content.alerts_reports import show_alerts, show_reports
from pages_content.settings import show_settings

# Page Configuration
st.set_page_config(
    page_title="CloudCull AI | SaaS Spend Optimization",
    page_icon="\u2601\ufe0f",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session & Styles
init_db_session()
apply_custom_styles()

# Navigation Logic
if st.session_state.user is None:
    show_auth_page()
elif not st.session_state.onboarded:
    show_onboarding_page()
else:
    # Sidebar Navigation
    with st.sidebar:
        import os
        logo_path = os.path.join("assets", "logo.png")
        if os.path.exists(logo_path):
            st.image(logo_path, use_container_width=True)
        else:
            st.markdown('<h1 style="color: #0EA5E9; font-size: 28px; font-weight: 800; margin-bottom: 20px;">CloudCull AI</h1>', unsafe_allow_html=True)
        
        page = st.radio(
            "Navigation",
            ["Dashboard", "Apps Inventory", "Waste Detector", "AI Optimizer", "Alerts", "Savings Report", "Settings"],
            index=0
        )
        
        st.markdown("---")
        if st.button("Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.onboarded = False
            st.session_state.data = None
            st.rerun()
            
        st.markdown('<div style="position: fixed; bottom: 20px; color: #6B7280; font-size: 12px;">\u00a9 2024 TechVista Solutions</div>', unsafe_allow_html=True)

    # Page Routing
    if page == "Dashboard":
        show_dashboard()
    elif page == "Apps Inventory":
        show_apps_table()
    elif page == "Waste Detector":
        show_waste_detector()
    elif page == "AI Optimizer":
        show_ai_optimizer()
    elif page == "Alerts":
        show_alerts()
    elif page == "Savings Report":
        show_reports()
    elif page == "Settings":
        show_settings()
