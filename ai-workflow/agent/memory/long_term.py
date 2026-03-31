"""
long_term.py
Long-term memory — the student's persistent profile.

Reads from the student_profiles table once at session start to build
the context string that gets injected into the system prompt.

Writes back once at session end to update mastery scores (update_mastery).

Uses SQLAlchemy with the same engine/session as the rest of the backend.
"""

import json
import logging
from datetime import datetime, timezone

from sqlalchemy import text
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


async def get_student_context(student_id: str, db: Session) -> str:
    """
    Retrieve the student's long-term profile and format it as a context
    string for the system prompt.

    Queries student_profiles by student_id, pulls mastery scores, preferences,
    learning notes, and behavioral data, then formats everything into a
    readable block the agent can use to personalize its responses.

    Args:
        student_id: The student's ID (text, matches student_profiles.student_id).
        db: SQLAlchemy session from the FastAPI dependency.

    Returns:
        Formatted string describing the student. If no profile is found,
        returns a minimal context indicating a new student.
    """
    row = db.execute(
        text("SELECT * FROM student_profiles WHERE student_id = :sid"),
        {"sid": student_id},
    ).mappings().first()

    if not row:
        return f"**Student ID:** {student_id}\n**Status:** New student — no profile yet. Treat as a first-time learner."

    # ── Identity ──────────────────────────────────────────────────────────
    name = row["name"] or "Unknown"
    preferred_mode = row["preferred_mode"]
    hint_sensitivity = row["hint_sensitivity"]
    frustration_threshold = row["frustration_threshold"]

    # ── Hint sensitivity label ────────────────────────────────────────────
    if hint_sensitivity <= 0.3:
        hint_label = "patient — prefers to sit with hints and work through them"
    elif hint_sensitivity <= 0.6:
        hint_label = "moderate"
    else:
        hint_label = "wants faster progression and more explicit help"

    # ── Course enrollment ─────────────────────────────────────────────────
    enrollment = row["course_enrollment"] or {}
    course_name = enrollment.get("course_name", "unknown")
    current_chapter = enrollment.get("current_chapter", "?")

    # ── Last session timing ───────────────────────────────────────────────
    last_session = row["last_session_at"]
    if last_session:
        if isinstance(last_session, str):
            last_session = datetime.fromisoformat(last_session)
        days_ago = (datetime.now(timezone.utc) - last_session).days
        if days_ago == 0:
            session_recency = "today"
        elif days_ago == 1:
            session_recency = "yesterday"
        elif days_ago <= 7:
            session_recency = f"{days_ago} days ago"
        elif days_ago <= 21:
            session_recency = f"{days_ago} days ago — consider reviewing previous material"
        else:
            session_recency = f"{days_ago} days ago — extended break, start with review"
    else:
        session_recency = "never — this is their first session"

    # ── Topic mastery ─────────────────────────────────────────────────────
    topic_mastery = row["topic_mastery"] or {}
    mastery_lines = []
    for topic, data in topic_mastery.items():
        mastery = data.get("mastery", 0)
        trend = data.get("trend", "unknown")
        attempts = data.get("attempts", 0)
        avg_hints = data.get("avg_hints_needed", 0)

        # Strength label
        if mastery >= 0.8:
            strength = "strong"
        elif mastery >= 0.6:
            strength = "solid"
        elif mastery >= 0.4:
            strength = "developing"
        else:
            strength = "weak"

        mastery_lines.append(
            f"- {topic}: {mastery:.2f} ({strength}, {trend}) — "
            f"{attempts} attempts, avg {avg_hints:.1f} hints needed"
        )

    mastery_block = "\n".join(mastery_lines) if mastery_lines else "- No topics practiced yet."

    # ── Weak areas ────────────────────────────────────────────────────────
    weak_areas = row["weak_areas"] or []
    if weak_areas:
        weak_block = "\n".join(f"- {area}" for area in weak_areas)
    else:
        weak_block = "- None identified yet."

    # ── Learning notes ────────────────────────────────────────────────────
    learning_notes = row["learning_notes"] or []
    if learning_notes:
        notes_block = "\n".join(f"- {note}" for note in learning_notes)
    else:
        notes_block = "- No observations yet."

    # ── Stats ─────────────────────────────────────────────────────────────
    total_sessions = row["total_sessions"]
    total_problems = row["total_problems_attempted"]
    success_rate = row["overall_success_rate"]
    longest_streak = row["longest_streak"]

    # ── Assemble ──────────────────────────────────────────────────────────
    return f"""**Name:** {name}
**Preferred Mode:** {preferred_mode}
**Hint Sensitivity:** {hint_sensitivity} ({hint_label})
**Frustration Threshold:** {frustration_threshold} consecutive wrong answers
**Course:** {course_name}, Chapter {current_chapter}
**Last Session:** {session_recency}

**Lifetime Stats:** {total_sessions} sessions, {total_problems} problems, {success_rate:.0%} success rate, longest streak: {longest_streak}

**Topic Mastery:**
{mastery_block}

**Weak Areas:**
{weak_block}

**Learning Notes:**
{notes_block}"""


async def update_mastery(student_id: str, session_data: dict, db: Session) -> None:
    """
    Update the student's long-term profile based on a completed session.

    Runs at the END of a tutoring session. Takes the session data from
    close_session() and updates student_profiles accordingly.

    What it updates:
      - topic_mastery: exponential moving average per topic
      - mode_effectiveness: success rate per mode
      - total_sessions, total_problems_attempted
      - overall_success_rate
      - longest_streak (if beaten this session)
      - last_session_at
      - weak_areas: topics with mastery < 0.4

    Args:
        student_id: The student's ID.
        session_data: Dict from close_session() containing:
            problems, total_problems, correct_count, success_rate.
        db: SQLAlchemy session.
    """
    problems = session_data.get("problems", [])
    if not problems:
        return

    # ── Read current profile ──────────────────────────────────────────────
    row = db.execute(
        text("SELECT * FROM student_profiles WHERE student_id = :sid"),
        {"sid": student_id},
    ).mappings().first()

    if not row:
        logger.warning(f"update_mastery: no profile found for {student_id}")
        return

    topic_mastery = dict(row["topic_mastery"] or {})
    mode_effectiveness = dict(row["mode_effectiveness"] or {})
    total_sessions = (row["total_sessions"] or 0) + 1
    total_problems = (row["total_problems_attempted"] or 0) + len(problems)
    old_correct_total = round((row["overall_success_rate"] or 0) * (row["total_problems_attempted"] or 0))
    new_correct_total = old_correct_total + session_data.get("correct_count", 0)
    new_success_rate = new_correct_total / total_problems if total_problems > 0 else 0.0

    # ── Update topic mastery (exponential moving average) ─────────────────
    # alpha = 0.3 means recent performance counts 30%, history counts 70%
    alpha = 0.3

    for p in problems:
        topic = p.get("type", "")
        if not topic:
            continue

        # Skip unassessed problems — we don't know if they were right or wrong
        if p.get("result") in ("unassessed", None):
            continue

        is_correct = p.get("result") in ("correct", "correct_with_hints")
        score = 1.0 if is_correct else 0.0
        hints = p.get("hints_used", 0)
        time_secs = p.get("time_seconds")

        if topic in topic_mastery:
            entry = dict(topic_mastery[topic])
            old_mastery = entry.get("mastery", 0.5)
            entry["mastery"] = round(old_mastery * (1 - alpha) + score * alpha, 4)
            entry["attempts"] = entry.get("attempts", 0) + 1
            entry["last_practiced"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")

            # Update avg_hints_needed (running average)
            old_hints = entry.get("avg_hints_needed", 0)
            old_attempts = entry.get("attempts", 1) - 1  # before this one
            if old_attempts > 0:
                entry["avg_hints_needed"] = round(
                    (old_hints * old_attempts + hints) / (old_attempts + 1), 2
                )
            else:
                entry["avg_hints_needed"] = float(hints)

            # Update avg_time_seconds
            if time_secs:
                old_time = entry.get("avg_time_seconds", 0)
                if old_attempts > 0:
                    entry["avg_time_seconds"] = round(
                        (old_time * old_attempts + time_secs) / (old_attempts + 1), 1
                    )
                else:
                    entry["avg_time_seconds"] = float(time_secs)

            # Compute trend from mastery direction
            if entry["mastery"] > old_mastery + 0.05:
                entry["trend"] = "improving"
            elif entry["mastery"] < old_mastery - 0.05:
                entry["trend"] = "declining"
            else:
                entry["trend"] = "stable"

            topic_mastery[topic] = entry
        else:
            # New topic — first time seeing it
            topic_mastery[topic] = {
                "mastery": score,
                "attempts": 1,
                "last_practiced": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "trend": "stable",
                "avg_hints_needed": float(hints),
                "avg_time_seconds": float(time_secs) if time_secs else 0,
            }

    # ── Update mode effectiveness ─────────────────────────────────────────
    for p in problems:
        mode = p.get("mode_used", "")
        if not mode:
            continue

        # Skip unassessed — can't measure mode effectiveness without a result
        if p.get("result") in ("unassessed", None):
            continue

        is_correct = p.get("result") in ("correct", "correct_with_hints")

        if mode in mode_effectiveness:
            entry = dict(mode_effectiveness[mode])
            old_total = entry.get("total_problems", 0)
            old_rate = entry.get("success_rate", 0)
            old_correct = round(old_rate * old_total)
            new_total = old_total + 1
            new_correct = old_correct + (1 if is_correct else 0)
            entry["total_problems"] = new_total
            entry["success_rate"] = round(new_correct / new_total, 4)
            mode_effectiveness[mode] = entry
        else:
            mode_effectiveness[mode] = {
                "total_problems": 1,
                "success_rate": 1.0 if is_correct else 0.0,
            }

    # ── Determine preferred_mode from effectiveness ───────────────────────
    best_mode = "socratic"
    best_rate = 0
    for mode, data in mode_effectiveness.items():
        if data.get("total_problems", 0) >= 5 and data.get("success_rate", 0) > best_rate:
            best_rate = data["success_rate"]
            best_mode = mode

    # ── Compute weak_areas (topics with mastery < 0.4) ────────────────────
    weak_areas = []
    for topic, data in topic_mastery.items():
        if data.get("mastery", 0) < 0.4 and data.get("attempts", 0) >= 3:
            weak_areas.append(topic)

    # ── Update longest_streak ─────────────────────────────────────────────
    # Calculate the best streak from this session's problems
    session_best_streak = 0
    current_streak = 0
    for p in problems:
        if p.get("result") in ("correct", "correct_with_hints"):
            current_streak += 1
            session_best_streak = max(session_best_streak, current_streak)
        else:
            current_streak = 0

    longest_streak = max(row["longest_streak"] or 0, session_best_streak)

    # ── Compute hint_sensitivity ──────────────────────────────────────────
    # Based on average hints needed across all topics this session.
    # More hints needed → higher sensitivity (wants more help).
    # Scale: 0-3+ hints maps to 0.0-1.0
    session_hints = [p.get("hints_used", 0) for p in problems]
    if session_hints:
        avg_session_hints = sum(session_hints) / len(session_hints)
        # EMA with old value (alpha = 0.3 for new session data)
        old_sensitivity = row["hint_sensitivity"] or 0.5
        new_sensitivity = old_sensitivity * 0.7 + min(avg_session_hints / 3.0, 1.0) * 0.3
        hint_sensitivity = round(max(0.0, min(1.0, new_sensitivity)), 2)
    else:
        hint_sensitivity = row["hint_sensitivity"] or 0.5

    # ── Compute frustration_threshold ─────────────────────────────────────
    # Count consecutive wrong answers before a mode switch or session end.
    # If the student switched modes after 2 wrong, their threshold is ~2.
    frustration_signals = session_data.get("problems", [])
    consecutive_wrong = 0
    wrong_streaks = []
    for p in problems:
        if p.get("result") == "incorrect":
            consecutive_wrong += 1
        else:
            if consecutive_wrong >= 2:
                wrong_streaks.append(consecutive_wrong)
            consecutive_wrong = 0
    if consecutive_wrong >= 2:
        wrong_streaks.append(consecutive_wrong)

    if wrong_streaks:
        observed_threshold = round(sum(wrong_streaks) / len(wrong_streaks))
        # EMA with old value
        old_threshold = row["frustration_threshold"] or 3
        frustration_threshold = max(1, min(10, round(old_threshold * 0.7 + observed_threshold * 0.3)))
    else:
        frustration_threshold = row["frustration_threshold"] or 3

    # ── Compute engagement_patterns ───────────────────────────────────────
    old_patterns = dict(row["engagement_patterns"] or {})

    # Average session length (EMA)
    session_minutes = session_data.get("total_problems", 0) * 3  # rough estimate from problem count
    old_avg_length = old_patterns.get("avg_session_length_minutes", 25)
    new_avg_length = round(old_avg_length * 0.7 + session_minutes * 0.3, 1)

    # Average problems per session (EMA)
    old_avg_problems = old_patterns.get("avg_problems_per_session", 5)
    session_problem_count = len(problems)
    new_avg_problems = round(old_avg_problems * 0.7 + session_problem_count * 0.3, 1)

    # Performance trend within session
    if len(problems) >= 3:
        first_half = problems[:len(problems) // 2]
        second_half = problems[len(problems) // 2:]
        first_correct = sum(1 for p in first_half if p.get("result") in ("correct", "correct_with_hints"))
        second_correct = sum(1 for p in second_half if p.get("result") in ("correct", "correct_with_hints"))
        first_rate = first_correct / len(first_half) if first_half else 0
        second_rate = second_correct / len(second_half) if second_half else 0
        if second_rate > first_rate + 0.15:
            trend = "improves_during_session"
        elif second_rate < first_rate - 0.15:
            trend = f"declines_after_problem_{len(first_half)}"
        else:
            trend = "consistent"
    else:
        trend = old_patterns.get("performance_trend_in_session", "consistent")

    engagement_patterns = {
        "avg_session_length_minutes": new_avg_length,
        "avg_problems_per_session": new_avg_problems,
        "best_time_of_day": old_patterns.get("best_time_of_day", "unknown"),
        "performance_trend_in_session": trend,
    }

    # ── Generate learning_notes (keep existing + add new observations) ────
    existing_notes = list(row["learning_notes"] or [])
    new_notes = _generate_learning_notes(problems, session_data, existing_notes)

    # ── Write everything back ─────────────────────────────────────────────
    db.execute(
        text("""
            UPDATE student_profiles
            SET topic_mastery = :mastery,
                mode_effectiveness = :mode_eff,
                preferred_mode = :pref_mode,
                weak_areas = :weak,
                total_sessions = :sessions,
                total_problems_attempted = :problems,
                overall_success_rate = :rate,
                longest_streak = :streak,
                last_session_at = :now,
                hint_sensitivity = :hint_sens,
                frustration_threshold = :frust_thresh,
                engagement_patterns = :engage,
                learning_notes = :notes
            WHERE student_id = :sid
        """),
        {
            "mastery": json.dumps(topic_mastery),
            "mode_eff": json.dumps(mode_effectiveness),
            "pref_mode": best_mode,
            "weak": weak_areas,
            "sessions": total_sessions,
            "problems": total_problems,
            "rate": round(new_success_rate, 4),
            "streak": longest_streak,
            "now": datetime.now(timezone.utc),
            "hint_sens": hint_sensitivity,
            "frust_thresh": frustration_threshold,
            "engage": json.dumps(engagement_patterns),
            "notes": new_notes,
            "sid": student_id,
        },
    )
    db.commit()

    logger.info(
        f"Updated mastery for {student_id}: "
        f"{len(problems)} problems, {total_sessions} total sessions, "
        f"success rate {new_success_rate:.0%}"
    )


def _generate_learning_notes(
    problems: list, session_data: dict, existing_notes: list
) -> list:
    """
    Generate new learning observations from this session's data.

    Looks for patterns in the session and adds observations that aren't
    already in the existing notes. Caps at 15 total notes.

    Returns the updated notes list.
    """
    notes = list(existing_notes)

    # Pattern: student switches to direct mode when frustrated
    mode_switches = [p for p in problems if p.get("mode_source") == "student_selected"]
    if mode_switches:
        for i, p in enumerate(problems):
            if (p.get("mode_source") == "student_selected"
                    and p.get("mode_used") == "direct"
                    and i > 0
                    and problems[i - 1].get("result") == "incorrect"):
                note = "switches to Direct mode when frustrated with incorrect answers"
                if note not in notes:
                    notes.append(note)

    # Pattern: performs better with concept_first mode
    concept_first_problems = [p for p in problems if p.get("mode_used") == "concept_first"]
    if len(concept_first_problems) >= 2:
        cf_correct = sum(1 for p in concept_first_problems if p.get("result") in ("correct", "correct_with_hints"))
        cf_rate = cf_correct / len(concept_first_problems)
        if cf_rate >= 0.8:
            note = "responds well to concept-first approach — teach the idea before the problem"
            if note not in notes:
                notes.append(note)

    # Pattern: needs fewer hints over time on same topic
    topics_seen = {}
    for p in problems:
        topic = p.get("type", "")
        if topic:
            topics_seen.setdefault(topic, []).append(p.get("hints_used", 0))

    for topic, hint_counts in topics_seen.items():
        if len(hint_counts) >= 2 and hint_counts[-1] < hint_counts[0]:
            note = f"shows improvement within session on {topic} — fewer hints needed over time"
            if note not in notes:
                notes.append(note)

    # Pattern: consistently slow on specific error type
    error_counts: dict[str, int] = {}
    for p in problems:
        for err in p.get("error_types", []):
            error_counts[err] = error_counts.get(err, 0) + 1

    for err, count in error_counts.items():
        if count >= 2:
            note = f"recurring error pattern: {err}"
            if note not in notes:
                notes.append(note)

    # Cap at 15 notes — keep the most recent ones
    if len(notes) > 15:
        notes = notes[-15:]

    return notes
