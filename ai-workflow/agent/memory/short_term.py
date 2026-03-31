"""
short_term.py
Short-term memory — in-memory message list for the current ReAct loop.

This is the conversation happening RIGHT NOW. It lives in RAM for the
duration of one API request (~5-30 seconds) and then disappears.

Never touches Supabase. Never persisted. Just a clean wrapper around
the messages list so the loop body reads better.

Lifecycle:
  1. init() — combine session context + user message into the first message
  2. Loop iterations — add_tool_call() and add_tool_result() build up the list
  3. get_messages() — the loop reads this every iteration to send to the LLM
  4. Request ends — garbage collected, gone
"""

from typing import Any


class ShortTermMemory:
    """In-memory message list for one ReAct loop execution."""

    def __init__(self) -> None:
        self._messages: list[dict[str, Any]] = []

    def init(
        self,
        system_prompt: str,
        session_context: str,
        user_message: str,
        conversation_history: list[dict[str, str]] | None = None,
    ) -> None:
        """
        Build the initial messages list.

        The system prompt goes in as a system message. Session context
        goes into the first user message. If there's prior conversation
        history from earlier in this session, it gets inserted between
        the session context and the current message — so the agent
        remembers what was said before.

        Args:
            system_prompt: The full system prompt from prompt.py.
            session_context: The formatted session state from session.py.
            user_message: What the student just said or asked.
            conversation_history: Prior messages from this session.
                Each dict has "role" and "content" keys.
        """
        self._messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"[Session context: {session_context}]",
            },
        ]

        # Insert prior conversation so the agent has continuity
        if conversation_history:
            for msg in conversation_history:
                self._messages.append({
                    "role": msg["role"],
                    "content": msg["content"],
                })

        # Add the current message
        self._messages.append({
            "role": "user",
            "content": user_message,
        })

    def add_tool_call(self, assistant_message: dict[str, Any]) -> None:
        """
        Append the assistant's response (containing tool_calls) to the messages.

        Called when the LLM returns a tool_use response. The full message
        object (including tool_calls metadata) gets added so the next
        LLM call has the complete conversation history.

        Args:
            assistant_message: The assistant message dict from
                choice.message.model_dump(). Contains role, content,
                and tool_calls.
        """
        self._messages.append(assistant_message)

    def add_tool_result(self, tool_call_id: str, result: str) -> None:
        """
        Append a tool result to the messages.

        Called after a tool is executed. The result gets fed back to the
        LLM as a tool message so it can observe what the tool returned
        and decide what to do next.

        Args:
            tool_call_id: The ID from the tool_call that triggered this result.
            result: The tool's output as a JSON string.
        """
        self._messages.append({
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": result,
        })

    def get_messages(self) -> list[dict[str, Any]]:
        """Return the full messages list for the LLM call."""
        return self._messages
