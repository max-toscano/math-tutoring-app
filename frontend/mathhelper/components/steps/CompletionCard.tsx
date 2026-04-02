/**
 * CompletionCard.tsx - Celebration card shown when all steps are complete
 */

import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '../../constants/Colors';

interface CompletionCardProps {
  problemTitle: string;
  stepsCompleted: number;
}

export default function CompletionCard({
  problemTitle,
  stepsCompleted,
}: CompletionCardProps) {
  return (
    <View style={styles.container}>
      <View style={styles.iconWrap}>
        <Ionicons name="trophy" size={36} color={Colors.primary} />
      </View>
      <Text style={styles.title}>All steps complete!</Text>
      <Text style={styles.subtitle}>
        You worked through {stepsCompleted} {stepsCompleted === 1 ? 'step' : 'steps'}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    backgroundColor: '#F8FCF9',
    borderRadius: 16,
    padding: 20,
    marginTop: 12,
    borderWidth: 2,
    borderColor: 'rgba(46, 204, 113, 0.3)',
    gap: 8,
  },
  iconWrap: {
    marginBottom: 4,
  },
  title: {
    fontSize: 18,
    fontWeight: '700',
    color: Colors.green,
  },
  subtitle: {
    fontSize: 14,
    color: Colors.textLight,
  },
});
