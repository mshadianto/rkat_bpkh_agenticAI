from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="RKAT BPKH Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str
    password: str

USERS = {
    "admin": {"password": "admin123", "name": "Administrator BPKH", "role": "administrator"},
    "badan_pelaksana": {"password": "bp123", "name": "Badan Pelaksana", "role": "badan_pelaksana"}
}

@app.get("/")
async def root():
    return {"message": "RKAT BPKH Backend is running!", "status": "active"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/auth/login")
async def login(credentials: LoginRequest):
    username = credentials.username
    password = credentials.password
    
    if username not in USERS or USERS[username]["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = USERS[username]
    return {
        "access_token": f"token_{username}",
        "token_type": "bearer",
        "user_info": {
            "id": 1,
            "username": username,
            "full_name": user["name"],
            "role": user["role"],
            "department": "BPKH"
        }
    }

@app.get("/api/analytics/dashboard-metrics")
async def dashboard():
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
            {"id": 1, "title": "RKAT BPKH 2026", "status": "draft", "creator": "Admin", "created_at": "2025-01-15T10:00:00"}
        ],
        "performance_metrics": {"total_rkats": 18, "approved_rkats": 12, "avg_approval_time_days": 7.5}
    }

if __name__ == "__main__":
    print("🚀 RKAT BPKH Backend Starting...")
    print("📍 URL: http://localhost:8000")
    print("✅ Ready! You can now login with: admin/admin123")
    uvicorn.run(app, host="0.0.0.0", port=8000)