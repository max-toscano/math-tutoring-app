import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Image,
  Modal,
  ActivityIndicator,
} from 'react-native';
import { useState, useRef } from 'react';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import * as ImagePicker from 'expo-image-picker';
import { analyzeMathImage, type MathAnalysis } from '../../services/openai';
import { useAppContext } from '../../context/AppContext';
import { Colors } from '../../constants/Colors';

const QUICK_TOPICS = [
  { name: 'Algebra', icon: 'calculator-outline', color: Colors.primary },
  { name: 'Geometry', icon: 'shapes-outline', color: Colors.teal },
  { name: 'Calculus', icon: 'trending-up-outline', color: Colors.secondary },
  { name: 'Trigonometry', icon: 'radio-outline', color: Colors.orange },
  { name: 'Statistics', icon: 'bar-chart-outline', color: Colors.green },
];

const DIFF_COLORS: Record<string, string> = {
  Easy: Colors.green,
  Medium: Colors.orange,
  Hard: Colors.secondary,
};

// ─── Analysis Results ─────────────────────────────────────────────────────────
function AnalysisResults({
  result,
  onDismiss,
  onSave,
  saved,
}: {
  result: MathAnalysis;
  onDismiss: () => void;
  onSave: () => void;
  saved: boolean;
}) {
  const diffColor = DIFF_COLORS[result.difficulty] ?? Colors.orange;

  return (
    <View style={rs.container}>
      {/* Header */}
      <View style={rs.header}>
        <View style={rs.headerLeft}>
          <Ionicons name="sparkles" size={17} color={Colors.primary} />
          <Text style={rs.headerTitle}>AI Analysis Complete</Text>
        </View>
        <TouchableOpacity onPress={onDismiss} style={rs.dismissBtn}>
          <Ionicons name="close" size={17} color={Colors.textLight} />
        </TouchableOpacity>
      </View>

      {/* Problem */}
      <View style={rs.problemBox}>
        <Text style={rs.sectionLabel}>PROBLEM DETECTED</Text>
        <Text style={rs.problemText}>{result.problem}</Text>
        <View style={rs.badgeRow}>
          <View style={[rs.badge, { backgroundColor: Colors.primaryLight }]}>
            <Text style={[rs.badgeText, { color: Colors.primary }]}>{result.topic}</Text>
          </View>
          <View style={[rs.badge, { backgroundColor: diffColor + '22' }]}>
            <Text style={[rs.badgeText, { color: diffColor }]}>{result.difficulty}</Text>
          </View>
        </View>
      </View>

      {/* Answer */}
      <View style={rs.answerBox}>
        <Text style={[rs.sectionLabel, { color: Colors.green }]}>ANSWER</Text>
        <Text style={rs.answerText}>{result.answer}</Text>
      </View>

      {/* Steps */}
      <Text style={rs.stepsHeading}>Step-by-Step Solution</Text>
      {result.steps.map((s) => (
        <View key={s.step} style={rs.stepRow}>
          <View style={rs.stepBubble}>
            <Text style={rs.stepBubbleText}>{s.step}</Text>
          </View>
          <View style={rs.stepBody}>
            <Text style={rs.stepTitle}>{s.title}</Text>
            <Text style={rs.stepExplanation}>{s.explanation}</Text>
            {s.math ? (
              <View style={rs.mathBox}>
                <Text style={rs.mathText}>{s.math}</Text>
              </View>
            ) : null}
          </View>
        </View>
      ))}

      {/* Concepts */}
      {result.concepts?.length > 0 && (
        <View style={rs.conceptsSection}>
          <Text style={rs.conceptsHeading}>Key Concepts</Text>
          <View style={rs.conceptsPills}>
            {result.concepts.map((c, i) => (
              <View key={i} style={rs.pill}>
                <Text style={rs.pillText}>{c}</Text>
              </View>
            ))}
          </View>
        </View>
      )}

      {/* Tip */}
      {result.tip ? (
        <View style={rs.tipBox}>
          <Ionicons name="bulb-outline" size={18} color={Colors.yellow} />
          <Text style={rs.tipText}>{result.tip}</Text>
        </View>
      ) : null}

      {/* Save Button */}
      <TouchableOpacity
        style={[rs.saveBtn, saved && rs.saveBtnSaved]}
        onPress={onSave}
        disabled={saved}
        activeOpacity={0.8}
      >
        <Ionicons name={saved ? 'bookmark' : 'bookmark-outline'} size={18} color={saved ? Colors.white : Colors.primary} />
        <Text style={[rs.saveBtnText, saved && rs.saveBtnTextSaved]}>
          {saved ? 'Saved to Collection' : 'Save to Collection'}
        </Text>
      </TouchableOpacity>
    </View>
  );
}

// ─── Dashboard ────────────────────────────────────────────────────────────────
export default function DashboardScreen() {
  const insets = useSafeAreaInsets();
  const router = useRouter();
  const { savedItems, saveAnalysis } = useAppContext();

  const [photoUri, setPhotoUri] = useState<string | null>(null);
  const [previewVisible, setPreviewVisible] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<MathAnalysis | null>(null);
  const [analysisError, setAnalysisError] = useState<string | null>(null);
  const [isSaved, setIsSaved] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  async function handleTakePhoto() {
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    if (status !== 'granted') return;
    const result = await ImagePicker.launchCameraAsync({ allowsEditing: true, quality: 0.9 });
    if (!result.canceled) {
      setPhotoUri(result.assets[0].uri);
      setAnalysisResult(null);
      setAnalysisError(null);
      setIsSaved(false);
      setPreviewVisible(true);
    }
  }

  async function handleUploadPhoto() {
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (status !== 'granted') return;
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      quality: 0.9,
    });
    if (!result.canceled) {
      setPhotoUri(result.assets[0].uri);
      setAnalysisResult(null);
      setAnalysisError(null);
      setIsSaved(false);
      setPreviewVisible(true);
    }
  }

  async function handleAnalyze() {
    if (!photoUri) return;
    setPreviewVisible(false);
    setAnalyzing(true);
    setAnalysisResult(null);
    setAnalysisError(null);
    setIsSaved(false);
    try {
      const result = await analyzeMathImage(photoUri);
      setAnalysisResult(result);
    } catch (e: any) {
      setAnalysisError(e.message ?? 'Something went wrong. Please try again.');
    } finally {
      setAnalyzing(false);
    }
  }

  async function handleSave() {
    if (!photoUri || !analysisResult || isSaved) return;
    setIsSaving(true);
    try {
      await saveAnalysis(photoUri, analysisResult);
      setIsSaved(true);
    } catch {
      // silently fail — user can retry
    } finally {
      setIsSaving(false);
    }
  }

  function handleClearPhoto() {
    setPhotoUri(null);
    setPreviewVisible(false);
    setAnalysisResult(null);
    setAnalysisError(null);
    setIsSaved(false);
  }

  const recentSaved = savedItems.slice(0, 3);
  const uniqueTopics = [...new Set(savedItems.map((i) => i.analysis.topic))].length;

  return (
    <View style={styles.container}>
      {/* ── Header ── */}
      <View style={[styles.header, { paddingTop: insets.top + 16 }]}>
        <View style={styles.headerTop}>
          <View>
            <Text style={styles.greeting}>Math Helper 📚</Text>
            <Text style={styles.subGreeting}>Scan a problem to get started</Text>
          </View>
          <TouchableOpacity style={styles.avatarBtn}>
            <View style={styles.avatar}>
              <Ionicons name="person" size={20} color={Colors.white} />
            </View>
          </TouchableOpacity>
        </View>
      </View>

      <ScrollView style={styles.scroll} contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>

        {/* ── Stats ── */}
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
              <Ionicons name="layers" size={20} color={Colors.teal} />
            </View>
            <Text style={styles.statValue}>{uniqueTopics}</Text>
            <Text style={styles.statLabel}>Topics</Text>
          </View>
          <View style={styles.statCard}>
            <View style={[styles.statIconWrap, { backgroundColor: Colors.green + '20' }]}>
              <Ionicons name="scan" size={20} color={Colors.green} />
            </View>
            <Text style={styles.statValue}>{savedItems.length}</Text>
            <Text style={styles.statLabel}>Scanned</Text>
          </View>
        </View>

        {/* ── Scan a Problem ── */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Scan a Problem</Text>
          <View style={styles.photoWidget}>
            {photoUri ? (
              <View>
                <TouchableOpacity onPress={() => setPreviewVisible(true)} activeOpacity={0.9}>
                  <Image source={{ uri: photoUri }} style={styles.photoThumb} resizeMode="cover" />
                  <View style={styles.photoOverlay}>
                    <Ionicons name="expand-outline" size={20} color={Colors.white} />
                    <Text style={styles.photoOverlayText}>Tap to expand</Text>
                  </View>
                </TouchableOpacity>
                <View style={styles.photoActions}>
                  <TouchableOpacity style={styles.photoRemoveBtn} onPress={handleClearPhoto}>
                    <Ionicons name="trash-outline" size={15} color={Colors.textLight} />
                    <Text style={styles.photoRemoveText}>Remove</Text>
                  </TouchableOpacity>
                  <TouchableOpacity
                    style={[styles.analyzeBtn, analyzing && styles.analyzeBtnDisabled]}
                    onPress={handleAnalyze}
                    disabled={analyzing}
                    activeOpacity={0.8}
                  >
                    <Ionicons name="sparkles" size={15} color={Colors.white} />
                    <Text style={styles.analyzeBtnText}>Analyze Problem</Text>
                  </TouchableOpacity>
                </View>
              </View>
            ) : (
              <View style={styles.photoUploadArea}>
                <View style={styles.photoUploadIcon}>
                  <Ionicons name="scan-outline" size={36} color={Colors.primary} />
                </View>
                <Text style={styles.photoUploadTitle}>Upload your math problem</Text>
                <Text style={styles.photoUploadSub}>Take a photo or choose from your gallery</Text>
                <View style={styles.photoButtonRow}>
                  <TouchableOpacity style={styles.photoCameraBtn} onPress={handleTakePhoto} activeOpacity={0.8}>
                    <Ionicons name="camera" size={18} color={Colors.white} />
                    <Text style={styles.photoCameraBtnText}>Take Photo</Text>
                  </TouchableOpacity>
                  <TouchableOpacity style={styles.photoGalleryBtn} onPress={handleUploadPhoto} activeOpacity={0.8}>
                    <Ionicons name="images-outline" size={18} color={Colors.primary} />
                    <Text style={styles.photoGalleryBtnText}>Upload</Text>
                  </TouchableOpacity>
                </View>
              </View>
            )}
          </View>
        </View>

        {/* ── Analyzing Spinner ── */}
        {analyzing && (
          <View style={styles.section}>
            <View style={styles.loadingCard}>
              <ActivityIndicator size="large" color={Colors.primary} />
              <Text style={styles.loadingTitle}>Analyzing your problem...</Text>
              <Text style={styles.loadingSub}>MathHelper AI is working on it</Text>
            </View>
          </View>
        )}

        {/* ── Analysis Error ── */}
        {analysisError && !analyzing && (
          <View style={styles.section}>
            <View style={styles.errorCard}>
              <Ionicons name="alert-circle-outline" size={28} color={Colors.secondary} />
              <Text style={styles.errorText}>{analysisError}</Text>
              <TouchableOpacity style={styles.retryBtn} onPress={handleAnalyze}>
                <Ionicons name="refresh-outline" size={15} color={Colors.primary} />
                <Text style={styles.retryBtnText}>Try Again</Text>
              </TouchableOpacity>
            </View>
          </View>
        )}

        {/* ── Analysis Results ── */}
        {analysisResult && !analyzing && (
          <View style={styles.section}>
            <AnalysisResults
              result={analysisResult}
              onDismiss={() => setAnalysisResult(null)}
              onSave={handleSave}
              saved={isSaved}
            />
          </View>
        )}

        {/* ── Quick Practice ── */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Quick Practice</Text>
          <ScrollView horizontal showsHorizontalScrollIndicator={false}>
            <View style={styles.topicPills}>
              {QUICK_TOPICS.map((t) => (
                <TouchableOpacity
                  key={t.name}
                  style={[styles.topicPill, { backgroundColor: t.color + '15', borderColor: t.color + '40' }]}
                  activeOpacity={0.7}
                >
                  <Ionicons name={t.icon as any} size={15} color={t.color} />
                  <Text style={[styles.topicPillText, { color: t.color }]}>{t.name}</Text>
                </TouchableOpacity>
              ))}
            </View>
          </ScrollView>
        </View>

        {/* ── Recently Saved ── */}
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
              <Ionicons name="bookmark-outline" size={36} color={Colors.textMuted} />
              <Text style={styles.emptyStateTitle}>No saved problems yet</Text>
              <Text style={styles.emptyStateSub}>
                Scan a problem above and tap "Save to Collection"
              </Text>
            </View>
          ) : (
            recentSaved.map((item) => (
              <View key={item.id} style={styles.recentCard}>
                <Image source={{ uri: item.imageUri }} style={styles.recentThumb} resizeMode="cover" />
                <View style={styles.recentInfo}>
                  <View style={[styles.topicBadge, { backgroundColor: Colors.primary + '18' }]}>
                    <Text style={[styles.topicBadgeText, { color: Colors.primary }]}>
                      {item.analysis.topic}
                    </Text>
                  </View>
                  <Text style={styles.recentProblem} numberOfLines={2}>
                    {item.analysis.problem}
                  </Text>
                  <Text style={styles.recentAnswer} numberOfLines={1}>
                    {item.analysis.answer}
                  </Text>
                </View>
              </View>
            ))
          )}
        </View>
      </ScrollView>

      {/* ── Full-screen Photo Preview Modal ── */}
      <Modal visible={previewVisible} transparent animationType="fade" onRequestClose={() => setPreviewVisible(false)}>
        <View style={styles.modalOverlay}>
          <View style={styles.modalCard}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>Problem Photo</Text>
              <TouchableOpacity onPress={() => setPreviewVisible(false)} style={styles.modalCloseBtn}>
                <Ionicons name="close" size={22} color={Colors.text} />
              </TouchableOpacity>
            </View>
            {photoUri && <Image source={{ uri: photoUri }} style={styles.modalImage} resizeMode="contain" />}
            <View style={styles.modalFooter}>
              <TouchableOpacity style={styles.modalAnalyzeBtn} onPress={handleAnalyze}>
                <Ionicons name="sparkles" size={16} color={Colors.white} />
                <Text style={styles.modalAnalyzeBtnText}>Analyze This Problem</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.modalRemoveBtn} onPress={handleClearPhoto}>
                <Ionicons name="trash-outline" size={15} color={Colors.secondary} />
                <Text style={styles.modalRemoveBtnText}>Remove</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </View>
  );
}

// ─── Styles ───────────────────────────────────────────────────────────────────
const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
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
  avatarBtn: {},
  avatar: {
    width: 42, height: 42, borderRadius: 21,
    backgroundColor: 'rgba(255,255,255,0.25)',
    alignItems: 'center', justifyContent: 'center',
    borderWidth: 2, borderColor: 'rgba(255,255,255,0.4)',
  },
  scroll: { flex: 1 },
  scrollContent: { padding: 16, paddingBottom: 32 },

  // Stats
  statsRow: { flexDirection: 'row', gap: 10, marginBottom: 24 },
  statCard: {
    flex: 1, backgroundColor: Colors.card, borderRadius: 16,
    padding: 14, alignItems: 'center', gap: 6,
    shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.06, shadowRadius: 8, elevation: 2,
  },
  statIconWrap: { width: 38, height: 38, borderRadius: 10, alignItems: 'center', justifyContent: 'center' },
  statValue: { fontSize: 20, fontWeight: '700', color: Colors.text },
  statLabel: { fontSize: 11, color: Colors.textLight, fontWeight: '500' },

  // Sections
  section: { marginBottom: 24 },
  sectionHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 },
  sectionTitle: { fontSize: 17, fontWeight: '700', color: Colors.text, marginBottom: 12 },
  seeAll: { fontSize: 14, color: Colors.primary, fontWeight: '600', marginBottom: 12 },

  // Photo Widget
  photoWidget: {
    backgroundColor: Colors.card, borderRadius: 16, overflow: 'hidden',
    shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.07, shadowRadius: 8, elevation: 2,
  },
  photoUploadArea: {
    alignItems: 'center', paddingVertical: 30, paddingHorizontal: 20, gap: 8,
    borderWidth: 2, borderColor: Colors.primary + '30', borderStyle: 'dashed', borderRadius: 16,
  },
  photoUploadIcon: {
    width: 68, height: 68, borderRadius: 18,
    backgroundColor: Colors.primaryLight, alignItems: 'center', justifyContent: 'center', marginBottom: 4,
  },
  photoUploadTitle: { fontSize: 16, fontWeight: '700', color: Colors.text },
  photoUploadSub: { fontSize: 13, color: Colors.textLight, textAlign: 'center', marginBottom: 8 },
  photoButtonRow: { flexDirection: 'row', gap: 12, marginTop: 4 },
  photoCameraBtn: {
    flexDirection: 'row', alignItems: 'center', gap: 8,
    backgroundColor: Colors.primary, paddingHorizontal: 20, paddingVertical: 11, borderRadius: 12,
  },
  photoCameraBtnText: { color: Colors.white, fontWeight: '700', fontSize: 14 },
  photoGalleryBtn: {
    flexDirection: 'row', alignItems: 'center', gap: 8,
    backgroundColor: Colors.primaryLight, paddingHorizontal: 20, paddingVertical: 11,
    borderRadius: 12, borderWidth: 1, borderColor: Colors.primary + '40',
  },
  photoGalleryBtnText: { color: Colors.primary, fontWeight: '700', fontSize: 14 },
  photoThumb: { width: '100%', height: 200 },
  photoOverlay: {
    position: 'absolute', bottom: 0, left: 0, right: 0, height: 52,
    backgroundColor: 'rgba(0,0,0,0.42)',
    flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8,
  },
  photoOverlayText: { color: Colors.white, fontSize: 13, fontWeight: '600' },
  photoActions: {
    flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center',
    paddingHorizontal: 14, paddingVertical: 12,
    borderTopWidth: 1, borderTopColor: Colors.border,
  },
  photoRemoveBtn: {
    flexDirection: 'row', alignItems: 'center', gap: 5,
    paddingHorizontal: 12, paddingVertical: 7, borderRadius: 8, backgroundColor: Colors.background,
  },
  photoRemoveText: { fontSize: 13, color: Colors.textLight, fontWeight: '500' },
  analyzeBtn: {
    flexDirection: 'row', alignItems: 'center', gap: 7,
    backgroundColor: Colors.primary, paddingHorizontal: 18, paddingVertical: 10, borderRadius: 12,
  },
  analyzeBtnDisabled: { opacity: 0.5 },
  analyzeBtnText: { color: Colors.white, fontWeight: '700', fontSize: 14 },

  // Loading / Error
  loadingCard: {
    backgroundColor: Colors.card, borderRadius: 16, padding: 32,
    alignItems: 'center', gap: 14,
    shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.06, shadowRadius: 8, elevation: 2,
  },
  loadingTitle: { fontSize: 16, fontWeight: '700', color: Colors.text },
  loadingSub: { fontSize: 13, color: Colors.textLight },
  errorCard: {
    backgroundColor: Colors.card, borderRadius: 16, padding: 24,
    alignItems: 'center', gap: 12,
    borderWidth: 1, borderColor: Colors.secondary + '30',
  },
  errorText: { fontSize: 14, color: Colors.text, textAlign: 'center', lineHeight: 20 },
  retryBtn: {
    flexDirection: 'row', alignItems: 'center', gap: 6,
    backgroundColor: Colors.primaryLight, borderRadius: 10, paddingHorizontal: 16, paddingVertical: 9,
  },
  retryBtnText: { fontSize: 14, fontWeight: '600', color: Colors.primary },

  // Quick Practice
  topicPills: { flexDirection: 'row', gap: 10, paddingRight: 16 },
  topicPill: {
    flexDirection: 'row', alignItems: 'center', gap: 6,
    paddingHorizontal: 14, paddingVertical: 9, borderRadius: 24, borderWidth: 1,
  },
  topicPillText: { fontSize: 13, fontWeight: '600' },

  // Recently Saved
  emptyState: {
    backgroundColor: Colors.card, borderRadius: 16, padding: 32,
    alignItems: 'center', gap: 10,
    borderWidth: 1, borderColor: Colors.border, borderStyle: 'dashed',
  },
  emptyStateTitle: { fontSize: 15, fontWeight: '700', color: Colors.textLight },
  emptyStateSub: { fontSize: 13, color: Colors.textMuted, textAlign: 'center' },
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

  // Modal
  modalOverlay: {
    flex: 1, backgroundColor: 'rgba(0,0,0,0.75)',
    justifyContent: 'center', alignItems: 'center', padding: 20,
  },
  modalCard: {
    backgroundColor: Colors.card, borderRadius: 20,
    width: '100%', maxWidth: 500, overflow: 'hidden',
  },
  modalHeader: {
    flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center',
    paddingHorizontal: 20, paddingVertical: 16,
    borderBottomWidth: 1, borderBottomColor: Colors.border,
  },
  modalTitle: { fontSize: 17, fontWeight: '700', color: Colors.text },
  modalCloseBtn: {
    width: 32, height: 32, borderRadius: 16,
    backgroundColor: Colors.background, alignItems: 'center', justifyContent: 'center',
  },
  modalImage: { width: '100%', height: 320, backgroundColor: Colors.background },
  modalFooter: {
    flexDirection: 'row', alignItems: 'center', gap: 12,
    padding: 16, borderTopWidth: 1, borderTopColor: Colors.border,
  },
  modalAnalyzeBtn: {
    flex: 1, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8,
    backgroundColor: Colors.primary, borderRadius: 12, paddingVertical: 12,
  },
  modalAnalyzeBtnText: { color: Colors.white, fontWeight: '700', fontSize: 15 },
  modalRemoveBtn: {
    flexDirection: 'row', alignItems: 'center', gap: 6,
    paddingHorizontal: 14, paddingVertical: 12,
    borderRadius: 12, backgroundColor: Colors.secondary + '15',
  },
  modalRemoveBtnText: { fontSize: 14, color: Colors.secondary, fontWeight: '600' },
});

// ─── Analysis Results Styles ──────────────────────────────────────────────────
const rs = StyleSheet.create({
  container: {
    backgroundColor: Colors.card, borderRadius: 16, overflow: 'hidden',
    shadowColor: '#000', shadowOffset: { width: 0, height: 3 }, shadowOpacity: 0.09, shadowRadius: 12, elevation: 4,
  },
  header: {
    flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center',
    padding: 16, backgroundColor: Colors.primaryLight,
    borderBottomWidth: 1, borderBottomColor: Colors.primary + '25',
  },
  headerLeft: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  headerTitle: { fontSize: 15, fontWeight: '700', color: Colors.primary },
  dismissBtn: {
    width: 28, height: 28, borderRadius: 14,
    backgroundColor: Colors.white, alignItems: 'center', justifyContent: 'center',
  },
  sectionLabel: { fontSize: 10, fontWeight: '700', color: Colors.textMuted, letterSpacing: 1.2 },
  problemBox: { padding: 16, borderBottomWidth: 1, borderBottomColor: Colors.border, gap: 10 },
  problemText: { fontSize: 16, color: Colors.text, fontWeight: '500', lineHeight: 23 },
  badgeRow: { flexDirection: 'row', gap: 8 },
  badge: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 8 },
  badgeText: { fontSize: 12, fontWeight: '700' },
  answerBox: {
    margin: 16, backgroundColor: Colors.green + '14', borderRadius: 14,
    padding: 18, alignItems: 'center', gap: 8,
    borderWidth: 1, borderColor: Colors.green + '35',
  },
  answerText: { fontSize: 24, fontWeight: '700', color: Colors.text, textAlign: 'center' },
  stepsHeading: { fontSize: 15, fontWeight: '700', color: Colors.text, paddingHorizontal: 16, paddingTop: 4, paddingBottom: 12 },
  stepRow: { flexDirection: 'row', gap: 12, paddingHorizontal: 16, paddingBottom: 18 },
  stepBubble: {
    width: 30, height: 30, borderRadius: 15,
    backgroundColor: Colors.primary, alignItems: 'center', justifyContent: 'center', flexShrink: 0, marginTop: 1,
  },
  stepBubbleText: { fontSize: 13, fontWeight: '700', color: Colors.white },
  stepBody: { flex: 1, gap: 5 },
  stepTitle: { fontSize: 14, fontWeight: '700', color: Colors.text },
  stepExplanation: { fontSize: 13, color: Colors.textLight, lineHeight: 20 },
  mathBox: {
    backgroundColor: Colors.primaryLight, borderLeftWidth: 3, borderLeftColor: Colors.primary,
    borderRadius: 8, padding: 10, marginTop: 6,
  },
  mathText: { fontSize: 14, fontFamily: 'monospace', color: Colors.primaryDark, letterSpacing: 0.4 },
  conceptsSection: { padding: 16, paddingTop: 0, gap: 10 },
  conceptsHeading: { fontSize: 13, fontWeight: '700', color: Colors.text },
  conceptsPills: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  pill: {
    backgroundColor: Colors.primaryLight, borderRadius: 20,
    paddingHorizontal: 12, paddingVertical: 5,
    borderWidth: 1, borderColor: Colors.primary + '30',
  },
  pillText: { fontSize: 12, fontWeight: '600', color: Colors.primary },
  tipBox: {
    flexDirection: 'row', gap: 10, margin: 16, marginTop: 4,
    backgroundColor: Colors.yellow + '18', borderRadius: 12, padding: 14,
    borderWidth: 1, borderColor: Colors.yellow + '40', alignItems: 'flex-start',
  },
  tipText: { flex: 1, fontSize: 13, color: Colors.text, lineHeight: 20 },
  saveBtn: {
    flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8,
    margin: 16, marginTop: 4, paddingVertical: 13, borderRadius: 14,
    backgroundColor: Colors.primaryLight,
    borderWidth: 1.5, borderColor: Colors.primary,
  },
  saveBtnSaved: {
    backgroundColor: Colors.green,
    borderColor: Colors.green,
  },
  saveBtnText: { fontSize: 15, fontWeight: '700', color: Colors.primary },
  saveBtnTextSaved: { color: Colors.white },
});
