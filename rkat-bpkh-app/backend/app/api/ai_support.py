from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.api.auth import get_current_user
from app.services.ai_service import AIService
from app.models.user import User
from typing import List, Dict, Optional

router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    context: Optional[Dict] = None

class ScenarioRequest(BaseModel):
    base_budget: float
    parameters: Dict
    scenario_count: int = 3

class OptimizationRequest(BaseModel):
    rkat_id: int
    optimization_goals: List[str]

@router.post("/chat")
async def ai_chat(
    request: QueryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """AI-powered chat for RKAT queries"""
    try:
        ai_service = AIService()
        response = await ai_service.process_query(
            query=request.query,
            user_context={
                "user_id": current_user.id,
                "role": current_user.role.value,
                "department": current_user.department
            },
            additional_context=request.context
        )
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")

@router.post("/scenario-analysis")
async def scenario_analysis(
    request: ScenarioRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate budget scenarios using AI"""
    try:
        ai_service = AIService()
        scenarios = await ai_service.generate_budget_scenarios(
            base_budget=request.base_budget,
            parameters=request.parameters,
            scenario_count=request.scenario_count
        )
        
        return {"scenarios": scenarios}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scenario analysis error: {str(e)}")

@router.post("/optimize-budget")
async def optimize_budget(
    request: OptimizationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """AI-powered budget optimization"""
    try:
        ai_service = AIService()
        optimization_result = await ai_service.optimize_rkat_budget(
            rkat_id=request.rkat_id,
            goals=request.optimization_goals,
            db=db
        )
        
        return {"optimization": optimization_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Budget optimization error: {str(e)}")

@router.get("/compliance-suggestions/{rkat_id}")
async def get_compliance_suggestions(
    rkat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-generated compliance improvement suggestions"""
    try:
        ai_service = AIService()
        suggestions = await ai_service.generate_compliance_suggestions(rkat_id, db)
        
        return {"suggestions": suggestions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Compliance analysis error: {str(e)}")

@router.post("/document-analysis")
async def analyze_document(
    file_content: str,
    document_type: str,  # 'kak', 'rab', 'timeline'
    current_user: User = Depends(get_current_user)
):
    """AI-powered document analysis"""
    try:
        ai_service = AIService()
        analysis = await ai_service.analyze_document(file_content, document_type)
        
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document analysis error: {str(e)}")