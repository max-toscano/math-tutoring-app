"""
tutor_engine.py
The orchestration core of the tutoring system.

Responsibility:
    Coordinates subject resolution, mode resolution, prompt building,
    and the LLM call. Returns a structured response dict.
"""

import os
from anthropic import Anthropic

from tutoring.orchestrator.subject_resolver import resolve_subject
from tutoring.orchestrator.mode_resolver import resolve_mode
from tutoring.orchestrator.prompt_builder import build_tutoring_prompt

# ---------------------------------------------------------------------------
# Claude client (initialized once)
# ---------------------------------------------------------------------------

client = Anthropic()  # reads ANTHROPIC_API_KEY from env


# ---------------------------------------------------------------------------
# Mode context loader
# ---------------------------------------------------------------------------

def load_mode_context(mode: str) -> dict:
    """
    Load rules from the appropriate mode module.

    Falls back to direct mode rules if the mode is unrecognised.
    """
    loaders: dict[str, callable] = {}

    try:
        from tutoring.modes.direct.mode_rules import get_direct_mode_rules
        loaders["direct"] = get_direct_mode_rules
    except ImportError:
        pass

    try:
        from tutoring.modes.socratic.mode_rules import get_socratic_mode_rules
        loaders["socratic"] = get_socratic_mode_rules
    except ImportError:
        pass

    try:
        from tutoring.modes.hint.mode_rules import get_hint_mode_rules
        loaders["hint"] = get_hint_mode_rules
    except ImportError:
        pass

    try:
        from tutoring.modes.check_work.mode_rules import get_check_work_mode_rules
        loaders["check_work"] = get_check_work_mode_rules
    except ImportError:
        pass

    loader = loaders.get(mode) or loaders.get("direct")
    rules = loader() if loader else ["Be a clear and helpful tutor."]

    return {
        "mode":  mode,
        "rules": rules,
    }


# ---------------------------------------------------------------------------
# LLM call
# ---------------------------------------------------------------------------

def call_llm(system_prompt: str, messages: list[dict]) -> str:
    """
    Send the assembled prompt to Claude and return the response text.

    Args:
        system_prompt:  The system instruction (tutor identity + mode rules).
        messages:       Conversation history as a list of {role, content} dicts.

    Returns:
        The assistant's response text.
    """
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=system_prompt,
        messages=messages,
    )
    return response.content[0].text


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def generate_tutoring_response(
    student_input: str,
    requested_subject: str | None = None,
    requested_mode: str | None = None,
    conversation_history: list[dict] | None = None,
) -> dict:
    """
    Orchestrate a full tutoring response for a student request.

    Args:
        student_input:          Raw text from the student.
        requested_subject:      Optional subject override.
        requested_mode:         Optional mode override.
        conversation_history:   Prior messages as [{role, content}, ...].

    Returns:
        dict with keys: subject, mode, response, conversation_history.
    """
    # Step 1 — Resolve subject.
    subject = resolve_subject(student_input, requested_subject)

    # Step 2 — Resolve mode.
    mode = resolve_mode(student_input, requested_mode)

    # Step 3 — Load mode context.
    mode_context = load_mode_context(mode)

    # Step 4 — Build prompt.
    prompt_parts = build_tutoring_prompt(
        student_input=student_input,
        subject=subject,
        mode=mode,
        mode_context=mode_context,
    )

    # Step 5 — Build messages list (conversation history + new input).
    messages = list(conversation_history or [])
    messages.append({"role": "user", "content": prompt_parts["user_message"]})

    # Step 6 — Call LLM.
    response = call_llm(prompt_parts["system"], messages)

    # Step 7 — Append assistant response to history.
    messages.append({"role": "assistant", "content": response})

    return {
        "subject":  subject,
        "mode":     mode,
        "response": response,
        "conversation_history": messages,
    }
