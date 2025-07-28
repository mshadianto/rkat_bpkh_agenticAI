# minimal_backend.py - Lightweight version
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI(title="RKAT BPKH Minimal Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str
    password: str

# Mock Data - Lightweight
USERS = {
    "admin": {"password": "admin123", "name": "Administrator BPKH", "role": "administrator"},
    "badan_pelaksana": {"password": "bp123", "name": "Badan Pelaksana", "role": "badan_pelaksana"},
    "audit_internal": {"password": "audit123", "name": "Audit Internal", "role": "audit_internal"},
    "komite_dewan": {"password": "komite123", "name": "Komite Dewan", "role": "komite_dewan_pengawas"},
    "dewan_pengawas": {"password": "dewan123", "name": "Dewan Pengawas", "role": "dewan_pengawas"}
}

RKAT_DATA = [
    {
        "id": 1,
        "title": "RKAT BPKH Tahun 2026 - Institutional Strengthening",
        "year": 2026,
        "status": "draft",
        "total_budget": 1500000000.0,
        "operational_budget": 1050000000.0,
        "personnel_budget": 450000000.0,
        "kup_compliance_score": 87.5,
        "sbo_compliance_score": 92.3,
        "creator_name": "Badan Pelaksana",
        "created_at": "2025-01-15T10:00:00",
        "activities_count": 5,
        "program": "Program Audit Fungsi Korporasi"
    },
    {
        "id": 2,
        "title": "RKAT Digital Transformation 2026",
        "year": 2026,
        "status": "submitted",
        "total_budget": 2000000000.0,
        "operational_budget": 1400000000.0,
        "personnel_budget": 600000000.0,
        "kup_compliance_score": 91.2,
        "sbo_compliance_score": 88.7,
        "creator_name": "Audit Internal",
        "created_at": "2025-01-10T14:30:00",
        "activities_count": 3,
        "program": "Program Audit Fungsi Bisnis"
    },
    {
        "id": 3,
        "title": "RKAT Optimisasi Operasional Q3 2026",
        "year": 2026,
        "status": "under_audit_review",
        "total_budget": 800000000.0,
        "operational_budget": 560000000.0,
        "personnel_budget": 240000000.0,
        "kup_compliance_score": 89.8,
        "sbo_compliance_score": 94.1,
        "creator_name": "Komite Dewan",
        "created_at": "2025-01-05T09:15:00",
        "activities_count": 7,
        "program": "Program Evaluasi Kinerja"
    }
]

# Basic Routes
@app.get("/")
async def root():
    return {"message": "RKAT BPKH Minimal Backend", "status": "active", "version": "1.0"}

@app.get("/health")
async def health():
    return {"status": "healthy", "message": "Minimal backend ready!"}

@app.get("/test")
async def test():
    return {
        "message": "All endpoints working!",
        "endpoints": [
            "GET / - Root",
            "GET /health - Health check",
            "POST /api/auth/login - Login",
            "GET /api/rkat/list - RKAT list",
            "GET /api/rkat/{id} - RKAT detail"
        ]
    }

# Auth
@app.post("/api/auth/login")
async def login(credentials: LoginRequest):
    username = credentials.username
    password = credentials.password
    
    if username not in USERS or USERS[username]["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = USERS[username]
    return {
        "access_token": f"token_{username}_123",
        "token_type": "bearer",
        "user_info": {
            "id": hash(username) % 1000,
            "username": username,
            "full_name": user["name"],
            "role": user["role"],
            "department": "BPKH"
        }
    }

@app.get("/api/auth/me")
async def get_me():
    return {
        "id": 1,
        "username": "admin",
        "full_name": "Administrator BPKH",
        "role": "administrator",
        "department": "IT"
    }

# RKAT
@app.get("/api/rkat/list")
async def get_rkat_list():
    return RKAT_DATA

@app.get("/api/rkat/{rkat_id}")
async def get_rkat_detail(rkat_id: int):
    rkat = next((r for r in RKAT_DATA if r["id"] == rkat_id), None)
    if not rkat:
        raise HTTPException(status_code=404, detail="RKAT not found")
    
    activities = [
        {
            "id": 1,
            "activity_code": "010101",
            "activity_name": "Pembentukan Peraturan",
            "description": "Penyusunan dan harmonisasi PBPKH/PKBP",
            "budget_amount": 1351555220.0,
            "sbo_reference": "PBPKH-001",
            "output_target": "12 PBPKH/PKBP",
            "outcome_target": "Meningkatnya tata kelola peraturan BPKH"
        }
    ]
    
    return {
        "rkat": {
            **rkat,
            "strategic_objectives": [
                "Pengembangan investasi pada ekosistem haji dan umroh",
                "Amandemen peraturan untuk penguatan kelembagaan BPKH"
            ],
            "key_activities": [
                "Penyusunan dan harmonisasi peraturan BPKH",
                "Pengembangan sistem teknologi informasi"
            ],
            "performance_indicators": [
                {"indicator": "Jumlah PBPKH", "target": "12", "unit": "dokumen"}
            ],
            "creator": {"name": rkat["creator_name"], "department": "BPKH"}
        },
        "activities": activities
    }

# Analytics
@app.get("/api/analytics/dashboard-metrics")
async def dashboard_metrics():
    return {
        "status_distribution": {
            "draft": 5,
            "submitted": 3,
            "under_audit_review": 2,
            "audit_approved": 4,
            "final_approved": 8
        },
        "budget_summary": {
            "total_budget": 25000000000.0,
            "operational_budget": 17500000000.0,
            "personnel_budget": 7500000000.0,
            "avg_kup_compliance": 89.3,
            "avg_sbo_compliance": 91.8
        }
    }

@app.get("/api/workflow/pending-reviews")
async def pending_reviews():
    pending = [r for r in RKAT_DATA if r["status"] in ["submitted", "under_audit_review"]]
    return {"pending_reviews": pending}

@app.post("/api/ai/chat")
async def ai_chat(request: dict):
    query = request.get("query", "").lower()
    
    if "anggaran" in query:
        response = "Berdasarkan SBO BPKH 2026, standar biaya operasional sudah ditetapkan."
    elif "workflow" in query:
        response = "Alur RKAT: Penyusunan → Review Audit → Review Komite → Persetujuan Dewan."
    else:
        response = "Saya dapat membantu dengan pertanyaan RKAT, anggaran, dan workflow BPKH."
    
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
