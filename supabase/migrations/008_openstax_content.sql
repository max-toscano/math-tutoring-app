-- ============================================================================
-- Migration 008: OpenStax Content (Structured RAG)
--
-- Stores OpenStax textbook content organized by topic for instant retrieval.
-- The AI looks up content by topic_slug instead of searching vectors.
-- Falls back to web search if a topic isn't in this table.
--
-- One row = one section of one chapter of one textbook.
-- ~150 rows covers Algebra/Trig + Calculus 1 completely.
-- ~10MB covers ALL OpenStax math textbooks.
-- ============================================================================

CREATE TABLE openstax_content (

    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- ── Which textbook and where ─────────────────────────────────────────
    textbook        TEXT NOT NULL,           -- "algebra_trig", "calculus_vol1"
    edition         TEXT NOT NULL DEFAULT '2e',
    chapter_number  INT NOT NULL,
    chapter_title   TEXT NOT NULL,
    section_number  TEXT NOT NULL,           -- "3.6", "7.3"
    section_title   TEXT NOT NULL,           -- "The Chain Rule"

    -- ── Topic mapping ────────────────────────────────────────────────────
    topic_slug      TEXT NOT NULL,           -- "chain_rule" — matches curriculum
    subject         TEXT NOT NULL,           -- "trigonometry", "calculus", "algebra"

    -- ── Content ──────────────────────────────────────────────────────────
    content         TEXT NOT NULL,           -- Full section text (~2000 words)
    summary         TEXT,                    -- 2-3 sentence summary for quick context

    -- ── Structured data ──────────────────────────────────────────────────
    key_formulas    TEXT[] NOT NULL DEFAULT '{}',
    prerequisites   TEXT[] NOT NULL DEFAULT '{}',   -- topic_slugs student should know
    learning_objectives TEXT[] NOT NULL DEFAULT '{}',
    examples        JSONB NOT NULL DEFAULT '[]',    -- [{problem, solution}]
    common_mistakes TEXT[] NOT NULL DEFAULT '{}',

    -- ── Metadata ─────────────────────────────────────────────────────────
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ─── Indexes ──────────────────────────────────────────────────────────────

-- Primary lookup: the retriever queries by topic_slug
CREATE INDEX idx_openstax_topic ON openstax_content (topic_slug);

-- Lookup by subject (get all trig content, all calculus content)
CREATE INDEX idx_openstax_subject ON openstax_content (subject);

-- Lookup by textbook + chapter (browse a textbook)
CREATE INDEX idx_openstax_textbook_chapter ON openstax_content (textbook, chapter_number);

-- ─── RLS ──────────────────────────────────────────────────────────────────

ALTER TABLE openstax_content ENABLE ROW LEVEL SECURITY;

-- Everyone can read textbook content (it's open source)
CREATE POLICY "Anyone can read openstax content"
    ON openstax_content FOR SELECT
    USING (true);

-- Only service role can insert/update (admin/loader scripts)
CREATE POLICY "Service role can manage openstax content"
    ON openstax_content FOR ALL
    USING (auth.role() = 'service_role');


-- ─── Seed Data (key math topics) ─────────────────────────────────────────

INSERT INTO openstax_content (textbook, chapter_number, chapter_title, section_number, section_title, topic_slug, subject, content, summary, key_formulas, prerequisites, learning_objectives, examples, common_mistakes) VALUES

-- ═══ TRIGONOMETRY ═══════════════════════════════════════════════════════

('algebra_trig', 7, 'Trigonometric Identities', '7.1', 'Pythagorean Identity', 'pythagorean_identity', 'trigonometry',
'The fundamental Pythagorean identity states that for any angle θ, sin²θ + cos²θ = 1. This identity comes directly from the unit circle: if a point on the unit circle has coordinates (cos θ, sin θ), then by the Pythagorean theorem, cos²θ + sin²θ = 1.

From this fundamental identity, two additional forms can be derived:
- Dividing both sides by cos²θ gives: tan²θ + 1 = sec²θ
- Dividing both sides by sin²θ gives: 1 + cot²θ = csc²θ

These three identities are used extensively in simplifying trigonometric expressions, proving other identities, and solving trigonometric equations. When simplifying, look for sin²θ or cos²θ terms that can be replaced using these identities.

To prove an identity, work with one side (usually the more complex side) and transform it into the other side using algebraic manipulation and known identities. Never work with both sides simultaneously as if the identity were an equation.',
'The Pythagorean identity sin²θ + cos²θ = 1 and its two derived forms are fundamental tools for simplifying trig expressions and proving identities.',
ARRAY['sin²θ + cos²θ = 1', 'tan²θ + 1 = sec²θ', '1 + cot²θ = csc²θ'],
ARRAY['unit_circle', 'six_trig_ratios'],
ARRAY['State and apply the three Pythagorean identities', 'Derive the alternate forms from sin²θ + cos²θ = 1', 'Use Pythagorean identities to simplify expressions'],
'[{"problem": "Simplify sin²θ + sin²θ·tan²θ", "solution": "Factor: sin²θ(1 + tan²θ) = sin²θ · sec²θ = sin²θ/cos²θ = tan²θ"}, {"problem": "Verify: sec²θ - 1 = sin²θ · sec²θ", "solution": "LHS: sec²θ - 1 = tan²θ = sin²θ/cos²θ = sin²θ · sec²θ = RHS"}]'::jsonb,
ARRAY['Forgetting to factor before applying the identity', 'Using the wrong form of the identity for the situation', 'Working with both sides of an identity simultaneously']),

('algebra_trig', 7, 'Trigonometric Identities', '7.3', 'Double-Angle Formulas', 'double_angle', 'trigonometry',
'The double-angle formulas express trigonometric functions of 2θ in terms of functions of θ.

The sine double-angle formula: sin(2θ) = 2sin(θ)cos(θ). This comes from the sum formula sin(A+B) = sinAcosB + cosAsinB with A = B = θ.

The cosine double-angle formula has three equivalent forms:
- cos(2θ) = cos²(θ) − sin²(θ)
- cos(2θ) = 2cos²(θ) − 1 (substituting sin²θ = 1 − cos²θ)
- cos(2θ) = 1 − 2sin²(θ) (substituting cos²θ = 1 − sin²θ)

The tangent double-angle formula: tan(2θ) = 2tan(θ)/(1 − tan²(θ))

These formulas are essential for simplifying expressions, solving equations, and evaluating trig functions. The cosine forms are particularly useful because you can choose whichever form eliminates one of sin or cos.',
'Double-angle formulas rewrite sin(2θ), cos(2θ), and tan(2θ) in terms of single-angle functions. Derived from the sum formulas with A = B.',
ARRAY['sin(2θ) = 2sin(θ)cos(θ)', 'cos(2θ) = cos²(θ) − sin²(θ)', 'cos(2θ) = 2cos²(θ) − 1', 'cos(2θ) = 1 − 2sin²(θ)', 'tan(2θ) = 2tan(θ)/(1 − tan²(θ))'],
ARRAY['pythagorean_identity', 'sum_difference_identities'],
ARRAY['Apply the double-angle formulas for sin, cos, and tan', 'Choose the appropriate cosine double-angle form', 'Use double-angle formulas to simplify and solve'],
'[{"problem": "Find sin(2θ) if sinθ = 3/5 and θ is in Q1", "solution": "cosθ = 4/5 (Pythagorean), sin(2θ) = 2(3/5)(4/5) = 24/25"}, {"problem": "Simplify 2cos²(x) - 1", "solution": "This matches cos(2θ) = 2cos²(θ) - 1, so the answer is cos(2x)"}]'::jsonb,
ARRAY['Forgetting the factor of 2 in sin(2θ)', 'Using the wrong cosine form and making the problem harder', 'Confusing sin(2θ) with 2sin(θ)']),

('algebra_trig', 7, 'Trigonometric Identities', '7.4', 'Sum-to-Product Formulas', 'sum_to_product', 'trigonometry',
'The sum-to-product formulas convert sums or differences of sine and cosine into products:

sin A + sin B = 2 sin((A+B)/2) cos((A−B)/2)
sin A − sin B = 2 cos((A+B)/2) sin((A−B)/2)
cos A + cos B = 2 cos((A+B)/2) cos((A−B)/2)
cos A − cos B = −2 sin((A+B)/2) sin((A−B)/2)

These are derived by adding or subtracting the sum and difference identities for sine and cosine. They are useful when you need to factor trigonometric expressions or solve certain types of equations.

The product-to-sum formulas go in the reverse direction, converting products into sums:
sinA·cosB = (1/2)[sin(A+B) + sin(A−B)]
cosA·cosB = (1/2)[cos(A−B) + cos(A+B)]
sinA·sinB = (1/2)[cos(A−B) − cos(A+B)]',
'Sum-to-product formulas convert sin A ± sin B and cos A ± cos B into products. Useful for factoring trig expressions.',
ARRAY['sin A + sin B = 2sin((A+B)/2)cos((A−B)/2)', 'sin A − sin B = 2cos((A+B)/2)sin((A−B)/2)', 'cos A + cos B = 2cos((A+B)/2)cos((A−B)/2)', 'cos A − cos B = −2sin((A+B)/2)sin((A−B)/2)'],
ARRAY['double_angle', 'sum_difference_identities'],
ARRAY['Convert sums and differences of trig functions to products', 'Apply product-to-sum formulas', 'Use these formulas to solve trig equations'],
'[{"problem": "Express sin(3x) + sin(x) as a product", "solution": "2sin((3x+x)/2)cos((3x-x)/2) = 2sin(2x)cos(x)"}]'::jsonb,
ARRAY['Getting the (A+B)/2 and (A-B)/2 mixed up', 'Forgetting the negative sign in the cos A - cos B formula']),

('algebra_trig', 5, 'Trigonometric Functions', '5.3', 'Unit Circle', 'unit_circle', 'trigonometry',
'The unit circle is a circle of radius 1 centered at the origin. For any angle θ measured from the positive x-axis, the point on the unit circle is (cos θ, sin θ).

Key angles and their coordinates:
- 0° (0): (1, 0)
- 30° (π/6): (√3/2, 1/2)
- 45° (π/4): (√2/2, √2/2)
- 60° (π/3): (1/2, √3/2)
- 90° (π/2): (0, 1)

The signs of sine and cosine depend on the quadrant:
- Q1: both positive
- Q2: sin positive, cos negative
- Q3: both negative
- Q4: sin negative, cos positive

Remember: All Students Take Calculus (ASTC) — tells which functions are positive in each quadrant.

Reference angles allow you to evaluate trig functions for any angle by relating them to acute angles in Q1.',
'The unit circle defines sin and cos as coordinates of a point. Key angles, quadrant signs, and reference angles are essential tools.',
ARRAY['(cos θ, sin θ) = coordinates on unit circle', 'sin²θ + cos²θ = 1', 'tan θ = sin θ / cos θ'],
ARRAY['degree_radian_conversion', 'right_triangle_trig'],
ARRAY['Define trig functions using the unit circle', 'Evaluate trig functions at key angles', 'Determine signs by quadrant', 'Use reference angles'],
'[{"problem": "Find sin(5π/6)", "solution": "Reference angle = π/6, Q2 (sin positive), sin(5π/6) = sin(π/6) = 1/2"}, {"problem": "Find cos(225°)", "solution": "Reference angle = 45°, Q3 (cos negative), cos(225°) = -cos(45°) = -√2/2"}]'::jsonb,
ARRAY['Mixing up which coordinate is sin vs cos', 'Getting the sign wrong for the quadrant', 'Confusing reference angle with the angle itself']),

-- ═══ CALCULUS 1 ════════════════════════════════════════════════════════

('calculus_vol1', 2, 'Limits', '2.2', 'The Limit of a Function', 'limits_intro', 'calculus',
'The limit of a function f(x) as x approaches a, written lim(x→a) f(x) = L, means that f(x) gets arbitrarily close to L as x gets close to a (but not equal to a).

Key concepts:
- The limit may exist even if f(a) is undefined
- Left-hand limit: lim(x→a⁻) f(x) — approaching from the left
- Right-hand limit: lim(x→a⁺) f(x) — approaching from the right
- The two-sided limit exists only if both one-sided limits exist and are equal

Techniques for evaluating limits:
1. Direct substitution — try plugging in the value first
2. Factoring — factor and cancel common terms
3. Rationalizing — multiply by the conjugate for expressions with radicals
4. Limits at infinity — divide by the highest power of x

Common limits: lim(x→0) sin(x)/x = 1 and lim(x→0) (1-cos(x))/x = 0.',
'Limits describe the behavior of f(x) as x approaches a value. One-sided limits must agree for the two-sided limit to exist.',
ARRAY['lim(x→a) f(x) = L', 'lim(x→0) sin(x)/x = 1', 'lim(x→0) (1-cos(x))/x = 0'],
ARRAY['function_notation', 'domain_range'],
ARRAY['Evaluate limits using substitution, factoring, and rationalizing', 'Determine one-sided and two-sided limits', 'Evaluate limits at infinity'],
'[{"problem": "Find lim(x→2) (x²-4)/(x-2)", "solution": "Factor: (x-2)(x+2)/(x-2) = x+2. As x→2: 2+2 = 4"}, {"problem": "Find lim(x→∞) (3x²+1)/(x²-5)", "solution": "Divide by x²: (3+1/x²)/(1-5/x²) → 3/1 = 3"}]'::jsonb,
ARRAY['Assuming the limit equals f(a) without checking', 'Forgetting to check one-sided limits', 'Not factoring before evaluating']),

('calculus_vol1', 3, 'Derivatives', '3.1', 'Definition of the Derivative', 'derivative_definition', 'calculus',
'The derivative of f at x is defined as:
f''(x) = lim(h→0) [f(x+h) − f(x)] / h

This limit, when it exists, gives the instantaneous rate of change of f at x and the slope of the tangent line to the graph at (x, f(x)).

Geometric interpretation: The derivative f''(a) is the slope of the tangent line to y = f(x) at x = a. The tangent line equation is y − f(a) = f''(a)(x − a).

Physical interpretation: If s(t) is position, then s''(t) is velocity — the instantaneous rate of change of position.

A function is differentiable at a if f''(a) exists. Differentiability implies continuity, but continuity does not imply differentiability (e.g., |x| at x = 0 is continuous but not differentiable).',
'The derivative is the limit of the difference quotient. It gives the slope of the tangent line and the instantaneous rate of change.',
ARRAY['f''(x) = lim(h→0) [f(x+h) − f(x)] / h', 'tangent line: y − f(a) = f''(a)(x − a)'],
ARRAY['limits_intro', 'function_notation'],
ARRAY['Compute derivatives using the limit definition', 'Find the equation of a tangent line', 'Interpret the derivative as rate of change'],
'[{"problem": "Find f''(x) for f(x) = x² using the definition", "solution": "lim(h→0) [(x+h)²-x²]/h = lim(h→0) [2xh+h²]/h = lim(h→0) (2x+h) = 2x"}, {"problem": "Find the tangent line to f(x) = x² at x = 3", "solution": "f(3) = 9, f''(3) = 6, tangent: y - 9 = 6(x - 3), y = 6x - 9"}]'::jsonb,
ARRAY['Forgetting to take the limit (leaving h in the answer)', 'Algebraic errors when expanding (x+h)²', 'Confusing the tangent line slope with the function value']),

('calculus_vol1', 3, 'Derivatives', '3.3', 'The Power Rule', 'power_rule', 'calculus',
'The power rule states: if f(x) = xⁿ, then f''(x) = nxⁿ⁻¹, where n is any real number.

Combined with the constant multiple rule (d/dx[cf(x)] = cf''(x)) and the sum rule (d/dx[f(x)+g(x)] = f''(x)+g''(x)), this allows differentiation of any polynomial.

Examples:
- d/dx[x⁵] = 5x⁴
- d/dx[3x²] = 6x
- d/dx[x⁻¹] = -x⁻² = -1/x²
- d/dx[√x] = d/dx[x^(1/2)] = (1/2)x^(-1/2) = 1/(2√x)

For a polynomial like f(x) = 4x³ − 2x² + 7x − 5:
f''(x) = 12x² − 4x + 7

The power rule works for any real exponent: integers, fractions, negatives.',
'The power rule d/dx[xⁿ] = nxⁿ⁻¹ is the foundational differentiation rule. Works for any real exponent.',
ARRAY['d/dx[xⁿ] = nxⁿ⁻¹', 'd/dx[cf(x)] = cf''(x)', 'd/dx[f+g] = f'' + g'''],
ARRAY['derivative_definition', 'exponent_rules'],
ARRAY['Apply the power rule to any real exponent', 'Combine with constant multiple and sum rules', 'Differentiate polynomials term by term'],
'[{"problem": "Find d/dx[3x⁴ - 2x + 1]", "solution": "12x³ - 2"}, {"problem": "Find d/dx[5/x²]", "solution": "Rewrite as 5x⁻², derivative = -10x⁻³ = -10/x³"}]'::jsonb,
ARRAY['Not rewriting roots and fractions as power form first', 'Forgetting the derivative of a constant is 0', 'Subtracting 1 from the exponent incorrectly']),

('calculus_vol1', 3, 'Derivatives', '3.5', 'Product and Quotient Rules', 'product_quotient_rule', 'calculus',
'The product rule: d/dx[f(x)g(x)] = f''(x)g(x) + f(x)g''(x)

In words: the derivative of the first times the second, plus the first times the derivative of the second.

The quotient rule: d/dx[f(x)/g(x)] = [f''(x)g(x) − f(x)g''(x)] / [g(x)]²

In words: the derivative of the top times the bottom, minus the top times the derivative of the bottom, all over the bottom squared.

The quotient rule can be remembered as: "low d-high minus high d-low, over the square of what''s below."

Example using product rule: d/dx[x²sin(x)] = 2x·sin(x) + x²·cos(x)

Example using quotient rule: d/dx[sin(x)/x] = [cos(x)·x − sin(x)·1]/x² = [x·cos(x) − sin(x)]/x²',
'Product rule: (fg)'' = f''g + fg''. Quotient rule: (f/g)'' = (f''g - fg'')/g².',
ARRAY['(fg)'' = f''g + fg''', '(f/g)'' = (f''g − fg'')/g²'],
ARRAY['power_rule', 'trig_derivatives'],
ARRAY['Apply the product rule', 'Apply the quotient rule', 'Decide when each rule is needed'],
'[{"problem": "Find d/dx[x³·eˣ]", "solution": "3x²·eˣ + x³·eˣ = eˣ(3x² + x³) = x²eˣ(3 + x)"}, {"problem": "Find d/dx[(2x+1)/(x-3)]", "solution": "[2(x-3) - (2x+1)(1)]/(x-3)² = -7/(x-3)²"}]'::jsonb,
ARRAY['Getting the sign wrong in the quotient rule (it is minus, not plus)', 'Forgetting to square the denominator', 'Not simplifying after applying the rule']),

('calculus_vol1', 3, 'Derivatives', '3.6', 'The Chain Rule', 'chain_rule', 'calculus',
'The chain rule differentiates composite functions. If y = f(g(x)), then:
dy/dx = f''(g(x)) · g''(x)

In Leibniz notation: if y = f(u) and u = g(x), then dy/dx = (dy/du)(du/dx).

Steps to apply the chain rule:
1. Identify the outer function f and the inner function g
2. Differentiate the outer function, leaving the inner function inside
3. Multiply by the derivative of the inner function

Common patterns:
- d/dx[sin(3x)] = cos(3x) · 3 = 3cos(3x)
- d/dx[(x²+1)⁵] = 5(x²+1)⁴ · 2x = 10x(x²+1)⁴
- d/dx[eˣ²] = eˣ² · 2x = 2xeˣ²
- d/dx[ln(sin x)] = (1/sin x) · cos x = cot x

The chain rule can be applied multiple times for deeply nested compositions.',
'The chain rule differentiates composite functions: d/dx[f(g(x))] = f''(g(x))·g''(x). Identify outer and inner functions.',
ARRAY['d/dx[f(g(x))] = f''(g(x)) · g''(x)', 'dy/dx = (dy/du)(du/dx)'],
ARRAY['power_rule', 'product_quotient_rule', 'trig_derivatives'],
ARRAY['Identify outer and inner functions in a composition', 'Apply the chain rule', 'Combine with other differentiation rules'],
'[{"problem": "Find d/dx[sin(x²)]", "solution": "outer: sin(u), inner: x². d/dx = cos(x²) · 2x = 2x·cos(x²)"}, {"problem": "Find d/dx[(3x+1)⁴]", "solution": "4(3x+1)³ · 3 = 12(3x+1)³"}]'::jsonb,
ARRAY['Forgetting to multiply by the inner derivative', 'Not identifying the correct outer/inner functions', 'Stopping after differentiating the outer function']),

('calculus_vol1', 5, 'Integration', '5.1', 'Antiderivatives', 'antiderivatives', 'calculus',
'An antiderivative of f(x) is a function F(x) such that F''(x) = f(x). The general antiderivative is F(x) + C, where C is the constant of integration.

Basic antiderivative rules (reverse of derivative rules):
- ∫xⁿ dx = xⁿ⁺¹/(n+1) + C, where n ≠ -1
- ∫(1/x) dx = ln|x| + C
- ∫eˣ dx = eˣ + C
- ∫sin(x) dx = -cos(x) + C
- ∫cos(x) dx = sin(x) + C
- ∫sec²(x) dx = tan(x) + C

The constant of integration C is necessary because many different functions can have the same derivative (they differ by a constant). For example, x², x² + 5, and x² - 3 all have derivative 2x.

When finding a particular antiderivative, use an initial condition to solve for C.',
'An antiderivative reverses differentiation. The general antiderivative includes + C because constants disappear in differentiation.',
ARRAY['∫xⁿ dx = xⁿ⁺¹/(n+1) + C', '∫sin(x) dx = -cos(x) + C', '∫cos(x) dx = sin(x) + C', '∫eˣ dx = eˣ + C'],
ARRAY['power_rule', 'trig_derivatives'],
ARRAY['Find antiderivatives using basic rules', 'Include the constant of integration', 'Use initial conditions to find particular solutions'],
'[{"problem": "Find ∫(3x² + 2x - 1)dx", "solution": "x³ + x² - x + C"}, {"problem": "Find f(x) if f''(x) = 2x and f(0) = 5", "solution": "f(x) = x² + C, f(0) = 5 → C = 5, so f(x) = x² + 5"}]'::jsonb,
ARRAY['Forgetting the + C', 'Getting the sign wrong on trig antiderivatives', 'Using the power rule with n = -1 (need ln|x| instead)']),

('calculus_vol1', 5, 'Integration', '5.3', 'The Fundamental Theorem of Calculus', 'fundamental_theorem', 'calculus',
'The Fundamental Theorem of Calculus (FTC) connects differentiation and integration.

Part 1: If f is continuous on [a,b] and F(x) = ∫ₐˣ f(t)dt, then F''(x) = f(x). In other words, the derivative of an integral (with variable upper limit) is the original function.

Part 2: If F is any antiderivative of f on [a,b], then:
∫ₐᵇ f(x)dx = F(b) − F(a)

This means to evaluate a definite integral:
1. Find an antiderivative F(x)
2. Evaluate F at the upper limit b
3. Subtract F evaluated at the lower limit a

Example: ∫₁³ 2x dx = [x²]₁³ = 3² − 1² = 9 − 1 = 8

FTC Part 1 tells us differentiation undoes integration.
FTC Part 2 tells us integration undoes differentiation (up to a constant).',
'The FTC connects derivatives and integrals. Part 1: d/dx[∫ₐˣ f(t)dt] = f(x). Part 2: ∫ₐᵇ f(x)dx = F(b) - F(a).',
ARRAY['∫ₐᵇ f(x)dx = F(b) − F(a)', 'd/dx[∫ₐˣ f(t)dt] = f(x)'],
ARRAY['antiderivatives', 'limits_intro'],
ARRAY['State both parts of the FTC', 'Evaluate definite integrals using FTC Part 2', 'Apply FTC Part 1 to derivatives of integrals'],
'[{"problem": "Evaluate ∫₀² (3x² + 1)dx", "solution": "[x³ + x]₀² = (8 + 2) - (0 + 0) = 10"}, {"problem": "Find d/dx[∫₀ˣ cos(t²)dt]", "solution": "By FTC Part 1: cos(x²)"}]'::jsonb,
ARRAY['Forgetting to evaluate at both limits (upper minus lower)', 'Getting the subtraction order wrong (it is F(b) - F(a))', 'Not applying the chain rule when the upper limit is not just x']),

-- ═══ ALGEBRA ═══════════════════════════════════════════════════════════

('college_algebra', 2, 'Equations and Inequalities', '2.5', 'Quadratic Equations', 'quadratic_formula', 'algebra',
'A quadratic equation has the form ax² + bx + c = 0 where a ≠ 0.

Methods for solving:
1. Factoring: Find two numbers that multiply to ac and add to b
2. Completing the square: Rewrite in the form (x + p)² = q
3. Quadratic formula: x = (-b ± √(b²-4ac)) / (2a)

The discriminant b²-4ac determines the nature of the solutions:
- If b²-4ac > 0: two distinct real solutions
- If b²-4ac = 0: one repeated real solution
- If b²-4ac < 0: two complex conjugate solutions

The quadratic formula works for ANY quadratic equation and is derived by completing the square on the general form ax² + bx + c = 0.

For the equation 2x² - 5x + 3 = 0: a=2, b=-5, c=3
x = (5 ± √(25-24))/4 = (5 ± 1)/4, so x = 3/2 or x = 1.',
'The quadratic formula x = (-b ± √(b²-4ac))/(2a) solves any quadratic. The discriminant tells you how many real solutions exist.',
ARRAY['x = (-b ± √(b²-4ac)) / (2a)', 'discriminant = b² - 4ac'],
ARRAY['factoring', 'square_roots'],
ARRAY['Solve quadratics by factoring, completing the square, and the formula', 'Use the discriminant to determine the number of solutions', 'Choose the most efficient method'],
'[{"problem": "Solve x² - 5x + 6 = 0", "solution": "Factor: (x-2)(x-3) = 0, x = 2 or x = 3"}, {"problem": "Solve 2x² + 3x - 1 = 0", "solution": "x = (-3 ± √(9+8))/4 = (-3 ± √17)/4"}]'::jsonb,
ARRAY['Sign errors with the ± and the -b', 'Forgetting to divide the entire numerator by 2a', 'Not checking if factoring works first (faster than the formula)']),

('college_algebra', 3, 'Functions', '3.4', 'Difference of Squares', 'difference_of_squares', 'algebra',
'The difference of squares pattern states: a² - b² = (a - b)(a + b)

This factoring pattern applies whenever you have a subtraction between two perfect squares.

How to recognize it:
- The expression has exactly two terms
- The terms are subtracted (not added)
- Both terms are perfect squares

Examples:
- x² - 9 = (x - 3)(x + 3) because 9 = 3²
- 4x² - 25 = (2x - 5)(2x + 5) because 4x² = (2x)² and 25 = 5²
- x⁴ - 16 = (x² - 4)(x² + 4) = (x - 2)(x + 2)(x² + 4)

Note: a² + b² (sum of squares) does NOT factor over the real numbers.

This pattern appears frequently in simplifying expressions, solving equations, and working with rational expressions.',
'Difference of squares: a² - b² = (a-b)(a+b). Recognize perfect squares being subtracted. Sum of squares does not factor.',
ARRAY['a² - b² = (a - b)(a + b)'],
ARRAY['exponent_rules', 'perfect_squares'],
ARRAY['Recognize the difference of squares pattern', 'Factor using a² - b² = (a-b)(a+b)', 'Apply to higher-degree expressions'],
'[{"problem": "Factor x² - 49", "solution": "(x - 7)(x + 7)"}, {"problem": "Factor 9x² - 16y²", "solution": "(3x - 4y)(3x + 4y)"}, {"problem": "Factor x⁴ - 81", "solution": "(x² - 9)(x² + 9) = (x-3)(x+3)(x²+9)"}]'::jsonb,
ARRAY['Trying to factor a² + b² (it does not factor)', 'Not recognizing that 4x² is a perfect square (2x)²', 'Stopping too early — check if factors can be factored further']);
