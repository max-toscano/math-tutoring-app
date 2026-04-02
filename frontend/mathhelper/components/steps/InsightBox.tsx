/**
 * InsightBox.tsx - Displays key insights in a highlighted yellow box
 */

import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

interface InsightBoxProps {
  text: string;
}

export default function InsightBox({ text }: InsightBoxProps) {
  return (
    <View style={styles.container}>
      <View style={styles.iconWrap}>
        <Ionicons name="bulb" size={16} color="#F59E0B" />
      </View>
      <View style={styles.textWrap}>
        <Text style={styles.label}>Key Insight</Text>
        <Text style={styles.text}>{text}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    backgroundColor: '#FEF9C3',
    borderRadius: 12,
    padding: 12,
    gap: 10,
    borderLeftWidth: 3,
    borderLeftColor: '#F59E0B',
  },
  iconWrap: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: 'rgba(245, 158, 11, 0.2)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  textWrap: {
    flex: 1,
    gap: 2,
  },
  label: {
    fontSize: 11,
    fontWeight: '700',
    color: '#92400E',
    letterSpacing: 0.5,
    textTransform: 'uppercase',
  },
  text: {
    fontSize: 13,
    fontWeight: '500',
    color: '#92400E',
    lineHeight: 19,
  },
});
