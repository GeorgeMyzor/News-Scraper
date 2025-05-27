from typing import Optional
from pydantic import BaseModel, Field

class Article(BaseModel):
    """News article scrapped from web page."""
    headline: str = Field(
        default=None,
        exclude=True
    )
    content: str = Field(
        default=None,
        exclude=True
    )
    summary: str = Field(
        default=None, description="Summary that captures key points of the article"
    )
    topics: Optional[list[str]] = Field(
        default=None, description="List of topics mentioned in the article", 
    )
    political_bias: Optional[str] = Field(
        default=None, description="Political bias of the article", enum=["Right", "Lean Right", "None", "Lean Left", "Left"]
    )