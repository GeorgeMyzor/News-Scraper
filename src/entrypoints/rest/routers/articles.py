from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.application.use_cases.summarize_articles_use_case import SummarizeArticlesUseCase
from src.application.use_cases.query_articles_use_case import QueryArticleUseCase
from src.abstractions.dependencies import get_summarize_articles_user_case, get_query_articles_user_case
from src.application.models.related_article_dto import RelatedArticleDTO
from src.application.models.article_summary_dto import ArticleSummaryDTO

router = APIRouter(prefix="/articles")

@router.post("/summary", status_code=status.HTTP_200_OK)
async def summarize_article(
    urls: list[str],
    use_case: Annotated[SummarizeArticlesUseCase, Depends(get_summarize_articles_user_case)],
) -> list[ArticleSummaryDTO]:
    return await use_case(urls)

    
@router.get("/query", status_code=status.HTTP_200_OK)
async def query_related(
    query: str,
    use_case: Annotated[QueryArticleUseCase, Depends(get_query_articles_user_case)],
) -> list[RelatedArticleDTO]:
    return await use_case(query)