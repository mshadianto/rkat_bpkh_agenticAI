import streamlit as st
from utils.api_client import APIClient
from config.settings import settings

class AuthComponent:
    def __init__(self, api_client: APIClient):
        self.api = api_client
    
    def login_form(self):
        """Display login form"""
        with st.form("login_form"):
            st.subheader("🔐 Login RKAT BPKH")
            
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.form_submit_button("Login", use_container_width=True):
                if username and password:
                    response = self.api.login(username, password)
                    
                    if response["success"]:
                        # Store auth data in session
                        st.session_state.auth_token = response["data"]["access_token"]
                        st.session_state.user_info = response["data"]["user_info"]
                        st.session_state.authenticated = True
                        
                        # Set API token
                        self.api.set_auth_token(response["data"]["access_token"])
                        
                        st.success("Login berhasil!")
                        st.rerun()
                    else:
                        st.error(f"Login gagal: {response.get('error', 'Unknown error')}")
                else:
                    st.warning("Silakan masukkan username dan password")
    
    def logout(self):
        """Logout user"""
        # Clear session state
        for key in ["auth_token", "user_info", "authenticated"]:
            if key in st.session_state:
                del st.session_state[key]
        
        # Clear API token
        self.api.clear_auth_token()
        
        st.success("Logout berhasil!")
        st.rerun()
    
    def get_user_info(self):
        """Get current user info"""
        return st.session_state.get("user_info", {})
    
    def is_authenticated(self):
        """Check if user is authenticated"""
        return st.session_state.get("authenticated", False)
    
    def has_role(self, role: str):
        """Check if user has specific role"""
        user_info = self.get_user_info()
        return user_info.get("role") == role
    
    def can_create_rkat(self):
        """Check if user can create RKAT"""
        return self.has_role("badan_pelaksana")
    
    def can_review_rkat(self):
        """Check if user can review RKAT"""
        return self.has_role("audit_internal") or \
               self.has_role("komite_dewan_pengawas") or \
               self.has_role("dewan_pengawas")