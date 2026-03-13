"""
prompt_builder.py
Constructs the final prompt string that will be sent to the LLM.

Responsibility:
    Receives all assembled context (subject, mode, rules, patterns,
    strategies) and formats it into a single coherent prompt string.
    This file decides how to talk to the LLM — not what to teach.

    Keeping prompt construction separate from the engine means the
    prompt format can be changed without touching orchestration logic.
"""


def build_tutoring_prompt(
    student_input: str,
    subject: str,
    mode: str,
    subject_context: dict,
    mode_context: dict,
) -> str:
    """
    Build the final prompt string from all assembled context.

    Args:
        student_input:    The raw question or answer from the student.
        subject:          The resolved subject (e.g. "math").
        mode:             The resolved teaching mode (e.g. "socratic").
        subject_context:  Dict containing rules, patterns, strategies
                          loaded from the subject module.
        mode_context:     Dict containing rules loaded from the mode module.

    Returns:
        A formatted prompt string ready to send to the LLM.
    """
    sections: list[str] = []

    # --- System identity ---
    sections.append(f"You are an expert {subject} tutor.")

    # --- Teaching mode instruction ---
    sections.append(f"Teaching mode: {mode.upper()}")
    mode_rules: list[str] = mode_context.get("rules", [])
    if mode_rules:
        formatted = "\n".join(f"  - {r}" for r in mode_rules)
        sections.append(f"Mode rules:\n{formatted}")

    # --- Subject rules ---
    subject_rules: list[str] = subject_context.get("rules", [])
    if subject_rules:
        formatted = "\n".join(f"  - {r}" for r in subject_rules)
        sections.append(f"Subject rules:\n{formatted}")

    # --- Response style ---
    opener: str = subject_context.get("opener", "")
    if opener:
        sections.append(f"Begin your response with: \"{opener}\"")

    strategy: str = subject_context.get("strategy", "")
    if strategy:
        sections.append(f"Teaching strategy context: {strategy}")

    follow_up: str = subject_context.get("follow_up", "")
    if follow_up:
        sections.append(f"End with this follow-up question: \"{follow_up}\"")

    # --- Student input ---
    sections.append(f"Student input:\n{student_input}")

    return "\n\n".join(sections)
