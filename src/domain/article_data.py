from typing import Optional
from pydantic import BaseModel

class ArticleData(BaseModel):
    """
    Represents the data structure for an article, including its title, content,
    summary, topics, and political bias.
    """
    headline: Optional[str]
    content: str
    summary: str
    topics: Optional[list[str]]
    political_bias: Optional[str]
    
    class Config:
        frozen = True 
