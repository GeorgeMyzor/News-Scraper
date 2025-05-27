from abc import ABC, abstractmethod
from src.domain.article import Article

class ArticlesRepo(ABC):
    @abstractmethod
    def save(self, article: Article) -> None:
        pass

    @abstractmethod
    def query(self, query: str) -> str:
        pass
