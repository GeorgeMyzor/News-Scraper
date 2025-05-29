from typing import Optional
from pydantic import BaseModel

class ArticleQuery(BaseModel):
    """
    Represents the data structure for an article, including its title, content,
    summary, topics, and political bias.
    """
    headline: Optional[str] = None
    content: str
    summary: str
    topics: Optional[list[str]] = None
    political_bias: Optional[str] = None
