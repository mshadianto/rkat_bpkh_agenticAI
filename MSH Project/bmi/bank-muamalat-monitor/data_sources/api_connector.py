import requests
import json
from typing import Dict, Optional, Any, List
import logging
import time

class APIConnector:
    """Connector untuk API dengan rate limiting dan error handling"""
    
    def __init__(self, base_url: str = "", headers: Optional[Dict] = None):
        self.base_url = base_url
        self.headers = headers or {}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.logger = logging.getLogger(__name__)
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """GET request dengan error handling"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"GET request error for {endpoint}: {e}")
            return None
    
    def post(self, endpoint: str, data: Optional[Dict] = None) -> Optional[Dict]:
        """POST request dengan error handling"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.post(url, json=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"POST request error for {endpoint}: {e}")
            return None
    
    def paginated_get(self, endpoint: str, params: Optional[Dict] = None, 
                     limit: int = 100) -> List[Dict]:
        """GET request dengan pagination"""
        all_data = []
        page = 1
        
        while True:
            current_params = params.copy() if params else {}
            current_params.update({'page': page, 'limit': limit})
            
            response = self.get(endpoint, current_params)
            if not response or not response.get('data'):
                break
                
            all_data.extend(response['data'])
            
            if len(response['data']) < limit:
                break
                
            page += 1
            time.sleep(0.1)  # Rate limiting
        
        return all_data
    
    def set_auth(self, token: str, auth_type: str = "Bearer"):
        """Set authorization header"""
        self.session.headers.update({
            'Authorization': f"{auth_type} {token}"
        })
    
    def batch_request(self, endpoints: List[str], delay: float = 0.1) -> Dict[str, Any]:
        """Multiple requests dengan delay"""
        results = {}
        for endpoint in endpoints:
            results[endpoint] = self.get(endpoint)
            time.sleep(delay)
        return results