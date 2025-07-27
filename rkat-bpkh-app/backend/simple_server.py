from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="RKAT BPKH Simple Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "RKAT BPKH Backend", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/api/auth/login")
def login(data: dict):
    username = data.get("username", "")
    password = data.get("password", "")
    
    # Mock login
    if username == "admin" and password == "admin123":
        return {
            "access_token": "test_token",
            "token_type": "bearer",
            "user_info": {
                "id": 1,
                "username": "admin",
                "full_name": "Administrator BPKH",
                "role": "administrator",
                "department": "IT"
            }
        }
    return {"error": "Invalid credentials"}

@app.get("/api/analytics/dashboard-metrics")
def dashboard():
    return {
        "status_distribution": {"draft": 5, "approved": 8},
        "budget_summary": {
            "total_budget": 15000000000.0,
            "operational_budget": 10500000000.0,
            "personnel_budget": 4500000000.0,
            "avg_kup_compliance": 87.5,
            "avg_sbo_compliance": 91.2
        },
        "recent_activities": [
            {"id": 1, "title": "RKAT BPKH 2026", "status": "draft", "creator": "Admin"}
        ],
        "performance_metrics": {"total_rkats": 18, "approved_rkats": 12, "avg_approval_time_days": 7.5}
    }

if __name__ == "__main__":
    print("🚀 RKAT Backend Starting...")
    print("📍 URL: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)