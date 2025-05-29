import asyncio
import httpx
import logging
from bs4 import BeautifulSoup
from typing import Optional

from abstractions.articles_provider import ArticlesProvider
from application.exceptions.no_content_error import NoContentError

class WebScrapingArticlesProvider(ArticlesProvider):
    """
    Implements ArticlesProvider to scrape articles from the web using HTTP requests.
    """

    async def get_async(self, paths: list[str]) -> list[tuple[Optional[str], str]]:
        """
        Scrapes articles from the provided URLs asynchronously.
        Args:
            paths (list[str]): List of URLs to scrape articles from.
        Returns:
            list[tuple[Optional[str], str]]: List of tuples containing the article title and content.
        """
        tasks = [self._scrap_article_async(url) for url in paths]
        
        return await asyncio.gather(*tasks)

    async def _scrap_article_async(self, url: str) -> tuple[Optional[str], str]:
        """
        Scrapes a single article from the given URL.
        Args:
            url (str): The URL of the article to scrape.
        Returns:
            tuple[Optional[str], str]: A tuple containing the article title and content.
        """
        logging.info("Scraping article from URL: %s", url)

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        title = (soup.title.string if soup.title else None) or \
                (soup.find('h1').get_text(strip=True) if soup.find('h1') else "No title found")

        article_body = soup.find('article') or soup.find('main')
        if article_body:
            content = article_body.get_text(separator="\n", strip=True)
        else:
            paragraphs = soup.find_all('p')            
            content = "\n".join(p.get_text(strip=True) for p in paragraphs) if paragraphs else "No article content found"
            
        if(not is_valid_article(content)):
            raise NoContentError(url)
        
        return {
            "headline": title.strip(),
            "content": content.strip()
        }
        
def is_valid_article(text) -> bool:
    """
    Validates if the scraped text is a valid article.
    Args:
        text (str): The text content of the article.
    Returns:
        bool: True if the text is a valid article, False otherwise.
    """
    if len(text.split()) < 100:
        return False
    if text.count('.') < 5:
        return False
    return True