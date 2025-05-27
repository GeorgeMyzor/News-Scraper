from abc import ABC, abstractmethod
from src.domain.article_data import ArticleData

class Summarizer(ABC):
    @abstractmethod
    async def summarize_async(self, headline: str, content: str) -> list[ArticleData]:
        pass
