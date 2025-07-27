# 🏛️ RKAT BPKH Management System

Sistem Manajemen Rencana Kerja dan Anggaran Tahunan (RKAT) untuk Badan Pengelola Keuangan Haji (BPKH) dengan fitur AI-powered decision support dan RAG (Retrieval-Augmented Generation).

## 🚀 Features

### Core Features
- **📊 RKAT Management**: Penyusunan, editing, dan monitoring RKAT
- **🔄 Multi-stage Workflow**: Approval process sesuai regulasi BPKH
- **✅ Compliance Check**: Validasi KUP dan SBO otomatis
- **📈 Analytics Dashboard**: Real-time monitoring dan insights
- **👥 User Management**: Role-based access control

### AI-Powered Features
- **💡 AI Assistant**: Chat AI untuk bantuan RKAT
- **📊 Scenario Planning**: Multiple budget scenarios analysis
- **🎯 Budget Optimization**: AI-powered budget recommendations
- **📋 Compliance Assistant**: Smart compliance suggestions
- **🔍 Document Analysis**: AI document review dan validation

### Technical Features
- **🛡️ Security**: JWT authentication, RBAC, audit logging
- **🚀 Performance**: Redis caching, optimized queries
- **📱 Responsive**: Modern web interface dengan Streamlit
- **🔄 Real-time**: WebSocket notifications
- **🐳 Containerized**: Docker deployment ready

## 🏗️ Architecture

```
Frontend (Streamlit) ←→ Backend (FastAPI) ←→ Database (PostgreSQL)
                                ↓
                        AI Services (Qwen3 via OpenRouter)
                                ↓
                        RAG Engine (ChromaDB)
```

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL 12+
- Redis 6+
- OpenRouter API Key (untuk AI features)

## 🛠️ Installation & Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd rkat-bpkh-app
```

### 2. Setup Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env dengan konfigurasi database dan API keys
```

### 3. Setup Frontend
```bash
cd frontend
pip install -r requirements.txt
```

### 4. Setup Database
```bash
python scripts/setup_database.py --all
```

### 5. Run Development Server
```bash
python scripts/run_development.py
```

Atau manual:
```bash
# Terminal 1 - Backend
cd backend && python run.py

# Terminal 2 - Frontend  
cd frontend && streamlit run app.py
```

## 🐳 Docker Deployment

### Development
```bash
docker-compose up -d
```

### Production
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 📚 Usage Guide

### 1. Login & User Roles

Default users untuk testing:
- **admin** / admin123 (Administrator)
- **badan_pelaksana** / bp123 (Badan Pelaksana)
- **audit_internal** / audit123 (Audit Internal)
- **komite_dewan** / komite123 (Komite Dewan Pengawas)
- **dewan_pengawas** / dewan123 (Dewan Pengawas)

### 2. RKAT Workflow

```
1. Badan Pelaksana → Buat RKAT → Submit
2. Audit Internal → Review → Approve/Reject
3. Komite Dewan Pengawas → Review → Approve/Reject
4. Dewan Pengawas → Final Approval → Approve/Reject
```

### 3. Key Features Usage

#### Membuat RKAT Baru
1. Login sebagai Badan Pelaksana
2. Navigate ke "RKAT Management"
3. Tab "Buat RKAT" → Isi form → Submit
4. Tambah kegiatan dan upload dokumen
5. Check compliance → Submit untuk review

#### Review RKAT
1. Login sebagai Reviewer (Audit/Komite/Dewan)
2. Navigate ke "Workflow"
3. Pilih RKAT dari Review Queue
4. Analisis compliance dan detail
5. Approve/Reject dengan komentar

#### AI Assistant
1. Navigate ke "AI Assistant"
2. Chat dengan AI untuk bantuan RKAT
3. Generate scenarios untuk budget planning
4. Optimize budget dengan AI recommendations

## 🔧 Configuration

### Environment Variables
**Backend (.env)**
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/rkat_bpkh
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Service
OPENROUTER_API_KEY=your-openrouter-api-key
MODEL_NAME=anthropic/claude-3-haiku

# Email (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your-email@domain.com
EMAIL_PASSWORD=your-email-password
```

### Compliance Configuration

File konfigurasi KUP dan SBO tersedia di:
- `data/kup/kebijakan_umum_penganggaran_2026.json`
- `data/sbo/standar_biaya_operasional_2026.json`

## 📊 API Documentation

Setelah backend running, akses:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints
- `POST /api/auth/login` - Authentication
- `GET /api/rkat/list` - Get RKAT list
- `POST /api/rkat/create` - Create new RKAT
- `POST /api/workflow/{rkat_id}/submit` - Submit RKAT
- `POST /api/ai/chat` - AI chat assistant

## 🧪 Testing

```bash
# Run backend tests
cd backend
python -m pytest tests/

# Run frontend tests
cd frontend
streamlit run --headless tests/test_components.py
```

## 📈 Monitoring & Analytics

### Key Metrics
- RKAT submission rate
- Approval cycle time
- Compliance scores (KUP & SBO)
- Budget efficiency ratios
- User activity logs

### Dashboard Features
- Real-time status tracking
- Budget analysis charts
- Compliance trends
- Performance metrics
- Workflow analytics

## 🛡️ Security

### Authentication & Authorization
- JWT-based authentication
- Role-based access control (RBAC)
- Session management with Redis
- Password hashing with bcrypt

### Data Protection
- Input validation & sanitization
- SQL injection prevention
- XSS protection
- CSRF protection
- Audit logging

### Compliance
- BPKH regulation compliance
- Data retention policies
- Access control matrix
- Security monitoring

## 🚀 Deployment

### Production Setup
1. Setup production database (PostgreSQL cluster)
2. Configure Redis cluster for caching
3. Setup SSL certificates
4. Configure load balancer (Nginx)
5. Setup monitoring (Prometheus + Grafana)
6. Configure backup strategy

### Environment-specific Configs
- **Development**: Local database, debug enabled
- **Staging**: Replica database, testing features
- **Production**: Cluster setup, monitoring enabled

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

Copyright © 2025 Badan Pengelola Keuangan Haji (BPKH)

## 🆘 Support

Untuk support dan pertanyaan:
- 📧 Email: support@bpkh.go.id
- 📱 WhatsApp: +62-xxx-xxxx-xxxx
- 🌐 Website: https://bpkh.go.id

## 🔄 Changelog

### v1.0.0 (2025-01-XX)
- Initial release
- Core RKAT management features
- Multi-stage workflow system
- AI assistant integration
- Compliance checking (KUP & SBO)
- Analytics dashboard
- User management & RBAC

---

**Dibuat dengan ❤️ untuk BPKH Indonesia**