# app/agents/base.py

from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, llm_service=None):
        self.llm_service = llm_service
    
    @abstractmethod
    def execute(self, query: str, **kwargs) -> Dict[str, Any]:
        """Execute the agent's main functionality"""
        pass