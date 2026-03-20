/**
 * learn.ts — API client for the Learn tab (structured lessons & progress).
 * Calls the /learn/* endpoints on the FastAPI backend.
 * Supports both flat subjects (no chapter) and chaptered subjects (chapter param).
 */

import { apiFetch } from './api';

// ─── Types ──────────────────────────────────────────────────────────────────

export interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export interface QuizResult {
  is_correct: boolean;
  explanation: string;
  running_score?: { correct: number; total: number };
  concept_tested?: string;
}

export interface QuizOutcome {
  score: number;
  passed: boolean;
  new_phase: string;
  new_status: string;
  missed_concepts: string[];
}

export interface LessonQuestion {
  type: 'multiple_choice' | 'free_response';
  text: string;
  options?: string[];
  correct_answer?: string;
  question_number?: number;
}

export interface GraphData {
  graph_type: string;
  data: Record<string, any>;
  image_base64?: string;
}

export interface LessonResponse {
  message: string;
  phase: string | null;
  images: string[];
  graphs: GraphData[];
  question: LessonQuestion | null;
  quiz_result: QuizResult | null;
  quiz_outcome: QuizOutcome | null;
  conversation_history: Message[];
  // Legacy compat
  response_text?: string;
  assessment?: any;
}

export type Phase = 'lesson' | 'practice' | 'quiz' | 'review' | 'done';

export interface TopicProgress {
  subject: string;
  chapter: string | null;
  topic: string;
  status: 'not_started' | 'in_progress' | 'completed' | 'failed_last_attempt';
  phase: Phase | null;
  messages_count: number;
  last_accessed_at: string | null;
}

// ─── Progress ───────────────────────────────────────────────────────────────

/** Get all topic progress for the current user (powers Continue Learning). */
export async function getAllProgress(): Promise<TopicProgress[]> {
  const res = await apiFetch('/learn/progress');
  return res.json();
}

/** Get topic progress within a specific subject. */
export async function getSubjectProgress(
  subject: string,
): Promise<TopicProgress[]> {
  const res = await apiFetch(`/learn/progress/${subject}`);
  return res.json();
}

// ─── Lessons ────────────────────────────────────────────────────────────────

/** Start a new lesson (no student input) or continue one. */
export async function sendLessonMessage(
  subject: string,
  topic: string,
  options?: {
    chapter?: string;
    studentInput?: string;
    conversationHistory?: Message[];
  },
): Promise<LessonResponse> {
  const body = {
    subject,
    chapter: options?.chapter ?? null,
    topic,
    student_input: options?.studentInput ?? null,
    conversation_history: options?.conversationHistory ?? null,
  };

  const res = await apiFetch('/learn/lesson', {
    method: 'POST',
    body: JSON.stringify(body),
  });

  return res.json();
}

/** Mark a topic as completed. */
export async function markTopicComplete(
  subject: string,
  topic: string,
  chapter?: string,
): Promise<{ status: string; subject: string; topic: string }> {
  const res = await apiFetch('/learn/complete', {
    method: 'POST',
    body: JSON.stringify({ subject, chapter: chapter ?? null, topic }),
  });

  return res.json();
}
