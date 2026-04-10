import React, { useEffect, useRef } from 'react';
import { View, Text, StyleSheet, Animated } from 'react-native';
import { Colors } from '../constants/Colors';
import { getPasswordStrengthLabel } from '../utils/validation';

interface PasswordStrengthMeterProps {
  score: number;
  visible: boolean;
}

const BAR_COLORS = ['#EF4444', '#F97316', '#EAB308', '#22C55E'];
const INACTIVE_COLOR = Colors.border;

export default function PasswordStrengthMeter({ score, visible }: PasswordStrengthMeterProps) {
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

  const label = score > 0 ? getPasswordStrengthLabel(score) : '';
  const activeColor = score > 0 ? BAR_COLORS[score - 1] : INACTIVE_COLOR;

  return (
    <Animated.View style={[styles.container, { opacity, transform: [{ translateY }] }]}>
      <View style={styles.barsRow}>
        {[1, 2, 3, 4].map((level) => (
          <View
            key={level}
            style={[
              styles.bar,
              { backgroundColor: score >= level ? activeColor : INACTIVE_COLOR },
            ]}
          />
        ))}
      </View>
      {label ? (
        <Text style={[styles.label, { color: activeColor }]}>{label}</Text>
      ) : null}
    </Animated.View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    paddingLeft: 4,
    paddingTop: 2,
  },
  barsRow: {
    flexDirection: 'row',
    gap: 4,
    flex: 1,
  },
  bar: {
    flex: 1,
    height: 4,
    borderRadius: 2,
  },
  label: {
    fontSize: 12,
    fontWeight: '600',
    minWidth: 40,
  },
});
