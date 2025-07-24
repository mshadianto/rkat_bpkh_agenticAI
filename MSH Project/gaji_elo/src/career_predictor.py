"""Career Path Predictor module for long-term career projection."""

import logging
from typing import Dict, List, Tuple, Any, Optional
import numpy as np
from datetime import datetime, timedelta
import json
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum

# Since we don't have the actual imports, let's create mock classes
class ExperienceLevel(Enum):
    ENTRY = "entry"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    EXPERT = "expert"

class Industry(Enum):
    TECHNOLOGY = "Technology"
    BANKING = "Banking"
    HEALTHCARE = "Healthcare"
    RETAIL = "Retail"
    MANUFACTURING = "Manufacturing"

class EducationLevel(Enum):
    HIGH_SCHOOL = "high_school"
    BACHELOR = "bachelor"
    MASTER = "master"
    PHD = "phd"

@dataclass
class CVProfile:
    current_title: Optional[str] = None
    total_experience_years: float = 0
    experience_level: ExperienceLevel = ExperienceLevel.ENTRY
    detected_industry: Optional[Industry] = None
    technical_skills: List[str] = field(default_factory=list)
    soft_skills: List[str] = field(default_factory=list)
    education_level: EducationLevel = EducationLevel.BACHELOR

@dataclass
class SalaryEstimation:
    estimated_salary_avg: float = 0
    estimated_salary_min: float = 0
    estimated_salary_max: float = 0
    confidence: float = 0

class SkillsGapAnalyzer:
    """Mock class for skills analysis"""
    pass

logger = logging.getLogger(__name__)

class CareerPredictor:
    """Predict career paths and salary progression over 5-10 years."""
    
    def __init__(self):
        self.skills_analyzer = SkillsGapAnalyzer()
        
        # Career progression patterns
        self.career_paths = {
            "Technology": {
                "developer": {
                    "junior": ["mid developer", "full-stack developer"],
                    "mid": ["senior developer", "tech lead", "architect"],
                    "senior": ["tech lead", "architect", "engineering manager"],
                    "lead": ["engineering manager", "principal engineer", "director"]
                },
                "data": {
                    "analyst": ["senior analyst", "data scientist"],
                    "scientist": ["senior scientist", "lead scientist", "ml engineer"],
                    "engineer": ["senior engineer", "architect", "engineering manager"]
                }
            },
            "Management": {
                "individual": ["team lead", "supervisor"],
                "team_lead": ["manager", "senior manager"],
                "manager": ["senior manager", "director"],
                "director": ["vp", "senior director", "cto/cio"]
            }
        }
        
        # Salary growth patterns (annual percentage)
        self.growth_patterns = {
            "high_growth": {  # Tech, startups
                "entry": 15,
                "junior": 12,
                "mid": 10,
                "senior": 8,
                "expert": 6
            },
            "moderate_growth": {  # Established companies
                "entry": 10,
                "junior": 8,
                "mid": 7,
                "senior": 6,
                "expert": 5
            },
            "stable_growth": {  # Traditional industries
                "entry": 8,
                "junior": 6,
                "mid": 5,
                "senior": 4,
                "expert": 3
            }
        }
        
        # Role transition probabilities
        self.transition_probability = {
            "stay_technical": 0.6,
            "move_to_management": 0.3,
            "change_domain": 0.1
        }
        
    def predict_career_path(
        self,
        cv_profile: CVProfile,
        current_estimation: SalaryEstimation,
        years_to_predict: int = 10,
        target_role: Optional[str] = None,
        industry_growth: str = "moderate_growth"
    ) -> Dict[str, Any]:
        """Predict career path and salary progression."""
        
        predictions = {
            "current_state": self._get_current_state(cv_profile, current_estimation),
            "career_paths": self._generate_career_paths(cv_profile, target_role),
            "salary_progression": self._predict_salary_progression(
                cv_profile, current_estimation, years_to_predict, industry_growth
            ),
            "skill_roadmap": self._create_skill_roadmap(cv_profile, years_to_predict),
            "milestones": self._predict_milestones(cv_profile, years_to_predict),
            "investment_roi": self._calculate_investment_roi(cv_profile),
            "market_trends": self._analyze_market_trends(cv_profile.detected_industry),
            "recommendations": self._generate_career_recommendations(cv_profile)
        }
        
        return predictions
        
    def _get_current_state(
        self,
        cv_profile: CVProfile,
        current_estimation: SalaryEstimation
    ) -> Dict[str, Any]:
        """Get current career state."""
        return {
            "title": cv_profile.current_title or "Unknown",
            "experience_years": cv_profile.total_experience_years,
            "experience_level": cv_profile.experience_level.value,
            "current_salary": current_estimation.estimated_salary_avg,
            "industry": cv_profile.detected_industry.value if cv_profile.detected_industry else "General",
            "key_skills": cv_profile.technical_skills[:5],
            "education": cv_profile.education_level.value
        }
        
    def _generate_career_paths(
        self,
        cv_profile: CVProfile,
        target_role: Optional[str]
    ) -> List[Dict[str, Any]]:
        """Generate possible career paths."""
        
        paths = []
        current_role = cv_profile.current_title or "developer"
        current_level = cv_profile.experience_level.value
        
        # Technical progression path
        tech_path = self._create_technical_path(current_role, current_level)
        paths.append({
            "path_name": "Technical Specialist",
            "description": "Deep technical expertise and architecture",
            "progression": tech_path["roles"],
            "peak_salary": tech_path["peak_salary"],
            "time_to_peak": tech_path["time_to_peak"],
            "required_skills": tech_path["required_skills"],
            "probability": self.transition_probability["stay_technical"]
        })
        
        # Management path
        mgmt_path = self._create_management_path(current_role, current_level)
        paths.append({
            "path_name": "Engineering Management",
            "description": "People leadership and strategic planning",
            "progression": mgmt_path["roles"],
            "peak_salary": mgmt_path["peak_salary"],
            "time_to_peak": mgmt_path["time_to_peak"],
            "required_skills": mgmt_path["required_skills"],
            "probability": self.transition_probability["move_to_management"]
        })
        
        # Hybrid path
        hybrid_path = self._create_hybrid_path(current_role, current_level)
        paths.append({
            "path_name": "Technical Leadership",
            "description": "Mix of technical work and team leadership",
            "progression": hybrid_path["roles"],
            "peak_salary": hybrid_path["peak_salary"],
            "time_to_peak": hybrid_path["time_to_peak"],
            "required_skills": hybrid_path["required_skills"],
            "probability": 0.5  # Balanced probability
        })
        
        # Entrepreneurial path
        if cv_profile.total_experience_years > 5:
            startup_path = self._create_entrepreneurial_path(current_level)
            paths.append({
                "path_name": "Entrepreneurial",
                "description": "Startup founder or technical co-founder",
                "progression": startup_path["roles"],
                "peak_salary": startup_path["peak_salary"],
                "time_to_peak": startup_path["time_to_peak"],
                "required_skills": startup_path["required_skills"],
                "probability": 0.1
            })
            
        return paths
        
    def _create_technical_path(self, current_role: str, current_level: str) -> Dict[str, Any]:
        """Create technical specialist career path."""
        
        # Define progression based on current level
        progressions = {
            "entry": [
                {"year": 0, "role": "Junior Developer", "salary": 20},
                {"year": 2, "role": "Developer", "salary": 30},
                {"year": 5, "role": "Senior Developer", "salary": 50},
                {"year": 8, "role": "Tech Lead", "salary": 70},
                {"year": 10, "role": "Principal Engineer", "salary": 100}
            ],
            "junior": [
                {"year": 0, "role": "Developer", "salary": 30},
                {"year": 3, "role": "Senior Developer", "salary": 50},
                {"year": 6, "role": "Tech Lead", "salary": 70},
                {"year": 8, "role": "Staff Engineer", "salary": 90},
                {"year": 10, "role": "Principal Engineer", "salary": 120}
            ],
            "mid": [
                {"year": 0, "role": "Senior Developer", "salary": 50},
                {"year": 3, "role": "Tech Lead", "salary": 70},
                {"year": 5, "role": "Staff Engineer", "salary": 90},
                {"year": 8, "role": "Principal Engineer", "salary": 120},
                {"year": 10, "role": "Distinguished Engineer", "salary": 150}
            ],
            "senior": [
                {"year": 0, "role": "Tech Lead", "salary": 70},
                {"year": 2, "role": "Staff Engineer", "salary": 90},
                {"year": 5, "role": "Principal Engineer", "salary": 120},
                {"year": 8, "role": "Distinguished Engineer", "salary": 150},
                {"year": 10, "role": "Chief Architect", "salary": 180}
            ],
            "expert": [
                {"year": 0, "role": "Principal Engineer", "salary": 120},
                {"year": 3, "role": "Distinguished Engineer", "salary": 150},
                {"year": 5, "role": "Chief Architect", "salary": 180},
                {"year": 8, "role": "CTO/VP Engineering", "salary": 220},
                {"year": 10, "role": "CTO", "salary": 250}
            ]
        }
        
        progression = progressions.get(current_level, progressions["mid"])
        
        return {
            "roles": progression,
            "peak_salary": progression[-1]["salary"],
            "time_to_peak": 10,
            "required_skills": [
                "System Design",
                "Architecture Patterns",
                "Performance Optimization",
                "Code Review",
                "Technical Mentoring",
                "Innovation"
            ]
        }
        
    def _create_management_path(self, current_role: str, current_level: str) -> Dict[str, Any]:
        """Create management career path."""
        
        progressions = {
            "junior": [
                {"year": 0, "role": "Developer", "salary": 30},
                {"year": 3, "role": "Team Lead", "salary": 45},
                {"year": 5, "role": "Engineering Manager", "salary": 70},
                {"year": 8, "role": "Senior Manager", "salary": 100},
                {"year": 10, "role": "Director", "salary": 140}
            ],
            "mid": [
                {"year": 0, "role": "Senior Developer", "salary": 50},
                {"year": 2, "role": "Team Lead", "salary": 65},
                {"year": 4, "role": "Engineering Manager", "salary": 85},
                {"year": 7, "role": "Senior Manager", "salary": 120},
                {"year": 10, "role": "Director", "salary": 160}
            ],
            "senior": [
                {"year": 0, "role": "Tech Lead", "salary": 70},
                {"year": 2, "role": "Engineering Manager", "salary": 90},
                {"year": 5, "role": "Senior Manager", "salary": 130},
                {"year": 8, "role": "Director", "salary": 170},
                {"year": 10, "role": "VP Engineering", "salary": 220}
            ]
        }
        
        progression = progressions.get(current_level, progressions["mid"])
        
        return {
            "roles": progression,
            "peak_salary": progression[-1]["salary"],
            "time_to_peak": 10,
            "required_skills": [
                "People Management",
                "Strategic Planning",
                "Budget Management",
                "Stakeholder Communication",
                "Performance Reviews",
                "Hiring & Recruiting",
                "Conflict Resolution"
            ]
        }
        
    def _create_hybrid_path(self, current_role: str, current_level: str) -> Dict[str, Any]:
        """Create hybrid technical-management path."""
        
        progressions = {
            "mid": [
                {"year": 0, "role": "Senior Developer", "salary": 50},
                {"year": 3, "role": "Tech Lead", "salary": 70},
                {"year": 5, "role": "Technical Manager", "salary": 90},
                {"year": 8, "role": "Principal Engineer & Manager", "salary": 130},
                {"year": 10, "role": "Technical Director", "salary": 170}
            ],
            "senior": [
                {"year": 0, "role": "Tech Lead", "salary": 70},
                {"year": 2, "role": "Technical Manager", "salary": 95},
                {"year": 5, "role": "Principal Engineer & Manager", "salary": 140},
                {"year": 8, "role": "Technical Director", "salary": 180},
                {"year": 10, "role": "VP of Engineering", "salary": 220}
            ]
        }
        
        progression = progressions.get(current_level, progressions["mid"])
        
        return {
            "roles": progression,
            "peak_salary": progression[-1]["salary"],
            "time_to_peak": 10,
            "required_skills": [
                "Technical Excellence",
                "Team Leadership",
                "Project Management",
                "Architecture Design",
                "Mentoring",
                "Cross-functional Collaboration"
            ]
        }
        
    def _create_entrepreneurial_path(self, current_level: str) -> Dict[str, Any]:
        """Create entrepreneurial career path."""
        
        return {
            "roles": [
                {"year": 0, "role": "Senior Professional", "salary": 70},
                {"year": 2, "role": "Technical Co-founder", "salary": 50},  # Initial drop
                {"year": 4, "role": "Startup CTO", "salary": 80},
                {"year": 7, "role": "Founder & CEO", "salary": 150},
                {"year": 10, "role": "Serial Entrepreneur", "salary": 300}  # High variance
            ],
            "peak_salary": 300,  # Potential is much higher but uncertain
            "time_to_peak": 10,
            "required_skills": [
                "Business Acumen",
                "Risk Management",
                "Fundraising",
                "Product Vision",
                "Team Building",
                "Market Analysis",
                "Financial Planning"
            ]
        }
        
    def _predict_salary_progression(
        self,
        cv_profile: CVProfile,
        current_estimation: SalaryEstimation,
        years: int,
        growth_pattern: str
    ) -> Dict[str, Any]:
        """Predict salary progression over years."""
        
        current_salary = current_estimation.estimated_salary_avg
        current_level = cv_profile.experience_level.value
        
        # Get growth rates
        growth_rates = self.growth_patterns.get(growth_pattern, self.growth_patterns["moderate_growth"])
        
        # Generate yearly projections
        projections = []
        cumulative_salary = current_salary
        
        for year in range(years + 1):
            # Determine level at this year
            total_experience = cv_profile.total_experience_years + year
            if total_experience < 2:
                level = "entry"
            elif total_experience < 5:
                level = "junior"
            elif total_experience < 8:
                level = "mid"
            elif total_experience < 12:
                level = "senior"
            else:
                level = "expert"
                
            # Apply growth rate
            if year > 0:
                annual_growth = growth_rates.get(level, 5) / 100
                
                # Add randomness for realism
                variation = np.random.uniform(-0.02, 0.02)
                actual_growth = annual_growth + variation
                
                # Account for promotions
                if year % 3 == 0 and year > 0:  # Promotion every 3 years
                    actual_growth += 0.1  # 10% promotion bump
                    
                cumulative_salary *= (1 + actual_growth)
                
            projections.append({
                "year": year,
                "experience_total": total_experience,
                "level": level,
                "salary": round(cumulative_salary, 1),
                "annual_increase": round(cumulative_salary - (projections[-1]["salary"] if projections else current_salary), 1) if year > 0 else 0
            })
            
        # Calculate summary statistics
        total_increase = projections[-1]["salary"] - current_salary
        avg_annual_increase = total_increase / years
        total_percentage_increase = (total_increase / current_salary) * 100
        
        return {
            "projections": projections,
            "summary": {
                "current_salary": current_salary,
                "projected_salary": projections[-1]["salary"],
                "total_increase": round(total_increase, 1),
                "percentage_increase": round(total_percentage_increase, 1),
                "average_annual_increase": round(avg_annual_increase, 1),
                "cagr": round(((projections[-1]["salary"] / current_salary) ** (1/years) - 1) * 100, 2)
            },
            "milestones": self._identify_salary_milestones(projections)
        }
        
    def _identify_salary_milestones(self, projections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify significant salary milestones."""
        
        milestones = []
        thresholds = [50, 75, 100, 150, 200, 250, 300]
        
        for threshold in thresholds:
            for proj in projections:
                if proj["salary"] >= threshold and (not milestones or milestones[-1]["threshold"] < threshold):
                    milestones.append({
                        "year": proj["year"],
                        "threshold": threshold,
                        "salary": proj["salary"],
                        "message": f"Reach IDR {threshold}M/month milestone"
                    })
                    break
                    
        return milestones
        
    def _create_skill_roadmap(self, cv_profile: CVProfile, years: int) -> List[Dict[str, Any]]:
        """Create skill development roadmap."""
        
        roadmap = []
        current_skills = set(cv_profile.technical_skills + cv_profile.soft_skills)
        
        # Define skill progression by year
        skill_timeline = {
            1: {
                "technical": ["Advanced Python", "System Design Basics", "Cloud Fundamentals"],
                "soft": ["Team Collaboration", "Communication Skills"],
                "certifications": ["AWS Certified Cloud Practitioner"]
            },
            3: {
                "technical": ["Microservices", "Kubernetes", "Advanced Databases"],
                "soft": ["Leadership Basics", "Project Management"],
                "certifications": ["AWS Solutions Architect", "Kubernetes CKA"]
            },
            5: {
                "technical": ["Architecture Patterns", "ML/AI Basics", "Security Best Practices"],
                "soft": ["Strategic Thinking", "Mentoring"],
                "certifications": ["Cloud Architect Professional", "Security+"]
            },
            7: {
                "technical": ["Enterprise Architecture", "AI/ML Advanced", "Blockchain"],
                "soft": ["Executive Communication", "Business Strategy"],
                "certifications": ["TOGAF", "PMP"]
            },
            10: {
                "technical": ["Technology Strategy", "Innovation Management", "Digital Transformation"],
                "soft": ["Board Presentation", "Organizational Leadership"],
                "certifications": ["Executive Education", "Industry Thought Leader"]
            }
        }
        
        for year_milestone, skills in skill_timeline.items():
            if year_milestone <= years:
                # Filter out skills already possessed
                new_technical = [s for s in skills["technical"] if s.lower() not in [cs.lower() for cs in current_skills]]
                new_soft = [s for s in skills["soft"] if s.lower() not in [cs.lower() for cs in current_skills]]
                
                roadmap.append({
                    "year": year_milestone,
                    "technical_skills": new_technical[:3],  # Top 3
                    "soft_skills": new_soft[:2],  # Top 2
                    "certifications": skills["certifications"][:2],  # Top 2
                    "focus_area": self._determine_focus_area(year_milestone),
                    "learning_hours_estimated": year_milestone * 100  # Rough estimate
                })
                
        return roadmap
        
    def _determine_focus_area(self, year: int) -> str:
        """Determine primary focus area for a given year."""
        
        if year <= 2:
            return "Technical Depth - Master core technologies"
        elif year <= 4:
            return "Technical Breadth - Expand technology stack"
        elif year <= 6:
            return "Leadership Skills - Team and project leadership"
        elif year <= 8:
            return "Strategic Thinking - Architecture and planning"
        else:
            return "Executive Skills - Business and organizational leadership"
            
    def _predict_milestones(self, cv_profile: CVProfile, years: int) -> List[Dict[str, Any]]:
        """Predict career milestones."""
        
        milestones = []
        current_exp = cv_profile.total_experience_years
        
        # Experience-based milestones
        experience_milestones = {
            2: "Complete junior phase",
            5: "Achieve mid-level status",
            8: "Reach senior level",
            10: "Become industry expert",
            15: "Executive leadership potential"
        }
        
        for exp_years, milestone in experience_milestones.items():
            years_until = exp_years - current_exp
            if 0 < years_until <= years:
                milestones.append({
                    "year": int(years_until),
                    "type": "experience",
                    "milestone": milestone,
                    "description": f"After {exp_years} total years of experience"
                })
                
        # Role-based milestones
        if current_exp < 5:
            milestones.append({
                "year": 3,
                "type": "role",
                "milestone": "Team Lead opportunity",
                "description": "Ready for first leadership role"
            })
            
        if current_exp < 8:
            milestones.append({
                "year": 5,
                "type": "role",
                "milestone": "Manager/Architect role",
                "description": "Transition to senior positions"
            })
            
        # Skill milestones
        milestones.extend([
            {
                "year": 2,
                "type": "skill",
                "milestone": "Cloud certification",
                "description": "Complete major cloud platform certification"
            },
            {
                "year": 4,
                "type": "skill",
                "milestone": "Domain expertise",
                "description": "Recognized expert in specific technology domain"
            }
        ])
        
        # Sort by year and filter
        milestones = sorted([m for m in milestones if m["year"] <= years], key=lambda x: x["year"])
        
        return milestones
        
    def _calculate_investment_roi(self, cv_profile: CVProfile) -> Dict[str, Any]:
        """Calculate ROI for various career investments."""
        
        investments = []
        
        # Education ROI
        education_options = {
            "MBA": {
                "cost": 50,  # Million IDR
                "duration_years": 2,
                "salary_increase_percentage": 25,
                "suitable_for": ["mid", "senior"]
            },
            "Technical Certification": {
                "cost": 5,
                "duration_years": 0.25,
                "salary_increase_percentage": 10,
                "suitable_for": ["junior", "mid", "senior"]
            },
            "Bootcamp": {
                "cost": 20,
                "duration_years": 0.5,
                "salary_increase_percentage": 15,
                "suitable_for": ["entry", "junior", "mid"]
            },
            "Online Courses": {
                "cost": 2,
                "duration_years": 0.5,
                "salary_increase_percentage": 5,
                "suitable_for": ["all"]
            }
        }
        
        current_level = cv_profile.experience_level.value
        base_salary = 50  # Assume base for calculation
        
        for edu_type, details in education_options.items():
            if current_level in details["suitable_for"] or details["suitable_for"] == ["all"]:
                # Calculate ROI
                salary_increase = base_salary * (details["salary_increase_percentage"] / 100)
                annual_return = salary_increase * 12
                payback_period = details["cost"] / annual_return if annual_return > 0 else float('inf')
                
                # 5-year ROI
                total_return_5y = (annual_return * 5) - details["cost"]
                roi_percentage = (total_return_5y / details["cost"] * 100) if details["cost"] > 0 else 0
                
                investments.append({
                    "type": edu_type,
                    "cost": details["cost"],
                    "duration": details["duration_years"],
                    "expected_salary_increase": details["salary_increase_percentage"],
                    "payback_period_years": round(payback_period, 1),
                    "roi_5_years": round(roi_percentage, 1),
                    "recommendation": "Recommended" if roi_percentage > 100 else "Consider carefully"
                })
                
        # Sort by ROI
        investments.sort(key=lambda x: x["roi_5_years"], reverse=True)
        
        return {
            "investments": investments,
            "best_roi": investments[0] if investments else None,
            "quick_wins": [inv for inv in investments if inv["duration"] <= 0.5],
            "long_term": [inv for inv in investments if inv["duration"] > 1]
        }
        
    def _analyze_market_trends(self, industry: Optional[Any]) -> Dict[str, Any]:
        """Analyze market trends for career planning."""
        
        trends = {
            "Technology": {
                "growth_rate": 15,
                "hot_skills": ["AI/ML", "Cloud", "Cybersecurity", "Blockchain"],
                "declining_skills": ["Legacy systems", "Basic HTML/CSS", "Manual QA"],
                "future_outlook": "Excellent - Continuous innovation and digital transformation",
                "job_security": "High - Tech talent always in demand",
                "remote_opportunities": "Abundant - 80% roles offer remote"
            },
            "Banking": {
                "growth_rate": 8,
                "hot_skills": ["Fintech", "Digital Banking", "Risk Analytics", "Compliance Tech"],
                "declining_skills": ["Traditional banking ops", "Manual processing"],
                "future_outlook": "Good - Digital transformation ongoing",
                "job_security": "Moderate - Automation impact",
                "remote_opportunities": "Moderate - 40% roles offer remote"
            },
            "default": {
                "growth_rate": 10,
                "hot_skills": ["Digital skills", "Data analysis", "Automation"],
                "declining_skills": ["Manual processes", "Paper-based work"],
                "future_outlook": "Moderate - Depends on digital adoption",
                "job_security": "Moderate - Varies by role",
                "remote_opportunities": "Growing - 30% roles offer remote"
            }
        }
        
        industry_name = industry.value if industry else "default"
        market_data = trends.get(industry_name, trends["default"])
        
        # Add predictive insights
        market_data["predictions"] = {
            "5_year_outlook": self._generate_5_year_prediction(industry_name),
            "emerging_roles": self._get_emerging_roles(industry_name),
            "salary_trend": "Upward" if market_data["growth_rate"] > 10 else "Stable"
        }
        
        return market_data
        
    def _generate_5_year_prediction(self, industry: str) -> str:
        """Generate 5-year industry prediction."""
        
        predictions = {
            "Technology": "AI will reshape all tech roles. Full-stack + AI skills will command premium salaries.",
            "Banking": "Digital banking will dominate. Traditional roles will merge with tech.",
            "default": "Digital transformation will accelerate. Tech skills become mandatory."
        }
        
        return predictions.get(industry, predictions["default"])
        
    def _get_emerging_roles(self, industry: str) -> List[str]:
        """Get emerging roles by industry."""
        
        emerging_roles = {
            "Technology": [
                "AI Engineer",
                "ML Ops Engineer",
                "Cloud Security Architect",
                "Blockchain Developer",
                "Quantum Computing Researcher"
            ],
            "Banking": [
                "Digital Banking Product Manager",
                "Fintech Integration Specialist",
                "Cryptocurrency Analyst",
                "RegTech Developer"
            ],
            "default": [
                "Data Analyst",
                "Digital Transformation Manager",
                "Automation Specialist"
            ]
        }
        
        return emerging_roles.get(industry, emerging_roles["default"])
        
    def _generate_career_recommendations(self, cv_profile: CVProfile) -> List[str]:
        """Generate personalized career recommendations."""
        
        recommendations = []
        
        # Experience-based recommendations
        if cv_profile.total_experience_years < 5:
            recommendations.append(
                "Focus on building deep technical expertise in 2-3 core technologies. "
                "This is your foundation-building phase."
            )
        elif cv_profile.total_experience_years < 10:
            recommendations.append(
                "Time to decide: technical specialist or management track? "
                "Start developing skills for your chosen path."
            )
        else:
            recommendations.append(
                "Consider strategic roles or consulting. Your experience is valuable "
                "for mentoring and architectural decisions."
            )
            
        # Skill-based recommendations
        if len(cv_profile.technical_skills) < 5:
            recommendations.append(
                "Expand your technical skill set. Modern roles require diverse skills. "
                "Aim for 8-10 complementary technologies."
            )
            
        # Education recommendations
        if cv_profile.education_level.value == "bachelor":
            recommendations.append(
                "Consider specialized certifications or a Master's degree "
                "for 15-25% salary boost and leadership roles."
            )
            
        # Industry-specific
        if cv_profile.detected_industry:
            if cv_profile.detected_industry.value == "Technology":
                recommendations.append(
                    "Stay updated with AI/ML trends. These skills will be mandatory "
                    "in 3-5 years for senior roles."
                )
                
        # Career pivots
        recommendations.append(
            "Build a strong professional network. 70% of senior roles "
            "are filled through referrals, not job postings."
        )
        
        return recommendations

    def generate_career_report(self, predictions: Dict[str, Any]) -> str:
        """Generate a formatted career prediction report."""
        
        report = []
        report.append("=" * 60)
        report.append("CAREER PATH PREDICTION REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Current State
        current = predictions["current_state"]
        report.append("CURRENT POSITION")
        report.append("-" * 30)
        report.append(f"Title: {current['title']}")
        report.append(f"Experience: {current['experience_years']} years ({current['experience_level']})")
        report.append(f"Industry: {current['industry']}")
        report.append(f"Current Salary: IDR {current['current_salary']}M/month")
        report.append(f"Key Skills: {', '.join(current['key_skills'])}")
        report.append("")
        
        # Career Paths
        report.append("RECOMMENDED CAREER PATHS")
        report.append("-" * 30)
        for i, path in enumerate(predictions["career_paths"], 1):
            report.append(f"\n{i}. {path['path_name']} (Probability: {path['probability']*100:.0f}%)")
            report.append(f"   Description: {path['description']}")
            report.append(f"   Peak Salary: IDR {path['peak_salary']}M/month")
            report.append(f"   Time to Peak: {path['time_to_peak']} years")
            report.append("   Career Progression:")
            for role in path["progression"][:3]:  # Show first 3 roles
                report.append(f"     Year {role['year']}: {role['role']} (IDR {role['salary']}M)")
        report.append("")
        
        # Salary Progression
        salary_summary = predictions["salary_progression"]["summary"]
        report.append("SALARY PROJECTION SUMMARY")
        report.append("-" * 30)
        report.append(f"Current: IDR {salary_summary['current_salary']}M/month")
        report.append(f"10-Year Projection: IDR {salary_summary['projected_salary']}M/month")
        report.append(f"Total Increase: {salary_summary['percentage_increase']:.1f}%")
        report.append(f"Annual Growth Rate (CAGR): {salary_summary['cagr']}%")
        report.append("")
        
        # Key Milestones
        report.append("KEY CAREER MILESTONES")
        report.append("-" * 30)
        for milestone in predictions["milestones"][:5]:  # Show top 5
            report.append(f"Year {milestone['year']}: {milestone['milestone']}")
            report.append(f"  {milestone['description']}")
        report.append("")
        
        # Top Recommendations
        report.append("TOP RECOMMENDATIONS")
        report.append("-" * 30)
        for i, rec in enumerate(predictions["recommendations"][:3], 1):
            report.append(f"{i}. {rec}")
        report.append("")
        
        # Market Trends
        trends = predictions["market_trends"]
        report.append("MARKET OUTLOOK")
        report.append("-" * 30)
        report.append(f"Industry Growth Rate: {trends['growth_rate']}%")
        report.append(f"Hot Skills: {', '.join(trends['hot_skills'][:3])}")
        report.append(f"Future Outlook: {trends['future_outlook']}")
        report.append("")
        
        report.append("=" * 60)
        
        return "\n".join(report)

# === MAIN FUNCTION AND USAGE EXAMPLES ===

def create_sample_profile() -> Tuple[CVProfile, SalaryEstimation]:
    """Create a sample CV profile for demonstration."""
    
    profile = CVProfile(
        current_title="Senior Software Engineer",
        total_experience_years=6,
        experience_level=ExperienceLevel.MID,
        detected_industry=Industry.TECHNOLOGY,
        technical_skills=[
            "Python", "Java", "AWS", "Docker", "Kubernetes",
            "PostgreSQL", "React", "Node.js"
        ],
        soft_skills=[
            "Team Collaboration", "Problem Solving", "Communication"
        ],
        education_level=EducationLevel.BACHELOR
    )
    
    salary = SalaryEstimation(
        estimated_salary_avg=45,  # 45M IDR/month
        estimated_salary_min=40,
        estimated_salary_max=50,
        confidence=0.85
    )
    
    return profile, salary

def main():
    """Main function to demonstrate Career Path Predictor."""
    
    print("Career Path Predictor - Demo")
    print("=" * 60)
    
    # Initialize predictor
    predictor = CareerPredictor()
    
    # Create sample profile
    profile, current_salary = create_sample_profile()
    
    # Run prediction
    print("\nAnalyzing career path...")
    predictions = predictor.predict_career_path(
        cv_profile=profile,
        current_estimation=current_salary,
        years_to_predict=10,
        industry_growth="high_growth"  # Tech industry growth
    )
    
    # Generate and print report
    report = predictor.generate_career_report(predictions)
    print(report)
    
    # Optional: Save to file
    save_to_file = input("\nSave report to file? (y/n): ")
    if save_to_file.lower() == 'y':
        filename = f"career_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w') as f:
            f.write(report)
        print(f"Report saved to {filename}")
    
    # Interactive mode
    print("\n" + "=" * 60)
    print("INTERACTIVE MODE")
    print("=" * 60)
    
    while True:
        print("\nOptions:")
        print("1. View detailed salary progression")
        print("2. View skill roadmap")
        print("3. View investment ROI analysis")
        print("4. Create custom profile")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ")
        
        if choice == '1':
            print("\nDETAILED SALARY PROGRESSION")
            print("-" * 30)
            for proj in predictions["salary_progression"]["projections"]:
                print(f"Year {proj['year']}: IDR {proj['salary']}M/month "
                      f"(Level: {proj['level']}, "
                      f"Increase: IDR {proj['annual_increase']}M)")
                
        elif choice == '2':
            print("\nSKILL DEVELOPMENT ROADMAP")
            print("-" * 30)
            for stage in predictions["skill_roadmap"]:
                print(f"\nYear {stage['year']}: {stage['focus_area']}")
                print(f"  Technical: {', '.join(stage['technical_skills'])}")
                print(f"  Soft Skills: {', '.join(stage['soft_skills'])}")
                print(f"  Certifications: {', '.join(stage['certifications'])}")
                
        elif choice == '3':
            print("\nINVESTMENT ROI ANALYSIS")
            print("-" * 30)
            for inv in predictions["investment_roi"]["investments"]:
                print(f"\n{inv['type']}:")
                print(f"  Cost: IDR {inv['cost']}M")
                print(f"  Duration: {inv['duration']} years")
                print(f"  Expected Salary Increase: {inv['expected_salary_increase']}%")
                print(f"  5-Year ROI: {inv['roi_5_years']}%")
                print(f"  Recommendation: {inv['recommendation']}")
                
        elif choice == '4':
            print("\nCREATE CUSTOM PROFILE")
            print("-" * 30)
            
            # Get user input
            title = input("Current job title: ")
            exp_years = float(input("Years of experience: "))
            
            # Determine experience level
            if exp_years < 2:
                exp_level = ExperienceLevel.ENTRY
            elif exp_years < 5:
                exp_level = ExperienceLevel.JUNIOR
            elif exp_years < 8:
                exp_level = ExperienceLevel.MID
            elif exp_years < 12:
                exp_level = ExperienceLevel.SENIOR
            else:
                exp_level = ExperienceLevel.EXPERT
                
            industry = input("Industry (Technology/Banking/Healthcare/Retail/Manufacturing): ")
            try:
                industry_enum = Industry[industry.upper()]
            except:
                industry_enum = Industry.TECHNOLOGY
                
            current_sal = float(input("Current salary (in millions IDR/month): "))
            
            # Create new profile
            new_profile = CVProfile(
                current_title=title,
                total_experience_years=exp_years,
                experience_level=exp_level,
                detected_industry=industry_enum,
                technical_skills=["Python", "Cloud", "Data Analysis"],  # Default skills
                soft_skills=["Communication", "Leadership"],
                education_level=EducationLevel.BACHELOR
            )
            
            new_salary = SalaryEstimation(
                estimated_salary_avg=current_sal,
                estimated_salary_min=current_sal * 0.9,
                estimated_salary_max=current_sal * 1.1,
                confidence=0.8
            )
            
            # Run new prediction
            print("\nGenerating custom career prediction...")
            custom_predictions = predictor.predict_career_path(
                cv_profile=new_profile,
                current_estimation=new_salary,
                years_to_predict=10
            )
            
            # Show summary
            custom_report = predictor.generate_career_report(custom_predictions)
            print(custom_report)
            
        elif choice == '5':
            print("\nThank you for using Career Path Predictor!")
            break
            
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run main program
    main()