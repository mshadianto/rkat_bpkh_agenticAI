import os
from typing import Dict, Any

class Settings:
    # API Configuration
    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
    
    # Application Configuration
    APP_TITLE = "RKAT BPKH Management System"
    APP_ICON = "🏛️"
    LAYOUT = "wide"
    
    # UI Configuration
    SIDEBAR_DEFAULT_EXPANDED = True
    
    # File Upload Configuration
    MAX_FILE_SIZE_MB = 50
    ALLOWED_FILE_TYPES = ['pdf', 'doc', 'docx', 'xls', 'xlsx']
    
    # User Roles
    USER_ROLES = {
        "badan_pelaksana": "Badan Pelaksana",
        "audit_internal": "Audit Internal", 
        "komite_dewan_pengawas": "Komite Dewan Pengawas",
        "dewan_pengawas": "Dewan Pengawas",
        "administrator": "Administrator"
    }
    
    # RKAT Status
    RKAT_STATUS = {
        "draft": "Draft",
        "submitted": "Disubmit",
        "under_audit_review": "Review Audit Internal",
        "audit_approved": "Disetujui Audit",
        "audit_rejected": "Ditolak Audit",
        "under_committee_review": "Review Komite",
        "committee_approved": "Disetujui Komite", 
        "committee_rejected": "Ditolak Komite",
        "under_board_review": "Review Dewan Pengawas",
        "board_approved": "Disetujui Dewan",
        "board_rejected": "Ditolak Dewan",
        "final_approved": "Final Approved"
    }
    
    # Colors
    COLORS = {
        "primary": "#1f77b4",
        "secondary": "#ff7f0e", 
        "success": "#2ca02c",
        "warning": "#ff7f0e",
        "danger": "#d62728",
        "info": "#17a2b8"
    }

settings = Settings()