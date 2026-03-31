"""
services/mode_service.py
Determine and apply the tutoring mode.

Modes:
  1. auto          — adapts to the student's situation (mastery, frustration, context)
  2. explain       — explain the concept behind the problem
  3. guide_me      — walk the student through step by step
  4. hint          — give small nudges toward the answer
  5. check_answer  — check the student's submitted work

Priority:
  1. Student selected mode → use it
  2. auto → system reads mastery + session state and picks the best approach
  3. Student's preferred_mode from profile → fallback
"""


VALID_MODES = {"auto", "explain", "guide_me", "hint", "check_answer"}


MODE_INSTRUCTIONS = {
    "auto": (
        "You are in AUTO mode. Adapt your approach to what the student needs right now. "
        "Read their mastery level, their session state, and their message to decide "
        "whether to explain, guide, hint, or check. "
        "If mastery is low → explain the concept first. "
        "If mastery is moderate → guide them step by step. "
        "If mastery is high → give hints and let them work. "
        "If they submitted work → check it. "
        "If they're frustrated → be more direct and supportive."
    ),
    "explain": (
        "You are in EXPLAIN mode. The student wants to understand the concept. "
        "Teach the underlying idea before touching the specific problem. "
        "Use a simple example first, then connect it to their question. "
        "Structure: the big idea → simple example → their specific problem. "
        "Name every rule and theorem you reference."
    ),
    "guide_me": (
        "You are in GUIDE ME mode. Walk the student through the problem step by step. "
        "Show each step clearly with proper math notation. "
        "Explain WHY each step works, not just what it is. "
        "Teach a repeatable method they can apply to similar problems. "
        "Go at their pace — one step at a time."
    ),
    "hint": (
        "You are in HINT mode. Give a small nudge toward the answer. "
        "Do NOT reveal the solution or the next step directly. "
        "Point the student in the right direction with a question or observation. "
        "One hint at a time — if they need more, they'll ask. "
        "Good: 'What identity involves sin² and cos²?' "
        "Bad: 'Use the Pythagorean identity to substitute.'"
    ),
    "check_answer": (
        "You are in CHECK ANSWER mode. The student submitted their work for review. "
        "Go through each step and verify it. "
        "If correct, confirm it and celebrate what they did right. "
        "If wrong, identify the SPECIFIC step with the error and explain what went wrong. "
        "Don't just say 'wrong' — show them exactly where and why."
    ),
}


class ModeService:
    """Determine and format the tutoring mode."""

    def resolve_mode(
        self,
        selected_mode: str | None = None,
        hint_strategy_result: dict | None = None,
        preferred_mode: str | None = None,
    ) -> str:
        """
        Determine which mode to use.

        Args:
            selected_mode: What the student picked in the UI.
            hint_strategy_result: Result from get_hint_strategy tool.
            preferred_mode: Student's preferred mode from their profile.

        Returns:
            The resolved mode string.
        """
        if selected_mode and selected_mode in VALID_MODES:
            return selected_mode

        if hint_strategy_result:
            recommended = hint_strategy_result.get("recommended_mode")
            if recommended and recommended in VALID_MODES:
                return recommended

        if preferred_mode and preferred_mode in VALID_MODES:
            return preferred_mode

        return "auto"

    def get_mode_instruction(self, mode: str) -> str:
        """Get the prompt instruction text for a mode."""
        return MODE_INSTRUCTIONS.get(mode, MODE_INSTRUCTIONS["auto"])

    def get_mode_source(self, selected_mode: str | None, resolved_mode: str) -> str:
        """Determine if the mode was student-selected or system-determined."""
        if selected_mode and selected_mode == resolved_mode:
            return "student_selected"
        return "agent_determined"
