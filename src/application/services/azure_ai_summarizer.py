import asyncio
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from src.domain.article_enriched import ArticleEnriched
from src.domain.article_data import ArticleData
from src.abstractions.summarizer import Summarizer

class AzureAISummarizer(Summarizer):
    def __init__(
        self,
        llm: AzureChatOpenAI,
        prompt_template: ChatPromptTemplate
    ):
        self.llm = llm.with_structured_output(schema=ArticleEnriched)
        self.prompt = prompt_template

    async def summarize_async(self, articles: list[tuple[str, str]]) -> list[ArticleData]:
        tasks = [
            self._summarize_async(headline, content)
            for headline, content in articles
        ]
        return await asyncio.gather(*tasks)
    
    async def _summarize_async(self, headline: str, content: str) -> ArticleData:
        messages = await self.prompt.ainvoke({"headline": headline, "content": content})

        output = await self.llm.ainvoke(messages)
        article = ArticleData(**output.dict(), headline=headline, content=content)

        return article
