# AI-Powered Salary Estimator RAG Application

An advanced salary estimation tool that uses Retrieval-Augmented Generation (RAG) and Agentic AI to analyze CVs and provide accurate salary predictions based on the Indonesia Salary Guide 2025.

## 🚀 Features

- **Smart CV Parsing**: Automatically extracts key information from uploaded CVs (PDF format)
- **RAG-Powered Search**: Semantic search through salary database using ChromaDB
- **AI Analysis**: Leverages Qwen3 model via OpenRouter for intelligent insights
- **Industry-Specific Matching**: Matches profiles to relevant industries and positions
- **Comprehensive Factors**: Considers experience, education, skills, and location
- **Interactive Dashboard**: Beautiful Streamlit interface with data visualizations
- **Career Recommendations**: Personalized advice for career advancement

## 📋 Prerequisites

- Python 3.11 or higher
- OpenRouter API key (free tier available)
- 4GB RAM minimum
- Modern web browser

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/salary-estimator-rag.git
cd salary-estimator-rag
```

2. **Create a virtual environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Copy the template
cp .env.template .env

# Edit .env and add your OpenRouter API key
# Get a free API key from: https://openrouter.ai/
```

5. **Initialize the salary database**
```bash
python -c "from src.utils import save_salary_data_to_json; from pathlib import Path; save_salary_data_to_json(Path('data'))"
```

## 🚀 Running the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 📚 Usage Guide

1. **Upload Your CV**
   - Click on "Choose your CV file" 
   - Select a PDF file (LinkedIn CV format works best)
   - Click "Analyze My CV" to parse the document

2. **Review Profile**
   - Check the extracted information
   - Verify your experience level and detected industry
   - View skills and education details

3. **Get Salary Estimation**
   - Click "Estimate My Salary"
   - Wait for AI analysis (usually 10-15 seconds)
   - Review comprehensive results

4. **Understand Results**
   - **Salary Range**: Min, average, and max monthly salary in IDR millions
   - **Match Confidence**: How well your profile matches the data
   - **Factors**: Experience, education, skills, and location multipliers
   - **Recommendations**: Personalized career advancement tips

## 🏗️ Architecture

### Core Components

1. **CV Parser** (`src/cv_parser.py`)
   - Extracts text from PDFs using PyPDF2 and pdfplumber
   - Identifies sections (experience, education, skills)
   - Detects industry and experience level

2. **RAG Engine** (`src/rag_engine.py`)
   - Manages ChromaDB vector database
   - Performs semantic search on salary data
   - Falls back to TF-IDF for reliability

3. **LLM Client** (`src/llm_client.py`)
   - Integrates with Qwen3 via OpenRouter API
   - Generates intelligent analysis and recommendations
   - Handles async/sync operations

4. **Salary Matcher** (`src/salary_matcher.py`)
   - Matches CV profiles to salary positions
   - Calculates multipliers and factors
   - Generates final estimations

### Data Flow

```
CV Upload → PDF Parsing → Profile Extraction → RAG Search → 
Position Matching → Factor Calculation → LLM Analysis → Results Display
```

## 📊 Salary Data Structure

The application uses structured salary data from the Indonesia Salary Guide 2025:

```json
{
  "industry": "Technology",
  "category": "Development",
  "job_title": "Full-stack Developer",
  "salary": 30  // in IDR millions per month
}
```

## 🔧 Configuration

Key settings in `config/settings.py`:

- **Experience Multipliers**: Adjust salary based on years of experience
- **Education Multipliers**: Factor in educational qualifications
- **Location Multipliers**: Account for regional differences
- **LLM Parameters**: Temperature, max tokens, model selection

## 🐛 Troubleshooting

### Common Issues

1. **"API Key Invalid"**
   - Ensure your OpenRouter API key is correctly set in `.env`
   - Check if the key has available credits

2. **"CV Parsing Failed"**
   - Ensure the PDF is not encrypted or corrupted
   - Try re-saving the PDF with a standard PDF viewer

3. **"No Salary Matches Found"**
   - The CV might be too brief or unclear
   - Try adding more details about job titles and skills

4. **Slow Performance**
   - First run indexes the salary database (one-time operation)
   - LLM API calls may take 5-15 seconds depending on load

## 📈 Advanced Features

### Custom Salary Data

Add your own salary data by editing `data/salary_guide_2025.json`:

```json
{
  "industry": "New Industry",
  "category": "New Category",
  "job_title": "New Position",
  "salary": 50
}
```

Then re-index the database:
```bash
python -c "from src.rag_engine import RAGEngine; engine = RAGEngine(); engine.index_salary_data()"
```

### API Rate Limits

The free OpenRouter tier has rate limits. For production use:
- Consider upgrading to a paid plan
- Implement caching for repeated queries
- Add request queuing for multiple users

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Michael Page Indonesia** for the Salary Guide 2025 data
- **OpenRouter** for providing access to Qwen3 model
- **Streamlit** for the amazing web framework
- **ChromaDB** for vector database capabilities

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the [FAQ section](#-troubleshooting)
- Contact: support@salaryestimator.ai

---

Built with ❤️ by the Michael Page, McKinsey & BCG AI Team