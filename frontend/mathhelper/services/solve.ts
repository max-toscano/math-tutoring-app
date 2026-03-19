/**
 * solve.ts — Calls the backend /solve endpoints to get structured math solutions.
 * Replaces the old direct-to-OpenAI flow with a single backend call.
 */

import { Platform } from 'react-native';
import { apiFetch } from './api';

// ─── Types ────────────────────────────────────────────────────────────────────

export interface SolveStep {
  step: number;
  title: string;
  math?: string;
  explanation: string;
  note?: string;
}

export interface SolveResponse {
  problem: string;
  topic: string;
  subject_area: string;
  difficulty: 'Easy' | 'Medium' | 'Hard';
  answer: string;
  method: string;
  steps: SolveStep[];
  verification?: string;
  concepts: string[];
  prerequisites: string[];
  common_mistakes: string[];
  tip?: string;
}

// ─── Image helpers ────────────────────────────────────────────────────────────

async function imageUriToBase64(
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

// ─── API calls ────────────────────────────────────────────────────────────────

/**
 * Solve a math problem from a photo/image URI.
 * Converts the image to base64 and sends it to the backend.
 */
export async function solveFromImage(
  imageUri: string,
  studentQuestion?: string,
): Promise<SolveResponse> {
  const { base64, mimeType } = await imageUriToBase64(imageUri);

  const body = {
    image_base64: base64,
    mime_type: mimeType,
    student_question: studentQuestion ?? null,
  };

  const response = await apiFetch('/solve/image', {
    method: 'POST',
    body: JSON.stringify(body),
  });

  return response.json();
}

/**
 * Solve a math problem from typed text.
 */
export async function solveFromText(
  problemText: string,
  studentQuestion?: string,
): Promise<SolveResponse> {
  const body = {
    problem_text: problemText,
    student_question: studentQuestion ?? null,
  };

  const response = await apiFetch('/solve/text', {
    method: 'POST',
    body: JSON.stringify(body),
  });

  return response.json();
}
