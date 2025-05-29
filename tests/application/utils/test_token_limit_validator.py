import pytest
from unittest.mock import MagicMock, patch

from application.utils.token_limit_validator import TokenLimitValidator
from application.exceptions.token_limit_exceeded_error import TokenLimitExceededError
from langchain_core.prompts.chat import ChatPromptValue
from langchain_core.messages import AIMessage, HumanMessage


@pytest.fixture
def mock_encoding():
    encoding = MagicMock()
    encoding.encode.side_effect = lambda s: s.split() 
    return encoding


def test_invoke_within_token_limit(mock_encoding):
    with patch("tiktoken.encoding_for_model", return_value=mock_encoding):
        validator = TokenLimitValidator(max_tokens=10, model_name="gpt-3.5-turbo")

        input = ChatPromptValue(messages=[
            HumanMessage(content="Hello there."),
            AIMessage(content="Hi! How can I help?")
        ])
        
        result = validator.invoke(input)
        assert result == input


def test_invoke_exceeds_token_limit(mock_encoding):
    with patch("tiktoken.encoding_for_model", return_value=mock_encoding):
        validator = TokenLimitValidator(max_tokens=3, model_name="gpt-3.5-turbo")

        input = ChatPromptValue(messages=[
            HumanMessage(content="This is going to break the limit"),
            AIMessage(content="Indeed, it should fail.")
        ])

        with pytest.raises(TokenLimitExceededError) as exc_info:
            validator.invoke(input)

        assert exc_info.value.args[0] == "Input has 11 tokens, which exceeds the limit of 3."
