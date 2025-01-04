from abc import ABC, abstractmethod
from typing import Optional

class BaseLLM(ABC):
    """Base class for all LLM implementations"""

    @abstractmethod
    def ask(self, prompt: str, system_message: Optional[str] = None):
        """Send a prompt to the LLM and get a response."""
        pass

 