"""Simple RAG Engine without ChromaDB dependency."""

import json
import logging
from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from pathlib import Path

from config.settings import (
    CHROMA_PERSIST_DIRECTORY,
    COLLECTION_NAME,
    SALARY_GUIDE_JSON
)
from models.schemas import SalaryData, RAGQuery, RAGResponse

logger = logging.getLogger(__name__)


class SimpleRAGEngine:
    """Simple RAG Engine using TF-IDF for semantic search."""
    
    def __init__(self):
        # Storage paths
        self.index_path = Path(CHROMA_PERSIST_DIRECTORY) / "tfidf_index.pkl"
        self.data_path = Path(CHROMA_PERSIST_DIRECTORY) / "salary_data.pkl"
        
        # Ensure directory exists
        Path(CHROMA_PERSIST_DIRECTORY).mkdir(parents=True, exist_ok=True)
        
        # Initialize TF-IDF vectorizer
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 3),
            min_df=1,
            max_df=0.95
        )
        
        # Load salary data
        self.salary_data = self._load_salary_data()
        
        # Load or create index
        self._load_or_create_index()
        
    def _load_salary_data(self) -> List[Dict[str, Any]]:
        """Load salary data from JSON file."""
        try:
            with open(SALARY_GUIDE_JSON, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Salary guide JSON not found at {SALARY_GUIDE_JSON}")
            return self._get_sample_salary_data()
        except Exception as e:
            logger.error(f"Error loading salary data: {str(e)}")
            return []
            
    def _get_sample_salary_data(self) -> List[Dict[str, Any]]:
        """Get sample salary data based on the PDF content."""
        return [
            # Technology
            {"industry": "Technology", "category": "Development", "job_title": "Front-end Developer", "salary": 20},
            {"industry": "Technology", "category": "Development", "job_title": "Back-end Developer", "salary": 25},
            {"industry": "Technology", "category": "Development", "job_title": "Full-stack Developer", "salary": 30},
            {"industry": "Technology", "category": "Development", "job_title": "Tech Lead", "salary": 40},
            {"industry": "Technology", "category": "Development", "job_title": "Engineering Manager", "salary": 67},
            {"industry": "Technology", "category": "Analytics", "job_title": "Data Analyst", "salary": 30},
            {"industry": "Technology", "category": "Analytics", "job_title": "Data Scientist", "salary": 46},
            {"industry": "Technology", "category": "Analytics", "job_title": "Data Science Manager", "salary": 72},
            
            # Accounting & Finance
            {"industry": "Accounting & Finance", "category": "Accounting", "job_title": "Senior Accountant", "salary": 25},
            {"industry": "Accounting & Finance", "category": "Accounting", "job_title": "Accounting Manager", "salary": 45},
            {"industry": "Accounting & Finance", "category": "Accounting", "job_title": "Finance Manager", "salary": 50},
            {"industry": "Accounting & Finance", "category": "Accounting", "job_title": "Financial Controller", "salary": 80},
            
            # Sales & Marketing
            {"industry": "Sales & Marketing", "category": "Consumer Products", "job_title": "Marketing Executive", "salary": 12},
            {"industry": "Sales & Marketing", "category": "Consumer Products", "job_title": "Brand Manager", "salary": 35},
            {"industry": "Sales & Marketing", "category": "Consumer Products", "job_title": "Marketing Manager", "salary": 70},
            {"industry": "Sales & Marketing", "category": "Digital", "job_title": "Digital Marketing Manager", "salary": 40},
            
            # Human Resources
            {"industry": "Human Resources", "category": "Generalist", "job_title": "HR Generalist", "salary": 21},
            {"industry": "Human Resources", "category": "Generalist", "job_title": "HR Manager", "salary": 35},
            {"industry": "Human Resources", "category": "Generalist", "job_title": "HR Business Partner", "salary": 45},
            {"industry": "Human Resources", "category": "Generalist", "job_title": "Head of HR", "salary": 100},
        ]
        
    def _load_or_create_index(self):
        """Load existing index or create new one."""
        if self.index_path.exists() and self.data_path.exists():
            try:
                # Load existing index
                with open(self.index_path, 'rb') as f:
                    index_data = pickle.load(f)
                    self.tfidf_vectorizer = index_data['vectorizer']
                    self.doc_vectors = index_data['vectors']
                    
                logger.info("Loaded existing TF-IDF index")
                return
            except Exception as e:
                logger.warning(f"Failed to load index: {str(e)}")
                
        # Create new index
        self.index_salary_data()
        
    def index_salary_data(self):
        """Index salary data using TF-IDF."""
        if not self.salary_data:
            logger.warning("No salary data to index")
            return
            
        try:
            # Create searchable texts
            documents = [self._create_searchable_text(item) for item in self.salary_data]
            
            # Fit and transform
            self.doc_vectors = self.tfidf_vectorizer.fit_transform(documents)
            
            # Save index
            index_data = {
                'vectorizer': self.tfidf_vectorizer,
                'vectors': self.doc_vectors
            }
            
            with open(self.index_path, 'wb') as f:
                pickle.dump(index_data, f)
                
            # Save salary data
            with open(self.data_path, 'wb') as f:
                pickle.dump(self.salary_data, f)
                
            logger.info(f"Indexed {len(documents)} salary records")
            
        except Exception as e:
            logger.error(f"Error indexing salary data: {str(e)}")
            
    def _create_searchable_text(self, item: Dict[str, Any]) -> str:
        """Create searchable text from salary item."""
        parts = [
            item.get("job_title", ""),
            item.get("industry", ""),
            item.get("category", ""),
            f"salary {item.get('salary', 0)} million IDR",
            self._get_job_variations(item.get("job_title", ""))
        ]
        
        return " ".join(filter(None, parts))
        
    def _get_job_variations(self, job_title: str) -> str:
        """Get variations and related terms for a job title."""
        variations = {
            "Developer": "programmer engineer coder software development coding",
            "Manager": "lead head supervisor coordinator management leader",
            "Analyst": "specialist expert consultant analysis analytics",
            "Director": "head vp vice president executive leadership",
            "Engineer": "developer specialist technical engineering",
            "Marketing": "brand digital social media advertising promotion",
            "Finance": "accounting financial controller treasury audit",
            "HR": "human resources people talent recruitment organizational",
        }
        
        result = []
        for key, values in variations.items():
            if key.lower() in job_title.lower():
                result.append(values)
                
        return " ".join(result)
        
    def search_salaries(self, query: RAGQuery) -> RAGResponse:
        """Search for relevant salary information."""
        try:
            # Prepare search query
            search_text = self._prepare_search_query(query)
            
            # Transform query
            query_vector = self.tfidf_vectorizer.transform([search_text])
            
            # Calculate similarities
            similarities = cosine_similarity(query_vector, self.doc_vectors).flatten()
            
            # Get top results
            n_results = query.context_window
            top_indices = similarities.argsort()[-n_results:][::-1]
            
            # Process results
            relevant_salaries = []
            context_snippets = []
            distances = []
            
            for idx in top_indices:
                if idx < len(self.salary_data):
                    item = self.salary_data[idx]
                    
                    salary_item = SalaryData(
                        industry=item.get("industry", "Unknown"),
                        job_title=item.get("job_title", "Unknown"),
                        average_monthly_salary_idr=int(item.get("salary", 0)),
                        category=item.get("category", "")
                    )
                    relevant_salaries.append(salary_item)
                    
                    context_snippets.append(self._create_searchable_text(item))
                    distances.append(1 - similarities[idx])
                    
            # Calculate confidence score
            confidence = self._calculate_confidence(distances, query.cv_profile)
            
            return RAGResponse(
                relevant_salaries=relevant_salaries,
                context_snippets=context_snippets,
                llm_analysis="",  # Will be filled by LLM
                confidence_score=confidence
            )
            
        except Exception as e:
            logger.error(f"Error searching salaries: {str(e)}")
            return RAGResponse(
                relevant_salaries=[],
                context_snippets=[],
                llm_analysis="Error occurred during search",
                confidence_score=0.0
            )
            
    def _prepare_search_query(self, query: RAGQuery) -> str:
        """Prepare optimized search query from CV profile."""
        parts = []
        
        # Add current title
        if query.cv_profile.current_title:
            parts.append(query.cv_profile.current_title)
            
        # Add industry
        if query.cv_profile.detected_industry:
            parts.append(query.cv_profile.detected_industry.value)
            
        # Add key skills
        if query.cv_profile.technical_skills:
            parts.extend(query.cv_profile.technical_skills[:5])
            
        # Add experience level
        parts.append(f"{query.cv_profile.experience_level.value} level")
        
        # Add any explicit query text
        if query.query_text:
            parts.append(query.query_text)
            
        return " ".join(parts)
        
    def _calculate_confidence(self, distances: List[float], cv_profile) -> float:
        """Calculate confidence score based on search results and CV profile."""
        if not distances:
            return 0.0
            
        # Base confidence on search distance
        avg_distance = np.mean(distances) if distances else 1.0
        search_confidence = max(0, 1 - avg_distance)
        
        # Boost confidence based on profile completeness
        profile_score = 0
        if cv_profile.current_title:
            profile_score += 0.2
        if cv_profile.work_experiences:
            profile_score += 0.2
        if cv_profile.education_details:
            profile_score += 0.2
        if cv_profile.technical_skills:
            profile_score += 0.2
        if cv_profile.detected_industry:
            profile_score += 0.2
            
        # Combined confidence
        confidence = (search_confidence * 0.7) + (profile_score * 0.3)
        
        return min(1.0, confidence)
        
    def get_similar_roles(self, job_title: str, industry: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get similar roles for comparison."""
        # Create query text
        search_text = f"{job_title} {industry}"
        query_vector = self.tfidf_vectorizer.transform([search_text])
        
        # Calculate similarities
        similarities = cosine_similarity(query_vector, self.doc_vectors).flatten()
        
        # Get top results
        top_indices = similarities.argsort()[-(limit * 2):][::-1]
        
        # Filter and deduplicate
        seen_titles = set()
        similar_roles = []
        
        for idx in top_indices:
            if idx < len(self.salary_data):
                item = self.salary_data[idx]
                title = item.get("job_title", "")
                
                if title and title != job_title and title not in seen_titles:
                    seen_titles.add(title)
                    similar_roles.append({
                        "title": title,
                        "industry": item.get("industry", ""),
                        "salary": int(item.get("salary", 0))
                    })
                    
                    if len(similar_roles) >= limit:
                        break
                        
        return similar_roles