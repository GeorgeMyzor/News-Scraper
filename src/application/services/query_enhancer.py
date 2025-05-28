from langchain_openai import AzureChatOpenAI
from src.config.prompts import build_query_enhancement_prompt
from langsmith import traceable
from src.config.settings import settings

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

    async def enchance_async(self, query: str) -> str: 
        """
        Enhances the given query using an LLM.
        Args:
            query (str): The original search query input by the user.
        Returns:
            str: The enhanced query that is more semantically rich and specific.
        """ 
        if settings.USE_DETERMINISTIC_QUERY:
            return query    
        
        promt = build_query_enhancement_prompt()
        message = await promt.ainvoke(query)
        result = await self.llm.ainvoke(message)

        return result.content