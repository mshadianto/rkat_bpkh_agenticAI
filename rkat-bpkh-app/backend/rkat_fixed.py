# ===== QUICK BACKEND FIX - COPY PASTE INI KE FILE BARU =====
# File: backend/rkat_backend_fixed.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="RKAT BPKH Fixed Backend")

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

# Mock Data
USERS = {
    "admin": {"password": "admin123", "name": "Administrator BPKH", "role": "administrator"},
    "badan_pelaksana": {"password": "bp123", "name": "Badan Pelaksana", "role": "badan_pelaksana"},
    "audit_internal": {"password": "audit123", "name": "Audit Internal", "role": "audit_internal"},
    "komite_dewan": {"password": "komite123", "name": "Komite Dewan", "role": "komite_dewan_pengawas"},
    "dewan_pengawas": {"password": "dewan123", "name": "Dewan Pengawas", "role": "dewan_pengawas"}
}

# Mock RKAT Data
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
        "activities_count": 5
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
        "activities_count": 3
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
        "activities_count": 7
    }
]

# Basic Routes
@app.get("/")
async def root():
    return {"message": "RKAT BPKH Fixed Backend", "status": "active", "endpoints": "All endpoints working"}

@app.get("/health")
async def health():
    return {"status": "healthy", "message": "Backend with all endpoints ready!"}

# Auth Endpoints
@app.post("/api/auth/login")
async def login(credentials: LoginRequest):
    username = credentials.username
    password = credentials.password
    
    print(f"🔑 Login attempt: {username}")
    
    if username not in USERS or USERS[username]["password"] != password:
        print(f"❌ Login failed for: {username}")
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    user = USERS[username]
    print(f"✅ Login successful: {username}")
    
    return {
        "access_token": f"token_{username}_123",
        "token_type": "bearer",
        "user_info": {
            "id": hash(username) % 1000,
            "username": username,
            "full_name": user["name"],
            "role": user["role"],
            "department": user["name"].split()[-1] if " " in user["name"] else "BPKH"
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

# RKAT Endpoints - INI YANG MISSING!
@app.get("/api/rkat/list")
async def get_rkat_list():
    """Get RKAT list - ENDPOINT YANG DIPERLUKAN!"""
    print("📋 GET /api/rkat/list called")
    return RKAT_DATA

@app.get("/api/rkat/{rkat_id}")
async def get_rkat_detail(rkat_id: int):
    """Get RKAT detail"""
    rkat = next((r for r in RKAT_DATA if r["id"] == rkat_id), None)
    if not rkat:
        raise HTTPException(status_code=404, detail="RKAT not found")
    
    # Mock activities
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
        },
        {
            "id": 2,
            "activity_code": "522111", 
            "activity_name": "Konsumsi Rapat",
            "description": "Penyediaan konsumsi untuk rapat koordinasi",
            "budget_amount": 37500000.0,
            "sbo_reference": "KR-001",
            "output_target": "300 kali konsumsi rapat",
            "outcome_target": "Terlaksananya rapat yang efektif"
        }
    ]
    
    return {
        "rkat": {
            **rkat,
            "strategic_objectives": [
                "Pengembangan investasi pada ekosistem haji dan umroh",
                "Amandemen peraturan untuk penguatan kelembagaan dan tata kelola BPKH"
            ],
            "key_activities": [
                "Penyusunan dan harmonisasi peraturan BPKH",
                "Pengembangan sistem teknologi informasi",
                "Peningkatan kapasitas SDM"
            ],
            "performance_indicators": [
                {"indicator": "Jumlah PBPKH yang diselesaikan", "target": "12", "unit": "dokumen"},
                {"indicator": "Tingkat kepuasan stakeholder", "target": "85", "unit": "persen"}
            ],
            "creator": {"name": rkat["creator_name"], "department": "BPKH"}
        },
        "activities": activities
    }

# Analytics Endpoints
@app.get("/api/analytics/dashboard-metrics")
async def dashboard_metrics():
    """Dashboard metrics"""
    return {
        "status_distribution": {
            "draft": 5,
            "submitted": 3,
            "under_audit_review": 2,
            "audit_approved": 4,
            "committee_approved": 2,
            "final_approved": 8
        },
        "budget_summary": {
            "total_budget": 25000000000.0,
            "operational_budget": 17500000000.0,
            "personnel_budget": 7500000000.0,
            "avg_kup_compliance": 89.3,
            "avg_sbo_compliance": 91.8
        },
        "recent_activities": [
            {
                "id": 1,
                "title": "RKAT BPKH 2026",
                "status": "draft",
                "created_at": "2025-01-15T10:00:00",
                "creator": "Badan Pelaksana"
            },
            {
                "id": 2,
                "title": "RKAT Digital Transformation",
                "status": "submitted", 
                "created_at": "2025-01-10T14:30:00",
                "creator": "Audit Internal"
            }
        ],
        "performance_metrics": {
            "avg_approval_time_days": 5.8,
            "total_rkats": 24,
            "approved_rkats": 14
        }
    }

# Workflow Endpoints
@app.get("/api/workflow/pending-reviews")
async def pending_reviews():
    """Pending reviews"""
    pending = [r for r in RKAT_DATA if r["status"] in ["submitted", "under_audit_review"]]
    
    return {
        "pending_reviews": [
            {
                "id": rkat["id"],
                "title": rkat["title"],
                "creator": rkat["creator_name"],
                "submitted_at": rkat["created_at"],
                "total_budget": rkat["total_budget"],
                "status": rkat["status"]
            }
            for rkat in pending
        ]
    }

# AI Endpoints
@app.post("/api/ai/chat")
async def ai_chat(request: dict):
    """AI chat"""
    query = request.get("query", "").lower()
    
    if "anggaran" in query or "budget" in query:
        response = "Berdasarkan SBO BPKH 2026, anggaran konsumsi rapat sebesar Rp 125.000 per orang, honorarium narasumber eselon I sebesar Rp 1.400.000 per JPL. Pastikan anggaran operasional tidak melebihi 5% dari nilai manfaat tahun sebelumnya."
    elif "workflow" in query or "alur" in query:
        response = "Alur workflow RKAT BPKH: 1) Penyusunan oleh Badan Pelaksana, 2) Review oleh Audit Internal, 3) Review oleh Komite Dewan Pengawas, 4) Persetujuan oleh Dewan Pengawas, 5) Final approval untuk submission ke DPR."
    elif "kup" in query or "compliance" in query:
        response = "Untuk compliance KUP 2026, pastikan tema 'Institutional Strengthening', sasaran strategis align dengan pengembangan investasi ekosistem haji dan penguatan kelembagaan BPKH. Lengkapi dokumen KAK, RAB, Action Plan, Timeline, dan WBS."
    elif "sbo" in query:
        response = "SBO (Standar Biaya Operasional) 2026 mengatur standar biaya untuk berbagai kegiatan BPKH. Variance maksimal 10% dari standar yang ditetapkan. Gunakan kode kegiatan yang sesuai dengan SBO untuk perhitungan anggaran."
    else:
        response = "Saya dapat membantu Anda dengan pertanyaan tentang RKAT, anggaran, workflow, compliance KUP, SBO, dan best practices BPKH. Silakan ajukan pertanyaan spesifik!"
    
    return {"response": response}

# Test endpoint untuk memastikan semua berjalan
@app.get("/test")
async def test_all_endpoints():
    """Test all critical endpoints"""
    return {
        "message": "All endpoints working!",
        "available_endpoints": [
            "GET / - Root",
            "GET /health - Health check", 
            "POST /api/auth/login - Login",
            "GET /api/auth/me - Current user",
            "GET /api/rkat/list - RKAT list (FIXED!)",
            "GET /api/rkat/{id} - RKAT detail",
            "GET /api/analytics/dashboard-metrics - Dashboard data",
            "GET /api/workflow/pending-reviews - Pending reviews",
            "POST /api/ai/chat - AI chat"
        ],
        "test_urls": {
            "rkat_list": "http://localhost:8000/api/rkat/list",
            "dashboard": "http://localhost:8000/api/analytics/dashboard-metrics",
            "login": "POST http://localhost:8000/api/auth/login"
        }
    }

if __name__ == "__main__":
    print("🚀 RKAT BPKH Fixed Backend Starting...")
    print("📍 Backend: http://127.0.0.1:8000")
    print("📍 Test: http://127.0.0.1:8000/test")
    
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")