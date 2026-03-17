-- ============================================================================
-- Migration 005: Add Teaching Phase & Quiz Tracking
--
-- Extends user_topic_progress with phase tracking columns so the app knows
-- which teaching phase (lesson/practice/quiz/review/done) a student is in.
-- Adds quiz_attempts table to store full quiz history with per-question detail.
--
-- The 5-phase flow: lesson → practice → quiz → review (if failed) → quiz → done
-- Phase transitions are enforced by the app, not the AI.
-- ============================================================================

-- ─── Add phase tracking columns to user_topic_progress ─────────────────────

-- Which phase the student is currently in within this sub-chapter
-- NULL means they haven't started the structured flow yet
ALTER TABLE user_topic_progress
    ADD COLUMN phase TEXT DEFAULT NULL
    CHECK (phase IN (NULL, 'lesson', 'practice', 'quiz', 'review', 'done'));

-- Best quiz score achieved (out of 5), NULL if never quizzed
ALTER TABLE user_topic_progress
    ADD COLUMN best_quiz_score INTEGER DEFAULT NULL;

-- Total number of quiz attempts
ALTER TABLE user_topic_progress
    ADD COLUMN quiz_attempts INTEGER NOT NULL DEFAULT 0;

-- Links this topic's progress to a tutoring_session (the chat)
ALTER TABLE user_topic_progress
    ADD COLUMN session_id UUID REFERENCES tutoring_sessions(id) ON DELETE SET NULL;

-- ─── Update status CHECK to include 'failed_last_attempt' ──────────────────
-- Drop the existing constraint and recreate with the new value

ALTER TABLE user_topic_progress
    DROP CONSTRAINT IF EXISTS user_topic_progress_status_check;

ALTER TABLE user_topic_progress
    ADD CONSTRAINT user_topic_progress_status_check
    CHECK (status IN ('not_started', 'in_progress', 'completed', 'failed_last_attempt'));

-- ─── Quiz Attempts History ─────────────────────────────────────────────────
-- One row per quiz attempt. Stores full question/answer detail so the review
-- phase knows which concepts were missed and the AI can generate fresh questions.

CREATE TABLE quiz_attempts (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    progress_id     UUID NOT NULL REFERENCES user_topic_progress(id) ON DELETE CASCADE,
    subject         TEXT NOT NULL,
    chapter         TEXT NOT NULL,
    topic           TEXT NOT NULL,
    attempt_number  INTEGER NOT NULL,
    score           INTEGER NOT NULL,        -- 0-5
    passed          BOOLEAN NOT NULL,        -- score >= 3
    questions       JSONB NOT NULL,          -- [{question, student_answer, correct_answer, is_correct, concept}]
    missed_concepts JSONB DEFAULT '[]',      -- ["concept_slug_1", "concept_slug_2"]
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ─── Indexes ────────────────────────────────────────────────────────────────

-- Look up quiz history for a specific topic progress record
CREATE INDEX idx_quiz_attempts_progress
    ON quiz_attempts (progress_id, attempt_number DESC);

-- Look up all quiz attempts for a user (analytics, recent activity)
CREATE INDEX idx_quiz_attempts_user
    ON quiz_attempts (user_id, created_at DESC);

-- ─── Row Level Security ─────────────────────────────────────────────────────

ALTER TABLE quiz_attempts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own quiz attempts"
    ON quiz_attempts FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own quiz attempts"
    ON quiz_attempts FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Quiz attempts are append-only (no update/delete policies) to preserve integrity.
