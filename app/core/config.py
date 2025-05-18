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
    FINNHUB_API_KEY: Optional[str] = None
    NEWSAPI_KEY: Optional[str] = None


    DATABASE_URL: Optional[str] = None
    

    # CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
    # CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
    
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()