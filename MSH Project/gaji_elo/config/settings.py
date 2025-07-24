"""Configuration settings for the Salary Estimator RAG application."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

# OpenRouter Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen/qwen-2.5-72b-instruct")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

# ChromaDB Configuration
CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "salary_guide_2025")

# Salary Guide Data Path
SALARY_GUIDE_JSON = DATA_DIR / "salary_guide_2025.json"
SALARY_GUIDE_PDF = DATA_DIR / "raw" / "indonesia_salary_guide_2025.pdf"

# Application Settings
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Supported file types for CV upload
SUPPORTED_CV_FORMATS = [".pdf", ".docx", ".txt"]

# Salary estimation parameters
EXPERIENCE_MULTIPLIERS = {
    "entry": 0.7,      # 0-2 years
    "junior": 0.85,    # 2-5 years
    "mid": 1.0,        # 5-8 years
    "senior": 1.2,     # 8-12 years
    "expert": 1.4,     # 12+ years
}

EDUCATION_MULTIPLIERS = {
    "high_school": 0.7,
    "diploma": 0.85,
    "bachelor": 1.0,
    "master": 1.15,
    "phd": 1.3,
}

SKILL_MATCH_WEIGHTS = {
    "exact_match": 1.0,
    "similar_skill": 0.7,
    "related_skill": 0.4,
}