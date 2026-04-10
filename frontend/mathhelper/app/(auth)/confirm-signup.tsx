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
import { useRouter, useLocalSearchParams } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '../../constants/Colors';
import { confirmSignUp, signUp } from '../../services/auth';

export default function ConfirmSignUpScreen() {
  const router = useRouter();

  // email is passed from signup.tsx via router.push params
  const { email, username } = useLocalSearchParams<{ email: string; username: string }>();

  const [code, setCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [resending, setResending] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  async function handleConfirm() {
    if (!code.trim()) {
      setError('Please enter the confirmation code.');
      return;
    }
    setError('');
    setLoading(true);
    try {
      await confirmSignUp(username, code.trim());
      setSuccess(true);
    } catch (e: any) {
      const msg = e?.message ?? 'Invalid code. Please try again.';
      setError(msg);
      if (Platform.OS !== 'web') {
        Alert.alert('Confirmation Failed', msg);
      }
    } finally {
      setLoading(false);
    }
  }

  async function handleResend() {
    setResending(true);
    setError('');
    try {
      // Cognito resends the code when you call resendSignUpCode.
      // We import it from services/auth — if it's not there yet we'll add it.
      const { resendSignUpCode } = await import('aws-amplify/auth');
      await resendSignUpCode({ username });
      if (Platform.OS === 'web') {
        setError(''); // clear any previous error
        // Show a non-error success hint by briefly setting a success message
      } else {
        Alert.alert('Code Sent', 'A new confirmation code has been sent to your email.');
      }
    } catch (e: any) {
      setError(e?.message ?? 'Failed to resend code.');
    } finally {
      setResending(false);
    }
  }

  if (success) {
    return (
      <View style={[styles.container, styles.center]}>
        <View style={[styles.iconCircle, { backgroundColor: '#10B981' }]}>
          <Ionicons name="checkmark-circle-outline" size={40} color={Colors.white} />
        </View>
        <Text style={styles.title}>Account Confirmed</Text>
        <Text style={styles.subtitle}>
          Your account is active.{'\n'}Sign in to get started.
        </Text>
        <TouchableOpacity
          style={styles.button}
          onPress={() => router.replace('/(auth)/login')}
          activeOpacity={0.8}
        >
          <Text style={styles.buttonText}>Go to Sign In</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <View style={styles.inner}>
        {/* Header */}
        <View style={styles.header}>
          <View style={styles.iconCircle}>
            <Ionicons name="mail-open-outline" size={40} color={Colors.white} />
          </View>
          <Text style={styles.title}>Check Your Email</Text>
          <Text style={styles.subtitle}>
            We sent a 6-digit code to{'\n'}
            <Text style={styles.emailText}>{email}</Text>
          </Text>
        </View>

        {/* Form */}
        <View style={styles.form}>
          {error ? (
            <View style={styles.errorBox}>
              <Ionicons name="alert-circle" size={16} color={Colors.secondary} />
              <Text style={styles.errorText}>{error}</Text>
            </View>
          ) : null}

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Confirmation Code</Text>
            <View style={styles.inputRow}>
              <Ionicons
                name="key-outline"
                size={20}
                color={Colors.textMuted}
                style={styles.inputIcon}
              />
              <TextInput
                style={styles.input}
                placeholder="Enter 6-digit code"
                placeholderTextColor={Colors.textMuted}
                value={code}
                onChangeText={setCode}
                keyboardType="number-pad"
                maxLength={6}
                autoComplete="one-time-code"
                editable={!loading}
              />
            </View>
          </View>

          <TouchableOpacity
            style={[styles.button, loading && styles.buttonDisabled]}
            onPress={handleConfirm}
            disabled={loading}
            activeOpacity={0.8}
          >
            {loading ? (
              <ActivityIndicator color={Colors.white} />
            ) : (
              <Text style={styles.buttonText}>Confirm Account</Text>
            )}
          </TouchableOpacity>

          {/* Resend */}
          <View style={styles.resendRow}>
            <Text style={styles.resendText}>Didn't get the code? </Text>
            <TouchableOpacity onPress={handleResend} disabled={resending}>
              <Text style={[styles.resendLink, resending && styles.resendLinkDisabled]}>
                {resending ? 'Sending...' : 'Resend'}
              </Text>
            </TouchableOpacity>
          </View>

          {/* Back to sign up */}
          <TouchableOpacity
            style={styles.backLink}
            onPress={() => router.back()}
          >
            <Ionicons name="arrow-back" size={16} color={Colors.textMuted} />
            <Text style={styles.backText}>Back to Sign Up</Text>
          </TouchableOpacity>
        </View>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  center: {
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 28,
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
  iconCircle: {
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
  },
  emailText: {
    fontWeight: '600',
    color: Colors.text,
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
    fontSize: 20,
    fontWeight: '600',
    color: Colors.text,
    letterSpacing: 4,
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
    opacity: 0.7,
  },
  buttonText: {
    color: Colors.white,
    fontSize: 16,
    fontWeight: '600',
  },
  resendRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  resendText: {
    fontSize: 14,
    color: Colors.textLight,
  },
  resendLink: {
    fontSize: 14,
    fontWeight: '600',
    color: Colors.primary,
  },
  resendLinkDisabled: {
    opacity: 0.5,
  },
  backLink: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 6,
    marginTop: 4,
  },
  backText: {
    fontSize: 14,
    color: Colors.textMuted,
  },
});
