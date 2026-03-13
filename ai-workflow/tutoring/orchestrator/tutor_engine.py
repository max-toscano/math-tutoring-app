"""
tutor_engine.py
The orchestration core of the tutoring system.

Responsibility:
    Coordinates subject resolution, mode resolution, context loading,
    prompt building, and the LLM call. Returns a structured response dict.

    This file must NOT contain teaching logic, subject rules, or mode rules.
    It only coordinates — everything else is delegated.

Architecture:
    router.py
        → generate_tutoring_response()
            → subject_resolver.resolve_subject()
            → mode_resolver.resolve_mode()
            → load_subject_context()     ← pulls from tutoring/subjects/
            → load_mode_context()        ← pulls from tutoring/modes/
            → prompt_builder.build_tutoring_prompt()
            → call_llm()
"""

from tutoring.orchestrator.subject_resolver import resolve_subject
from tutoring.orchestrator.mode_resolver import resolve_mode
from tutoring.orchestrator.prompt_builder import build_tutoring_prompt


# ---------------------------------------------------------------------------
# Subject context loader
# ---------------------------------------------------------------------------

def load_subject_context(subject: str) -> dict:
    """
    Load rules, patterns, and strategies from the appropriate subject module.

    Args:
        subject: The resolved subject string (e.g. "math").

    Returns:
        A dict with keys: rules, opener, follow_up, strategy.
        Falls back to placeholder values if the subject is unsupported
        or if specific imports are unavailable.
    """
    if subject == "math":
        try:
            from tutoring.subjects.math import (
                get_rules,
                openers,
                guided_questions,
                solve_step_by_step,
            )
            return {
                "rules":     get_rules(),
                "opener":    openers[0],
                "follow_up": guided_questions[0],
                "strategy":  solve_step_by_step,   # function ref, called below
            }
        except ImportError:
            pass  # Fall through to placeholder

    # Unsupported or unavailable subject — return safe placeholders.
    return {
        "rules":     [f"Tutor the student clearly in {subject}."],
        "opener":    "Let's work through this together.",
        "follow_up": "Does that make sense so far?",
        "strategy":  None,
    }


# ---------------------------------------------------------------------------
# Mode context loader
# ---------------------------------------------------------------------------

def load_mode_context(mode: str) -> dict:
    """
    Load rules from the appropriate mode module.

    Args:
        mode: The resolved mode string (e.g. "socratic").

    Returns:
        A dict with keys: mode, rules.
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
# LLM call (placeholder)
# ---------------------------------------------------------------------------

def call_llm(prompt: str) -> str:
    """
    Send the assembled prompt to the LLM and return the response.

    TODO: Replace this placeholder with a real Claude API call:
        from anthropic import Anthropic
        client = Anthropic()
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    """
    return "LLM call placeholder: tutoring response not implemented yet."


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def generate_tutoring_response(
    student_input: str,
    requested_subject: str | None = None,
    requested_mode: str | None = None,
) -> dict:
    """
    Orchestrate a full tutoring response for a student request.

    Flow:
        1. Resolve subject
        2. Resolve teaching mode
        3. Load subject context (rules, patterns, strategies)
        4. Load mode context (mode rules)
        5. Build the prompt string
        6. Call the LLM
        7. Return structured response dict

    Args:
        student_input:      Raw text from the student.
        requested_subject:  Optional subject override from the API request.
        requested_mode:     Optional mode override from the API request.

    Returns:
        dict with keys: subject, mode, prompt, response.
    """
    # Step 1 — Resolve subject.
    subject = resolve_subject(student_input, requested_subject)

    # Step 2 — Resolve mode.
    mode = resolve_mode(student_input, requested_mode)

    # Step 3 — Load subject context.
    subject_context = load_subject_context(subject)

    # Step 4 — Load mode context.
    mode_context = load_mode_context(mode)

    # Step 5 — Resolve strategy string if a function reference was stored.
    strategy_fn = subject_context.get("strategy")
    if callable(strategy_fn):
        subject_context["strategy"] = strategy_fn(student_input)

    # Step 6 — Build prompt.
    prompt = build_tutoring_prompt(
        student_input=student_input,
        subject=subject,
        mode=mode,
        subject_context=subject_context,
        mode_context=mode_context,
    )

    # Step 7 — Call LLM.
    response = call_llm(prompt)

    return {
        "subject":  subject,
        "mode":     mode,
        "prompt":   prompt,
        "response": response,
    }
