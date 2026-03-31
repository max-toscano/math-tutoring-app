"""
rag/stores/vector_store.py
Simple vector store using JSON file + NumPy cosine similarity.

Stores chunks with their embeddings on disk. Searches by cosine similarity.
Replace with pgvector, Pinecone, or Weaviate when scaling.
"""

import json
import logging
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)


class VectorStore:
    """Store and search document chunks by vector similarity."""

    def __init__(self, store_path: str):
        self.store_path = Path(store_path)
        self.chunks: list[dict] = []
        self.embeddings: np.ndarray | None = None
        self._load()

    def add(self, chunks: list[dict], embeddings: list[list[float]]) -> None:
        """Add chunks with their embeddings to the store."""
        self.chunks.extend(chunks)

        new_embeddings = np.array(embeddings)
        if self.embeddings is not None and len(self.embeddings) > 0:
            self.embeddings = np.vstack([self.embeddings, new_embeddings])
        else:
            self.embeddings = new_embeddings

        self._save()
        logger.info(f"Added {len(chunks)} chunks. Total: {len(self.chunks)}")

    def search(self, query_embedding: list[float], top_k: int = 5) -> list[dict]:
        """Find the most similar chunks to a query embedding."""
        if self.embeddings is None or len(self.embeddings) == 0:
            return []

        query_vec = np.array(query_embedding)
        # Cosine similarity
        norms = np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_vec)
        norms = np.where(norms == 0, 1, norms)  # avoid division by zero
        similarities = np.dot(self.embeddings, query_vec) / norms

        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            chunk = self.chunks[idx].copy()
            chunk["similarity"] = float(similarities[idx])
            results.append(chunk)

        return results

    def _save(self) -> None:
        """Persist chunks and embeddings to disk."""
        self.store_path.mkdir(parents=True, exist_ok=True)

        chunks_path = self.store_path / "chunks.json"
        embeddings_path = self.store_path / "embeddings.npy"

        with open(chunks_path, "w", encoding="utf-8") as f:
            json.dump(self.chunks, f, indent=2)

        if self.embeddings is not None:
            np.save(str(embeddings_path), self.embeddings)

    def _load(self) -> None:
        """Load chunks and embeddings from disk if they exist."""
        chunks_path = self.store_path / "chunks.json"
        embeddings_path = self.store_path / "embeddings.npy"

        if chunks_path.exists() and embeddings_path.exists():
            with open(chunks_path, "r", encoding="utf-8") as f:
                self.chunks = json.load(f)
            self.embeddings = np.load(str(embeddings_path))
            logger.info(f"Loaded {len(self.chunks)} chunks from {self.store_path}")
        else:
            self.chunks = []
            self.embeddings = None

    def clear(self) -> None:
        """Remove all stored data."""
        self.chunks = []
        self.embeddings = None
        self._save()
