import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from application.services.query_enhancer import QueryEnhancer
from application.exceptions.token_limit_exceeded_error import TokenLimitExceededError


@pytest.fixture
def mock_llm():
    llm = MagicMock()
    llm.__or__.return_value = llm 
    return llm

@pytest.fixture
def mock_prompt():
    prompt = MagicMock()
    prompt.__or__.return_value = prompt
    return prompt

@pytest.fixture
def mock_token_limit_validator():
    validator = MagicMock()
    validator.__or__.return_value = validator
    return validator

@pytest.fixture
def enhancer(mock_llm, mock_prompt, mock_token_limit_validator):
    return QueryEnhancer(llm=mock_llm, prompt=mock_prompt, token_limit_validator=mock_token_limit_validator)


@pytest.mark.asyncio
async def test_enhance_async_returns_original_if_deterministic(enhancer):
    # Arrange
    with patch("config.settings.settings.USE_DETERMINISTIC_QUERY", True):
        # Act
        result = await enhancer.enhance_async("original query")

    # Assert
    assert result == "original query"


@pytest.mark.asyncio
async def test_enhance_async_calls_chain_and_returns_result(enhancer, mock_llm, mock_prompt, mock_token_limit_validator):
    # Arrange
    chain = MagicMock()
    chain.ainvoke = AsyncMock(return_value="enhanced query")

    mock_prompt.__or__.return_value = mock_token_limit_validator
    mock_token_limit_validator.__or__.return_value = mock_llm
    mock_llm.__or__.return_value = chain

    with patch("config.settings.settings.USE_DETERMINISTIC_QUERY", False):
        # Act
        result = await enhancer.enhance_async("user input")

    # Assert
    assert result == "enhanced query"
    chain.ainvoke.assert_called_once_with({"userQuery": "user input"})


@pytest.mark.asyncio
async def test_enhance_async_retries_on_exception(enhancer, mock_llm, mock_prompt, mock_token_limit_validator):
    # Arrange
    chain = MagicMock()
    chain.ainvoke = AsyncMock(side_effect=[Exception("Temporary failure"), "fixed output"])

    mock_prompt.__or__.return_value = mock_token_limit_validator
    mock_token_limit_validator.__or__.return_value = mock_llm
    mock_llm.__or__.return_value = chain

    with patch("config.settings.settings.USE_DETERMINISTIC_QUERY", False):
        # Act
        result = await enhancer.enhance_async("resilient query")

    # Assert
    assert result == "fixed output"
    assert chain.ainvoke.call_count == 2


@pytest.mark.asyncio
async def test_enhance_async_does_not_retry_on_token_limit_exceeded(enhancer, mock_llm, mock_prompt, mock_token_limit_validator):
    # Arrange
    chain = MagicMock()
    chain.ainvoke = AsyncMock(side_effect=TokenLimitExceededError("Too long", max_tokens=4096))

    mock_prompt.__or__.return_value = mock_token_limit_validator
    mock_token_limit_validator.__or__.return_value = mock_llm
    mock_llm.__or__.return_value = chain

    with patch("config.settings.settings.USE_DETERMINISTIC_QUERY", False):
        # Act & Assert
        with pytest.raises(TokenLimitExceededError):
            await enhancer.enhance_async("token bomb")

    assert chain.ainvoke.call_count == 1
