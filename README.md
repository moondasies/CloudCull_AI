# CloudCull AI - SaaS Spend Optimization

CloudCull AI is a professional, premium SaaS spend optimization dashboard built with **Streamlit**, **Supabase**, and **Groq AI**. It helps companies like "TechVista Solutions" identify wasted subscription costs, cull inactive seats, and manage their entire SaaS ecosystem from a single, beautiful interface.

## 🚀 Features

- **Supabase Authentication**: Secure login and signup (with a demo fallback for quick viewing).
- **Onboarding Pipeline**: Three methods to connect expense data (Mock Bank, CSV, Manual).
- **Executive Dashboard**: Real-time metrics on spend, active apps, and potential savings.
- **Waste Detector**: Core feature that identifies inactive seats (>30 days) and allows one-click "culling."
- **AI Optimizer Chat**: Branded chat interface powered by **Groq (Llama-3.3-70b)** for actionable financial advice.
- **Professional Reports**: Downloadable PDF summaries with spend breakdowns and savings trends.
- **Sleek UI**: Custom CSS overrides to provide a premium, modern B2B SaaS aesthetic.

## 🛠️ Tech Stack

- **Frontend/Backend**: Streamlit
- **Database/Auth**: Supabase
- **AI Engine**: Groq API
- **Charts**: Plotly
- **PDF Generation**: fpdf2

## 📁 Folder Structure

```text
CloudCull AI/
├── app.py                  # Main entry point & routing
├── pages_content/          # Individual page implementations
├── utils/                  # Core logic, DB, AI, and styles
├── .env.example            # Environment variable template
├── requirements.txt        # Python dependencies
└── README.md               # You are here
```

## ⚙️ Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd "CloudCull AI"
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   - Create a `.env` file from `.env.example`.
   - **Supabase**: Visit [Supabase](https://supabase.com/) to create a free project and get your URL and Project API Key (anon).
   - **Groq**: Visit [Groq Console](https://console.groq.com/) to get a free API key.

4. **Run the App**:
   ```bash
   streamlit run app.py
   ```

## 💰 Demo Mode
If you don't have API keys handy, the app will automatically enter **Demo Mode**, allowing you to explore the interface, see the realistic "TechVista Solutions" data (15 SaaS tools, ₹1,85,000 spend), and test the optimization features.

## 🌐 Deployment
Deploy instantly to **Streamlit Community Cloud**:
1. Push this code to GitHub.
2. Connect your repo to [Streamlit Cloud](https://share.streamlit.io/).
3. Add your secrets (`SUPABASE_URL`, `SUPABASE_KEY`, `GROQ_API_KEY`) to the Streamlit app settings.
