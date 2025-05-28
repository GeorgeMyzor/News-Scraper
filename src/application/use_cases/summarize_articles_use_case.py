from src.application.services.scrapper import scrap_articles_async
from src.abstractions.articles_repo import ArticlesRepo
from src.abstractions.summarizer import Summarizer
from src.domain.article import Article
from src.application.models.article_summary_dto import ArticleSummaryDTO

class SummarizeArticlesUseCase():
    """
    Use case for summarizing articles from given URLs.
    It scrapes the articles, summarizes them, and saves the results to a vector database.
    """
    def __init__(self, repo: ArticlesRepo, summarizer: Summarizer) -> None:
        self.repo = repo
        self.summarizer = summarizer

    async def __call__(self, urls: list[str]) -> list[ArticleSummaryDTO]:
        """
        Process the input to summarize articles from the provided URLs.
        Args:
            input (str): A space-separated string of URLs to scrape and summarize.
        """
        scrapped_articles = await scrap_articles_async(urls)
        
        articles: list[Article] = await self.summarizer.summarize_async(scrapped_articles)

        await self.repo.save_async(articles)
        
        return [ArticleSummaryDTO.from_article(article=article) for article in articles]
    