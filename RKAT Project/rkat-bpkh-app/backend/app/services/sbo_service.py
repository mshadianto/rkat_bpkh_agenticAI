import json
from typing import Dict, List, Optional
from app.models.rkat import RKAT, RKATActivity

class SBOService:
    """Service for Standar Biaya Operasional validation and calculations"""
    
    def __init__(self):
        # Load SBO standards
        self.sbo_standards = self._load_sbo_standards()
    
    def _load_sbo_standards(self) -> Dict:
        """Load SBO standards from configuration"""
        # This would typically be loaded from database or JSON file
        return {
            "personnel": {
                "honorarium_narasumber_eselon_1": 1_400_000,
                "honorarium_narasumber_eselon_2": 1_000_000,
                "honorarium_narasumber_eselon_3": 900_000,
                "uang_harian_gol_a": 300_000,
                "uang_harian_gol_b": 350_000,
                "uang_harian_gol_c": 300_000,
                "uang_harian_gol_d": 250_000,
                "uang_harian_gol_f": 200_000
            },
            "meetings": {
                "paket_fullday": 635_000,
                "paket_halfday": 450_000,
                "konsumsi_rapat_per_orang": 125_000,
                "sewa_perlengkapan_meeting": 30_000_000
            },
            "office": {
                "atk_per_paket": 5_000_000,
                "dokumentasi_foto_video": 20_000_000,
                "inventaris_kantor_per_unit": 2_000_000
            },
            "travel": {
                "dalam_negeri_per_hari": 1_500_000,
                "luar_negeri_per_hari": 3_000_000
            }
        }
    
    def validate_activity_budget(self, activity_code: str, budget_amount: float) -> Dict:
        """Validate activity budget against SBO standards"""
        sbo_reference = self._get_sbo_reference(activity_code)
        
        if not sbo_reference:
            return {
                "is_valid": False,
                "message": "No SBO reference found for this activity",
                "sbo_code": None,
                "variance": None
            }
        
        standard_amount = sbo_reference["amount"]
        variance_percentage = ((budget_amount - standard_amount) / standard_amount) * 100
        
        # Allow 10% variance
        is_valid = abs(variance_percentage) <= 10
        
        return {
            "is_valid": is_valid,
            "sbo_code": sbo_reference["code"],
            "standard_amount": standard_amount,
            "proposed_amount": budget_amount,
            "variance": variance_percentage,
            "message": f"Variance: {variance_percentage:.1f}% from SBO standard"
        }
    
    def calculate_budget_from_sbo(self, activity_type: str, parameters: Dict) -> Dict:
        """Calculate budget based on SBO standards and parameters"""
        calculations = {}
        
        if activity_type == "meeting":
            calculations = self._calculate_meeting_budget(parameters)
        elif activity_type == "personnel":
            calculations = self._calculate_personnel_budget(parameters)
        elif activity_type == "office":
            calculations = self._calculate_office_budget(parameters)
        elif activity_type == "travel":
            calculations = self._calculate_travel_budget(parameters)
        
        return calculations
    
    def calculate_compliance_score(self, rkat: RKAT) -> float:
        """Calculate SBO compliance score for entire RKAT"""
        activities = getattr(rkat, 'activities', [])
        
        if not activities:
            return 0.0
        
        total_score = 0
        for activity in activities:
            validation = self.validate_activity_budget(
                activity.activity_code, 
                activity.budget_amount
            )
            
            if validation["is_valid"]:
                total_score += 100
            elif validation["variance"] is not None:
                # Partial score based on variance
                variance = abs(validation["variance"])
                if variance <= 20:
                    total_score += max(50, 100 - variance * 2)
        
        return total_score / len(activities)
    
    def _get_sbo_reference(self, activity_code: str) -> Optional[Dict]:
        """Get SBO reference for activity code"""
        # Map activity codes to SBO standards
        code_mapping = {
            "522111": {"code": "konsumsi_rapat", "amount": 125_000},
            "522113": {"code": "atk", "amount": 5_000_000},
            "522114": {"code": "dokumentasi", "amount": 20_000_000},
            "522121": {"code": "jasa_konsultan", "amount": 500_000_000},
            "522124": {"code": "honorarium_narasumber", "amount": 1_000_000},
            "522512": {"code": "paket_meeting", "amount": 635_000},
            "522514": {"code": "sewa_perlengkapan", "amount": 30_000_000},
            "522515": {"code": "uang_saku", "amount": 250_000},
            "522517": {"code": "uang_harian", "amount": 300_000}
        }
        
        return code_mapping.get(activity_code)
    
    def _calculate_meeting_budget(self, params: Dict) -> Dict:
        """Calculate meeting budget based on SBO"""
        participants = params.get("participants", 0)
        duration_days = params.get("duration_days", 1)
        meeting_type = params.get("type", "fullday")  # fullday/halfday
        
        # Meeting package cost
        package_rate = self.sbo_standards["meetings"]["paket_fullday"] if meeting_type == "fullday" else self.sbo_standards["meetings"]["paket_halfday"]
        package_cost = package_rate * participants * duration_days
        
        # Additional costs
        equipment_cost = self.sbo_standards["meetings"]["sewa_perlengkapan_meeting"]
        documentation_cost = self.sbo_standards["office"]["dokumentasi_foto_video"]
        
        total_cost = package_cost + equipment_cost + documentation_cost
        
        return {
            "breakdown": {
                "meeting_package": package_cost,
                "equipment_rental": equipment_cost,
                "documentation": documentation_cost
            },
            "total": total_cost,
            "sbo_reference": "Meeting SBO Standards"
        }
    
    def _calculate_personnel_budget(self, params: Dict) -> Dict:
        """Calculate personnel budget based on SBO"""
        # Implementation for personnel cost calculation
        return {"total": 0, "breakdown": {}}
    
    def _calculate_office_budget(self, params: Dict) -> Dict:
        """Calculate office budget based on SBO"""  
        # Implementation for office cost calculation
        return {"total": 0, "breakdown": {}}
    
    def _calculate_travel_budget(self, params: Dict) -> Dict:
        """Calculate travel budget based on SBO"""
        # Implementation for travel cost calculation
        return {"total": 0, "breakdown": {}}