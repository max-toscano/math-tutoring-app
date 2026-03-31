/**
 * MessageReactions.tsx
 * 👍 "This helped" and 😕 "Still confused" buttons below AI responses.
 *
 * - "This helped" logs a positive signal and shows a checkmark
 * - "Still confused" auto-sends a follow-up asking the AI to explain simpler
 * - Reaction state is tracked per message so it persists during the session
 */

import { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Animated } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '../constants/Colors';

interface MessageReactionsProps {
  messageId: string;
  onHelpful?: () => void;
  onConfused?: () => void;
}

export default function MessageReactions({ messageId, onHelpful, onConfused }: MessageReactionsProps) {
  const [reaction, setReaction] = useState<'helpful' | 'confused' | null>(null);

  function handleHelpful() {
    setReaction('helpful');
    onHelpful?.();
  }

  function handleConfused() {
    setReaction('confused');
    onConfused?.();
  }

  if (reaction) {
    return (
      <View style={styles.container}>
        <View style={[styles.reacted, reaction === 'helpful' ? styles.reactedHelpful : styles.reactedConfused]}>
          <Ionicons
            name={reaction === 'helpful' ? 'checkmark-circle' : 'refresh-circle'}
            size={14}
            color={reaction === 'helpful' ? Colors.green || '#2ECC71' : Colors.primary}
          />
          <Text style={[styles.reactedText, reaction === 'helpful' ? styles.reactedTextHelpful : styles.reactedTextConfused]}>
            {reaction === 'helpful' ? 'Glad that helped!' : 'Let me try a different approach...'}
          </Text>
        </View>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.btn} onPress={handleHelpful} activeOpacity={0.7}>
        <Ionicons name="thumbs-up-outline" size={14} color={Colors.green || '#2ECC71'} />
        <Text style={styles.btnTextHelpful}>This helped</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.btn} onPress={handleConfused} activeOpacity={0.7}>
        <Ionicons name="help-circle-outline" size={14} color={Colors.primary} />
        <Text style={styles.btnTextConfused}>Still confused</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    gap: 8,
    marginTop: 6,
    paddingLeft: 36, // align with assistant bubble
  },
  btn: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 14,
    backgroundColor: '#F5F5F8',
    borderWidth: 1,
    borderColor: '#E8E8F0',
  },
  btnTextHelpful: {
    fontSize: 12,
    fontWeight: '500',
    color: Colors.green || '#2ECC71',
  },
  btnTextConfused: {
    fontSize: 12,
    fontWeight: '500',
    color: Colors.primary,
  },
  reacted: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 14,
  },
  reactedHelpful: {
    backgroundColor: (Colors.green || '#2ECC71') + '15',
  },
  reactedConfused: {
    backgroundColor: Colors.primary + '15',
  },
  reactedText: {
    fontSize: 12,
    fontWeight: '500',
  },
  reactedTextHelpful: {
    color: Colors.green || '#2ECC71',
  },
  reactedTextConfused: {
    color: Colors.primary,
  },
});
