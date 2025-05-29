import tiktoken
from langchain_core.runnables import Runnable
from langchain_core.runnables.config import RunnableConfig
from langchain_core.prompts.chat import ChatPromptValue
from langchain_core.messages import BaseMessage

from config.settings import settings
from application.exceptions.token_limit_exceeded_error import TokenLimitExceededError

class TokenLimitValidator(Runnable):
    """
    Validates that the token count of a chat prompt does not exceed a specified limit.
    This is useful for ensuring that the input to an LLM does not exceed the model's token limit.
    """
    def __init__(self, max_tokens: int, model_name: str):
        self.max_tokens = max_tokens
        self.encoding = tiktoken.encoding_for_model(model_name)

    def invoke(self, input: ChatPromptValue, config: RunnableConfig = None) -> str:
        """
        Validates the token count of the input chat prompt.
        Args:
            input (ChatPromptValue): The chat prompt containing messages to validate.
            config (RunnableConfig, optional): Configuration for the runnable. Defaults to None.
        Raises:
            TokenLimitExceededError: If the token count exceeds the maximum allowed."""
        messages: list[BaseMessage] = input.messages
        
        combined = " ".join([f"{msg.content}" for msg in messages])

        token_count = len(self.encoding.encode(combined))
        
        if token_count > self.max_tokens:
            raise TokenLimitExceededError(token_count, self.max_tokens)
        
        return input