# llm_service/base.py

from abc import ABC, abstractmethod
from typing import Any

class BaseLLM(ABC):
    """
    Abstract factory class for providing LLM and Embedding models.
    Implementations should provide specific vendor models.
    """

    @abstractmethod
    def get_llm(self, **kwargs: Any) -> Any: 
        """
        Get a Language Model instance.
        Implementations should handle API key retrieval from environment variables.
        """
        pass

    @abstractmethod
    def get_embedding(self, **kwargs: Any) -> Any: 
        """
        Get an Embedding Model instance.
        Implementations should handle API key retrieval from environment variables.
        """
        pass

