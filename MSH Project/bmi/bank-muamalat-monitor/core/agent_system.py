"""
Agentic AI System for Bank Muamalat Health Monitoring
Orchestrates multiple specialized agents for comprehensive analysis
"""

import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import Tool
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage, HumanMessage
from langchain.memory import ConversationSummaryBufferMemory

from agents.financial_agent import FinancialAnalysisAgent
from agents.risk_agent import RiskAssessmentAgent
from agents.compliance_agent import ComplianceAgent
from agents.business_agent import BusinessStrategyAgent
from core.rag_engine import BankMuamalatRAGEngine

logger = logging.getLogger(__name__)

class AgentOrchestrator:
    """
    Master orchestrator that coordinates multiple specialized agents
    """
    
    def __init__(self, config):
        self.config = config
        self.rag_engine = BankMuamalatRAGEngine(config)
        self.agents = {}
        self.llm = ChatOpenAI(
            model_name=config.LLM_MODEL,
            temperature=0.1,  # Lower temperature for more consistent analysis
            openai_api_key=config.OPENAI_API_KEY
        )
        self.executor = ThreadPoolExecutor(max_workers=4)
        self._initialize_agents()
        
    def _initialize_agents(self):
        """Initialize all specialized agents"""
        try:
            # Financial Analysis Agent
            self.agents['financial'] = FinancialAnalysisAgent(
                self.llm, self.rag_engine, self.config
            )
            
            # Risk Assessment Agent
            self.agents['risk'] = RiskAssessmentAgent(
                self.llm, self.rag_engine, self.config
            )
            
            # Compliance & GRC Agent
            self.agents['compliance'] = ComplianceAgent(
                self.llm, self.rag_engine, self.config
            )
            
            # Business Strategy Agent
            self.agents['business'] = BusinessStrategyAgent(
                self.llm, self.rag_engine, self.config
            )
            
            logger.info("All agents initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize agents: {str(e)}")
            raise
            
    def analyze_bank_health(
        self, 
        focus_areas: Optional[List[str]] = None,
        time_period: str = "latest"
    ) -> Dict[str, Any]:
        """
        Comprehensive bank health analysis using multiple agents
        """
        if not focus_areas:
            focus_areas = ['financial', 'risk', 'compliance', 'business']
            
        logger.info(f"Starting comprehensive analysis for areas: {focus_areas}")
        
        # Prepare analysis context
        context = self._prepare_analysis_context(time_period)
        
        # Run parallel analysis with different agents
        analysis_results = {}
        futures = {}
        
        for area in focus_areas:
            if area in self.agents:
                future = self.executor.submit(
                    self._run_agent_analysis, area, context
                )
                futures[future] = area
                
        # Collect results
        for future in as_completed(futures):
            area = futures[future]
            try:
                result = future.result(timeout=self.config.AGENT_TIMEOUT)
                analysis_results[area] = result
                logger.info(f"Completed {area} analysis")
            except Exception as e:
                logger.error(f"Error in {area} analysis: {str(e)}")
                analysis_results[area] = {"error": str(e)}
                
        # Synthesize results
        synthesis = self._synthesize_analysis(analysis_results)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(synthesis)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'period': time_period,
            'detailed_analysis': analysis_results,
            'synthesis': synthesis,
            'recommendations': recommendations,
            'risk_score': self._calculate_risk_score(analysis_results),
            'decision_support': self._generate_decision_support(synthesis)
        }
        
    def _prepare_analysis_context(self, time_period: str) -> Dict[str, Any]:
        """Prepare context for analysis"""
        # Get latest metrics from RAG
        metrics_query = f"""
        Provide the latest financial metrics for Bank Muamalat including:
        CAR, NPF, ROA, ROE, BOPO, FDR, Total Assets, and Net Profit
        for period: {time_period}
        """
        
        metrics_result = self.rag_engine.query_with_context(
            metrics_query, context_type="financial"
        )
        
        return {
            'time_period': time_period,
            'latest_metrics': metrics_result,
            'ownership_structure': {
                'BPKH_percentage': self.config.BPKH_OWNERSHIP_PERCENTAGE,
                'investment_amount': self.config.BPKH_INVESTMENT_AMOUNT
            },
            'regulatory_limits': self.config.get_regulatory_limits()
        }
        
    def _run_agent_analysis(self, agent_type: str, context: Dict) -> Dict[str, Any]:
        """Run analysis for specific agent"""
        agent = self.agents[agent_type]
        return agent.analyze(context)
        
    def _synthesize_analysis(self, analysis_results: Dict) -> Dict[str, Any]:
        """Synthesize insights from all agents"""
        synthesis_prompt = f"""
        Based on the following multi-agent analysis results for Bank Muamalat:
        
        {json.dumps(analysis_results, indent=2)}
        
        Provide a synthesized analysis that:
        1. Identifies key themes and patterns across all analyses
        2. Highlights critical issues requiring immediate attention
        3. Notes any conflicting assessments and potential reasons
        4. Summarizes the overall health status
        5. Prioritizes areas for intervention
        
        Format as a structured JSON response.
        """
        
        messages = [
            SystemMessage(content="You are a senior banking consultant synthesizing multiple expert analyses."),
            HumanMessage(content=synthesis_prompt)
        ]
        
        response = self.llm.predict_messages(messages)
        
        try:
            return json.loads(response.content)
        except:
            return {"synthesis": response.content}
            
    def _generate_recommendations(self, synthesis: Dict) -> List[Dict[str, Any]]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Financial recommendations
        if 'financial_health' in synthesis:
            if synthesis['financial_health'].get('npf_concern', False):
                recommendations.append({
                    'category': 'Financial',
                    'priority': 'HIGH',
                    'recommendation': 'Immediate NPF reduction program',
                    'actions': [
                        'Establish dedicated NPF task force',
                        'Accelerate recovery and restructuring',
                        'Review and tighten credit policies'
                    ],
                    'timeline': '3-6 months',
                    'impact': 'Critical for regulatory compliance'
                })
                
        # Risk recommendations
        if 'risk_assessment' in synthesis:
            risk_level = synthesis['risk_assessment'].get('overall_risk', 'MEDIUM')
            if risk_level == 'HIGH':
                recommendations.append({
                    'category': 'Risk Management',
                    'priority': 'HIGH',
                    'recommendation': 'Comprehensive risk mitigation program',
                    'actions': [
                        'Strengthen risk management framework',
                        'Enhance early warning systems',
                        'Increase risk provisions'
                    ],
                    'timeline': 'Immediate',
                    'impact': 'Essential for stability'
                })
                
        # Strategic recommendations
        recommendations.append({
            'category': 'Strategic',
            'priority': 'MEDIUM',
            'recommendation': 'Digital transformation acceleration',
            'actions': [
                'Enhance digital banking capabilities',
                'Optimize operational efficiency',
                'Focus on profitable segments (haji, umrah, ASN)'
            ],
            'timeline': '12-18 months',
            'impact': 'Long-term competitiveness'
        })
        
        return recommendations
        
    def _calculate_risk_score(self, analysis_results: Dict) -> Dict[str, Any]:
        """Calculate overall risk score"""
        risk_factors = {
            'financial': 0.4,
            'operational': 0.3,
            'compliance': 0.2,
            'strategic': 0.1
        }
        
        total_score = 0
        component_scores = {}
        
        # Financial risk score
        if 'financial' in analysis_results:
            financial_data = analysis_results['financial']
            npf = financial_data.get('metrics', {}).get('npf', 0)
            car = financial_data.get('metrics', {}).get('car', 100)
            
            financial_score = min((npf / 5.0) * 50 + ((30 - car) / 30) * 50, 100)
            component_scores['financial'] = financial_score
            total_score += financial_score * risk_factors['financial']
            
        # Add other risk components...
        
        risk_level = 'LOW' if total_score < 33 else 'MEDIUM' if total_score < 67 else 'HIGH'
        
        return {
            'overall_score': round(total_score, 2),
            'risk_level': risk_level,
            'components': component_scores,
            'interpretation': self._interpret_risk_score(total_score, risk_level)
        }
        
    def _interpret_risk_score(self, score: float, level: str) -> str:
        """Interpret risk score for decision makers"""
        interpretations = {
            'LOW': "Bank is in stable condition with manageable risks.",
            'MEDIUM': "Bank faces moderate risks requiring active management and monitoring.",
            'HIGH': "Bank is in critical condition requiring immediate intervention."
        }
        return interpretations.get(level, "Unable to determine risk level")
        
    def _generate_decision_support(self, synthesis: Dict) -> Dict[str, Any]:
        """Generate decision support for BPKH"""
        # Analyze against divestment thresholds
        triggers = []
        metrics = synthesis.get('financial_health', {}).get('metrics', {})
        
        if metrics.get('npf', 0) > self.config.DIVESTMENT_THRESHOLDS['npf_critical']:
            triggers.append("NPF exceeds critical threshold")
            
        if metrics.get('car', 100) < self.config.DIVESTMENT_THRESHOLDS['car_minimum']:
            triggers.append("CAR below regulatory minimum")
            
        # Decision recommendation
        if len(triggers) >= 2:
            decision = "CONSIDER DIVESTMENT"
            confidence = "HIGH"
        elif len(triggers) == 1:
            decision = "MAINTAIN WITH CONDITIONS"
            confidence = "MEDIUM"
        else:
            decision = "MAINTAIN INVESTMENT"
            confidence = "HIGH"
            
        return {
            'recommendation': decision,
            'confidence': confidence,
            'triggers': triggers,
            'rationale': self._generate_decision_rationale(decision, triggers, synthesis),
            'alternative_options': self._generate_alternatives(decision)
        }
        
    def _generate_decision_rationale(
        self, 
        decision: str, 
        triggers: List[str], 
        synthesis: Dict
    ) -> str:
        """Generate detailed rationale for decision"""
        if decision == "MAINTAIN INVESTMENT":
            return """
            Bank Muamalat shows acceptable performance metrics within regulatory limits.
            Continued ownership allows BPKH to:
            1. Support Islamic banking ecosystem
            2. Leverage synergies with hajj services
            3. Achieve reasonable returns on investment
            Strategic transformation initiatives show promise for improvement.
            """
        elif decision == "MAINTAIN WITH CONDITIONS":
            return f"""
            While concerns exist ({', '.join(triggers)}), the bank retains strategic value.
            Recommended conditions:
            1. Quarterly performance reviews
            2. Specific improvement targets
            3. Management accountability measures
            4. Timeline for addressing identified issues
            """
        else:
            return f"""
            Multiple critical issues ({', '.join(triggers)}) suggest high risk.
            Divestment considerations:
            1. Minimize potential losses to hajj funds
            2. Ensure orderly transition
            3. Explore strategic buyers who can strengthen the bank
            4. Maintain Islamic banking principles
            """
            
    def _generate_alternatives(self, primary_decision: str) -> List[Dict[str, str]]:
        """Generate alternative strategic options"""
        alternatives = []
        
        if primary_decision == "MAINTAIN INVESTMENT":
            alternatives.append({
                'option': 'Increase stake for full control',
                'pros': 'Complete strategic alignment, easier transformation',
                'cons': 'Higher capital requirement, increased risk exposure'
            })
            
        alternatives.extend([
            {
                'option': 'Strategic partnership',
                'pros': 'Shared risk, access to expertise',
                'cons': 'Diluted control, complexity'
            },
            {
                'option': 'Phased divestment',
                'pros': 'Gradual risk reduction, market timing flexibility',
                'cons': 'Prolonged uncertainty, execution complexity'
            }
        ])
        
        return alternatives
        
    async def get_real_time_insights(self, query: str) -> Dict[str, Any]:
        """Get real-time insights for specific queries"""
        # This can be extended to connect to live data feeds
        return await self._process_real_time_query(query)
        
    async def _process_real_time_query(self, query: str) -> Dict[str, Any]:
        """Process real-time queries asynchronously"""
        # Implementation for real-time data processing
        pass
        
    def generate_board_report(self) -> Dict[str, Any]:
        """Generate comprehensive report for BPKH board"""
        analysis = self.analyze_bank_health()
        
        return {
            'executive_summary': self.rag_engine.generate_executive_summary(),
            'detailed_analysis': analysis['detailed_analysis'],
            'risk_assessment': analysis['risk_score'],
            'recommendations': analysis['recommendations'],
            'decision_support': analysis['decision_support'],
            'appendices': {
                'methodology': 'Multi-agent RAG-based analysis',
                'data_sources': 'Annual reports, regulatory filings, market data',
                'analysis_date': datetime.now().isoformat()
            }
        }
        
    def shutdown(self):
        """Cleanup resources"""
        self.executor.shutdown(wait=True)
        logger.info("Agent orchestrator shutdown complete")