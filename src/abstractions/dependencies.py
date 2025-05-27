from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.repositories.chroma_articles_repo import ChromaArticlesRepo
from src.application.services.azure_ai_summarizer import AzureAISummarizer
from src.application.use_cases.summarize_articles_use_case import SummarizeArticlesUseCase
from src.application.use_cases.query_articles_use_case import QueryArticleUseCase
from src.application.services.query_enhancer import QueryEnhancer
from src.abstractions.use_case import UseCase
from src.abstractions.articles_repo import ArticlesRepo
from src.abstractions.summarizer import Summarizer
from src.config.prompts import build_summary_prompt
from src.config.settings import settings

### Database
def build_embeddings():
    return HuggingFaceEmbeddings(model_name=settings.HUGGINGFACE_MODEL_NAME)

def build_chroma() -> Chroma: 
    return Chroma(
        collection_name=settings.ARTICLES_COLLECTION_NAME,
        embedding_function=build_embeddings(),
        persist_directory=settings.CHROMA_PERSIST_DIRECTORY
    )

def build_articles_repo() -> ArticlesRepo:
    vector_store = build_chroma()

    return ChromaArticlesRepo(vector_store)


### LLM
def build_llm() -> AzureChatOpenAI:
    return AzureChatOpenAI(
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        azure_deployment=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
        openai_api_version=settings.AZURE_OPENAI_API_VERSION,
    )

def build_query_enhancer():
    llm = build_llm() 

    return QueryEnhancer(llm)

def build_summarizer() -> Summarizer:
    llm = build_llm()    
    prompt = build_summary_prompt()
    
    return AzureAISummarizer(llm, prompt)

### Services
def get_use_case(is_url_input: bool) -> UseCase:
    repo = build_articles_repo()

    if is_url_input:
        summarizer = build_summarizer()

        return SummarizeArticlesUseCase(repo, summarizer)
    else:
        query_enhancer = build_query_enhancer()

        return QueryArticleUseCase(repo, query_enhancer)
