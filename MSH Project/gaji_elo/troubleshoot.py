"""Troubleshooting script for Salary Estimator."""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check Python version."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.11+")
        return False

def check_virtual_env():
    """Check if in virtual environment."""
    print("\n🔧 Checking virtual environment...")
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment is active")
        return True
    else:
        print("❌ Not in virtual environment")
        print("   Run: venv\\Scripts\\activate (Windows) or source venv/bin/activate (Mac/Linux)")
        return False

def check_dependencies():
    """Check if all dependencies are installed."""
    print("\n📦 Checking dependencies...")
    required = [
        'streamlit',
        'pandas',
        'numpy',
        'sklearn',
        'PyPDF2',
        'pdfplumber',
        'nltk',
        'plotly',
        'httpx',
        'pydantic',
        'dotenv'
    ]
    
    missing = []
    for package in required:
        try:
            if package == 'sklearn':
                __import__('sklearn')
            elif package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            print(f"✅ {package} - installed")
        except ImportError:
            print(f"❌ {package} - missing")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    return True

def check_env_file():
    """Check .env file and API key."""
    print("\n🔑 Checking .env file...")
    env_path = Path(".env")
    
    if not env_path.exists():
        print("❌ .env file not found")
        print("   Run: python init_project.py")
        return False
    
    with open(env_path, 'r') as f:
        content = f.read()
    
    if 'your_openrouter_api_key_here' in content:
        print("⚠️  .env file exists but API key not set")
        print("   Edit .env and add your OpenRouter API key")
        return False
    
    if 'OPENROUTER_API_KEY=' in content:
        print("✅ .env file exists with API key")
        return True
    
    return False

def check_directories():
    """Check if required directories exist."""
    print("\n📁 Checking directories...")
    dirs = ['data', 'src', 'models', 'config', 'chroma_db']
    all_exist = True
    
    for dir_name in dirs:
        if Path(dir_name).exists():
            print(f"✅ {dir_name}/ - exists")
        else:
            print(f"❌ {dir_name}/ - missing")
            all_exist = False
    
    if not all_exist:
        print("\n❌ Some directories missing")
        print("   Run: python init_project.py")
        return False
    return True

def check_salary_data():
    """Check if salary data is initialized."""
    print("\n📊 Checking salary data...")
    data_file = Path("data/salary_guide_2025.json")
    
    if data_file.exists():
        print("✅ Salary data file exists")
        return True
    else:
        print("❌ Salary data not found")
        print("   Run: python init_project.py")
        return False

def check_chromadb_issue():
    """Check for ChromaDB/ONNX issues."""
    print("\n🔍 Checking for ONNX runtime issues...")
    try:
        import onnxruntime
        print("⚠️  ONNX runtime is installed - might cause issues on Windows")
        print("   The app now uses SimpleRAGEngine instead of ChromaDB")
        return True
    except ImportError:
        print("✅ ONNX runtime not installed - good!")
        return True

def main():
    """Run all checks."""
    print("=" * 50)
    print("🔧 Salary Estimator Troubleshooting")
    print("=" * 50)
    
    checks = [
        check_python_version(),
        check_virtual_env(),
        check_dependencies(),
        check_env_file(),
        check_directories(),
        check_salary_data(),
        check_chromadb_issue()
    ]
    
    if all(checks):
        print("\n✅ All checks passed! You should be able to run:")
        print("   streamlit run app.py")
    else:
        print("\n❌ Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("1. Activate virtual environment: venv\\Scripts\\activate")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Initialize project: python init_project.py")
        print("4. Add API key to .env file")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()