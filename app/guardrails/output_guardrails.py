"""
guardrails/output_guardrails.py
Validate the agent's response before returning it to the student.

Checks mode compliance, length, and empty responses.
Flags issues for monitoring but only replaces empty responses.
"""

import logging

from app.guardrails.policy import MAX_RESPONSE_WORDS, MODE_RULES

logger = logging.getLogger(__name__)


class OutputGuardrails:
    """Validate agent responses before they reach the student."""

    def validate(self, response_text: str, mode: str | None = None) -> dict:
        """
        Check the response against mode rules and format guidelines.

        Returns:
            {
                "valid": bool,
                "flags": list[str],       # issues found (logged, not blocking)
                "corrected_text": str,     # the response (replaced if empty)
            }
        """
        flags = []
        corrected = response_text

        # ── Empty response (critical — replace) ──────────────────────
        if not response_text or not response_text.strip():
            flags.append("empty_response")
            corrected = (
                "I'm not sure I understood that — could you rephrase "
                "your question or show me what you're working on?"
            )
            return {"valid": False, "flags": flags, "corrected_text": corrected}

        # ── Length check (soft — flag only) ───────────────────────────
        word_count = len(response_text.split())
        if word_count > MAX_RESPONSE_WORDS:
            flags.append(f"over_length:{word_count}_words")

        # ── Mode compliance (soft — flag only) ────────────────────────
        if mode and mode in MODE_RULES:
            rules = MODE_RULES[mode]
            if rules.get("must_end_with_question"):
                if not response_text.rstrip().endswith("?"):
                    flags.append(f"{mode}_no_question")

        if mode == "check_answer":
            lower = response_text.lower()
            has_verdict = any(w in lower for w in [
                "correct", "incorrect", "error", "mistake", "right", "wrong",
            ])
            if not has_verdict:
                flags.append("check_answer_no_verdict")

        if flags:
            logger.info(f"Output guardrail flags: {flags}")

        return {
            "valid": len(flags) == 0,
            "flags": flags,
            "corrected_text": corrected,
        }
