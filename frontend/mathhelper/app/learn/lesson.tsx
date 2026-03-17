import {
  View,
  Text,
  TextInput,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  ActivityIndicator,
  Image,
} from 'react-native';
import { useState, useRef, useEffect } from 'react';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Colors } from '../../constants/Colors';
import { getSubject, getTopic, getChapterTopic, getChapter } from '../../constants/curriculums';
import { getImageSource } from '../../constants/imageCatalog';
import {
  sendLessonMessage,
  type Message,
  type QuizResult,
  type QuizOutcome,
} from '../../services/learn';

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  images?: string[];
  quizResult?: QuizResult;
  quizOutcome?: QuizOutcome;
}

export default function LessonScreen() {
  const { subject: subjectSlug, chapter: chapterSlug, topic: topicSlug } = useLocalSearchParams<{
    subject: string;
    chapter?: string;
    topic: string;
  }>();
  const router = useRouter();
  const insets = useSafeAreaInsets();
  const scrollRef = useRef<ScrollView>(null);

  const subject = getSubject(subjectSlug ?? '');
  const chapter = chapterSlug ? getChapter(subjectSlug ?? '', chapterSlug) : undefined;
  const topic = chapterSlug
    ? getChapterTopic(subjectSlug ?? '', chapterSlug, topicSlug ?? '')
    : getTopic(subjectSlug ?? '', topicSlug ?? '');

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [conversationHistory, setConversationHistory] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [phase, setPhase] = useState<string | null>(null);
  const [quizOutcome, setQuizOutcome] = useState<QuizOutcome | null>(null);
  const [completed, setCompleted] = useState(false);
  const [saved, setSaved] = useState(false);

  // Auto-start lesson on mount
  useEffect(() => {
    if (subjectSlug && topicSlug && messages.length === 0) {
      startLesson();
    }
  }, [subjectSlug, topicSlug]);

  function handleLessonResult(result: import('../../services/learn').LessonResponse) {
    const aiMsg: ChatMessage = {
      id: Date.now().toString(),
      role: 'assistant',
      content: result.message,
      images: result.images?.length ? result.images : undefined,
      quizResult: result.quiz_result ?? undefined,
      quizOutcome: result.quiz_outcome ?? undefined,
    };
    setMessages((prev) => [...prev, aiMsg]);
    setConversationHistory(result.conversation_history);
    if (result.phase) setPhase(result.phase);
    if (result.quiz_outcome) {
      setQuizOutcome(result.quiz_outcome);
      if (result.quiz_outcome.passed) setCompleted(true);
    }
  }

  async function startLesson() {
    setLoading(true);
    setError(null);
    try {
      const result = await sendLessonMessage(subjectSlug!, topicSlug!, {
        chapter: chapterSlug ?? undefined,
      });
      setMessages([]);
      handleLessonResult(result);
    } catch (e: any) {
      setError(e.message ?? 'Failed to start lesson');
    } finally {
      setLoading(false);
    }
  }

  async function handleSend() {
    const text = input.trim();
    if (!text || loading) return;

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: text,
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setError(null);
    setLoading(true);

    setTimeout(() => scrollRef.current?.scrollToEnd({ animated: true }), 100);

    try {
      const result = await sendLessonMessage(subjectSlug!, topicSlug!, {
        chapter: chapterSlug ?? undefined,
        studentInput: text,
        conversationHistory,
      });
      handleLessonResult(result);
    } catch (e: any) {
      setError(e.message ?? 'Something went wrong.');
    } finally {
      setLoading(false);
      setTimeout(() => scrollRef.current?.scrollToEnd({ animated: true }), 100);
    }
  }

  function handleSave() {
    // Progress is already saved server-side on every message.
    // This gives the user visual confirmation and navigates back.
    setSaved(true);
    setTimeout(() => router.back(), 600);
  }

  const headerColor = subject?.color ?? Colors.primary;

  // Progress stepper logic
  const STEPS = [
    { key: 'lesson', label: 'Learn', icon: 'book-outline' as const },
    { key: 'practice', label: 'Practice', icon: 'pencil-outline' as const },
    { key: 'quiz', label: 'Quiz', icon: 'help-circle-outline' as const },
    { key: 'done', label: 'Done', icon: 'checkmark-circle-outline' as const },
  ];

  function getStepStatus(stepKey: string): 'completed' | 'active' | 'upcoming' {
    if (!phase) return stepKey === 'lesson' ? 'active' : 'upcoming';
    const phaseOrder = ['lesson', 'practice', 'quiz', 'done'];
    const currentIdx = phaseOrder.indexOf(phase === 'review' ? 'quiz' : phase);
    const stepIdx = phaseOrder.indexOf(stepKey);
    if (phase === 'done') return 'completed';
    if (stepIdx < currentIdx) return 'completed';
    if (stepIdx === currentIdx) return 'active';
    return 'upcoming';
  }

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={[styles.header, { paddingTop: insets.top + 8, backgroundColor: headerColor }]}>
        <View style={styles.headerRow}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backBtn}>
            <Ionicons name="arrow-back" size={22} color={Colors.white} />
          </TouchableOpacity>
          <View style={styles.headerCenter}>
            <Text style={styles.headerTitle} numberOfLines={1}>
              {topic?.name ?? 'Lesson'}
            </Text>
            <Text style={styles.headerSub}>
              {chapter ? `${chapter.name} · ${subject?.name ?? ''}` : (subject?.name ?? '')}
            </Text>
          </View>
          <TouchableOpacity onPress={handleSave} style={styles.backBtn} activeOpacity={0.7}>
            <Ionicons
              name={saved ? 'checkmark-circle' : 'bookmark-outline'}
              size={22}
              color={Colors.white}
            />
          </TouchableOpacity>
        </View>

        {/* Progress Stepper */}
        <View style={styles.stepperRow}>
          {STEPS.map((step, i) => {
            const status = getStepStatus(step.key);
            const isReview = phase === 'review' && step.key === 'quiz';
            return (
              <View key={step.key} style={styles.stepperItem}>
                {i > 0 && (
                  <View
                    style={[
                      styles.stepperLine,
                      status === 'upcoming'
                        ? styles.stepperLineUpcoming
                        : styles.stepperLineCompleted,
                    ]}
                  />
                )}
                <View
                  style={[
                    styles.stepperCircle,
                    status === 'completed' && styles.stepperCircleCompleted,
                    status === 'active' && styles.stepperCircleActive,
                    status === 'upcoming' && styles.stepperCircleUpcoming,
                  ]}
                >
                  {status === 'completed' ? (
                    <Ionicons name="checkmark" size={14} color={Colors.white} />
                  ) : (
                    <Ionicons
                      name={isReview ? 'refresh-outline' : step.icon}
                      size={14}
                      color={status === 'active' ? headerColor : 'rgba(255,255,255,0.4)'}
                    />
                  )}
                </View>
                <Text
                  style={[
                    styles.stepperLabel,
                    status === 'active' && styles.stepperLabelActive,
                    status === 'upcoming' && styles.stepperLabelUpcoming,
                  ]}
                >
                  {isReview ? 'Review' : step.label}
                </Text>
              </View>
            );
          })}
        </View>
      </View>

      {/* Chat */}
      <KeyboardAvoidingView
        style={styles.chatArea}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
        keyboardVerticalOffset={0}
      >
        <ScrollView
          ref={scrollRef}
          style={styles.messageList}
          contentContainerStyle={styles.messageListContent}
          showsVerticalScrollIndicator={false}
          onContentSizeChange={() => scrollRef.current?.scrollToEnd({ animated: true })}
        >
          {messages.map((msg) => (
            <View
              key={msg.id}
              style={[
                styles.messageBubble,
                msg.role === 'user' ? styles.userBubble : styles.assistantBubble,
              ]}
            >
              {msg.role === 'assistant' && (
                <View style={[styles.assistantAvatar, { backgroundColor: (subject?.bgColor ?? Colors.primaryLight) }]}>
                  <Ionicons name="school" size={14} color={headerColor} />
                </View>
              )}
              <View
                style={[
                  styles.bubbleContent,
                  msg.role === 'user' ? styles.userBubbleContent : styles.assistantBubbleContent,
                ]}
              >
                <Text
                  style={[
                    styles.bubbleText,
                    msg.role === 'user' ? styles.userBubbleText : styles.assistantBubbleText,
                  ]}
                >
                  {msg.content}
                </Text>
                {msg.images?.map((imageId) => {
                  const source = getImageSource(imageId);
                  if (!source) return null;
                  return (
                    <Image
                      key={imageId}
                      source={source}
                      style={styles.lessonImage}
                      resizeMode="contain"
                    />
                  );
                })}
              </View>
            </View>
          ))}

          {loading && (
            <View style={[styles.messageBubble, styles.assistantBubble]}>
              <View style={[styles.assistantAvatar, { backgroundColor: (subject?.bgColor ?? Colors.primaryLight) }]}>
                <Ionicons name="school" size={14} color={headerColor} />
              </View>
              <View style={[styles.bubbleContent, styles.assistantBubbleContent]}>
                <ActivityIndicator size="small" color={headerColor} />
                <Text style={styles.thinkingText}>
                  {messages.length === 0 ? 'Preparing lesson...' : 'Thinking...'}
                </Text>
              </View>
            </View>
          )}

          {error && (
            <View style={styles.errorCard}>
              <Ionicons name="alert-circle-outline" size={18} color={Colors.secondary} />
              <Text style={styles.errorText}>{error}</Text>
              <TouchableOpacity onPress={messages.length === 0 ? startLesson : handleSend}>
                <Text style={styles.retryText}>Retry</Text>
              </TouchableOpacity>
            </View>
          )}
        </ScrollView>

        {/* Save confirmation */}
        {saved && (
          <View style={styles.saveToast}>
            <Ionicons name="checkmark-circle" size={18} color={Colors.green} />
            <Text style={styles.saveToastText}>Progress saved!</Text>
          </View>
        )}

        {/* Quiz outcome banner */}
        {quizOutcome && (
          <View style={[styles.quizBanner, { backgroundColor: quizOutcome.passed ? Colors.green + '18' : Colors.secondary + '18' }]}>
            <Ionicons
              name={quizOutcome.passed ? 'checkmark-circle' : 'refresh-circle'}
              size={22}
              color={quizOutcome.passed ? Colors.green : Colors.secondary}
            />
            <Text style={[styles.quizBannerText, { color: quizOutcome.passed ? Colors.green : Colors.secondary }]}>
              {quizOutcome.passed
                ? `Passed! ${quizOutcome.score}/5`
                : `${quizOutcome.score}/5 — Review and retry`}
            </Text>
          </View>
        )}

        {/* Done — go back */}
        {completed && (
          <TouchableOpacity
            style={[styles.completeBtn, { backgroundColor: Colors.green }]}
            onPress={() => router.back()}
            activeOpacity={0.8}
          >
            <Ionicons name="checkmark-done" size={20} color={Colors.white} />
            <Text style={styles.completeBtnText}>Done! Go back</Text>
          </TouchableOpacity>
        )}

        {/* Input */}
        <View style={[styles.inputBar, { paddingBottom: Math.max(insets.bottom, 12) }]}>
          <TextInput
            style={styles.textInput}
            value={input}
            onChangeText={setInput}
            placeholder="Type your answer..."
            placeholderTextColor={Colors.textMuted}
            multiline
            maxLength={2000}
            onSubmitEditing={handleSend}
            blurOnSubmit={false}
            editable={!loading && messages.length > 0}
          />
          <TouchableOpacity
            style={[
              styles.sendBtn,
              { backgroundColor: headerColor },
              (!input.trim() || loading) && styles.sendBtnDisabled,
            ]}
            onPress={handleSend}
            disabled={!input.trim() || loading}
            activeOpacity={0.7}
          >
            <Ionicons name="send" size={18} color={Colors.white} />
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  header: {
    paddingHorizontal: 20,
    paddingBottom: 14,
    borderBottomLeftRadius: 24,
    borderBottomRightRadius: 24,
  },
  headerRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 4,
  },
  backBtn: { width: 40, height: 40, borderRadius: 12, alignItems: 'center', justifyContent: 'center' },
  headerCenter: { flex: 1, alignItems: 'center' },
  headerTitle: { fontSize: 17, fontWeight: '700', color: Colors.white },
  headerSub: { fontSize: 12, color: 'rgba(255,255,255,0.7)', marginTop: 2 },
  stepperRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 10,
    paddingHorizontal: 4,
  },
  stepperItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  stepperLine: {
    width: 28,
    height: 2,
    marginHorizontal: 2,
    borderRadius: 1,
  },
  stepperLineCompleted: {
    backgroundColor: 'rgba(255,255,255,0.7)',
  },
  stepperLineUpcoming: {
    backgroundColor: 'rgba(255,255,255,0.2)',
  },
  stepperCircle: {
    width: 28,
    height: 28,
    borderRadius: 14,
    alignItems: 'center',
    justifyContent: 'center',
  },
  stepperCircleCompleted: {
    backgroundColor: 'rgba(255,255,255,0.85)',
  },
  stepperCircleActive: {
    backgroundColor: Colors.white,
  },
  stepperCircleUpcoming: {
    backgroundColor: 'rgba(255,255,255,0.15)',
  },
  stepperLabel: {
    fontSize: 10,
    color: Colors.white,
    fontWeight: '600',
    marginLeft: 4,
    marginRight: 2,
  },
  stepperLabelActive: {
    fontWeight: '700',
  },
  stepperLabelUpcoming: {
    opacity: 0.5,
  },

  chatArea: { flex: 1 },
  messageList: { flex: 1 },
  messageListContent: { padding: 16, paddingBottom: 8 },

  messageBubble: { marginBottom: 16 },
  userBubble: { alignItems: 'flex-end' },
  assistantBubble: { flexDirection: 'row', alignItems: 'flex-start', gap: 8 },
  assistantAvatar: {
    width: 28, height: 28, borderRadius: 14,
    alignItems: 'center', justifyContent: 'center', marginTop: 2,
  },
  bubbleContent: { maxWidth: '80%', borderRadius: 18, padding: 14 },
  userBubbleContent: { backgroundColor: Colors.primary, borderBottomRightRadius: 4 },
  assistantBubbleContent: {
    backgroundColor: Colors.card, borderBottomLeftRadius: 4,
    shadowColor: '#000', shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05, shadowRadius: 4, elevation: 1,
  },
  bubbleText: { fontSize: 15, lineHeight: 22 },
  lessonImage: {
    width: '100%',
    height: 180,
    marginTop: 10,
    borderRadius: 10,
    backgroundColor: Colors.background,
  },
  userBubbleText: { color: Colors.white },
  assistantBubbleText: { color: Colors.text },
  thinkingText: { fontSize: 13, color: Colors.textLight, marginLeft: 8 },

  errorCard: {
    flexDirection: 'row', alignItems: 'center', gap: 8,
    backgroundColor: Colors.secondary + '15', borderRadius: 12, padding: 12,
    marginBottom: 12,
  },
  errorText: { flex: 1, fontSize: 13, color: Colors.text },
  retryText: { fontSize: 13, fontWeight: '700', color: Colors.primary },

  inputBar: {
    flexDirection: 'row', alignItems: 'flex-end', gap: 10,
    paddingHorizontal: 16, paddingTop: 12,
    borderTopWidth: 1, borderTopColor: Colors.border, backgroundColor: Colors.card,
  },
  textInput: {
    flex: 1, fontSize: 15, color: Colors.text,
    backgroundColor: Colors.background, borderRadius: 20,
    paddingHorizontal: 16, paddingVertical: 10,
    maxHeight: 100, borderWidth: 1, borderColor: Colors.border,
  },
  sendBtn: {
    width: 42, height: 42, borderRadius: 21,
    alignItems: 'center', justifyContent: 'center', marginBottom: 2,
  },
  sendBtnDisabled: { opacity: 0.4 },
  saveToast: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 6,
    marginHorizontal: 16,
    marginTop: 8,
    paddingVertical: 10,
    paddingHorizontal: 16,
    borderRadius: 12,
    backgroundColor: Colors.green + '15',
  },
  saveToastText: {
    fontSize: 14,
    fontWeight: '600',
    color: Colors.green,
  },
  quizBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginHorizontal: 16,
    marginTop: 8,
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderRadius: 14,
  },
  quizBannerText: {
    fontSize: 15,
    fontWeight: '700',
  },
  completeBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    marginHorizontal: 16,
    marginTop: 8,
    paddingVertical: 14,
    borderRadius: 14,
  },
  completeBtnText: {
    fontSize: 15,
    fontWeight: '700',
    color: Colors.white,
  },
});
