from langchain_openai import AzureChatOpenAI
from langsmith import traceable
from config.settings import settings
from langchain_core.output_parsers import StrOutputParser
import logging

@traceable
class QueryEnhancer():
    """
    Enhances user queries to be more semantically rich and specific for searching documents.
    Uses an LLM to rewrite the query based on a predefined prompt.
    """
    def __init__(
        self,
        llm: AzureChatOpenAI,
        prompt: str
    ):
        self.llm = llm
        self.prompt = prompt

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
                
        chain = self.prompt | self.llm | StrOutputParser()
        result = await chain.ainvoke({"userQuery": query})
        
        logging.info("Enhanced query: %s", result)

        return result