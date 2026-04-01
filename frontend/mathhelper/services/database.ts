/**
 * Database service — Supabase CRUD operations for sessions and saved items.
 *
 * Mirrors the AppContext API surface so the context provider can delegate here.
 * All functions assume RLS is enforced (user_id filtering happens server-side).
 */
import { supabase } from '../lib/supabase';
import type { MathAnalysis } from './openai';
import type { Message } from './tutoring';

// ─── Types matching the existing app interfaces ─────────────────────────────

export interface SessionMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  imageUri?: string;
}

export interface TutoringSession {
  id: string;
  title: string;
  preview: string;
  messages: SessionMessage[];
  conversationHistory: Message[];
  analysis?: MathAnalysis;
  photoUri?: string;
  savedAt: string;
  updatedAt: string;
}

export interface SavedItem {
  id: string;
  imageUri: string;
  analysis: MathAnalysis;
  savedAt: string;
}

// ─── Profile ────────────────────────────────────────────────────────────────

export interface UserProfile {
  id: string;
  display_name: string | null;
  grade_level: string | null;
  avatar_url: string | null;
  bio: string | null;
}

export async function fetchProfile(userId: string): Promise<UserProfile | null> {
  const { data, error } = await supabase
    .from('profiles')
    .select('id, display_name, grade_level, avatar_url, bio')
    .eq('id', userId)
    .single();

  if (error) {
    if (error.code === 'PGRST116') return null;
    throw error;
  }
  return data as UserProfile;
}

export async function updateProfile(
  userId: string,
  updates: Partial<Pick<UserProfile, 'display_name' | 'grade_level' | 'avatar_url' | 'bio'>>,
): Promise<void> {
  const { error } = await supabase
    .from('profiles')
    .update(updates)
    .eq('id', userId);
  if (error) throw error;
}

// ─── Saved Items ────────────────────────────────────────────────────────────

export async function fetchSavedItems(): Promise<SavedItem[]> {
  const { data, error } = await supabase
    .from('saved_items')
    .select('*')
    .order('created_at', { ascending: false });

  if (error) throw error;

  return (data ?? []).map((row) => ({
    id: row.id,
    imageUri: row.image_url,
    analysis: row.analysis as MathAnalysis,
    savedAt: row.created_at,
  }));
}

export async function insertSavedItem(
  userId: string,
  imageUrl: string,
  analysis: MathAnalysis,
): Promise<SavedItem> {
  const { data, error } = await supabase
    .from('saved_items')
    .insert({ user_id: userId, image_url: imageUrl, analysis })
    .select()
    .single();

  if (error) throw error;

  return {
    id: data.id,
    imageUri: data.image_url,
    analysis: data.analysis as MathAnalysis,
    savedAt: data.created_at,
  };
}

export async function deleteSavedItem(id: string): Promise<void> {
  const { error } = await supabase.from('saved_items').delete().eq('id', id);
  if (error) throw error;
}

// ─── Tutoring Sessions ──────────────────────────────────────────────────────

export async function fetchSessions(): Promise<TutoringSession[]> {
  const { data: sessions, error } = await supabase
    .from('tutoring_sessions')
    .select('*')
    .order('updated_at', { ascending: false });

  if (error) throw error;
  if (!sessions?.length) return [];

  // Fetch all messages for these sessions in one query
  const sessionIds = sessions.map((s) => s.id);
  const { data: allMessages, error: msgError } = await supabase
    .from('session_messages')
    .select('*')
    .in('session_id', sessionIds)
    .order('sort_order', { ascending: true });

  if (msgError) throw msgError;

  // Group messages by session
  const messagesBySession = new Map<string, typeof allMessages>();
  for (const msg of allMessages ?? []) {
    const existing = messagesBySession.get(msg.session_id) ?? [];
    existing.push(msg);
    messagesBySession.set(msg.session_id, existing);
  }

  return sessions.map((session) => {
    const msgs = messagesBySession.get(session.id) ?? [];
    const sessionMessages: SessionMessage[] = msgs.map((m) => ({
      id: m.id,
      role: m.role as 'user' | 'assistant',
      content: m.content,
      imageUri: m.image_url ?? undefined,
    }));

    // Derive conversationHistory from messages (role + content only)
    const conversationHistory: Message[] = msgs.map((m) => ({
      role: m.role as 'user' | 'assistant',
      content: m.content,
    }));

    return {
      id: session.id,
      title: session.title,
      preview: session.preview ?? '',
      messages: sessionMessages,
      conversationHistory,
      analysis: (session.analysis as MathAnalysis) ?? undefined,
      photoUri: session.photo_url ?? undefined,
      savedAt: session.created_at,
      updatedAt: session.updated_at,
    };
  });
}

export async function insertSession(
  userId: string,
  session: {
    title: string;
    preview: string;
    messages: SessionMessage[];
    analysis?: MathAnalysis;
    photoUrl?: string;
  },
): Promise<string> {
  // Insert the session row
  const { data, error } = await supabase
    .from('tutoring_sessions')
    .insert({
      user_id: userId,
      title: session.title,
      preview: session.preview,
      photo_url: session.photoUrl ?? null,
      analysis: session.analysis ?? null,
    })
    .select('id')
    .single();

  if (error) throw error;
  const sessionId = data.id;

  // Insert messages in bulk
  if (session.messages.length > 0) {
    const messageRows = session.messages.map((msg, idx) => ({
      session_id: sessionId,
      role: msg.role,
      content: msg.content,
      image_url: msg.imageUri ?? null,
      sort_order: idx,
    }));

    const { error: msgError } = await supabase
      .from('session_messages')
      .insert(messageRows);

    if (msgError) throw msgError;
  }

  return sessionId;
}

export async function updateSession(
  sessionId: string,
  updates: {
    title?: string;
    messages?: SessionMessage[];
    analysis?: MathAnalysis;
    photoUrl?: string;
  },
): Promise<void> {
  // Update the session row
  const sessionUpdate: Record<string, unknown> = {};
  if (updates.title !== undefined) sessionUpdate.title = updates.title;
  if (updates.analysis !== undefined) sessionUpdate.analysis = updates.analysis;
  if (updates.photoUrl !== undefined) sessionUpdate.photo_url = updates.photoUrl;

  if (Object.keys(sessionUpdate).length > 0) {
    const { error } = await supabase
      .from('tutoring_sessions')
      .update(sessionUpdate)
      .eq('id', sessionId);
    if (error) throw error;
  }

  // Replace messages if provided (delete old, insert new)
  if (updates.messages) {
    const { error: delError } = await supabase
      .from('session_messages')
      .delete()
      .eq('session_id', sessionId);
    if (delError) throw delError;

    if (updates.messages.length > 0) {
      const messageRows = updates.messages.map((msg, idx) => ({
        session_id: sessionId,
        role: msg.role,
        content: msg.content,
        image_url: msg.imageUri ?? null,
        sort_order: idx,
      }));

      const { error: insError } = await supabase
        .from('session_messages')
        .insert(messageRows);
      if (insError) throw insError;
    }
  }
}

export async function deleteSession(sessionId: string): Promise<void> {
  // Messages are cascade-deleted by the FK constraint
  const { error } = await supabase
    .from('tutoring_sessions')
    .delete()
    .eq('id', sessionId);
  if (error) throw error;
}

export async function getSession(sessionId: string): Promise<TutoringSession | null> {
  const { data: session, error } = await supabase
    .from('tutoring_sessions')
    .select('*')
    .eq('id', sessionId)
    .single();

  if (error) {
    if (error.code === 'PGRST116') return null; // not found
    throw error;
  }

  const { data: msgs, error: msgError } = await supabase
    .from('session_messages')
    .select('*')
    .eq('session_id', sessionId)
    .order('sort_order', { ascending: true });

  if (msgError) throw msgError;

  const messages: SessionMessage[] = (msgs ?? []).map((m) => ({
    id: m.id,
    role: m.role as 'user' | 'assistant',
    content: m.content,
    imageUri: m.image_url ?? undefined,
  }));

  const conversationHistory: Message[] = (msgs ?? []).map((m) => ({
    role: m.role as 'user' | 'assistant',
    content: m.content,
  }));

  return {
    id: session.id,
    title: session.title,
    preview: session.preview ?? '',
    messages,
    conversationHistory,
    analysis: (session.analysis as MathAnalysis) ?? undefined,
    photoUri: session.photo_url ?? undefined,
    savedAt: session.created_at,
    updatedAt: session.updated_at,
  };
}
