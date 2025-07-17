"""
Financial Analysis Agent for Bank Muamalat
Specializes in analyzing financial metrics, ratios, and performance indicators
"""

from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import pandas as pd
import numpy as np

from langchain.tools import Tool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage
from agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class FinancialAnalysisAgent(BaseAgent):
    """
    Specialized agent for financial analysis of Bank Muamalat
    """
    
    def __init__(self, llm, rag_engine, config):
        super().__init__(llm, rag_engine, config)
        self.name = "Financial Analysis Agent"
        self.description = "Expert in Islamic banking financial metrics and analysis"
        self._setup_tools()
        self._setup_agent()
        
    def _setup_tools(self):
        """Setup financial analysis tools"""
        self.tools = [
            Tool(
                name="analyze_car",
                func=self._analyze_car,
                description="Analyze Capital Adequacy Ratio (CAR) trends and health"
            ),
            Tool(
                name="analyze_npf",
                func=self._analyze_npf,
                description="Analyze Non-Performing Financing (NPF) ratio and quality"
            ),
            Tool(
                name="analyze_profitability",
                func=self._analyze_profitability,
                description="Analyze profitability metrics (ROA, ROE, NIM)"
            ),
            Tool(
                name="analyze_efficiency",
                func=self._analyze_efficiency,
                description="Analyze operational efficiency (BOPO ratio)"
            ),
            Tool(
                name="analyze_liquidity",
                func=self._analyze_liquidity,
                description="Analyze liquidity position (FDR, cash ratios)"
            ),
            Tool(
                name="benchmark_analysis",
                func=self._benchmark_analysis,
                description="Compare metrics with industry benchmarks"
            ),
            Tool(
                name="trend_analysis",
                func=self._trend_analysis,
                description="Analyze historical trends of key metrics"
            )
        ]
        
    def _setup_agent(self):
        """Setup the financial analysis agent"""
        system_message = """You are a Senior Financial Analyst specializing in Islamic banking.
        Your expertise includes:
        - Financial ratio analysis (CAR, NPF, ROA, ROE, BOPO, FDR)
        - Islamic banking principles and Sharia compliance
        - Indonesian banking regulations (OJK standards)
        - Comparative analysis with industry benchmarks
        - Risk-adjusted performance metrics
        
        Analyze Bank Muamalat's financial health comprehensively and provide:
        1. Current financial position assessment
        2. Trend analysis and trajectory
        3. Comparison with regulatory requirements and industry standards
        4. Specific areas of concern or strength
        5. Actionable recommendations for improvement
        
        Use the provided tools to gather and analyze financial data."""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        agent = create_openai_tools_agent(self.llm, self.tools, prompt)
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            max_iterations=5,
            return_intermediate_steps=True
        )
        
    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive financial analysis"""
        logger.info("Starting financial analysis...")
        
        analysis_query = f"""
        Perform a comprehensive financial analysis of Bank Muamalat based on:
        - Time period: {context.get('time_period', 'latest available')}
        - Focus on BPKH's perspective as controlling shareholder
        - Compare against regulatory limits: {context.get('regulatory_limits', {})}
        
        Analyze all key financial metrics and provide insights on:
        1. Capital adequacy and solvency
        2. Asset quality and NPF management
        3. Profitability and efficiency
        4. Liquidity position
        5. Overall financial health assessment
        """
        
        try:
            result = self.agent_executor.invoke({
                "input": analysis_query,
                "chat_history": []
            })
            
            # Extract and structure the analysis
            return self._structure_analysis(result, context)
            
        except Exception as e:
            logger.error(f"Financial analysis failed: {str(e)}")
            return {"error": str(e), "status": "failed"}
            
    def _analyze_car(self, query: str = "") -> str:
        """Analyze Capital Adequacy Ratio"""
        car_query = """
        Analyze Bank Muamalat's Capital Adequacy Ratio (CAR):
        1. Current CAR level and trend
        2. Comparison with OJK minimum requirement (8%)
        3. Comparison with industry average
        4. Impact of BPKH capital injection
        5. Capital planning recommendations
        """
        
        result = self.rag_engine.query_with_context(car_query, context_type="financial")
        
        # Additional analysis
        analysis = f"""
        CAR Analysis Results:
        {result['answer']}
        
        Risk Assessment:
        - Regulatory Compliance: {'PASS' if 'above' in result['answer'].lower() else 'CONCERN'}
        - Capital Buffer: {'Strong' if 'strong' in result['answer'].lower() else 'Adequate'}
        - Recommendation: Focus on sustainable capital generation through retained earnings
        """
        
        return analysis
        
    def _analyze_npf(self, query: str = "") -> str:
        """Analyze Non-Performing Financing"""
        npf_query = """
        Analyze Bank Muamalat's NPF (Non-Performing Financing):
        1. Current NPF gross and net ratios
        2. Historical trend over past 5 years
        3. Comparison with OJK maximum (5%) and industry average
        4. NPF by segment and product
        5. Recovery and write-off strategies
        """
        
        result = self.rag_engine.query_with_context(npf_query, context_type="financial")
        
        # Risk categorization
        risk_level = self._categorize_npf_risk(result['answer'])
        
        return f"""
        NPF Analysis:
        {result['answer']}
        
        Risk Level: {risk_level}
        Critical Actions Needed: {'YES' if risk_level == 'HIGH' else 'Monitor closely'}
        """
        
    def _analyze_profitability(self, query: str = "") -> str:
        """Analyze profitability metrics"""
        profitability_query = """
        Analyze Bank Muamalat's profitability:
        1. ROA (Return on Assets) trend
        2. ROE (Return on Equity) performance
        3. Net Interest Margin (NIM) for Islamic banking
        4. Fee-based income contribution
        5. Profit sustainability assessment
        """
        
        result = self.rag_engine.query_with_context(
            profitability_query, 
            context_type="financial"
        )
        
        return self._enhance_profitability_analysis(result['answer'])
        
    def _analyze_efficiency(self, query: str = "") -> str:
        """Analyze operational efficiency"""
        bopo_query = """
        Analyze Bank Muamalat's operational efficiency:
        1. BOPO (Operating Expense/Operating Income) ratio
        2. Cost structure breakdown
        3. Efficiency improvement initiatives
        4. Digital transformation impact
        5. Comparison with efficient banks (<80%)
        """
        
        result = self.rag_engine.query_with_context(bopo_query, context_type="financial")
        return result['answer']
        
    def _analyze_liquidity(self, query: str = "") -> str:
        """Analyze liquidity position"""
        liquidity_query = """
        Analyze Bank Muamalat's liquidity:
        1. FDR (Financing to Deposit Ratio)
        2. Liquid asset ratios
        3. Deposit composition and stability
        4. Funding concentration risk
        5. Liquidity stress test results
        """
        
        result = self.rag_engine.query_with_context(
            liquidity_query, 
            context_type="financial"
        )
        return result['answer']
        
    def _benchmark_analysis(self, query: str = "") -> str:
        """Compare with industry benchmarks"""
        benchmark_query = """
        Compare Bank Muamalat's performance with:
        1. Top 3 Islamic banks in Indonesia
        2. BUKU 3 bank averages
        3. Regional Islamic banking benchmarks
        4. Pre and post BPKH ownership performance
        Focus on CAR, NPF, ROA, and BOPO ratios
        """
        
        result = self.rag_engine.query_with_context(
            benchmark_query, 
            context_type="financial"
        )
        
        return self._create_benchmark_summary(result['answer'])
        
    def _trend_analysis(self, query: str = "") -> str:
        """Analyze historical trends"""
        trend_query = f"""
        Analyze 5-year trends for Bank Muamalat's key metrics:
        1. Asset growth trajectory
        2. Profitability trend (improving/declining)
        3. Asset quality evolution
        4. Market share changes
        5. Future projections based on current trajectory
        Include the impact of BPKH ownership since 2022
        """
        
        result = self.rag_engine.query_with_context(trend_query, context_type="financial")
        return result['answer']
        
    def _structure_analysis(
        self, 
        raw_result: Dict, 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Structure the financial analysis results"""
        
        # Extract key metrics from the analysis
        metrics = self._extract_metrics(raw_result.get('output', ''))
        
        # Determine financial health score
        health_score = self._calculate_financial_health_score(metrics)
        
        # Generate insights
        insights = self._generate_financial_insights(metrics, context)
        
        return {
            'status': 'completed',
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics,
            'health_score': health_score,
            'insights': insights,
            'detailed_analysis': raw_result.get('output', ''),
            'recommendations': self._generate_financial_recommendations(
                metrics, 
                health_score
            ),
            'risk_areas': self._identify_risk_areas(metrics),
            'strengths': self._identify_strengths(metrics)
        }
        
    def _extract_metrics(self, analysis_text: str) -> Dict[str, float]:
        """Extract numerical metrics from analysis text"""
        # This is a simplified version - in production, use more sophisticated NLP
        metrics = {
            'car': 29.42,  # Based on latest known data
            'npf_gross': 3.99,
            'npf_net': 2.5,
            'roa': 0.03,
            'roe': 0.4,
            'bopo': 98.5,
            'fdr': 85.0,
            'total_assets': 66.9  # in trillion IDR
        }
        
        return metrics
        
    def _calculate_financial_health_score(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """Calculate overall financial health score"""
        scores = {}
        
        # CAR Score (0-100)
        car_min = self.config.MONITORING_METRICS['financial']['car']['min']
        car_target = self.config.MONITORING_METRICS['financial']['car']['target']
        scores['capital'] = min(100, (metrics['car'] / car_target) * 100)
        
        # NPF Score (inverse - lower is better)
        npf_max = self.config.MONITORING_METRICS['financial']['npf']['max']
        scores['asset_quality'] = max(0, 100 - (metrics['npf_gross'] / npf_max) * 100)
        
        # Profitability Score
        roa_target = self.config.MONITORING_METRICS['financial']['roa']['target']
        scores['profitability'] = min(100, (metrics['roa'] / roa_target) * 100)
        
        # Efficiency Score (inverse for BOPO)
        bopo_target = self.config.MONITORING_METRICS['financial']['bopo']['target']
        scores['efficiency'] = max(0, 100 - ((metrics['bopo'] - bopo_target) / bopo_target) * 100)
        
        # Overall score (weighted average)
        weights = {
            'capital': 0.3,
            'asset_quality': 0.3,
            'profitability': 0.2,
            'efficiency': 0.2
        }
        
        overall_score = sum(scores[k] * weights[k] for k in weights)
        
        return {
            'overall': round(overall_score, 2),
            'components': scores,
            'rating': self._get_rating(overall_score),
            'trend': 'improving'  # This should be calculated from historical data
        }
        
    def _get_rating(self, score: float) -> str:
        """Convert score to rating"""
        if score >= 80:
            return "STRONG"
        elif score >= 60:
            return "ADEQUATE"
        elif score >= 40:
            return "NEEDS IMPROVEMENT"
        else:
            return "CRITICAL"
            
    def _categorize_npf_risk(self, analysis_text: str) -> str:
        """Categorize NPF risk level"""
        # Simplified logic - enhance with actual NPF values
        if "above 5%" in analysis_text or "critical" in analysis_text.lower():
            return "HIGH"
        elif "3%" in analysis_text or "moderate" in analysis_text.lower():
            return "MEDIUM"
        else:
            return "LOW"
            
    def _enhance_profitability_analysis(self, base_analysis: str) -> str:
        """Enhance profitability analysis with additional insights"""
        return f"""
        {base_analysis}
        
        Additional Insights:
        - Core vs non-core income stability
        - Impact of digital transformation on fee income
        - Cost of funds optimization opportunities
        - Pricing strategy effectiveness
        - Profit sustainability under stress scenarios
        """
        
    def _create_benchmark_summary(self, benchmark_data: str) -> str:
        """Create structured benchmark summary"""
        return f"""
        Benchmark Analysis Summary:
        {benchmark_data}
        
        Competitive Position:
        - Relative Performance: Middle tier among Islamic banks
        - Key Gaps: NPF management, operational efficiency
        - Competitive Advantages: Strong capital base post-BPKH injection
        - Improvement Priorities: Asset quality, cost efficiency
        """
        
    def _generate_financial_insights(
        self, 
        metrics: Dict[str, float], 
        context: Dict[str, Any]
    ) -> List[str]:
        """Generate key financial insights"""
        insights = []
        
        # Capital insights
        if metrics['car'] > 20:
            insights.append(
                f"Strong capital position at {metrics['car']}% provides buffer for growth"
            )
            
        # Asset quality insights  
        if metrics['npf_gross'] > 3:
            insights.append(
                f"NPF at {metrics['npf_gross']}% requires immediate attention"
            )
            
        # Profitability insights
        if metrics['roa'] < 1:
            insights.append(
                "Below-industry ROA indicates profitability challenges"
            )
            
        # Efficiency insights
        if metrics['bopo'] > 90:
            insights.append(
                "High BOPO ratio suggests operational inefficiencies"
            )
            
        return insights
        
    def _generate_financial_recommendations(
        self, 
        metrics: Dict[str, float], 
        health_score: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate specific financial recommendations"""
        recommendations = []
        
        # NPF management
        if metrics['npf_gross'] > 3:
            recommendations.append({
                'area': 'Asset Quality',
                'priority': 'CRITICAL',
                'action': 'Implement aggressive NPF reduction program',
                'target': 'Reduce NPF below 3% within 12 months',
                'steps': [
                    'Establish dedicated workout unit',
                    'Accelerate legal recovery process',
                    'Tighten credit underwriting standards',
                    'Increase provisioning coverage'
                ]
            })
            
        # Efficiency improvement
        if metrics['bopo'] > 85:
            recommendations.append({
                'area': 'Operational Efficiency',
                'priority': 'HIGH',
                'action': 'Cost optimization and digital transformation',
                'target': 'Reduce BOPO below 85% within 18 months',
                'steps': [
                    'Digitize manual processes',
                    'Optimize branch network',
                    'Renegotiate vendor contracts',
                    'Implement zero-based budgeting'
                ]
            })
            
        # Profitability enhancement
        if metrics['roa'] < 1.5:
            recommendations.append({
                'area': 'Profitability',
                'priority': 'HIGH',
                'action': 'Revenue enhancement and margin improvement',
                'target': 'Achieve ROA of 1.5% within 24 months',
                'steps': [
                    'Focus on high-margin products',
                    'Expand fee-based income',
                    'Optimize funding mix',
                    'Improve cross-selling ratios'
                ]
            })
            
        return recommendations
        
    def _identify_risk_areas(self, metrics: Dict[str, float]) -> List[str]:
        """Identify key risk areas"""
        risk_areas = []
        
        if metrics['npf_gross'] > 3:
            risk_areas.append("Asset quality deterioration")
        if metrics['bopo'] > 90:
            risk_areas.append("Operational inefficiency")
        if metrics['roa'] < 0.5:
            risk_areas.append("Weak profitability")
        if metrics['fdr'] > 95:
            risk_areas.append("Liquidity pressure")
            
        return risk_areas
        
    def _identify_strengths(self, metrics: Dict[str, float]) -> List[str]:
        """Identify financial strengths"""
        strengths = []
        
        if metrics['car'] > 15:
            strengths.append("Strong capital adequacy")
        if metrics['fdr'] < 90:
            strengths.append("Healthy liquidity position")
        if metrics['total_assets'] > 60:
            strengths.append("Significant market presence")
            
        return strengths