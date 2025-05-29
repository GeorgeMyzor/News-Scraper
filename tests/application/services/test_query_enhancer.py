import pytest

from application.services.query_enhancer import QueryEnhancer
from langchain_openai import AzureChatOpenAI
from config.settings import settings


@pytest.mark.integration
@pytest.mark.asyncio
async def test_query_enhancer_returns_enhanced_query():
    # Arrange
    llm = AzureChatOpenAI(
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        azure_deployment=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
        openai_api_version=settings.AZURE_OPENAI_API_VERSION,
        temperature=0.3
    )
    enhancer = QueryEnhancer(llm)

    original_query = "climate change effects"

    # Act
    enhanced_query = await enhancer.enhance_async(original_query)

    # Assert
    assert isinstance(enhanced_query, str)
    assert len(enhanced_query) > 0
    assert enhanced_query != original_query or settings.USE_DETERMINISTIC_QUERY is True

@pytest.mark.integration
@pytest.mark.asyncio
async def test_query_enhancer_deterministic_mode(monkeypatch):
    # Arrange
    monkeypatch.setattr(settings, "USE_DETERMINISTIC_QUERY", True)

    llm = AzureChatOpenAI(
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        azure_deployment=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
        openai_api_version=settings.AZURE_OPENAI_API_VERSION,
        temperature=0.3
    )
    enhancer = QueryEnhancer(llm)
    query = "AI in healthcare"

    # Act
    enhanced = await enhancer.enhance_async(query)

    # Assert
    assert enhanced == query
