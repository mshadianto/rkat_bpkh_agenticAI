"""
RAG (Retrieval-Augmented Generation) Engine for Bank Muamalat Health Monitoring
"""

import os
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import numpy as np
from datetime import datetime
import logging

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader, UnstructuredExcelLoader
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.callbacks import StreamingStdOutCallbackHandler

from sentence_transformers import CrossEncoder
import chromadb
from chromadb.config import Settings

logger = logging.getLogger(__name__)

class BankMuamalatRAGEngine:
    """
    Advanced RAG engine specifically designed for Bank Muamalat analysis
    """
    
    def __init__(self, config):
        self.config = config
        self.embeddings = None
        self.vector_store = None
        self.llm = None
        self.reranker = None
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self._initialize_components()
        
    def _initialize_components(self):
        """Initialize all RAG components"""
        try:
            # Initialize embeddings
            logger.info("Initializing embeddings...")
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.config.EMBEDDING_MODEL,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            
            # Initialize vector store
            logger.info("Initializing vector store...")
            chroma_client = chromadb.PersistentClient(
                path=self.config.VECTOR_DB_PATH,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            self.vector_store = Chroma(
                client=chroma_client,
                collection_name="bank_muamalat_docs",
                embedding_function=self.embeddings
            )
            
            # Initialize LLM
            logger.info("Initializing LLM...")
            self.llm = ChatOpenAI(
                model_name=self.config.LLM_MODEL,
                temperature=self.config.TEMPERATURE,
                max_tokens=self.config.MAX_TOKENS,
                openai_api_key=self.config.OPENAI_API_KEY,
                streaming=True,
                callbacks=[StreamingStdOutCallbackHandler()]
            )
            
            # Initialize reranker for better retrieval
            logger.info("Initializing reranker...")
            self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
            
            logger.info("RAG engine initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG engine: {str(e)}")
            raise
            
    def load_documents(self, file_paths: List[str]) -> List[Document]:
        """Load documents from various sources"""
        documents = []
        
        for file_path in file_paths:
            path = Path(file_path)
            
            try:
                if path.suffix.lower() == '.pdf':
                    loader = PyPDFLoader(str(path))
                    documents.extend(loader.load())
                    
                elif path.suffix.lower() in ['.xlsx', '.xls']:
                    loader = UnstructuredExcelLoader(str(path))
                    documents.extend(loader.load())
                    
                else:
                    logger.warning(f"Unsupported file type: {path.suffix}")
                    
            except Exception as e:
                logger.error(f"Error loading {file_path}: {str(e)}")
                
        # Add metadata
        for doc in documents:
            doc.metadata.update({
                'source_type': 'annual_report',
                'bank': 'muamalat',
                'indexed_at': datetime.now().isoformat()
            })
            
        return documents
        
    def process_documents(self, documents: List[Document]) -> List[Document]:
        """Process and chunk documents"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.CHUNK_SIZE,
            chunk_overlap=self.config.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        processed_docs = []
        for doc in documents:
            chunks = text_splitter.split_documents([doc])
            
            # Add chunk metadata
            for i, chunk in enumerate(chunks):
                chunk.metadata.update({
                    'chunk_index': i,
                    'total_chunks': len(chunks),
                    'original_doc_id': doc.metadata.get('source', 'unknown')
                })
                processed_docs.append(chunk)
                
        return processed_docs
        
    def add_documents(self, documents: List[Document]):
        """Add documents to vector store"""
        try:
            self.vector_store.add_documents(documents)
            logger.info(f"Added {len(documents)} documents to vector store")
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise
            
    def semantic_search(
        self, 
        query: str, 
        k: int = None,
        filter_dict: Optional[Dict] = None
    ) -> List[Tuple[Document, float]]:
        """Perform semantic search with reranking"""
        k = k or self.config.TOP_K_RETRIEVAL
        
        # Initial retrieval
        if filter_dict:
            results = self.vector_store.similarity_search_with_score(
                query, k=k*2, filter=filter_dict
            )
        else:
            results = self.vector_store.similarity_search_with_score(
                query, k=k*2
            )
            
        # Rerank results
        if self.reranker and results:
            # Prepare texts for reranking
            texts = [doc.page_content for doc, _ in results]
            scores = self.reranker.predict([(query, text) for text in texts])
            
            # Combine with original scores
            reranked_results = []
            for i, (doc, orig_score) in enumerate(results):
                combined_score = 0.7 * scores[i] + 0.3 * (1 - orig_score)
                reranked_results.append((doc, combined_score))
                
            # Sort by combined score
            reranked_results.sort(key=lambda x: x[1], reverse=True)
            return reranked_results[:k]
            
        return results[:k]
        
    def query_with_context(
        self, 
        query: str,
        context_type: str = "general",
        filters: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Query with specific context and return structured response"""
        
        # Get relevant documents
        relevant_docs = self.semantic_search(query, filter_dict=filters)
        
        # Filter by relevance threshold
        relevant_docs = [
            (doc, score) for doc, score in relevant_docs 
            if score >= self.config.RELEVANCE_THRESHOLD
        ]
        
        if not relevant_docs:
            return {
                'answer': "No relevant information found in the knowledge base.",
                'sources': [],
                'confidence': 0.0
            }
            
        # Prepare context
        context = "\n\n".join([
            f"[Source {i+1}] {doc.page_content}" 
            for i, (doc, _) in enumerate(relevant_docs)
        ])
        
        # Get appropriate prompt template
        prompt_template = self._get_context_prompt(context_type)
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # Generate response
        chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(
                search_kwargs={"k": self.config.TOP_K_RETRIEVAL}
            ),
            chain_type_kwargs={
                "prompt": prompt,
                "memory": self.memory
            }
        )
        
        response = chain.run(query)
        
        # Calculate confidence based on relevance scores
        avg_score = np.mean([score for _, score in relevant_docs])
        confidence = min(avg_score * 100, 100)
        
        return {
            'answer': response,
            'sources': [
                {
                    'content': doc.page_content[:200] + "...",
                    'metadata': doc.metadata,
                    'relevance_score': float(score)
                }
                for doc, score in relevant_docs[:5]
            ],
            'confidence': confidence,
            'context_type': context_type
        }
        
    def _get_context_prompt(self, context_type: str) -> str:
        """Get context-specific prompt template"""
        prompts = {
            "financial": """
            You are a senior financial analyst specializing in Islamic banking.
            Use the following context to answer the question about Bank Muamalat's financial health.
            
            Context: {context}
            
            Question: {question}
            
            Provide a detailed analysis including:
            1. Key financial metrics and trends
            2. Comparison with regulatory requirements
            3. Strengths and areas of concern
            4. Specific recommendations
            
            Answer:
            """,
            
            "risk": """
            You are a risk management expert for Islamic financial institutions.
            Analyze the following information about Bank Muamalat's risk profile.
            
            Context: {context}
            
            Question: {question}
            
            Focus on:
            1. Credit risk indicators (NPF analysis)
            2. Operational risk factors
            3. Market and liquidity risks
            4. Regulatory compliance risks
            5. Risk mitigation recommendations
            
            Answer:
            """,
            
            "strategic": """
            You are a McKinsey/PwC senior consultant advising BPKH on Bank Muamalat.
            Provide strategic insights based on the following information.
            
            Context: {context}
            
            Question: {question}
            
            Your analysis should cover:
            1. Strategic positioning and market competitiveness
            2. Growth opportunities and threats
            3. Transformation recommendations
            4. Investment decision support (maintain/divest)
            5. Implementation roadmap
            
            Answer:
            """,
            
            "general": """
            Based on the following context about Bank Muamalat, answer the question comprehensively.
            
            Context: {context}
            
            Question: {question}
            
            Provide a clear, well-structured answer with supporting evidence from the context.
            
            Answer:
            """
        }
        
        return prompts.get(context_type, prompts["general"])
        
    def analyze_metrics_trend(
        self, 
        metric_name: str,
        time_period: str = "5_years"
    ) -> Dict[str, Any]:
        """Analyze specific metric trends"""
        query = f"""
        Analyze the {metric_name} trend for Bank Muamalat over the past {time_period}.
        Include historical values, trend direction, and comparison with benchmarks.
        """
        
        return self.query_with_context(
            query, 
            context_type="financial",
            filters={"metric_type": metric_name}
        )
        
    def generate_executive_summary(self) -> str:
        """Generate executive summary of bank health"""
        query = """
        Provide an executive summary of Bank Muamalat's current health status including:
        1. Overall financial performance
        2. Key risk indicators
        3. Strategic position
        4. Critical issues requiring immediate attention
        5. Recommendation for BPKH as controlling shareholder
        """
        
        result = self.query_with_context(query, context_type="strategic")
        return result['answer']
        
    def clear_memory(self):
        """Clear conversation memory"""
        self.memory.clear()
        
    def get_statistics(self) -> Dict[str, Any]:
        """Get RAG engine statistics"""
        collection = self.vector_store._collection
        stats = {
            'total_documents': collection.count(),
            'embedding_model': self.config.EMBEDDING_MODEL,
            'llm_model': self.config.LLM_MODEL,
            'vector_db_path': self.config.VECTOR_DB_PATH,
            'memory_buffer_size': len(self.memory.buffer)
        }
        return stats