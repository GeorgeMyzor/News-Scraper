from typing import Annotated
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from src.repositories.chroma_articles_repo import ChromaArticlesRepo
from src.use_cases.summarizers.azure_ai_summarizer import AzureAISummarizer
from src.use_cases.summarize_articles_use_case import SummarizeArticlesUseCase
from src.use_cases.query_articles_use_case import QueryArticleUseCase
from src.abstrations.use_case import UseCase
from src.abstrations.articles_repo import ArticlesRepo
from src.abstrations.summarizer import Summarizer
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.config.settings import settings

### Database
def build_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

def build_chroma() -> Chroma: 
    return Chroma(
        collection_name="articles",
        embedding_function=build_embeddings(),
        persist_directory="./chroma_db"
    )

def build_articles_repo() -> ArticlesRepo:
    vector_store = build_chroma()

    return ChromaArticlesRepo(vector_store)


### LLM
def build_prompt() -> ChatPromptTemplate:
    system_template = """
        You are a helpful assistant that summarizes news articles.
        Only extract relevant information from the text. 
        If you do not know the value of an attribute asked to extract, 
        return null for the attribute's value.
    """
    user_template = """
        Summarize the following news article:
        Headline: {headline}
        Content: {content}
    """
    return ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("user",   user_template),
    ])

def build_llm() -> AzureChatOpenAI:
    return AzureChatOpenAI(
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        azure_deployment=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
        openai_api_version=settings.AZURE_OPENAI_API_VERSION,
    )

def build_summarizer() -> Summarizer:
    llm = build_llm()    
    prompt = build_prompt()
    
    return AzureAISummarizer(llm, prompt)

### Services
def get_use_case(are_urls: bool) -> UseCase:
    repo = build_articles_repo()

    if are_urls:
        summarizer = build_summarizer()

        return SummarizeArticlesUseCase(repo, summarizer)
    else:
        return QueryArticleUseCase(repo)
