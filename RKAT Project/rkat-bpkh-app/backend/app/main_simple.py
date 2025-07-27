from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

# Simple FastAPI app without complex dependencies
app = FastAPI(
    title="RKAT BPKH Management System",
    description="Sistem Manajemen Rencana Kerja dan Anggaran Tahunan BPKH",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_info: dict

# Mock users database
MOCK_USERS = {
    "admin": {
        "password": "admin123",
        "info": {
            "id": 1,
            "username": "admin",
            "full_name": "Administrator BPKH",
            "role": "administrator",
            "department": "IT"
        }
    },
    "badan_pelaksana": {
        "password": "bp123",
        "info": {
            "id": 2,
            "username": "badan_pelaksana",
            "full_name": "Badan Pelaksana",
            "role": "badan_pelaksana",
            "department": "Badan Pelaksana"
        }
    },
    "audit_internal": {
        "password": "audit123",
        "info": {
            "id": 3,
            "username": "audit_internal",
            "full_name": "Audit Internal",
            "role": "audit_internal",
            "department": "Audit Internal"
        }
    },
    "komite_dewan": {
        "password": "komite123",
        "info": {
            "id": 4,
            "username": "komite_dewan",
            "full_name": "Komite Dewan Pengawas",
            "role": "komite_dewan_pengawas",
            "department": "Dewan Pengawas"
        }
    },
    "dewan_pengawas": {
        "password": "dewan123",
        "info": {
            "id": 5,
            "username": "dewan_pengawas",
            "full_name": "Dewan Pengawas",
            "role": "dewan_pengawas",
            "department": "Dewan Pengawas"
        }
    }
}

# Routes
@app.get("/")
async def root():
    return {
        "message": "RKAT BPKH Management System API",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Backend is running successfully"}

@app.post("/api/auth/login")
async def login(user_credentials: UserLogin):
    """Authenticate user and return access token"""
    username = user_credentials.username
    password = user_credentials.password
    
    # Check credentials
    if username not in MOCK_USERS:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    user_data = MOCK_USERS[username]
    if user_data["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Return token (mock)
    return {
        "access_token": f"mock_token_{username}",
        "token_type": "bearer",
        "user_info": user_data["info"]
    }

@app.get("/api/auth/me")
async def get_current_user():
    """Get current user info (mock)"""
    return {
        "id": 1,
        "username": "admin",
        "full_name": "Administrator BPKH",
        "role": "administrator",
        "department": "IT"
    }

@app.get("/api/rkat/list")
async def get_rkat_list():
    """Get RKAT list (mock data)"""
    return [
        {
            "id": 1,
            "title": "RKAT BPKH Tahun 2026",
            "year": 2026,
            "status": "draft",
            "total_budget": 1500000000.0,
            "operational_budget": 1050000000.0,
            "personnel_budget": 450000000.0,
            "kup_compliance_score": 85.5,
            "sbo_compliance_score": 92.3,
            "creator_name": "Badan Pelaksana",
            "created_at": "2025-01-01T00:00:00",
            "activities_count": 3
        }
    ]

@app.get("/api/analytics/dashboard-metrics")
async def get_dashboard_metrics():
    """Get dashboard metrics (mock data)"""
    return {
        "status_distribution": {
            "draft": 5,
            "submitted": 3,
            "under_review": 2,
            "approved": 8
        },
        "budget_summary": {
            "total_budget": 15000000000.0,
            "operational_budget": 10500000000.0,
            "personnel_budget": 4500000000.0,
            "avg_kup_compliance": 87.5,
            "avg_sbo_compliance": 91.2
        },
        "recent_activities": [
            {
                "id": 1,
                "title": "RKAT BPKH 2026",
                "status": "draft",
                "created_at": "2025-01-01T00:00:00",
                "creator": "Badan Pelaksana"
            }
        ],
        "performance_metrics": {
            "avg_approval_time_days": 7.5,
            "total_rkats": 18,
            "approved_rkats": 12
        }
    }

if __name__ == "__main__":
    print("Ì∫Ä Starting RKAT BPKH Backend (Simple Version)...")
    print("Ì≥ç Backend URL: http://localhost:8000")
    print("Ì≥ç Health Check: http://localhost:8000/health")
    print("Ì≥ç API Docs: http://localhost:8000/docs")
    print("Ì≥ç Frontend: http://localhost:8501")
    print("\n‚úÖ Backend ready for connections!")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
