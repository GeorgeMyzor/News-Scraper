import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from application.services.query_enhancer import QueryEnhancer
from application.exceptions.token_limit_exceeded import TokenLimitExceeded


@pytest.fixture
def mock_llm():
    llm = MagicMock()
    llm.__or__.return_value = llm  # Allow chaining
    return llm

@pytest.fixture
def mock_prompt():
    prompt = MagicMock()
    prompt.__or__.return_value = prompt  # Allow chaining
    return prompt

@pytest.fixture
def mock_token_limit_validator():
    validator = MagicMock()
    validator.__or__.return_value = validator  # Allow chaining
    return validator

@pytest.fixture
def enhancer(mock_llm, mock_prompt, mock_token_limit_validator):
    return QueryEnhancer(llm=mock_llm, prompt=mock_prompt, token_limit_validator=mock_token_limit_validator)


@pytest.mark.asyncio
async def test_enhance_async_returns_original_if_deterministic(enhancer):
    with patch("config.settings.settings.USE_DETERMINISTIC_QUERY", True):
        result = await enhancer.enhance_async("original query")
        assert result == "original query"


@pytest.mark.asyncio
async def test_enhance_async_calls_chain_and_returns_result(enhancer, mock_llm, mock_prompt, mock_token_limit_validator):
    # Set up the chain
    chain = MagicMock()
    chain.ainvoke = AsyncMock(return_value="enhanced query")

    # Simulate full chain
    mock_prompt.__or__.return_value = mock_token_limit_validator
    mock_token_limit_validator.__or__.return_value = mock_llm
    mock_llm.__or__.return_value = chain  # Final chain

    with patch("config.settings.settings.USE_DETERMINISTIC_QUERY", False):
        result = await enhancer.enhance_async("user input")
        assert result == "enhanced query"
        chain.ainvoke.assert_called_once_with({"userQuery": "user input"})


@pytest.mark.asyncio
async def test_enhance_async_retries_on_exception(enhancer, mock_llm, mock_prompt, mock_token_limit_validator):
    chain = MagicMock()
    # First call fails, second succeeds
    chain.ainvoke = AsyncMock(side_effect=[Exception("Temporary failure"), "fixed output"])

    mock_prompt.__or__.return_value = mock_token_limit_validator
    mock_token_limit_validator.__or__.return_value = mock_llm
    mock_llm.__or__.return_value = chain

    with patch("config.settings.settings.USE_DETERMINISTIC_QUERY", False):
        result = await enhancer.enhance_async("resilient query")
        assert result == "fixed output"
        assert chain.ainvoke.call_count == 2


@pytest.mark.asyncio
async def test_enhance_async_does_not_retry_on_token_limit_exceeded(enhancer, mock_llm, mock_prompt, mock_token_limit_validator):
    chain = MagicMock()
    chain.ainvoke = AsyncMock(side_effect=TokenLimitExceeded("Too long", max_tokens=4096))  # Adjust max_tokens as needed

    mock_prompt.__or__.return_value = mock_token_limit_validator
    mock_token_limit_validator.__or__.return_value = mock_llm
    mock_llm.__or__.return_value = chain

    with patch("config.settings.settings.USE_DETERMINISTIC_QUERY", False):
        with pytest.raises(TokenLimitExceeded):
            await enhancer.enhance_async("token bomb")
        assert chain.ainvoke.call_count == 1