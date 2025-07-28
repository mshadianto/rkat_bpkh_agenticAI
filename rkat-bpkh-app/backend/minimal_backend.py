# minimal_backend.py - Complete Fixed Version
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
            "GET /api/auth/me - Current user",
            "GET /api/rkat/list - RKAT list",
            "GET /api/rkat/{id} - RKAT detail",
            "GET /api/analytics/dashboard-metrics - Dashboard metrics",
            "GET /api/workflow/pending-reviews - Pending reviews",
            "POST /api/ai/chat - AI chat"
        ]
    }

# Auth Endpoints
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

# RKAT Endpoints
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
    """Complete dashboard metrics with all required fields"""
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
            },
            {
                "id": 3,
                "title": "RKAT Optimisasi Operasional",
                "status": "under_audit_review", 
                "created_at": "2025-01-05T09:15:00",
                "creator": "Komite Dewan"
            }
        ],
        "performance_metrics": {
            "avg_approval_time_days": 5.8,
            "total_rkats": 24,
            "approved_rkats": 14,
            "pending_rkats": 6,
            "rejected_rkats": 4,
            "completion_rate": 85.5,
            "budget_utilization": 78.3,
            "compliance_score": 91.2
        },
        "monthly_trends": {
            "rkat_created": [3, 5, 4, 8, 6, 7],
            "rkat_approved": [2, 4, 3, 6, 5, 6],
            "budget_allocated": [1200000000, 1500000000, 1300000000, 1800000000, 1600000000, 1700000000]
        },
        "compliance_overview": {
            "kup_compliance": 87.5,
            "sbo_compliance": 92.3,
            "documentation_complete": 89.1,
            "workflow_adherence": 94.7
        },
        "top_performers": [
            {"name": "Badan Pelaksana", "score": 94.2, "rkats_completed": 8},
            {"name": "Audit Internal", "score": 91.7, "rkats_completed": 6},
            {"name": "Komite Dewan", "score": 88.9, "rkats_completed": 4}
        ]
    }

# Workflow Endpoints
@app.get("/api/workflow/pending-reviews")
async def pending_reviews():
    pending = [r for r in RKAT_DATA if r["status"] in ["submitted", "under_audit_review"]]
    
    return {
        "pending_reviews": [
            {
                "id": rkat["id"],
                "title": rkat["title"],
                "creator": rkat["creator_name"],
                "submitted_at": rkat["created_at"],
                "total_budget": rkat["total_budget"],
                "status": rkat["status"],
                "priority": "high" if rkat["total_budget"] > 1500000000 else "medium",
                "days_pending": 3
            }
            for rkat in pending
        ],
        "summary": {
            "total_pending": len(pending),
            "high_priority": sum(1 for r in pending if r["total_budget"] > 1500000000),
            "overdue": 1
        }
    }

@app.get("/api/workflow/history/{rkat_id}")
async def workflow_history(rkat_id: int):
    """Get workflow history for specific RKAT"""
    return {
        "workflow_history": [
            {
                "id": 1,
                "action": "created",
                "user": "Badan Pelaksana",
                "timestamp": "2025-01-15T10:00:00",
                "previous_status": None,
                "new_status": "draft",
                "comments": "RKAT dibuat dengan tema Institutional Strengthening"
            },
            {
                "id": 2,
                "action": "submitted",
                "user": "Badan Pelaksana",
                "timestamp": "2025-01-16T14:30:00",
                "previous_status": "draft",
                "new_status": "submitted",
                "comments": "RKAT telah lengkap dan siap untuk review"
            }
        ]
    }

# AI Assistant Endpoints
@app.post("/api/ai/chat")
async def ai_chat(request: dict):
    query = request.get("query", "").lower()
    
    if "anggaran" in query or "budget" in query:
        response = "Berdasarkan SBO BPKH 2026, anggaran konsumsi rapat sebesar Rp 125.000 per orang, honorarium narasumber eselon I sebesar Rp 1.400.000 per JPL. Pastikan anggaran operasional tidak melebihi 5% dari nilai manfaat tahun sebelumnya."
    elif "workflow" in query or "alur" in query:
        response = "Alur workflow RKAT BPKH: 1) Penyusunan oleh Badan Pelaksana, 2) Review oleh Audit Internal, 3) Review oleh Komite Dewan Pengawas, 4) Persetujuan oleh Dewan Pengawas, 5) Final approval untuk submission ke DPR."
    elif "kup" in query or "compliance" in query:
        response = "Untuk compliance KUP 2026, pastikan tema 'Institutional Strengthening', sasaran strategis align dengan pengembangan investasi ekosistem haji dan penguatan kelembagaan BPKH. Lengkapi dokumen KAK, RAB, Action Plan, Timeline, dan WBS."
    elif "sbo" in query:
        response = "SBO (Standar Biaya Operasional) 2026 mengatur standar biaya untuk berbagai kegiatan BPKH. Variance maksimal 10% dari standar yang ditetapkan. Gunakan kode kegiatan yang sesuai dengan SBO untuk perhitungan anggaran."
    elif "status" in query:
        response = "Status RKAT saat ini: 5 draft, 3 submitted, 2 under review, 4 approved. Rata-rata waktu approval 5.8 hari. Tingkat compliance KUP 89.3% dan SBO 91.8%."
    elif "help" in query or "bantuan" in query:
        response = "Saya dapat membantu dengan: 1) Informasi anggaran dan SBO, 2) Workflow dan status RKAT, 3) Compliance KUP dan regulasi, 4) Best practices penyusunan RKAT, 5) Analisis dashboard dan metrics."
    else:
        response = "Saya dapat membantu Anda dengan pertanyaan tentang RKAT, anggaran, workflow, compliance KUP, SBO, dan best practices BPKH. Silakan ajukan pertanyaan spesifik!"
    
    return {
        "response": response,
        "timestamp": "2025-01-28T10:00:00",
        "query_type": "general" if "help" in query else "specific"
    }

# Additional RKAT Management Endpoints
@app.post("/api/rkat/create")
async def create_rkat(rkat_data: dict):
    """Create new RKAT"""
    new_id = max([r["id"] for r in RKAT_DATA]) + 1
    
    new_rkat = {
        "id": new_id,
        "title": rkat_data.get("title", f"RKAT Baru {new_id}"),
        "year": rkat_data.get("year", 2026),
        "status": "draft",
        "total_budget": rkat_data.get("total_budget", 0),
        "operational_budget": rkat_data.get("operational_budget", 0),
        "personnel_budget": rkat_data.get("personnel_budget", 0),
        "kup_compliance_score": 0,
        "sbo_compliance_score": 0,
        "creator_name": rkat_data.get("creator_name", "User"),
        "created_at": "2025-01-28T10:00:00",
        "activities_count": 0,
        "program": rkat_data.get("program", "Program Umum")
    }
    
    RKAT_DATA.append(new_rkat)
    
    return {
        "success": True,
        "message": "RKAT berhasil dibuat",
        "rkat_id": new_id,
        "rkat": new_rkat
    }

@app.put("/api/rkat/{rkat_id}/submit")
async def submit_rkat(rkat_id: int):
    """Submit RKAT for review"""
    rkat = next((r for r in RKAT_DATA if r["id"] == rkat_id), None)
    if not rkat:
        raise HTTPException(status_code=404, detail="RKAT not found")
    
    if rkat["status"] != "draft":
        raise HTTPException(status_code=400, detail="Only draft RKAT can be submitted")
    
    rkat["status"] = "submitted"
    
    return {
        "success": True,
        "message": "RKAT berhasil disubmit untuk review",
        "rkat": rkat
    }

# File Upload Simulation
@app.post("/api/files/upload")
async def upload_file(file_data: dict):
    """Simulate file upload"""
    return {
        "success": True,
        "file_id": "file_123",
        "filename": file_data.get("filename", "document.pdf"),
        "size": file_data.get("size", 1024),
        "upload_date": "2025-01-28T10:00:00"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    
    print("🚀 RKAT BPKH Minimal Backend Starting...")
    print(f"📍 Port: {port}")
    print("📍 Backend ready with all endpoints!")
    print("\n🔑 Login Credentials:")
    for username, data in USERS.items():
        print(f"   • {username} / {data['password']}")
    print("\n✅ ALL ENDPOINTS READY!")
    
    uvicorn.run(app, host="0.0.0.0", port=port)
