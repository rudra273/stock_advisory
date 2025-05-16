# llm_service/openai_llm.py

import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from app.services.llm.base import BaseLLM
from app.core.config import settings


api_key = settings.OPENAI_API_KEY


class OpenAILLM(BaseLLM):
    def get_llm(self):
        return ChatOpenAI(
            model="gpt-4.1-nano-2025-04-14",
            temperature=0.7,
            openai_api_key=api_key
        )

    def get_embedding(self):
        return OpenAIEmbeddings(
            openai_api_key=api_key
        )

