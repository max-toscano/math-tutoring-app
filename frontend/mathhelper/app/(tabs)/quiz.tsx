import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Colors } from '../../constants/Colors';

const QUIZ_CATEGORIES = [
  {
    id: '1',
    name: 'Algebra',
    emoji: '📐',
    questions: 20,
    bestScore: '18/20',
    difficulty: 'Medium',
    color: Colors.primary,
    bgColor: Colors.primaryLight,
    lastAttempt: '2 days ago',
  },
  {
    id: '2',
    name: 'Geometry',
    emoji: '📏',
    questions: 15,
    bestScore: '11/15',
    difficulty: 'Medium',
    color: Colors.teal,
    bgColor: '#E8F8F7',
    lastAttempt: '4 days ago',
  },
  {
    id: '3',
    name: 'Trigonometry',
    emoji: '🔺',
    questions: 12,
    bestScore: '8/12',
    difficulty: 'Hard',
    color: Colors.orange,
    bgColor: '#FFF4E6',
    lastAttempt: '1 week ago',
  },
  {
    id: '4',
    name: 'Calculus',
    emoji: '∫',
    questions: 18,
    bestScore: '10/18',
    difficulty: 'Hard',
    color: Colors.secondary,
    bgColor: '#FFF0F0',
    lastAttempt: '1 week ago',
  },
  {
    id: '5',
    name: 'Statistics',
    emoji: '📊',
    questions: 10,
    bestScore: '9/10',
    difficulty: 'Easy',
    color: Colors.green,
    bgColor: '#EAFAF1',
    lastAttempt: '3 days ago',
  },
];

const RECENT_RESULTS = [
  {
    id: '1',
    topic: 'Algebra',
    score: 8,
    total: 10,
    date: 'Today',
    timeSpent: '8 min',
    color: Colors.primary,
    stars: 4,
  },
  {
    id: '2',
    topic: 'Statistics',
    score: 9,
    total: 10,
    date: 'Yesterday',
    timeSpent: '6 min',
    color: Colors.green,
    stars: 5,
  },
  {
    id: '3',
    topic: 'Geometry',
    score: 6,
    total: 10,
    date: '3 days ago',
    timeSpent: '12 min',
    color: Colors.teal,
    stars: 3,
  },
];

const DIFFICULTY_COLORS: Record<string, string> = {
  Easy: Colors.green,
  Medium: Colors.orange,
  Hard: Colors.secondary,
};

function StarRating({ stars }: { stars: number }) {
  return (
    <View style={{ flexDirection: 'row', gap: 2 }}>
      {[1, 2, 3, 4, 5].map((i) => (
        <Ionicons
          key={i}
          name={i <= stars ? 'star' : 'star-outline'}
          size={13}
          color={i <= stars ? Colors.yellow : Colors.border}
        />
      ))}
    </View>
  );
}

export default function QuizScreen() {
  const insets = useSafeAreaInsets();

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={[styles.header, { paddingTop: insets.top + 16 }]}>
        <View style={styles.headerRow}>
          <View>
            <Text style={styles.headerTitle}>Quiz</Text>
            <Text style={styles.headerSub}>Test your knowledge</Text>
          </View>
          <TouchableOpacity style={styles.historyBtn}>
            <Ionicons name="time-outline" size={20} color={Colors.white} />
          </TouchableOpacity>
        </View>
      </View>

      <ScrollView
        style={styles.scroll}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* Daily Challenge */}
        <View style={styles.section}>
          <TouchableOpacity style={styles.dailyChallenge} activeOpacity={0.85}>
            <View style={styles.dailyChallengeLeft}>
              <View style={styles.dailyBadge}>
                <Ionicons name="trophy" size={13} color={Colors.yellow} />
                <Text style={styles.dailyBadgeText}>DAILY CHALLENGE</Text>
              </View>
              <Text style={styles.dailyTitle}>Mixed Review</Text>
              <Text style={styles.dailySub}>5 questions across all topics</Text>
              <View style={styles.dailyMeta}>
                <View style={styles.dailyMetaItem}>
                  <Ionicons name="time-outline" size={14} color="rgba(255,255,255,0.8)" />
                  <Text style={styles.dailyMetaText}>~10 min</Text>
                </View>
                <View style={styles.dailyMetaItem}>
                  <Ionicons name="flash-outline" size={14} color="rgba(255,255,255,0.8)" />
                  <Text style={styles.dailyMetaText}>+50 XP</Text>
                </View>
              </View>
              <TouchableOpacity style={styles.startChallengeBtn}>
                <Text style={styles.startChallengeBtnText}>Start Challenge</Text>
                <Ionicons name="arrow-forward" size={16} color={Colors.orange} />
              </TouchableOpacity>
            </View>
            <View style={styles.trophyWrap}>
              <Text style={styles.trophyEmoji}>🏆</Text>
            </View>
          </TouchableOpacity>
        </View>

        {/* XP Progress */}
        <View style={styles.section}>
          <View style={styles.xpCard}>
            <View style={styles.xpHeader}>
              <View>
                <Text style={styles.xpTitle}>Daily XP Progress</Text>
                <Text style={styles.xpSub}>320 / 500 XP earned today</Text>
              </View>
              <View style={styles.xpBadge}>
                <Text style={styles.xpBadgeText}>Lvl 12</Text>
              </View>
            </View>
            <View style={styles.xpTrack}>
              <View style={[styles.xpFill, { width: '64%' }]} />
            </View>
          </View>
        </View>

        {/* Recent Results */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Recent Results</Text>
            <TouchableOpacity>
              <Text style={styles.seeAll}>View all</Text>
            </TouchableOpacity>
          </View>
          {RECENT_RESULTS.map((result) => {
            const pct = Math.round((result.score / result.total) * 100);
            return (
              <View key={result.id} style={styles.resultCard}>
                <View style={[styles.resultAccent, { backgroundColor: result.color }]} />
                <View style={styles.resultInfo}>
                  <View style={styles.resultTop}>
                    <Text style={styles.resultTopic}>{result.topic}</Text>
                    <View style={styles.resultScoreBadge}>
                      <Text style={styles.resultScore}>
                        {result.score}/{result.total}
                      </Text>
                    </View>
                  </View>
                  <StarRating stars={result.stars} />
                  <View style={styles.resultMeta}>
                    <Text style={styles.resultMetaText}>{result.date}</Text>
                    <Text style={styles.resultMetaDot}>·</Text>
                    <Text style={styles.resultMetaText}>{result.timeSpent}</Text>
                    <Text style={styles.resultMetaDot}>·</Text>
                    <Text style={[styles.resultPct, { color: pct >= 80 ? Colors.green : pct >= 60 ? Colors.orange : Colors.secondary }]}>
                      {pct}%
                    </Text>
                  </View>
                </View>
              </View>
            );
          })}
        </View>

        {/* Practice by Topic */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Practice by Topic</Text>
          {QUIZ_CATEGORIES.map((cat) => (
            <TouchableOpacity key={cat.id} style={styles.quizCatCard} activeOpacity={0.75}>
              <View style={[styles.catEmoji, { backgroundColor: cat.bgColor }]}>
                <Text style={styles.catEmojiText}>{cat.emoji}</Text>
              </View>
              <View style={styles.catInfo}>
                <Text style={styles.catName}>{cat.name}</Text>
                <View style={styles.catMeta}>
                  <Text style={styles.catQuestions}>{cat.questions} questions</Text>
                  <Text style={styles.catDot}>·</Text>
                  <Text style={styles.catBest}>Best: {cat.bestScore}</Text>
                </View>
              </View>
              <View style={styles.catRight}>
                <View
                  style={[
                    styles.diffBadge,
                    { backgroundColor: DIFFICULTY_COLORS[cat.difficulty] + '20' },
                  ]}
                >
                  <Text
                    style={[
                      styles.diffText,
                      { color: DIFFICULTY_COLORS[cat.difficulty] },
                    ]}
                  >
                    {cat.difficulty}
                  </Text>
                </View>
                <Ionicons name="chevron-forward" size={18} color={Colors.textMuted} />
              </View>
            </TouchableOpacity>
          ))}
        </View>

        {/* Quick Fire Round */}
        <View style={styles.section}>
          <TouchableOpacity style={styles.quickFireCard} activeOpacity={0.85}>
            <View style={styles.quickFireLeft}>
              <Text style={styles.quickFireTitle}>⚡ Quick Fire Round</Text>
              <Text style={styles.quickFireSub}>
                60 seconds · Answer as many as you can
              </Text>
            </View>
            <View style={styles.quickFireBtn}>
              <Ionicons name="flash" size={18} color={Colors.white} />
            </View>
          </TouchableOpacity>
        </View>
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
  headerRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
  },
  headerTitle: {
    fontSize: 26,
    fontWeight: '700',
    color: Colors.white,
    marginBottom: 2,
  },
  headerSub: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.7)',
  },
  historyBtn: {
    width: 40,
    height: 40,
    borderRadius: 12,
    backgroundColor: 'rgba(255,255,255,0.2)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  scroll: {
    flex: 1,
  },
  scrollContent: {
    padding: 16,
    paddingBottom: 32,
  },
  section: {
    marginBottom: 24,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 17,
    fontWeight: '700',
    color: Colors.text,
    marginBottom: 12,
  },
  seeAll: {
    fontSize: 14,
    color: Colors.primary,
    fontWeight: '600',
    marginBottom: 12,
  },
  dailyChallenge: {
    backgroundColor: Colors.orange,
    borderRadius: 20,
    padding: 20,
    flexDirection: 'row',
    alignItems: 'center',
    overflow: 'hidden',
  },
  dailyChallengeLeft: {
    flex: 1,
  },
  dailyBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 5,
    backgroundColor: 'rgba(255,255,255,0.2)',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 8,
    alignSelf: 'flex-start',
    marginBottom: 10,
  },
  dailyBadgeText: {
    color: Colors.yellow,
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 1,
  },
  dailyTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: Colors.white,
    marginBottom: 4,
  },
  dailySub: {
    fontSize: 13,
    color: 'rgba(255,255,255,0.8)',
    marginBottom: 12,
  },
  dailyMeta: {
    flexDirection: 'row',
    gap: 16,
    marginBottom: 16,
  },
  dailyMetaItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  dailyMetaText: {
    fontSize: 12,
    color: 'rgba(255,255,255,0.85)',
    fontWeight: '500',
  },
  startChallengeBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: Colors.white,
    borderRadius: 10,
    paddingHorizontal: 16,
    paddingVertical: 9,
    alignSelf: 'flex-start',
  },
  startChallengeBtnText: {
    fontSize: 14,
    fontWeight: '700',
    color: Colors.orange,
  },
  trophyWrap: {
    marginLeft: 8,
  },
  trophyEmoji: {
    fontSize: 60,
  },
  xpCard: {
    backgroundColor: Colors.card,
    borderRadius: 16,
    padding: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 8,
    elevation: 2,
  },
  xpHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 14,
  },
  xpTitle: {
    fontSize: 15,
    fontWeight: '600',
    color: Colors.text,
    marginBottom: 2,
  },
  xpSub: {
    fontSize: 12,
    color: Colors.textLight,
  },
  xpBadge: {
    backgroundColor: Colors.primaryLight,
    borderRadius: 10,
    paddingHorizontal: 10,
    paddingVertical: 5,
  },
  xpBadgeText: {
    fontSize: 13,
    fontWeight: '700',
    color: Colors.primary,
  },
  xpTrack: {
    height: 10,
    backgroundColor: Colors.border,
    borderRadius: 5,
    overflow: 'hidden',
  },
  xpFill: {
    height: '100%',
    backgroundColor: Colors.primary,
    borderRadius: 5,
  },
  resultCard: {
    backgroundColor: Colors.card,
    borderRadius: 14,
    flexDirection: 'row',
    overflow: 'hidden',
    marginBottom: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 1,
  },
  resultAccent: {
    width: 4,
  },
  resultInfo: {
    flex: 1,
    padding: 14,
    gap: 6,
  },
  resultTop: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  resultTopic: {
    fontSize: 15,
    fontWeight: '700',
    color: Colors.text,
  },
  resultScoreBadge: {
    backgroundColor: Colors.background,
    borderRadius: 8,
    paddingHorizontal: 10,
    paddingVertical: 4,
  },
  resultScore: {
    fontSize: 14,
    fontWeight: '700',
    color: Colors.text,
  },
  resultMeta: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  resultMetaText: {
    fontSize: 12,
    color: Colors.textMuted,
  },
  resultMetaDot: {
    fontSize: 12,
    color: Colors.border,
  },
  resultPct: {
    fontSize: 12,
    fontWeight: '700',
  },
  quizCatCard: {
    backgroundColor: Colors.card,
    borderRadius: 14,
    padding: 14,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 14,
    marginBottom: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 1,
  },
  catEmoji: {
    width: 46,
    height: 46,
    borderRadius: 13,
    alignItems: 'center',
    justifyContent: 'center',
  },
  catEmojiText: {
    fontSize: 22,
  },
  catInfo: {
    flex: 1,
    gap: 5,
  },
  catName: {
    fontSize: 15,
    fontWeight: '600',
    color: Colors.text,
  },
  catMeta: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  catQuestions: {
    fontSize: 12,
    color: Colors.textLight,
  },
  catDot: {
    fontSize: 12,
    color: Colors.textMuted,
  },
  catBest: {
    fontSize: 12,
    color: Colors.textLight,
  },
  catRight: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  diffBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
  },
  diffText: {
    fontSize: 11,
    fontWeight: '700',
  },
  quickFireCard: {
    backgroundColor: Colors.primary,
    borderRadius: 16,
    padding: 18,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  quickFireLeft: {
    flex: 1,
    gap: 4,
  },
  quickFireTitle: {
    fontSize: 17,
    fontWeight: '700',
    color: Colors.white,
  },
  quickFireSub: {
    fontSize: 13,
    color: 'rgba(255,255,255,0.75)',
  },
  quickFireBtn: {
    width: 46,
    height: 46,
    borderRadius: 14,
    backgroundColor: 'rgba(255,255,255,0.2)',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
