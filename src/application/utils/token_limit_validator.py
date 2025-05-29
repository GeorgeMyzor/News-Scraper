import tiktoken
from langchain_core.runnables import Runnable
from langchain_core.runnables.config import RunnableConfig
from langchain_core.prompts.chat import ChatPromptValue
from langchain_core.messages import BaseMessage

from config.settings import settings
from application.exceptions.token_limit_exceeded import TokenLimitExceeded

class TokenLimitValidator(Runnable):
    def __init__(self, max_tokens: int, model_name: str):
        self.max_tokens = max_tokens
        self.encoding = tiktoken.encoding_for_model(model_name)

    def invoke(self, input: ChatPromptValue, config: RunnableConfig = None) -> str:
        messages: list[BaseMessage] = input.messages
        
        combined = " ".join([f"{msg.content}" for msg in messages])

        token_count = len(self.encoding.encode(combined))
        
        if token_count > self.max_tokens:
            raise TokenLimitExceeded(token_count, self.max_tokens)
        
        return input