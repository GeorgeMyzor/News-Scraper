from abc import ABC, abstractmethod
from src.domain.article_data import ArticleData

class Summarizer(ABC):
    """
    Abstract base class for summarizers.
    This class defines the interface for summarizing articles.
    It should be implemented by any concrete summarizer class.
    """
    @abstractmethod
    async def summarize_async(self, headline: str, content: str) -> list[ArticleData]:
        pass
