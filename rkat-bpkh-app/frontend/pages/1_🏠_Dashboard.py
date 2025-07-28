# frontend/pages/1_🏠_Dashboard.py - Fixed version
import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Configuration
BACKEND_URL = "https://rkat-bpkh-agenticai.onrender.com"

def get_auth_headers():
    """Get authorization headers with safe session state access"""
    # Fix: Handle multiple possible token keys
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
        kwargs['timeout'] = 30
        
        if method.upper() == "GET":
            response = requests.get(url, **kwargs)
        elif method.upper() == "POST":
            response = requests.post(url, **kwargs)
        
        return response
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

def main():
    st.title("📊 Dashboard RKAT BPKH")
    
    # Check authentication with safe access
    if not st.session_state.get('authenticated', False):
        st.error("❌ Anda belum login. Silahkan login terlebih dahulu.")
        st.info("👈 Klik halaman utama untuk login")
        return
    
    # Debug info
    with st.expander("🔧 Debug Session State"):
        st.write("Session State Keys:", list(st.session_state.keys()))
        st.write("Authenticated:", st.session_state.get('authenticated'))
        st.write("Has token:", bool(st.session_state.get('token')))
        st.write("Has auth_token:", bool(st.session_state.get('auth_token')))
        st.write("User:", st.session_state.get('user', {}).get('name', 'Not found'))
    
    try:
        # FIXED: Safe session state access - line yang error sebelumnya
        headers = get_auth_headers()
        
        if not headers:
            st.error("❌ Token tidak ditemukan. Silahkan login ulang.")
            if st.button("🔄 Refresh Page"):
                st.rerun()
            return
        
        with st.spinner("Loading dashboard data..."):
            response = make_api_request("GET", "/dashboard/metrics", headers=headers)
            
            if response and response.status_code == 200:
                metrics = response.json()
                
                # Display metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        label="Total RKAT",
                        value=metrics.get('total_rkat', 0)
                    )
                
                with col2:
                    st.metric(
                        label="RKAT Disetujui", 
                        value=metrics.get('approved_rkat', 0)
                    )
                
                with col3:
                    budget = metrics.get('total_budget', 0)
                    st.metric(
                        label="Total Anggaran",
                        value=f"Rp {budget/1000000000:.1f}B"
                    )
                
                with col4:
                    avg_days = metrics.get('avg_approval_days', 0)
                    st.metric(
                        label="Rata-rata Approval",
                        value=f"{avg_days:.1f} hari"
                    )
                
                # Status distribution chart
                st.subheader("📈 Distribusi Status RKAT")
                
                status_dist = metrics.get('status_distribution', {})
                if status_dist:
                    # Convert to DataFrame for visualization
                    df = pd.DataFrame(
                        list(status_dist.items()), 
                        columns=['Status', 'Count']
                    )
                    
                    # Filter non-zero counts
                    df = df[df['Count'] > 0]
                    
                    if not df.empty:
                        st.bar_chart(df.set_index('Status'))
                        
                        # Show table as well
                        st.subheader("📋 Detail Status")
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("📝 Belum ada data RKAT")
                else:
                    st.info("📊 Data status belum tersedia")
                
                # Success message
                st.success("✅ Dashboard data loaded successfully!")
                
            elif response and response.status_code == 401:
                st.error("❌ Token expired. Please login again.")
                # Clear session state
                for key in ['authenticated', 'token', 'auth_token', 'user']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
                
            else:
                st.error("❌ Gagal memuat data dashboard")
                if response:
                    st.code(f"Status: {response.status_code}")
                    st.code(f"Response: {response.text}")
                
                # Show mock data as fallback
                show_mock_dashboard()
                
    except Exception as e:
        st.error(f"❌ Error loading dashboard: {str(e)}")
        st.info("Menampilkan data mock untuk demo...")
        show_mock_dashboard()

def show_mock_dashboard():
    """Show mock dashboard data as fallback"""
    st.info("📊 Menampilkan data mock untuk demo")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total RKAT", 24)
    with col2:
        st.metric("RKAT Disetujui", 14)
    with col3:
        st.metric("Total Anggaran", "Rp 25.0B")
    with col4:
        st.metric("Rata-rata Approval", "5.8 hari")
    
    # Mock chart data
    mock_data = pd.DataFrame({
        'Status': ['Draft', 'Pending Review', 'Approved'],
        'Count': [5, 8, 11]
    })
    
    st.bar_chart(mock_data.set_index('Status'))

if __name__ == "__main__":
    main()
