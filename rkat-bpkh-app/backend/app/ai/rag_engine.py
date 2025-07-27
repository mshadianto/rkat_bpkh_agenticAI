import chromadb
from chromadb.config import Settings
import os
from typing import List, Dict, Any
import json

class RAGEngine:
    """Retrieval-Augmented Generation engine for BPKH knowledge base"""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Collections for different document types
        self.collections = {
            "regulations": self._get_or_create_collection("bpkh_regulations"),
            "kup_policies": self._get_or_create_collection("kup_policies"),
            "sbo_standards": self._get_or_create_collection("sbo_standards"),
            "templates": self._get_or_create_collection("rkat_templates"),
            "faqs": self._get_or_create_collection("bpkh_faqs")
        }
        
        # Initialize with BPKH knowledge
        self._initialize_knowledge_base()
    
    def _get_or_create_collection(self, name: str):
        """Get or create a ChromaDB collection"""
        try:
            return self.client.get_collection(name)
        except:
            return self.client.create_collection(name)
    
    def _initialize_knowledge_base(self):
        """Initialize knowledge base with BPKH documents and policies"""
        
        # KUP 2026 Knowledge
        kup_knowledge = [
            {
                "id": "kup_theme_2026",
                "content": "Tema RKAT 2026 adalah Institutional Strengthening yang berfokus pada penguatan internal dan proses bisnis untuk mendukung tata kelola yang baik.",
                "metadata": {"type": "theme", "year": 2026}
            },
            {
                "id": "kup_strategic_objectives",
                "content": "Sasaran strategis RKAT 2026: (1) Pengembangan investasi pada ekosistem haji dan umroh, (2) Amandemen peraturan untuk penguatan kelembagaan dan tata kelola BPKH.",
                "metadata": {"type": "objectives", "year": 2026}
            },
            {
                "id": "kup_budget_principles",
                "content": "Biaya operasional digunakan berdasarkan prinsip efisien, efektif, rasional dan akuntabel dengan tetap memperhatikan dukungan terhadap pencapaian target nilai manfaat, dana haji yang dikelola, perolehan calon jemaah haji baru, dan distribusi program kemaslahatan.",
                "metadata": {"type": "principles", "year": 2026}
            },
            {
                "id": "kup_required_documents",
                "content": "Rancangan usulan rencana kegiatan beserta rencana anggaran biaya pengeluaran operasional dalam RKAT Tahun 2026 harus disusun dalam rangka memenuhi IKU serta didukung dengan alasan yang logis, kuat, sesuai dengan prinsip input – process – output – outcome, kemudian dilengkapi dengan Rincian Anggaran Biaya (RAB) dan Kerangka Acuan Kerja (KAK), Action Plan, Timeline, dan Work Breakdown Structure (WBS).",
                "metadata": {"type": "requirements", "year": 2026}
            }
        ]
        
        # SBO 2026 Knowledge
        sbo_knowledge = [
            {
                "id": "sbo_honorarium_eselon1", 
                "content": "Honorarium narasumber/pembahas eksternal Eselon I (Dirjen): Rp 1.400.000 per JPL",
                "metadata": {"type": "honorarium", "level": "eselon1"}
            },
            {
                "id": "sbo_honorarium_eselon2",
                "content": "Honorarium narasumber/pembahas eksternal Eselon II: Rp 1.000.000 per JPL",
                "metadata": {"type": "honorarium", "level": "eselon2"}
            },
            {
                "id": "sbo_meeting_fullday",
                "content": "Paket meeting fullday: Rp 635.000 per orang per hari",
                "metadata": {"type": "meeting", "package": "fullday"}
            },
            {
                "id": "sbo_konsumsi_rapat",
                "content": "Konsumsi rapat: Rp 125.000 per orang",
                "metadata": {"type": "consumption", "category": "meeting"}
            }
        ]
        
        # Regulations Knowledge
        regulations_knowledge = [
            {
                "id": "uu_34_2014",
                "content": "Undang-Undang Nomor 34 Tahun 2014 tentang Pengelolaan Keuangan Haji mengatur bahwa batas maksimal pengeluaran operasional ditetapkan sebesar 5% dari nilai manfaat tahun sebelumnya.",
                "metadata": {"type": "regulation", "law": "UU 34/2014"}
            },
            {
                "id": "pp_5_2018",
                "content": "Peraturan Pemerintah Nomor 5 Tahun 2018 tentang Pelaksanaan Undang-Undang Nomor 34 Tahun 2014 tentang Pengelolaan Keuangan Haji.",
                "metadata": {"type": "regulation", "law": "PP 5/2018"}
            }
        ]
        
        # Add knowledge to collections
        self._add_documents_to_collection("kup_policies", kup_knowledge)
        self._add_documents_to_collection("sbo_standards", sbo_knowledge)
        self._add_documents_to_collection("regulations", regulations_knowledge)
    
    def _add_documents_to_collection(self, collection_name: str, documents: List[Dict]):
        """Add documents to a specific collection"""
        collection = self.collections[collection_name]
        
        # Check if documents already exist
        try:
            existing_docs = collection.get()
            existing_ids = set(existing_docs["ids"]) if existing_docs["ids"] else set()
        except:
            existing_ids = set()
        
        # Add only new documents
        new_docs = [doc for doc in documents if doc["id"] not in existing_ids]
        
        if new_docs:
            collection.add(
                documents=[doc["content"] for doc in new_docs],
                ids=[doc["id"] for doc in new_docs],
                metadatas=[doc["metadata"] for doc in new_docs]
            )
    
    def search_knowledge(self, query: str, collection_types: List[str] = None, limit: int = 5) -> List[Dict]:
        """Search knowledge base using semantic similarity"""
        
        if collection_types is None:
            collection_types = list(self.collections.keys())
        
        results = []
        
        for collection_type in collection_types:
            if collection_type in self.collections:
                collection = self.collections[collection_type]
                
                try:
                    search_results = collection.query(
                        query_texts=[query],
                        n_results=min(limit, 10)
                    )
                    
                    for i, doc in enumerate(search_results["documents"][0]):
                        results.append({
                            "content": doc,
                            "metadata": search_results["metadatas"][0][i],
                            "similarity": 1 - search_results["distances"][0][i],  # Convert distance to similarity
                            "collection": collection_type
                        })
                except Exception as e:
                    print(f"Error searching collection {collection_type}: {e}")
        
        # Sort by similarity and return top results
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:limit]
    
    def get_contextual_information(self, query: str, context_type: str = "general") -> str:
        """Get contextual information for AI responses"""
        
        # Determine which collections to search based on context
        if context_type == "kup":
            collections = ["kup_policies", "regulations"]
        elif context_type == "sbo":
            collections = ["sbo_standards"]
        elif context_type == "compliance":
            collections = ["kup_policies", "sbo_standards", "regulations"]
        else:
            collections = list(self.collections.keys())
        
        search_results = self.search_knowledge(query, collections, limit=3)
        
        if not search_results:
            return "Tidak ditemukan informasi yang relevan dalam knowledge base."
        
        context_info = "Informasi relevan dari knowledge base BPKH:\n\n"
        
        for i, result in enumerate(search_results, 1):
            context_info += f"{i}. {result['content']}\n"
            context_info += f"   (Sumber: {result['collection']}, Similarity: {result['similarity']:.2f})\n\n"
        
        return context_info
    
    def add_document(self, collection_name: str, document_id: str, content: str, metadata: Dict):
        """Add a new document to the knowledge base"""
        
        if collection_name not in self.collections:
            self.collections[collection_name] = self._get_or_create_collection(collection_name)
        
        collection = self.collections[collection_name]
        
        collection.add(
            documents=[content],
            ids=[document_id],
            metadatas=[metadata]
        )
    
    def update_document(self, collection_name: str, document_id: str, content: str, metadata: Dict):
        """Update an existing document in the knowledge base"""
        
        if collection_name in self.collections:
            collection = self.collections[collection_name]
            
            # Delete old version
            try:
                collection.delete(ids=[document_id])
            except:
                pass
            
            # Add updated version
            collection.add(
                documents=[content],
                ids=[document_id],
                metadatas=[metadata]
            )