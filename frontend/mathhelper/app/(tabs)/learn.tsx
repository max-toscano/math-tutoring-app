import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Dimensions,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Colors } from '../../constants/Colors';

const { width } = Dimensions.get('window');
const CARD_WIDTH = (width - 48) / 2;

const TOPICS = [
  {
    id: '1',
    name: 'Algebra',
    emoji: '📐',
    lessons: 24,
    completed: 16,
    color: Colors.primary,
    bgColor: Colors.primaryLight,
    description: 'Equations, functions & polynomials',
  },
  {
    id: '2',
    name: 'Geometry',
    emoji: '📏',
    lessons: 18,
    completed: 7,
    color: Colors.teal,
    bgColor: '#E8F8F7',
    description: 'Shapes, angles & theorems',
  },
  {
    id: '3',
    name: 'Trigonometry',
    emoji: '🔺',
    lessons: 15,
    completed: 3,
    color: Colors.orange,
    bgColor: '#FFF4E6',
    description: 'Sin, cos, tan & identities',
  },
  {
    id: '4',
    name: 'Calculus',
    emoji: '∫',
    lessons: 30,
    completed: 4,
    color: Colors.secondary,
    bgColor: '#FFF0F0',
    description: 'Derivatives, integrals & limits',
  },
  {
    id: '5',
    name: 'Statistics',
    emoji: '📊',
    lessons: 12,
    completed: 7,
    color: Colors.green,
    bgColor: '#EAFAF1',
    description: 'Probability, data & distributions',
  },
  {
    id: '6',
    name: 'Number Theory',
    emoji: '🔢',
    lessons: 8,
    completed: 0,
    color: '#9B59B6',
    bgColor: '#F5EEF8',
    description: 'Primes, divisibility & proofs',
  },
];

const FEATURED_LESSON = {
  topic: 'Algebra',
  title: 'Mastering Quadratic Equations',
  duration: '12 min',
  parts: 4,
  color: Colors.primary,
  bgColor: Colors.primaryLight,
  emoji: '📐',
};

const RECENT_LESSONS = [
  {
    id: '1',
    title: 'Graphing Linear Equations',
    topic: 'Algebra',
    duration: '8 min',
    completed: true,
    color: Colors.primary,
  },
  {
    id: '2',
    title: 'The Unit Circle',
    topic: 'Trigonometry',
    duration: '15 min',
    completed: true,
    color: Colors.orange,
  },
  {
    id: '3',
    title: 'Introduction to Derivatives',
    topic: 'Calculus',
    duration: '20 min',
    completed: false,
    color: Colors.secondary,
  },
];

export default function LearnScreen() {
  const insets = useSafeAreaInsets();

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={[styles.header, { paddingTop: insets.top + 16 }]}>
        <Text style={styles.headerTitle}>Learn</Text>
        <Text style={styles.headerSub}>Build your math skills step by step</Text>

        {/* Search Bar */}
        <TouchableOpacity style={styles.searchBar} activeOpacity={0.8}>
          <Ionicons name="search-outline" size={18} color={Colors.textMuted} />
          <Text style={styles.searchPlaceholder}>Search topics and lessons...</Text>
          <Ionicons name="mic-outline" size={18} color={Colors.textMuted} />
        </TouchableOpacity>
      </View>

      <ScrollView
        style={styles.scroll}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* Featured Lesson */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Featured Lesson</Text>
          <TouchableOpacity
            style={[styles.featuredCard, { backgroundColor: FEATURED_LESSON.color }]}
            activeOpacity={0.85}
          >
            <View style={styles.featuredContent}>
              <View>
                <View style={styles.featuredBadge}>
                  <Ionicons name="star" size={11} color={Colors.yellow} />
                  <Text style={styles.featuredBadgeText}>FEATURED</Text>
                </View>
                <Text style={styles.featuredTitle}>{FEATURED_LESSON.title}</Text>
                <Text style={styles.featuredTopic}>{FEATURED_LESSON.topic}</Text>
                <View style={styles.featuredMeta}>
                  <View style={styles.featuredMetaItem}>
                    <Ionicons name="time-outline" size={13} color="rgba(255,255,255,0.8)" />
                    <Text style={styles.featuredMetaText}>{FEATURED_LESSON.duration}</Text>
                  </View>
                  <View style={styles.featuredMetaItem}>
                    <Ionicons name="layers-outline" size={13} color="rgba(255,255,255,0.8)" />
                    <Text style={styles.featuredMetaText}>{FEATURED_LESSON.parts} parts</Text>
                  </View>
                </View>
                <TouchableOpacity style={styles.startBtn}>
                  <Text style={styles.startBtnText}>Start Lesson</Text>
                  <Ionicons name="arrow-forward" size={16} color={Colors.primary} />
                </TouchableOpacity>
              </View>
              <Text style={styles.featuredEmoji}>{FEATURED_LESSON.emoji}</Text>
            </View>
          </TouchableOpacity>
        </View>

        {/* Continue Section */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Continue Learning</Text>
            <TouchableOpacity>
              <Text style={styles.seeAll}>See all</Text>
            </TouchableOpacity>
          </View>
          {RECENT_LESSONS.map((lesson) => (
            <TouchableOpacity key={lesson.id} style={styles.lessonCard} activeOpacity={0.75}>
              <View style={[styles.lessonDot, { backgroundColor: lesson.color }]} />
              <View style={styles.lessonInfo}>
                <Text style={styles.lessonTitle}>{lesson.title}</Text>
                <View style={styles.lessonMeta}>
                  <Text style={[styles.lessonTopic, { color: lesson.color }]}>{lesson.topic}</Text>
                  <Text style={styles.lessonDuration}>· {lesson.duration}</Text>
                </View>
              </View>
              <View style={styles.lessonRight}>
                {lesson.completed ? (
                  <View style={styles.completedBadge}>
                    <Ionicons name="checkmark" size={14} color={Colors.green} />
                  </View>
                ) : (
                  <View style={styles.resumeBtn}>
                    <Text style={styles.resumeBtnText}>Resume</Text>
                  </View>
                )}
              </View>
            </TouchableOpacity>
          ))}
        </View>

        {/* All Topics Grid */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>All Topics</Text>
          <View style={styles.topicGrid}>
            {TOPICS.map((topic) => {
              const pct = Math.round((topic.completed / topic.lessons) * 100);
              return (
                <TouchableOpacity
                  key={topic.id}
                  style={[styles.topicCard, { borderTopColor: topic.color, borderTopWidth: 3 }]}
                  activeOpacity={0.8}
                >
                  <View style={[styles.topicEmojiWrap, { backgroundColor: topic.bgColor }]}>
                    <Text style={styles.topicEmoji}>{topic.emoji}</Text>
                  </View>
                  <Text style={styles.topicName}>{topic.name}</Text>
                  <Text style={styles.topicDesc} numberOfLines={2}>{topic.description}</Text>
                  <Text style={styles.lessonCount}>{topic.lessons} lessons</Text>
                  <View style={styles.progressRow}>
                    <View style={styles.progressTrack}>
                      <View
                        style={[
                          styles.progressFill,
                          { width: `${pct}%`, backgroundColor: topic.color },
                        ]}
                      />
                    </View>
                    <Text style={[styles.progressPct, { color: topic.color }]}>{pct}%</Text>
                  </View>
                </TouchableOpacity>
              );
            })}
          </View>
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
  headerTitle: {
    fontSize: 26,
    fontWeight: '700',
    color: Colors.white,
    marginBottom: 4,
  },
  headerSub: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.7)',
    marginBottom: 16,
  },
  searchBar: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Colors.white,
    borderRadius: 12,
    paddingHorizontal: 14,
    paddingVertical: 12,
    gap: 10,
  },
  searchPlaceholder: {
    flex: 1,
    fontSize: 14,
    color: Colors.textMuted,
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
  featuredCard: {
    borderRadius: 20,
    padding: 20,
    overflow: 'hidden',
  },
  featuredContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  featuredBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    backgroundColor: 'rgba(255,255,255,0.2)',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
    alignSelf: 'flex-start',
    marginBottom: 10,
  },
  featuredBadgeText: {
    color: Colors.yellow,
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 1,
  },
  featuredTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: Colors.white,
    marginBottom: 4,
    maxWidth: 200,
  },
  featuredTopic: {
    fontSize: 13,
    color: 'rgba(255,255,255,0.75)',
    marginBottom: 12,
  },
  featuredMeta: {
    flexDirection: 'row',
    gap: 14,
    marginBottom: 16,
  },
  featuredMetaItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  featuredMetaText: {
    fontSize: 12,
    color: 'rgba(255,255,255,0.8)',
  },
  startBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: Colors.white,
    borderRadius: 10,
    paddingHorizontal: 16,
    paddingVertical: 9,
    alignSelf: 'flex-start',
  },
  startBtnText: {
    fontSize: 14,
    fontWeight: '700',
    color: Colors.primary,
  },
  featuredEmoji: {
    fontSize: 64,
    opacity: 0.85,
  },
  lessonCard: {
    backgroundColor: Colors.card,
    borderRadius: 14,
    padding: 14,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    marginBottom: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 1,
  },
  lessonDot: {
    width: 10,
    height: 10,
    borderRadius: 5,
  },
  lessonInfo: {
    flex: 1,
    gap: 4,
  },
  lessonTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: Colors.text,
  },
  lessonMeta: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  lessonTopic: {
    fontSize: 12,
    fontWeight: '600',
  },
  lessonDuration: {
    fontSize: 12,
    color: Colors.textMuted,
  },
  lessonRight: {},
  completedBadge: {
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: Colors.green + '20',
    alignItems: 'center',
    justifyContent: 'center',
  },
  resumeBtn: {
    backgroundColor: Colors.primaryLight,
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 6,
  },
  resumeBtnText: {
    fontSize: 12,
    fontWeight: '600',
    color: Colors.primary,
  },
  topicGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  topicCard: {
    width: CARD_WIDTH,
    backgroundColor: Colors.card,
    borderRadius: 16,
    padding: 14,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.07,
    shadowRadius: 8,
    elevation: 2,
    overflow: 'hidden',
  },
  topicEmojiWrap: {
    width: 48,
    height: 48,
    borderRadius: 14,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 10,
  },
  topicEmoji: {
    fontSize: 24,
  },
  topicName: {
    fontSize: 15,
    fontWeight: '700',
    color: Colors.text,
    marginBottom: 4,
  },
  topicDesc: {
    fontSize: 12,
    color: Colors.textLight,
    lineHeight: 16,
    marginBottom: 10,
  },
  lessonCount: {
    fontSize: 11,
    color: Colors.textMuted,
    marginBottom: 6,
    fontWeight: '500',
  },
  progressRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  progressTrack: {
    flex: 1,
    height: 5,
    backgroundColor: Colors.border,
    borderRadius: 3,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    borderRadius: 3,
  },
  progressPct: {
    fontSize: 11,
    fontWeight: '700',
    width: 28,
    textAlign: 'right',
  },
});
