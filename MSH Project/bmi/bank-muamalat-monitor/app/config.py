"""
Configuration settings for Bank Muamalat Health Monitoring System
"""

import os
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Config:
    """Configuration class for the application"""
    
    # Application settings
    APP_NAME: str = "Bank Muamalat Health Monitor"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Database settings
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    
    # API settings
    API_BASE_URL: str = os.getenv("API_BASE_URL", "https://api.example.com")
    API_KEY: Optional[str] = os.getenv("API_KEY")
    
    # AI/ML settings
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4")
    
    # Data sources
    OJK_API_URL: str = "https://www.ojk.go.id/api"
    BI_API_URL: str = "https://www.bi.go.id/api"
    
    # File paths
    DATA_DIR: str = "data"
    LOGS_DIR: str = "logs"
    
    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALLOWED_HOSTS: list = field(default_factory=lambda: ["localhost", "127.0.0.1"])
    
    # Performance settings
    CACHE_TIMEOUT: int = 3600  # 1 hour
    MAX_WORKERS: int = 4
    
    # Monitoring settings
    HEALTH_CHECK_INTERVAL: int = 300  # 5 minutes
    ALERT_THRESHOLD: dict = field(default_factory=lambda: {
        "npf": 5.0,
        "car": 8.0,
        "bopo": 94.0,
        "roa": 0.5
    })
    
    def __post_init__(self):
        """Post-initialization setup"""
        # Create directories if they don't exist
        os.makedirs(self.DATA_DIR, exist_ok=True)
        os.makedirs(self.LOGS_DIR, exist_ok=True)
        
    def is_production(self) -> bool:
        """Check if running in production"""
        return not self.DEBUG
        
    def get_database_config(self) -> dict:
        """Get database configuration"""
        return {
            "url": self.DATABASE_URL,
            "echo": self.DEBUG
        }
        
    def get_api_config(self) -> dict:
        """Get API configuration"""
        return {
            "base_url": self.API_BASE_URL,
            "api_key": self.API_KEY,
            "timeout": 30
        }
        
    def get_alert_thresholds(self) -> dict:
        """Get alert thresholds configuration"""
        return self.ALERT_THRESHOLD.copy()
        
    def get_allowed_hosts(self) -> list:
        """Get allowed hosts list"""
        return self.ALLOWED_HOSTS.copy()

# Global config instance
config = Config()

# Export
__all__ = ['Config', 'config']