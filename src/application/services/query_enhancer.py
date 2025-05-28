from langchain_openai import AzureChatOpenAI
from config.prompts import build_query_enhancement_prompt
from langsmith import traceable
from config.settings import settings
import logging

@traceable
class QueryEnhancer():
    """
    Enhances user queries to be more semantically rich and specific for searching documents.
    Uses an LLM to rewrite the query based on a predefined prompt.
    """
    def __init__(
        self,
        llm: AzureChatOpenAI
    ):
        self.llm = llm

    async def enhance_async(self, query: str) -> str: 
        """
        Enhances the given query using an LLM.
        Args:
            query (str): The original search query input by the user.
        Returns:
            str: The enhanced query that is more semantically rich and specific.
        """ 
        if settings.USE_DETERMINISTIC_QUERY:
            return query    
        
        logging.info("Enhancing query: %s", query)
        
        promt = build_query_enhancement_prompt()
        message = await promt.ainvoke(query)
        result = await self.llm.ainvoke(message)
        
        logging.info("Enhanced query: %s", result.content)

        return result.content