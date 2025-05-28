import asyncio
import httpx
from bs4 import BeautifulSoup
from typing import List, Tuple, Optional
import logging

async def scrap_articles_async(urls: List[str]) -> List[Tuple[Optional[str], str]]:
    """
    Scrapes multiple articles asynchronously from a list of URLs.
    Args:
        urls (List[str]): A list of URLs to scrape.
    Returns:    
        List[Tuple[Optional[str], str]]: A list of tuples, each containing the article title (or None if not found) and the article content.
    """
    tasks = [scrap_article_async(url) for url in urls]
    return await asyncio.gather(*tasks)

async def scrap_article_async(url: str) -> Tuple[Optional[str], str]:
    """
    Scrapes the article title and content from a given URL.
    Args:
        url (str): The URL of the article to scrape.
    Returns:
        Tuple[Optional[str], str]: A tuple containing the article title (or None if not found) and the article content.
    """ 
    logging.info(f"Scraping article from URL: {url}")
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url)
        response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    title = (soup.title.string if soup.title else None) or \
            (soup.find('h1').get_text(strip=True) if soup.find('h1') else "No title found")

    article_body = soup.find('article') or soup.find('main') or None
    if article_body:
        content = article_body.get_text(separator="\n", strip=True)
    else:
        paragraphs = soup.find_all('p')
        content = "\n".join(p.get_text(strip=True) for p in paragraphs) if paragraphs else "No article content found"

    logging.info(f"Scraped article title: {title.strip() if title else 'No title'}")
    
    return title.strip(), content.strip()
