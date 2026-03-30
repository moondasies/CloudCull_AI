import streamlit as st
from utils.db_utils import load_user_apps

def show_apps_table():
    # Load Real Data from Supabase
    df = load_user_apps()
    
    if df is None or df.empty:
        st.info("No data found. Please complete the onboarding process first.")
        return
        
    st.markdown('<h1 class="header-title">Apps Inventory</h1>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle">Search, filter and manage TechVista\'s SaaS ecosystem</p>', unsafe_allow_html=True)
    
    # Search & Filter
    col1, col2 = st.columns([2, 1])
    search = col1.text_input("Search by Tool Name", placeholder="e.g., Notion, AWS...")
    dept = col2.selectbox("Filter by Department", ["All Departments"] + list(df["Department"].unique()))
    
    filtered_df = df.copy()
    if search:
        filtered_df = filtered_df[filtered_df["Tool Name"].str.contains(search, case=False)]
    if dept != "All Departments":
        filtered_df = filtered_df[filtered_df["Department"] == dept]
        
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.dataframe(
        filtered_df,
        column_config={
            "Monthly Cost (\u20b9)": st.column_config.NumberColumn(format="\u20b9 %d"),
            "Potential Savings (\u20b9)": st.column_config.NumberColumn(format="\u20b9 %d"),
            "Status": st.column_config.SelectboxColumn(
                options=["Active", "Wasted", "Trial"]
            ),
        },
        hide_index=True,
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Detail View Mock
    st.write("### Tool Insights")
    selected_tool = st.selectbox("Select a tool for details", df["Tool Name"].tolist())
    
    if selected_tool:
        tool_data = df[df["Tool Name"] == selected_tool].iloc[0]
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Total Seats", tool_data["Total Seats"])
            st.metric("Active Users", tool_data["Active Users"])
        with c2:
            st.metric("Inactive Seats", tool_data["Inactive Seats"])
            st.metric("Last Used", tool_data["Last Used"])
        with c3:
            st.metric("Potential Savings", f"\u20b9{tool_data['Potential Savings (\u20b9)']:,.0f}")
            if st.button(f"Go to {selected_tool} in Waste Detector"):
                st.info(f"Navigate to Waste Detector to manage {selected_tool} seats.")
        st.markdown('</div>', unsafe_allow_html=True)
