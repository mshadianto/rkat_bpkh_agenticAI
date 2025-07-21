"""
Authentication and Security Module for Streamlit Deployment
"""

import streamlit as st
import hashlib
import os
from datetime import datetime, timedelta
import secrets
from typing import Dict, List, Optional
import time

class StreamlitAuth:
    """Authentication system for Streamlit app"""
    
    def __init__(self):
        self.session_timeout = 3600  # 1 hour
        self.max_login_attempts = 3
        self.lockout_duration = 900  # 15 minutes
        
        # Load authorized users from environment or config
        self.authorized_users = self._load_authorized_users()
        self.authorized_ips = self._load_authorized_ips()
        
    def _load_authorized_users(self) -> Dict[str, str]:
        """Load authorized users from environment variables"""
        users = {}
        
        # Method 1: Environment variables
        user_list = os.getenv("AUTHORIZED_USERS", "")
        if user_list:
            # Format: "user1:password1,user2:password2"
            for user_pass in user_list.split(","):
                if ":" in user_pass:
                    username, password = user_pass.split(":", 1)
                    users[username.strip()] = self._hash_password(password.strip())
        
        # Method 2: Default users (for development only)
        if not users:
            users = {
                "admin": self._hash_password("bpkh2024!"),
                "mshadianto": self._hash_password("komiteaudit2024"),
                "bpkh_user": self._hash_password("muamalat2024")
            }
            
        return users
    
    def _load_authorized_ips(self) -> List[str]:
        """Load authorized IP addresses"""
        ip_list = os.getenv("AUTHORIZED_IPS", "")
        if ip_list:
            return [ip.strip() for ip in ip_list.split(",")]
        
        # Default: Allow all IPs (remove in production)
        return []
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _get_client_ip(self) -> str:
        """Get client IP address"""
        # Try to get real IP from headers (works with reverse proxies)
        headers = st.context.headers if hasattr(st.context, 'headers') else {}
        
        # Check various headers for real IP
        for header in ['X-Forwarded-For', 'X-Real-IP', 'CF-Connecting-IP']:
            if header in headers:
                ip = headers[header].split(',')[0].strip()
                if ip and ip != 'unknown':
                    return ip
        
        # Fallback
        return "unknown"
    
    def check_ip_whitelist(self) -> bool:
        """Check if client IP is in whitelist"""
        if not self.authorized_ips:
            return True  # No IP restriction
        
        client_ip = self._get_client_ip()
        return client_ip in self.authorized_ips or client_ip == "unknown"
    
    def check_login_attempts(self, username: str) -> bool:
        """Check if user has exceeded login attempts"""
        key = f"login_attempts_{username}"
        lockout_key = f"lockout_until_{username}"
        
        # Check if user is locked out
        if lockout_key in st.session_state:
            lockout_until = st.session_state[lockout_key]
            if datetime.now() < lockout_until:
                return False
            else:
                # Lockout expired, reset
                del st.session_state[lockout_key]
                if key in st.session_state:
                    del st.session_state[key]
        
        return True
    
    def record_failed_attempt(self, username: str):
        """Record failed login attempt"""
        key = f"login_attempts_{username}"
        
        if key not in st.session_state:
            st.session_state[key] = 0
        
        st.session_state[key] += 1
        
        if st.session_state[key] >= self.max_login_attempts:
            # Lock out user
            lockout_key = f"lockout_until_{username}"
            st.session_state[lockout_key] = datetime.now() + timedelta(seconds=self.lockout_duration)
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate user credentials"""
        if username not in self.authorized_users:
            return False
        
        hashed_input = self._hash_password(password)
        return hashed_input == self.authorized_users[username]
    
    def login(self) -> bool:
        """Handle user login"""
        # Check IP whitelist first
        if not self.check_ip_whitelist():
            st.error("🚫 Access denied: Your IP address is not authorized")
            st.info("Contact MS Hadianto | Komite Audit for access authorization")
            return False
        
        # Initialize session state
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'username' not in st.session_state:
            st.session_state.username = None
        if 'login_time' not in st.session_state:
            st.session_state.login_time = None
        
        # Check if already authenticated and session valid
        if st.session_state.authenticated and self._is_session_valid():
            return True
        
        # Show login form
        return self._show_login_form()
    
    def _is_session_valid(self) -> bool:
        """Check if current session is still valid"""
        if not st.session_state.login_time:
            return False
        
        session_age = datetime.now() - st.session_state.login_time
        return session_age.total_seconds() < self.session_timeout
    
    def _show_login_form(self) -> bool:
        """Display login form"""
        st.markdown("""
        <div style='text-align: center; padding: 2rem;'>
            <h1>🏦 Bank Muamalat Health Monitor</h1>
            <h3>🔐 Secure Access Portal</h3>
            <p>Authorized Personnel Only</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create login form
        with st.form("login_form"):
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                st.markdown("### Please Login")
                username = st.text_input("👤 Username", placeholder="Enter your username")
                password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
                
                col_login, col_help = st.columns([1, 1])
                
                with col_login:
                    login_clicked = st.form_submit_button("🔓 Login", use_container_width=True)
                
                with col_help:
                    if st.form_submit_button("❓ Help", use_container_width=True):
                        self._show_help()
        
        if login_clicked:
            if not username or not password:
                st.error("Please enter both username and password")
                return False
            
            # Check login attempts
            if not self.check_login_attempts(username):
                st.error(f"🔒 Account locked due to multiple failed attempts. Try again in {self.lockout_duration//60} minutes.")
                return False
            
            # Authenticate
            if self.authenticate_user(username, password):
                # Success
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.login_time = datetime.now()
                
                # Clear failed attempts
                key = f"login_attempts_{username}"
                if key in st.session_state:
                    del st.session_state[key]
                
                st.success(f"✅ Welcome, {username}!")
                time.sleep(1)
                st.rerun()
                return True
            else:
                # Failed
                self.record_failed_attempt(username)
                remaining_attempts = self.max_login_attempts - st.session_state.get(f"login_attempts_{username}", 0)
                
                if remaining_attempts > 0:
                    st.error(f"❌ Invalid credentials. {remaining_attempts} attempts remaining.")
                else:
                    st.error(f"🔒 Account locked due to multiple failed attempts.")
                
                return False
        
        return False
    
    def _show_help(self):
        """Show help information"""
        st.info("""
        **Need Access?**
        
        This application is restricted to authorized BPKH personnel only.
        
        **For Access Requests:**
        - Contact: MS Hadianto
        - Position: Komite Audit
        - Organization: BPKH
        - Email: support@bpkh.go.id
        
        **Authorized Users:**
        - BPKH Board Members
        - Investment Committee
        - Risk Management Team
        - Audit Committee
        """)
    
    def logout(self):
        """Handle user logout"""
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.login_time = None
        st.success("✅ Successfully logged out")
        st.rerun()
    
    def require_auth(self, func):
        """Decorator to require authentication"""
        def wrapper(*args, **kwargs):
            if self.login():
                return func(*args, **kwargs)
            else:
                return None
        return wrapper
    
    def get_user_info(self) -> Dict[str, str]:
        """Get current user information"""
        if not st.session_state.authenticated:
            return {}
        
        return {
            'username': st.session_state.username,
            'login_time': st.session_state.login_time.isoformat() if st.session_state.login_time else None,
            'session_valid': self._is_session_valid(),
            'ip_address': self._get_client_ip()
        }

class EnvironmentAuth:
    """Simple environment-based authentication"""
    
    @staticmethod
    def check_access_token() -> bool:
        """Check if valid access token is provided"""
        # Method 1: URL parameter
        query_params = st.experimental_get_query_params()
        token_from_url = query_params.get('token', [None])[0]
        
        # Method 2: Environment variable
        valid_token = os.getenv('ACCESS_TOKEN', 'bpkh-muamalat-2024')
        
        return token_from_url == valid_token
    
    @staticmethod
    def check_environment() -> bool:
        """Check if running in authorized environment"""
        # Check if specific environment variables are set
        required_env = os.getenv('APP_ENVIRONMENT', 'development')
        return required_env in ['production', 'development']

# Initialize global auth instance
auth = StreamlitAuth()

# Export authentication functions
def require_authentication():
    """Main authentication function"""
    return auth.login()

def get_current_user():
    """Get current authenticated user"""
    return auth.get_user_info()

def logout_user():
    """Logout current user"""
    auth.logout()

def is_authenticated():
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)

# Export all
__all__ = [
    'StreamlitAuth',
    'EnvironmentAuth', 
    'require_authentication',
    'get_current_user',
    'logout_user',
    'is_authenticated',
    'auth'
]