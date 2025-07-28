# minimal_backend.py - Updated dengan endpoints yang dibutuhkan frontend
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import os

# Initialize FastAPI app
app = FastAPI(
    title="RKAT BPKH API - Minimal",
    description="Backend minimal untuk Sistem RKAT BPKH",
    version="1.0.0"
)

# CORS Configuration - CRITICAL untuk Streamlit Cloud
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://rkat-bpkh-mshadianto.streamlit.app",
        "http://localhost:8501",
        "*"  # Allow all origins for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class LoginRequest(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: str
    username: str
    name: str
    email: str
    role: str
    bidang: str
    permissions: List[str]

# Mock Database
USERS_DB = {
    "admin123": {
        "id": "user_001",
        "username": "admin123",
        "password": "admin123",
        "name": "Administrator BPKH",
        "email": "admin@bpkh.go.id",
        "role": "admin",
        "bidang": "Administrasi",
        "permissions": ["create_rkat", "edit_rkat", "approve_rkat", "view_all"]
    },
    "audit123": {
        "id": "user_002",
        "username": "audit123",
        "password": "audit123",
        "name": "Tim Audit Internal",
        "email": "audit@bpkh.go.id",
        "role": "audit_internal",
        "bidang": "Audit Internal",
        "permissions": ["review_rkat", "view_assigned", "comment_rkat"]
    },
    "komite123": {
        "id": "user_003",
        "username": "komite123",
        "password": "komite123",
        "name": "Komite Dewan Pengawas",
        "email": "komite@bpkh.go.id",
        "role": "komite_dewan_pengawas",
        "bidang": "Dewan Pengawas",
        "permissions": ["review_rkat", "view_assigned", "comment_rkat"]
    },
    "dewan123": {
        "id": "user_004",
        "username": "dewan123",
        "password": "dewan123",
        "name": "Dewan Pengawas",
        "email": "dewan@bpkh.go.id",
        "role": "dewan_pengawas",
        "bidang": "Dewan Pengawas",
        "permissions": ["approve_rkat", "view_all", "final_approval"]
    }
}

# Mock RKAT Data
RKAT_DB = [
    {
        "id": "RKAT-2026-001",
        "judul": "RKAT Audit Internal 2026",
        "bidang": "Audit Internal",
        "pengaju": "Misbah Taufiqurrohman",
        "tanggal_pengajuan": "2025-01-15",
        "total_anggaran": 2500000000,
        "status": "pending_audit_review",
        "progress_percentage": 25
    },
    {
        "id": "RKAT-2026-002", 
        "judul": "RKAT Teknologi Informasi 2026",
        "bidang": "Teknologi Informasi",
        "pengaju": "Emir Rio Krishna",
        "tanggal_pengajuan": "2025-01-10",
        "total_anggaran": 5000000000,
        "status": "approved",
        "progress_percentage": 100
    }
]

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "RKAT BPKH API - Minimal Backend",
        "version": "1.0.0",
        "status": "running",
        "backend_file": "minimal_backend.py",
        "environment": os.getenv("ENVIRONMENT", "production"),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "backend": "minimal_backend.py"
    }

@app.post("/auth/login")
async def login(request: LoginRequest):
    """User authentication"""
    user_data = USERS_DB.get(request.username)
    
    if not user_data or user_data["password"] != request.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
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
    total_rkat = len(RKAT_DB)
    approved_rkat = len([r for r in RKAT_DB if r["status"] == "approved"])
    total_budget = sum(r["total_anggaran"] for r in RKAT_DB)
    
    # Status distribution
    status_distribution = {}
    for rkat in RKAT_DB:
        status = rkat["status"]
        status_distribution[status] = status_distribution.get(status, 0) + 1
    
    return {
        "total_rkat": total_rkat,
        "approved_rkat": approved_rkat,
        "total_budget": total_budget,
        "avg_approval_days": 5.8,  # Mock data
        "status_distribution": status_distribution
    }

@app.get("/rkat/")
async def get_rkat_list():
    """Get list of RKAT"""
    return RKAT_DB

@app.get("/rkat/{rkat_id}")
async def get_rkat_detail(rkat_id: str):
    """Get RKAT detail"""
    rkat = next((r for r in RKAT_DB if r["id"] == rkat_id), None)
    if not rkat:
        raise HTTPException(status_code=404, detail="RKAT not found")
    return rkat

@app.get("/workflow/steps")
async def get_workflow_steps():
    """Get workflow steps"""
    return [
        {
            "step": 1,
            "title": "Pengajuan RKAT",
            "description": "Bidang mengajukan RKAT sesuai KUP & SBO",
            "roles": ["bidang_pengaju"],
            "duration": "1-3 hari"
        },
        {
            "step": 2,
            "title": "Review Audit Internal",
            "description": "Audit Internal melakukan review kelayakan",
            "roles": ["audit_internal"],
            "duration": "5-7 hari"
        },
        {
            "step": 3,
            "title": "Review Komite Dewan",
            "description": "Komite Dewan Pengawas melakukan evaluasi",
            "roles": ["komite_dewan_pengawas"],
            "duration": "3-5 hari"
        },
        {
            "step": 4,
            "title": "Persetujuan Dewan",
            "description": "Dewan Pengawas memberikan persetujuan final",
            "roles": ["dewan_pengawas"],
            "duration": "2-3 hari"
        }
    ]

@app.get("/references/kup")
async def get_kup_references():
    """Get KUP references"""
    return [
        {
            "kup_id": "KUP-AI-2026",
            "title": "Kebijakan Umum Audit Internal 2026",
            "description": "Pedoman penganggaran untuk kegiatan audit internal",
            "budget_limit": 5000000000
        },
        {
            "kup_id": "KUP-TI-2026",
            "title": "Kebijakan Umum Teknologi Informasi 2026", 
            "description": "Pedoman penganggaran untuk transformasi digital",
            "budget_limit": 10000000000
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
            "unit": "per kegiatan"
        },
        {
            "sbo_id": "SBO-TECH-002",
            "category": "Technology Development",
            "standard_cost": 200000000,
            "unit": "per sistem"
        }
    ]

@app.get("/users/me")
async def get_current_user():
    """Get current user info (mock)"""
    return {
        "id": "user_001",
        "name": "Administrator BPKH",
        "role": "admin",
        "bidang": "Administrasi"
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "error": "Endpoint not found",
        "message": f"The requested endpoint does not exist in minimal_backend.py",
        "available_endpoints": [
            "/",
            "/health", 
            "/auth/login",
            "/dashboard/metrics",
            "/rkat/",
            "/workflow/steps",
            "/references/kup",
            "/references/sbo"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
