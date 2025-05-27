from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langsmith import traceable

from src.domain.article import Article
from src.abstrations.summarizer import Summarizer

class AzureAISummarizer(Summarizer):
    def __init__(
        self,
        llm: AzureChatOpenAI,
        prompt_template: ChatPromptTemplate
    ):
        self.llm = llm.with_structured_output(schema=Article)
        self.prompt = prompt_template

    @traceable
    def summarize(self, headline: str, content: str) -> Article:
        messages = self.prompt.invoke({"headline": headline, "content": content})

        article = self.llm.invoke(messages)
        article.headline = headline
        article.content = content

        return article
