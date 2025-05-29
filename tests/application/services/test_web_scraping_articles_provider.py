import pytest
from unittest.mock import AsyncMock, MagicMock, PropertyMock
from application.services.web_scraping_articles_provider import WebScrapingArticlesProvider, is_valid_article
from application.exceptions.no_content_error import NoContentError


VALID_HTML = """
<html>
<head><title>Test Title</title></head>
<body>
<article>
    <p>This is a test sentence. Another sentence. And a third. Fourth sentence. Finally, the fifth sentence.</p>
    <p>{}</p>
</article>
</body>
</html>
""".format("Word " * 100)

INVALID_HTML = "<html><body><p>Too short</p></body></html>"


@pytest.mark.asyncio
async def test_get_async_returns_valid_articles(monkeypatch):
    # Arrange
    provider = WebScrapingArticlesProvider()
    url = "http://example.com"
    
    mock_response = MagicMock()
    type(mock_response).text = PropertyMock(return_value=VALID_HTML)
    mock_response.raise_for_status = MagicMock()

    async def mock_get(*args, **kwargs):
        return mock_response
    
    async_client_mock = MagicMock()
    async_client_mock.__aenter__.return_value = async_client_mock
    async_client_mock.__aexit__.return_value = None
    async_client_mock.get = AsyncMock(side_effect=mock_get)
    
    monkeypatch.setattr("httpx.AsyncClient", MagicMock(return_value=async_client_mock))
    
    # Act
    result = await provider.get_async([url])

    # Assert
    assert len(result) == 1
    assert result[0]["headline"] == "Test Title"
    assert "Word" in result[0]["content"]


@pytest.mark.asyncio
async def test_get_async_raises_no_content_error(monkeypatch):
    # Arrange
    provider = WebScrapingArticlesProvider()
    url = "http://example.com/invalid"
    
    mock_response = MagicMock()
    type(mock_response).text = PropertyMock(return_value=INVALID_HTML)
    mock_response.raise_for_status = MagicMock()

    async def mock_get(*args, **kwargs):
        return mock_response
    
    async_client_mock = MagicMock()
    async_client_mock.__aenter__.return_value = async_client_mock
    async_client_mock.__aexit__.return_value = None
    async_client_mock.get = AsyncMock(side_effect=mock_get)
    
    monkeypatch.setattr("httpx.AsyncClient", MagicMock(return_value=async_client_mock))
    
    # Act & Assert
    with pytest.raises(NoContentError) as exc:
        await provider.get_async([url])
    
    assert url in str(exc.value)


def test_is_valid_article_true():
    # Arrange
    text = "This sentence. " * 6 + "word " * 100

    # Act
    result = is_valid_article(text)

    # Assert
    assert result


def test_is_valid_article_false_word_count():
    # Arrange
    text = "This is a short article. Just some text. Not enough."

    # Act
    result = not is_valid_article(text)

    # Assert
    assert result


def test_is_valid_article_false_sentence_count():
    # Arrange
    text = "word " * 200

    # Act
    result = not is_valid_article(text)

    # Assert
    assert result