import json
from typing import Dict, List
from app.models.rkat import RKAT

class KUPService:
    """Service for Kebijakan Umum Penganggaran validation and compliance"""
    
    def __init__(self):
        # Load KUP rules and guidelines
        self.kup_rules = self._load_kup_rules()
    
    def _load_kup_rules(self) -> Dict:
        """Load KUP rules from configuration"""
        return {
            "theme_2026": "Institutional Strengthening",
            "strategic_objectives": [
                "Pengembangan investasi pada ekosistem haji dan umroh",
                "Amandemen peraturan untuk penguatan kelembagaan dan tata kelola BPKH"
            ],
            "efficiency_principles": [
                "efisien", "efektif", "rasional", "akuntabel"
            ],
            "required_documents": [
                "KAK", "RAB", "Action Plan", "Timeline", "WBS"
            ],
            "budget_efficiency_rules": {
                "no_duplicate_activities": True,
                "minimize_travel_budget": True,
                "optimize_meeting_rooms": True,
                "align_with_tupoksi": True
            }
        }
    
    def validate_rkat_compliance(self, rkat: RKAT) -> Dict:
        """Validate RKAT compliance with KUP"""
        compliance_checks = []
        score = 0
        max_score = 100
        
        # Theme compliance (20 points)
        if rkat.theme == self.kup_rules["theme_2026"]:
            score += 20
            compliance_checks.append({
                "check": "Theme Compliance", 
                "status": "PASS", 
                "points": 20,
                "message": f"Theme '{rkat.theme}' aligns with KUP 2026"
            })
        else:
            compliance_checks.append({
                "check": "Theme Compliance", 
                "status": "FAIL", 
                "points": 0,
                "message": f"Theme should be '{self.kup_rules['theme_2026']}'"
            })
        
        # Strategic objectives alignment (30 points)
        strategic_score = self._check_strategic_alignment(rkat.strategic_objectives)
        score += strategic_score
        compliance_checks.append({
            "check": "Strategic Objectives Alignment",
            "status": "PASS" if strategic_score > 15 else "PARTIAL" if strategic_score > 0 else "FAIL",
            "points": strategic_score,
            "message": f"Strategic objectives alignment score: {strategic_score}/30"
        })
        
        # Budget efficiency (25 points)
        efficiency_score = self._check_budget_efficiency(rkat)
        score += efficiency_score
        compliance_checks.append({
            "check": "Budget Efficiency",
            "status": "PASS" if efficiency_score > 18 else "PARTIAL" if efficiency_score > 10 else "FAIL",
            "points": efficiency_score,
            "message": f"Budget efficiency score: {efficiency_score}/25"
        })
        
        # Documentation completeness (25 points)
        doc_score = self._check_documentation(rkat)
        score += doc_score
        compliance_checks.append({
            "check": "Documentation Completeness",
            "status": "PASS" if doc_score > 18 else "PARTIAL" if doc_score > 10 else "FAIL", 
            "points": doc_score,
            "message": f"Documentation completeness score: {doc_score}/25"
        })
        
        return {
            "total_score": score,
            "max_score": max_score,
            "compliance_percentage": (score / max_score) * 100,
            "compliance_level": self._get_compliance_level(score, max_score),
            "checks": compliance_checks,
            "recommendations": self._generate_recommendations(compliance_checks)
        }
    
    def calculate_compliance_score(self, rkat: RKAT) -> float:
        """Calculate simple compliance score (0-100)"""
        validation_result = self.validate_rkat_compliance(rkat)
        return validation_result["compliance_percentage"]
    
    def _check_strategic_alignment(self, objectives: List) -> int:
        """Check alignment with strategic objectives"""
        if not objectives:
            return 0
        
        score = 0
        for objective in objectives:
            for kup_objective in self.kup_rules["strategic_objectives"]:
                if any(keyword in objective.lower() for keyword in kup_objective.lower().split()):
                    score += 15
                    break
        
        return min(score, 30)  # Max 30 points
    
    def _check_budget_efficiency(self, rkat: RKAT) -> int:
        """Check budget efficiency compliance"""
        score = 25  # Start with full score, deduct for violations
        
        # Check operational budget percentage
        if hasattr(rkat, 'operational_budget') and hasattr(rkat, 'total_budget'):
            if rkat.total_budget > 0:
                op_percentage = (rkat.operational_budget / rkat.total_budget) * 100
                if op_percentage > 70:  # High operational percentage
                    score -= 10
        
        # Additional efficiency checks would go here
        # For now, return base score
        return max(score, 0)
    
    def _check_documentation(self, rkat: RKAT) -> int:
        """Check documentation completeness"""
        score = 0
        activities = getattr(rkat, 'activities', [])
        
        if not activities:
            return 0
        
        doc_fields = ['kak_document', 'rab_document', 'timeline_document']
        total_docs = len(activities) * len(doc_fields)
        completed_docs = 0
        
        for activity in activities:
            for field in doc_fields:
                if getattr(activity, field, None):
                    completed_docs += 1
        
        if total_docs > 0:
            score = int((completed_docs / total_docs) * 25)
        
        return score
    
    def _get_compliance_level(self, score: int, max_score: int) -> str:
        """Get compliance level based on score"""
        percentage = (score / max_score) * 100
        
        if percentage >= 90:
            return "EXCELLENT"
        elif percentage >= 80:
            return "GOOD"
        elif percentage >= 70:
            return "SATISFACTORY"
        elif percentage >= 60:
            return "NEEDS_IMPROVEMENT"
        else:
            return "POOR"
    
    def _generate_recommendations(self, checks: List[Dict]) -> List[str]:
        """Generate recommendations based on compliance checks"""
        recommendations = []
        
        for check in checks:
            if check["status"] == "FAIL":
                if check["check"] == "Theme Compliance":
                    recommendations.append("Update RKAT theme to 'Institutional Strengthening' sesuai KUP 2026")
                elif check["check"] == "Strategic Objectives Alignment":
                    recommendations.append("Align strategic objectives with fokus pengembangan investasi dan penguatan kelembagaan")
                elif check["check"] == "Budget Efficiency":
                    recommendations.append("Review budget allocation untuk meningkatkan efisiensi sesuai prinsip KUP")
                elif check["check"] == "Documentation Completeness":
                    recommendations.append("Lengkapi dokumen pendukung: KAK, RAB, Action Plan, Timeline, WBS")
        
        return recommendations