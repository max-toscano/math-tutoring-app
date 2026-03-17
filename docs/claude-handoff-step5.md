# MathHelper — Structured Learning Implementation: Handoff at Step 5

## Where We Left Off

We are implementing a 5-phase structured teaching flow for a React Native math tutoring app. Steps 1-4 are COMPLETE. Step 5 (Quiz Scoring Logic) is next.

## What's Already Built (Steps 1-4 COMPLETE)

### Step 1: Migration 005 — DONE
File: `supabase/migrations/005_add_phase_quiz_tracking.sql`

Added to `user_topic_progress`:
- `phase` TEXT — lesson | practice | quiz | review | done (NULL = not started)
- `best_quiz_score` INTEGER — best score out of 5
- `quiz_attempts` INTEGER — total quiz attempts
- `session_id` UUID — FK to tutoring_sessions

Created `quiz_attempts` table:
- Stores full quiz history: questions (JSONB), score, passed, missed_concepts
- Append-only (insert + select only, no update/delete)
- RLS enabled

Updated `user_topic_progress.status` CHECK to include `'failed_last_attempt'`.

SQLAlchemy models updated in `ai-workflow/db/models.py`:
- `UserTopicProgress` has the 4 new columns
- New `QuizAttempt` model added

**NOTE: This migration needs to be run in Supabase SQL Editor if not already done.**

### Step 2: Course Data for Chapter 1 — DONE
File: `ai-workflow/prompts/topic_guides.py`

Contains `TOPIC_GUIDES` dict with structured teaching content for all 6 sub-chapters of Chapter 1 (Foundations — Angles and Their Measurement):
- `what-is-an-angle` (1.1)
- `degree-measure` (1.2)
- `radian-measure` (1.3)
- `converting-degrees-radians` (1.4)
- `arc-length-sector-area` (1.5)
- `angular-linear-speed` (1.6)

Each guide has: chunked teaching_content, key_concepts (slugs), available_images, practice_problems, quiz_guidelines, common_mistakes, prerequisites, builds_toward.

Helper functions: `get_topic_guide(slug)`, `get_chapter_guides(chapter_slug)`, `get_key_concepts(slug)`

### Step 3: Prompt Builder — DONE
File: `ai-workflow/prompts/prompt_builder.py`

`build_lesson_prompt()` assembles a full system prompt from 7 sections:
- [A] Role & Personality (static — warm, patient tutor)
- [B] Sub-chapter Content (from topic_guides.py)
- [C] Phase Rules (different instructions per phase)
- [D] Student Progress (completed topics, prerequisites)
- [E] Available Images (image IDs for this topic)
- [F] Response Format (JSON schema the AI must follow)
- [G] Constraints (guardrails — stay on topic, never decide pass/fail, etc.)

Signature:
```python
def build_lesson_prompt(
    topic_slug: str,
    phase: str,                          # "lesson" | "practice" | "quiz" | "review" | "done"
    quiz_attempt_number: int = 0,
    missed_concepts: list[str] = None,
    completed_topics: list[str] = None,
) -> str:
```

Falls back to old generic `system_prompt.py` for topics without guides (Chapters 2-13).

### Step 4: Phase State Machine — DONE
File: `ai-workflow/api/phase_machine.py`

Controls phase transitions. The APP decides, not the AI.

Functions:
- `get_initial_phase()` → returns `"lesson"`
- `validate_transition(current_phase, requested_phase)` → returns new phase or None (rejected)
- `resolve_quiz_outcome(score)` → score >= 3 = `"done"`, < 3 = `"review"`
- `get_status_for_phase(phase, quiz_passed)` → maps phase to status string
- `can_skip_to_quiz(current_phase)` → True only from None or "lesson"

Valid transitions:
```
None       → lesson
lesson     → practice, quiz
practice   → quiz
quiz       → (app only: done or review via resolve_quiz_outcome)
review     → quiz
done       → (terminal)
```

The AI CANNOT set done or review directly. Those only come from `resolve_quiz_outcome()` after all 5 quiz questions.

---

## What Still Needs To Be Built (Steps 5-8)

### Step 5: Quiz Scoring Logic ← START HERE
Track quiz answers as they come in, enforce the 3/5 pass rule, and save results.

Needs to handle:
- Local state tracking: { question_number, correct_count, answers[] } across the 5-question quiz
- Parsing `quiz_result` from each GPT response (after each quiz answer)
- After question 5: parsing `quiz_summary`, checking score against threshold
- Inserting a row into `quiz_attempts` table with full question/answer detail
- Updating `user_topic_progress`: best_quiz_score, quiz_attempts count, status, phase
- Saving individual quiz interactions to `interactions` table

The AI responds with this during quiz:
```json
{
  "message": "That's correct! ...",
  "quiz_result": {
    "is_correct": true,
    "explanation": "Why right/wrong",
    "running_score": { "correct": 2, "total": 3 },
    "concept_tested": "dms_to_decimal_conversion"
  }
}
```

After question 5, the AI also includes:
```json
{
  "quiz_summary": {
    "passed": true,
    "final_score": 4,
    "missed_concepts": ["coterminal_angles"],
    "message": "Great job! You got 4 out of 5."
  }
}
```

The app validates the score and calls `resolve_quiz_outcome()` from phase_machine.py — it does NOT trust the AI's `passed` field.

### Step 6: Wire Everything Together
Connect Steps 2-5 to the existing `/learn/lesson` endpoint in `ai-workflow/api/routes/learn.py`.

Currently the endpoint:
1. Validates subject/chapter/topic slugs
2. Calls `build_system_prompt()` (old generic prompt)
3. Sends to OpenAI
4. Parses simple JSON response (response_text + assessment)
5. Upserts user_topic_progress
6. Returns response

Needs to become:
1. Validates subject/chapter/topic slugs (same)
2. Loads user_topic_progress row (get current phase, quiz_attempts)
3. If first visit: set phase to "lesson"
4. Calls `build_lesson_prompt()` (NEW — phase-aware prompt from prompt_builder.py)
5. Sends to OpenAI with response_format=json
6. Parses structured JSON response (message, quiz_result, quiz_summary, phase_transition, images)
7. If quiz_result: track score, save to interactions
8. If quiz_summary: insert quiz_attempts row, call resolve_quiz_outcome(), update progress
9. If phase_transition: call validate_transition(), update progress.phase
10. Update messages_count, last_accessed_at, status
11. Returns full structured response to frontend

The frontend lesson.tsx also needs updates to:
- Display the new JSON response format (message field instead of response_text)
- Show quiz results inline
- Handle phase transitions (update header badge)
- Show images when the AI references them

### Step 7: Pre-Made Image System
- Create static images for Chapter 1 (~2-3 per sub-chapter)
- Image catalog mapping IDs to asset paths
- Chat bubble component renders images inline when AI references them

### Step 8: Full Flow Test
- Test complete flow: lesson → practice → quiz (pass) → done
- Test fail flow: lesson → quiz (fail) → review → quiz (pass) → done
- Verify all database records update correctly

---

## Existing Codebase — Critical Files to Read

Before implementing, READ these files to understand the current code:

### Backend (Python/FastAPI)
- `ai-workflow/api/routes/learn.py` — Current lesson endpoint (needs modification in Step 6)
- `ai-workflow/api/schemas.py` — Pydantic models (LessonRequest, LessonResponse — may need updates)
- `ai-workflow/api/auth_middleware.py` — JWT auth (don't touch)
- `ai-workflow/db/models.py` — SQLAlchemy models (already updated in Step 1)
- `ai-workflow/db/database.py` — DB session factory
- `ai-workflow/prompts/prompt_builder.py` — Phase-aware prompt builder (Step 3)
- `ai-workflow/prompts/topic_guides.py` — Teaching content for Chapter 1 (Step 2)
- `ai-workflow/prompts/system_prompt.py` — Old generic prompt (Tutor tab still uses this)
- `ai-workflow/api/phase_machine.py` — Phase transition validator (Step 4)

### Frontend (TypeScript/React Native)
- `frontend/mathhelper/app/learn/lesson.tsx` — Chat screen (needs updates in Step 6)
- `frontend/mathhelper/services/learn.ts` — API client for Learn endpoints
- `frontend/mathhelper/services/api.ts` — Shared apiFetch() with Supabase JWT
- `frontend/mathhelper/constants/curriculums/math.ts` — Curriculum data (all 73 trig topics)
- `frontend/mathhelper/constants/curriculums/index.ts` — Types and helpers
- `frontend/mathhelper/app/learn/[subject].tsx` — Subject detail screen
- `frontend/mathhelper/app/learn/chapter.tsx` — Chapter detail screen
- `frontend/mathhelper/app/(tabs)/learn.tsx` — Learn tab entry

### Database
- `supabase/migrations/005_add_phase_quiz_tracking.sql` — The migration from Step 1

---

## The 5-Phase Teaching Flow (Reference)

```
LESSON → PRACTICE → QUIZ (5 questions, 3/5 to pass) → REVIEW (if fail) → DONE
                                    ↑                          |
                                    └──────────────────────────┘
                                         (retry with fresh questions)
```

- Student can skip PRACTICE and go straight to QUIZ from LESSON
- Quiz always has exactly 5 questions
- Pass threshold: 3 out of 5
- Review only covers missed concepts, then retries quiz with fresh questions
- Done is terminal — revisiting doesn't reset completion

## AI Response JSON Schema (All Phases)

```json
{
  "message": "Conversational message (markdown)",
  "images": ["image_id"],
  "question": {
    "type": "multiple_choice | free_response",
    "text": "Question text",
    "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
    "correct_answer": "A",
    "question_number": 3
  },
  "quiz_result": {
    "is_correct": true,
    "explanation": "Why right/wrong",
    "running_score": { "correct": 2, "total": 3 },
    "concept_tested": "concept_slug"
  },
  "quiz_summary": {
    "passed": true,
    "final_score": 4,
    "missed_concepts": ["slug"],
    "message": "Score summary"
  },
  "phase_transition": "practice | quiz | review | done"
}
```

All fields except `message` are optional.

---

## How to Run

```bash
# Backend (port 8000)
cd ai-workflow && uvicorn api.main:app --reload

# Frontend (port 8081)
cd frontend/mathhelper && npx expo start --web
```

## Environment
- Backend: FastAPI + Python, OpenAI GPT-4o, SQLAlchemy, Supabase Postgres
- Frontend: React Native + Expo, TypeScript, Supabase JS client
- Auth: Supabase JWT (ES256 via JWKS)
