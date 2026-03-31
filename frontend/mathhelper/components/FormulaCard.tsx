/**
 * FormulaCard.tsx
 * Renders key formulas as visually prominent cards.
 *
 * Detects display math ($$...$$) in the response and renders each one
 * as a highlighted card with a colored left border and larger font.
 * Makes formulas impossible to miss in a long explanation.
 *
 * Usage: wrap response content — FormulaCard detects and highlights
 * display math blocks automatically.
 */

import { View, StyleSheet, Platform } from 'react-native';
import { Colors } from '../constants/Colors';
import MathRenderer from './MathRenderer';

interface FormulaCardProps {
  /** A single display math expression (without $$ delimiters) */
  formula: string;
}

export default function FormulaCard({ formula }: FormulaCardProps) {
  return (
    <View style={styles.card}>
      <View style={styles.accent} />
      <View style={styles.content}>
        <MathRenderer content={`$$${formula}$$`} isUser={false} />
      </View>
    </View>
  );
}

/**
 * Splits response text into segments: regular text and formula blocks.
 * Returns null if no display formulas found.
 */
export function splitFormulas(content: string): { type: 'text' | 'formula'; value: string }[] | null {
  const pattern = /\$\$([\s\S]*?)\$\$/g;
  const segments: { type: 'text' | 'formula'; value: string }[] = [];
  let lastIndex = 0;
  let match;
  let formulaCount = 0;

  while ((match = pattern.exec(content)) !== null) {
    // Text before the formula
    const textBefore = content.substring(lastIndex, match.index).trim();
    if (textBefore) {
      segments.push({ type: 'text', value: textBefore });
    }
    // The formula
    segments.push({ type: 'formula', value: match[1].trim() });
    formulaCount++;
    lastIndex = match.index + match[0].length;
  }

  // Text after the last formula
  const textAfter = content.substring(lastIndex).trim();
  if (textAfter) {
    segments.push({ type: 'text', value: textAfter });
  }

  return formulaCount >= 1 ? segments : null;
}

const styles = StyleSheet.create({
  card: {
    flexDirection: 'row',
    marginVertical: 8,
    borderRadius: 10,
    backgroundColor: Colors.primaryLight || '#EDE9FF',
    overflow: 'hidden',
  },
  accent: {
    width: 4,
    backgroundColor: Colors.primary,
  },
  content: {
    flex: 1,
    paddingVertical: 8,
    paddingHorizontal: 12,
  },
});
