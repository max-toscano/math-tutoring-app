/**
 * EnhancedStepCards.tsx - Main container for enhanced step visualization
 */

import { useState, useCallback, useMemo } from 'react';
import {
  View,
  StyleSheet,
  LayoutAnimation,
  Platform,
  UIManager,
} from 'react-native';
import { Colors } from '../../constants/Colors';
import StepProgressHeader from './StepProgressHeader';
import StepCard from './StepCard';
import CompletionCard from './CompletionCard';
import { parseEnhancedSteps } from './stepParser';

if (Platform.OS === 'android' && UIManager.setLayoutAnimationEnabledExperimental) {
  UIManager.setLayoutAnimationEnabledExperimental(true);
}

interface EnhancedStepCardsProps {
  content: string;
  onExplainMore?: (stepNumber: number, stepContent: string) => void;
  onStepComplete?: (stepNumber: number) => void;
}

export default function EnhancedStepCards({
  content,
  onExplainMore,
  onStepComplete,
}: EnhancedStepCardsProps) {
  const steps = useMemo(() => parseEnhancedSteps(content), [content]);

  const [completedSteps, setCompletedSteps] = useState<Set<number>>(new Set());
  const [expandedStep, setExpandedStep] = useState<number>(0);

  if (!steps || steps.length < 2) {
    return null; // Fallback to regular rendering
  }

  const currentStepIndex = Math.min(completedSteps.size, steps.length - 1);
  const allComplete = completedSteps.size === steps.length;

  const handleGotIt = useCallback((index: number) => {
    LayoutAnimation.configureNext(LayoutAnimation.Presets.easeInEaseOut);
    setCompletedSteps((prev) => new Set(prev).add(index));

    // Auto-expand next step
    if (index < steps.length - 1) {
      setExpandedStep(index + 1);
    }

    onStepComplete?.(steps[index].number);
  }, [steps, onStepComplete]);

  const handleToggleExpand = useCallback((index: number) => {
    LayoutAnimation.configureNext(LayoutAnimation.Presets.easeInEaseOut);
    setExpandedStep((prev) => prev === index ? -1 : index);
  }, []);

  const getStepState = (index: number): 'locked' | 'active' | 'complete' => {
    if (completedSteps.has(index)) return 'complete';
    if (index <= currentStepIndex) return 'active';
    return 'locked';
  };

  return (
    <View style={styles.container}>
      <StepProgressHeader
        totalSteps={steps.length}
        completedSteps={completedSteps.size}
        currentStep={currentStepIndex}
      />

      <View style={styles.timeline}>
        {steps.map((step, index) => {
          const state = getStepState(index);
          const isExpanded = expandedStep === index;
          const isLast = index === steps.length - 1;

          return (
            <View key={step.number} style={styles.stepRow}>
              {/* Timeline connector */}
              <View style={styles.connectorColumn}>
                <View
                  style={[
                    styles.connectorLine,
                    index === 0 && styles.connectorLineFirst,
                    state === 'complete' && styles.connectorLineComplete,
                    state === 'active' && styles.connectorLineActive,
                  ]}
                />
                {!isLast && (
                  <View
                    style={[
                      styles.connectorLineBottom,
                      state === 'complete' && styles.connectorLineComplete,
                    ]}
                  />
                )}
              </View>

              {/* Step card */}
              <StepCard
                step={step}
                state={state}
                isExpanded={isExpanded && state !== 'locked'}
                onToggle={() => handleToggleExpand(index)}
                onGotIt={() => handleGotIt(index)}
                onExplainMore={() => onExplainMore?.(step.number, step.content)}
              />
            </View>
          );
        })}
      </View>

      {allComplete && (
        <CompletionCard
          problemTitle={steps[0]?.title || 'Problem'}
          stepsCompleted={steps.length}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    gap: 12,
  },
  timeline: {
    gap: 0,
  },
  stepRow: {
    flexDirection: 'row',
    alignItems: 'stretch',
  },
  connectorColumn: {
    width: 20,
    alignItems: 'center',
    marginRight: 8,
  },
  connectorLine: {
    position: 'absolute',
    top: 14,
    width: 2,
    height: 14,
    backgroundColor: '#D1D5DB',
  },
  connectorLineFirst: {
    height: 0,
  },
  connectorLineBottom: {
    position: 'absolute',
    top: 28,
    bottom: 0,
    width: 2,
    backgroundColor: '#D1D5DB',
  },
  connectorLineComplete: {
    backgroundColor: Colors.green,
  },
  connectorLineActive: {
    backgroundColor: Colors.primary,
  },
});
