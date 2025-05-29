from abstractions.articles_repo import ArticlesRepo
from abstractions.summarizer import Summarizer
from abstractions.articles_provider import ArticlesProvider
from domain.article_enriched import ArticleEnriched
from application.models.article_summary_dto import ArticleSummaryDTO
import logging

class SummarizeArticlesUseCase():
    """
    Use case for summarizing articles from given URLs.
    It scrapes the articles, summarizes them, and saves the results to a vector database.
    """
    def __init__(self, repo: ArticlesRepo, summarizer: Summarizer, articles_provider: ArticlesProvider) -> None:
        self.repo = repo
        self.summarizer = summarizer
        self.articles_provider = articles_provider

    async def __call__(self, urls: list[str]) -> list[ArticleSummaryDTO]:
        """
        Process the input to summarize articles from the provided URLs.
        Args:
            input (str): A space-separated string of URLs to scrape and summarize.
        """
        logging.info("Executing summarize articles use case")
        
        scrapped_articles = await self.articles_provider.get_async(urls)
        
        articles: list[ArticleEnriched] = await self.summarizer.summarize_async(scrapped_articles)

        await self.repo.save_async(articles)
        
        logging.info("Summarize articles use case completed with %d articles", len(articles))
        
        return [ArticleSummaryDTO.from_article(article=article) for article in articles]
    