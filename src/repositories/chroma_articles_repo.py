from langchain_core.documents import Document
from langchain_chroma import Chroma
from src.abstractions.articles_repo import ArticlesRepo
from src.domain.article_data import ArticleData
from typing import List, Tuple

class ChromaArticlesRepo(ArticlesRepo):
    """Articles repository based on ChromaDB."""

    def __init__(self, vector_store: Chroma) -> None:
        self.vector_store = vector_store

    async def save_async(self, articles: List[ArticleData]) -> None:
        """
        Saves a summarized article to the vector store.
        """
        
        documents = self._articles_to_documents(articles)

        await self.vector_store.aadd_documents(documents)

    def _articles_to_documents(self, articles: List[ArticleData]) -> List[Document]:
        documents = []
        for article in articles:
            semantic_text = f"{article.summary}\nTopics: {', '.join(article.topics)}"
            doc = Document(
                page_content=semantic_text,
                metadata={
                    "headline": article.headline,
                    "summary": article.summary,
                    "topics": ','.join(article.topics),
                    "content": article.content,
                    "political_bias": article.political_bias,
                },
            )
            documents.append(doc)
        return documents
    
    async def query_async(self, query: str) -> List[Tuple[Document, float]] :
        """
        Runs a similarity search on the vector DB and returns top results.
        """
        return await self.vector_store.asimilarity_search_with_score(query)
    
