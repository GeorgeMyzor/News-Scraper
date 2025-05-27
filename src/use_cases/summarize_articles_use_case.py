from src.use_cases.news_scrapper import scrap_article
from src.abstrations.articles_repo import ArticlesRepo
from src.abstrations.summarizer import Summarizer

class SummarizeArticlesUseCase:
    def __init__(self, repo: ArticlesRepo, summarizer: Summarizer) -> None:
        self.repo = repo
        self.summarizer = summarizer

    def process(self, urls):
        headline, content = scrap_article(urls)
        
        if headline and content:
            print(f"Title:\n{headline}\n")
            print(f"Article Content:\n{content}\n")
        else:
            print(content) 

        article = self.summarizer.summarize(headline, content)

        self.repo.save(article)
    