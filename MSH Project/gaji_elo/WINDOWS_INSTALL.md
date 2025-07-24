# Windows Installation Guide

This guide addresses the ONNX runtime DLL error on Windows and provides a clean installation process.

## Prerequisites

- Windows 10/11
- Python 3.11 installed
- Git Bash or Command Prompt
- Visual Studio Code (recommended)

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd salary-estimator-rag
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate
```

### 3. Install Dependencies (Fixed for Windows)

```bash
# Install core dependencies first
pip install numpy==1.26.3 scikit-learn==1.4.0

# Install all requirements (ChromaDB removed)
pip install -r requirements.txt
```

### 4. Initialize the Project

```bash
python init_project.py
```

### 5. Configure API Key

1. Open `.env` file in your editor
2. Replace `your_openrouter_api_key_here` with your actual OpenRouter API key
3. Get a free key from: https://openrouter.ai/

### 6. Run the Application

```bash
streamlit run app.py
```

## Troubleshooting

### If you still get ONNX runtime errors:

1. **Option 1: Clean Installation**
```bash
# Deactivate and delete virtual environment
deactivate
rmdir /s venv

# Recreate and reinstall
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. **Option 2: Install Visual C++ Redistributable**
- Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe
- Install and restart your computer

3. **Option 3: Use the fix script**
```bash
# Run the Windows fix script
fix_windows_install.bat
```

### Common Issues

**"Module not found" errors**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate
```

**"Port already in use"**
```bash
# Use a different port
streamlit run app.py --server.port 8502
```

**PDF parsing fails**
- Ensure PDF is not password protected
- Try re-saving the PDF with Adobe Reader

## Testing the Installation

1. Create a simple test CV:
```
Name: Test User
Email: test@example.com
Experience: Software Developer at Tech Company (2020-2024)
Skills: Python, JavaScript, React
Education: Bachelor in Computer Science
```

2. Save as PDF and upload to the application

3. You should see:
   - Detected industry: Technology
   - Estimated salary range
   - Match confidence percentage

## Performance Tips

- First run will be slower as it indexes the salary data
- Subsequent runs will be much faster
- The TF-IDF based search is lightweight and fast

## What We Changed

To fix the Windows ONNX runtime issue, we:

1. **Removed ChromaDB** - It requires ONNX runtime which has DLL issues on Windows
2. **Created SimpleRAGEngine** - Uses pure Python TF-IDF for semantic search
3. **Simplified dependencies** - Removed heavy ML libraries
4. **Maintained functionality** - All features still work, just using different backend

The application now uses a lightweight, pure-Python approach that works reliably on Windows without complex dependencies.

## Need Help?

- Check the main README.md
- Open an issue on GitHub
- The application works best with LinkedIn-exported CVs