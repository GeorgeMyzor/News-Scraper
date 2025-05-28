import asyncio
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from domain.article_enrichment import ArticleEnrichment
from domain.article import Article
from abstractions.summarizer import Summarizer
from langsmith import traceable

@traceable
class AzureAISummarizer(Summarizer):
    """
    Summarizes articles using an Azure OpenAI LLM.
    Uses a structured output schema to enrich the article data.
    """
    def __init__(
        self,
        llm: AzureChatOpenAI,
        prompt_template: ChatPromptTemplate
    ):
        self.llm = llm.with_structured_output(schema=ArticleEnrichment)
        self.prompt = prompt_template

    async def summarize_async(self, articles: list[tuple[str, str]]) -> list[Article]:
        tasks = [
            self._summarize_async(headline, content)
            for headline, content in articles
        ]
        return await asyncio.gather(*tasks)
    
    async def _summarize_async(self, headline: str, content: str) -> Article:
        messages = await self.prompt.ainvoke({"headline": headline, "content": content})

        output = await self.llm.ainvoke(messages)
        article = Article(**output.dict(), headline=headline, content=content)

        return article
