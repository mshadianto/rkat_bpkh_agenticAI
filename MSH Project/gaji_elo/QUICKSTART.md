# 🚀 Quick Start Guide

Get the Salary Estimator running in 5 minutes!

## Prerequisites

- Python 3.11+ installed
- Git installed
- Web browser

## Step 1: Clone and Setup (2 minutes)

```bash
# Clone the repository
git clone <repository-url>
cd salary-estimator-rag

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Configure API Key (1 minute)

1. Get a FREE OpenRouter API key:
   - Go to https://openrouter.ai/
   - Sign up (it's free)
   - Go to Dashboard → API Keys
   - Create new key

2. Add key to project:
```bash
# Run initialization script
python init_project.py

# Edit .env file and add your key
# Replace 'your_openrouter_api_key_here' with actual key
```

## Step 3: Run the Application (1 minute)

```bash
streamlit run app.py
```

Your browser will open automatically to http://localhost:8501

## Step 4: Test with Sample CV (1 minute)

Don't have a CV ready? No problem! Here's a quick test:

1. Create a simple text file named `test_cv.pdf` with:
```
John Doe
Email: john.doe@email.com
Phone: +62 812 3456 7890
Location: Jakarta, Indonesia

EXPERIENCE
Senior Software Engineer - Tech Corp Indonesia (2020-Present)
- Lead development of microservices architecture
- Manage team of 5 developers
- Implement CI/CD pipelines

Software Engineer - StartupXYZ (2018-2020)
- Developed REST APIs using Python/Django
- Worked with React for frontend development

EDUCATION
Bachelor of Computer Science - University of Indonesia (2014-2018)

SKILLS
Technical: Python, JavaScript, React, Django, AWS, Docker, Kubernetes
Soft Skills: Leadership, Communication, Problem Solving
```

2. Save as PDF (use any online text-to-PDF converter)

3. Upload in the application!

## Expected Results

For the sample CV above, you should see:
- **Detected Industry**: Technology
- **Experience Level**: Senior (5+ years)
- **Estimated Salary Range**: IDR 35-65 million/month
- **Best Match**: Senior Software Engineer positions

## Troubleshooting

### "API Key Invalid"
- Double-check your API key in `.env`
- Make sure there are no extra spaces
- Try generating a new key

### "Cannot parse CV"
- Ensure PDF is not password-protected
- Try a simpler PDF without complex formatting
- Use LinkedIn's "Save as PDF" feature

### Application won't start
- Make sure port 8501 is not in use
- Try: `streamlit run app.py --server.port 8502`

## Next Steps

1. **Upload your real CV** for accurate estimates
2. **Explore the visualizations** and insights
3. **Read the recommendations** for career growth
4. **Export results** for future reference

## Need Help?

- Check the full README.md
- Open an issue on GitHub
- Review the troubleshooting guide

---

**Pro Tip**: For best results, use a detailed CV with clear job titles, complete work history, and comprehensive skills list!