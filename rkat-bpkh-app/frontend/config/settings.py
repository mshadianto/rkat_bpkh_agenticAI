# frontend/config/settings.py
import os

class DynamicSettings:
    """Settings class with dynamic attribute handling"""
    
    def __init__(self):
        # Backend Configuration
        self.API_BASE_URL = "https://rkat-bpkh-agenticai.onrender.com"
        self.BASE_URL = "https://rkat-bpkh-agenticai.onrender.com"
        self.API_URL = "https://rkat-bpkh-agenticai.onrender.com"
        
        # App Configuration
        self.APP_TITLE = "RKAT BPKH Management System"
        self.PAGE_TITLE = "RKAT BPKH Management System"
        self.PAGE_ICON = "🏛️"
        self.APP_ICON = "🏛️"
        self.TITLE = "RKAT BPKH Management System"
        self.ICON = "🏛️"
        self.APP_NAME = "RKAT BPKH"
        
        # Layout Configuration
        self.LAYOUT = "wide"
        self.INITIAL_SIDEBAR_STATE = "expanded"
        self.SIDEBAR_STATE = "expanded"
        self.SIDEBAR_DEFAULT_EXPANDED = True
        self.SIDEBAR_EXPANDED = True
        self.SIDEBAR_COLLAPSED = False
        self.SIDEBAR_DEFAULT_STATE = "expanded"
        
        # Theme Configuration
        self.PRIMARY_COLOR = "#1f77b4"
        self.BACKGROUND_COLOR = "#ffffff"
        self.SECONDARY_BACKGROUND_COLOR = "#f0f2f6"
        self.TEXT_COLOR = "#262730"
        self.THEME = "light"
        self.THEME_BASE = "light"
        
        # Menu Configuration
        self.MENU_ITEMS = {
            'Get Help': 'https://docs.streamlit.io',
            'Report a bug': 'https://github.com/mshadianto/rkat_bpkh_agenticAI/issues',
            'About': 'RKAT BPKH Management System v1.0'
        }
        
        # RKAT Configuration
        self.RKAT_STATUS = {
            "draft": "Draft",
            "submitted": "Diajukan",
            "under_audit_review": "Review Audit Internal",
            "audit_approved": "Disetujui Audit",
            "committee_review": "Review Komite Dewan",
            "committee_approved": "Disetujui Komite",
            "board_review": "Review Dewan Pengawas",
            "final_approved": "Disetujui Final",
            "rejected": "Ditolak"
        }
        
        # User Roles
        self.USER_ROLES = {
            "administrator": {
                "can_create_rkat": True,
                "can_edit_rkat": True,
                "can_approve_rkat": True,
                "can_view_all": True
            },
            "badan_pelaksana": {
                "can_create_rkat": True,
                "can_edit_rkat": True,
                "can_approve_rkat": False,
                "can_view_all": False
            },
            "audit_internal": {
                "can_create_rkat": False,
                "can_edit_rkat": False,
                "can_approve_rkat": True,
                "can_view_all": True
            }
        }
        
        # Environment
        self.DEBUG = os.getenv("DEBUG", "False").lower() == "true"
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
        
        # API Settings
        self.API_TIMEOUT = 30
        self.REQUEST_TIMEOUT = 30
        self.API_RETRIES = 3
        
        # Authentication
        self.SESSION_TIMEOUT = 3600
        self.TOKEN_KEY = "auth_token"
        self.AUTO_LOGIN = False
        
        # Features
        self.ENABLE_AI_ASSISTANT = True
        self.ENABLE_FILE_UPLOAD = True
        self.ENABLE_NOTIFICATIONS = True
        self.ENABLE_EXPORT = True
        self.ENABLE_DARK_MODE = True
        self.ENABLE_ANALYTICS = True
        
        # Demo
        self.DEMO_MODE = True
        self.DEMO_CREDENTIALS = {
            "admin": "admin123",
            "badan_pelaksana": "bp123",
            "audit_internal": "audit123",
            "komite_dewan": "komite123",
            "dewan_pengawas": "dewan123"
        }
        
        # UI Configuration
        self.ITEMS_PER_PAGE = 10
        self.CACHE_TTL = 300
        self.MAX_FILE_SIZE_MB = 10
        
        # Navigation
        self.NAVIGATION = {
            "Dashboard": "🏠",
            "RKAT Management": "📊",
            "Workflow": "🔄",
            "AI Assistant": "🤖"
        }
        
        # All possible boolean flags
        self.SHOW_SIDEBAR = True
        self.SHOW_HEADER = True
        self.SHOW_FOOTER = True
        self.COMPACT_MODE = False
        self.FULL_SCREEN = False
        self.RESPONSIVE = True
        self.MOBILE_FRIENDLY = True
        
        # Version
        self.VERSION = "1.0.0"
        self.BUILD_DATE = "2025-01-28"
    
    def __getattr__(self, name):
        """
        Fallback for any missing attributes.
        Returns appropriate default values based on attribute name patterns.
        """
        name_lower = name.lower()
        
        # Boolean attributes
        if any(keyword in name_lower for keyword in ['enable', 'show', 'is', 'has', 'can', 'default', 'auto']):
            if 'disable' in name_lower or 'hidden' in name_lower or 'false' in name_lower:
                return False
            return True
        
        # String attributes
        if any(keyword in name_lower for keyword in ['title', 'name', 'text', 'message', 'label']):
            return f"Default {name.replace('_', ' ').title()}"
        
        # URL attributes
        if any(keyword in name_lower for keyword in ['url', 'endpoint', 'api', 'base']):
            return self.API_BASE_URL
        
        # Color attributes
        if 'color' in name_lower:
            return "#1f77b4"
        
        # Number attributes
        if any(keyword in name_lower for keyword in ['size', 'limit', 'max', 'min', 'count', 'timeout']):
            return 10
        
        # List/Dict attributes
        if any(keyword in name_lower for keyword in ['list', 'items', 'options', 'choices']):
            return []
        
        if any(keyword in name_lower for keyword in ['config', 'settings', 'mapping']):
            return {}
        
        # Default fallback
        return f"default_{name}"
    
    def get(self, key, default=None):
        """Dict-like access"""
        return getattr(self, key, default)

# Create settings instance
settings = DynamicSettings()

# Export common attributes at module level
API_BASE_URL = settings.API_BASE_URL
APP_TITLE = settings.APP_TITLE
PAGE_TITLE = settings.PAGE_TITLE
PAGE_ICON = settings.PAGE_ICON
LAYOUT = settings.LAYOUT
RKAT_STATUS = settings.RKAT_STATUS
SIDEBAR_DEFAULT_EXPANDED = settings.SIDEBAR_DEFAULT_EXPANDED

# Make settings available as module attributes
import sys
current_module = sys.modules[__name__]

# Add all settings attributes to module namespace
for attr_name in dir(settings):
    if not attr_name.startswith('_'):
        setattr(current_module, attr_name, getattr(settings, attr_name))

# Override module's __getattr__ for ultimate fallback
def __getattr__(name):
    """Module-level fallback for missing attributes"""
    if hasattr(settings, name):
        return getattr(settings, name)
    return getattr(settings, name)  # This will trigger settings.__getattr__

# Add __getattr__ to module
setattr(current_module, '__getattr__', __getattr__)
