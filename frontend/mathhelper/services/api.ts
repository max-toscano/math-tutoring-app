/**
 * api.ts — Shared authenticated fetch for all backend API calls.
 * Extracted so tutoring.ts and learn.ts don't duplicate auth/fetch logic.
 */

import { supabase } from '../lib/supabase';

export const API_BASE_URL =
  process.env.EXPO_PUBLIC_TUTORING_API_URL ?? 'http://localhost:8000';

/**
 * Get the current Supabase access token for backend API calls.
 */
export async function getAccessToken(): Promise<string> {
  const {
    data: { session },
  } = await supabase.auth.getSession();
  if (!session?.access_token) {
    throw new Error('Not authenticated — please sign in');
  }
  return session.access_token;
}

/**
 * Make an authenticated request to the backend API.
 * Throws with the server's `detail` message on non-2xx responses.
 */
export async function apiFetch(
  path: string,
  options: RequestInit = {},
): Promise<Response> {
  const token = await getAccessToken();
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
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
