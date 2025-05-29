from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import AzureChatOpenAI
from langchain.text_splitter import TokenTextSplitter
from langchain_core.language_models.chat_models import BaseChatModel
from typing import Annotated
from fastapi import Depends
from langchain_core.rate_limiters import InMemoryRateLimiter

from abstractions.articles_repo import ArticlesRepo
from abstractions.summarizer import Summarizer
from abstractions.articles_provider import ArticlesProvider
from application.services.azure_ai_summarizer import AzureAISummarizer
from application.use_cases.summarize_articles_use_case import SummarizeArticlesUseCase
from application.use_cases.query_articles_use_case import QueryArticleUseCase
from application.services.query_enhancer import QueryEnhancer
from application.services.web_scraping_articles_provider import WebScrapingArticlesProvider
from config.prompts import build_summary_prompt, build_chunk_summary_prompt, build_query_enhancement_prompt
from config.settings import settings
from repositories.chroma_articles_repo import ChromaArticlesRepo
from application.utils.token_limit_validator import TokenLimitValidator

### Vectore Stores
def get_embeddings():
    return HuggingFaceEmbeddings(model_name=settings.HUGGINGFACE_MODEL_NAME)

def get_chroma(embeddings: Annotated[HuggingFaceEmbeddings, Depends(get_embeddings)]) -> Chroma: 
    return Chroma(
        collection_name=settings.ARTICLES_COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=settings.CHROMA_PERSIST_DIRECTORY,
        
    )

def get_articles_repo(
    chroma_vectore_store: Annotated[Chroma, Depends(get_chroma)],
) -> ArticlesRepo:
    return ChromaArticlesRepo(chroma_vectore_store)

### LLM
def get_llm() -> BaseChatModel:
    rate_limiter = InMemoryRateLimiter(
        requests_per_second=10, # 10 per second
        check_every_n_seconds=0.1,  # Wake up every 100 ms to check whether allowed to make a request
        max_bucket_size=10,  # Controls the maximum burst size
    )
    return AzureChatOpenAI(
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        azure_deployment=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
        openai_api_version=settings.AZURE_OPENAI_API_VERSION,
        temperature=0.3,
        rate_limiter=rate_limiter
    )

def get_query_token_validator() -> TokenLimitValidator:
    return TokenLimitValidator(max_tokens=settings.QUERY_TOKEN_LIMIT,model_name=settings.AZURE_OPENAI_DEPLOYMENT_NAME)

def get_query_enhancer(
    llm: Annotated[AzureChatOpenAI, Depends(get_llm)],
    token_limit_validator: Annotated[TokenLimitValidator, Depends(get_query_token_validator)]
):    
    prompt = build_query_enhancement_prompt()
    
    return QueryEnhancer(llm, prompt, token_limit_validator)

def get_summary_token_validator() -> TokenLimitValidator:
    return TokenLimitValidator(max_tokens=settings.MAX_TOKEN_LIMIT,model_name=settings.AZURE_OPENAI_DEPLOYMENT_NAME)

def get_token_text_splitter() -> TokenTextSplitter:
    return TokenTextSplitter(model_name=settings.AZURE_OPENAI_DEPLOYMENT_NAME, chunk_size=settings.CHUNK_TOKEN_LIMIT, chunk_overlap=50)

def get_summarizer(
    llm: Annotated[BaseChatModel, Depends(get_llm)],
    token_text_splitter: Annotated[TokenTextSplitter, Depends(get_token_text_splitter)],
    token_limit_validator: Annotated[TokenLimitValidator, Depends(get_summary_token_validator)]
    ) -> Summarizer:
    summary_prompt = build_summary_prompt()
    chunk_summary_prompt = build_chunk_summary_prompt()
    
    return AzureAISummarizer(llm, summary_prompt, chunk_summary_prompt, token_text_splitter, token_limit_validator)

### Services    
def get_articles_provider() -> ArticlesProvider:
    return WebScrapingArticlesProvider()

def get_query_articles_user_case(
        articles_repo: Annotated[ArticlesRepo, Depends(get_articles_repo)],
        query_enhancer: Annotated[QueryEnhancer, Depends(get_query_enhancer)]
) -> QueryArticleUseCase:
    return QueryArticleUseCase(articles_repo, query_enhancer)

def get_summarize_articles_user_case(
        articles_repo: Annotated[ArticlesRepo, Depends(get_articles_repo)],
        summarizer: Annotated[Summarizer, Depends(get_summarizer)],
        articles_provider: Annotated[ArticlesProvider, Depends(get_articles_provider)],
) -> SummarizeArticlesUseCase:
    return SummarizeArticlesUseCase(articles_repo, summarizer, articles_provider)
