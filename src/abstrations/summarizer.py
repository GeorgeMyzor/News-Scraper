from abc import ABC, abstractmethod
from src.domain.article import Article

class Summarizer(ABC):
    @abstractmethod
    def summarize(self, headline: str, content: str) -> Article:
        pass
