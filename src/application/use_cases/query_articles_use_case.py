import logging

from abstractions.articles_repo import ArticlesRepo
from application.services.query_enhancer import QueryEnhancer
from application.models.related_article_dto import RelatedArticleDTO

class QueryArticleUseCase():
    """
    Use case for querying articles based on a search query.
    """
    def __init__(self, repo: ArticlesRepo, query_enhancer: QueryEnhancer) -> None:
        self.repo = repo
        self.query_enhancer = query_enhancer

    async def __call__(self, query: str) -> list[RelatedArticleDTO]:
        """
        Process the input to query related articles based on the provided search query.
        Args:
            query (str): The search query to find related articles.
        Returns:
            list[RelatedArticleDTO]: List of related articles matching the query.
        """
        logging.info("Exectuing query articles use case with query: %s", query)
        
        query = await self.query_enhancer.enhance_async(query)
        results = await self.repo.query_async(query)

        logging.info("Query articles use case completed with %d results", len(results))
        
        return [RelatedArticleDTO.from_document(document=document, score=score) for (document, score) in results]
    