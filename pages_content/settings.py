import streamlit as st
import os
from utils.db_utils import get_supabase
from utils.ai_utils import get_groq_client

def show_settings():
    st.markdown('<h1 class="header-title">Settings & Connectivity</h1>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle">Manage your account and verify API connections</p>', unsafe_allow_html=True)
    
    # Connection Status
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.write("### API Connection Status")
    
    # Supabase Check
    supabase = get_supabase()
    if supabase:
        st.success("\u2705 Supabase Cloud: Connected")
    else:
        st.error("\u274c Supabase Cloud: Disconnected")
        
    # Groq Check
    groq = get_groq_client()
    if groq:
        st.success("\u2705 Groq AI (Llama 3.3): Connected")
    else:
        st.error("\u274c Groq AI: Disconnected (DEMO MODE)")
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Profile Information
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.write("### User Profile")
    if st.session_state.user:
        st.write(f"**Email:** {st.session_state.user.email}")
        st.write(f"**User ID:** `{st.session_state.user.id}`")
    else:
        st.write("Auth Status: Not Authenticated")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Table Setup Helper
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.write("### Database Setup")
    st.info("If you haven't initialized your Supabase tables yet, copy the SQL from `supabase_schema.sql` in the project root and run it in your Supabase SQL Editor.")
    st.markdown('</div>', unsafe_allow_html=True)
