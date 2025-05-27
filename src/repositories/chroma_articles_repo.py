from langchain_core.documents import Document
from src.domain.article import Article
from langchain_chroma import Chroma
from src.abstrations.articles_repo import ArticlesRepo

class ChromaArticlesRepo(ArticlesRepo):
    """Articles repository based on chromadb"""
    def __init__(self, vector_store: Chroma) -> None:
        self.vector_store = vector_store
        
    def save(self, article: Article):
        """
        Saves a document to the vector database.
        """

        semantic_text = f"{article.summary}\nTopics: {', '.join(article.topics)}"

        documents = [
            Document(
                page_content=semantic_text,
                metadata={
                    "headline": article.headline,
                    "summary": article.summary,
                    "topics": ','.join(article.topics),
                    "content": article.content,
                    "political_bias": article.political_bias
                },
            )
        ]
        self.vector_store.add_documents(
            documents=documents
        )
        print(f"Article saved to vector DB: {article.headline}")

        
    def query(self, query: str):
        """
        Query
        """

        results = self.vector_store.similarity_search_with_score(query)

        for i, doc in enumerate(results):
            print(f"\nResult {i + 1}:")
            print(f"\nScore: {doc[1]}")
            print(f"\nTitle: {doc[0].metadata['headline']}")
