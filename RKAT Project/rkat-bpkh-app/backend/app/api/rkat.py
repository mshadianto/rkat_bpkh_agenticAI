from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.api.auth import get_current_user
from app.services.rkat_service import RKATService
from app.models.user import User
from app.models.rkat import RKAT, RKATActivity, RKATStatus
from typing import List, Optional, Dict
from datetime import datetime
import json

router = APIRouter()

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

class RKATResponse(BaseModel):
    id: int
    title: str
    year: int
    status: RKATStatus
    total_budget: float
    operational_budget: float
    personnel_budget: float
    theme: Optional[str]
    kup_compliance_score: Optional[float]
    sbo_compliance_score: Optional[float]
    created_at: datetime
    creator_name: str
    activities_count: int

@router.post("/create")
async def create_rkat(
    rkat_data: RKATCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new RKAT proposal"""
    try:
        rkat_service = RKATService(db)
        rkat = rkat_service.create_rkat(rkat_data.dict(), current_user)
        
        return {
            "message": "RKAT created successfully",
            "rkat_id": rkat.id,
            "status": rkat.status.value
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/list", response_model=List[RKATResponse])
async def get_rkat_list(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get RKAT list based on user role"""
    rkat_service = RKATService(db)
    rkats = rkat_service.get_rkat_by_user_role(current_user)
    
    result = []
    for rkat in rkats:
        activities_count = len(rkat.activities) if hasattr(rkat, 'activities') else 0
        result.append({
            "id": rkat.id,
            "title": rkat.title,
            "year": rkat.year,
            "status": rkat.status,
            "total_budget": rkat.total_budget,
            "operational_budget": rkat.operational_budget,
            "personnel_budget": rkat.personnel_budget,
            "theme": rkat.theme,
            "kup_compliance_score": rkat.kup_compliance_score,
            "sbo_compliance_score": rkat.sbo_compliance_score,
            "created_at": rkat.created_at,
            "creator_name": rkat.creator.full_name if rkat.creator else "Unknown",
            "activities_count": activities_count
        })
    
    return result

@router.get("/{rkat_id}")
async def get_rkat_detail(
    rkat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed RKAT information"""
    rkat = db.query(RKAT).filter(RKAT.id == rkat_id).first()
    
    if not rkat:
        raise HTTPException(status_code=404, detail="RKAT not found")
    
    # Get activities
    activities = db.query(RKATActivity).filter(RKATActivity.rkat_id == rkat_id).all()
    
    return {
        "rkat": {
            "id": rkat.id,
            "title": rkat.title,
            "year": rkat.year,
            "status": rkat.status.value,
            "total_budget": rkat.total_budget,
            "operational_budget": rkat.operational_budget,
            "personnel_budget": rkat.personnel_budget,
            "theme": rkat.theme,
            "strategic_objectives": rkat.strategic_objectives,
            "key_activities": rkat.key_activities,
            "performance_indicators": rkat.performance_indicators,
            "kup_compliance_score": rkat.kup_compliance_score,
            "sbo_compliance_score": rkat.sbo_compliance_score,
            "created_at": rkat.created_at,
            "creator": {
                "name": rkat.creator.full_name,
                "department": rkat.creator.department
            }
        },
        "activities": [
            {
                "id": activity.id,
                "activity_code": activity.activity_code,
                "activity_name": activity.activity_name,
                "description": activity.description,
                "budget_amount": activity.budget_amount,
                "sbo_reference": activity.sbo_reference,
                "output_target": activity.output_target,
                "outcome_target": activity.outcome_target,
                "kak_document": activity.kak_document,
                "rab_document": activity.rab_document,
                "timeline_document": activity.timeline_document
            }
            for activity in activities
        ]
    }

@router.post("/{rkat_id}/activities")
async def add_activity(
    rkat_id: int,
    activity_data: ActivityCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add activity to RKAT"""
    # Check if RKAT exists and user has permission
    rkat = db.query(RKAT).filter(RKAT.id == rkat_id).first()
    if not rkat:
        raise HTTPException(status_code=404, detail="RKAT not found")
    
    if rkat.created_by != current_user.id and rkat.status != RKATStatus.DRAFT:
        raise HTTPException(status_code=403, detail="Cannot modify RKAT in current status")
    
    try:
        rkat_service = RKATService(db)
        activity = rkat_service.add_activity(rkat_id, activity_data.dict())
        
        return {
            "message": "Activity added successfully",
            "activity_id": activity.id
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{rkat_id}/upload-document")
async def upload_document(
    rkat_id: int,
    activity_id: int,
    document_type: str,  # 'kak', 'rab', 'timeline'
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload document for RKAT activity"""
    # Validate file type and size
    allowed_types = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Only PDF and Word documents are allowed")
    
    if file.size > settings.max_file_size:
        raise HTTPException(status_code=400, detail="File too large")
    
    # Get activity
    activity = db.query(RKATActivity).filter(
        RKATActivity.id == activity_id,
        RKATActivity.rkat_id == rkat_id
    ).first()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Save file
    import os
    from datetime import datetime
    
    upload_dir = f"{settings.upload_dir}/rkat_{rkat_id}/activity_{activity_id}"
    os.makedirs(upload_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{document_type}_{timestamp}_{file.filename}"
    file_path = os.path.join(upload_dir, filename)
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Update activity record
    if document_type == "kak":
        activity.kak_document = file_path
    elif document_type == "rab":
        activity.rab_document = file_path
    elif document_type == "timeline":
        activity.timeline_document = file_path
    
    db.commit()
    
    return {"message": "Document uploaded successfully", "file_path": file_path}

@router.get("/{rkat_id}/compliance-check")
async def check_compliance(
    rkat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check RKAT compliance with KUP and SBO"""
    rkat = db.query(RKAT).filter(RKAT.id == rkat_id).first()
    
    if not rkat:
        raise HTTPException(status_code=404, detail="RKAT not found")
    
    rkat_service = RKATService(db)
    
    # Get KUP compliance
    kup_compliance = rkat_service.kup_service.validate_rkat_compliance(rkat)
    
    # Get SBO compliance score
    sbo_score = rkat_service.sbo_service.calculate_compliance_score(rkat)
    
    return {
        "kup_compliance": kup_compliance,
        "sbo_compliance": {
            "score": sbo_score,
            "level": "EXCELLENT" if sbo_score >= 90 else "GOOD" if sbo_score >= 80 else "NEEDS_IMPROVEMENT"
        }
    }