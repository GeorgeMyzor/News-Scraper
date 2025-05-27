from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.repositories.chroma_articles_repo import ChromaArticlesRepo
from src.use_cases.summarizers.azure_ai_summarizer import AzureAISummarizer
from src.use_cases.summarize_articles_use_case import SummarizeArticlesUseCase
from src.use_cases.query_articles_use_case import QueryArticleUseCase
from src.abstractions.use_case import UseCase
from src.abstractions.articles_repo import ArticlesRepo
from src.abstractions.summarizer import Summarizer
from src.config.settings import settings

### Database
def build_embeddings() -> HuggingFaceEmbeddings:
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
def get_use_case(is_url_input: bool) -> UseCase:
    repo = build_articles_repo()

    if is_url_input:
        summarizer = build_summarizer()

        return SummarizeArticlesUseCase(repo, summarizer)
    else:
        return QueryArticleUseCase(repo)
