"""
llm/model.py
LLM provider abstraction. One place to configure the model.
Swap providers by changing this file — nothing else changes.
"""

from langchain_openai import ChatOpenAI
from app.config import OPENAI_API_KEY, OPENAI_MODEL


def get_llm(temperature: float = 0.3, max_tokens: int = 3000) -> ChatOpenAI:
    """
    Return a configured LLM instance.

    Every module that needs to call the LLM imports this function.
    Changing the provider means changing only this file.
    """
    return ChatOpenAI(
        model=OPENAI_MODEL,
        api_key=OPENAI_API_KEY,
        temperature=temperature,
        max_tokens=max_tokens,
    )
