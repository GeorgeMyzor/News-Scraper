from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import AzureChatOpenAI
from repositories.chroma_articles_repo import ChromaArticlesRepo
from application.services.azure_ai_summarizer import AzureAISummarizer
from application.use_cases.summarize_articles_use_case import SummarizeArticlesUseCase
from application.use_cases.query_articles_use_case import QueryArticleUseCase
from application.services.query_enhancer import QueryEnhancer
from abstractions.articles_repo import ArticlesRepo
from abstractions.summarizer import Summarizer
from config.prompts import build_summary_prompt
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
    return QueryEnhancer(llm)

def get_summarizer(llm: Annotated[AzureChatOpenAI, Depends(get_llm)]) -> Summarizer:
    prompt = build_summary_prompt()
    
    return AzureAISummarizer(llm, prompt)

### Services    
def get_query_articles_user_case(
        articles_repo: Annotated[ArticlesRepo, Depends(get_articles_repo)],
        query_enhancer: Annotated[QueryEnhancer, Depends(get_query_enhancer)]
) -> QueryArticleUseCase:
    return QueryArticleUseCase(articles_repo, query_enhancer)

def get_summarize_articles_user_case(
        articles_repo: Annotated[ArticlesRepo, Depends(get_articles_repo)],
        summarizer: Annotated[Summarizer, Depends(get_summarizer)]
) -> SummarizeArticlesUseCase:
    return SummarizeArticlesUseCase(articles_repo, summarizer)
