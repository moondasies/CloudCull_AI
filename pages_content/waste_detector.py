import streamlit as st
import pandas as pd
from utils.db_utils import update_db_record, load_user_apps

def show_waste_detector():
    # Load fresh data from DB if possible
    df = load_user_apps()
    if df is None or df.empty:
        st.info("No data found. Please complete the onboarding process first.")
        return
        
    st.markdown('<h1 class="header-title">Waste Detector</h1>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle">Intelligent detection of inactive seats, duplicate tools, and expiring trials</p>', unsafe_allow_html=True)
    
    # Filter for waste
    waste_df = df[df["Inactive Seats"] > 0].sort_values(by="Potential Savings (\u20b9)", ascending=False)
    
    if waste_df.empty:
        st.success("No wasted seats detected! Great job, TechVista Solutions.")
    else:
        st.markdown(f'<div class="premium-card">', unsafe_allow_html=True)
        st.write(f"### {len(waste_df)} Tools with Significant Waste")
        
        for idx, row in waste_df.iterrows():
            with st.expander(f"\u26a0\ufe0f {row['Tool Name']} - \u20b9{row['Potential Savings (\u20b9)']:,.0f} Wasted", expanded=True):
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    st.write(f"**Inactive Seats:** {row['Inactive Seats']}")
                    st.write(f"**Active Users:** {row['Active Users']}")
                with col2:
                    st.write(f"**Monthly Cost:** \u20b9{row['Monthly Cost (\u20b9)']:,.0f}")
                    st.write(f"**Potential Savings:** \u20b9{row['Potential Savings (\u20b9)']:,.0f}")
                with col3:
                    if st.button(f"Cull {row['Tool Name']} Seats", key=f"cull_{row['Tool Name']}"):
                        with st.spinner("Processing optimization in Supabase..."):
                            # Logic to update database
                            new_total_seats = int(row['Active Users'])
                            success = update_db_record(row['Tool Name'], {
                                "total_seats": new_total_seats,
                                "status": "Active"
                            })
                            if success:
                                st.success(f"Optimized {row['Tool Name']}! Savings realized.")
                                st.session_state.data = load_user_apps()
                                st.rerun()
                            else:
                                st.error("Failed to update database.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Secondary Waste Types
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.write("### Trial Optimization")
    trials = df[df["Status"] == "Trial"]
    if trials.empty:
        st.write("No active trials found.")
    else:
        for _, row in trials.iterrows():
            st.warning(f"**{row['Tool Name']}** trial expires soon. Estimated cost: \u20b9{row['Monthly Cost (\u20b9)']:,.1f}")
            if st.button(f"Cancel {row['Tool Name']} Trial", key=f"cancel_{row['Tool Name']}"):
                st.info(f"Cancellation request sent for {row['Tool Name']}.")
    st.markdown('</div>', unsafe_allow_html=True)
