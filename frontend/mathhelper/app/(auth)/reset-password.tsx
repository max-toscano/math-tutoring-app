/**
 * Reset Password Screen
 * ═══════════════════════════════════════════════════════════════════════════
 *
 * This screen is where the user types their NEW password after clicking
 * the reset link in their email.
 *
 * HOW THE USER GETS HERE:
 *   1. They requested a password reset (forgot-password screen)
 *   2. Supabase sent them an email with a magic link
 *   3. They clicked the link → it opened this app via deep linking
 *   4. _layout.tsx caught the deep link, extracted the auth tokens,
 *      called supabase.auth.setSession() → user is now "logged in"
 *      with a special recovery session
 *   5. _layout.tsx navigated to this screen: /(auth)/reset-password
 *
 * WHAT THIS SCREEN DOES:
 *   • Shows two password fields (new password + confirm)
 *   • Validates they match and are long enough (6+ characters)
 *   • Calls updatePassword() which tells Supabase to change the password
 *   • Clears the recovery mode flag so the auth gate works normally again
 *   • Shows success message, then lets user continue to the app
 *
 * WHY THE USER HAS A SESSION:
 *   When they clicked the email link, Supabase exchanged the recovery
 *   token for a real access_token + refresh_token. The deep link handler
 *   in _layout.tsx called setSession() with those tokens. So right now,
 *   the user is authenticated — which is required for updateUser() to work.
 *
 *   However, isRecoveringPassword is true in AppContext, so the AuthGate
 *   lets them stay on this (auth) screen instead of redirecting to tabs.
 *
 * FILE LOCATION:
 *   app/(auth)/reset-password.tsx
 *   Route: /(auth)/reset-password
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
import { updatePassword } from '../../services/auth';
import { useAppContext } from '../../context/AppContext';

export default function ResetPasswordScreen() {
  const router = useRouter();

  // Pull clearPasswordRecovery from context.
  // We call this after the password is successfully changed to tell
  // the AuthGate: "recovery is done, resume normal redirect behavior."
  const { clearPasswordRecovery } = useAppContext();

  // ── State ──────────────────────────────────────────────────────────────
  //
  // password:        the new password the user is typing
  // confirmPassword: they type it again to make sure they didn't mistype
  // showPassword:    toggles visibility of the password text (eye icon)
  // loading:         true while waiting for Supabase to process the change
  // success:         true after password was changed — we show a success screen
  // error:           any validation or server error message
  //
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');

  // ── Handler ────────────────────────────────────────────────────────────
  //
  // Called when the user taps "Set New Password".
  //
  async function handleUpdatePassword() {
    // ── Client-side validation ──
    //
    // We validate BEFORE making the API call. This gives instant feedback
    // and avoids unnecessary network requests.

    // Check: did they type anything?
    if (!password || !confirmPassword) {
      setError('Please fill in both fields.');
      return;
    }

    // Check: minimum length.
    // Supabase enforces 6 characters server-side too, but checking here
    // gives a better error message than the generic Supabase error.
    if (password.length < 6) {
      setError('Password must be at least 6 characters.');
      return;
    }

    // Check: do the two fields match?
    // This is a classic UX pattern. Since the password is hidden (dots),
    // it's easy to mistype. Making them type it twice catches typos.
    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    setError('');
    setLoading(true);

    try {
      // ── This is the actual Supabase call ──
      //
      // updatePassword() lives in services/auth.ts.
      // It calls supabase.auth.updateUser({ password: newPassword }).
      //
      // Under the hood, Supabase:
      //   1. Verifies the current session is valid (from the recovery tokens)
      //   2. Hashes the new password with bcrypt
      //   3. Updates the auth.users row in PostgreSQL
      //   4. Returns success
      //
      // After this, the old password no longer works. The user must use
      // the new password for future logins.
      //
      await updatePassword(password);

      // ── Clear the recovery flag ──
      //
      // This tells AppContext: "password recovery is done."
      // The AuthGate will now resume its normal behavior:
      //   user + inAuthGroup → redirect to (tabs)
      //
      // We don't redirect immediately though — we show a success screen
      // first so the user knows it worked. They tap "Continue" to proceed.
      //
      clearPasswordRecovery();

      // Show success state
      setSuccess(true);

    } catch (e: any) {
      // Common errors:
      //   "New password should be different from the old password"
      //     → Supabase rejects reusing the same password
      //   "Auth session missing"
      //     → The recovery session expired (tokens are short-lived)
      //     → User needs to request a new reset email
      const msg = e?.message ?? 'Failed to update password. Try again.';
      setError(msg);
      if (Platform.OS !== 'web') {
        Alert.alert('Error', msg);
      }
    } finally {
      setLoading(false);
    }
  }

  // ── Success State ──────────────────────────────────────────────────────
  //
  // Password was changed successfully. Show a confirmation and a button
  // to continue to the app. Since clearPasswordRecovery() was already
  // called, tapping "Continue" will trigger the AuthGate to redirect
  // to (tabs) because the user is authenticated + not in recovery mode.
  //
  if (success) {
    return (
      <View style={styles.container}>
        <View style={styles.inner}>
          <View style={styles.header}>
            <View style={[styles.logoCircle, { backgroundColor: '#10B981' }]}>
              <Ionicons name="checkmark-circle-outline" size={40} color={Colors.white} />
            </View>
            <Text style={styles.title}>Password Updated</Text>
            <Text style={styles.subtitle}>
              Your password has been changed successfully.
              {'\n'}You're all set!
            </Text>
          </View>

          <TouchableOpacity
            style={styles.button}
            onPress={() => router.replace('/(tabs)')}
            // router.replace (not push) so they can't go "back" to this
            // screen — the reset flow is done, going back makes no sense.
          >
            <Text style={styles.buttonText}>Continue to App</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  }

  // ── Form State ─────────────────────────────────────────────────────────
  //
  // Two password fields + a submit button.
  //
  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <View style={styles.inner}>
        {/* ── Header ── */}
        <View style={styles.header}>
          <View style={styles.logoCircle}>
            <Ionicons name="lock-open-outline" size={40} color={Colors.white} />
          </View>
          <Text style={styles.title}>New Password</Text>
          <Text style={styles.subtitle}>
            Choose a new password for your account.
            {'\n'}Must be at least 6 characters.
          </Text>
        </View>

        {/* ── Form ── */}
        <View style={styles.form}>
          {/* Error display */}
          {error ? (
            <View style={styles.errorBox}>
              <Ionicons name="alert-circle" size={16} color={Colors.secondary} />
              <Text style={styles.errorText}>{error}</Text>
            </View>
          ) : null}

          {/* New password input */}
          <View style={styles.inputGroup}>
            <Text style={styles.label}>New Password</Text>
            <View style={styles.inputRow}>
              <Ionicons
                name="lock-closed-outline"
                size={20}
                color={Colors.textMuted}
                style={styles.inputIcon}
              />
              <TextInput
                style={[styles.input, { flex: 1 }]}
                placeholder="At least 6 characters"
                placeholderTextColor={Colors.textMuted}
                value={password}
                onChangeText={setPassword}
                secureTextEntry={!showPassword}
                // secureTextEntry: when true, shows dots instead of text.
                // We toggle this with the eye icon button.
                autoComplete="new-password"
                // "new-password" tells the OS password manager this is a
                // NEW password (not logging in), so it offers to save it.
                editable={!loading}
              />
              {/* Eye toggle — tap to show/hide the password text */}
              <TouchableOpacity
                onPress={() => setShowPassword(!showPassword)}
                style={styles.eyeBtn}
              >
                <Ionicons
                  name={showPassword ? 'eye-off-outline' : 'eye-outline'}
                  size={20}
                  color={Colors.textMuted}
                />
              </TouchableOpacity>
            </View>
          </View>

          {/* Confirm password input */}
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Confirm Password</Text>
            <View style={styles.inputRow}>
              <Ionicons
                name="lock-closed-outline"
                size={20}
                color={Colors.textMuted}
                style={styles.inputIcon}
              />
              <TextInput
                style={styles.input}
                placeholder="Type it again"
                placeholderTextColor={Colors.textMuted}
                value={confirmPassword}
                onChangeText={setConfirmPassword}
                secureTextEntry={!showPassword}
                // Shares the same showPassword toggle as the first field.
                // This way tapping the eye icon reveals both fields at once,
                // making it easier to verify they match.
                autoComplete="new-password"
                editable={!loading}
              />
            </View>
          </View>

          {/* Submit button */}
          <TouchableOpacity
            style={[styles.button, loading && styles.buttonDisabled]}
            onPress={handleUpdatePassword}
            disabled={loading}
            activeOpacity={0.8}
          >
            {loading ? (
              <ActivityIndicator color={Colors.white} />
            ) : (
              <Text style={styles.buttonText}>Set New Password</Text>
            )}
          </TouchableOpacity>
        </View>
      </View>
    </KeyboardAvoidingView>
  );
}

// ── Styles ────────────────────────────────────────────────────────────────
//
// Same visual language as login, signup, and forgot-password screens.
//
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  inner: {
    flex: 1,
    justifyContent: 'center',
    paddingHorizontal: 28,
  },
  header: {
    alignItems: 'center',
    marginBottom: 36,
  },
  logoCircle: {
    width: 80,
    height: 80,
    borderRadius: 40,
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
    lineHeight: 22,
    paddingHorizontal: 10,
  },
  form: {
    gap: 18,
  },
  errorBox: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: '#FEE2E2',
    padding: 12,
    borderRadius: 10,
  },
  errorText: {
    color: Colors.secondary,
    fontSize: 13,
    flex: 1,
  },
  inputGroup: {
    gap: 6,
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
    flex: 1,
    fontSize: 15,
    color: Colors.text,
    height: '100%',
  },
  eyeBtn: {
    padding: 4,
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
    opacity: 0.7,
  },
  buttonText: {
    color: Colors.white,
    fontSize: 16,
    fontWeight: '600',
  },
});
