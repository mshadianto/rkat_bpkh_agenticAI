"""
Embeddings module for Bank Muamalat Health Monitoring System
Supports multiple embedding models and caching
"""

import os
from typing import List, Dict, Any, Optional, Union
import numpy as np
from pathlib import Path
import pickle
import hashlib
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from sentence_transformers import SentenceTransformer
import torch

from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class EmbeddingCache:
    """Cache for embeddings to avoid recomputation"""
    
    def __init__(self, cache_dir: str, ttl_hours: int = 24):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)
        
    def _get_cache_key(self, text: str, model_name: str) -> str:
        """Generate cache key from text and model"""
        content = f"{model_name}:{text}"
        return hashlib.md5(content.encode()).hexdigest()
        
    def get(self, text: str, model_name: str) -> Optional[List[float]]:
        """Get embedding from cache"""
        cache_key = self._get_cache_key(text, model_name)
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    data = pickle.load(f)
                    
                # Check if cache is still valid
                if datetime.now() - data['timestamp'] < self.ttl:
                    return data['embedding']
                else:
                    # Cache expired, delete it
                    cache_file.unlink()
            except Exception as e:
                logger.error(f"Error loading cache: {e}")
                
        return None
        
    def set(self, text: str, model_name: str, embedding: List[float]):
        """Save embedding to cache"""
        cache_key = self._get_cache_key(text, model_name)
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        
        data = {
            'embedding': embedding,
            'timestamp': datetime.now(),
            'text_length': len(text),
            'model': model_name
        }
        
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            logger.error(f"Error saving to cache: {e}")
            
    def clear(self):
        """Clear all cache"""
        for cache_file in self.cache_dir.glob("*.pkl"):
            cache_file.unlink()
        logger.info("Embedding cache cleared")


class BaseEmbeddings(ABC):
    """Base class for embeddings"""
    
    def __init__(self, model_name: str, cache_dir: Optional[str] = None):
        self.model_name = model_name
        self.cache = EmbeddingCache(cache_dir) if cache_dir else None
        
    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple documents"""
        pass
        
    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        """Embed single query"""
        pass
        
    def _use_cache(self, texts: List[str], embed_func) -> List[List[float]]:
        """Use cache for embeddings if available"""
        if not self.cache:
            return embed_func(texts)
            
        embeddings = []
        texts_to_embed = []
        text_indices = []
        
        # Check cache
        for i, text in enumerate(texts):
            cached = self.cache.get(text, self.model_name)
            if cached:
                embeddings.append((i, cached))
            else:
                texts_to_embed.append(text)
                text_indices.append(i)
                
        # Embed uncached texts
        if texts_to_embed:
            new_embeddings = embed_func(texts_to_embed)
            
            # Save to cache and collect results
            for text, embedding, idx in zip(texts_to_embed, new_embeddings, text_indices):
                self.cache.set(text, self.model_name, embedding)
                embeddings.append((idx, embedding))
                
        # Sort by original index and return
        embeddings.sort(key=lambda x: x[0])
        return [emb for _, emb in embeddings]


class MultilingualEmbeddings(BaseEmbeddings):
    """
    Multilingual embeddings supporting Indonesian and English
    Optimized for financial documents
    """
    
    def __init__(
        self,
        model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        cache_dir: Optional[str] = None,
        device: Optional[str] = None
    ):
        super().__init__(model_name, cache_dir)
        
        # Detect device
        if device is None:
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        else:
            self.device = device
            
        # Load model
        self.model = SentenceTransformer(model_name, device=self.device)
        logger.info(f"Loaded multilingual model: {model_name} on {self.device}")
        
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed documents with preprocessing"""
        # Preprocess texts
        processed_texts = [self._preprocess_text(text) for text in texts]
        
        # Use cache
        return self._use_cache(processed_texts, self._embed_batch)
        
    def embed_query(self, text: str) -> List[float]:
        """Embed single query"""
        processed_text = self._preprocess_text(text)
        
        # Check cache
        if self.cache:
            cached = self.cache.get(processed_text, self.model_name)
            if cached:
                return cached
                
        # Compute embedding
        embedding = self.model.encode(
            processed_text,
            convert_to_tensor=False,
            normalize_embeddings=True
        ).tolist()
        
        # Cache result
        if self.cache:
            self.cache.set(processed_text, self.model_name, embedding)
            
        return embedding
        
    def _embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embed batch of texts"""
        embeddings = self.model.encode(
            texts,
            batch_size=32,
            convert_to_tensor=False,
            normalize_embeddings=True,
            show_progress_bar=len(texts) > 100
        )
        return embeddings.tolist()
        
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text for better embeddings"""
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Truncate if too long (max 512 tokens for most models)
        max_length = 512 * 4  # Approximate characters
        if len(text) > max_length:
            text = text[:max_length] + "..."
            
        return text


class FinancialEmbeddings(BaseEmbeddings):
    """
    Specialized embeddings for financial documents
    Fine-tuned for banking terminology
    """
    
    def __init__(
        self,
        base_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        cache_dir: Optional[str] = None,
        enhance_with_keywords: bool = True
    ):
        super().__init__(base_model, cache_dir)
        self.base_embeddings = HuggingFaceEmbeddings(
            model_name=base_model,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        self.enhance_with_keywords = enhance_with_keywords
        
        # Financial keywords for enhancement
        self.financial_keywords = {
            'car': ['capital adequacy ratio', 'modal', 'kecukupan modal'],
            'npf': ['non performing financing', 'pembiayaan bermasalah', 'kredit macet'],
            'roa': ['return on assets', 'imbal hasil aset', 'profitabilitas'],
            'roe': ['return on equity', 'imbal hasil ekuitas'],
            'bopo': ['biaya operasional', 'pendapatan operasional', 'efisiensi'],
            'fdr': ['financing deposit ratio', 'rasio pembiayaan', 'likuiditas']
        }
        
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed documents with financial context enhancement"""
        if self.enhance_with_keywords:
            enhanced_texts = [self._enhance_text(text) for text in texts]
        else:
            enhanced_texts = texts
            
        return self.base_embeddings.embed_documents(enhanced_texts)
        
    def embed_query(self, text: str) -> List[float]:
        """Embed query with financial context"""
        if self.enhance_with_keywords:
            enhanced_text = self._enhance_text(text)
        else:
            enhanced_text = text
            
        return self.base_embeddings.embed_query(enhanced_text)
        
    def _enhance_text(self, text: str) -> str:
        """Enhance text with financial context"""
        text_lower = text.lower()
        
        # Add relevant keywords based on content
        enhancements = []
        for key, keywords in self.financial_keywords.items():
            if key in text_lower or any(kw in text_lower for kw in keywords):
                enhancements.extend(keywords)
                
        if enhancements:
            # Add unique keywords to the end
            unique_enhancements = list(set(enhancements))
            enhanced_text = f"{text} {' '.join(unique_enhancements)}"
            return enhanced_text
            
        return text


class HybridEmbeddings:
    """
    Hybrid embeddings combining multiple models
    for better retrieval performance
    """
    
    def __init__(
        self,
        models: List[BaseEmbeddings],
        weights: Optional[List[float]] = None
    ):
        self.models = models
        self.weights = weights or [1.0 / len(models)] * len(models)
        
        assert len(self.models) == len(self.weights), "Models and weights must have same length"
        assert abs(sum(self.weights) - 1.0) < 1e-6, "Weights must sum to 1"
        
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Combine embeddings from multiple models"""
        all_embeddings = []
        
        for model, weight in zip(self.models, self.weights):
            embeddings = model.embed_documents(texts)
            weighted_embeddings = [[e * weight for e in emb] for emb in embeddings]
            all_embeddings.append(weighted_embeddings)
            
        # Combine embeddings
        combined = []
        for i in range(len(texts)):
            combined_embedding = []
            for embeddings in all_embeddings:
                combined_embedding.extend(embeddings[i])
            combined.append(combined_embedding)
            
        return combined
        
    def embed_query(self, text: str) -> List[float]:
        """Combine query embeddings from multiple models"""
        combined_embedding = []
        
        for model, weight in zip(self.models, self.weights):
            embedding = model.embed_query(text)
            weighted_embedding = [e * weight for e in embedding]
            combined_embedding.extend(weighted_embedding)
            
        return combined_embedding


def create_embeddings(
    config: Dict[str, Any],
    embedding_type: str = "multilingual"
) -> Union[BaseEmbeddings, HybridEmbeddings]:
    """
    Factory function to create embeddings based on configuration
    """
    cache_dir = config.get('CACHE_DIR', 'data/cache/embeddings')
    
    if embedding_type == "multilingual":
        return MultilingualEmbeddings(
            model_name=config.get('EMBEDDING_MODEL', 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'),
            cache_dir=cache_dir
        )
        
    elif embedding_type == "financial":
        return FinancialEmbeddings(
            base_model=config.get('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2'),
            cache_dir=cache_dir,
            enhance_with_keywords=True
        )
        
    elif embedding_type == "openai":
        return OpenAIEmbeddings(
            openai_api_key=config.get('OPENAI_API_KEY'),
            model="text-embedding-ada-002"
        )
        
    elif embedding_type == "hybrid":
        # Combine multilingual and financial embeddings
        multilingual = MultilingualEmbeddings(cache_dir=cache_dir)
        financial = FinancialEmbeddings(cache_dir=cache_dir)
        
        return HybridEmbeddings(
            models=[multilingual, financial],
            weights=[0.6, 0.4]
        )
        
    else:
        raise ValueError(f"Unknown embedding type: {embedding_type}")


def test_embeddings():
    """Test embedding models"""
    test_texts = [
        "Bank Muamalat mencatat CAR sebesar 29.42% pada tahun 2023",
        "The capital adequacy ratio meets regulatory requirements",
        "NPF meningkat menjadi 3.99% memerlukan perhatian khusus"
    ]
    
    # Test multilingual embeddings
    embeddings = MultilingualEmbeddings()
    results = embeddings.embed_documents(test_texts)
    
    print(f"Embedding dimensions: {len(results[0])}")
    print(f"Number of documents: {len(results)}")
    
    # Test similarity
    query = "capital adequacy ratio Bank Muamalat"
    query_embedding = embeddings.embed_query(query)
    
    # Calculate similarities
    for i, text in enumerate(test_texts):
        similarity = np.dot(query_embedding, results[i])
        print(f"Similarity with '{text[:50]}...': {similarity:.3f}")


if __name__ == "__main__":
    test_embeddings()