/**
 * quickQuestions.ts — Pool of randomized quick-ask questions for the home screen.
 *
 * Each app session (or chat reset) picks 4 questions from the pool,
 * biased toward different categories for variety.
 */

// ─── Types ──────────────────────────────────────────────────────────────────

export interface QuickQuestion {
  text: string;           // Question displayed on chip and sent as chat message
  category: string;       // Subject slug (e.g., 'trigonometry', 'calc-1')
  categoryLabel: string;  // Short display label (e.g., 'Trig', 'Calc 1')
  icon: string;           // Ionicons icon name
}

// ─── Question Pool ──────────────────────────────────────────────────────────

export const QUICK_QUESTIONS_POOL: QuickQuestion[] = [
  // ── Trigonometry (12) ─────────────────────────────────────────────────────
  { text: 'What is the unit circle?', category: 'trigonometry', categoryLabel: 'Trig', icon: 'analytics-outline' },
  { text: 'How do I convert degrees to radians?', category: 'trigonometry', categoryLabel: 'Trig', icon: 'analytics-outline' },
  { text: 'Help me with trig identities', category: 'trigonometry', categoryLabel: 'Trig', icon: 'analytics-outline' },
  { text: 'What is SOH-CAH-TOA?', category: 'trigonometry', categoryLabel: 'Trig', icon: 'analytics-outline' },
  { text: 'How do I find sin(30)?', category: 'trigonometry', categoryLabel: 'Trig', icon: 'analytics-outline' },
  { text: 'How do inverse trig functions work?', category: 'trigonometry', categoryLabel: 'Trig', icon: 'analytics-outline' },
  { text: 'What are the double angle formulas?', category: 'trigonometry', categoryLabel: 'Trig', icon: 'analytics-outline' },
  { text: 'How do I graph y = sin(x)?', category: 'trigonometry', categoryLabel: 'Trig', icon: 'analytics-outline' },
  { text: 'What is the law of cosines?', category: 'trigonometry', categoryLabel: 'Trig', icon: 'analytics-outline' },
  { text: 'How do I solve a right triangle?', category: 'trigonometry', categoryLabel: 'Trig', icon: 'analytics-outline' },
  { text: 'Explain amplitude and period', category: 'trigonometry', categoryLabel: 'Trig', icon: 'analytics-outline' },
  { text: 'What is the law of sines?', category: 'trigonometry', categoryLabel: 'Trig', icon: 'analytics-outline' },

  // ── Calculus 1 (12) ───────────────────────────────────────────────────────
  { text: 'What is a derivative?', category: 'calc-1', categoryLabel: 'Calc 1', icon: 'trending-up-outline' },
  { text: 'Explain the chain rule', category: 'calc-1', categoryLabel: 'Calc 1', icon: 'trending-up-outline' },
  { text: 'How do I find a limit?', category: 'calc-1', categoryLabel: 'Calc 1', icon: 'trending-up-outline' },
  { text: 'What is the power rule?', category: 'calc-1', categoryLabel: 'Calc 1', icon: 'trending-up-outline' },
  { text: 'How does the product rule work?', category: 'calc-1', categoryLabel: 'Calc 1', icon: 'trending-up-outline' },
  { text: 'What is the quotient rule?', category: 'calc-1', categoryLabel: 'Calc 1', icon: 'trending-up-outline' },
  { text: 'How do I find critical points?', category: 'calc-1', categoryLabel: 'Calc 1', icon: 'trending-up-outline' },
  { text: 'What does continuity mean?', category: 'calc-1', categoryLabel: 'Calc 1', icon: 'trending-up-outline' },
  { text: 'How do I use L\'Hopital\'s rule?', category: 'calc-1', categoryLabel: 'Calc 1', icon: 'trending-up-outline' },
  { text: 'What is implicit differentiation?', category: 'calc-1', categoryLabel: 'Calc 1', icon: 'trending-up-outline' },
  { text: 'How do related rates problems work?', category: 'calc-1', categoryLabel: 'Calc 1', icon: 'trending-up-outline' },
  { text: 'What is the mean value theorem?', category: 'calc-1', categoryLabel: 'Calc 1', icon: 'trending-up-outline' },

  // ── Calculus 2 (8) ────────────────────────────────────────────────────────
  { text: 'How do I integrate by parts?', category: 'calc-2', categoryLabel: 'Calc 2', icon: 'infinite-outline' },
  { text: 'What is a Taylor series?', category: 'calc-2', categoryLabel: 'Calc 2', icon: 'infinite-outline' },
  { text: 'How does u-substitution work?', category: 'calc-2', categoryLabel: 'Calc 2', icon: 'infinite-outline' },
  { text: 'What is an improper integral?', category: 'calc-2', categoryLabel: 'Calc 2', icon: 'infinite-outline' },
  { text: 'How do I find a series\' convergence?', category: 'calc-2', categoryLabel: 'Calc 2', icon: 'infinite-outline' },
  { text: 'What is the ratio test?', category: 'calc-2', categoryLabel: 'Calc 2', icon: 'infinite-outline' },
  { text: 'How do partial fractions work?', category: 'calc-2', categoryLabel: 'Calc 2', icon: 'infinite-outline' },
  { text: 'What is a Maclaurin series?', category: 'calc-2', categoryLabel: 'Calc 2', icon: 'infinite-outline' },

  // ── Calculus 3 (7) ────────────────────────────────────────────────────────
  { text: 'What is a partial derivative?', category: 'calc-3', categoryLabel: 'Calc 3', icon: 'cube-outline' },
  { text: 'How do double integrals work?', category: 'calc-3', categoryLabel: 'Calc 3', icon: 'cube-outline' },
  { text: 'What is the gradient vector?', category: 'calc-3', categoryLabel: 'Calc 3', icon: 'cube-outline' },
  { text: 'How do I parametrize a curve?', category: 'calc-3', categoryLabel: 'Calc 3', icon: 'cube-outline' },
  { text: 'What is a line integral?', category: 'calc-3', categoryLabel: 'Calc 3', icon: 'cube-outline' },
  { text: 'How does Stokes\' theorem work?', category: 'calc-3', categoryLabel: 'Calc 3', icon: 'cube-outline' },
  { text: 'What is the divergence theorem?', category: 'calc-3', categoryLabel: 'Calc 3', icon: 'cube-outline' },

  // ── Differential Equations (6) ────────────────────────────────────────────
  { text: 'What is a differential equation?', category: 'diff-eq', categoryLabel: 'Diff Eq', icon: 'git-branch-outline' },
  { text: 'How do I solve separable DEs?', category: 'diff-eq', categoryLabel: 'Diff Eq', icon: 'git-branch-outline' },
  { text: 'What is an integrating factor?', category: 'diff-eq', categoryLabel: 'Diff Eq', icon: 'git-branch-outline' },
  { text: 'How do Laplace transforms work?', category: 'diff-eq', categoryLabel: 'Diff Eq', icon: 'git-branch-outline' },
  { text: 'What are linear first-order DEs?', category: 'diff-eq', categoryLabel: 'Diff Eq', icon: 'git-branch-outline' },
  { text: 'How do I solve exact equations?', category: 'diff-eq', categoryLabel: 'Diff Eq', icon: 'git-branch-outline' },

  // ── Linear Algebra (6) ────────────────────────────────────────────────────
  { text: 'What is a matrix determinant?', category: 'linear-algebra', categoryLabel: 'Linear Alg', icon: 'grid-outline' },
  { text: 'How do eigenvalues work?', category: 'linear-algebra', categoryLabel: 'Linear Alg', icon: 'grid-outline' },
  { text: 'What is row echelon form?', category: 'linear-algebra', categoryLabel: 'Linear Alg', icon: 'grid-outline' },
  { text: 'How do I multiply two matrices?', category: 'linear-algebra', categoryLabel: 'Linear Alg', icon: 'grid-outline' },
  { text: 'What is a vector space?', category: 'linear-algebra', categoryLabel: 'Linear Alg', icon: 'grid-outline' },
  { text: 'How do I find a matrix inverse?', category: 'linear-algebra', categoryLabel: 'Linear Alg', icon: 'grid-outline' },

  // ── General / Algebra (5) ─────────────────────────────────────────────────
  { text: 'How do I factor x\u00B2 - 9?', category: 'algebra', categoryLabel: 'Algebra', icon: 'calculator-outline' },
  { text: 'How do I solve a quadratic?', category: 'algebra', categoryLabel: 'Algebra', icon: 'calculator-outline' },
  { text: 'What is the quadratic formula?', category: 'algebra', categoryLabel: 'Algebra', icon: 'calculator-outline' },
  { text: 'How do I simplify a fraction?', category: 'algebra', categoryLabel: 'Algebra', icon: 'calculator-outline' },
  { text: 'What are exponent rules?', category: 'algebra', categoryLabel: 'Algebra', icon: 'calculator-outline' },
];

// ─── Helpers ────────────────────────────────────────────────────────────────

/**
 * Fisher-Yates (Knuth) shuffle — mutates in-place and returns the array.
 */
function shuffle<T>(arr: T[]): T[] {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

/**
 * Pick `count` questions from the pool, biased toward different categories.
 *
 * Algorithm:
 *  1. Group questions by category and shuffle each group.
 *  2. Shuffle the category order.
 *  3. Round-robin one question per category until we have `count`.
 *  4. If we run out of categories, loop back through them.
 *
 * This ensures maximum category diversity in the selected set.
 */
export function pickRandomQuestions(count = 4): QuickQuestion[] {
  // Group by category
  const groups = new Map<string, QuickQuestion[]>();
  for (const q of QUICK_QUESTIONS_POOL) {
    if (!groups.has(q.category)) groups.set(q.category, []);
    groups.get(q.category)!.push({ ...q }); // shallow-copy so we don't mutate pool
  }

  // Shuffle each category group internally
  for (const group of groups.values()) {
    shuffle(group);
  }

  // Shuffle category order
  const categoryKeys = shuffle([...groups.keys()]);

  // Round-robin pick
  const result: QuickQuestion[] = [];
  let catIdx = 0;

  while (result.length < count && categoryKeys.length > 0) {
    const key = categoryKeys[catIdx % categoryKeys.length];
    const group = groups.get(key)!;

    if (group.length > 0) {
      result.push(group.pop()!);
    } else {
      // Category exhausted — remove it and adjust index
      categoryKeys.splice(catIdx % categoryKeys.length, 1);
      if (categoryKeys.length === 0) break;
      continue; // don't increment catIdx so we try the next key at this position
    }

    catIdx++;
  }

  // Final shuffle so categories aren't in a predictable order
  return shuffle(result);
}
