/**
 * SessionSummaryCard.tsx
 * Shown when the student taps "Exit" — summarizes the session.
 *
 * Shows: topics practiced, problems correct, mastery change, session summary.
 * Includes an animated progress bar.
 */

import { useEffect, useRef } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Animated,
  Modal,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '../constants/Colors';

interface SessionSummaryProps {
  visible: boolean;
  onClose: () => void;
  summary?: string;
  totalProblems: number;
  successRate: number;
  topicsPracticed?: string[];
  sessionDuration?: number; // minutes
}

export default function SessionSummaryCard({
  visible,
  onClose,
  summary,
  totalProblems,
  successRate,
  topicsPracticed,
  sessionDuration,
}: SessionSummaryProps) {
  const progressAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    if (visible) {
      progressAnim.setValue(0);
      Animated.timing(progressAnim, {
        toValue: successRate,
        duration: 1200,
        useNativeDriver: false,
      }).start();
    }
  }, [visible, successRate]);

  const progressWidth = progressAnim.interpolate({
    inputRange: [0, 1],
    outputRange: ['0%', '100%'],
  });

  const ratePercent = Math.round(successRate * 100);

  return (
    <Modal visible={visible} transparent animationType="fade">
      <View style={styles.backdrop}>
        <View style={styles.card}>
          {/* Header */}
          <View style={styles.header}>
            <View style={styles.iconCircle}>
              <Ionicons name="trophy" size={28} color={Colors.primary} />
            </View>
            <Text style={styles.title}>Session Complete!</Text>
          </View>

          {/* Stats row */}
          <View style={styles.statsRow}>
            <View style={styles.stat}>
              <Text style={styles.statValue}>{totalProblems}</Text>
              <Text style={styles.statLabel}>Problems</Text>
            </View>
            <View style={styles.statDivider} />
            <View style={styles.stat}>
              <Text style={styles.statValue}>{ratePercent}%</Text>
              <Text style={styles.statLabel}>Success</Text>
            </View>
            {sessionDuration != null && (
              <>
                <View style={styles.statDivider} />
                <View style={styles.stat}>
                  <Text style={styles.statValue}>{sessionDuration}</Text>
                  <Text style={styles.statLabel}>Minutes</Text>
                </View>
              </>
            )}
          </View>

          {/* Progress bar */}
          <View style={styles.progressSection}>
            <Text style={styles.progressLabel}>Session Score</Text>
            <View style={styles.progressBar}>
              <Animated.View
                style={[
                  styles.progressFill,
                  { width: progressWidth },
                  ratePercent >= 70 ? styles.progressGood : ratePercent >= 40 ? styles.progressOk : styles.progressLow,
                ]}
              />
            </View>
          </View>

          {/* Topics */}
          {topicsPracticed && topicsPracticed.length > 0 && (
            <View style={styles.topicsSection}>
              <Text style={styles.topicsLabel}>Topics Practiced</Text>
              <View style={styles.topicChips}>
                {topicsPracticed.map((t, i) => (
                  <View key={i} style={styles.topicChip}>
                    <Text style={styles.topicChipText}>{t.replace(/_/g, ' ')}</Text>
                  </View>
                ))}
              </View>
            </View>
          )}

          {/* Summary text */}
          {summary && (
            <View style={styles.summarySection}>
              <Text style={styles.summaryText}>{summary}</Text>
            </View>
          )}

          {/* Close button */}
          <TouchableOpacity style={styles.closeBtn} onPress={onClose} activeOpacity={0.8}>
            <Text style={styles.closeBtnText}>Done</Text>
          </TouchableOpacity>
        </View>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  backdrop: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  card: {
    width: '100%',
    maxWidth: 380,
    backgroundColor: '#FFF',
    borderRadius: 20,
    padding: 24,
    alignItems: 'center',
  },
  header: {
    alignItems: 'center',
    gap: 10,
    marginBottom: 20,
  },
  iconCircle: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: Colors.primaryLight || '#EDE9FF',
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: 20,
    fontWeight: '700',
    color: Colors.text || '#1A1A2E',
  },

  statsRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 16,
    marginBottom: 20,
  },
  stat: {
    alignItems: 'center',
  },
  statValue: {
    fontSize: 24,
    fontWeight: '700',
    color: Colors.primary,
  },
  statLabel: {
    fontSize: 12,
    color: Colors.textMuted || '#999',
    marginTop: 2,
  },
  statDivider: {
    width: 1,
    height: 30,
    backgroundColor: '#E8E8F0',
  },

  progressSection: {
    width: '100%',
    marginBottom: 16,
  },
  progressLabel: {
    fontSize: 12,
    fontWeight: '600',
    color: Colors.textMuted || '#999',
    marginBottom: 6,
  },
  progressBar: {
    height: 8,
    backgroundColor: '#E8E8F0',
    borderRadius: 4,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    borderRadius: 4,
  },
  progressGood: { backgroundColor: Colors.green || '#2ECC71' },
  progressOk: { backgroundColor: Colors.orange || '#FF9F43' },
  progressLow: { backgroundColor: Colors.secondary || '#FF6B6B' },

  topicsSection: {
    width: '100%',
    marginBottom: 16,
  },
  topicsLabel: {
    fontSize: 12,
    fontWeight: '600',
    color: Colors.textMuted || '#999',
    marginBottom: 6,
  },
  topicChips: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 6,
  },
  topicChip: {
    backgroundColor: Colors.primaryLight || '#EDE9FF',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
  },
  topicChipText: {
    fontSize: 12,
    fontWeight: '500',
    color: Colors.primary,
    textTransform: 'capitalize',
  },

  summarySection: {
    width: '100%',
    backgroundColor: '#F8F8FC',
    borderRadius: 12,
    padding: 14,
    marginBottom: 20,
  },
  summaryText: {
    fontSize: 13,
    lineHeight: 20,
    color: Colors.text || '#1A1A2E',
  },

  closeBtn: {
    width: '100%',
    paddingVertical: 14,
    backgroundColor: Colors.primary,
    borderRadius: 14,
    alignItems: 'center',
  },
  closeBtnText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#FFF',
  },
});
