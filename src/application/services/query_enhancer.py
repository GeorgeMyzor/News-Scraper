import asyncio
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class QueryEnhancer():
    def __init__(
        self,
        llm: AzureChatOpenAI
    ):
        self.llm = llm

    async def enchance_async(self, query: str) -> str:      
        promt = ChatPromptTemplate.from_messages([
            ("user",  "Rewrite this query to make it semantically rich and specific for searching documents. Query: {userQuery}"),
        ])
        message = await promt.ainvoke(query)
        result = await self.llm.ainvoke(message)
        return result.content