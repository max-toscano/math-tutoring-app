/**
 * Tutoring API service — calls our FastAPI ai-workflow backend.
 * Uses the shared apiFetch from api.ts for authenticated requests.
 */

import { apiFetch } from './api';

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
