from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class RKATStatus(enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_AUDIT_REVIEW = "under_audit_review"
    AUDIT_APPROVED = "audit_approved" 
    AUDIT_REJECTED = "audit_rejected"
    UNDER_COMMITTEE_REVIEW = "under_committee_review"
    COMMITTEE_APPROVED = "committee_approved"
    COMMITTEE_REJECTED = "committee_rejected"
    UNDER_BOARD_REVIEW = "under_board_review"
    BOARD_APPROVED = "board_approved"
    BOARD_REJECTED = "board_rejected"
    FINAL_APPROVED = "final_approved"

class RKAT(Base):
    __tablename__ = "rkat"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    status = Column(Enum(RKATStatus), default=RKATStatus.DRAFT)
    total_budget = Column(Float, nullable=False)
    operational_budget = Column(Float, nullable=False)
    personnel_budget = Column(Float, nullable=False)
    renstra_reference = Column(String, nullable=True)
    kup_compliance_score = Column(Float, nullable=True)
    sbo_compliance_score = Column(Float, nullable=True)
    theme = Column(String, nullable=True)
    strategic_objectives = Column(JSON, nullable=True)
    key_activities = Column(JSON, nullable=True)
    performance_indicators = Column(JSON, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    current_reviewer = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    creator = relationship("User", foreign_keys=[created_by])
    reviewer = relationship("User", foreign_keys=[current_reviewer])

class RKATActivity(Base):
    __tablename__ = "rkat_activities"
    
    id = Column(Integer, primary_key=True, index=True)
    rkat_id = Column(Integer, ForeignKey("rkat.id"))
    activity_code = Column(String, nullable=False)
    activity_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    budget_amount = Column(Float, nullable=False)
    sbo_reference = Column(String, nullable=True)
    budget_calculation = Column(JSON, nullable=True)
    output_target = Column(String, nullable=True)
    outcome_target = Column(String, nullable=True)
    performance_indicators = Column(JSON, nullable=True)
    kak_document = Column(String, nullable=True)
    rab_document = Column(String, nullable=True)
    timeline_document = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    rkat = relationship("RKAT", backref="activities")
