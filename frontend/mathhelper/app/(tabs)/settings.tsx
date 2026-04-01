import { useEffect, useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Switch,
  Image,
} from 'react-native';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Colors } from '../../constants/Colors';
import { useAppContext } from '../../context/AppContext';
import { fetchProfile, type UserProfile } from '../../services/database';
import { getImageUrl } from '../../services/storage';
import { signOut } from '../../services/auth';

type IoniconsName = React.ComponentProps<typeof Ionicons>['name'];

interface SettingRowProps {
  icon: IoniconsName;
  iconColor: string;
  label: string;
  value?: string;
  hasToggle?: boolean;
  toggleValue?: boolean;
  onPress?: () => void;
  showChevron?: boolean;
  danger?: boolean;
}

function SettingRow({
  icon,
  iconColor,
  label,
  value,
  hasToggle = false,
  toggleValue = false,
  onPress,
  showChevron = true,
  danger = false,
}: SettingRowProps) {
  return (
    <TouchableOpacity style={styles.settingRow} activeOpacity={hasToggle ? 1 : 0.7} onPress={onPress}>
      <View style={[styles.settingIconWrap, { backgroundColor: iconColor + '18' }]}>
        <Ionicons name={icon} size={18} color={danger ? Colors.secondary : iconColor} />
      </View>
      <Text style={[styles.settingLabel, danger && styles.settingLabelDanger]}>{label}</Text>
      <View style={styles.settingRight}>
        {value ? <Text style={styles.settingValue}>{value}</Text> : null}
        {hasToggle ? (
          <Switch
            value={toggleValue}
            onValueChange={() => {}}
            trackColor={{ false: Colors.border, true: Colors.primary + '80' }}
            thumbColor={toggleValue ? Colors.primary : Colors.white}
            ios_backgroundColor={Colors.border}
          />
        ) : showChevron ? (
          <Ionicons name="chevron-forward" size={18} color={Colors.textMuted} />
        ) : null}
      </View>
    </TouchableOpacity>
  );
}

interface SettingSectionProps {
  title: string;
  children: React.ReactNode;
}

function SettingSection({ title, children }: SettingSectionProps) {
  return (
    <View style={styles.section}>
      <Text style={styles.sectionTitle}>{title}</Text>
      <View style={styles.sectionCard}>{children}</View>
    </View>
  );
}

const ACHIEVEMENTS = [
  { emoji: '🔥', label: '7-Day Streak', color: Colors.orange },
  { emoji: '💯', label: 'Perfect Score', color: Colors.green },
  { emoji: '📚', label: '100 Problems', color: Colors.primary },
  { emoji: '⚡', label: 'Speed Solver', color: Colors.yellow },
];

export default function SettingsScreen() {
  const insets = useSafeAreaInsets();
  const router = useRouter();
  const { user } = useAppContext();

  // ─── Load real profile data ───────────────────────────────────────────────
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [avatarUri, setAvatarUri] = useState<string | null>(null);

  useEffect(() => {
    if (!user) return;
    (async () => {
      try {
        const p = await fetchProfile(user.id);
        setProfile(p);
        if (p?.avatar_url) {
          try {
            const signed = await getImageUrl(p.avatar_url);
            setAvatarUri(signed);
          } catch { /* skip */ }
        }
      } catch { /* skip */ }
    })();
  }, [user]);

  // Refresh profile when returning from edit-profile screen
  useEffect(() => {
    // Re-fetch each time the screen is focused (settings tab is visible)
    const interval = setInterval(async () => {
      if (!user) return;
      try {
        const p = await fetchProfile(user.id);
        if (p && (p.display_name !== profile?.display_name || p.avatar_url !== profile?.avatar_url || p.grade_level !== profile?.grade_level)) {
          setProfile(p);
          if (p.avatar_url) {
            try { setAvatarUri(await getImageUrl(p.avatar_url)); } catch {}
          } else {
            setAvatarUri(null);
          }
        }
      } catch {}
    }, 2000);
    return () => clearInterval(interval);
  }, [user, profile]);

  const displayName = profile?.display_name || user?.email || 'Student';
  const initials = displayName
    .split(' ')
    .map((w: string) => w[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);

  async function handleSignOut() {
    try {
      await signOut();
    } catch {}
  }

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={[styles.header, { paddingTop: insets.top + 16 }]}>
        <Text style={styles.headerTitle}>Settings</Text>
      </View>

      <ScrollView
        style={styles.scroll}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* Profile Card — tapping navigates to the edit profile screen */}
        <TouchableOpacity
          style={styles.profileCard}
          activeOpacity={0.85}
          onPress={() => router.push('/edit-profile')}
        >
          {avatarUri ? (
            <Image source={{ uri: avatarUri }} style={styles.profileAvatarImg} />
          ) : (
            <View style={styles.profileAvatar}>
              <Text style={styles.profileAvatarText}>{initials}</Text>
            </View>
          )}
          <View style={styles.profileInfo}>
            <Text style={styles.profileName}>{displayName}</Text>
            <Text style={styles.profileMeta}>
              {profile?.grade_level ?? 'No grade set'}
              {profile?.bio ? `  ·  ${profile.bio.slice(0, 30)}${profile.bio.length > 30 ? '...' : ''}` : ''}
            </Text>
          </View>
          <Ionicons name="chevron-forward" size={20} color={Colors.textMuted} />
        </TouchableOpacity>

        {/* Achievements */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Achievements</Text>
            <TouchableOpacity>
              <Text style={styles.seeAll}>See all</Text>
            </TouchableOpacity>
          </View>
          <ScrollView horizontal showsHorizontalScrollIndicator={false}>
            <View style={styles.achievementRow}>
              {ACHIEVEMENTS.map((a) => (
                <View key={a.label} style={styles.achievementCard}>
                  <View style={[styles.achievementEmoji, { backgroundColor: a.color + '20' }]}>
                    <Text style={styles.achievementEmojiText}>{a.emoji}</Text>
                  </View>
                  <Text style={styles.achievementLabel}>{a.label}</Text>
                </View>
              ))}
            </View>
          </ScrollView>
        </View>

        {/* Account */}
        <SettingSection title="Account">
          <SettingRow
            icon="person-outline"
            iconColor={Colors.primary}
            label="Edit Profile"
            onPress={() => router.push('/edit-profile')}
          />
          <View style={styles.rowDivider} />
          <SettingRow
            icon="school-outline"
            iconColor={Colors.teal}
            label="Grade Level"
            value={profile?.grade_level ?? 'Not set'}
          />
          <View style={styles.rowDivider} />
          <SettingRow
            icon="ribbon-outline"
            iconColor={Colors.orange}
            label="Subscription"
            value="Free Plan"
          />
          <View style={styles.rowDivider} />
          <SettingRow
            icon="shield-checkmark-outline"
            iconColor={Colors.green}
            label="Privacy"
          />
        </SettingSection>

        {/* Language */}
        <SettingSection title="Language">
          <SettingRow
            icon="language-outline"
            iconColor={Colors.teal}
            label="Language"
            value="English"
          />
        </SettingSection>

        {/* Notifications */}
        <SettingSection title="Notifications">
          <SettingRow
            icon="notifications-outline"
            iconColor={Colors.primary}
            label="Push Notifications"
            hasToggle
            toggleValue={true}
            showChevron={false}
          />
          <View style={styles.rowDivider} />
          <SettingRow
            icon="alarm-outline"
            iconColor={Colors.orange}
            label="Daily Reminder"
            hasToggle
            toggleValue={true}
            showChevron={false}
          />
          <View style={styles.rowDivider} />
          <SettingRow
            icon="time-outline"
            iconColor={Colors.teal}
            label="Reminder Time"
            value="7:00 PM"
          />
          <View style={styles.rowDivider} />
          <SettingRow
            icon="trophy-outline"
            iconColor={Colors.yellow}
            label="Achievement Alerts"
            hasToggle
            toggleValue={true}
            showChevron={false}
          />
        </SettingSection>

        {/* Appearance */}
        <SettingSection title="Appearance">
          <SettingRow
            icon="moon-outline"
            iconColor="#9B59B6"
            label="Dark Mode"
            hasToggle
            toggleValue={false}
            showChevron={false}
          />
          <View style={styles.rowDivider} />
          <SettingRow
            icon="text-outline"
            iconColor={Colors.teal}
            label="Font Size"
            value="Medium"
          />
          <View style={styles.rowDivider} />
          <SettingRow
            icon="color-palette-outline"
            iconColor={Colors.primary}
            label="Theme Color"
            value="Purple"
          />
        </SettingSection>

        {/* About */}
        <SettingSection title="About">
          <SettingRow
            icon="star-outline"
            iconColor={Colors.yellow}
            label="Rate MathHelper"
          />
          <View style={styles.rowDivider} />
          <SettingRow
            icon="help-circle-outline"
            iconColor={Colors.teal}
            label="Help & Support"
          />
          <View style={styles.rowDivider} />
          <SettingRow
            icon="document-text-outline"
            iconColor={Colors.textLight}
            label="Terms of Service"
          />
          <View style={styles.rowDivider} />
          <SettingRow
            icon="lock-closed-outline"
            iconColor={Colors.textLight}
            label="Privacy Policy"
          />
          <View style={styles.rowDivider} />
          <SettingRow
            icon="information-circle-outline"
            iconColor={Colors.textLight}
            label="Version"
            value="1.0.0"
            showChevron={false}
          />
        </SettingSection>

        {/* Sign Out */}
        <View style={styles.section}>
          <View style={styles.sectionCard}>
            <SettingRow
              icon="log-out-outline"
              iconColor={Colors.secondary}
              label="Sign Out"
              showChevron={false}
              danger
              onPress={handleSignOut}
            />
          </View>
        </View>

        <Text style={styles.footerText}>MathHelper · Made for students, by students</Text>
        <View style={styles.bottomPad} />
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  header: {
    backgroundColor: Colors.primary,
    paddingHorizontal: 20,
    paddingBottom: 20,
    borderBottomLeftRadius: 24,
    borderBottomRightRadius: 24,
  },
  headerTitle: {
    fontSize: 26,
    fontWeight: '700',
    color: Colors.white,
  },
  scroll: {
    flex: 1,
  },
  scrollContent: {
    padding: 16,
  },
  profileCard: {
    backgroundColor: Colors.card,
    borderRadius: 20,
    padding: 18,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 16,
    marginBottom: 24,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.1,
    shadowRadius: 10,
    elevation: 4,
    borderWidth: 1,
    borderColor: Colors.primaryLight,
  },
  profileAvatarImg: {
    width: 60,
    height: 60,
    borderRadius: 20,
    borderWidth: 2,
    borderColor: Colors.primaryLight,
  },
  profileAvatar: {
    width: 60,
    height: 60,
    borderRadius: 20,
    backgroundColor: Colors.primary,
    alignItems: 'center',
    justifyContent: 'center',
    position: 'relative',
  },
  profileAvatarText: {
    fontSize: 22,
    fontWeight: '700',
    color: Colors.white,
  },
  profileBadge: {
    position: 'absolute',
    bottom: -3,
    right: -3,
    width: 20,
    height: 20,
    borderRadius: 10,
    backgroundColor: Colors.orange,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 2,
    borderColor: Colors.white,
  },
  profileInfo: {
    flex: 1,
    gap: 4,
  },
  profileName: {
    fontSize: 18,
    fontWeight: '700',
    color: Colors.text,
  },
  profileMeta: {
    fontSize: 13,
    color: Colors.textLight,
  },
  profileLevelRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginTop: 2,
  },
  profileLevelBadge: {
    backgroundColor: Colors.primaryLight,
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 8,
  },
  profileLevelText: {
    fontSize: 12,
    fontWeight: '700',
    color: Colors.primary,
  },
  profileXP: {
    fontSize: 12,
    color: Colors.textLight,
    fontWeight: '500',
  },
  section: {
    marginBottom: 20,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 13,
    fontWeight: '700',
    color: Colors.textMuted,
    textTransform: 'uppercase',
    letterSpacing: 0.8,
    marginBottom: 8,
  },
  seeAll: {
    fontSize: 14,
    color: Colors.primary,
    fontWeight: '600',
    marginBottom: 8,
  },
  sectionCard: {
    backgroundColor: Colors.card,
    borderRadius: 16,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 1,
  },
  settingRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 14,
    gap: 14,
  },
  settingIconWrap: {
    width: 36,
    height: 36,
    borderRadius: 10,
    alignItems: 'center',
    justifyContent: 'center',
  },
  settingLabel: {
    flex: 1,
    fontSize: 15,
    color: Colors.text,
    fontWeight: '500',
  },
  settingLabelDanger: {
    color: Colors.secondary,
  },
  settingRight: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  settingValue: {
    fontSize: 14,
    color: Colors.textLight,
  },
  rowDivider: {
    height: 1,
    backgroundColor: Colors.border,
    marginLeft: 66,
  },
  achievementRow: {
    flexDirection: 'row',
    gap: 12,
    paddingRight: 16,
  },
  achievementCard: {
    alignItems: 'center',
    gap: 8,
    width: 80,
  },
  achievementEmoji: {
    width: 56,
    height: 56,
    borderRadius: 16,
    alignItems: 'center',
    justifyContent: 'center',
  },
  achievementEmojiText: {
    fontSize: 26,
  },
  achievementLabel: {
    fontSize: 11,
    color: Colors.textLight,
    textAlign: 'center',
    fontWeight: '500',
    lineHeight: 14,
  },
  footerText: {
    textAlign: 'center',
    fontSize: 12,
    color: Colors.textMuted,
    marginTop: 8,
    marginBottom: 4,
  },
  bottomPad: {
    height: 16,
  },
});
