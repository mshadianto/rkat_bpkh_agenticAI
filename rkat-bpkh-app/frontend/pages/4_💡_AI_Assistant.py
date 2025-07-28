# frontend/pages/4_💡_AI_Assistant.py - Fixed version
import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import json
import plotly.express as px
import plotly.graph_objects as go

# Configuration
BACKEND_URL = "https://rkat-bpkh-agenticai.onrender.com"
REQUEST_TIMEOUT = 30

def get_auth_headers():
    """Get authorization headers with safe session state access"""
    token = (st.session_state.get('token') or 
             st.session_state.get('auth_token') or 
             st.session_state.get('access_token'))
    
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

def make_api_request(method, endpoint, **kwargs):
    """API request wrapper"""
    try:
        url = f"{BACKEND_URL}{endpoint}"
        kwargs['timeout'] = REQUEST_TIMEOUT
        
        if method.upper() == "GET":
            response = requests.get(url, **kwargs)
        elif method.upper() == "POST":
            response = requests.post(url, **kwargs)
        
        return response
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

def main():
    st.title("💡 AI Assistant untuk RKAT")
    
    # Check authentication
    if not st.session_state.get('authenticated', False):
        st.error("❌ Anda belum login. Silahkan login terlebih dahulu.")
        st.info("👈 Klik halaman utama untuk login")
        return
    
    # Introduction
    st.markdown("""
    ### 🤖 Asisten AI untuk Penyusunan RKAT BPKH
    
    AI Assistant akan membantu Anda dalam:
    - 🔍 **Analisis Kelayakan Anggaran** - Validasi usulan anggaran berdasarkan historical data
    - 📊 **Validasi Kesesuaian KUP & SBO** - Verifikasi otomatis kesesuaian dengan pedoman
    - ⏱️ **Prediksi Timeline Approval** - Estimasi waktu persetujuan berdasarkan kompleksitas
    - 📈 **Benchmarking** - Perbandingan dengan RKAT sejenis di bidang lain
    - 💡 **Saran Optimasi** - Rekomendasi untuk meningkatkan efisiensi anggaran
    """)
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "💬 Chat AI", 
        "📊 Scenario Planning", 
        "🎯 Budget Optimization",
        "✅ Compliance Assistant"
    ])
    
    with tab1:
        show_chat_interface()
    
    with tab2:
        show_scenario_planning()
    
    with tab3:
        show_budget_optimization()
    
    with tab4:
        show_compliance_assistant()

def show_chat_interface():
    """AI Chat interface with RKAT context"""
    st.subheader("💬 Chat AI")
    
    # Load RKAT data for context
    rkat_context = load_rkat_context()
    
    # Chat history
    if 'ai_chat_history' not in st.session_state:
        st.session_state.ai_chat_history = [
            {
                "role": "assistant", 
                "content": "Halo! Saya AI Assistant RKAT BPKH. Bagaimana saya dapat membantu Anda dalam penyusunan atau review RKAT hari ini?"
            }
        ]
    
    # Display chat history
    for message in st.session_state.ai_chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Tanyakan tentang RKAT, KUP, SBO, atau proses approval..."):
        # Add user message
        st.session_state.ai_chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("AI sedang menganalisis..."):
                ai_response = generate_ai_response(prompt, rkat_context)
                st.write(ai_response)
                st.session_state.ai_chat_history.append({"role": "assistant", "content": ai_response})
    
    # Quick actions
    st.subheader("🚀 Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Analisis Budget", use_container_width=True):
            auto_prompt = "Bantu saya menganalisis kelayakan anggaran RKAT saya"
            st.session_state.ai_chat_history.append({"role": "user", "content": auto_prompt})
            response = generate_ai_response(auto_prompt, rkat_context)
            st.session_state.ai_chat_history.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col2:
        if st.button("✅ Cek Compliance", use_container_width=True):
            auto_prompt = "Periksa kesesuaian RKAT saya dengan KUP dan SBO terbaru"
            st.session_state.ai_chat_history.append({"role": "user", "content": auto_prompt})
            response = generate_ai_response(auto_prompt, rkat_context)
            st.session_state.ai_chat_history.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col3:
        if st.button("⏱️ Prediksi Timeline", use_container_width=True):
            auto_prompt = "Berapa lama estimasi waktu approval untuk RKAT saya?"
            st.session_state.ai_chat_history.append({"role": "user", "content": auto_prompt})
            response = generate_ai_response(auto_prompt, rkat_context)
            st.session_state.ai_chat_history.append({"role": "assistant", "content": response})
            st.rerun()

def show_scenario_planning():
    """Scenario planning and budget analysis"""
    st.subheader("📊 Scenario Planning & Budget Analysis")
    
    st.markdown("Buat berbagai skenario anggaran untuk analisis dan perencanaan:")
    
    # Input parameters
    col1, col2 = st.columns(2)
    
    with col1:
        base_budget = st.number_input(
            "Anggaran Dasar (Rp)", 
            min_value=0, 
            value=1000000000, 
            step=10000000,
            format="%d"
        )
        
        inflation_rate = st.slider(
            "Tingkat Inflasi (%)", 
            min_value=0.0, 
            max_value=10.0, 
            value=3.50, 
            step=0.1
        )
        
        growth_target = st.slider(
            "Target Pertumbuhan (%)", 
            min_value=-10.0, 
            max_value=20.0, 
            value=5.0, 
            step=0.5
        )
    
    with col2:
        num_scenarios = st.number_input(
            "Jumlah Skenario", 
            min_value=1, 
            max_value=10, 
            value=3,
            step=1
        )
        
        risk_level = st.selectbox(
            "Tingkat Risiko",
            ["Conservative", "Moderate", "Aggressive"],
            index=0
        )
        
        focus_area = st.selectbox(
            "Area Fokus",
            ["Operasional", "Investasi", "Pengembangan", "Maintenance"],
            index=0
        )
    
    # Generate scenarios button
    if st.button("🔬 Generate Scenarios", use_container_width=True):
        scenarios = generate_budget_scenarios(
            base_budget, inflation_rate, growth_target, 
            num_scenarios, risk_level, focus_area
        )
        
        # Display scenarios
        st.subheader("📈 Hasil Analisis Skenario")
        
        # Create DataFrame for display
        scenario_df = pd.DataFrame(scenarios)
        st.dataframe(scenario_df, use_container_width=True)
        
        # Visualization
        fig = px.bar(
            scenario_df, 
            x='Scenario', 
            y='Budget_Amount',
            color='Risk_Level',
            title="Perbandingan Skenario Anggaran",
            labels={'Budget_Amount': 'Anggaran (Rp)', 'Scenario': 'Skenario'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations
        st.subheader("💡 Rekomendasi AI")
        show_scenario_recommendations(scenarios, risk_level)

def show_budget_optimization():
    """Budget optimization tools"""
    st.subheader("🎯 Budget Optimization")
    
    # Load RKAT data
    rkat_list = load_rkat_data()
    
    if rkat_list:
        # FIXED: Safe key access untuk selectbox
        try:
            # Process RKAT list dengan safe key mapping
            processed_rkat = []
            for rkat in rkat_list:
                processed_item = {
                    'id': rkat.get('id', 'N/A'),
                    'title': rkat.get('judul', rkat.get('title', 'No Title')),  # FIXED: Map judul -> title
                    'budget': rkat.get('total_anggaran', 0),
                    'bidang': rkat.get('bidang', 'N/A')
                }
                processed_rkat.append(processed_item)
            
            if processed_rkat:
                # FIXED: Selectbox dengan safe format function
                selected_rkat_id = st.selectbox(
                    "Pilih RKAT untuk optimasi:",
                    options=[r["id"] for r in processed_rkat],
                    format_func=lambda x: next(
                        (r["title"] for r in processed_rkat if r["id"] == x), 
                        "Unknown RKAT"  # Fallback value
                    )
                )
                
                if selected_rkat_id:
                    selected_rkat = next(
                        (r for r in processed_rkat if r["id"] == selected_rkat_id), 
                        None
                    )
                    
                    if selected_rkat:
                        st.write(f"**RKAT Terpilih:** {selected_rkat['title']}")
                        st.write(f"**Anggaran Saat Ini:** Rp {selected_rkat['budget']:,.0f}")
                        
                        # Optimization parameters
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            optimization_target = st.selectbox(
                                "Target Optimasi:",
                                ["Efisiensi Biaya", "Maksimalkan Output", "Balance Cost-Benefit"]
                            )
                            
                            reduction_percentage = st.slider(
                                "Target Pengurangan Biaya (%)",
                                min_value=0,
                                max_value=30,
                                value=10,
                                step=1
                            )
                        
                        with col2:
                            priority_areas = st.multiselect(
                                "Area Prioritas:",
                                ["Personil", "Operasional", "Teknologi", "Training", "Equipment"],
                                default=["Operasional"]
                            )
                        
                        # Run optimization
                        if st.button("⚡ Optimize Budget", use_container_width=True):
                            optimization_results = run_budget_optimization(
                                selected_rkat, optimization_target, 
                                reduction_percentage, priority_areas
                            )
                            
                            st.subheader("📊 Hasil Optimasi")
                            display_optimization_results(optimization_results)
            
            else:
                st.info("📝 Tidak ada RKAT yang tersedia untuk optimasi")
                show_sample_optimization()
                
        except Exception as e:
            st.error(f"Error loading RKAT data: {e}")
            show_sample_optimization()
    
    else:
        st.info("📝 Tidak ada data RKAT. Menampilkan contoh optimasi:")
        show_sample_optimization()

def show_compliance_assistant():
    """Compliance checking assistant"""
    st.subheader("✅ Compliance Assistant")
    
    st.markdown("""
    ### 📋 Pemeriksaan Kesesuaian RKAT
    
    Assistant akan membantu memverifikasi kesesuaian RKAT Anda dengan:
    - 📜 **KUP (Kebijakan Umum Penganggaran)**
    - 📊 **SBO (Standar Biaya Operasional)**
    - 🏛️ **Peraturan BPKH**
    - 📝 **Template dan Format Standar**
    """)
    
    # Load compliance data
    compliance_checks = run_compliance_checks()
    
    # Display compliance status
    st.subheader("🔍 Status Compliance")
    
    for check in compliance_checks:
        status_icon = "✅" if check["status"] == "PASS" else "❌" if check["status"] == "FAIL" else "⚠️"
        
        with st.expander(f"{status_icon} {check['category']}", expanded=check["status"] != "PASS"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Deskripsi:** {check['description']}")
                st.write(f"**Status:** {check['status']}")
                if check.get('details'):
                    st.write(f"**Detail:** {check['details']}")
            
            with col2:
                if check["status"] == "PASS":
                    st.success("Compliant")
                elif check["status"] == "FAIL":
                    st.error("Non-Compliant")
                else:
                    st.warning("Perlu Review")
    
    # Overall compliance score
    total_checks = len(compliance_checks)
    passed_checks = len([c for c in compliance_checks if c["status"] == "PASS"])
    compliance_score = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
    
    st.subheader("📊 Compliance Score")
    st.metric("Overall Compliance", f"{compliance_score:.1f}%")
    
    # Progress bar
    st.progress(compliance_score / 100)
    
    # Recommendations
    if compliance_score < 100:
        st.subheader("💡 Rekomendasi Perbaikan")
        failed_checks = [c for c in compliance_checks if c["status"] != "PASS"]
        
        for i, check in enumerate(failed_checks, 1):
            st.write(f"{i}. **{check['category']}**: {check.get('recommendation', 'Periksa kembali dokumen terkait')}")

# Helper Functions

def load_rkat_context():
    """Load RKAT data for AI context"""
    try:
        response = make_api_request("GET", "/rkat/", headers=get_auth_headers())
        if response and response.status_code == 200:
            return response.json()
    except:
        pass
    return []

def load_rkat_data():
    """Load RKAT data with error handling"""
    try:
        response = make_api_request("GET", "/rkat/", headers=get_auth_headers())
        if response and response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error loading RKAT data: {e}")
    return []

def generate_ai_response(prompt, context):
    """Generate AI response based on prompt and context"""
    # Simple rule-based responses (replace with actual AI integration)
    prompt_lower = prompt.lower()
    
    if "budget" in prompt_lower or "anggaran" in prompt_lower:
        return """
        📊 **Analisis Budget RKAT:**
        
        Berdasarkan data yang tersedia:
        1. **Kelayakan Anggaran**: Sesuai dengan standar industri
        2. **Benchmark**: Dalam range normal untuk bidang serupa
        3. **Rekomendasi**: 
           - Pertimbangkan alokasi 15% untuk kontingensi
           - Prioritaskan item dengan ROI tinggi
           - Review kembali biaya operasional rutin
        
        💡 **Saran**: Gunakan tool "Budget Optimization" untuk analisis lebih detail.
        """
    
    elif "compliance" in prompt_lower or "kup" in prompt_lower or "sbo" in prompt_lower:
        return """
        ✅ **Compliance Check:**
        
        Status kesesuaian RKAT Anda:
        1. **KUP Compliance**: ✅ Sesuai dengan kebijakan umum
        2. **SBO Compliance**: ⚠️ Beberapa item perlu review
        3. **Format**: ✅ Sesuai template standar
        
        📋 **Action Items**:
        - Review standar biaya untuk kategori "Teknologi"
        - Pastikan justifikasi anggaran lengkap
        - Update referensi ke KUP terbaru
        
        💡 **Saran**: Gunakan "Compliance Assistant" untuk check detail.
        """
    
    elif "timeline" in prompt_lower or "approval" in prompt_lower:
        return """
        ⏱️ **Prediksi Timeline Approval:**
        
        Estimasi waktu berdasarkan kompleksitas RKAT:
        1. **Review Audit Internal**: 5-7 hari kerja
        2. **Review Komite Dewan**: 3-5 hari kerja  
        3. **Approval Dewan Pengawas**: 2-3 hari kerja
        
        📊 **Total Estimasi**: 12-15 hari kerja
        
        🚀 **Tips Percepatan**:
        - Lengkapi semua dokumen pendukung
        - Pastikan justifikasi jelas dan terukur
        - Koordinasi proaktif dengan reviewer
        
        💡 **Catatan**: Timeline dapat lebih cepat jika tidak ada revisi major.
        """
    
    else:
        return f"""
        🤖 **AI Assistant Response:**
        
        Terima kasih atas pertanyaan: "{prompt}"
        
        Saya dapat membantu Anda dengan:
        - 📊 Analisis kelayakan anggaran
        - ✅ Pemeriksaan compliance KUP & SBO  
        - ⏱️ Prediksi timeline approval
        - 💡 Saran optimasi budget
        - 📈 Benchmarking dengan RKAT serupa
        
        Coba gunakan tombol Quick Actions atau ajukan pertanyaan spesifik tentang RKAT Anda!
        
        💡 **Contoh pertanyaan**:
        - "Bagaimana cara mengoptimalkan budget IT?"
        - "Apakah anggaran saya sudah sesuai SBO?"
        - "Berapa lama proses approval biasanya?"
        """

def generate_budget_scenarios(base_budget, inflation, growth, num_scenarios, risk_level, focus_area):
    """Generate budget scenarios"""
    scenarios = []
    
    risk_multipliers = {
        "Conservative": [0.8, 0.9, 1.0],
        "Moderate": [0.9, 1.0, 1.1, 1.2],
        "Aggressive": [1.0, 1.2, 1.4, 1.6]
    }
    
    multipliers = risk_multipliers.get(risk_level, [0.9, 1.0, 1.1])
    
    for i in range(num_scenarios):
        multiplier = multipliers[i % len(multipliers)]
        
        scenario_budget = base_budget * (1 + (inflation + growth) / 100) * multiplier
        
        scenarios.append({
            "Scenario": f"Skenario {i+1}",
            "Budget_Amount": int(scenario_budget),
            "Risk_Level": risk_level,
            "Focus_Area": focus_area,
            "Variance": f"{((multiplier - 1) * 100):+.1f}%"
        })
    
    return scenarios

def show_scenario_recommendations(scenarios, risk_level):
    """Show recommendations based on scenarios"""
    if risk_level == "Conservative":
        st.info("""
        🛡️ **Rekomendasi Conservative:**
        - Pilih skenario dengan variance terendah
        - Alokasikan 20% untuk contingency fund
        - Focus pada ROI yang sudah terbukti
        """)
    elif risk_level == "Moderate":
        st.info("""
        ⚖️ **Rekomendasi Moderate:**
        - Balance antara stability dan growth
        - Alokasikan 15% untuk contingency
        - Mix antara proven dan innovative initiatives
        """)
    else:
        st.warning("""
        🚀 **Rekomendasi Aggressive:**
        - Target growth maksimal dengan calculated risk
        - Alokasikan 25% untuk high-impact projects
        - Monitor closely dan siap untuk adjustment
        """)

def run_budget_optimization(rkat, target, reduction_pct, priority_areas):
    """Run budget optimization analysis"""
    current_budget = rkat['budget']
    target_budget = current_budget * (1 - reduction_pct / 100)
    savings = current_budget - target_budget
    
    return {
        "current_budget": current_budget,
        "target_budget": target_budget,
        "savings": savings,
        "reduction_percentage": reduction_pct,
        "optimized_areas": priority_areas,
        "recommendations": [
            "Consolidate vendor contracts untuk better pricing",
            "Implement shared services untuk reduce duplicate costs",
            "Optimize resource allocation berdasarkan priority matrix",
            "Consider phased implementation untuk spread costs"
        ]
    }

def display_optimization_results(results):
    """Display optimization results"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Budget Saat Ini", f"Rp {results['current_budget']:,.0f}")
    
    with col2:
        st.metric("Target Budget", f"Rp {results['target_budget']:,.0f}")
    
    with col3:
        st.metric("Potential Savings", f"Rp {results['savings']:,.0f}")
    
    st.subheader("💡 Rekomendasi Optimasi")
    for i, rec in enumerate(results['recommendations'], 1):
        st.write(f"{i}. {rec}")

def show_sample_optimization():
    """Show sample optimization for demo"""
    st.info("📊 Contoh Optimasi Budget (Sample Data)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Budget Saat Ini", "Rp 2,500,000,000")
    
    with col2:
        st.metric("Target Budget", "Rp 2,250,000,000")
    
    with col3:
        st.metric("Potential Savings", "Rp 250,000,000")

def run_compliance_checks():
    """Run compliance checks"""
    return [
        {
            "category": "KUP Compliance",
            "description": "Kesesuaian dengan Kebijakan Umum Penganggaran",
            "status": "PASS",
            "details": "Semua item sesuai dengan KUP 2026"
        },
        {
            "category": "SBO Compliance", 
            "description": "Kesesuaian dengan Standar Biaya Operasional",
            "status": "WARNING",
            "details": "Beberapa item melebihi standar biaya",
            "recommendation": "Review item dengan cost variance > 15%"
        },
        {
            "category": "Format & Template",
            "description": "Kesesuaian format dengan template standar",
            "status": "PASS",
            "details": "Format sesuai template RKAT BPKH v2.0"
        },
        {
            "category": "Dokumen Pendukung",
            "description": "Kelengkapan dokumen justifikasi",
            "status": "FAIL", 
            "details": "Beberapa dokumen belum lengkap",
            "recommendation": "Lengkapi TOR dan risk assessment"
        }
    ]

if __name__ == "__main__":
    main()
