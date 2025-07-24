"""LLM Client for OpenRouter/Qwen3 integration."""

import httpx
import json
import asyncio
from typing import Dict, List, Optional, Any
import logging
from config.settings import (
    OPENROUTER_API_KEY, 
    OPENROUTER_BASE_URL, 
    LLM_MODEL,
    MAX_TOKENS,
    TEMPERATURE
)

logger = logging.getLogger(__name__)


class LLMClient:
    """Client for interacting with Qwen3 via OpenRouter."""
    
    def __init__(self):
        self.api_key = OPENROUTER_API_KEY
        self.base_url = OPENROUTER_BASE_URL
        self.model = LLM_MODEL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8501",  # Streamlit default
            "X-Title": "Salary Estimator RAG"
        }
        
    async def generate_completion(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = TEMPERATURE,
        max_tokens: int = MAX_TOKENS
    ) -> str:
        """Generate completion using Qwen3 model."""
        try:
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
                
            messages.append({"role": "user", "content": prompt})
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"]
                else:
                    logger.error(f"LLM API error: {response.status_code} - {response.text}")
                    raise Exception(f"LLM API error: {response.status_code}")
                    
        except Exception as e:
            logger.error(f"Error generating completion: {str(e)}")
            raise
            
    def generate_completion_sync(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = TEMPERATURE,
        max_tokens: int = MAX_TOKENS
    ) -> str:
        """Synchronous wrapper for generate_completion."""
        return asyncio.run(self.generate_completion(prompt, system_prompt, temperature, max_tokens))
        
    async def analyze_cv_for_salary(
        self, 
        cv_text: str, 
        matched_positions: List[Dict[str, Any]],
        industry: str
    ) -> Dict[str, Any]:
        """Analyze CV and provide salary insights using LLM."""
        
        system_prompt = """You are an expert HR consultant and salary analyst specializing in the Indonesian job market. 
        Your task is to analyze CVs and provide accurate salary estimations based on the Indonesia Salary Guide 2025.
        
        Consider the following factors:
        1. Years of experience and career progression
        2. Educational background and certifications
        3. Technical and soft skills relevance
        4. Industry standards and market demand
        5. Location factors (Jakarta typically offers higher salaries)
        
        Provide practical and actionable insights."""
        
        # Prepare matched positions summary
        positions_summary = "\n".join([
            f"- {pos['title']} in {pos['industry']}: IDR {pos['salary']} million/month"
            for pos in matched_positions[:5]  # Top 5 matches
        ])
        
        prompt = f"""Analyze the following CV information and matched salary data:

CV Summary:
{cv_text[:1500]}  # Limit to avoid token limits

Industry: {industry}

Matched Positions from Salary Guide 2025:
{positions_summary}

Please provide:
1. A detailed salary estimation explanation considering all factors
2. Key strengths that justify higher salary ranges
3. Areas for improvement to reach higher salary brackets
4. 3-5 specific recommendations for career advancement
5. Market insights for this profile in Indonesia

Format your response as JSON with the following structure:
{{
    "explanation": "detailed explanation",
    "strengths": ["strength1", "strength2", ...],
    "improvements": ["area1", "area2", ...],
    "recommendations": ["recommendation1", "recommendation2", ...],
    "market_insights": "insights about current market"
}}"""

        try:
            response = await self.generate_completion(prompt, system_prompt)
            
            # Try to parse JSON response
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                # If not valid JSON, return structured response
                return {
                    "explanation": response,
                    "strengths": [],
                    "improvements": [],
                    "recommendations": [],
                    "market_insights": ""
                }
                
        except Exception as e:
            logger.error(f"Error in CV analysis: {str(e)}")
            return {
                "explanation": "Unable to generate detailed analysis at this time.",
                "strengths": [],
                "improvements": [],
                "recommendations": [],
                "market_insights": ""
            }
            
    def analyze_cv_for_salary_sync(
        self, 
        cv_text: str, 
        matched_positions: List[Dict[str, Any]],
        industry: str
    ) -> Dict[str, Any]:
        """Synchronous wrapper for analyze_cv_for_salary."""
        return asyncio.run(self.analyze_cv_for_salary(cv_text, matched_positions, industry))
        
    async def generate_skill_recommendations(
        self,
        current_skills: List[str],
        target_role: str,
        industry: str
    ) -> List[str]:
        """Generate skill recommendations for career advancement."""
        
        prompt = f"""Based on the Indonesian job market in 2025, what skills should someone with the following profile develop to advance their career?

Current Skills: {', '.join(current_skills[:10])}
Target Role: {target_role}
Industry: {industry}

Provide 5 specific skill recommendations that would significantly increase their market value and salary potential in Indonesia.
Format as a JSON array of strings."""

        try:
            response = await self.generate_completion(prompt, max_tokens=500)
            
            # Try to parse JSON response
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                # Extract recommendations from text
                lines = response.strip().split('\n')
                recommendations = [line.strip('- ').strip() for line in lines if line.strip()]
                return recommendations[:5]
                
        except Exception as e:
            logger.error(f"Error generating skill recommendations: {str(e)}")
            return [
                "Enhance English communication skills",
                "Learn data analysis and visualization",
                "Develop project management capabilities",
                "Improve digital literacy and tech skills",
                "Build leadership and team management skills"
            ]
            
    def generate_skill_recommendations_sync(
        self,
        current_skills: List[str],
        target_role: str,
        industry: str
    ) -> List[str]:
        """Synchronous wrapper for generate_skill_recommendations."""
        return asyncio.run(self.generate_skill_recommendations(current_skills, target_role, industry))