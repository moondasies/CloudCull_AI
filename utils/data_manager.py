import pandas as pd
import random
from datetime import datetime, timedelta

def get_demo_apps():
    """
    Returns 15 realistic SaaS tools for TechVista Solutions.
    """
    tools = [
        {"name": "Slack", "dept": "Communication", "price": 1200, "seats": 150, "active": 142},
        {"name": "Notion", "dept": "Productivity", "price": 800, "seats": 80, "active": 65},
        {"name": "Zoom", "dept": "Communication", "price": 2500, "seats": 40, "active": 20},
        {"name": "Salesforce", "dept": "Sales", "price": 12000, "seats": 25, "active": 24},
        {"name": "Figma", "dept": "Design", "price": 3500, "seats": 12, "active": 10},
        {"name": "GitHub", "dept": "Engineering", "price": 1500, "seats": 45, "active": 45},
        {"name": "AWS", "dept": "Engineering", "price": 45000, "seats": 1, "active": 1},
        {"name": "Google Workspace", "dept": "IT", "price": 10000, "seats": 160, "active": 158},
        {"name": "Zendesk", "dept": "Support", "price": 6000, "seats": 15, "active": 12},
        {"name": "HubSpot", "dept": "Marketing", "price": 22000, "seats": 10, "active": 8},
        {"name": "Miro", "dept": "Productivity", "price": 1200, "seats": 30, "active": 10},
        {"name": "Loom", "dept": "Communication", "price": 800, "seats": 50, "active": 15},
        {"name": "Intercom", "dept": "Support", "price": 15000, "seats": 5, "active": 5},
        {"name": "Datadog", "dept": "Engineering", "price": 25000, "seats": 1, "active": 1},
        {"name": "Canva", "dept": "Marketing", "price": 900, "seats": 20, "active": 5}
    ]
    
    data = []
    for t in tools:
        # Calculate waste
        inactive_seats = t["seats"] - t["active"]
        waste_amt = (t["price"] / max(t["seats"], 1)) * inactive_seats
        
        status = "Active"
        if inactive_seats > (t["seats"] * 0.5):
            status = "Wasted"
        elif random.random() < 0.1:
            status = "Trial"
            
        data.append({
            "Tool Name": t["name"],
            "Department": t["dept"],
            "Monthly Cost (\u20b9)": t["price"],
            "Total Seats": t["seats"],
            "Active Users": t["active"],
            "Inactive Seats": inactive_seats,
            "Potential Savings (\u20b9)": round(waste_amt, 0),
            "Status": status,
            "Last Used": (datetime.now() - timedelta(days=random.randint(0, 45))).strftime("%Y-%m-%d"),
            "Renewal Date": (datetime.now() + timedelta(days=random.randint(2, 60))).strftime("%Y-%m-%d")
        })
        
    return pd.DataFrame(data)

def get_demo_metrics(df):
    total_spend = df["Monthly Cost (\u20b9)"].sum()
    active_apps = len(df)
    wasted_seats = df["Inactive Seats"].sum()
    potential_savings = df["Potential Savings (\u20b9)"].sum()
    
    return {
        "total_spend": total_spend,
        "active_apps": active_apps,
        "wasted_seats": wasted_seats,
        "potential_savings": potential_savings
    }
