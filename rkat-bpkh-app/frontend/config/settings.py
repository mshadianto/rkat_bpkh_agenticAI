# frontend/config/settings.py
import os

class Settings:
    # Backend Configuration
    API_BASE_URL = "https://rkat-bpkh-agenticai.onrender.com"
    BASE_URL = "https://rkat-bpkh-agenticai.onrender.com"
    API_URL = "https://rkat-bpkh-agenticai.onrender.com"
    
    # Streamlit App Configuration
    APP_TITLE = "RKAT BPKH Management System"
    PAGE_TITLE = "RKAT BPKH Management System"
    PAGE_ICON = "🏛️"
    APP_ICON = "🏛️"
    TITLE = "RKAT BPKH Management System"
    ICON = "🏛️"
    APP_NAME = "RKAT BPKH"
    
    # Streamlit Layout Configuration
    LAYOUT = "wide"
    INITIAL_SIDEBAR_STATE = "expanded"
    SIDEBAR_STATE = "expanded"
    
    # Theme Configuration
    PRIMARY_COLOR = "#1f77b4"
    BACKGROUND_COLOR = "#ffffff"
    SECONDARY_BACKGROUND_COLOR = "#f0f2f6"
    TEXT_COLOR = "#262730"
    THEME = "light"
    
    # Menu Configuration
    MENU_ITEMS = {
        'Get Help': 'https://docs.streamlit.io',
        'Report a bug': 'https://github.com/mshadianto/rkat_bpkh_agenticAI/issues',
        'About': 'RKAT BPKH Management System v1.0'
    }
    
    # RKAT Status mapping
    RKAT_STATUS = {
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
    
    # User roles and permissions
    USER_ROLES = {
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
        },
        "komite_dewan_pengawas": {
            "can_create_rkat": False,
            "can_edit_rkat": False,
            "can_approve_rkat": True,
            "can_view_all": True
        },
        "dewan_pengawas": {
            "can_create_rkat": False,
            "can_edit_rkat": False,
            "can_approve_rkat": True,
            "can_view_all": True
        }
    }
    
    # Environment Configuration
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
    
    # API Configuration
    API_TIMEOUT = 30
    REQUEST_TIMEOUT = 30
    API_RETRIES = 3
    
    # Authentication Configuration
    SESSION_TIMEOUT = 3600
    TOKEN_KEY = "auth_token"
    AUTO_LOGIN = False
    
    # Navigation Configuration
    NAVIGATION = {
        "Dashboard": "🏠",
        "RKAT Management": "📊", 
        "Workflow": "🔄",
        "AI Assistant": "🤖"
    }
    
    # File Configuration
    MAX_FILE_SIZE_MB = 10
    ALLOWED_FILE_TYPES = ["pdf", "docx", "xlsx", "csv"]
    UPLOAD_DIRECTORY = "/tmp/uploads"
    
    # Pagination Configuration
    ITEMS_PER_PAGE = 10
    MAX_ITEMS_PER_PAGE = 100
    
    # Cache Configuration
    CACHE_TTL = 300  # 5 minutes
    CACHE_ENABLED = True
    
    # Feature Flags
    ENABLE_AI_ASSISTANT = True
    ENABLE_FILE_UPLOAD = True
    ENABLE_NOTIFICATIONS = True
    ENABLE_EXPORT = True
    ENABLE_DARK_MODE = True
    ENABLE_ANALYTICS = True
    
    # Demo Configuration
    DEMO_MODE = True
    DEMO_CREDENTIALS = {
        "admin": "admin123",
        "badan_pelaksana": "bp123",
        "audit_internal": "audit123",
        "komite_dewan": "komite123",
        "dewan_pengawas": "dewan123"
    }
    
    # UI Text Configuration
    LOGIN_TITLE = "Login ke RKAT BPKH"
    LOGIN_SUBTITLE = "Masukkan kredensial Anda"
    WELCOME_MESSAGE = "Selamat datang di RKAT BPKH Management System"
    
    # Error Messages
    ERROR_MESSAGES = {
        "connection_failed": "Koneksi ke server gagal",
        "invalid_credentials": "Username atau password salah",
        "access_denied": "Akses ditolak",
        "server_error": "Terjadi kesalahan server"
    }
    
    # Success Messages
    SUCCESS_MESSAGES = {
        "login_success": "Login berhasil",
        "rkat_created": "RKAT berhasil dibuat",
        "rkat_updated": "RKAT berhasil diperbarui",
        "rkat_submitted": "RKAT berhasil disubmit"
    }
    
    # API Endpoints
    ENDPOINTS = {
        "auth": {
            "login": "/api/auth/login",
            "me": "/api/auth/me",
            "logout": "/api/auth/logout"
        },
        "rkat": {
            "list": "/api/rkat/list",
            "detail": "/api/rkat/{id}",
            "create": "/api/rkat/create",
            "update": "/api/rkat/{id}",
            "delete": "/api/rkat/{id}",
            "submit": "/api/rkat/{id}/submit"
        },
        "analytics": {
            "dashboard": "/api/analytics/dashboard-metrics",
            "reports": "/api/analytics/reports"
        },
        "workflow": {
            "pending": "/api/workflow/pending-reviews",
            "history": "/api/workflow/history/{id}",
            "approve": "/api/workflow/approve/{id}",
            "reject": "/api/workflow/reject/{id}"
        },
        "ai": {
            "chat": "/api/ai/chat",
            "suggestions": "/api/ai/suggestions"
        },
        "files": {
            "upload": "/api/files/upload",
            "download": "/api/files/download/{id}"
        }
    }
    
    # Chart Configuration
    CHART_COLORS = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
        "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
    ]
    
    # Table Configuration
    TABLE_PAGE_SIZE = 20
    TABLE_SORTABLE = True
    TABLE_SEARCHABLE = True
    
    # Notification Configuration
    NOTIFICATION_DURATION = 5000  # milliseconds
    NOTIFICATION_POSITION = "top-right"
    
    # Export Configuration
    EXPORT_FORMATS = ["xlsx", "csv", "pdf"]
    EXPORT_FILENAME_PREFIX = "rkat_export"
    
    # Version Information
    VERSION = "1.0.0"
    BUILD_DATE = "2025-01-28"
    
    # Contact Information
    SUPPORT_EMAIL = "support@bpkh.go.id"
    HELP_URL = "https://docs.bpkh.go.id"

# Create settings instance
settings = Settings()

# Export all attributes at module level for backward compatibility
_module_vars = {}
for attr_name in dir(settings):
    if not attr_name.startswith('_'):
        _module_vars[attr_name] = getattr(settings, attr_name)

# Add to global namespace
globals().update(_module_vars)

# Explicit exports for common access patterns
API_BASE_URL = settings.API_BASE_URL
APP_TITLE = settings.APP_TITLE
PAGE_TITLE = settings.PAGE_TITLE
PAGE_ICON = settings.PAGE_ICON
LAYOUT = settings.LAYOUT
RKAT_STATUS = settings.RKAT_STATUS
