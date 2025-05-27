from src.abstractions.articles_repo import ArticlesRepo
from src.abstractions.use_case import UseCase
from src.application.services.query_enhancer import QueryEnhancer

class QueryArticleUseCase(UseCase):
    def __init__(self, repo: ArticlesRepo, query_enhancer: QueryEnhancer) -> None:
        self.repo = repo
        self.query_enhancer = query_enhancer

    async def process_async(self, query: str) -> None:
        query = await self.query_enhancer.enchance_async(query)
        results = await self.repo.query_async(query)
    
        if not results:
            print("No similar articles found.")
            return

        for i, (doc, score) in enumerate(results, start=1):
            print(f"\nResult {i}:")
            print(f"Score: {score:.4f}")
            print(f"Title: {doc.metadata.get('headline', '[No title]')}")


    