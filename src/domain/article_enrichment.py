from typing import Optional
from pydantic import BaseModel, Field

class ArticleEnrichment(BaseModel):
    """
    Represents the enriched data structure for an article, including its title, content,
    AI generated summary and topics, and political bias.
    """
    summary: str = Field(
        default=None, description="Summary that captures key points of the article."
    )
    topics: Optional[list[str]] = Field(
        default=None, description="Two to four most relevant topics mentioned in the article.",
    )
    political_bias: Optional[str] = Field(
        default=None,
        description="Political bias of the article.",
        json_schema_extra={
            "enum":["Right", "Lean Right", "None", "Lean Left", "Left"]
        }
    )