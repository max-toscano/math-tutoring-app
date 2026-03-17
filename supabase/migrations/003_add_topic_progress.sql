-- ============================================================================
-- Migration 003: User Topic Progress
--
-- Tracks which subtopic each student is working on, their status, and when
-- they last accessed it. Powers the "Continue Learning" section and the
-- progress indicators on subject/topic cards.
--
-- subject + topic values match the slugs defined in constants/curriculum.ts
-- e.g. subject = 'calc-2', topic = 'taylor-maclaurin'
-- ============================================================================

CREATE TABLE user_topic_progress (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id          UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Which subject and topic (matches curriculum.ts slugs)
    subject          TEXT NOT NULL,
    topic            TEXT NOT NULL,

    -- Learning state
    status           TEXT NOT NULL DEFAULT 'not_started'
                     CHECK (status IN ('not_started', 'in_progress', 'completed')),
    messages_count   INTEGER NOT NULL DEFAULT 0,

    -- Timestamps
    last_accessed_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- One progress row per user per subtopic
    UNIQUE (user_id, subject, topic)
);

-- ─── Indexes ────────────────────────────────────────────────────────────────

-- "Continue Learning" query: get most recently accessed topics for a user
CREATE INDEX idx_topic_progress_recent
    ON user_topic_progress (user_id, last_accessed_at DESC);

-- Subject detail page: get all topic progress for a user within one subject
CREATE INDEX idx_topic_progress_subject
    ON user_topic_progress (user_id, subject);

-- ─── Row Level Security ─────────────────────────────────────────────────────

ALTER TABLE user_topic_progress ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own progress"
    ON user_topic_progress FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own progress"
    ON user_topic_progress FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own progress"
    ON user_topic_progress FOR UPDATE
    USING (auth.uid() = user_id);

-- ─── Auto-update updated_at ─────────────────────────────────────────────────

CREATE TRIGGER set_topic_progress_updated_at
    BEFORE UPDATE ON user_topic_progress
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
