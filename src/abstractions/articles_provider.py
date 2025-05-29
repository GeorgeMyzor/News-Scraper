from abc import ABC, abstractmethod
from typing import Optional

class ArticlesProvider(ABC):
    """
    Abstract base class for articles provider.
    This class defines the interface for fetching articles from various sources.
    It should be implemented by any concrete provider class.
    """
    @abstractmethod
    def get_async(self, paths: list[str]) -> tuple[Optional[str], str]:
        pass
