"""
learn.py
Endpoints for the Learn tab — structured lessons and topic progress tracking.
Supports both flat subjects (topic list) and chaptered subjects (chapter > topic).
"""

import json
import os
from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from openai import OpenAI

from db.database import get_db
from db.models import UserTopicProgress, QuizAttempt
from api.schemas import (
    LessonRequest, LessonResponse, TopicProgress, Message,
    QuizResultResponse, QuizOutcome,
)
from api.auth_middleware import get_current_user_id
from prompts.system_prompt import build_system_prompt
from prompts.prompt_builder import build_lesson_prompt
from prompts.topic_guides import get_topic_guide
from api.phase_machine import (
    get_initial_phase, validate_transition, resolve_quiz_outcome,
    get_status_for_phase,
)
from api.quiz_scorer import (
    extract_quiz_state, process_quiz_result, is_quiz_complete,
    finalize_quiz, save_quiz_interaction,
)

router = APIRouter(prefix="/learn", tags=["learn"])

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Valid subject slugs
VALID_SUBJECTS = {
    "trigonometry", "calc-1", "calc-2", "calc-3", "diff-eq", "linear-algebra"
}

# Subject slug -> display name
SUBJECT_NAMES = {
    "trigonometry": "Trigonometry",
    "calc-1": "Calculus 1",
    "calc-2": "Calculus 2",
    "calc-3": "Calculus 3",
    "diff-eq": "Differential Equations",
    "linear-algebra": "Linear Algebra",
}

# Subjects that use chapter hierarchy
CHAPTERED_SUBJECTS = {"trigonometry", "calc-1"}

# Chapter slug -> { "_display": chapter display name, topic_slug: topic display name }
CHAPTER_NAMES: dict[str, dict[str, dict[str, str]]] = {
    "trigonometry": {
        "angles-and-measurement": {
            "_display": "Foundations — Angles and Their Measurement",
            "what-is-an-angle": "What Is an Angle?",
            "degree-measure": "Degree Measure",
            "radian-measure": "Radian Measure",
            "converting-degrees-radians": "Converting Between Degrees and Radians",
            "arc-length-sector-area": "Arc Length and Sector Area",
            "angular-linear-speed": "Angular and Linear Speed",
        },
        "right-triangle-trig": {
            "_display": "Right Triangle Trigonometry",
            "six-trig-ratios": "The Six Trigonometric Ratios",
            "evaluating-trig-acute": "Evaluating Trig Functions of Acute Angles",
            "special-right-triangles": "Special Right Triangles",
            "cofunctions-complementary": "Cofunctions and Complementary Angles",
            "solving-right-triangles": "Solving Right Triangles",
            "right-triangle-applications": "Applications of Right Triangle Trigonometry",
        },
        "unit-circle": {
            "_display": "The Unit Circle",
            "defining-unit-circle": "Defining the Unit Circle",
            "trig-any-angle": "Trig Functions for Any Angle",
            "reference-angles": "Reference Angles",
            "memorizing-unit-circle": "Memorizing the Unit Circle",
            "quadrantal-angles": "Quadrantal Angles",
            "unit-circle-expressions": "Using the Unit Circle to Evaluate Expressions",
        },
        "trig-as-functions": {
            "_display": "Trigonometric Functions as Functions",
            "domain-and-range": "Domain and Range",
            "even-odd-trig": "Even and Odd Trig Functions",
            "periodicity": "Periodicity",
            "fundamental-identities-intro": "Fundamental Identities — First Look",
        },
        "graphing-trig": {
            "_display": "Graphs of Trigonometric Functions",
            "graphing-sine-cosine": "Graphing Sine and Cosine",
            "amplitude-vertical-shift": "Transformations — Amplitude and Vertical Shift",
            "period-phase-shift": "Transformations — Period and Phase Shift",
            "graphing-tan-cot": "Graphing Tangent and Cotangent",
            "graphing-sec-csc": "Graphing Secant and Cosecant",
            "sinusoidal-modeling": "Sinusoidal Modeling",
        },
        "inverse-trig": {
            "_display": "Inverse Trigonometric Functions",
            "restricted-domains": "Why Inverses Require Restricted Domains",
            "arcsine": "Arcsine",
            "arccosine": "Arccosine",
            "arctangent": "Arctangent",
            "inverse-csc-sec-cot": "Inverse Cosecant, Secant, and Cotangent",
            "compositions-trig-inverse": "Compositions of Trig and Inverse Trig Functions",
        },
        "trig-identities": {
            "_display": "Trigonometric Identities",
            "fundamental-identities-review": "Review of Fundamental Identities",
            "proving-identities": "Proving (Verifying) Identities",
            "sum-difference-identities": "Sum and Difference Identities",
            "double-angle-identities": "Double-Angle Identities",
            "half-angle-identities": "Half-Angle Identities",
            "product-sum-identities": "Product-to-Sum and Sum-to-Product Identities",
        },
        "trig-equations": {
            "_display": "Trigonometric Equations",
            "basic-trig-equations": "Solving Basic Trig Equations",
            "single-trig-function": "Equations Involving a Single Trig Function",
            "equations-requiring-identities": "Equations Requiring Identities",
            "multiple-angle-equations": "Equations with Multiple Angles",
            "equations-inverse-trig": "Equations Involving Inverse Trig Functions",
            "trig-equation-applications": "Applications of Trig Equations",
        },
        "law-of-sines-cosines": {
            "_display": "The Laws of Sines and Cosines",
            "when-right-triangle-fails": "When Right-Triangle Methods Aren't Enough",
            "law-of-sines": "The Law of Sines",
            "ambiguous-case": "The Ambiguous Case — Deep Dive",
            "law-of-cosines": "The Law of Cosines",
            "triangle-area": "Area of a Triangle",
            "oblique-triangle-applications": "Applications of Oblique Triangles",
        },
        "vectors-and-trig": {
            "_display": "Vectors and Trigonometry",
            "intro-to-vectors": "Introduction to Vectors",
            "vector-operations": "Vector Operations",
            "unit-vectors-direction": "Unit Vectors and Direction Angles",
            "dot-product": "The Dot Product",
            "vector-projections-work": "Vector Projections and Work",
            "vector-applications": "Applications of Vectors",
        },
        "polar-and-complex": {
            "_display": "Polar Coordinates and Complex Numbers",
            "polar-coordinate-system": "The Polar Coordinate System",
            "polar-rectangular-conversion": "Converting Between Polar and Rectangular",
            "polar-equation-graphs": "Graphs of Polar Equations",
            "complex-trig-form": "Complex Numbers in Trigonometric (Polar) Form",
            "complex-multiply-divide": "Multiplication and Division in Trigonometric Form",
            "demoivres-theorem": "De Moivre's Theorem and Roots of Complex Numbers",
        },
        "parametric-and-applications": {
            "_display": "Parametric Equations and Trig Applications",
            "parametric-basics": "Parametric Equations — Basics",
            "parametric-trig-curves": "Parametric Curves with Trigonometric Functions",
            "projectile-motion": "Projectile Motion",
            "simple-harmonic-motion": "Simple Harmonic Motion",
            "combining-sinusoidal": "Combining Sinusoidal Functions",
        },
        "additional-topics": {
            "_display": "Additional Topics and Course Wrap-Up",
            "trig-substitution-preview": "Trigonometric Substitution Preview (Calculus Bridge)",
            "hyperbolic-trig-intro": "Hyperbolic Trig Functions — Brief Introduction",
            "common-mistakes": "Common Mistakes and How to Avoid Them",
            "problem-solving-strategies": "Problem-Solving Strategies — Summary",
            "course-review": "Course Review and Final Assessment Guide",
        },
    },
    "calc-1": {
        "functions-review": {
            "_display": "Functions and Their Properties",
            "functions-and-notation": "Functions and Function Notation",
            "domain-and-range": "Domain and Range",
            "combining-functions": "Combining Functions",
            "transformations": "Transformations of Functions",
            "polynomial-rational-functions": "Polynomial and Rational Functions",
            "transcendental-functions-review": "Trig, Exponential, and Logarithmic Functions",
        },
        "limits": {
            "_display": "Limits — The Foundation of Calculus",
            "idea-of-a-limit": "The Idea of a Limit",
            "limits-from-graphs-tables": "Finding Limits from Graphs and Tables",
            "limit-laws": "Limit Laws and Algebraic Techniques",
            "limits-involving-infinity": "Limits Involving Infinity",
            "squeeze-theorem": "The Squeeze Theorem",
            "epsilon-delta": "The Formal Definition of a Limit",
        },
        "continuity": {
            "_display": "Continuity",
            "what-is-continuity": "What Is Continuity?",
            "types-of-discontinuities": "Types of Discontinuities",
            "continuity-on-interval": "Continuity on an Interval",
            "intermediate-value-theorem": "The Intermediate Value Theorem",
        },
        "defining-the-derivative": {
            "_display": "Defining the Derivative",
            "tangent-lines-rates-of-change": "Tangent Lines and Rates of Change",
            "derivative-at-a-point": "The Derivative at a Point",
            "derivative-as-a-function": "The Derivative as a Function",
            "differentiability-vs-continuity": "Differentiability vs. Continuity",
            "interpreting-the-derivative": "Interpreting the Derivative",
        },
        "differentiation-rules": {
            "_display": "Differentiation Rules",
            "power-rule": "The Power Rule",
            "constant-sum-difference-rules": "Constant Multiple, Sum, and Difference Rules",
            "product-rule": "The Product Rule",
            "quotient-rule": "The Quotient Rule",
            "derivatives-of-trig": "Derivatives of Trigonometric Functions",
            "higher-order-derivatives": "Higher-Order Derivatives",
        },
        "chain-rule-and-advanced": {
            "_display": "The Chain Rule and Advanced Differentiation",
            "chain-rule": "The Chain Rule",
            "implicit-differentiation": "Implicit Differentiation",
            "derivatives-of-inverse-trig": "Derivatives of Inverse Trig Functions",
            "derivatives-of-exponentials": "Derivatives of Exponential Functions",
            "derivatives-of-logarithms": "Derivatives of Logarithmic Functions",
            "logarithmic-differentiation": "Logarithmic Differentiation",
        },
        "applications-of-derivatives-1": {
            "_display": "Applications of Derivatives — Part 1",
            "related-rates": "Related Rates",
            "linear-approximation": "Linear Approximation and Differentials",
            "mean-value-theorem": "The Mean Value Theorem",
            "lhopitals-rule": "L'Hopital's Rule",
            "newtons-method": "Newton's Method",
        },
        "analyzing-functions": {
            "_display": "Analyzing Functions with Derivatives",
            "increasing-decreasing": "Increasing and Decreasing Functions",
            "first-derivative-test": "The First Derivative Test",
            "concavity-second-derivative": "Concavity and the Second Derivative",
            "second-derivative-test": "The Second Derivative Test",
            "curve-sketching": "Curve Sketching — Putting It All Together",
        },
        "optimization": {
            "_display": "Optimization",
            "absolute-extrema": "Absolute (Global) Extrema",
            "closed-interval-method": "The Closed Interval Method",
            "applied-optimization": "Applied Optimization Problems",
            "optimization-strategies": "Optimization Problem-Solving Strategies",
        },
        "intro-to-integration": {
            "_display": "Introduction to Integration",
            "antiderivatives": "Antiderivatives",
            "basic-antidifferentiation": "Basic Antidifferentiation Rules",
            "sigma-notation": "Sigma Notation and Summation Formulas",
            "riemann-sums": "Riemann Sums and Area Under a Curve",
            "the-definite-integral": "The Definite Integral",
        },
        "fundamental-theorem": {
            "_display": "The Fundamental Theorem of Calculus",
            "ftc-part-1": "The Fundamental Theorem of Calculus, Part 1",
            "ftc-part-2": "The Fundamental Theorem of Calculus, Part 2",
            "net-change-theorem": "The Net Change Theorem",
            "properties-of-definite-integrals": "Properties of Definite Integrals",
        },
        "integration-techniques": {
            "_display": "Integration Techniques",
            "u-substitution-indefinite": "U-Substitution (Indefinite Integrals)",
            "u-substitution-definite": "U-Substitution with Definite Integrals",
            "integrals-exp-log": "Integrals of Exponential and Logarithmic Functions",
            "integrals-trig": "Integrals of Trigonometric Functions",
            "integrals-inverse-trig": "Integrals Resulting in Inverse Trig Functions",
        },
        "applications-of-integration": {
            "_display": "Applications of Integration",
            "area-between-curves": "Area Between Curves",
            "volumes-disk-washer": "Volumes by Disk and Washer Methods",
            "volumes-shells": "Volumes by Cylindrical Shells",
            "average-value": "Average Value of a Function",
            "calc1-review": "Course Review and What Comes Next",
        },
    },
}

# Flat topic names for non-chaptered subjects
TOPIC_NAMES: dict[str, dict[str, str]] = {
    "calc-2": {
        "integration-techniques": "Integration Techniques",
        "improper-integrals": "Improper Integrals",
        "sequences-series": "Sequences & Series",
        "convergence-tests": "Convergence Tests",
        "taylor-maclaurin": "Taylor & Maclaurin Series",
        "parametric-polar": "Parametric & Polar Curves",
        "arc-length-surface-area": "Arc Length & Surface Area",
    },
    "calc-3": {
        "vectors-vector-functions": "Vectors & Vector Functions",
        "partial-derivatives": "Partial Derivatives",
        "multiple-integrals": "Multiple Integrals",
        "vector-fields": "Vector Fields",
        "line-surface-integrals": "Line & Surface Integrals",
        "fundamental-theorems": "Green's, Stokes' & Divergence Theorems",
        "coordinate-systems": "Cylindrical & Spherical Coordinates",
    },
    "diff-eq": {
        "first-order-odes": "First Order ODEs",
        "second-order-odes": "Second Order Linear ODEs",
        "laplace-transforms": "Laplace Transforms",
        "systems-of-odes": "Systems of ODEs",
        "series-solutions": "Series Solutions",
        "numerical-methods": "Numerical Methods",
        "applications": "Applications",
    },
    "linear-algebra": {
        "systems-row-reduction": "Systems of Equations & Row Reduction",
        "matrix-operations": "Matrix Operations & Inverses",
        "determinants": "Determinants",
        "vector-spaces": "Vector Spaces & Subspaces",
        "eigenvalues-eigenvectors": "Eigenvalues & Eigenvectors",
        "orthogonality": "Orthogonality & Least Squares",
        "linear-transformations": "Linear Transformations",
    },
}


def _validate_subject_chapter_topic(
    subject: str, chapter: str | None, topic: str
) -> tuple[str, str | None, str]:
    """Validate slugs and return (subject_display, chapter_display, topic_display)."""
    if subject not in VALID_SUBJECTS:
        raise HTTPException(400, f"Invalid subject '{subject}'. Valid: {sorted(VALID_SUBJECTS)}")

    if subject in CHAPTERED_SUBJECTS:
        if not chapter:
            raise HTTPException(400, f"Subject '{subject}' requires a chapter parameter.")
        chapters = CHAPTER_NAMES.get(subject, {})
        if chapter not in chapters:
            raise HTTPException(400, f"Invalid chapter '{chapter}' for subject '{subject}'.")
        chapter_data = chapters[chapter]
        if topic not in chapter_data:
            raise HTTPException(400, f"Invalid topic '{topic}' for chapter '{chapter}'.")
        return SUBJECT_NAMES[subject], chapter_data["_display"], chapter_data[topic]
    else:
        topics = TOPIC_NAMES.get(subject, {})
        if topic not in topics:
            raise HTTPException(400, f"Invalid topic '{topic}' for subject '{subject}'.")
        return SUBJECT_NAMES[subject], None, topics[topic]


def _progress_to_schema(r: UserTopicProgress) -> TopicProgress:
    """Convert a DB row to the TopicProgress response schema."""
    return TopicProgress(
        subject=r.subject,
        chapter=r.chapter if r.chapter != "_default" else None,
        topic=r.topic,
        status=r.status,
        phase=r.phase,
        messages_count=r.messages_count,
        last_accessed_at=r.last_accessed_at.isoformat() if r.last_accessed_at else None,
    )


def _chapter_value(chapter: str | None) -> str:
    """Convert an optional chapter slug to the DB value."""
    return chapter if chapter else "_default"


# ---------------------------------------------------------------------------
# GET /learn/progress — all topic progress for user
# ---------------------------------------------------------------------------

@router.get("/progress", response_model=list[TopicProgress])
def get_all_progress(
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Return all topic progress records for the current user."""
    rows = (
        db.query(UserTopicProgress)
        .filter(UserTopicProgress.user_id == user_id)
        .order_by(UserTopicProgress.last_accessed_at.desc())
        .all()
    )
    return [_progress_to_schema(r) for r in rows]


# ---------------------------------------------------------------------------
# GET /learn/progress/{subject} — per-topic progress within a subject
# ---------------------------------------------------------------------------

@router.get("/progress/{subject}", response_model=list[TopicProgress])
def get_subject_progress(
    subject: str,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Return topic progress for a specific subject."""
    if subject not in VALID_SUBJECTS:
        raise HTTPException(400, f"Invalid subject '{subject}'.")
    rows = (
        db.query(UserTopicProgress)
        .filter(
            UserTopicProgress.user_id == user_id,
            UserTopicProgress.subject == subject,
        )
        .all()
    )
    return [_progress_to_schema(r) for r in rows]


# ---------------------------------------------------------------------------
# POST /learn/lesson — core lesson endpoint (calls OpenAI)
# ---------------------------------------------------------------------------

@router.post("/lesson", response_model=LessonResponse)
def lesson(
    req: LessonRequest,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Send a lesson message (or start a new lesson) and get AI teaching response.

    Phase-aware: uses prompt_builder for topics with guides (Chapter 1),
    falls back to generic prompt for others.
    """
    subject_name, chapter_name, topic_name = _validate_subject_chapter_topic(
        req.subject, req.chapter, req.topic
    )

    # ── 1. Load or create progress row ──────────────────────────────────────
    chapter_val = _chapter_value(req.chapter)
    now = datetime.now(timezone.utc)
    progress = (
        db.query(UserTopicProgress)
        .filter(
            UserTopicProgress.user_id == user_id,
            UserTopicProgress.subject == req.subject,
            UserTopicProgress.chapter == chapter_val,
            UserTopicProgress.topic == req.topic,
        )
        .first()
    )
    if not progress:
        progress = UserTopicProgress(
            user_id=user_id,
            subject=req.subject,
            chapter=chapter_val,
            topic=req.topic,
            status="in_progress",
            phase=get_initial_phase(),
            messages_count=0,
            last_accessed_at=now,
        )
        db.add(progress)
        db.flush()  # need progress.id for quiz_attempts FK

    # First visit: ensure phase is set
    if progress.phase is None:
        progress.phase = get_initial_phase()

    current_phase = progress.phase

    # ── 2. Build system prompt ──────────────────────────────────────────────
    guide = get_topic_guide(req.topic)
    if guide:
        # Get completed topics for context
        completed_rows = (
            db.query(UserTopicProgress.topic)
            .filter(
                UserTopicProgress.user_id == user_id,
                UserTopicProgress.subject == req.subject,
                UserTopicProgress.status == "completed",
            )
            .all()
        )
        completed_topics = [r.topic for r in completed_rows]

        # Get missed concepts if in review phase
        missed_concepts = None
        if current_phase == "review":
            latest_attempt = (
                db.query(QuizAttempt)
                .filter(QuizAttempt.progress_id == progress.id)
                .order_by(QuizAttempt.attempt_number.desc())
                .first()
            )
            if latest_attempt and latest_attempt.missed_concepts:
                missed_concepts = latest_attempt.missed_concepts

        system_prompt = build_lesson_prompt(
            topic_slug=req.topic,
            phase=current_phase,
            quiz_attempt_number=progress.quiz_attempts or 0,
            missed_concepts=missed_concepts,
            completed_topics=completed_topics,
            subject=req.subject,
        )
    else:
        # Fallback for topics without guides
        system_prompt = build_system_prompt(
            subject_name, "lesson", topic=topic_name, chapter=chapter_name
        )

    # ── 3. Build OpenAI messages ────────────────────────────────────────────
    messages = [{"role": "system", "content": system_prompt}]

    if req.conversation_history:
        for msg in req.conversation_history:
            messages.append({"role": msg.role, "content": msg.content})

    if req.student_input:
        messages.append({"role": "user", "content": req.student_input})
    else:
        messages.append({
            "role": "user",
            "content": "I'm ready to learn. Please introduce this topic and start teaching me.",
        })

    # ── 4. Call OpenAI ──────────────────────────────────────────────────────
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o"),
        messages=messages,
        temperature=0.4,
        max_tokens=2500,
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content
    llm_result = json.loads(raw)

    # ── 5. Extract fields from AI response ──────────────────────────────────
    ai_message = llm_result.get("message", llm_result.get("response_text", ""))
    ai_images = llm_result.get("images", [])
    ai_quiz_result = llm_result.get("quiz_result")
    ai_quiz_summary = llm_result.get("quiz_summary")
    ai_phase_transition = llm_result.get("phase_transition")

    quiz_result_resp = None
    quiz_outcome_resp = None

    # ── 6. Quiz scoring (if in quiz phase) ──────────────────────────────────
    if current_phase == "quiz" and guide:
        # Rebuild quiz state from history
        history_dicts = [
            {"role": m.role, "content": m.content}
            for m in (req.conversation_history or [])
        ]
        quiz_state = extract_quiz_state(history_dicts)

        # Process this response's quiz_result
        if ai_quiz_result:
            quiz_state = process_quiz_result(llm_result, quiz_state)
            quiz_result_resp = QuizResultResponse(
                is_correct=ai_quiz_result.get("is_correct", False),
                explanation=ai_quiz_result.get("explanation", ""),
                running_score=ai_quiz_result.get("running_score"),
                concept_tested=ai_quiz_result.get("concept_tested"),
            )

            # Save quiz interaction
            if req.student_input:
                save_quiz_interaction(
                    db, user_id, req.subject, req.topic,
                    req.student_input, ai_message, ai_quiz_result,
                )

        # After question 5: finalize quiz
        if is_quiz_complete(quiz_state):
            outcome = finalize_quiz(
                db, user_id, progress, quiz_state, ai_quiz_summary,
            )
            quiz_outcome_resp = QuizOutcome(**outcome)
            # Phase was updated by finalize_quiz
            current_phase = progress.phase

    # ── 7. Handle phase transitions (non-quiz) ─────────────────────────────
    if ai_phase_transition and not quiz_outcome_resp:
        new_phase = validate_transition(current_phase, ai_phase_transition)
        if new_phase:
            progress.phase = new_phase
            progress.status = get_status_for_phase(new_phase)
            current_phase = new_phase

    # ── 8. Update progress bookkeeping ──────────────────────────────────────
    progress.messages_count += 1
    progress.last_accessed_at = now
    progress.updated_at = now
    db.commit()

    # ── 9. Build response ───────────────────────────────────────────────────
    new_history = list(req.conversation_history or [])
    if req.student_input:
        new_history.append(Message(role="user", content=req.student_input))
    new_history.append(Message(role="assistant", content=raw))

    return LessonResponse(
        message=ai_message,
        response_text=ai_message,  # legacy compat
        phase=current_phase,
        images=ai_images,
        quiz_result=quiz_result_resp,
        quiz_outcome=quiz_outcome_resp,
        conversation_history=new_history,
    )


# ---------------------------------------------------------------------------
# POST /learn/complete — mark a topic as completed
# ---------------------------------------------------------------------------

@router.post("/complete")
def mark_complete(
    req: LessonRequest,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Mark a topic as completed for the current user."""
    _validate_subject_chapter_topic(req.subject, req.chapter, req.topic)

    chapter_val = _chapter_value(req.chapter)
    now = datetime.now(timezone.utc)
    progress = (
        db.query(UserTopicProgress)
        .filter(
            UserTopicProgress.user_id == user_id,
            UserTopicProgress.subject == req.subject,
            UserTopicProgress.chapter == chapter_val,
            UserTopicProgress.topic == req.topic,
        )
        .first()
    )
    if progress:
        progress.status = "completed"
        progress.updated_at = now
    else:
        progress = UserTopicProgress(
            user_id=user_id,
            subject=req.subject,
            chapter=chapter_val,
            topic=req.topic,
            status="completed",
            messages_count=0,
            last_accessed_at=now,
        )
        db.add(progress)
    db.commit()

    return {"status": "completed", "subject": req.subject, "topic": req.topic}
