import streamlit as st
from config.settings import settings

# Configure the page
st.set_page_config(
    page_title=settings.APP_TITLE,
    page_icon=settings.APP_ICON,
    layout=settings.LAYOUT,
    initial_sidebar_state="expanded" if settings.SIDEBAR_DEFAULT_EXPANDED else "collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    
    .stMetric {
        background-color: #f0f2f6;
        border: 1px solid #e0e0e0;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    
    .stAlert {
        margin: 1rem 0;
    }
    
    .rkat-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .status-badge {
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-weight: bold;
        text-transform: uppercase;
    }
    
    .status-draft {
        background-color: #ffeaa7;
        color: #2d3436;
    }
    
    .status-submitted {
        background-color: #74b9ff;
        color: white;
    }
    
    .status-approved {
        background-color: #00b894;
        color: white;
    }
    
    .status-rejected {
        background-color: #e17055;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Main welcome page
st.title(f"{settings.APP_ICON} {settings.APP_TITLE}")

st.markdown("""
### Selamat datang di Sistem Manajemen RKAT BPKH

Sistem komprehensif untuk mengelola Rencana Kerja dan Anggaran Tahunan (RKAT) 
Badan Pengelola Keuangan Haji dengan fitur:

- 📊 **Dashboard Analytics** - Monitoring dan analisis RKAT
- 📝 **RKAT Management** - Penyusunan dan pengelolaan RKAT
- 🔄 **Workflow System** - Proses approval multi-stage
- 💡 **AI Assistant** - Bantuan AI untuk optimasi dan compliance
- 📈 **Advanced Analytics** - Laporan dan insights mendalam
- ⚙️ **Settings & Admin** - Konfigurasi sistem

### Fitur Utama:

**🎯 Compliance Check**
- Validasi KUP (Kebijakan Umum Penganggaran)
- Validasi SBO (Standar Biaya Operasional) 
- Auto-calculation sesuai standar BPKH

**🤖 AI-Powered Features**
- Scenario planning dan budget analysis
- Smart compliance recommendations
- Natural language query untuk data RKAT
- Document analysis dan validation

**📋 Workflow Management**
- Multi-stage approval process
- Real-time status tracking
- Automated notifications
- Audit trail lengkap

### Workflow RKAT BPKH:

```
Badan Pelaksana → Audit Internal → Komite Dewan Pengawas → Dewan Pengawas → DPR RI
    (Penyusun)      (Review)         (Review)               (Approval)     (Final)
```

---

**Mulai dengan login atau navigasi ke halaman yang diinginkan menggunakan sidebar.**
""")

# Quick stats (if available)
if 'auth_token' in st.session_state:
    st.markdown("### 📊 Quick Stats")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total RKAT", "12", delta="2")
    
    with col2:
        st.metric("Pending Review", "3", delta="-1")
    
    with col3:
        st.metric("Approved", "8", delta="1")
    
    with col4:
        st.metric("Total Budget", "Rp 15.2M", delta="5%")

# Footer
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: gray; padding: 2rem;'>
        {settings.APP_TITLE} v1.0 | 
        Powered by AI & Modern Technology | 
        © 2025 Badan Pengelola Keuangan Haji
    </div>
    """, 
    unsafe_allow_html=True
)