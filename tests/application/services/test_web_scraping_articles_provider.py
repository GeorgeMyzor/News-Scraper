import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from application.services.web_scraping_articles_provider import WebScrapingArticlesProvider

# Enable asyncio test support
pytestmark = pytest.mark.asyncio


@pytest.fixture
def provider():
    return WebScrapingArticlesProvider()


async def test_get_async_aggregates_results(provider):
    urls = ['http://example.com/1', 'http://example.com/2']
    
    # Patch the _scrap_article_async method
    with patch.object(provider, '_scrap_article_async', side_effect=[
        {"headline": "Title 1", "content": "Content 1"},
        {"headline": "Title 2", "content": "Content 2"},
    ]) as mock_scrap:
        results = await provider.get_async(urls)
        assert results == [
            {"headline": "Title 1", "content": "Content 1"},
            {"headline": "Title 2", "content": "Content 2"}
        ]
        assert mock_scrap.call_count == 2


async def test__scrap_article_async_with_article_tag(provider):
    html = '''
    <html>
        <head><title>Sample Title</title></head>
        <body>
            <article>
                <p>Paragraph 1.</p>
                <p>Paragraph 2.</p>
            </article>
        </body>
    </html>
    '''

    response_mock = MagicMock()
    response_mock.text = html
    response_mock.raise_for_status = MagicMock()

    async def mock_get(*args, **kwargs):
        return response_mock

    with patch('httpx.AsyncClient.get', new=mock_get):
        result = await provider._scrap_article_async("http://example.com")
        assert result["headline"] == "Sample Title"
        assert "Paragraph 1." in result["content"]
        assert "Paragraph 2." in result["content"]


async def test__scrap_article_async_with_no_title_and_no_article(provider):
    html = '''
    <html>
        <body>
            <main>
                <p>Only paragraph in main tag.</p>
            </main>
        </body>
    </html>
    '''

    response_mock = MagicMock()
    response_mock.text = html
    response_mock.raise_for_status = MagicMock()

    async def mock_get(*args, **kwargs):
        return response_mock

    with patch('httpx.AsyncClient.get', new=mock_get):
        result = await provider._scrap_article_async("http://example.com")
        assert result["headline"] == "No title found"
        assert "Only paragraph in main tag." in result["content"]
