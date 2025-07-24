"""Salary Matcher module for calculating salary estimations."""

import logging
from typing import List, Dict, Any, Tuple, Optional
import numpy as np
from datetime import datetime

from config.settings import (
    EXPERIENCE_MULTIPLIERS,
    EDUCATION_MULTIPLIERS,
    SKILL_MATCH_WEIGHTS
)
from models.schemas import (
    CVProfile,
    SalaryEstimation,
    SalaryData,
    RAGQuery,
    RAGResponse
)
from src.simple_rag_engine import SimpleRAGEngine
from src.llm_client import LLMClient

logger = logging.getLogger(__name__)


class SalaryMatcher:
    """Match CV profiles to salary data and generate estimations."""
    
    def __init__(self):
        self.rag_engine = SimpleRAGEngine()
        self.llm_client = LLMClient()
        
        # Location multipliers for major Indonesian cities
        self.location_multipliers = {
            "jakarta": 1.0,
            "surabaya": 0.85,
            "bandung": 0.85,
            "medan": 0.80,
            "semarang": 0.80,
            "other": 0.75
        }
        
    def estimate_salary(self, cv_profile: CVProfile) -> SalaryEstimation:
        """Estimate salary based on CV profile."""
        try:
            # Create RAG query
            rag_query = RAGQuery(
                query_text=f"{cv_profile.current_title} {cv_profile.detected_industry}",
                cv_profile=cv_profile,
                context_window=10,
                include_similar_roles=True
            )
            
            # Search for relevant salaries
            rag_response = self.rag_engine.search_salaries(rag_query)
            
            # Get matched positions
            matched_positions = self._match_positions(cv_profile, rag_response)
            
            # Calculate base salary range
            base_min, base_max, base_avg = self._calculate_base_salary(matched_positions)
            
            # Apply multipliers
            exp_factor = EXPERIENCE_MULTIPLIERS.get(cv_profile.experience_level.value, 1.0)
            edu_factor = EDUCATION_MULTIPLIERS.get(cv_profile.education_level.value, 1.0)
            skills_factor = self._calculate_skills_factor(cv_profile, matched_positions)
            location_factor = self._get_location_factor(cv_profile.location)
            
            # Calculate final estimates
            final_min = int(base_min * exp_factor * edu_factor * skills_factor * location_factor)
            final_max = int(base_max * exp_factor * edu_factor * skills_factor * location_factor)
            final_avg = int(base_avg * exp_factor * edu_factor * skills_factor * location_factor)
            
            # Get best match
            best_match = matched_positions[0] if matched_positions else None
            
            # Generate LLM analysis
            llm_analysis = self.llm_client.analyze_cv_for_salary_sync(
                cv_profile.raw_text[:2000],  # Limit text
                matched_positions[:5],
                cv_profile.detected_industry.value if cv_profile.detected_industry else "General"
            )
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                cv_profile,
                matched_positions,
                llm_analysis
            )
            
            return SalaryEstimation(
                estimated_salary_min=final_min,
                estimated_salary_max=final_max,
                estimated_salary_avg=final_avg,
                matched_positions=matched_positions,
                best_match_title=best_match["title"] if best_match else None,
                match_confidence=rag_response.confidence_score,
                experience_factor=exp_factor,
                education_factor=edu_factor,
                skills_factor=skills_factor,
                location_factor=location_factor,
                explanation=llm_analysis.get("explanation", ""),
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error estimating salary: {str(e)}")
            # Return default estimation
            return self._get_default_estimation(cv_profile)
            
    def _match_positions(self, cv_profile: CVProfile, rag_response: RAGResponse) -> List[Dict[str, Any]]:
        """Match CV profile to salary positions."""
        matched = []
        
        for salary_data in rag_response.relevant_salaries:
            match_score = self._calculate_match_score(cv_profile, salary_data)
            
            matched.append({
                "title": salary_data.job_title,
                "industry": salary_data.industry,
                "salary": salary_data.average_monthly_salary_idr,
                "match_score": match_score,
                "category": salary_data.category
            })
            
        # Sort by match score
        matched.sort(key=lambda x: x["match_score"], reverse=True)
        
        return matched
        
    def _calculate_match_score(self, cv_profile: CVProfile, salary_data: SalaryData) -> float:
        """Calculate match score between CV and salary position."""
        score = 0.0
        
        # Title similarity
        if cv_profile.current_title and salary_data.job_title:
            title_similarity = self._calculate_text_similarity(
                cv_profile.current_title.lower(),
                salary_data.job_title.lower()
            )
            score += title_similarity * 0.4
            
        # Industry match
        if cv_profile.detected_industry and salary_data.industry:
            if cv_profile.detected_industry.value == salary_data.industry:
                score += 0.3
            elif self._are_industries_related(cv_profile.detected_industry.value, salary_data.industry):
                score += 0.15
                
        # Experience level match
        exp_match = self._match_experience_to_role(cv_profile.experience_level.value, salary_data.job_title)
        score += exp_match * 0.3
        
        return min(1.0, score)
        
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple text similarity."""
        # Simple word overlap calculation
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
            
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
        
    def _are_industries_related(self, industry1: str, industry2: str) -> bool:
        """Check if two industries are related."""
        related_industries = {
            "Technology": ["Engineering & Manufacturing", "Banking & Financial Services"],
            "Accounting & Finance": ["Banking & Financial Services", "Executive"],
            "Sales & Marketing": ["Retail", "Technology"],
            "Human Resources": ["Executive", "Healthcare & Life Sciences"],
        }
        
        if industry1 in related_industries:
            return industry2 in related_industries[industry1]
        if industry2 in related_industries:
            return industry1 in related_industries[industry2]
            
        return False
        
    def _match_experience_to_role(self, experience_level: str, job_title: str) -> float:
        """Match experience level to job title."""
        job_title_lower = job_title.lower()
        
        # Define expected experience levels for different roles
        if "junior" in job_title_lower or "assistant" in job_title_lower:
            expected = ["entry", "junior"]
        elif "senior" in job_title_lower or "lead" in job_title_lower:
            expected = ["senior", "expert"]
        elif "manager" in job_title_lower or "head" in job_title_lower:
            expected = ["mid", "senior", "expert"]
        elif "director" in job_title_lower or "vp" in job_title_lower or "chief" in job_title_lower:
            expected = ["expert"]
        else:
            expected = ["junior", "mid"]
            
        if experience_level in expected:
            return 1.0
        elif self._is_adjacent_level(experience_level, expected):
            return 0.6
        else:
            return 0.3
            
    def _is_adjacent_level(self, level: str, expected: List[str]) -> bool:
        """Check if experience level is adjacent to expected levels."""
        level_order = ["entry", "junior", "mid", "senior", "expert"]
        
        try:
            level_idx = level_order.index(level)
            for exp in expected:
                exp_idx = level_order.index(exp)
                if abs(level_idx - exp_idx) == 1:
                    return True
        except ValueError:
            pass
            
        return False
        
    def _calculate_base_salary(self, matched_positions: List[Dict[str, Any]]) -> Tuple[int, int, int]:
        """Calculate base salary range from matched positions."""
        if not matched_positions:
            return 20, 40, 30  # Default range
            
        # Use top 5 matches
        top_matches = matched_positions[:5]
        salaries = [p["salary"] for p in top_matches]
        
        # Weight by match score
        weights = [p["match_score"] for p in top_matches]
        
        # Weighted average
        weighted_avg = np.average(salaries, weights=weights)
        
        # Calculate range
        min_salary = int(weighted_avg * 0.8)
        max_salary = int(weighted_avg * 1.2)
        
        return min_salary, max_salary, int(weighted_avg)
        
    def _calculate_skills_factor(self, cv_profile: CVProfile, matched_positions: List[Dict[str, Any]]) -> float:
        """Calculate skills matching factor."""
        if not cv_profile.technical_skills:
            return 0.9  # Slight penalty for no skills listed
            
        # For now, use a simple calculation based on number of skills
        # More sophisticated: match against required skills for positions
        num_skills = len(cv_profile.technical_skills) + len(cv_profile.soft_skills)
        
        if num_skills >= 15:
            return 1.1
        elif num_skills >= 10:
            return 1.05
        elif num_skills >= 5:
            return 1.0
        else:
            return 0.95
            
    def _get_location_factor(self, location: Optional[str]) -> float:
        """Get location multiplier."""
        if not location:
            return 1.0  # Assume Jakarta if not specified
            
        location_lower = location.lower()
        
        for city, multiplier in self.location_multipliers.items():
            if city in location_lower:
                return multiplier
                
        return self.location_multipliers["other"]
        
    def _generate_recommendations(
        self, 
        cv_profile: CVProfile,
        matched_positions: List[Dict[str, Any]],
        llm_analysis: Dict[str, Any]
    ) -> List[str]:
        """Generate career recommendations."""
        recommendations = []
        
        # Add LLM recommendations if available
        if llm_analysis.get("recommendations"):
            recommendations.extend(llm_analysis["recommendations"])
            
        # Add specific recommendations based on analysis
        if cv_profile.experience_level.value in ["entry", "junior"]:
            recommendations.append(
                "Focus on building technical expertise and obtaining relevant certifications "
                "to accelerate career progression."
            )
            
        if not cv_profile.certifications:
            recommendations.append(
                "Consider obtaining industry-relevant certifications to increase market value "
                "and salary potential."
            )
            
        if matched_positions and matched_positions[0]["salary"] > 50:
            recommendations.append(
                "Your profile matches senior-level positions. Consider negotiating for "
                "leadership roles or exploring executive opportunities."
            )
            
        # Limit to 5 recommendations
        return recommendations[:5]
        
    def _get_default_estimation(self, cv_profile: CVProfile) -> SalaryEstimation:
        """Get default salary estimation when error occurs."""
        # Basic estimation based on experience level
        base_salaries = {
            "entry": (10, 20, 15),
            "junior": (20, 35, 27),
            "mid": (35, 60, 47),
            "senior": (60, 100, 80),
            "expert": (100, 200, 150)
        }
        
        min_sal, max_sal, avg_sal = base_salaries.get(
            cv_profile.experience_level.value,
            (25, 50, 37)
        )
        
        return SalaryEstimation(
            estimated_salary_min=min_sal,
            estimated_salary_max=max_sal,
            estimated_salary_avg=avg_sal,
            matched_positions=[],
            match_confidence=0.5,
            explanation="Default estimation based on experience level. Upload a complete CV for more accurate results.",
            recommendations=[
                "Ensure your CV includes detailed work experience and skills",
                "Add relevant certifications and achievements",
                "Include specific job titles and responsibilities"
            ]
        )