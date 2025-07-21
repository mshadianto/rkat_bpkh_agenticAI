# 🏦 Bank Muamalat Health Monitor

Secure Streamlit dashboard for BPKH investment portfolio monitoring and risk analysis.

## 📋 Features

- **🔐 Secure Authentication**: Multi-layer security with user authentication, IP whitelisting, and session management
- **💼 Portfolio Monitoring**: Real-time investment portfolio tracking and analysis
- **⚠️ Risk Assessment**: Comprehensive risk analysis with automated alerts
- **📊 Shariah Compliance**: Islamic finance compliance monitoring and reporting
- **📈 Performance Analytics**: Investment performance tracking with benchmarking
- **📁 File Management**: Secure file upload and management system for portfolio data, reports, and documents
- **📱 Responsive Design**: Mobile-friendly interface with modern UI

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Git
- Access to Streamlit Cloud (for deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd bank-muamalat-health-monitor
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up configuration**
   ```bash
   # Copy the template secrets file
   cp .streamlit/secrets.toml.template .streamlit/secrets.toml
   
   # Edit the secrets file with your actual values
   nano .streamlit/secrets.toml
   ```

5. **Set up UI modules integration** (if you have existing ui/pages/ modules)
   ```bash
   # Create __init__.py files for proper imports
   touch ui/__init__.py
   touch ui/pages/__init__.py
   
   # See INTEGRATION_GUIDE.md for detailed setup
   ```

6. **Run the application**
   ```bash
   streamlit run main.py
   ```

7. **Access the application**
   - Open your browser and go to `http://localhost:8501`
   - Use the default credentials or the ones you configured

## 📁 Project Structure

```
bank-muamalat-health-monitor/
├── main.py                          # Main application file (updated with module integration)
├── app/
│   └── security/
│       └── auth.py                  # Authentication module
├── ui/                              # UI Package
│   ├── __init__.py                  # UI package initialization
│   └── pages/                       # Page modules
│       ├── __init__.py              # Pages package initialization
│       ├── overview.py              # Portfolio overview module
│       ├── decision_support.py      # Decision support system
│       ├── risk_assessment.py       # Risk assessment module
│       ├── compliance_monitoring.py # Shariah compliance monitoring
│       ├── strategic_analysis.py    # Strategic analysis tools
│       ├── financial_health.py      # Financial health assessment
│       └── app_info.py             # Application information
├── .streamlit/
│   ├── config.toml                  # Streamlit configuration
│   └── secrets.toml                 # Secret configuration (not in repo)
├── requirements.txt                 # Python dependencies
├── README.md                       # This file
├── INTEGRATION_GUIDE.md            # Guide for integrating existing UI modules
└── .gitignore                      # Git ignore rules
```

## 🔐 Authentication Setup

### Default Credentials (Development Only)

- **Username**: `admin`, **Password**: `bpkh2024!`
- **Username**: `mshadianto`, **Password**: `komiteaudit2024`
- **Username**: `bpkh_user`, **Password**: `muamalat2024`

### Production Setup

1. **Environment Variables** (Recommended)
   ```bash
   export AUTHORIZED_USERS="user1:password1,user2:password2"
   export AUTHORIZED_IPS="192.168.1.100,203.123.45.67"
   export ACCESS_TOKEN="your-secure-token"
   ```

2. **Streamlit Secrets** (For Streamlit Cloud)
   ```toml
   [auth]
   AUTHORIZED_USERS = "admin:hashed_password,user:hashed_password"
   AUTHORIZED_IPS = "ip1,ip2"
   ACCESS_TOKEN = "your-secure-token"
   ```

### Security Features

- **Password Hashing**: SHA256 encryption for stored passwords
- **Session Management**: Automatic session timeout (1 hour default)
- **Login Attempts**: Rate limiting with lockout (3 attempts, 15 min lockout)
- **IP Whitelisting**: Optional IP address restrictions
- **CSRF Protection**: Built-in cross-site request forgery protection

## 🌐 Deployment

### Streamlit Cloud Deployment

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select the `main.py` file
   - Configure secrets in the Streamlit Cloud dashboard

3. **Configure Secrets**
   - In Streamlit Cloud, go to your app settings
   - Add the secrets from `.streamlit/secrets.toml`
   - Save and redeploy

### Alternative Deployment Options

#### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Heroku Deployment
```bash
# Create Procfile
echo "web: sh setup.sh && streamlit run main.py" > Procfile

# Create setup.sh
cat > setup.sh << EOF
mkdir -p ~/.streamlit/
echo "[server]" > ~/.streamlit/config.toml
echo "port = \$PORT" >> ~/.streamlit/config.toml
echo "enableCORS = false" >> ~/.streamlit/config.toml
echo "headless = true" >> ~/.streamlit/config.toml
EOF
```

## 📁 File Upload System

### Supported File Types

- **Portfolio Data**: CSV, Excel (.xlsx, .xls)
- **Documents**: PDF, TXT, JSON
- **Archives**: ZIP files
- **Maximum Size**: 200MB per file

### File Categories

1. **📊 Portfolio Data**
   - Investment holdings
   - Asset valuations
   - Transaction data
   - Required columns: Date, Asset, Value

2. **⚠️ Risk Assessment**
   - Risk registers
   - Assessment reports
   - Expected columns: Risk_Type, Probability, Impact, Mitigation

3. **📋 Compliance Documents**
   - Shariah compliance reports
   - Audit documents
   - Regulatory filings
   - Internal assessments

4. **📄 External Reports**
   - Market analysis
   - Economic reports
   - Industry research
   - Third-party analysis

### Upload Process

1. **Navigate** to File Manager page
2. **Select** appropriate category tab
3. **Choose** files using the file uploader
4. **Validate** file format and content
5. **Preview** data (for CSV/Excel files)
6. **Configure** column mapping if needed
7. **Save** or **Import** to system

### Security Features

- **File Validation**: Automatic type and size checking
- **Access Control**: User-based upload permissions
- **Secure Storage**: Organized file system with user tracking
- **Audit Trail**: Upload history and user activity logging

### File Management

- **Browse Files**: View all uploaded files by category
- **Search & Filter**: Find files by name, date, or category
- **Preview**: Quick preview for supported file types
- **Download**: Secure file download functionality
- **Delete**: Remove files with proper permissions

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `AUTHORIZED_USERS` | Comma-separated user:password pairs | See defaults | No |
| `AUTHORIZED_IPS` | Comma-separated IP addresses | None (allow all) | No |
| `ACCESS_TOKEN` | URL-based access token | bpkh-muamalat-2024 | No |
| `APP_ENVIRONMENT` | Application environment | development | No |
| `SESSION_TIMEOUT` | Session timeout in seconds | 3600 | No |
| `MAX_LOGIN_ATTEMPTS` | Maximum login attempts | 3 | No |
| `LOCKOUT_DURATION` | Lockout duration in seconds | 900 | No |

### Streamlit Configuration

The `.streamlit/config.toml` file contains Streamlit-specific settings:

- **Server settings**: Port, CORS, upload limits
- **Theme customization**: Colors, fonts, layout
- **Security settings**: XSRF protection, static serving
- **Browser settings**: Usage stats, error details

## 📊 Features Overview

### Dashboard Modules

1. **Portfolio Overview**
   - Real-time asset allocation
   - Performance metrics
   - Composition charts

2. **Risk Analysis**
   - Risk matrix visualization
   - Alert system
   - Compliance monitoring

3. **Shariah Compliance**
   - Islamic finance compliance tracking
   - Prohibited sector monitoring
   - Purification calculations

4. **Reports & Analytics**
   - Performance reports
   - Compliance reports
   - Custom report builder

5. **File Management**
   - **📊 Portfolio Data Upload**: CSV/Excel files with portfolio holdings and valuations
   - **⚠️ Risk Assessment Files**: Risk data import and analysis
   - **📋 Compliance Documents**: Shariah compliance reports and audit documents
   - **📄 External Reports**: Market analysis and regulatory reports
   - **📁 File Browser**: Secure file storage with preview, download, and management features
   - **Supported Formats**: CSV, Excel (.xlsx, .xls), PDF, JSON, TXT, ZIP
   - **Security Features**: File validation, size limits (200MB), type restrictions, user access control

6. **Settings & Administration**
   - User preferences
   - Notification settings
   - Security configuration

### Modular Architecture

The application supports both **integrated** and **modular** approaches:

**🔗 Integrated Mode** (Default):
- All functionality in `main.py`
- Quick setup and deployment
- Self-contained application

**📦 Modular Mode** (Advanced):
- Separate modules in `ui/pages/` directory
- **📊 Overview Module**: Enhanced portfolio overview with advanced analytics
- **🎯 Decision Support**: AI-powered investment recommendations and scenario analysis
- **⚠️ Risk Assessment**: Comprehensive risk modeling and stress testing
- **📋 Compliance Monitoring**: Real-time Shariah compliance tracking and alerts
- **📈 Strategic Analysis**: Long-term strategic planning and optimization tools
- **🩺 Financial Health**: Overall financial health assessment and scoring
- Easy to maintain and extend
- Professional enterprise architecture

**Auto-Detection**: The application automatically detects if `ui/pages/` modules are available and switches to modular mode. If modules are not found, it falls back to integrated mode.

### Data Sources

Currently uses simulated data for demonstration. In production, integrate with:

- Core banking systems
- Investment management platforms
- Risk management systems
- Shariah compliance databases
- Market data providers

## 🔧 Customization

### Adding New Features

1. **Create new module**
   ```python
   # app/modules/new_feature.py
   def show_new_feature():
       st.markdown("## New Feature")
       # Your implementation
   ```

2. **Import in main.py**
   ```python
   from app.modules.new_feature import show_new_feature
   ```

3. **Add to navigation**
   ```python
   page = st.sidebar.selectbox(
       "Select Page",
       ["🏠 Dashboard", "💼 Portfolio", "🆕 New Feature"],
   )
   ```

### Styling Customization

Modify the CSS in the `st.markdown()` sections of `main.py` to customize:
- Colors and themes
- Card layouts
- Typography
- Responsive design

### Data Integration

Replace the `generate_sample_data()` function with real data sources:

```python
def connect_to_database():
    # Your database connection logic
    pass

def fetch_portfolio_data():
    # Fetch real portfolio data
    pass
```

## 🛡️ Security Best Practices

1. **Never commit secrets**
   - Use `.gitignore` for sensitive files
   - Use environment variables or Streamlit secrets

2. **Regular security updates**
   - Keep dependencies updated
   - Monitor for security vulnerabilities

3. **Production hardening**
   - Remove default credentials
   - Enable IP whitelisting
   - Use strong passwords
   - Enable HTTPS

4. **Monitoring and logging**
   - Monitor failed login attempts
   - Log security events
   - Set up alerts for suspicious activity

## 📞 Support

- **Developer**: MS Hadianto | Komite Audit
- **Organization**: BPKH
- **Email**: support@bpkh.go.id
- **Documentation**: See this README and inline code comments

## 📝 License

This application is proprietary software developed for BPKH. Unauthorized use, distribution, or modification is prohibited.

## 🔄 Version History

- **v1.0.0** - Initial release with core features
- **v1.1.0** - Enhanced security features
- **v1.2.0** - Added Shariah compliance monitoring
- **v1.3.0** - Improved UI/UX and performance

## 🚨 Troubleshooting

### Common Issues

1. **Authentication not working**
   - Check credentials in secrets.toml
   - Verify IP whitelist settings
   - Clear browser cache and cookies

2. **App not loading**
   - Check Python version compatibility
   - Verify all dependencies are installed
   - Check Streamlit Cloud logs

3. **Data not displaying**
   - Verify data source connections
   - Check date range filters
   - Review error logs

### Debug Mode

Enable debug mode for troubleshooting:

```python
# In main.py
import streamlit as st
st.set_option('logger.level', 'debug')
```

For additional support, contact the development team or check the Streamlit documentation.