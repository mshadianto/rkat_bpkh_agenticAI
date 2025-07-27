from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.api.auth import get_current_user
from app.services.workflow_service import WorkflowService
from app.models.user import User
from typing import Optional, List, Dict

router = APIRouter()

class WorkflowAction(BaseModel):
    action: str  # 'approve', 'reject', 'request_revision'
    comments: Optional[str] = None

@router.post("/{rkat_id}/submit")
async def submit_rkat(
    rkat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit RKAT for review"""
    try:
        workflow_service = WorkflowService(db)
        result = workflow_service.submit_rkat(rkat_id, current_user)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{rkat_id}/review")
async def review_rkat(
    rkat_id: int,
    workflow_action: WorkflowAction,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Review RKAT (approve/reject)"""
    try:
        workflow_service = WorkflowService(db)
        result = workflow_service.review_rkat(
            rkat_id, 
            current_user, 
            workflow_action.action,
            workflow_action.comments
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{rkat_id}/history")
async def get_workflow_history(
    rkat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get workflow history for RKAT"""
    workflow_service = WorkflowService(db)
    history = workflow_service.get_workflow_history(rkat_id)
    return {"workflow_history": history}

@router.get("/pending-reviews")
async def get_pending_reviews(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get RKATs pending review for current user"""
    from app.services.rkat_service import RKATService
    rkat_service = RKATService(db)
    pending_rkats = rkat_service.get_rkat_by_user_role(current_user)
    
    # Filter for pending reviews based on user role
    pending = []
    for rkat in pending_rkats:
        if current_user.role.value == "audit_internal" and rkat.status.value in ["submitted", "under_audit_review"]:
            pending.append(rkat)
        elif current_user.role.value == "komite_dewan_pengawas" and rkat.status.value in ["audit_approved", "under_committee_review"]:
            pending.append(rkat)
        elif current_user.role.value == "dewan_pengawas" and rkat.status.value in ["committee_approved", "under_board_review"]:
            pending.append(rkat)
    
    return {
        "pending_reviews": [
            {
                "id": rkat.id,
                "title": rkat.title,
                "creator": rkat.creator.full_name,
                "submitted_at": rkat.submitted_at,
                "total_budget": rkat.total_budget,
                "status": rkat.status.value
            }
            for rkat in pending
        ]
    }