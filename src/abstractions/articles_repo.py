from abc import ABC, abstractmethod
from domain.article_enriched import ArticleEnriched

class ArticlesRepo(ABC):
    """
    Abstract base class for articles repository.
    This class defines the interface for saving and querying articles.
    It should be implemented by any concrete repository class.
    """
    @abstractmethod
    def save_async(self, article: ArticleEnriched) -> None:
        pass

    @abstractmethod
    def query_async(self, query: str) -> str:
        pass
