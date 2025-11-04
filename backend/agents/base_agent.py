"""
Base Agent Class - All agents inherit from this
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    
    Every agent must implement the execute() method.
    Provides common functionality like logging and timing.
    """
    
    def __init__(self, name: str):
        """
        Initialize base agent.
        
        Args:
            name (str): Name of the agent (e.g., "Data Fetcher")
        """
        self.name = name
        self.logger = logging.getLogger(name)
        self.start_time = None
        self.end_time = None
    
    @abstractmethod
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's task.
        
        This method MUST be implemented by all agents.
        
        Args:
            state (Dict): Current state containing all data
            
        Returns:
            Dict: Updated state with agent's output
        """
        pass
    
    def log(self, message: str, level: str = "info"):
        """
        Log a message with the agent's name.
        
        Args:
            message (str): Message to log
            level (str): Log level (info, warning, error)
        """
        if level == "info":
            self.logger.info(f"[{self.name}] {message}")
        elif level == "warning":
            self.logger.warning(f"[{self.name}] {message}")
        elif level == "error":
            self.logger.error(f"[{self.name}] {message}")
    
    def start_timer(self):
        """Start timing the agent's execution"""
        self.start_time = datetime.now()
        self.log(f"Starting execution...")
    
    def end_timer(self):
        """End timing and log duration"""
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        self.log(f"Completed in {duration:.2f} seconds")
        return duration
    
    def create_error_state(self, state: Dict[str, Any], error_message: str) -> Dict[str, Any]:
        """
        Create an error state when something goes wrong.
        
        Args:
            state (Dict): Current state
            error_message (str): Error description
            
        Returns:
            Dict: State with error information
        """
        self.log(f"Error: {error_message}", level="error")
        return {
            **state,
            "status": "error",
            "error": error_message,
            "failed_agent": self.name
        }