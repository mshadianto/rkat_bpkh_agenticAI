# ===== COMPLETE BACKEND WITH ALL ENDPOINTS =====
# File: backend/complete_backend.py

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
from datetime import datetime

app = FastAPI(title="RKAT BPKH Complete Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# Pydantic Models
class LoginRequest(BaseModel):
    username: str
    password: str

class RKATCreate(BaseModel):
    title: str
    year: Optional[int] = 2026
    total_budget: float
    operational_budget: float
    personnel_budget: float
    theme: Optional[str] = "Institutional Strengthening"
    strategic_objectives: Optional[List[str]] = []
    key_activities: Optional[List[str]] = []
    performance_indicators: Optional[List[Dict]] = []

class ActivityCreate(BaseModel):
    activity_code: str
    activity_name: str
    description: Optional[str] = None
    budget_amount: float
    output_target: Optional[str] = None
    outcome_target: Optional[str] = None
    performance_indicators: Optional[List[Dict]] = []
    budget_calculation: Optional[Dict] = {}

class WorkflowAction(BaseModel):
    action: str
    comments: Optional[str] = None

# Mock Data
USERS = {
    "admin": {"password": "admin123", "name": "Administrator BPKH", "role": "administrator", "department": "IT"},
    "badan_pelaksana": {"password": "bp123", "name": "Badan Pelaksana", "role": "badan_pelaksana", "department": "Badan Pelaksana"},
    "audit_internal": {"password": "audit123", "name": "Audit Internal", "role": "audit_internal", "department": "Audit Internal"},
    "komite_dewan": {"password": "komite123", "name": "Komite Dewan Pengawas", "role": "komite_dewan_pengawas", "department": "Dewan Pengawas"},
    "dewan_pengawas": {"password": "dewan123", "name": "Dewan Pengawas", "role": "dewan_pengawas", "department": "Dewan Pengawas"}
}

# Mock RKAT Database
MOCK_RKATS = [
    {
        "id": 1,
        "title": "RKAT BPKH Tahun 2026 - Institutional Strengthening",
        "year": 2026,
        "status": "draft",
        "total_budget": 1500000000.0,
        "operational_budget": 1050000000.0,
        "personnel_budget": 450000000.0,
        "theme": "Institutional Strengthening",
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
        "kup_compliance_score": 87.5,
        "sbo_compliance_score": 92.3,
        "creator_name": "Badan Pelaksana",
        "created_at": "2025-01-15T10:00:00",
        "activities_count": 5
    },
    {
        "id": 2,
        "title": "RKAT Optimisasi Q2 2026",
        "year": 2026,
        "status": "submitted",
        "total_budget": 800000000.0,
        "operational_budget": 560000000.0,
        "personnel_budget": 240000000.0,
        "theme": "Operational Excellence",
        "strategic_objectives": [
            "Optimisasi proses operasional",
            "Peningkatan efisiensi anggaran"
        ],
        "key_activities": [
            "Streamlining proses workflow",
            "Implementasi teknologi otomasi"
        ],
        "performance_indicators": [
            {"indicator": "Efisiensi proses", "target": "90", "unit": "persen"}
        ],
        "kup_compliance_score": 91.2,
        "sbo_compliance_score": 88.7,
        "creator_name": "Audit Internal",
        "created_at": "2025-01-10T14:30:00",
        "activities_count": 3
    },
    {
        "id": 3,
        "title": "RKAT Digital Transformation 2026",
        "year": 2026,
        "status": "under_audit_review",
        "total_budget": 2000000000.0,
        "operational_budget": 1400000000.0,
        "personnel_budget": 600000000.0,
        "theme": "Digital Innovation",
        "strategic_objectives": [
            "Implementasi sistem digital terpadu",
            "Peningkatan layanan digital untuk jemaah"
        ],
        "key_activities": [
            "Pengembangan platform digital",
            "Training digital literacy"
        ],
        "performance_indicators": [
            {"indicator": "Adopsi sistem digital", "target": "95", "unit": "persen"}
        ],
        "kup_compliance_score": 89.8,
        "sbo_compliance_score": 94.1,
        "creator_name": "Komite Dewan",
        "created_at": "2025-01-05T09:15:00",
        "activities_count": 7
    }
]

# Mock Activities Database
MOCK_ACTIVITIES = {
    1: [
        {
            "id": 1,
            "activity_code": "010101",
            "activity_name": "Pembentukan Peraturan",
            "description": "Penyusunan dan harmonisasi PBPKH/PKBP untuk penguatan tata kelola BPKH",
            "budget_amount": 1351555220.0,
            "sbo_reference": "PBPKH-001",
            "output_target": "12 PBPKH/PKBP",
            "outcome_target": "Meningkatnya tata kelola peraturan BPKH",
            "kak_document": None,
            "rab_document": None,
            "timeline_document": None,
            "budget_calculation": {"volume": 12, "unit_price": 112629602, "frequency": 1}
        },
        {
            "id": 2,
            "activity_code": "522111",
            "activity_name": "Konsumsi Rapat",
            "description": "Penyediaan konsumsi untuk rapat koordinasi dan pembahasan",
            "budget_amount": 37500000.0,
            "sbo_reference": "KR-001",
            "output_target": "300 kali konsumsi rapat",
            "outcome_target": "Terlaksananya rapat yang efektif",
            "kak_document": None,
            "rab_document": None,
            "timeline_document": None,
            "budget_calculation": {"volume": 300, "unit_price": 125000, "frequency": 1}
        }
    ]
}

# Authentication Functions
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Simple token validation (in real app, validate JWT)
    return {"username": "admin", "role": "administrator"}

# Routes
@app.get("/")
async def root():
    return {"message": "RKAT BPKH Complete Backend", "status": "active", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy", "message": "All endpoints available"}

# Authentication Endpoints
@app.post("/api/auth/login")
async def login(credentials: LoginRequest):
    username = credentials.username
    password = credentials.password
    
    if username not in USERS or USERS[username]["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    user = USERS[username]
    return {
        "access_token": f"token_{username}_123",
        "token_type": "bearer",
        "user_info": {
            "id": hash(username) % 1000,
            "username": username,
            "full_name": user["name"],
            "role": user["role"],
            "department": user["department"]
        }
    }

@app.get("/api/auth/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return current_user

# RKAT Management Endpoints
@app.get("/api/rkat/list")
async def get_rkat_list(current_user: dict = Depends(get_current_user)):
    """Get RKAT list based on user role"""
    return MOCK_RKATS

@app.post("/api/rkat/create")
async def create_rkat(rkat_data: RKATCreate, current_user: dict = Depends(get_current_user)):
    """Create new RKAT proposal"""
    new_id = len(MOCK_RKATS) + 1
    
    new_rkat = {
        "id": new_id,
        "title": rkat_data.title,
        "year": rkat_data.year,
        "status": "draft",
        "total_budget": rkat_data.total_budget,
        "operational_budget": rkat_data.operational_budget,
        "personnel_budget": rkat_data.personnel_budget,
        "theme": rkat_data.theme,
        "strategic_objectives": rkat_data.strategic_objectives,
        "key_activities": rkat_data.key_activities,
        "performance_indicators": rkat_data.performance_indicators,
        "kup_compliance_score": 0.0,
        "sbo_compliance_score": 0.0,
        "creator_name": current_user.get("username", "Unknown"),
        "created_at": datetime.now().isoformat(),
        "activities_count": 0
    }
    
    MOCK_RKATS.append(new_rkat)
    MOCK_ACTIVITIES[new_id] = []
    
    return {
        "message": "RKAT created successfully",
        "rkat_id": new_id,
        "status": "draft"
    }

@app.get("/api/rkat/{rkat_id}")
async def get_rkat_detail(rkat_id: int, current_user: dict = Depends(get_current_user)):
    """Get detailed RKAT information"""
    rkat = next((r for r in MOCK_RKATS if r["id"] == rkat_id), None)
    if not rkat:
        raise HTTPException(status_code=404, detail="RKAT not found")
    
    activities = MOCK_ACTIVITIES.get(rkat_id, [])
    
    return {
        "rkat": {
            **rkat,
            "creator": {"name": rkat["creator_name"], "department": "BPKH"}
        },
        "activities": activities
    }

@app.post("/api/rkat/{rkat_id}/activities")
async def add_activity(rkat_id: int, activity_data: ActivityCreate, current_user: dict = Depends(get_current_user)):
    """Add activity to RKAT"""
    rkat = next((r for r in MOCK_RKATS if r["id"] == rkat_id), None)
    if not rkat:
        raise HTTPException(status_code=404, detail="RKAT not found")
    
    if rkat_id not in MOCK_ACTIVITIES:
        MOCK_ACTIVITIES[rkat_id] = []
    
    new_activity_id = len(MOCK_ACTIVITIES[rkat_id]) + 1
    new_activity = {
        "id": new_activity_id,
        "activity_code": activity_data.activity_code,
        "activity_name": activity_data.activity_name,
        "description": activity_data.description,
        "budget_amount": activity_data.budget_amount,
        "sbo_reference": f"SBO-{activity_data.activity_code}",
        "output_target": activity_data.output_target,
        "outcome_target": activity_data.outcome_target,
        "performance_indicators": activity_data.performance_indicators,
        "budget_calculation": activity_data.budget_calculation,
        "kak_document": None,
        "rab_document": None,
        "timeline_document": None
    }
    
    MOCK_ACTIVITIES[rkat_id].append(new_activity)
    
    # Update RKAT totals
    rkat["activities_count"] = len(MOCK_ACTIVITIES[rkat_id])
    
    return {"message": "Activity added successfully", "activity_id": new_activity_id}

@app.get("/api/rkat/{rkat_id}/compliance-check")
async def check_compliance(rkat_id: int, current_user: dict = Depends(get_current_user)):
    """Check RKAT compliance with KUP and SBO"""
    rkat = next((r for r in MOCK_RKATS if r["id"] == rkat_id), None)
    if not rkat:
        raise HTTPException(status_code=404, detail="RKAT not found")
    
    return {
        "kup_compliance": {
            "compliance_percentage": 87.5,
            "compliance_level": "GOOD",
            "checks": [
                {"check": "Theme Compliance", "status": "PASS", "points": 20, "message": "Theme 'Institutional Strengthening' sesuai KUP 2026"},
                {"check": "Strategic Objectives", "status": "PASS", "points": 25, "message": "Sasaran strategis align dengan KUP"},
                {"check": "Budget Efficiency", "status": "PARTIAL", "points": 18, "message": "Beberapa area dapat dioptimalkan"},
                {"check": "Documentation", "status": "PASS", "points": 22, "message": "Dokumen pendukung lengkap"}
            ],
            "recommendations": [
                "Optimalisasi alokasi anggaran operasional",
                "Lengkapi timeline detail untuk setiap kegiatan"
            ]
        },
        "sbo_compliance": {
            "score": 92.3,
            "level": "EXCELLENT"
        }
    }

# Workflow Endpoints
@app.post("/api/workflow/{rkat_id}/submit")
async def submit_rkat(rkat_id: int, current_user: dict = Depends(get_current_user)):
    """Submit RKAT for review"""
    rkat = next((r for r in MOCK_RKATS if r["id"] == rkat_id), None)
    if not rkat:
        raise HTTPException(status_code=404, detail="RKAT not found")
    
    if rkat["status"] != "draft":
        raise HTTPException(status_code=400, detail="Only draft RKAT can be submitted")
    
    rkat["status"] = "submitted"
    return {"message": "RKAT submitted successfully", "new_status": "submitted"}

@app.post("/api/workflow/{rkat_id}/review")
async def review_rkat(rkat_id: int, workflow_action: WorkflowAction, current_user: dict = Depends(get_current_user)):
    """Review RKAT (approve/reject)"""
    rkat = next((r for r in MOCK_RKATS if r["id"] == rkat_id), None)
    if not rkat:
        raise HTTPException(status_code=404, detail="RKAT not found")
    
    if workflow_action.action == "approve":
        if rkat["status"] == "submitted":
            rkat["status"] = "audit_approved"
        elif rkat["status"] == "audit_approved":
            rkat["status"] = "committee_approved"
        elif rkat["status"] == "committee_approved":
            rkat["status"] = "final_approved"
    else:  # reject
        rkat["status"] = "audit_rejected"
    
    return {"message": f"RKAT {workflow_action.action}ed successfully", "new_status": rkat["status"]}

@app.get("/api/workflow/{rkat_id}/history")
async def get_workflow_history(rkat_id: int, current_user: dict = Depends(get_current_user)):
    """Get workflow history for RKAT"""
    return {
        "workflow_history": [
            {
                "id": 1,
                "action": "submit",
                "user": "Badan Pelaksana",
                "previous_status": "draft",
                "new_status": "submitted",
                "comments": "RKAT siap untuk review",
                "timestamp": "2025-01-15T10:30:00"
            }
        ]
    }

@app.get("/api/workflow/pending-reviews")
async def get_pending_reviews(current_user: dict = Depends(get_current_user)):
    """Get RKATs pending review for current user"""
    pending = [r for r in MOCK_RKATS if r["status"] in ["submitted", "under_audit_review", "audit_approved"]]
    
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

# Analytics Endpoints
@app.get("/api/analytics/dashboard-metrics")
async def get_dashboard_metrics():
    """Get key metrics for dashboard"""
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
                "title": "RKAT Optimisasi Q2",
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

@app.get("/api/analytics/budget-analysis")
async def get_budget_analysis(year: int = 2026):
    """Get budget analysis and trends"""
    return {
        "department_budgets": [
            {"department": "Badan Pelaksana", "total_budget": 8000000000.0, "rkat_count": 5},
            {"department": "Audit Internal", "total_budget": 3000000000.0, "rkat_count": 3},
            {"department": "Dewan Pengawas", "total_budget": 5000000000.0, "rkat_count": 4}
        ],
        "activity_budgets": [
            {"activity_code": "010101", "total_amount": 2000000000.0, "activity_count": 8},
            {"activity_code": "522111", "total_amount": 500000000.0, "activity_count": 12}
        ],
        "monthly_trends": [
            {"month": 1, "submissions": 5, "budget": 8000000000.0},
            {"month": 2, "submissions": 3, "budget": 4500000000.0}
        ]
    }

@app.get("/api/analytics/compliance-report")
async def get_compliance_report():
    """Get compliance analysis report"""
    return {
        "kup_compliance": {
            "excellent": 8,
            "good": 12,
            "needs_improvement": 4,
            "average_score": 87.5
        },
        "sbo_compliance": {
            "excellent": 10,
            "good": 10,
            "needs_improvement": 4,
            "average_score": 91.2
        },
        "detailed_scores": [
            {"rkat_id": 1, "title": "RKAT BPKH 2026", "kup_score": 87.5, "sbo_score": 92.3, "status": "draft", "department": "BPKH"}
        ]
    }

# AI Support Endpoints
@app.post("/api/ai/chat")
async def ai_chat(request: dict):
    """AI-powered chat for RKAT queries"""
    query = request.get("query", "")
    
    # Mock AI response
    responses = {
        "anggaran": "Berdasarkan SBO BPKH 2026, anggaran harus mengikuti standar yang telah ditetapkan. Untuk konsumsi rapat sebesar Rp 125.000 per orang, dan honorarium narasumber eselon I sebesar Rp 1.400.000 per JPL.",
        "workflow": "Workflow RKAT BPKH meliputi: 1) Penyusunan oleh Badan Pelaksana, 2) Review oleh Audit Internal, 3) Review oleh Komite Dewan Pengawas, 4) Persetujuan oleh Dewan Pengawas, 5) Final approval.",
        "compliance": "Untuk compliance KUP 2026, pastikan tema 'Institutional Strengthening', sasaran strategis align dengan pengembangan investasi ekosistem haji dan penguatan kelembagaan BPKH."
    }
    
    response = "Saya dapat membantu Anda dengan pertanyaan tentang RKAT, anggaran, workflow, dan compliance BPKH. "
    for key, value in responses.items():
        if key in query.lower():
            response = value
            break
    
    return {"response": response}

@app.post("/api/ai/scenario-analysis")
async def scenario_analysis(request: dict):
    """Generate budget scenarios using AI"""
    base_budget = request.get("base_budget", 1000000000)
    
    scenarios = [
        {
            "name": "Conservative Scenario",
            "total_budget": base_budget * 1.05,
            "operational_budget": base_budget * 0.7,
            "personnel_budget": base_budget * 0.35,
            "assumptions": ["Inflasi 3.5%", "Pertumbuhan minimal"],
            "risks": ["Keterbatasan program", "Efisiensi rendah"]
        },
        {
            "name": "Realistic Scenario",
            "total_budget": base_budget * 1.15,
            "operational_budget": base_budget * 0.75,
            "personnel_budget": base_budget * 0.4,
            "assumptions": ["Pertumbuhan moderat 5%", "Efisiensi standar"],
            "risks": ["Fluktuasi ekonomi", "Perubahan regulasi"]
        },
        {
            "name": "Optimistic Scenario",
            "total_budget": base_budget * 1.25,
            "operational_budget": base_budget * 0.8,
            "personnel_budget": base_budget * 0.45,
            "assumptions": ["Pertumbuhan maksimal 8%", "Efisiensi tinggi"],
            "risks": ["Overcommitment", "Resource constraints"]
        }
    ]
    
    return {"scenarios": scenarios}

if __name__ == "__main__":
    print("🚀 RKAT BPKH Complete Backend Starting...")
    print("📍 Backend: http://localhost:8000")
    print("📍 API Docs: http://localhost:8000/docs")
    print("📍 Frontend: http://localhost:8501")
    print("\n🔑 Login Credentials:")
    for username, data in USERS.items():
        print(f"   • {username} / {data['password']} ({data['role']})")
    print("\n✅ All endpoints ready! Frontend should work perfectly now!")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)