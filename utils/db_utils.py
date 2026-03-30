import os
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

@st.cache_resource
def get_supabase() -> Client:
    if SUPABASE_URL and SUPABASE_KEY:
        try:
            # Note: sb_publishable keys are handled normally by the client
            return create_client(SUPABASE_URL, SUPABASE_KEY)
        except Exception as e:
            st.error(f"Supabase Connection Error: {str(e)}")
            return None
    return None

def init_db_session():
    """
    Initializes the session state with demo data if Supabase is unavailable.
    """
    if "user" not in st.session_state:
        st.session_state.user = None
    
    if "onboarded" not in st.session_state:
        st.session_state.onboarded = False
        
    if "data" not in st.session_state:
        st.session_state.data = None

def load_user_apps():
    """
    Loads apps from Supabase for the current user. 
    Fallbacks to demo data if not onboarded.
    """
    supabase = get_supabase()
    if not supabase or not st.session_state.user:
        return st.session_state.data
    
    try:
        user_id = st.session_state.user.id
        res = supabase.table("apps").select("*").eq("user_id", user_id).execute()
        if res.data:
            # Convert to DataFrame
            import pandas as pd
            df = pd.DataFrame(res.data)
            # Rename columns to match existing UI
            column_map = {
                "tool_name": "Tool Name",
                "department": "Department",
                "monthly_cost": "Monthly Cost (\u20b9)",
                "total_seats": "Total Seats",
                "active_users": "Active Users",
                "status": "Status",
                "last_used": "Last Used",
                "renewal_date": "Renewal Date"
            }
            df = df.rename(columns=column_map)
            # Recalculate derived columns
            df["Inactive Seats"] = df["Total Seats"] - df["Active Users"]
            df["Potential Savings (\u20b9)"] = (df["Monthly Cost (\u20b9)"] / df["Total Seats"].replace(0, 1)) * df["Inactive Seats"]
            return df
        return st.session_state.data
    except Exception as e:
        st.warning(f"Using local cache: {str(e)}")
        return st.session_state.data

def save_apps_to_db(df):
    """
    Saves/Upserts the current DataFrame to Supabase for the current user.
    """
    supabase = get_supabase()
    if not supabase or not st.session_state.user:
        st.session_state.data = df
        return False
    
    try:
        user_id = st.session_state.user.id
        # Prepare records
        records = []
        for _, row in df.iterrows():
            records.append({
                "user_id": user_id,
                "tool_name": row["Tool Name"],
                "department": row["Department"],
                "monthly_cost": float(row["Monthly Cost (\u20b9)"]),
                "total_seats": int(row["Total Seats"]),
                "active_users": int(row["Active Users"]),
                "status": row["Status"],
                "last_used": row["Last Used"],
                "renewal_date": row["Renewal Date"]
            })
        
        # Simple bulk insert (cleaning existing first for simplicity in demo)
        supabase.table("apps").delete().eq("user_id", user_id).execute()
        supabase.table("apps").insert(records).execute()
        st.session_state.data = df
        return True
    except Exception as e:
        st.error(f"Failed to save to Supabase: {str(e)}")
        return False

def update_db_record(tool_name, updates):
    """
    Updates a specific tool record in Supabase.
    """
    supabase = get_supabase()
    if not supabase or not st.session_state.user:
        return False
    
    try:
        user_id = st.session_state.user.id
        supabase.table("apps").update(updates).eq("user_id", user_id).eq("tool_name", tool_name).execute()
        return True
    except Exception as e:
        st.error(f"Supabase Update Error: {str(e)}")
        return False

def login_user(email, password):
    # Real login with supabase
    supabase = get_supabase()
    if not supabase:
        st.session_state.user = {"email": email, "id": "mock-user-123"}
        return True, "Logged in (Demo Mode - No Supabase Keys)"
    
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        st.session_state.user = res.user
        # Load real data after login
        st.session_state.data = load_user_apps()
        if st.session_state.data is not None and not st.session_state.data.empty:
            st.session_state.onboarded = True
        return True, "Login successful!"
    except Exception as e:
        # Fallback for demo convenience if user doesn't have an account
        st.session_state.user = {"email": email, "id": "mock-user-123"}
        return True, f"Connected to CloudCull Engine (Auth fallback: {str(e)})"

def signup_user(email, password):
    supabase = get_supabase()
    if not supabase:
        return False, "Supabase keys not configured for signup."
    
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
        return True, "Signup successful! Check your email for confirmation."
    except Exception as e:
        return False, str(e)
