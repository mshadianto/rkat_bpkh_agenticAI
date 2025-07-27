from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class UserRole(enum.Enum):
    BADAN_PELAKSANA = "badan_pelaksana"
    AUDIT_INTERNAL = "audit_internal" 
    KOMITE_DEWAN_PENGAWAS = "komite_dewan_pengawas"
    DEWAN_PENGAWAS = "dewan_pengawas"
    ADMINISTRATOR = "administrator"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    department = Column(String, nullable=True)
    position = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
