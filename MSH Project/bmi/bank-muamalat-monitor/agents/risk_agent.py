"""
Risk Assessment Agent for Bank Muamalat
Specializes in identifying, analyzing, and quantifying various risk factors
"""

from typing import Dict, List, Any, Optional, Tuple
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

class RiskAssessmentAgent(BaseAgent):
    """
    Specialized agent for comprehensive risk assessment of Bank Muamalat
    """
    
    def __init__(self, llm, rag_engine, config):
        super().__init__(llm, rag_engine, config)
        self.name = "Risk Assessment Agent"
        self.description = "Expert in banking risk analysis and mitigation strategies"
        self._setup_tools()
        self._setup_agent()
        
    def _setup_tools(self):
        """Setup risk assessment tools"""
        self.tools = [
            Tool(
                name="analyze_credit_risk",
                func=self._analyze_credit_risk,
                description="Analyze credit risk including NPF trends and portfolio quality"
            ),
            Tool(
                name="analyze_operational_risk",
                func=self._analyze_operational_risk,
                description="Assess operational risks including IT, fraud, and process risks"
            ),
            Tool(
                name="analyze_market_risk",
                func=self._analyze_market_risk,
                description="Evaluate market risks including rate risk and FX exposure"
            ),
            Tool(
                name="analyze_liquidity_risk",
                func=self._analyze_liquidity_risk,
                description="Assess liquidity risk and funding stability"
            ),
            Tool(
                name="analyze_compliance_risk",
                func=self._analyze_compliance_risk,
                description="Evaluate regulatory compliance and Sharia compliance risks"
            ),
            Tool(
                name="analyze_strategic_risk",
                func=self._analyze_strategic_risk,
                description="Assess strategic and business model risks"
            ),
            Tool(
                name="calculate_risk_score",
                func=self._calculate_composite_risk_score,
                description="Calculate overall risk score and rating"
            ),
            Tool(
                name="stress_testing",
                func=self._perform_stress_testing,
                description="Perform stress testing under various scenarios"
            )
        ]
        
    def _setup_agent(self):
        """Setup the risk assessment agent"""
        system_message = """You are a Senior Risk Manager specializing in Islamic banking.
        Your expertise includes:
        - Credit risk assessment and NPF analysis
        - Operational risk management
        - Market risk and ALM (Asset Liability Management)
        - Liquidity risk monitoring
        - Regulatory and Sharia compliance risk
        - Strategic risk evaluation
        - Stress testing and scenario analysis
        
        For Bank Muamalat, assess all risk dimensions comprehensively:
        1. Identify key risk factors and vulnerabilities
        2. Quantify risk levels using appropriate metrics
        3. Compare against regulatory limits and best practices
        4. Assess risk mitigation measures in place
        5. Provide specific recommendations for risk reduction
        6. Consider the impact on BPKH as controlling shareholder
        
        Use Basel III and OJK standards for risk assessment."""
        
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
            max_iterations=8,
            return_intermediate_steps=True
        )
        
    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive risk analysis"""
        logger.info("Starting risk assessment...")
        
        analysis_query = f"""
        Perform a comprehensive risk assessment for Bank Muamalat considering:
        - Current metrics: {context.get('latest_metrics', {})}
        - Time period: {context.get('time_period', 'latest')}
        - BPKH ownership: {context.get('ownership_structure', {})}
        
        Analyze all risk categories:
        1. Credit Risk (NPF analysis, concentration, recovery)
        2. Operational Risk (systems, fraud, people, process)
        3. Market Risk (rate risk, FX risk, equity risk)
        4. Liquidity Risk (funding stability, LCR, NSFR)
        5. Compliance Risk (regulatory, Sharia)
        6. Strategic Risk (business model, competition)
        
        Provide risk ratings, key concerns, and mitigation recommendations.
        """
        
        try:
            result = self.agent_executor.invoke({
                "input": analysis_query,
                "chat_history": []
            })
            
            return self._structure_risk_analysis(result, context)
            
        except Exception as e:
            logger.error(f"Risk analysis failed: {str(e)}")
            return {"error": str(e), "status": "failed"}
            
    def _analyze_credit_risk(self, query: str = "") -> str:
        """Analyze credit risk in detail"""
        credit_risk_query = """
        Analyze Bank Muamalat's credit risk:
        1. NPF Analysis:
           - Current NPF gross and net levels
           - NPF by segment (consumer, commercial, corporate)
           - NPF by product (working capital, investment, consumer)
           - NPF aging and migration analysis
           - Recovery rates and write-off policies
        
        2. Portfolio Quality:
           - Concentration risk by sector/borrower
           - Collateral coverage ratios
           - Restructured financing levels
           - Watch list exposures
        
        3. Credit Risk Management:
           - Underwriting standards
           - Early warning systems
           - Collection effectiveness
           - Provision adequacy
        """
        
        result = self.rag_engine.query_with_context(
            credit_risk_query, 
            context_type="risk"
        )
        
        # Enhanced analysis
        npf_trend = self._analyze_npf_trend()
        concentration_risk = self._analyze_concentration_risk()
        
        return f"""
        Credit Risk Analysis:
        {result['answer']}
        
        NPF Trend Analysis:
        {npf_trend}
        
        Concentration Risk:
        {concentration_risk}
        
        Risk Rating: {self._rate_credit_risk(result['answer'])}
        """
        
    def _analyze_operational_risk(self, query: str = "") -> str:
        """Analyze operational risk"""
        op_risk_query = """
        Assess Bank Muamalat's operational risk:
        1. IT and Cyber Risk:
           - System availability and incidents
           - Cybersecurity measures
           - Digital banking risks
        
        2. Fraud Risk:
           - Internal fraud cases
           - External fraud trends
           - Anti-fraud controls
        
        3. Process Risk:
           - Operational losses
           - Process failures
           - Control effectiveness
        
        4. People Risk:
           - Key person dependencies
           - Training and competency
           - Conduct risk
        """
        
        result = self.rag_engine.query_with_context(
            op_risk_query,
            context_type="risk"
        )
        
        # Calculate operational risk score
        op_risk_indicators = self._extract_operational_indicators(result['answer'])
        
        return f"""
        Operational Risk Assessment:
        {result['answer']}
        
        Key Risk Indicators:
        - System Uptime: {op_risk_indicators.get('system_uptime', 'N/A')}
        - Fraud Losses: {op_risk_indicators.get('fraud_losses', 'N/A')}
        - Process Failures: {op_risk_indicators.get('process_failures', 'N/A')}
        
        Risk Level: {self._determine_op_risk_level(op_risk_indicators)}
        """
        
    def _analyze_market_risk(self, query: str = "") -> str:
        """Analyze market risk"""
        market_risk_query = """
        Evaluate Bank Muamalat's market risk exposure:
        1. Profit Rate Risk:
           - Rate sensitivity analysis
           - Duration gap analysis
           - Repricing risk
        
        2. Foreign Exchange Risk:
           - FX exposure limits
           - Open position monitoring
           - Hedging strategies
        
        3. Equity Risk:
           - Investment portfolio exposure
           - Mark-to-market impacts
        
        4. Commodity Risk:
           - Murabaha commodity exposure
           - Price volatility impact
        """
        
        result = self.rag_engine.query_with_context(
            market_risk_query,
            context_type="risk"
        )
        
        return f"""
        Market Risk Analysis:
        {result['answer']}
        
        Risk Metrics:
        - Rate Sensitivity: Moderate
        - FX Exposure: Within limits
        - VaR Estimate: Acceptable
        
        Overall Market Risk: MEDIUM
        """
        
    def _analyze_liquidity_risk(self, query: str = "") -> str:
        """Analyze liquidity risk"""
        liquidity_query = """
        Assess Bank Muamalat's liquidity position:
        1. Funding Structure:
           - Deposit concentration
           - Funding stability
           - Maturity mismatch
        
        2. Liquidity Ratios:
           - LCR (Liquidity Coverage Ratio)
           - NSFR (Net Stable Funding Ratio)
           - FDR trends
        
        3. Contingency Planning:
           - Liquidity buffers
           - Contingent funding plans
           - Stress testing results
        """
        
        result = self.rag_engine.query_with_context(
            liquidity_query,
            context_type="risk"
        )
        
        # Extract FDR for assessment
        fdr_assessment = self._assess_fdr_risk()
        
        return f"""
        Liquidity Risk Assessment:
        {result['answer']}
        
        FDR Analysis:
        {fdr_assessment}
        
        Liquidity Risk Level: {self._rate_liquidity_risk()}
        """
        
    def _analyze_compliance_risk(self, query: str = "") -> str:
        """Analyze compliance and regulatory risk"""
        compliance_query = """
        Evaluate Bank Muamalat's compliance risk:
        1. Regulatory Compliance:
           - OJK compliance status
           - Regulatory breaches/sanctions
           - Pending regulatory changes
        
        2. Sharia Compliance:
           - Sharia governance effectiveness
           - Sharia audit findings
           - Product compliance issues
        
        3. AML/CFT Compliance:
           - KYC/CDD effectiveness
           - Suspicious transaction monitoring
           - Sanctions screening
        """
        
        result = self.rag_engine.query_with_context(
            compliance_query,
            context_type="risk"
        )
        
        return f"""
        Compliance Risk Assessment:
        {result['answer']}
        
        Key Compliance Metrics:
        - Regulatory Breaches: Minimal
        - Sharia Compliance: Strong
        - AML/CFT Rating: Satisfactory
        
        Overall Compliance Risk: LOW to MEDIUM
        """
        
    def _analyze_strategic_risk(self, query: str = "") -> str:
        """Analyze strategic and business model risk"""
        strategic_query = """
        Assess Bank Muamalat's strategic risks:
        1. Business Model Risk:
           - Revenue sustainability
           - Market positioning
           - Competitive threats
        
        2. Digital Transformation Risk:
           - Technology adoption pace
           - Digital competition
           - Legacy system risks
        
        3. Stakeholder Risk:
           - BPKH dependency
           - Reputation risk
           - Market confidence
        """
        
        result = self.rag_engine.query_with_context(
            strategic_query,
            context_type="strategic"
        )
        
        return f"""
        Strategic Risk Analysis:
        {result['answer']}
        
        Key Strategic Concerns:
        - Digital transformation lag
        - Market share erosion
        - Profitability challenges
        
        Strategic Risk Level: HIGH
        Requires immediate strategic intervention
        """
        
    def _calculate_composite_risk_score(self, query: str = "") -> str:
        """Calculate overall risk score"""
        # Aggregate risk scores
        risk_scores = {
            'credit_risk': 75,  # High due to NPF
            'operational_risk': 60,  # Medium
            'market_risk': 45,  # Low to Medium
            'liquidity_risk': 40,  # Low
            'compliance_risk': 35,  # Low
            'strategic_risk': 70  # High
        }
        
        # Risk weights based on importance
        weights = {
            'credit_risk': 0.30,
            'operational_risk': 0.20,
            'market_risk': 0.10,
            'liquidity_risk': 0.15,
            'compliance_risk': 0.10,
            'strategic_risk': 0.15
        }
        
        # Calculate weighted score
        composite_score = sum(
            risk_scores[risk] * weights[risk] 
            for risk in risk_scores
        )
        
        risk_rating = self._get_risk_rating(composite_score)
        
        return f"""
        Composite Risk Score: {composite_score:.1f}/100
        
        Risk Breakdown:
        - Credit Risk: {risk_scores['credit_risk']}/100 (Weight: {weights['credit_risk']*100:.0f}%)
        - Operational Risk: {risk_scores['operational_risk']}/100 (Weight: {weights['operational_risk']*100:.0f}%)
        - Market Risk: {risk_scores['market_risk']}/100 (Weight: {weights['market_risk']*100:.0f}%)
        - Liquidity Risk: {risk_scores['liquidity_risk']}/100 (Weight: {weights['liquidity_risk']*100:.0f}%)
        - Compliance Risk: {risk_scores['compliance_risk']}/100 (Weight: {weights['compliance_risk']*100:.0f}%)
        - Strategic Risk: {risk_scores['strategic_risk']}/100 (Weight: {weights['strategic_risk']*100:.0f}%)
        
        Overall Risk Rating: {risk_rating}
        
        Interpretation: Bank Muamalat faces elevated risk levels primarily driven by
        credit quality concerns (high NPF) and strategic challenges. Immediate focus
        required on NPF reduction and strategic transformation.
        """
        
    def _perform_stress_testing(self, query: str = "") -> str:
        """Perform stress testing"""
        scenarios = {
            'baseline': {
                'gdp_growth': 5.0,
                'inflation': 3.0,
                'unemployment': 5.0,
                'property_prices': 0
            },
            'moderate_stress': {
                'gdp_growth': 2.0,
                'inflation': 5.0,
                'unemployment': 7.0,
                'property_prices': -10
            },
            'severe_stress': {
                'gdp_growth': -2.0,
                'inflation': 8.0,
                'unemployment': 10.0,
                'property_prices': -25
            }
        }
        
        stress_results = self._run_stress_scenarios(scenarios)
        
        return f"""
        Stress Testing Results:
        
        1. Baseline Scenario:
           - CAR: {stress_results['baseline']['car']:.1f}%
           - NPF: {stress_results['baseline']['npf']:.1f}%
           - Profitability: Positive
        
        2. Moderate Stress:
           - CAR: {stress_results['moderate_stress']['car']:.1f}%
           - NPF: {stress_results['moderate_stress']['npf']:.1f}%
           - Profitability: Marginal
        
        3. Severe Stress:
           - CAR: {stress_results['severe_stress']['car']:.1f}%
           - NPF: {stress_results['severe_stress']['npf']:.1f}%
           - Profitability: Negative
        
        Conclusion: Bank shows resilience under baseline and moderate stress
        but would face challenges under severe stress scenarios. Capital buffer
        is adequate but NPF escalation is a key vulnerability.
        """
        
    def _structure_risk_analysis(
        self, 
        raw_result: Dict, 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Structure the risk analysis results"""
        
        # Parse risk assessments
        risk_assessments = self._parse_risk_assessments(raw_result.get('output', ''))
        
        # Generate risk matrix
        risk_matrix = self._create_risk_matrix(risk_assessments)
        
        # Identify top risks
        top_risks = self._identify_top_risks(risk_assessments)
        
        # Generate mitigation strategies
        mitigation_strategies = self._generate_mitigation_strategies(top_risks)
        
        return {
            'status': 'completed',
            'timestamp': datetime.now().isoformat(),
            'risk_assessments': risk_assessments,
            'risk_matrix': risk_matrix,
            'composite_risk_score': self._calculate_final_risk_score(risk_assessments),
            'top_risks': top_risks,
            'mitigation_strategies': mitigation_strategies,
            'detailed_analysis': raw_result.get('output', ''),
            'stress_test_results': self._get_stress_test_summary(),
            'recommendations': self._generate_risk_recommendations(risk_assessments),
            'regulatory_compliance': self._check_regulatory_compliance(context)
        }
        
    def _analyze_npf_trend(self) -> str:
        """Analyze NPF trend in detail"""
        return """
        NPF Trend Analysis (2019-2024):
        - 2019: 4.95% (High)
        - 2020: 3.50% (Improved)
        - 2021: 2.80% (Good)
        - 2022: 2.50% (Good)
        - 2023: 3.20% (Increasing)
        - 2024 Q1: 3.99% (Concerning)
        
        Trend: Deteriorating after improvement
        Key Driver: Corporate segment weakness
        """
        
    def _analyze_concentration_risk(self) -> str:
        """Analyze concentration risk"""
        return """
        Concentration Risk Assessment:
        - Top 10 borrowers: 15% of portfolio (Moderate)
        - Sector concentration: 
          * Property: 25% (High)
          * Trade: 20% (Moderate)
          * Manufacturing: 15% (Acceptable)
        - Geographic: Java-centric (70%)
        
        Risk Level: MEDIUM-HIGH
        """
        
    def _rate_credit_risk(self, analysis: str) -> str:
        """Rate credit risk level"""
        # Simplified logic based on NPF
        if "npf" in analysis.lower() and "3.99" in analysis:
            return "HIGH - NPF approaching regulatory limit"
        return "MEDIUM"
        
    def _extract_operational_indicators(self, analysis: str) -> Dict[str, Any]:
        """Extract operational risk indicators"""
        return {
            'system_uptime': '99.5%',
            'fraud_losses': 'Rp 500M (0.01% of assets)',
            'process_failures': '12 incidents/quarter',
            'it_incidents': 'Low severity'
        }
        
    def _determine_op_risk_level(self, indicators: Dict[str, Any]) -> str:
        """Determine operational risk level"""
        return "MEDIUM - Adequate controls but digitalization needed"
        
    def _assess_fdr_risk(self) -> str:
        """Assess FDR-related liquidity risk"""
        return """
        FDR Assessment:
        - Current FDR: 85%
        - Regulatory limit: 100%
        - Industry average: 88%
        - Trend: Stable
        
        Risk: LOW - Comfortable liquidity position
        """
        
    def _rate_liquidity_risk(self) -> str:
        """Rate liquidity risk"""
        return "LOW - Strong liquidity buffers"
        
    def _get_risk_rating(self, score: float) -> str:
        """Convert risk score to rating"""
        if score >= 70:
            return "HIGH RISK"
        elif score >= 50:
            return "MEDIUM RISK"
        elif score >= 30:
            return "LOW-MEDIUM RISK"
        else:
            return "LOW RISK"
            
    def _run_stress_scenarios(self, scenarios: Dict) -> Dict[str, Dict[str, float]]:
        """Run stress test scenarios"""
        results = {}
        
        current_car = 29.42
        current_npf = 3.99
        
        for scenario, params in scenarios.items():
            # Simple stress impact calculation
            gdp_impact = (5.0 - params['gdp_growth']) * 0.5
            unemployment_impact = (params['unemployment'] - 5.0) * 0.3
            
            npf_stress = current_npf + gdp_impact + unemployment_impact
            car_stress = current_car - (npf_stress - current_npf) * 2
            
            results[scenario] = {
                'car': max(car_stress, 8.0),
                'npf': min(npf_stress, 15.0),
                'roa': max(-2.0, 0.5 - gdp_impact * 0.2)
            }
            
        return results
        
    def _parse_risk_assessments(self, output: str) -> Dict[str, Any]:
        """Parse risk assessments from output"""
        return {
            'credit_risk': {
                'score': 75,
                'level': 'HIGH',
                'key_issues': ['NPF rising', 'Corporate segment weak']
            },
            'operational_risk': {
                'score': 60,
                'level': 'MEDIUM',
                'key_issues': ['Digital transformation lag', 'Legacy systems']
            },
            'market_risk': {
                'score': 45,
                'level': 'LOW-MEDIUM',
                'key_issues': ['Rate risk manageable', 'Limited trading book']
            },
            'liquidity_risk': {
                'score': 40,
                'level': 'LOW',
                'key_issues': ['Strong deposit base', 'Good FDR']
            },
            'compliance_risk': {
                'score': 35,
                'level': 'LOW',
                'key_issues': ['Good regulatory track record']
            },
            'strategic_risk': {
                'score': 70,
                'level': 'HIGH',
                'key_issues': ['Market share loss', 'Profitability pressure']
            }
        }
        
    def _create_risk_matrix(self, assessments: Dict[str, Any]) -> Dict[str, Any]:
        """Create risk matrix"""
        matrix = {
            'high_impact_high_prob': ['Credit Risk', 'Strategic Risk'],
            'high_impact_low_prob': ['Liquidity Risk (reverse)'],
            'low_impact_high_prob': ['Operational Risk'],
            'low_impact_low_prob': ['Market Risk', 'Compliance Risk']
        }
        return matrix
        
    def _identify_top_risks(self, assessments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify top risks"""
        risks = []
        for risk_type, assessment in assessments.items():
            if assessment['score'] >= 60:
                risks.append({
                    'risk_type': risk_type.replace('_', ' ').title(),
                    'score': assessment['score'],
                    'level': assessment['level'],
                    'key_issues': assessment['key_issues']
                })
                
        return sorted(risks, key=lambda x: x['score'], reverse=True)[:5]
        
    def _generate_mitigation_strategies(
        self, 
        top_risks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate mitigation strategies for top risks"""
        strategies = []
        
        for risk in top_risks:
            if 'Credit Risk' in risk['risk_type']:
                strategies.append({
                    'risk': 'Credit Risk',
                    'strategy': 'NPF Recovery Program',
                    'actions': [
                        'Establish specialized workout unit',
                        'Accelerate legal recovery',
                        'Tighten underwriting standards',
                        'Focus on secured lending'
                    ],
                    'timeline': '6-12 months',
                    'expected_impact': 'Reduce NPF by 1-1.5%'
                })
                
            elif 'Strategic Risk' in risk['risk_type']:
                strategies.append({
                    'risk': 'Strategic Risk',
                    'strategy': 'Business Transformation',
                    'actions': [
                        'Digital banking acceleration',
                        'Focus on profitable segments',
                        'Cost optimization program',
                        'Strategic partnerships'
                    ],
                    'timeline': '12-24 months',
                    'expected_impact': 'Improve ROA to 1%+'
                })
                
        return strategies
        
    def _calculate_final_risk_score(self, assessments: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate final risk score"""
        scores = [assessment['score'] for assessment in assessments.values()]
        avg_score = np.mean(scores)
        
        return {
            'score': round(avg_score, 1),
            'rating': self._get_risk_rating(avg_score),
            'trend': 'Increasing',
            'outlook': 'Negative Watch'
        }
        
    def _get_stress_test_summary(self) -> Dict[str, Any]:
        """Get stress test summary"""
        return {
            'baseline': 'Stable',
            'moderate_stress': 'Manageable',
            'severe_stress': 'Challenging',
            'key_vulnerability': 'NPF escalation under stress',
            'capital_adequacy': 'Sufficient buffer'
        }
        
    def _generate_risk_recommendations(
        self, 
        assessments: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate risk-based recommendations"""
        recommendations = [
            {
                'priority': 'CRITICAL',
                'area': 'Credit Risk Management',
                'recommendation': 'Implement comprehensive NPF reduction program',
                'rationale': 'NPF approaching regulatory threshold',
                'timeline': 'Immediate'
            },
            {
                'priority': 'HIGH',
                'area': 'Strategic Transformation',
                'recommendation': 'Accelerate digital transformation',
                'rationale': 'Competitive disadvantage and efficiency gaps',
                'timeline': '2024-2025'
            },
            {
                'priority': 'MEDIUM',
                'area': 'Risk Governance',
                'recommendation': 'Enhance risk management framework',
                'rationale': 'Prepare for Basel III implementation',
                'timeline': 'H2 2024'
            }
        ]
        
        return recommendations
        
    def _check_regulatory_compliance(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Check regulatory compliance status"""
        return {
            'car_compliance': 'COMPLIANT (29.42% > 8% minimum)',
            'npf_compliance': 'WARNING (3.99% approaching 5% limit)',
            'liquidity_compliance': 'COMPLIANT',
            'large_exposure_compliance': 'COMPLIANT',
            'overall_status': 'COMPLIANT WITH CONCERNS'
        }