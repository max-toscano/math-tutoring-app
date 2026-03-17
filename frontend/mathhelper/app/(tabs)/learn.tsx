import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Dimensions,
  Animated,
} from 'react-native';
import { useEffect, useState, useCallback, useRef } from 'react';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { useFocusEffect } from '@react-navigation/native';
import { Colors } from '../../constants/Colors';
import {
  ALL_SUBJECTS,
  getSubject,
  getTopic,
  getChapter,
  getChapterTopic,
  hasChapters,
  getTotalTopicCount,
} from '../../constants/curriculums';
import { getAllProgress, type TopicProgress } from '../../services/learn';

const { width } = Dimensions.get('window');
const CARD_WIDTH = (width - 48) / 2;

function SkeletonCard() {
  const opacity = useRef(new Animated.Value(0.3)).current;
  useEffect(() => {
    const anim = Animated.loop(
      Animated.sequence([
        Animated.timing(opacity, { toValue: 0.7, duration: 800, useNativeDriver: true }),
        Animated.timing(opacity, { toValue: 0.3, duration: 800, useNativeDriver: true }),
      ]),
    );
    anim.start();
    return () => anim.stop();
  }, []);
  return (
    <Animated.View style={[styles.topicCard, { borderTopWidth: 3, borderTopColor: Colors.border, opacity }]}>
      <View style={[styles.topicEmojiWrap, { backgroundColor: Colors.border }]} />
      <View style={{ width: '60%', height: 14, backgroundColor: Colors.border, borderRadius: 4, marginBottom: 6 }} />
      <View style={{ width: '80%', height: 10, backgroundColor: Colors.border, borderRadius: 4, marginBottom: 10 }} />
      <View style={{ width: '40%', height: 10, backgroundColor: Colors.border, borderRadius: 4, marginBottom: 6 }} />
      <View style={styles.progressRow}>
        <View style={styles.progressTrack} />
      </View>
    </Animated.View>
  );
}

export default function LearnScreen() {
  const insets = useSafeAreaInsets();
  const router = useRouter();

  const [progress, setProgress] = useState<TopicProgress[]>([]);
  const [loadingProgress, setLoadingProgress] = useState(true);
  const [progressError, setProgressError] = useState(false);

  // Reload progress every time the tab is focused
  useFocusEffect(
    useCallback(() => {
      loadProgress();
    }, []),
  );

  async function loadProgress() {
    setProgressError(false);
    try {
      const data = await getAllProgress();
      setProgress(data);
    } catch {
      setProgressError(true);
    } finally {
      setLoadingProgress(false);
    }
  }

  // Build a lookup: "subject:chapter:topic" -> TopicProgress
  // For flat subjects chapter is "_default"
  const progressMap = new Map<string, TopicProgress>();
  for (const p of progress) {
    const chapterKey = p.chapter ?? '_default';
    progressMap.set(`${p.subject}:${chapterKey}:${p.topic}`, p);
  }

  // Continue Learning: in_progress topics, sorted by last_accessed (already sorted by backend)
  const recentTopics = progress
    .filter((p) => p.status === 'in_progress')
    .slice(0, 3);

  // Per-subject completion stats (handles both flat and chaptered)
  function getSubjectStats(subjectSlug: string) {
    const subject = getSubject(subjectSlug);
    if (!subject) return { completed: 0, total: 0 };
    const total = getTotalTopicCount(subject);
    let completed = 0;

    if (hasChapters(subject)) {
      for (const ch of subject.chapters!) {
        for (const t of ch.topics) {
          if (progressMap.get(`${subjectSlug}:${ch.slug}:${t.slug}`)?.status === 'completed') {
            completed++;
          }
        }
      }
    } else {
      for (const t of subject.topics) {
        if (progressMap.get(`${subjectSlug}:_default:${t.slug}`)?.status === 'completed') {
          completed++;
        }
      }
    }
    return { completed, total };
  }

  // Featured lesson: most recent in-progress topic, or first untouched topic
  const featuredTopic = (() => {
    // Prefer most recent in-progress
    if (recentTopics.length > 0) {
      const p = recentTopics[0];
      const s = getSubject(p.subject);
      if (!s) return null;

      if (p.chapter && hasChapters(s)) {
        const ch = getChapter(p.subject, p.chapter);
        const t = getChapterTopic(p.subject, p.chapter, p.topic);
        if (ch && t) return { subject: s, chapter: ch, topic: t, isResume: true };
      } else {
        const t = getTopic(p.subject, p.topic);
        if (t) return { subject: s, chapter: undefined, topic: t, isResume: true };
      }
    }
    // Otherwise, first untouched topic across all subjects
    for (const s of ALL_SUBJECTS) {
      if (hasChapters(s)) {
        for (const ch of s.chapters!) {
          for (const t of ch.topics) {
            if (!progressMap.has(`${s.slug}:${ch.slug}:${t.slug}`)) {
              return { subject: s, chapter: ch, topic: t, isResume: false };
            }
          }
        }
      } else {
        for (const t of s.topics) {
          if (!progressMap.has(`${s.slug}:_default:${t.slug}`)) {
            return { subject: s, chapter: undefined, topic: t, isResume: false };
          }
        }
      }
    }
    return null;
  })();

  // Build lesson nav params for featured/continue cards
  function getLessonParams(p: { subject: string; chapter?: string | null; topic: string }) {
    const params: Record<string, string> = { subject: p.subject, topic: p.topic };
    if (p.chapter) params.chapter = p.chapter;
    return params;
  }

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
        {featuredTopic && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Featured Lesson</Text>
            <TouchableOpacity
              style={[styles.featuredCard, { backgroundColor: featuredTopic.subject.color }]}
              activeOpacity={0.85}
              onPress={() =>
                router.push({
                  pathname: '/learn/lesson',
                  params: getLessonParams({
                    subject: featuredTopic.subject.slug,
                    chapter: featuredTopic.chapter?.slug,
                    topic: featuredTopic.topic.slug,
                  }),
                })
              }
            >
              <View style={styles.featuredContent}>
                <View style={{ flex: 1 }}>
                  <View style={styles.featuredBadge}>
                    <Ionicons name="star" size={11} color={Colors.yellow} />
                    <Text style={styles.featuredBadgeText}>
                      {featuredTopic.isResume ? 'CONTINUE' : 'START'}
                    </Text>
                  </View>
                  <Text style={styles.featuredTitle}>{featuredTopic.topic.name}</Text>
                  <Text style={styles.featuredSubject}>
                    {featuredTopic.chapter
                      ? `${featuredTopic.chapter.name} · ${featuredTopic.subject.name}`
                      : featuredTopic.subject.name}
                  </Text>
                  <TouchableOpacity style={styles.startBtn}>
                    <Text style={[styles.startBtnText, { color: featuredTopic.subject.color }]}>
                      {featuredTopic.isResume ? 'Resume Lesson' : 'Start Lesson'}
                    </Text>
                    <Ionicons name="arrow-forward" size={16} color={featuredTopic.subject.color} />
                  </TouchableOpacity>
                </View>
                <Text style={styles.featuredEmoji}>{featuredTopic.subject.emoji}</Text>
              </View>
            </TouchableOpacity>
          </View>
        )}

        {/* Progress error */}
        {progressError && (
          <View style={styles.errorBanner}>
            <Ionicons name="cloud-offline-outline" size={18} color={Colors.secondary} />
            <Text style={styles.errorBannerText}>Couldn't load progress</Text>
            <TouchableOpacity onPress={loadProgress}>
              <Text style={styles.errorRetry}>Retry</Text>
            </TouchableOpacity>
          </View>
        )}

        {/* Continue Learning */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Continue Learning</Text>
          </View>
          {loadingProgress ? (
            <View style={styles.emptyState}>
              <View style={{ width: '100%', height: 12, backgroundColor: Colors.border, borderRadius: 4, marginBottom: 8 }} />
              <View style={{ width: '70%', height: 12, backgroundColor: Colors.border, borderRadius: 4 }} />
            </View>
          ) : recentTopics.length === 0 ? (
            <View style={styles.emptyState}>
              <Ionicons name="book-outline" size={32} color={Colors.textMuted} />
              <Text style={styles.emptyStateText}>Start a topic below to begin learning</Text>
            </View>
          ) : (
            recentTopics.map((p) => {
              const subject = getSubject(p.subject);
              if (!subject) return null;

              // Resolve topic name for both flat and chaptered subjects
              let topicName = p.topic;
              if (p.chapter && hasChapters(subject)) {
                const t = getChapterTopic(p.subject, p.chapter, p.topic);
                topicName = t?.name ?? p.topic;
              } else {
                const t = getTopic(p.subject, p.topic);
                topicName = t?.name ?? p.topic;
              }

              const chapterName = p.chapter
                ? getChapter(p.subject, p.chapter)?.name
                : undefined;

              return (
                <TouchableOpacity
                  key={`${p.subject}:${p.chapter ?? ''}:${p.topic}`}
                  style={styles.lessonCard}
                  activeOpacity={0.75}
                  onPress={() =>
                    router.push({
                      pathname: '/learn/lesson',
                      params: getLessonParams(p),
                    })
                  }
                >
                  <View style={[styles.lessonDot, { backgroundColor: subject.color }]} />
                  <View style={styles.lessonInfo}>
                    <Text style={styles.lessonTitle}>{topicName}</Text>
                    <View style={styles.lessonMeta}>
                      <Text style={[styles.lessonTopic, { color: subject.color }]}>
                        {chapterName ? `${chapterName} · ${subject.name}` : subject.name}
                      </Text>
                      <Text style={styles.lessonDuration}>
                        · {p.messages_count} messages
                      </Text>
                    </View>
                  </View>
                  <View style={styles.resumeBtn}>
                    <Text style={styles.resumeBtnText}>Resume</Text>
                  </View>
                </TouchableOpacity>
              );
            })
          )}
        </View>

        {/* All Subjects Grid */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>All Subjects</Text>
          <View style={styles.topicGrid}>
            {loadingProgress
              ? Array.from({ length: 4 }).map((_, i) => <SkeletonCard key={i} />)
              : ALL_SUBJECTS.map((subject) => {
                  const { completed, total } = getSubjectStats(subject.slug);
                  const pct = total > 0 ? Math.round((completed / total) * 100) : 0;
                  const isChaptered = hasChapters(subject);
                  const countLabel = isChaptered
                    ? `${subject.chapters!.length} chapters`
                    : `${total} topics`;
                  return (
                    <TouchableOpacity
                      key={subject.slug}
                      style={[styles.topicCard, { borderTopColor: subject.color, borderTopWidth: 3 }]}
                      activeOpacity={0.8}
                      onPress={() =>
                        router.push({
                          pathname: '/learn/[subject]',
                          params: { subject: subject.slug },
                        })
                      }
                    >
                      <View style={[styles.topicEmojiWrap, { backgroundColor: subject.bgColor }]}>
                        <Text style={styles.topicEmoji}>{subject.emoji}</Text>
                      </View>
                      <Text style={styles.topicName}>{subject.name}</Text>
                      <Text style={styles.topicDesc} numberOfLines={2}>
                        {subject.description}
                      </Text>
                      <Text style={styles.lessonCount}>{countLabel}</Text>
                      <View style={styles.progressRow}>
                        <View style={styles.progressTrack}>
                          <View
                            style={[
                              styles.progressFill,
                              { width: `${pct}%`, backgroundColor: subject.color },
                            ]}
                          />
                        </View>
                        <Text style={[styles.progressPct, { color: subject.color }]}>{pct}%</Text>
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
  featuredSubject: {
    fontSize: 13,
    color: 'rgba(255,255,255,0.75)',
    marginBottom: 14,
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
  },
  featuredEmoji: {
    fontSize: 64,
    opacity: 0.85,
  },
  errorBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: Colors.secondary + '15',
    borderRadius: 12,
    padding: 12,
    marginBottom: 16,
  },
  errorBannerText: {
    flex: 1,
    fontSize: 13,
    color: Colors.text,
  },
  errorRetry: {
    fontSize: 13,
    fontWeight: '700',
    color: Colors.primary,
  },
  emptyState: {
    backgroundColor: Colors.card,
    borderRadius: 14,
    padding: 24,
    alignItems: 'center',
    gap: 10,
  },
  emptyStateText: {
    fontSize: 14,
    color: Colors.textMuted,
    textAlign: 'center',
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
