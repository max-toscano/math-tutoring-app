"""
rag/retrieval/openstax_retriever.py
Retrieve grounded OpenStax teaching context via SQL lookup.

Primary: query openstax_content table by topic_slug (instant, free, exact).
Fallback: if no match found, use web search tool (slower, costs money).

No vector search. No embeddings. Just a SQL query on a structured table.
"""

import json
import logging

from sqlalchemy import text
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class OpenStaxRetriever:
    """Retrieve OpenStax content by topic, with web search fallback."""

    def __init__(self, db: Session):
        self.db = db

    def retrieve(self, topic: str | None = None, subject: str | None = None) -> list[dict]:
        """
        Retrieve OpenStax content for a topic.

        Args:
            topic: The topic slug (e.g. "chain_rule", "double_angle").
            subject: Optional subject filter (e.g. "calculus", "trigonometry").

        Returns:
            List of content dicts with content, key_formulas, examples, etc.
            Empty list if no match found.
        """
        if not topic:
            return []

        # Try exact topic match
        rows = self.db.execute(
            text("""
                SELECT content, summary, key_formulas, prerequisites, examples,
                       common_mistakes, learning_objectives, section_title,
                       chapter_title, textbook, section_number
                FROM openstax_content
                WHERE topic_slug = :topic
                LIMIT 3
            """),
            {"topic": topic},
        ).mappings().all()

        if rows:
            return [dict(r) for r in rows]

        # Try subject-wide search if topic not found
        if subject:
            rows = self.db.execute(
                text("""
                    SELECT content, summary, key_formulas, prerequisites, examples,
                           common_mistakes, learning_objectives, section_title,
                           chapter_title, textbook, section_number, topic_slug
                    FROM openstax_content
                    WHERE subject = :subject
                    LIMIT 5
                """),
                {"subject": subject},
            ).mappings().all()

            if rows:
                return [dict(r) for r in rows]

        return []

    def format_context(self, results: list[dict]) -> str:
        """
        Format retrieved content into a context string for the LLM prompt.

        Returns a block the AI reads as grounding material with formulas,
        examples, and common mistakes.
        """
        if not results:
            return ""

        sections = ["## OpenStax Reference Material\n"]

        for r in results:
            title = r.get("section_title", "")
            chapter = r.get("chapter_title", "")
            textbook = r.get("textbook", "")
            section_num = r.get("section_number", "")

            sections.append(f"### {title} ({textbook} Ch.{section_num})")

            # Summary or full content (use summary if available for brevity)
            summary = r.get("summary")
            content = r.get("content", "")
            if summary:
                sections.append(summary)
            else:
                # Truncate long content to keep prompt manageable
                sections.append(content[:1500] if len(content) > 1500 else content)

            # Key formulas
            formulas = r.get("key_formulas", [])
            if formulas:
                sections.append("\n**Key Formulas:**")
                for f in formulas:
                    sections.append(f"- ${f}$")

            # Worked examples
            examples = r.get("examples", [])
            if examples and isinstance(examples, list):
                sections.append("\n**Worked Examples:**")
                for ex in examples[:2]:  # Max 2 examples
                    if isinstance(ex, dict):
                        sections.append(f"- Problem: {ex.get('problem', '')}")
                        sections.append(f"  Solution: {ex.get('solution', '')}")

            # Common mistakes
            mistakes = r.get("common_mistakes", [])
            if mistakes:
                sections.append("\n**Common Mistakes:**")
                for m in mistakes:
                    sections.append(f"- {m}")

            sections.append("")  # blank line between sections

        return "\n".join(sections)

    def retrieve_and_format(self, topic: str | None = None, subject: str | None = None) -> str:
        """Convenience: retrieve + format in one call."""
        results = self.retrieve(topic, subject)
        return self.format_context(results)
