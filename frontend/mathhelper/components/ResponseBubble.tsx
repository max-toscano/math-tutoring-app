/**
 * ResponseBubble.tsx
 * Rich assistant message bubble with:
 *  - Topic & mode badge at top
 *  - KaTeX math rendering via MathRenderer
 *  - Graph cards with full-screen option
 *  - Tool badges showing what was used
 *  - Copy button
 */

import { useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Modal,
  Image,
  Platform,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '../constants/Colors';
import MathRenderer from './MathRenderer';
import DesmosGraph from './DesmosGraph';
import EnhancedStepCards from './steps/EnhancedStepCards';
import type { GraphOutput } from '../services/agent';

// Clipboard: use navigator.clipboard on web, expo-clipboard on native if installed
async function copyToClipboard(text: string): Promise<boolean> {
  try {
    if (Platform.OS === 'web' && navigator?.clipboard) {
      await navigator.clipboard.writeText(text);
      return true;
    }
    // Native fallback — try expo-clipboard if installed
    try {
      const ExpoClipboard = require('expo-clipboard');
      await ExpoClipboard.setStringAsync(text);
      return true;
    } catch {
      return false;
    }
  } catch {
    return false;
  }
}

interface ResponseBubbleProps {
  content: string;
  topic?: string;
  mode?: string;
  tools?: string[];
  graphs?: GraphOutput[];
  onExplainMore?: (stepNumber: number, stepContent: string) => void;
}

const MODE_LABELS: Record<string, { label: string; icon: string }> = {
  auto: { label: 'Auto', icon: 'sparkles-outline' },
  explain: { label: 'Explain', icon: 'bulb-outline' },
  guide_me: { label: 'Guide Me', icon: 'help-circle-outline' },
  hint: { label: 'Hint', icon: 'eye-outline' },
  check_answer: { label: 'Check', icon: 'checkmark-circle-outline' },
};

const TOOL_ICONS: Record<string, string> = {
  symbolic_math: 'calculator-outline',
  numerical_math: 'stats-chart-outline',
  linear_algebra: 'grid-outline',
  graphing: 'bar-chart-outline',
  math_web_search: 'globe-outline',
};

function ContentRenderer({
  content,
  graphs,
  onExplainMore,
}: {
  content: string;
  graphs?: GraphOutput[];
  onExplainMore?: (stepNumber: number, stepContent: string) => void;
}) {
  // Try to render as enhanced step cards first
  const enhancedSteps = (
    <EnhancedStepCards
      content={content}
      onExplainMore={onExplainMore}
    />
  );

  // If steps are detected, show step cards; otherwise, fall back to regular math render
  if (enhancedSteps) {
    return enhancedSteps;
  }

  // Fallback: Single MathRenderer for the entire response.
  // Formula highlighting happens via CSS inside the iframe.
  // No splitting into multiple iframes — that causes height glitches.
  return <MathRenderer content={content} graphs={graphs} isUser={false} />;
}

export default function ResponseBubble({ content, topic, mode, tools, graphs, onExplainMore }: ResponseBubbleProps) {
  const [copied, setCopied] = useState(false);
  const [fullScreenGraph, setFullScreenGraph] = useState<string | null>(null);

  const modeInfo = mode ? MODE_LABELS[mode] : null;
  const topicDisplay = topic?.replace(/_/g, ' ') ?? null;

  async function handleCopy() {
    const success = await copyToClipboard(content);
    if (success) {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  }

  return (
    <View style={styles.container}>
      {/* Topic & Mode badges */}
      {(topicDisplay || modeInfo) && (
        <View style={styles.badgeRow}>
          {topicDisplay && (
            <View style={styles.topicBadge}>
              <Ionicons name="book-outline" size={11} color={Colors.primary} />
              <Text style={styles.topicText}>{topicDisplay}</Text>
            </View>
          )}
          {modeInfo && (
            <View style={styles.modeBadge}>
              <Ionicons name={modeInfo.icon as any} size={11} color="#666" />
              <Text style={styles.modeText}>{modeInfo.label}</Text>
            </View>
          )}
        </View>
      )}

      {/* Rendered content with KaTeX math */}
      <ContentRenderer content={content} graphs={graphs} onExplainMore={onExplainMore} />

      {/* Interactive Desmos graphs */}
      {graphs && graphs.length > 0 && (
        <View style={styles.graphsContainer}>
          {graphs.map((g, i) => {
            // New format: Desmos config
            if (g.desmos && g.desmos.expressions) {
              return (
                <DesmosGraph
                  key={i}
                  expressions={g.desmos.expressions}
                  bounds={g.desmos.bounds}
                  graphType={g.graph_type}
                />
              );
            }
            // Legacy fallback: static base64 image
            if (g.image_base64) {
              return (
                <TouchableOpacity
                  key={i}
                  style={styles.graphCard}
                  onPress={() => setFullScreenGraph(g.image_base64!)}
                  activeOpacity={0.8}
                >
                  <Image
                    source={{ uri: `data:image/png;base64,${g.image_base64}` }}
                    style={styles.graphImage}
                    resizeMode="contain"
                  />
                </TouchableOpacity>
              );
            }
            return null;
          })}
        </View>
      )}

      {/* Bottom row: tools + copy button */}
      <View style={styles.bottomRow}>
        {tools && tools.length > 0 && (
          <View style={styles.toolsRow}>
            {tools.map((t, i) => (
              <View key={i} style={styles.toolBadge}>
                <Ionicons
                  name={(TOOL_ICONS[t] || 'construct-outline') as any}
                  size={10}
                  color={Colors.primary}
                />
                <Text style={styles.toolText}>{t.replace(/_/g, ' ')}</Text>
              </View>
            ))}
          </View>
        )}
        <TouchableOpacity style={styles.copyBtn} onPress={handleCopy} activeOpacity={0.7}>
          <Ionicons
            name={copied ? 'checkmark-outline' : 'copy-outline'}
            size={14}
            color={copied ? '#4ECDC4' : '#999'}
          />
        </TouchableOpacity>
      </View>

      {/* Full screen graph modal */}
      {fullScreenGraph && (
        <Modal visible transparent animationType="fade">
          <TouchableOpacity
            style={styles.modalBackdrop}
            onPress={() => setFullScreenGraph(null)}
            activeOpacity={1}
          >
            <View style={styles.modalContent}>
              <Image
                source={{ uri: `data:image/png;base64,${fullScreenGraph}` }}
                style={styles.modalImage}
                resizeMode="contain"
              />
              <TouchableOpacity
                style={styles.modalClose}
                onPress={() => setFullScreenGraph(null)}
              >
                <Ionicons name="close" size={24} color="#FFF" />
              </TouchableOpacity>
            </View>
          </TouchableOpacity>
        </Modal>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { width: '100%' },

  badgeRow: {
    flexDirection: 'row',
    gap: 6,
    marginBottom: 8,
    flexWrap: 'wrap',
  },
  topicBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    backgroundColor: Colors.primaryLight || '#EDE9FF',
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 10,
  },
  topicText: {
    fontSize: 11,
    fontWeight: '600',
    color: Colors.primary,
    textTransform: 'capitalize',
  },
  modeBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    backgroundColor: '#F0F0F0',
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 10,
  },
  modeText: {
    fontSize: 11,
    fontWeight: '500',
    color: '#666',
  },

  graphsContainer: {
    marginTop: 8,
    gap: 8,
  },
  graphCard: {
    borderRadius: 12,
    overflow: 'hidden',
    backgroundColor: '#FAFAFA',
    borderWidth: 1,
    borderColor: Colors.border || '#EEE',
  },
  graphImage: {
    width: '100%',
    height: 200,
  },
  graphFooter: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    padding: 8,
  },
  graphLabel: {
    fontSize: 12,
    color: '#999',
    textTransform: 'capitalize',
  },

  bottomRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 8,
  },
  toolsRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 4,
    flex: 1,
  },
  toolBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 3,
    backgroundColor: Colors.primaryLight || '#EDE9FF',
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 6,
  },
  toolText: {
    fontSize: 9,
    fontWeight: '600',
    color: Colors.primary,
  },
  copyBtn: {
    padding: 6,
  },

  modalBackdrop: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.9)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    width: '95%',
    height: '80%',
  },
  modalImage: {
    width: '100%',
    height: '100%',
  },
  modalClose: {
    position: 'absolute',
    top: 10,
    right: 10,
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: 'rgba(0,0,0,0.5)',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
