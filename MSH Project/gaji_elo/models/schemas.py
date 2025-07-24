"""Data models and schemas for the Salary Estimator application."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class EducationLevel(str, Enum):
    HIGH_SCHOOL = "high_school"
    DIPLOMA = "diploma"
    BACHELOR = "bachelor"
    MASTER = "master"
    PHD = "phd"


class ExperienceLevel(str, Enum):
    ENTRY = "entry"        # 0-2 years
    JUNIOR = "junior"      # 2-5 years
    MID = "mid"           # 5-8 years
    SENIOR = "senior"     # 8-12 years
    EXPERT = "expert"     # 12+ years


class Industry(str, Enum):
    ACCOUNTING_FINANCE = "Accounting & Finance"
    BANKING_FINANCIAL_SERVICES = "Banking & Financial Services"
    CONSTRUCTION = "Construction"
    ENERGY_NATURAL_RESOURCES = "Energy & Natural Resources"
    ENGINEERING_MANUFACTURING = "Engineering & Manufacturing"
    EXECUTIVE = "Executive"
    HEALTHCARE_LIFE_SCIENCES = "Healthcare & Life Sciences"
    HUMAN_RESOURCES = "Human Resources"
    LEGAL = "Legal"
    PROCUREMENT_SUPPLY_CHAIN = "Procurement & Supply Chain"
    PROPERTY_FACILITIES = "Property & Facilities Management"
    RETAIL = "Retail"
    SALES_MARKETING = "Sales & Marketing"
    TECHNOLOGY = "Technology"


class CVProfile(BaseModel):
    """Extracted CV profile information."""
    
    # Personal Information
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    
    # Professional Summary
    summary: Optional[str] = None
    current_title: Optional[str] = None
    
    # Experience
    total_experience_years: float = 0
    experience_level: ExperienceLevel = ExperienceLevel.ENTRY
    work_experiences: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Education
    education_level: EducationLevel = EducationLevel.BACHELOR
    education_details: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Skills
    technical_skills: List[str] = Field(default_factory=list)
    soft_skills: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    
    # Industry Detection
    detected_industry: Optional[Industry] = None
    industry_confidence: float = 0.0
    
    # Raw text for RAG
    raw_text: str = ""


class SalaryData(BaseModel):
    """Salary information from the guide."""
    
    industry: Industry
    job_title: str
    average_monthly_salary_idr: int  # In millions IDR
    category: Optional[str] = None
    subcategory: Optional[str] = None


class SalaryEstimation(BaseModel):
    """Salary estimation result."""
    
    # Main estimation
    estimated_salary_min: int  # In millions IDR
    estimated_salary_max: int  # In millions IDR
    estimated_salary_avg: int  # In millions IDR
    
    # Matched positions
    matched_positions: List[Dict[str, Any]] = Field(default_factory=list)
    best_match_title: Optional[str] = None
    match_confidence: float = 0.0
    
    # Factors
    experience_factor: float = 1.0
    education_factor: float = 1.0
    skills_factor: float = 1.0
    location_factor: float = 1.0
    
    # Explanation
    explanation: str = ""
    recommendations: List[str] = Field(default_factory=list)
    
    # Metadata
    estimation_date: datetime = Field(default_factory=datetime.now)
    algorithm_version: str = "1.0.0"  # Changed from model_version to avoid pydantic warning
    
    class Config:
        protected_namespaces = ()  # Disable protected namespace warning


class RAGQuery(BaseModel):
    """Query structure for RAG system."""
    
    query_text: str
    cv_profile: CVProfile
    context_window: int = 5
    include_similar_roles: bool = True
    
    
class RAGResponse(BaseModel):
    """Response from RAG system."""
    
    relevant_salaries: List[SalaryData]
    context_snippets: List[str]
    llm_analysis: str
    confidence_score: float