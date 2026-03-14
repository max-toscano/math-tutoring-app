"""
prompt_builder.py
Constructs the system prompt and user message for the Claude API.

Responsibility:
    Receives subject, mode, and mode rules, then formats them into
    a system prompt and user message. The Claude API accepts these
    as separate parameters for better instruction following.
"""


def build_system_prompt(
    subject: str,
    mode: str,
    mode_context: dict,
) -> str:
    """
    Build the system prompt that defines the tutor's identity and behavior.

    Returns:
        A formatted system prompt string.
    """
    sections: list[str] = []

    sections.append(f"You are an expert {subject} tutor.")
    sections.append(f"Teaching mode: {mode.upper()}")

    mode_rules: list[str] = mode_context.get("rules", [])
    if mode_rules:
        formatted = "\n".join(f"  - {r}" for r in mode_rules)
        sections.append(f"Mode rules:\n{formatted}")

    return "\n\n".join(sections)


def build_tutoring_prompt(
    student_input: str,
    subject: str,
    mode: str,
    mode_context: dict,
) -> dict:
    """
    Build the full prompt context for the Claude API.

    Returns:
        A dict with keys: system, user_message.
    """
    return {
        "system": build_system_prompt(subject, mode, mode_context),
        "user_message": student_input,
    }
