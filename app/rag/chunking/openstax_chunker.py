"""
rag/chunking/openstax_chunker.py
Split OpenStax documents into retrieval-friendly chunks.
Splits at sentence boundaries with overlap so context isn't lost at chunk edges.
"""


class OpenStaxChunker:
    """Chunk OpenStax documents for embedding and retrieval."""

    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, documents: list[dict]) -> list[dict]:
        """
        Split documents into overlapping chunks.
        Each chunk inherits the parent document's metadata plus a chunk_index.
        """
        chunks = []
        for doc in documents:
            content = doc.get("content", "")
            metadata = doc.get("metadata", {})

            if len(content) <= self.chunk_size:
                chunks.append({
                    "content": content,
                    "metadata": {**metadata, "chunk_index": 0},
                })
                continue

            sentences = self._split_sentences(content)
            current_chunk = ""
            chunk_index = 0

            for sentence in sentences:
                if len(current_chunk) + len(sentence) > self.chunk_size and current_chunk:
                    chunks.append({
                        "content": current_chunk.strip(),
                        "metadata": {**metadata, "chunk_index": chunk_index},
                    })
                    chunk_index += 1
                    overlap_text = current_chunk[-self.overlap:] if len(current_chunk) > self.overlap else current_chunk
                    current_chunk = overlap_text + sentence
                else:
                    current_chunk += sentence

            if current_chunk.strip():
                chunks.append({
                    "content": current_chunk.strip(),
                    "metadata": {**metadata, "chunk_index": chunk_index},
                })

        return chunks

    def _split_sentences(self, text: str) -> list[str]:
        """Split text into sentences at period + space boundaries."""
        parts = []
        current = ""
        for char in text:
            current += char
            if char in ".!?" and len(current) > 10:
                parts.append(current)
                current = ""
        if current:
            parts.append(current)
        return parts
