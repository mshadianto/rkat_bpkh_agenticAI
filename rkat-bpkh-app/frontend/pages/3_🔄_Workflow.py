# frontend/pages/3_🔄_Workflow.py - Fixed version
import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Configuration
BACKEND_URL = "https://rkat-bpkh-agenticai.onrender.com"
REQUEST_TIMEOUT = 30

def get_auth_headers():
    """Get authorization headers with safe session state access"""
    token = (st.session_state.get('token') or 
             st.session_state.get('auth_token') or 
             st.session_state.get('access_token'))
    
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

def make_api_request(method, endpoint, **kwargs):
    """API request wrapper"""
    try:
        url = f"{BACKEND_URL}{endpoint}"
        kwargs['timeout'] = REQUEST_TIMEOUT
        
        if method.upper() == "GET":
            response = requests.get(url, **kwargs)
        elif method.upper() == "POST":
            response = requests.post(url, **kwargs)
        
        return response
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

def main():
    st.title("🔄 Workflow Management")
    
    # Check authentication
    if not st.session_state.get('authenticated', False):
        st.error("❌ Anda belum login. Silahkan login terlebih dahulu.")
        st.info("👈 Klik halaman utama untuk login")
        return
    
    # Navigation tabs
    tab1, tab2 = st.tabs([
        "📋 Status RKAT Saya", 
        "📊 Workflow Analytics"
    ])
    
    with tab1:
        show_my_rkat_status()
    
    with tab2:
        show_workflow_analytics()

def show_my_rkat_status():
    """Show current user's RKAT status with fixed data structure"""
    st.subheader("📋 Status RKAT Saya")
    
    # User info
    user = st.session_state.get('user', {})
    user_name = user.get('name', 'Unknown User')
    user_role = user.get('role', 'unknown')
    
    st.info(f"👤 **{user_name}** | 📋 Role: **{user_role}**")
    
    # Load RKAT data
    with st.spinner("Loading RKAT data..."):
        response = make_api_request("GET", "/rkat/", headers=get_auth_headers())
        
        if response and response.status_code == 200:
            try:
                rkat_list = response.json()
                
                if rkat_list:
                    # Process RKAT data with FIXED key mapping
                    processed_rkat = []
                    for rkat in rkat_list:
                        # FIXED: Map backend keys to expected frontend keys
                        processed_item = {
                            'id': rkat.get('id', 'N/A'),
                            'title': rkat.get('judul', 'No Title'),  # FIXED: judul -> title
                            'judul': rkat.get('judul', 'No Title'),  # Keep original for compatibility
                            'bidang': rkat.get('bidang', 'N/A'),
                            'status': rkat.get('status', 'draft'),
                            'progress_percentage': rkat.get('progress_percentage', 0),
                            'total_anggaran': rkat.get('total_anggaran', 0),
                            'pengaju': rkat.get('pengaju', rkat.get('pengaju_name', 'N/A')),
                            'tanggal_pengajuan': rkat.get('tanggal_pengajuan', 'N/A')
                        }
                        processed_rkat.append(processed_item)
                    
                    # Filter by user role/permission if needed
                    display_rkat = processed_rkat  # For now, show all
                    
                    if display_rkat:
                        # Display RKAT cards
                        for rkat in display_rkat:
                            with st.container():
                                col1, col2, col3 = st.columns([3, 1, 1])
                                
                                with col1:
                                    # FIXED: Use safe key access
                                    st.write(f"**{rkat.get('title', 'No Title')}**")
                                    st.write(f"📂 {rkat.get('bidang', 'N/A')} | 👤 {rkat.get('pengaju', 'N/A')}")
                                    
                                    # Status badge
                                    status = rkat.get('status', 'draft')
                                    status_color = get_status_color(status)
                                    st.markdown(f"<span style='background-color: {status_color}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px;'>{status.title()}</span>", unsafe_allow_html=True)
                                
                                with col2:
                                    progress = rkat.get('progress_percentage', 0)
                                    st.metric("Progress", f"{progress}%")
                                    st.progress(progress / 100)
                                
                                with col3:
                                    anggaran = rkat.get('total_anggaran', 0)
                                    st.metric("Anggaran", f"Rp {anggaran/1000000:.1f}M")
                                    
                                    # Action buttons
                                    if st.button(f"👁️ Detail", key=f"detail_{rkat.get('id')}"):
                                        show_rkat_detail(rkat.get('id'))
                                
                                st.divider()
                    
                    else:
                        st.info("📝 Tidak ada RKAT yang sesuai dengan role Anda")
                        
                else:
                    st.info("📝 Belum ada RKAT yang dibuat")
                    show_sample_workflow_data()
                    
            except Exception as e:
                st.error(f"Error processing RKAT data: {e}")
                st.code(str(e))  # Debug info
                show_sample_workflow_data()
                
        else:
            st.error("❌ Gagal memuat data RKAT")
            if response:
                st.code(f"Status: {response.status_code}")
            show_sample_workflow_data()

def show_workflow_analytics():
    """Show workflow analytics and statistics"""
    st.subheader("📊 Workflow Analytics")
    
    # Load workflow steps
    with st.spinner("Loading workflow analytics..."):
        # Get workflow steps
        workflow_response = make_api_request("GET", "/workflow/steps", headers=get_auth_headers())
        
        # Get RKAT data for analytics
        rkat_response = make_api_request("GET", "/rkat/", headers=get_auth_headers())
        
        if workflow_response and workflow_response.status_code == 200:
            try:
                workflow_steps = workflow_response.json()
                
                # Display workflow steps
                st.subheader("🔄 Alur Workflow RKAT BPKH")
                
                for i, step in enumerate(workflow_steps):
                    with st.expander(f"Step {step.get('step', i+1)}: {step.get('title', 'Unknown Step')}", expanded=True):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.write(f"**Deskripsi:** {step.get('description', 'No description')}")
                            st.write(f"**Penanggung Jawab:** {', '.join(step.get('roles', []))}")
                            if 'duration' in step:
                                st.write(f"**Estimasi Waktu:** {step.get('duration')}")
                        
                        with col2:
                            # Step visualization
                            st.markdown(f"""
                            <div style="
                                background: linear-gradient(45deg, #667eea, #764ba2);
                                color: white;
                                padding: 20px;
                                border-radius: 10px;
                                text-align: center;
                                font-size: 18px;
                                font-weight: bold;
                            ">
                                Step {step.get('step', i+1)}
                            </div>
                            """, unsafe_allow_html=True)
                
                # Analytics from RKAT data
                if rkat_response and rkat_response.status_code == 200:
                    try:
                        rkat_data = rkat_response.json()
                        show_workflow_statistics(rkat_data)
                    except:
                        show_sample_analytics()
                else:
                    show_sample_analytics()
                    
            except Exception as e:
                st.error(f"Error loading workflow steps: {e}")
                show_default_workflow_steps()
        else:
            st.error("❌ Gagal memuat workflow steps")
            show_default_workflow_steps()

def show_workflow_statistics(rkat_data):
    """Show workflow statistics from RKAT data"""
    if not rkat_data:
        show_sample_analytics()
        return
    
    st.subheader("📈 Statistik Workflow")
    
    # Process status distribution
    status_counts = {}
    for rkat in rkat_data:
        status = rkat.get('status', 'draft')
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total RKAT", len(rkat_data))
    
    with col2:
        in_progress = sum(1 for rkat in rkat_data if rkat.get('progress_percentage', 0) < 100)
        st.metric("In Progress", in_progress)
    
    with col3:
        completed = sum(1 for rkat in rkat_data if rkat.get('status') == 'approved')
        st.metric("Completed", completed)
    
    with col4:
        avg_progress = sum(rkat.get('progress_percentage', 0) for rkat in rkat_data) / len(rkat_data) if rkat_data else 0
        st.metric("Avg Progress", f"{avg_progress:.1f}%")
    
    # Status distribution chart
    if status_counts:
        fig = px.pie(
            values=list(status_counts.values()),
            names=list(status_counts.keys()),
            title="Distribusi Status RKAT"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Progress distribution
    if rkat_data:
        progress_data = [rkat.get('progress_percentage', 0) for rkat in rkat_data]
        fig = px.histogram(
            x=progress_data,
            bins=10,
            title="Distribusi Progress RKAT",
            labels={'x': 'Progress (%)', 'y': 'Jumlah RKAT'}
        )
        st.plotly_chart(fig, use_container_width=True)

def show_sample_workflow_data():
    """Show sample workflow data for demo"""
    st.info("📊 Menampilkan data sample untuk demo")
    
    sample_rkat = [
        {
            'id': 'RKAT-2026-001',
            'title': 'RKAT Audit Internal 2026',
            'bidang': 'Audit Internal',
            'status': 'pending_audit_review',
            'progress_percentage': 25,
            'total_anggaran': 2500000000,
            'pengaju': 'Misbah Taufiqurrohman'
        },
        {
            'id': 'RKAT-2026-002',
            'title': 'RKAT Teknologi Informasi 2026',
            'bidang': 'Teknologi Informasi', 
            'status': 'approved',
            'progress_percentage': 100,
            'total_anggaran': 5000000000,
            'pengaju': 'Emir Rio Krishna'
        }
    ]
    
    # Display sample cards
    for rkat in sample_rkat:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"**{rkat['title']}**")
                st.write(f"📂 {rkat['bidang']} | 👤 {rkat['pengaju']}")
                
                status = rkat['status']
                status_color = get_status_color(status)
                st.markdown(f"<span style='background-color: {status_color}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px;'>{status.title()}</span>", unsafe_allow_html=True)
            
            with col2:
                progress = rkat['progress_percentage']
                st.metric("Progress", f"{progress}%")
                st.progress(progress / 100)
            
            with col3:
                anggaran = rkat['total_anggaran']
                st.metric("Anggaran", f"Rp {anggaran/1000000:.1f}M")
            
            st.divider()

def show_sample_analytics():
    """Show sample analytics data"""
    st.subheader("📈 Statistik Workflow (Sample)")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total RKAT", 24)
    with col2:
        st.metric("In Progress", 10)
    with col3:
        st.metric("Completed", 14)
    with col4:
        st.metric("Avg Progress", "65.8%")

def show_default_workflow_steps():
    """Show default workflow steps if API fails"""
    st.subheader("🔄 Alur Workflow RKAT BPKH")
    
    default_steps = [
        {
            "step": 1,
            "title": "Pengajuan RKAT",
            "description": "Bidang mengajukan RKAT sesuai KUP & SBO",
            "roles": ["Bidang Pengaju"],
            "duration": "1-3 hari"
        },
        {
            "step": 2,
            "title": "Review Audit Internal",
            "description": "Audit Internal melakukan review kelayakan dan kesesuaian",
            "roles": ["Tim Audit Internal"],
            "duration": "5-7 hari"
        },
        {
            "step": 3,
            "title": "Review Komite Dewan",
            "description": "Komite Dewan Pengawas melakukan evaluasi strategis",
            "roles": ["Komite Dewan Pengawas"],
            "duration": "3-5 hari"
        },
        {
            "step": 4,
            "title": "Persetujuan Dewan",
            "description": "Dewan Pengawas memberikan persetujuan final",
            "roles": ["Dewan Pengawas"],
            "duration": "2-3 hari"
        }
    ]
    
    for step in default_steps:
        with st.expander(f"Step {step['step']}: {step['title']}", expanded=True):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Deskripsi:** {step['description']}")
                st.write(f"**Penanggung Jawab:** {', '.join(step['roles'])}")
                st.write(f"**Estimasi Waktu:** {step['duration']}")
            
            with col2:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(45deg, #667eea, #764ba2);
                    color: white;
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                    font-size: 18px;
                    font-weight: bold;
                ">
                    Step {step['step']}
                </div>
                """, unsafe_allow_html=True)

def get_status_color(status):
    """Get color for status badge"""
    colors = {
        'draft': '#6c757d',
        'pending_audit_review': '#ffc107',
        'audit_reviewed': '#17a2b8',
        'pending_komite_review': '#6f42c1',
        'komite_reviewed': '#6610f2',
        'pending_dewan_approval': '#fd7e14',
        'approved': '#28a745',
        'rejected': '#dc3545',
        'revision_needed': '#e83e8c'
    }
    return colors.get(status, '#6c757d')

def show_rkat_detail(rkat_id):
    """Show RKAT detail in modal/expander"""
    with st.expander(f"📄 Detail RKAT: {rkat_id}", expanded=True):
        response = make_api_request("GET", f"/rkat/{rkat_id}", headers=get_auth_headers())
        
        if response and response.status_code == 200:
            try:
                rkat_detail = response.json()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**ID:**", rkat_detail.get('id'))
                    st.write("**Judul:**", rkat_detail.get('judul'))
                    st.write("**Bidang:**", rkat_detail.get('bidang'))
                    st.write("**Program:**", rkat_detail.get('program', 'N/A'))
                
                with col2:
                    st.write("**Status:**", rkat_detail.get('status'))
                    st.write("**Progress:**", f"{rkat_detail.get('progress_percentage', 0)}%")
                    st.write("**Anggaran:**", f"Rp {rkat_detail.get('total_anggaran', 0):,.0f}")
                    st.write("**Pengaju:**", rkat_detail.get('pengaju', 'N/A'))
                
                # Progress bar
                progress = rkat_detail.get('progress_percentage', 0)
                st.progress(progress / 100)
                
                # Additional details
                if rkat_detail.get('latar_belakang'):
                    st.write("**Latar Belakang:**", rkat_detail.get('latar_belakang'))
                if rkat_detail.get('tujuan'):
                    st.write("**Tujuan:**", rkat_detail.get('tujuan'))
                
            except Exception as e:
                st.error(f"Error loading RKAT detail: {e}")
        else:
            st.error("❌ Gagal memuat detail RKAT")

if __name__ == "__main__":
    main()
