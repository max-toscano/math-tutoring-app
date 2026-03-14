-- ============================================================================
-- MathHelper Database Schema
-- Run this in the Supabase SQL Editor (supabase.com/dashboard → SQL Editor)
-- ============================================================================

-- ─── Profiles ───────────────────────────────────────────────────────────────
-- Extends Supabase Auth with app-specific user data.
-- Auto-created when a new user signs up via the trigger below.

CREATE TABLE profiles (
  id          UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  display_name TEXT,
  grade_level  TEXT,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ─── Tutoring Sessions ──────────────────────────────────────────────────────

CREATE TABLE tutoring_sessions (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id    UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  title      TEXT NOT NULL,
  preview    TEXT,
  subject    TEXT DEFAULT 'math',
  mode       TEXT,
  photo_url  TEXT,              -- Supabase Storage path
  analysis   JSONB,             -- MathAnalysis object
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ─── Session Messages ───────────────────────────────────────────────────────
-- Normalized from the SessionMessage[] array.
-- conversation_history for the AI is derived: SELECT role, content ORDER BY sort_order

CREATE TABLE session_messages (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID NOT NULL REFERENCES tutoring_sessions(id) ON DELETE CASCADE,
  role       TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
  content    TEXT NOT NULL,
  image_url  TEXT,              -- Supabase Storage path (if message has an image)
  sort_order INTEGER NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ─── Saved Items (photo analysis results) ───────────────────────────────────

CREATE TABLE saved_items (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id    UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  image_url  TEXT NOT NULL,     -- Supabase Storage path
  analysis   JSONB NOT NULL,   -- MathAnalysis object
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ─── Indexes ────────────────────────────────────────────────────────────────

CREATE INDEX idx_sessions_user      ON tutoring_sessions (user_id, updated_at DESC);
CREATE INDEX idx_messages_session    ON session_messages  (session_id, sort_order);
CREATE INDEX idx_saved_items_user    ON saved_items       (user_id, created_at DESC);

-- ─── Row-Level Security ─────────────────────────────────────────────────────
-- Every table is locked down: users can only touch their own rows.

ALTER TABLE profiles          ENABLE ROW LEVEL SECURITY;
ALTER TABLE tutoring_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE session_messages  ENABLE ROW LEVEL SECURITY;
ALTER TABLE saved_items       ENABLE ROW LEVEL SECURITY;

-- Profiles
CREATE POLICY "Users can view own profile"
  ON profiles FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE USING (auth.uid() = id);

-- Tutoring sessions (full CRUD)
CREATE POLICY "Users can select own sessions"
  ON tutoring_sessions FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own sessions"
  ON tutoring_sessions FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own sessions"
  ON tutoring_sessions FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own sessions"
  ON tutoring_sessions FOR DELETE USING (auth.uid() = user_id);

-- Session messages (access via session ownership)
CREATE POLICY "Users can select own session messages"
  ON session_messages FOR SELECT
  USING (session_id IN (SELECT id FROM tutoring_sessions WHERE user_id = auth.uid()));

CREATE POLICY "Users can insert own session messages"
  ON session_messages FOR INSERT
  WITH CHECK (session_id IN (SELECT id FROM tutoring_sessions WHERE user_id = auth.uid()));

CREATE POLICY "Users can update own session messages"
  ON session_messages FOR UPDATE
  USING (session_id IN (SELECT id FROM tutoring_sessions WHERE user_id = auth.uid()));

CREATE POLICY "Users can delete own session messages"
  ON session_messages FOR DELETE
  USING (session_id IN (SELECT id FROM tutoring_sessions WHERE user_id = auth.uid()));

-- Saved items (full CRUD)
CREATE POLICY "Users can select own saved items"
  ON saved_items FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own saved items"
  ON saved_items FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own saved items"
  ON saved_items FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own saved items"
  ON saved_items FOR DELETE USING (auth.uid() = user_id);

-- ─── Auto-create profile on signup ─────────────────────────────────────────

CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO profiles (id, display_name)
  VALUES (
    NEW.id,
    COALESCE(NEW.raw_user_meta_data ->> 'display_name', NEW.email)
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION handle_new_user();

-- ─── Updated_at trigger ─────────────────────────────────────────────────────

CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at
  BEFORE UPDATE ON profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER set_updated_at
  BEFORE UPDATE ON tutoring_sessions
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ─── Storage bucket for math problem images ─────────────────────────────────
-- Run this separately in the SQL Editor if the INSERT doesn't work via migration:

INSERT INTO storage.buckets (id, name, public)
VALUES ('math-images', 'math-images', false)
ON CONFLICT (id) DO NOTHING;

-- Storage policies: users can upload/read/delete their own images
-- Files are stored under: math-images/{user_id}/...

CREATE POLICY "Users can upload own images"
  ON storage.objects FOR INSERT
  WITH CHECK (
    bucket_id = 'math-images'
    AND (storage.foldername(name))[1] = auth.uid()::text
  );

CREATE POLICY "Users can view own images"
  ON storage.objects FOR SELECT
  USING (
    bucket_id = 'math-images'
    AND (storage.foldername(name))[1] = auth.uid()::text
  );

CREATE POLICY "Users can delete own images"
  ON storage.objects FOR DELETE
  USING (
    bucket_id = 'math-images'
    AND (storage.foldername(name))[1] = auth.uid()::text
  );
