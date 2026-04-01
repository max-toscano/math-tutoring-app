-- ============================================================================
-- Migration 009: Add avatar_url and bio to profiles
-- Supports the Edit Profile screen.
-- ============================================================================

ALTER TABLE profiles ADD COLUMN IF NOT EXISTS avatar_url TEXT;
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS bio TEXT;
