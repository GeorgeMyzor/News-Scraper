import pytest
from unittest.mock import AsyncMock, patch, Mock
from application.services.scrapper import scrap_articles_async

@pytest.mark.asyncio
@patch("application.services.scrapper.httpx.AsyncClient.get")
async def test_scrap_articles_async_success(mock_get):
    # Arrange
    html = """
        <html>
            <head><title>Test Article</title></head>
            <body>
                <article><p>This is a test article content.</p></article>
            </body>
        </html>
    """

    mock_response = Mock()
    mock_response.text = html
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    urls = ["https://example.com/article1", "https://example.com/article2"]

    # Act
    results = await scrap_articles_async(urls)

    # Assert
    assert len(results) == 2
    for title, content in results:
        assert title == "Test Article"
        assert "This is a test article content." in content


@pytest.mark.asyncio
@patch("application.services.scrapper.httpx.AsyncClient.get")
async def test_scrap_articles_async_missing_title_and_article(mock_get):
    # Arrange
    html = """
        <html>
            <body>
                <p>Paragraph 1</p>
                <p>Paragraph 2</p>
            </body>
        </html>
    """
    mock_response = Mock()
    mock_response.text = html
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    urls = ["https://example.com/no-title"]
    
    # Act
    results = await scrap_articles_async(urls)

    # Assert
    assert results[0][0] == "No title found"
    assert "Paragraph 1" in results[0][1]
    assert "Paragraph 2" in results[0][1]


@pytest.mark.asyncio
@patch("application.services.scrapper.httpx.AsyncClient.get")
async def test_scrap_articles_async_http_error(mock_get):
    # Arrange
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = Exception("404 Not Found")
    mock_get.return_value = mock_response

    urls = ["https://example.com/404"]

    # Act & Assert
    with pytest.raises(Exception, match="404 Not Found"):
        await scrap_articles_async(urls)
