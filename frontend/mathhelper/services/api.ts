/**
 * services/api.ts
 * ─────────────────────────────────────────────────────────────────────────────
 * Shared authenticated fetch helper used by every service that talks to the
 * Python backend. Nothing in this file is specific to any feature — it just
 * handles the two things every request needs:
 *   1. Attach the Cognito JWT as a Bearer token so the backend can identify
 *      who is making the request.
 *   2. Throw a readable error if the server returns a non-2xx response.
 *
 * CHANGED FROM SUPABASE VERSION:
 *   Before: getAccessToken() read the token from supabase.auth.getSession()
 *   Now:    getAccessToken() calls getToken() from services/auth.ts, which
 *           uses Amplify's fetchAuthSession() to get the Cognito idToken.
 *
 * Why the idToken and not the accessToken?
 *   Cognito issues both. The idToken contains the user's identity claims
 *   (sub, email, name). The accessToken is for calling Cognito's own APIs.
 *   Our Python backend needs to know WHO is making the request, so it wants
 *   the idToken. The backend decodes it to extract the `sub` (user UUID).
 */

import { getToken } from './auth';

// ── API base URL ──────────────────────────────────────────────────────────────
//
// Read from the EXPO_PUBLIC_TUTORING_API_URL environment variable.
// EXPO_PUBLIC_ prefix is required by Expo — any env var the frontend needs
// must have this prefix or Expo won't include it in the build.
//
// Falls back to localhost:8001 for local development.
// In production you'd set this to your deployed backend URL.
//
export const API_BASE_URL =
  process.env.EXPO_PUBLIC_TUTORING_API_URL ?? 'http://localhost:8001';

// ── getAccessToken ────────────────────────────────────────────────────────────
//
// Gets the Cognito idToken from Amplify's local token cache.
// Amplify stores tokens in AsyncStorage and auto-refreshes them before
// they expire (~1 hour), so this is nearly always instant — no network call.
//
// Throws if nobody is signed in, which will bubble up as an error in
// whatever screen triggered the API call.
//
export async function getAccessToken(): Promise<string> {
  const token = await getToken();

  if (!token) {
    // This should only happen if:
    //   a) The user is not signed in (shouldn't reach this if AuthGate works)
    //   b) The refresh token also expired (user was inactive for 30+ days)
    // In both cases the app should redirect to login.
    throw new Error('Not authenticated — please sign in');
  }

  return token;
}

// ── apiFetch ──────────────────────────────────────────────────────────────────
//
// Wrapper around the native fetch() that:
//   1. Gets the Cognito token and adds it to the Authorization header
//   2. Sets Content-Type to JSON (our backend always expects JSON)
//   3. Throws a descriptive error on non-2xx responses instead of
//      returning a response object that callers have to check manually
//
// Usage:
//   const response = await apiFetch('/chat/message', {
//     method: 'POST',
//     body: JSON.stringify({ message: 'help me' }),
//   });
//   const data = await response.json();
//
// The `path` should start with a slash, e.g. '/chat/start-session'.
// The `options` are the same as native fetch() options (method, body, etc.).
//
export async function apiFetch(
  path: string,
  options: RequestInit = {},
): Promise<Response> {
  const token = await getAccessToken();

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,   // spread caller's options first (method, body, etc.)
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,  // Cognito idToken — backend validates this
      ...options.headers,                 // caller can override headers if needed
    },
  });

  if (!response.ok) {
    // Try to parse the backend's error message.
    // FastAPI returns { "detail": "..." } on errors — we surface that.
    // If the response isn't JSON, fall back to a generic message.
    const err = await response.json().catch(() => ({}));
    throw new Error(
      (err as any)?.detail ?? `API request failed (${response.status})`,
    );
  }

  return response;
}
