from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class WorkflowAction(enum.Enum):
    SUBMIT = "submit"
    APPROVE = "approve"
    REJECT = "reject"
    REQUEST_REVISION = "request_revision"
    RESUBMIT = "resubmit"

class WorkflowLog(Base):
    __tablename__ = "workflow_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    rkat_id = Column(Integer, ForeignKey("rkat.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(Enum(WorkflowAction), nullable=False)
    previous_status = Column(String, nullable=True)
    new_status = Column(String, nullable=False)
    comments = Column(Text, nullable=True)
    attachments = Column(String, nullable=True)  # JSON array of file paths
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    rkat = relationship("RKAT", backref="workflow_logs")
    user = relationship("User", backref="workflow_actions")