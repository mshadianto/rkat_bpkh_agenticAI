# app.py - Streamlit Frontend yang diperbaiki
import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px

# Configuration
API_BASE_URL = "http://localhost:8000"  # Update sesuai deployment

def main():
    st.set_page_config(
        page_title="RKAT BPKH",
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Authentication
    if 'user' not in st.session_state:
        login_page()
    else:
        main_app()

def login_page():
    st.title("🏛️ Sistem RKAT BPKH")
    st.subheader("Login ke Sistem")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", use_container_width=True):
            try:
                response = requests.post(f"{API_BASE_URL}/auth/login", 
                                       json={"username": username, "password": password})
                if response.status_code == 200:
                    st.session_state['user'] = response.json()['user']
                    st.session_state['token'] = response.json()['access_token']
                    st.rerun()
                else:
                    st.error("Username atau password salah")
            except:
                st.error("Tidak dapat terhubung ke server")

def main_app():
    # Sidebar Navigation
    with st.sidebar:
        st.image("https://via.placeholder.com/200x80/1f77b4/white?text=BPKH", width=200)
        st.write(f"**{st.session_state['user']['name']}**")
        st.write(f"Role: {st.session_state['user']['role']}")
        
        pages = {
            "📊 Dashboard": "dashboard",
            "📋 RKAT Management": "rkat", 
            "🔄 Workflow": "workflow",
            "🤖 AI Assistant": "ai"
        }
        
        selected = st.radio("Navigation", list(pages.keys()))
        page = pages[selected]
        
        if st.button("Logout"):
            del st.session_state['user']
            st.rerun()
    
    # Main Content
    if page == "dashboard":
        dashboard_page()
    elif page == "rkat":
        rkat_management_page()
    elif page == "workflow":
        workflow_page()
    elif page == "ai":
        ai_assistant_page()

def dashboard_page():
    st.title("📊 Dashboard RKAT BPKH")
    
    # Get metrics from API
    try:
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        response = requests.get(f"{API_BASE_URL}/dashboard/metrics", headers=headers)
        metrics = response.json()
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total RKAT", metrics['total_rkat'])
        with col2:
            st.metric("RKAT Disetujui", metrics['approved_rkat'])
        with col3:
            st.metric("Total Anggaran", f"Rp {metrics['total_budget']/1000000:.1f}M")
        with col4:
            st.metric("Rata-rata Approval", f"{metrics['avg_approval_days']:.1f} hari")
        
        # Status distribution chart
        st.subheader("Distribusi Status RKAT")
        status_df = pd.DataFrame(list(metrics['status_distribution'].items()), 
                               columns=['Status', 'Count'])
        fig = px.pie(status_df, values='Count', names='Status')
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")

def rkat_management_page():
    st.title("📋 Manajemen RKAT")
    
    # RKAT List
    try:
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        response = requests.get(f"{API_BASE_URL}/rkat/", headers=headers)
        rkat_list = response.json()
        
        if rkat_list:
            df = pd.DataFrame(rkat_list)
            st.dataframe(df[['id', 'judul', 'bidang', 'status', 'total_anggaran', 'progress_percentage']], 
                        use_container_width=True)
        else:
            st.info("Belum ada RKAT yang dibuat")
            
    except Exception as e:
        st.error(f"Error loading RKAT: {e}")

def workflow_page():
    st.title("🔄 Workflow RKAT")
    
    # Show workflow steps
    steps = [
        {"step": 1, "title": "Pengajuan RKAT", "desc": "Bidang mengajukan RKAT sesuai KUP & SBO"},
        {"step": 2, "title": "Review Audit Internal", "desc": "Audit Internal melakukan review kelayakan"},
        {"step": 3, "title": "Review Komite Dewan", "desc": "Komite Dewan Pengawas melakukan evaluasi"},
        {"step": 4, "title": "Persetujuan Dewan", "desc": "Dewan Pengawas memberikan persetujuan final"}
    ]
    
    for step in steps:
        with st.expander(f"Step {step['step']}: {step['title']}"):
            st.write(step['desc'])

def ai_assistant_page():
    st.title("🤖 AI Assistant RKAT")
    st.info("Fitur AI Assistant untuk membantu penyusunan RKAT akan segera hadir")

if __name__ == "__main__":
    main()
