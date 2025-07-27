from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from app.config import settings
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RKAT BPKH Management System",
    description="Sistem Manajemen Rencana Kerja dan Anggaran Tahunan BPKH",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

@app.get("/")
async def root():
    return {
        "message": "RKAT BPKH Management System API",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
