import pytest
import asyncio
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from application.services.azure_ai_summarizer1 import AzureAISummarizer
from domain.article_query import ArticleQuery
from config.settings import settings
from config.prompts import build_summary_prompt

@pytest.mark.integration
@pytest.mark.asyncio
async def test_summarize_single_article_real_llm():
    # Use your real Azure OpenAI LLM setup here:
    llm = AzureChatOpenAI(
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        azure_deployment=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
        openai_api_version=settings.AZURE_OPENAI_API_VERSION,
        temperature=0.3
    )

    # Create a prompt template that matches ArticleEnrichment schema
    # Replace with your real prompt or import from your config
    prompt_template = build_summary_prompt()

    summarizer = AzureAISummarizer(llm, prompt_template)

    articles = [("Breaking News", "The economy is growing steadily this quarter.")]

    result = await summarizer.summarize_async(articles)

    assert isinstance(result, list)
    assert len(result) == 1
    article = result[0]
    assert isinstance(article, ArticleQuery)
    assert article.headline == "Breaking News"
    assert article.summary is not None
    assert hasattr(article, "topics")  # Depending on your Article model

@pytest.mark.integration
@pytest.mark.asyncio
async def test_summarize_multiple_articles_real_llm():
    llm = AzureChatOpenAI(
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        azure_deployment=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
        openai_api_version=settings.AZURE_OPENAI_API_VERSION,
        temperature=0.3
    )

    prompt_template = build_summary_prompt()

    summarizer = AzureAISummarizer(llm, prompt_template)

    articles = [
        ("Breaking News", "The economy is growing steadily this quarter."),
        ("Breaking News", "Covid outbreak (again)."),
    ]

    results = await summarizer.summarize_async(articles)

    assert isinstance(results, list)
    assert len(results) == 2
    for article in results:
        assert isinstance(article, ArticleQuery)
        assert article.summary is not None
