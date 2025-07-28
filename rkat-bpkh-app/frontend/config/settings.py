# frontend/config/settings.py
import os

class Settings:
    # Backend URL - UPDATE INI!
    API_BASE_URL = "https://rkat-bpkh-agenticai.onrender.com"
    
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
    
    # App configuration
    APP_TITLE = "RKAT BPKH Management System"
    PAGE_TITLE = "RKAT BPKH Management System"
    PAGE_ICON = "🏛️"
    APP_ICON = "🏛️"
    
    # Environment-specific settings
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # API timeout settings
    API_TIMEOUT = 30
    
    # Login credentials for demo (remove in production)
    DEMO_CREDENTIALS = {
        "admin": "admin123",
        "badan_pelaksana": "bp123",
        "audit_internal": "audit123",
        "komite_dewan": "komite123",
        "dewan_pengawas": "dewan123"
    }

# Create settings instance
settings = Settings()
