import pytest
from unittest.mock import AsyncMock, MagicMock

from application.services.azure_ai_summarizer import AzureAISummarizer
from application.exceptions.token_limit_exceeded_error import TokenLimitExceededError
from domain.article_enriched import ArticleEnriched


@pytest.fixture
def mock_llm():
    llm = MagicMock()
    llm.with_structured_output.return_value = llm 
    return llm

@pytest.fixture
def mock_token_validator():
    return MagicMock()

@pytest.fixture
def mock_prompt():
    return MagicMock()

@pytest.fixture
def mock_text_splitter():
    splitter = MagicMock()
    splitter.split_text.side_effect = lambda text: text.split("\n\n") 
    return splitter

@pytest.fixture
def summarizer(mock_llm, mock_prompt, mock_token_validator, mock_text_splitter):
    return AzureAISummarizer(
        llm=mock_llm,
        summary_prompt=mock_prompt,
        chunk_summary_prompt=mock_prompt,
        token_text_splitter=mock_text_splitter,
        token_limit_validator=mock_token_validator
    )


@pytest.mark.asyncio
async def test_summarize_async_single_chunk(summarizer):
    # Arrange
    summarizer.text_splitter.split_text = MagicMock(return_value=["Only one chunk"])
    mock_summary_chain = MagicMock()
    mock_result = MagicMock(spec=ArticleEnriched, headline="Title", content="Original")
    mock_summary_chain.ainvoke = AsyncMock(return_value=mock_result)
    summarizer.summary_chain = mock_summary_chain
    articles = [{"headline": "Title", "content": "Only one chunk"}]

    # Act
    result = await summarizer.summarize_async(articles)

    # Assert
    assert len(result) == 1
    assert result[0] == mock_result


@pytest.mark.asyncio
async def test_summarize_async_multiple_chunks(summarizer):
    # Arrange
    summarizer.text_splitter.split_text = MagicMock(return_value=["chunk1", "chunk2"])

    mock_chunk_chain = MagicMock()
    mock_chunk_chain.abatch = AsyncMock(return_value=["summary1", "summary2"])
    summarizer.chunk_chain = mock_chunk_chain

    mock_summary_chain = MagicMock()
    final_result = MagicMock(spec=ArticleEnriched, headline="My Title", content="Original content")
    mock_summary_chain.ainvoke = AsyncMock(return_value=final_result)
    summarizer.summary_chain = mock_summary_chain

    articles = [{"headline": "My Title", "content": "chunk1\n\nchunk2"}]

    # Act
    result = await summarizer.summarize_async(articles)

    # Assert
    assert result[0] == final_result
    mock_chunk_chain.abatch.assert_awaited_once()
    mock_summary_chain.ainvoke.assert_awaited_once()


@pytest.mark.asyncio
async def test_summarize_async_handles_token_limit_exceeded(summarizer):
    # Arrange
    summarizer.text_splitter.split_text = MagicMock(return_value=["chunk1", "chunk2"])

    mock_chunk_chain = MagicMock()
    mock_chunk_chain.abatch = AsyncMock(return_value=["summary1", "summary2"])
    summarizer.chunk_chain = mock_chunk_chain

    mock_summary_chain = MagicMock()
    mock_summary_chain.ainvoke = AsyncMock(side_effect=TokenLimitExceededError("too long", max_tokens=4096))
    summarizer.summary_chain = mock_summary_chain

    articles = [{"headline": "Retry Me", "content": "chunk1\n\nchunk2"}]

    # Act & Assert
    with pytest.raises(TokenLimitExceededError):
        await summarizer.summarize_async(articles)

    assert mock_summary_chain.ainvoke.call_count == 1 


@pytest.mark.asyncio
async def test_summarize_async_multiple_articles(summarizer):
    # Arrange
    summarizer.text_splitter.split_text = MagicMock(return_value=["chunk"])

    mock_summary_chain = MagicMock()
    mock_summary_chain.ainvoke = AsyncMock(side_effect=[
        MagicMock(spec=ArticleEnriched, headline="H1", content="C1"),
        MagicMock(spec=ArticleEnriched, headline="H2", content="C2")
    ])
    summarizer.summary_chain = mock_summary_chain

    summarizer.chunk_chain.abatch = AsyncMock(return_value=["summary"])

    articles = [
        {"headline": "H1", "content": "chunk"},
        {"headline": "H2", "content": "chunk"}
    ]

    # Act
    result = await summarizer.summarize_async(articles)

    # Assert
    assert len(result) == 2
    assert result[0].headline == "H1"
    assert result[1].headline == "H2"
