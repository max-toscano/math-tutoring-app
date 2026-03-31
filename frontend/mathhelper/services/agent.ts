/**
 * agent.ts — Service for the new AI tutoring backend (app/).
 * Calls /chat/start-session, /chat/message, /chat/close-session.
 */

import { Platform } from 'react-native';
import { apiFetch, API_BASE_URL } from './api';

/**
 * Convert an image URI to base64 (works on web and native).
 */
export async function imageUriToBase64(
  uri: string,
): Promise<{ base64: string; mimeType: string }> {
  if (Platform.OS === 'web') {
    const res = await fetch(uri);
    const blob = await res.blob();
    const mimeType = blob.type || 'image/jpeg';
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const dataUrl = reader.result as string;
        resolve({ base64: dataUrl.split(',')[1], mimeType });
      };
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
  } else {
    const FileSystem = require('expo-file-system');
    const base64 = await FileSystem.readAsStringAsync(uri, {
      encoding: FileSystem.EncodingType.Base64,
    });
    const ext = uri.split('.').pop()?.toLowerCase() ?? 'jpg';
    return { base64, mimeType: ext === 'png' ? 'image/png' : 'image/jpeg' };
  }
}

export interface AgentMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface GraphOutput {
  graph_type?: string;
  image_base64?: string;
  desmos?: {
    expressions: {
      latex: string;
      color?: string;
      lineStyle?: string;
      label?: string;
      fillOpacity?: number;
      pointStyle?: string;
    }[];
    bounds?: {
      left: number;
      right: number;
      top: number;
      bottom: number;
    };
  };
}

export interface AgentResponse {
  response: string;
  subject?: string;
  topic?: string;
  mode?: string;
  mode_source?: string;
  tools_used: string[];
  graphs: GraphOutput[];
  validation_flags: string[];
  suggestions: string[];
}

export interface SessionResponse {
  session_id: string;
}

export interface CloseSessionResponse {
  session_summary?: string;
  total_problems: number;
  success_rate: number;
}

/**
 * Start a new tutoring session.
 * Call this when the user opens the Tutor tab or starts a new chat.
 */
export async function startAgentSession(): Promise<SessionResponse> {
  const response = await apiFetch('/chat/start-session', {
    method: 'POST',
  });
  return response.json();
}

/**
 * Send a message to the AI tutor.
 */
export async function sendAgentMessage(
  sessionId: string,
  message: string,
  options?: {
    selectedMode?: string;
    conversationHistory?: AgentMessage[];
    imageBase64?: string;
  },
): Promise<AgentResponse> {
  const body = {
    session_id: sessionId,
    message,
    selected_mode: options?.selectedMode ?? null,
    conversation_history: options?.conversationHistory ?? null,
    image_base64: options?.imageBase64 ?? null,
  };

  const response = await apiFetch('/chat/message', {
    method: 'POST',
    body: JSON.stringify(body),
  });

  return response.json();
}

/**
 * Close the current session. Generates a summary and updates mastery.
 * Call this when the user leaves the Tutor tab or closes the app.
 */
export async function closeAgentSession(
  sessionId: string,
): Promise<CloseSessionResponse> {
  const response = await apiFetch('/chat/close-session', {
    method: 'POST',
    body: JSON.stringify({ session_id: sessionId }),
  });
  return response.json();
}
