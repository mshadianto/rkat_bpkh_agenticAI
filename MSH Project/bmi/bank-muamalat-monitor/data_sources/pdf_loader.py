"""PDF Loader for Bank Muamalat documents"""

import os
from typing import List, Dict, Any
from pathlib import Path
import logging
from pypdf import PdfReader
from langchain.schema import Document
import re

logger = logging.getLogger(__name__)

class PDFLoader:
    def __init__(self, extract_tables: bool = True, extract_images: bool = False):
        self.extract_tables = extract_tables
        self.extract_images = extract_images
        
    def load(self, file_path: str) -> List[Document]:
        """Load PDF and return documents"""
        try:
            reader = PdfReader(file_path)
            documents = []
            
            metadata = self._extract_metadata(reader, file_path)
            
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                
                if self._is_relevant_content(text):
                    doc_metadata = {
                        **metadata,
                        'page': page_num + 1,
                        'total_pages': len(reader.pages)
                    }
                    
                    # Extract financial data if present
                    financial_data = self._extract_financial_data(text)
                    if financial_data:
                        doc_metadata['financial_metrics'] = financial_data
                    
                    documents.append(
                        Document(
                            page_content=self._clean_text(text),
                            metadata=doc_metadata
                        )
                    )
                    
            logger.info(f"Loaded {len(documents)} pages from {file_path}")
            return documents
            
        except Exception as e:
            logger.error(f"Error loading PDF {file_path}: {str(e)}")
            return []
    
    def load_directory(self, directory_path: str) -> List[Document]:
        """Load all PDFs from directory"""
        documents = []
        path = Path(directory_path)
        
        for pdf_file in path.glob("*.pdf"):
            documents.extend(self.load(str(pdf_file)))
            
        return documents
    
    def _extract_metadata(self, reader: PdfReader, file_path: str) -> Dict[str, Any]:
        """Extract PDF metadata"""
        metadata = {
            'source': file_path,
            'filename': os.path.basename(file_path),
            'type': 'pdf'
        }
        
        if reader.metadata:
            metadata.update({
                'title': getattr(reader.metadata, 'title', None),
                'author': getattr(reader.metadata, 'author', None),
                'creation_date': str(getattr(reader.metadata, 'creation_date', None))
            })
            
        # Extract year from filename
        year_match = re.search(r'20\d{2}', metadata['filename'])
        if year_match:
            metadata['year'] = int(year_match.group())
            
        return metadata
    
    def _is_relevant_content(self, text: str) -> bool:
        """Check if page contains relevant content"""
        if len(text.strip()) < 100:
            return False
            
        irrelevant_patterns = [
            r'^table of contents',
            r'^daftar isi',
            r'^halaman ini sengaja dikosongkan'
        ]
        
        text_lower = text.lower().strip()
        return not any(re.match(pattern, text_lower) for pattern in irrelevant_patterns)
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove page numbers
        text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)
        # Remove headers/footers
        text = re.sub(r'PT Bank Muamalat Indonesia Tbk.*?Annual Report', '', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    def _extract_financial_data(self, text: str) -> Dict[str, float]:
        """Extract financial metrics from text"""
        metrics = {}
        
        patterns = {
            'car': r'CAR\s*[:=]\s*([\d,]+\.?\d*)\s*%',
            'npf': r'NPF\s*[:=]\s*([\d,]+\.?\d*)\s*%',
            'roa': r'ROA\s*[:=]\s*([\d,]+\.?\d*)\s*%',
            'roe': r'ROE\s*[:=]\s*([\d,]+\.?\d*)\s*%',
            'bopo': r'BOPO\s*[:=]\s*([\d,]+\.?\d*)\s*%',
            'fdr': r'FDR\s*[:=]\s*([\d,]+\.?\d*)\s*%',
            'total_aset': r'Total\s+Aset\s*[:=]\s*Rp\s*([\d,]+)',
            'laba_bersih': r'Laba\s+Bersih\s*[:=]\s*Rp\s*([\d,]+)'
        }
        
        for metric, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = match.group(1).replace(',', '')
                try:
                    metrics[metric] = float(value)
                except ValueError:
                    pass
                    
        return metrics