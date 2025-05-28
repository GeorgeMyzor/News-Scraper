from src.abstractions.articles_repo import ArticlesRepo
from src.application.services.query_enhancer import QueryEnhancer
from src.application.models.related_article_dto import RelatedArticleDTO
from src.application.mappers.article_to_article_dto_mapper import map_articles_from_vector_db

class QueryArticleUseCase():
    """
    Use case for querying articles based on a search query.
    """
    def __init__(self, repo: ArticlesRepo, query_enhancer: QueryEnhancer) -> None:
        self.repo = repo
        self.query_enhancer = query_enhancer

    async def __call__(self, query: str) -> list[RelatedArticleDTO]:
        """
        Process the query to find similar articles.
        This method enhances the query using the QueryEnhancer service
        and retrieves articles from the repository that match the enhanced query.
        Args:
            query (str): The search query input by the user.
        """
        query = await self.query_enhancer.enchance_async(query)
        results = await self.repo.query_async(query)

        articles = map_articles_from_vector_db(results)

        return articles
    