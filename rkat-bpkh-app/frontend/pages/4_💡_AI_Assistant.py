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
    
    Assistant akan membantu memverifikasi kesesuaian RKA
