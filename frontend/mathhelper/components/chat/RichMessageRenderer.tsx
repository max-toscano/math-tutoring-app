/**
 * RichMessageRenderer.tsx — Renders AI lesson messages with structured blocks,
 * proper math symbols, formula cards, tips, definitions, and quiz UI.
 */

import { View, Text, StyleSheet, TouchableOpacity, Platform, Image } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '../../constants/Colors';
import { RichText } from './RichText';
import { parseMessageBlocks, type ContentBlock } from '../../utils/messageParser';
import { replaceMathSymbols } from '../../utils/mathText';
import { getImageSource } from '../../constants/imageCatalog';
import type { QuizResult, QuizOutcome, GraphData } from '../../services/learn';

// ─── Props ────────────────────────────────────────────────────────────────────

interface Props {
  content: string;
  images?: string[];
  graphs?: GraphData[];
  question?: {
    type: 'multiple_choice' | 'free_response';
    text: string;
    options?: string[];
    question_number?: number;
  };
  quizResult?: QuizResult;
  quizOutcome?: QuizOutcome;
  onQuizAnswer?: (answer: string) => void;
  accentColor: string;
}

// ─── Main Component ───────────────────────────────────────────────────────────

export function RichMessageRenderer({
  content,
  images,
  graphs,
  question,
  quizResult,
  quizOutcome,
  onQuizAnswer,
  accentColor,
}: Props) {
  const blocks = parseMessageBlocks(content);

  return (
    <View style={styles.container}>
      {/* Content blocks */}
      {blocks.map((block, i) => (
        <BlockRenderer key={i} block={block} accentColor={accentColor} />
      ))}

      {/* Images */}
      {images?.map((imageId) => {
        const source = getImageSource(imageId);
        if (!source) return null;
        return (
          <View key={imageId} style={styles.imageWrap}>
            <Image source={source} style={styles.image} resizeMode="contain" />
          </View>
        );
      })}

      {/* Server-generated graphs */}
      {graphs?.map((g, idx) => g.image_base64 ? (
        <View key={`graph-${idx}`} style={styles.graphWrap}>
          <Image
            source={{ uri: `data:image/png;base64,${g.image_base64}` }}
            style={styles.graphImage}
            resizeMode="contain"
          />
        </View>
      ) : null)}

      {/* Quiz question (multiple choice buttons) */}
      {question && question.type === 'multiple_choice' && question.options && (
        <View style={styles.quizCard}>
          <View style={styles.quizHeader}>
            <View style={[styles.quizBadge, { backgroundColor: accentColor + '18' }]}>
              <Text style={[styles.quizBadgeText, { color: accentColor }]}>
                Q{question.question_number ?? ''}
              </Text>
            </View>
            <RichText style={styles.quizQuestionText}>{question.text}</RichText>
          </View>
          <View style={styles.quizOptions}>
            {question.options.map((opt, idx) => {
              const letter = opt.charAt(0);
              const isCorrect = quizResult && quizResult.is_correct && opt.startsWith(letter);
              const isWrong = quizResult && !quizResult.is_correct && opt.startsWith(letter);
              return (
                <TouchableOpacity
                  key={idx}
                  style={[
                    styles.quizOption,
                    !quizResult && { borderColor: accentColor + '30' },
                    isCorrect && styles.quizOptionCorrect,
                    isWrong && styles.quizOptionWrong,
                  ]}
                  onPress={() => !quizResult && onQuizAnswer?.(opt)}
                  disabled={!!quizResult}
                  activeOpacity={0.7}
                >
                  <View style={[
                    styles.quizOptionLetter,
                    { backgroundColor: accentColor + '15' },
                    isCorrect && { backgroundColor: Colors.green + '20' },
                    isWrong && { backgroundColor: Colors.secondary + '20' },
                  ]}>
                    <Text style={[
                      styles.quizOptionLetterText,
                      { color: accentColor },
                      isCorrect && { color: Colors.green },
                      isWrong && { color: Colors.secondary },
                    ]}>
                      {letter}
                    </Text>
                  </View>
                  <RichText style={styles.quizOptionText}>
                    {opt.replace(/^[A-D][.)]\s*/, '')}
                  </RichText>
                </TouchableOpacity>
              );
            })}
          </View>
        </View>
      )}

      {/* Quiz result feedback */}
      {quizResult && (
        <View style={[
          styles.quizResultCard,
          quizResult.is_correct ? styles.quizResultCorrect : styles.quizResultWrong,
        ]}>
          <Ionicons
            name={quizResult.is_correct ? 'checkmark-circle' : 'close-circle'}
            size={20}
            color={quizResult.is_correct ? Colors.green : Colors.secondary}
          />
          <View style={{ flex: 1 }}>
            <Text style={[
              styles.quizResultLabel,
              { color: quizResult.is_correct ? Colors.green : Colors.secondary },
            ]}>
              {quizResult.is_correct ? 'Correct!' : 'Not quite'}
            </Text>
            {quizResult.explanation ? (
              <RichText style={styles.quizResultExplanation}>{quizResult.explanation}</RichText>
            ) : null}
            {quizResult.running_score && (
              <View style={styles.scoreRow}>
                {Array.from({ length: quizResult.running_score.total }).map((_, idx) => (
                  <View
                    key={idx}
                    style={[
                      styles.scoreDot,
                      idx < quizResult.running_score!.correct
                        ? { backgroundColor: Colors.green }
                        : { backgroundColor: Colors.secondary + '40' },
                    ]}
                  />
                ))}
                <Text style={styles.scoreText}>
                  {quizResult.running_score.correct}/{quizResult.running_score.total}
                </Text>
              </View>
            )}
          </View>
        </View>
      )}
    </View>
  );
}

// ─── Block Renderer ───────────────────────────────────────────────────────────

function BlockRenderer({ block, accentColor }: { block: ContentBlock; accentColor: string }) {
  switch (block.type) {
    case 'heading':
      return (
        <View style={styles.headingWrap}>
          <View style={[styles.headingAccent, { backgroundColor: accentColor }]} />
          <Text style={styles.headingText}>{block.text}</Text>
        </View>
      );

    case 'formula':
      return (
        <View style={[styles.formulaCard, { borderLeftColor: accentColor }]}>
          {block.label && <Text style={styles.formulaLabel}>{block.label}</Text>}
          <Text style={[styles.formulaText, { color: accentColor }]}>{block.expression}</Text>
        </View>
      );

    case 'definition':
      return (
        <View style={[styles.definitionCard, { borderLeftColor: accentColor }]}>
          <Text style={[styles.definitionTerm, { color: accentColor }]}>{block.term}</Text>
          <RichText style={styles.definitionBody} accentColor={accentColor}>{block.body}</RichText>
        </View>
      );

    case 'bullet_list':
      return (
        <View style={styles.listWrap}>
          {block.items.map((item, i) => (
            <View key={i} style={styles.bulletItem}>
              <View style={[styles.bulletDot, { backgroundColor: accentColor }]} />
              <RichText style={styles.listItemText} accentColor={accentColor}>{item}</RichText>
            </View>
          ))}
        </View>
      );

    case 'numbered_list':
      return (
        <View style={styles.listWrap}>
          {block.items.map((item, i) => (
            <View key={i} style={styles.numberedItem}>
              <View style={[styles.numberCircle, { backgroundColor: accentColor + '15' }]}>
                <Text style={[styles.numberText, { color: accentColor }]}>{i + 1}</Text>
              </View>
              <RichText style={styles.listItemText} accentColor={accentColor}>{item}</RichText>
            </View>
          ))}
        </View>
      );

    case 'tip': {
      const configs = {
        tip: { icon: 'bulb-outline' as const, bg: Colors.yellow + '12', color: '#B8860B' },
        note: { icon: 'information-circle-outline' as const, bg: Colors.primary + '10', color: Colors.primary },
        remember: { icon: 'bookmark-outline' as const, bg: Colors.teal + '12', color: Colors.teal },
        important: { icon: 'alert-circle-outline' as const, bg: Colors.orange + '12', color: Colors.orange },
        warning: { icon: 'warning-outline' as const, bg: Colors.secondary + '10', color: Colors.secondary },
      };
      const cfg = configs[block.variant] ?? configs.tip;
      return (
        <View style={[styles.tipCard, { backgroundColor: cfg.bg }]}>
          <Ionicons name={cfg.icon} size={18} color={cfg.color} style={{ marginTop: 2 }} />
          <View style={{ flex: 1 }}>
            <Text style={[styles.tipLabel, { color: cfg.color }]}>
              {block.variant.charAt(0).toUpperCase() + block.variant.slice(1)}
            </Text>
            <RichText style={styles.tipText}>{block.text}</RichText>
          </View>
        </View>
      );
    }

    case 'example':
      return (
        <View style={styles.exampleCard}>
          <View style={styles.exampleHeader}>
            <Ionicons name="code-working-outline" size={16} color={accentColor} />
            <Text style={[styles.exampleTitle, { color: accentColor }]}>{block.title}</Text>
          </View>
          <View style={[styles.exampleBody, { borderLeftColor: accentColor + '30' }]}>
            <RichText style={styles.exampleText} accentColor={accentColor}>{block.body}</RichText>
          </View>
        </View>
      );

    case 'divider':
      return <View style={styles.divider} />;

    case 'paragraph':
    default:
      return (
        <RichText style={styles.paragraph} accentColor={accentColor}>{block.text}</RichText>
      );
  }
}

// ─── Styles ───────────────────────────────────────────────────────────────────

const styles = StyleSheet.create({
  container: { gap: 10 },

  // Paragraph
  paragraph: { fontSize: 15, lineHeight: 23, color: Colors.text },

  // Heading
  headingWrap: { flexDirection: 'row', alignItems: 'center', gap: 8, marginTop: 4, marginBottom: 2 },
  headingAccent: { width: 3, height: 20, borderRadius: 2 },
  headingText: { fontSize: 16, fontWeight: '700', color: Colors.text, flex: 1 },

  // Formula
  formulaCard: {
    backgroundColor: '#F8F7FF',
    borderRadius: 12,
    padding: 14,
    borderLeftWidth: 4,
    alignItems: 'center',
  },
  formulaLabel: { fontSize: 11, fontWeight: '600', color: Colors.textLight, marginBottom: 4, textTransform: 'uppercase', letterSpacing: 0.5 },
  formulaText: {
    fontSize: 18,
    fontWeight: '700',
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
    textAlign: 'center',
  },

  // Definition
  definitionCard: {
    backgroundColor: Colors.background,
    borderRadius: 10,
    padding: 12,
    borderLeftWidth: 3,
  },
  definitionTerm: { fontSize: 14, fontWeight: '700', marginBottom: 3 },
  definitionBody: { fontSize: 14, lineHeight: 21, color: Colors.text },

  // Lists
  listWrap: { gap: 6, paddingLeft: 4 },
  bulletItem: { flexDirection: 'row', alignItems: 'flex-start', gap: 10 },
  bulletDot: { width: 6, height: 6, borderRadius: 3, marginTop: 8 },
  numberedItem: { flexDirection: 'row', alignItems: 'flex-start', gap: 10 },
  numberCircle: { width: 22, height: 22, borderRadius: 11, alignItems: 'center', justifyContent: 'center', marginTop: 1 },
  numberText: { fontSize: 12, fontWeight: '800' },
  listItemText: { flex: 1, fontSize: 14.5, lineHeight: 22, color: Colors.text },

  // Tip / Callout
  tipCard: {
    flexDirection: 'row',
    gap: 10,
    borderRadius: 12,
    padding: 12,
  },
  tipLabel: { fontSize: 12, fontWeight: '700', marginBottom: 2, textTransform: 'uppercase', letterSpacing: 0.3 },
  tipText: { fontSize: 14, lineHeight: 21, color: Colors.text },

  // Example
  exampleCard: {
    backgroundColor: Colors.background,
    borderRadius: 12,
    overflow: 'hidden',
  },
  exampleHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    padding: 10,
    paddingBottom: 6,
  },
  exampleTitle: { fontSize: 13, fontWeight: '700', textTransform: 'uppercase', letterSpacing: 0.3 },
  exampleBody: {
    paddingHorizontal: 12,
    paddingBottom: 12,
    paddingLeft: 16,
    borderLeftWidth: 3,
    marginLeft: 12,
  },
  exampleText: {
    fontSize: 14,
    lineHeight: 22,
    color: Colors.text,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },

  // Divider
  divider: { height: 1, backgroundColor: Colors.border, marginVertical: 4 },

  // Image
  imageWrap: {
    backgroundColor: Colors.background,
    borderRadius: 12,
    overflow: 'hidden',
    marginTop: 4,
  },
  image: {
    width: '100%',
    height: 180,
    borderRadius: 12,
  },

  // Server-generated graphs
  graphWrap: {
    backgroundColor: '#FAFAFA',
    borderRadius: 14,
    overflow: 'hidden',
    marginTop: 6,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  graphImage: {
    width: '100%',
    height: 260,
  },

  // Quiz
  quizCard: {
    backgroundColor: Colors.background,
    borderRadius: 14,
    padding: 14,
    marginTop: 4,
  },
  quizHeader: { marginBottom: 12 },
  quizBadge: {
    alignSelf: 'flex-start',
    paddingHorizontal: 10,
    paddingVertical: 3,
    borderRadius: 8,
    marginBottom: 8,
  },
  quizBadgeText: { fontSize: 12, fontWeight: '800' },
  quizQuestionText: { fontSize: 15, lineHeight: 22, color: Colors.text, fontWeight: '500' },
  quizOptions: { gap: 8 },
  quizOption: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    backgroundColor: Colors.card,
    borderRadius: 12,
    padding: 12,
    borderWidth: 1.5,
    borderColor: Colors.border,
  },
  quizOptionCorrect: {
    borderColor: Colors.green,
    backgroundColor: Colors.green + '08',
  },
  quizOptionWrong: {
    borderColor: Colors.secondary,
    backgroundColor: Colors.secondary + '08',
  },
  quizOptionLetter: {
    width: 32,
    height: 32,
    borderRadius: 10,
    alignItems: 'center',
    justifyContent: 'center',
  },
  quizOptionLetterText: { fontSize: 15, fontWeight: '800' },
  quizOptionText: { flex: 1, fontSize: 14.5, color: Colors.text },

  // Quiz result
  quizResultCard: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 10,
    borderRadius: 12,
    padding: 12,
    marginTop: 4,
  },
  quizResultCorrect: { backgroundColor: Colors.green + '10' },
  quizResultWrong: { backgroundColor: Colors.secondary + '10' },
  quizResultLabel: { fontSize: 14, fontWeight: '800', marginBottom: 2 },
  quizResultExplanation: { fontSize: 14, lineHeight: 20, color: Colors.text },
  scoreRow: { flexDirection: 'row', alignItems: 'center', gap: 4, marginTop: 8 },
  scoreDot: { width: 10, height: 10, borderRadius: 5 },
  scoreText: { fontSize: 12, fontWeight: '700', color: Colors.textLight, marginLeft: 4 },
});
