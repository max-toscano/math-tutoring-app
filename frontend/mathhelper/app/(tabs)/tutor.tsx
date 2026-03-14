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
} from 'react-native';
import { useState, useRef } from 'react';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Colors } from '../../constants/Colors';
import { sendTutoringMessage, type Message } from '../../services/tutoring';

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

const MODE_OPTIONS = [
  { key: null, label: 'Auto', icon: 'sparkles-outline' },
  { key: 'direct', label: 'Explain', icon: 'bulb-outline' },
  { key: 'socratic', label: 'Guide Me', icon: 'help-circle-outline' },
  { key: 'hint', label: 'Hint', icon: 'eye-outline' },
  { key: 'check_work', label: 'Check Work', icon: 'checkmark-circle-outline' },
] as const;

export default function TutorScreen() {
  const insets = useSafeAreaInsets();
  const scrollRef = useRef<ScrollView>(null);

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [conversationHistory, setConversationHistory] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedMode, setSelectedMode] = useState<string | null>(null);

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
      const result = await sendTutoringMessage(text, {
        mode: selectedMode ?? undefined,
        conversationHistory,
      });

      const assistantMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: result.response_text ?? result.response ?? '',
      };

      setMessages((prev) => [...prev, assistantMsg]);
      setConversationHistory(result.conversation_history);
    } catch (e: any) {
      setError(e.message ?? 'Something went wrong.');
    } finally {
      setLoading(false);
      setTimeout(() => scrollRef.current?.scrollToEnd({ animated: true }), 100);
    }
  }

  function handleNewChat() {
    setMessages([]);
    setConversationHistory([]);
    setError(null);
    setInput('');
  }

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={[styles.header, { paddingTop: insets.top + 12 }]}>
        <View style={styles.headerRow}>
          <View>
            <Text style={styles.headerTitle}>Math Tutor</Text>
            <Text style={styles.headerSub}>Ask me anything</Text>
          </View>
          <TouchableOpacity style={styles.newChatBtn} onPress={handleNewChat}>
            <Ionicons name="add" size={22} color={Colors.white} />
          </TouchableOpacity>
        </View>

        {/* Mode Selector */}
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.modeScroll}>
          <View style={styles.modeRow}>
            {MODE_OPTIONS.map((mode) => {
              const active = selectedMode === mode.key;
              return (
                <TouchableOpacity
                  key={mode.label}
                  style={[styles.modePill, active && styles.modePillActive]}
                  onPress={() => setSelectedMode(mode.key)}
                  activeOpacity={0.7}
                >
                  <Ionicons
                    name={mode.icon as any}
                    size={14}
                    color={active ? Colors.primary : 'rgba(255,255,255,0.7)'}
                  />
                  <Text style={[styles.modePillText, active && styles.modePillTextActive]}>
                    {mode.label}
                  </Text>
                </TouchableOpacity>
              );
            })}
          </View>
        </ScrollView>
      </View>

      {/* Messages */}
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
          {messages.length === 0 && !loading && (
            <View style={styles.emptyState}>
              <View style={styles.emptyIcon}>
                <Ionicons name="school-outline" size={48} color={Colors.primary} />
              </View>
              <Text style={styles.emptyTitle}>Ready to learn!</Text>
              <Text style={styles.emptySub}>
                Type a math question below and I'll help you understand it step by step.
              </Text>
              <View style={styles.suggestions}>
                {[
                  'How do I solve 2x + 5 = 15?',
                  'Explain the Pythagorean theorem',
                  'What is a derivative?',
                ].map((s) => (
                  <TouchableOpacity
                    key={s}
                    style={styles.suggestionPill}
                    onPress={() => setInput(s)}
                    activeOpacity={0.7}
                  >
                    <Text style={styles.suggestionText}>{s}</Text>
                  </TouchableOpacity>
                ))}
              </View>
            </View>
          )}

          {messages.map((msg) => (
            <View
              key={msg.id}
              style={[
                styles.messageBubble,
                msg.role === 'user' ? styles.userBubble : styles.assistantBubble,
              ]}
            >
              {msg.role === 'assistant' && (
                <View style={styles.assistantAvatar}>
                  <Ionicons name="school" size={14} color={Colors.primary} />
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
              </View>
            </View>
          ))}

          {loading && (
            <View style={[styles.messageBubble, styles.assistantBubble]}>
              <View style={styles.assistantAvatar}>
                <Ionicons name="school" size={14} color={Colors.primary} />
              </View>
              <View style={[styles.bubbleContent, styles.assistantBubbleContent]}>
                <ActivityIndicator size="small" color={Colors.primary} />
                <Text style={styles.thinkingText}>Thinking...</Text>
              </View>
            </View>
          )}

          {error && (
            <View style={styles.errorCard}>
              <Ionicons name="alert-circle-outline" size={18} color={Colors.secondary} />
              <Text style={styles.errorText}>{error}</Text>
              <TouchableOpacity onPress={handleSend}>
                <Text style={styles.retryText}>Retry</Text>
              </TouchableOpacity>
            </View>
          )}
        </ScrollView>

        {/* Input */}
        <View style={[styles.inputBar, { paddingBottom: Math.max(insets.bottom, 12) }]}>
          <TextInput
            style={styles.textInput}
            value={input}
            onChangeText={setInput}
            placeholder="Ask a math question..."
            placeholderTextColor={Colors.textMuted}
            multiline
            maxLength={2000}
            onSubmitEditing={handleSend}
            blurOnSubmit={false}
          />
          <TouchableOpacity
            style={[styles.sendBtn, (!input.trim() || loading) && styles.sendBtnDisabled]}
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
    backgroundColor: Colors.primary,
    paddingHorizontal: 20,
    paddingBottom: 14,
    borderBottomLeftRadius: 24,
    borderBottomRightRadius: 24,
  },
  headerRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  headerTitle: { fontSize: 22, fontWeight: '700', color: Colors.white },
  headerSub: { fontSize: 13, color: 'rgba(255,255,255,0.7)', marginTop: 2 },
  newChatBtn: {
    width: 40, height: 40, borderRadius: 12,
    backgroundColor: 'rgba(255,255,255,0.2)',
    alignItems: 'center', justifyContent: 'center',
  },
  modeScroll: { marginBottom: 2 },
  modeRow: { flexDirection: 'row', gap: 8 },
  modePill: {
    flexDirection: 'row', alignItems: 'center', gap: 5,
    paddingHorizontal: 12, paddingVertical: 7, borderRadius: 20,
    backgroundColor: 'rgba(255,255,255,0.15)',
  },
  modePillActive: { backgroundColor: Colors.white },
  modePillText: { fontSize: 12, fontWeight: '600', color: 'rgba(255,255,255,0.8)' },
  modePillTextActive: { color: Colors.primary },

  chatArea: { flex: 1 },
  messageList: { flex: 1 },
  messageListContent: { padding: 16, paddingBottom: 8 },

  emptyState: { alignItems: 'center', paddingTop: 60, paddingHorizontal: 32, gap: 12 },
  emptyIcon: {
    width: 80, height: 80, borderRadius: 24,
    backgroundColor: Colors.primaryLight, alignItems: 'center', justifyContent: 'center',
    marginBottom: 8,
  },
  emptyTitle: { fontSize: 20, fontWeight: '700', color: Colors.text },
  emptySub: { fontSize: 14, color: Colors.textLight, textAlign: 'center', lineHeight: 21 },
  suggestions: { marginTop: 16, gap: 10, width: '100%' },
  suggestionPill: {
    backgroundColor: Colors.card, borderRadius: 14, padding: 14,
    borderWidth: 1, borderColor: Colors.border,
  },
  suggestionText: { fontSize: 14, color: Colors.primary, fontWeight: '500' },

  messageBubble: { marginBottom: 16 },
  userBubble: { alignItems: 'flex-end' },
  assistantBubble: { flexDirection: 'row', alignItems: 'flex-start', gap: 8 },
  assistantAvatar: {
    width: 28, height: 28, borderRadius: 14,
    backgroundColor: Colors.primaryLight, alignItems: 'center', justifyContent: 'center',
    marginTop: 2,
  },
  bubbleContent: { maxWidth: '80%', borderRadius: 18, padding: 14 },
  userBubbleContent: { backgroundColor: Colors.primary, borderBottomRightRadius: 4 },
  assistantBubbleContent: {
    backgroundColor: Colors.card, borderBottomLeftRadius: 4,
    shadowColor: '#000', shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05, shadowRadius: 4, elevation: 1,
  },
  bubbleText: { fontSize: 15, lineHeight: 22 },
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
    borderTopWidth: 1, borderTopColor: Colors.border,
    backgroundColor: Colors.card,
  },
  textInput: {
    flex: 1, fontSize: 15, color: Colors.text,
    backgroundColor: Colors.background, borderRadius: 20,
    paddingHorizontal: 16, paddingVertical: 10,
    maxHeight: 100, borderWidth: 1, borderColor: Colors.border,
  },
  sendBtn: {
    width: 42, height: 42, borderRadius: 21,
    backgroundColor: Colors.primary, alignItems: 'center', justifyContent: 'center',
    marginBottom: 2,
  },
  sendBtnDisabled: { opacity: 0.4 },
});
