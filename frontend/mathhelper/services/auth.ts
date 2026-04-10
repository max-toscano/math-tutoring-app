/**
 * services/auth.ts
 * Auth service — wraps AWS Cognito (via aws-amplify v6) for sign-up,
 * sign-in, sign-out, email confirmation, and password reset.
 *
 * ── Why this file exists ─────────────────────────────────────────────────────
 *
 * Rather than importing aws-amplify directly in every screen, all auth
 * logic lives here. Screens call these functions and never touch Cognito
 * directly. If we ever swap auth providers again, only this file changes.
 *
 * ── How Cognito works under the hood ────────────────────────────────────────
 *
 * 1. A user signs up with email + password.
 * 2. Cognito sends a 6-digit verification code to their email.
 * 3. The user must enter that code (confirmSignUp) before they can sign in.
 * 4. On sign-in, Cognito issues three tokens:
 *      • idToken   — proves who the user is (contains sub, email, etc.)
 *                    → we send this to our backend API as the Bearer token
 *      • accessToken — used to call Cognito's own APIs (e.g. change password)
 *      • refreshToken — used to get new id/access tokens when they expire (~1hr)
 *    Amplify stores these in AsyncStorage and auto-refreshes them silently.
 * 5. Password reset is code-based: Cognito emails a 6-digit code, the user
 *    types it in the app along with their new password. No magic links.
 *    No deep link handling needed.
 *
 * ── Key differences from Supabase auth ──────────────────────────────────────
 *
 * Supabase                       → Cognito equivalent
 * ─────────────────────────────────────────────────────
 * signUp()                       → signUp() here (same name)
 * signIn()                       → signIn() here (same name)
 * signOut()                      → signOut() here (same name)
 * getSession() → { user, token } → getSession() here returns { user }
 * updatePassword(newPw)          → REMOVED. Use confirmPasswordReset() instead.
 *                                   (Cognito password-change-within-session uses
 *                                    updatePassword from aws-amplify/auth directly
 *                                    — not needed for our reset flow)
 * requestPasswordReset(email)    → same name, but sends a CODE not a magic link
 * onAuthStateChange(cb)          → same name, but uses Hub internally
 * PASSWORD_RECOVERY event        → GONE. No deep links = no recovery event.
 *
 * ── The User type ────────────────────────────────────────────────────────────
 *
 * We define our own User interface (below) instead of exposing Cognito's
 * AuthUser directly. This keeps the rest of the app insulated from Cognito
 * internals. Cognito's AuthUser has:
 *   • userId   — the "sub" UUID (unique ID, used as our database FK)
 *   • username — the email address (used as the login credential)
 *
 * We map these to:
 *   • id    — maps from userId (so AppContext's user.id keeps working)
 *   • email — maps from username
 */

import {
  signIn as amplifySignIn,
  signOut as amplifySignOut,
  signUp as amplifySignUp,
  confirmSignUp as amplifyConfirmSignUp,
  resetPassword,
  confirmResetPassword,
  getCurrentUser,
  fetchAuthSession,
  type AuthUser,
} from 'aws-amplify/auth';
import 'react-native-get-random-values';
import { v4 as uuidv4 } from 'uuid';
import { Hub } from 'aws-amplify/utils';

// ── Public types ──────────────────────────────────────────────────────────────

/**
 * Our app's user type. Hides Cognito's AuthUser so screens never
 * import from aws-amplify directly.
 *
 *   user.id    → Cognito sub (UUID) — used as the FK in our database
 *   user.email → the email address they signed up with
 */
export interface User {
  id: string;
  email: string;
}

/**
 * Cognito has no "session" object like Supabase does. We define a minimal
 * Session so AppContext doesn't need to change its types yet.
 * It just wraps the User.
 */
export interface Session {
  user: User;
}

// ── Internal helper ───────────────────────────────────────────────────────────

/**
 * Converts Cognito's AuthUser to our app's User type.
 * Cognito's username field is the email (that's how we configured the User Pool).
 */
function toUser(cognitoUser: AuthUser): User {
  return {
    id: cognitoUser.userId,       // Cognito "sub" — stable UUID for this user
    email: cognitoUser.username,  // email (the sign-up credential)
  };
}

// ── Sign Up ───────────────────────────────────────────────────────────────────
//
// Step 1 of 2 for new users. After this succeeds, Cognito sends a 6-digit
// code to the user's email. They CANNOT sign in until they confirm.
// → Navigate to the confirm-signup screen after calling this.
//
// displayName is stored as the standard Cognito "name" attribute.
// Make sure "name" is an allowed attribute in your Cognito User Pool settings.
//
export async function signUp(
  email: string,
  password: string,
  displayName?: string,
): Promise<{ username: string }> {
  const username = uuidv4();
  await amplifySignUp({
    username,
    password,
    options: {
      userAttributes: {
        email,
        preferred_username: email,
        ...(displayName ? { name: displayName } : {}),
      },
    },
  });
  return { username };
} 
// ── Confirm Sign Up ───────────────────────────────────────────────────────────
//
// Step 2 of 2 for new users. The user enters the 6-digit code from their
// email. On success, the account is activated and they can sign in.
//
// "email" here is the username (same value passed to signUp).
//
export async function confirmSignUp(email: string, code: string) {
  return amplifyConfirmSignUp({
    username: email,
    confirmationCode: code,
  });
}

// ── Sign In ───────────────────────────────────────────────────────────────────
//
// Authenticates the user and stores tokens in AsyncStorage.
// Amplify auto-refreshes the idToken before it expires (~1 hour).
//
// On success, Hub fires a 'signedIn' event → our onAuthStateChange listener
// picks it up and updates AppContext.
//
export async function signIn(email: string, password: string) {
  return amplifySignIn({ username: email, password });
}

// ── Sign Out ──────────────────────────────────────────────────────────────────
//
// Clears all stored tokens from AsyncStorage. Hub fires 'signedOut'.
//
export async function signOut() {
  return amplifySignOut();
}

// ── Get User ──────────────────────────────────────────────────────────────────
//
// Returns the currently signed-in user, or null if nobody is signed in.
// This reads from Amplify's token cache — no network call needed.
//
export async function getUser(): Promise<User | null> {
  try {
    const cognitoUser = await getCurrentUser();
    return toUser(cognitoUser);
  } catch {
    return null; // Not signed in
  }
}

// ── Get Session ───────────────────────────────────────────────────────────────
//
// Returns a { user } session object (like Supabase did) so AppContext
// doesn't need to change. Internally just wraps getUser().
//
export async function getSession(): Promise<Session | null> {
  const user = await getUser();
  if (!user) return null;
  return { user };
}

// ── Get JWT Token ─────────────────────────────────────────────────────────────
//
// Returns the Cognito idToken as a string. This is the Bearer token we
// send to our Python backend. The backend validates it against Cognito's
// JWKS endpoint.
//
// Call this in services/api.ts instead of reading from Supabase session.
//
export async function getToken(): Promise<string | null> {
  try {
    const { tokens } = await fetchAuthSession();
    return tokens?.idToken?.toString() ?? null;
  } catch {
    return null;
  }
}

// ── Request Password Reset (Step 1) ──────────────────────────────────────────
//
// Tells Cognito to send a 6-digit reset code to the user's email.
//
// IMPORTANT: This is NOT a magic link (unlike Supabase).
// The user stays inside the app and types the code on the next screen.
// No deep links, no URL parsing, no token-in-fragment handling.
//
// SECURITY: Cognito returns success even if the email doesn't exist —
// prevents attackers from discovering which emails are registered.
//
export async function requestPasswordReset(email: string) {
  await resetPassword({ username: email });
}

// ── Confirm Password Reset (Step 2) ──────────────────────────────────────────
//
// The user provides: their email, the 6-digit code from the email, and
// their new password. No active session required — the code IS the proof
// of identity.
//
// After this succeeds, the user can sign in with their new password.
// → Navigate back to login after calling this.
//
export async function confirmPasswordReset(
  email: string,
  code: string,
  newPassword: string,
) {
  await confirmResetPassword({
    username: email,
    confirmationCode: code,
    newPassword,
  });
}

// ── Auth State Listener ───────────────────────────────────────────────────────
//
// Subscribes to Cognito auth events via Amplify's Hub (an internal event bus).
//
// Hub fires these events:
//   'signedIn'      → user successfully signed in (tokens stored)
//   'signedOut'     → user signed out, or session expired without refresh
//   'tokenRefresh'  → idToken was auto-refreshed (every ~1 hour silently)
//
// We wrap Hub so AppContext keeps the same shape it had with Supabase:
//   onAuthStateChange((event, session) => { ... })
//
// The callback receives:
//   event   → 'signedIn' | 'signedOut' | 'tokenRefresh'
//   session → { user } on sign-in/refresh, null on sign-out
//
// Returns { unsubscribe } — call it in the useEffect cleanup to stop listening.
//
// NOTE: 'PASSWORD_RECOVERY' is gone. Cognito's code-based reset flow doesn't
// need it — the user never leaves the app, so no deep link event fires.
//
export function onAuthStateChange(
  callback: (event: string, session: Session | null) => void,
) {
  const unlisten = Hub.listen('auth', async ({ payload }) => {
    const { event } = payload;

    if (event === 'signedIn' || event === 'tokenRefresh') {
      try {
        const cognitoUser = await getCurrentUser();
        callback(event, { user: toUser(cognitoUser) });
      } catch {
        callback(event, null);
      }
    } else if (event === 'signedOut') {
      callback('signedOut', null);
    }
    // Other events (e.g. 'signInWithRedirect', 'customOAuthState') are ignored
  });

  return { unsubscribe: unlisten };
}
