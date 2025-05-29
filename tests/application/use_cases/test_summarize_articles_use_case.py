import pytest
from unittest.mock import AsyncMock, MagicMock
from application.use_cases.summarize_articles_use_case import SummarizeArticlesUseCase
from domain.article_enriched import ArticleEnriched
from application.models.article_summary_dto import ArticleSummaryDTO


@pytest.fixture
def mock_repo():
    repo = MagicMock()
    repo.save_async = AsyncMock()
    return repo


@pytest.fixture
def mock_articles_provider():
    provider = MagicMock()
    provider.get_async = AsyncMock()
    return provider


@pytest.fixture
def mock_summarizer():
    summarizer = MagicMock()
    summarizer.summarize_async = AsyncMock()
    return summarizer


@pytest.fixture
def use_case(mock_repo, mock_summarizer, mock_articles_provider):
    return SummarizeArticlesUseCase(
        repo=mock_repo,
        summarizer=mock_summarizer,
        articles_provider=mock_articles_provider
    )


@pytest.mark.asyncio
async def test_use_case_executes_full_pipeline(use_case, mock_articles_provider, mock_summarizer, mock_repo):
    urls = ["https://example.com/article1", "https://example.com/article2"]

    # Mock article scraping result
    scrapped = [("Title1", "Content1"), ("Title2", "Content2")]
    mock_articles_provider.get_async.return_value = scrapped

    # Mock summarizer output
    enriched = [
        ArticleEnriched(headline="Title1", content="Content1", summary="Summary1"),
        ArticleEnriched(headline="Title2", content="Content2", summary="Summary2")
    ]
    mock_summarizer.summarize_async.return_value = enriched

    # Act
    result = await use_case(urls)

    # Assert
    mock_articles_provider.get_async.assert_awaited_once_with(urls)
    mock_summarizer.summarize_async.assert_awaited_once_with(scrapped)
    mock_repo.save_async.assert_awaited_once_with(enriched)

    assert all(isinstance(dto, ArticleSummaryDTO) for dto in result)
    assert result[0].headline == "Title1"
    assert result[0].summary == "Summary1"


@pytest.mark.asyncio
async def test_use_case_handles_empty_url_list(use_case, mock_articles_provider, mock_summarizer, mock_repo):
    mock_articles_provider.get_async.return_value = []
    mock_summarizer.summarize_async.return_value = []

    result = await use_case([])

    mock_articles_provider.get_async.assert_awaited_once_with([])
    mock_summarizer.summarize_async.assert_awaited_once_with([])
    mock_repo.save_async.assert_awaited_once_with([])

    assert result == []
