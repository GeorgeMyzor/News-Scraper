import pytest
from unittest.mock import AsyncMock, patch

from application.models.article_summary_dto import ArticleSummaryDTO
from application.use_cases.summarize_articles_use_case import SummarizeArticlesUseCase
from domain.article_query import ArticleQuery


@pytest.mark.asyncio
@patch("application.use_cases.summarize_articles_use_case.scrap_articles_async")
async def test_summarize_articles_use_case_happy_path(mock_scrap_articles):
    # Arrange
    urls = ["http://example.com/article1", "http://example.com/article2"]
    
    # Mock scrapped articles returned from scrap_articles_async
    scrapped_articles = ["raw article 1", "raw article 2"]
    mock_scrap_articles.return_value = scrapped_articles
    
    # Mock summarizer with summarize_async method
    mock_summarizer = AsyncMock()
    # Summarizer returns list of Article domain objects
    article1 = ArticleQuery(headline="Title 1", content="Summary 1", summary="This is a summary of article 1.")
    article2 = ArticleQuery(headline="Title 2", content="Summary 2", summary="This is a summary of article 2.")
    mock_summarizer.summarize_async.return_value = [article1, article2]
    
    # Mock repo with save_async method
    mock_repo = AsyncMock()
    use_case = SummarizeArticlesUseCase(repo=mock_repo, summarizer=mock_summarizer)
    
    # Act
    results = await use_case(urls)
    
    # Assert
    mock_scrap_articles.assert_awaited_once_with(urls)
    mock_summarizer.summarize_async.assert_awaited_once_with(scrapped_articles)
    mock_repo.save_async.assert_awaited_once_with([article1, article2])
    
    # Check results are list of ArticleSummaryDTO with correct data
    assert isinstance(results, list)
    assert all(isinstance(r, ArticleSummaryDTO) for r in results)
    assert results[0].headline == article1.headline
    assert results[1].headline == article2.headline


@pytest.mark.asyncio
@patch("application.use_cases.summarize_articles_use_case.scrap_articles_async")
async def test_summarize_articles_use_case_empty_urls(mock_scrap_articles):
    # Arrange
    urls = []
    mock_scrap_articles.return_value = []
    mock_summarizer = AsyncMock()
    mock_summarizer.summarize_async.return_value = []
    mock_repo = AsyncMock()
    use_case = SummarizeArticlesUseCase(repo=mock_repo, summarizer=mock_summarizer)
    
    # Act
    results = await use_case(urls)
    
    # Assert
    mock_scrap_articles.assert_awaited_once_with(urls)
    mock_summarizer.summarize_async.assert_awaited_once_with([])
    mock_repo.save_async.assert_awaited_once_with([])
    assert results == []

@pytest.mark.asyncio
@patch("application.use_cases.summarize_articles_use_case.scrap_articles_async")
async def test_summarize_articles_use_case_partial_failure_in_scrap(mock_scrap_articles):
    # Arrange
    urls = ["http://valid.com", "http://fail.com"]
    mock_scrap_articles.return_value = ["valid article content", None]

    mock_summarizer = AsyncMock()
    # Summarizer should only get valid articles (depends on your logic, adjust accordingly)
    mock_summarizer.summarize_async.return_value = [ArticleQuery(headline="Valid", content="Content", summary="Summary")]

    mock_repo = AsyncMock()

    use_case = SummarizeArticlesUseCase(repo=mock_repo, summarizer=mock_summarizer)

    # Act
    results = await use_case(urls)

    # Assert
    mock_scrap_articles.assert_awaited_once_with(urls)
    mock_summarizer.summarize_async.assert_awaited_once()
    mock_repo.save_async.assert_awaited_once()
    
    assert len(results) == 1
    assert isinstance(results[0], ArticleSummaryDTO)


@pytest.mark.asyncio
@patch("application.use_cases.summarize_articles_use_case.scrap_articles_async")
async def test_summarize_articles_use_case_summarizer_raises_exception(mock_scrap_articles):
    # Arrange
    urls = ["http://example.com"]
    mock_scrap_articles.return_value = ["article content"]

    mock_summarizer = AsyncMock()
    mock_summarizer.summarize_async.side_effect = Exception("Summarization failed")

    mock_repo = AsyncMock()

    use_case = SummarizeArticlesUseCase(repo=mock_repo, summarizer=mock_summarizer)

    # Act & Assert
    with pytest.raises(Exception, match="Summarization failed"):
        await use_case(urls)

    mock_scrap_articles.assert_awaited_once_with(urls)
    mock_summarizer.summarize_async.assert_awaited_once()
    mock_repo.save_async.assert_not_called()


@pytest.mark.asyncio
@patch("application.use_cases.summarize_articles_use_case.scrap_articles_async")
async def test_summarize_articles_use_case_repo_raises_exception(mock_scrap_articles):
    # Arrange
    urls = ["http://example.com"]
    mock_scrap_articles.return_value = ["article content"]

    mock_summarizer = AsyncMock()
    article = ArticleQuery(headline="Headline", content="Summary", summary="This is a summary.")
    mock_summarizer.summarize_async.return_value = [article]

    mock_repo = AsyncMock()
    mock_repo.save_async.side_effect = Exception("Database save failed")

    use_case = SummarizeArticlesUseCase(repo=mock_repo, summarizer=mock_summarizer)

    # Act & Assert
    with pytest.raises(Exception, match="Database save failed"):
        await use_case(urls)

    mock_scrap_articles.assert_awaited_once_with(urls)
    mock_summarizer.summarize_async.assert_awaited_once()
    mock_repo.save_async.assert_awaited_once()


@pytest.mark.asyncio
@patch("application.use_cases.summarize_articles_use_case.scrap_articles_async")
async def test_summarize_articles_use_case_handles_empty_scraped_article(mock_scrap_articles):
    # Arrange
    urls = ["http://example.com"]
    # scrap returns empty string or whitespace
    mock_scrap_articles.return_value = ["   "]

    mock_summarizer = AsyncMock()
    mock_summarizer.summarize_async.return_value = []

    mock_repo = AsyncMock()

    use_case = SummarizeArticlesUseCase(repo=mock_repo, summarizer=mock_summarizer)

    # Act
    results = await use_case(urls)

    # Assert
    assert results == []