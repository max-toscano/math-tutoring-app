import React, { useEffect, useRef } from 'react';
import { View, Text, StyleSheet, Animated } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '../constants/Colors';

interface ChecklistItem {
  label: string;
  passed: boolean;
}

interface ValidationChecklistProps {
  items: ChecklistItem[];
  visible: boolean;
}

const PASSED_COLOR = '#22C55E';

export default function ValidationChecklist({ items, visible }: ValidationChecklistProps) {
  const animValue = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.timing(animValue, {
      toValue: visible ? 1 : 0,
      duration: 200,
      useNativeDriver: true,
    }).start();
  }, [visible]);

  const opacity = animValue;
  const translateY = animValue.interpolate({
    inputRange: [0, 1],
    outputRange: [8, 0],
  });

  if (!visible) return null;

  return (
    <Animated.View style={[styles.container, { opacity, transform: [{ translateY }] }]}>
      {items.map((item, index) => (
        <View key={index} style={styles.row}>
          <Ionicons
            name={item.passed ? 'checkmark-circle' : 'ellipse-outline'}
            size={14}
            color={item.passed ? PASSED_COLOR : Colors.textMuted}
          />
          <Text style={[styles.label, item.passed && styles.labelPassed]}>
            {item.label}
          </Text>
        </View>
      ))}
    </Animated.View>
  );
}

const styles = StyleSheet.create({
  container: {
    gap: 4,
    paddingLeft: 4,
    paddingTop: 4,
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  label: {
    fontSize: 12,
    color: Colors.textMuted,
  },
  labelPassed: {
    color: Colors.textLight,
  },
});
