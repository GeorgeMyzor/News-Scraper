import logging
from langchain_openai import AzureChatOpenAI
from langsmith import traceable
from langchain_core.output_parsers import StrOutputParser
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_not_exception_type

from config.settings import settings
from application.exceptions.token_limit_exceeded import TokenLimitExceeded
from application.utils.token_limit_validator import TokenLimitValidator

@traceable
class QueryEnhancer():
    """
    Enhances user queries to be more semantically rich and specific for searching documents.
    Uses an LLM to rewrite the query based on a predefined prompt.
    """
    def __init__(
        self,
        llm: AzureChatOpenAI,
        prompt: str,        
        token_limit_validator: TokenLimitValidator
    ):
        self.llm = llm
        self.prompt = prompt
        self.token_limit_validator = token_limit_validator

    @retry(
        wait=wait_exponential(multiplier=1, min=1, max=5), 
        stop=stop_after_attempt(2),
        retry=retry_if_not_exception_type(TokenLimitExceeded)
    )
    async def enhance_async(self, query: str) -> str: 
        """
        Enhances the input query to make it semantically rich and specific for searching articles.
        Args:
            query (str): The original user query to enhance.
        Returns:
            str: The enhanced query ready for searching articles.
        """
        if settings.USE_DETERMINISTIC_QUERY:
            return query    
        
        logging.info("Enhancing query: %s", query)
                
        chain = self.prompt | self.token_limit_validator | self.llm | StrOutputParser()
        result = await chain.ainvoke({"userQuery": query})
        
        logging.info("Enhanced query: %s", result)

        return result