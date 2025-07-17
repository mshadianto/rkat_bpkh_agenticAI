"""
Agent Orchestrator for coordinating multiple agents
This module manages the interaction between different specialized agents
"""

from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor
import json

logger = logging.getLogger(__name__)

class AgentOrchestrator:
    """
    Orchestrates multiple agents for comprehensive analysis
    """
    
    def __init__(self, agents: Dict[str, Any]):
        self.agents = agents
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.results_cache = {}
        
    def run_analysis(
        self,
        analysis_type: str = "comprehensive",
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Run coordinated analysis across multiple agents
        
        Args:
            analysis_type: Type of analysis to run
            context: Additional context for agents
            
        Returns:
            Combined analysis results
        """
        if context is None:
            context = self._prepare_default_context()
            
        logger.info(f"Starting {analysis_type} analysis with orchestrator")
        
        if analysis_type == "comprehensive":
            return self._run_comprehensive_analysis(context)
        elif analysis_type == "financial_focus":
            return self._run_financial_focus_analysis(context)
        elif analysis_type == "risk_focus":
            return self._run_risk_focus_analysis(context)
        elif analysis_type == "strategic":
            return self._run_strategic_analysis(context)
        else:
            return self._run_custom_analysis(analysis_type, context)
            
    def _run_comprehensive_analysis(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Run analysis using all available agents"""
        start_time = datetime.now()
        
        # Define agent execution order and dependencies
        execution_plan = [
            # Phase 1: Independent analyses
            {
                'phase': 1,
                'agents': ['financial', 'compliance'],
                'parallel': True
            },
            # Phase 2: Dependent on Phase 1
            {
                'phase': 2,
                'agents': ['risk', 'business'],
                'parallel': True,
                'dependencies': ['financial']
            }
        ]
        
        results = {}
        
        for phase in execution_plan:
            phase_results = self._execute_phase(phase, context, results)
            results.update(phase_results)
            
        # Synthesize results
        synthesis = self._synthesize_results(results)
        
        # Generate final recommendations
        recommendations = self._generate_final_recommendations(synthesis)
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return {
            'analysis_type': 'comprehensive',
            'timestamp': datetime.now().isoformat(),
            'execution_time_seconds': execution_time,
            'agent_results': results,
            'synthesis': synthesis,
            'recommendations': recommendations,
            'executive_summary': self._generate_executive_summary(synthesis),
            'decision_matrix': self._generate_decision_matrix(synthesis)
        }
        
    def _run_financial_focus_analysis(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Run analysis focused on financial aspects"""
        agents_to_run = ['financial', 'risk']
        results = {}
        
        for agent_name in agents_to_run:
            if agent_name in self.agents:
                try:
                    result = self.agents[agent_name].analyze(context)
                    results[agent_name] = result
                except Exception as e:
                    logger.error(f"Error in {agent_name} agent: {str(e)}")
                    results[agent_name] = {'error': str(e)}
                    
        return {
            'analysis_type': 'financial_focus',
            'timestamp': datetime.now().isoformat(),
            'results': results,
            'financial_health_score': self._calculate_financial_health_score(results),
            'key_insights': self._extract_financial_insights(results)
        }
        
    def _run_risk_focus_analysis(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Run analysis focused on risk assessment"""
        agents_to_run = ['risk', 'compliance', 'financial']
        results = {}
        
        for agent_name in agents_to_run:
            if agent_name in self.agents:
                try:
                    result = self.agents[agent_name].analyze(context)
                    results[agent_name] = result
                except Exception as e:
                    logger.error(f"Error in {agent_name} agent: {str(e)}")
                    results[agent_name] = {'error': str(e)}
                    
        return {
            'analysis_type': 'risk_focus',
            'timestamp': datetime.now().isoformat(),
            'results': results,
            'risk_matrix': self._generate_risk_matrix(results),
            'early_warnings': self._compile_early_warnings(results),
            'mitigation_priorities': self._prioritize_mitigations(results)
        }
        
    def _run_strategic_analysis(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Run strategic analysis for BPKH decision making"""
        # Run all agents for comprehensive strategic view
        results = {}
        
        # Sequential execution for strategic analysis
        agent_sequence = ['financial', 'risk', 'compliance', 'business']
        
        for agent_name in agent_sequence:
            if agent_name in self.agents:
                # Pass previous results as context
                enriched_context = {
                    **context,
                    'previous_analyses': results
                }
                
                try:
                    result = self.agents[agent_name].analyze(enriched_context)
                    results[agent_name] = result
                except Exception as e:
                    logger.error(f"Error in {agent_name} agent: {str(e)}")
                    results[agent_name] = {'error': str(e)}
                    
        return {
            'analysis_type': 'strategic',
            'timestamp': datetime.now().isoformat(),
            'results': results,
            'strategic_options': self._evaluate_strategic_options(results),
            'decision_recommendation': self._generate_decision_recommendation(results),
            'implementation_roadmap': self._create_implementation_roadmap(results)
        }
        
    def _execute_phase(
        self,
        phase: Dict[str, Any],
        context: Dict[str, Any],
        previous_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a phase of agent analysis"""
        phase_results = {}
        
        # Enrich context with dependencies
        enriched_context = context.copy()
        if 'dependencies' in phase:
            for dep in phase['dependencies']:
                if dep in previous_results:
                    enriched_context[f'{dep}_analysis'] = previous_results[dep]
                    
        if phase.get('parallel', False):
            # Run agents in parallel
            futures = {}
            
            for agent_name in phase['agents']:
                if agent_name in self.agents:
                    future = self.executor.submit(
                        self.agents[agent_name].analyze,
                        enriched_context
                    )
                    futures[future] = agent_name
                    
            # Collect results
            for future in futures:
                agent_name = futures[future]
                try:
                    result = future.result(timeout=300)  # 5 minute timeout
                    phase_results[agent_name] = result
                except Exception as e:
                    logger.error(f"Error in {agent_name} agent: {str(e)}")
                    phase_results[agent_name] = {'error': str(e)}
        else:
            # Run agents sequentially
            for agent_name in phase['agents']:
                if agent_name in self.agents:
                    try:
                        result = self.agents[agent_name].analyze(enriched_context)
                        phase_results[agent_name] = result
                        # Add to context for next agent
                        enriched_context[f'{agent_name}_analysis'] = result
                    except Exception as e:
                        logger.error(f"Error in {agent_name} agent: {str(e)}")
                        phase_results[agent_name] = {'error': str(e)}
                        
        return phase_results
        
    def _synthesize_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize results from multiple agents"""
        synthesis = {
            'overall_health': 'MODERATE',
            'key_strengths': [],
            'critical_issues': [],
            'opportunities': [],
            'consensus_areas': [],
            'divergent_views': []
        }
        
        # Extract key metrics
        if 'financial' in results and 'metrics' in results['financial']:
            financial_metrics = results['financial']['metrics']
            
            # Assess overall health
            if financial_metrics.get('npf_gross', 0) > 3.5:
                synthesis['overall_health'] = 'CONCERNING'
                synthesis['critical_issues'].append('High NPF level')
                
            if financial_metrics.get('car', 0) > 20:
                synthesis['key_strengths'].append('Strong capital position')
                
        # Extract risk assessment
        if 'risk' in results and 'risk_matrix' in results['risk']:
            risk_data = results['risk']['risk_matrix']
            high_risks = [
                risk for risk, data in risk_data.items()
                if data.get('level') == 'HIGH'
            ]
            synthesis['critical_issues'].extend(high_risks)
            
        # Extract opportunities
        if 'business' in results and 'growth_opportunities' in results['business']:
            opportunities = results['business']['growth_opportunities'].get('high_priority', [])
            synthesis['opportunities'] = opportunities[:3]  # Top 3
            
        # Find consensus and divergence
        synthesis['consensus_areas'] = self._find_consensus(results)
        synthesis['divergent_views'] = self._find_divergence(results)
        
        return synthesis
        
    def _generate_final_recommendations(self, synthesis: Dict[str, Any]) -> List[Dict]:
        """Generate final recommendations based on synthesis"""
        recommendations = []
        
        # Critical recommendations based on issues
        for issue in synthesis.get('critical_issues', []):
            if 'NPF' in issue:
                recommendations.append({
                    'category': 'Asset Quality',
                    'recommendation': 'Implement immediate NPF reduction program',
                    'priority': 'CRITICAL',
                    'timeline': '3 months',
                    'expected_impact': 'Reduce NPF by 1-2 percentage points',
                    'resource_requirement': 'High'
                })
                
        # Strategic recommendations based on opportunities
        for opp in synthesis.get('opportunities', []):
            recommendations.append({
                'category': 'Growth',
                'recommendation': f"Pursue {opp.get('opportunity', 'growth opportunity')}",
                'priority': 'HIGH',
                'timeline': opp.get('timeline', '12 months'),
                'expected_impact': opp.get('potential_value', 'Significant'),
                'resource_requirement': 'Medium'
            })
            
        # Governance recommendations
        if synthesis.get('overall_health') in ['CONCERNING', 'MODERATE']:
            recommendations.append({
                'category': 'Governance',
                'recommendation': 'Strengthen BPKH oversight and monitoring',
                'priority': 'HIGH',
                'timeline': 'Immediate',
                'expected_impact': 'Improved decision making and risk management',
                'resource_requirement': 'Low'
            })
            
        return recommendations
        
    def _generate_executive_summary(self, synthesis: Dict[str, Any]) -> str:
        """Generate executive summary"""
        health_status = synthesis.get('overall_health', 'UNKNOWN')
        strengths = ', '.join(synthesis.get('key_strengths', ['None identified']))
        issues = ', '.join(synthesis.get('critical_issues', ['None identified']))
        
        summary = f"""
        EXECUTIVE SUMMARY - Bank Muamalat Health Assessment
        
        Overall Status: {health_status}
        
        Bank Muamalat shows mixed performance with strong capital adequacy but 
        concerning asset quality trends. The bank benefits from BPKH's capital 
        injection (CAR: 29.42%) but faces challenges with rising NPF (3.99%) 
        and operational inefficiency (BOPO: 98.5%).
        
        Key Strengths: {strengths}
        
        Critical Issues: {issues}
        
        Strategic Recommendation: MAINTAIN INVESTMENT WITH CONDITIONS
        - Implement aggressive NPF reduction program
        - Accelerate digital transformation
        - Focus on profitable niches (hajj/umrah, ASN)
        - Consider strategic partnership for expertise
        
        The bank has potential for turnaround but requires decisive action 
        within 12-18 months to avoid further deterioration.
        """
        
        return summary.strip()
        
    def _generate_decision_matrix(self, synthesis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate decision matrix for BPKH"""
        return {
            'maintain_investment': {
                'score': 65,
                'pros': [
                    'Strong capital base',
                    'Strategic fit with hajj ecosystem',
                    'Islamic banking mission alignment'
                ],
                'cons': [
                    'Declining profitability',
                    'High operational costs',
                    'Competitive pressures'
                ],
                'conditions': [
                    'NPF reduction to <3% within 12 months',
                    'BOPO improvement to <90% within 18 months',
                    'Digital transformation completion'
                ]
            },
            'divest': {
                'score': 35,
                'pros': [
                    'Avoid further losses',
                    'Focus on core BPKH mission',
                    'Reduce regulatory burden'
                ],
                'cons': [
                    'Loss of strategic asset',
                    'Negative market signal',
                    'Limited buyer interest'
                ],
                'conditions': [
                    'NPF exceeds 5%',
                    'Consecutive losses for 4 quarters',
                    'Regulatory sanctions'
                ]
            }
        }
        
    def _prepare_default_context(self) -> Dict[str, Any]:
        """Prepare default context for analysis"""
        return {
            'time_period': 'latest',
            'analysis_date': datetime.now().isoformat(),
            'ownership_structure': {
                'BPKH_percentage': 82.66,
                'investment_amount': 3_000_000_000_000
            },
            'focus_areas': ['financial', 'risk', 'compliance', 'strategic']
        }
        
    def _calculate_financial_health_score(self, results: Dict) -> float:
        """Calculate overall financial health score"""
        if 'financial' in results and 'health_score' in results['financial']:
            return results['financial']['health_score'].get('overall', 50.0)
        return 50.0  # Default neutral score
        
    def _extract_financial_insights(self, results: Dict) -> List[str]:
        """Extract key financial insights"""
        insights = []
        
        if 'financial' in results:
            financial_data = results['financial']
            if 'insights' in financial_data:
                insights.extend(financial_data['insights'][:5])  # Top 5
                
        return insights
        
    def _generate_risk_matrix(self, results: Dict) -> Dict[str, Any]:
        """Generate consolidated risk matrix"""
        risk_matrix = {}
        
        if 'risk' in results and 'risk_matrix' in results['risk']:
            risk_matrix = results['risk']['risk_matrix']
            
        return risk_matrix
        
    def _compile_early_warnings(self, results: Dict) -> List[Dict]:
        """Compile early warnings from all agents"""
        warnings = []
        
        for agent_name, result in results.items():
            if 'early_warnings' in result:
                warnings.extend(result['early_warnings'])
                
        # Deduplicate and prioritize
        unique_warnings = []
        seen = set()
        
        for warning in sorted(warnings, key=lambda x: x.get('severity', 'LOW')):
            key = warning.get('message', '')
            if key not in seen:
                seen.add(key)
                unique_warnings.append(warning)
                
        return unique_warnings[:10]  # Top 10 warnings
        
    def _prioritize_mitigations(self, results: Dict) -> List[Dict]:
        """Prioritize risk mitigation actions"""
        mitigations = []
        
        # Extract from risk agent
        if 'risk' in results and 'risk_mitigation_plan' in results['risk']:
            mitigations.extend(results['risk']['risk_mitigation_plan'])
            
        # Sort by priority and impact
        mitigations.sort(
            key=lambda x: (
                x.get('priority', 'LOW') == 'CRITICAL',
                x.get('expected_impact', 'Low') == 'High'
            ),
            reverse=True
        )
        
        return mitigations[:5]  # Top 5 priorities
        
    def _evaluate_strategic_options(self, results: Dict) -> List[Dict]:
        """Evaluate strategic options for BPKH"""
        options = []
        
        if 'business' in results and 'bpkh_decision_options' in results['business']:
            return results['business']['bpkh_decision_options']
            
        return options
        
    def _generate_decision_recommendation(self, results: Dict) -> Dict[str, Any]:
        """Generate final decision recommendation"""
        # Aggregate scores and factors
        factors = {
            'financial_health': 40,  # weight
            'risk_level': 30,
            'strategic_fit': 20,
            'compliance_status': 10
        }
        
        scores = {}
        if 'financial' in results:
            scores['financial_health'] = 45  # Based on weak profitability
        if 'risk' in results:
            scores['risk_level'] = 35  # High risk
        if 'business' in results:
            scores['strategic_fit'] = 75  # Good fit with BPKH
        if 'compliance' in results:
            scores['compliance_status'] = 85  # Generally compliant
            
        # Calculate weighted score
        total_score = sum(
            scores.get(factor, 50) * weight / 100
            for factor, weight in factors.items()
        )
        
        if total_score > 60:
            decision = "MAINTAIN WITH CONDITIONS"
        elif total_score > 40:
            decision = "RESTRUCTURE"
        else:
            decision = "CONSIDER EXIT"
            
        return {
            'recommendation': decision,
            'confidence_level': 'MEDIUM-HIGH',
            'score': total_score,
            'key_factors': scores,
            'rationale': self._generate_rationale(decision, scores)
        }
        
    def _generate_rationale(self, decision: str, scores: Dict) -> str:
        """Generate rationale for decision"""
        if decision == "MAINTAIN WITH CONDITIONS":
            return """
            Despite current challenges, Bank Muamalat retains strategic value 
            for BPKH due to strong synergies with hajj ecosystem and Islamic 
            banking mission. With focused intervention on NPF reduction and 
            operational efficiency, the bank can return to profitability 
            within 18-24 months.
            """
        elif decision == "RESTRUCTURE":
            return """
            Significant restructuring is required to address fundamental 
            issues. Consider bringing in strategic partners or merging with 
            another Islamic bank to achieve scale and efficiency.
            """
        else:
            return """
            Current trajectory suggests limited recovery potential. 
            Strategic exit should be considered to minimize further losses 
            and redirect resources to core BPKH mission.
            """
            
    def _create_implementation_roadmap(self, results: Dict) -> Dict[str, List]:
        """Create implementation roadmap"""
        if 'business' in results and 'implementation_roadmap' in results['business']:
            return results['business']['implementation_roadmap']
            
        # Default roadmap
        return {
            'immediate_0_3_months': [
                'Establish NPF task force',
                'Launch cost reduction program',
                'Strengthen risk monitoring'
            ],
            'short_term_3_6_months': [
                'Implement digital quick wins',
                'Optimize branch network',
                'Launch hajj ecosystem products'
            ],
            'medium_term_6_12_months': [
                'Complete core banking upgrade',
                'Achieve NPF target <3%',
                'Scale digital channels'
            ],
            'long_term_12_24_months': [
                'Complete digital transformation',
                'Achieve BOPO <85%',
                'Market leadership in Islamic niche'
            ]
        }
        
    def _run_custom_analysis(self, analysis_type: str, context: Dict) -> Dict:
        """Run custom analysis type"""
        logger.warning(f"Unknown analysis type: {analysis_type}, running comprehensive")
        return self._run_comprehensive_analysis(context)
        
    def cleanup(self):
        """Cleanup resources"""
        self.executor.shutdown(wait=True)
        self.results_cache.clear()