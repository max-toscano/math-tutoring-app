/**
 * StepCards.tsx
 * Renders a step-by-step solution as progressive reveal cards.
 *
 * Parses the AI response text into individual steps.
 * Each step is a card the student unlocks by tapping "Got It".
 * "Explain More" sends a follow-up about that specific step.
 *
 * Falls back to null if no steps are detected (caller renders normally).
 */

import { useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Animated,
  LayoutAnimation,
  Platform,
  UIManager,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '../constants/Colors';
import MathRenderer from './MathRenderer';

// Enable LayoutAnimation on Android
if (Platform.OS === 'android' && UIManager.setLayoutAnimationEnabledExperimental) {
  UIManager.setLayoutAnimationEnabledExperimental(true);
}

interface Step {
  number: number;
  title: string;
  content: string;   // The full step text (includes math)
}

interface StepCardsProps {
  content: string;
  onExplainMore?: (stepNumber: number, stepContent: string) => void;
}

// ── Step parser ──────────────────────────────────────────────────────────

const STEP_PATTERNS = [
  /(?:^|\n)\s*(?:\*\*)?Step\s+(\d+)(?:\s*[:.])?(?:\*\*)?[\s:]*(.*?)(?=(?:\n\s*(?:\*\*)?Step\s+\d|\n\s*#{1,3}\s*Step\s+\d|$))/gis,
  /(?:^|\n)\s*#{1,3}\s*Step\s+(\d+)(?:\s*[:.])?[\s:]*(.*?)(?=(?:\n\s*#{1,3}\s*Step\s+\d|$))/gis,
];

function parseSteps(text: string): Step[] | null {
  // Try each pattern
  for (const pattern of STEP_PATTERNS) {
    pattern.lastIndex = 0;
    const steps: Step[] = [];
    let match;

    while ((match = pattern.exec(text)) !== null) {
      const number = parseInt(match[1], 10);
      const rest = match[2]?.trim() || '';

      // Split first line as title, rest as content
      const lines = rest.split('\n');
      const title = lines[0]?.replace(/^\*\*|\*\*$/g, '').replace(/^[:.\s]+/, '').trim() || `Step ${number}`;
      const content = lines.slice(1).join('\n').trim() || rest;

      steps.push({ number, title, content });
    }

    if (steps.length >= 2) {
      return steps;
    }
  }

  // Fallback: try numbered list (1., 2., 3.)
  const numberedPattern = /(?:^|\n)\s*(\d+)\.\s+(.*?)(?=(?:\n\s*\d+\.\s|$))/gs;
  numberedPattern.lastIndex = 0;
  const steps: Step[] = [];
  let match;

  while ((match = numberedPattern.exec(text)) !== null) {
    const number = parseInt(match[1], 10);
    const rest = match[2]?.trim() || '';
    const lines = rest.split('\n');
    const title = lines[0]?.replace(/^\*\*|\*\*$/g, '').trim() || `Step ${number}`;
    const content = rest;

    steps.push({ number, title, content });
  }

  if (steps.length >= 2) {
    return steps;
  }

  return null; // No steps detected
}

// ── Component ────────────────────────────────────────────────────────────

export default function StepCards({ content, onExplainMore }: StepCardsProps) {
  const steps = parseSteps(content);

  if (!steps || steps.length < 2) {
    return null; // Caller should fall back to normal rendering
  }

  return <StepCardList steps={steps} onExplainMore={onExplainMore} />;
}

function StepCardList({
  steps,
  onExplainMore,
}: {
  steps: Step[];
  onExplainMore?: (stepNumber: number, stepContent: string) => void;
}) {
  const [unlockedUpTo, setUnlockedUpTo] = useState(0); // Index of the highest unlocked step
  const [completedSteps, setCompletedSteps] = useState<Set<number>>(new Set());

  function handleGotIt(index: number) {
    LayoutAnimation.configureNext(LayoutAnimation.Presets.easeInEaseOut);
    setCompletedSteps((prev) => new Set(prev).add(index));
    if (index >= unlockedUpTo) {
      setUnlockedUpTo(index + 1);
    }
  }

  function handleExplainMore(step: Step) {
    if (onExplainMore) {
      onExplainMore(step.number, step.content);
    }
  }

  const allComplete = completedSteps.size === steps.length;

  return (
    <View style={styles.container}>
      {/* Progress bar */}
      <View style={styles.progressRow}>
        <View style={styles.progressBar}>
          <View
            style={[
              styles.progressFill,
              { width: `${(completedSteps.size / steps.length) * 100}%` },
            ]}
          />
        </View>
        <Text style={styles.progressText}>
          {completedSteps.size}/{steps.length}
        </Text>
      </View>

      {/* Step cards */}
      {steps.map((step, index) => {
        const isUnlocked = index <= unlockedUpTo;
        const isCompleted = completedSteps.has(index);
        const isCurrent = index === unlockedUpTo && !isCompleted;

        return (
          <View
            key={step.number}
            style={[
              styles.card,
              isCompleted && styles.cardCompleted,
              !isUnlocked && styles.cardLocked,
              isCurrent && styles.cardCurrent,
            ]}
          >
            {/* Card header */}
            <View style={styles.cardHeader}>
              <View style={[
                styles.stepBadge,
                isCompleted && styles.stepBadgeCompleted,
                !isUnlocked && styles.stepBadgeLocked,
              ]}>
                {isCompleted ? (
                  <Ionicons name="checkmark" size={12} color="#FFF" />
                ) : (
                  <Text style={[
                    styles.stepBadgeText,
                    !isUnlocked && styles.stepBadgeTextLocked,
                  ]}>{step.number}</Text>
                )}
              </View>
              <Text
                style={[
                  styles.stepTitle,
                  isCompleted && styles.stepTitleCompleted,
                  !isUnlocked && styles.stepTitleLocked,
                ]}
                numberOfLines={isUnlocked ? undefined : 1}
              >
                {step.title}
              </Text>
              {!isUnlocked && (
                <Ionicons name="lock-closed" size={14} color={Colors.textMuted || '#CCC'} />
              )}
            </View>

            {/* Card content (only if unlocked) */}
            {isUnlocked && (
              <View style={styles.cardContent}>
                <MathRenderer content={step.content} isUser={false} />

                {/* Action buttons */}
                {!isCompleted && (
                  <View style={styles.actionRow}>
                    <TouchableOpacity
                      style={styles.explainBtn}
                      onPress={() => handleExplainMore(step)}
                      activeOpacity={0.7}
                    >
                      <Ionicons name="help-circle-outline" size={16} color={Colors.primary} />
                      <Text style={styles.explainBtnText}>Explain More</Text>
                    </TouchableOpacity>

                    <TouchableOpacity
                      style={styles.gotItBtn}
                      onPress={() => handleGotIt(index)}
                      activeOpacity={0.7}
                    >
                      <Ionicons name="checkmark-circle" size={16} color="#FFF" />
                      <Text style={styles.gotItBtnText}>Got It</Text>
                    </TouchableOpacity>
                  </View>
                )}
              </View>
            )}
          </View>
        );
      })}

      {/* Completion message */}
      {allComplete && (
        <View style={styles.completeCard}>
          <Ionicons name="trophy" size={24} color={Colors.primary} />
          <Text style={styles.completeText}>All steps understood!</Text>
        </View>
      )}
    </View>
  );
}

// ── Export the parser for external use ────────────────────────────────────
export { parseSteps };

const styles = StyleSheet.create({
  container: {
    gap: 8,
  },

  // Progress bar
  progressRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 4,
  },
  progressBar: {
    flex: 1,
    height: 4,
    backgroundColor: '#E8E8F0',
    borderRadius: 2,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: Colors.primary,
    borderRadius: 2,
  },
  progressText: {
    fontSize: 11,
    fontWeight: '600',
    color: Colors.textMuted || '#999',
  },

  // Cards
  card: {
    borderRadius: 12,
    backgroundColor: '#FAFAFE',
    borderWidth: 1,
    borderColor: '#E8E8F0',
    overflow: 'hidden',
  },
  cardCompleted: {
    borderColor: (Colors.green || '#2ECC71') + '40',
    backgroundColor: (Colors.green || '#2ECC71') + '08',
  },
  cardLocked: {
    opacity: 0.6,
    backgroundColor: '#F5F5F8',
  },
  cardCurrent: {
    borderColor: Colors.primary + '60',
    borderWidth: 2,
  },

  // Card header
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    padding: 12,
  },
  stepBadge: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: Colors.primary,
    alignItems: 'center',
    justifyContent: 'center',
  },
  stepBadgeCompleted: {
    backgroundColor: Colors.green || '#2ECC71',
  },
  stepBadgeLocked: {
    backgroundColor: '#D0D0D8',
  },
  stepBadgeText: {
    fontSize: 12,
    fontWeight: '700',
    color: '#FFF',
  },
  stepBadgeTextLocked: {
    color: '#FFF',
  },
  stepTitle: {
    flex: 1,
    fontSize: 14,
    fontWeight: '600',
    color: Colors.text || '#1A1A2E',
  },
  stepTitleCompleted: {
    color: Colors.green || '#2ECC71',
  },
  stepTitleLocked: {
    color: Colors.textMuted || '#999',
  },

  // Card content
  cardContent: {
    paddingHorizontal: 12,
    paddingBottom: 12,
  },

  // Action buttons
  actionRow: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
    gap: 8,
    marginTop: 10,
  },
  explainBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
    backgroundColor: Colors.primaryLight || '#EDE9FF',
  },
  explainBtnText: {
    fontSize: 12,
    fontWeight: '600',
    color: Colors.primary,
  },
  gotItBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
    backgroundColor: Colors.primary,
  },
  gotItBtnText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#FFF',
  },

  // Completion
  completeCard: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    padding: 12,
    borderRadius: 12,
    backgroundColor: Colors.primaryLight || '#EDE9FF',
  },
  completeText: {
    fontSize: 14,
    fontWeight: '700',
    color: Colors.primary,
  },
});
