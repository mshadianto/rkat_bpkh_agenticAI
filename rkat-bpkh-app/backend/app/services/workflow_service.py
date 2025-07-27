from sqlalchemy.orm import Session
from app.models.rkat import RKAT, RKATStatus
from app.models.workflow import WorkflowLog, WorkflowAction
from app.models.user import User, UserRole
from app.services.notification_service import NotificationService
from typing import Dict, List
from datetime import datetime

class WorkflowService:
    def __init__(self, db: Session):
        self.db = db
        self.notification_service = NotificationService()
    
    def submit_rkat(self, rkat_id: int, user: User) -> Dict:
        """Submit RKAT for review"""
        rkat = self.db.query(RKAT).filter(RKAT.id == rkat_id).first()
        
        if not rkat:
            raise ValueError("RKAT not found")
        
        if rkat.created_by != user.id:
            raise ValueError("Only creator can submit RKAT")
        
        if rkat.status != RKATStatus.DRAFT:
            raise ValueError("Only draft RKAT can be submitted")
        
        # Update status
        previous_status = rkat.status
        rkat.status = RKATStatus.SUBMITTED
        rkat.submitted_at = datetime.utcnow()
        
        # Log workflow action
        self._log_workflow_action(
            rkat_id=rkat_id,
            user_id=user.id,
            action=WorkflowAction.SUBMIT,
            previous_status=previous_status.value,
            new_status=rkat.status.value
        )
        
        # Notify audit internal team
        self._notify_next_reviewers(rkat, UserRole.AUDIT_INTERNAL)
        
        self.db.commit()
        
        return {"message": "RKAT submitted successfully", "new_status": rkat.status.value}
    
    def review_rkat(self, rkat_id: int, user: User, action: str, comments: str = None) -> Dict:
        """Review RKAT (approve/reject/request revision)"""
        rkat = self.db.query(RKAT).filter(RKAT.id == rkat_id).first()
        
        if not rkat:
            raise ValueError("RKAT not found")
        
        # Validate reviewer permissions
        self._validate_reviewer_permissions(rkat, user)
        
        previous_status = rkat.status
        new_status = self._determine_new_status(rkat.status, user.role, action)
        
        # Update RKAT status
        rkat.status = new_status
        if action == "approve" and new_status == RKATStatus.FINAL_APPROVED:
            rkat.approved_at = datetime.utcnow()
        
        # Log workflow action
        workflow_action = WorkflowAction.APPROVE if action == "approve" else WorkflowAction.REJECT
        self._log_workflow_action(
            rkat_id=rkat_id,
            user_id=user.id,
            action=workflow_action,
            previous_status=previous_status.value,
            new_status=new_status.value,
            comments=comments
        )
        
        # Notify next reviewers or creator
        if action == "approve":
            next_role = self._get_next_reviewer_role(user.role)
            if next_role:
                self._notify_next_reviewers(rkat, next_role)
            else:
                self._notify_creator(rkat, "RKAT approved successfully")
        else:
            self._notify_creator(rkat, f"RKAT rejected: {comments}")
        
        self.db.commit()
        
        return {"message": f"RKAT {action}ed successfully", "new_status": new_status.value}
    
    def get_workflow_history(self, rkat_id: int) -> List[Dict]:
        """Get workflow history for RKAT"""
        logs = self.db.query(WorkflowLog)\
            .filter(WorkflowLog.rkat_id == rkat_id)\
            .order_by(WorkflowLog.created_at.desc())\
            .all()
        
        return [
            {
                "id": log.id,
                "action": log.action.value,
                "user": log.user.full_name,
                "previous_status": log.previous_status,
                "new_status": log.new_status,
                "comments": log.comments,
                "timestamp": log.created_at
            }
            for log in logs
        ]
    
    def _validate_reviewer_permissions(self, rkat: RKAT, user: User):
        """Validate if user can review this RKAT"""
        valid_combinations = {
            RKATStatus.SUBMITTED: [UserRole.AUDIT_INTERNAL],
            RKATStatus.UNDER_AUDIT_REVIEW: [UserRole.AUDIT_INTERNAL],
            RKATStatus.AUDIT_APPROVED: [UserRole.KOMITE_DEWAN_PENGAWAS],
            RKATStatus.UNDER_COMMITTEE_REVIEW: [UserRole.KOMITE_DEWAN_PENGAWAS],
            RKATStatus.COMMITTEE_APPROVED: [UserRole.DEWAN_PENGAWAS],
            RKATStatus.UNDER_BOARD_REVIEW: [UserRole.DEWAN_PENGAWAS]
        }
        
        if rkat.status not in valid_combinations or user.role not in valid_combinations[rkat.status]:
            raise ValueError("User not authorized to review this RKAT at current status")
    
    def _determine_new_status(self, current_status: RKATStatus, user_role: UserRole, action: str) -> RKATStatus:
        """Determine new status based on current status, user role, and action"""
        if action == "approve":
            status_transitions = {
                (RKATStatus.SUBMITTED, UserRole.AUDIT_INTERNAL): RKATStatus.AUDIT_APPROVED,
                (RKATStatus.AUDIT_APPROVED, UserRole.KOMITE_DEWAN_PENGAWAS): RKATStatus.COMMITTEE_APPROVED,
                (RKATStatus.COMMITTEE_APPROVED, UserRole.DEWAN_PENGAWAS): RKATStatus.FINAL_APPROVED
            }
        else:  # reject
            status_transitions = {
                (RKATStatus.SUBMITTED, UserRole.AUDIT_INTERNAL): RKATStatus.AUDIT_REJECTED,
                (RKATStatus.AUDIT_APPROVED, UserRole.KOMITE_DEWAN_PENGAWAS): RKATStatus.COMMITTEE_REJECTED,
                (RKATStatus.COMMITTEE_APPROVED, UserRole.DEWAN_PENGAWAS): RKATStatus.BOARD_REJECTED
            }
        
        return status_transitions.get((current_status, user_role), current_status)
    
    def _get_next_reviewer_role(self, current_role: UserRole) -> UserRole:
        """Get next reviewer role in workflow"""
        role_sequence = {
            UserRole.AUDIT_INTERNAL: UserRole.KOMITE_DEWAN_PENGAWAS,
            UserRole.KOMITE_DEWAN_PENGAWAS: UserRole.DEWAN_PENGAWAS,
            UserRole.DEWAN_PENGAWAS: None  # Final approval
        }
        return role_sequence.get(current_role)
    
    def _log_workflow_action(self, rkat_id: int, user_id: int, action: WorkflowAction, 
                           previous_status: str, new_status: str, comments: str = None):
        """Log workflow action"""
        log = WorkflowLog(
            rkat_id=rkat_id,
            user_id=user_id,
            action=action,
            previous_status=previous_status,
            new_status=new_status,
            comments=comments
        )
        self.db.add(log)
    
    def _notify_next_reviewers(self, rkat: RKAT, role: UserRole):
        """Notify users with specific role about new RKAT to review"""
        # Implementation depends on notification service
        pass
    
    def _notify_creator(self, rkat: RKAT, message: str):
        """Notify RKAT creator about status update"""
        # Implementation depends on notification service
        pass