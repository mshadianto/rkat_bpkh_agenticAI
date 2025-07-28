# app.py - Main Streamlit app dengan session state yang diperbaiki
import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import json
import time
import os

# Configuration
BACKEND_URL = "https://rkat-bpkh-agenticai.onrender.com"
REQUEST_TIMEOUT = 30

# Page config
st.set_page_config(
    page_title="RKAT BPKH",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize session state dengan keys yang konsisten"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'token' not in st.session_state:
        st.session_state.token = None
    if 'auth_token' not in st.session_state:
        st.session_state.auth_token = None

def test_backend_connection():
    """Test koneksi ke backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=10)
        if response.status_code == 200:
            return True
        return False
    except:
        return False

def make_api_request(method, endpoint, **kwargs):
    """API request wrapper dengan error handling"""
    try:
        url = f"{BACKEND_URL}{endpoint}"
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
        
    except requests.exceptions.RequestException as e:
        st.error(f"❌ API Error: {str(e)}")
        return None

def get_auth_headers():
    """Get authorization headers - dengan fallback untuk berbagai session keys"""
    token = st.session_state.get('token') or st.session_state.get('auth_token')
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

def login_page():
    """Login page dengan session state management yang proper"""
    st.markdown("""
    <div style="text-align: center;">
        <h1>🏛️ Sistem RKAT BPKH</h1>
        <h3>Login ke Sistem</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Backend connection check
    if not test_backend_connection():
        st.error("❌ Backend tidak dapat diakses")
        st.info(f"Backend URL: {BACKEND_URL}")
        return
    else:
        st.success("✅ Backend terhubung")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username", value="admin123")
            password = st.text_input("Password", value="admin123", type="password")
            
            submitted = st.form_submit_button("Login", use_container_width=True)
            
            if submitted:
                with st.spinner("Memverifikasi login..."):
                    response = make_api_request("POST", "/auth/login", 
                                              json={"username": username, "password": password})
                    
                    if response and response.status_code == 200:
                        try:
                            data = response.json()
                            
                            # Set session state dengan keys yang konsisten
                            st.session_state['authenticated'] = True
                            st.session_state['user'] = data['user'] 
                            st.session_state['token'] = data['access_token']
                            st.session_state['auth_token'] = data['access_token']  # Duplicate untuk compatibility
                            
                            st.success("✅ Login berhasil!")
                            time.sleep(1)
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"Error parsing response: {e}")
                    else:
                        st.error("❌ Login gagal")
    
    # Available credentials
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
    """Main application dengan navigation"""
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 10px;">
            <h2>🏛️ BPKH</h2>
            <p>Sistem RKAT</p>
        </div>
        """, unsafe_allow_html=True)
        
        # User info - dengan safe access
        user = st.session_state.get('user', {})
        st.markdown(f"""
        **👤 {user.get('name', 'Unknown User')}**  
        📋 Role: {user.get('role', 'N/A')}  
        🏢 Bidang: {user.get('bidang', 'N/A')}
        """)
        
        st.divider()
        
        # Navigation
        page = st.radio("Navigation", [
            "📊 Dashboard",
            "📋 RKAT Management", 
            "🔄 Workflow",
            "🤖 AI Assistant"
        ])
        
        st.divider()
        
        # Debug info
        st.markdown("**🔧 Debug Info:**")
        st.write(f"Authenticated: {st.session_state.get('authenticated', False)}")
        st.write(f"Token exists: {bool(st.session_state.get('token'))}")
        st.write(f"Auth token exists: {bool(st.session_state.get('auth_token'))}")
        
        if st.button("🚪 Logout", use_container_width=True):
            # Clear all session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Main content
    if page == "📊 Dashboard":
        dashboard_page()
    elif page == "📋 RKAT Management":
        rkat_management_page()
    elif page == "🔄 Workflow":
        workflow_page()
    elif page == "🤖 AI Assistant":
        ai_assistant_page()

def dashboard_page():
    """Dashboard page dengan error handling yang proper"""
    st.title("📊 Dashboard RKAT BPKH")
    
    # Check authentication
    if not st.session_state.get('authenticated'):
        st.error("❌ Anda belum login")
        return
    
    try:
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
                    df = df[df['Count'] > 0]
                    
                    if not df.empty:
                        st.bar_chart(df.set_index('Status'))
                    else:
                        st.info("Belum ada data RKAT")
                else:
                    st.info("Belum ada data untuk ditampilkan")
                    
            else:
                st.error("Gagal memuat data dashboard")
                show_mock_dashboard()
                
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")
        show_mock_dashboard()

def show_mock_dashboard():
    """Show mock dashboard data"""
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
    """RKAT Management page"""
    st.title("📋 Manajemen RKAT")
    
    with st.spinner("Loading RKAT data..."):
        response = make_api_request("GET", "/rkat/", headers=get_auth_headers())
        
        if response and response.status_code == 200:
            try:
                rkat_list = response.json()
                
                if rkat_list:
                    df = pd.DataFrame(rkat_list)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("📝 Belum ada RKAT yang dibuat")
                    
            except Exception as e:
                st.error(f"Error parsing RKAT data: {e}")
        else:
            st.error("Gagal memuat data RKAT")

def workflow_page():
    """Workflow page"""
    st.title("🔄 Workflow RKAT BPKH")
    
    st.markdown("""
    ### Alur Persetujuan RKAT
    
    Sistem RKAT BPKH mengikuti alur persetujuan 4 tahap:
    1. 📝 **Pengajuan RKAT** - Bidang mengajukan RKAT sesuai KUP & SBO
    2. 🔍 **Review Audit Internal** - Tim Audit Internal melakukan review kelayakan
    3. 📋 **Review Komite Dewan** - Komite Dewan Pengawas melakukan evaluasi
    4. ✅ **Persetujuan Dewan** - Dewan Pengawas memberikan persetujuan final
    """)
    
    # Test workflow endpoints
    if st.button("🧪 Test Workflow API"):
        response = make_api_request("GET", "/workflow/steps", headers=get_auth_headers())
        if response and response.status_code == 200:
            st.json(response.json())
        else:
            st.error("Failed to load workflow steps")

def ai_assistant_page():
    """AI Assistant page"""
    st.title("🤖 AI Assistant RKAT")
    
    st.markdown("""
    ### Bantuan Penyusunan RKAT
    
    AI Assistant akan membantu Anda dalam:
    - 🔍 Analisis kelayakan anggaran
    - 📊 Validasi kesesuaian KUP & SBO
    - ⏱️ Prediksi timeline approval
    - 💡 Saran optimasi
    """)
    
    # Simple chat interface
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "Halo! Saya AI Assistant RKAT BPKH. Bagaimana saya dapat membantu Anda?"}
        ]
    
    # Display chat history
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Tanya tentang RKAT..."):
        # Add user message
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        # Add AI response
        with st.chat_message("assistant"):
            response = f"Terima kasih atas pertanyaan Anda tentang '{prompt}'. Fitur AI Assistant sedang dalam pengembangan dan akan segera tersedia dengan kemampuan analisis yang lebih canggih."
            st.write(response)
            st.session_state.chat_messages.append({"role": "assistant", "content": response})

def main():
    """Main function"""
    # Initialize session state
    initialize_session_state()
    
    # Show login or main app
    if not st.session_state.get('authenticated'):
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()
