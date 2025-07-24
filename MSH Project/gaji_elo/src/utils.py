"""Utility functions for the Salary Estimator application."""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)


def load_salary_guide_data() -> List[Dict[str, Any]]:
    """
    Load and structure salary guide data from the PDF content.
    This creates the salary_guide_2025.json file from the PDF data.
    """
    
    # Complete salary data extracted from the Indonesia Salary Guide 2025 PDF
    salary_data = [
        # Accounting & Finance
        {"industry": "Accounting & Finance", "category": "Accounting", "job_title": "Senior Accountant", "salary": 25},
        {"industry": "Accounting & Finance", "category": "Accounting", "job_title": "Accounts Payable Manager", "salary": 35},
        {"industry": "Accounting & Finance", "category": "Accounting", "job_title": "Accounts Receivable Manager", "salary": 35},
        {"industry": "Accounting & Finance", "category": "Accounting", "job_title": "Accounting Manager", "salary": 45},
        {"industry": "Accounting & Finance", "category": "Accounting", "job_title": "Finance Manager", "salary": 50},
        {"industry": "Accounting & Finance", "category": "Accounting", "job_title": "Group Finance Manager", "salary": 60},
        {"industry": "Accounting & Finance", "category": "Accounting", "job_title": "Head of Accounting", "salary": 80},
        {"industry": "Accounting & Finance", "category": "Accounting", "job_title": "Head of Finance", "salary": 100},
        {"industry": "Accounting & Finance", "category": "Accounting", "job_title": "Finance Director", "salary": 180},
        
        # Audit
        {"industry": "Accounting & Finance", "category": "Audit", "job_title": "Internal Audit Manager", "salary": 40},
        {"industry": "Accounting & Finance", "category": "Audit", "job_title": "Internal Control Manager", "salary": 45},
        {"industry": "Accounting & Finance", "category": "Audit", "job_title": "Head of Internal Audit", "salary": 120},
        
        # Controller
        {"industry": "Accounting & Finance", "category": "Controller", "job_title": "Cost Accountant", "salary": 25},
        {"industry": "Accounting & Finance", "category": "Controller", "job_title": "Credit Controller", "salary": 35},
        {"industry": "Accounting & Finance", "category": "Controller", "job_title": "Plant Controller", "salary": 40},
        {"industry": "Accounting & Finance", "category": "Controller", "job_title": "Project Controller", "salary": 40},
        {"industry": "Accounting & Finance", "category": "Controller", "job_title": "Assistant Financial Controller", "salary": 45},
        {"industry": "Accounting & Finance", "category": "Controller", "job_title": "Business Controller", "salary": 50},
        {"industry": "Accounting & Finance", "category": "Controller", "job_title": "Financial Controller", "salary": 80},
        {"industry": "Accounting & Finance", "category": "Controller", "job_title": "Group Financial Controller", "salary": 100},
        
        # Banking & Financial Services
        {"industry": "Banking & Financial Services", "category": "Corporate Finance", "job_title": "Corporate Finance & Strategy Analyst", "salary": 20},
        {"industry": "Banking & Financial Services", "category": "Corporate Finance", "job_title": "Corporate Finance & Strategy Manager", "salary": 50},
        {"industry": "Banking & Financial Services", "category": "Corporate Finance", "job_title": "Head of Corporate Finance", "salary": 120},
        {"industry": "Banking & Financial Services", "category": "Investment", "job_title": "Investment Banking Analyst", "salary": 36},
        {"industry": "Banking & Financial Services", "category": "Investment", "job_title": "Investment Banking Associate", "salary": 39},
        {"industry": "Banking & Financial Services", "category": "Investment", "job_title": "Investment Banking Manager", "salary": 70},
        {"industry": "Banking & Financial Services", "category": "Investment", "job_title": "Fund Manager", "salary": 80},
        
        # Technology - Development
        {"industry": "Technology", "category": "Development", "job_title": "Front-end Developer", "salary": 20},
        {"industry": "Technology", "category": "Development", "job_title": "Quality Assurance Engineer", "salary": 23},
        {"industry": "Technology", "category": "Development", "job_title": "Back-end Developer", "salary": 25},
        {"industry": "Technology", "category": "Development", "job_title": "Mobile Developer", "salary": 25},
        {"industry": "Technology", "category": "Development", "job_title": "Full-stack Developer", "salary": 30},
        {"industry": "Technology", "category": "Development", "job_title": "Tech Lead", "salary": 40},
        {"industry": "Technology", "category": "Development", "job_title": "Solution Architect", "salary": 55},
        {"industry": "Technology", "category": "Development", "job_title": "Engineering Manager", "salary": 67},
        {"industry": "Technology", "category": "Development", "job_title": "Head of Engineering", "salary": 81},
        {"industry": "Technology", "category": "Development", "job_title": "Vice President Engineering", "salary": 108},
        
        # Technology - Analytics
        {"industry": "Technology", "category": "Analytics", "job_title": "Business Intelligence Analyst", "salary": 27},
        {"industry": "Technology", "category": "Analytics", "job_title": "Lead Data Analyst", "salary": 30},
        {"industry": "Technology", "category": "Analytics", "job_title": "Business Analytics Manager", "salary": 39},
        {"industry": "Technology", "category": "Analytics", "job_title": "Lead Data Engineer", "salary": 42},
        {"industry": "Technology", "category": "Analytics", "job_title": "Lead Data Scientist", "salary": 46},
        {"industry": "Technology", "category": "Analytics", "job_title": "Data Science Manager", "salary": 72},
        {"industry": "Technology", "category": "Analytics", "job_title": "Head of Data", "salary": 80},
        {"industry": "Technology", "category": "Analytics", "job_title": "Vice President Data", "salary": 132},
        
        # Sales & Marketing
        {"industry": "Sales & Marketing", "category": "Consumer Products", "job_title": "Marketing Executive", "salary": 12},
        {"industry": "Sales & Marketing", "category": "Consumer Products", "job_title": "Assistant Brand Manager", "salary": 20},
        {"industry": "Sales & Marketing", "category": "Consumer Products", "job_title": "Trade Marketing Manager", "salary": 28},
        {"industry": "Sales & Marketing", "category": "Consumer Products", "job_title": "Marketing Communications Manager", "salary": 30},
        {"industry": "Sales & Marketing", "category": "Consumer Products", "job_title": "Brand Manager", "salary": 35},
        {"industry": "Sales & Marketing", "category": "Consumer Products", "job_title": "Senior Brand Manager", "salary": 50},
        {"industry": "Sales & Marketing", "category": "Consumer Products", "job_title": "Marketing Manager", "salary": 70},
        {"industry": "Sales & Marketing", "category": "Consumer Products", "job_title": "Head of Marketing", "salary": 90},
        {"industry": "Sales & Marketing", "category": "Consumer Products", "job_title": "Marketing Director", "salary": 130},
        
        # Human Resources
        {"industry": "Human Resources", "category": "Generalist", "job_title": "HR Operations", "salary": 16},
        {"industry": "Human Resources", "category": "Generalist", "job_title": "HR Generalist", "salary": 21},
        {"industry": "Human Resources", "category": "Generalist", "job_title": "HR Superintendent", "salary": 25},
        {"industry": "Human Resources", "category": "Generalist", "job_title": "HR Project Manager", "salary": 31},
        {"industry": "Human Resources", "category": "Generalist", "job_title": "HR Manager", "salary": 35},
        {"industry": "Human Resources", "category": "Generalist", "job_title": "HR Business Partner", "salary": 45},
        {"industry": "Human Resources", "category": "Generalist", "job_title": "Senior HR Business Partner", "salary": 55},
        {"industry": "Human Resources", "category": "Generalist", "job_title": "Head of HR", "salary": 100},
        {"industry": "Human Resources", "category": "Generalist", "job_title": "HR Director", "salary": 120},
        
        # Executive
        {"industry": "Executive", "category": "C-Suite", "job_title": "Operations Director", "salary": 96},
        {"industry": "Executive", "category": "C-Suite", "job_title": "Chief Technology Officer", "salary": 150},
        {"industry": "Executive", "category": "C-Suite", "job_title": "Chief Marketing Officer", "salary": 190},
        {"industry": "Executive", "category": "C-Suite", "job_title": "Chief Financial Officer", "salary": 225},
        {"industry": "Executive", "category": "C-Suite", "job_title": "Chief Executive Officer", "salary": 519},
    ]
    
    return salary_data


def save_salary_data_to_json(data_dir: Path):
    """Save salary data to JSON file."""
    try:
        salary_data = load_salary_guide_data()
        
        # Ensure data directory exists
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Save to JSON
        json_path = data_dir / "salary_guide_2025.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(salary_data, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Saved {len(salary_data)} salary records to {json_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error saving salary data: {str(e)}")
        return False


def format_salary_range(min_salary: int, max_salary: int) -> str:
    """Format salary range for display."""
    return f"IDR {min_salary:,} - {max_salary:,} million/month"


def calculate_annual_salary(monthly_salary: int) -> int:
    """Calculate annual salary from monthly (including 13th month bonus)."""
    return monthly_salary * 13


def get_percentile_rank(salary: int, all_salaries: List[int]) -> float:
    """Calculate percentile rank of a salary."""
    if not all_salaries:
        return 50.0
        
    sorted_salaries = sorted(all_salaries)
    position = 0
    
    for s in sorted_salaries:
        if s < salary:
            position += 1
        else:
            break
            
    percentile = (position / len(sorted_salaries)) * 100
    return round(percentile, 1)


def generate_salary_report(estimation, profile) -> Dict[str, Any]:
    """Generate comprehensive salary report."""
    return {
        "generated_date": datetime.now().isoformat(),
        "profile_summary": {
            "name": profile.full_name or "Anonymous",
            "current_title": profile.current_title,
            "experience_years": profile.total_experience_years,
            "experience_level": profile.experience_level.value,
            "education_level": profile.education_level.value,
            "industry": profile.detected_industry.value if profile.detected_industry else "Unknown",
            "skills_count": len(profile.technical_skills) + len(profile.soft_skills),
        },
        "salary_estimation": {
            "monthly_min": estimation.estimated_salary_min,
            "monthly_avg": estimation.estimated_salary_avg,
            "monthly_max": estimation.estimated_salary_max,
            "annual_min": calculate_annual_salary(estimation.estimated_salary_min),
            "annual_avg": calculate_annual_salary(estimation.estimated_salary_avg),
            "annual_max": calculate_annual_salary(estimation.estimated_salary_max),
            "confidence": estimation.match_confidence,
        },
        "matched_positions": estimation.matched_positions[:10],
        "factors": {
            "experience": estimation.experience_factor,
            "education": estimation.education_factor,
            "skills": estimation.skills_factor,
            "location": estimation.location_factor,
        },
        "recommendations": estimation.recommendations,
        "market_analysis": estimation.explanation,
    }


def validate_cv_content(cv_text: str) -> Dict[str, bool]:
    """Validate CV content for completeness."""
    validations = {
        "has_contact_info": any(keyword in cv_text.lower() for keyword in ['email', '@', 'phone', 'contact']),
        "has_experience": any(keyword in cv_text.lower() for keyword in ['experience', 'work', 'employment']),
        "has_education": any(keyword in cv_text.lower() for keyword in ['education', 'university', 'degree', 'bachelor', 'master']),
        "has_skills": any(keyword in cv_text.lower() for keyword in ['skill', 'expertise', 'proficient', 'knowledge']),
        "has_sufficient_length": len(cv_text) > 500,
    }
    
    validations["completeness_score"] = sum(validations.values()) / len(validations)
    
    return validations


def clean_text_for_analysis(text: str) -> str:
    """Clean text for analysis."""
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove special characters but keep important ones
    allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,;:!?@#$%&*()-_+=/')
    text = ''.join(c for c in text if c in allowed_chars)
    
    return text.strip()


def get_career_stage(experience_years: float) -> str:
    """Determine career stage from experience years."""
    if experience_years < 2:
        return "Early Career"
    elif experience_years < 5:
        return "Developing Professional"
    elif experience_years < 10:
        return "Experienced Professional"
    elif experience_years < 15:
        return "Senior Professional"
    else:
        return "Executive/Expert"


def calculate_skill_relevance_score(cv_skills: List[str], job_requirements: List[str]) -> float:
    """Calculate how well CV skills match job requirements."""
    if not job_requirements:
        return 1.0
        
    cv_skills_lower = [s.lower() for s in cv_skills]
    matches = 0
    
    for req in job_requirements:
        req_lower = req.lower()
        if any(req_lower in skill or skill in req_lower for skill in cv_skills_lower):
            matches += 1
            
    return matches / len(job_requirements) if job_requirements else 0.0