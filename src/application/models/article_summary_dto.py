from typing import Optional
from pydantic import BaseModel

class ArticleSummaryDTO(BaseModel):
    """
    Represents the data structure for an article, including its headline,
    summary, topics, and political bias.
    """
    headline: Optional[str]
    summary: str
    topics: Optional[list[str]]
    political_bias: Optional[str]

    @classmethod
    def from_article(cls, article) -> 'ArticleSummaryDTO':
        """
        Converts an Article object to an ArticleSummaryDTO.
        
        Args:
            article (Article): The Article object to convert.
        
        Returns:
            ArticleSummaryDTO: The converted DTO.
        """
        return cls(
            headline=article.headline,
            summary=article.summary,
            topics=article.topics,
            political_bias=article.political_bias
        )