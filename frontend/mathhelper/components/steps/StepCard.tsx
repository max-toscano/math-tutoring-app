/**
 * StepCard.tsx - Individual step card with expand/collapse and actions
 */

import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '../../constants/Colors';
import MathRenderer from '../MathRenderer';
import InsightBox from './InsightBox';
import WarningBox from './WarningBox';
import type { EnhancedStep } from './stepParser';

interface StepCardProps {
  step: EnhancedStep;
  state: 'locked' | 'active' | 'complete';
  isExpanded: boolean;
  onToggle: () => void;
  onGotIt: () => void;
  onExplainMore: () => void;
}

export default function StepCard({
  step,
  state,
  isExpanded,
  onToggle,
  onGotIt,
  onExplainMore,
}: StepCardProps) {
  const isLocked = state === 'locked';
  const isComplete = state === 'complete';
  const isActive = state === 'active';

  return (
    <View
      style={[
        styles.card,
        isLocked && styles.cardLocked,
        isActive && isExpanded && styles.cardActiveExpanded,
        isComplete && styles.cardComplete,
      ]}
    >
      {/* Header - always visible */}
      <TouchableOpacity
        style={styles.header}
        onPress={onToggle}
        disabled={isLocked}
        activeOpacity={0.7}
        accessibilityRole="button"
        accessibilityState={{ expanded: isExpanded, disabled: isLocked }}
        accessibilityLabel={`Step ${step.number}: ${step.title}`}
      >
        {/* Step badge */}
        <View
          style={[
            styles.badge,
            isLocked && styles.badgeLocked,
            isActive && styles.badgeActive,
            isComplete && styles.badgeComplete,
          ]}
        >
          {isComplete ? (
            <Ionicons name="checkmark" size={14} color="#FFF" />
          ) : (
            <Text style={styles.badgeText}>{step.number}</Text>
          )}
        </View>

        {/* Title */}
        <Text
          style={[
            styles.title,
            isLocked && styles.titleLocked,
            isComplete && styles.titleComplete,
          ]}
          numberOfLines={isExpanded ? undefined : 1}
        >
          {step.title}
        </Text>

        {/* State icon */}
        {isLocked ? (
          <Ionicons name="lock-closed" size={16} color={Colors.textMuted} />
        ) : (
          <Ionicons
            name={isExpanded ? 'chevron-up' : 'chevron-down'}
            size={18}
            color={isComplete ? Colors.green : Colors.primary}
          />
        )}
      </TouchableOpacity>

      {/* Content - only when expanded and not locked */}
      {isExpanded && !isLocked && (
        <View style={styles.content}>
          {/* Main step content with math */}
          <View style={styles.mathWrapper}>
            <MathRenderer content={step.content} isUser={false} />
          </View>

          {/* Insight box (optional) */}
          {step.insight && <InsightBox text={step.insight} />}

          {/* Warning box (optional) */}
          {step.warning && <WarningBox text={step.warning} />}

          {/* Action buttons */}
          {!isComplete && (
            <View style={styles.actions}>
              <TouchableOpacity
                style={styles.explainBtn}
                onPress={onExplainMore}
                activeOpacity={0.7}
                accessibilityRole="button"
                accessibilityLabel="Explain this step more"
              >
                <Ionicons
                  name="help-circle-outline"
                  size={18}
                  color={Colors.primary}
                />
                <Text style={styles.explainBtnText}>Explain More</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={styles.gotItBtn}
                onPress={onGotIt}
                activeOpacity={0.7}
                accessibilityRole="button"
                accessibilityLabel="Mark step as understood"
              >
                <Ionicons name="checkmark-circle" size={18} color="#FFF" />
                <Text style={styles.gotItBtnText}>Got It!</Text>
              </TouchableOpacity>
            </View>
          )}
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    flex: 1,
    backgroundColor: '#FAFAFE',
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#E8E8F0',
    marginBottom: 8,
    overflow: 'hidden',
  },
  cardLocked: {
    opacity: 0.6,
    backgroundColor: '#F5F5F8',
  },
  cardActiveExpanded: {
    backgroundColor: '#FCFBFF',
    borderColor: Colors.primary,
    borderWidth: 2,
    shadowColor: Colors.primary,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 12,
    elevation: 4,
  },
  cardComplete: {
    backgroundColor: '#F8FCF9',
    borderColor: 'rgba(46, 204, 113, 0.3)',
  },

  header: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    padding: 14,
    minHeight: 52,
  },

  badge: {
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: '#D1D5DB',
    alignItems: 'center',
    justifyContent: 'center',
  },
  badgeLocked: {
    backgroundColor: '#D1D5DB',
  },
  badgeActive: {
    backgroundColor: Colors.primary,
  },
  badgeComplete: {
    backgroundColor: Colors.green,
  },
  badgeText: {
    fontSize: 13,
    fontWeight: '700',
    color: '#FFF',
  },

  title: {
    flex: 1,
    fontSize: 15,
    fontWeight: '600',
    color: Colors.text,
    lineHeight: 20,
  },
  titleLocked: {
    color: Colors.textMuted,
  },
  titleComplete: {
    color: Colors.green,
  },

  content: {
    paddingHorizontal: 14,
    paddingBottom: 14,
    gap: 12,
  },

  mathWrapper: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 12,
    borderWidth: 1,
    borderColor: '#E8E8F0',
  },

  actions: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
    gap: 10,
    marginTop: 4,
  },

  explainBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 22,
    backgroundColor: Colors.primaryLight,
    borderWidth: 1,
    borderColor: 'rgba(108, 99, 255, 0.2)',
    minHeight: 44,
  },
  explainBtnText: {
    fontSize: 13,
    fontWeight: '600',
    color: Colors.primary,
  },

  gotItBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 22,
    backgroundColor: Colors.primary,
    minHeight: 44,
    shadowColor: Colors.primary,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 6,
    elevation: 3,
  },
  gotItBtnText: {
    fontSize: 13,
    fontWeight: '700',
    color: '#FFF',
  },
});
