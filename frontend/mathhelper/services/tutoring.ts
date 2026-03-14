/**
 * Tutoring API service — calls our FastAPI ai-workflow backend.
 * Passes the Supabase JWT token for authentication.
 */

import { supabase } from '../lib/supabase';

const API_BASE_URL = process.env.EXPO_PUBLIC_TUTORING_API_URL ?? 'http://localhost:8000';

export interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export interface Assessment {
  is_correct?: boolean;
  mistake_type?: string;
  topic?: string;
  difficulty?: string;
  concepts: string[];
}

export interface TutorResponse {
  subject: string;
  mode: string;
  response?: string;
  response_text?: string;
  assessment?: Assessment;
  conversation_history: Message[];
}

/**
 * Get the current Supabase access token for backend API calls.
 */
async function getAccessToken(): Promise<string> {
  const { data: { session } } = await supabase.auth.getSession();
  if (!session?.access_token) {
    throw new Error('Not authenticated — please sign in');
  }
  return session.access_token;
}

/**
 * Make an authenticated request to the backend API.
 */
async function apiFetch(path: string, options: RequestInit = {}): Promise<Response> {
  const token = await getAccessToken();
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...options.headers,
    },
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(
      (err as any)?.detail ?? `API request failed (${response.status})`,
    );
  }

  return response;
}

export async function sendTutoringMessage(
  studentInput: string,
  options?: {
    subject?: string;
    mode?: string;
    conversationHistory?: Message[];
    imageBase64?: string;
  },
): Promise<TutorResponse> {
  const body = {
    student_input: studentInput,
    subject: options?.subject ?? 'math',
    mode: options?.mode ?? 'direct',
    conversation_history: options?.conversationHistory ?? null,
    image_base64: options?.imageBase64 ?? null,
  };

  const response = await apiFetch('/tutor/respond', {
    method: 'POST',
    body: JSON.stringify(body),
  });

  return response.json();
}

export async function getProgressSummary() {
  const response = await apiFetch('/progress/summary');
  return response.json();
}

export async function getSubjectDetail(subject: string) {
  const response = await apiFetch(`/progress/subject/${subject}`);
  return response.json();
}

export async function getWeakAreas() {
  const response = await apiFetch('/progress/weak-areas');
  return response.json();
}

export async function getProfile() {
  const response = await apiFetch('/auth/me');
  return response.json();
}
