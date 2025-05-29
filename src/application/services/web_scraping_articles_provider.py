import asyncio
import httpx
from bs4 import BeautifulSoup
from typing import List, Tuple, Optional
import logging

from abstractions.articles_provider import ArticlesProvider

class WebScrapingArticlesProvider(ArticlesProvider):
    """
    Implements ArticlesProvider to scrape articles from the web using HTTP requests.
    """

    async def get_async(self, paths: List[str]) -> List[Tuple[Optional[str], str]]:
        """
        Asynchronously scrapes articles from a list of URLs.
        Args:
            paths (List[str]): A list of article URLs.
        Returns:
            List[Tuple[Optional[str], str]]: A list of (title, content) tuples.
        """
        tasks = [self._scrap_article_async(url) for url in paths]
        return await asyncio.gather(*tasks)

    async def _scrap_article_async(self, url: str) -> Tuple[Optional[str], str]:
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

        return {
            "headline": title.strip(),
            "content": content.strip()
        }
