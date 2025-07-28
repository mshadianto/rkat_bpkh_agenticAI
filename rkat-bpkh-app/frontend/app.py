# frontend/app.py - Konfigurasi untuk backend rkat_fixed.py
import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import json
import time
import os

# Configuration - Sesuaikan dengan backend yang running
BACKEND_URL = "https://rkat-bpkh-agenticai.onrender.com"
REQUEST_TIMEOUT = 30

# Debug info
st.sidebar.markdown(f"""
**🔧 Config Info:**
- Backend File: `rkat_fixed.py`
- Backend URL: `{BACKEND_URL}`
- Status: {'🟢 Connected' if True else '🔴 Disconnected'}
""")

def test_backend_connection():
    """Test koneksi ke backend rkat_fixed.py"""
    try:
        # Test basic endpoint
        response = requests.get(f"{BACKEND_URL}/", timeout=10)
        if response.status_code == 200:
            st.success(f"✅ Backend connected: rkat_fixed.py")
            return True
        else:
            st.warning(f"⚠️ Backend responded: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Cannot connect to backend: {str(e)}")
        st.info(f"Backend URL: {BACKEND_URL}")
        
        # Show troubleshooting
        with st.expander("🔧 Troubleshooting"):
            st.markdown(f"""
            **Current Setup:**
            - Backend file: `rkat_fixed.py`
            - Backend URL: `{BACKEND_URL}`
            - Frontend: Streamlit Cloud
            
            **Check:**
            1. [Test backend directly]({BACKEND_URL})
            2. Check Render.com logs
            3. Verify `rkat_fixed.py` is the correct entry point
            4. Check CORS configuration in `rkat_fixed.py`
            """)
        
        return False

def make_api_request(method, endpoint, **kwargs):
    """API request wrapper untuk rkat_fixed.py backend"""
    try:
        url = f"{BACKEND_URL}{endpoint}"
        kwargs['timeout'] = REQUEST_TIMEOUT
        
        # Debug request info
        st.write(f"🔄 {method} {endpoint}")
        
        if method.upper() == "GET":
            response = requests.get(url, **kwargs)
        elif method.upper() == "POST":
            response = requests.post(url, **kwargs)
        elif method.upper() == "PUT":
            response = requests.put(url, **kwargs)
        elif method.upper() == "DELETE":
            response = requests.delete(url, **kwargs)
        
        st.write(f"📡 Status: {response.status_code}")
        return response
        
    except requests.exceptions.RequestException as e:
        st.error(f"❌ API Error: {str(e)}")
        return None

def main():
    st.set_page_config(
        page_title="RKAT BPKH",
        page_icon="🏛️",
        layout="wide"
    )
    
    st.title("🏛️ Sistem RKAT BPKH")
    
    # Backend connection test
    if not test_backend_connection():
        st.markdown("""
        ### ⚠️ Backend Connection Issue
        
        **Problem**: Frontend tidak dapat connect ke `rkat_fixed.py` backend.
        
        **Solution Steps:**
        1. **Verify backend is running:**
           - Check Render.com dashboard
           - Look at deployment logs
           - Ensure `rkat_fixed.py` is the entry point
        
        2. **Test backend directly:**
           - Open: https://rkat-bpkh-agenticai.onrender.com
           - Should return API response
        
        3. **Check CORS in rkat_fixed.py:**
           ```python
           app.add_middleware(
               CORSMiddleware,
               allow_origins=["*"],
               allow_credentials=True,
               allow_methods=["*"],
               allow_headers=["*"],
           )
           ```
        """)
        return
    
    # Authentication flow
    if 'authenticated' not in st.session_state:
        login_page()
    else:
        main_app()

def login_page():
    st.subheader("🔐 Login ke Sistem")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        username = st.text_input("Username", value="admin123")
        password = st.text_input("Password", value="admin123", type="password")
        
        if st.button("Login", use_container_width=True):
            with st.spinner("Connecting to rkat_fixed.py backend..."):
                response = make_api_request("POST", "/auth/login", 
                                          json={"username": username, "password": password})
                
                if response and response.status_code == 200:
                    try:
                        data = response.json()
                        st.session_state['authenticated'] = True
                        st.session_state['user'] = data.get('user', {})
                        st.session_state['token'] = data.get('access_token', '')
                        st.success("✅ Login berhasil!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Login response error: {e}")
                        st.code(response.text)
                else:
                    st.error("❌ Login gagal atau backend tidak merespons")
                    if response:
                        st.code(f"Status: {response.status_code}")
                        st.code(response.text)
    
    # Available credentials
    with st.expander("🔑 Available Credentials"):
        st.markdown("""
        Test dengan credentials berikut:
        - `admin123` / `admin123`
        - `audit123` / `audit123`
        - `komite123` / `komite123`
        """)

def main_app():
    st.success("🎉 Successfully connected to rkat_fixed.py backend!")
    
    # Navigation
    tabs = st.tabs(["📊 Dashboard", "📋 RKAT Management", "🔄 Workflow", "🤖 AI Assistant"])
    
    with tabs[0]:
        dashboard_page()
    
    with tabs[1]:
        rkat_page()
    
    with tabs[2]:
        workflow_page()
    
    with tabs[3]:
        ai_page()
    
    # Logout button
    if st.sidebar.button("🚪 Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

def get_auth_headers():
    """Get authorization headers"""
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

def dashboard_page():
    st.subheader("📊 Dashboard")
    
    with st.spinner("Loading data from rkat_fixed.py..."):
        response = make_api_request("GET", "/dashboard/metrics", headers=get_auth_headers())
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total RKAT", data.get('total_rkat', 0))
                with col2:
                    st.metric("Approved", data.get('approved_rkat', 0))
                with col3:
                    st.metric("Budget", f"Rp {data.get('total_budget', 0)/1000000:.1f}M")
                with col4:
                    st.metric("Avg Days", f"{data.get('avg_approval_days', 0):.1f}")
                
                st.success("✅ Data loaded from rkat_fixed.py successfully!")
                
            except Exception as e:
                st.error(f"Error parsing dashboard data: {e}")
        else:
            st.warning("Using mock data (backend connection issue)")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total RKAT", 24)
            with col2:
                st.metric("Approved", 14)
            with col3:
                st.metric("Budget", "Rp 25.0M")
            with col4:
                st.metric("Avg Days", "5.8")

def rkat_page():
    st.subheader("📋 RKAT Management")
    
    with st.spinner("Loading RKAT data..."):
        response = make_api_request("GET", "/rkat/", headers=get_auth_headers())
        
        if response and response.status_code == 200:
            try:
                rkat_list = response.json()
                if rkat_list:
                    df = pd.DataFrame(rkat_list)
                    st.dataframe(df[['id', 'judul', 'bidang', 'status']], use_container_width=True)
                else:
                    st.info("No RKAT data found")
            except Exception as e:
                st.error(f"Error loading RKAT data: {e}")
        else:
            st.info("RKAT data will appear here when backend is fully connected")

def workflow_page():
    st.subheader("🔄 Workflow RKAT")
    
    st.markdown("""
    **Alur Persetujuan RKAT BPKH:**
    1. 📝 Pengajuan RKAT oleh Bidang
    2. 🔍 Review oleh Audit Internal  
    3. 📋 Review oleh Komite Dewan Pengawas
    4. ✅ Persetujuan oleh Dewan Pengawas
    """)
    
    # Test workflow endpoints
    if st.button("🧪 Test Workflow Endpoints"):
        endpoints = ["/workflow/steps", "/references/kup", "/references/sbo"]
        
        for endpoint in endpoints:
            with st.expander(f"Test {endpoint}"):
                response = make_api_request("GET", endpoint, headers=get_auth_headers())
                if response:
                    st.code(f"Status: {response.status_code}")
                    if response.status_code == 200:
                        try:
                            st.json(response.json())
                        except:
                            st.text(response.text)

def ai_page():
    st.subheader("🤖 AI Assistant")
    
    st.markdown("""
    AI Assistant untuk RKAT BPKH:
    - 🔍 Analisis kelayakan anggaran
    - 📊 Validasi kesesuaian KUP & SBO
    - ⏱️ Prediksi timeline approval
    - 💡 Saran optimasi
    """)
    
    # Simple chat interface
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    if prompt := st.chat_input("Tanya tentang RKAT..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            response = f"AI Assistant: Pertanyaan Anda tentang '{prompt}' akan dijawab ketika fitur AI terintegrasi dengan backend rkat_fixed.py"
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
