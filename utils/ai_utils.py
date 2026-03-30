import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@st.cache_resource
def get_groq_client():
    if GROQ_API_KEY:
        try:
            return Groq(api_key=GROQ_API_KEY)
        except:
            return None
    return None

def get_ai_response(messages, context_data=None):
    client = get_groq_client()
    if not client:
        return "AI Optimizer is currently in 'Demo Mode' because no GROQ_API_KEY was found. Please add a key to .env to enable live AI insights."

    # Prepare system prompt with context
    system_prompt = f"""
    You are CloudCull AI, a professional SaaS Spend Optimizer.
    Company: TechVista Solutions
    Current SaaS Data Highlights: {context_data if context_data else 'Daily SaaS spend analysis'}
    
    Your goal is to provide concise, professional, and actionable advice in Indian Rupees (₹).
    Focus on:
    1. Identifying duplicate tools.
    2. Suggesting 'culling' of inactive seats.
    3. Warning about upcoming renewals.
    
    Keep responses friendly but finance-focused. Use markdown for structure.
    """
    
    full_messages = [{"role": "system", "content": system_prompt}] + messages
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-specdec",
            messages=full_messages,
            temperature=0.7,
            max_tokens=1024,
            stream=False
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error connecting to Groq: {str(e)}"
