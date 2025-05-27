import requests
from bs4 import BeautifulSoup
from src.domain.article import Article

def scrap_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.title.string if soup.title else "No title found"
        article_body = soup.find('article')
        
        content = article_body.get_text(strip=True) if article_body else "No article content found"

        return title, content
    except Exception as e:
        return None, f"An error occurred: {str(e)}"