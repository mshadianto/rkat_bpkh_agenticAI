from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    database_url: str = "postgresql://user:password@localhost:5432/rkat_bpkh"
    redis_url: str = "redis://localhost:6379"
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    model_name: str = "anthropic/claude-3-haiku"
    upload_dir: str = "./uploads"
    max_file_size: int = 50 * 1024 * 1024
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    email_username: str = ""
    email_password: str = ""
    max_operational_budget_percentage: float = 0.05
    rkat_year: int = 2026
    
    class Config:
        env_file = ".env"

settings = Settings()
