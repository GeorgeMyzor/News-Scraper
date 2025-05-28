from abc import ABC, abstractmethod
from src.domain.article_data import ArticleData

class ArticlesRepo(ABC):
    """
    Abstract base class for articles repository.
    This class defines the interface for saving and querying articles.
    It should be implemented by any concrete repository class.
    """
    @abstractmethod
    def save_async(self, article: ArticleData) -> None:
        pass

    @abstractmethod
    def query_async(self, query: str) -> str:
        pass
