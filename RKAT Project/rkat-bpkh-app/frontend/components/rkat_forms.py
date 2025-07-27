import streamlit as st
import pandas as pd
from typing import Dict, List
from utils.api_client import APIClient
from config.settings import settings

class RKATForms:
    def __init__(self, api_client: APIClient):
        self.api = api_client
    
    def create_rkat_form(self):
        """Form for creating new RKAT"""
        st.subheader("📝 Buat RKAT Baru")
        
        with st.form("create_rkat_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input("Judul RKAT*", 
                                    placeholder="Contoh: RKAT BPKH Tahun 2026")
                year = st.number_input("Tahun", min_value=2024, max_value=2030, value=2026)
                theme = st.selectbox("Tema", ["Institutional Strengthening", "Operational Excellence", "Digital Transformation"])
            
            with col2:
                total_budget = st.number_input("Total Anggaran (Rp)", min_value=0.0, step=1000000.0)
                operational_budget = st.number_input("Anggaran Operasional (Rp)", min_value=0.0, step=1000000.0)
                personnel_budget = st.number_input("Anggaran Personel (Rp)", min_value=0.0, step=1000000.0)
            
            # Strategic Objectives
            st.subheader("Sasaran Strategis")
            strategic_objectives = []
            for i in range(3):
                obj = st.text_input(f"Sasaran Strategis {i+1}", key=f"obj_{i}")
                if obj:
                    strategic_objectives.append(obj)
            
            # Key Activities
            st.subheader("Kegiatan Utama")
            key_activities = []
            for i in range(5):
                activity = st.text_input(f"Kegiatan Utama {i+1}", key=f"activity_{i}")
                if activity:
                    key_activities.append(activity)
            
            # Performance Indicators
            st.subheader("Indikator Kinerja")
            performance_indicators = []
            for i in range(3):
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    indicator = st.text_input(f"Indikator {i+1}", key=f"indicator_{i}")
                with col_b:
                    target = st.text_input(f"Target {i+1}", key=f"target_{i}")
                with col_c:
                    unit = st.text_input(f"Satuan {i+1}", key=f"unit_{i}")
                
                if indicator and target:
                    performance_indicators.append({
                        "indicator": indicator,
                        "target": target,
                        "unit": unit
                    })
            
            if st.form_submit_button("Buat RKAT", use_container_width=True):
                if not title:
                    st.error("Judul RKAT harus diisi")
                    return
                
                if total_budget <= 0:
                    st.error("Total anggaran harus lebih dari 0")
                    return
                
                rkat_data = {
                    "title": title,
                    "year": year,
                    "total_budget": total_budget,
                    "operational_budget": operational_budget,
                    "personnel_budget": personnel_budget,
                    "theme": theme,
                    "strategic_objectives": strategic_objectives,
                    "key_activities": key_activities,
                    "performance_indicators": performance_indicators
                }
                
                response = self.api.create_rkat(rkat_data)
                
                if response["success"]:
                    st.success("RKAT berhasil dibuat!")
                    st.balloons()
                    
                    # Show next steps
                    st.info("Langkah selanjutnya: Tambahkan kegiatan dan upload dokumen pendukung")
                    
                    if st.button("Lihat RKAT"):
                        st.session_state.selected_rkat_id = response["data"]["rkat_id"]
                        st.rerun()
                else:
                    st.error(f"Gagal membuat RKAT: {response.get('error', 'Unknown error')}")
    
    def add_activity_form(self, rkat_id: int):
        """Form for adding activity to RKAT"""
        st.subheader("➕ Tambah Kegiatan")
        
        with st.form("add_activity_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                activity_code = st.text_input("Kode Kegiatan*", 
                                            placeholder="Contoh: 522111")
                activity_name = st.text_input("Nama Kegiatan*",
                                            placeholder="Contoh: Konsumsi Rapat")
                budget_amount = st.number_input("Anggaran (Rp)*", min_value=0.0, step=100000.0)
            
            with col2:
                output_target = st.text_input("Target Output",
                                            placeholder="Contoh: 12 kali rapat")
                outcome_target = st.text_input("Target Outcome", 
                                             placeholder="Contoh: Meningkatnya koordinasi")
            
            description = st.text_area("Deskripsi Kegiatan")
            
            # Budget Calculation Details
            st.subheader("Rincian Perhitungan Anggaran")
            calc_col1, calc_col2, calc_col3 = st.columns(3)
            
            with calc_col1:
                volume = st.number_input("Volume", min_value=0.0, step=1.0)
            with calc_col2:
                unit_price = st.number_input("Harga Satuan (Rp)", min_value=0.0, step=1000.0)
            with calc_col3:
                frequency = st.number_input("Frekuensi", min_value=1, step=1)
            
            # Auto calculate budget
            calculated_budget = volume * unit_price * frequency
            if calculated_budget > 0:
                st.info(f"Anggaran terhitung: Rp {calculated_budget:,.0f}")
            
            if st.form_submit_button("Tambah Kegiatan", use_container_width=True):
                if not all([activity_code, activity_name, budget_amount]):
                    st.error("Kode kegiatan, nama kegiatan, dan anggaran harus diisi")
                    return
                
                activity_data = {
                    "activity_code": activity_code,
                    "activity_name": activity_name,
                    "description": description,
                    "budget_amount": budget_amount,
                    "output_target": output_target,
                    "outcome_target": outcome_target,
                    "budget_calculation": {
                        "volume": volume,
                        "unit_price": unit_price,
                        "frequency": frequency,
                        "total": calculated_budget
                    }
                }
                
                response = self.api.add_activity(rkat_id, activity_data)
                
                if response["success"]:
                    st.success("Kegiatan berhasil ditambahkan!")
                    st.rerun()
                else:
                    st.error(f"Gagal menambah kegiatan: {response.get('error', 'Unknown error')}")
    
    def upload_documents_form(self, rkat_id: int, activity_id: int):
        """Form for uploading documents"""
        st.subheader("📎 Upload Dokumen Pendukung")
        
        doc_types = {
            "kak": "Kerangka Acuan Kerja (KAK)",
            "rab": "Rencana Anggaran Biaya (RAB)",  
            "timeline": "Timeline & Action Plan"
        }
        
        for doc_type, doc_name in doc_types.items():
            with st.expander(f"Upload {doc_name}"):
                uploaded_file = st.file_uploader(
                    f"Pilih file {doc_name}",
                    type=settings.ALLOWED_FILE_TYPES,
                    key=f"{doc_type}_{activity_id}"
                )
                
                if uploaded_file:
                    if st.button(f"Upload {doc_name}", key=f"upload_{doc_type}_{activity_id}"):
                        # In a real implementation, you would upload the file
                        st.success(f"{doc_name} berhasil diupload!")
    
    def compliance_checker(self, rkat_id: int):
        """Check and display compliance status"""
        st.subheader("✅ Cek Kepatuhan")
        
        if st.button("Periksa Kepatuhan KUP & SBO"):
            response = self.api.check_compliance(rkat_id)
            
            if response["success"]:
                compliance_data = response["data"]
                
                # KUP Compliance
                st.subheader("Kepatuhan KUP (Kebijakan Umum Penganggaran)")
                kup_compliance = compliance_data.get("kup_compliance", {})
                
                score = kup_compliance.get("compliance_percentage", 0)
                level = kup_compliance.get("compliance_level", "UNKNOWN")
                
                # Progress bar
                st.progress(score / 100)
                st.metric("Skor KUP", f"{score:.1f}%", level)
                
                # Detailed checks
                checks = kup_compliance.get("checks", [])
                for check in checks:
                    status_icon = "✅" if check["status"] == "PASS" else "⚠️" if check["status"] == "PARTIAL" else "❌"
                    st.write(f"{status_icon} {check['check']}: {check['message']}")
                
                # Recommendations
                recommendations = kup_compliance.get("recommendations", [])
                if recommendations:
                    st.subheader("Rekomendasi Perbaikan")
                    for rec in recommendations:
                        st.write(f"• {rec}")
                
                # SBO Compliance
                st.subheader("Kepatuhan SBO (Standar Biaya Operasional)")
                sbo_compliance = compliance_data.get("sbo_compliance", {})
                
                sbo_score = sbo_compliance.get("score", 0)
                sbo_level = sbo_compliance.get("level", "UNKNOWN")
                
                st.progress(sbo_score / 100)
                st.metric("Skor SBO", f"{sbo_score:.1f}%", sbo_level)
                
            else:
                st.error(f"Gagal memeriksa kepatuhan: {response.get('error', 'Unknown error')}")
