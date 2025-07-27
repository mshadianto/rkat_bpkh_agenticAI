#!/usr/bin/env python3
"""
Development runner script for RKAT BPKH application
"""

import subprocess
import sys
import os
import time
import signal
from concurrent.futures import ThreadPoolExecutor
import click

def run_backend():
    """Run FastAPI backend"""
    os.chdir("backend")
    try:
        subprocess.run([sys.executable, "run.py"], check=True)
    except KeyboardInterrupt:
        print("Backend stopped")
    except subprocess.CalledProcessError as e:
        print(f"Backend error: {e}")

def run_frontend():
    """Run Streamlit frontend"""
    os.chdir("frontend")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"], check=True)
    except KeyboardInterrupt:
        print("Frontend stopped")
    except subprocess.CalledProcessError as e:
        print(f"Frontend error: {e}")

def check_dependencies():
    """Check if required dependencies are installed"""
    backend_requirements = ["fastapi", "uvicorn", "sqlalchemy", "redis"]
    frontend_requirements = ["streamlit", "pandas", "plotly"]
    
    missing = []
    
    for req in backend_requirements + frontend_requirements:
        try:
            __import__(req)
        except ImportError:
            missing.append(req)
    
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("Run: pip install -r backend/requirements.txt && pip install -r frontend/requirements.txt")
        return False
    
    return True

def setup_environment():
    """Setup environment variables and configuration"""
    if not os.path.exists("backend/.env"):
        print("⚠️  Backend .env file not found. Creating from template...")
        if os.path.exists("backend/.env.example"):
            subprocess.run(["cp", "backend/.env.example", "backend/.env"])
        else:
            print("❌ .env.example not found. Please create backend/.env manually")
            return False
    
    return True

@click.command()
@click.option('--backend-only', is_flag=True, help='Run only backend')
@click.option('--frontend-only', is_flag=True, help='Run only frontend')
@click.option('--setup-db', is_flag=True, help='Setup database before running')
@click.option('--port-backend', default=8000, help='Backend port (default: 8000)')
@click.option('--port-frontend', default=8501, help='Frontend port (default: 8501)')
def main(backend_only, frontend_only, setup_db, port_backend, port_frontend):
    """Development runner for RKAT BPKH application"""
    
    print("🚀 Starting RKAT BPKH Development Environment")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        sys.exit(1)
    
    # Setup database if requested
    if setup_db:
        print("🗄️  Setting up database...")
        try:
            subprocess.run([sys.executable, "scripts/setup_database.py", "--all"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Database setup failed: {e}")
            sys.exit(1)
    
    # Determine what to run
    if backend_only:
        print(f"🔧 Starting backend only on port {port_backend}...")
        run_backend()
    elif frontend_only:
        print(f"🎨 Starting frontend only on port {port_frontend}...")
        run_frontend()
    else:
        print(f"🔧 Starting backend on port {port_backend}...")
        print(f"🎨 Starting frontend on port {port_frontend}...")
        print("Press Ctrl+C to stop both services")
        
        # Run both services concurrently
        with ThreadPoolExecutor(max_workers=2) as executor:
            try:
                backend_future = executor.submit(run_backend)
                time.sleep(2)  # Give backend time to start
                frontend_future = executor.submit(run_frontend)
                
                # Wait for either to complete (usually due to error or interruption)
                backend_future.result()
                frontend_future.result()
                
            except KeyboardInterrupt:
                print("\n🛑 Stopping services...")
                # The individual functions handle their own cleanup
    
    print("👋 RKAT BPKH Development Environment stopped")

if __name__ == "__main__":
    main()