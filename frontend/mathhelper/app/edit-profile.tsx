import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  ActivityIndicator,
  Alert,
  Image,
} from 'react-native';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import * as ImagePicker from 'expo-image-picker';
import { Colors } from '../constants/Colors';
import { useAppContext } from '../context/AppContext';
import { fetchProfile, updateProfile, type UserProfile } from '../services/database';
import { uploadImage, getImageUrl } from '../services/storage';
import { requestPasswordReset } from '../services/auth';

// ─── Grade levels the user can pick from ────────────────────────────────────
const GRADE_OPTIONS = [
  'Grade 6', 'Grade 7', 'Grade 8', 'Grade 9', 'Grade 10',
  'Grade 11', 'Grade 12', 'College Freshman', 'College Sophomore',
];

export default function EditProfileScreen() {
  const router = useRouter();
  const insets = useSafeAreaInsets();
  const { user } = useAppContext();

  // ─── Form state ───────────────────────────────────────────────────────────
  const [displayName, setDisplayName] = useState('');
  const [bio, setBio] = useState('');
  const [gradeLevel, setGradeLevel] = useState('');
  const [avatarUri, setAvatarUri] = useState<string | null>(null);
  const [avatarStoragePath, setAvatarStoragePath] = useState<string | null>(null);

  // ─── UI state ─────────────────────────────────────────────────────────────
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [hasChanges, setHasChanges] = useState(false);
  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');
  const [showGradePicker, setShowGradePicker] = useState(false);
  const [resetEmailSent, setResetEmailSent] = useState(false);

  // Store the original values so we can detect changes
  const originalRef = useRef<{ name: string; bio: string; grade: string; avatar: string | null }>({
    name: '', bio: '', grade: '', avatar: null,
  });

  // ─── Load profile on mount ────────────────────────────────────────────────
  useEffect(() => {
    if (!user) return;
    (async () => {
      try {
        const profile = await fetchProfile(user.id);
        if (profile) {
          setDisplayName(profile.display_name ?? '');
          setBio(profile.bio ?? '');
          setGradeLevel(profile.grade_level ?? '');
          setAvatarStoragePath(profile.avatar_url);

          originalRef.current = {
            name: profile.display_name ?? '',
            bio: profile.bio ?? '',
            grade: profile.grade_level ?? '',
            avatar: profile.avatar_url,
          };

          // Resolve avatar signed URL
          if (profile.avatar_url) {
            try {
              const signed = await getImageUrl(profile.avatar_url);
              setAvatarUri(signed);
            } catch {
              // Avatar path might be invalid — no crash
            }
          }
        }
      } catch (e) {
        console.error('Failed to load profile:', e);
      } finally {
        setLoading(false);
      }
    })();
  }, [user]);

  // ─── Track changes ────────────────────────────────────────────────────────
  useEffect(() => {
    const orig = originalRef.current;
    const changed =
      displayName !== orig.name ||
      bio !== orig.bio ||
      gradeLevel !== orig.grade ||
      avatarStoragePath !== orig.avatar;
    setHasChanges(changed);
  }, [displayName, bio, gradeLevel, avatarStoragePath]);

  // ─── Pick avatar from camera roll ─────────────────────────────────────────
  async function handlePickAvatar() {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ['images'],
      allowsEditing: true,
      aspect: [1, 1],
      quality: 0.7,
    });

    if (result.canceled || !result.assets[0]) return;

    const localUri = result.assets[0].uri;
    setAvatarUri(localUri); // Show the local preview immediately

    if (!user) return;
    try {
      // Upload to Supabase Storage
      const path = await uploadImage(user.id, localUri);
      setAvatarStoragePath(path);
    } catch (e: any) {
      Alert.alert('Upload Failed', e?.message ?? 'Could not upload image.');
    }
  }

  function handleRemoveAvatar() {
    setAvatarUri(null);
    setAvatarStoragePath(null);
  }

  // ─── Save profile ─────────────────────────────────────────────────────────
  async function handleSave() {
    if (!user) return;

    // Validation
    if (!displayName.trim()) {
      setError('Display name cannot be empty.');
      return;
    }
    if (displayName.trim().length > 50) {
      setError('Display name must be under 50 characters.');
      return;
    }
    if (bio.length > 200) {
      setError('Bio must be under 200 characters.');
      return;
    }

    setError('');
    setSaving(true);

    try {
      await updateProfile(user.id, {
        display_name: displayName.trim(),
        bio: bio.trim() || null,
        grade_level: gradeLevel || null,
        avatar_url: avatarStoragePath,
      });

      // Update originals so hasChanges resets
      originalRef.current = {
        name: displayName.trim(),
        bio: bio.trim(),
        grade: gradeLevel,
        avatar: avatarStoragePath,
      };
      setHasChanges(false);
      setSuccessMsg('Profile updated!');
      setTimeout(() => setSuccessMsg(''), 2500);
    } catch (e: any) {
      const msg = e?.message ?? 'Failed to save. Try again.';
      setError(msg);
      if (Platform.OS !== 'web') Alert.alert('Error', msg);
    } finally {
      setSaving(false);
    }
  }

  // ─── Discard & go back ────────────────────────────────────────────────────
  function handleCancel() {
    if (hasChanges) {
      Alert.alert(
        'Discard Changes?',
        'You have unsaved changes. Are you sure you want to go back?',
        [
          { text: 'Keep Editing', style: 'cancel' },
          { text: 'Discard', style: 'destructive', onPress: () => router.back() },
        ],
      );
    } else {
      router.back();
    }
  }

  // ─── Send password reset ──────────────────────────────────────────────────
  async function handleChangePassword() {
    if (!user?.email) return;
    try {
      await requestPasswordReset(user.email);
      setResetEmailSent(true);
      Alert.alert('Email Sent', `A password reset link was sent to ${user.email}.`);
    } catch (e: any) {
      Alert.alert('Error', e?.message ?? 'Could not send reset email.');
    }
  }

  // ─── Initials for fallback avatar ─────────────────────────────────────────
  const initials = displayName
    .split(' ')
    .map((w) => w[0])
    .join('')
    .toUpperCase()
    .slice(0, 2) || '?';

  // ─── Loading state ────────────────────────────────────────────────────────
  if (loading) {
    return (
      <View style={[styles.container, styles.centered]}>
        <ActivityIndicator size="large" color={Colors.primary} />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* ── Header ─────────────────────────────────────────────────────────── */}
      <View style={[styles.header, { paddingTop: insets.top + 12 }]}>
        <TouchableOpacity onPress={handleCancel} style={styles.headerBtn}>
          <Ionicons name="arrow-back" size={24} color={Colors.white} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Edit Profile</Text>
        <TouchableOpacity
          onPress={handleSave}
          disabled={!hasChanges || saving}
          style={styles.headerBtn}
        >
          {saving ? (
            <ActivityIndicator size="small" color={Colors.white} />
          ) : (
            <Text style={[styles.saveText, !hasChanges && styles.saveTextDisabled]}>
              Save
            </Text>
          )}
        </TouchableOpacity>
      </View>

      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      >
        <ScrollView
          style={styles.scroll}
          contentContainerStyle={styles.scrollContent}
          keyboardShouldPersistTaps="handled"
          showsVerticalScrollIndicator={false}
        >
          {/* ── Success / Error banners ──────────────────────────────────── */}
          {successMsg ? (
            <View style={styles.successBanner}>
              <Ionicons name="checkmark-circle" size={18} color="#10B981" />
              <Text style={styles.successText}>{successMsg}</Text>
            </View>
          ) : null}
          {error ? (
            <View style={styles.errorBanner}>
              <Ionicons name="alert-circle" size={18} color={Colors.secondary} />
              <Text style={styles.errorText}>{error}</Text>
            </View>
          ) : null}

          {/* ── Avatar section ───────────────────────────────────────────── */}
          <View style={styles.avatarSection}>
            <TouchableOpacity onPress={handlePickAvatar} activeOpacity={0.8}>
              {avatarUri ? (
                <Image source={{ uri: avatarUri }} style={styles.avatarImage} />
              ) : (
                <View style={styles.avatarFallback}>
                  <Text style={styles.avatarInitials}>{initials}</Text>
                </View>
              )}
              <View style={styles.cameraBadge}>
                <Ionicons name="camera" size={14} color={Colors.white} />
              </View>
            </TouchableOpacity>

            <View style={styles.avatarActions}>
              <TouchableOpacity onPress={handlePickAvatar} style={styles.avatarBtn}>
                <Text style={styles.avatarBtnText}>Change Photo</Text>
              </TouchableOpacity>
              {avatarUri ? (
                <TouchableOpacity onPress={handleRemoveAvatar} style={styles.avatarBtn}>
                  <Text style={[styles.avatarBtnText, { color: Colors.secondary }]}>Remove</Text>
                </TouchableOpacity>
              ) : null}
            </View>
          </View>

          {/* ── Form fields ──────────────────────────────────────────────── */}
          <View style={styles.formCard}>
            {/* Display Name */}
            <View style={styles.fieldGroup}>
              <Text style={styles.fieldLabel}>Display Name</Text>
              <TextInput
                style={styles.fieldInput}
                value={displayName}
                onChangeText={setDisplayName}
                placeholder="Your name"
                placeholderTextColor={Colors.textMuted}
                maxLength={50}
                autoCapitalize="words"
              />
              <Text style={styles.charCount}>{displayName.length}/50</Text>
            </View>

            <View style={styles.fieldDivider} />

            {/* Email (read-only) */}
            <View style={styles.fieldGroup}>
              <Text style={styles.fieldLabel}>Email</Text>
              <View style={styles.readOnlyRow}>
                <Text style={styles.readOnlyValue}>{user?.email ?? ''}</Text>
                <View style={styles.lockBadge}>
                  <Ionicons name="lock-closed" size={12} color={Colors.textMuted} />
                </View>
              </View>
              <Text style={styles.fieldHint}>
                Email is tied to your login and can't be changed here.
              </Text>
            </View>

            <View style={styles.fieldDivider} />

            {/* Grade Level */}
            <View style={styles.fieldGroup}>
              <Text style={styles.fieldLabel}>Grade Level</Text>
              <TouchableOpacity
                style={styles.pickerRow}
                onPress={() => setShowGradePicker(!showGradePicker)}
                activeOpacity={0.7}
              >
                <Text style={[styles.pickerValue, !gradeLevel && styles.pickerPlaceholder]}>
                  {gradeLevel || 'Select your grade'}
                </Text>
                <Ionicons
                  name={showGradePicker ? 'chevron-up' : 'chevron-down'}
                  size={18}
                  color={Colors.textMuted}
                />
              </TouchableOpacity>
              {showGradePicker ? (
                <View style={styles.pickerOptions}>
                  {GRADE_OPTIONS.map((g) => (
                    <TouchableOpacity
                      key={g}
                      style={[styles.pickerOption, gradeLevel === g && styles.pickerOptionActive]}
                      onPress={() => { setGradeLevel(g); setShowGradePicker(false); }}
                    >
                      <Text style={[
                        styles.pickerOptionText,
                        gradeLevel === g && styles.pickerOptionTextActive,
                      ]}>
                        {g}
                      </Text>
                      {gradeLevel === g ? (
                        <Ionicons name="checkmark" size={18} color={Colors.primary} />
                      ) : null}
                    </TouchableOpacity>
                  ))}
                </View>
              ) : null}
            </View>

            <View style={styles.fieldDivider} />

            {/* Bio */}
            <View style={styles.fieldGroup}>
              <Text style={styles.fieldLabel}>Bio</Text>
              <TextInput
                style={[styles.fieldInput, styles.bioInput]}
                value={bio}
                onChangeText={setBio}
                placeholder="Tell us about yourself (optional)"
                placeholderTextColor={Colors.textMuted}
                maxLength={200}
                multiline
                numberOfLines={3}
                textAlignVertical="top"
              />
              <Text style={styles.charCount}>{bio.length}/200</Text>
            </View>
          </View>

          {/* ── Security section ──────────────────────────────────────────── */}
          <Text style={styles.sectionLabel}>SECURITY</Text>
          <View style={styles.formCard}>
            <TouchableOpacity
              style={styles.securityRow}
              onPress={handleChangePassword}
              disabled={resetEmailSent}
              activeOpacity={0.7}
            >
              <View style={[styles.securityIcon, { backgroundColor: Colors.orange + '18' }]}>
                <Ionicons name="key-outline" size={18} color={Colors.orange} />
              </View>
              <View style={{ flex: 1 }}>
                <Text style={styles.securityLabel}>Change Password</Text>
                <Text style={styles.securityHint}>
                  {resetEmailSent
                    ? 'Reset link sent — check your email'
                    : 'We\'ll send a reset link to your email'}
                </Text>
              </View>
              {resetEmailSent ? (
                <Ionicons name="checkmark-circle" size={20} color="#10B981" />
              ) : (
                <Ionicons name="chevron-forward" size={18} color={Colors.textMuted} />
              )}
            </TouchableOpacity>
          </View>

          {/* Bottom padding */}
          <View style={{ height: 40 }} />
        </ScrollView>
      </KeyboardAvoidingView>
    </View>
  );
}

// ─── Styles ──────────────────────────────────────────────────────────────────

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  centered: {
    justifyContent: 'center',
    alignItems: 'center',
  },

  // Header
  header: {
    backgroundColor: Colors.primary,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingBottom: 16,
    borderBottomLeftRadius: 24,
    borderBottomRightRadius: 24,
  },
  headerBtn: {
    width: 50,
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: Colors.white,
  },
  saveText: {
    fontSize: 16,
    fontWeight: '700',
    color: Colors.white,
  },
  saveTextDisabled: {
    opacity: 0.4,
  },

  // Scroll
  scroll: { flex: 1 },
  scrollContent: { padding: 16 },

  // Banners
  successBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: '#D1FAE5',
    padding: 12,
    borderRadius: 12,
    marginBottom: 16,
  },
  successText: { color: '#065F46', fontSize: 14, fontWeight: '500', flex: 1 },
  errorBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: '#FEE2E2',
    padding: 12,
    borderRadius: 12,
    marginBottom: 16,
  },
  errorText: { color: Colors.secondary, fontSize: 14, flex: 1 },

  // Avatar
  avatarSection: {
    alignItems: 'center',
    marginBottom: 24,
    gap: 12,
  },
  avatarImage: {
    width: 100,
    height: 100,
    borderRadius: 50,
    borderWidth: 3,
    borderColor: Colors.primary,
  },
  avatarFallback: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: Colors.primary,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 3,
    borderColor: Colors.primaryLight,
  },
  avatarInitials: {
    fontSize: 36,
    fontWeight: '700',
    color: Colors.white,
  },
  cameraBadge: {
    position: 'absolute',
    bottom: 0,
    right: 0,
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: Colors.primary,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 3,
    borderColor: Colors.white,
  },
  avatarActions: {
    flexDirection: 'row',
    gap: 16,
  },
  avatarBtn: {
    paddingVertical: 4,
    paddingHorizontal: 8,
  },
  avatarBtnText: {
    fontSize: 14,
    fontWeight: '600',
    color: Colors.primary,
  },

  // Form card
  formCard: {
    backgroundColor: Colors.card,
    borderRadius: 16,
    overflow: 'hidden',
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 1,
  },
  fieldGroup: {
    paddingHorizontal: 16,
    paddingVertical: 14,
  },
  fieldLabel: {
    fontSize: 12,
    fontWeight: '700',
    color: Colors.textMuted,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
    marginBottom: 8,
  },
  fieldInput: {
    fontSize: 16,
    color: Colors.text,
    backgroundColor: Colors.background,
    borderRadius: 10,
    paddingHorizontal: 14,
    paddingVertical: 12,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  bioInput: {
    minHeight: 80,
    paddingTop: 12,
  },
  charCount: {
    fontSize: 11,
    color: Colors.textMuted,
    textAlign: 'right',
    marginTop: 4,
  },
  fieldHint: {
    fontSize: 12,
    color: Colors.textMuted,
    marginTop: 4,
  },
  fieldDivider: {
    height: 1,
    backgroundColor: Colors.border,
    marginHorizontal: 16,
  },

  // Read-only row (email)
  readOnlyRow: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Colors.background,
    borderRadius: 10,
    paddingHorizontal: 14,
    paddingVertical: 12,
    borderWidth: 1,
    borderColor: Colors.border,
    gap: 8,
  },
  readOnlyValue: {
    flex: 1,
    fontSize: 16,
    color: Colors.textLight,
  },
  lockBadge: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: Colors.border,
    alignItems: 'center',
    justifyContent: 'center',
  },

  // Grade picker
  pickerRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: Colors.background,
    borderRadius: 10,
    paddingHorizontal: 14,
    paddingVertical: 12,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  pickerValue: {
    fontSize: 16,
    color: Colors.text,
  },
  pickerPlaceholder: {
    color: Colors.textMuted,
  },
  pickerOptions: {
    marginTop: 8,
    backgroundColor: Colors.background,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: Colors.border,
    overflow: 'hidden',
  },
  pickerOption: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 14,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  pickerOptionActive: {
    backgroundColor: Colors.primaryLight,
  },
  pickerOptionText: {
    fontSize: 15,
    color: Colors.text,
  },
  pickerOptionTextActive: {
    color: Colors.primary,
    fontWeight: '600',
  },

  // Section label
  sectionLabel: {
    fontSize: 13,
    fontWeight: '700',
    color: Colors.textMuted,
    letterSpacing: 0.8,
    marginBottom: 8,
    marginLeft: 4,
  },

  // Security row
  securityRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 14,
    gap: 14,
  },
  securityIcon: {
    width: 36,
    height: 36,
    borderRadius: 10,
    alignItems: 'center',
    justifyContent: 'center',
  },
  securityLabel: {
    fontSize: 15,
    fontWeight: '500',
    color: Colors.text,
  },
  securityHint: {
    fontSize: 12,
    color: Colors.textMuted,
    marginTop: 2,
  },
});
