"""
memory/summarizer.py
Compress old conversation messages to prevent token overflow.

When conversation history gets too long, older messages get
summarized into a compact block while keeping recent messages intact.
"""

from typing import Any


class ConversationSummarizer:
    """Summarize old conversation messages to save tokens."""

    def __init__(self, max_tokens: int = 40000):
        self.max_tokens = max_tokens

    def summarize_if_needed(self, messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        If messages exceed the token limit, compress older ones.

        Keeps:
          - messages[0]: system prompt (always)
          - messages[1]: session context (always)
          - Last 6 messages: recent conversation (always)

        Compresses everything in between into one summary message.
        """
        total_chars = sum(len(str(m.get("content", ""))) for m in messages)
        estimated_tokens = total_chars // 4

        if estimated_tokens < self.max_tokens:
            return messages

        if len(messages) <= 8:
            return messages

        preserved_start = messages[:2]
        preserved_end = messages[-6:]
        middle = messages[2:-6]

        if not middle:
            return messages

        summary_parts = []
        for m in middle:
            role = m.get("role", "unknown")
            content = str(m.get("content", ""))
            if len(content) > 100:
                content = content[:100] + "..."
            if role in ("user", "assistant"):
                summary_parts.append(f"{role}: {content}")

        summary_text = "[Earlier conversation summarized: " + " | ".join(summary_parts) + "]"

        return preserved_start + [{"role": "user", "content": summary_text}] + preserved_end
