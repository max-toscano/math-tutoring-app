/**
 * Forgot Password Screen
 * ═══════════════════════════════════════════════════════════════════════════
 *
 * This is the screen the user sees when they tap "Forgot password?" on the
 * login page. Its job is simple: collect the user's email address and tell
 * Supabase to send them a password-reset link.
 *
 * THE FLOW:
 *   1. User taps "Forgot password?" on the login screen
 *      → router.push('/(auth)/forgot-password') brings them here
 *
 *   2. They type their email and tap "Send Reset Link"
 *      → we call requestPasswordReset(email) from auth.ts
 *      → Supabase sends an email with a magic link
 *
 *   3. We show a success screen ("Check your email")
 *      → User opens their email app, clicks the link
 *      → That link opens this app via deep linking (handled in _layout.tsx)
 *      → They land on the reset-password screen to set a new password
 *
 * WHAT HAPPENS IF THE EMAIL DOESN'T EXIST?
 *   Supabase still returns success (no error). This is a deliberate
 *   security measure called "preventing email enumeration." If Supabase
 *   returned "email not found", an attacker could submit random emails
 *   to discover which ones are registered in your app.
 *
 *   So from the user's perspective, they always see "Check your email" —
 *   if the email exists, they get the link. If not, nothing arrives.
 *
 * FILE LOCATION:
 *   app/(auth)/forgot-password.tsx
 *
 *   It's inside the (auth) folder, which means:
 *     • It shares the auth layout (no header, just a plain screen)
 *     • The AuthGate in _layout.tsx won't redirect unauthenticated users
 *       away from it (auth screens are accessible without login)
 *     • The route path becomes: /(auth)/forgot-password
 */

import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '../../constants/Colors';
import { requestPasswordReset } from '../../services/auth';

export default function ForgotPasswordScreen() {
  const router = useRouter();

  // ── State ──────────────────────────────────────────────────────────────
  //
  // email:   what the user types in the input field
  // loading: true while we're waiting for Supabase to respond
  //          (disables the button and shows a spinner to prevent double-taps)
  // sent:    flips to true after the email is sent successfully
  //          (we swap the entire screen to a "check your email" message)
  // error:   holds any error message to display (empty string = no error)
  //
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);
  const [error, setError] = useState('');

  // ── Handler ────────────────────────────────────────────────────────────
  //
  // Called when the user taps "Send Reset Link".
  //
  async function handleReset() {
    // Basic validation — check they actually typed something.
    // We use .trim() to ignore whitespace-only input like "   ".
    if (!email.trim()) {
      setError('Please enter your email address.');
      return;
    }

    setError('');     // Clear any previous error
    setLoading(true); // Show spinner, disable button

    try {
      // ── This is the actual Supabase call ──
      // requestPasswordReset() lives in services/auth.ts.
      // It calls supabase.auth.resetPasswordForEmail() with a redirect URL.
      // If successful, Supabase queues an email to this address.
      // If the email doesn't exist, it still returns success (no error).
      await requestPasswordReset(email.trim());

      // Flip to the success screen
      setSent(true);

    } catch (e: any) {
      // This catch runs if something actually went wrong — like a network
      // error, or Supabase being down. NOT for "email not found" (that's
      // treated as success by Supabase, remember).
      const msg = e?.message ?? 'Something went wrong. Try again.';
      setError(msg);

      // On mobile (iOS/Android), also show a native alert popup.
      // On web, the inline error message is enough.
      if (Platform.OS !== 'web') {
        Alert.alert('Error', msg);
      }
    } finally {
      // Always stop the spinner, whether we succeeded or failed.
      // "finally" runs after try OR catch, guaranteed.
      setLoading(false);
    }
  }

  // ── Success State ──────────────────────────────────────────────────────
  //
  // After the email is sent, we replace the form with a confirmation
  // message. This is a common UX pattern — it prevents the user from
  // accidentally sending multiple reset emails by tapping the button again.
  //
  if (sent) {
    return (
      <View style={styles.container}>
        <View style={styles.inner}>
          <View style={styles.header}>
            {/* Green circle with a mail icon to signal success */}
            <View style={[styles.logoCircle, { backgroundColor: '#10B981' }]}>
              <Ionicons name="mail-open-outline" size={40} color={Colors.white} />
            </View>
            <Text style={styles.title}>Check Your Email</Text>
            <Text style={styles.subtitle}>
              We sent a password reset link to{' '}
              <Text style={{ fontWeight: '600' }}>{email}</Text>.
              {'\n\n'}
              Click the link in the email to set a new password.
              It may take a minute to arrive — check your spam folder too.
            </Text>
          </View>

          {/* Button to go back to login */}
          <TouchableOpacity
            style={styles.button}
            onPress={() => router.replace('/(auth)/login')}
          >
            <Text style={styles.buttonText}>Back to Login</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  }

  // ── Form State ─────────────────────────────────────────────────────────
  //
  // The main screen: email input + send button + back link.
  // The layout and styles match the login screen for visual consistency.
  //
  return (
    <KeyboardAvoidingView
      style={styles.container}
      // On iOS, "padding" pushes the content up when the keyboard opens
      // so the input field stays visible. Android handles this automatically.
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <View style={styles.inner}>
        {/* ── Header ── */}
        <View style={styles.header}>
          <View style={styles.logoCircle}>
            <Ionicons name="key-outline" size={40} color={Colors.white} />
          </View>
          <Text style={styles.title}>Reset Password</Text>
          <Text style={styles.subtitle}>
            Enter the email address you signed up with.{'\n'}
            We'll send you a link to reset your password.
          </Text>
        </View>

        {/* ── Form ── */}
        <View style={styles.form}>
          {/* Error message (only visible when error state is non-empty) */}
          {error ? (
            <View style={styles.errorBox}>
              <Ionicons name="alert-circle" size={16} color={Colors.secondary} />
              <Text style={styles.errorText}>{error}</Text>
            </View>
          ) : null}

          {/* Email input */}
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Email</Text>
            <View style={styles.inputRow}>
              <Ionicons
                name="mail-outline"
                size={20}
                color={Colors.textMuted}
                style={styles.inputIcon}
              />
              <TextInput
                style={styles.input}
                placeholder="you@example.com"
                placeholderTextColor={Colors.textMuted}
                value={email}
                onChangeText={setEmail}
                autoCapitalize="none"       // don't capitalize the first letter
                keyboardType="email-address" // show @ and .com on the keyboard
                autoComplete="email"         // let the OS autofill saved emails
                editable={!loading}          // disable while sending
              />
            </View>
          </View>

          {/* Submit button */}
          <TouchableOpacity
            style={[styles.button, loading && styles.buttonDisabled]}
            onPress={handleReset}
            disabled={loading}
            activeOpacity={0.8} // slight dim on press for feedback
          >
            {loading ? (
              // Show a spinner while waiting for Supabase
              <ActivityIndicator color={Colors.white} />
            ) : (
              <Text style={styles.buttonText}>Send Reset Link</Text>
            )}
          </TouchableOpacity>

          {/* Back to login link */}
          <TouchableOpacity
            style={styles.backLink}
            onPress={() => router.back()}
            // router.back() goes to the previous screen (login).
            // Unlike router.replace(), back() preserves the navigation
            // stack so the user can use the system back gesture too.
          >
            <Ionicons name="arrow-back" size={16} color={Colors.primary} />
            <Text style={styles.backLinkText}> Back to Login</Text>
          </TouchableOpacity>
        </View>
      </View>
    </KeyboardAvoidingView>
  );
}

// ── Styles ────────────────────────────────────────────────────────────────
//
// These are intentionally identical to the login screen styles.
// Keeping auth screens visually consistent makes the app feel polished.
// If you change the login screen design, update these to match.
//
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  inner: {
    flex: 1,
    justifyContent: 'center',   // vertically center the content
    paddingHorizontal: 28,       // breathing room on the sides
  },
  header: {
    alignItems: 'center',
    marginBottom: 36,
  },
  logoCircle: {
    width: 80,
    height: 80,
    borderRadius: 40,            // half of width = perfect circle
    backgroundColor: Colors.primary,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 16,
  },
  title: {
    fontSize: 28,
    fontWeight: '700',
    color: Colors.text,
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 15,
    color: Colors.textLight,
    textAlign: 'center',
    lineHeight: 22,              // more space between lines for readability
    paddingHorizontal: 10,
  },
  form: {
    gap: 18,                     // space between each form element
  },
  errorBox: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: '#FEE2E2', // light red background
    padding: 12,
    borderRadius: 10,
  },
  errorText: {
    color: Colors.secondary,     // red text
    fontSize: 13,
    flex: 1,
  },
  inputGroup: {
    gap: 6,                      // space between label and input
  },
  label: {
    fontSize: 13,
    fontWeight: '600',
    color: Colors.text,
    marginLeft: 2,
  },
  inputRow: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Colors.card,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: Colors.border,
    paddingHorizontal: 14,
    height: 50,
  },
  inputIcon: {
    marginRight: 10,
  },
  input: {
    flex: 1,                     // fill remaining space in the row
    fontSize: 15,
    color: Colors.text,
    height: '100%',
  },
  button: {
    backgroundColor: Colors.primary,
    height: 52,
    borderRadius: 14,
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 4,
  },
  buttonDisabled: {
    opacity: 0.7,                // dim the button when loading
  },
  buttonText: {
    color: Colors.white,
    fontSize: 16,
    fontWeight: '600',
  },
  backLink: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 8,
  },
  backLinkText: {
    color: Colors.primary,
    fontSize: 14,
    fontWeight: '600',
  },
});
