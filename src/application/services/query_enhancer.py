from langchain_openai import AzureChatOpenAI
from src.config.prompts import build_query_enhancement_prompt
from langsmith import traceable

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
        promt = build_query_enhancement_prompt()
        message = await promt.ainvoke(query)
        result = await self.llm.ainvoke(message)

        return result.content