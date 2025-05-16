# llm_service/gemini_llm.py
from typing import Any
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from app.services.llm.base import BaseLLM
from app.core.config import settings


api_key = settings.GEMINI_API_KEY


class GeminiLLM(BaseLLM):
    def get_llm(self):
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.7,
            google_api_key=api_key
        )

    def get_embedding(self):
        return GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=api_key
        )

