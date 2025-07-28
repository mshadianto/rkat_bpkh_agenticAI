# rkat_fixed.py - Clean backend tanpa streamlit imports
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from enum import Enum
import uuid
import json
import os

# Initialize FastAPI app
app = FastAPI(
    title="RKAT BPKH API",
    description="Sistem Rencana Kerja dan Anggaran Tahunan - Badan Pengelola Keuangan Haji",
    version="2.0.0"
)

# CORS Configuration - CRITICAL untuk Streamlit Cloud
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://rkat-bpkh-mshadianto.streamlit.app",
        "http://localhost:8501",
        "*"  # Allow all for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Enums for Status
class RKATStatus(str, Enum):
    DRAFT = "draft"
    PENDING_AUDIT_REVIEW = "pending_audit_review"
    AUDIT_REVIEWED = "audit_reviewed"
    PENDING_KOMITE_REVIEW = "pending_komite_review"
    KOMITE_REVIEWED = "komite_reviewed"
    PENDING_DEWAN_APPROVAL = "pending_dewan_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    REVISION_NEEDED = "revision_needed"

class UserRole(str, Enum):
    ADMIN = "admin"
    BIDANG_PENGAJU = "bidang_pengaju"
    AUDIT_INTERNAL = "audit_internal"
    KOMITE_DEWAN_PENGAWAS = "komite_dewan_pengawas"
    DEWAN_PENGAWAS = "dewan_pengawas"

# Data Models
class User(BaseModel):
    id: str
    username: str
    name: str
    email: str
    role: UserRole
    bidang: Optional[str] = None
    permissions: List[str]

class LoginRequest(BaseModel):
    username: str
    password: str

class Comment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    user_name: str
    message: str
    created_at: datetime = Field(default_factory=datetime.now)

class RKAT(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    judul: str
    bidang: str
    divisi: str
    program: str
    pengaju_id: str
    pengaju_name: str
    tahun_anggaran: int
    tanggal_pengajuan: datetime = Field(default_factory=datetime.now)
    tanggal_update: datetime = Field(default_factory=datetime.now)
    total_anggaran: float
    latar_belakang: str
    tujuan: str
    sasaran: str
    kup_references: List[str]
    sbo_references: List[str]
    status: RKATStatus = RKATStatus.DRAFT
    progress_percentage: int = 0
    comments: List[Comment] = []

# In-Memory Database
USERS_DB = {
    "admin123": {
        "id": "user_001",
        "username": "admin123",
        "password": "admin123",
        "name": "Administrator BPKH",
        "email": "admin@bpkh.go.id",
        "role": UserRole.ADMIN,
        "bidang": "Administrasi",
        "permissions": ["create_rkat", "edit_rkat", "approve_rkat", "view_all", "manage_users"]
    },
    "audit123": {
        "id": "user_002",
        "username": "audit123",
        "password": "audit123",
        "name": "Tim Audit Internal",
        "email": "audit@bpkh.go.id",
        "role": UserRole.AUDIT_INTERNAL,
        "bidang": "Audit Internal",
        "permissions": ["review_rkat", "view_assigned", "comment_rkat"]
    },
    "komite123": {
        "id": "user_003",
        "username": "komite123",
        "password": "komite123",
        "name": "Komite Dewan Pengawas",
        "email": "komite@bpkh.go.id",
        "role": UserRole.KOMITE_DEWAN_PENGAWAS,
        "bidang": "Dewan Pengawas",
        "permissions": ["review_rkat", "view_assigned", "comment_rkat"]
    },
    "dewan123": {
        "id": "user_004",
        "username": "dewan123",
        "password": "dewan123",
        "name": "Dewan Pengawas",
        "email": "dewan@bpkh.go.id",
        "role": UserRole.DEWAN_PENGAWAS,
        "bidang": "Dewan Pengawas",
        "permissions": ["approve_rkat", "view_all", "final_approval"]
    },
    "bidang_ti": {
        "id": "user_005",
        "username": "bidang_ti",
        "password": "ti123",
        "name": "Emir Rio Krishna",
        "email": "ti@bpkh.go.id",
        "role": UserRole.BIDANG_PENGAJU,
        "bidang": "Teknologi Informasi",
        "permissions": ["create_rkat", "edit_own_rkat", "view_own"]
    }
}

# Sample RKAT Data
RKAT_DB = {}

# Helper Functions
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Mock authentication - replace with real JWT validation"""
    # For demo purposes, return admin user
    user_data = USERS_DB["admin123"]
    return User(**user_data)

def calculate_progress(rkat: RKAT) -> int:
    """Calculate progress percentage based on status"""
    progress_map = {
        RKATStatus.DRAFT: 0,
        RKATStatus.PENDING_AUDIT_REVIEW: 10,
        RKATStatus.AUDIT_REVIEWED: 30,
        RKATStatus.PENDING_KOMITE_REVIEW: 50,
        RKATStatus.KOMITE_REVIEWED: 70,
        RKATStatus.PENDING_DEWAN_APPROVAL: 85,
        RKATStatus.APPROVED: 100,
        RKATStatus.REJECTED: 0,
        RKATStatus.REVISION_NEEDED: 25
    }
    return progress_map.get(rkat.status, 0)

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "RKAT BPKH API - Fixed Backend", 
        "version": "2.0.0",
        "status": "running",
        "backend_file": "rkat_fixed.py",
        "environment": os.getenv("ENVIRONMENT", "production"),
        "timestamp": datetime.now().isoformat(),
        "endpoints": [
            "/health",
            "/auth/login", 
            "/dashboard/metrics",
            "/rkat/",
            "/workflow/steps",
            "/references/kup",
            "/references/sbo"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "backend": "rkat_fixed.py (cleaned)",
        "timestamp": datetime.now().isoformat(),
        "database": "in-memory",
        "users_count": len(USERS_DB),
        "rkat_count": len(RKAT_DB)
    }

@app.post("/auth/login")
async def login(request: LoginRequest):
    """User authentication"""
    user_data = USERS_DB.get(request.username)
    if not user_data or user_data["password"] != request.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Remove password from response
    user_response = {k: v for k, v in user_data.items() if k != "password"}
    
    return {
        "access_token": f"mock_token_{request.username}",
        "token_type": "bearer",
        "user": user_response
    }

@app.get("/dashboard/metrics")
async def get_dashboard_metrics():
    """Get dashboard metrics"""
    # Add some sample data if empty
    if not RKAT_DB:
        sample_rkat = {
            "id": "RKAT-2026-001",
            "judul": "RKAT Audit Internal 2026",
            "bidang": "Audit Internal",
            "status": "pending_audit_review",
            "total_anggaran": 2500000000,
            "progress_percentage": 25
        }
        RKAT_DB["RKAT-2026-001"] = sample_rkat
        
        sample_rkat2 = {
            "id": "RKAT-2026-002",
            "judul": "RKAT Teknologi Informasi 2026", 
            "bidang": "Teknologi Informasi",
            "status": "approved",
            "total_anggaran": 5000000000,
            "progress_percentage": 100
        }
        RKAT_DB["RKAT-2026-002"] = sample_rkat2
    
    total_rkat = len(RKAT_DB)
    approved_rkat = len([r for r in RKAT_DB.values() if r.get("status") == "approved"])
    total_budget = sum(r.get("total_anggaran", 0) for r in RKAT_DB.values())
    
    # Status distribution
    status_distribution = {}
    for rkat in RKAT_DB.values():
        status = rkat.get("status", "draft")
        status_distribution[status] = status_distribution.get(status, 0) + 1
    
    return {
        "total_rkat": total_rkat,
        "approved_rkat": approved_rkat,
        "total_budget": total_budget,
        "avg_approval_days": 5.8,
        "status_distribution": status_distribution
    }

@app.get("/rkat/")
async def get_rkat_list():
    """Get list of RKAT"""
    return list(RKAT_DB.values())

@app.get("/rkat/{rkat_id}")
async def get_rkat_detail(rkat_id: str):
    """Get RKAT detail"""
    if rkat_id not in RKAT_DB:
        raise HTTPException(status_code=404, detail="RKAT not found")
    return RKAT_DB[rkat_id]

@app.get("/workflow/steps")
async def get_workflow_steps():
    """Get workflow steps information"""
    return [
        {
            "step": 1,
            "title": "Pengajuan RKAT",
            "description": "Bidang mengajukan RKAT sesuai KUP & SBO",
            "roles": ["bidang_pengaju"],
            "actions": ["create", "submit"]
        },
        {
            "step": 2,
            "title": "Review Audit Internal",
            "description": "Audit Internal melakukan review kelayakan",
            "roles": ["audit_internal"],
            "actions": ["review", "approve", "reject", "request_revision"]
        },
        {
            "step": 3,
            "title": "Review Komite Dewan",
            "description": "Komite Dewan Pengawas melakukan evaluasi",
            "roles": ["komite_dewan_pengawas"],
            "actions": ["review", "approve", "reject", "request_revision"]
        },
        {
            "step": 4,
            "title": "Persetujuan Dewan",
            "description": "Dewan Pengawas memberikan persetujuan final",
            "roles": ["dewan_pengawas"],
            "actions": ["approve", "reject"]
        }
    ]

@app.get("/references/kup")
async def get_kup_references():
    """Get KUP references"""
    return [
        {
            "kup_id": "KUP-AI-2026",
            "title": "Kebijakan Umum Audit Internal 2026",
            "description": "Pedoman penganggaran untuk kegiatan audit internal dan tata kelola",
            "budget_limit": 5000000000,
            "validity_period": "2026"
        },
        {
            "kup_id": "KUP-TI-2026", 
            "title": "Kebijakan Umum Teknologi Informasi 2026",
            "description": "Pedoman penganggaran untuk transformasi digital dan IT",
            "budget_limit": 10000000000,
            "validity_period": "2026"
        }
    ]

@app.get("/references/sbo")
async def get_sbo_references():
    """Get SBO references"""
    return [
        {
            "sbo_id": "SBO-CORP-001",
            "category": "Audit & Corporate Governance",
            "standard_cost": 50000000,
            "unit": "per kegiatan",
            "description": "Standar biaya untuk kegiatan audit dan tata kelola perusahaan"
        },
        {
            "sbo_id": "SBO-TECH-002",
            "category": "Technology Development",
            "standard_cost": 200000000,
            "unit": "per sistem",
            "description": "Standar biaya pengembangan sistem dan aplikasi"
        }
    ]

@app.get("/users/me")
async def get_current_user_info():
    """Get current user information"""
    return {
        "id": "user_001",
        "name": "Administrator BPKH",
        "role": "admin",
        "bidang": "Administrasi"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
