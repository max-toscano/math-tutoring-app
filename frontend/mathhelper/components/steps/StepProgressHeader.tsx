/**
 * StepProgressHeader.tsx - Shows progress bar and step count
 */

import { View, Text, StyleSheet } from 'react-native';
import { Colors } from '../../constants/Colors';

interface StepProgressHeaderProps {
  totalSteps: number;
  completedSteps: number;
  currentStep: number;
}

export default function StepProgressHeader({
  totalSteps,
  completedSteps,
  currentStep,
}: StepProgressHeaderProps) {
  const completedPercent = (completedSteps / totalSteps) * 100;
  const currentPercent = ((currentStep + 1) / totalSteps) * 100;

  return (
    <View style={styles.container}>
      <View style={styles.topRow}>
        <Text style={styles.title}>Solution Steps</Text>
        <View style={styles.countBadge}>
          <Text style={styles.countText}>
            {completedSteps}/{totalSteps}
          </Text>
        </View>
      </View>

      <View style={styles.progressBar}>
        {/* Completed segment */}
        <View
          style={[
            styles.progressSegment,
            styles.progressComplete,
            { width: `${completedPercent}%` },
          ]}
        />
        {/* Current segment */}
        {completedSteps < totalSteps && (
          <View
            style={[
              styles.progressSegment,
              styles.progressCurrent,
              {
                left: `${completedPercent}%`,
                width: `${(1 / totalSteps) * 100}%`,
              },
            ]}
          />
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    gap: 8,
    marginBottom: 4,
  },
  topRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  title: {
    fontSize: 13,
    fontWeight: '600',
    color: Colors.textLight,
    letterSpacing: 0.3,
  },
  countBadge: {
    backgroundColor: Colors.primaryLight,
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
  },
  countText: {
    fontSize: 12,
    fontWeight: '700',
    color: Colors.primary,
  },
  progressBar: {
    height: 6,
    backgroundColor: '#E8E8F0',
    borderRadius: 3,
    overflow: 'hidden',
    position: 'relative',
  },
  progressSegment: {
    position: 'absolute',
    top: 0,
    bottom: 0,
    borderRadius: 3,
  },
  progressComplete: {
    backgroundColor: Colors.green,
    left: 0,
  },
  progressCurrent: {
    backgroundColor: Colors.primary,
  },
});
