from abc import ABC, abstractmethod
from src.domain.article_data import ArticleData

class ArticlesRepo(ABC):
    @abstractmethod
    def save_async(self, article: ArticleData) -> None:
        pass

    @abstractmethod
    def query_async(self, query: str) -> str:
        pass
