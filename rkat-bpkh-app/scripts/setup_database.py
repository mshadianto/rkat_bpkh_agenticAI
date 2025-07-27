#!/usr/bin/env python3
"""
Database setup script for RKAT BPKH application
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.user import User, UserRole
from app.models.rkat import RKAT, RKATActivity
from app.models.workflow import WorkflowLog
from app.services.auth_service import AuthService
from app.config import settings
import click

def create_database():
    """Create database tables"""
    engine = create_engine(settings.database_url)
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")

def create_default_users():
    """Create default users for testing"""
    engine = create_engine(settings.database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    default_users = [
        {
            "username": "admin",
            "email": "admin@bpkh.go.id",
            "full_name": "Administrator BPKH",
            "password": "admin123",
            "role": UserRole.ADMINISTRATOR,
            "department": "IT",
            "position": "System Administrator"
        },
        {
            "username": "badan_pelaksana",
            "email": "bp@bpkh.go.id", 
            "full_name": "Badan Pelaksana",
            "password": "bp123",
            "role": UserRole.BADAN_PELAKSANA,
            "department": "Badan Pelaksana",
            "position": "Kepala Badan"
        },
        {
            "username": "audit_internal",
            "email": "audit@bpkh.go.id",
            "full_name": "Audit Internal",
            "password": "audit123", 
            "role": UserRole.AUDIT_INTERNAL,
            "department": "Audit Internal",
            "position": "Kepala Audit"
        },
        {
            "username": "komite_dewan",
            "email": "komite@bpkh.go.id",
            "full_name": "Komite Dewan Pengawas",
            "password": "komite123",
            "role": UserRole.KOMITE_DEWAN_PENGAWAS,
            "department": "Dewan Pengawas",
            "position": "Ketua Komite"
        },
        {
            "username": "dewan_pengawas",
            "email": "dewan@bpkh.go.id",
            "full_name": "Dewan Pengawas", 
            "password": "dewan123",
            "role": UserRole.DEWAN_PENGAWAS,
            "department": "Dewan Pengawas", 
            "position": "Ketua Dewan"
        }
    ]
    
    for user_data in default_users:
        # Check if user already exists
        existing_user = db.query(User).filter(User.username == user_data["username"]).first()
        
        if not existing_user:
            hashed_password = AuthService.get_password_hash(user_data["password"])
            
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                full_name=user_data["full_name"],
                hashed_password=hashed_password,
                role=user_data["role"],
                department=user_data["department"],
                position=user_data["position"]
            )
            
            db.add(user)
            print(f"✅ Created user: {user_data['username']}")
        else:
            print(f"⚠️  User already exists: {user_data['username']}")
    
    db.commit()
    db.close()
    print("✅ Default users created successfully")

def seed_sample_data():
    """Create sample RKAT data for testing"""
    engine = create_engine(settings.database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    # Get badan pelaksana user
    bp_user = db.query(User).filter(User.role == UserRole.BADAN_PELAKSANA).first()
    
    if bp_user:
        # Create sample RKAT
        sample_rkat = RKAT(
            title="RKAT BPKH Tahun 2026 - Institutional Strengthening",
            year=2026,
            total_budget=1500000000.0,  # 1.5 Milyar
            operational_budget=1050000000.0,  # 1.05 Milyar
            personnel_budget=450000000.0,  # 450 Juta
            theme="Institutional Strengthening",
            strategic_objectives=[
                "Pengembangan investasi pada ekosistem haji dan umroh",
                "Amandemen peraturan untuk penguatan kelembagaan dan tata kelola BPKH"
            ],
            key_activities=[
                "Penyusunan dan harmonisasi peraturan BPKH",
                "Pengembangan sistem teknologi informasi",
                "Peningkatan kapasitas SDM",
                "Optimalisasi investasi dana haji"
            ],
            performance_indicators=[
                {"indicator": "Jumlah PBPKH yang diselesaikan", "target": "12", "unit": "dokumen"},
                {"indicator": "Tingkat kepuasan stakeholder", "target": "85", "unit": "persen"},
                {"indicator": "Efisiensi anggaran operasional", "target": "95", "unit": "persen"}
            ],
            created_by=bp_user.id
        )
        
        db.add(sample_rkat)
        db.commit()
        db.refresh(sample_rkat)
        
        # Add sample activities
        sample_activities = [
            {
                "activity_code": "010101",
                "activity_name": "Pembentukan Peraturan",
                "description": "Penyusunan dan harmonisasi PBPKH/PKBP untuk penguatan tata kelola BPKH",
                "budget_amount": 1351555220.0,
                "output_target": "12 PBPKH/PKBP",
                "outcome_target": "Meningkatnya tata kelola peraturan BPKH"
            },
            {
                "activity_code": "522111",
                "activity_name": "Konsumsi Rapat",
                "description": "Penyediaan konsumsi untuk rapat koordinasi dan pembahasan",
                "budget_amount": 37500000.0,
                "output_target": "300 kali konsumsi rapat",
                "outcome_target": "Terlaksananya rapat yang efektif"
            },
            {
                "activity_code": "522114", 
                "activity_name": "Dokumentasi Kegiatan",
                "description": "Dokumentasi foto dan video kegiatan BPKH",
                "budget_amount": 20000000.0,
                "output_target": "100 dokumentasi kegiatan",
                "outcome_target": "Terciptanya arsip dokumentasi yang baik"
            }
        ]
        
        for activity_data in sample_activities:
            activity = RKATActivity(
                rkat_id=sample_rkat.id,
                activity_code=activity_data["activity_code"],
                activity_name=activity_data["activity_name"],
                description=activity_data["description"],
                budget_amount=activity_data["budget_amount"],
                output_target=activity_data["output_target"],
                outcome_target=activity_data["outcome_target"]
            )
            db.add(activity)
        
        db.commit()
        print("✅ Sample RKAT data created successfully")
    
    db.close()

@click.command()
@click.option('--create-tables', is_flag=True, help='Create database tables')
@click.option('--create-users', is_flag=True, help='Create default users')
@click.option('--seed-data', is_flag=True, help='Seed sample data')
@click.option('--all', is_flag=True, help='Run all setup tasks')
def main(create_tables, create_users, seed_data, all):
    """Database setup script for RKAT BPKH application"""
    
    if all:
        create_tables = create_users = seed_data = True
    
    if create_tables:
        print("🚀 Creating database tables...")
        create_database()
    
    if create_users:
        print("👥 Creating default users...")
        create_default_users()
    
    if seed_data:
        print("🌱 Seeding sample data...")
        seed_sample_data()
    
    if not any([create_tables, create_users, seed_data]):
        print("ℹ️  Use --help to see available options")
    
    print("🎉 Database setup completed!")

if __name__ == "__main__":
    main()