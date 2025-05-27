from typing import Optional
from pydantic import BaseModel

class ArticleData(BaseModel):
    headline: Optional[str]
    content: str
    summary: str
    topics: Optional[list[str]]
    political_bias: Optional[str]
    
    class Config:
        frozen = True 
