from src.application.services.scrapper import scrap_articles_async
from src.abstractions.articles_repo import ArticlesRepo
from src.abstractions.summarizer import Summarizer
from src.abstractions.use_case import UseCase
from src.domain.article_data import ArticleData

class SummarizeArticlesUseCase(UseCase):
    def __init__(self, repo: ArticlesRepo, summarizer: Summarizer) -> None:
        self.repo = repo
        self.summarizer = summarizer

    async def process_async(self, input: str) -> None:
        urls: list[str] = input.split(' ')
        scrapped_articles = await scrap_articles_async(urls)
        
        articles: list[ArticleData] = await self.summarizer.summarize_async(scrapped_articles)

        await self.repo.save_async(articles)
        
        print(f"Article(s) saved to vector DB:")        
        for i, article in enumerate(articles, start=1):
            print(f"Title: {article.headline}")
            print(f"Topics: {', '.join(article.topics)}")
            print(f"Summary: {article.summary}\n")
    