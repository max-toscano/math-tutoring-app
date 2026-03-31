"""
session.py
Session memory — current session state + recent session history.

Full lifecycle:
  - start_session()        → creates a new agent_sessions row
  - get_session_context()  → reads active session + recent summaries
  - save_problem_result()  → updates session state after each problem
  - close_session()        → deactivates session, computes duration, generates summary

Uses SQLAlchemy with the same engine/session as the rest of the backend.
"""

import os
import json
import logging
from datetime import datetime, timezone
from typing import Any

from openai import OpenAI
from sqlalchemy import text
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
_model = os.getenv("OPENAI_MODEL", "gpt-4o")


async def start_session(student_id: str, db: Session) -> str:
    """
    Create a new active session for a student.

    Deactivates any existing active session first (there can only be one).
    Returns the new session's UUID.

    Args:
        student_id: The student's ID (matches student_profiles.student_id).
        db: SQLAlchemy session.

    Returns:
        The new session UUID as a string.
    """
    # Deactivate any existing active session for this student
    existing = db.execute(
        text("SELECT id FROM agent_sessions WHERE student_id = :sid AND is_active = true"),
        {"sid": student_id},
    ).mappings().first()

    if existing:
        now = datetime.now(timezone.utc)
        db.execute(
            text("""
                UPDATE agent_sessions
                SET is_active = false,
                    ended_at = :now,
                    duration_minutes = EXTRACT(EPOCH FROM (:now - started_at)) / 60
                WHERE id = :sid
            """),
            {"now": now, "sid": existing["id"]},
        )

    # Create new session
    result = db.execute(
        text("""
            INSERT INTO agent_sessions (student_id, is_active, started_at)
            VALUES (:sid, true, now())
            RETURNING id
        """),
        {"sid": student_id},
    ).mappings().first()

    db.commit()
    return str(result["id"])


async def get_session_context(
    session_id: str,
    db: Session,
    selected_mode: str | None = None,
) -> str:
    """
    Build the session context string from the active session + recent history.

    This gets injected into the first user message so the agent knows:
      - Which mode to use (student-selected or needs determining)
      - What happened so far in this session (problems, streak, frustration)
      - What happened in recent past sessions (summaries only, not full state)

    Args:
        session_id: The active session UUID.
        db: SQLAlchemy session.
        selected_mode: Mode the student picked in the UI, or None.

    Returns:
        Formatted context string with mode instruction, current session
        state, and recent session summaries.
    """

    # ── Mode instruction (appears first — agent reads top-down) ───────────
    if selected_mode:
        mode_line = f"STUDENT SELECTED MODE: {selected_mode} — use this mode, do not override."
    else:
        mode_line = (
            "No mode selected — use get_hint_strategy to determine the best mode, "
            "or fall back to the student's preferred mode from their profile."
        )

    # ── Current session state ─────────────────────────────────────────────
    row = db.execute(
        text("SELECT * FROM agent_sessions WHERE id = :sid AND is_active = true"),
        {"sid": session_id},
    ).mappings().first()

    if not row:
        return f"{mode_line}\n\n**Current Session:** New session — no problems attempted yet."

    state = row["session_state"] or {}
    problems = state.get("problems_attempted", [])
    streak = state.get("streak", 0)
    frustration = state.get("frustration_signals", 0)
    current_mode = state.get("current_mode", "socratic")
    topics_covered = state.get("topics_covered", [])
    mode_switches = state.get("mode_switches", 0)

    # Format current session summary
    if problems:
        last = problems[-1]
        last_summary = (
            f"last problem: {last.get('type', 'unknown')} "
            f"({last.get('result', 'unknown')}, {last.get('mode_used', 'unknown')}, "
            f"{last.get('hints_used', 0)} hints)"
        )
    else:
        last_summary = "no problems attempted yet"

    session_block = (
        f"**Current Session:**\n"
        f"{len(problems)} problems attempted, streak: {streak}, "
        f"frustration signals: {frustration}, mode switches: {mode_switches}\n"
        f"Current mode: {current_mode}, topics covered: {', '.join(topics_covered) or 'none'}\n"
        f"{last_summary}"
    )

    # ── Recent session summaries (last 5 completed sessions) ──────────────
    student_id = row["student_id"]
    recent_rows = db.execute(
        text("""
            SELECT session_summary, started_at, total_problems, session_success_rate
            FROM agent_sessions
            WHERE student_id = :sid AND is_active = false AND session_summary IS NOT NULL
            ORDER BY started_at DESC
            LIMIT 5
        """),
        {"sid": student_id},
    ).mappings().all()

    if recent_rows:
        history_lines = []
        for r in recent_rows:
            started = r["started_at"]
            if isinstance(started, str):
                started = datetime.fromisoformat(started)
            days_ago = (datetime.now(timezone.utc) - started).days
            if days_ago == 0:
                when = "today"
            elif days_ago == 1:
                when = "yesterday"
            else:
                when = f"{days_ago} days ago"

            problems = r["total_problems"]
            rate = r["session_success_rate"]
            summary = r["session_summary"] or "No summary available."
            history_lines.append(
                f"- {when} ({problems} problems, {rate:.0%} success): {summary}"
            )
        history_block = "**Recent Sessions:**\n" + "\n".join(history_lines)
    else:
        history_block = "**Recent Sessions:** None — this is the student's first session."

    return f"{mode_line}\n\n{session_block}\n\n{history_block}"


async def save_problem_result(session_id: str, result: dict, db: Session) -> None:
    """
    Update the session state after a problem is completed.

    Appends the problem to problems_attempted, updates streak, frustration
    signals, topics covered, mode tracking, and the denormalized analytics
    counters (total_problems, correct_count, session_success_rate, avg_time).

    Args:
        session_id: The active session UUID.
        result: Dict containing the problem outcome:
            - expression: str (the problem text)
            - type: str (topic type like "double_angle")
            - chapter: int
            - result: str ("correct", "correct_with_hints", "incorrect", "abandoned")
            - hints_used: int
            - mode_used: str ("socratic", "direct", "concept_first")
            - mode_source: str ("student_selected", "agent_determined")
            - time_seconds: int
            - error_types: list[str]
            - iterations_used: int
        db: SQLAlchemy session.
    """
    row = db.execute(
        text("SELECT session_state, total_problems, correct_count FROM agent_sessions WHERE id = :sid AND is_active = true"),
        {"sid": session_id},
    ).mappings().first()

    if not row:
        logger.warning(f"save_problem_result: no active session found for {session_id}")
        return

    state = dict(row["session_state"] or {})
    problems = list(state.get("problems_attempted", []))

    # ── Append the new problem ────────────────────────────────────────────
    problem_entry = {
        "expression": result.get("expression", ""),
        "type": result.get("type", ""),
        "chapter": result.get("chapter"),
        "result": result.get("result", ""),
        "hints_used": result.get("hints_used", 0),
        "mode_used": result.get("mode_used", ""),
        "mode_source": result.get("mode_source", ""),
        "time_seconds": result.get("time_seconds"),
        "error_types": result.get("error_types", []),
        "iterations_used": result.get("iterations_used"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    problems.append(problem_entry)
    state["problems_attempted"] = problems

    # ── Update streak ─────────────────────────────────────────────────────
    outcome = result.get("result", "")
    if outcome in ("correct", "correct_with_hints"):
        state["streak"] = state.get("streak", 0) + 1
    elif outcome == "incorrect":
        state["streak"] = 0
    # "unassessed" doesn't affect streak — we don't know

    # ── Update frustration signals ────────────────────────────────────────
    # Increment if 2+ wrong in a row
    if outcome == "incorrect":
        recent_results = [p.get("result") for p in problems[-2:]]
        if len(recent_results) >= 2 and all(r == "incorrect" for r in recent_results):
            state["frustration_signals"] = state.get("frustration_signals", 0) + 1

    # ── Update topics covered ─────────────────────────────────────────────
    topic_type = result.get("type", "")
    topics = list(state.get("topics_covered", []))
    if topic_type and topic_type not in topics:
        topics.append(topic_type)
    state["topics_covered"] = topics

    # ── Update mode tracking ──────────────────────────────────────────────
    new_mode = result.get("mode_used", "")
    old_mode = state.get("current_mode", "")
    if new_mode and new_mode != old_mode:
        state["current_mode"] = new_mode
        state["mode_switches"] = state.get("mode_switches", 0) + 1

    # ── Update denormalized counters ──────────────────────────────────────
    new_total = (row["total_problems"] or 0) + 1
    is_correct = outcome in ("correct", "correct_with_hints")
    # Only count toward correct if we actually assessed it
    new_correct = (row["correct_count"] or 0) + (1 if is_correct else 0)
    # Success rate only counts assessed problems
    assessed_total = sum(1 for p in problems if p.get("result") not in ("unassessed", None))
    assessed_correct = sum(1 for p in problems if p.get("result") in ("correct", "correct_with_hints"))
    new_rate = assessed_correct / assessed_total if assessed_total > 0 else 0.0

    # Average time per problem
    times = [p.get("time_seconds") for p in problems if p.get("time_seconds")]
    avg_time = sum(times) / len(times) if times else None

    # ── Write back ────────────────────────────────────────────────────────
    db.execute(
        text("""
            UPDATE agent_sessions
            SET session_state = :state,
                total_problems = :total,
                correct_count = :correct,
                session_success_rate = :rate,
                avg_time_per_problem = :avg_time
            WHERE id = :sid
        """),
        {
            "state": json.dumps(state),
            "total": new_total,
            "correct": new_correct,
            "rate": round(new_rate, 4),
            "avg_time": avg_time,
            "sid": session_id,
        },
    )
    db.commit()


async def close_session(session_id: str, db: Session) -> dict:
    """
    Close an active session.

    1. Sets is_active = false
    2. Sets ended_at = now()
    3. Computes duration_minutes
    4. Reads the session state to generate a summary via LLM
    5. Writes the summary back
    6. Returns the session data for the mastery updater

    Args:
        session_id: The active session UUID.
        db: SQLAlchemy session.

    Returns:
        Dict with session data needed by update_mastery:
        {
            "student_id": str,
            "problems": list[dict],
            "total_problems": int,
            "correct_count": int,
            "success_rate": float,
            "session_summary": str,
        }
    """
    now = datetime.now(timezone.utc)

    # ── 1. Read current session ───────────────────────────────────────────
    row = db.execute(
        text("SELECT * FROM agent_sessions WHERE id = :sid AND is_active = true"),
        {"sid": session_id},
    ).mappings().first()

    if not row:
        logger.warning(f"close_session: no active session found for {session_id}")
        return {}

    state = row["session_state"] or {}
    problems = state.get("problems_attempted", [])
    student_id = row["student_id"]

    # ── 2. Generate session summary via LLM ───────────────────────────────
    summary = await _generate_session_summary(problems, state)

    # ── 3. Close the session ──────────────────────────────────────────────
    db.execute(
        text("""
            UPDATE agent_sessions
            SET is_active = false,
                ended_at = :now,
                duration_minutes = EXTRACT(EPOCH FROM (:now - started_at)) / 60,
                session_summary = :summary
            WHERE id = :sid
        """),
        {"now": now, "summary": summary, "sid": session_id},
    )
    db.commit()

    logger.info(f"Session {session_id} closed. {len(problems)} problems, summary generated.")

    return {
        "student_id": student_id,
        "problems": problems,
        "total_problems": row["total_problems"],
        "correct_count": row["correct_count"],
        "success_rate": row["session_success_rate"],
        "session_summary": summary,
    }


async def _generate_session_summary(problems: list, state: dict) -> str:
    """
    Generate a short narrative summary of the session using the LLM.

    This summary is what future sessions will read — it needs to capture
    what happened, what improved, and what still needs work.

    Args:
        problems: The problems_attempted array from session_state.
        state: The full session_state dict.

    Returns:
        A 2-3 sentence summary string.
    """
    if not problems:
        return "Session ended with no problems attempted."

    # Build a compact representation for the LLM
    problem_lines = []
    for p in problems:
        problem_lines.append(
            f"- {p.get('type', 'unknown')}: {p.get('result', 'unknown')}, "
            f"{p.get('hints_used', 0)} hints, mode: {p.get('mode_used', 'unknown')}"
        )

    prompt = f"""Summarize this tutoring session in 2-3 sentences. Focus on:
- What topics were practiced
- What improved vs what still needs work
- Any notable patterns (mode switches, frustration, streaks)

Session data:
{chr(10).join(problem_lines)}
Streak: {state.get('streak', 0)}
Mode switches: {state.get('mode_switches', 0)}
Frustration signals: {state.get('frustration_signals', 0)}

Write a concise summary as if you're leaving a note for the next tutor."""

    try:
        response = _client.chat.completions.create(
            model=_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=200,
        )
        return response.choices[0].message.content or "Session completed."
    except Exception as e:
        logger.error(f"Failed to generate session summary: {e}")
        # Fallback: build a basic summary without LLM
        topics = ", ".join(state.get("topics_covered", []))
        total = len(problems)
        correct = sum(1 for p in problems if p.get("result") in ("correct", "correct_with_hints"))
        return f"Practiced {topics}. {correct}/{total} correct."
