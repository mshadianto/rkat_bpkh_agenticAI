"""
HADIANT - AI Wedding Platform
Main Application Entry Point
Version: 1.0.0
"""

import streamlit as st
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Page config must be first
st.set_page_config(
    page_title="HADIANT - AI Wedding Platform",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import modules
from src.config import settings
from src.database import supabase_client
from src.components.sidebar import render_sidebar
from src.pages import dashboard, tenants, analytics, settings_page

# ============================================
# CUSTOM CSS
# ============================================
def load_css():
    st.markdown("""
    <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        
        /* Main background */
        .stApp {
            background: linear-gradient(180deg, #0f0f17 0%, #1a1a2e 100%);
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a2e 0%, #16162a 100%);
            border-right: 1px solid #2d2d3d;
        }
        
        [data-testid="stSidebar"] * {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        
        /* Logo */
        .logo {
            font-size: 28px;
            font-weight: 800;
            background: linear-gradient(135deg, #8b5cf6 0%, #d946ef 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
        }
        
        .tagline {
            color: #6b7280;
            font-size: 12px;
            margin-bottom: 30px;
        }
        
        /* Cards */
        .metric-card {
            background: linear-gradient(135deg, #1a1a2e 0%, #1f1f2e 100%);
            border: 1px solid #2d2d3d;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 16px;
        }
        
        /* Status badges */
        .badge {
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            display: inline-block;
        }
        
        .badge-active {
            background: rgba(16, 185, 129, 0.15);
            color: #10b981;
        }
        
        .badge-inactive {
            background: rgba(245, 158, 11, 0.15);
            color: #f59e0b;
        }
        
        .badge-starter {
            background: rgba(99, 102, 241, 0.15);
            color: #6366f1;
        }
        
        .badge-professional {
            background: rgba(139, 92, 246, 0.15);
            color: #8b5cf6;
        }
        
        .badge-business {
            background: rgba(217, 70, 239, 0.15);
            color: #d946ef;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: 600;
            font-family: 'Plus Jakarta Sans', sans-serif;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%);
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
        }
        
        /* Secondary button */
        .stButton > button[kind="secondary"] {
            background: #1f1f2e;
            border: 1px solid #2d2d3d;
        }
        
        /* Input fields */
        .stTextInput > div > div > input {
            background: #1f1f2e;
            border: 1px solid #2d2d3d;
            border-radius: 10px;
            color: white;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        
        .stSelectbox > div > div {
            background: #1f1f2e;
            border: 1px solid #2d2d3d;
            border-radius: 10px;
        }
        
        /* Tables */
        .stDataFrame {
            background: #1a1a2e;
            border-radius: 12px;
        }
        
        /* Metrics */
        [data-testid="stMetricValue"] {
            font-size: 28px;
            font-weight: 800;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        
        [data-testid="stMetricDelta"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: transparent;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: #1f1f2e;
            border: 1px solid #2d2d3d;
            border-radius: 10px;
            color: #9ca3af;
            padding: 10px 20px;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%) !important;
            border-color: transparent !important;
            color: white !important;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background: #1f1f2e;
            border: 1px solid #2d2d3d;
            border-radius: 10px;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Divider */
        hr {
            border-color: #2d2d3d;
        }
        
        /* Headers */
        h1, h2, h3 {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 700;
        }
        
        /* Plotly charts background */
        .js-plotly-plot {
            background: transparent !important;
        }
    </style>
    """, unsafe_allow_html=True)

# ============================================
# MAIN APP
# ============================================
def main():
    # Load CSS
    load_css()
    
    # Initialize session state
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = True  # For now, skip auth
    if "current_page" not in st.session_state:
        st.session_state.current_page = "dashboard"
    
    # Render sidebar and get selected page
    selected_page = render_sidebar()
    
    # Route to pages
    if selected_page == "dashboard":
        dashboard.render()
    elif selected_page == "tenants":
        tenants.render()
    elif selected_page == "analytics":
        analytics.render()
    elif selected_page == "settings":
        settings_page.render()
    
    # Footer
    st.divider()
    st.caption("© 2025 HADIANT - AI Wedding Platform by MS Hadianto")

if __name__ == "__main__":
    main()
