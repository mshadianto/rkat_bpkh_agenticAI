import streamlit as st
import pandas as pd
from utils.api_client import APIClient
from components.auth import AuthComponent
from components.rkat_forms import RKATForms
from config.settings import settings

# Page config
st.set_page_config(
    page_title="RKAT Management - RKAT BPKH",
    page_icon="📊",
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
rkat_forms = RKATForms(api_client)

st.title("📊 Manajemen RKAT")

# Tabs for different RKAT management functions
tab1, tab2, tab3, tab4 = st.tabs(["📋 Daftar RKAT", "➕ Buat RKAT", "✏️ Edit RKAT", "📄 Detail RKAT"])

with tab1:
    st.subheader("📋 Daftar RKAT")
    
    # Get RKAT list
    with st.spinner("Memuat daftar RKAT..."):
        try:
            response = api_client.get_rkat_list()
            
            if response["success"]:
                rkat_list = response["data"]
                
                if rkat_list:
                    # Convert to DataFrame
                    df = pd.DataFrame(rkat_list)
                    df['Status'] = df['status'].map(settings.RKAT_STATUS)
                    df['Total Budget'] = df['total_budget'].apply(lambda x: f"Rp {x/1e9:.2f}B")
                    df['KUP Score'] = df['kup_compliance_score'].fillna(0).apply(lambda x: f"{x:.1f}%")
                    df['SBO Score'] = df['sbo_compliance_score'].fillna(0).apply(lambda x: f"{x:.1f}%")
                    
                    # Search and filter
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        search_term = st.text_input("🔍 Cari RKAT", placeholder="Masukkan judul RKAT...")
                    
                    with col2:
                        status_filter = st.selectbox("Filter Status", 
                                                   ["Semua"] + list(settings.RKAT_STATUS.values()))
                    
                    with col3:
                        year_filter = st.selectbox("Filter Tahun", 
                                                 ["Semua"] + sorted(df['year'].unique().tolist(), reverse=True))
                    
                    # Apply filters
                    filtered_df = df.copy()
                    
                    if search_term:
                        filtered_df = filtered_df[filtered_df['title'].str.contains(search_term, case=False, na=False)]
                    
                    if status_filter != "Semua":
                        filtered_df = filtered_df[filtered_df['Status'] == status_filter]
                    
                    if year_filter != "Semua":
                        filtered_df = filtered_df[filtered_df['year'] == year_filter]
                    
                    # Display table
                    st.dataframe(
                        filtered_df[['title', 'year', 'Status', 'Total Budget', 'KUP Score', 'SBO Score', 'creator_name', 'created_at']],
                        column_config={
                            'title': st.column_config.TextColumn('Judul RKAT'),
                            'year': st.column_config.NumberColumn('Tahun'),
                            'Status': st.column_config.TextColumn('Status'),
                            'Total Budget': st.column_config.TextColumn('Total Anggaran'),
                            'KUP Score': st.column_config.TextColumn('Skor KUP'),
                            'SBO Score': st.column_config.TextColumn('Skor SBO'),
                            'creator_name': st.column_config.TextColumn('Pembuat'),
                            'created_at': st.column_config.DatetimeColumn('Tanggal Dibuat')
                        },
                        use_container_width=True,
                        height=400
                    )
                    
                    # Select RKAT for detailed view
                    st.subheader("Pilih RKAT untuk Detail")
                    selected_rkat = st.selectbox(
                        "Pilih RKAT",
                        options=filtered_df['id'].tolist(),
                        format_func=lambda x: filtered_df[filtered_df['id'] == x]['title'].iloc[0]
                    )
                    
                    if st.button("Lihat Detail RKAT"):
                        st.session_state.selected_rkat_id = selected_rkat
                        st.rerun()
                
                else:
                    st.info("Belum ada RKAT yang dibuat")
                    
                    if auth.can_create_rkat():
                        if st.button("Buat RKAT Pertama"):
                            st.switch_page("pages/2_📊_RKAT_Management.py")
            
            else:
                st.error(f"Gagal memuat daftar RKAT: {response.get('error', 'Unknown error')}")
        
        except Exception as e:
            st.error(f"Error saat memuat daftar RKAT: {str(e)}")

with tab2:
    if auth.can_create_rkat():
        rkat_forms.create_rkat_form()
    else:
        st.warning("Anda tidak memiliki akses untuk membuat RKAT")

with tab3:
    st.subheader("✏️ Edit RKAT")
    
    if 'selected_rkat_id' in st.session_state:
        rkat_id = st.session_state.selected_rkat_id
        
        try:
            # Get RKAT details
            response = api_client.get_rkat_detail(rkat_id)
            
            if response["success"]:
                rkat_data = response["data"]["rkat"]
                activities = response["data"]["activities"]
                
                # Only allow editing if RKAT is in draft status
                if rkat_data["status"] == "draft":
                    st.success(f"Mengedit RKAT: {rkat_data['title']}")
                    
                    # Add activities section
                    st.subheader("Kegiatan RKAT")
                    
                    # Display existing activities
                    if activities:
                        st.write("**Kegiatan yang sudah ada:**")
                        
                        activities_df = pd.DataFrame(activities)
                        activities_df['Budget'] = activities_df['budget_amount'].apply(lambda x: f"Rp {x:,.0f}")
                        
                        st.dataframe(
                            activities_df[['activity_code', 'activity_name', 'Budget', 'output_target']],
                            column_config={
                                'activity_code': 'Kode',
                                'activity_name': 'Nama Kegiatan', 
                                'Budget': 'Anggaran',
                                'output_target': 'Target Output'
                            },
                            use_container_width=True
                        )
                    
                    # Add new activity
                    rkat_forms.add_activity_form(rkat_id)
                    
                    # Submit RKAT
                    st.subheader("Submit RKAT")
                    st.warning("Setelah disubmit, RKAT tidak dapat diedit lagi.")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("🚀 Submit RKAT untuk Review", type="primary"):
                            response = api_client.submit_rkat(rkat_id)
                            
                            if response["success"]:
                                st.success("RKAT berhasil disubmit untuk review!")
                                st.balloons()
                                st.rerun()
                            else:
                                st.error(f"Gagal submit RKAT: {response.get('error', 'Unknown error')}")
                    
                    with col2:
                        if st.button("💾 Simpan sebagai Draft"):
                            st.success("RKAT disimpan sebagai draft")
                
                else:
                    st.warning(f"RKAT dengan status '{settings.RKAT_STATUS.get(rkat_data['status'], rkat_data['status'])}' tidak dapat diedit")
            
            else:
                st.error("Gagal memuat detail RKAT")
        
        except Exception as e:
            st.error(f"Error saat memuat detail RKAT: {str(e)}")
    
    else:
        st.info("Pilih RKAT dari tab 'Daftar RKAT' untuk diedit")

with tab4:
    st.subheader("📄 Detail RKAT")
    
    if 'selected_rkat_id' in st.session_state:
        rkat_id = st.session_state.selected_rkat_id
        
        try:
            # Get RKAT details
            response = api_client.get_rkat_detail(rkat_id)
            
            if response["success"]:
                rkat_data = response["data"]["rkat"]
                activities = response["data"]["activities"]
                
                # RKAT Info - FIXED: Use .get() untuk field yang mungkin tidak ada
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Judul", rkat_data["title"])
                    st.metric("Tahun", rkat_data["year"])
                    st.metric("Status", settings.RKAT_STATUS.get(rkat_data["status"], rkat_data["status"]))
                    # FIX: Gunakan .get() dengan default value
                    st.metric("Program", rkat_data.get("program", "Tidak ada"))
                
                with col2:
                    st.metric("Total Anggaran", f"Rp {rkat_data['total_budget']:,.0f}")
                    st.metric("Anggaran Operasional", f"Rp {rkat_data['operational_budget']:,.0f}")
                    st.metric("Anggaran Personel", f"Rp {rkat_data['personnel_budget']:,.0f}")
                    # FIX: Handle nested creator field
                    creator_name = rkat_data.get("creator", {}).get("name", rkat_data.get("creator_name", "Tidak diketahui"))
                    st.metric("Pembuat", creator_name)
                
                # Compliance Scores
                if rkat_data.get("kup_compliance_score") is not None:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Skor KUP", f"{rkat_data['kup_compliance_score']:.1f}%")
                        st.progress(rkat_data['kup_compliance_score'] / 100)
                    
                    with col2:
                        st.metric("Skor SBO", f"{rkat_data.get('sbo_compliance_score', 0):.1f}%")
                        st.progress(rkat_data.get('sbo_compliance_score', 0) / 100)
                
                # Strategic Objectives
                if rkat_data.get("strategic_objectives"):
                    st.subheader("🎯 Sasaran Strategis")
                    for i, obj in enumerate(rkat_data["strategic_objectives"], 1):
                        st.write(f"{i}. {obj}")
                
                # Key Activities Summary
                if rkat_data.get("key_activities"):
                    st.subheader("🔑 Kegiatan Utama")
                    for i, activity in enumerate(rkat_data["key_activities"], 1):
                        st.write(f"{i}. {activity}")
                
                # Performance Indicators
                if rkat_data.get("performance_indicators"):
                    st.subheader("📈 Indikator Kinerja")
                    indicators_df = pd.DataFrame(rkat_data["performance_indicators"])
                    st.dataframe(indicators_df, use_container_width=True)
                
                # Activities Detail
                st.subheader("📝 Detail Kegiatan")
                
                if activities:
                    for activity in activities:
                        with st.expander(f"{activity['activity_code']} - {activity['activity_name']}"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write(f"**Anggaran:** Rp {activity['budget_amount']:,.0f}")
                                st.write(f"**Target Output:** {activity.get('output_target', 'Tidak ada')}")
                                st.write(f"**Target Outcome:** {activity.get('outcome_target', 'Tidak ada')}")
                            
                            with col2:
                                st.write(f"**Referensi SBO:** {activity.get('sbo_reference', 'Tidak ada')}")
                                
                                # Document status
                                docs = {
                                    "KAK": activity.get('kak_document'),
                                    "RAB": activity.get('rab_document'), 
                                    "Timeline": activity.get('timeline_document')
                                }
                                
                                st.write("**Status Dokumen:**")
                                for doc_name, doc_path in docs.items():
                                    status = "✅ Ada" if doc_path else "❌ Belum ada"
                                    st.write(f"- {doc_name}: {status}")
                            
                            if activity.get('description'):
                                st.write(f"**Deskripsi:** {activity['description']}")
                
                else:
                    st.info("Belum ada kegiatan yang ditambahkan")
                
                # Workflow History (dengan try-catch untuk handle missing endpoint)
                try:
                    st.subheader("📋 Riwayat Workflow")
                    
                    workflow_response = api_client.get_workflow_history(rkat_id)
                    
                    if workflow_response["success"]:
                        workflow_history = workflow_response["data"]["workflow_history"]
                        
                        if workflow_history:
                            for entry in workflow_history:
                                with st.container():
                                    col1, col2, col3 = st.columns([2, 1, 1])
                                    
                                    with col1:
                                        st.write(f"**{entry['action'].title()}** oleh {entry['user']}")
                                        if entry.get('comments'):
                                            st.write(f"Komentar: {entry['comments']}")
                                    
                                    with col2:
                                        st.write(f"Status: {entry['previous_status']} → {entry['new_status']}")
                                    
                                    with col3:
                                        st.write(f"Tanggal: {entry['timestamp']}")
                                
                                st.divider()
                        
                        else:
                            st.info("Belum ada riwayat workflow")
                    else:
                        st.info("Riwayat workflow tidak tersedia")
                
                except Exception as e:
                    st.info("Riwayat workflow tidak tersedia")
            
            else:
                st.error("Gagal memuat detail RKAT")
        
        except Exception as e:
            st.error(f"Error saat memuat detail RKAT: {str(e)}")
    
    else:
        st.info("Pilih RKAT dari tab 'Daftar RKAT' untuk melihat detail")