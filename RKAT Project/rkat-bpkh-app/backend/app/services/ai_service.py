import httpx
import json
from typing import Dict, List, Any, Optional
from app.config import settings
from app.models.rkat import RKAT, RKATActivity
from sqlalchemy.orm import Session

class AIService:
    """AI service using Qwen3 via OpenRouter for RKAT assistance"""
    
    def __init__(self):
        self.api_key = settings.openrouter_api_key
        self.base_url = settings.openrouter_base_url
        self.model = settings.model_name
        self.client = httpx.AsyncClient()
    
    async def process_query(self, query: str, user_context: Dict, additional_context: Dict = None) -> str:
        """Process natural language query about RKAT"""
        
        # Build context-aware prompt
        system_prompt = self._build_system_prompt(user_context)
        user_prompt = self._build_user_prompt(query, additional_context)
        
        try:
            response = await self._call_ai_api(system_prompt, user_prompt)
            return response
        except Exception as e:
            return f"Maaf, terjadi error dalam memproses query: {str(e)}"
    
    async def generate_budget_scenarios(self, base_budget: float, parameters: Dict, scenario_count: int = 3) -> List[Dict]:
        """Generate multiple budget scenarios using AI"""
        
        system_prompt = """Anda adalah expert budget planning untuk BPKH. 
        Buat beberapa skenario anggaran yang realistis berdasarkan parameter yang diberikan.
        
        Berikan output dalam format JSON dengan struktur:
        [
            {
                "name": "Nama skenario",
                "total_budget": angka,
                "operational_budget": angka,
                "personnel_budget": angka,
                "assumptions": ["asumsi1", "asumsi2"],
                "risks": ["risiko1", "risiko2"],
                "description": "penjelasan skenario"
            }
        ]"""
        
        user_prompt = f"""
        Buat {scenario_count} skenario anggaran BPKH berdasarkan data berikut:
        
        Anggaran Dasar: Rp {base_budget:,.0f}
        Tingkat Inflasi: {parameters.get('inflation_rate', 3.5)}%
        Target Pertumbuhan: {parameters.get('growth_target', 5.0)}%
        Tingkat Risiko: {parameters.get('risk_level', 'Moderate')}
        Area Fokus: {', '.join(parameters.get('focus_areas', []))}
        
        Pertimbangkan:
        1. Batas maksimal operasional 5% dari nilai manfaat
        2. Kepatuhan dengan SBO BPKH 2026
        3. Tema "Institutional Strengthening"
        4. Efisiensi dan efektivitas anggaran
        
        Berikan skenario optimistic, realistic, dan conservative.
        """
        
        try:
            response = await self._call_ai_api(system_prompt, user_prompt)
            
            # Parse JSON response
            scenarios = json.loads(response)
            return scenarios
        
        except json.JSONDecodeError:
            # Fallback scenarios if JSON parsing fails
            return self._generate_fallback_scenarios(base_budget, parameters)
        except Exception as e:
            return [{"error": f"Failed to generate scenarios: {str(e)}"}]
    
    async def optimize_rkat_budget(self, rkat_id: int, goals: List[str], db: Session) -> Dict:
        """AI-powered budget optimization for RKAT"""
        
        # Get RKAT data
        rkat = db.query(RKAT).filter(RKAT.id == rkat_id).first()
        if not rkat:
            return {"error": "RKAT not found"}
        
        activities = db.query(RKATActivity).filter(RKATActivity.rkat_id == rkat_id).all()
        
        system_prompt = """Anda adalah expert optimization untuk anggaran BPKH.
        Analisis RKAT dan berikan rekomendasi optimasi yang spesifik dan actionable.
        
        Berikan output dalam format JSON:
        {
            "current_analysis": {
                "total_budget": angka,
                "efficiency_score": angka_0_100,
                "issues": ["masalah1", "masalah2"]
            },
            "optimizations": [
                {
                    "category": "kategori optimasi",
                    "recommendation": "rekomendasi spesifik",
                    "potential_savings": angka,
                    "implementation_difficulty": "Low/Medium/High",
                    "priority": "High/Medium/Low"
                }
            ],
            "optimized_budget": {
                "total_budget": angka,
                "operational_budget": angka,
                "personnel_budget": angka,
                "savings_amount": angka,
                "savings_percentage": angka
            }
        }"""
        
        activities_data = [
            {
                "code": a.activity_code,
                "name": a.activity_name,
                "budget": a.budget_amount,
                "sbo_reference": a.sbo_reference
            }
            for a in activities
        ]
        
        user_prompt = f"""
        Optimasi RKAT berikut:
        
        RKAT: {rkat.title}
        Total Budget: Rp {rkat.total_budget:,.0f}
        Operational: Rp {rkat.operational_budget:,.0f}
        Personnel: Rp {rkat.personnel_budget:,.0f}
        
        Kegiatan:
        {json.dumps(activities_data, indent=2)}
        
        Tujuan Optimasi: {', '.join(goals)}
        
        Berikan rekomendasi optimasi yang:
        1. Sesuai dengan SBO BPKH 2026
        2. Mempertahankan efektivitas program
        3. Meningkatkan compliance KUP
        4. Actionable dan implementable
        """
        
        try:
            response = await self._call_ai_api(system_prompt, user_prompt)
            return json.loads(response)
        except Exception as e:
            return {"error": f"Failed to optimize budget: {str(e)}"}
    
    async def generate_compliance_suggestions(self, rkat_id: int, db: Session) -> Dict:
        """Generate AI suggestions for improving compliance"""
        
        # Get RKAT data
        rkat = db.query(RKAT).filter(RKAT.id == rkat_id).first()
        if not rkat:
            return {"error": "RKAT not found"}
        
        # Get compliance scores
        from app.services.kup_service import KUPService
        from app.services.sbo_service import SBOService
        
        kup_service = KUPService()
        sbo_service = SBOService()
        
        kup_compliance = kup_service.validate_rkat_compliance(rkat)
        sbo_score = sbo_service.calculate_compliance_score(rkat)
        
        system_prompt = """Anda adalah compliance expert untuk BPKH.
        Berikan saran spesifik untuk meningkatkan kepatuhan KUP dan SBO.
        
        Format output JSON:
        {
            "kup_suggestions": [
                {
                    "issue": "masalah kepatuhan",
                    "recommendation": "saran perbaikan",
                    "priority": "High/Medium/Low",
                    "effort": "Low/Medium/High"
                }
            ],
            "sbo_suggestions": [...],
            "quick_wins": ["saran mudah implementasi"],
            "long_term_improvements": ["saran jangka panjang"]
        }"""
        
        user_prompt = f"""
        RKAT: {rkat.title}
        
        KUP Compliance:
        - Score: {kup_compliance['compliance_percentage']:.1f}%
        - Level: {kup_compliance['compliance_level']}
        - Issues: {json.dumps(kup_compliance.get('checks', []), indent=2)}
        
        SBO Compliance:
        - Score: {sbo_score:.1f}%
        
        Berikan saran spesifik untuk meningkatkan compliance berdasarkan:
        1. Kebijakan Umum Penganggaran 2026
        2. Standar Biaya Operasional 2026
        3. Best practices BPKH
        """
        
        try:
            response = await self._call_ai_api(system_prompt, user_prompt)
            return json.loads(response)
        except Exception as e:
            return {"error": f"Failed to generate suggestions: {str(e)}"}
    
    async def analyze_document(self, file_content: str, document_type: str) -> Dict:
        """AI-powered document analysis"""
        
        system_prompt = f"""Anda adalah document analyzer expert untuk dokumen BPKH.
        Analisis dokumen {document_type} dan berikan feedback konstruktif.
        
        Format output JSON:
        {{
            "document_type": "{document_type}",
            "completeness_score": angka_0_100,
            "quality_score": angka_0_100,
            "strengths": ["kelebihan1", "kelebihan2"],
            "weaknesses": ["kelemahan1", "kelemahan2"],
            "suggestions": ["saran1", "saran2"],
            "compliance_check": {{
                "meets_bpkh_standards": true/false,
                "missing_elements": ["elemen yang kurang"]
            }}
        }}"""
        
        user_prompt = f"""
        Analisis dokumen {document_type} berikut:
        
        {file_content[:2000]}...
        
        Evaluasi berdasarkan:
        1. Kelengkapan sesuai standar BPKH
        2. Kualitas isi dan struktur
        3. Kepatuhan dengan regulasi
        4. Kejelasan dan detail
        """
        
        try:
            response = await self._call_ai_api(system_prompt, user_prompt)
            return json.loads(response)
        except Exception as e:
            return {"error": f"Failed to analyze document: {str(e)}"}
    
    async def _call_ai_api(self, system_prompt: str, user_prompt: str) -> str:
        """Call OpenRouter API with Qwen3"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 2000,
            "temperature": 0.7
        }
        
        response = await self.client.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            raise Exception(f"API call failed: {response.status_code} - {response.text}")
    
    def _build_system_prompt(self, user_context: Dict) -> str:
        """Build system prompt with user context"""
        
        role = user_context.get('role', 'user')
        department = user_context.get('department', 'Unknown')
        
        return f"""Anda adalah AI Assistant expert untuk RKAT BPKH (Badan Pengelola Keuangan Haji).
        
        User Context:
        - Role: {role}
        - Department: {department}
        
        Anda memiliki pengetahuan mendalam tentang:
        1. Kebijakan Umum Penganggaran (KUP) BPKH 2026
        2. Standar Biaya Operasional (SBO) BPKH 2026
        3. Workflow approval RKAT
        4. Regulasi dan best practices BPKH
        5. Prinsip penganggaran yang efisien dan efektif
        
        Selalu berikan jawaban yang:
        - Akurat dan berdasarkan regulasi BPKH
        - Praktis dan actionable
        - Sesuai dengan role user
        - Dalam bahasa Indonesia yang jelas
        - Mengutip referensi yang relevan jika perlu
        """
    
    def _build_user_prompt(self, query: str, additional_context: Dict = None) -> str:
        """Build user prompt with additional context"""
        
        prompt = f"Pertanyaan: {query}"
        
        if additional_context:
            prompt += f"\n\nKontext tambahan:\n{json.dumps(additional_context, indent=2)}"
        
        return prompt
    
    def _generate_fallback_scenarios(self, base_budget: float, parameters: Dict) -> List[Dict]:
        """Generate fallback scenarios if AI fails"""
        
        inflation = parameters.get('inflation_rate', 3.5) / 100
        growth = parameters.get('growth_target', 5.0) / 100
        
        # Conservative scenario
        conservative_budget = base_budget * (1 + inflation)
        
        # Realistic scenario  
        realistic_budget = base_budget * (1 + inflation + growth * 0.5)
        
        # Optimistic scenario
        optimistic_budget = base_budget * (1 + inflation + growth)
        
        return [
            {
                "name": "Conservative Scenario",
                "total_budget": conservative_budget,
                "operational_budget": conservative_budget * 0.7,
                "personnel_budget": conservative_budget * 0.3,
                "assumptions": ["Inflasi normal", "Pertumbuhan minimal"],
                "risks": ["Keterbatasan program", "Efisiensi rendah"]
            },
            {
                "name": "Realistic Scenario", 
                "total_budget": realistic_budget,
                "operational_budget": realistic_budget * 0.65,
                "personnel_budget": realistic_budget * 0.35,
                "assumptions": ["Pertumbuhan moderat", "Efisiensi standar"],
                "risks": ["Fluktuasi ekonomi", "Perubahan regulasi"]
            },
            {
                "name": "Optimistic Scenario",
                "total_budget": optimistic_budget,
                "operational_budget": optimistic_budget * 0.6,
                "personnel_budget": optimistic_budget * 0.4,
                "assumptions": ["Pertumbuhan maksimal", "Efisiensi tinggi"],
                "risks": ["Overcommitment", "Resource constraints"]
            }
        ]