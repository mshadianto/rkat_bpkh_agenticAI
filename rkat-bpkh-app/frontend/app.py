# app.py - Streamlit Frontend dengan koneksi yang diperbaiki
import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import json
import time

# Configuration - Update sesuai environment
if st.secrets.get("environment") == "production":
    API_BASE_URL = "https://your-backend-url.herokuapp.com"  # Ganti dengan URL production
else:
    API_BASE_URL = "http://localhost:8000"  # Local development

# Timeout untuk requests
REQUEST_TIMEOUT = 10

def test_backend_connection():
    """Test koneksi ke backend"""
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=REQUEST_TIMEOUT)
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Backend tidak dapat diakses: {str(e)}")
        st.info(f"Pastikan backend berjalan di: {API_BASE_URL}")
        return False

def make_api_request(method, endpoint, **kwargs):
    """Wrapper untuk semua API requests dengan error handling"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        kwargs['timeout'] = REQUEST_TIMEOUT
        
        if method.upper() == "GET":
            response = requests.get(url, **kwargs)
        elif method.upper() == "POST":
            response = requests.post(url, **kwargs)
        elif method.upper() == "PUT":
            response = requests.put(url, **kwargs)
        elif method.upper() == "DELETE":
            response = requests.delete(url, **kwargs)
        
        return response
    except requests.exceptions.ConnectionError:
        st.error("❌ Tidak dapat terhubung ke server. Pastikan backend berjalan.")
        return None
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timeout. Server tidak merespons.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error: {str(e)}")
        return None

def main():
    st.set_page_config(
        page_title="RKAT BPKH",
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Check backend connection first
    if not test_backend_connection():
        st.markdown("""
        ### 🔧 Troubleshooting
        
        **Backend tidak berjalan. Ikuti langkah berikut:**
        
        1. **Jalankan Backend:**
           ```bash
           cd backend
           uvicorn minimal_backend:app --reload --port 8000
           ```
        
        2. **Pastikan Port 8000 tidak digunakan:**
           ```bash
           lsof -i :8000  # Check port usage
           ```
        
        3. **Install Dependencies:**
           ```bash
           pip install fastapi uvicorn python-multipart
           ```
        
        4. **Test Manual:**
           Buka http://localhost:8000 di browser
        """)
        return
    
    # Authentication
    if 'user' not in st.session_state:
        login_page()
    else:
        main_app()

def login_page():
    st.markdown("""
    <div style="text-align: center;">
        <h1>🏛️ Sistem RKAT BPKH</h1>
        <h3>Login ke Sistem</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username", value="", placeholder="Masukkan username")
            password = st.text_input("Password", type="password", placeholder="Masukkan password")
            
            submitted = st.form_submit_button("Login", use_container_width=True)
            
            if submitted:
                if not username or not password:
                    st.error("Username dan password harus diisi")
                    return
                
                with st.spinner("Memverifikasi login..."):
                    response = make_api_request("POST", "/auth/login", 
                                              json={"username": username, "password": password})
                    
                    if response and response.status_code == 200:
                        data = response.json()
                        st.session_state['user'] = data['user']
                        st.session_state['token'] = data['access_token']
                        st.success("Login berhasil!")
                        time.sleep(1)
                        st.rerun()
                    elif response and response.status_code == 401:
                        st.error("Username atau password salah")
                    else:
                        st.error("Gagal login. Silahkan coba lagi.")
        
        # Demo credentials
        with st.expander("🔑 Demo Credentials"):
            st.markdown("""
            **Available Users:**
            - **Admin**: `admin123` / `admin123`
            - **Audit Internal**: `audit123` / `audit123` 
            - **Komite Dewan**: `komite123` / `komite123`
            - **Dewan Pengawas**: `dewan123` / `dewan123`
            - **Bidang TI**: `bidang_ti` / `ti123`
            """)

def main_app():
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 10px;">
            <h2>🏛️ BPKH</h2>
            <p>Sistem RKAT</p>
        </div>
        """, unsafe_allow_html=True)
        
        # User info
        user = st.session_state['user']
        st.markdown(f"""
        **👤 {user['name']}**  
        📋 Role: {user['role']}  
        🏢 Bidang: {user.get('bidang', 'N/A')}
        """)
        
        st.divider()
        
        # Navigation
        pages = {
            "📊 Dashboard": "dashboard",
            "📋 RKAT Management": "rkat", 
            "🔄 Workflow": "workflow",
            "🤖 AI Assistant": "ai"
        }
        
        selected = st.radio("Navigation", list(pages.keys()), key="nav_radio")
        page = pages[selected]
        
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
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

def get_auth_headers():
    """Get authorization headers"""
    if 'token' in st.session_state:
        return {"Authorization": f"Bearer {st.session_state['token']}"}
    return {}

def dashboard_page():
    st.title("📊 Dashboard RKAT BPKH")
    
    # Test API connection
    with st.spinner("Loading dashboard data..."):
        response = make_api_request("GET", "/dashboard/metrics", headers=get_auth_headers())
        
        if response and response.status_code == 200:
            metrics = response.json()
            
            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total RKAT", metrics.get('total_rkat', 0))
            with col2:
                st.metric("RKAT Disetujui", metrics.get('approved_rkat', 0))
            with col3:
                budget = metrics.get('total_budget', 0)
                st.metric("Total Anggaran", f"Rp {budget/1000000000:.1f}B")
            with col4:
                avg_days = metrics.get('avg_approval_days', 0)
                st.metric("Rata-rata Approval", f"{avg_days:.1f} hari")
            
            # Status distribution
            st.subheader("📈 Distribusi Status RKAT")
            status_dist = metrics.get('status_distribution', {})
            
            if status_dist:
                df = pd.DataFrame(list(status_dist.items()), columns=['Status', 'Count'])
                df = df[df['Count'] > 0]  # Only show non-zero counts
                
                if not df.empty:
                    st.bar_chart(df.set_index('Status'))
                else:
                    st.info("Belum ada data RKAT")
            else:
                st.info("Belum ada data untuk ditampilkan")
                
        else:
            st.error("Gagal memuat data dashboard")
            # Show mock data for demo
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total RKAT", 24)
            with col2:
                st.metric("RKAT Disetujui", 14)
            with col3:
                st.metric("Total Anggaran", "Rp 25.0B")
            with col4:
                st.metric("Rata-rata Approval", "5.8 hari")

def rkat_management_page():
    st.title("📋 Manajemen RKAT")
    
    # Filter controls
    col1, col2, col3 = st.columns(3)
    with col1:
        search_term = st.text_input("🔍 Cari RKAT", placeholder="Masukkan kata kunci...")
    with col2:
        status_filter = st.selectbox("Status", ["Semua", "Draft", "Pending Review", "Approved"])
    with col3:
        bidang_filter = st.selectbox("Bidang", ["Semua", "Audit Internal", "Teknologi Informasi", "Akuntansi"])
    
    # Create new RKAT button
    if st.button("➕ Buat RKAT Baru", use_container_width=True):
        st.info("Fitur pembuatan RKAT baru akan segera tersedia")
    
    # RKAT List
    with st.spinner("Loading RKAT data..."):
        response = make_api_request("GET", "/rkat/", headers=get_auth_headers())
        
        if response and response.status_code == 200:
            rkat_list = response.json()
            
            if rkat_list:
                df = pd.DataFrame(rkat_list)
                
                # Apply filters
                if search_term:
                    mask = df['judul'].str.contains(search_term, case=False, na=False)
                    df = df[mask]
                
                # Display table
                st.dataframe(
                    df[['id', 'judul', 'bidang', 'status', 'total_anggaran', 'progress_percentage']],
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
            else:
                st.info("📝 Belum ada RKAT yang dibuat")
                
        else:
            st.error("Gagal memuat data RKAT")

def workflow_page():
    st.title("🔄 Workflow RKAT BPKH")
    
    st.markdown("""
    ### Alur Persetujuan RKAT
    
    Sistem RKAT BPKH mengikuti alur persetujuan 4 tahap sesuai dengan struktur organisasi dan tata kelola BPKH.
    """)
    
    # Workflow steps
    steps = [
        {
            "step": 1, 
            "title": "📝 Pengajuan RKAT", 
            "desc": "Bidang mengajukan RKAT sesuai KUP & SBO",
            "roles": "Bidang Pengaju",
            "duration": "1-3 hari"
        },
        {
            "step": 2, 
            "title": "🔍 Review Audit Internal", 
            "desc": "Audit Internal melakukan review kelayakan dan kesesuaian",
            "roles": "Tim Audit Internal",
            "duration": "5-7 hari"
        },
        {
            "step": 3, 
            "title": "📋 Review Komite Dewan", 
            "desc": "Komite Dewan Pengawas melakukan evaluasi strategis",
            "roles": "Komite Dewan Pengawas",
            "duration": "3-5 hari"
        },
        {
            "step": 4, 
            "title": "✅ Persetujuan Dewan", 
            "desc": "Dewan Pengawas memberikan persetujuan final",
            "roles": "Dewan Pengawas",
            "duration": "2-3 hari"
        }
    ]
    
    for step in steps:
        with st.expander(f"Step {step['step']}: {step['title']}", expanded=True):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Deskripsi:** {step['desc']}")
                st.write(f"**Penanggung Jawab:** {step['roles']}")
                st.write(f"**Estimasi Waktu:** {step['duration']}")
            
            with col2:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(45deg, #ff6b6b, #feca57);
                    color: white;
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                    font-size: 24px;
                    font-weight: bold;
                ">
                    Step {step['step']}
                </div>
                """, unsafe_allow_html=True)

def ai_assistant_page():
    st.title("🤖 AI Assistant RKAT")
    
    st.markdown("""
    ### Bantuan Penyusunan RKAT
    
    AI Assistant akan membantu Anda dalam:
    """)
    
    features = [
        "🔍 **Analisis Kelayakan Anggaran** - Validasi usulan anggaran berdasarkan historical data",
        "📊 **Validasi Kesesuaian KUP & SBO** - Verifikasi otomatis kesesuaian dengan pedoman",
        "⏱️ **Prediksi Timeline Approval** - Estimasi waktu persetujuan berdasarkan kompleksitas",
        "📈 **Benchmarking** - Perbandingan dengan RKAT sejenis di bidang lain",
        "💡 **Saran Optimasi** - Rekomendasi untuk meningkatkan efisiensi anggaran"
    ]
    
    for feature in features:
        st.markdown(feature)
    
    st.divider()
    
    # Chat interface
    st.subheader("💬 Chat dengan AI Assistant")
    
    # Chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Halo! Saya AI Assistant RKAT BPKH. Bagaimana saya dapat membantu Anda hari ini?"}
        ]
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"**👤 Anda:** {message['content']}")
        else:
            st.markdown(f"**🤖 AI:** {message['content']}")
    
    # Chat input
    user_input = st.text_input("Tanyakan tentang RKAT, KUP, SBO, atau proses approval...", key="chat_input")
    
    if st.button("Kirim", use_container_width=True):
        if user_input:
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Simple AI response (replace with actual AI integration)
            ai_response = f"Terima kasih atas pertanyaan Anda tentang '{user_input}'. Fitur AI Assistant sedang dalam pengembangan dan akan segera tersedia dengan kemampuan analisis yang lebih canggih."
            
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.rerun()

if __name__ == "__main__":
    main()
