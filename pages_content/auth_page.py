import streamlit as st
from utils.db_utils import login_user, signup_user

def show_auth_page():
    st.markdown('<div style="text-align: center; margin-top: 50px;">', unsafe_allow_html=True)
    import os
    logo_path = os.path.join("assets", "logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, width=250)
    else:
        st.markdown('<h1 style="color: #0EA5E9; font-size: 42px; font-weight: 800;">CloudCull AI</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #6B7280; font-size: 18px;">Cull the waste, keep the value</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("Sign In", use_container_width=True):
                success, msg = login_user(email, password)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
        
        with tab2:
            s_email = st.text_input("Email", key="s_email")
            s_pass = st.text_input("Password", type="password", key="s_pass")
            if st.button("Create Account", use_container_width=True):
                success, msg = signup_user(s_email, s_pass)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
    
    st.markdown('<div style="text-align: center; margin-top: 40px; color: #9CA3AF; font-size: 14px;">"The best way to save money is to stop spending it on things you don\'t use."</div>', unsafe_allow_html=True)
