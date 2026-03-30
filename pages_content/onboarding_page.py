import streamlit as st
import pandas as pd
from utils.data_manager import get_demo_apps
from utils.db_utils import save_apps_to_db

def show_onboarding_page():
    st.markdown('<div style="text-align: center; margin-bottom: 40px;">', unsafe_allow_html=True)
    st.markdown('<h2 style="font-weight: 800; font-size: 32px;">Connect your expenses in 60 seconds</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #6B7280;">CloudCull AI analyzes your SaaS footprint to find immediate savings.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            """
            <div class="premium-card" style="text-align: center; min-height: 300px;">
                <div style="font-size: 48px; margin-bottom: 20px;">\ud83c\udfe6</div>
                <h4 style="font-weight: 700;">Mock Bank</h4>
                <p style="color: #6B7280; font-size: 14px;">Instantly connect to TechVista's simulated finance account (Recommended).</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        if st.button("Connect Account", key="btn_bank", use_container_width=True):
            with st.spinner("Analyzing transactions..."):
                demo_data = get_demo_apps()
                success = save_apps_to_db(demo_data)
                if success:
                    st.session_state.data = demo_data
                    st.session_state.onboarded = True
                    st.success("Demo data synchronized with Supabase!")
                    st.rerun()
                else:
                    st.error("Failed to sync with Supabase. Check your connection.")
                
    with col2:
        st.markdown(
            """
            <div class="premium-card" style="text-align: center; min-height: 300px;">
                <div style="font-size: 48px; margin-bottom: 20px;">\ud83d\udcc4</div>
                <h4 style="font-weight: 700;">Upload CSV</h4>
                <p style="color: #6B7280; font-size: 14px;">Export your expense report from Ramp, Brex, or Excel and upload it here.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            try:
                user_df = pd.read_csv(uploaded_file)
                # Basic validation: ensure required columns exist or map them
                required_cols = ["Tool Name", "Department", "Monthly Cost (\u20b9)", "Total Seats", "Active Users", "Status", "Last Used", "Renewal Date"]
                if all(col in user_df.columns for col in required_cols):
                    if st.button("Process & Save Upload", use_container_width=True):
                        success = save_apps_to_db(user_df)
                        if success:
                            st.session_state.data = user_df
                            st.session_state.onboarded = True
                            st.success("Custom CSV synchronized!")
                            st.rerun()
                else:
                    st.error(f"CSV must contain columns: {', '.join(required_cols)}")
            except Exception as e:
                st.error(f"Error parsing CSV: {e}")
            
    with col3:
        st.markdown(
            """
            <div class="premium-card" style="text-align: center; min-height: 300px;">
                <div style="font-size: 48px; margin-bottom: 20px;">\u270d\ufe0f</div>
                <h4 style="font-weight: 700;">Add Manually</h4>
                <p style="color: #6B7280; font-size: 14px;">Manually list the tools your team uses one by one.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        if st.button("Get Started", key="btn_manual", use_container_width=True):
            # For manual, we'll just pre-fill with an empty template but for demo just use demo apps
            st.session_state.data = get_demo_apps()
            st.session_state.onboarded = True
            st.rerun()
