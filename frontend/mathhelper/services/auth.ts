/**
 * Auth service — wraps Supabase Auth for sign-up, sign-in, sign-out,
 * and password reset.
 *
 * Profile creation is handled here (not via database trigger).
 *
 * ── How Supabase Auth works under the hood ──────────────────────────────
 *
 * Supabase Auth is a layer on top of PostgreSQL's auth.users table.
 * When a user signs up, Supabase:
 *   1. Creates a row in auth.users with their email + hashed password
 *   2. Returns a JWT (JSON Web Token) — a signed string that proves
 *      "this person is user X"
 *   3. The JWT is stored on the device (AsyncStorage for React Native)
 *   4. Every API call includes this JWT in the Authorization header
 *   5. Your backend validates the JWT to know who's making the request
 *
 * JWTs expire (default: 1 hour). The Supabase client automatically
 * "refreshes" them using a refresh_token before they expire, so the
 * user stays logged in. This happens invisibly — you don't need to
 * code anything for it (autoRefreshToken: true in supabase.ts).
 */
import { supabase } from '../lib/supabase';
import type { AuthChangeEvent, Session, User } from '@supabase/supabase-js';
import * as Linking from 'expo-linking';

export type { Session, User };

export async function signUp(email: string, password: string, displayName?: string) {
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
    options: {
      data: { display_name: displayName },
    },
  });
  if (error) throw error;

  // Create profile row (trigger was unreliable, so we do it here)
  if (data.user) {
    const { error: profileError } = await supabase
      .from('profiles')
      .upsert({
        id: data.user.id,
        display_name: displayName ?? email,
      }, { onConflict: 'id' });

    if (profileError) {
      console.warn('Failed to create profile:', profileError.message);
    }
  }

  return data;
}

export async function signIn(email: string, password: string) {
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });
  if (error) throw error;

  // Ensure profile exists on login too (in case it was missed)
  if (data.user) {
    const { data: profile } = await supabase
      .from('profiles')
      .select('id')
      .eq('id', data.user.id)
      .single();

    if (!profile) {
      await supabase
        .from('profiles')
        .upsert({
          id: data.user.id,
          display_name: data.user.user_metadata?.display_name ?? data.user.email,
        }, { onConflict: 'id' });
    }
  }

  return data;
}

export async function signOut() {
  const { error } = await supabase.auth.signOut();
  if (error) throw error;
}

export async function getSession(): Promise<Session | null> {
  const { data: { session } } = await supabase.auth.getSession();
  return session;
}

export async function getUser(): Promise<User | null> {
  const { data: { user } } = await supabase.auth.getUser();
  return user;
}

// ── Password Reset ────────────────────────────────────────────────────────
//
// Password reset is a 2-step flow:
//
//   STEP 1 — requestPasswordReset(email)
//     • Your app calls this when the user taps "Forgot password?"
//     • Supabase sends an email with a magic link
//     • The link looks like:
//         https://yourproject.supabase.co/auth/v1/verify?type=recovery&token=abc
//     • When clicked, Supabase verifies the token, then REDIRECTS to
//       the redirectTo URL you provide, with access/refresh tokens in
//       the URL fragment (#access_token=xxx&refresh_token=yyy)
//     • Your app catches this redirect via deep linking (the "mathhelper://"
//       scheme in app.json), parses the tokens, and sets the session
//     • This triggers the PASSWORD_RECOVERY event in onAuthStateChange
//
//   STEP 2 — updatePassword(newPassword)
//     • Now the user has a valid session (from the recovery tokens)
//     • Your app shows a "new password" form
//     • When submitted, calls updatePassword() which tells Supabase
//       to change the password for the currently-authenticated user
//     • Done — user can now log in with their new password
//
// SECURITY NOTE: Supabase returns success even if the email doesn't exist.
// This is intentional — it prevents "email enumeration" attacks where an
// attacker submits random emails to discover which ones are registered.

/**
 * Sends a password-reset email to the given address.
 *
 * @param email - The email address the user signed up with.
 *
 * How the redirect works:
 *   Linking.createURL('reset-password') generates a URL that opens your app:
 *     • In production:  "mathhelper://reset-password"
 *       (uses the "scheme" field from app.json)
 *     • In Expo Go dev: "exp://192.168.1.27:8081/--/reset-password"
 *       (Expo Go intercepts this and routes it to your app)
 *
 *   Supabase appends auth tokens to this URL as a fragment (#...),
 *   so the full redirect looks like:
 *     mathhelper://reset-password#access_token=eyJ...&refresh_token=abc&type=recovery
 *
 *   Your app's deep link handler (_layout.tsx) catches this URL,
 *   extracts the tokens, and calls supabase.auth.setSession().
 *
 * IMPORTANT — Supabase Dashboard config required:
 *   Go to Supabase Dashboard → Authentication → URL Configuration
 *   → add your redirect URL to the "Redirect URLs" allowlist.
 *   Without this, Supabase will REJECT the redirect and the link won't work.
 *   Add both:
 *     mathhelper://reset-password           (for production builds)
 *     exp://192.168.1.27:8081/--/reset-password  (for Expo Go dev)
 */
export async function requestPasswordReset(email: string) {
  // Linking.createURL builds the right deep-link URL for the current
  // environment (Expo Go vs standalone build)
  const redirectUrl = Linking.createURL('reset-password');

  const { error } = await supabase.auth.resetPasswordForEmail(email, {
    redirectTo: redirectUrl,
  });
  if (error) throw error;
}

/**
 * Sets a new password for the currently signed-in user.
 *
 * This only works when there is an active session — which Supabase
 * automatically creates when the user clicks the password-reset email link
 * and your app calls setSession() with the recovery tokens.
 *
 * @param newPassword - Must be at least 6 characters (enforced by Supabase)
 */
export async function updatePassword(newPassword: string) {
  const { error } = await supabase.auth.updateUser({
    password: newPassword,
  });
  if (error) throw error;
}

// ── Auth State Listener ───────────────────────────────────────────────────
//
// onAuthStateChange subscribes to Supabase auth events. Supabase fires
// these events whenever the user's auth state changes:
//
//   'SIGNED_IN'          → user just logged in (email/password or OAuth)
//   'SIGNED_OUT'         → user logged out or session expired
//   'TOKEN_REFRESHED'    → JWT was auto-refreshed (happens every ~hour)
//   'USER_UPDATED'       → user's profile was changed (e.g. new password)
//   'PASSWORD_RECOVERY'  → user clicked a password-reset email link
//                          and the recovery session was established
//
// We pass BOTH the event name and the session to the callback so the app
// can react differently depending on WHY the auth state changed.
// For example, on PASSWORD_RECOVERY we navigate to the reset-password
// screen instead of the normal app tabs.
//
// The previous version discarded the event name:
//   (_event, session) => callback(session)
// Now we pass it through so the app can detect PASSWORD_RECOVERY.

export function onAuthStateChange(
  callback: (event: AuthChangeEvent, session: Session | null) => void,
) {
  const { data: { subscription } } = supabase.auth.onAuthStateChange(
    (event, session) => callback(event, session),
  );
  return subscription;
}
