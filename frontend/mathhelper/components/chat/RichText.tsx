/**
 * RichText.tsx — Renders inline styled text with bold, italic, and math segments.
 */

import { Text, StyleSheet, Platform } from 'react-native';
import { parseInlineSegments } from '../../utils/mathText';
import { Colors } from '../../constants/Colors';

interface RichTextProps {
  children: string;
  style?: any;
  accentColor?: string;
}

export function RichText({ children, style, accentColor }: RichTextProps) {
  const segments = parseInlineSegments(children);

  return (
    <Text style={[styles.base, style]}>
      {segments.map((seg, i) => {
        switch (seg.type) {
          case 'bold':
            return <Text key={i} style={styles.bold}>{seg.content}</Text>;
          case 'italic':
            return <Text key={i} style={styles.italic}>{seg.content}</Text>;
          case 'math':
            return (
              <Text key={i} style={[styles.math, accentColor ? { color: accentColor } : null]}>
                {seg.content}
              </Text>
            );
          default:
            return <Text key={i}>{seg.content}</Text>;
        }
      })}
    </Text>
  );
}

const styles = StyleSheet.create({
  base: {
    fontSize: 15,
    lineHeight: 23,
    color: Colors.text,
  },
  bold: {
    fontWeight: '700',
    color: Colors.text,
  },
  italic: {
    fontStyle: 'italic',
  },
  math: {
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
    fontWeight: '600',
    color: Colors.primaryDark,
    fontSize: 14.5,
  },
});
