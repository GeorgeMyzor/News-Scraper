from src.abstractions.articles_repo import ArticlesRepo
from src.abstractions.use_case import UseCase

class QueryArticleUseCase(UseCase):
    def __init__(self, repo: ArticlesRepo) -> None:
        self.repo = repo

    async def process_async(self, query: str) -> None:        
        results = await self.repo.query_async(query)
    
        if not results:
            print("No similar articles found.")
            return

        for i, (doc, score) in enumerate(results, start=1):
            print(f"\nResult {i}:")
            print(f"Score: {score:.4f}")
            print(f"Title: {doc.metadata.get('headline', '[No title]')}")


    