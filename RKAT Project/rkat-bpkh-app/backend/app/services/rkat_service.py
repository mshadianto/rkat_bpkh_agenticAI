from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.rkat import RKAT, RKATActivity, RKATStatus
from app.models.user import User, UserRole
from app.services.kup_service import KUPService
from app.services.sbo_service import SBOService
from typing import List, Dict, Optional
import json

class RKATService:
    def __init__(self, db: Session):
        self.db = db
        self.kup_service = KUPService()
        self.sbo_service = SBOService()
    
    def create_rkat(self, rkat_data: dict, user: User) -> RKAT:
        """Create new RKAT proposal"""
        # Validate budget compliance
        self._validate_budget_limits(rkat_data)
        
        rkat = RKAT(
            title=rkat_data["title"],
            year=rkat_data.get("year", settings.rkat_year),
            total_budget=rkat_data["total_budget"],
            operational_budget=rkat_data["operational_budget"],
            personnel_budget=rkat_data["personnel_budget"],
            theme=rkat_data.get("theme", "Institutional Strengthening"),
            strategic_objectives=rkat_data.get("strategic_objectives", []),
            key_activities=rkat_data.get("key_activities", []),
            performance_indicators=rkat_data.get("performance_indicators", []),
            created_by=user.id,
            status=RKATStatus.DRAFT
        )
        
        self.db.add(rkat)
        self.db.commit()
        self.db.refresh(rkat)
        
        # Calculate compliance scores
        self._calculate_compliance_scores(rkat)
        
        return rkat
    
    def add_activity(self, rkat_id: int, activity_data: dict) -> RKATActivity:
        """Add activity to RKAT"""
        # Validate SBO compliance
        sbo_validation = self.sbo_service.validate_activity_budget(
            activity_data["activity_code"],
            activity_data["budget_amount"]
        )
        
        activity = RKATActivity(
            rkat_id=rkat_id,
            activity_code=activity_data["activity_code"],
            activity_name=activity_data["activity_name"],
            description=activity_data.get("description"),
            budget_amount=activity_data["budget_amount"],
            sbo_reference=sbo_validation.get("sbo_code"),
            budget_calculation=activity_data.get("budget_calculation", {}),
            output_target=activity_data.get("output_target"),
            outcome_target=activity_data.get("outcome_target"),
            performance_indicators=activity_data.get("performance_indicators", [])
        )
        
        self.db.add(activity)
        self.db.commit()
        self.db.refresh(activity)
        
        # Update RKAT totals
        self._update_rkat_totals(rkat_id)
        
        return activity
    
    def get_rkat_by_user_role(self, user: User) -> List[RKAT]:
        """Get RKAT list based on user role"""
        query = self.db.query(RKAT)
        
        if user.role == UserRole.BADAN_PELAKSANA:
            # Can see own RKATs
            query = query.filter(RKAT.created_by == user.id)
        elif user.role == UserRole.AUDIT_INTERNAL:
            # Can see submitted RKATs for review
            query = query.filter(RKAT.status.in_([
                RKATStatus.SUBMITTED, 
                RKATStatus.UNDER_AUDIT_REVIEW,
                RKATStatus.AUDIT_APPROVED,
                RKATStatus.AUDIT_REJECTED
            ]))
        elif user.role == UserRole.KOMITE_DEWAN_PENGAWAS:
            # Can see audit-approved RKATs
            query = query.filter(RKAT.status.in_([
                RKATStatus.AUDIT_APPROVED,
                RKATStatus.UNDER_COMMITTEE_REVIEW,
                RKATStatus.COMMITTEE_APPROVED,
                RKATStatus.COMMITTEE_REJECTED
            ]))
        elif user.role == UserRole.DEWAN_PENGAWAS:
            # Can see committee-approved RKATs
            query = query.filter(RKAT.status.in_([
                RKATStatus.COMMITTEE_APPROVED,
                RKATStatus.UNDER_BOARD_REVIEW,
                RKATStatus.BOARD_APPROVED,
                RKATStatus.BOARD_REJECTED,
                RKATStatus.FINAL_APPROVED
            ]))
        
        return query.order_by(RKAT.created_at.desc()).all()
    
    def _validate_budget_limits(self, rkat_data: dict):
        """Validate budget against BPKH limits"""
        operational_budget = rkat_data["operational_budget"]
        
        # TODO: Get previous year's nilai manfaat from database
        # For now, using a placeholder value
        previous_year_nilai_manfaat = 10_000_000_000  # 10 Milyar
        max_operational = previous_year_nilai_manfaat * settings.max_operational_budget_percentage
        
        if operational_budget > max_operational:
            raise ValueError(f"Operational budget exceeds 5% limit: {operational_budget:,.0f} > {max_operational:,.0f}")
    
    def _calculate_compliance_scores(self, rkat: RKAT):
        """Calculate KUP and SBO compliance scores"""
        # KUP Compliance
        kup_score = self.kup_service.calculate_compliance_score(rkat)
        
        # SBO Compliance
        sbo_score = self.sbo_service.calculate_compliance_score(rkat)
        
        rkat.kup_compliance_score = kup_score
        rkat.sbo_compliance_score = sbo_score
        self.db.commit()
    
    def _update_rkat_totals(self, rkat_id: int):
        """Update RKAT total budgets based on activities"""
        rkat = self.db.query(RKAT).filter(RKAT.id == rkat_id).first()
        activities = self.db.query(RKATActivity).filter(RKATActivity.rkat_id == rkat_id).all()
        
        total_budget = sum(activity.budget_amount for activity in activities)
        rkat.total_budget = total_budget
        self.db.commit()
