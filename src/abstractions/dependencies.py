from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import AzureChatOpenAI
from repositories.chroma_articles_repo import ChromaArticlesRepo
from langchain.text_splitter import TokenTextSplitter
from application.services.azure_ai_summarizer import AzureAISummarizer
from application.use_cases.summarize_articles_use_case import SummarizeArticlesUseCase
from application.use_cases.query_articles_use_case import QueryArticleUseCase
from application.services.query_enhancer import QueryEnhancer
from abstractions.articles_repo import ArticlesRepo
from abstractions.summarizer import Summarizer
from abstractions.articles_provider import ArticlesProvider
from application.services.web_scraping_articles_provider import WebScrapingArticlesProvider
from config.prompts import build_summary_prompt, build_chunk_summary_prompt, build_query_enhancement_prompt
from config.settings import settings
from typing import Annotated
from fastapi import Depends

### Vectore Stores
def get_embeddings():
    return HuggingFaceEmbeddings(model_name=settings.HUGGINGFACE_MODEL_NAME)

def get_chroma(embeddings: Annotated[HuggingFaceEmbeddings, Depends(get_embeddings)]) -> Chroma: 
    return Chroma(
        collection_name=settings.ARTICLES_COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=settings.CHROMA_PERSIST_DIRECTORY
    )

def get_articles_repo(
    chroma_vectore_store: Annotated[Chroma, Depends(get_chroma)],
) -> ArticlesRepo:
    return ChromaArticlesRepo(chroma_vectore_store)

### LLM
def get_llm() -> AzureChatOpenAI:
    return AzureChatOpenAI(
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        azure_deployment=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
        openai_api_version=settings.AZURE_OPENAI_API_VERSION,
        temperature=0.3
    )

def get_query_enhancer(llm: Annotated[AzureChatOpenAI, Depends(get_llm)]):    
    prompt = build_query_enhancement_prompt()
    
    return QueryEnhancer(llm, prompt)

def get_token_text_splitter() -> TokenTextSplitter:
    return TokenTextSplitter(model_name=settings.AZURE_OPENAI_DEPLOYMENT_NAME, chunk_size=1000, chunk_overlap=50)

def get_summarizer(
    llm: Annotated[AzureChatOpenAI, Depends(get_llm)],
    token_text_splitter: Annotated[TokenTextSplitter, Depends(get_token_text_splitter)]
    ) -> Summarizer:
    summary_prompt = build_summary_prompt()
    chunk_summary_prompt = build_chunk_summary_prompt()
    
    return AzureAISummarizer(llm, summary_prompt, chunk_summary_prompt, token_text_splitter)

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
