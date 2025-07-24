"""CV Parser module for extracting information from uploaded CVs."""

import re
import PyPDF2
import pdfplumber
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import logging

from models.schemas import CVProfile, EducationLevel, ExperienceLevel, Industry

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
except:
    pass

logger = logging.getLogger(__name__)


class CVParser:
    """Parser for extracting structured information from CVs."""
    
    def __init__(self):
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,9}'
        self.linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        
        # Keywords for section detection
        self.section_keywords = {
            'experience': ['experience', 'work history', 'employment', 'career', 'professional experience'],
            'education': ['education', 'academic', 'qualification', 'degree', 'university', 'college'],
            'skills': ['skills', 'competencies', 'expertise', 'technical skills', 'technologies'],
            'summary': ['summary', 'profile', 'objective', 'about', 'introduction'],
            'certifications': ['certification', 'certificates', 'training', 'courses'],
            'languages': ['languages', 'language skills'],
        }
        
        # Industry keywords mapping
        self.industry_keywords = {
            Industry.TECHNOLOGY: ['software', 'developer', 'programmer', 'engineer', 'IT', 'data', 'cloud', 'devops', 'AI', 'machine learning'],
            Industry.ACCOUNTING_FINANCE: ['accountant', 'finance', 'audit', 'tax', 'controller', 'treasury', 'financial'],
            Industry.SALES_MARKETING: ['sales', 'marketing', 'brand', 'digital marketing', 'business development', 'account manager'],
            Industry.HUMAN_RESOURCES: ['HR', 'human resources', 'recruitment', 'talent', 'people', 'organizational'],
            Industry.BANKING_FINANCIAL_SERVICES: ['bank', 'investment', 'trading', 'risk', 'compliance', 'fund'],
            Industry.ENGINEERING_MANUFACTURING: ['engineer', 'manufacturing', 'production', 'quality', 'maintenance', 'plant'],
            Industry.HEALTHCARE_LIFE_SCIENCES: ['medical', 'healthcare', 'pharmaceutical', 'clinical', 'hospital', 'doctor', 'nurse'],
        }
        
    def parse_cv(self, file_path: str) -> CVProfile:
        """Parse CV file and extract structured information."""
        try:
            # Extract text from PDF
            text = self._extract_text_from_pdf(file_path)
            
            # Create CV profile
            profile = CVProfile(raw_text=text)
            
            # Extract basic information
            profile.email = self._extract_email(text)
            profile.phone = self._extract_phone(text)
            profile.linkedin_url = self._extract_linkedin(text)
            
            # Extract sections
            sections = self._identify_sections(text)
            
            # Parse each section
            if 'summary' in sections:
                profile.summary = sections['summary']
                
            if 'experience' in sections:
                profile.work_experiences = self._parse_experience(sections['experience'])
                profile.total_experience_years = self._calculate_total_experience(profile.work_experiences)
                profile.experience_level = self._determine_experience_level(profile.total_experience_years)
                profile.current_title = self._extract_current_title(profile.work_experiences)
                
            if 'education' in sections:
                profile.education_details = self._parse_education(sections['education'])
                profile.education_level = self._determine_education_level(profile.education_details)
                
            if 'skills' in sections:
                skills = self._parse_skills(sections['skills'])
                profile.technical_skills = skills.get('technical', [])
                profile.soft_skills = skills.get('soft', [])
                
            if 'certifications' in sections:
                profile.certifications = self._parse_certifications(sections['certifications'])
                
            if 'languages' in sections:
                profile.languages = self._parse_languages(sections['languages'])
            
            # Detect industry
            industry_result = self._detect_industry(text, profile)
            profile.detected_industry = industry_result[0]
            profile.industry_confidence = industry_result[1]
            
            return profile
            
        except Exception as e:
            logger.error(f"Error parsing CV: {str(e)}")
            raise
            
    def _extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file using multiple methods."""
        text = ""
        
        # Try pdfplumber first (better for complex layouts)
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            logger.warning(f"pdfplumber failed: {str(e)}")
            
        # Fallback to PyPDF2 if needed
        if not text.strip():
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            except Exception as e:
                logger.error(f"PyPDF2 failed: {str(e)}")
                raise
                
        return text.strip()
        
    def _extract_email(self, text: str) -> Optional[str]:
        """Extract email address from text."""
        emails = re.findall(self.email_pattern, text)
        return emails[0] if emails else None
        
    def _extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number from text."""
        phones = re.findall(self.phone_pattern, text)
        return phones[0] if phones else None
        
    def _extract_linkedin(self, text: str) -> Optional[str]:
        """Extract LinkedIn URL from text."""
        linkedin_urls = re.findall(self.linkedin_pattern, text)
        return f"https://{linkedin_urls[0]}" if linkedin_urls else None
        
    def _identify_sections(self, text: str) -> Dict[str, str]:
        """Identify and extract different sections from CV text."""
        sections = {}
        lines = text.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if line is a section header
            section_found = None
            for section_type, keywords in self.section_keywords.items():
                if any(keyword in line_lower for keyword in keywords):
                    # Check if it's likely a header (short line, possibly in caps)
                    if len(line.strip()) < 50 and (line.isupper() or ':' in line):
                        section_found = section_type
                        break
                        
            if section_found:
                # Save previous section
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                    
                current_section = section_found
                current_content = []
            elif current_section:
                current_content.append(line)
                
        # Save last section
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content).strip()
            
        return sections
        
    def _parse_experience(self, experience_text: str) -> List[Dict[str, Any]]:
        """Parse work experience section."""
        experiences = []
        
        # Split by common patterns (dates, company names)
        date_pattern = r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}\b'
        
        # Simple heuristic: split by date patterns
        parts = re.split(f'({date_pattern})', experience_text)
        
        current_exp = {}
        for i, part in enumerate(parts):
            if re.match(date_pattern, part):
                # This is a date
                if 'start_date' not in current_exp:
                    current_exp['start_date'] = part
                else:
                    current_exp['end_date'] = part
            else:
                # This is content
                lines = part.strip().split('\n')
                if lines and current_exp:
                    # First line often contains company and title
                    if 'company' not in current_exp and lines[0]:
                        # Simple extraction - can be improved
                        current_exp['title'] = lines[0].strip()
                        if len(lines) > 1:
                            current_exp['company'] = lines[1].strip()
                        current_exp['description'] = '\n'.join(lines[2:]) if len(lines) > 2 else ""
                        
                        experiences.append(current_exp)
                        current_exp = {}
                        
        return experiences
        
    def _calculate_total_experience(self, experiences: List[Dict[str, Any]]) -> float:
        """Calculate total years of experience."""
        if not experiences:
            return 0
            
        # Simple calculation based on number of positions
        # More sophisticated: parse dates and calculate actual duration
        return len(experiences) * 2.5  # Rough estimate
        
    def _determine_experience_level(self, years: float) -> ExperienceLevel:
        """Determine experience level based on years."""
        if years < 2:
            return ExperienceLevel.ENTRY
        elif years < 5:
            return ExperienceLevel.JUNIOR
        elif years < 8:
            return ExperienceLevel.MID
        elif years < 12:
            return ExperienceLevel.SENIOR
        else:
            return ExperienceLevel.EXPERT
            
    def _extract_current_title(self, experiences: List[Dict[str, Any]]) -> Optional[str]:
        """Extract current job title."""
        if experiences and experiences[0].get('title'):
            return experiences[0]['title']
        return None
        
    def _parse_education(self, education_text: str) -> List[Dict[str, Any]]:
        """Parse education section."""
        education = []
        
        # Common degree patterns
        degree_patterns = [
            r'(Bachelor|B\.S\.|B\.A\.|BSc|BA)',
            r'(Master|M\.S\.|M\.A\.|MSc|MA|MBA)',
            r'(Ph\.D\.|PhD|Doctorate)',
            r'(Diploma|Associate)',
        ]
        
        lines = education_text.split('\n')
        for line in lines:
            for pattern in degree_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    education.append({
                        'degree': pattern,
                        'details': line.strip()
                    })
                    break
                    
        return education
        
    def _determine_education_level(self, education_details: List[Dict[str, Any]]) -> EducationLevel:
        """Determine highest education level."""
        if any('Ph.D' in str(edu) or 'PhD' in str(edu) for edu in education_details):
            return EducationLevel.PHD
        elif any('Master' in str(edu) or 'MBA' in str(edu) for edu in education_details):
            return EducationLevel.MASTER
        elif any('Bachelor' in str(edu) or 'B.S' in str(edu) or 'B.A' in str(edu) for edu in education_details):
            return EducationLevel.BACHELOR
        elif any('Diploma' in str(edu) for edu in education_details):
            return EducationLevel.DIPLOMA
        else:
            return EducationLevel.HIGH_SCHOOL
            
    def _parse_skills(self, skills_text: str) -> Dict[str, List[str]]:
        """Parse skills section."""
        skills = {'technical': [], 'soft': []}
        
        # Technical skill keywords
        tech_keywords = ['python', 'java', 'javascript', 'sql', 'react', 'aws', 'docker', 
                        'kubernetes', 'git', 'agile', 'scrum', 'api', 'database', 'cloud']
        
        # Soft skill keywords
        soft_keywords = ['leadership', 'communication', 'teamwork', 'problem solving', 
                        'analytical', 'creative', 'management', 'collaboration']
        
        # Extract individual skills (comma or bullet separated)
        skill_items = re.split(r'[,\n•·\-*]', skills_text.lower())
        
        for item in skill_items:
            item = item.strip()
            if len(item) > 2:  # Filter out empty or very short items
                if any(tech in item for tech in tech_keywords):
                    skills['technical'].append(item)
                elif any(soft in item for soft in soft_keywords):
                    skills['soft'].append(item)
                else:
                    # Default to technical if unclear
                    skills['technical'].append(item)
                    
        return skills
        
    def _parse_certifications(self, cert_text: str) -> List[str]:
        """Parse certifications section."""
        certs = []
        lines = cert_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and len(line) > 5:  # Filter out empty lines
                # Remove common prefixes
                line = re.sub(r'^[-•·*]\s*', '', line)
                certs.append(line)
                
        return certs
        
    def _parse_languages(self, lang_text: str) -> List[str]:
        """Parse languages section."""
        languages = []
        
        # Common language names
        common_languages = ['english', 'indonesian', 'bahasa', 'mandarin', 'chinese', 
                           'japanese', 'korean', 'french', 'german', 'spanish']
        
        lang_text_lower = lang_text.lower()
        for lang in common_languages:
            if lang in lang_text_lower:
                languages.append(lang.capitalize())
                
        return languages
        
    def _detect_industry(self, text: str, profile: CVProfile) -> Tuple[Optional[Industry], float]:
        """Detect most likely industry based on CV content."""
        text_lower = text.lower()
        industry_scores = {}
        
        # Score based on keyword matches
        for industry, keywords in self.industry_keywords.items():
            score = 0
            for keyword in keywords:
                score += text_lower.count(keyword)
                
            # Boost score if industry keyword appears in current title
            if profile.current_title:
                title_lower = profile.current_title.lower()
                for keyword in keywords:
                    if keyword in title_lower:
                        score += 5
                        
            industry_scores[industry] = score
            
        # Find industry with highest score
        if industry_scores:
            best_industry = max(industry_scores, key=industry_scores.get)
            max_score = industry_scores[best_industry]
            
            # Calculate confidence (0-1)
            total_score = sum(industry_scores.values())
            confidence = max_score / total_score if total_score > 0 else 0
            
            return best_industry, confidence
            
        return None, 0.0