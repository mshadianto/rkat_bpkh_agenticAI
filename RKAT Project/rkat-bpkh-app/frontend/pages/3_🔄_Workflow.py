import streamlit as st
import pandas as pd
from datetime import datetime
from utils.api_client import APIClient
from components.auth import AuthComponent
from config.settings import settings

# Page config
st.set_page_config(
    page_title="Workflow - RKAT BPKH",
    page_icon="🔄",
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

st.title("🔄 Workflow Management")

user_info = auth.get_user_info()
user_role = user_info.get('role', '')

# Workflow tabs based on user role
if auth.can_review_rkat():
    tab1, tab2, tab3 = st.tabs(["📥 Review Queue", "✅ Review RKAT", "📊 Workflow Analytics"])
else:
    tab1, tab2 = st.tabs(["📋 Status RKAT Saya", "📊 Workflow Analytics"])

# Tab 1: Review Queue or My RKAT Status
with tab1:
    if auth.can_review_rkat():
        st.subheader("📥 RKAT Menunggu Review")
        
        # Get pending reviews
        with st.spinner("Memuat RKAT yang menunggu review..."):
            response = api_client.get_pending_reviews()
            
            if response["success"]:
                pending_reviews = response["data"]["pending_reviews"]
                
                if pending_reviews:
                    # Display pending reviews
                    for rkat in pending_reviews:
                        with st.container():
                            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                            
                            with col1:
                                st.write(f"**{rkat['title']}**")
                                st.write(f"Pembuat: {rkat['creator']}")
                                st.write(f"Disubmit: {rkat['submitted_at']}")
                            
                            with col2:
                                st.write(f"**Status:**")
                                st.write(settings.RKAT_STATUS.get(rkat['status'], rkat['status']))
                            
                            with col3:
                                st.write(f"**Anggaran:**")
                                st.write(f"Rp {rkat['total_budget']/1e9:.2f}M")
                            
                            with col4:
                                if st.button(f"Review", key=f"review_{rkat['id']}"):
                                    st.session_state.review_rkat_id = rkat['id']
                                    st.rerun()
                        
                        st.divider()
                
                else:
                    st.info("Tidak ada RKAT yang menunggu review")
            
            else:
                st.error(f"Gagal memuat review queue: {response.get('error', 'Unknown error')}")
    
    else:
        st.subheader("📋 Status RKAT Saya")
        
        # Get user's RKAT list
        response = api_client.get_rkat_list()
        
        if response["success"]:
            user_rkats = response["data"]
            
            if user_rkats:
                # Create timeline view
                for rkat in user_rkats:
                    with st.container():
                        col1, col2, col3 = st.columns([2, 1, 1])
                        
                        with col1:
                            st.write(f"**{rkat['title']}**")
                            
                            # Status progress
                            status = rkat['status']
                            if status in ['draft']:
                                progress = 0.1
                            elif status in ['submitted', 'under_audit_review']:
                                progress = 0.3
                            elif status in ['audit_approved', 'under_committee_review']:
                                progress = 0.5
                            elif status in ['committee_approved', 'under_board_review']:
                                progress = 0.7
                            elif status in ['board_approved', 'final_approved']:
                                progress = 1.0
                            else:
                                progress = 0.2
                            
                            st.progress(progress)
                        
                        with col2:
                            st.write(f"**Status:**")
                            st.write(settings.RKAT_STATUS.get(status, status))
                        
                        with col3:
                            st.write(f"**Anggaran:**")
                            st.write(f"Rp {rkat['total_budget']/1e9:.2f}M")
                    
                    st.divider()
            
            else:
                st.info("Anda belum membuat RKAT")

# Tab 2: Review RKAT (only for reviewers)
if auth.can_review_rkat():
    with tab2:
        st.subheader("✅ Review RKAT")
        
        if 'review_rkat_id' in st.session_state:
            rkat_id = st.session_state.review_rkat_id
            
            # Get RKAT details
            response = api_client.get_rkat_detail(rkat_id)
            
            if response["success"]:
                rkat_data = response["data"]["rkat"]
                activities = response["data"]["activities"]
                
                # RKAT Summary
                st.write(f"### {rkat_data['title']}")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Anggaran", f"Rp {rkat_data['total_budget']:,.0f}")
                
                with col2:
                    st.metric("Jumlah Kegiatan", len(activities))
                
                with col3:
                    st.metric("Status", settings.RKAT_STATUS.get(rkat_data['status'], rkat_data['status']))
                
                # Compliance Check
                st.subheader("📊 Cek Kepatuhan")
                
                if st.button("Periksa Kepatuhan"):
                    compliance_response = api_client.check_compliance(rkat_id)
                    
                    if compliance_response["success"]:
                        compliance_data = compliance_response["data"]
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Kepatuhan KUP:**")
                            kup_score = compliance_data["kup_compliance"]["compliance_percentage"]
                            st.progress(kup_score / 100)
                            st.write(f"Skor: {kup_score:.1f}%")
                            
                            # Show recommendations
                            recommendations = compliance_data["kup_compliance"].get("recommendations", [])
                            if recommendations:
                                st.write("**Rekomendasi:**")
                                for rec in recommendations:
                                    st.write(f"• {rec}")
                        
                        with col2:
                            st.write("**Kepatuhan SBO:**")
                            sbo_score = compliance_data["sbo_compliance"]["score"]
                            st.progress(sbo_score / 100)
                            st.write(f"Skor: {sbo_score:.1f}%")
                
                # Activities Review
                st.subheader("📝 Review Kegiatan")
                
                if activities:
                    activities_df = pd.DataFrame(activities)
                    activities_df['Budget'] = activities_df['budget_amount'].apply(lambda x: f"Rp {x:,.0f}")
                    
                    st.dataframe(
                        activities_df[['activity_code', 'activity_name', 'Budget', 'output_target', 'sbo_reference']],
                        column_config={
                            'activity_code': 'Kode',
                            'activity_name': 'Nama Kegiatan',
                            'Budget': 'Anggaran', 
                            'output_target': 'Target Output',
                            'sbo_reference': 'Ref. SBO'
                        },
                        use_container_width=True
                    )
                
                # Review Decision
                st.subheader("📋 Keputusan Review")
                
                review_form = st.form("review_form")
                
                with review_form:
                    action = st.radio(
                        "Keputusan Review:",
                        options=["approve", "reject"],
                        format_func=lambda x: "✅ Setujui" if x == "approve" else "❌ Tolak"
                    )
                    
                    comments = st.text_area(
                        "Komentar/Catatan:",
                        placeholder="Berikan komentar atau catatan review...",
                        height=150
                    )
                    
                    if action == "reject":
                        st.warning("⚠️ RKAT akan dikembalikan ke pembuat dengan catatan revisi")
                    else:
                        st.success("✅ RKAT akan diteruskan ke tahap review berikutnya")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.form_submit_button("Submit Review", type="primary", use_container_width=True):
                            review_response = api_client.review_rkat(rkat_id, action, comments)
                            
                            if review_response["success"]:
                                st.success("Review berhasil disubmit!")
                                st.balloons()
                                
                                # Clear review session
                                if 'review_rkat_id' in st.session_state:
                                    del st.session_state.review_rkat_id
                                
                                st.rerun()
                            else:
                                st.error(f"Gagal submit review: {review_response.get('error', 'Unknown error')}")
                    
                    with col2:
                        if st.form_submit_button("Batal", use_container_width=True):
                            if 'review_rkat_id' in st.session_state:
                                del st.session_state.review_rkat_id
                            st.rerun()
            
            else:
                st.error("Gagal memuat detail RKAT untuk review")
        
        else:
            st.info("Pilih RKAT dari Review Queue untuk melakukan review")

# Tab 3/2: Workflow Analytics
with (tab3 if auth.can_review_rkat() else tab2):
    st.subheader("📊 Workflow Analytics")
    
    # Get analytics data
    response = api_client.get_dashboard_metrics()
    
    if response["success"]:
        metrics = response["data"]
        
        # Workflow Performance Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_approval_time = metrics["performance_metrics"]["avg_approval_time_days"]
            st.metric("Rata-rata Waktu Approval", f"{avg_approval_time:.1f} hari")
        
        with col2:
            total_rkats = metrics["performance_metrics"]["total_rkats"]
            approved_rkats = metrics["performance_metrics"]["approved_rkats"]
            approval_rate = (approved_rkats / total_rkats * 100) if total_rkats > 0 else 0
            st.metric("Tingkat Approval", f"{approval_rate:.1f}%")
        
        with col3:
            pending_count = sum(1 for status in metrics["status_distribution"].keys() 
                              if 'under_' in status or status == 'submitted')
            st.metric("RKAT Pending", pending_count)
        
        # Status Distribution Chart
        import plotly.express as px
        
        status_data = metrics["status_distribution"]
        if status_data:
            # Group statuses for better visualization
            grouped_status = {}
            for status, count in status_data.items():
                if status in ['draft']:
                    grouped_status['Draft'] = grouped_status.get('Draft', 0) + count
                elif 'under_' in status or status == 'submitted':
                    grouped_status['Under Review'] = grouped_status.get('Under Review', 0) + count
                elif 'approved' in status:
                    grouped_status['Approved'] = grouped_status.get('Approved', 0) + count
                elif 'rejected' in status:
                    grouped_status['Rejected'] = grouped_status.get('Rejected', 0) + count
            
            fig = px.bar(
                x=list(grouped_status.keys()),
                y=list(grouped_status.values()),
                title="Distribusi Status Workflow RKAT",
                labels={'x': 'Status', 'y': 'Jumlah RKAT'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Recent Workflow Activities
        st.subheader("🕒 Aktivitas Workflow Terbaru")
        
        recent_activities = metrics["recent_activities"]
        if recent_activities:
            for activity in recent_activities[:5]:  # Show last 5
                with st.container():
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.write(f"**{activity['title']}**")
                        st.write(f"Pembuat: {activity['creator']}")
                    
                    with col2:
                        st.write(f"**Status:**")
                        st.write(settings.RKAT_STATUS.get(activity['status'], activity['status']))
                    
                    with col3:
                        st.write(f"**Tanggal:**")
                        st.write(activity['created_at'][:10])  # Show date only
                
                st.divider()
    
    else:
        st.error("Gagal memuat data analytics")