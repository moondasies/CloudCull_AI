import streamlit as st

def apply_custom_styles():
    st.markdown(
        """
        <style>
        /* Main page background */
        .stApp {
            background-color: #F9FAFB;
        }

        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #E5E7EB;
        }

        [data-testid="stSidebarNav"] {
            background-color: #FFFFFF;
        }

        /* Typography */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
        }

        /* Custom Card styling */
        .premium-card {
            background: white;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
            margin-bottom: 20px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .premium-card:hover {
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            border-color: #0EA5E9;
        }

        /* Header styling */
        .header-title {
            color: #111827;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        
        .header-subtitle {
            color: #6B7280;
            font-size: 16px;
            margin-bottom: 24px;
        }

        /* Metric Value styling */
        .metric-value {
            font-size: 32px;
            font-weight: 700;
            color: #111827;
            margin-top: 4px;
        }
        
        .metric-label {
            font-size: 14px;
            font-weight: 500;
            color: #6B7280;
            text-transform: uppercase;
            letter-spacing: 0.025em;
        }

        /* Buttons styling */
        div.stButton > button {
            background-color: #0EA5E9;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: 600;
            transition: background-color 0.2s ease;
        }
        
        div.stButton > button:hover {
            background-color: #0284C7;
            border: none;
            color: white;
        }

        /* Progress bars */
        .stProgress > div > div > div > div {
            background-color: #0EA5E9;
        }

        /* Hide default streamlit elements for cleaner look */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Chat styles */
        .chat-bubble {
            padding: 12px 16px;
            border-radius: 12px;
            margin-bottom: 12px;
            max-width: 80%;
        }
        
        .user-chat {
            background-color: #0EA5E9;
            color: white;
            align-self: flex-end;
            margin-left: auto;
        }
        
        .ai-chat {
            background-color: #F3F4F6;
            color: #1F2937;
            align-self: flex-start;
        }

        /* Table styling overrides */
        .stDataFrame {
            border: 1px solid #E5E7EB;
            border-radius: 8px;
        }

        /* Status colors */
        .status-active { color: #10B981; font-weight: 600; }
        .status-wasted { color: #EF4444; font-weight: 600; }
        .status-trial { color: #F59E0B; font-weight: 600; }
        </style>
        """,
        unsafe_allow_html=True
    )

def premium_card(label, value, delta=None, delta_color="normal"):
    delta_html = ""
    if delta:
        color = "#10B981" if delta_color == "normal" else "#EF4444"
        delta_html = f'<div style="color: {color}; font-size: 14px; font-weight: 600; margin-top: 4px;">{delta}</div>'
    
    st.markdown(
        f"""
        <div class="premium-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True
    )
