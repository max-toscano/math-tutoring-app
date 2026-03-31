/**
 * ToolStatus.tsx
 * Animated loading indicator that shows what the AI is doing.
 * Cycles through realistic status messages during the thinking phase.
 */

import { useEffect, useState, useRef } from 'react';
import { View, Text, StyleSheet, Animated } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '../constants/Colors';

interface ToolStatusProps {
  isLoading: boolean;
}

const STATUS_STEPS = [
  { icon: 'search-outline', text: 'Understanding your question...' },
  { icon: 'book-outline', text: 'Looking up relevant material...' },
  { icon: 'calculator-outline', text: 'Working through the math...' },
  { icon: 'create-outline', text: 'Writing response...' },
];

export default function ToolStatus({ isLoading }: ToolStatusProps) {
  const [stepIndex, setStepIndex] = useState(0);
  const fadeAnim = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    if (!isLoading) {
      setStepIndex(0);
      return;
    }

    const interval = setInterval(() => {
      // Fade out
      Animated.timing(fadeAnim, {
        toValue: 0,
        duration: 200,
        useNativeDriver: true,
      }).start(() => {
        setStepIndex((prev) => (prev + 1) % STATUS_STEPS.length);
        // Fade in
        Animated.timing(fadeAnim, {
          toValue: 1,
          duration: 200,
          useNativeDriver: true,
        }).start();
      });
    }, 2500);

    return () => clearInterval(interval);
  }, [isLoading]);

  if (!isLoading) return null;

  const step = STATUS_STEPS[stepIndex];

  return (
    <View style={styles.container}>
      <View style={styles.avatar}>
        <Ionicons name="school" size={14} color={Colors.primary} />
      </View>
      <Animated.View style={[styles.bubble, { opacity: fadeAnim }]}>
        <View style={styles.dotRow}>
          <View style={[styles.dot, styles.dot1]} />
          <View style={[styles.dot, styles.dot2]} />
          <View style={[styles.dot, styles.dot3]} />
        </View>
        <View style={styles.statusRow}>
          <Ionicons name={step.icon as any} size={14} color={Colors.primary} />
          <Text style={styles.statusText}>{step.text}</Text>
        </View>
      </Animated.View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 8,
    marginBottom: 16,
  },
  avatar: {
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: Colors.primaryLight || '#EDE9FF',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 2,
  },
  bubble: {
    backgroundColor: Colors.card || '#FFFFFF',
    borderRadius: 18,
    borderBottomLeftRadius: 4,
    padding: 14,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 1,
  },
  dotRow: {
    flexDirection: 'row',
    gap: 4,
    marginBottom: 6,
  },
  dot: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: Colors.primary,
  },
  dot1: { opacity: 0.3 },
  dot2: { opacity: 0.6 },
  dot3: { opacity: 1.0 },
  statusRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  statusText: {
    fontSize: 13,
    color: Colors.textLight || '#999',
    fontStyle: 'italic',
  },
});
