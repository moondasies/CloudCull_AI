import streamlit as st
from utils.ai_utils import get_ai_response
from utils.db_utils import load_user_apps

def show_ai_optimizer():
    # Load Real Data for Context
    df = load_user_apps()
    
    st.markdown('<h1 class="header-title">AI Optimizer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle">Chat with CloudCull AI to get actionable insights and recommendations based on your actual spend</p>', unsafe_allow_html=True)
    
    if df is None or df.empty:
        st.warning("Chat is limited: No SaaS tools detected in your database. Please onboard some tools first.")
        context_summary = "User has no SaaS tools connected yet."
    else:
        # Context Data for AI
        top_waste = df.sort_values(by="Potential Savings (\u20b9)", ascending=False).head(3)
        context_summary = f"User has {len(df)} total tools. Top 3 waste items: " + \
                          ", ".join([f"{r['Tool Name']} (\u20b9{r['Potential Savings (\u20b9)']:,.0f} potential savings)" for _, r in top_waste.iterrows()])
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm CloudCull AI. I've analyzed your Supabase SaaS inventory. How can I help you optimize your spend today?"}
        ]
        
    # Example Chips
    st.write("### Try asking:")
    cols = st.columns(3)
    if cols[0].button("What are our top 3 waste tools?"):
        st.session_state.messages.append({"role": "user", "content": "What are our top 3 waste tools?"})
        # Process and rerun
    if cols[1].button("Find redundant tools"):
        st.session_state.messages.append({"role": "user", "content": "Find redundant tools in our inventory"})
    if cols[2].button("How to reduce AWS costs?"):
        st.session_state.messages.append({"role": "user", "content": "Give me specific tips for reducing cloud hosting costs like AWS/Azure"})

    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Ask CloudCull AI (e.g., 'What can we cull this week?')"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("AI is thinking..."):
                response = get_ai_response(st.session_state.messages, context_data=context_summary)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
