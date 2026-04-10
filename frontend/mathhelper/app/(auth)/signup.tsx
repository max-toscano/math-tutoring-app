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
  ScrollView,
} from 'react-native';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '../../constants/Colors';
import { signUp } from '../../services/auth';
import { validatePassword, validateDisplayName } from '../../utils/validation';
import ValidationChecklist from '../../components/ValidationChecklist';
import PasswordStrengthMeter from '../../components/PasswordStrengthMeter';

export default function SignUpScreen() {
  const router = useRouter();
  const [displayName, setDisplayName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [displayNameFocused, setDisplayNameFocused] = useState(false);
  const [passwordFocused, setPasswordFocused] = useState(false);

  async function handleSignUp() {
    if (!email.trim() || !password) {
      setError('Please fill in all required fields.');
      return;
    }
    const pwResult = validatePassword(password);
    if (!pwResult.minLength || !pwResult.hasUppercase || !pwResult.hasLowercase || !pwResult.hasNumber || !pwResult.hasSpecial) {
      setError('Password does not meet all requirements. Check the checklist below the password field.');
      return;
    }
    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }
    setError('');
    setLoading(true);
    try {
      const { username } = await signUp(email.trim(), password, displayName.trim() || undefined);
      // Pass both email (for display) and username (UUID, required by Cognito for confirmSignUp/resend)
      router.push({ pathname: '/(auth)/confirm-signup', params: { email: email.trim(), username } });
    } catch (e: any) {
      const msg = e?.message ?? 'Sign up failed. Please try again.';
      setError(msg);
      if (Platform.OS !== 'web') {
        Alert.alert('Sign Up Error', msg);
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <ScrollView
        contentContainerStyle={styles.scroll}
        keyboardShouldPersistTaps="handled"
      >
        <View style={styles.inner}>
          {/* Header */}
          <View style={styles.header}>
            <View style={styles.logoCircle}>
              <Ionicons name="calculator" size={40} color={Colors.white} />
            </View>
            <Text style={styles.title}>Create Account</Text>
            <Text style={styles.subtitle}>Start solving math with AI</Text>
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
              <Text style={styles.label}>Display Name</Text>
              <View style={styles.inputRow}>
                <Ionicons name="person-outline" size={20} color={Colors.textMuted} style={styles.inputIcon} />
                <TextInput
                  style={styles.input}
                  placeholder="What should we call you?"
                  placeholderTextColor={Colors.textMuted}
                  value={displayName}
                  onChangeText={setDisplayName}
                  autoCapitalize="none"
                  editable={!loading}
                  onFocus={() => setDisplayNameFocused(true)}
                  onBlur={() => setDisplayNameFocused(false)}
                />
              </View>
              {(() => {
                const dnVisible = displayNameFocused || displayName.length > 0;
                const dnVal = validateDisplayName(displayName);
                return (
                  <ValidationChecklist
                    visible={dnVisible}
                    items={[
                      { label: 'At least 3 characters', passed: dnVal.minLength },
                      { label: '20 characters max', passed: dnVal.maxLength },
                      { label: 'No spaces', passed: dnVal.noSpaces },
                      { label: 'Letters, numbers, and underscores only', passed: dnVal.validChars },
                    ]}
                  />
                );
              })()}
            </View>

            <View style={styles.inputGroup}>
              <Text style={styles.label}>Email *</Text>
              <View style={styles.inputRow}>
                <Ionicons name="mail-outline" size={20} color={Colors.textMuted} style={styles.inputIcon} />
                <TextInput
                  style={styles.input}
                  placeholder="you@example.com"
                  placeholderTextColor={Colors.textMuted}
                  value={email}
                  onChangeText={setEmail}
                  autoCapitalize="none"
                  keyboardType="email-address"
                  autoComplete="email"
                  editable={!loading}
                />
              </View>
            </View>

            <View style={styles.inputGroup}>
              <Text style={styles.label}>Password *</Text>
              <View style={styles.inputRow}>
                <Ionicons name="lock-closed-outline" size={20} color={Colors.textMuted} style={styles.inputIcon} />
                <TextInput
                  style={[styles.input, { flex: 1 }]}
                  placeholder="At least 8 characters"
                  placeholderTextColor={Colors.textMuted}
                  value={password}
                  onChangeText={setPassword}
                  secureTextEntry={!showPassword}
                  autoComplete="new-password"
                  editable={!loading}
                  onFocus={() => setPasswordFocused(true)}
                  onBlur={() => setPasswordFocused(false)}
                />
                <TouchableOpacity onPress={() => setShowPassword(!showPassword)} style={styles.eyeBtn}>
                  <Ionicons name={showPassword ? 'eye-off-outline' : 'eye-outline'} size={20} color={Colors.textMuted} />
                </TouchableOpacity>
              </View>
              {(() => {
                const pwVisible = passwordFocused || password.length > 0;
                const pwVal = validatePassword(password);
                return (
                  <>
                    <PasswordStrengthMeter visible={pwVisible} score={pwVal.strength} />
                    <ValidationChecklist
                      visible={pwVisible}
                      items={[
                        { label: 'At least 8 characters', passed: pwVal.minLength },
                        { label: 'One uppercase letter', passed: pwVal.hasUppercase },
                        { label: 'One lowercase letter', passed: pwVal.hasLowercase },
                        { label: 'One number', passed: pwVal.hasNumber },
                        { label: 'One special character (!@#$...)', passed: pwVal.hasSpecial },
                      ]}
                    />
                  </>
                );
              })()}
            </View>

            <View style={styles.inputGroup}>
              <Text style={styles.label}>Confirm Password *</Text>
              <View style={styles.inputRow}>
                <Ionicons name="lock-closed-outline" size={20} color={Colors.textMuted} style={styles.inputIcon} />
                <TextInput
                  style={styles.input}
                  placeholder="Re-enter your password"
                  placeholderTextColor={Colors.textMuted}
                  value={confirmPassword}
                  onChangeText={setConfirmPassword}
                  secureTextEntry={!showPassword}
                  autoComplete="new-password"
                  editable={!loading}
                />
              </View>
            </View>

            <TouchableOpacity
              style={[styles.button, loading && styles.buttonDisabled]}
              onPress={handleSignUp}
              disabled={loading}
              activeOpacity={0.8}
            >
              {loading ? (
                <ActivityIndicator color={Colors.white} />
              ) : (
                <Text style={styles.buttonText}>Create Account</Text>
              )}
            </TouchableOpacity>

            <View style={styles.footer}>
              <Text style={styles.footerText}>Already have an account?</Text>
              <TouchableOpacity onPress={() => router.back()}>
                <Text style={styles.footerLink}> Sign In</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  scroll: {
    flexGrow: 1,
    justifyContent: 'center',
  },
  inner: {
    paddingHorizontal: 28,
    paddingVertical: 40,
  },
  header: {
    alignItems: 'center',
    marginBottom: 32,
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
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 15,
    color: Colors.textLight,
  },
  form: {
    gap: 16,
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
  footer: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: 8,
  },
  footerText: {
    color: Colors.textLight,
    fontSize: 14,
  },
  footerLink: {
    color: Colors.primary,
    fontSize: 14,
    fontWeight: '600',
  },
});
