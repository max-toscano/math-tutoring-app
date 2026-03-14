import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Image,
  Alert,
  Platform,
} from 'react-native';
import { useState, useMemo } from 'react';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useAppContext, type SavedItem, type TutoringSession } from '../../context/AppContext';
import { Colors } from '../../constants/Colors';

const DIFF_COLORS: Record<string, string> = {
  Easy: Colors.green,
  Medium: Colors.orange,
  Hard: Colors.secondary,
};

function formatDate(iso: string) {
  const d = new Date(iso);
  const now = new Date();
  const diffMs = now.getTime() - d.getTime();
  const diffDays = Math.floor(diffMs / 86400000);
  if (diffDays === 0) return 'Today';
  if (diffDays === 1) return 'Yesterday';
  if (diffDays < 7) return `${diffDays} days ago`;
  return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
}

// ─── Tab Selector ─────────────────────────────────────────────────────────────
type TabKey = 'problems' | 'sessions';

// ─── Expandable Saved Card ────────────────────────────────────────────────────
function SavedCard({ item, onDelete }: { item: SavedItem; onDelete: () => void }) {
  const [expanded, setExpanded] = useState(false);
  const diffColor = DIFF_COLORS[item.analysis.difficulty] ?? Colors.orange;

  function confirmDelete() {
    if (Platform.OS === 'web') {
      if (window.confirm('Are you sure you want to remove this from your collection?')) {
        onDelete();
      }
    } else {
      Alert.alert(
        'Delete Saved Problem',
        'Are you sure you want to remove this from your collection?',
        [
          { text: 'Cancel', style: 'cancel' },
          { text: 'Delete', style: 'destructive', onPress: onDelete },
        ]
      );
    }
  }

  return (
    <View style={styles.card}>
      <Image source={{ uri: item.imageUri }} style={styles.cardImage} resizeMode="cover" />

      <View style={styles.cardBody}>
        <View style={styles.cardTopRow}>
          <View style={styles.badgeRow}>
            <View style={[styles.badge, { backgroundColor: Colors.primaryLight }]}>
              <Text style={[styles.badgeText, { color: Colors.primary }]}>{item.analysis.topic}</Text>
            </View>
            <View style={[styles.badge, { backgroundColor: diffColor + '20' }]}>
              <Text style={[styles.badgeText, { color: diffColor }]}>{item.analysis.difficulty}</Text>
            </View>
          </View>
          <Text style={styles.dateText}>{formatDate(item.savedAt)}</Text>
        </View>

        <Text style={styles.problemText} numberOfLines={expanded ? undefined : 2}>
          {item.analysis.problem}
        </Text>

        <View style={styles.answerRow}>
          <View style={styles.answerBox}>
            <Text style={styles.answerLabel}>ANSWER</Text>
            <Text style={styles.answerText}>{item.analysis.answer}</Text>
          </View>
        </View>

        <TouchableOpacity style={styles.expandBtn} onPress={() => setExpanded((v) => !v)} activeOpacity={0.7}>
          <Text style={styles.expandBtnText}>{expanded ? 'Hide Breakdown' : 'View Full Breakdown'}</Text>
          <Ionicons name={expanded ? 'chevron-up' : 'chevron-down'} size={16} color={Colors.primary} />
        </TouchableOpacity>

        {expanded && (
          <View style={styles.breakdown}>
            <Text style={styles.breakdownTitle}>Step-by-Step Solution</Text>
            {item.analysis.steps.map((s) => (
              <View key={s.step} style={styles.stepRow}>
                <View style={styles.stepBubble}>
                  <Text style={styles.stepBubbleText}>{s.step}</Text>
                </View>
                <View style={styles.stepBody}>
                  <Text style={styles.stepTitle}>{s.title}</Text>
                  <Text style={styles.stepExplanation}>{s.explanation}</Text>
                  {s.math ? (
                    <View style={styles.mathBox}>
                      <Text style={styles.mathText}>{s.math}</Text>
                    </View>
                  ) : null}
                </View>
              </View>
            ))}

            {item.analysis.concepts?.length > 0 && (
              <View style={styles.conceptsSection}>
                <Text style={styles.conceptsHeading}>Key Concepts</Text>
                <View style={styles.conceptsPills}>
                  {item.analysis.concepts.map((c, i) => (
                    <View key={i} style={styles.pill}>
                      <Text style={styles.pillText}>{c}</Text>
                    </View>
                  ))}
                </View>
              </View>
            )}

            {item.analysis.tip ? (
              <View style={styles.tipBox}>
                <Ionicons name="bulb-outline" size={17} color={Colors.yellow} />
                <Text style={styles.tipText}>{item.analysis.tip}</Text>
              </View>
            ) : null}
          </View>
        )}

        <TouchableOpacity style={styles.deleteBtn} onPress={confirmDelete} activeOpacity={0.7}>
          <Ionicons name="trash-outline" size={15} color={Colors.secondary} />
          <Text style={styles.deleteBtnText}>Remove from Saved</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

// ─── Session Card (for Saved tab) ─────────────────────────────────────────────
function SessionCard({ session, onDelete }: { session: TutoringSession; onDelete: () => void }) {
  const [expanded, setExpanded] = useState(false);

  function confirmDelete() {
    if (Platform.OS === 'web') {
      if (window.confirm('Are you sure you want to delete this tutoring session?')) {
        onDelete();
      }
    } else {
      Alert.alert(
        'Delete Session',
        'Are you sure you want to delete this tutoring session?',
        [
          { text: 'Cancel', style: 'cancel' },
          { text: 'Delete', style: 'destructive', onPress: onDelete },
        ]
      );
    }
  }

  const messageCount = session.messages.length;
  const userMsgCount = session.messages.filter((m) => m.role === 'user').length;
  const assistantMsgCount = session.messages.filter((m) => m.role === 'assistant').length;

  return (
    <View style={styles.card}>
      {/* Session header bar */}
      <View style={styles.sessionHeaderBar}>
        <View style={styles.sessionHeaderIcon}>
          <Ionicons name="chatbubbles" size={18} color={Colors.primary} />
        </View>
        <View style={styles.sessionHeaderInfo}>
          <Text style={styles.sessionHeaderTitle} numberOfLines={1}>{session.title}</Text>
          <Text style={styles.sessionHeaderDate}>{formatDate(session.savedAt)}</Text>
        </View>
        {session.analysis && (
          <View style={[styles.badge, { backgroundColor: Colors.primaryLight }]}>
            <Text style={[styles.badgeText, { color: Colors.primary }]}>{session.analysis.topic}</Text>
          </View>
        )}
      </View>

      <View style={styles.cardBody}>
        {/* Preview */}
        <Text style={styles.sessionPreviewText} numberOfLines={expanded ? undefined : 3}>
          {session.preview}
        </Text>

        {/* Stats row */}
        <View style={styles.sessionStatsRow}>
          <View style={styles.sessionStat}>
            <Ionicons name="chatbubble-outline" size={13} color={Colors.textLight} />
            <Text style={styles.sessionStatText}>{messageCount} messages</Text>
          </View>
          <View style={styles.sessionStat}>
            <Ionicons name="person-outline" size={13} color={Colors.textLight} />
            <Text style={styles.sessionStatText}>{userMsgCount} questions</Text>
          </View>
          <View style={styles.sessionStat}>
            <Ionicons name="school-outline" size={13} color={Colors.textLight} />
            <Text style={styles.sessionStatText}>{assistantMsgCount} responses</Text>
          </View>
        </View>

        {/* Expand to see full conversation */}
        <TouchableOpacity style={styles.expandBtn} onPress={() => setExpanded((v) => !v)} activeOpacity={0.7}>
          <Text style={styles.expandBtnText}>{expanded ? 'Hide Conversation' : 'View Conversation'}</Text>
          <Ionicons name={expanded ? 'chevron-up' : 'chevron-down'} size={16} color={Colors.primary} />
        </TouchableOpacity>

        {/* Expanded: full conversation */}
        {expanded && (
          <View style={styles.conversationWrap}>
            {session.messages.map((msg) => (
              <View
                key={msg.id}
                style={[
                  styles.convBubble,
                  msg.role === 'user' ? styles.convBubbleUser : styles.convBubbleAssistant,
                ]}
              >
                <View style={styles.convBubbleHeader}>
                  <Ionicons
                    name={msg.role === 'user' ? 'person-circle-outline' : 'school-outline'}
                    size={14}
                    color={msg.role === 'user' ? Colors.primary : Colors.teal}
                  />
                  <Text style={styles.convBubbleRole}>
                    {msg.role === 'user' ? 'You' : 'Tutor'}
                  </Text>
                </View>
                {msg.imageUri && (
                  <Image source={{ uri: msg.imageUri }} style={styles.convBubbleImage} resizeMode="cover" />
                )}
                <Text style={styles.convBubbleText}>{msg.content}</Text>
              </View>
            ))}
          </View>
        )}

        {/* Delete */}
        <TouchableOpacity style={styles.deleteBtn} onPress={confirmDelete} activeOpacity={0.7}>
          <Ionicons name="trash-outline" size={15} color={Colors.secondary} />
          <Text style={styles.deleteBtnText}>Delete Session</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

// ─── Saved Screen ─────────────────────────────────────────────────────────────
export default function SavedScreen() {
  const insets = useSafeAreaInsets();
  const { savedItems, deleteItem, sessions, deleteSession } = useAppContext();
  const [activeTab, setActiveTab] = useState<TabKey>('problems');
  const [activeFilter, setActiveFilter] = useState('All');

  const filters = useMemo(() => {
    const topics = [...new Set(savedItems.map((i) => i.analysis.topic))].sort();
    return ['All', ...topics];
  }, [savedItems]);

  const filtered = useMemo(() => {
    if (activeFilter === 'All') return savedItems;
    return savedItems.filter((i) => i.analysis.topic === activeFilter);
  }, [savedItems, activeFilter]);

  const totalCount = savedItems.length + sessions.length;

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={[styles.header, { paddingTop: insets.top + 16 }]}>
        <View style={styles.headerRow}>
          <View>
            <Text style={styles.headerTitle}>Saved</Text>
            <Text style={styles.headerSub}>
              {totalCount} item{totalCount !== 1 ? 's' : ''} saved
            </Text>
          </View>
          {totalCount > 0 && (
            <View style={styles.countBadge}>
              <Text style={styles.countBadgeText}>{totalCount}</Text>
            </View>
          )}
        </View>

        {/* Tab switcher */}
        <View style={styles.tabRow}>
          <TouchableOpacity
            style={[styles.tabBtn, activeTab === 'problems' && styles.tabBtnActive]}
            onPress={() => setActiveTab('problems')}
            activeOpacity={0.7}
          >
            <Ionicons
              name="bookmark"
              size={15}
              color={activeTab === 'problems' ? Colors.primary : 'rgba(255,255,255,0.6)'}
            />
            <Text style={[styles.tabBtnText, activeTab === 'problems' && styles.tabBtnTextActive]}>
              Problems ({savedItems.length})
            </Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.tabBtn, activeTab === 'sessions' && styles.tabBtnActive]}
            onPress={() => setActiveTab('sessions')}
            activeOpacity={0.7}
          >
            <Ionicons
              name="chatbubbles"
              size={15}
              color={activeTab === 'sessions' ? Colors.primary : 'rgba(255,255,255,0.6)'}
            />
            <Text style={[styles.tabBtnText, activeTab === 'sessions' && styles.tabBtnTextActive]}>
              Sessions ({sessions.length})
            </Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* ── Problems Tab ── */}
      {activeTab === 'problems' && (
        <>
          {savedItems.length === 0 ? (
            <View style={styles.emptyContainer}>
              <View style={styles.emptyIconWrap}>
                <Ionicons name="bookmark-outline" size={48} color={Colors.textMuted} />
              </View>
              <Text style={styles.emptyTitle}>Nothing saved yet</Text>
              <Text style={styles.emptySub}>
                Scan a math problem on the Dashboard, get the AI analysis, then tap{' '}
                <Text style={{ fontWeight: '700', color: Colors.primary }}>"Save to Collection"</Text>
                {' '}to store it here.
              </Text>
            </View>
          ) : (
            <>
              {filters.length > 1 && (
                <View style={styles.filterWrap}>
                  <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.filterScroll}>
                    {filters.map((f) => (
                      <TouchableOpacity
                        key={f}
                        style={[styles.filterPill, activeFilter === f && styles.filterPillActive]}
                        onPress={() => setActiveFilter(f)}
                        activeOpacity={0.7}
                      >
                        <Text style={[styles.filterText, activeFilter === f && styles.filterTextActive]}>{f}</Text>
                      </TouchableOpacity>
                    ))}
                  </ScrollView>
                </View>
              )}

              <ScrollView style={styles.scroll} contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
                {filtered.length === 0 ? (
                  <View style={styles.emptyFilterState}>
                    <Text style={styles.emptyFilterText}>No {activeFilter} problems saved.</Text>
                  </View>
                ) : (
                  filtered.map((item) => (
                    <SavedCard key={item.id} item={item} onDelete={() => deleteItem(item.id)} />
                  ))
                )}
                <View style={{ height: 32 }} />
              </ScrollView>
            </>
          )}
        </>
      )}

      {/* ── Sessions Tab ── */}
      {activeTab === 'sessions' && (
        <>
          {sessions.length === 0 ? (
            <View style={styles.emptyContainer}>
              <View style={styles.emptyIconWrap}>
                <Ionicons name="chatbubbles-outline" size={48} color={Colors.textMuted} />
              </View>
              <Text style={styles.emptyTitle}>No sessions saved</Text>
              <Text style={styles.emptySub}>
                Start a tutoring session on the Dashboard and tap{' '}
                <Text style={{ fontWeight: '700', color: Colors.primary }}>"Save"</Text>
                {' '}to keep it for later.
              </Text>
            </View>
          ) : (
            <ScrollView style={styles.scroll} contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
              {sessions.map((session) => (
                <SessionCard
                  key={session.id}
                  session={session}
                  onDelete={() => deleteSession(session.id)}
                />
              ))}
              <View style={{ height: 32 }} />
            </ScrollView>
          )}
        </>
      )}
    </View>
  );
}

// ─── Styles ───────────────────────────────────────────────────────────────────
const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },

  header: {
    backgroundColor: Colors.primary,
    paddingHorizontal: 20,
    paddingBottom: 14,
    borderBottomLeftRadius: 24,
    borderBottomRightRadius: 24,
  },
  headerRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 },
  headerTitle: { fontSize: 26, fontWeight: '700', color: Colors.white, marginBottom: 2 },
  headerSub: { fontSize: 14, color: 'rgba(255,255,255,0.75)' },
  countBadge: {
    backgroundColor: 'rgba(255,255,255,0.25)', borderRadius: 20,
    paddingHorizontal: 14, paddingVertical: 6,
  },
  countBadgeText: { fontSize: 18, fontWeight: '700', color: Colors.white },

  // Tab switcher
  tabRow: { flexDirection: 'row', gap: 8 },
  tabBtn: {
    flex: 1, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 6,
    paddingVertical: 10, borderRadius: 14,
    backgroundColor: 'rgba(255,255,255,0.12)',
  },
  tabBtnActive: { backgroundColor: Colors.white },
  tabBtnText: { fontSize: 13, fontWeight: '600', color: 'rgba(255,255,255,0.7)' },
  tabBtnTextActive: { color: Colors.primary },

  // Empty state
  emptyContainer: {
    flex: 1, alignItems: 'center', justifyContent: 'center', padding: 40,
  },
  emptyIconWrap: {
    width: 90, height: 90, borderRadius: 24,
    backgroundColor: Colors.card, alignItems: 'center', justifyContent: 'center',
    marginBottom: 20,
    shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.06, shadowRadius: 8, elevation: 2,
  },
  emptyTitle: { fontSize: 20, fontWeight: '700', color: Colors.text, marginBottom: 12 },
  emptySub: { fontSize: 15, color: Colors.textLight, textAlign: 'center', lineHeight: 22 },

  // Filters
  filterWrap: {
    backgroundColor: Colors.white,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
    paddingVertical: 12,
  },
  filterScroll: { paddingHorizontal: 16, gap: 8 },
  filterPill: {
    paddingHorizontal: 16, paddingVertical: 7, borderRadius: 20,
    borderWidth: 1, borderColor: Colors.border, backgroundColor: Colors.white,
  },
  filterPillActive: { backgroundColor: Colors.primary, borderColor: Colors.primary },
  filterText: { fontSize: 13, fontWeight: '500', color: Colors.textLight },
  filterTextActive: { color: Colors.white, fontWeight: '700' },

  scroll: { flex: 1 },
  scrollContent: { padding: 16 },

  emptyFilterState: { padding: 32, alignItems: 'center' },
  emptyFilterText: { fontSize: 14, color: Colors.textMuted },

  // ── Problem Card ──
  card: {
    backgroundColor: Colors.card, borderRadius: 18, overflow: 'hidden', marginBottom: 16,
    shadowColor: '#000', shadowOffset: { width: 0, height: 3 }, shadowOpacity: 0.09, shadowRadius: 10, elevation: 3,
  },
  cardImage: { width: '100%', height: 180 },
  cardBody: { padding: 16 },
  cardTopRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 },
  badgeRow: { flexDirection: 'row', gap: 6 },
  badge: { paddingHorizontal: 9, paddingVertical: 4, borderRadius: 8 },
  badgeText: { fontSize: 11, fontWeight: '700' },
  dateText: { fontSize: 12, color: Colors.textMuted },

  problemText: { fontSize: 15, color: Colors.text, fontWeight: '500', lineHeight: 22, marginBottom: 12 },

  answerRow: { marginBottom: 12 },
  answerBox: {
    backgroundColor: Colors.green + '14', borderRadius: 12,
    padding: 14, borderWidth: 1, borderColor: Colors.green + '35',
    gap: 4,
  },
  answerLabel: { fontSize: 10, fontWeight: '700', color: Colors.green, letterSpacing: 1.2 },
  answerText: { fontSize: 20, fontWeight: '700', color: Colors.text },

  expandBtn: {
    flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 6,
    paddingVertical: 10, borderRadius: 10,
    backgroundColor: Colors.primaryLight,
    borderWidth: 1, borderColor: Colors.primary + '30',
    marginBottom: 12,
  },
  expandBtnText: { fontSize: 14, fontWeight: '600', color: Colors.primary },

  // Breakdown
  breakdown: {
    borderTopWidth: 1, borderTopColor: Colors.border,
    paddingTop: 16, marginBottom: 12,
  },
  breakdownTitle: { fontSize: 15, fontWeight: '700', color: Colors.text, marginBottom: 12 },
  stepRow: { flexDirection: 'row', gap: 12, marginBottom: 16 },
  stepBubble: {
    width: 28, height: 28, borderRadius: 14,
    backgroundColor: Colors.primary, alignItems: 'center', justifyContent: 'center', flexShrink: 0, marginTop: 2,
  },
  stepBubbleText: { fontSize: 12, fontWeight: '700', color: Colors.white },
  stepBody: { flex: 1, gap: 5 },
  stepTitle: { fontSize: 14, fontWeight: '700', color: Colors.text },
  stepExplanation: { fontSize: 13, color: Colors.textLight, lineHeight: 19 },
  mathBox: {
    backgroundColor: Colors.primaryLight, borderLeftWidth: 3, borderLeftColor: Colors.primary,
    borderRadius: 8, padding: 10, marginTop: 4,
  },
  mathText: { fontSize: 13, fontFamily: 'monospace', color: Colors.primaryDark, letterSpacing: 0.3 },
  conceptsSection: { marginBottom: 12, gap: 8 },
  conceptsHeading: { fontSize: 13, fontWeight: '700', color: Colors.text },
  conceptsPills: { flexDirection: 'row', flexWrap: 'wrap', gap: 6 },
  pill: {
    backgroundColor: Colors.primaryLight, borderRadius: 20,
    paddingHorizontal: 11, paddingVertical: 5,
    borderWidth: 1, borderColor: Colors.primary + '30',
  },
  pillText: { fontSize: 12, fontWeight: '600', color: Colors.primary },
  tipBox: {
    flexDirection: 'row', gap: 8, padding: 12,
    backgroundColor: Colors.yellow + '18', borderRadius: 10,
    borderWidth: 1, borderColor: Colors.yellow + '40', marginBottom: 12,
  },
  tipText: { flex: 1, fontSize: 13, color: Colors.text, lineHeight: 19 },

  // Delete
  deleteBtn: {
    flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 6,
    paddingVertical: 10, borderRadius: 10,
    backgroundColor: Colors.secondary + '12',
    borderWidth: 1, borderColor: Colors.secondary + '30',
  },
  deleteBtnText: { fontSize: 13, fontWeight: '600', color: Colors.secondary },

  // ── Session Card ──
  sessionHeaderBar: {
    flexDirection: 'row', alignItems: 'center', gap: 10,
    padding: 14, borderBottomWidth: 1, borderBottomColor: Colors.border,
    backgroundColor: Colors.primaryLight,
  },
  sessionHeaderIcon: {
    width: 36, height: 36, borderRadius: 10,
    backgroundColor: Colors.white, alignItems: 'center', justifyContent: 'center',
  },
  sessionHeaderInfo: { flex: 1 },
  sessionHeaderTitle: { fontSize: 15, fontWeight: '700', color: Colors.text },
  sessionHeaderDate: { fontSize: 12, color: Colors.textLight, marginTop: 1 },

  sessionPreviewText: {
    fontSize: 14, color: Colors.textLight, lineHeight: 20, marginBottom: 12,
  },

  sessionStatsRow: {
    flexDirection: 'row', gap: 16, marginBottom: 12,
    paddingVertical: 10, paddingHorizontal: 12,
    backgroundColor: Colors.background, borderRadius: 10,
  },
  sessionStat: { flexDirection: 'row', alignItems: 'center', gap: 5 },
  sessionStatText: { fontSize: 12, color: Colors.textLight, fontWeight: '500' },

  // Conversation (expanded)
  conversationWrap: {
    borderTopWidth: 1, borderTopColor: Colors.border,
    paddingTop: 14, marginBottom: 12, gap: 12,
  },
  convBubble: {
    borderRadius: 14, padding: 12,
  },
  convBubbleUser: {
    backgroundColor: Colors.primary + '08',
    borderLeftWidth: 3, borderLeftColor: Colors.primary,
  },
  convBubbleAssistant: {
    backgroundColor: Colors.teal + '08',
    borderLeftWidth: 3, borderLeftColor: Colors.teal,
  },
  convBubbleHeader: {
    flexDirection: 'row', alignItems: 'center', gap: 5, marginBottom: 6,
  },
  convBubbleRole: { fontSize: 12, fontWeight: '700', color: Colors.textLight },
  convBubbleImage: {
    width: '100%', height: 120, borderRadius: 8, marginBottom: 8,
  },
  convBubbleText: { fontSize: 14, color: Colors.text, lineHeight: 20 },
});
