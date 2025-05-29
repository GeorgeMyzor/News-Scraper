from langchain_core.documents import Document
from langchain_chroma import Chroma
from abstractions.articles_repo import ArticlesRepo
from domain.article_query import ArticleQuery

class ChromaArticlesRepo(ArticlesRepo):
    """
    Repository for storing and querying articles using Chroma vector store.
    This class implements the ArticlesRepo interface and provides methods
    to save articles and perform similarity searches.
    """

    def __init__(self, vector_store: Chroma) -> None:
        self.vector_store = vector_store

    async def save_async(self, articles: list[ArticleQuery]) -> None:
        """
        Saves a list of ArticleData objects to the vector store.
        Args:
            articles (List[ArticleData]): List of ArticleData objects to save.
        """        
        documents = self._articles_to_documents(articles)

        await self.vector_store.aadd_documents(documents)

    def _articles_to_documents(self, articles: list[ArticleQuery]) -> list[Document]:
        """
        Converts a list of ArticleData objects to a list of Document objects
        for storage in the vector store.
        Args:
            articles (List[ArticleData]): List of ArticleData objects to convert.
        Returns:
            List[Document]: List of Document objects ready for vector store.
        """
        documents = []
        for article in articles:
            semantic_text = f"Headline: {article.headline}\nSummary: {article.summary}\nTopics: {', '.join(article.topics)}"
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
    
    async def query_async(self, query: str) -> list[tuple[Document, float]] :
        """
        Queries the vector store for documents similar to the given query.
        Args:
            query (str): The search query to find similar articles.
        Returns:
            List[Tuple[Document, float]]: List of tuples containing Document and similarity score.
        """                
        return await self.vector_store.asimilarity_search_with_score(query)
    
