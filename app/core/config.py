# app/core/config.py
from pydantic_settings import BaseSettings
from typing import List, Optional
from functools import lru_cache


class Settings(BaseSettings):
    PROJECT_NAME: str = "Stock Advisory System"
    API_V1_STR: str = "/v1"
    
    # LLM Provider configs
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None

    GOOGLE_SEARCH_API_KEY: Optional[str] = None
    SEARCH_ENGINE_ID: Optional[str] = None
    
    # Default LLM provider
    DEFAULT_LLM_PROVIDER: str = "openai"
    
    # # Financial data API keys
    ALPHA_VANTAGE_API_KEY: Optional[str] = None
    # IEX_CLOUD_API_KEY: Optional[str] = None
    
    # Database settings
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "stock_advisory"
    DATABASE_URL: Optional[str] = None
    
    # # Vector database settings
    # VECTOR_DB_TYPE: str = "pinecone"  # Options: pinecone, weaviate
    # PINECONE_API_KEY: Optional[str] = None
    # PINECONE_ENVIRONMENT: Optional[str] = None
    
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()