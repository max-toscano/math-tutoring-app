/**
 * Tutoring API service — calls our FastAPI ai-workflow backend.
 */

const API_BASE_URL = process.env.EXPO_PUBLIC_TUTORING_API_URL ?? 'http://localhost:8000';

export interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export interface TutorResponse {
  subject: string;
  mode: string;
  response: string;
  conversation_history: Message[];
}

export async function sendTutoringMessage(
  studentInput: string,
  options?: {
    subject?: string;
    mode?: string;
    conversationHistory?: Message[];
  },
): Promise<TutorResponse> {
  const body = {
    student_input: studentInput,
    subject: options?.subject ?? 'math',
    mode: options?.mode ?? null,
    conversation_history: options?.conversationHistory ?? null,
  };

  const response = await fetch(`${API_BASE_URL}/tutor/respond`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(
      (err as any)?.detail ?? `Tutoring request failed (${response.status})`,
    );
  }

  return response.json();
}
