"""
rag/indexing/build_openstax_index.py
Offline script — run once to build the OpenStax vector index.

Usage:
    python -m app.rag.indexing.build_openstax_index

Pipeline:
    1. Load OpenStax content (loader)
    2. Chunk into retrieval-friendly pieces (chunker)
    3. Generate embeddings for each chunk (embedder)
    4. Store chunks + embeddings in the vector store (store)
"""

import sys
import logging

from app.config import OPENSTAX_DATA_PATH, VECTOR_STORE_PATH
from app.rag.loaders.openstax_loader import OpenStaxLoader
from app.rag.chunking.openstax_chunker import OpenStaxChunker
from app.rag.embeddings.embedder import Embedder
from app.rag.stores.vector_store import VectorStore

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
logger = logging.getLogger(__name__)


def build_index():
    """Run the full indexing pipeline."""

    # 1. Load
    logger.info(f"Loading OpenStax content from {OPENSTAX_DATA_PATH}...")
    loader = OpenStaxLoader(OPENSTAX_DATA_PATH)
    documents = loader.load()
    logger.info(f"Loaded {len(documents)} documents")

    # 2. Chunk
    logger.info("Chunking documents...")
    chunker = OpenStaxChunker(chunk_size=500, overlap=50)
    chunks = chunker.chunk(documents)
    logger.info(f"Created {len(chunks)} chunks")

    # 3. Embed
    logger.info("Generating embeddings...")
    embedder = Embedder()
    texts = [c["content"] for c in chunks]

    # Batch embedding to avoid rate limits
    batch_size = 50
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        embeddings = embedder.embed_documents(batch)
        all_embeddings.extend(embeddings)
        logger.info(f"  Embedded {min(i + batch_size, len(texts))}/{len(texts)} chunks")

    # 4. Store
    logger.info(f"Storing in vector store at {VECTOR_STORE_PATH}...")
    store = VectorStore(VECTOR_STORE_PATH)
    store.clear()
    store.add(chunks, all_embeddings)

    logger.info(f"Done. {len(chunks)} chunks indexed and stored.")


if __name__ == "__main__":
    build_index()
