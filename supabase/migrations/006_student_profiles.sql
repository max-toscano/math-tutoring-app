-- ============================================================================
-- Migration 006: Student Profiles (Long-Term Memory)
--
-- The student's permanent record. Stores everything the AI agent needs to know
-- about who a student is as a learner across 6–12 months of tutoring.
--
-- Read once at session start → injected into the system prompt.
-- Written once at session end → mastery scores updated.
--
-- This table is separate from `profiles` (which is the basic auth profile).
-- student_profiles holds learning intelligence; profiles holds account info.
-- ============================================================================


-- ─── Table ────────────────────────────────────────────────────────────────────

CREATE TABLE student_profiles (

    -- ── Identity Block ───────────────────────────────────────────────────────
    -- Who this student is. student_id is the lookup key used by the agent.

    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id      TEXT UNIQUE NOT NULL,
    name            TEXT,
    email           TEXT,

    -- ── Preference Block ─────────────────────────────────────────────────────
    -- How this student learns best. Drives mode selection and hint pacing.

    preferred_mode  TEXT NOT NULL DEFAULT 'socratic'
                    CHECK (preferred_mode IN ('socratic', 'direct', 'concept_first')),

    mode_effectiveness JSONB NOT NULL DEFAULT '{}',
        -- { "socratic": {"success_rate": 0.72, "total_problems": 45}, ... }

    hint_sensitivity FLOAT NOT NULL DEFAULT 0.5
                     CHECK (hint_sensitivity >= 0.0 AND hint_sensitivity <= 1.0),
        -- 0.2 = patient, sits with hints. 0.8 = wants faster help.

    -- ── Academic Context Block ───────────────────────────────────────────────
    -- What course and topics the student is working through.

    course_enrollment JSONB NOT NULL DEFAULT '{}',
        -- { "course_name": "trigonometry", "current_chapter": 5, "started_at": "2026-01-15" }

    topic_mastery JSONB NOT NULL DEFAULT '{}',
        -- Per-topic breakdown. Most important column in the table.
        -- { "pythagorean_identity": { "mastery": 0.72, "attempts": 24,
        --     "last_practiced": "2026-03-24", "trend": "improving",
        --     "avg_hints_needed": 1.2, "avg_time_seconds": 180 }, ... }

    weak_areas TEXT[] NOT NULL DEFAULT '{}',
        -- Specific sub-skills, not just low-mastery topics.
        -- e.g. "factoring in identity proofs", "recognizing double angle patterns"

    -- ── Behavioral Observation Block ─────────────────────────────────────────
    -- How this student behaves during tutoring. Observed over time.

    learning_notes TEXT[] NOT NULL DEFAULT '{}',
        -- Freeform observations from post-session analysis.
        -- e.g. "responds well to real-world analogies"

    frustration_threshold INT NOT NULL DEFAULT 3
                          CHECK (frustration_threshold >= 1 AND frustration_threshold <= 10),
        -- Consecutive wrong answers before student typically shows frustration.

    engagement_patterns JSONB NOT NULL DEFAULT '{}',
        -- { "avg_session_length_minutes": 25, "avg_problems_per_session": 6,
        --   "best_time_of_day": "afternoon",
        --   "performance_trend_in_session": "declines_after_problem_5" }

    -- ── Statistics Block ─────────────────────────────────────────────────────
    -- Lifetime stats. Used for experience gauging and motivation.

    total_sessions          INT NOT NULL DEFAULT 0,
    total_problems_attempted INT NOT NULL DEFAULT 0,

    overall_success_rate    FLOAT NOT NULL DEFAULT 0.0
                            CHECK (overall_success_rate >= 0.0 AND overall_success_rate <= 1.0),

    longest_streak          INT NOT NULL DEFAULT 0,

    last_session_at         TIMESTAMPTZ,
        -- NULL = never completed a session.
        -- 3+ weeks ago = agent should start with review.
        -- Yesterday = agent can pick up where they left off.

    -- ── Metadata Block ───────────────────────────────────────────────────────

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);


-- ─── Indexes ──────────────────────────────────────────────────────────────────

-- Primary lookup: the agent queries by student_id every session start.
-- UNIQUE constraint creates an implicit index, but explicit for clarity.
CREATE UNIQUE INDEX idx_student_profiles_student_id
    ON student_profiles (student_id);

-- Admin queries: find students inactive for X days.
CREATE INDEX idx_student_profiles_last_session
    ON student_profiles (last_session_at);


-- ─── Updated_at Trigger ───────────────────────────────────────────────────────
-- Reuses the update_updated_at() function from migration 001.

CREATE TRIGGER set_updated_at
    BEFORE UPDATE ON student_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();


-- ─── Row-Level Security ───────────────────────────────────────────────────────

ALTER TABLE student_profiles ENABLE ROW LEVEL SECURITY;

-- Students can read their own profile (if we ever expose this to the client).
CREATE POLICY "Students can read their own profile"
    ON student_profiles FOR SELECT
    USING (auth.uid()::text = student_id);

-- Service role has full access (used by the FastAPI backend).
CREATE POLICY "Service role has full access"
    ON student_profiles FOR ALL
    USING (auth.role() = 'service_role');


-- ─── Seed Data ────────────────────────────────────────────────────────────────
-- Test student with realistic data so we can test the agent loop immediately.

INSERT INTO student_profiles (
    student_id,
    name,
    preferred_mode,
    mode_effectiveness,
    hint_sensitivity,
    course_enrollment,
    topic_mastery,
    weak_areas,
    learning_notes,
    frustration_threshold,
    engagement_patterns,
    total_sessions,
    total_problems_attempted,
    overall_success_rate,
    longest_streak,
    last_session_at
) VALUES (
    'test_student_001',
    'Test Student',
    'socratic',
    '{
        "socratic": {"success_rate": 0.72, "total_problems": 45},
        "direct": {"success_rate": 0.55, "total_problems": 20},
        "concept_first": {"success_rate": 0.68, "total_problems": 15}
    }'::jsonb,
    0.5,
    '{
        "course_name": "trigonometry",
        "current_chapter": 5,
        "started_at": "2026-01-15"
    }'::jsonb,
    '{
        "pythagorean_identity": {
            "mastery": 0.40,
            "attempts": 12,
            "last_practiced": "2026-03-24",
            "trend": "stable",
            "avg_hints_needed": 2.1,
            "avg_time_seconds": 210
        },
        "double_angle": {
            "mastery": 0.75,
            "attempts": 8,
            "last_practiced": "2026-03-23",
            "trend": "improving",
            "avg_hints_needed": 1.0,
            "avg_time_seconds": 160
        },
        "sum_to_product": {
            "mastery": 0.30,
            "attempts": 5,
            "last_practiced": "2026-03-20",
            "trend": "declining",
            "avg_hints_needed": 2.8,
            "avg_time_seconds": 300
        }
    }'::jsonb,
    ARRAY['factoring in identity proofs', 'recognizing sum-to-product patterns'],
    ARRAY[
        'responds well to real-world analogies',
        'struggles with factoring — needs extra scaffolding',
        'gets frustrated after 3 wrong attempts'
    ],
    3,
    '{
        "avg_session_length_minutes": 25,
        "avg_problems_per_session": 6,
        "best_time_of_day": "afternoon",
        "performance_trend_in_session": "declines_after_problem_5"
    }'::jsonb,
    12,
    67,
    0.64,
    7,
    '2026-03-22T15:30:00Z'
);
