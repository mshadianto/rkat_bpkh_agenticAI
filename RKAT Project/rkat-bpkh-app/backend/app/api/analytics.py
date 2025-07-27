from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.rkat import RKAT, RKATActivity, RKATStatus
from typing import List, Optional
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/dashboard-metrics")
async def get_dashboard_metrics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get key metrics for dashboard"""
    
    # Total RKATs by status
    status_counts = db.query(
        RKAT.status, 
        func.count(RKAT.id)
    ).group_by(RKAT.status).all()
    
    # Budget summary
    budget_summary = db.query(
        func.sum(RKAT.total_budget).label('total_budget'),
        func.sum(RKAT.operational_budget).label('operational_budget'),
        func.sum(RKAT.personnel_budget).label('personnel_budget'),
        func.avg(RKAT.kup_compliance_score).label('avg_kup_score'),
        func.avg(RKAT.sbo_compliance_score).label('avg_sbo_score')
    ).filter(RKAT.year == 2026).first()
    
    # Recent activities
    recent_rkats = db.query(RKAT).order_by(RKAT.created_at.desc()).limit(5).all()
    
    # Approval timeline
    approval_times = db.query(
        func.extract('epoch', RKAT.approved_at - RKAT.submitted_at).label('approval_time')
    ).filter(
        RKAT.approved_at.isnot(None),
        RKAT.submitted_at.isnot(None)
    ).all()
    
    avg_approval_time = sum(t.approval_time for t in approval_times) / len(approval_times) if approval_times else 0
    
    return {
        "status_distribution": {status.value: count for status, count in status_counts},
        "budget_summary": {
            "total_budget": float(budget_summary.total_budget or 0),
            "operational_budget": float(budget_summary.operational_budget or 0),
            "personnel_budget": float(budget_summary.personnel_budget or 0),
            "avg_kup_compliance": float(budget_summary.avg_kup_score or 0),
            "avg_sbo_compliance": float(budget_summary.avg_sbo_score or 0)
        },
        "recent_activities": [
            {
                "id": rkat.id,
                "title": rkat.title,
                "status": rkat.status.value,
                "created_at": rkat.created_at,
                "creator": rkat.creator.full_name
            }
            for rkat in recent_rkats
        ],
        "performance_metrics": {
            "avg_approval_time_days": avg_approval_time / (24 * 3600) if avg_approval_time else 0,
            "total_rkats": len(status_counts),
            "approved_rkats": sum(count for status, count in status_counts if 'approved' in status.value)
        }
    }

@router.get("/budget-analysis")
async def get_budget_analysis(
    year: Optional[int] = Query(2026),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get budget analysis and trends"""
    
    # Budget by department/division
    dept_budgets = db.query(
        User.department,
        func.sum(RKAT.total_budget).label('total_budget'),
        func.count(RKAT.id).label('rkat_count')
    ).join(RKAT, User.id == RKAT.created_by)\
     .filter(RKAT.year == year)\
     .group_by(User.department).all()
    
    # Budget by activity type
    activity_budgets = db.query(
        RKATActivity.activity_code,
        func.sum(RKATActivity.budget_amount).label('total_amount'),
        func.count(RKATActivity.id).label('activity_count')
    ).join(RKAT, RKATActivity.rkat_id == RKAT.id)\
     .filter(RKAT.year == year)\
     .group_by(RKATActivity.activity_code).all()
    
    # Monthly submission trends
    monthly_trends = db.query(
        extract('month', RKAT.created_at).label('month'),
        func.count(RKAT.id).label('submissions'),
        func.sum(RKAT.total_budget).label('budget')
    ).filter(RKAT.year == year)\
     .group_by(extract('month', RKAT.created_at)).all()
    
    return {
        "department_budgets": [
            {
                "department": dept or "Unknown",
                "total_budget": float(budget),
                "rkat_count": count
            }
            for dept, budget, count in dept_budgets
        ],
        "activity_budgets": [
            {
                "activity_code": code,
                "total_amount": float(amount),
                "activity_count": count
            }
            for code, amount, count in activity_budgets
        ],
        "monthly_trends": [
            {
                "month": int(month),
                "submissions": submissions,
                "budget": float(budget or 0)
            }
            for month, submissions, budget in monthly_trends
        ]
    }

@router.get("/compliance-report")
async def get_compliance_report(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get compliance analysis report"""
    
    # Compliance score distribution
    compliance_data = db.query(
        RKAT.id,
        RKAT.title,
        RKAT.kup_compliance_score,
        RKAT.sbo_compliance_score,
        RKAT.status,
        User.department
    ).join(User, RKAT.created_by == User.id)\
     .filter(RKAT.year == 2026).all()
    
    # Calculate compliance levels
    kup_excellent = sum(1 for r in compliance_data if (r.kup_compliance_score or 0) >= 90)
    kup_good = sum(1 for r in compliance_data if 80 <= (r.kup_compliance_score or 0) < 90)
    kup_needs_improvement = sum(1 for r in compliance_data if (r.kup_compliance_score or 0) < 80)
    
    sbo_excellent = sum(1 for r in compliance_data if (r.sbo_compliance_score or 0) >= 90)
    sbo_good = sum(1 for r in compliance_data if 80 <= (r.sbo_compliance_score or 0) < 90)
    sbo_needs_improvement = sum(1 for r in compliance_data if (r.sbo_compliance_score or 0) < 80)
    
    return {
        "kup_compliance": {
            "excellent": kup_excellent,
            "good": kup_good,
            "needs_improvement": kup_needs_improvement,
            "average_score": sum(r.kup_compliance_score or 0 for r in compliance_data) / len(compliance_data) if compliance_data else 0
        },
        "sbo_compliance": {
            "excellent": sbo_excellent,
            "good": sbo_good,
            "needs_improvement": sbo_needs_improvement,
            "average_score": sum(r.sbo_compliance_score or 0 for r in compliance_data) / len(compliance_data) if compliance_data else 0
        },
        "detailed_scores": [
            {
                "rkat_id": r.id,
                "title": r.title,
                "kup_score": r.kup_compliance_score,
                "sbo_score": r.sbo_compliance_score,
                "status": r.status.value,
                "department": r.department
            }
            for r in compliance_data
        ]
    }