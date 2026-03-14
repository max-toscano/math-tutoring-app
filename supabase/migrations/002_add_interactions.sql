-- ============================================================================
-- Add interactions table for tutoring progress tracking
-- Run this in the Supabase SQL Editor after 001_initial_schema.sql
-- ============================================================================

-- ─── Interactions ───────────────────────────────────────────────────────────
-- Every tutoring Q&A exchange. Core analytics table for progress tracking.
-- The progress API computes accuracy, weak areas, and mistake patterns from this.

CREATE TABLE interactions (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    subject     TEXT NOT NULL,                -- "math", "chemistry", "physics"
    topic       TEXT,                         -- AI-determined: "algebra", "stoichiometry"
    mode        TEXT NOT NULL,                -- "socratic", "hint", "direct", "check_work"
    student_input TEXT NOT NULL,
    ai_response   TEXT NOT NULL,
    is_correct  BOOLEAN,                     -- null if not an answer-check
    mistake_type TEXT,                        -- "sign_error", "wrong_formula", etc.
    difficulty  TEXT,                         -- "Easy", "Medium", "Hard"
    concepts    JSONB DEFAULT '[]',           -- array of concept strings
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ─── Indexes ────────────────────────────────────────────────────────────────

CREATE INDEX idx_interactions_user    ON interactions (user_id, created_at DESC);
CREATE INDEX idx_interactions_subject ON interactions (user_id, subject);
CREATE INDEX idx_interactions_topic   ON interactions (user_id, subject, topic);

-- ─── Row-Level Security ─────────────────────────────────────────────────────

ALTER TABLE interactions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own interactions"
    ON interactions FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own interactions"
    ON interactions FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Note: interactions are append-only (no update/delete) to preserve analytics integrity.
-- If you need users to delete their data (GDPR), the CASCADE on user_id handles full account deletion.
