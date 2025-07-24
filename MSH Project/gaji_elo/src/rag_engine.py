"""RAG Engine for semantic search and retrieval of salary information."""

import json
import logging
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import hashlib

from config.settings import (
    CHROMA_PERSIST_DIRECTORY,
    COLLECTION_NAME,
    SALARY_GUIDE_JSON
)
from models.schemas import SalaryData, RAGQuery, RAGResponse

logger = logging.getLogger(__name__)


class SimpleEmbeddingFunction(embedding_functions.EmbeddingFunction):
    """Simple embedding function using TF-IDF to avoid ONNX dependency."""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
        self.is_fitted = False
        
    def __call__(self, input: List[str]) -> List[List[float]]:
        """Generate embeddings for input texts."""
        if not self.is_fitted and len(input) > 0:
            # Fit on first call
            self.vectorizer.fit(input)
            self.is_fitted = True
            
        # Transform to embeddings
        if self.is_fitted:
            embeddings = self.vectorizer.transform(input).toarray()
            return embeddings.tolist()
        else:
            # Return random embeddings if not fitted (for single doc)
            # Use hash for consistency
            embeddings = []
            for text in input:
                hash_obj = hashlib.md5(text.encode())
                hash_hex = hash_obj.hexdigest()
                # Convert hash to float array
                embedding = [int(hash_hex[i:i+2], 16) / 255.0 for i in range(0, 32, 2)]
                # Pad to 500 dimensions
                embedding.extend([0.0] * (500 - len(embedding)))
                embeddings.append(embedding)
            return embeddings


class RAGEngine:
    """RAG Engine for salary data retrieval and matching."""
    
    def __init__(self):
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=CHROMA_PERSIST_DIRECTORY,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Create custom embedding function
        self.embedding_function = SimpleEmbeddingFunction()
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(
                name=COLLECTION_NAME,
                embedding_function=self.embedding_function
            )
            logger.info(f"Loaded existing collection: {COLLECTION_NAME}")
        except:
            self.collection = self.client.create_collection(
                name=COLLECTION_NAME,
                embedding_function=self.embedding_function,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"Created new collection: {COLLECTION_NAME}")
            
        # Load salary data
        self.salary_data = self._load_salary_data()
        
        # Initialize TF-IDF vectorizer for fallback
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Fit vectorizer if we have data
        if self.salary_data:
            texts = [self._create_searchable_text(item) for item in self.salary_data]
            self.tfidf_vectorizer.fit(texts)
            
    def _load_salary_data(self) -> List[Dict[str, Any]]:
        """Load salary data from JSON file."""
        try:
            with open(SALARY_GUIDE_JSON, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Salary guide JSON not found at {SALARY_GUIDE_JSON}")
            # Return sample data for demonstration
            return self._get_sample_salary_data()
        except Exception as e:
            logger.error(f"Error loading salary data: {str(e)}")
            return []
            
    def _get_sample_salary_data(self) -> List[Dict[str, Any]]:
        """Get sample salary data based on the PDF content."""
        # This is a subset of the data from the salary guide
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
        
    def index_salary_data(self):
        """Index salary data into ChromaDB."""
        if not self.salary_data:
            logger.warning("No salary data to index")
            return
            
        try:
            # Prepare documents for indexing
            documents = []
            metadatas = []
            ids = []
            
            for idx, item in enumerate(self.salary_data):
                # Create searchable text
                doc_text = self._create_searchable_text(item)
                documents.append(doc_text)
                
                # Prepare metadata
                metadatas.append({
                    "industry": item.get("industry", ""),
                    "category": item.get("category", ""),
                    "job_title": item.get("job_title", ""),
                    "salary": str(item.get("salary", 0))
                })
                
                ids.append(f"salary_{idx}")
                
            # Add to collection
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
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
            # Add variations and related terms
            self._get_job_variations(item.get("job_title", ""))
        ]
        
        return " ".join(filter(None, parts))
        
    def _get_job_variations(self, job_title: str) -> str:
        """Get variations and related terms for a job title."""
        variations = {
            "Developer": "programmer engineer coder software",
            "Manager": "lead head supervisor coordinator",
            "Analyst": "specialist expert consultant",
            "Director": "head vp vice president executive",
            "Engineer": "developer specialist technical",
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
            
            # Search in ChromaDB
            results = self.collection.query(
                query_texts=[search_text],
                n_results=query.context_window,
                include=["documents", "metadatas", "distances"]
            )
            
            # If no results from ChromaDB, use TF-IDF fallback
            if not results["documents"][0]:
                logger.info("No ChromaDB results, using TF-IDF fallback")
                results = self._tfidf_search(search_text, query.context_window)
                
            # Process results
            relevant_salaries = []
            context_snippets = []
            
            for idx, (doc, metadata) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
                salary_item = SalaryData(
                    industry=metadata.get("industry", "Unknown"),
                    job_title=metadata.get("job_title", "Unknown"),
                    average_monthly_salary_idr=int(metadata.get("salary", 0)),
                    category=metadata.get("category", "")
                )
                relevant_salaries.append(salary_item)
                context_snippets.append(doc)
                
            # Calculate confidence score
            confidence = self._calculate_confidence(
                results["distances"][0] if "distances" in results else [],
                query.cv_profile
            )
            
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
        
    def _tfidf_search(self, query: str, n_results: int) -> Dict[str, List]:
        """Fallback TF-IDF based search."""
        if not self.salary_data:
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
            
        # Transform query
        query_vec = self.tfidf_vectorizer.transform([query])
        
        # Transform all documents
        docs = [self._create_searchable_text(item) for item in self.salary_data]
        doc_vecs = self.tfidf_vectorizer.transform(docs)
        
        # Calculate similarities
        similarities = cosine_similarity(query_vec, doc_vecs).flatten()
        
        # Get top results
        top_indices = similarities.argsort()[-n_results:][::-1]
        
        # Format results
        documents = []
        metadatas = []
        distances = []
        
        for idx in top_indices:
            item = self.salary_data[idx]
            documents.append(self._create_searchable_text(item))
            metadatas.append({
                "industry": item.get("industry", ""),
                "category": item.get("category", ""),
                "job_title": item.get("job_title", ""),
                "salary": str(item.get("salary", 0))
            })
            distances.append(1 - similarities[idx])  # Convert similarity to distance
            
        return {
            "documents": [documents],
            "metadatas": [metadatas],
            "distances": [distances]
        }
        
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
        # Search for similar roles
        search_text = f"{job_title} {industry}"
        
        results = self.collection.query(
            query_texts=[search_text],
            n_results=limit * 2,  # Get more to filter
            include=["metadatas"]
        )
        
        # Filter and deduplicate
        seen_titles = set()
        similar_roles = []
        
        for metadata in results["metadatas"][0]:
            title = metadata.get("job_title", "")
            if title and title != job_title and title not in seen_titles:
                seen_titles.add(title)
                similar_roles.append({
                    "title": title,
                    "industry": metadata.get("industry", ""),
                    "salary": int(metadata.get("salary", 0))
                })
                
                if len(similar_roles) >= limit:
                    break
                    
        return similar_roles