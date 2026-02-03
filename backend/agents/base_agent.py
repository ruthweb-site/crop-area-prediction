"""
Base Agent - Abstract base class for all CropAgent sub-agents.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

class BaseAgent(ABC):
    """Abstract base class for all agents in the CropAgent system."""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"CropAgent.{name}")
        self.last_execution_time: Optional[datetime] = None
        self.execution_count = 0
    
    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's main task.
        
        Args:
            task: Dictionary containing task parameters
            
        Returns:
            Dictionary containing execution results
        """
        pass
    
    @abstractmethod
    def get_capabilities(self) -> list:
        """
        Return a list of capabilities this agent provides.
        
        Returns:
            List of capability strings
        """
        pass
    
    def log_activity(self, message: str, level: str = "info"):
        """Log agent activity."""
        log_func = getattr(self.logger, level, self.logger.info)
        log_func(f"[{self.name}] {message}")
    
    def _record_execution(self):
        """Record execution metrics."""
        self.last_execution_time = datetime.now()
        self.execution_count += 1
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status information."""
        return {
            "name": self.name,
            "last_execution": self.last_execution_time.isoformat() if self.last_execution_time else None,
            "execution_count": self.execution_count,
            "capabilities": self.get_capabilities()
        }
