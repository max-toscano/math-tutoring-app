/**
 * SuggestionChips.tsx
 * Context-aware follow-up buttons shown after the AI responds.
 * Tapping a chip sends that text as the next message.
 */

import { View, Text, TouchableOpacity, StyleSheet, ScrollView } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '../constants/Colors';

interface SuggestionChipsProps {
  suggestions: string[];
  onPress: (text: string) => void;
  disabled?: boolean;
}

export default function SuggestionChips({ suggestions, onPress, disabled }: SuggestionChipsProps) {
  if (!suggestions || suggestions.length === 0) return null;

  return (
    <ScrollView
      horizontal
      showsHorizontalScrollIndicator={false}
      style={styles.container}
      contentContainerStyle={styles.content}
    >
      {suggestions.map((text, i) => (
        <TouchableOpacity
          key={i}
          style={[styles.chip, disabled && styles.chipDisabled]}
          onPress={() => onPress(text)}
          disabled={disabled}
          activeOpacity={0.7}
        >
          <Ionicons name="arrow-forward-circle-outline" size={14} color={Colors.primary} />
          <Text style={styles.chipText}>{text}</Text>
        </TouchableOpacity>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    marginTop: 8,
    marginBottom: 4,
  },
  content: {
    paddingLeft: 36, // align with assistant bubble (avatar width + gap)
    gap: 8,
  },
  chip: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 18,
    backgroundColor: Colors.primaryLight || '#EDE9FF',
    borderWidth: 1,
    borderColor: Colors.primary + '30',
  },
  chipDisabled: {
    opacity: 0.5,
  },
  chipText: {
    fontSize: 13,
    fontWeight: '500',
    color: Colors.primary,
  },
});
