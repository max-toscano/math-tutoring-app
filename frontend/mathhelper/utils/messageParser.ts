/**
 * messageParser.ts — Parses AI message text into structured content blocks.
 *
 * The AI returns conversational text with predictable patterns:
 * - **Bold:** headings
 * - Bullet lists (- or *)
 * - Numbered lists (1. 2. 3.)
 * - Math formulas on their own line
 * - Tip/Note/Remember callouts
 * - --- dividers
 */

import { replaceMathSymbols } from './mathText';

// ─── Block Types ──────────────────────────────────────────────────────────────

export type ContentBlock =
  | { type: 'paragraph'; text: string }
  | { type: 'heading'; text: string }
  | { type: 'formula'; expression: string; label?: string }
  | { type: 'bullet_list'; items: string[] }
  | { type: 'numbered_list'; items: string[] }
  | { type: 'tip'; text: string; variant: 'tip' | 'note' | 'remember' | 'important' | 'warning' }
  | { type: 'definition'; term: string; body: string }
  | { type: 'divider' }
  | { type: 'example'; title: string; body: string };

// ─── Detection Helpers ────────────────────────────────────────────────────────

const HEADING_RE = /^\*\*(.+?)\*\*\s*$/;
const DEFINITION_RE = /^\*\*(.+?):\*\*\s*(.+)/;
const BULLET_RE = /^[-*•]\s+(.+)/;
const NUMBERED_RE = /^\d+[.)]\s+(.+)/;
const DIVIDER_RE = /^-{3,}$|^={3,}$/;
const TIP_RE = /^(Tip|Note|Remember|Important|Warning|Hint|Common mistake):\s*(.+)/i;
const EXAMPLE_RE = /^(Example\s*\d*|Worked Example|Step-by-step):\s*(.*)/i;

// A line is likely a standalone formula if it's mostly math symbols and short
function isFormulaLine(line: string): boolean {
  if (line.length > 120 || line.length < 3) return false;
  // Must contain = or an operator and mostly non-letter chars
  const hasEquals = /[=≤≥<>]/.test(line);
  const hasMathChars = /[\^√πθ∫∞²³⁴⁵⁶⁷⁸⁹⁰±·]/.test(line) || /[+\-*/=()[\]{}]/.test(line);
  const letterRatio = (line.match(/[a-zA-Z]/g)?.length ?? 0) / line.length;
  // If it has equals and is short with low letter ratio, it's likely a formula
  return hasEquals && hasMathChars && letterRatio < 0.5 && line.split(' ').length <= 12;
}

// ─── Main Parser ──────────────────────────────────────────────────────────────

export function parseMessageBlocks(rawText: string): ContentBlock[] {
  const text = replaceMathSymbols(rawText);
  const lines = text.split('\n');
  const blocks: ContentBlock[] = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i].trim();

    // Skip empty lines
    if (!line) { i++; continue; }

    // Divider
    if (DIVIDER_RE.test(line)) {
      blocks.push({ type: 'divider' });
      i++; continue;
    }

    // Tip / Note / Remember callout
    const tipMatch = line.match(TIP_RE);
    if (tipMatch) {
      const variant = tipMatch[1].toLowerCase() as any;
      blocks.push({ type: 'tip', text: tipMatch[2], variant: variant === 'hint' ? 'tip' : variant === 'common mistake' ? 'warning' : variant });
      i++; continue;
    }

    // Example block
    const exampleMatch = line.match(EXAMPLE_RE);
    if (exampleMatch) {
      const title = exampleMatch[1];
      const firstLine = exampleMatch[2];
      // Collect subsequent indented/continued lines
      const bodyLines = firstLine ? [firstLine] : [];
      i++;
      while (i < lines.length && lines[i].trim() && !DIVIDER_RE.test(lines[i].trim()) && !HEADING_RE.test(lines[i].trim())) {
        bodyLines.push(lines[i].trim());
        i++;
      }
      blocks.push({ type: 'example', title, body: bodyLines.join('\n') });
      continue;
    }

    // Heading (standalone bold line)
    const headingMatch = line.match(HEADING_RE);
    if (headingMatch) {
      blocks.push({ type: 'heading', text: headingMatch[1] });
      i++; continue;
    }

    // Definition (bold term followed by text)
    const defMatch = line.match(DEFINITION_RE);
    if (defMatch) {
      blocks.push({ type: 'definition', term: defMatch[1], body: defMatch[2] });
      i++; continue;
    }

    // Bullet list (collect consecutive)
    if (BULLET_RE.test(line)) {
      const items: string[] = [];
      while (i < lines.length && BULLET_RE.test(lines[i].trim())) {
        items.push(lines[i].trim().match(BULLET_RE)![1]);
        i++;
      }
      blocks.push({ type: 'bullet_list', items });
      continue;
    }

    // Numbered list (collect consecutive)
    if (NUMBERED_RE.test(line)) {
      const items: string[] = [];
      while (i < lines.length && NUMBERED_RE.test(lines[i].trim())) {
        items.push(lines[i].trim().match(NUMBERED_RE)![1]);
        i++;
      }
      blocks.push({ type: 'numbered_list', items });
      continue;
    }

    // Formula (standalone math-heavy line)
    if (isFormulaLine(line)) {
      // Check if previous block could be a label
      const prev = blocks[blocks.length - 1];
      const label = prev?.type === 'paragraph' && prev.text.length < 60 ? prev.text : undefined;
      if (label) blocks.pop(); // remove label paragraph, it becomes formula label
      blocks.push({ type: 'formula', expression: line, label });
      i++; continue;
    }

    // Default: paragraph
    // Collect consecutive non-special lines into one paragraph
    const paraLines: string[] = [line];
    i++;
    while (
      i < lines.length &&
      lines[i].trim() &&
      !DIVIDER_RE.test(lines[i].trim()) &&
      !HEADING_RE.test(lines[i].trim()) &&
      !DEFINITION_RE.test(lines[i].trim()) &&
      !BULLET_RE.test(lines[i].trim()) &&
      !NUMBERED_RE.test(lines[i].trim()) &&
      !TIP_RE.test(lines[i].trim()) &&
      !EXAMPLE_RE.test(lines[i].trim()) &&
      !isFormulaLine(lines[i].trim())
    ) {
      paraLines.push(lines[i].trim());
      i++;
    }
    blocks.push({ type: 'paragraph', text: paraLines.join(' ') });
  }

  return blocks;
}
