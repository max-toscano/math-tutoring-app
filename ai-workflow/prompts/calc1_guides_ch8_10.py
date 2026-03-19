"""
Calc 1 curriculum guides for Chapters 8-10:
  Ch 8 - Analyzing Functions with Derivatives
  Ch 9 - Optimization
  Ch 10 - Introduction to Integration

Each entry maps a slug to a guide dict with teaching content, quiz guidelines,
practice problems, and metadata.
"""

CALC1_GUIDES_CH8_10 = {

    # =========================================================================
    # CHAPTER 8 — Analyzing Functions with Derivatives
    # =========================================================================

    "increasing-decreasing": {
        "id": "calc1-8-1",
        "slug": "increasing-decreasing",
        "title": "Increasing and Decreasing Functions",
        "chapter": 8,
        "chapter_title": "Analyzing Functions with Derivatives",
        "subject": "calc-1",
        "prerequisites": ["derivative-rules", "chain-rule"],
        "estimated_time": "30 min",
        "difficulty": "medium",
        "teaching_content": (
            "CHUNK 1: The Connection Between f' and Increasing/Decreasing\n"
            "\n"
            "The derivative tells us the slope of the tangent line, and slope tells us direction.\n"
            "\n"
            "Core rules:\n"
            "- If f'(x) > 0 on an interval, then f is INCREASING on that interval.\n"
            "- If f'(x) < 0 on an interval, then f is DECREASING on that interval.\n"
            "- If f'(x) = 0 on an entire interval, then f is CONSTANT on that interval.\n"
            "\n"
            "Think of it this way: positive slope means the function goes uphill (left to right), "
            "negative slope means it goes downhill.\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 2: Critical Points\n"
            "\n"
            "A critical point of f is a value x = c in the domain of f where either:\n"
            "  1) f'(c) = 0, OR\n"
            "  2) f'(c) does not exist (DNE)\n"
            "\n"
            "Critical points are the ONLY places where f can change from increasing to decreasing "
            "or vice versa. They are the candidates for local maxima and minima.\n"
            "\n"
            "Example: Find the critical points of f(x) = x^3 - 3x + 1.\n"
            "  f'(x) = 3x^2 - 3 = 3(x^2 - 1) = 3(x - 1)(x + 1)\n"
            "  Set f'(x) = 0: x = -1 and x = 1.\n"
            "  f' exists everywhere, so the only critical points are x = -1 and x = 1.\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 3: The Sign Chart Method\n"
            "\n"
            "To determine where f is increasing or decreasing:\n"
            "  Step 1: Find f'(x).\n"
            "  Step 2: Find all critical points (where f' = 0 or DNE).\n"
            "  Step 3: Plot critical points on a number line, creating intervals.\n"
            "  Step 4: Pick a test point in each interval. Plug into f' to find the sign.\n"
            "  Step 5: f' > 0 means increasing, f' < 0 means decreasing.\n"
            "\n"
            "Worked Example: f(x) = x^3 - 3x + 1\n"
            "  f'(x) = 3(x - 1)(x + 1)\n"
            "  Critical points: x = -1, x = 1\n"
            "  Intervals: (-inf, -1), (-1, 1), (1, inf)\n"
            "\n"
            "  Test x = -2: f'(-2) = 3((-2)-1)((-2)+1) = 3(-3)(-1) = 9 > 0 => increasing\n"
            "  Test x = 0:  f'(0) = 3(0-1)(0+1) = 3(-1)(1) = -3 < 0 => decreasing\n"
            "  Test x = 2:  f'(2) = 3(2-1)(2+1) = 3(1)(3) = 9 > 0 => increasing\n"
            "\n"
            "  Conclusion: f is increasing on (-inf, -1) and (1, inf), decreasing on (-1, 1).\n"
            "\n"
            "Worked Example 2: f(x) = x^(2/3)\n"
            "  f'(x) = (2/3)x^(-1/3) = 2 / (3 * x^(1/3))\n"
            "  f'(0) is undefined (division by zero), and f'(x) never equals 0.\n"
            "  Critical point: x = 0 (f' DNE but f(0) exists).\n"
            "  Test x = -1: f'(-1) = 2/(3*(-1)) = -2/3 < 0 => decreasing\n"
            "  Test x = 1:  f'(1) = 2/3 > 0 => increasing\n"
            "  So f is decreasing on (-inf, 0) and increasing on (0, inf).\n"
        ),
        "key_concepts": [
            "f'(x) > 0 means f is increasing",
            "f'(x) < 0 means f is decreasing",
            "Critical point: f'(c) = 0 or f'(c) DNE",
            "Sign chart method for classifying intervals",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Ask students to find critical points of a polynomial and determine intervals "
            "of increase/decrease. Include one problem where f' DNE at a point. "
            "Test whether students can build a sign chart and interpret results."
        ),
        "practice_problems": [
            {
                "problem": "Find the intervals where f(x) = 2x^3 - 9x^2 + 12x is increasing and decreasing.",
                "answer": (
                    "f'(x) = 6x^2 - 18x + 12 = 6(x^2 - 3x + 2) = 6(x-1)(x-2). "
                    "Critical points: x=1, x=2. "
                    "Test intervals: f'(0)=12>0, f'(1.5)=6(0.5)(-0.5)=-1.5<0, f'(3)=6(2)(1)=12>0. "
                    "Increasing on (-inf,1) and (2,inf). Decreasing on (1,2)."
                ),
            },
            {
                "problem": "Find the critical points of g(x) = x^4 - 4x^3.",
                "answer": (
                    "g'(x) = 4x^3 - 12x^2 = 4x^2(x - 3). "
                    "Set g'(x) = 0: x = 0 and x = 3. "
                    "Both are critical points."
                ),
            },
            {
                "problem": "Find the critical points and intervals of increase/decrease for h(x) = x + 4/x, x != 0.",
                "answer": (
                    "h'(x) = 1 - 4/x^2 = (x^2 - 4)/x^2. "
                    "h'(x) = 0 when x^2 = 4, so x = -2, x = 2. h' DNE at x = 0 (not in domain). "
                    "Test intervals: h'(-3) = 5/9 > 0 (inc), h'(-1) = -3 < 0 (dec), "
                    "h'(1) = -3 < 0 (dec), h'(3) = 5/9 > 0 (inc). "
                    "Increasing on (-inf,-2) and (2,inf). Decreasing on (-2,0) and (0,2)."
                ),
            },
        ],
        "common_mistakes": [
            "Forgetting to check where f' is undefined (not just where f' = 0)",
            "Plugging test points into f(x) instead of f'(x)",
            "Saying a function is increasing at a single point instead of on an interval",
        ],
        "builds_toward": ["first-derivative-test", "curve-sketching"],
    },

    "first-derivative-test": {
        "id": "calc1-8-2",
        "slug": "first-derivative-test",
        "title": "The First Derivative Test",
        "chapter": 8,
        "chapter_title": "Analyzing Functions with Derivatives",
        "subject": "calc-1",
        "prerequisites": ["increasing-decreasing"],
        "estimated_time": "25 min",
        "difficulty": "medium",
        "teaching_content": (
            "CHUNK 1: What the First Derivative Test Does\n"
            "\n"
            "We know critical points are CANDIDATES for local extrema. The First Derivative Test "
            "tells us which critical points are actually local maxima, local minima, or neither.\n"
            "\n"
            "The idea: look at how f' changes sign around a critical point c.\n"
            "\n"
            "First Derivative Test:\n"
            "  - If f' changes from POSITIVE to NEGATIVE at c => f has a LOCAL MAXIMUM at c.\n"
            "    (function goes up then down — it peaked)\n"
            "  - If f' changes from NEGATIVE to POSITIVE at c => f has a LOCAL MINIMUM at c.\n"
            "    (function goes down then up — it bottomed out)\n"
            "  - If f' does NOT change sign at c => f has NEITHER a max nor min at c.\n"
            "    (function keeps going the same direction)\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 2: Worked Examples\n"
            "\n"
            "Example 1: f(x) = x^3 - 3x + 1\n"
            "  f'(x) = 3(x-1)(x+1). Critical points: x = -1, x = 1.\n"
            "  Sign chart from previous lesson:\n"
            "    (-inf, -1): f' > 0 | (-1, 1): f' < 0 | (1, inf): f' > 0\n"
            "  At x = -1: f' changes from + to - => LOCAL MAXIMUM. f(-1) = (-1)^3 - 3(-1) + 1 = 3.\n"
            "  At x = 1:  f' changes from - to + => LOCAL MINIMUM. f(1) = 1 - 3 + 1 = -1.\n"
            "\n"
            "Example 2: f(x) = x^4\n"
            "  f'(x) = 4x^3. Critical point: x = 0.\n"
            "  Test x = -1: f'(-1) = -4 < 0 (decreasing)\n"
            "  Test x = 1:  f'(1) = 4 > 0 (increasing)\n"
            "  At x = 0: f' changes from - to + => LOCAL MINIMUM at (0, 0).\n"
            "\n"
            "Example 3: f(x) = x^3\n"
            "  f'(x) = 3x^2. Critical point: x = 0.\n"
            "  Test x = -1: f'(-1) = 3 > 0 (increasing)\n"
            "  Test x = 1:  f'(1) = 3 > 0 (increasing)\n"
            "  At x = 0: f' does NOT change sign (+ to +) => NEITHER max nor min.\n"
            "  The point (0,0) is an inflection point, not an extremum.\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 3: Strategy and Common Patterns\n"
            "\n"
            "Quick-reference pattern for polynomial critical points:\n"
            "  - If the factor (x - c) appears to an ODD power in f'(x), f' CHANGES sign at c.\n"
            "  - If the factor (x - c) appears to an EVEN power in f'(x), f' does NOT change sign.\n"
            "\n"
            "Example: f'(x) = (x-1)^2 * (x-3)\n"
            "  Critical points: x = 1 (even power, no sign change) and x = 3 (odd power, sign change).\n"
            "  So x = 1 is neither max nor min, and x = 3 needs a sign check.\n"
            "  Test x = 0: f'(0) = (1)(−3) = −3 < 0\n"
            "  Test x = 2: f'(2) = (1)(−1) = −1 < 0\n"
            "  Test x = 4: f'(4) = (9)(1) = 9 > 0\n"
            "  At x = 3: f' goes from − to + => LOCAL MINIMUM.\n"
            "  At x = 1: f' stays negative => NEITHER.\n"
        ),
        "key_concepts": [
            "f' changes + to - at c => local maximum",
            "f' changes - to + at c => local minimum",
            "f' no sign change at c => neither max nor min",
            "Even-power factor in f' means no sign change",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Give students a function, ask them to find all critical points and use the first "
            "derivative test to classify each one. Include a case where f' does not change sign."
        ),
        "practice_problems": [
            {
                "problem": "Use the first derivative test to classify the critical points of f(x) = x^3 - 6x^2 + 9x + 2.",
                "answer": (
                    "f'(x) = 3x^2 - 12x + 9 = 3(x^2 - 4x + 3) = 3(x-1)(x-3). "
                    "Critical points: x=1, x=3. "
                    "Test x=0: f'=3(−1)(−3)=9>0. Test x=2: f'=3(1)(−1)=−3<0. Test x=4: f'=3(3)(1)=9>0. "
                    "At x=1: + to − => local max, f(1)=6. "
                    "At x=3: − to + => local min, f(3)=2."
                ),
            },
            {
                "problem": "Classify the critical points of g(x) = 3x^5 - 5x^3.",
                "answer": (
                    "g'(x) = 15x^4 - 15x^2 = 15x^2(x^2 - 1) = 15x^2(x-1)(x+1). "
                    "Critical points: x = -1, 0, 1. "
                    "x = 0 has even-power factor x^2 => neither. "
                    "Test x=-2: g'>0. Test x=-0.5: g'>0 (confirming no sign change at 0 from left). "
                    "Actually: test x=-2: 15(4)(3)=180>0. test x=-0.5: 15(0.25)(-0.75)=-2.8<0. "
                    "test x=0.5: 15(0.25)(-0.75)=-2.8<0. test x=2: 15(4)(3)=180>0. "
                    "At x=-1: + to - => local max, g(-1)=2. "
                    "At x=0: - to - => neither. "
                    "At x=1: - to + => local min, g(1)=-2."
                ),
            },
        ],
        "common_mistakes": [
            "Confusing the sign of f'(x) with the sign of f(x) — always check the derivative",
            "Assuming every critical point is a local extremum",
            "Forgetting to evaluate f(c) to report the actual max/min VALUE",
        ],
        "builds_toward": ["second-derivative-test", "curve-sketching"],
    },

    "concavity-second-derivative": {
        "id": "calc1-8-3",
        "slug": "concavity-second-derivative",
        "title": "Concavity and the Second Derivative",
        "chapter": 8,
        "chapter_title": "Analyzing Functions with Derivatives",
        "subject": "calc-1",
        "prerequisites": ["increasing-decreasing", "first-derivative-test"],
        "estimated_time": "30 min",
        "difficulty": "medium",
        "teaching_content": (
            "CHUNK 1: What Is Concavity?\n"
            "\n"
            "Concavity describes the 'bending' of a curve:\n"
            "  - CONCAVE UP (like a cup, or a smile): the curve bends upward. "
            "Tangent lines lie BELOW the curve. f' is increasing.\n"
            "  - CONCAVE DOWN (like a frown): the curve bends downward. "
            "Tangent lines lie ABOVE the curve. f' is decreasing.\n"
            "\n"
            "The second derivative controls concavity:\n"
            "  - f''(x) > 0 on an interval => f is CONCAVE UP on that interval.\n"
            "  - f''(x) < 0 on an interval => f is CONCAVE DOWN on that interval.\n"
            "\n"
            "Why? Because f'' is the derivative of f'. If f'' > 0, then f' is increasing — "
            "the slopes are getting steeper (or less negative), which means the curve bends upward.\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 2: Inflection Points\n"
            "\n"
            "An inflection point is where the concavity CHANGES (from up to down or down to up).\n"
            "\n"
            "To find inflection points:\n"
            "  Step 1: Find f''(x).\n"
            "  Step 2: Find where f''(x) = 0 or f''(x) DNE.\n"
            "  Step 3: Check that f'' actually CHANGES SIGN at that point.\n"
            "\n"
            "IMPORTANT: f''(c) = 0 does NOT guarantee an inflection point. You must verify "
            "the sign change. For example, f(x) = x^4 has f''(x) = 12x^2, and f''(0) = 0, "
            "but f'' >= 0 everywhere, so no sign change and no inflection point.\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 3: Worked Examples\n"
            "\n"
            "Example 1: f(x) = x^3 - 3x^2 + 2\n"
            "  f'(x) = 3x^2 - 6x\n"
            "  f''(x) = 6x - 6 = 6(x - 1)\n"
            "  f''(x) = 0 when x = 1.\n"
            "  Test x = 0: f''(0) = -6 < 0 => concave down\n"
            "  Test x = 2: f''(2) = 6 > 0 => concave up\n"
            "  f'' changes sign at x = 1 => inflection point at (1, f(1)) = (1, 0).\n"
            "  Concave down on (-inf, 1), concave up on (1, inf).\n"
            "\n"
            "Example 2: f(x) = x^4 - 6x^2\n"
            "  f'(x) = 4x^3 - 12x\n"
            "  f''(x) = 12x^2 - 12 = 12(x^2 - 1) = 12(x-1)(x+1)\n"
            "  f''(x) = 0 when x = -1 and x = 1.\n"
            "  Test x = -2: f''(-2) = 12(3) = 36 > 0 => concave up\n"
            "  Test x = 0:  f''(0) = -12 < 0 => concave down\n"
            "  Test x = 2:  f''(2) = 36 > 0 => concave up\n"
            "  Inflection points at x = -1 and x = 1.\n"
            "  f(-1) = 1 - 6 = -5, f(1) = 1 - 6 = -5.\n"
            "  Inflection points: (-1, -5) and (1, -5).\n"
            "\n"
            "Example 3: f(x) = x^(1/3)\n"
            "  f'(x) = (1/3)x^(-2/3)\n"
            "  f''(x) = (-2/9)x^(-5/3)\n"
            "  f'' is never 0, but f''(0) DNE.\n"
            "  Test x = -1: f''(-1) = (-2/9)(-1) = 2/9 > 0 => concave up\n"
            "  Test x = 1:  f''(1) = -2/9 < 0 => concave down\n"
            "  Sign change at x = 0 => inflection point at (0, 0).\n"
        ),
        "key_concepts": [
            "f''(x) > 0 => concave up",
            "f''(x) < 0 => concave down",
            "Inflection point: where f'' changes sign",
            "f''(c) = 0 alone does not guarantee an inflection point",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Ask students to find intervals of concavity and inflection points. Include "
            "a problem where f''(c) = 0 but there is no inflection point."
        ),
        "practice_problems": [
            {
                "problem": "Find the intervals of concavity and inflection points of f(x) = x^3 + 3x^2 - 9x + 4.",
                "answer": (
                    "f'(x) = 3x^2 + 6x - 9. f''(x) = 6x + 6 = 6(x + 1). "
                    "f''=0 at x = -1. Test x=-2: f''=-6<0 (concave down). Test x=0: f''=6>0 (concave up). "
                    "Sign changes at x=-1 => inflection point. f(-1) = -1+3+9+4 = 15. "
                    "Concave down on (-inf,-1), concave up on (-1,inf). Inflection point: (-1, 15)."
                ),
            },
            {
                "problem": "Find the inflection points of g(x) = x^4 - 4x^3 + 6x^2.",
                "answer": (
                    "g'(x) = 4x^3 - 12x^2 + 12x. g''(x) = 12x^2 - 24x + 12 = 12(x^2 - 2x + 1) = 12(x-1)^2. "
                    "g''(x) = 0 at x = 1, but g''(x) = 12(x-1)^2 >= 0 for all x. "
                    "No sign change => NO inflection point. g is concave up everywhere."
                ),
            },
            {
                "problem": "Find the concavity intervals for h(x) = sin(x) on [0, 2*pi].",
                "answer": (
                    "h'(x) = cos(x). h''(x) = -sin(x). "
                    "h''(x) = 0 at x = pi. "
                    "On (0, pi): -sin(x) < 0 => concave down. "
                    "On (pi, 2*pi): -sin(x) > 0 => concave up. "
                    "Inflection point at (pi, 0)."
                ),
            },
        ],
        "common_mistakes": [
            "Assuming f''(c) = 0 always gives an inflection point without checking sign change",
            "Confusing concave up/down with increasing/decreasing",
            "Forgetting to check where f'' is undefined",
        ],
        "builds_toward": ["second-derivative-test", "curve-sketching"],
    },

    "second-derivative-test": {
        "id": "calc1-8-4",
        "slug": "second-derivative-test",
        "title": "The Second Derivative Test",
        "chapter": 8,
        "chapter_title": "Analyzing Functions with Derivatives",
        "subject": "calc-1",
        "prerequisites": ["first-derivative-test", "concavity-second-derivative"],
        "estimated_time": "20 min",
        "difficulty": "medium",
        "teaching_content": (
            "CHUNK 1: The Second Derivative Test\n"
            "\n"
            "The Second Derivative Test is a quick way to classify critical points where f'(c) = 0.\n"
            "\n"
            "Suppose f'(c) = 0 and f''(c) exists. Then:\n"
            "  - If f''(c) > 0 => f has a LOCAL MINIMUM at c.\n"
            "    (Concave up at c means the curve opens upward — it's a valley.)\n"
            "  - If f''(c) < 0 => f has a LOCAL MAXIMUM at c.\n"
            "    (Concave down at c means the curve opens downward — it's a peak.)\n"
            "  - If f''(c) = 0 => the test is INCONCLUSIVE. Use the first derivative test instead.\n"
            "\n"
            "When to use each test:\n"
            "  - Second derivative test: quick and clean when f'' is easy to compute and f''(c) != 0.\n"
            "  - First derivative test: always works, required when f''(c) = 0 or f'' is hard to find.\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 2: Worked Examples\n"
            "\n"
            "Example 1: f(x) = x^3 - 12x + 5\n"
            "  f'(x) = 3x^2 - 12 = 3(x^2 - 4) = 3(x-2)(x+2)\n"
            "  Critical points: x = -2, x = 2.\n"
            "  f''(x) = 6x.\n"
            "  At x = -2: f''(-2) = -12 < 0 => LOCAL MAXIMUM. f(-2) = -8 + 24 + 5 = 21.\n"
            "  At x = 2:  f''(2) = 12 > 0 => LOCAL MINIMUM. f(2) = 8 - 24 + 5 = -11.\n"
            "\n"
            "Example 2: f(x) = x^4\n"
            "  f'(x) = 4x^3. Critical point: x = 0.\n"
            "  f''(x) = 12x^2. f''(0) = 0 => INCONCLUSIVE.\n"
            "  Fall back to the first derivative test:\n"
            "    f'(-1) = -4 < 0, f'(1) = 4 > 0 => sign changes from - to + => local minimum.\n"
            "\n"
            "Example 3: f(x) = 2x^3 + 3x^2 - 36x\n"
            "  f'(x) = 6x^2 + 6x - 36 = 6(x^2 + x - 6) = 6(x+3)(x-2)\n"
            "  Critical points: x = -3, x = 2.\n"
            "  f''(x) = 12x + 6.\n"
            "  At x = -3: f''(-3) = -36 + 6 = -30 < 0 => LOCAL MAXIMUM. f(-3) = -54+27+108 = 81.\n"
            "  At x = 2:  f''(2) = 24 + 6 = 30 > 0 => LOCAL MINIMUM. f(2) = 16+12-72 = -44.\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 3: When to Use Which Test\n"
            "\n"
            "Summary comparison:\n"
            "  First Derivative Test:\n"
            "    + Always works.\n"
            "    + Handles critical points where f' DNE.\n"
            "    - Requires a sign chart (more steps).\n"
            "\n"
            "  Second Derivative Test:\n"
            "    + Quick when f'' is easy to compute.\n"
            "    - Only works when f'(c) = 0 AND f''(c) != 0.\n"
            "    - Cannot classify critical points where f' DNE.\n"
            "\n"
            "Tip: On an exam, if you compute f''(c) and get 0, don't waste time — immediately "
            "switch to the first derivative test.\n"
        ),
        "key_concepts": [
            "f'(c)=0 and f''(c)>0 => local minimum",
            "f'(c)=0 and f''(c)<0 => local maximum",
            "f''(c)=0 => test is inconclusive, use first derivative test",
            "Second derivative test cannot handle points where f' DNE",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Give a function and ask students to find and classify critical points using "
            "the second derivative test. Include one critical point where the test is inconclusive."
        ),
        "practice_problems": [
            {
                "problem": "Use the second derivative test to classify the critical points of f(x) = x^4 - 8x^2 + 3.",
                "answer": (
                    "f'(x) = 4x^3 - 16x = 4x(x^2 - 4) = 4x(x-2)(x+2). "
                    "Critical points: x = -2, 0, 2. "
                    "f''(x) = 12x^2 - 16. "
                    "f''(-2) = 48 - 16 = 32 > 0 => local min. f(-2) = 16-32+3 = -13. "
                    "f''(0) = -16 < 0 => local max. f(0) = 3. "
                    "f''(2) = 48-16 = 32 > 0 => local min. f(2) = 16-32+3 = -13."
                ),
            },
            {
                "problem": "Classify the critical points of g(x) = x^5 - 5x using the second derivative test.",
                "answer": (
                    "g'(x) = 5x^4 - 5 = 5(x^4 - 1) = 5(x^2-1)(x^2+1) = 5(x-1)(x+1)(x^2+1). "
                    "Critical points: x = -1, x = 1. "
                    "g''(x) = 20x^3. "
                    "g''(-1) = -20 < 0 => local max. g(-1) = -1+5 = 4. "
                    "g''(1) = 20 > 0 => local min. g(1) = 1-5 = -4."
                ),
            },
        ],
        "common_mistakes": [
            "Trying to use the second derivative test when f''(c) = 0 (it is inconclusive)",
            "Mixing up the conclusion: f'' > 0 is concave UP which means local MIN (not max)",
            "Forgetting to compute the actual y-value f(c) of the extremum",
        ],
        "builds_toward": ["curve-sketching", "applied-optimization"],
    },

    "curve-sketching": {
        "id": "calc1-8-5",
        "slug": "curve-sketching",
        "title": "Curve Sketching",
        "chapter": 8,
        "chapter_title": "Analyzing Functions with Derivatives",
        "subject": "calc-1",
        "prerequisites": [
            "increasing-decreasing",
            "first-derivative-test",
            "concavity-second-derivative",
            "second-derivative-test",
        ],
        "estimated_time": "40 min",
        "difficulty": "hard",
        "teaching_content": (
            "CHUNK 1: The 7-Step Curve Sketching Process\n"
            "\n"
            "To sketch a curve y = f(x), follow these steps systematically:\n"
            "\n"
            "  Step 1: DOMAIN — What x-values are allowed?\n"
            "  Step 2: INTERCEPTS — Set x=0 for y-intercept, y=0 for x-intercepts.\n"
            "  Step 3: SYMMETRY — Is f even (symmetric about y-axis), odd (symmetric about origin), or neither?\n"
            "  Step 4: ASYMPTOTES\n"
            "    - Vertical: where denominator = 0 (for rational functions)\n"
            "    - Horizontal: lim as x -> +/-inf\n"
            "    - Oblique/slant: if degree of numerator = degree of denominator + 1\n"
            "  Step 5: FIRST DERIVATIVE ANALYSIS — f'(x). Find critical points, intervals of "
            "increase/decrease, local extrema.\n"
            "  Step 6: SECOND DERIVATIVE ANALYSIS — f''(x). Find concavity intervals and inflection points.\n"
            "  Step 7: SKETCH — Plot key points (intercepts, extrema, inflection points), draw asymptotes, "
            "then connect with a smooth curve respecting all the information.\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 2: Full Worked Example — Rational Function\n"
            "\n"
            "Sketch f(x) = (2x^2) / (x^2 - 1).\n"
            "\n"
            "Step 1: Domain. x^2 - 1 = 0 when x = +/-1. Domain: all real x except x = -1, 1.\n"
            "\n"
            "Step 2: Intercepts.\n"
            "  y-intercept: f(0) = 0/(-1) = 0. Point: (0, 0).\n"
            "  x-intercept: 2x^2 = 0 => x = 0. Point: (0, 0).\n"
            "\n"
            "Step 3: Symmetry. f(-x) = 2(-x)^2/((-x)^2-1) = 2x^2/(x^2-1) = f(x). So f is EVEN "
            "(symmetric about the y-axis).\n"
            "\n"
            "Step 4: Asymptotes.\n"
            "  Vertical: x = -1 and x = 1 (denominator = 0).\n"
            "  Horizontal: lim x->inf 2x^2/(x^2-1) = lim 2/(1-1/x^2) = 2. So y = 2 is a horizontal asymptote.\n"
            "\n"
            "Step 5: First derivative.\n"
            "  f'(x) = [4x(x^2-1) - 2x^2(2x)] / (x^2-1)^2 = [4x^3 - 4x - 4x^3] / (x^2-1)^2 = -4x / (x^2-1)^2\n"
            "  Critical point: f'(x) = 0 when -4x = 0, so x = 0.\n"
            "  Sign analysis of f'(x) = -4x / (x^2-1)^2:\n"
            "    (x^2-1)^2 is always positive (where it exists).\n"
            "    So sign of f' = sign of -4x = opposite sign of x.\n"
            "    x < -1: x < 0, so -4x > 0 => f' > 0 (increasing)\n"
            "    -1 < x < 0: x < 0, so f' > 0 (increasing)\n"
            "    0 < x < 1: x > 0, so f' < 0 (decreasing)\n"
            "    x > 1: x > 0, so f' < 0 (decreasing)\n"
            "  At x = 0: f' changes from + to - => LOCAL MAXIMUM at (0, 0).\n"
            "\n"
            "Step 6: Second derivative (we can note from the shape).\n"
            "  Near x = +/-1 (vertical asymptotes), the function approaches +/-inf.\n"
            "  For |x| > 1, f(x) > 2 and approaches 2 from above => concave up.\n"
            "  For |x| < 1, f(x) < 0 (check: f(0.5) = 0.5/(-0.75) = -2/3) => concave down between the asymptotes.\n"
            "\n"
            "Step 7: Sketch.\n"
            "  Key features: origin is both intercept and local max, vertical asymptotes at x=+/-1, "
            "  horizontal asymptote y=2, symmetric about y-axis.\n"
            "  Between x=-1 and x=1: curve rises to (0,0) then falls, staying below x-axis except at origin.\n"
            "  For x>1 and x<-1: curve comes from +inf near asymptotes, decreases toward y=2.\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 3: Worked Example — Polynomial\n"
            "\n"
            "Sketch f(x) = x^3 - 3x^2 + 4.\n"
            "\n"
            "Step 1: Domain = all reals.\n"
            "\n"
            "Step 2: y-intercept: f(0) = 4. x-intercepts: solve x^3 - 3x^2 + 4 = 0. "
            "Try x = -1: (-1) - 3 + 4 = 0. Yes! Factor: (x+1)(x^2 - 4x + 4) = (x+1)(x-2)^2. "
            "x-intercepts: x = -1 and x = 2.\n"
            "\n"
            "Step 3: f(-x) = -x^3 - 3x^2 + 4 != f(x) or -f(x). Neither even nor odd.\n"
            "\n"
            "Step 4: No asymptotes (polynomial).\n"
            "\n"
            "Step 5: f'(x) = 3x^2 - 6x = 3x(x - 2). Critical points: x = 0, x = 2.\n"
            "  Test x = -1: f'(-1) = 3(1)(−3) = 9 > 0 (increasing).\n"
            "  Wait, let me recompute: f'(-1) = 3(-1)(-1-2) = 3(-1)(-3) = 9 > 0.\n"
            "  Test x = 1: f'(1) = 3(1)(1-2) = 3(1)(-1) = -3 < 0 (decreasing).\n"
            "  Test x = 3: f'(3) = 3(3)(3-2) = 9 > 0 (increasing).\n"
            "  x = 0: + to - => local max at (0, 4).\n"
            "  x = 2: - to + => local min at (2, 0). Note: this is also an x-intercept!\n"
            "\n"
            "Step 6: f''(x) = 6x - 6 = 6(x - 1). f'' = 0 at x = 1.\n"
            "  x < 1: f'' < 0, concave down. x > 1: f'' > 0, concave up.\n"
            "  Inflection point at (1, f(1)) = (1, 2).\n"
            "\n"
            "Step 7: Sketch with key points: (−1, 0), (0, 4) local max, (1, 2) inflection, "
            "(2, 0) local min. Curve rises from −inf, peaks at (0,4), decreases through inflection "
            "at (1,2), bottoms at (2,0), then rises to +inf.\n"
        ),
        "key_concepts": [
            "7-step systematic process: domain, intercepts, symmetry, asymptotes, f', f'', sketch",
            "Combine all derivative information into one coherent picture",
            "Identify key points: intercepts, extrema, inflection points, asymptotes",
            "Use symmetry to reduce work when applicable",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Give a function (polynomial or simple rational) and ask for a complete curve "
            "sketch with all 7 steps shown. Students should identify domain, intercepts, "
            "symmetry, asymptotes, extrema, concavity, and inflection points."
        ),
        "practice_problems": [
            {
                "problem": "Perform a complete curve sketch analysis for f(x) = x^3 - 3x.",
                "answer": (
                    "Domain: all reals. y-int: (0,0). x-int: x(x^2-3)=0 => x=0, x=+-sqrt(3). "
                    "Symmetry: f(-x)=-f(x), so odd (symmetric about origin). No asymptotes. "
                    "f'(x)=3x^2-3=3(x-1)(x+1). Crit pts: x=-1,1. "
                    "f' test: inc on (-inf,-1), dec on (-1,1), inc on (1,inf). "
                    "Local max at (-1,2), local min at (1,-2). "
                    "f''(x)=6x. f''=0 at x=0. Concave down on (-inf,0), concave up on (0,inf). "
                    "Inflection point at (0,0)."
                ),
            },
            {
                "problem": "Sketch f(x) = x/(x^2+1). Find extrema, concavity, and asymptotes.",
                "answer": (
                    "Domain: all reals. y-int: (0,0). x-int: x=0. Odd function. "
                    "Horizontal asymptote y=0 (both directions). No vertical asymptotes. "
                    "f'(x)=(x^2+1-x*2x)/(x^2+1)^2 = (1-x^2)/(x^2+1)^2. "
                    "f'=0 when x=+-1. f'(0)=1>0, f'(2)=-3/25<0. "
                    "Local max at (1, 1/2), local min at (-1, -1/2). "
                    "f'' analysis yields inflection points at x=0 and x=+-sqrt(3)."
                ),
            },
        ],
        "common_mistakes": [
            "Skipping steps — always go through all 7 systematically",
            "Forgetting horizontal asymptotes for rational functions",
            "Not plotting enough key points before connecting the curve",
            "Ignoring the behavior near vertical asymptotes",
        ],
        "builds_toward": ["applied-optimization"],
    },

    # =========================================================================
    # CHAPTER 9 — Optimization
    # =========================================================================

    "absolute-extrema": {
        "id": "calc1-9-1",
        "slug": "absolute-extrema",
        "title": "Absolute Extrema",
        "chapter": 9,
        "chapter_title": "Optimization",
        "subject": "calc-1",
        "prerequisites": ["first-derivative-test", "second-derivative-test"],
        "estimated_time": "25 min",
        "difficulty": "medium",
        "teaching_content": (
            "CHUNK 1: Absolute vs Local Extrema\n"
            "\n"
            "Local extremum: f(c) is larger (or smaller) than all NEARBY values.\n"
            "Absolute extremum: f(c) is the largest (or smallest) value on the ENTIRE domain.\n"
            "\n"
            "The absolute maximum is the single highest point of f on its domain.\n"
            "The absolute minimum is the single lowest point of f on its domain.\n"
            "\n"
            "Key facts:\n"
            "  - An absolute extremum is also a local extremum (unless it occurs at an endpoint).\n"
            "  - A function can have many local extrema but at most one absolute max value "
            "and one absolute min value (though the value may be achieved at multiple points).\n"
            "  - A function might not have an absolute max or min at all (e.g., f(x) = x on (-inf, inf)).\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 2: The Extreme Value Theorem\n"
            "\n"
            "Extreme Value Theorem (EVT): If f is CONTINUOUS on a CLOSED interval [a, b], then f "
            "attains both an absolute maximum and an absolute minimum on [a, b].\n"
            "\n"
            "Both conditions are essential:\n"
            "  - Continuous: f(x) = 1/x on [-1, 1] is not continuous (undefined at 0), and has no max or min.\n"
            "  - Closed interval: f(x) = x on (0, 1) (open interval) gets arbitrarily close to 0 and 1 "
            "but never reaches them — no absolute max or min.\n"
            "\n"
            "Where can absolute extrema occur on [a, b]?\n"
            "  1) At critical points inside (a, b)\n"
            "  2) At the endpoints a and b\n"
            "That's it! No other possibilities.\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 3: Open vs Closed Domains\n"
            "\n"
            "On a CLOSED interval [a, b] (continuous f): the EVT guarantees absolute extrema exist. "
            "Use the Closed Interval Method (next lesson) to find them.\n"
            "\n"
            "On an OPEN interval or all of R: absolute extrema are NOT guaranteed.\n"
            "  - If f has only ONE critical point c and it's a local max, it might be an absolute max.\n"
            "  - Check the behavior as x -> endpoints of the domain (or +/-inf).\n"
            "\n"
            "Example: f(x) = -x^2 + 4x on (-inf, inf).\n"
            "  f'(x) = -2x + 4 = 0 => x = 2. f''(2) = -2 < 0, so local max.\n"
            "  f(2) = -4 + 8 = 4.\n"
            "  As x -> +/-inf, f(x) -> -inf.\n"
            "  Since f goes to -inf in both directions and has only one critical point (a local max), "
            "  the local max at (2, 4) is also the ABSOLUTE max. There is no absolute minimum.\n"
            "\n"
            "Example: f(x) = x^3 on [-2, 3].\n"
            "  f'(x) = 3x^2 = 0 at x = 0. f(0) = 0.\n"
            "  Endpoints: f(-2) = -8, f(3) = 27.\n"
            "  Absolute min = -8 at x = -2. Absolute max = 27 at x = 3.\n"
        ),
        "key_concepts": [
            "Absolute extremum: largest/smallest value on the entire domain",
            "Extreme Value Theorem: continuous on [a,b] guarantees absolute extrema",
            "Absolute extrema occur at critical points or endpoints",
            "On open intervals, absolute extrema are not guaranteed",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Test conceptual understanding of EVT. Ask students to identify where absolute "
            "extrema can occur. Include examples on both closed and open intervals."
        ),
        "practice_problems": [
            {
                "problem": "Does f(x) = 1/(x-1) have an absolute maximum on (1, 5]? Explain.",
                "answer": (
                    "No. As x -> 1+, f(x) -> +inf, so f has no absolute maximum. "
                    "The EVT does not apply because the interval is not closed "
                    "(open at x=1) and f is not continuous on a closed interval containing x=1."
                ),
            },
            {
                "problem": "Find the absolute extrema of f(x) = x^2 - 2x + 3 on [0, 4].",
                "answer": (
                    "f'(x) = 2x - 2 = 0 at x = 1. "
                    "Evaluate: f(0) = 3, f(1) = 1 - 2 + 3 = 2, f(4) = 16 - 8 + 3 = 11. "
                    "Absolute min = 2 at x=1. Absolute max = 11 at x=4."
                ),
            },
            {
                "problem": "Find the absolute max of g(x) = -x^4 + 2x^2 on all real numbers, or explain why it doesn't exist.",
                "answer": (
                    "g'(x) = -4x^3 + 4x = -4x(x^2 - 1) = -4x(x-1)(x+1). "
                    "Critical points: x = -1, 0, 1. g(-1) = -1+2 = 1, g(0) = 0, g(1) = 1. "
                    "As x -> +/-inf, g(x) -> -inf. "
                    "Absolute max = 1, achieved at x = -1 and x = 1. No absolute min (goes to -inf)."
                ),
            },
        ],
        "common_mistakes": [
            "Forgetting to check endpoints on a closed interval",
            "Applying EVT when the function is not continuous or the interval is not closed",
            "Confusing local extrema with absolute extrema",
        ],
        "builds_toward": ["closed-interval-method", "applied-optimization"],
    },

    "closed-interval-method": {
        "id": "calc1-9-2",
        "slug": "closed-interval-method",
        "title": "The Closed Interval Method",
        "chapter": 9,
        "chapter_title": "Optimization",
        "subject": "calc-1",
        "prerequisites": ["absolute-extrema"],
        "estimated_time": "20 min",
        "difficulty": "medium",
        "teaching_content": (
            "CHUNK 1: The Method\n"
            "\n"
            "To find the absolute maximum and minimum of a continuous function f on [a, b]:\n"
            "\n"
            "  Step 1: Find all critical points of f in the OPEN interval (a, b).\n"
            "          (Where f'(x) = 0 or f'(x) DNE.)\n"
            "  Step 2: Evaluate f at each critical point AND at both endpoints a and b.\n"
            "  Step 3: The largest value is the absolute maximum. The smallest is the absolute minimum.\n"
            "\n"
            "That's it! No sign charts needed. Just compare numbers.\n"
            "\n"
            "Why this works: By the EVT, the absolute extrema exist. They must occur at critical "
            "points or endpoints. So we just check all candidates and pick the winner.\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 2: Worked Examples\n"
            "\n"
            "Example 1: Find the absolute extrema of f(x) = x^3 - 3x^2 + 1 on [-1, 4].\n"
            "  Step 1: f'(x) = 3x^2 - 6x = 3x(x - 2). f' = 0 at x = 0 and x = 2.\n"
            "    Both are in (-1, 4). ✓\n"
            "  Step 2: Evaluate:\n"
            "    f(-1) = -1 - 3 + 1 = -3\n"
            "    f(0) = 0 - 0 + 1 = 1\n"
            "    f(2) = 8 - 12 + 1 = -3\n"
            "    f(4) = 64 - 48 + 1 = 17\n"
            "  Step 3: Absolute max = 17 at x = 4. Absolute min = -3 at x = -1 and x = 2.\n"
            "\n"
            "Example 2: Find the absolute extrema of g(x) = x^(2/3) on [-8, 27].\n"
            "  Step 1: g'(x) = (2/3)x^(-1/3). g' DNE at x = 0. g' is never 0.\n"
            "    x = 0 is in (-8, 27). ✓\n"
            "  Step 2: Evaluate:\n"
            "    g(-8) = (-8)^(2/3) = (cube root of -8)^2 = (-2)^2 = 4\n"
            "    g(0) = 0\n"
            "    g(27) = 27^(2/3) = (cube root of 27)^2 = 3^2 = 9\n"
            "  Step 3: Absolute max = 9 at x = 27. Absolute min = 0 at x = 0.\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 3: Important Reminders\n"
            "\n"
            "Example 3: f(x) = sin(x) + cos(x) on [0, pi].\n"
            "  f'(x) = cos(x) - sin(x) = 0 => cos(x) = sin(x) => tan(x) = 1 => x = pi/4 in [0, pi].\n"
            "  Evaluate:\n"
            "    f(0) = 0 + 1 = 1\n"
            "    f(pi/4) = sin(pi/4) + cos(pi/4) = sqrt(2)/2 + sqrt(2)/2 = sqrt(2) ≈ 1.414\n"
            "    f(pi) = 0 + (-1) = -1\n"
            "  Absolute max = sqrt(2) at x = pi/4. Absolute min = -1 at x = pi.\n"
            "\n"
            "Common pitfalls to avoid:\n"
            "  - Don't forget to check endpoints. Many students find the critical points and stop.\n"
            "  - Only use critical points INSIDE (a, b). If a critical point equals a or b, "
            "it's already counted as an endpoint.\n"
            "  - Make sure f is actually continuous on [a, b] before using this method.\n"
        ),
        "key_concepts": [
            "Find critical points in (a,b), evaluate f at crits and endpoints, compare",
            "No sign chart needed — just compare function values",
            "Works because EVT guarantees extrema exist on closed intervals",
            "Always check both endpoints",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Give students a function on a closed interval and ask for absolute max and min. "
            "Include one example with a critical point where f' DNE, and one trig function."
        ),
        "practice_problems": [
            {
                "problem": "Find the absolute extrema of f(x) = 2x^3 - 3x^2 - 12x + 5 on [-2, 3].",
                "answer": (
                    "f'(x) = 6x^2 - 6x - 12 = 6(x^2 - x - 2) = 6(x-2)(x+1). "
                    "Critical points: x = -1, x = 2 (both in (-2,3)). "
                    "f(-2) = -16-12+24+5 = 1. f(-1) = -2-3+12+5 = 12. "
                    "f(2) = 16-12-24+5 = -15. f(3) = 54-27-36+5 = -4. "
                    "Absolute max = 12 at x = -1. Absolute min = -15 at x = 2."
                ),
            },
            {
                "problem": "Find the absolute max and min of h(x) = x * sqrt(4 - x^2) on [-2, 2].",
                "answer": (
                    "h(x) = x(4-x^2)^(1/2). Using the product rule: "
                    "h'(x) = (4-x^2)^(1/2) + x * (1/2)(4-x^2)^(-1/2)(-2x) "
                    "= (4-x^2)^(1/2) - x^2/(4-x^2)^(1/2) = (4-x^2-x^2)/(4-x^2)^(1/2) = (4-2x^2)/sqrt(4-x^2). "
                    "h'=0 when 4-2x^2=0 => x=+-sqrt(2). h' DNE at x=+-2 (endpoints). "
                    "h(-2)=0, h(-sqrt(2))=-sqrt(2)*sqrt(2)=-2, h(sqrt(2))=sqrt(2)*sqrt(2)=2, h(2)=0. "
                    "Absolute max = 2 at x=sqrt(2). Absolute min = -2 at x=-sqrt(2)."
                ),
            },
        ],
        "common_mistakes": [
            "Forgetting to evaluate f at the endpoints",
            "Including critical points outside the interval [a, b]",
            "Not checking if f is continuous before applying the method",
        ],
        "builds_toward": ["applied-optimization"],
    },

    "applied-optimization": {
        "id": "calc1-9-3",
        "slug": "applied-optimization",
        "title": "Applied Optimization",
        "chapter": 9,
        "chapter_title": "Optimization",
        "subject": "calc-1",
        "prerequisites": ["closed-interval-method", "second-derivative-test"],
        "estimated_time": "45 min",
        "difficulty": "hard",
        "teaching_content": (
            "CHUNK 1: The 6-Step Method for Applied Optimization\n"
            "\n"
            "Real-world optimization problems ask you to maximize or minimize some quantity. "
            "Follow this systematic approach:\n"
            "\n"
            "  Step 1: DRAW a picture and label variables.\n"
            "  Step 2: Identify the OBJECTIVE function — what you want to maximize or minimize.\n"
            "  Step 3: Identify the CONSTRAINT equation — a relationship between variables.\n"
            "  Step 4: Use the constraint to write the objective as a function of ONE variable.\n"
            "  Step 5: Find the domain of this single-variable function.\n"
            "  Step 6: OPTIMIZE — find critical points, test them, check endpoints if applicable.\n"
            "\n"
            "After solving, always ask: Does my answer make physical sense?\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 2: Worked Example 1 — The Fence Problem\n"
            "\n"
            "Problem: A farmer has 200 meters of fencing and wants to enclose the largest possible "
            "rectangular area against a straight river (no fence needed on the river side). "
            "What dimensions should the farmer use?\n"
            "\n"
            "Step 1: Draw a rectangle with one side along the river. Let x = width (two sides), "
            "y = length (one side, parallel to river).\n"
            "\n"
            "Step 2: Objective: Maximize A = x * y (area).\n"
            "\n"
            "Step 3: Constraint: 2x + y = 200 (total fencing; no fence on river side).\n"
            "\n"
            "Step 4: Solve constraint for y: y = 200 - 2x.\n"
            "  Substitute: A(x) = x(200 - 2x) = 200x - 2x^2.\n"
            "\n"
            "Step 5: Domain: x > 0 and y > 0, so 200 - 2x > 0 => x < 100. Domain: (0, 100).\n"
            "\n"
            "Step 6: A'(x) = 200 - 4x = 0 => x = 50.\n"
            "  A''(x) = -4 < 0, so x = 50 gives a maximum.\n"
            "  y = 200 - 2(50) = 100.\n"
            "  Maximum area = 50 * 100 = 5000 square meters.\n"
            "\n"
            "Check: The total fencing is 2(50) + 100 = 200. ✓ Makes sense.\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 3: Worked Example 2 — Minimum Material Box\n"
            "\n"
            "Problem: An open-top box with a square base must have a volume of 32 cubic inches. "
            "Find the dimensions that minimize the amount of material (surface area).\n"
            "\n"
            "Step 1: Let x = side of the square base, h = height.\n"
            "\n"
            "Step 2: Objective: Minimize S = x^2 + 4xh (base + four sides, no top).\n"
            "\n"
            "Step 3: Constraint: V = x^2 * h = 32.\n"
            "\n"
            "Step 4: Solve for h: h = 32/x^2.\n"
            "  Substitute: S(x) = x^2 + 4x(32/x^2) = x^2 + 128/x.\n"
            "\n"
            "Step 5: Domain: x > 0.\n"
            "\n"
            "Step 6: S'(x) = 2x - 128/x^2 = (2x^3 - 128)/x^2.\n"
            "  Set numerator = 0: 2x^3 = 128 => x^3 = 64 => x = 4.\n"
            "  S''(x) = 2 + 256/x^3. S''(4) = 2 + 256/64 = 2 + 4 = 6 > 0 => local minimum.\n"
            "  Since this is the only critical point and S -> inf as x -> 0+ and x -> inf, "
            "it's the absolute minimum.\n"
            "  h = 32/16 = 2.\n"
            "  Minimum surface area: S = 16 + 128/4 = 16 + 32 = 48 square inches.\n"
            "  Dimensions: 4 x 4 x 2 inches.\n"
            "\n"
            "Check: Volume = 4*4*2 = 32 ✓.\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 4: Tips for Setting Up Problems\n"
            "\n"
            "Setting up the equations is usually the hardest part. Some tips:\n"
            "  - Always draw a diagram first.\n"
            "  - Label every unknown with a variable.\n"
            "  - The objective is what you want to maximize/minimize.\n"
            "  - The constraint is the fixed quantity (budget, perimeter, volume, etc.).\n"
            "  - Common formulas to remember:\n"
            "      Rectangle: A = lw, P = 2l + 2w\n"
            "      Box: V = lwh, SA = 2lw + 2lh + 2wh (or drop a face for open-top)\n"
            "      Circle: A = pi*r^2, C = 2*pi*r\n"
            "      Cylinder: V = pi*r^2*h, SA = 2*pi*r^2 + 2*pi*r*h\n"
            "  - After substituting the constraint, double-check that your function has only ONE variable.\n"
        ),
        "key_concepts": [
            "6-step method: draw, variables, objective, constraint, single-variable, optimize",
            "Use constraint to eliminate a variable from the objective function",
            "Always verify the answer satisfies the original constraint",
            "Check if the domain is open or closed to decide between methods",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Give a word problem requiring setup and solution. Require students to clearly "
            "state the objective function, constraint, substitution, and verification. "
            "Include problems with different geometries."
        ),
        "practice_problems": [
            {
                "problem": (
                    "Find two positive numbers whose sum is 60 and whose product is as large as possible."
                ),
                "answer": (
                    "Let x and y be the numbers. Constraint: x + y = 60. "
                    "Objective: maximize P = xy. Substitute y = 60 - x: P(x) = x(60-x) = 60x - x^2. "
                    "P'(x) = 60 - 2x = 0 => x = 30. P''(x) = -2 < 0 => max. "
                    "y = 30. Maximum product = 900. The numbers are 30 and 30."
                ),
            },
            {
                "problem": (
                    "A piece of wire 40 cm long is bent into a rectangle. "
                    "What dimensions give the maximum area?"
                ),
                "answer": (
                    "Constraint: 2l + 2w = 40, so l + w = 20, l = 20 - w. "
                    "Objective: A = lw = w(20-w) = 20w - w^2. "
                    "A'(w) = 20 - 2w = 0 => w = 10. l = 10. "
                    "Maximum area = 100 cm^2. (A square gives maximum area for fixed perimeter.)"
                ),
            },
            {
                "problem": (
                    "Find the point on the curve y = sqrt(x) closest to the point (3, 0)."
                ),
                "answer": (
                    "Distance^2 = (x-3)^2 + (sqrt(x))^2 = (x-3)^2 + x = x^2 - 6x + 9 + x = x^2 - 5x + 9. "
                    "Minimizing D^2 is equivalent to minimizing D (since sqrt is increasing). "
                    "Let f(x) = x^2 - 5x + 9, x >= 0. "
                    "f'(x) = 2x - 5 = 0 => x = 5/2. "
                    "f''(x) = 2 > 0 => min. y = sqrt(5/2) = sqrt(10)/2. "
                    "Closest point: (5/2, sqrt(10)/2)."
                ),
            },
        ],
        "common_mistakes": [
            "Not drawing a diagram — leads to wrong constraint equations",
            "Forgetting to express the objective in terms of ONE variable",
            "Not checking that the answer satisfies the constraint",
            "Minimizing distance instead of distance-squared (works but is harder)",
        ],
        "builds_toward": ["optimization-strategies"],
    },

    "optimization-strategies": {
        "id": "calc1-9-4",
        "slug": "optimization-strategies",
        "title": "Optimization Strategies and Tips",
        "chapter": 9,
        "chapter_title": "Optimization",
        "subject": "calc-1",
        "prerequisites": ["applied-optimization"],
        "estimated_time": "20 min",
        "difficulty": "medium",
        "teaching_content": (
            "CHUNK 1: Common Optimization Patterns\n"
            "\n"
            "After working many optimization problems, you'll notice recurring patterns:\n"
            "\n"
            "Pattern 1: Maximize area with fixed perimeter.\n"
            "  - Among all rectangles with perimeter P, the square has the largest area.\n"
            "  - Among all shapes with perimeter P, the circle has the largest area.\n"
            "\n"
            "Pattern 2: Minimize perimeter/material with fixed area/volume.\n"
            "  - Among all rectangles with area A, the square has the smallest perimeter.\n"
            "  - Minimum surface area for a given volume often leads to symmetric shapes.\n"
            "\n"
            "Pattern 3: Distance minimization.\n"
            "  - Minimize D^2 instead of D (avoids square roots in the derivative).\n"
            "  - The answer is the same since D and D^2 are minimized at the same point.\n"
            "\n"
            "Pattern 4: Box/can problems.\n"
            "  - Open-top box with square base and fixed volume: optimal h = x/2 (height is half the base).\n"
            "  - Closed cylinder with fixed volume: optimal h = 2r (height equals diameter).\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 2: Verification and Sanity Checks\n"
            "\n"
            "Always verify your answer:\n"
            "\n"
            "1) Does it satisfy the constraint? Plug the values back in.\n"
            "2) Is it a max or min? Use the second derivative test or check endpoint behavior.\n"
            "3) Does it make physical sense? Negative lengths, zero areas, or infinite quantities "
            "mean something went wrong.\n"
            "4) Are the units correct?\n"
            "5) Try extreme cases: What happens if one dimension is very large? Very small? "
            "The optimal answer should be somewhere in between.\n"
            "\n"
            "Example of sanity check: If you are minimizing material for a box and your answer "
            "says make the box infinitely tall and paper-thin, something is wrong.\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 3: Problem-Solving Strategies\n"
            "\n"
            "When you're stuck on setup:\n"
            "  - Re-read the problem and underline what's being maximized/minimized.\n"
            "  - Underline any fixed or given quantities — these form the constraint.\n"
            "  - Name every unknown with a variable and write down what each represents.\n"
            "  - Write every equation you can, then identify which is objective vs constraint.\n"
            "\n"
            "When the algebra is messy:\n"
            "  - Consider substituting BEFORE differentiating.\n"
            "  - Factor common terms before setting the derivative to zero.\n"
            "  - If you have a fraction, just set the numerator = 0 (denominator doesn't = 0 at extrema "
            "in most well-posed problems).\n"
            "\n"
            "Example: Revisiting the open-top box problem.\n"
            "  S(x) = x^2 + 128/x. Rather than using the quotient rule, rewrite as x^2 + 128*x^(-1).\n"
            "  S'(x) = 2x - 128*x^(-2) = 2x - 128/x^2.\n"
            "  Multiply through by x^2: 2x^3 - 128 = 0 => x^3 = 64 => x = 4. Much cleaner.\n"
        ),
        "key_concepts": [
            "Recognize common patterns: max area/fixed perimeter, min material/fixed volume",
            "Minimize D^2 instead of D for distance problems",
            "Always verify: satisfies constraint, correct type (max/min), physically sensible",
            "Simplify algebra by substituting before differentiating",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Present a multi-step optimization word problem and ask students to identify "
            "the objective, constraint, and which known pattern applies. Ask them to verify "
            "their answer makes sense."
        ),
        "practice_problems": [
            {
                "problem": (
                    "A rectangular garden is built against a house wall (no fence needed on that side). "
                    "You have 120 feet of fencing. Without solving, identify the objective function, "
                    "constraint, and what pattern this matches."
                ),
                "answer": (
                    "Objective: maximize area A = xy. "
                    "Constraint: 2x + y = 120 (two widths and one length). "
                    "Pattern: maximize area with fixed perimeter (three-sided rectangle). "
                    "Expected answer: the width should be half the length, x = 30, y = 60, A = 1800 sq ft."
                ),
            },
            {
                "problem": (
                    "You need to design a closed cylindrical can with volume 1000 cm^3. "
                    "What ratio of height to radius minimizes material? "
                    "(Recall: V = pi*r^2*h, SA = 2*pi*r^2 + 2*pi*r*h)"
                ),
                "answer": (
                    "Constraint: pi*r^2*h = 1000, so h = 1000/(pi*r^2). "
                    "SA = 2*pi*r^2 + 2*pi*r*(1000/(pi*r^2)) = 2*pi*r^2 + 2000/r. "
                    "SA'(r) = 4*pi*r - 2000/r^2 = 0 => 4*pi*r^3 = 2000 => r^3 = 500/pi => r = (500/pi)^(1/3). "
                    "h = 1000/(pi*r^2). The ratio h/r = 2, so h = 2r (height equals diameter). "
                    "This matches the known pattern for optimal closed cylinders."
                ),
            },
        ],
        "common_mistakes": [
            "Not recognizing a known pattern and overcomplicating the problem",
            "Forgetting to verify the answer satisfies the original constraint",
            "Getting the right critical point but not confirming it is a max vs min",
        ],
        "builds_toward": [],
    },

    # =========================================================================
    # CHAPTER 10 — Introduction to Integration
    # =========================================================================

    "antiderivatives": {
        "id": "calc1-10-1",
        "slug": "antiderivatives",
        "title": "Antiderivatives",
        "chapter": 10,
        "chapter_title": "Introduction to Integration",
        "subject": "calc-1",
        "prerequisites": ["derivative-rules"],
        "estimated_time": "25 min",
        "difficulty": "medium",
        "teaching_content": (
            "CHUNK 1: What Is an Antiderivative?\n"
            "\n"
            "An antiderivative of f(x) is a function F(x) such that F'(x) = f(x).\n"
            "\n"
            "In other words, differentiation and antidifferentiation are reverse operations.\n"
            "  - Derivative asks: given F, what is F'?\n"
            "  - Antiderivative asks: given f, what F has f as its derivative?\n"
            "\n"
            "Example: An antiderivative of f(x) = 2x is F(x) = x^2, because d/dx(x^2) = 2x.\n"
            "\n"
            "But wait — F(x) = x^2 + 5 also works, since d/dx(x^2 + 5) = 2x.\n"
            "And F(x) = x^2 - 100 works too!\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 2: The + C Constant\n"
            "\n"
            "Key fact: If F(x) is an antiderivative of f(x), then so is F(x) + C for ANY constant C.\n"
            "And these are ALL the antiderivatives — there are no others.\n"
            "\n"
            "Why? If F'(x) = G'(x) = f(x), then (F - G)'(x) = 0 for all x, "
            "which means F(x) - G(x) = C (a constant). So G(x) = F(x) + C.\n"
            "\n"
            "The family of ALL antiderivatives of f is written:\n"
            "  F(x) + C\n"
            "where C is an arbitrary constant (the \"constant of integration\").\n"
            "\n"
            "NEVER forget the + C when finding antiderivatives! It's the most common mistake.\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 3: Indefinite Integral Notation\n"
            "\n"
            "We write the family of all antiderivatives using integral notation:\n"
            "  integral of f(x) dx = F(x) + C\n"
            "\n"
            "The symbol ∫ is the integral sign. The dx indicates the variable of integration. "
            "This is called an INDEFINITE integral (no bounds).\n"
            "\n"
            "Examples:\n"
            "  integral of 2x dx = x^2 + C (because d/dx(x^2) = 2x)\n"
            "  integral of cos(x) dx = sin(x) + C (because d/dx(sin(x)) = cos(x))\n"
            "  integral of 3 dx = 3x + C (because d/dx(3x) = 3)\n"
            "  integral of 0 dx = C (a constant function has derivative 0)\n"
            "\n"
            "To verify an antiderivative, just differentiate your answer. If you get back f(x), "
            "you're correct. This is a great way to check your work!\n"
            "\n"
            "Verification example: Claim: integral of x^3 dx = x^4/4 + C.\n"
            "  Check: d/dx(x^4/4 + C) = 4x^3/4 = x^3. ✓\n"
        ),
        "key_concepts": [
            "Antiderivative F(x) satisfies F'(x) = f(x)",
            "The +C constant: all antiderivatives differ by a constant",
            "Indefinite integral notation: integral of f(x) dx = F(x) + C",
            "Verify by differentiating: d/dx(F(x) + C) should equal f(x)",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Ask students to find antiderivatives and verify them. Include a problem "
            "that tests understanding of why + C is needed. Test the connection between "
            "derivatives and antiderivatives."
        ),
        "practice_problems": [
            {
                "problem": "Find the most general antiderivative of f(x) = 5x^4.",
                "answer": "F(x) = x^5 + C. Check: d/dx(x^5 + C) = 5x^4. ✓",
            },
            {
                "problem": "Find the most general antiderivative of f(x) = 1 (a constant function).",
                "answer": "F(x) = x + C. Check: d/dx(x + C) = 1. ✓",
            },
            {
                "problem": (
                    "True or false: If F(x) and G(x) are both antiderivatives of the same function f(x), "
                    "then F(x) = G(x)."
                ),
                "answer": (
                    "FALSE. They differ by a constant: F(x) = G(x) + C. "
                    "For example, x^2 and x^2 + 7 are both antiderivatives of 2x."
                ),
            },
        ],
        "common_mistakes": [
            "Forgetting the + C constant of integration",
            "Confusing derivative direction with antiderivative direction",
            "Not verifying by differentiating the answer",
        ],
        "builds_toward": ["basic-antidifferentiation", "the-definite-integral"],
    },

    "basic-antidifferentiation": {
        "id": "calc1-10-2",
        "slug": "basic-antidifferentiation",
        "title": "Basic Antidifferentiation Rules",
        "chapter": 10,
        "chapter_title": "Introduction to Integration",
        "subject": "calc-1",
        "prerequisites": ["antiderivatives"],
        "estimated_time": "35 min",
        "difficulty": "medium",
        "teaching_content": (
            "CHUNK 1: The Power Rule for Antiderivatives\n"
            "\n"
            "The most fundamental antidifferentiation rule reverses the power rule for derivatives.\n"
            "\n"
            "Power Rule for Integrals:\n"
            "  integral of x^n dx = x^(n+1) / (n+1) + C,  provided n != -1.\n"
            "\n"
            "Why n != -1? Because if n = -1, the formula gives x^0/0 which is undefined. "
            "The antiderivative of x^(-1) = 1/x is ln|x| + C (covered separately).\n"
            "\n"
            "Examples:\n"
            "  integral of x^3 dx = x^4/4 + C\n"
            "  integral of x^(-2) dx = x^(-1)/(-1) + C = -1/x + C\n"
            "  integral of sqrt(x) dx = integral of x^(1/2) dx = x^(3/2)/(3/2) + C = (2/3)x^(3/2) + C\n"
            "  integral of 1 dx = integral of x^0 dx = x^1/1 + C = x + C\n"
            "\n"
            "Linearity rules (just like derivatives):\n"
            "  integral of [f(x) + g(x)] dx = integral of f(x) dx + integral of g(x) dx\n"
            "  integral of k*f(x) dx = k * integral of f(x) dx  (k is a constant)\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 2: Trig, Exponential, and Logarithmic Antiderivatives\n"
            "\n"
            "Memorize these (they are the reverse of derivative rules):\n"
            "\n"
            "  integral of cos(x) dx = sin(x) + C\n"
            "  integral of sin(x) dx = -cos(x) + C\n"
            "  integral of sec^2(x) dx = tan(x) + C\n"
            "  integral of csc^2(x) dx = -cot(x) + C\n"
            "  integral of sec(x)tan(x) dx = sec(x) + C\n"
            "  integral of csc(x)cot(x) dx = -csc(x) + C\n"
            "\n"
            "  integral of e^x dx = e^x + C\n"
            "  integral of 1/x dx = ln|x| + C   (note the absolute value!)\n"
            "  integral of a^x dx = a^x / ln(a) + C  (for a > 0, a != 1)\n"
            "\n"
            "Worked example: integral of (3cos(x) - 2e^x + 5/x) dx\n"
            "  = 3sin(x) - 2e^x + 5ln|x| + C\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 3: Initial Value Problems\n"
            "\n"
            "An initial value problem (IVP) gives you f'(x) and a specific value f(a) = b. "
            "This lets you determine the exact value of C.\n"
            "\n"
            "Example 1: Find f(x) given f'(x) = 3x^2 - 4x + 1 and f(0) = 5.\n"
            "  Step 1: Antidifferentiate: f(x) = x^3 - 2x^2 + x + C.\n"
            "  Step 2: Use initial condition: f(0) = 0 - 0 + 0 + C = C = 5.\n"
            "  So f(x) = x^3 - 2x^2 + x + 5.\n"
            "\n"
            "Example 2: Find f(x) given f''(x) = 6x, f'(0) = 2, f(0) = 1.\n"
            "  Step 1: Antidifferentiate f'': f'(x) = 3x^2 + C1.\n"
            "  Step 2: Use f'(0) = 2: 0 + C1 = 2, so C1 = 2. Thus f'(x) = 3x^2 + 2.\n"
            "  Step 3: Antidifferentiate f': f(x) = x^3 + 2x + C2.\n"
            "  Step 4: Use f(0) = 1: 0 + 0 + C2 = 1, so C2 = 1.\n"
            "  Answer: f(x) = x^3 + 2x + 1.\n"
            "\n"
            "Example 3 (physics): A ball is thrown upward with initial velocity 20 m/s from height 5 m.\n"
            "  a(t) = -9.8 (gravity). v(t) = integral of -9.8 dt = -9.8t + C.\n"
            "  v(0) = 20, so C = 20. v(t) = -9.8t + 20.\n"
            "  s(t) = integral of (-9.8t + 20) dt = -4.9t^2 + 20t + C.\n"
            "  s(0) = 5, so C = 5. s(t) = -4.9t^2 + 20t + 5.\n"
        ),
        "key_concepts": [
            "Power rule: integral of x^n dx = x^(n+1)/(n+1) + C (n != -1)",
            "Trig antiderivatives: sin -> -cos, cos -> sin, sec^2 -> tan",
            "integral of e^x dx = e^x + C, integral of 1/x dx = ln|x| + C",
            "Initial value problems: use a given point to solve for C",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Include a mix of power rule, trig, and exponential integrals. "
            "Include at least one initial value problem. Test that students remember + C."
        ),
        "practice_problems": [
            {
                "problem": "Find: integral of (4x^3 - 2x + 7) dx.",
                "answer": "x^4 - x^2 + 7x + C.",
            },
            {
                "problem": "Find: integral of (sec^2(x) + 3e^x) dx.",
                "answer": "tan(x) + 3e^x + C.",
            },
            {
                "problem": "Find f(x) given f'(x) = 2x - 3 and f(1) = 4.",
                "answer": (
                    "f(x) = x^2 - 3x + C. f(1) = 1 - 3 + C = -2 + C = 4, so C = 6. "
                    "f(x) = x^2 - 3x + 6."
                ),
            },
        ],
        "common_mistakes": [
            "Forgetting +C on indefinite integrals",
            "Using the power rule with n = -1 (gives division by zero; use ln|x| instead)",
            "Getting the sign wrong on trig antiderivatives (especially integral of sin = -cos)",
            "Forgetting absolute value: integral of 1/x = ln|x|, not ln(x)",
        ],
        "builds_toward": ["sigma-notation", "the-definite-integral"],
    },

    "sigma-notation": {
        "id": "calc1-10-3",
        "slug": "sigma-notation",
        "title": "Sigma Notation and Summation",
        "chapter": 10,
        "chapter_title": "Introduction to Integration",
        "subject": "calc-1",
        "prerequisites": [],
        "estimated_time": "25 min",
        "difficulty": "medium",
        "teaching_content": (
            "CHUNK 1: Sigma Notation Basics\n"
            "\n"
            "Sigma notation is a compact way to write sums. The Greek letter Sigma (a big E-like symbol) "
            "means 'add up.'\n"
            "\n"
            "  Sum from i=1 to n of a_i = a_1 + a_2 + a_3 + ... + a_n\n"
            "\n"
            "  - i is the INDEX variable (also called dummy variable).\n"
            "  - The number below Sigma (here 1) is the STARTING value.\n"
            "  - The number above Sigma (here n) is the ENDING value.\n"
            "  - a_i is the GENERAL TERM.\n"
            "\n"
            "Examples:\n"
            "  Sum from i=1 to 4 of i^2 = 1^2 + 2^2 + 3^2 + 4^2 = 1 + 4 + 9 + 16 = 30\n"
            "  Sum from i=1 to 3 of (2i + 1) = 3 + 5 + 7 = 15\n"
            "  Sum from i=0 to 3 of 2^i = 1 + 2 + 4 + 8 = 15\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 2: Properties of Sums\n"
            "\n"
            "These properties make it easier to work with sigma notation:\n"
            "\n"
            "  1) Sum of (a_i + b_i) = Sum of a_i + Sum of b_i  (split sums)\n"
            "  2) Sum of c * a_i = c * Sum of a_i  (pull out constants)\n"
            "  3) Sum from i=1 to n of c = c * n  (sum of a constant)\n"
            "\n"
            "Example: Sum from i=1 to 5 of (3i^2 + 2)\n"
            "  = 3 * Sum(i^2, i=1 to 5) + Sum(2, i=1 to 5)\n"
            "  = 3 * (1 + 4 + 9 + 16 + 25) + 2*5\n"
            "  = 3 * 55 + 10 = 165 + 10 = 175\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 3: Useful Summation Formulas\n"
            "\n"
            "These closed-form formulas are essential for Riemann sums:\n"
            "\n"
            "  Sum from i=1 to n of 1 = n\n"
            "\n"
            "  Sum from i=1 to n of i = n(n+1)/2\n"
            "\n"
            "  Sum from i=1 to n of i^2 = n(n+1)(2n+1)/6\n"
            "\n"
            "  Sum from i=1 to n of i^3 = [n(n+1)/2]^2\n"
            "\n"
            "Worked example: Compute Sum from i=1 to 100 of i.\n"
            "  Using the formula: 100(101)/2 = 5050.\n"
            "\n"
            "Worked example: Compute Sum from i=1 to n of (2i - 1).\n"
            "  = 2 * Sum(i) - Sum(1)\n"
            "  = 2 * n(n+1)/2 - n\n"
            "  = n(n+1) - n\n"
            "  = n^2 + n - n\n"
            "  = n^2.\n"
            "  (This is the well-known result that the sum of the first n odd numbers is n^2.)\n"
            "\n"
            "Worked example: Simplify Sum from i=1 to n of (3i^2 + 2i) / n^3.\n"
            "  = (1/n^3) * [3 * Sum(i^2) + 2 * Sum(i)]\n"
            "  = (1/n^3) * [3 * n(n+1)(2n+1)/6 + 2 * n(n+1)/2]\n"
            "  = (1/n^3) * [n(n+1)(2n+1)/2 + n(n+1)]\n"
            "  = (1/n^3) * n(n+1) * [(2n+1)/2 + 1]\n"
            "  = (1/n^3) * n(n+1) * (2n+3)/2\n"
            "  = (n+1)(2n+3) / (2n^2)\n"
        ),
        "key_concepts": [
            "Sigma notation: compact notation for sums with index, start, end, general term",
            "Properties: split sums, factor out constants, sum of a constant = c*n",
            "Key formula: sum of i from 1 to n = n(n+1)/2",
            "Key formula: sum of i^2 from 1 to n = n(n+1)(2n+1)/6",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Ask students to expand sigma notation into explicit sums, evaluate finite sums, "
            "and use closed-form formulas. Include one problem that requires simplifying "
            "an expression involving n."
        ),
        "practice_problems": [
            {
                "problem": "Evaluate: Sum from i=1 to 50 of i.",
                "answer": "Using n(n+1)/2: 50(51)/2 = 1275.",
            },
            {
                "problem": "Evaluate: Sum from i=1 to 4 of (i^2 + 3i).",
                "answer": (
                    "Expand: (1+3) + (4+6) + (9+9) + (16+12) = 4 + 10 + 18 + 28 = 60. "
                    "Or: Sum(i^2) + 3*Sum(i) = 4(5)(9)/6 + 3*4(5)/2 = 30 + 30 = 60."
                ),
            },
            {
                "problem": "Simplify Sum from i=1 to n of (4i/n^2) and find its limit as n -> infinity.",
                "answer": (
                    "(4/n^2) * Sum(i) = (4/n^2) * n(n+1)/2 = 4(n+1)/(2n) = 2(n+1)/n = 2 + 2/n. "
                    "As n -> inf, this approaches 2."
                ),
            },
        ],
        "common_mistakes": [
            "Confusing the index starting value (i=0 vs i=1 changes the result!)",
            "Misremembering the sum formulas — write them down on your formula sheet",
            "Not factoring out constants before applying summation formulas",
        ],
        "builds_toward": ["riemann-sums", "the-definite-integral"],
    },

    "riemann-sums": {
        "id": "calc1-10-4",
        "slug": "riemann-sums",
        "title": "Riemann Sums",
        "chapter": 10,
        "chapter_title": "Introduction to Integration",
        "subject": "calc-1",
        "prerequisites": ["sigma-notation"],
        "estimated_time": "35 min",
        "difficulty": "hard",
        "teaching_content": (
            "CHUNK 1: Approximating Area Under a Curve\n"
            "\n"
            "How do we find the area under y = f(x) from x = a to x = b? "
            "The key idea: approximate using rectangles, then take the limit.\n"
            "\n"
            "Setup for n rectangles:\n"
            "  - Divide [a, b] into n equal subintervals.\n"
            "  - Width of each rectangle: Delta_x = (b - a) / n.\n"
            "  - The i-th subinterval is [x_(i-1), x_i] where x_i = a + i * Delta_x.\n"
            "\n"
            "Three common choices for rectangle heights:\n"
            "  LEFT Riemann sum: use the left endpoint of each subinterval.\n"
            "    L_n = Sum from i=0 to n-1 of f(x_i) * Delta_x\n"
            "         = Sum from i=0 to n-1 of f(a + i*Delta_x) * Delta_x\n"
            "\n"
            "  RIGHT Riemann sum: use the right endpoint.\n"
            "    R_n = Sum from i=1 to n of f(x_i) * Delta_x\n"
            "         = Sum from i=1 to n of f(a + i*Delta_x) * Delta_x\n"
            "\n"
            "  MIDPOINT Riemann sum: use the midpoint of each subinterval.\n"
            "    M_n = Sum from i=1 to n of f((x_(i-1) + x_i)/2) * Delta_x\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 2: Worked Example\n"
            "\n"
            "Approximate the area under f(x) = x^2 from x = 0 to x = 2 using n = 4 rectangles.\n"
            "\n"
            "  Delta_x = (2 - 0)/4 = 0.5\n"
            "  Subintervals: [0, 0.5], [0.5, 1], [1, 1.5], [1.5, 2]\n"
            "\n"
            "LEFT sum (L_4):\n"
            "  Heights: f(0)=0, f(0.5)=0.25, f(1)=1, f(1.5)=2.25\n"
            "  L_4 = (0 + 0.25 + 1 + 2.25) * 0.5 = 3.5 * 0.5 = 1.75\n"
            "\n"
            "RIGHT sum (R_4):\n"
            "  Heights: f(0.5)=0.25, f(1)=1, f(1.5)=2.25, f(2)=4\n"
            "  R_4 = (0.25 + 1 + 2.25 + 4) * 0.5 = 7.5 * 0.5 = 3.75\n"
            "\n"
            "MIDPOINT sum (M_4):\n"
            "  Midpoints: 0.25, 0.75, 1.25, 1.75\n"
            "  Heights: f(0.25)=0.0625, f(0.75)=0.5625, f(1.25)=1.5625, f(1.75)=3.0625\n"
            "  M_4 = (0.0625 + 0.5625 + 1.5625 + 3.0625) * 0.5 = 5.25 * 0.5 = 2.625\n"
            "\n"
            "The exact area (found by integration) is 8/3 ≈ 2.667. The midpoint sum is closest!\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 3: Over- and Underestimates\n"
            "\n"
            "For a function that is INCREASING on [a, b]:\n"
            "  - Left sum is an UNDERESTIMATE (rectangles miss area above them).\n"
            "  - Right sum is an OVERESTIMATE (rectangles extend beyond the curve).\n"
            "\n"
            "For a function that is DECREASING on [a, b]:\n"
            "  - Left sum is an OVERESTIMATE.\n"
            "  - Right sum is an UNDERESTIMATE.\n"
            "\n"
            "For CONCAVE UP functions: midpoint is an underestimate.\n"
            "For CONCAVE DOWN functions: midpoint is an overestimate.\n"
            "\n"
            "As n increases (more rectangles), ALL Riemann sums get closer to the true area. "
            "In the limit as n -> infinity, they all converge to the same value.\n"
            "\n"
            "Example: For f(x) = x^2 on [0, 2] (increasing and concave up):\n"
            "  L_4 = 1.75 (underestimate ✓)\n"
            "  R_4 = 3.75 (overestimate ✓)\n"
            "  M_4 = 2.625 (underestimate for concave up ✓, since exact = 2.667)\n"
        ),
        "key_concepts": [
            "Delta_x = (b-a)/n for n equal subintervals",
            "Left sum uses left endpoints, right sum uses right endpoints, midpoint uses midpoints",
            "Increasing function: left = under, right = over",
            "As n -> infinity, all Riemann sums converge to the exact area",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Ask students to compute a left or right Riemann sum with a specific n. "
            "Ask them to determine whether a sum is an overestimate or underestimate. "
            "Include one problem that sets up the sum in sigma notation."
        ),
        "practice_problems": [
            {
                "problem": "Compute the right Riemann sum for f(x) = 3x on [1, 5] with n = 4.",
                "answer": (
                    "Delta_x = (5-1)/4 = 1. Right endpoints: 2, 3, 4, 5. "
                    "R_4 = [f(2) + f(3) + f(4) + f(5)] * 1 = [6 + 9 + 12 + 15] = 42. "
                    "(Exact area = integral of 3x from 1 to 5 = 3x^2/2 from 1 to 5 = 75/2 - 3/2 = 36. "
                    "R_4 = 42 is an overestimate since f is increasing.)"
                ),
            },
            {
                "problem": "Is a left Riemann sum for f(x) = 1/x on [1, 4] an overestimate or underestimate?",
                "answer": (
                    "f(x) = 1/x is DECREASING on [1, 4]. "
                    "For a decreasing function, the left endpoint is the highest point on each subinterval, "
                    "so the left sum is an OVERESTIMATE."
                ),
            },
            {
                "problem": (
                    "Write the right Riemann sum for f(x) = x^2 on [0, 3] with n subintervals in sigma notation."
                ),
                "answer": (
                    "Delta_x = 3/n. x_i = 0 + i*(3/n) = 3i/n. "
                    "R_n = Sum from i=1 to n of f(3i/n) * (3/n) "
                    "= Sum from i=1 to n of (3i/n)^2 * (3/n) "
                    "= Sum from i=1 to n of (9i^2/n^2) * (3/n) "
                    "= Sum from i=1 to n of 27i^2/n^3 "
                    "= (27/n^3) * n(n+1)(2n+1)/6 "
                    "= 27(n+1)(2n+1)/(6n^2) "
                    "= 9(n+1)(2n+1)/(2n^2)."
                ),
            },
        ],
        "common_mistakes": [
            "Using the wrong index range (left starts at i=0, right starts at i=1)",
            "Forgetting to multiply by Delta_x — each term is f(x_i) * Delta_x, not just f(x_i)",
            "Mixing up overestimate/underestimate for increasing vs decreasing functions",
        ],
        "builds_toward": ["the-definite-integral"],
    },

    "the-definite-integral": {
        "id": "calc1-10-5",
        "slug": "the-definite-integral",
        "title": "The Definite Integral",
        "chapter": 10,
        "chapter_title": "Introduction to Integration",
        "subject": "calc-1",
        "prerequisites": ["riemann-sums", "antiderivatives"],
        "estimated_time": "35 min",
        "difficulty": "hard",
        "teaching_content": (
            "CHUNK 1: From Riemann Sums to the Definite Integral\n"
            "\n"
            "The definite integral is the LIMIT of Riemann sums as the number of rectangles "
            "approaches infinity:\n"
            "\n"
            "  integral from a to b of f(x) dx = lim as n->inf of Sum from i=1 to n of f(x_i*) * Delta_x\n"
            "\n"
            "where Delta_x = (b-a)/n and x_i* is any sample point in the i-th subinterval.\n"
            "\n"
            "If this limit exists (regardless of how we choose the sample points), we say f is "
            "INTEGRABLE on [a, b].\n"
            "\n"
            "Key fact: Every continuous function on [a, b] is integrable.\n"
            "\n"
            "Notation: integral from a to b of f(x) dx\n"
            "  - a is the LOWER limit of integration.\n"
            "  - b is the UPPER limit of integration.\n"
            "  - f(x) is the INTEGRAND.\n"
            "  - dx indicates the variable of integration.\n"
            "\n"
            "Unlike the indefinite integral, the definite integral produces a NUMBER, not a function. "
            "There is no + C.\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 2: Signed Area Interpretation\n"
            "\n"
            "The definite integral represents SIGNED area:\n"
            "  - Area above the x-axis counts as POSITIVE.\n"
            "  - Area below the x-axis counts as NEGATIVE.\n"
            "\n"
            "So integral from a to b of f(x) dx = (area above x-axis) - (area below x-axis).\n"
            "\n"
            "Example: integral from 0 to 2*pi of sin(x) dx = 0.\n"
            "  From 0 to pi, sin(x) >= 0 (area = 2 above x-axis).\n"
            "  From pi to 2*pi, sin(x) <= 0 (area = 2 below x-axis).\n"
            "  Net signed area = 2 - 2 = 0.\n"
            "\n"
            "If you want TOTAL area (ignoring sign), integrate |f(x)| instead, or split into "
            "separate integrals where f is positive and negative.\n"
            "\n"
            "Example: Total area between sin(x) and x-axis from 0 to 2*pi:\n"
            "  = integral from 0 to pi of sin(x) dx + integral from pi to 2*pi of |sin(x)| dx\n"
            "  = integral from 0 to pi of sin(x) dx - integral from pi to 2*pi of sin(x) dx\n"
            "  = 2 + 2 = 4.\n"
            "\n"
            "---\n"
            "\n"
            "CHUNK 3: Properties of Definite Integrals\n"
            "\n"
            "These properties are extremely useful:\n"
            "\n"
            "  1) integral from a to a of f(x) dx = 0  (zero-width interval)\n"
            "\n"
            "  2) integral from b to a of f(x) dx = - integral from a to b of f(x) dx  (swap limits = negate)\n"
            "\n"
            "  3) integral from a to b of [f(x) + g(x)] dx = integral from a to b of f(x) dx + integral from a to b of g(x) dx\n"
            "\n"
            "  4) integral from a to b of c*f(x) dx = c * integral from a to b of f(x) dx\n"
            "\n"
            "  5) integral from a to b of f(x) dx + integral from b to c of f(x) dx = integral from a to c of f(x) dx\n"
            "     (you can split or combine intervals)\n"
            "\n"
            "  6) If f(x) >= 0 on [a, b], then integral from a to b of f(x) dx >= 0.\n"
            "\n"
            "  7) If f(x) >= g(x) on [a, b], then integral from a to b of f(x) dx >= integral from a to b of g(x) dx.\n"
            "\n"
            "Worked example using the limit definition:\n"
            "Compute integral from 0 to 3 of x^2 dx using the limit of right Riemann sums.\n"
            "  R_n = Sum from i=1 to n of (3i/n)^2 * (3/n) = (27/n^3) * Sum(i^2)\n"
            "  = (27/n^3) * n(n+1)(2n+1)/6 = 27(n+1)(2n+1)/(6n^2)\n"
            "  = (27/6) * (n+1)(2n+1)/n^2 = (9/2) * (2n^2 + 3n + 1)/n^2\n"
            "  = (9/2) * (2 + 3/n + 1/n^2)\n"
            "  As n -> inf: limit = (9/2)(2) = 9.\n"
            "  So integral from 0 to 3 of x^2 dx = 9.\n"
            "\n"
            "  (Check: antiderivative of x^2 is x^3/3. Evaluating: 27/3 - 0 = 9. ✓)\n"
        ),
        "key_concepts": [
            "Definite integral = limit of Riemann sums as n -> infinity",
            "Definite integral gives a NUMBER (not a function, no + C)",
            "Signed area: above x-axis is positive, below is negative",
            "Properties: swap limits negates, split intervals, linearity",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Test understanding of signed area vs total area. Ask students to use properties "
            "to evaluate integrals given partial information. Include one limit-of-Riemann-sums "
            "computation and one conceptual question about signed area."
        ),
        "practice_problems": [
            {
                "problem": (
                    "If integral from 0 to 5 of f(x) dx = 7 and integral from 0 to 3 of f(x) dx = 4, "
                    "find integral from 3 to 5 of f(x) dx."
                ),
                "answer": (
                    "By the interval splitting property: "
                    "integral from 0 to 3 + integral from 3 to 5 = integral from 0 to 5. "
                    "So 4 + integral from 3 to 5 = 7. "
                    "integral from 3 to 5 of f(x) dx = 3."
                ),
            },
            {
                "problem": "Compute integral from 0 to 2 of x^3 dx using the limit of right Riemann sums.",
                "answer": (
                    "Delta_x = 2/n, x_i = 2i/n. "
                    "R_n = Sum from i=1 to n of (2i/n)^3 * (2/n) = (16/n^4) * Sum(i^3) "
                    "= (16/n^4) * [n(n+1)/2]^2 = (16/n^4) * n^2(n+1)^2/4 = 4(n+1)^2/n^2. "
                    "As n -> inf: limit = 4(1)^2 = 4. (Or: 4*(n^2+2n+1)/n^2 -> 4.) "
                    "integral from 0 to 2 of x^3 dx = 4."
                ),
            },
            {
                "problem": (
                    "The graph of f(x) on [0, 6] forms a triangle above the x-axis from x=0 to x=4 "
                    "with height 3, and a triangle below the x-axis from x=4 to x=6 with depth 2. "
                    "Find integral from 0 to 6 of f(x) dx."
                ),
                "answer": (
                    "Area above = (1/2)(4)(3) = 6 (positive). "
                    "Area below = (1/2)(2)(2) = 2 (negative). "
                    "Signed area = 6 - 2 = 4."
                ),
            },
        ],
        "common_mistakes": [
            "Confusing signed area with total area — the integral can be zero or negative",
            "Adding + C to a definite integral (definite integrals produce numbers, not functions)",
            "Forgetting to take the limit as n -> infinity (the Riemann sum alone is an approximation)",
            "Swapping integration limits without negating the result",
        ],
        "builds_toward": [],
    },
}
