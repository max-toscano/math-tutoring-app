-- ============================================================================
-- Migration 004: Add Chapter Layer
--
-- Adds a `chapter` column to user_topic_progress to support hierarchical
-- curriculum structure (Subject > Chapter > Topic). Subjects without chapters
-- use the sentinel value '_default'.
--
-- Trigonometry is being restructured from 7 flat topics into 13 chapters
-- with ~5-6 sub-chapters each. Other subjects remain flat for now.
-- ============================================================================

-- ─── Add chapter column ───────────────────────────────────────────────────────
-- Existing rows get '_default' meaning "flat subject, no chapter hierarchy"
ALTER TABLE user_topic_progress
    ADD COLUMN chapter TEXT NOT NULL DEFAULT '_default';

-- ─── Update unique constraint ─────────────────────────────────────────────────
-- Old: (user_id, subject, topic)
-- New: (user_id, subject, chapter, topic)
ALTER TABLE user_topic_progress
    DROP CONSTRAINT user_topic_progress_user_id_subject_topic_key;

ALTER TABLE user_topic_progress
    ADD CONSTRAINT user_topic_progress_user_id_subject_chapter_topic_key
    UNIQUE (user_id, subject, chapter, topic);

-- ─── Update indexes ───────────────────────────────────────────────────────────
-- Subject-level index now includes chapter for filtered queries
DROP INDEX IF EXISTS idx_topic_progress_subject;
CREATE INDEX idx_topic_progress_subject
    ON user_topic_progress (user_id, subject, chapter);

-- The recent-access index stays the same (user_id, last_accessed_at DESC)
-- since "Continue Learning" queries across all subjects/chapters
