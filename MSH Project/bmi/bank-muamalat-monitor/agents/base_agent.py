"""
Base Agent Class for all specialized agents
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """
    Abstract base class for all specialized agents
    """
    
    def __init__(self, llm, rag_engine, config):
        self.llm = llm
        self.rag_engine = rag_engine
        self.config = config
        self.name = "Base Agent"
        self.description = "Base agent class"
        self.tools = []
        self.agent_executor = None
        self.memory = []
        
    @abstractmethod
    def _setup_tools(self):
        """Setup agent-specific tools"""
        pass
        
    @abstractmethod
    def _setup_agent(self):
        """Setup the agent with prompts and tools"""
        pass
        
    @abstractmethod
    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform agent-specific analysis"""
        pass
        
    def log_analysis(self, analysis_type: str, result: Any):
        """Log analysis results"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'agent': self.name,
            'analysis_type': analysis_type,
            'result_summary': str(result)[:200]
        }
        self.memory.append(log_entry)
        logger.info(f"{self.name} - {analysis_type} completed")
        
    def get_memory(self) -> List[Dict[str, Any]]:
        """Get agent's memory/history"""
        return self.memory
        
    def clear_memory(self):
        """Clear agent's memory"""
        self.memory = []
        logger.info(f"{self.name} memory cleared")
        
    def validate_context(self, context: Dict[str, Any]) -> bool:
        """Validate input context"""
        required_fields = ['time_period']
        for field in required_fields:
            if field not in context:
                logger.error(f"Missing required field: {field}")
                return False
        return True
        
    def format_error_response(self, error: Exception) -> Dict[str, Any]:
        """Format error response"""
        return {
            'status': 'error',
            'agent': self.name,
            'error_message': str(error),
            'timestamp': datetime.now().isoformat()
        }