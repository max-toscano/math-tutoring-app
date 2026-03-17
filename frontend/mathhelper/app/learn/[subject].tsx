import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Animated,
} from 'react-native';
import { useEffect, useState, useRef } from 'react';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Colors } from '../../constants/Colors';
import {
  getSubject,
  hasChapters,
  getTotalTopicCount,
  type Subject,
  type Topic,
  type Chapter,
} from '../../constants/curriculums';
import { getSubjectProgress, type TopicProgress } from '../../services/learn';

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
    <Animated.View style={[styles.topicCard, { opacity }]}>
      <View style={styles.topicLeft}>
        <View style={[styles.topicNumber, { backgroundColor: Colors.border }]} />
        <View style={styles.topicInfo}>
          <View style={{ width: '60%', height: 14, backgroundColor: Colors.border, borderRadius: 4, marginBottom: 4 }} />
          <View style={{ width: '90%', height: 10, backgroundColor: Colors.border, borderRadius: 4 }} />
        </View>
      </View>
      <View style={[styles.topicBtn, { backgroundColor: Colors.border }]}>
        <Text style={{ color: 'transparent' }}>Start</Text>
      </View>
    </Animated.View>
  );
}

export default function SubjectDetailScreen() {
  const { subject: subjectSlug } = useLocalSearchParams<{ subject: string }>();
  const router = useRouter();
  const insets = useSafeAreaInsets();

  const subject = getSubject(subjectSlug ?? '') as Subject | undefined;
  const isChaptered = subject ? hasChapters(subject) : false;

  const [progressList, setProgressList] = useState<TopicProgress[]>([]);
  const [loadingProgress, setLoadingProgress] = useState(true);
  const [progressError, setProgressError] = useState(false);

  useEffect(() => {
    if (!subjectSlug) return;
    loadProgress();
  }, [subjectSlug]);

  async function loadProgress() {
    setProgressError(false);
    try {
      const data = await getSubjectProgress(subjectSlug!);
      setProgressList(data);
    } catch {
      setProgressError(true);
    } finally {
      setLoadingProgress(false);
    }
  }

  if (!subject) {
    return (
      <View style={[styles.container, { paddingTop: insets.top }]}>
        <Text style={styles.errorText}>Subject not found</Text>
      </View>
    );
  }

  // Build progress lookup — keyed by "chapter:topic" for chaptered, "topic" for flat
  const progressMap: Record<string, TopicProgress> = {};
  for (const p of progressList) {
    if (isChaptered && p.chapter) {
      progressMap[`${p.chapter}:${p.topic}`] = p;
    } else {
      progressMap[p.topic] = p;
    }
  }

  // Total and completed counts
  const totalTopics = getTotalTopicCount(subject);
  let completedCount = 0;
  if (isChaptered) {
    for (const ch of subject.chapters!) {
      for (const t of ch.topics) {
        if (progressMap[`${ch.slug}:${t.slug}`]?.status === 'completed') completedCount++;
      }
    }
  } else {
    completedCount = subject.topics.filter(
      (t) => progressMap[t.slug]?.status === 'completed',
    ).length;
  }

  // ─── Helpers for flat topic cards ─────────────────────────────────────────

  function getTopicStatusIcon(topic: Topic) {
    const p = progressMap[topic.slug];
    if (!p || p.status === 'not_started') return null;
    if (p.status === 'completed') return 'checkmark-circle' as const;
    return 'play-circle' as const;
  }

  function getTopicStatusColor(topic: Topic) {
    const p = progressMap[topic.slug];
    if (p?.status === 'completed') return Colors.green;
    if (p?.status === 'in_progress') return subject!.color;
    return Colors.textMuted;
  }

  function getTopicButtonLabel(topic: Topic) {
    const p = progressMap[topic.slug];
    if (p?.status === 'completed') return 'Review';
    if (p?.status === 'in_progress') return 'Continue';
    return 'Start';
  }

  // ─── Helpers for chapter cards ────────────────────────────────────────────

  function getChapterCompletedCount(chapter: Chapter): number {
    return chapter.topics.filter(
      (t) => progressMap[`${chapter.slug}:${t.slug}`]?.status === 'completed',
    ).length;
  }

  function getChapterInProgressCount(chapter: Chapter): number {
    return chapter.topics.filter(
      (t) => progressMap[`${chapter.slug}:${t.slug}`]?.status === 'in_progress',
    ).length;
  }

  function getChapterStatus(chapter: Chapter): 'completed' | 'in_progress' | 'not_started' {
    const completed = getChapterCompletedCount(chapter);
    if (completed === chapter.topics.length) return 'completed';
    if (completed > 0 || getChapterInProgressCount(chapter) > 0) return 'in_progress';
    return 'not_started';
  }

  function getChapterStatusIcon(chapter: Chapter) {
    const status = getChapterStatus(chapter);
    if (status === 'completed') return 'checkmark-circle' as const;
    if (status === 'in_progress') return 'play-circle' as const;
    return null;
  }

  function getChapterStatusColor(chapter: Chapter) {
    const status = getChapterStatus(chapter);
    if (status === 'completed') return Colors.green;
    if (status === 'in_progress') return subject!.color;
    return Colors.textMuted;
  }

  function getChapterButtonLabel(chapter: Chapter) {
    const status = getChapterStatus(chapter);
    if (status === 'completed') return 'Review';
    if (status === 'in_progress') return 'Continue';
    return 'Start';
  }

  // ─── Render ───────────────────────────────────────────────────────────────

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={[styles.header, { paddingTop: insets.top + 12, backgroundColor: subject.color }]}>
        <View style={styles.headerRow}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backBtn}>
            <Ionicons name="arrow-back" size={22} color={Colors.white} />
          </TouchableOpacity>
          <View style={styles.headerCenter}>
            <Text style={styles.headerEmoji}>{subject.emoji}</Text>
            <Text style={styles.headerTitle}>{subject.name}</Text>
          </View>
          <View style={styles.backBtn} />
        </View>
        <Text style={styles.headerSub}>{subject.description}</Text>
        <View style={styles.headerProgress}>
          <View style={styles.headerProgressTrack}>
            <View
              style={[
                styles.headerProgressFill,
                { width: totalTopics > 0 ? `${(completedCount / totalTopics) * 100}%` : '0%' },
              ]}
            />
          </View>
          <Text style={styles.headerProgressText}>
            {completedCount}/{totalTopics} completed
          </Text>
        </View>
      </View>

      {/* Content */}
      <ScrollView
        style={styles.scroll}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {progressError && (
          <View style={styles.errorBanner}>
            <Ionicons name="cloud-offline-outline" size={18} color={Colors.secondary} />
            <Text style={styles.errorBannerText}>Couldn't load progress</Text>
            <TouchableOpacity onPress={loadProgress}>
              <Text style={styles.errorRetry}>Retry</Text>
            </TouchableOpacity>
          </View>
        )}

        {loadingProgress
          ? Array.from({ length: 5 }).map((_, i) => <SkeletonCard key={i} />)
          : null}

        {/* ── Chaptered Subject: show chapter cards ── */}
        {!loadingProgress && isChaptered && subject.chapters!.map((chapter, index) => {
          const chCompleted = getChapterCompletedCount(chapter);
          const chTotal = chapter.topics.length;
          const statusIcon = getChapterStatusIcon(chapter);
          const statusColor = getChapterStatusColor(chapter);
          const buttonLabel = getChapterButtonLabel(chapter);

          return (
            <TouchableOpacity
              key={chapter.slug}
              style={styles.topicCard}
              activeOpacity={0.75}
              onPress={() =>
                router.push({
                  pathname: '/learn/chapter',
                  params: { subject: subjectSlug!, chapter: chapter.slug },
                })
              }
            >
              <View style={styles.topicLeft}>
                <View style={[styles.topicNumber, { backgroundColor: subject.bgColor }]}>
                  {statusIcon ? (
                    <Ionicons name={statusIcon} size={20} color={statusColor} />
                  ) : (
                    <Text style={[styles.topicNumberText, { color: subject.color }]}>
                      {index + 1}
                    </Text>
                  )}
                </View>
                <View style={styles.topicInfo}>
                  <Text style={styles.topicName}>{chapter.name}</Text>
                  <Text style={styles.topicDesc} numberOfLines={2}>
                    {chapter.description}
                  </Text>
                  <Text style={[styles.topicMeta, { color: statusColor }]}>
                    {chCompleted}/{chTotal} lessons
                  </Text>
                </View>
              </View>
              <View style={[styles.topicBtn, { backgroundColor: subject.bgColor }]}>
                <Text style={[styles.topicBtnText, { color: subject.color }]}>{buttonLabel}</Text>
              </View>
            </TouchableOpacity>
          );
        })}

        {/* ── Flat Subject: show topic cards (unchanged) ── */}
        {!loadingProgress && !isChaptered && subject.topics.map((topic, index) => {
          const statusIcon = getTopicStatusIcon(topic);
          const statusColor = getTopicStatusColor(topic);
          const buttonLabel = getTopicButtonLabel(topic);
          const p = progressMap[topic.slug];

          return (
            <TouchableOpacity
              key={topic.slug}
              style={styles.topicCard}
              activeOpacity={0.75}
              onPress={() =>
                router.push({
                  pathname: '/learn/lesson',
                  params: { subject: subjectSlug!, topic: topic.slug },
                })
              }
            >
              <View style={styles.topicLeft}>
                <View style={[styles.topicNumber, { backgroundColor: subject.bgColor }]}>
                  {statusIcon ? (
                    <Ionicons name={statusIcon} size={20} color={statusColor} />
                  ) : (
                    <Text style={[styles.topicNumberText, { color: subject.color }]}>
                      {index + 1}
                    </Text>
                  )}
                </View>
                <View style={styles.topicInfo}>
                  <Text style={styles.topicName}>{topic.name}</Text>
                  <Text style={styles.topicDesc} numberOfLines={2}>
                    {topic.description}
                  </Text>
                  {p && p.status === 'in_progress' && (
                    <Text style={[styles.topicMeta, { color: subject.color }]}>
                      {p.messages_count} messages
                    </Text>
                  )}
                </View>
              </View>
              <View style={[styles.topicBtn, { backgroundColor: subject.bgColor }]}>
                <Text style={[styles.topicBtnText, { color: subject.color }]}>{buttonLabel}</Text>
              </View>
            </TouchableOpacity>
          );
        })}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  errorText: { fontSize: 16, color: Colors.textLight, textAlign: 'center', marginTop: 60 },
  header: {
    paddingHorizontal: 20,
    paddingBottom: 20,
    borderBottomLeftRadius: 24,
    borderBottomRightRadius: 24,
  },
  headerRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  backBtn: { width: 40, height: 40, borderRadius: 12, alignItems: 'center', justifyContent: 'center' },
  headerCenter: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  headerEmoji: { fontSize: 24 },
  headerTitle: { fontSize: 22, fontWeight: '700', color: Colors.white },
  headerSub: { fontSize: 14, color: 'rgba(255,255,255,0.75)', textAlign: 'center', marginBottom: 14 },
  headerProgress: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  headerProgressTrack: {
    flex: 1, height: 6, backgroundColor: 'rgba(255,255,255,0.3)', borderRadius: 3, overflow: 'hidden',
  },
  headerProgressFill: { height: '100%', backgroundColor: Colors.white, borderRadius: 3 },
  headerProgressText: { fontSize: 12, color: 'rgba(255,255,255,0.85)', fontWeight: '600' },
  scroll: { flex: 1 },
  scrollContent: { padding: 16, paddingBottom: 32 },
  topicCard: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: Colors.card,
    borderRadius: 16,
    padding: 14,
    marginBottom: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 1,
  },
  topicLeft: { flexDirection: 'row', alignItems: 'center', gap: 12, flex: 1 },
  topicNumber: {
    width: 40, height: 40, borderRadius: 12, alignItems: 'center', justifyContent: 'center',
  },
  topicNumberText: { fontSize: 16, fontWeight: '700' },
  topicInfo: { flex: 1, gap: 2 },
  topicName: { fontSize: 15, fontWeight: '600', color: Colors.text },
  topicDesc: { fontSize: 12, color: Colors.textLight, lineHeight: 16 },
  topicMeta: { fontSize: 11, fontWeight: '600', marginTop: 2 },
  topicBtn: { borderRadius: 10, paddingHorizontal: 14, paddingVertical: 7, marginLeft: 8 },
  topicBtnText: { fontSize: 13, fontWeight: '700' },
  errorBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: Colors.secondary + '15',
    borderRadius: 12,
    padding: 12,
    marginBottom: 12,
  },
  errorBannerText: { flex: 1, fontSize: 13, color: Colors.text },
  errorRetry: { fontSize: 13, fontWeight: '700', color: Colors.primary },
});
