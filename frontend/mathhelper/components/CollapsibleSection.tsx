/**
 * CollapsibleSection.tsx
 * Renders response sections (### headers) as collapsible accordions.
 *
 * Auto-detects sections from headers like "### The Big Idea", "### Example",
 * "### Your Problem". Each section can be collapsed/expanded.
 * First section starts expanded, rest start collapsed.
 */

import { useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  LayoutAnimation,
  Platform,
  UIManager,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '../constants/Colors';
import MathRenderer from './MathRenderer';

if (Platform.OS === 'android' && UIManager.setLayoutAnimationEnabledExperimental) {
  UIManager.setLayoutAnimationEnabledExperimental(true);
}

interface Section {
  title: string;
  content: string;
}

interface CollapsibleSectionsProps {
  content: string;
}

/**
 * Parse response text into sections based on ### headers.
 * Returns null if no sections found (less than 2 headers).
 */
export function parseSections(text: string): Section[] | null {
  // Match ### headers or **Bold Headers**
  const pattern = /(?:^|\n)\s*(?:#{1,3}\s+(.+)|(?:\*\*(.+?)\*\*))\s*\n/g;
  const matches: { title: string; index: number }[] = [];

  let match;
  while ((match = pattern.exec(text)) !== null) {
    const title = (match[1] || match[2] || '').trim();
    if (title && title.length > 2 && title.length < 80) {
      matches.push({ title, index: match.index });
    }
  }

  if (matches.length < 2) return null;

  const sections: Section[] = [];

  // Content before the first header (intro text)
  const introContent = text.substring(0, matches[0].index).trim();
  if (introContent) {
    sections.push({ title: 'Overview', content: introContent });
  }

  // Each header section
  for (let i = 0; i < matches.length; i++) {
    const start = matches[i].index;
    const end = i < matches.length - 1 ? matches[i + 1].index : text.length;
    const sectionText = text.substring(start, end);
    // Remove the header line itself from the content
    const contentAfterHeader = sectionText.replace(/^.*\n/, '').trim();
    sections.push({
      title: matches[i].title,
      content: contentAfterHeader,
    });
  }

  return sections.length >= 2 ? sections : null;
}

export default function CollapsibleSections({ content }: CollapsibleSectionsProps) {
  const sections = parseSections(content);

  if (!sections) return null; // Caller falls back to normal rendering

  return <SectionList sections={sections} />;
}

function SectionList({ sections }: { sections: Section[] }) {
  // First section expanded, rest collapsed
  const [expanded, setExpanded] = useState<Set<number>>(new Set([0]));

  function toggle(index: number) {
    LayoutAnimation.configureNext(LayoutAnimation.Presets.easeInEaseOut);
    setExpanded((prev) => {
      const next = new Set(prev);
      if (next.has(index)) next.delete(index);
      else next.add(index);
      return next;
    });
  }

  return (
    <View style={styles.container}>
      {sections.map((section, i) => {
        const isExpanded = expanded.has(i);
        return (
          <View key={i} style={styles.section}>
            <TouchableOpacity
              style={styles.header}
              onPress={() => toggle(i)}
              activeOpacity={0.7}
            >
              <View style={styles.headerLeft}>
                <View style={[styles.dot, i === 0 && styles.dotFirst]} />
                <Text style={styles.headerText}>{section.title}</Text>
              </View>
              <Ionicons
                name={isExpanded ? 'chevron-up' : 'chevron-down'}
                size={16}
                color={Colors.textMuted || '#999'}
              />
            </TouchableOpacity>

            {isExpanded && (
              <View style={styles.body}>
                <MathRenderer content={section.content} isUser={false} />
              </View>
            )}
          </View>
        );
      })}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    gap: 4,
  },
  section: {
    borderRadius: 10,
    backgroundColor: '#FAFAFE',
    borderWidth: 1,
    borderColor: '#E8E8F0',
    overflow: 'hidden',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 10,
  },
  headerLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    flex: 1,
  },
  dot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: Colors.primary + '40',
  },
  dotFirst: {
    backgroundColor: Colors.primary,
  },
  headerText: {
    fontSize: 13,
    fontWeight: '600',
    color: Colors.text || '#1A1A2E',
    flex: 1,
  },
  body: {
    paddingHorizontal: 10,
    paddingBottom: 10,
    paddingTop: 2,
  },
});
