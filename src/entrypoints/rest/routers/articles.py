from typing import Annotated

from fastapi import APIRouter, Depends, status, Query

from application.use_cases.summarize_articles_use_case import SummarizeArticlesUseCase
from application.use_cases.query_articles_use_case import QueryArticleUseCase
from abstractions.dependencies import get_summarize_articles_user_case, get_query_articles_user_case
from application.models.related_article_dto import RelatedArticleDTO
from application.models.article_summary_dto import ArticleSummaryDTO

router = APIRouter(prefix="/articles")

@router.post(
    "/summary",
    status_code=status.HTTP_200_OK,
    summary="Summarize a list of article URLs",
    description="Accepts a list of URLs and returns summarized content for each article.",
    response_model=list[ArticleSummaryDTO],
    responses={
        422: {"description": "Validation or content extraction failed"},
        400: {"description": "Invalid URLs"},
        500: {"description": "Unexpected server error"}
    },
    tags=["Articles"]
)
async def summarize_articles(
    urls: list[str],
    use_case: Annotated[SummarizeArticlesUseCase, Depends(get_summarize_articles_user_case)],
) -> list[ArticleSummaryDTO]:
    return await use_case(urls)

@router.get(
    "/query",
    status_code=status.HTTP_200_OK,
    summary="Find articles related to a query",
    description="Searches and returns articles related to the provided query string.",
    response_model=list[RelatedArticleDTO],
    tags=["Articles"]
)
async def query_related(
    use_case: Annotated[QueryArticleUseCase, Depends(get_query_articles_user_case)],
    query: str = Query(..., description="Search query string", min_length=3),
) -> list[RelatedArticleDTO]:
    return await use_case(query)