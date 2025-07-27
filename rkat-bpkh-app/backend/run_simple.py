#!/usr/bin/env python3
"""
Simple runner for RKAT BPKH backend
"""

try:
    from app.main_simple import app
    import uvicorn
    
    if __name__ == "__main__":
        print("Ì∫Ä Starting RKAT BPKH Backend (Simple Version)...")
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
        
except ImportError as e:
    print(f"‚ùå Import error: {e}")
    print("Installing required packages...")
    
    import subprocess
    import sys
    
    # Install basic requirements
    subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "pydantic"])
    
    print("‚úÖ Packages installed. Please run again.")
