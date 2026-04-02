/**
 * WarningBox.tsx - Displays common mistakes or warnings in a highlighted red box
 */

import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

interface WarningBoxProps {
  text: string;
}

export default function WarningBox({ text }: WarningBoxProps) {
  return (
    <View style={styles.container}>
      <View style={styles.iconWrap}>
        <Ionicons name="warning" size={16} color="#FF6B6B" />
      </View>
      <View style={styles.textWrap}>
        <Text style={styles.label}>Watch Out</Text>
        <Text style={styles.text}>{text}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    backgroundColor: 'rgba(255, 107, 107, 0.08)',
    borderRadius: 12,
    padding: 12,
    gap: 10,
    borderLeftWidth: 3,
    borderLeftColor: '#FF6B6B',
  },
  iconWrap: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: 'rgba(255, 107, 107, 0.15)',
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
    color: '#CC2936',
    letterSpacing: 0.5,
    textTransform: 'uppercase',
  },
  text: {
    fontSize: 13,
    fontWeight: '500',
    color: '#1A1A2E',
    lineHeight: 19,
  },
});
