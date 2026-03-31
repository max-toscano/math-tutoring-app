"""
rag/embeddings/embedder.py
Generate vector embeddings for text using OpenAI.
Used offline (indexing) and at runtime (query embedding).
"""

import os
from openai import OpenAI
from app.config import OPENAI_API_KEY, EMBEDDING_MODEL


class Embedder:
    """Generate embeddings using OpenAI's embedding API."""

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = EMBEDDING_MODEL

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of documents. Used during indexing."""
        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
        )
        return [item.embedding for item in response.data]

    def embed_query(self, text: str) -> list[float]:
        """Embed a single query. Used at runtime."""
        response = self.client.embeddings.create(
            model=self.model,
            input=[text],
        )
        return response.data[0].embedding
