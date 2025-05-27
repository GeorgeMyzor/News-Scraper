from src.abstrations.articles_repo import ArticlesRepo

class QueryArticleUseCase:
    def __init__(self, repo: ArticlesRepo) -> None:
        self.repo = repo

    def process(self, query):
        self.repo.query(query)


    