from abc import ABC, abstractmethod
from domain.article_query import ArticleQuery

class Summarizer(ABC):
    """
    Abstract base class for summarizers.
    This class defines the interface for summarizing articles.
    It should be implemented by any concrete summarizer class.
    """
    @abstractmethod
    async def summarize_async(self, headline: str, content: str) -> list[ArticleQuery]:
        pass
