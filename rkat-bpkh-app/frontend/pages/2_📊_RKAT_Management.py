# frontend/pages/2_📊_RKAT_Management.py - Fixed URLs
import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import json

# Configuration - FIXED URLs to match backend
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
    """API request wrapper with proper error handling"""
    try:
        # FIXED: Remove /api prefix to match backend endpoints
        url = f"{BACKEND_URL}{endpoint}"  # Direct endpoint, no /api prefix
        kwargs['timeout'] = REQUEST_TIMEOUT
        
        st.write(f"🔄 Making request to: {url}")  # Debug info
        
        if method.upper() == "GET":
            response = requests.get(url, **kwargs)
        elif method.upper() == "POST":
            response = requests.post(url, **kwargs)
        elif method.upper() == "PUT":
            response = requests.put(url, **kwargs)
        elif method.upper() == "DELETE":
            response = requests.delete(url, **kwargs)
        
        st.write(f"📡 Response status: {response.status_code}")  # Debug info
        return response
        
    except requests.exceptions.RequestException as e:
        st.error(f"❌ API Error: {str(e)}")
        return None

def main():
    st.title("📊 Manajemen RKAT")
    
    # Check authentication
    if not st.session_state.get('authenticated', False):
        st.error("❌ Anda belum login. Silahkan login terlebih dahulu.")
        st.info("👈 Klik halaman utama untuk login")
        return
    
    # Debug info
    with st.expander("🔧 Debug Info"):
        st.write("Backend URL:", BACKEND_URL)
        st.write("Auth headers:", bool(get_auth_headers()))
        st.write("Session authenticated:", st.session_state.get('authenticated'))
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Daftar RKAT", 
        "➕ Buat RKAT", 
        "✏️ Edit RKAT", 
        "📄 Detail RKAT"
    ])
    
    with tab1:
        show_rkat_list()
    
    with tab2:
        show_create_rkat()
    
    with tab3:
        show_edit_rkat()
    
    with tab4:
        show_rkat_detail()

def show_rkat_list():
    """Show RKAT list with fixed endpoint"""
    st.subheader("📋 Daftar RKAT")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        search_term = st.text_input("🔍 Cari RKAT", placeholder="Masukkan kata kunci...")
    with col2:
        status_filter = st.selectbox("Status", ["Semua", "Draft", "Pending Review", "Approved"])
    with col3:
        bidang_filter = st.selectbox("Bidang", ["Semua", "Audit Internal", "Teknologi Informasi", "Akuntansi"])
    
    # Load RKAT data
    with st.spinner("Loading RKAT data..."):
        # FIXED: Use correct endpoint that matches backend
        response = make_api_request("GET", "/rkat/", headers=get_auth_headers())
        
        if response and response.status_code == 200:
            try:
                rkat_list = response.json()
                
                if rkat_list:
                    # Convert to DataFrame
                    df = pd.DataFrame(rkat_list)
                    
                    # Apply search filter
                    if search_term:
                        mask = df['judul'].str.contains(search_term, case=False, na=False)
                        df = df[mask]
                    
                    # Apply status filter
                    if status_filter != "Semua":
                        df = df[df['status'].str.contains(status_filter.lower(), case=False, na=False)]
                    
                    # Apply bidang filter
                    if bidang_filter != "Semua":
                        df = df[df['bidang'].str.contains(bidang_filter, case=False, na=False)]
                    
                    if not df.empty:
                        # Display RKAT table
                        st.dataframe(
                            df,
                            use_container_width=True,
                            column_config={
                                "id": "ID RKAT",
                                "judul": "Judul",
                                "bidang": "Bidang",
                                "status": "Status",
                                "total_anggaran": st.column_config.NumberColumn(
                                    "Total Anggaran",
                                    format="Rp%.0f"
                                ),
                                "progress_percentage": st.column_config.ProgressColumn(
                                    "Progress",
                                    min_value=0,
                                    max_value=100
                                )
                            }
                        )
                        
                        # Statistics
                        st.subheader("📊 Statistik RKAT")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Total RKAT", len(df))
                        with col2:
                            approved_count = len(df[df['status'] == 'approved'])
                            st.metric("RKAT Disetujui", approved_count)
                        with col3:
                            total_budget = df['total_anggaran'].sum() if 'total_anggaran' in df.columns else 0
                            st.metric("Total Anggaran", f"Rp {total_budget/1000000000:.1f}B")
                        
                    else:
                        st.info("📝 Tidak ada RKAT yang sesuai dengan filter")
                        
                else:
                    st.info("📝 Belum ada RKAT yang dibuat")
                    show_sample_rkat_data()
                    
            except Exception as e:
                st.error(f"Error parsing RKAT data: {e}")
                st.code(response.text)
                
        elif response and response.status_code == 404:
            st.error("❌ Endpoint tidak ditemukan")
            st.info("💡 Checking available endpoints...")
            
            # Try to get available endpoints from root
            root_response = make_api_request("GET", "/", headers=get_auth_headers())
            if root_response and root_response.status_code == 200:
                try:
                    root_data = root_response.json()
                    st.json(root_data)
                except:
                    st.code(root_response.text)
            
        else:
            st.error("❌ Gagal memuat data RKAT")
            if response:
                st.code(f"Status: {response.status_code}")
                st.code(f"Response: {response.text}")
            
            show_sample_rkat_data()

def show_sample_rkat_data():
    """Show sample RKAT data for demo"""
    st.info("📊 Menampilkan data sample untuk demo")
    
    sample_data = [
        {
            "id": "RKAT-2026-001",
            "judul": "RKAT Audit Internal 2026",
            "bidang": "Audit Internal",
            "status": "pending_audit_review",
            "total_anggaran": 2500000000,
            "progress_percentage": 25
        },
        {
            "id": "RKAT-2026-002", 
            "judul": "RKAT Teknologi Informasi 2026",
            "bidang": "Teknologi Informasi",
            "status": "approved",
            "total_anggaran": 5000000000,
            "progress_percentage": 100
        }
    ]
    
    df = pd.DataFrame(sample_data)
    st.dataframe(df, use_container_width=True)

def show_create_rkat():
    """Create new RKAT form"""
    st.subheader("➕ Buat RKAT Baru")
    
    with st.form("create_rkat_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            judul = st.text_input("Judul RKAT *", placeholder="Masukkan judul RKAT")
            bidang = st.selectbox("Bidang *", [
                "Audit Internal",
                "Teknologi Informasi", 
                "Akuntansi dan Keuangan",
                "Investasi dan Kemaslahatan"
            ])
            program = st.text_input("Program", placeholder="Nama program")
        
        with col2:
            tahun_anggaran = st.number_input("Tahun Anggaran", min_value=2024, max_value=2030, value=2026)
            total_anggaran = st.number_input("Total Anggaran (Rp)", min_value=0, value=0, step=1000000)
            divisi = st.text_input("Divisi", placeholder="Nama divisi")
        
        latar_belakang = st.text_area("Latar Belakang", placeholder="Uraian latar belakang")
        tujuan = st.text_area("Tujuan", placeholder="Tujuan pelaksanaan")
        sasaran = st.text_area("Sasaran", placeholder="Sasaran yang ingin dicapai")
        
        submitted = st.form_submit_button("🚀 Buat RKAT", use_container_width=True)
        
        if submitted:
            if judul and bidang:
                st.success("✅ RKAT berhasil dibuat!")
                st.info("💡 Fitur penyimpanan akan diintegrasikan dengan backend")
            else:
                st.error("❌ Judul dan Bidang harus diisi")

def show_edit_rkat():
    """Edit existing RKAT"""
    st.subheader("✏️ Edit RKAT")
    
    st.info("💡 Pilih RKAT dari daftar untuk mengedit")
    st.markdown("Fitur edit akan tersedia setelah memilih RKAT dari tab 'Daftar RKAT'")

def show_rkat_detail():
    """Show RKAT detail view"""
    st.subheader("📄 Detail RKAT")
    
    rkat_id = st.text_input("ID RKAT", placeholder="Masukkan ID RKAT untuk melihat detail")
    
    if st.button("🔍 Lihat Detail") and rkat_id:
        with st.spinner("Loading RKAT detail..."):
            # FIXED: Use correct endpoint
            response = make_api_request("GET", f"/rkat/{rkat_id}", headers=get_auth_headers())
            
            if response and response.status_code == 200:
                try:
                    rkat_data = response.json()
                    
                    # Display RKAT details
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**ID:**", rkat_data.get('id'))
                        st.write("**Judul:**", rkat_data.get('judul'))
                        st.write("**Bidang:**", rkat_data.get('bidang'))
                        st.write("**Status:**", rkat_data.get('status'))
                    
                    with col2:
                        st.write("**Total Anggaran:**", f"Rp {rkat_data.get('total_anggaran', 0):,.0f}")
                        st.write("**Progress:**", f"{rkat_data.get('progress_percentage', 0)}%")
                        st.write("**Tahun:**", rkat_data.get('tahun_anggaran'))
                    
                    # Progress bar
                    progress = rkat_data.get('progress_percentage', 0)
                    st.progress(progress / 100)
                    
                    st.json(rkat_data)
                    
                except Exception as e:
                    st.error(f"Error parsing RKAT detail: {e}")
                    
            elif response and response.status_code == 404:
                st.error("❌ RKAT tidak ditemukan")
            else:
                st.error("❌ Gagal memuat detail RKAT")

if __name__ == "__main__":
    main()
