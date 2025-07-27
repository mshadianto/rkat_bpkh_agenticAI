import streamlit as st
import pandas as pd
import plotly.express as px
from utils.api_client import APIClient
from components.auth import AuthComponent
from config.settings import settings

# Page config
st.set_page_config(
    page_title="AI Assistant - RKAT BPKH",
    page_icon="💡",
    layout="wide"
)

# Initialize components
api_client = APIClient(settings.API_BASE_URL)
auth = AuthComponent(api_client)

# Check authentication
if not auth.is_authenticated():
    st.error("Silakan login terlebih dahulu")
    st.stop()

# Set API token
api_client.set_auth_token(st.session_state.auth_token)

st.title("💡 AI Assistant untuk RKAT")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Tabs for different AI features
tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat AI", "📊 Scenario Planning", "🎯 Budget Optimization", "📋 Compliance Assistant"])

with tab1:
    st.subheader("💬 Chat dengan AI Assistant")
    
    # Chat interface
    st.write("Tanyakan apa saja tentang RKAT, anggaran, atau kebijakan BPKH!")
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        for i, chat in enumerate(st.session_state.chat_history):
            # User message
            with st.chat_message("user"):
                st.write(chat["user"])
            
            # AI response
            with st.chat_message("assistant"):
                st.write(chat["assistant"])
    
    # Chat input
    user_query = st.chat_input("Ketik pertanyaan Anda di sini...")
    
    if user_query:
        # Add user message to history
        with st.chat_message("user"):
            st.write(user_query)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("AI sedang berpikir..."):
                response = api_client.ai_chat(
                    query=user_query,
                    context={
                        "user_role": auth.get_user_info().get("role"),
                        "department": auth.get_user_info().get("department")
                    }
                )
                
                if response["success"]:
                    ai_response = response["data"]["response"]
                    st.write(ai_response)
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "user": user_query,
                        "assistant": ai_response
                    })
                else:
                    st.error(f"AI Error: {response.get('error', 'Unknown error')}")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()
    
    # Quick questions
    st.subheader("❓ Pertanyaan Cepat")
    
    quick_questions = [
        "Bagaimana cara menghitung anggaran sesuai SBO?",
        "Apa saja dokumen yang diperlukan untuk RKAT?",
        "Bagaimana proses workflow approval RKAT?",
        "Apa kriteria kepatuhan KUP yang harus dipenuhi?",
        "Berapa batas maksimal anggaran operasional BPKH?"
    ]
    
    col1, col2 = st.columns(2)
    
    for i, question in enumerate(quick_questions):
        with (col1 if i % 2 == 0 else col2):
            if st.button(question, key=f"quick_{i}"):
                # Simulate clicking the question
                st.session_state.quick_question = question
                st.rerun()

with tab2:
    st.subheader("📊 Scenario Planning & Budget Analysis")
    
    # Scenario planning form
    with st.form("scenario_form"):
        st.write("Buat berbagai skenario anggaran untuk analisis dan perencanaan:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            base_budget = st.number_input(
                "Anggaran Dasar (Rp)", 
                min_value=0.0, 
                value=1000000000.0,  # 1 Milyar
                step=100000000.0,
                format="%.0f"
            )
            
            inflation_rate = st.slider("Tingkat Inflasi (%)", 0.0, 10.0, 3.5)
            growth_target = st.slider("Target Pertumbuhan (%)", -10.0, 20.0, 5.0)
        
        with col2:
            scenario_count = st.selectbox("Jumlah Skenario", [3, 5, 7])
            
            risk_level = st.selectbox(
                "Tingkat Risiko",
                ["Conservative", "Moderate", "Aggressive"]
            )
            
            focus_area = st.multiselect(
                "Area Fokus",
                ["Operasional", "Teknologi", "SDM", "Infrastruktur", "Program Kemaslahatan"],
                default=["Operasional"]
            )
        
        if st.form_submit_button("🚀 Generate Scenarios", type="primary"):
            with st.spinner("AI sedang menganalisis dan membuat skenario..."):
                scenario_response = api_client.scenario_analysis(
                    base_budget=base_budget,
                    parameters={
                        "inflation_rate": inflation_rate,
                        "growth_target": growth_target,
                        "risk_level": risk_level,
                        "focus_areas": focus_area
                    },
                    scenario_count=scenario_count
                )
                
                if scenario_response["success"]:
                    scenarios = scenario_response["data"]["scenarios"]
                    
                    st.success("Skenario berhasil dibuat!")
                    
                    # Display scenarios
                    for i, scenario in enumerate(scenarios, 1):
                        with st.expander(f"Skenario {i}: {scenario.get('name', f'Scenario {i}')}"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.metric("Total Budget", f"Rp {scenario.get('total_budget', 0):,.0f}")
                                st.metric("Operational", f"Rp {scenario.get('operational_budget', 0):,.0f}")
                                st.metric("Personnel", f"Rp {scenario.get('personnel_budget', 0):,.0f}")
                            
                            with col2:
                                st.write("**Asumsi:**")
                                for assumption in scenario.get('assumptions', []):
                                    st.write(f"• {assumption}")
                                
                                st.write("**Risiko:**")
                                for risk in scenario.get('risks', []):
                                    st.write(f"• {risk}")
                    
                    # Comparison chart
                    if len(scenarios) > 1:
                        st.subheader("📊 Perbandingan Skenario")
                        
                        comparison_data = []
                        for i, scenario in enumerate(scenarios, 1):
                            comparison_data.append({
                                'Scenario': f"Skenario {i}",
                                'Total Budget': scenario.get('total_budget', 0),
                                'Operational': scenario.get('operational_budget', 0),
                                'Personnel': scenario.get('personnel_budget', 0)
                            })
                        
                        df = pd.DataFrame(comparison_data)
                        
                        fig = px.bar(
                            df, 
                            x='Scenario', 
                            y=['Total Budget', 'Operational', 'Personnel'],
                            title="Perbandingan Anggaran per Skenario",
                            barmode='group'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                
                else:
                    st.error(f"Gagal membuat skenario: {scenario_response.get('error', 'Unknown error')}")

with tab3:
    st.subheader("🎯 Budget Optimization")
    
    # Get user's RKATs for optimization
    rkat_response = api_client.get_rkat_list()
    
    if rkat_response["success"] and rkat_response["data"]:
        rkat_list = rkat_response["data"]
        
        # Select RKAT to optimize
        selected_rkat = st.selectbox(
            "Pilih RKAT untuk Optimasi",
            options=[r["id"] for r in rkat_list],
            format_func=lambda x: next(r["title"] for r in rkat_list if r["id"] == x)
        )
        
        if selected_rkat:
            # Optimization goals
            st.subheader("Tujuan Optimasi")
            
            optimization_goals = st.multiselect(
                "Pilih tujuan optimasi:",
                [
                    "Minimize Total Cost",
                    "Maximize Efficiency", 
                    "Improve Compliance",
                    "Balance Budget Allocation",
                    "Reduce Operational Overhead",
                    "Enhance Performance Metrics"
                ],
                default=["Minimize Total Cost", "Improve Compliance"]
            )
            
            if st.button("🎯 Optimize Budget", type="primary"):
                with st.spinner("AI sedang mengoptimalkan anggaran..."):
                    optimization_response = api_client.ai_chat(
                        query=f"Optimize budget for RKAT ID {selected_rkat} with goals: {', '.join(optimization_goals)}",
                        context={
                            "optimization_request": True,
                            "rkat_id": selected_rkat,
                            "goals": optimization_goals
                        }
                    )
                    
                    if optimization_response["success"]:
                        optimization_result = optimization_response["data"]["response"]
                        
                        st.success("Optimasi selesai!")
                        st.write(optimization_result)
                        
                        # Display optimization suggestions
                        st.subheader("💡 Rekomendasi Optimasi")
                        st.info("Hasil optimasi AI akan menampilkan saran spesifik untuk perbaikan anggaran Anda.")
                    
                    else:
                        st.error(f"Gagal melakukan optimasi: {optimization_response.get('error', 'Unknown error')}")
    
    else:
        st.info("Tidak ada RKAT tersedia untuk optimasi. Buat RKAT terlebih dahulu.")

with tab4:
    st.subheader("📋 Compliance Assistant")
    
    # Get user's RKATs for compliance check
    rkat_response = api_client.get_rkat_list()
    
    if rkat_response["success"] and rkat_response["data"]:
        rkat_list = rkat_response["data"]
        
        # Select RKAT for compliance analysis
        selected_rkat = st.selectbox(
            "Pilih RKAT untuk Analisis Kepatuhan",
            options=[r["id"] for r in rkat_list],
            format_func=lambda x: next(r["title"] for r in rkat_list if r["id"] == x),
            key="compliance_rkat"
        )
        
        if selected_rkat:
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔍 Analisis Kepatuhan KUP", use_container_width=True):
                    with st.spinner("Menganalisis kepatuhan KUP..."):
                        response = api_client.ai_chat(
                            query=f"Analyze KUP compliance for RKAT ID {selected_rkat}",
                            context={"compliance_type": "KUP", "rkat_id": selected_rkat}
                        )
                        
                        if response["success"]:
                            st.success("Analisis KUP selesai!")
                            st.write(response["data"]["response"])
            
            with col2:
                if st.button("🔍 Analisis Kepatuhan SBO", use_container_width=True):
                    with st.spinner("Menganalisis kepatuhan SBO..."):
                        response = api_client.ai_chat(
                            query=f"Analyze SBO compliance for RKAT ID {selected_rkat}",
                            context={"compliance_type": "SBO", "rkat_id": selected_rkat}
                        )
                        
                        if response["success"]:
                            st.success("Analisis SBO selesai!")
                            st.write(response["data"]["response"])
            
            # Comprehensive compliance check
            st.subheader("🏆 Comprehensive Compliance Check")
            
            if st.button("📊 Check Full Compliance", type="primary", use_container_width=True):
                with st.spinner("Melakukan pemeriksaan kepatuhan lengkap..."):
                    compliance_response = api_client.check_compliance(selected_rkat)
                    
                    if compliance_response["success"]:
                        compliance_data = compliance_response["data"]
                        
                        # KUP Compliance Detail
                        st.subheader("📋 Kepatuhan KUP")
                        kup_data = compliance_data["kup_compliance"]
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            score = kup_data["compliance_percentage"]
                            st.metric("Skor KUP", f"{score:.1f}%")
                            st.progress(score / 100)
                        
                        with col2:
                            level = kup_data["compliance_level"]
                            st.metric("Level Kepatuhan", level)
                        
                        # Detailed checks
                        st.write("**Detail Pemeriksaan:**")
                        for check in kup_data.get("checks", []):
                            status_icon = "✅" if check["status"] == "PASS" else "⚠️" if check["status"] == "PARTIAL" else "❌"
                            st.write(f"{status_icon} {check['check']}: {check['message']}")
                        
                        # Recommendations
                        recommendations = kup_data.get("recommendations", [])
                        if recommendations:
                            st.write("**Rekomendasi:**")
                            for rec in recommendations:
                                st.write(f"• {rec}")
                        
                        # SBO Compliance
                        st.subheader("💰 Kepatuhan SBO")
                        sbo_data = compliance_data["sbo_compliance"]
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            sbo_score = sbo_data["score"]
                            st.metric("Skor SBO", f"{sbo_score:.1f}%")
                            st.progress(sbo_score / 100)
                        
                        with col2:
                            sbo_level = sbo_data["level"]
                            st.metric("Level Kepatuhan", sbo_level)
                    
                    else:
                        st.error(f"Gagal memeriksa kepatuhan: {compliance_response.get('error', 'Unknown error')}")
    
    else:
        st.info("Tidak ada RKAT tersedia untuk analisis kepatuhan.")
    
    # Compliance Tips
    st.subheader("💡 Tips Kepatuhan")
    
    with st.expander("📖 Panduan KUP (Kebijakan Umum Penganggaran)"):
        st.write("""
        **Pastikan RKAT Anda memenuhi kriteria KUP:**
        
        1. **Tema 2026**: Institutional Strengthening
        2. **Sasaran Strategis**:
           - Pengembangan investasi pada ekosistem haji dan umroh
           - Amandemen peraturan untuk penguatan kelembagaan dan tata kelola BPKH
        3. **Prinsip Anggaran**: Efisien, efektif, rasional, dan akuntabel
        4. **Dokumen Lengkap**: KAK, RAB, Action Plan, Timeline, WBS
        5. **Efisiensi**: Hindari duplikasi kegiatan, optimalisasi ruang meeting, dll.
        """)
    
    with st.expander("💰 Panduan SBO (Standar Biaya Operasional)"):
        st.write("""
        **Pastikan anggaran sesuai dengan SBO 2026:**
        
        1. **Honorarium**: Sesuai eselon dan golongan
        2. **Meeting Package**: Fullday (Rp 635.000) vs Halfday (Rp 450.000)
        3. **Konsumsi Rapat**: Rp 125.000 per orang
        4. **ATK**: Rp 5.000.000 per paket
        5. **Dokumentasi**: Rp 20.000.000 untuk foto/video
        6. **Variance**: Maksimal 10% dari standar SBO
        """)