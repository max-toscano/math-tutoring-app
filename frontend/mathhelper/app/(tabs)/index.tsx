import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Image,
  ActivityIndicator,
  TextInput,
  KeyboardAvoidingView,
  Platform,
  Animated,
  Alert,
} from 'react-native';
import { useState, useRef, useEffect } from 'react';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import * as ImagePicker from 'expo-image-picker';
import {
  startAgentSession,
  sendAgentMessage,
  closeAgentSession,
  type AgentMessage,
  type GraphOutput,
} from '../../services/agent';
import { useAppContext, type TutoringSession } from '../../context/AppContext';
import { Colors } from '../../constants/Colors';
import { pickRandomQuestions, type QuickQuestion } from '../../constants/quickQuestions';
import ResponseBubble from '../../components/ResponseBubble';
import SuggestionChips from '../../components/SuggestionChips';
import ToolStatus from '../../components/ToolStatus';
import MessageReactions from '../../components/MessageReactions';

// ─── Types ───────────────────────────────────────────────────────────────────
interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  imageUri?: string;
  topic?: string;
  mode?: string;
  tools?: string[];
  graphs?: GraphOutput[];
  suggestions?: string[];
}

const MODE_OPTIONS = [
  { key: null, label: 'Auto', icon: 'sparkles-outline' },
  { key: 'explain', label: 'Explain', icon: 'bulb-outline' },
  { key: 'guide_me', label: 'Guide Me', icon: 'help-circle-outline' },
  { key: 'hint', label: 'Hint', icon: 'eye-outline' },
  { key: 'check_answer', label: 'Check Work', icon: 'checkmark-circle-outline' },
] as const;

// ─── Helpers ─────────────────────────────────────────────────────────────────
function formatSessionDate(iso: string) {
  const d = new Date(iso);
  const now = new Date();
  const diffMs = now.getTime() - d.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  if (diffMins < 1) return 'Just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  const diffHours = Math.floor(diffMins / 60);
  if (diffHours < 24) return `${diffHours}h ago`;
  const diffDays = Math.floor(diffHours / 24);
  if (diffDays === 1) return 'Yesterday';
  if (diffDays < 7) return `${diffDays}d ago`;
  return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
}

function generateSessionTitle(messages: ChatMessage[], analysis?: any): string {
  if (analysis?.problem) {
    return analysis.problem.length > 50
      ? analysis.problem.slice(0, 47) + '...'
      : analysis.problem;
  }
  const firstUserMsg = messages.find((m) => m.role === 'user');
  if (firstUserMsg?.content && firstUserMsg.content !== 'Sent a photo') {
    return firstUserMsg.content.length > 50
      ? firstUserMsg.content.slice(0, 47) + '...'
      : firstUserMsg.content;
  }
  return 'Tutoring Session';
}

function generateSessionPreview(messages: ChatMessage[]): string {
  const lastAssistant = [...messages].reverse().find((m) => m.role === 'assistant');
  if (lastAssistant) {
    return lastAssistant.content.length > 80
      ? lastAssistant.content.slice(0, 77) + '...'
      : lastAssistant.content;
  }
  return 'No response yet';
}

// ─── Dashboard ───────────────────────────────────────────────────────────────
export default function DashboardScreen() {
  const insets = useSafeAreaInsets();
  const router = useRouter();
  const scrollRef = useRef<ScrollView>(null);
  const { savedItems, saveAnalysis, sessions, saveSession, deleteSession } = useAppContext();

  // Photo state
  const [pendingPhoto, setPendingPhoto] = useState<string | null>(null);
  const [pendingPhotoBase64, setPendingPhotoBase64] = useState<string | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [expandedSteps, setExpandedSteps] = useState<Set<number>>(new Set());

  // Chat state
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [conversationHistory, setConversationHistory] = useState<AgentMessage[]>([]);
  const [chatInput, setChatInput] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const [chatError, setChatError] = useState<string | null>(null);

  // Agent session
  const [agentSessionId, setAgentSessionId] = useState<string | null>(null);

  // Stores the last text sent so the Retry button can re-send it after an error
  const lastAttemptedMessage = useRef<string>('');

  useEffect(() => {
    startAgentSession()
      .then(({ session_id }) => {
        console.log('Session started:', session_id);
        setAgentSessionId(session_id);
      })
      .catch((e) => {
        console.error('Session start failed:', e);
        setChatError('Failed to connect. Make sure the backend is running.');
      });
  }, []);

  // Session state
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null);
  const [sessionSaved, setSessionSaved] = useState(false);
  const [savingSession, setSavingSession] = useState(false);

  // Mode + Attach state
  const [selectedMode, setSelectedMode] = useState<string | null>(null);
  const [attachMenuOpen, setAttachMenuOpen] = useState(false);

  // Quick questions — randomized from pool each session
  const [quickQuestions, setQuickQuestions] = useState<QuickQuestion[]>(() => pickRandomQuestions(4));

  // Animated dot indicator for "thinking"
  const dotAnim = useRef(new Animated.Value(0)).current;
  useEffect(() => {
    if (chatLoading || analyzing) {
      const loop = Animated.loop(
        Animated.sequence([
          Animated.timing(dotAnim, { toValue: 1, duration: 600, useNativeDriver: true }),
          Animated.timing(dotAnim, { toValue: 0, duration: 600, useNativeDriver: true }),
        ])
      );
      loop.start();
      return () => loop.stop();
    }
  }, [chatLoading, analyzing]);

  const chatActive = chatMessages.length > 0 || analyzing;

  // ── Photo handlers ──
  async function handleTakePhoto() {
    setAttachMenuOpen(false);
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    if (status !== 'granted') return;
    const result = await ImagePicker.launchCameraAsync({ allowsEditing: true, quality: 0.9, base64: true });
    if (!result.canceled) {
      setPendingPhoto(result.assets[0].uri);
      setPendingPhotoBase64(result.assets[0].base64 ?? null);
    }
  }

  async function handleUploadPhoto() {
    setAttachMenuOpen(false);
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (status !== 'granted') return;
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      quality: 0.9,
      base64: true,
    });
    if (!result.canceled) {
      setPendingPhoto(result.assets[0].uri);
      setPendingPhotoBase64(result.assets[0].base64 ?? null);
    }
  }

  // ── "Still confused" — sends a contextual follow-up with full history ──
  async function handleStillConfused(confusingMessage: string) {
    if (chatLoading || !agentSessionId) return;

    // Build a follow-up that references what the student is confused about
    const truncated = confusingMessage.slice(0, 200);
    const followUpText = `I'm still confused about your previous explanation. Can you explain it more simply or try a different approach? Here's what I didn't understand: "${truncated}"`;

    // Show as a user message in the chat
    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: "I'm still confused — can you explain that differently?",
    };
    setChatMessages((prev) => [...prev, userMsg]);
    setChatLoading(true);

    setTimeout(() => scrollRef.current?.scrollToEnd({ animated: true }), 100);

    try {
      const result = await sendAgentMessage(agentSessionId, followUpText, {
        selectedMode: selectedMode ?? undefined,
        conversationHistory,
      });

      if (!result.response) throw new Error('The AI returned an empty response. Please try again.');

      const assistantMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: result.response,
        topic: result.topic ?? undefined,
        mode: result.mode ?? undefined,
        tools: result.tools_used,
        graphs: result.graphs,
        suggestions: result.suggestions,
      };
      setChatMessages((prev) => [...prev, assistantMsg]);
      setConversationHistory((prev) => [
        ...prev,
        { role: 'user' as const, content: followUpText },
        { role: 'assistant' as const, content: result.response },
      ]);
    } catch (e: any) {
      setChatError(e.message ?? 'Something went wrong.');
    } finally {
      setChatLoading(false);
      setTimeout(() => scrollRef.current?.scrollToEnd({ animated: true }), 200);
    }
  }

  // ── Send message (text, photo, or both) ──
  // `overrideText` lets callers pass text directly instead of relying on
  // chatInput state, which may not have updated yet (stale closure).
  async function handleSend(overrideText?: string) {
    const text = (overrideText ?? chatInput).trim();
    const photo = pendingPhoto;

    if ((!text && !photo) || chatLoading || analyzing) return;

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: text || (photo ? 'Sent a photo' : ''),
      imageUri: photo ?? undefined,
    };

    lastAttemptedMessage.current = text;
    setChatMessages((prev) => [...prev, userMsg]);
    setChatInput('');  // clear input regardless of overrideText
    setPendingPhoto(null);
    setPendingPhotoBase64(null);
    setChatError(null);
    setSessionSaved(false);

    setTimeout(() => scrollRef.current?.scrollToEnd({ animated: true }), 100);

    if (photo) {
      // Send photo through the AI agent (GPT-4o vision)
      setAnalyzing(true);
      setChatLoading(true);
      try {
        if (!agentSessionId) throw new Error('Session not started');
        if (!pendingPhotoBase64) throw new Error('Photo not ready');
        const result = await sendAgentMessage(agentSessionId, text || 'Solve this math problem from the photo', {
          selectedMode: selectedMode ?? undefined,
          conversationHistory,
          imageBase64: pendingPhotoBase64,
        });

        if (!result.response) throw new Error('The AI returned an empty response. Please try again.');

        const assistantMsg: ChatMessage = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: result.response,
          topic: result.topic ?? undefined,
          mode: result.mode ?? undefined,
          tools: result.tools_used,
          graphs: result.graphs,
          suggestions: result.suggestions,
        };
        setChatMessages((prev) => [...prev, assistantMsg]);
        setConversationHistory((prev) => [
          ...prev,
          { role: 'user' as const, content: text || '[photo of math problem]' },
          { role: 'assistant' as const, content: result.response },
        ]);
      } catch (e: any) {
        setChatError(e.message ?? 'Something went wrong. Please try again.');
      } finally {
        setAnalyzing(false);
        setChatLoading(false);
        setTimeout(() => scrollRef.current?.scrollToEnd({ animated: true }), 200);
      }
    } else {
      // Text chat via the agent
      setChatLoading(true);
      try {
        if (!agentSessionId) throw new Error('Session not started');
        const result = await sendAgentMessage(agentSessionId, text, {
          selectedMode: selectedMode ?? undefined,
          conversationHistory,
        });

        if (!result.response) throw new Error('The AI returned an empty response. Please try again.');

        const assistantMsg: ChatMessage = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: result.response,
          topic: result.topic ?? undefined,
          mode: result.mode ?? undefined,
          tools: result.tools_used,
          graphs: result.graphs,
          suggestions: result.suggestions,
        };
        setChatMessages((prev) => [...prev, assistantMsg]);
        setConversationHistory((prev) => [
          ...prev,
          { role: 'user' as const, content: text },
          { role: 'assistant' as const, content: result.response },
        ]);
      } catch (e: any) {
        setChatError(e.message ?? 'Something went wrong.');
      } finally {
        setChatLoading(false);
        setTimeout(() => scrollRef.current?.scrollToEnd({ animated: true }), 200);
      }
    }
  }

  // ── Save session ──
  async function handleSaveSession() {
    if (chatMessages.length === 0 || savingSession) return;
    setSavingSession(true);
    try {
      const title = generateSessionTitle(chatMessages, analysisResult);
      const preview = generateSessionPreview(chatMessages);
      const photoUri = chatMessages.find((m) => m.imageUri)?.imageUri;

      const id = await saveSession({
        title,
        preview,
        messages: chatMessages,
        conversationHistory,
        analysis: analysisResult ?? undefined,
        photoUri,
      });

      setCurrentSessionId(id);
      setSessionSaved(true);
    } catch (e: any) {
      Alert.alert('Save Failed', e.message ?? 'Could not save session.');
    } finally {
      setSavingSession(false);
    }
  }

  // ── Resume a saved session ──
  function handleResumeSession(session: TutoringSession) {
    resetAll();
    setChatMessages(session.messages as ChatMessage[]);
    setConversationHistory(session.conversationHistory);
    setAnalysisResult(session.analysis ?? null);
    setCurrentSessionId(session.id);
    setSessionSaved(true);
    setTimeout(() => scrollRef.current?.scrollToEnd({ animated: false }), 100);
  }

  // ── Delete session with confirmation (cross-platform) ──
  function handleDeleteSession(id: string) {
    if (Platform.OS === 'web') {
      if (window.confirm('Are you sure you want to delete this session?')) {
        deleteSession(id);
      }
    } else {
      Alert.alert(
        'Delete Session',
        'Are you sure you want to delete this session?',
        [
          { text: 'Cancel', style: 'cancel' },
          { text: 'Delete', style: 'destructive', onPress: () => deleteSession(id) },
        ]
      );
    }
  }

  async function handleExit() {
    // Close session and reset
    if (agentSessionId && chatMessages.some((m) => m.role === 'assistant')) {
      try {
        await closeAgentSession(agentSessionId);
      } catch {
        // Ignore close errors
      }
    }
    resetAll();
  }

  function resetAll() {
    setPendingPhoto(null);
    setAnalysisResult(null);
    setChatMessages([]);
    setConversationHistory([]);
    setChatInput('');
    setChatError(null);
    setChatLoading(false);
    setAnalyzing(false);
    setExpandedSteps(new Set());
    setCurrentSessionId(null);
    setSessionSaved(false);
    setAttachMenuOpen(false);
    setQuickQuestions(pickRandomQuestions(4));
    // Start fresh agent session
    startAgentSession()
      .then(({ session_id }) => setAgentSessionId(session_id))
      .catch(() => {});
  }

  const recentSaved = savedItems.slice(0, 3);
  const recentSessions = sessions.slice(0, 5);
  const uniqueTopics = [...new Set(savedItems.map((i) => i.analysis.topic))].length;

  return (
    <View style={styles.container}>
      {/* ── Header ── */}
      <View style={[styles.header, { paddingTop: insets.top + 16 }]}>
        <View style={styles.headerTop}>
          <View>
            <Text style={styles.greeting}>Math Helper</Text>
            <Text style={styles.subGreeting}>
              {chatActive ? 'Tutoring session' : 'Scan or ask anything'}
            </Text>
          </View>
          {chatActive ? (
            <View style={styles.headerActions}>
              {/* Save button */}
              <TouchableOpacity
                style={[styles.headerActionBtn, sessionSaved && styles.headerActionBtnSaved]}
                onPress={handleSaveSession}
                disabled={sessionSaved || savingSession || chatMessages.length === 0}
                activeOpacity={0.7}
              >
                {savingSession ? (
                  <ActivityIndicator size="small" color={Colors.white} />
                ) : (
                  <>
                    <Ionicons
                      name={sessionSaved ? 'checkmark-circle' : 'bookmark-outline'}
                      size={16}
                      color={Colors.white}
                    />
                    <Text style={styles.headerActionText}>
                      {sessionSaved ? 'Saved' : 'Save'}
                    </Text>
                  </>
                )}
              </TouchableOpacity>
              {/* Exit button */}
              <TouchableOpacity style={[styles.headerActionBtn, styles.headerActionBtnExit]} onPress={handleExit}>
                <Ionicons name="close-outline" size={18} color={Colors.white} />
                <Text style={styles.headerActionText}>Exit</Text>
              </TouchableOpacity>
            </View>
          ) : (
            <TouchableOpacity style={styles.avatarBtn}>
              <View style={styles.avatar}>
                <Ionicons name="person" size={20} color={Colors.white} />
              </View>
            </TouchableOpacity>
          )}
        </View>
      </View>

      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      >
        <ScrollView
          ref={scrollRef}
          style={styles.scroll}
          contentContainerStyle={styles.scrollContent}
          showsVerticalScrollIndicator={false}
          keyboardShouldPersistTaps="handled"
        >
          {/* ── Home View ── */}
          {!chatActive && (
            <>
              {/* Stats */}
              <View style={styles.statsRow}>
                <View style={styles.statCard}>
                  <View style={[styles.statIconWrap, { backgroundColor: Colors.primary + '20' }]}>
                    <Ionicons name="bookmark" size={20} color={Colors.primary} />
                  </View>
                  <Text style={styles.statValue}>{savedItems.length}</Text>
                  <Text style={styles.statLabel}>Saved</Text>
                </View>
                <View style={styles.statCard}>
                  <View style={[styles.statIconWrap, { backgroundColor: Colors.teal + '20' }]}>
                    <Ionicons name="chatbubbles" size={20} color={Colors.teal} />
                  </View>
                  <Text style={styles.statValue}>{sessions.length}</Text>
                  <Text style={styles.statLabel}>Sessions</Text>
                </View>
                <View style={styles.statCard}>
                  <View style={[styles.statIconWrap, { backgroundColor: Colors.green + '20' }]}>
                    <Ionicons name="layers" size={20} color={Colors.green} />
                  </View>
                  <Text style={styles.statValue}>{uniqueTopics}</Text>
                  <Text style={styles.statLabel}>Topics</Text>
                </View>
              </View>

              {/* ── Scan Card ── */}
              <View style={styles.scanCard}>
                {pendingPhoto ? (
                  /* Photo selected — show preview + actions */
                  <View>
                    <Image source={{ uri: pendingPhoto }} style={styles.scanPreviewImage} resizeMode="cover" />
                    <View style={styles.scanPreviewOverlay}>
                      <Ionicons name="checkmark-circle" size={18} color={Colors.white} />
                      <Text style={styles.scanPreviewOverlayText}>Photo ready</Text>
                    </View>
                    <View style={styles.scanPreviewActions}>
                      <TouchableOpacity style={styles.scanRemoveBtn} onPress={() => setPendingPhoto(null)} activeOpacity={0.7}>
                        <Ionicons name="trash-outline" size={16} color={Colors.secondary} />
                        <Text style={styles.scanRemoveBtnText}>Remove</Text>
                      </TouchableOpacity>
                      <TouchableOpacity
                        style={styles.scanSolveBtn}
                        onPress={handleSend}
                        disabled={chatLoading || analyzing}
                        activeOpacity={0.8}
                      >
                        <Ionicons name="sparkles" size={16} color={Colors.white} />
                        <Text style={styles.scanSolveBtnText}>Solve with AI</Text>
                      </TouchableOpacity>
                    </View>
                  </View>
                ) : (
                  /* No photo — show upload area */
                  <View style={styles.scanUploadArea}>
                    <View style={styles.scanIconRow}>
                      <View style={styles.scanIconCircle}>
                        <Ionicons name="scan-outline" size={32} color={Colors.primary} />
                      </View>
                    </View>
                    <Text style={styles.scanTitle}>Scan your math problem</Text>
                    <Text style={styles.scanSub}>
                      Take a photo or choose from your library and the AI will help you solve it
                    </Text>
                    <View style={styles.scanButtonRow}>
                      <TouchableOpacity style={styles.scanCameraBtn} onPress={handleTakePhoto} activeOpacity={0.8}>
                        <Ionicons name="camera" size={20} color={Colors.white} />
                        <Text style={styles.scanCameraBtnText}>Take Photo</Text>
                      </TouchableOpacity>
                      <TouchableOpacity style={styles.scanGalleryBtn} onPress={handleUploadPhoto} activeOpacity={0.8}>
                        <Ionicons name="images-outline" size={20} color={Colors.primary} />
                        <Text style={styles.scanGalleryBtnText}>Photo Library</Text>
                      </TouchableOpacity>
                    </View>
                  </View>
                )}
              </View>

              {/* Quick Questions */}
              <View style={styles.quickSection}>
                <Text style={styles.quickLabel}>Or ask a question</Text>
                <View style={styles.quickChips}>
                  {quickQuestions.map((q, index) => (
                    <TouchableOpacity
                      key={`${q.category}-${index}`}
                      style={styles.quickChip}
                      onPress={() => handleSend(q.text)}
                      activeOpacity={0.7}
                    >
                      <Ionicons name={q.icon as any} size={13} color={Colors.primary} />
                      <Text style={styles.quickChipText} numberOfLines={1}>{q.text}</Text>
                    </TouchableOpacity>
                  ))}
                </View>
              </View>

              {/* ── Saved Sessions ── */}
              <View style={styles.section}>
                <View style={styles.sectionHeader}>
                  <Text style={styles.sectionTitle}>Recent Sessions</Text>
                </View>
                {recentSessions.length === 0 ? (
                  <View style={styles.emptyState}>
                    <Ionicons name="chatbubbles-outline" size={32} color={Colors.textMuted} />
                    <Text style={styles.emptyStateTitle}>No sessions yet</Text>
                    <Text style={styles.emptyStateSub}>
                      Start a conversation and save it to pick up later
                    </Text>
                  </View>
                ) : (
                  recentSessions.map((session) => (
                    <TouchableOpacity
                      key={session.id}
                      style={styles.sessionCard}
                      onPress={() => handleResumeSession(session)}
                      activeOpacity={0.7}
                    >
                      {/* Left accent */}
                      <View style={styles.sessionAccent} />

                      {/* Content */}
                      <View style={styles.sessionContent}>
                        <View style={styles.sessionTopRow}>
                          <Text style={styles.sessionTitle} numberOfLines={1}>
                            {session.title}
                          </Text>
                          <Text style={styles.sessionDate}>
                            {formatSessionDate(session.updatedAt)}
                          </Text>
                        </View>

                        <Text style={styles.sessionPreview} numberOfLines={2}>
                          {session.preview}
                        </Text>

                        <View style={styles.sessionMeta}>
                          <View style={styles.sessionMetaPill}>
                            <Ionicons name="chatbubble-outline" size={11} color={Colors.primary} />
                            <Text style={styles.sessionMetaText}>
                              {session.messages.length} messages
                            </Text>
                          </View>
                          {session.analysis && (
                            <View style={[styles.sessionMetaPill, { backgroundColor: Colors.teal + '15' }]}>
                              <Ionicons name="school-outline" size={11} color={Colors.teal} />
                              <Text style={[styles.sessionMetaText, { color: Colors.teal }]}>
                                {session.analysis.topic}
                              </Text>
                            </View>
                          )}
                        </View>
                      </View>

                      {/* Delete */}
                      <TouchableOpacity
                        style={styles.sessionDeleteBtn}
                        onPress={() => handleDeleteSession(session.id)}
                        hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
                      >
                        <Ionicons name="trash-outline" size={16} color={Colors.textMuted} />
                      </TouchableOpacity>
                    </TouchableOpacity>
                  ))
                )}
              </View>

              {/* Recently Saved Problems */}
              <View style={styles.section}>
                <View style={styles.sectionHeader}>
                  <Text style={styles.sectionTitle}>Recently Saved</Text>
                  {savedItems.length > 0 && (
                    <TouchableOpacity onPress={() => router.push('/(tabs)/saved')}>
                      <Text style={styles.seeAll}>See all</Text>
                    </TouchableOpacity>
                  )}
                </View>
                {recentSaved.length === 0 ? (
                  <View style={styles.emptyState}>
                    <Ionicons name="bookmark-outline" size={32} color={Colors.textMuted} />
                    <Text style={styles.emptyStateTitle}>No saved problems yet</Text>
                    <Text style={styles.emptyStateSub}>
                      Your solved problems will appear here
                    </Text>
                  </View>
                ) : (
                  recentSaved.map((item) => (
                    <View key={item.id} style={styles.recentCard}>
                      <Image source={{ uri: item.imageUri }} style={styles.recentThumb} resizeMode="cover" />
                      <View style={styles.recentInfo}>
                        <View style={[styles.topicBadge, { backgroundColor: Colors.primary + '18' }]}>
                          <Text style={[styles.topicBadgeText, { color: Colors.primary }]}>{item.analysis.topic}</Text>
                        </View>
                        <Text style={styles.recentProblem} numberOfLines={2}>{item.analysis.problem}</Text>
                        <Text style={styles.recentAnswer} numberOfLines={1}>{item.analysis.answer}</Text>
                      </View>
                    </View>
                  ))
                )}
              </View>
            </>
          )}

          {/* ── Chat View ── */}
          {chatActive && (
            <View style={styles.chatArea}>
              {/* Analysis badge */}
              {analysisResult && (
                <View style={styles.analysisBadge}>
                  <View style={styles.analysisBadgeIcon}>
                    <Ionicons name="checkmark-circle" size={16} color={Colors.green} />
                  </View>
                  <View style={styles.analysisBadgeContent}>
                    <Text style={styles.analysisBadgeLabel}>
                      {analysisResult.topic} · {analysisResult.difficulty}
                    </Text>
                    <Text style={styles.analysisBadgeText} numberOfLines={2}>
                      {analysisResult.problem}
                    </Text>
                  </View>
                </View>
              )}

              {/* Session saved indicator */}
              {sessionSaved && (
                <View style={styles.savedIndicator}>
                  <Ionicons name="checkmark-circle" size={14} color={Colors.green} />
                  <Text style={styles.savedIndicatorText}>Session saved</Text>
                </View>
              )}

              {/* Messages */}
              {chatMessages.map((msg) => (
                <View key={msg.id} style={{ marginBottom: 8 }}>
                  {/* Message bubble */}
                  <View
                    style={[
                      styles.messageBubble,
                      msg.role === 'user' ? styles.userBubble : styles.assistantBubble,
                    ]}
                  >
                    {msg.role === 'assistant' && (
                      <View style={styles.tutorAvatar}>
                        <Ionicons name="school" size={14} color={Colors.primary} />
                      </View>
                    )}

                    <View
                        style={[
                          styles.bubbleContent,
                          msg.role === 'user' ? styles.userBubbleContent : styles.assistantBubbleContent,
                        ]}
                      >
                        {msg.imageUri && (
                          <Image source={{ uri: msg.imageUri }} style={styles.bubbleImage} resizeMode="cover" />
                        )}
                        {msg.role === 'assistant' ? (
                          <ResponseBubble
                            content={msg.content}
                            topic={msg.topic}
                            mode={msg.mode}
                            tools={msg.tools}
                            graphs={msg.graphs}
                            onExplainMore={(stepNum, stepContent) => {
                              setChatInput(`Can you explain Step ${stepNum} more simply? The part about: ${stepContent.slice(0, 100)}`);
                            }}
                          />
                        ) : (
                          <Text style={[styles.bubbleText, styles.userBubbleText]}>{msg.content}</Text>
                        )}
                      </View>
                  </View>

                  {/* Reactions below assistant messages */}
                  {msg.role === 'assistant' && (
                    <MessageReactions
                      messageId={msg.id}
                      onHelpful={() => {}}
                      onConfused={() => handleStillConfused(msg.content)}
                    />
                  )}
                </View>
              ))}

              {/* Suggestion chips after last assistant message */}
              {chatMessages.length > 0 && !chatLoading && !analyzing && (() => {
                const lastMsg = chatMessages[chatMessages.length - 1];
                if (lastMsg?.role === 'assistant' && lastMsg.suggestions?.length) {
                  return (
                    <SuggestionChips
                      suggestions={lastMsg.suggestions}
                      onPress={(text) => {
                        setChatInput(text);
                        setTimeout(() => {
                          setChatInput(text);
                        }, 100);
                      }}
                    />
                  );
                }
                return null;
              })()}

              {/* Animated tool status */}
              <ToolStatus isLoading={chatLoading || analyzing} />

              {/* Error */}
              {chatError && (
                <View style={styles.chatErrorCard}>
                  <Ionicons name="alert-circle-outline" size={16} color={Colors.secondary} />
                  <Text style={styles.chatErrorText}>{chatError}</Text>
                  <TouchableOpacity onPress={() => handleSend(lastAttemptedMessage.current || undefined)}>
                    <Text style={styles.retryText}>Retry</Text>
                  </TouchableOpacity>
                </View>
              )}
            </View>
          )}
        </ScrollView>

        {/* ── AI Input Bar ── */}
        <View style={[styles.inputBarWrap, { paddingBottom: Math.max(insets.bottom, 12) }]}>
          {/* Mode selector */}
          <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.modeScrollBar}>
            <View style={styles.modeRowBar}>
              {MODE_OPTIONS.map((m) => {
                const active = selectedMode === m.key;
                return (
                  <TouchableOpacity
                    key={m.label}
                    style={[styles.modeChip, active && styles.modeChipActive]}
                    onPress={() => setSelectedMode(m.key)}
                    activeOpacity={0.7}
                  >
                    <Ionicons
                      name={m.icon as any}
                      size={13}
                      color={active ? Colors.white : Colors.primary}
                    />
                    <Text style={[styles.modeChipText, active && styles.modeChipTextActive]}>
                      {m.label}
                    </Text>
                  </TouchableOpacity>
                );
              })}
            </View>
          </ScrollView>
          {/* Attachment menu */}
          {attachMenuOpen && !pendingPhoto && (
            <View style={styles.attachMenu}>
              <TouchableOpacity
                style={styles.attachOption}
                onPress={handleTakePhoto}
                activeOpacity={0.7}
              >
                <View style={[styles.attachOptionIcon, { backgroundColor: Colors.teal + '18' }]}>
                  <Ionicons name="camera" size={22} color={Colors.teal} />
                </View>
                <View>
                  <Text style={styles.attachOptionTitle}>Take Photo</Text>
                  <Text style={styles.attachOptionSub}>Use your camera</Text>
                </View>
              </TouchableOpacity>
              <View style={styles.attachDivider} />
              <TouchableOpacity
                style={styles.attachOption}
                onPress={handleUploadPhoto}
                activeOpacity={0.7}
              >
                <View style={[styles.attachOptionIcon, { backgroundColor: Colors.primary + '18' }]}>
                  <Ionicons name="images" size={22} color={Colors.primary} />
                </View>
                <View>
                  <Text style={styles.attachOptionTitle}>Photo Library</Text>
                  <Text style={styles.attachOptionSub}>Choose from gallery</Text>
                </View>
              </TouchableOpacity>
            </View>
          )}

          {/* Pending photo preview */}
          {pendingPhoto && (
            <View style={styles.photoPreviewRow}>
              <Image source={{ uri: pendingPhoto }} style={styles.photoPreviewThumb} resizeMode="cover" />
              <View style={styles.photoPreviewInfo}>
                <Ionicons name="image" size={14} color={Colors.primary} />
                <Text style={styles.photoPreviewText}>Photo attached</Text>
              </View>
              <TouchableOpacity
                style={styles.photoPreviewRemove}
                onPress={() => setPendingPhoto(null)}
                activeOpacity={0.7}
              >
                <Ionicons name="close-circle" size={20} color={Colors.textMuted} />
              </TouchableOpacity>
            </View>
          )}

          {/* Input row */}
          <View style={styles.inputRow}>
            {/* Attach / close button */}
            <TouchableOpacity
              style={[styles.attachBtn, attachMenuOpen && styles.attachBtnActive]}
              onPress={() => setAttachMenuOpen((v) => !v)}
              activeOpacity={0.7}
            >
              <Ionicons
                name={attachMenuOpen ? 'close' : 'add'}
                size={24}
                color={attachMenuOpen ? Colors.white : Colors.primary}
              />
            </TouchableOpacity>

            <TextInput
              style={styles.textInput}
              value={chatInput}
              onChangeText={setChatInput}
              placeholder={pendingPhoto ? 'Add instructions (optional)...' : 'Ask about your math problem...'}
              placeholderTextColor={Colors.textMuted}
              multiline
              maxLength={2000}
              onSubmitEditing={handleSend}
              blurOnSubmit={false}
              onFocus={() => setAttachMenuOpen(false)}
            />

            <TouchableOpacity
              style={[
                styles.sendBtn,
                (!chatInput.trim() && !pendingPhoto) || chatLoading || analyzing || !agentSessionId
                  ? styles.sendBtnDisabled
                  : null,
              ]}
              onPress={handleSend}
              disabled={(!chatInput.trim() && !pendingPhoto) || chatLoading || analyzing || !agentSessionId}
              activeOpacity={0.7}
            >
              <Ionicons name="arrow-up" size={20} color={Colors.white} />
            </TouchableOpacity>
          </View>
        </View>
      </KeyboardAvoidingView>
    </View>
  );
}

// ─── Styles ──────────────────────────────────────────────────────────────────
const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },

  // Header
  header: {
    backgroundColor: Colors.primary,
    paddingHorizontal: 20,
    paddingBottom: 20,
    borderBottomLeftRadius: 24,
    borderBottomRightRadius: 24,
  },
  headerTop: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  greeting: { fontSize: 22, fontWeight: '700', color: Colors.white, marginBottom: 4 },
  subGreeting: { fontSize: 14, color: 'rgba(255,255,255,0.75)' },
  headerActions: { flexDirection: 'row', gap: 8 },
  headerActionBtn: {
    flexDirection: 'row', alignItems: 'center', gap: 5,
    backgroundColor: 'rgba(255,255,255,0.2)',
    paddingHorizontal: 12, paddingVertical: 8, borderRadius: 12,
  },
  headerActionBtnSaved: {
    backgroundColor: 'rgba(46,204,113,0.35)',
  },
  headerActionBtnExit: {
    backgroundColor: 'rgba(255,255,255,0.12)',
  },
  headerActionText: { color: Colors.white, fontWeight: '600', fontSize: 13 },
  avatarBtn: {},
  avatar: {
    width: 42, height: 42, borderRadius: 21,
    backgroundColor: 'rgba(255,255,255,0.25)',
    alignItems: 'center', justifyContent: 'center',
    borderWidth: 2, borderColor: 'rgba(255,255,255,0.4)',
  },

  // Scroll
  scroll: { flex: 1 },
  scrollContent: { padding: 16, paddingBottom: 8 },

  // Stats
  statsRow: { flexDirection: 'row', gap: 10, marginBottom: 20 },
  statCard: {
    flex: 1, backgroundColor: Colors.card, borderRadius: 16,
    padding: 14, alignItems: 'center', gap: 6,
    shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.06, shadowRadius: 8, elevation: 2,
  },
  statIconWrap: { width: 38, height: 38, borderRadius: 10, alignItems: 'center', justifyContent: 'center' },
  statValue: { fontSize: 20, fontWeight: '700', color: Colors.text },
  statLabel: { fontSize: 11, color: Colors.textLight, fontWeight: '500' },

  // Scan Card
  scanCard: {
    backgroundColor: Colors.card, borderRadius: 20, overflow: 'hidden', marginBottom: 16,
    shadowColor: '#000', shadowOffset: { width: 0, height: 3 }, shadowOpacity: 0.08, shadowRadius: 12, elevation: 3,
  },
  // Upload area (no photo)
  scanUploadArea: {
    alignItems: 'center', paddingVertical: 28, paddingHorizontal: 24, gap: 10,
  },
  scanIconRow: { marginBottom: 4 },
  scanIconCircle: {
    width: 72, height: 72, borderRadius: 22,
    backgroundColor: Colors.primaryLight, alignItems: 'center', justifyContent: 'center',
    borderWidth: 2, borderColor: Colors.primary + '20',
  },
  scanTitle: { fontSize: 18, fontWeight: '700', color: Colors.text },
  scanSub: { fontSize: 14, color: Colors.textLight, textAlign: 'center', lineHeight: 20 },
  scanButtonRow: { flexDirection: 'row', gap: 12, marginTop: 8, width: '100%' },
  scanCameraBtn: {
    flex: 1, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8,
    backgroundColor: Colors.primary, paddingVertical: 14, borderRadius: 14,
  },
  scanCameraBtnText: { color: Colors.white, fontWeight: '700', fontSize: 15 },
  scanGalleryBtn: {
    flex: 1, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8,
    backgroundColor: Colors.primaryLight, paddingVertical: 14, borderRadius: 14,
    borderWidth: 1.5, borderColor: Colors.primary + '30',
  },
  scanGalleryBtnText: { color: Colors.primary, fontWeight: '700', fontSize: 15 },
  // Preview state (photo selected)
  scanPreviewImage: { width: '100%', height: 200 },
  scanPreviewOverlay: {
    position: 'absolute', top: 0, left: 0, right: 0, height: 200,
    backgroundColor: 'rgba(0,0,0,0.15)',
    flexDirection: 'row', alignItems: 'flex-end', justifyContent: 'flex-start',
    paddingHorizontal: 14, paddingBottom: 12, gap: 6,
  },
  scanPreviewOverlayText: { color: Colors.white, fontSize: 13, fontWeight: '600' },
  scanPreviewActions: {
    flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center',
    paddingHorizontal: 14, paddingVertical: 12, gap: 12,
    borderTopWidth: 1, borderTopColor: Colors.border,
  },
  scanRemoveBtn: {
    flexDirection: 'row', alignItems: 'center', gap: 6,
    paddingHorizontal: 14, paddingVertical: 10, borderRadius: 10,
    backgroundColor: Colors.secondary + '12',
    borderWidth: 1, borderColor: Colors.secondary + '25',
  },
  scanRemoveBtnText: { fontSize: 14, fontWeight: '600', color: Colors.secondary },
  scanSolveBtn: {
    flex: 1, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8,
    backgroundColor: Colors.primary, paddingVertical: 12, borderRadius: 12,
  },
  scanSolveBtnText: { color: Colors.white, fontWeight: '700', fontSize: 15 },

  // Quick questions
  quickSection: { marginBottom: 20 },
  quickLabel: { fontSize: 13, fontWeight: '600', color: Colors.textLight, marginBottom: 10 },
  quickChips: { gap: 8 },
  quickChip: {
    flexDirection: 'row', alignItems: 'center', gap: 8,
    backgroundColor: Colors.card, borderRadius: 12, padding: 13,
    borderWidth: 1, borderColor: Colors.border,
  },
  quickChipText: { fontSize: 14, color: Colors.primary, fontWeight: '500' },

  // Sections
  section: { marginBottom: 24 },
  sectionHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 },
  sectionTitle: { fontSize: 17, fontWeight: '700', color: Colors.text, marginBottom: 4 },
  seeAll: { fontSize: 14, color: Colors.primary, fontWeight: '600' },

  // Empty state
  emptyState: {
    backgroundColor: Colors.card, borderRadius: 16, padding: 28,
    alignItems: 'center', gap: 8,
    borderWidth: 1, borderColor: Colors.border, borderStyle: 'dashed',
  },
  emptyStateTitle: { fontSize: 15, fontWeight: '700', color: Colors.textLight },
  emptyStateSub: { fontSize: 13, color: Colors.textMuted, textAlign: 'center' },

  // ── Session Cards ──
  sessionCard: {
    backgroundColor: Colors.card, borderRadius: 14,
    flexDirection: 'row', overflow: 'hidden', marginBottom: 10,
    shadowColor: '#000', shadowOffset: { width: 0, height: 1 }, shadowOpacity: 0.05, shadowRadius: 4, elevation: 1,
  },
  sessionAccent: {
    width: 4, backgroundColor: Colors.primary,
  },
  sessionContent: {
    flex: 1, padding: 14, gap: 6,
  },
  sessionTopRow: {
    flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center',
  },
  sessionTitle: {
    flex: 1, fontSize: 14, fontWeight: '700', color: Colors.text, marginRight: 8,
  },
  sessionDate: { fontSize: 11, color: Colors.textMuted },
  sessionPreview: {
    fontSize: 13, color: Colors.textLight, lineHeight: 18,
  },
  sessionMeta: {
    flexDirection: 'row', gap: 8, marginTop: 2,
  },
  sessionMetaPill: {
    flexDirection: 'row', alignItems: 'center', gap: 4,
    backgroundColor: Colors.primaryLight, borderRadius: 8,
    paddingHorizontal: 8, paddingVertical: 3,
  },
  sessionMetaText: { fontSize: 11, fontWeight: '600', color: Colors.primary },
  sessionDeleteBtn: {
    justifyContent: 'center', paddingHorizontal: 14,
  },

  // Recent problem cards
  recentCard: {
    backgroundColor: Colors.card, borderRadius: 14,
    flexDirection: 'row', overflow: 'hidden', marginBottom: 10,
    shadowColor: '#000', shadowOffset: { width: 0, height: 1 }, shadowOpacity: 0.05, shadowRadius: 4, elevation: 1,
  },
  recentThumb: { width: 80, height: 80 },
  recentInfo: { flex: 1, padding: 12, gap: 5, justifyContent: 'center' },
  topicBadge: { alignSelf: 'flex-start', paddingHorizontal: 8, paddingVertical: 3, borderRadius: 6 },
  topicBadgeText: { fontSize: 11, fontWeight: '600' },
  recentProblem: { fontSize: 13, color: Colors.text, fontWeight: '500', lineHeight: 18 },
  recentAnswer: { fontSize: 12, color: Colors.textLight },

  // ── Chat Area ──
  chatArea: { paddingBottom: 8 },

  // Saved indicator
  savedIndicator: {
    flexDirection: 'row', alignItems: 'center', justifyContent: 'center',
    gap: 6, paddingVertical: 8, marginBottom: 12,
    backgroundColor: Colors.green + '12', borderRadius: 10,
  },
  savedIndicatorText: { fontSize: 12, fontWeight: '600', color: Colors.green },

  // Analysis badge
  analysisBadge: {
    flexDirection: 'row', alignItems: 'center', gap: 10,
    backgroundColor: Colors.card, borderRadius: 14, padding: 12,
    marginBottom: 16,
    borderWidth: 1, borderColor: Colors.green + '30',
    shadowColor: '#000', shadowOffset: { width: 0, height: 1 }, shadowOpacity: 0.04, shadowRadius: 4, elevation: 1,
  },
  analysisBadgeIcon: {
    width: 32, height: 32, borderRadius: 10,
    backgroundColor: Colors.green + '15', alignItems: 'center', justifyContent: 'center',
  },
  analysisBadgeContent: { flex: 1 },
  analysisBadgeLabel: { fontSize: 11, fontWeight: '700', color: Colors.textLight, letterSpacing: 0.5, marginBottom: 2 },
  analysisBadgeText: { fontSize: 14, fontWeight: '600', color: Colors.text, lineHeight: 20 },

  // Chat bubbles
  messageBubble: { marginBottom: 14 },
  userBubble: { alignItems: 'flex-end' },
  assistantBubble: { flexDirection: 'row', alignItems: 'flex-start', gap: 8 },
  tutorAvatar: {
    width: 28, height: 28, borderRadius: 14,
    backgroundColor: Colors.primaryLight, alignItems: 'center', justifyContent: 'center',
    marginTop: 2,
    flexShrink: 0,
  },
  bubbleContent: {
    flex: 1,
    maxWidth: '85%',
    borderRadius: 18,
    padding: 14,
  },
  userBubbleContent: {
    backgroundColor: Colors.primary,
    borderBottomRightRadius: 4,
    maxWidth: '80%',
    flex: 0,
  },
  assistantBubbleContent: {
    backgroundColor: Colors.card,
    borderBottomLeftRadius: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 1,
    flex: 1,
    maxWidth: undefined,
  },
  bubbleImage: {
    width: '100%', height: 160, borderRadius: 12, marginBottom: 8,
  },
  bubbleText: { fontSize: 15, lineHeight: 22 },
  userBubbleText: { color: Colors.white },
  assistantBubbleText: { color: Colors.text },

  // Thinking
  thinkingRow: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  thinkingDot: {
    width: 8, height: 8, borderRadius: 4,
    backgroundColor: Colors.primary,
  },
  thinkingText: { fontSize: 13, color: Colors.textLight },

  // Chat error
  chatErrorCard: {
    flexDirection: 'row', alignItems: 'center', gap: 8,
    backgroundColor: Colors.secondary + '12', borderRadius: 12, padding: 12,
    marginBottom: 8,
  },
  chatErrorText: { flex: 1, fontSize: 13, color: Colors.text },
  retryText: { fontSize: 13, fontWeight: '700', color: Colors.primary },

  // ── AI Input Bar ──
  inputBarWrap: {
    backgroundColor: Colors.card,
    borderTopWidth: 1, borderTopColor: Colors.border,
    paddingTop: 10,
    paddingHorizontal: 14,
  },

  photoPreviewRow: {
    flexDirection: 'row', alignItems: 'center', gap: 10,
    backgroundColor: Colors.primaryLight,
    borderRadius: 12, padding: 8,
    marginBottom: 10,
  },
  photoPreviewThumb: {
    width: 44, height: 44, borderRadius: 8,
  },
  photoPreviewInfo: {
    flex: 1, flexDirection: 'row', alignItems: 'center', gap: 6,
  },
  photoPreviewText: { fontSize: 13, color: Colors.primary, fontWeight: '600' },
  photoPreviewRemove: { padding: 4 },

  // Attachment menu
  attachMenu: {
    backgroundColor: Colors.background, borderRadius: 16,
    marginBottom: 10, overflow: 'hidden',
    borderWidth: 1, borderColor: Colors.border,
  },
  attachOption: {
    flexDirection: 'row', alignItems: 'center', gap: 12,
    paddingHorizontal: 14, paddingVertical: 12,
  },
  attachOptionIcon: {
    width: 42, height: 42, borderRadius: 12,
    alignItems: 'center', justifyContent: 'center',
  },
  attachOptionTitle: { fontSize: 15, fontWeight: '600', color: Colors.text },
  attachOptionSub: { fontSize: 12, color: Colors.textLight, marginTop: 1 },
  attachDivider: { height: 1, backgroundColor: Colors.border, marginHorizontal: 14 },

  inputRow: {
    flexDirection: 'row', alignItems: 'flex-end', gap: 8,
  },
  attachBtn: {
    width: 42, height: 42, borderRadius: 21,
    backgroundColor: Colors.primaryLight,
    alignItems: 'center', justifyContent: 'center',
    marginBottom: 1,
  },
  attachBtnActive: {
    backgroundColor: Colors.primary,
  },
  textInput: {
    flex: 1, fontSize: 15, color: Colors.text,
    backgroundColor: Colors.background, borderRadius: 22,
    paddingHorizontal: 16, paddingVertical: 11,
    maxHeight: 100, borderWidth: 1, borderColor: Colors.border,
  },
  sendBtn: {
    width: 42, height: 42, borderRadius: 21,
    backgroundColor: Colors.primary,
    alignItems: 'center', justifyContent: 'center',
    marginBottom: 1,
  },
  sendBtnDisabled: { opacity: 0.35 },

  // ── Solve Breakdown ──
  solveCard: {
    width: '100%', gap: 10,
  },
  solveAnswerCard: {
    backgroundColor: Colors.card, borderRadius: 16, padding: 16,
    borderWidth: 1.5, borderColor: Colors.green + '40',
    shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.06, shadowRadius: 8, elevation: 2,
  },
  solveAnswerHeader: {
    flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 8,
  },
  solveAnswerLabel: { fontSize: 13, fontWeight: '700', color: Colors.green, letterSpacing: 0.5 },
  solveAnswerText: { fontSize: 22, fontWeight: '800', color: Colors.text, marginBottom: 10, lineHeight: 30 },
  solveMetaRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 6 },
  solvePill: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 8 },
  solvePillText: { fontSize: 11, fontWeight: '700' },

  solveProblemCard: {
    backgroundColor: Colors.card, borderRadius: 14, padding: 14,
    borderWidth: 1, borderColor: Colors.border,
  },
  solveSectionLabel: { fontSize: 12, fontWeight: '700', color: Colors.textLight, letterSpacing: 0.4, marginBottom: 6 },
  solveProblemText: { fontSize: 15, color: Colors.text, lineHeight: 22 },

  solveStepsCard: {
    backgroundColor: Colors.card, borderRadius: 14, padding: 14,
    borderWidth: 1, borderColor: Colors.border,
  },
  solveStep: {
    backgroundColor: Colors.background, borderRadius: 12, padding: 12,
    marginTop: 8,
  },
  solveStepHeader: {
    flexDirection: 'row', alignItems: 'center', gap: 10,
  },
  solveStepNumber: {
    width: 26, height: 26, borderRadius: 13,
    backgroundColor: Colors.primary, alignItems: 'center', justifyContent: 'center',
  },
  solveStepNumberText: { fontSize: 13, fontWeight: '800', color: Colors.white },
  solveStepTitle: { flex: 1, fontSize: 14, fontWeight: '700', color: Colors.text },
  solveStepMath: {
    backgroundColor: Colors.primaryLight, borderRadius: 8, padding: 10, marginTop: 8,
    borderLeftWidth: 3, borderLeftColor: Colors.primary,
  },
  solveStepMathText: { fontSize: 14, fontWeight: '600', color: Colors.primaryDark, fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace' },
  solveStepExpanded: { marginTop: 8 },
  solveStepExplanation: { fontSize: 14, color: Colors.text, lineHeight: 21 },
  solveStepNote: {
    flexDirection: 'row', alignItems: 'flex-start', gap: 6, marginTop: 8,
    backgroundColor: Colors.orange + '10', borderRadius: 8, padding: 8,
  },
  solveStepNoteText: { flex: 1, fontSize: 13, color: Colors.text, lineHeight: 19 },

  solveVerifyCard: {
    flexDirection: 'row', alignItems: 'flex-start', gap: 10,
    backgroundColor: Colors.green + '10', borderRadius: 14, padding: 14,
    borderWidth: 1, borderColor: Colors.green + '25',
  },
  solveVerifyText: { fontSize: 14, color: Colors.text, lineHeight: 20 },

  solveExtrasCard: {
    backgroundColor: Colors.card, borderRadius: 14, padding: 14,
    borderWidth: 1, borderColor: Colors.border,
  },
  solveConceptsRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 6 },
  solveConceptChip: {
    backgroundColor: Colors.primaryLight, borderRadius: 8,
    paddingHorizontal: 10, paddingVertical: 5,
  },
  solveConceptChipText: { fontSize: 12, fontWeight: '600', color: Colors.primary },
  solveTipRow: {
    flexDirection: 'row', alignItems: 'flex-start', gap: 8,
    backgroundColor: Colors.orange + '10', borderRadius: 10, padding: 10,
  },
  solveTipText: { flex: 1, fontSize: 13, color: Colors.text, lineHeight: 19 },

  // Mode selector in input bar
  modeScrollBar: { marginBottom: 8 },
  modeRowBar: { flexDirection: 'row', gap: 6, paddingHorizontal: 4 },
  modeChip: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 14,
    backgroundColor: Colors.primaryLight || '#EDE9FF',
    borderWidth: 1,
    borderColor: 'transparent',
  },
  modeChipActive: {
    backgroundColor: Colors.primary,
    borderColor: Colors.primary,
  },
  modeChipText: {
    fontSize: 11,
    fontWeight: '600',
    color: Colors.primary,
  },
  modeChipTextActive: {
    color: Colors.white || '#FFF',
  },
});
