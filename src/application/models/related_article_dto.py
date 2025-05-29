from typing import Optional
from pydantic import BaseModel

class RelatedArticleDTO(BaseModel):
    """
    Represents the data structure for an article, including its title, content,
    summary, topics, and political bias.
    """
    headline: Optional[str] = None
    content: str
    summary: str
    topics: Optional[list[str]] = None
    political_bias: Optional[str] = None
    score: Optional[float] = None
        
    @classmethod
    def from_document(cls, document, score) -> 'RelatedArticleDTO':
        """
        Converts an Article object to an ArticleSummaryDTO.
        
        Args:
            article (Article): The Article object to convert.
        
        Returns:
            ArticleSummaryDTO: The converted DTO.
        """
        
        metadata = getattr(document, "metadata", {})

        topics = metadata.get("topics", None)

        # Convert topics from comma-separated string to list if needed
        if isinstance(topics, str):
            topics = [t.strip() for t in topics.split(",") if t.strip()]

        return cls(
            headline=metadata.get("headline"),
            summary=metadata.get("summary", ""),
            content=metadata.get("content", ""),
            topics=topics,
            political_bias=metadata.get("political_bias"),
            score=score
        )
    