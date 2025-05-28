import pytest
from unittest.mock import AsyncMock, MagicMock
from domain.article import Article
from langchain_core.documents import Document
from repositories.chroma_articles_repo import ChromaArticlesRepo

@pytest.fixture
def sample_articles():
    return [
        Article(
            headline="Title A",
            summary="Summary A",
            content="Full article content A.",
            topics=["politics", "world"],
            political_bias="center"
        ),
        Article(
            headline="Title B",
            summary="Summary B",
            content="Full article content B.",
            topics=["tech"],
            political_bias="left"
        ),
    ]


@pytest.mark.asyncio
async def test_save_async_calls_vector_store_with_correct_documents(sample_articles):
    # Arrange
    mock_chroma = AsyncMock()
    repo = ChromaArticlesRepo(vector_store=mock_chroma)

    # Act
    await repo.save_async(sample_articles)

    # Assert
    mock_chroma.aadd_documents.assert_awaited_once()
    
    # Check that the documents have expected fields
    docs = mock_chroma.aadd_documents.call_args[0][0]
    assert all(isinstance(doc, Document) for doc in docs)
    assert any("Headline: Title A" in doc.page_content for doc in docs)


def test_articles_to_documents_creates_expected_documents(sample_articles):
    # Arrange
    mock_chroma = MagicMock()
    repo = ChromaArticlesRepo(vector_store=mock_chroma)

    # Act
    documents = repo._articles_to_documents(sample_articles)

    # Assert
    assert len(documents) == 2
    assert isinstance(documents[0], Document)
    assert "Headline: Title A" in documents[0].page_content
    assert documents[0].metadata["topics"] == "politics,world"
    assert documents[1].metadata["political_bias"] == "left"


@pytest.mark.asyncio
async def test_query_async_returns_similarity_results():
    # Arrange
    mock_chroma = AsyncMock()
    fake_document = Document(page_content="Example content", metadata={})
    mock_chroma.asimilarity_search_with_score.return_value = [(fake_document, 0.9)]

    repo = ChromaArticlesRepo(vector_store=mock_chroma)

    # Act
    results = await repo.query_async("test query")

    # Assert
    mock_chroma.asimilarity_search_with_score.assert_awaited_once_with("test query")
    assert results == [(fake_document, 0.9)]
