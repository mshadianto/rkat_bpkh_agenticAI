"""Multi-CV Comparison module for side-by-side analysis."""

import logging
from typing import List, Dict, Any, Tuple, Optional
import numpy as np
import pandas as pd
from datetime import datetime

from models.schemas import CVProfile, SalaryEstimation
from src.skills_analyzer import SkillsGapAnalyzer

logger = logging.getLogger(__name__)


class CVComparison:
    """Compare multiple CVs for HR and recruitment purposes."""
    
    def __init__(self):
        self.skills_analyzer = SkillsGapAnalyzer()
        
        # Comparison weights
        self.weights = {
            "experience": 0.25,
            "education": 0.15,
            "skills": 0.30,
            "salary_fit": 0.20,
            "culture_fit": 0.10
        }
        
    def compare_cvs(
        self,
        cv_profiles: List[Tuple[CVProfile, SalaryEstimation]],
        target_role: str,
        target_industry: str,
        budget_range: Optional[Tuple[int, int]] = None
    ) -> Dict[str, Any]:
        """Compare multiple CV profiles."""
        
        if len(cv_profiles) < 2:
            raise ValueError("Need at least 2 CVs to compare")
            
        comparison_results = {
            "profiles": [],
            "rankings": {},
            "insights": {},
            "recommendations": [],
            "best_fit": None,
            "comparison_matrix": None
        }
        
        # Analyze each profile
        for idx, (profile, estimation) in enumerate(cv_profiles):
            profile_analysis = self._analyze_profile(
                profile, estimation, target_role, target_industry, budget_range
            )
            profile_analysis["index"] = idx
            comparison_results["profiles"].append(profile_analysis)
            
        # Create comparison matrix
        comparison_results["comparison_matrix"] = self._create_comparison_matrix(
            comparison_results["profiles"]
        )
        
        # Rank candidates
        comparison_results["rankings"] = self._rank_candidates(
            comparison_results["profiles"]
        )
        
        # Generate insights
        comparison_results["insights"] = self._generate_comparison_insights(
            comparison_results["profiles"],
            target_role,
            target_industry
        )
        
        # Determine best fit
        comparison_results["best_fit"] = comparison_results["rankings"]["overall"][0]
        
        # Generate recommendations
        comparison_results["recommendations"] = self._generate_recommendations(
            comparison_results["profiles"],
            comparison_results["rankings"],
            budget_range
        )
        
        return comparison_results
        
    def _analyze_profile(
        self,
        profile: CVProfile,
        estimation: SalaryEstimation,
        target_role: str,
        target_industry: str,
        budget_range: Optional[Tuple[int, int]]
    ) -> Dict[str, Any]:
        """Analyze individual profile for comparison."""
        
        # Skills analysis
        skills_analysis = self.skills_analyzer.analyze_skill_gaps(
            profile, target_role, target_industry
        )
        
        # Calculate scores
        experience_score = self._calculate_experience_score(
            profile.total_experience_years,
            profile.experience_level.value,
            target_role
        )
        
        education_score = self._calculate_education_score(
            profile.education_level.value,
            target_role
        )
        
        skills_score = skills_analysis["skill_match_score"]
        
        salary_fit_score = self._calculate_salary_fit_score(
            estimation,
            budget_range
        )
        
        culture_fit_score = self._calculate_culture_fit_score(
            profile,
            target_industry
        )
        
        # Overall score
        overall_score = (
            experience_score * self.weights["experience"] +
            education_score * self.weights["education"] +
            skills_score * self.weights["skills"] +
            salary_fit_score * self.weights["salary_fit"] +
            culture_fit_score * self.weights["culture_fit"]
        )
        
        return {
            "name": profile.full_name or f"Candidate {profile.email or 'Unknown'}",
            "current_title": profile.current_title,
            "experience_years": profile.total_experience_years,
            "experience_level": profile.experience_level.value,
            "education_level": profile.education_level.value,
            "skills_count": len(profile.technical_skills) + len(profile.soft_skills),
            "key_skills": profile.technical_skills[:5],
            "salary_expectation": estimation.estimated_salary_avg,
            "salary_range": (estimation.estimated_salary_min, estimation.estimated_salary_max),
            "scores": {
                "experience": experience_score,
                "education": education_score,
                "skills": skills_score,
                "salary_fit": salary_fit_score,
                "culture_fit": culture_fit_score,
                "overall": overall_score
            },
            "skills_analysis": skills_analysis,
            "strengths": self._identify_strengths(profile, skills_analysis),
            "weaknesses": self._identify_weaknesses(profile, skills_analysis),
            "unique_value": self._identify_unique_value(profile)
        }
        
    def _calculate_experience_score(
        self,
        years: float,
        level: str,
        target_role: str
    ) -> float:
        """Calculate experience score (0-100)."""
        
        # Ideal experience years for different roles
        ideal_experience = {
            "junior": (1, 3),
            "mid": (3, 7),
            "senior": (7, 12),
            "lead": (10, 15),
            "manager": (8, 15),
            "director": (12, 20)
        }
        
        # Find matching role level
        role_lower = target_role.lower()
        ideal_range = (3, 7)  # Default
        
        for role_key, range_val in ideal_experience.items():
            if role_key in role_lower:
                ideal_range = range_val
                break
                
        # Calculate score based on fit
        min_years, max_years = ideal_range
        
        if min_years <= years <= max_years:
            score = 100
        elif years < min_years:
            # Under-experienced
            score = max(40, 100 * (years / min_years))
        else:
            # Over-experienced (might be overqualified)
            over_factor = min(2, (years - max_years) / max_years)
            score = max(60, 100 - (over_factor * 20))
            
        return round(score, 1)
        
    def _calculate_education_score(self, education_level: str, target_role: str) -> float:
        """Calculate education score (0-100)."""
        
        # Education requirements by role
        role_education = {
            "engineer": "bachelor",
            "developer": "bachelor",
            "analyst": "bachelor",
            "scientist": "master",
            "manager": "bachelor",
            "director": "master",
            "executive": "master"
        }
        
        # Education hierarchy
        edu_hierarchy = {
            "high_school": 1,
            "diploma": 2,
            "bachelor": 3,
            "master": 4,
            "phd": 5
        }
        
        # Find required education
        required_edu = "bachelor"  # Default
        role_lower = target_role.lower()
        
        for role_key, edu in role_education.items():
            if role_key in role_lower:
                required_edu = edu
                break
                
        # Calculate score
        current_level = edu_hierarchy.get(education_level, 3)
        required_level = edu_hierarchy.get(required_edu, 3)
        
        if current_level >= required_level:
            score = min(100, 80 + (current_level - required_level) * 10)
        else:
            score = max(40, 100 - (required_level - current_level) * 20)
            
        return round(score, 1)
        
    def _calculate_salary_fit_score(
        self,
        estimation: SalaryEstimation,
        budget_range: Optional[Tuple[int, int]]
    ) -> float:
        """Calculate salary fit score (0-100)."""
        
        if not budget_range:
            return 80  # Default score if no budget specified
            
        min_budget, max_budget = budget_range
        expected_salary = estimation.estimated_salary_avg
        
        if min_budget <= expected_salary <= max_budget:
            # Perfect fit
            score = 100
        elif expected_salary < min_budget:
            # Under budget (good for employer)
            under_percentage = (min_budget - expected_salary) / min_budget
            score = min(95, 100 - under_percentage * 20)
        else:
            # Over budget
            over_percentage = (expected_salary - max_budget) / max_budget
            score = max(20, 100 - over_percentage * 100)
            
        return round(score, 1)
        
    def _calculate_culture_fit_score(self, profile: CVProfile, target_industry: str) -> float:
        """Calculate culture fit score based on soft skills and industry alignment."""
        
        score = 70  # Base score
        
        # Industry alignment
        if profile.detected_industry and profile.detected_industry.value == target_industry:
            score += 15
            
        # Soft skills indicators
        culture_indicators = {
            "teamwork": ["team", "collaboration", "cooperative"],
            "leadership": ["lead", "manage", "mentor", "guide"],
            "communication": ["communication", "presentation", "interpersonal"],
            "adaptability": ["agile", "flexible", "adaptable", "dynamic"],
            "innovation": ["innovative", "creative", "problem-solving"]
        }
        
        # Check soft skills
        soft_skills_lower = [s.lower() for s in profile.soft_skills]
        
        for indicator, keywords in culture_indicators.items():
            if any(keyword in skill for skill in soft_skills_lower for keyword in keywords):
                score += 3
                
        # Language skills (important in Indonesia)
        if profile.languages:
            if "english" in [l.lower() for l in profile.languages]:
                score += 5
            if len(profile.languages) > 2:
                score += 3
                
        return min(100, round(score, 1))
        
    def _identify_strengths(
        self,
        profile: CVProfile,
        skills_analysis: Dict[str, Any]
    ) -> List[str]:
        """Identify candidate strengths."""
        strengths = []
        
        # Experience strength
        if profile.total_experience_years > 5:
            strengths.append(f"Strong experience ({profile.total_experience_years:.1f} years)")
            
        # Skills strength
        if skills_analysis["skill_match_score"] > 80:
            strengths.append("Excellent skill match")
        
        valuable_skills = skills_analysis["market_insights"]["your_valuable_skills"]
        if valuable_skills:
            top_skill = valuable_skills[0]["skill"]
            strengths.append(f"High-demand skill: {top_skill}")
            
        # Education strength
        if profile.education_level.value in ["master", "phd"]:
            strengths.append(f"Advanced education ({profile.education_level.value})")
            
        # Certifications
        if profile.certifications:
            strengths.append(f"{len(profile.certifications)} professional certifications")
            
        return strengths[:4]  # Top 4 strengths
        
    def _identify_weaknesses(
        self,
        profile: CVProfile,
        skills_analysis: Dict[str, Any]
    ) -> List[str]:
        """Identify candidate weaknesses."""
        weaknesses = []
        
        # Experience gaps
        if profile.total_experience_years < 2:
            weaknesses.append("Limited experience")
            
        # Missing skills
        missing_required = skills_analysis["missing_required"]
        if len(missing_required) > 3:
            weaknesses.append(f"Missing {len(missing_required)} required skills")
            
        # Skill match
        if skills_analysis["skill_match_score"] < 60:
            weaknesses.append("Low skill match score")
            
        # No certifications
        if not profile.certifications:
            weaknesses.append("No professional certifications")
            
        return weaknesses[:3]  # Top 3 weaknesses
        
    def _identify_unique_value(self, profile: CVProfile) -> List[str]:
        """Identify unique value propositions."""
        unique_values = []
        
        # Rare skills
        rare_skills = ["blockchain", "quantum", "ai/ml", "kubernetes", "golang"]
        for skill in profile.technical_skills:
            if any(rare in skill.lower() for rare in rare_skills):
                unique_values.append(f"Rare skill: {skill}")
                
        # Multiple languages
        if len(profile.languages) > 3:
            unique_values.append(f"Polyglot ({len(profile.languages)} languages)")
            
        # Industry + technical combination
        if profile.detected_industry and len(profile.technical_skills) > 10:
            unique_values.append(f"Deep {profile.detected_industry.value} expertise")
            
        return unique_values[:2]
        
    def _create_comparison_matrix(self, profiles: List[Dict[str, Any]]) -> pd.DataFrame:
        """Create comparison matrix for visualization."""
        
        # Extract key metrics
        data = []
        for profile in profiles:
            data.append({
                "Candidate": profile["name"],
                "Experience (years)": profile["experience_years"],
                "Education": profile["education_level"],
                "Skills Count": profile["skills_count"],
                "Salary Expectation": profile["salary_expectation"],
                "Overall Score": profile["scores"]["overall"],
                "Experience Score": profile["scores"]["experience"],
                "Skills Match": profile["scores"]["skills"],
                "Salary Fit": profile["scores"]["salary_fit"],
                "Culture Fit": profile["scores"]["culture_fit"]
            })
            
        return pd.DataFrame(data)
        
    def _rank_candidates(self, profiles: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Rank candidates by different criteria."""
        
        rankings = {
            "overall": [],
            "experience": [],
            "skills": [],
            "salary_fit": [],
            "value_for_money": []
        }
        
        # Overall ranking
        overall_sorted = sorted(
            profiles,
            key=lambda x: x["scores"]["overall"],
            reverse=True
        )
        
        for rank, profile in enumerate(overall_sorted, 1):
            rankings["overall"].append({
                "rank": rank,
                "name": profile["name"],
                "score": profile["scores"]["overall"],
                "index": profile["index"]
            })
            
        # Other rankings
        criteria = ["experience", "skills", "salary_fit"]
        for criterion in criteria:
            sorted_profiles = sorted(
                profiles,
                key=lambda x: x["scores"][criterion],
                reverse=True
            )
            
            for rank, profile in enumerate(sorted_profiles, 1):
                rankings[criterion].append({
                    "rank": rank,
                    "name": profile["name"],
                    "score": profile["scores"][criterion],
                    "index": profile["index"]
                })
                
        # Value for money ranking (skill/salary ratio)
        value_sorted = sorted(
            profiles,
            key=lambda x: x["scores"]["skills"] / max(1, x["salary_expectation"] / 100),
            reverse=True
        )
        
        for rank, profile in enumerate(value_sorted, 1):
            value_score = profile["scores"]["skills"] / max(1, profile["salary_expectation"] / 100)
            rankings["value_for_money"].append({
                "rank": rank,
                "name": profile["name"],
                "score": round(value_score, 2),
                "index": profile["index"]
            })
            
        return rankings
        
    def _generate_comparison_insights(
        self,
        profiles: List[Dict[str, Any]],
        target_role: str,
        target_industry: str
    ) -> Dict[str, Any]:
        """Generate insights from comparison."""
        
        insights = {
            "summary": "",
            "team_composition": "",
            "skill_coverage": {},
            "cost_analysis": {},
            "risk_assessment": []
        }
        
        # Summary
        best_overall = max(profiles, key=lambda x: x["scores"]["overall"])
        most_experienced = max(profiles, key=lambda x: x["experience_years"])
        best_skills = max(profiles, key=lambda x: x["scores"]["skills"])
        most_economical = min(profiles, key=lambda x: x["salary_expectation"])
        
        insights["summary"] = (
            f"{best_overall['name']} is the best overall fit with a score of "
            f"{best_overall['scores']['overall']:.1f}. "
            f"{most_experienced['name']} has the most experience "
            f"({most_experienced['experience_years']:.1f} years). "
            f"{best_skills['name']} has the best skill match "
            f"({best_skills['scores']['skills']:.1f}%). "
            f"{most_economical['name']} is the most economical choice "
            f"(IDR {most_economical['salary_expectation']}M/month)."
        )
        
        # Team composition analysis
        if len(profiles) > 2:
            insights["team_composition"] = self._analyze_team_composition(profiles)
            
        # Skill coverage
        all_skills = set()
        for profile in profiles:
            all_skills.update(profile["key_skills"])
            
        insights["skill_coverage"] = {
            "total_unique_skills": len(all_skills),
            "skill_list": list(all_skills),
            "coverage_score": min(100, len(all_skills) * 5)  # Simple coverage metric
        }
        
        # Cost analysis
        total_cost = sum(p["salary_expectation"] for p in profiles)
        avg_cost = total_cost / len(profiles)
        
        insights["cost_analysis"] = {
            "total_monthly_cost": total_cost,
            "average_cost": round(avg_cost, 1),
            "annual_cost": total_cost * 13,  # Including 13th month
            "cost_variance": round(np.std([p["salary_expectation"] for p in profiles]), 1)
        }
        
        # Risk assessment
        insights["risk_assessment"] = self._assess_risks(profiles)
        
        return insights
        
    def _analyze_team_composition(self, profiles: List[Dict[str, Any]]) -> str:
        """Analyze team composition for multiple hires."""
        
        # Count experience levels
        experience_levels = {}
        for profile in profiles:
            level = profile["experience_level"]
            experience_levels[level] = experience_levels.get(level, 0) + 1
            
        # Generate composition summary
        composition_parts = []
        for level, count in experience_levels.items():
            composition_parts.append(f"{count} {level}")
            
        composition = ", ".join(composition_parts)
        
        # Assess balance
        if len(set(experience_levels.keys())) > 1:
            balance = "Good mix of experience levels"
        elif "senior" in experience_levels or "expert" in experience_levels:
            balance = "Senior-heavy team, consider adding junior members for balance"
        else:
            balance = "Junior-heavy team, consider adding senior leadership"
            
        return f"Team composition: {composition}. {balance}."
        
    def _assess_risks(self, profiles: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Assess hiring risks."""
        risks = []
        
        # Check for overqualification
        for profile in profiles:
            if profile["scores"]["experience"] < 70 and profile["experience_years"] > 10:
                risks.append({
                    "candidate": profile["name"],
                    "risk": "Overqualification",
                    "mitigation": "Discuss growth opportunities and challenges"
                })
                
        # Check for skill gaps
        for profile in profiles:
            if profile["scores"]["skills"] < 60:
                risks.append({
                    "candidate": profile["name"],
                    "risk": "Significant skill gaps",
                    "mitigation": "Plan comprehensive onboarding and training"
                })
                
        # Salary expectations
        for profile in profiles:
            if profile["scores"]["salary_fit"] < 50:
                risks.append({
                    "candidate": profile["name"],
                    "risk": "Salary expectation mismatch",
                    "mitigation": "Negotiate or consider alternative compensation"
                })
                
        return risks[:5]  # Top 5 risks
        
    def _generate_recommendations(
        self,
        profiles: List[Dict[str, Any]],
        rankings: Dict[str, List[Dict[str, Any]]],
        budget_range: Optional[Tuple[int, int]]
    ) -> List[str]:
        """Generate hiring recommendations."""
        
        recommendations = []
        
        # Best overall recommendation
        best_overall = rankings["overall"][0]
        recommendations.append(
            f"Recommended hire: {best_overall['name']} with an overall score of "
            f"{best_overall['score']:.1f}/100."
        )
        
        # Budget consideration
        if budget_range:
            within_budget = [p for p in profiles if p["salary_expectation"] <= budget_range[1]]
            if within_budget:
                best_value = max(within_budget, key=lambda x: x["scores"]["overall"])
                if best_value["name"] != best_overall["name"]:
                    recommendations.append(
                        f"Best within budget: {best_value['name']} "
                        f"(IDR {best_value['salary_expectation']}M/month)"
                    )
                    
        # Team hiring recommendation
        if len(profiles) > 2:
            recommendations.append(
                "For team hiring: Consider mixing experience levels for knowledge transfer "
                "and cost optimization."
            )
            
        # Skill gap consideration
        high_skill_match = [p for p in profiles if p["scores"]["skills"] > 80]
        if not high_skill_match:
            recommendations.append(
                "No candidate has >80% skill match. Consider providing additional training "
                "or adjusting role requirements."
            )
            
        # Fast hiring option
        ready_candidates = [
            p for p in profiles 
            if p["scores"]["overall"] > 75 and p["scores"]["salary_fit"] > 70
        ]
        if ready_candidates:
            recommendations.append(
                f"Fast hiring options: {', '.join([c['name'] for c in ready_candidates[:2]])} "
                "are ready to start with minimal negotiation."
            )
            
        return recommendations