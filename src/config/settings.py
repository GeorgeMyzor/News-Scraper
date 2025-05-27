from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_DEPLOYMENT_NAME: str
    AZURE_OPENAI_API_VERSION: str

    model_config = ConfigDict(extra="ignore")

settings = Settings()