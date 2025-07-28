# rkat_fixed.py - Updated dengan /api prefix support
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

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://rkat-bpkh-mshadianto.streamlit.app",
        "http://localhost:8501",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models (same as before)
class LoginRequest(BaseModel):
    username: str
    password: str

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
    }
}

# Sample RKAT Data - untuk mengatasi list kosong
RKAT_DB = {
    "RKAT-2026-001": {
        "id": "RKAT-2026-001",
        "judul": "RKAT Audit Internal 2026",
        "bidang": "Audit Internal",
        "divisi": "Audit Internal 1",
        "program": "Program Audit Fungsi Korporasi",
        "pengaju": "Misbah Taufiqurrohman",
        "tahun_anggaran": 2026,
        "tanggal_pengajuan": "2025-01-15",
        "total_anggaran": 2500000000,
        "status": "pending_audit_review",
        "progress_percentage": 25,
        "latar_belakang": "Mendukung penyelenggaraan fungsi audit internal BPKH",
        "tujuan": "Meningkatkan efektivitas audit internal",
        "sasaran": "Terwujudnya good governance"
    },
    "RKAT-2026-002": {
        "id": "RKAT-2026-002",
        "judul": "RKAT Teknologi Informasi 2026", 
        "bidang": "Teknologi Informasi",
        "divisi": "Pengembangan TI",
        "program": "Program Transformasi Digital",
        "pengaju": "Emir Rio Krishna",
        "tahun_anggaran": 2026,
        "tanggal_pengajuan": "2025-01-10",
        "total_anggaran": 5000000000,
        "status": "approved",
        "progress_percentage": 100,
        "latar_belakang": "Mendukung transformasi digital BPKH",
        "tujuan": "Meningkatkan efisiensi sistem IT",
        "sasaran": "Sistem terintegrasi dan modern"
    }
}

# Original Endpoints (keeping backward compatibility)
@app.get("/")
async def root():
    return {
        "message": "RKAT BPKH API - Fixed Backend",
        "version": "2.0.0", 
        "status": "running",
        "backend_file": "rkat_fixed.py",
        "environment": os.getenv("ENVIRONMENT", "production"),
        "timestamp": datetime.now().isoformat(),
        "available_endpoints": {
            "original": ["/", "/health", "/auth/login", "/dashboard/metrics", "/rkat/", "/workflow/steps"],
            "api_prefix": ["/api/rkat/list", "/api/rkat/{id}", "/api/dashboard/metrics", "/api/auth/login"]
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "backend": "rkat_fixed.py (with /api support)",
        "timestamp": datetime.now().isoformat(),
        "database": "in-memory",
        "rkat_count": len(RKAT_DB)
    }

@app.post("/auth/login")
async def login(request: LoginRequest):
    user_data = USERS_DB.get(request.username)
    if not user_data or user_data["password"] != request.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user_response = {k: v for k, v in user_data.items() if k != "password"}
    return {
        "access_token": f"mock_token_{request.username}",
        "token_type": "bearer",
        "user": user_response
    }

@app.get("/dashboard/metrics")
async def get_dashboard_metrics():
    total_rkat = len(RKAT_DB)
    approved_rkat = len([r for r in RKAT_DB.values() if r.get("status") == "approved"])
    total_budget = sum(r.get("total_anggaran", 0) for r in RKAT_DB.values())
    
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
    """Original endpoint - return list of RKAT"""
    return list(RKAT_DB.values())

@app.get("/rkat/{rkat_id}")
async def get_rkat_detail(rkat_id: str):
    if rkat_id not in RKAT_DB:
        raise HTTPException(status_code=404, detail="RKAT not found")
    return RKAT_DB[rkat_id]

@app.get("/workflow/steps")
async def get_workflow_steps():
    return [
        {
            "step": 1,
            "title": "Pengajuan RKAT",
            "description": "Bidang mengajukan RKAT sesuai KUP & SBO",
            "roles": ["bidang_pengaju"]
        },
        {
            "step": 2,
            "title": "Review Audit Internal",
            "description": "Audit Internal melakukan review kelayakan",
            "roles": ["audit_internal"]
        },
        {
            "step": 3,
            "title": "Review Komite Dewan",
            "description": "Komite Dewan Pengawas melakukan evaluasi",
            "roles": ["komite_dewan_pengawas"]
        },
        {
            "step": 4,
            "title": "Persetujuan Dewan",
            "description": "Dewan Pengawas memberikan persetujuan final",
            "roles": ["dewan_pengawas"]
        }
    ]

# NEW: /api prefix endpoints untuk compatibility dengan frontend yang sudah ada
@app.post("/api/auth/login")
async def api_login(request: LoginRequest):
    """API prefixed login endpoint"""
    return await login(request)

@app.get("/api/dashboard/metrics")
async def api_get_dashboard_metrics():
    """API prefixed dashboard metrics"""
    return await get_dashboard_metrics()

@app.get("/api/rkat/list")
async def api_get_rkat_list():
    """API prefixed RKAT list - FIXED endpoint yang dicari frontend"""
    return list(RKAT_DB.values())

@app.get("/api/rkat/{rkat_id}")
async def api_get_rkat_detail(rkat_id: str):
    """API prefixed RKAT detail"""
    return await get_rkat_detail(rkat_id)

@app.get("/api/workflow/steps")
async def api_get_workflow_steps():
    """API prefixed workflow steps"""
    return await get_workflow_steps()

@app.get("/references/kup")
async def get_kup_references():
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

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
