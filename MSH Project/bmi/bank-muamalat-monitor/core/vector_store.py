"""
Vector Store implementation for Bank Muamalat RAG system
"""

import os
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import json
import pickle
from datetime import datetime
import numpy as np

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import faiss
from langchain.vectorstores import Chroma, FAISS
from langchain.schema import Document
from langchain.embeddings.base import Embeddings

from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class HybridVectorStore:
    """
    Hybrid vector store using both ChromaDB and FAISS for optimal performance
    ChromaDB for metadata filtering and persistence
    FAISS for fast similarity search
    """
    
    def __init__(
        self,
        embeddings: Embeddings,
        persist_directory: str,
        collection_name: str = "bank_muamalat_docs"
    ):
        self.embeddings = embeddings
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        self.collection_name = collection_name
        
        # Initialize ChromaDB
        self._init_chromadb()
        
        # Initialize FAISS
        self._init_faiss()
        
        # Metadata index
        self.metadata_index = {}
        self._load_metadata_index()
        
    def _init_chromadb(self):
        """Initialize ChromaDB client and collection"""
        self.chroma_client = chromadb.PersistentClient(
            path=str(self.persist_directory / "chroma"),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create collection
        try:
            self.chroma_collection = self.chroma_client.get_collection(
                name=self.collection_name
            )
            logger.info(f"Loaded existing ChromaDB collection: {self.collection_name}")
        except:
            self.chroma_collection = self.chroma_client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"Created new ChromaDB collection: {self.collection_name}")
            
    def _init_faiss(self):
        """Initialize FAISS index"""
        self.faiss_index_path = self.persist_directory / "faiss" / "index.faiss"
        self.faiss_index_path.parent.mkdir(exist_ok=True)
        
        if self.faiss_index_path.exists():
            self.faiss_index = faiss.read_index(str(self.faiss_index_path))
            logger.info("Loaded existing FAISS index")
        else:
            # Initialize with dummy dimension, will be updated on first add
            self.faiss_index = None
            logger.info("FAISS index will be created on first document add")
            
    def add_documents(
        self,
        documents: List[Document],
        batch_size: int = 100
    ) -> List[str]:
        """Add documents to both vector stores"""
        logger.info(f"Adding {len(documents)} documents to vector store")
        
        all_ids = []
        
        # Process in batches
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            ids = self._add_batch(batch)
            all_ids.extend(ids)
            logger.info(f"Processed batch {i//batch_size + 1}/{len(documents)//batch_size + 1}")
            
        # Save indices
        self._save_indices()
        
        return all_ids
        
    def _add_batch(self, documents: List[Document]) -> List[str]:
        """Add a batch of documents"""
        # Generate embeddings
        texts = [doc.page_content for doc in documents]
        embeddings = self.embeddings.embed_documents(texts)
        
        # Generate IDs
        ids = [self._generate_doc_id(doc) for doc in documents]
        
        # Prepare metadata
        metadatas = []
        for doc in documents:
            metadata = doc.metadata.copy()
            metadata['added_at'] = datetime.now().isoformat()
            metadata['content_hash'] = self._hash_content(doc.page_content)
            metadatas.append(metadata)
            
        # Add to ChromaDB
        self.chroma_collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        # Add to FAISS
        self._add_to_faiss(embeddings, ids)
        
        # Update metadata index
        for id_, metadata in zip(ids, metadatas):
            self.metadata_index[id_] = metadata
            
        return ids
        
    def _add_to_faiss(self, embeddings: List[List[float]], ids: List[str]):
        """Add embeddings to FAISS index"""
        embeddings_array = np.array(embeddings).astype('float32')
        
        if self.faiss_index is None:
            # Create index on first add
            dimension = embeddings_array.shape[1]
            self.faiss_index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
            logger.info(f"Created FAISS index with dimension {dimension}")
            
        self.faiss_index.add(embeddings_array)
        
    def similarity_search(
        self,
        query: str,
        k: int = 10,
        filter: Optional[Dict[str, Any]] = None,
        threshold: float = 0.7
    ) -> List[Tuple[Document, float]]:
        """Perform similarity search"""
        # Get query embedding
        query_embedding = self.embeddings.embed_query(query)
        
        if filter:
            # Use ChromaDB for filtered search
            results = self._chromadb_search(query_embedding, k, filter)
        else:
            # Use FAISS for fast unfiltered search
            results = self._faiss_search(query_embedding, k)
            
        # Filter by threshold
        filtered_results = [
            (doc, score) for doc, score in results
            if score >= threshold
        ]
        
        return filtered_results
        
    def _chromadb_search(
        self,
        query_embedding: List[float],
        k: int,
        filter: Dict[str, Any]
    ) -> List[Tuple[Document, float]]:
        """Search using ChromaDB with metadata filtering"""
        results = self.chroma_collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where=filter
        )
        
        documents = []
        for i in range(len(results['documents'][0])):
            doc = Document(
                page_content=results['documents'][0][i],
                metadata=results['metadatas'][0][i]
            )
            score = 1 - results['distances'][0][i]  # Convert distance to similarity
            documents.append((doc, score))
            
        return documents
        
    def _faiss_search(
        self,
        query_embedding: List[float],
        k: int
    ) -> List[Tuple[Document, float]]:
        """Fast search using FAISS"""
        if self.faiss_index is None or self.faiss_index.ntotal == 0:
            return []
            
        query_array = np.array([query_embedding]).astype('float32')
        
        # Search
        scores, indices = self.faiss_index.search(query_array, min(k, self.faiss_index.ntotal))
        
        # Retrieve documents from ChromaDB using indices
        documents = []
        for idx, score in zip(indices[0], scores[0]):
            if idx >= 0:  # FAISS returns -1 for empty results
                # Get document from ChromaDB
                # This is simplified - in production, maintain an index mapping
                doc_data = self._get_document_by_index(idx)
                if doc_data:
                    doc = Document(
                        page_content=doc_data['content'],
                        metadata=doc_data['metadata']
                    )
                    documents.append((doc, float(score)))
                    
        return documents
        
    def _get_document_by_index(self, idx: int) -> Optional[Dict[str, Any]]:
        """Retrieve document by FAISS index"""
        # This is a simplified implementation
        # In production, maintain a mapping between FAISS indices and document IDs
        all_docs = self.chroma_collection.get()
        if idx < len(all_docs['documents']):
            return {
                'content': all_docs['documents'][idx],
                'metadata': all_docs['metadatas'][idx]
            }
        return None
        
    def update_document(self, doc_id: str, document: Document):
        """Update an existing document"""
        # Delete old version
        self.delete_documents([doc_id])
        
        # Add new version
        self.add_documents([document])
        
    def delete_documents(self, doc_ids: List[str]):
        """Delete documents by IDs"""
        # Delete from ChromaDB
        self.chroma_collection.delete(ids=doc_ids)
        
        # Remove from metadata index
        for doc_id in doc_ids:
            self.metadata_index.pop(doc_id, None)
            
        # Note: FAISS doesn't support deletion, would need to rebuild index
        logger.warning("FAISS index not updated after deletion. Consider rebuilding.")
        
    def get_document_count(self) -> int:
        """Get total number of documents"""
        return self.chroma_collection.count()
        
    def _generate_doc_id(self, document: Document) -> str:
        """Generate unique document ID"""
        import hashlib
        content_hash = hashlib.md5(document.page_content.encode()).hexdigest()[:8]
        source = document.metadata.get('source', 'unknown')
        return f"{source}_{content_hash}"
        
    def _hash_content(self, content: str) -> str:
        """Generate content hash"""
        import hashlib
        return hashlib.sha256(content.encode()).hexdigest()
        
    def _save_indices(self):
        """Save FAISS index and metadata"""
        # Save FAISS index
        if self.faiss_index is not None:
            faiss.write_index(self.faiss_index, str(self.faiss_index_path))
            
        # Save metadata index
        metadata_path = self.persist_directory / "metadata_index.json"
        with open(metadata_path, 'w') as f:
            json.dump(self.metadata_index, f)
            
    def _load_metadata_index(self):
        """Load metadata index"""
        metadata_path = self.persist_directory / "metadata_index.json"
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                self.metadata_index = json.load(f)
                
    def clear(self):
        """Clear all data"""
        # Clear ChromaDB
        self.chroma_client.delete_collection(self.collection_name)
        self._init_chromadb()
        
        # Clear FAISS
        self.faiss_index = None
        if self.faiss_index_path.exists():
            self.faiss_index_path.unlink()
            
        # Clear metadata
        self.metadata_index = {}
        
        logger.info("Vector store cleared")
        
    def get_statistics(self) -> Dict[str, Any]:
        """Get vector store statistics"""
        stats = {
            'total_documents': self.get_document_count(),
            'chroma_collection': self.collection_name,
            'faiss_index_size': self.faiss_index.ntotal if self.faiss_index else 0,
            'metadata_entries': len(self.metadata_index),
            'storage_path': str(self.persist_directory)
        }
        
        # Get storage size
        total_size = 0
        for path in self.persist_directory.rglob('*'):
            if path.is_file():
                total_size += path.stat().st_size
                
        stats['storage_size_mb'] = round(total_size / (1024 * 1024), 2)
        
        return stats


class BankMuamalatVectorStore(HybridVectorStore):
    """
    Specialized vector store for Bank Muamalat documents
    with custom preprocessing and metadata handling
    """
    
    def __init__(self, embeddings: Embeddings, persist_directory: str):
        super().__init__(
            embeddings=embeddings,
            persist_directory=persist_directory,
            collection_name="bank_muamalat_specialized"
        )
        
    def add_annual_report(
        self,
        document: Document,
        year: int,
        report_type: str = "annual"
    ) -> List[str]:
        """Add annual report with enhanced metadata"""
        # Enhance metadata
        document.metadata.update({
            'document_type': 'annual_report',
            'report_type': report_type,
            'year': year,
            'bank': 'muamalat',
            'source_type': 'official'
        })
        
        # Add document
        return self.add_documents([document])
        
    def search_by_metric(
        self,
        metric_name: str,
        time_period: Optional[str] = None,
        k: int = 5
    ) -> List[Tuple[Document, float]]:
        """Search for specific financial metrics"""
        query = f"Bank Muamalat {metric_name}"
        
        if time_period:
            query += f" {time_period}"
            
        filter_dict = {
            'document_type': 'annual_report',
            'bank': 'muamalat'
        }
        
        return self.similarity_search(query, k=k, filter=filter_dict)
        
    def get_documents_by_year(self, year: int) -> List[Document]:
        """Get all documents for a specific year"""
        results = self.chroma_collection.get(
            where={'year': year}
        )
        
        documents = []
        for i in range(len(results['documents'])):
            doc = Document(
                page_content=results['documents'][i],
                metadata=results['metadatas'][i]
            )
            documents.append(doc)
            
        return documents