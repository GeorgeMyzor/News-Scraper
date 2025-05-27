from src.abstractions.articles_repo import ArticlesRepo
from src.abstractions.use_case import UseCase
from src.application.services.query_enhancer import QueryEnhancer

class QueryArticleUseCase(UseCase):
    """
    Use case for querying articles based on a search query.
    """
    def __init__(self, repo: ArticlesRepo, query_enhancer: QueryEnhancer) -> None:
        self.repo = repo
        self.query_enhancer = query_enhancer

    async def process_async(self, query: str) -> None:
        """
        Process the query to find similar articles.
        This method enhances the query using the QueryEnhancer service
        and retrieves articles from the repository that match the enhanced query.
        Args:
            query (str): The search query input by the user.
        """
        query = await self.query_enhancer.enchance_async(query)
        results = await self.repo.query_async(query)
    
        if not results:
            print("No similar articles found.")
            return

        for i, (doc, score) in enumerate(results, start=1):
            print(f"\nResult {i}:")
            print(f"Score: {score:.4f}")
            print(f"Title: {doc.metadata.get('headline', '[No title]')}")


    