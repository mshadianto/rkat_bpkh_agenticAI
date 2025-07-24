"""Initialize the Salary Estimator project."""

import os
import sys
from pathlib import Path
import json

def init_project():
    """Initialize project structure and data."""
    
    print("🚀 Initializing Salary Estimator RAG Project...")
    
    # Create necessary directories
    directories = [
        "data",
        "data/raw",
        "chroma_db",
        "logs",
        "temp"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {dir_path}")
    
    # Check for .env file
    if not Path(".env").exists():
        print("\n⚠️  No .env file found!")
        print("Creating .env from template...")
        
        env_template = """# OpenRouter API Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# Model Configuration
LLM_MODEL=qwen/qwen-2.5-72b-instruct
MAX_TOKENS=2000
TEMPERATURE=0.7

# ChromaDB Configuration
CHROMA_PERSIST_DIRECTORY=./chroma_db
COLLECTION_NAME=salary_guide_2025

# Application Settings
DEBUG_MODE=False
LOG_LEVEL=INFO"""
        
        with open(".env", "w") as f:
            f.write(env_template)
        
        print("✅ Created .env file")
        print("\n🔑 IMPORTANT: Please edit .env and add your OpenRouter API key!")
        print("   Get a free key at: https://openrouter.ai/")
    
    # Initialize salary data
    print("\n📊 Initializing salary database...")
    
    try:
        from src.utils import save_salary_data_to_json
        if save_salary_data_to_json(Path("data")):
            print("✅ Salary data initialized successfully!")
        else:
            print("❌ Failed to initialize salary data")
    except Exception as e:
        print(f"❌ Error initializing salary data: {str(e)}")
        print("   Make sure all dependencies are installed: pip install -r requirements.txt")
    
    # Create sample .gitkeep files
    for dir_path in ["data/raw", "data/processed"]:
        gitkeep_path = Path(dir_path) / ".gitkeep"
        gitkeep_path.touch()
    
    print("\n✨ Project initialization complete!")
    print("\nNext steps:")
    print("1. Edit .env and add your OpenRouter API key")
    print("2. Run: streamlit run app.py")
    print("3. Upload a CV and get salary estimates!")
    
    # Check if ChromaDB needs indexing
    print("\n🔍 Checking if salary data needs indexing...")
    if not Path("chroma_db").exists() or not any(Path("chroma_db").iterdir()):
        print("📝 First run will index salary data (this may take a minute)")
    
    return True


if __name__ == "__main__":
    try:
        success = init_project()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Initialization cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Initialization failed: {str(e)}")
        sys.exit(1)