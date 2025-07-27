import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.api_client import APIClient
from components.auth import AuthComponent
from config.settings import settings

# Page config
st.set_page_config(
    page_title="Dashboard - RKAT BPKH",
    page_icon="🏠",
    layout="wide"
)

# Initialize API client
api_client = APIClient(settings.API_BASE_URL)
auth = AuthComponent(api_client)

# Check authentication
if not auth.is_authenticated():
    st.title("🏛️ RKAT BPKH Management System")
    st.subheader("Selamat datang di Sistem Manajemen Rencana Kerja dan Anggaran Tahunan BPKH")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        auth.login_form()
    
    st.stop()

# Set API token
api_client.set_auth_token(st.session_state.auth_token)

# Main Dashboard
st.title("🏠 Dashboard RKAT BPKH")

# User info header
user_info = auth.get_user_info()
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.write(f"**Selamat datang, {user_info.get('full_name', 'User')}**")
    st.write(f"Role: {settings.USER_ROLES.get(user_info.get('role', ''), 'Unknown')}")

with col3:
    if st.button("Logout"):
        auth.logout()

# Get dashboard metrics
with st.spinner("Memuat data dashboard..."):
    response = api_client.get_dashboard_metrics()
    
    if response["success"]:
        metrics = response["data"]
        
        # Key Metrics Cards
        st.subheader("📊 Metrics Utama")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_rkats = metrics["performance_metrics"]["total_rkats"]
            st.metric("Total RKAT", total_rkats, delta=None)
        
        with col2:
            approved_rkats = metrics["performance_metrics"]["approved_rkats"]
            st.metric("RKAT Disetujui", approved_rkats, delta=None)
        
        with col3:
            total_budget = metrics["budget_summary"]["total_budget"]
            st.metric("Total Anggaran", f"Rp {total_budget/1e9:.1f}M", delta=None)
        
        with col4:
            avg_approval_time = metrics["performance_metrics"]["avg_approval_time_days"]
            st.metric("Rata-rata Waktu Approval", f"{avg_approval_time:.1f} hari", delta=None)
        
        # Charts Section
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Distribusi Status RKAT")
            
            status_data = metrics["status_distribution"]
            if status_data:
                # Translate status to Indonesian
                status_labels = {k: settings.RKAT_STATUS.get(k, k) for k in status_data.keys()}
                
                fig = px.pie(
                    values=list(status_data.values()),
                    names=[status_labels[k] for k in status_data.keys()],
                    title="Status RKAT",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Tidak ada data RKAT")
        
        with col2:
            st.subheader("💰 Breakdown Anggaran")
            
            budget_data = metrics["budget_summary"]
            budget_df = pd.DataFrame({
                'Kategori': ['Operasional', 'Personel'],
                'Anggaran': [budget_data["operational_budget"], budget_data["personnel_budget"]]
            })
            
            if budget_df['Anggaran'].sum() > 0:
                fig = px.bar(
                    budget_df, 
                    x='Kategori', 
                    y='Anggaran',
                    title="Distribusi Anggaran",
                    color='Kategori',
                    color_discrete_sequence=['#1f77b4', '#ff7f0e']
                )
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Tidak ada data anggaran")
        
        # Compliance Scores
        st.subheader("✅ Skor Kepatuhan Rata-rata")
        
        col1, col2 = st.columns(2)
        
        with col1:
            kup_score = budget_data["avg_kup_compliance"]
            st.metric("Kepatuhan KUP", f"{kup_score:.1f}%")
            st.progress(kup_score / 100)
        
        with col2:
            sbo_score = budget_data["avg_sbo_compliance"] 
            st.metric("Kepatuhan SBO", f"{sbo_score:.1f}%")
            st.progress(sbo_score / 100)
        
        # Recent Activities
        st.subheader("🕒 Aktivitas Terbaru")
        
        recent_activities = metrics["recent_activities"]
        if recent_activities:
            activity_df = pd.DataFrame(recent_activities)
            activity_df['created_at'] = pd.to_datetime(activity_df['created_at'])
            activity_df['Status'] = activity_df['status'].map(settings.RKAT_STATUS)
            
            st.dataframe(
                activity_df[['title', 'Status', 'creator', 'created_at']],
                column_config={
                    'title': st.column_config.TextColumn('Judul RKAT'),
                    'Status': st.column_config.TextColumn('Status'),
                    'creator': st.column_config.TextColumn('Pembuat'),
                    'created_at': st.column_config.DatetimeColumn('Tanggal Dibuat')
                },
                use_container_width=True
            )
        else:
            st.info("Tidak ada aktivitas terbaru")
    
    else:
        st.error(f"Gagal memuat data dashboard: {response.get('error', 'Unknown error')}")

# Quick Actions based on role
st.subheader("⚡ Aksi Cepat")

col1, col2, col3 = st.columns(3)

with col1:
    if auth.can_create_rkat():
        if st.button("📝 Buat RKAT Baru", use_container_width=True):
            st.switch_page("pages/2_📊_RKAT_Management.py")

with col2:
    if auth.can_review_rkat():
        if st.button("👀 Review RKAT", use_container_width=True):
            st.switch_page("pages/3_🔄_Workflow.py")

with col3:
    if st.button("💡 AI Assistant", use_container_width=True):
        st.switch_page("pages/4_💡_AI_Assistant.py")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        RKAT BPKH Management System v1.0 | 
        Badan Pengelola Keuangan Haji | 
        © 2025
    </div>
    """, 
    unsafe_allow_html=True
)