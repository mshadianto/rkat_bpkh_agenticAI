# rkat_backend_complete.py - Backend Lengkap untuk Sistem RKAT BPKH
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from enum import Enum
import uuid
import json

# Initialize FastAPI app
app = FastAPI(
    title="RKAT BPKH API",
    description="Sistem Rencana Kerja dan Anggaran Tahunan - Badan Pengelola Keuangan Haji",
    version="2.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    attachment_url: Optional[str] = None

class KUPReference(BaseModel):
    kup_id: str
    title: str
    description: str
    budget_limit: float
    validity_period: str

class SBOReference(BaseModel):
    sbo_id: str
    category: str
    standard_cost: float
    unit: str
    description: str

class RKATItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    kegiatan: str
    output: str
    indikator_kinerja: str
    target: str
    anggaran: float
    sumber_anggaran: str
    kup_reference: str
    sbo_reference: str

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
    
    # RKAT Content
    items: List[RKATItem]
    total_anggaran: float
    latar_belakang: str
    tujuan: str
    sasaran: str
    ruang_lingkup: str
    metode_pelaksanaan: str
    
    # References
    kup_references: List[str]
    sbo_references: List[str]
    
    # Workflow
    status: RKATStatus = RKATStatus.DRAFT
    current_reviewer: Optional[str] = None
    progress_percentage: int = 0
    
    # Reviews and Approvals
    audit_review: Optional[Dict[str, Any]] = None
    komite_review: Optional[Dict[str, Any]] = None
    dewan_approval: Optional[Dict[str, Any]] = None
    
    # Comments and History
    comments: List[Comment] = []
    revision_history: List[Dict[str, Any]] = []
    
    # Deadlines
    deadline_audit: Optional[datetime] = None
    deadline_komite: Optional[datetime] = None
    deadline_dewan: Optional[datetime] = None

class ReviewRequest(BaseModel):
    rkat_id: str
    reviewer_comment: str
    recommendation: str  # approve, reject, revision_needed
    attachments: Optional[List[str]] = None

class ApprovalRequest(BaseModel):
    rkat_id: str
    approval_comment: str
    decision: str  # approve, reject
    conditions: Optional[List[str]] = None

# In-Memory Database (Replace with actual database in production)
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

KUP_DB = {
    "KUP-AI-2026": {
        "kup_id": "KUP-AI-2026",
        "title": "Kebijakan Umum Audit Internal 2026",
        "description": "Pedoman penganggaran untuk kegiatan audit internal dan tata kelola",
        "budget_limit": 5000000000,
        "validity_period": "2026"
    },
    "KUP-TI-2026": {
        "kup_id": "KUP-TI-2026", 
        "title": "Kebijakan Umum Teknologi Informasi 2026",
        "description": "Pedoman penganggaran untuk transformasi digital dan IT",
        "budget_limit": 10000000000,
        "validity_period": "2026"
    }
}

SBO_DB = {
    "SBO-CORP-001": {
        "sbo_id": "SBO-CORP-001",
        "category": "Audit & Corporate Governance",
        "standard_cost": 50000000,
        "unit": "per kegiatan",
        "description": "Standar biaya untuk kegiatan audit dan tata kelola perusahaan"
    },
    "SBO-TECH-002": {
        "sbo_id": "SBO-TECH-002",
        "category": "Technology Development",
        "standard_cost": 200000000,
        "unit": "per sistem",
        "description": "Standar biaya pengembangan sistem dan aplikasi"
    }
}

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

def set_deadlines(rkat: RKAT):
    """Set deadlines based on submission date"""
    rkat.deadline_audit = rkat.tanggal_pengajuan + timedelta(days=7)
    rkat.deadline_komite = rkat.deadline_audit + timedelta(days=5)
    rkat.deadline_dewan = rkat.deadline_komite + timedelta(days=5)

# API Endpoints

@app.post("/auth/login")
async def login(request: LoginRequest):
    """User authentication"""
    user_data = USERS_DB.get(request.username)
    if not user_data or user_data["password"] != request.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # In production, return JWT token
    return {
        "access_token": f"mock_token_{request.username}",
        "token_type": "bearer",
        "user": User(**user_data)
    }

@app.get("/auth/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user

@app.get("/dashboard/metrics")
async def get_dashboard_metrics(current_user: User = Depends(get_current_user)):
    """Get dashboard metrics"""
    total_rkat = len(RKAT_DB)
    approved_rkat = len([r for r in RKAT_DB.values() if r.status == RKATStatus.APPROVED])
    total_budget = sum(r.total_anggaran for r in RKAT_DB.values())
    
    # Calculate average approval time (mock data)
    avg_approval_days = 5.8
    
    # Status distribution
    status_distribution = {}
    for status in RKATStatus:
        status_distribution[status.value] = len([r for r in RKAT_DB.values() if r.status == status])
    
    return {
        "total_rkat": total_rkat,
        "approved_rkat": approved_rkat,
        "total_budget": total_budget,
        "avg_approval_days": avg_approval_days,
        "status_distribution": status_distribution
    }

@app.get("/rkat/", response_model=List[RKAT])
async def get_rkat_list(
    status: Optional[RKATStatus] = None,
    bidang: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Get list of RKAT with optional filters"""
    rkat_list = list(RKAT_DB.values())
    
    # Apply filters
    if status:
        rkat_list = [r for r in rkat_list if r.status == status]
    
    if bidang:
        rkat_list = [r for r in rkat_list if r.bidang == bidang]
    
    # Apply user permissions
    if current_user.role == UserRole.BIDANG_PENGAJU:
        rkat_list = [r for r in rkat_list if r.pengaju_id == current_user.id]
    elif current_user.role == UserRole.AUDIT_INTERNAL:
        rkat_list = [r for r in rkat_list if r.status in [
            RKATStatus.PENDING_AUDIT_REVIEW, 
            RKATStatus.AUDIT_REVIEWED
        ]]
    
    return rkat_list

@app.get("/rkat/{rkat_id}", response_model=RKAT)
async def get_rkat_detail(rkat_id: str, current_user: User = Depends(get_current_user)):
    """Get RKAT detail"""
    if rkat_id not in RKAT_DB:
        raise HTTPException(status_code=404, detail="RKAT not found")
    
    return RKAT_DB[rkat_id]

@app.post("/rkat/", response_model=RKAT)
async def create_rkat(rkat_data: RKAT, current_user: User = Depends(get_current_user)):
    """Create new RKAT"""
    if "create_rkat" not in current_user.permissions:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    # Set metadata
    rkat_data.pengaju_id = current_user.id
    rkat_data.pengaju_name = current_user.name
    rkat_data.bidang = current_user.bidang or rkat_data.bidang
    
    # Set deadlines
    set_deadlines(rkat_data)
    
    # Calculate progress
    rkat_data.progress_percentage = calculate_progress(rkat_data)
    
    # Store in database
    RKAT_DB[rkat_data.id] = rkat_data
    
    return rkat_data

@app.put("/rkat/{rkat_id}", response_model=RKAT)
async def update_rkat(
    rkat_id: str, 
    rkat_data: RKAT, 
    current_user: User = Depends(get_current_user)
):
    """Update RKAT"""
    if rkat_id not in RKAT_DB:
        raise HTTPException(status_code=404, detail="RKAT not found")
    
    existing_rkat = RKAT_DB[rkat_id]
    
    # Check permissions
    if (current_user.role == UserRole.BIDANG_PENGAJU and 
        existing_rkat.pengaju_id != current_user.id):
        raise HTTPException(status_code=403, detail="Can only edit own RKAT")
    
    # Update timestamp
    rkat_data.tanggal_update = datetime.now()
    rkat_data.progress_percentage = calculate_progress(rkat_data)
    
    # Store revision history
    rkat_data.revision_history.append({
        "timestamp": datetime.now(),
        "user": current_user.name,
        "changes": "RKAT updated"
    })
    
    RKAT_DB[rkat_id] = rkat_data
    return rkat_data

@app.post("/rkat/{rkat_id}/submit")
async def submit_rkat(rkat_id: str, current_user: User = Depends(get_current_user)):
    """Submit RKAT for review"""
    if rkat_id not in RKAT_DB:
        raise HTTPException(status_code=404, detail="RKAT not found")
    
    rkat = RKAT_DB[rkat_id]
    
    if rkat.pengaju_id != current_user.id:
        raise HTTPException(status_code=403, detail="Can only submit own RKAT")
    
    if rkat.status != RKATStatus.DRAFT:
        raise HTTPException(status_code=400, detail="RKAT already submitted")
    
    # Update status to pending audit review
    rkat.status = RKATStatus.PENDING_AUDIT_REVIEW
    rkat.progress_percentage = calculate_progress(rkat)
    rkat.tanggal_update = datetime.now()
    
    # Add to revision history
    rkat.revision_history.append({
        "timestamp": datetime.now(),
        "user": current_user.name,
        "action": "Submitted for audit review"
    })
    
    return {"message": "RKAT submitted successfully", "rkat": rkat}

@app.post("/rkat/{rkat_id}/review/audit")
async def audit_review_rkat(
    rkat_id: str, 
    review: ReviewRequest, 
    current_user: User = Depends(get_current_user)
):
    """Audit Internal review RKAT"""
    if current_user.role != UserRole.AUDIT_INTERNAL:
        raise HTTPException(status_code=403, detail="Only audit internal can review")
    
    if rkat_id not in RKAT_DB:
        raise HTTPException(status_code=404, detail="RKAT not found")
    
    rkat = RKAT_DB[rkat_id]
    
    if rkat.status != RKATStatus.PENDING_AUDIT_REVIEW:
        raise HTTPException(status_code=400, detail="RKAT not in review state")
    
    # Store audit review
    rkat.audit_review = {
        "reviewer_id": current_user.id,
        "reviewer_name": current_user.name,
        "comment": review.reviewer_comment,
        "recommendation": review.recommendation,
        "review_date": datetime.now(),
        "attachments": review.attachments or []
    }
    
    # Update status based on recommendation
    if review.recommendation == "approve":
        rkat.status = RKATStatus.PENDING_KOMITE_REVIEW
    elif review.recommendation == "reject":
        rkat.status = RKATStatus.REJECTED
    else:  # revision_needed
        rkat.status = RKATStatus.REVISION_NEEDED
    
    rkat.progress_percentage = calculate_progress(rkat)
    rkat.tanggal_update = datetime.now()
    
    # Add comment
    comment = Comment(
        user_id=current_user.id,
        user_name=current_user.name,
        message=f"Audit Review: {review.reviewer_comment}"
    )
    rkat.comments.append(comment)
    
    return {"message": "Audit review completed", "rkat": rkat}

@app.post("/rkat/{rkat_id}/review/komite")
async def komite_review_rkat(
    rkat_id: str, 
    review: ReviewRequest, 
    current_user: User = Depends(get_current_user)
):
    """Komite Dewan Pengawas review RKAT"""
    if current_user.role != UserRole.KOMITE_DEWAN_PENGAWAS:
        raise HTTPException(status_code=403, detail="Only komite can review")
    
    if rkat_id not in RKAT_DB:
        raise HTTPException(status_code=404, detail="RKAT not found")
    
    rkat = RKAT_DB[rkat_id]
    
    if rkat.status != RKATStatus.PENDING_KOMITE_REVIEW:
        raise HTTPException(status_code=400, detail="RKAT not in komite review state")
    
    # Store komite review
    rkat.komite_review = {
        "reviewer_id": current_user.id,
        "reviewer_name": current_user.name,
        "comment": review.reviewer_comment,
        "recommendation": review.recommendation,
        "review_date": datetime.now(),
        "attachments": review.attachments or []
    }
    
    # Update status based on recommendation
    if review.recommendation == "approve":
        rkat.status = RKATStatus.PENDING_DEWAN_APPROVAL
    elif review.recommendation == "reject":
        rkat.status = RKATStatus.REJECTED
    else:  # revision_needed
        rkat.status = RKATStatus.REVISION_NEEDED
    
    rkat.progress_percentage = calculate_progress(rkat)
    rkat.tanggal_update = datetime.now()
    
    # Add comment
    comment = Comment(
        user_id=current_user.id,
        user_name=current_user.name,
        message=f"Komite Review: {review.reviewer_comment}"
    )
    rkat.comments.append(comment)
    
    return {"message": "Komite review completed", "rkat": rkat}

@app.post("/rkat/{rkat_id}/approve")
async def approve_rkat(
    rkat_id: str, 
    approval: ApprovalRequest, 
    current_user: User = Depends(get_current_user)
):
    """Dewan Pengawas final approval"""
    if current_user.role != UserRole.DEWAN_PENGAWAS:
        raise HTTPException(status_code=403, detail="Only dewan pengawas can approve")
    
    if rkat_id not in RKAT_DB:
        raise HTTPException(status_code=404, detail="RKAT not found")
    
    rkat = RKAT_DB[rkat_id]
    
    if rkat.status != RKATStatus.PENDING_DEWAN_APPROVAL:
        raise HTTPException(status_code=400, detail="RKAT not ready for approval")
    
    # Store approval
    rkat.dewan_approval = {
        "approver_id": current_user.id,
        "approver_name": current_user.name,
        "comment": approval.approval_comment,
        "decision": approval.decision,
        "approval_date": datetime.now(),
        "conditions": approval.conditions or []
    }
    
    # Update status based on decision
    if approval.decision == "approve":
        rkat.status = RKATStatus.APPROVED
    else:  # reject
        rkat.status = RKATStatus.REJECTED
    
    rkat.progress_percentage = calculate_progress(rkat)
    rkat.tanggal_update = datetime.now()
    
    # Add comment
    comment = Comment(
        user_id=current_user.id,
        user_name=current_user.name,
        message=f"Final Approval: {approval.approval_comment}"
    )
    rkat.comments.append(comment)
    
    return {"message": "RKAT approval completed", "rkat": rkat}

@app.get("/references/kup")
async def get_kup_references(current_user: User = Depends(get_current_user)):
    """Get KUP references"""
    return list(KUP_DB.values())

@app.get("/references/sbo")
async def get_sbo_references(current_user: User = Depends(get_current_user)):
    """Get SBO references"""
    return list(SBO_DB.values())

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

@app.post("/rkat/{rkat_id}/comments")
async def add_comment(
    rkat_id: str,
    comment_text: str,
    current_user: User = Depends(get_current_user)
):
    """Add comment to RKAT"""
    if rkat_id not in RKAT_DB:
        raise HTTPException(status_code=404, detail="RKAT not found")
    
    rkat = RKAT_DB[rkat_id]
    
    comment = Comment(
        user_id=current_user.id,
        user_name=current_user.name,
        message=comment_text
    )
    
    rkat.comments.append(comment)
    rkat.tanggal_update = datetime.now()
    
    return {"message": "Comment added", "comment": comment}

@app.get("/reports/status")
async def get_status_report(current_user: User = Depends(get_current_user)):
    """Get status report for all RKAT"""
    report = {
        "total_rkat": len(RKAT_DB),
        "by_status": {},
        "by_bidang": {},
        "budget_summary": {
            "total_requested": 0,
            "total_approved": 0
        },
        "timeline_analysis": {
            "on_time": 0,
            "delayed": 0,
            "avg_processing_days": 0
        }
    }
    
    # Calculate statistics
    for rkat in RKAT_DB.values():
        # By status
        status_key = rkat.status.value
        report["by_status"][status_key] = report["by_status"].get(status_key, 0) + 1
        
        # By bidang
        bidang_key = rkat.bidang
        report["by_bidang"][bidang_key] = report["by_bidang"].get(bidang_key, 0) + 1
        
        # Budget summary
        report["budget_summary"]["total_requested"] += rkat.total_anggaran
        if rkat.status == RKATStatus.APPROVED:
            report["budget_summary"]["total_approved"] += rkat.total_anggaran
    
    return report

if __name__ == "__main__":
    import uvicorn
    
    # Add some sample data for demo
    sample_rkat = RKAT(
        id="RKAT-2026-001",
        judul="RKAT Audit Internal 2026",
        bidang="Audit Internal",
        divisi="Audit Internal 1",
        program="Program Audit Fungsi Korporasi",
        pengaju_id="user_002",
        pengaju_name="Misbah Taufiqurrohman",
        tahun_anggaran=2026,
        items=[
            RKATItem(
                kegiatan="Pelaksanaan Asurans Umum",
                output="4 Laporan Audit",
                indikator_kinerja="Laporan audit berkualitas",
                target="100% sesuai jadwal",
                anggaran=85125000,
                sumber_anggaran="DIPA BPKH",
                kup_reference="KUP-AI-2026",
                sbo_reference="SBO-CORP-001"
            )
        ],
        total_anggaran=2500000000,
        latar_belakang="Mendukung penyelenggaraan fungsi audit internal BPKH",
        tujuan="Meningkatkan efektivitas audit internal",
        sasaran="Terwujudnya good governance",
        ruang_lingkup="Audit fungsi korporasi",
        metode_pelaksanaan="Audit berbasis risiko",
        kup_references=["KUP-AI-2026"],
        sbo_references=["SBO-CORP-001"],
        status=RKATStatus.PENDING_AUDIT_REVIEW
    )
    
    set_deadlines(sample_rkat)
    sample_rkat.progress_percentage = calculate_progress(sample_rkat)
    RKAT_DB[sample_rkat.id] = sample_rkat
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
