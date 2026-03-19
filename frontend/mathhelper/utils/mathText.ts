/**
 * mathText.ts — Converts plain-text math notation to proper Unicode symbols.
 *
 * The AI outputs: x^2, sqrt(x), pi, theta, >=, etc.
 * This module converts them to: x², √(x), π, θ, ≥, etc.
 */

// ─── Superscript / Subscript Maps ─────────────────────────────────────────────

const SUPERSCRIPT: Record<string, string> = {
  '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
  '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
  '+': '⁺', '-': '⁻', '=': '⁼', '(': '⁽', ')': '⁾',
  'n': 'ⁿ', 'i': 'ⁱ', 'x': 'ˣ',
};

const SUBSCRIPT: Record<string, string> = {
  '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
  '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
  '+': '₊', '-': '₋', '=': '₌', '(': '₍', ')': '₎',
  'a': 'ₐ', 'e': 'ₑ', 'i': 'ᵢ', 'n': 'ₙ', 'x': 'ₓ',
};

// ─── Greek Letters ────────────────────────────────────────────────────────────

const GREEK: [RegExp, string][] = [
  [/\btheta\b/gi, 'θ'],
  [/\balpha\b/gi, 'α'],
  [/\bbeta\b/gi, 'β'],
  [/\bgamma\b/gi, 'γ'],
  [/\bdelta\b/gi, 'δ'],
  [/\bDelta\b/g, 'Δ'],
  [/\bepsilon\b/gi, 'ε'],
  [/\bsigma\b/gi, 'σ'],
  [/\bSigma\b/g, 'Σ'],
  [/\bomega\b/gi, 'ω'],
  [/\bOmega\b/g, 'Ω'],
  [/\bphi\b/gi, 'φ'],
  [/\blambda\b/gi, 'λ'],
  [/\bmu\b/gi, 'μ'],
  [/\btau\b/gi, 'τ'],
  [/\bpi\b/g, 'π'],
  [/\bPi\b/g, 'Π'],
];

// ─── Operator / Symbol Replacements ───────────────────────────────────────────

const OPERATORS: [RegExp, string][] = [
  [/\bsqrt\(/g, '√('],
  [/\binfinity\b/gi, '∞'],
  [/\bintegral\b/gi, '∫'],
  [/(\s)>=(\s)/g, '$1≥$2'],
  [/(\s)<=(\s)/g, '$1≤$2'],
  [/(\s)!=(\s)/g, '$1≠$2'],
  [/\+-/g, '±'],
  [/(\s)->(\s)/g, '$1→$2'],
  [/\.\.\./g, '…'],
  [/\bapprox\b/gi, '≈'],
];

// ─── Core Functions ───────────────────────────────────────────────────────────

function toSuperscript(s: string): string {
  return s.split('').map(c => SUPERSCRIPT[c] ?? c).join('');
}

function toSubscript(s: string): string {
  return s.split('').map(c => SUBSCRIPT[c] ?? c).join('');
}

/**
 * Replace plain-text math notation with Unicode equivalents.
 */
export function replaceMathSymbols(text: string): string {
  let result = text;

  // Superscripts: x^2, x^{23}, x^n, x^(n+1)
  // Handle braced: x^{...}
  result = result.replace(/\^{([^}]+)}/g, (_, inner) => toSuperscript(inner));
  // Handle parenthesized: x^(n+1) — only short ones
  result = result.replace(/\^(\([^)]{1,6}\))/g, (_, inner) => toSuperscript(inner));
  // Handle single char/digit: x^2, x^n
  result = result.replace(/\^([0-9n])/g, (_, c) => SUPERSCRIPT[c] ?? `^${c}`);

  // Subscripts: x_0, x_{n+1}, a_n
  result = result.replace(/_{([^}]+)}/g, (_, inner) => toSubscript(inner));
  result = result.replace(/_([0-9nxi])\b/g, (_, c) => SUBSCRIPT[c] ?? `_${c}`);

  // Greek letters (word-boundary aware)
  for (const [re, sym] of GREEK) {
    result = result.replace(re, sym);
  }

  // Operators and symbols
  for (const [re, sym] of OPERATORS) {
    result = result.replace(re, sym);
  }

  // Special: * between variables → · (multiplication dot)
  // Only when both sides look like variables/numbers, not in words
  result = result.replace(/([a-zA-Z0-9)π])\*([a-zA-Z0-9(π])/g, '$1·$2');

  return result;
}

/**
 * Segment types for rich inline rendering.
 */
export interface TextSegment {
  type: 'text' | 'bold' | 'italic' | 'math';
  content: string;
}

/**
 * Parse text into styled segments for rich rendering.
 * Handles **bold**, *italic*, and `math` backticks.
 */
export function parseInlineSegments(text: string): TextSegment[] {
  const segments: TextSegment[] = [];
  // Pattern matches: **bold**, *italic*, `code/math`
  const re = /(\*\*(.+?)\*\*)|(\*(.+?)\*)|(`(.+?)`)/g;
  let lastIndex = 0;
  let match: RegExpExecArray | null;

  const processed = replaceMathSymbols(text);

  while ((match = re.exec(processed)) !== null) {
    // Push preceding text
    if (match.index > lastIndex) {
      segments.push({ type: 'text', content: processed.slice(lastIndex, match.index) });
    }

    if (match[2]) {
      segments.push({ type: 'bold', content: match[2] });
    } else if (match[4]) {
      segments.push({ type: 'italic', content: match[4] });
    } else if (match[6]) {
      segments.push({ type: 'math', content: match[6] });
    }

    lastIndex = match.index + match[0].length;
  }

  // Push remaining text
  if (lastIndex < processed.length) {
    segments.push({ type: 'text', content: processed.slice(lastIndex) });
  }

  if (segments.length === 0 && processed.length > 0) {
    segments.push({ type: 'text', content: processed });
  }

  return segments;
}
