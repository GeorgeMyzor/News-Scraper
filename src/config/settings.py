from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from dotenv import load_dotenv

load_dotenv()
class Settings(BaseSettings):
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_DEPLOYMENT_NAME: str
    AZURE_OPENAI_API_VERSION: str
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME: str
    AZURE_OPENAI_EMBEDDING_API_VERSION: str

    ARTICLES_COLLECTION_NAME: str
    CHROMA_PERSIST_DIRECTORY: str    
    
    LANGSMITH_TRACING: bool
    LANGSMITH_ENDPOINT: str
    LANGSMITH_API_KEY: str
    LANGSMITH_PROJECT: str

    HUGGINGFACE_MODEL_NAME: str

    USE_CHROMA_DB: bool
    USE_DETERMINISTIC_QUERY: bool

    RELEVANCE_SCORE_THRESHOLD: float

    model_config = ConfigDict(extra="ignore")

settings = Settings()