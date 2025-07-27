import requests
import streamlit as st
from typing import Dict, Any, Optional, List
import json

class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def set_auth_token(self, token: str):
        """Set authentication token for requests"""
        self.session.headers.update({"Authorization": f"Bearer {token}"})
    
    def clear_auth_token(self):
        """Clear authentication token"""
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to API"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e), "status_code": getattr(e.response, 'status_code', None)}
    
    # Authentication endpoints
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate user"""
        return self._make_request("POST", "/api/auth/login", json={
            "username": username,
            "password": password
        })
    
    def get_current_user(self) -> Dict[str, Any]:
        """Get current user info"""
        return self._make_request("GET", "/api/auth/me")
    
    def register_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Register new user"""
        return self._make_request("POST", "/api/auth/register", json=user_data)
    
    # RKAT endpoints
    def create_rkat(self, rkat_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new RKAT"""
        return self._make_request("POST", "/api/rkat/create", json=rkat_data)
    
    def get_rkat_list(self) -> Dict[str, Any]:
        """Get RKAT list"""
        return self._make_request("GET", "/api/rkat/list")
    
    def get_rkat_detail(self, rkat_id: int) -> Dict[str, Any]:
        """Get RKAT details"""
        return self._make_request("GET", f"/api/rkat/{rkat_id}")
    
    def add_activity(self, rkat_id: int, activity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add activity to RKAT"""
        return self._make_request("POST", f"/api/rkat/{rkat_id}/activities", json=activity_data)
    
    def check_compliance(self, rkat_id: int) -> Dict[str, Any]:
        """Check RKAT compliance"""
        return self._make_request("GET", f"/api/rkat/{rkat_id}/compliance-check")
    
    # Workflow endpoints
    def submit_rkat(self, rkat_id: int) -> Dict[str, Any]:
        """Submit RKAT for review"""
        return self._make_request("POST", f"/api/workflow/{rkat_id}/submit")
    
    def review_rkat(self, rkat_id: int, action: str, comments: str = None) -> Dict[str, Any]:
        """Review RKAT"""
        return self._make_request("POST", f"/api/workflow/{rkat_id}/review", json={
            "action": action,
            "comments": comments
        })
    
    def get_workflow_history(self, rkat_id: int) -> Dict[str, Any]:
        """Get workflow history"""
        return self._make_request("GET", f"/api/workflow/{rkat_id}/history")
    
    def get_pending_reviews(self) -> Dict[str, Any]:
        """Get pending reviews"""
        return self._make_request("GET", "/api/workflow/pending-reviews")
    
    # Analytics endpoints
    def get_dashboard_metrics(self) -> Dict[str, Any]:
        """Get dashboard metrics"""
        return self._make_request("GET", "/api/analytics/dashboard-metrics")
    
    def get_budget_analysis(self, year: int = 2026) -> Dict[str, Any]:
        """Get budget analysis"""
        return self._make_request("GET", f"/api/analytics/budget-analysis?year={year}")
    
    def get_compliance_report(self) -> Dict[str, Any]:
        """Get compliance report"""
        return self._make_request("GET", "/api/analytics/compliance-report")
    
    # AI Support endpoints
    def ai_chat(self, query: str, context: Dict = None) -> Dict[str, Any]:
        """AI chat query"""
        return self._make_request("POST", "/api/ai/chat", json={
            "query": query,
            "context": context
        })
    
    def scenario_analysis(self, base_budget: float, parameters: Dict, scenario_count: int = 3) -> Dict[str, Any]:
        """Budget scenario analysis"""
        return self._make_request("POST", "/api/ai/scenario-analysis", json={
            "base_budget": base_budget,
            "parameters": parameters,
            "scenario_count": scenario_count
        })