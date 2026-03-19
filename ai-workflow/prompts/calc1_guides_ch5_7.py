"""
Calculus 1 Teaching Guides — Chapters 5, 6, and 7
Differentiation Rules, Chain Rule & Advanced Differentiation,
and Applications of Derivatives Part 1.

17 lesson guides covering topics 5.1 through 7.5.
"""

CALC1_GUIDES_CH5_7 = {

    # =========================================================================
    # CHAPTER 5 — Differentiation Rules
    # =========================================================================

    "power-rule": {
        "id": "5.1",
        "slug": "power-rule",
        "title": "The Power Rule",
        "chapter": 5,
        "chapter_title": "Differentiation Rules",
        "subject": "calc-1",
        "prerequisites": ["definition-of-derivative", "limit-laws"],
        "estimated_time": "25 min",
        "difficulty": "beginner",
        "teaching_content": (
            "CHUNK 1: The Power Rule Statement\n"
            "The power rule is the single most-used differentiation rule in all of calculus. "
            "It says: if f(x) = x^n, then f'(x) = n * x^(n-1). In words, bring the exponent "
            "down as a coefficient and reduce the exponent by one.\n\n"
            "This rule works for ALL real exponents n — positive integers, negative integers, "
            "fractions, even irrational numbers like pi.\n\n"
            "Proof sketch for positive integers:\n"
            "Start from the limit definition: f'(x) = lim(h->0) [(x+h)^n - x^n] / h.\n"
            "Expand (x+h)^n using the binomial theorem:\n"
            "(x+h)^n = x^n + n*x^(n-1)*h + terms with h^2, h^3, ...\n"
            "Subtract x^n, divide by h, and all higher-order terms vanish as h->0, "
            "leaving n*x^(n-1).\n"
            "---\n"
            "CHUNK 2: Examples with Positive Integer Exponents\n\n"
            "Example 1: f(x) = x^5\n"
            "f'(x) = 5 * x^(5-1) = 5x^4\n\n"
            "Example 2: f(x) = x^1\n"
            "f'(x) = 1 * x^(1-1) = 1 * x^0 = 1\n"
            "This confirms that the derivative of x is 1, which makes sense — the line y=x "
            "has slope 1 everywhere.\n\n"
            "Example 3: f(x) = x^0 = 1 (a constant)\n"
            "f'(x) = 0 * x^(-1) = 0\n"
            "Constants have derivative zero. The power rule handles this naturally.\n"
            "---\n"
            "CHUNK 3: Negative and Fractional Exponents\n\n"
            "The power rule extends seamlessly to non-positive-integer exponents. The key is "
            "to rewrite functions in x^n form first.\n\n"
            "Example 1 (negative exponent): f(x) = 1/x^3 = x^(-3)\n"
            "f'(x) = -3 * x^(-3-1) = -3x^(-4) = -3/x^4\n\n"
            "Example 2 (fractional exponent): f(x) = sqrt(x) = x^(1/2)\n"
            "f'(x) = (1/2) * x^(1/2 - 1) = (1/2) * x^(-1/2) = 1 / (2*sqrt(x))\n\n"
            "Example 3 (negative fraction): f(x) = 1/sqrt(x) = x^(-1/2)\n"
            "f'(x) = (-1/2) * x^(-1/2 - 1) = (-1/2) * x^(-3/2) = -1 / (2*x^(3/2))\n\n"
            "Tip: Always rewrite roots and reciprocals as power functions before differentiating."
        ),
        "key_concepts": [
            "d/dx[x^n] = n * x^(n-1) for all real n",
            "Bring exponent down, reduce by one",
            "Works for negative and fractional exponents",
            "Rewrite roots and reciprocals as powers first",
            "Proof via binomial theorem for positive integers",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Test basic power rule with positive integers, then require rewriting "
            "roots or reciprocals before differentiating. Include at least one fractional "
            "exponent and one negative exponent problem."
        ),
        "practice_problems": [
            {"problem": "Find f'(x) if f(x) = x^7", "answer": "7x^6"},
            {"problem": "Differentiate g(x) = x^(-2)", "answer": "-2x^(-3) or -2/x^3"},
            {"problem": "Find dy/dx if y = x^(3/4)", "answer": "(3/4)x^(-1/4)"},
            {"problem": "Differentiate h(x) = 1/x^5", "answer": "-5x^(-6) or -5/x^6"},
        ],
        "common_mistakes": [
            "Forgetting to subtract 1 from the exponent (writing x^n instead of x^(n-1))",
            "Not rewriting sqrt(x) as x^(1/2) before applying the rule",
            "Dropping the negative sign when working with negative exponents",
        ],
        "builds_toward": ["constant-sum-difference-rules", "product-rule", "chain-rule"],
    },

    "constant-sum-difference-rules": {
        "id": "5.2",
        "slug": "constant-sum-difference-rules",
        "title": "Constant, Sum, and Difference Rules",
        "chapter": 5,
        "chapter_title": "Differentiation Rules",
        "subject": "calc-1",
        "prerequisites": ["power-rule", "definition-of-derivative"],
        "estimated_time": "20 min",
        "difficulty": "beginner",
        "teaching_content": (
            "CHUNK 1: The Constant Multiple Rule\n"
            "If c is a constant and f(x) is differentiable, then:\n"
            "d/dx[c * f(x)] = c * f'(x)\n\n"
            "In words: constants factor out of derivatives. This follows directly from the "
            "limit definition since constants pass through limits.\n\n"
            "Example 1: d/dx[7x^3] = 7 * d/dx[x^3] = 7 * 3x^2 = 21x^2\n\n"
            "Example 2: d/dx[-4x^5] = -4 * 5x^4 = -20x^4\n\n"
            "Special case — the constant rule: d/dx[c] = 0 for any constant c. A constant "
            "function has zero rate of change everywhere.\n"
            "---\n"
            "CHUNK 2: The Sum and Difference Rules\n"
            "d/dx[f(x) + g(x)] = f'(x) + g'(x)\n"
            "d/dx[f(x) - g(x)] = f'(x) - g'(x)\n\n"
            "In words: the derivative of a sum (or difference) is the sum (or difference) "
            "of the derivatives. You can differentiate term by term.\n\n"
            "Together with the constant multiple rule, these properties mean differentiation "
            "is a LINEAR operation. You can break any polynomial into individual terms and "
            "handle each one separately.\n"
            "---\n"
            "CHUNK 3: Putting It All Together — Polynomials\n\n"
            "Example 1: f(x) = 3x^4 - 5x^2 + 8x - 11\n"
            "f'(x) = 3*4x^3 - 5*2x + 8*1 - 0 = 12x^3 - 10x + 8\n\n"
            "Example 2: g(x) = (2/3)x^6 + 4*sqrt(x) - 1/x\n"
            "Rewrite: g(x) = (2/3)x^6 + 4x^(1/2) - x^(-1)\n"
            "g'(x) = (2/3)*6x^5 + 4*(1/2)x^(-1/2) - (-1)x^(-2)\n"
            "      = 4x^5 + 2/sqrt(x) + 1/x^2\n\n"
            "Example 3: h(t) = 5t^3 - 2t^(-2) + 7\n"
            "h'(t) = 15t^2 + 4t^(-3) = 15t^2 + 4/t^3"
        ),
        "key_concepts": [
            "d/dx[c * f(x)] = c * f'(x) — constants factor out",
            "d/dx[c] = 0 — derivative of a constant is zero",
            "d/dx[f + g] = f' + g' — sum rule",
            "d/dx[f - g] = f' - g' — difference rule",
            "Differentiation is linear: differentiate term by term",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Give polynomials of degree 3-5 with various constant coefficients. "
            "Include at least one problem mixing fractional exponents and negative exponents "
            "with constant multiples."
        ),
        "practice_problems": [
            {"problem": "Differentiate f(x) = 6x^3 - 2x + 9", "answer": "18x^2 - 2"},
            {"problem": "Find g'(x) if g(x) = -3x^4 + x^2 - 7x + 1", "answer": "-12x^3 + 2x - 7"},
            {"problem": "Differentiate h(x) = 5*sqrt(x) + 3/x", "answer": "5/(2*sqrt(x)) - 3/x^2"},
        ],
        "common_mistakes": [
            "Forgetting the derivative of a standalone constant term (it is 0, not 1)",
            "Losing track of negative signs when differentiating a difference",
            "Not distributing the constant multiple before differentiating (e.g., treating 3x^2 as x^2)",
        ],
        "builds_toward": ["product-rule", "quotient-rule", "higher-order-derivatives"],
    },

    "product-rule": {
        "id": "5.3",
        "slug": "product-rule",
        "title": "The Product Rule",
        "chapter": 5,
        "chapter_title": "Differentiation Rules",
        "subject": "calc-1",
        "prerequisites": ["power-rule", "constant-sum-difference-rules"],
        "estimated_time": "30 min",
        "difficulty": "intermediate",
        "teaching_content": (
            "CHUNK 1: Why We Need the Product Rule\n"
            "A common early mistake is to assume d/dx[f*g] = f' * g'. This is FALSE.\n"
            "For instance, d/dx[x * x] should be d/dx[x^2] = 2x, not 1 * 1 = 1.\n\n"
            "The correct product rule is:\n"
            "d/dx[f(x) * g(x)] = f'(x) * g(x) + f(x) * g'(x)\n\n"
            "In words: (derivative of the first)(times the second) + (the first)(times the "
            "derivative of the second).\n\n"
            "Proof sketch: Start with the limit definition and add/subtract f(x)*g(x+h) in the "
            "numerator to split into two limits:\n"
            "lim(h->0) [f(x+h)g(x+h) - f(x)g(x)] / h\n"
            "= lim(h->0) [f(x+h)g(x+h) - f(x)g(x+h) + f(x)g(x+h) - f(x)g(x)] / h\n"
            "= lim(h->0) g(x+h)*[f(x+h)-f(x)]/h + f(x)*[g(x+h)-g(x)]/h\n"
            "= g(x)*f'(x) + f(x)*g'(x)\n"
            "---\n"
            "CHUNK 2: Worked Examples\n\n"
            "Example 1: y = x^2 * sin(x)\n"
            "Let f = x^2, g = sin(x). Then f' = 2x, g' = cos(x).\n"
            "y' = 2x * sin(x) + x^2 * cos(x)\n\n"
            "Example 2: y = (3x + 1)(x^2 - 4)\n"
            "Let f = 3x + 1, g = x^2 - 4. Then f' = 3, g' = 2x.\n"
            "y' = 3*(x^2 - 4) + (3x + 1)*2x\n"
            "   = 3x^2 - 12 + 6x^2 + 2x\n"
            "   = 9x^2 + 2x - 12\n"
            "(You can verify by expanding first: y = 3x^3 + x^2 - 12x - 4, y' = 9x^2 + 2x - 12. Same answer!)\n\n"
            "Example 3: y = sqrt(x) * (x^2 + 3)\n"
            "f = x^(1/2), g = x^2 + 3. Then f' = (1/2)x^(-1/2), g' = 2x.\n"
            "y' = (1/2)x^(-1/2)*(x^2 + 3) + x^(1/2)*2x\n"
            "   = (x^2 + 3)/(2*sqrt(x)) + 2x*sqrt(x)\n"
            "   = (x^2 + 3)/(2*sqrt(x)) + 2x^(3/2)\n"
            "---\n"
            "CHUNK 3: Tips and Extensions\n\n"
            "Mnemonic: Think of it as \"first d-second + d-first second\" or remember the "
            "phrase: \"left d-right plus d-left right.\"\n\n"
            "The product rule extends to three or more factors:\n"
            "d/dx[f*g*h] = f'*g*h + f*g'*h + f*g*h'\n"
            "Each factor takes a turn being differentiated while the others stay.\n\n"
            "When one factor is just a constant, the product rule still works but reduces "
            "to the constant multiple rule (the derivative of the constant factor is 0)."
        ),
        "key_concepts": [
            "d/dx[f*g] = f'*g + f*g' — NOT f'*g'",
            "Proof uses the add-and-subtract trick in the limit definition",
            "Extends to three+ factors: each takes a turn being differentiated",
            "Reduces to constant multiple rule when one factor is constant",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Include products of polynomials (verifiable by expanding), products involving "
            "trig functions, and at least one product of three factors."
        ),
        "practice_problems": [
            {"problem": "Differentiate f(x) = x^3 * (2x + 5)", "answer": "3x^2*(2x+5) + x^3*2 = 8x^3 + 15x^2"},
            {"problem": "Find dy/dx if y = (x^2 + 1)*sin(x)", "answer": "2x*sin(x) + (x^2+1)*cos(x)"},
            {"problem": "Differentiate g(x) = x * e^x", "answer": "e^x + x*e^x = (1+x)*e^x"},
        ],
        "common_mistakes": [
            "Assuming d/dx[f*g] = f' * g' (the most common error)",
            "Forgetting one of the two terms in the product rule",
            "Not simplifying the result when possible",
        ],
        "builds_toward": ["quotient-rule", "chain-rule", "implicit-differentiation"],
    },

    "quotient-rule": {
        "id": "5.4",
        "slug": "quotient-rule",
        "title": "The Quotient Rule",
        "chapter": 5,
        "chapter_title": "Differentiation Rules",
        "subject": "calc-1",
        "prerequisites": ["product-rule", "power-rule"],
        "estimated_time": "30 min",
        "difficulty": "intermediate",
        "teaching_content": (
            "CHUNK 1: The Quotient Rule Statement\n"
            "If f(x) and g(x) are differentiable and g(x) != 0, then:\n"
            "d/dx[f(x)/g(x)] = [f'(x)*g(x) - f(x)*g'(x)] / [g(x)]^2\n\n"
            "The classic mnemonic: \"lo d-hi minus hi d-lo, over lo-lo\" where \"hi\" is the "
            "numerator f, \"lo\" is the denominator g, and \"d\" means derivative.\n\n"
            "Another mnemonic: (bottom * d-top - top * d-bottom) / bottom^2\n\n"
            "Notice the MINUS sign — order matters! The product rule has a plus, but the "
            "quotient rule has a minus, and it is specifically f'g - fg' (not fg' - f'g).\n"
            "---\n"
            "CHUNK 2: Worked Examples\n\n"
            "Example 1: y = (x^2 + 1) / (x - 3)\n"
            "f = x^2 + 1, f' = 2x, g = x - 3, g' = 1\n"
            "y' = [2x*(x-3) - (x^2+1)*1] / (x-3)^2\n"
            "   = [2x^2 - 6x - x^2 - 1] / (x-3)^2\n"
            "   = (x^2 - 6x - 1) / (x-3)^2\n\n"
            "Example 2: y = sin(x) / x\n"
            "f = sin(x), f' = cos(x), g = x, g' = 1\n"
            "y' = [cos(x)*x - sin(x)*1] / x^2\n"
            "   = [x*cos(x) - sin(x)] / x^2\n\n"
            "Example 3: y = (3x + 2) / (x^2 + 1)\n"
            "f = 3x + 2, f' = 3, g = x^2 + 1, g' = 2x\n"
            "y' = [3*(x^2+1) - (3x+2)*2x] / (x^2+1)^2\n"
            "   = [3x^2 + 3 - 6x^2 - 4x] / (x^2+1)^2\n"
            "   = (-3x^2 - 4x + 3) / (x^2+1)^2\n"
            "---\n"
            "CHUNK 3: When to Avoid the Quotient Rule\n\n"
            "The quotient rule is powerful but messy. Sometimes it is easier to rewrite "
            "the function and use simpler rules:\n\n"
            "Instead of: d/dx[5/x^3], rewrite as d/dx[5*x^(-3)] = 5*(-3)*x^(-4) = -15/x^4\n\n"
            "Instead of: d/dx[(x^2 + 1)/x], rewrite as d/dx[x + x^(-1)] = 1 - 1/x^2\n\n"
            "Rule of thumb: if the denominator is a single power of x, rewriting with "
            "negative exponents and using the power rule is usually cleaner."
        ),
        "key_concepts": [
            "d/dx[f/g] = (f'g - fg') / g^2",
            "The minus sign makes order matter: f'g - fg', not fg' - f'g",
            "Mnemonic: lo d-hi minus hi d-lo over lo-lo",
            "Sometimes rewriting with negative exponents avoids the quotient rule entirely",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Include at least one straightforward quotient, one involving trig, and one "
            "where rewriting avoids the quotient rule. Test that students get the sign right."
        ),
        "practice_problems": [
            {"problem": "Differentiate y = x / (x + 1)", "answer": "1/(x+1)^2"},
            {"problem": "Find f'(x) for f(x) = (x^2 - 1)/(x^2 + 1)", "answer": "4x/(x^2+1)^2"},
            {"problem": "Differentiate y = cos(x)/x^2", "answer": "[-x*sin(x) - 2*cos(x)] / x^3"},
        ],
        "common_mistakes": [
            "Getting the subtraction order backwards (fg' - f'g instead of f'g - fg')",
            "Forgetting to square the denominator",
            "Using the quotient rule when rewriting with negative exponents would be simpler",
        ],
        "builds_toward": ["chain-rule", "derivatives-of-trig", "implicit-differentiation"],
    },

    "derivatives-of-trig": {
        "id": "5.5",
        "slug": "derivatives-of-trig",
        "title": "Derivatives of Trigonometric Functions",
        "chapter": 5,
        "chapter_title": "Differentiation Rules",
        "subject": "calc-1",
        "prerequisites": ["power-rule", "quotient-rule", "product-rule"],
        "estimated_time": "35 min",
        "difficulty": "intermediate",
        "teaching_content": (
            "CHUNK 1: The Big Six Trig Derivatives\n"
            "d/dx[sin(x)] = cos(x)\n"
            "d/dx[cos(x)] = -sin(x)\n"
            "d/dx[tan(x)] = sec^2(x)\n"
            "d/dx[cot(x)] = -csc^2(x)\n"
            "d/dx[sec(x)] = sec(x)*tan(x)\n"
            "d/dx[csc(x)] = -csc(x)*cot(x)\n\n"
            "Notice the pattern: the \"co-\" functions (cos, cot, csc) all have a negative sign "
            "in their derivatives.\n\n"
            "Memory aid: pair them up — sin/cos, tan/sec, cot/csc. In each pair, the derivative "
            "of the first uses the second (with possible negatives and squares).\n"
            "---\n"
            "CHUNK 2: Proving d/dx[sin(x)] = cos(x) from the Limit Definition\n\n"
            "f'(x) = lim(h->0) [sin(x+h) - sin(x)] / h\n\n"
            "Use the angle addition formula: sin(x+h) = sin(x)cos(h) + cos(x)sin(h)\n\n"
            "So: [sin(x)cos(h) + cos(x)sin(h) - sin(x)] / h\n"
            "  = sin(x)*[cos(h)-1]/h + cos(x)*sin(h)/h\n\n"
            "Now use the two key limits:\n"
            "  lim(h->0) sin(h)/h = 1\n"
            "  lim(h->0) [cos(h)-1]/h = 0\n\n"
            "Result: f'(x) = sin(x)*0 + cos(x)*1 = cos(x)\n\n"
            "Once you have d/dx[sin] = cos, you can derive d/dx[cos] = -sin similarly, "
            "and then get the other four using the quotient rule.\n"
            "---\n"
            "CHUNK 3: Deriving the Other Derivatives and Examples\n\n"
            "d/dx[tan(x)] = d/dx[sin(x)/cos(x)]:\n"
            "= [cos(x)*cos(x) - sin(x)*(-sin(x))] / cos^2(x)\n"
            "= [cos^2(x) + sin^2(x)] / cos^2(x)\n"
            "= 1/cos^2(x) = sec^2(x)\n\n"
            "Example 1: y = 3*sin(x) + 2*cos(x)\n"
            "y' = 3*cos(x) + 2*(-sin(x)) = 3*cos(x) - 2*sin(x)\n\n"
            "Example 2: y = x^2 * tan(x)  (product rule)\n"
            "y' = 2x*tan(x) + x^2*sec^2(x)\n\n"
            "Example 3: y = sec(x) / x  (quotient rule)\n"
            "y' = [sec(x)*tan(x)*x - sec(x)*1] / x^2\n"
            "   = sec(x)*[x*tan(x) - 1] / x^2"
        ),
        "key_concepts": [
            "d/dx[sin x] = cos x and d/dx[cos x] = -sin x",
            "d/dx[tan x] = sec^2 x and d/dx[sec x] = sec x * tan x",
            "d/dx[cot x] = -csc^2 x and d/dx[csc x] = -csc x * cot x",
            "Co-functions always carry a negative sign in their derivatives",
            "Proof of d/dx[sin x] relies on lim(h->0) sin(h)/h = 1",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Test recall of all six derivatives. Include combinations with product/quotient "
            "rules. Ask at least one question requiring the proof idea (which limits are used)."
        ),
        "practice_problems": [
            {"problem": "Differentiate f(x) = 5*sin(x) - 2*sec(x)", "answer": "5*cos(x) - 2*sec(x)*tan(x)"},
            {"problem": "Find dy/dx if y = x*cos(x)", "answer": "cos(x) - x*sin(x)"},
            {"problem": "Differentiate g(x) = tan(x) + cot(x)", "answer": "sec^2(x) - csc^2(x)"},
        ],
        "common_mistakes": [
            "Forgetting the negative sign in d/dx[cos x] = -sin x",
            "Confusing sec^2(x) with sec(x)^2 notation (they mean the same thing)",
            "Mixing up the derivatives of sec and csc",
        ],
        "builds_toward": ["chain-rule", "derivatives-of-inverse-trig", "implicit-differentiation"],
    },

    "higher-order-derivatives": {
        "id": "5.6",
        "slug": "higher-order-derivatives",
        "title": "Higher-Order Derivatives",
        "chapter": 5,
        "chapter_title": "Differentiation Rules",
        "subject": "calc-1",
        "prerequisites": ["power-rule", "constant-sum-difference-rules", "derivatives-of-trig"],
        "estimated_time": "20 min",
        "difficulty": "beginner",
        "teaching_content": (
            "CHUNK 1: What Are Higher-Order Derivatives?\n"
            "The derivative of a derivative is called the second derivative. You can keep going — "
            "the derivative of the second derivative is the third derivative, and so on.\n\n"
            "Notation for the second derivative:\n"
            "  f''(x)  or  d^2y/dx^2  or  y''\n\n"
            "Notation for the third derivative:\n"
            "  f'''(x)  or  d^3y/dx^3  or  y'''\n\n"
            "For the nth derivative (n >= 4), we write:\n"
            "  f^(n)(x)  or  d^n y / dx^n\n"
            "(Parentheses around n to distinguish from an exponent.)\n"
            "---\n"
            "CHUNK 2: Worked Examples\n\n"
            "Example 1: f(x) = x^5 - 3x^3 + 2x\n"
            "f'(x) = 5x^4 - 9x^2 + 2\n"
            "f''(x) = 20x^3 - 18x\n"
            "f'''(x) = 60x^2 - 18\n"
            "f^(4)(x) = 120x\n"
            "f^(5)(x) = 120\n"
            "f^(6)(x) = 0  (and all higher derivatives are 0)\n\n"
            "For a polynomial of degree n, the (n+1)th derivative and beyond are always 0.\n\n"
            "Example 2: f(x) = sin(x)\n"
            "f'(x) = cos(x)\n"
            "f''(x) = -sin(x)\n"
            "f'''(x) = -cos(x)\n"
            "f^(4)(x) = sin(x)\n"
            "The derivatives of sin cycle with period 4!\n\n"
            "Example 3: f(x) = e^x\n"
            "f'(x) = e^x, f''(x) = e^x, f'''(x) = e^x, ...\n"
            "Every derivative of e^x is e^x.\n"
            "---\n"
            "CHUNK 3: Physical Meaning — Position, Velocity, Acceleration\n\n"
            "If s(t) represents position as a function of time:\n"
            "  s'(t) = v(t) = velocity (rate of change of position)\n"
            "  s''(t) = v'(t) = a(t) = acceleration (rate of change of velocity)\n"
            "  s'''(t) = a'(t) = jerk (rate of change of acceleration)\n\n"
            "Example: A ball's height is s(t) = -16t^2 + 48t + 5 feet.\n"
            "Velocity: v(t) = s'(t) = -32t + 48 ft/s\n"
            "Acceleration: a(t) = s''(t) = -32 ft/s^2 (constant — this is gravity!)\n\n"
            "The second derivative also tells us about concavity of curves, which we will "
            "explore thoroughly in applications of derivatives."
        ),
        "key_concepts": [
            "f''(x) = d^2y/dx^2 is the second derivative (derivative of the derivative)",
            "Polynomial of degree n has all-zero derivatives from order n+1 onward",
            "Trig derivatives cycle: sin -> cos -> -sin -> -cos -> sin ...",
            "Position -> velocity -> acceleration via successive derivatives",
            "Second derivative relates to concavity of a curve",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Ask students to compute second and third derivatives of polynomials and "
            "trig functions. Include a word problem connecting position, velocity, and acceleration."
        ),
        "practice_problems": [
            {"problem": "Find f''(x) if f(x) = 4x^5 - x^3 + 6x", "answer": "80x^3 - 6x"},
            {"problem": "Find the third derivative of g(x) = cos(x)", "answer": "sin(x)"},
            {"problem": "If s(t) = t^3 - 6t^2 + 9t, find the acceleration a(t)", "answer": "a(t) = s''(t) = 6t - 12"},
        ],
        "common_mistakes": [
            "Confusing notation: f^(4)(x) means the fourth derivative, not f(x) to the 4th power",
            "Losing track of signs in repeated differentiation of trig functions",
            "Forgetting that acceleration is the second derivative, not the first",
        ],
        "builds_toward": ["mean-value-theorem", "lhopitals-rule", "related-rates"],
    },

    # =========================================================================
    # CHAPTER 6 — The Chain Rule and Advanced Differentiation
    # =========================================================================

    "chain-rule": {
        "id": "6.1",
        "slug": "chain-rule",
        "title": "The Chain Rule",
        "chapter": 6,
        "chapter_title": "The Chain Rule and Advanced Differentiation",
        "subject": "calc-1",
        "prerequisites": ["power-rule", "product-rule", "derivatives-of-trig"],
        "estimated_time": "40 min",
        "difficulty": "intermediate",
        "teaching_content": (
            "CHUNK 1: The Chain Rule Statement\n"
            "The chain rule handles compositions of functions — functions inside functions.\n\n"
            "If y = f(g(x)), then:\n"
            "dy/dx = f'(g(x)) * g'(x)\n\n"
            "In words: take the derivative of the OUTER function (evaluated at the inner function), "
            "then multiply by the derivative of the INNER function.\n\n"
            "Leibniz notation makes this intuitive. If y = f(u) and u = g(x), then:\n"
            "dy/dx = (dy/du) * (du/dx)\n"
            "The du's \"cancel\" (not rigorously, but it is a useful way to remember the rule).\n\n"
            "The outer-inner method:\n"
            "Step 1: Identify the outer function and the inner function.\n"
            "Step 2: Differentiate the outer function, leaving the inner function untouched.\n"
            "Step 3: Multiply by the derivative of the inner function.\n"
            "---\n"
            "CHUNK 2: Worked Examples\n\n"
            "Example 1: y = (3x + 1)^5\n"
            "Outer: u^5, Inner: u = 3x + 1\n"
            "dy/dx = 5*(3x+1)^4 * 3 = 15*(3x+1)^4\n\n"
            "Example 2: y = sin(x^2)\n"
            "Outer: sin(u), Inner: u = x^2\n"
            "dy/dx = cos(x^2) * 2x = 2x*cos(x^2)\n\n"
            "Example 3: y = sqrt(4x^3 - x)\n"
            "Rewrite: y = (4x^3 - x)^(1/2)\n"
            "Outer: u^(1/2), Inner: u = 4x^3 - x\n"
            "dy/dx = (1/2)*(4x^3 - x)^(-1/2) * (12x^2 - 1)\n"
            "      = (12x^2 - 1) / (2*sqrt(4x^3 - x))\n"
            "---\n"
            "CHUNK 3: Chains Within Chains and Tips\n\n"
            "Compositions can be nested multiple levels deep. Apply the chain rule repeatedly.\n\n"
            "Example: y = cos^3(2x) = [cos(2x)]^3\n"
            "Three layers: outermost is u^3, middle is cos(v), innermost is v = 2x.\n"
            "dy/dx = 3*[cos(2x)]^2 * (-sin(2x)) * 2\n"
            "      = -6*cos^2(2x)*sin(2x)\n\n"
            "Tip: The chain rule is used far more often than students expect. Anytime the "
            "argument of a function is anything other than plain x, you need the chain rule.\n\n"
            "d/dx[sin(5x)] = cos(5x) * 5  (inner = 5x, derivative = 5)\n"
            "d/dx[(x^2+1)^10] = 10*(x^2+1)^9 * 2x  (inner = x^2+1)\n\n"
            "The chain rule combines with every other rule — product rule + chain rule, "
            "quotient rule + chain rule, etc."
        ),
        "key_concepts": [
            "d/dx[f(g(x))] = f'(g(x)) * g'(x)",
            "Leibniz form: dy/dx = (dy/du)(du/dx)",
            "Outer-inner method: differentiate outer (leave inner alone), multiply by inner derivative",
            "Nested chains require applying the rule multiple times",
            "Used whenever the argument of a function is not just x",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Start with simple compositions (power of a linear function), then increase "
            "to trig of polynomial, nested compositions. Include at least one triple chain."
        ),
        "practice_problems": [
            {"problem": "Differentiate f(x) = (2x - 7)^4", "answer": "8*(2x-7)^3"},
            {"problem": "Find dy/dx for y = cos(3x^2)", "answer": "-6x*sin(3x^2)"},
            {"problem": "Differentiate g(x) = (sin(x))^3", "answer": "3*sin^2(x)*cos(x)"},
        ],
        "common_mistakes": [
            "Forgetting to multiply by the derivative of the inner function",
            "Not recognizing when the chain rule is needed (anything inside a function counts)",
            "Losing track of layers in a multi-level composition",
        ],
        "builds_toward": ["implicit-differentiation", "related-rates", "derivatives-of-inverse-trig"],
    },

    "implicit-differentiation": {
        "id": "6.2",
        "slug": "implicit-differentiation",
        "title": "Implicit Differentiation",
        "chapter": 6,
        "chapter_title": "The Chain Rule and Advanced Differentiation",
        "subject": "calc-1",
        "prerequisites": ["chain-rule", "product-rule", "quotient-rule"],
        "estimated_time": "35 min",
        "difficulty": "intermediate",
        "teaching_content": (
            "CHUNK 1: What Is Implicit Differentiation?\n"
            "Sometimes a relationship between x and y is given implicitly — that is, not "
            "solved for y. Examples: x^2 + y^2 = 25 (a circle), x*y = 1, x^3 + y^3 = 6*x*y.\n\n"
            "Implicit differentiation lets you find dy/dx without solving for y first.\n\n"
            "The method:\n"
            "1. Differentiate BOTH sides of the equation with respect to x.\n"
            "2. Every time you differentiate a term involving y, apply the chain rule: "
            "treat y as a function of x, so d/dx[y^n] = n*y^(n-1) * dy/dx.\n"
            "3. Collect all dy/dx terms on one side.\n"
            "4. Factor out dy/dx and solve for it.\n"
            "---\n"
            "CHUNK 2: Worked Examples\n\n"
            "Example 1: x^2 + y^2 = 25\n"
            "Differentiate: 2x + 2y*(dy/dx) = 0\n"
            "Solve: 2y*(dy/dx) = -2x\n"
            "dy/dx = -x/y\n\n"
            "At the point (3, 4): dy/dx = -3/4. This makes geometric sense — the tangent "
            "to a circle at (3,4) has slope -3/4.\n\n"
            "Example 2: x^3 + y^3 = 6xy\n"
            "Differentiate: 3x^2 + 3y^2*(dy/dx) = 6y + 6x*(dy/dx)\n"
            "(Note: 6xy requires the product rule: d/dx[6xy] = 6y + 6x*(dy/dx))\n"
            "Collect: 3y^2*(dy/dx) - 6x*(dy/dx) = 6y - 3x^2\n"
            "Factor: dy/dx * (3y^2 - 6x) = 6y - 3x^2\n"
            "dy/dx = (6y - 3x^2) / (3y^2 - 6x) = (2y - x^2) / (y^2 - 2x)\n\n"
            "Example 3: sin(y) + y = x^2\n"
            "Differentiate: cos(y)*(dy/dx) + dy/dx = 2x\n"
            "Factor: dy/dx * (cos(y) + 1) = 2x\n"
            "dy/dx = 2x / (cos(y) + 1)\n"
            "---\n"
            "CHUNK 3: Tips and When to Use Implicit Differentiation\n\n"
            "Use implicit differentiation when:\n"
            "- You cannot easily solve for y (e.g., x^3 + y^3 = 6xy)\n"
            "- The equation defines y as a multi-valued function (circles, ellipses)\n"
            "- You want dy/dx in terms of both x and y\n\n"
            "Key principle: y is a function of x, so d/dx[anything with y] always picks up a "
            "dy/dx factor via the chain rule.\n\n"
            "Common chain rule patterns in implicit differentiation:\n"
            "d/dx[y^2] = 2y * dy/dx\n"
            "d/dx[sin(y)] = cos(y) * dy/dx\n"
            "d/dx[e^y] = e^y * dy/dx\n"
            "d/dx[x*y] = y + x * dy/dx  (product rule + chain rule)"
        ),
        "key_concepts": [
            "Differentiate both sides with respect to x",
            "Chain rule on y terms: d/dx[f(y)] = f'(y) * dy/dx",
            "Collect, factor out, and solve for dy/dx",
            "Result is typically in terms of both x and y",
            "Useful when the equation cannot be solved explicitly for y",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Include a circle/ellipse problem, a cubic curve, and one involving trig. "
            "Ask students to find dy/dx and evaluate at a specific point."
        ),
        "practice_problems": [
            {"problem": "Find dy/dx for x^2 + y^2 = 16", "answer": "-x/y"},
            {"problem": "Find dy/dx for x*y + y^2 = 3", "answer": "-y / (x + 2y)"},
            {"problem": "Find dy/dx for x^2*y + x*y^2 = 6 at (1, 2)", "answer": "(2*1*2 + 1*2^2) cancels to dy/dx = -(2xy + y^2)/(x^2 + 2xy) = -(4+4)/(1+4) = -8/5"},
        ],
        "common_mistakes": [
            "Forgetting to apply the chain rule (missing dy/dx) when differentiating y terms",
            "Not using the product rule when x and y are multiplied together",
            "Errors in algebraic manipulation when solving for dy/dx",
        ],
        "builds_toward": ["derivatives-of-inverse-trig", "related-rates", "logarithmic-differentiation"],
    },

    "derivatives-of-inverse-trig": {
        "id": "6.3",
        "slug": "derivatives-of-inverse-trig",
        "title": "Derivatives of Inverse Trigonometric Functions",
        "chapter": 6,
        "chapter_title": "The Chain Rule and Advanced Differentiation",
        "subject": "calc-1",
        "prerequisites": ["chain-rule", "implicit-differentiation", "derivatives-of-trig"],
        "estimated_time": "30 min",
        "difficulty": "advanced",
        "teaching_content": (
            "CHUNK 1: The Key Inverse Trig Derivatives\n"
            "d/dx[arcsin(x)] = 1 / sqrt(1 - x^2)        for |x| < 1\n"
            "d/dx[arccos(x)] = -1 / sqrt(1 - x^2)       for |x| < 1\n"
            "d/dx[arctan(x)] = 1 / (1 + x^2)\n"
            "d/dx[arccot(x)] = -1 / (1 + x^2)\n"
            "d/dx[arcsec(x)] = 1 / (|x| * sqrt(x^2 - 1))   for |x| > 1\n"
            "d/dx[arccsc(x)] = -1 / (|x| * sqrt(x^2 - 1))  for |x| > 1\n\n"
            "The most commonly used are arcsin, arccos, and arctan.\n"
            "Notice: arcsin and arccos derivatives differ only by sign.\n"
            "Likewise: arctan and arccot differ only by sign.\n"
            "---\n"
            "CHUNK 2: Deriving d/dx[arcsin(x)] via Implicit Differentiation\n\n"
            "Let y = arcsin(x), so sin(y) = x where -pi/2 <= y <= pi/2.\n"
            "Differentiate both sides with respect to x:\n"
            "cos(y) * dy/dx = 1\n"
            "dy/dx = 1/cos(y)\n\n"
            "Now, since sin(y) = x, we need cos(y) in terms of x.\n"
            "Use sin^2(y) + cos^2(y) = 1:\n"
            "cos(y) = sqrt(1 - sin^2(y)) = sqrt(1 - x^2)\n"
            "(Positive root because -pi/2 <= y <= pi/2, where cosine is non-negative.)\n\n"
            "Therefore: d/dx[arcsin(x)] = 1/sqrt(1 - x^2)\n\n"
            "The same approach works for all inverse trig derivatives — set y = the inverse "
            "function, rewrite using the original trig function, and use implicit diff.\n"
            "---\n"
            "CHUNK 3: Examples with the Chain Rule\n\n"
            "With the chain rule, for any function u(x):\n"
            "d/dx[arcsin(u)] = u' / sqrt(1 - u^2)\n"
            "d/dx[arctan(u)] = u' / (1 + u^2)\n\n"
            "Example 1: y = arctan(3x)\n"
            "dy/dx = 3 / (1 + (3x)^2) = 3 / (1 + 9x^2)\n\n"
            "Example 2: y = arcsin(x^2)\n"
            "dy/dx = 2x / sqrt(1 - x^4)\n\n"
            "Example 3: y = x * arctan(x)\n"
            "Use the product rule:\n"
            "dy/dx = 1*arctan(x) + x * 1/(1+x^2)\n"
            "      = arctan(x) + x/(1+x^2)"
        ),
        "key_concepts": [
            "d/dx[arcsin x] = 1/sqrt(1-x^2) — derived via implicit differentiation",
            "d/dx[arccos x] = -1/sqrt(1-x^2) — negative of arcsin derivative",
            "d/dx[arctan x] = 1/(1+x^2)",
            "Each inverse trig derivative can be derived by implicit differentiation",
            "Chain rule extends all of these: replace x with u and multiply by u'",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Test the three main derivatives (arcsin, arccos, arctan) with chain rule "
            "applications. Include one derivation question asking for the implicit diff proof."
        ),
        "practice_problems": [
            {"problem": "Differentiate f(x) = arcsin(2x)", "answer": "2/sqrt(1-4x^2)"},
            {"problem": "Find dy/dx for y = arctan(x/3)", "answer": "(1/3)/(1+(x/3)^2) = 3/(9+x^2)"},
            {"problem": "Differentiate g(x) = arccos(sqrt(x))", "answer": "-1/(2*sqrt(x)*sqrt(1-x))"},
        ],
        "common_mistakes": [
            "Forgetting the chain rule when the argument is not plain x",
            "Mixing up which derivatives have sqrt(1-x^2) vs (1+x^2) in the denominator",
            "Getting the sign wrong on arccos (it is negative)",
        ],
        "builds_toward": ["related-rates", "lhopitals-rule"],
    },

    "derivatives-of-exponentials": {
        "id": "6.4",
        "slug": "derivatives-of-exponentials",
        "title": "Derivatives of Exponential Functions",
        "chapter": 6,
        "chapter_title": "The Chain Rule and Advanced Differentiation",
        "subject": "calc-1",
        "prerequisites": ["chain-rule", "power-rule"],
        "estimated_time": "25 min",
        "difficulty": "intermediate",
        "teaching_content": (
            "CHUNK 1: The Natural Exponential Function\n"
            "The single most important derivative formula for exponentials:\n"
            "d/dx[e^x] = e^x\n\n"
            "The function e^x is its own derivative! This is actually what makes e special — "
            "e is the unique base for which the exponential function equals its own derivative.\n\n"
            "Why? From the limit definition:\n"
            "d/dx[e^x] = lim(h->0) [e^(x+h) - e^x]/h = e^x * lim(h->0) [e^h - 1]/h\n"
            "The key limit lim(h->0) [e^h - 1]/h = 1, which is essentially the definition of e.\n\n"
            "With the chain rule:\n"
            "d/dx[e^(u(x))] = e^(u(x)) * u'(x)\n"
            "---\n"
            "CHUNK 2: General Exponential Functions\n"
            "For any positive base a (a != 1):\n"
            "d/dx[a^x] = a^x * ln(a)\n\n"
            "This follows from rewriting a^x = e^(x*ln(a)) and applying the chain rule:\n"
            "d/dx[e^(x*ln(a))] = e^(x*ln(a)) * ln(a) = a^x * ln(a)\n\n"
            "Notice: when a = e, ln(e) = 1, and we recover d/dx[e^x] = e^x.\n\n"
            "With the chain rule:\n"
            "d/dx[a^(u(x))] = a^(u(x)) * ln(a) * u'(x)\n"
            "---\n"
            "CHUNK 3: Worked Examples\n\n"
            "Example 1: y = e^(3x)\n"
            "dy/dx = e^(3x) * 3 = 3e^(3x)\n\n"
            "Example 2: y = 2^x\n"
            "dy/dx = 2^x * ln(2)\n"
            "(ln(2) is approximately 0.693)\n\n"
            "Example 3: y = e^(x^2 + 1)\n"
            "dy/dx = e^(x^2 + 1) * 2x = 2x * e^(x^2 + 1)\n\n"
            "Example with product rule: y = x^3 * e^x\n"
            "dy/dx = 3x^2 * e^x + x^3 * e^x = e^x * (3x^2 + x^3) = x^2 * e^x * (3 + x)\n\n"
            "Key insight: e^(anything) never equals zero, so exponential functions are always "
            "positive. This becomes important in optimization and differential equations."
        ),
        "key_concepts": [
            "d/dx[e^x] = e^x — the exponential is its own derivative",
            "d/dx[a^x] = a^x * ln(a) for any positive base a",
            "Chain rule: d/dx[e^u] = e^u * u'",
            "a^x can be rewritten as e^(x*ln(a))",
            "e^x is always positive — it never equals zero",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Include basic e^(kx) problems, a general base a^x problem, and a product "
            "rule combination with e^x. Ask why e is the special base."
        ),
        "practice_problems": [
            {"problem": "Differentiate f(x) = e^(5x)", "answer": "5e^(5x)"},
            {"problem": "Find dy/dx for y = 3^(2x)", "answer": "2 * 3^(2x) * ln(3)"},
            {"problem": "Differentiate g(x) = x * e^(-x)", "answer": "e^(-x) - x*e^(-x) = e^(-x)*(1-x)"},
        ],
        "common_mistakes": [
            "Writing d/dx[e^x] = x*e^(x-1) (confusing with the power rule — e^x is NOT a power function)",
            "Forgetting the ln(a) factor when differentiating a^x",
            "Forgetting the chain rule: d/dx[e^(3x)] = 3e^(3x), not just e^(3x)",
        ],
        "builds_toward": ["derivatives-of-logarithms", "logarithmic-differentiation", "lhopitals-rule"],
    },

    "derivatives-of-logarithms": {
        "id": "6.5",
        "slug": "derivatives-of-logarithms",
        "title": "Derivatives of Logarithmic Functions",
        "chapter": 6,
        "chapter_title": "The Chain Rule and Advanced Differentiation",
        "subject": "calc-1",
        "prerequisites": ["chain-rule", "derivatives-of-exponentials", "quotient-rule"],
        "estimated_time": "25 min",
        "difficulty": "intermediate",
        "teaching_content": (
            "CHUNK 1: Derivative of the Natural Logarithm\n"
            "d/dx[ln(x)] = 1/x    for x > 0\n\n"
            "This can be derived from the fact that ln(x) and e^x are inverses.\n"
            "Let y = ln(x), so e^y = x. Differentiate implicitly:\n"
            "e^y * dy/dx = 1\n"
            "dy/dx = 1/e^y = 1/x\n\n"
            "With the chain rule:\n"
            "d/dx[ln(u)] = u'/u = (1/u) * u'\n\n"
            "A useful extended form: d/dx[ln|x|] = 1/x for all x != 0.\n"
            "This is important because we often encounter ln|x| in integration.\n"
            "---\n"
            "CHUNK 2: General Logarithmic Functions\n"
            "For a logarithm with base a (a > 0, a != 1):\n"
            "d/dx[log_a(x)] = 1/(x * ln(a))\n\n"
            "This follows from the change of base formula:\n"
            "log_a(x) = ln(x)/ln(a)\n"
            "So d/dx[log_a(x)] = (1/ln(a)) * d/dx[ln(x)] = 1/(x * ln(a))\n\n"
            "With the chain rule:\n"
            "d/dx[log_a(u)] = u' / (u * ln(a))\n\n"
            "When a = e: ln(e) = 1, and we recover d/dx[ln x] = 1/x.\n"
            "When a = 10: d/dx[log_10(x)] = 1/(x * ln(10)) ≈ 1/(2.303 * x)\n"
            "---\n"
            "CHUNK 3: Worked Examples\n\n"
            "Example 1: y = ln(3x + 1)\n"
            "dy/dx = 3/(3x + 1)\n"
            "(Inner function is 3x + 1, its derivative is 3.)\n\n"
            "Example 2: y = ln(x^2 + 1)\n"
            "dy/dx = 2x/(x^2 + 1)\n\n"
            "Example 3: y = log_2(x)\n"
            "dy/dx = 1/(x * ln(2))\n\n"
            "Useful pattern — logarithmic properties simplify before differentiating:\n"
            "y = ln(x^3 * sin(x))\n"
            "Rewrite first: y = 3*ln(x) + ln(sin(x))\n"
            "dy/dx = 3/x + cos(x)/sin(x) = 3/x + cot(x)\n\n"
            "This technique — expanding with log properties before differentiating — is often "
            "much easier than blindly applying the chain rule to the original expression."
        ),
        "key_concepts": [
            "d/dx[ln x] = 1/x for x > 0",
            "d/dx[log_a(x)] = 1/(x * ln(a))",
            "Chain rule form: d/dx[ln(u)] = u'/u",
            "Expand logarithms using log properties before differentiating",
            "d/dx[ln|x|] = 1/x for all x != 0",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Include ln with chain rule, a general base log problem, and a problem "
            "where expanding the log first simplifies the work."
        ),
        "practice_problems": [
            {"problem": "Differentiate f(x) = ln(5x)", "answer": "1/x (since ln(5x) = ln(5) + ln(x))"},
            {"problem": "Find dy/dx for y = ln(x^2 - 4)", "answer": "2x/(x^2 - 4)"},
            {"problem": "Differentiate g(x) = log_3(x^2)", "answer": "2/(x * ln(3))"},
        ],
        "common_mistakes": [
            "Writing d/dx[ln x] = 1/x * 0 = 0 (confusing the constant ln(a) with a variable)",
            "Forgetting to apply the chain rule: d/dx[ln(2x)] = 1/x, not 1/(2x)",
            "Not simplifying with log properties first, leading to unnecessarily complex derivatives",
        ],
        "builds_toward": ["logarithmic-differentiation", "lhopitals-rule"],
    },

    "logarithmic-differentiation": {
        "id": "6.6",
        "slug": "logarithmic-differentiation",
        "title": "Logarithmic Differentiation",
        "chapter": 6,
        "chapter_title": "The Chain Rule and Advanced Differentiation",
        "subject": "calc-1",
        "prerequisites": ["derivatives-of-logarithms", "implicit-differentiation", "chain-rule"],
        "estimated_time": "30 min",
        "difficulty": "advanced",
        "teaching_content": (
            "CHUNK 1: When and Why to Use Logarithmic Differentiation\n"
            "Logarithmic differentiation is a technique where you take the natural log of "
            "both sides of y = f(x), then differentiate implicitly. It is especially useful for:\n\n"
            "1. Functions of the form y = [f(x)]^[g(x)] — variable base AND variable exponent "
            "(the power rule and exponential rule both fail here).\n"
            "2. Complicated products/quotients with many factors — logs turn products into sums.\n\n"
            "The method:\n"
            "Step 1: Write y = f(x)\n"
            "Step 2: Take ln of both sides: ln(y) = ln(f(x))\n"
            "Step 3: Simplify the right side using log properties\n"
            "Step 4: Differentiate both sides implicitly (left side becomes (1/y)*dy/dx)\n"
            "Step 5: Solve for dy/dx and substitute back y = f(x)\n"
            "---\n"
            "CHUNK 2: The Classic Case — x^x and Similar\n\n"
            "Example 1: y = x^x  (x > 0)\n"
            "ln(y) = x * ln(x)\n"
            "Differentiate: (1/y) * dy/dx = 1 * ln(x) + x * (1/x) = ln(x) + 1\n"
            "dy/dx = y * (ln(x) + 1) = x^x * (ln(x) + 1)\n\n"
            "Example 2: y = x^(sin(x))  (x > 0)\n"
            "ln(y) = sin(x) * ln(x)\n"
            "Differentiate: (1/y) * dy/dx = cos(x)*ln(x) + sin(x)/x\n"
            "dy/dx = x^(sin(x)) * [cos(x)*ln(x) + sin(x)/x]\n\n"
            "These problems CANNOT be solved by the power rule (exponent must be constant) "
            "or by the exponential rule (base must be constant). Logarithmic differentiation "
            "is the only approach.\n"
            "---\n"
            "CHUNK 3: Simplifying Messy Products and Quotients\n\n"
            "Example 3: y = [(x+1)^3 * (x-2)^5] / [(x+3)^7 * sqrt(x-1)]\n\n"
            "Taking ln of both sides:\n"
            "ln(y) = 3*ln(x+1) + 5*ln(x-2) - 7*ln(x+3) - (1/2)*ln(x-1)\n\n"
            "Differentiate:\n"
            "(1/y)*dy/dx = 3/(x+1) + 5/(x-2) - 7/(x+3) - 1/(2*(x-1))\n\n"
            "dy/dx = y * [3/(x+1) + 5/(x-2) - 7/(x+3) - 1/(2*(x-1))]\n\n"
            "Substitute back the original expression for y. Without logarithmic differentiation, "
            "this would require repeated product and quotient rules — far messier.\n\n"
            "Rule of thumb: if a function has more than two multiplicative factors, or has a "
            "variable in both the base and exponent, logarithmic differentiation is the way to go."
        ),
        "key_concepts": [
            "Take ln of both sides, then differentiate implicitly",
            "Left side always becomes (1/y) * dy/dx",
            "Required for y = f(x)^g(x) type (variable base AND exponent)",
            "Simplifies products of many factors via log properties",
            "Must substitute y = original expression at the end",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Include a variable-exponent problem like x^x or x^(1/x), and a messy "
            "multi-factor product. Ensure students show all steps of the method."
        ),
        "practice_problems": [
            {"problem": "Find dy/dx for y = x^x", "answer": "x^x * (ln(x) + 1)"},
            {"problem": "Differentiate y = (2x)^(x^2)", "answer": "(2x)^(x^2) * [2x*ln(2x) + x]"},
            {"problem": "Use logarithmic differentiation: y = (x^2+1)^3 * (x-1)^4", "answer": "y * [6x/(x^2+1) + 4/(x-1)]"},
        ],
        "common_mistakes": [
            "Trying to use the power rule on x^x (the exponent is not constant!)",
            "Forgetting to multiply by y at the end when solving for dy/dx",
            "Not substituting the original function back in for y in the final answer",
        ],
        "builds_toward": ["related-rates", "lhopitals-rule"],
    },

    # =========================================================================
    # CHAPTER 7 — Applications of Derivatives, Part 1
    # =========================================================================

    "related-rates": {
        "id": "7.1",
        "slug": "related-rates",
        "title": "Related Rates",
        "chapter": 7,
        "chapter_title": "Applications of Derivatives — Part 1",
        "subject": "calc-1",
        "prerequisites": ["chain-rule", "implicit-differentiation"],
        "estimated_time": "45 min",
        "difficulty": "advanced",
        "teaching_content": (
            "CHUNK 1: What Are Related Rates?\n"
            "In a related rates problem, two or more quantities are changing with respect to "
            "time (t), and they are connected by an equation. You know the rate of change of "
            "some quantities and need to find the rate of change of another.\n\n"
            "The 5-Step Method:\n"
            "1. Draw a picture and label all changing quantities with variables.\n"
            "2. Write an equation relating the variables.\n"
            "3. Differentiate both sides with respect to t (using the chain rule — every "
            "   variable is a function of t).\n"
            "4. Substitute all KNOWN values (do this AFTER differentiating, not before!).\n"
            "5. Solve for the unknown rate.\n\n"
            "Critical rule: NEVER substitute specific values for changing quantities until "
            "AFTER you differentiate. Substituting before differentiating treats a variable "
            "as a constant and destroys the derivative.\n"
            "---\n"
            "CHUNK 2: Classic Example — Expanding Balloon\n\n"
            "A spherical balloon is being inflated so its volume increases at 100 cm^3/s. "
            "How fast is the radius increasing when the radius is 10 cm?\n\n"
            "Step 1: Variables — V = volume, r = radius, both functions of t.\n"
            "Step 2: V = (4/3)*pi*r^3\n"
            "Step 3: Differentiate: dV/dt = 4*pi*r^2 * dr/dt\n"
            "Step 4: Given dV/dt = 100, r = 10:\n"
            "  100 = 4*pi*(10)^2 * dr/dt = 400*pi * dr/dt\n"
            "Step 5: dr/dt = 100/(400*pi) = 1/(4*pi) ≈ 0.0796 cm/s\n"
            "---\n"
            "CHUNK 3: More Classic Problems\n\n"
            "Example 2 — Sliding Ladder:\n"
            "A 10-foot ladder leans against a wall. The bottom slides away at 2 ft/s. "
            "How fast is the top sliding down when the bottom is 6 feet from the wall?\n\n"
            "Equation: x^2 + y^2 = 100  (Pythagorean theorem, ladder = hypotenuse)\n"
            "Differentiate: 2x*(dx/dt) + 2y*(dy/dt) = 0\n"
            "When x = 6: y = sqrt(100-36) = 8. Given dx/dt = 2:\n"
            "2(6)(2) + 2(8)(dy/dt) = 0\n"
            "24 + 16*(dy/dt) = 0\n"
            "dy/dt = -24/16 = -3/2 ft/s\n"
            "The top slides DOWN at 3/2 ft/s (negative because y is decreasing).\n\n"
            "Example 3 — Filling Cone:\n"
            "A conical tank (height 10 m, radius 5 m at top) is filled at 3 m^3/min. "
            "How fast is the water level rising when the water is 4 m deep?\n\n"
            "The cone's similar triangles give: r/h = 5/10, so r = h/2.\n"
            "V = (1/3)*pi*r^2*h = (1/3)*pi*(h/2)^2*h = pi*h^3/12\n"
            "dV/dt = (pi/4)*h^2 * dh/dt\n"
            "3 = (pi/4)*(16) * dh/dt\n"
            "dh/dt = 3/(4*pi) ≈ 0.239 m/min"
        ),
        "key_concepts": [
            "Related rates connect rates of change of linked quantities via differentiation",
            "5-step method: draw, write equation, differentiate wrt t, substitute, solve",
            "NEVER substitute values before differentiating",
            "Every variable is implicitly a function of t — chain rule applies to each",
            "Negative rates mean the quantity is decreasing",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Include one problem from each classic type: expanding/contracting shape, "
            "sliding ladder, and filling container. Emphasize the 5-step method."
        ),
        "practice_problems": [
            {"problem": "A circle's area grows at 6 cm^2/s. How fast is the radius growing when r = 3 cm?", "answer": "dr/dt = 6/(2*pi*3) = 1/pi cm/s"},
            {"problem": "A 13-ft ladder: bottom moves out at 1 ft/s. How fast does the top slide down when bottom is 5 ft out?", "answer": "y = 12, dy/dt = -5/12 ft/s"},
            {"problem": "Spherical snowball melts so volume decreases at 2 cm^3/min. How fast is radius decreasing when r = 5?", "answer": "dr/dt = -2/(4*pi*25) = -1/(50*pi) cm/min"},
        ],
        "common_mistakes": [
            "Substituting specific values BEFORE differentiating (the #1 error)",
            "Forgetting the chain rule — writing d/dt[r^2] = 2r instead of 2r*dr/dt",
            "Not using similar triangles or other geometric relationships to eliminate a variable before differentiating",
        ],
        "builds_toward": ["linear-approximation", "newtons-method"],
    },

    "linear-approximation": {
        "id": "7.2",
        "slug": "linear-approximation",
        "title": "Linear Approximation and Differentials",
        "chapter": 7,
        "chapter_title": "Applications of Derivatives — Part 1",
        "subject": "calc-1",
        "prerequisites": ["chain-rule", "derivatives-of-trig", "derivatives-of-exponentials"],
        "estimated_time": "30 min",
        "difficulty": "intermediate",
        "teaching_content": (
            "CHUNK 1: Linear Approximation (Linearization)\n"
            "The tangent line at a point provides the best linear approximation to a function "
            "near that point.\n\n"
            "The linearization of f at x = a is:\n"
            "L(x) = f(a) + f'(a) * (x - a)\n\n"
            "For x close to a: f(x) ≈ L(x) = f(a) + f'(a) * (x - a)\n\n"
            "This is the foundation of many numerical methods and a powerful estimation tool.\n\n"
            "Why does this work? The tangent line is the limit of secant lines and matches "
            "the function's value and slope at x = a. Near a, the function barely deviates "
            "from its tangent line.\n"
            "---\n"
            "CHUNK 2: Worked Examples\n\n"
            "Example 1: Approximate sqrt(4.1) without a calculator.\n"
            "Let f(x) = sqrt(x), a = 4 (nearest easy value).\n"
            "f(4) = 2, f'(x) = 1/(2*sqrt(x)), f'(4) = 1/4.\n"
            "L(x) = 2 + (1/4)*(x - 4)\n"
            "L(4.1) = 2 + (1/4)*(0.1) = 2 + 0.025 = 2.025\n"
            "Actual value: sqrt(4.1) ≈ 2.02485... Very close!\n\n"
            "Example 2: Approximate sin(0.1).\n"
            "f(x) = sin(x), a = 0.\n"
            "f(0) = 0, f'(0) = cos(0) = 1.\n"
            "L(x) = 0 + 1*(x - 0) = x\n"
            "So sin(0.1) ≈ 0.1. (Actual: 0.09983... — excellent for small angles!)\n\n"
            "Example 3: Approximate e^(0.05).\n"
            "f(x) = e^x, a = 0.\n"
            "f(0) = 1, f'(0) = 1.\n"
            "L(x) = 1 + x\n"
            "e^(0.05) ≈ 1.05. (Actual: 1.05127...)\n"
            "---\n"
            "CHUNK 3: Differentials\n\n"
            "Differentials provide another way to express the same idea.\n"
            "If y = f(x), define:\n"
            "  dx = delta x (a small change in x — you choose this)\n"
            "  dy = f'(x) * dx (the corresponding approximate change in y)\n\n"
            "dy approximates the actual change delta y = f(x + dx) - f(x).\n\n"
            "Example: y = x^3, x = 2, dx = 0.01.\n"
            "dy = 3x^2 * dx = 3(4)(0.01) = 0.12\n"
            "Actual: 2.01^3 - 8 = 8.120601 - 8 = 0.120601\n"
            "dy = 0.12 is very close to the actual change 0.1206.\n\n"
            "Differentials are used in error estimation: if a measurement has error dx, "
            "the propagated error in f(x) is approximately |dy| = |f'(x)| * |dx|."
        ),
        "key_concepts": [
            "L(x) = f(a) + f'(a)(x - a) — linearization at x = a",
            "Works well when x is close to a",
            "Common linearizations: sqrt(1+x) ≈ 1 + x/2, sin(x) ≈ x, e^x ≈ 1+x near 0",
            "Differentials: dy = f'(x) * dx approximates the actual change in f",
            "Used for error propagation and numerical estimation",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Include approximation problems (estimate sqrt, cube root, or trig values), "
            "a differential computation, and an error estimation problem."
        ),
        "practice_problems": [
            {"problem": "Use linear approximation to estimate sqrt(9.1)", "answer": "L(9.1) = 3 + (1/6)(0.1) = 3.01667 (f(x)=sqrt(x), a=9)"},
            {"problem": "Approximate cos(0.02) using linearization at a=0", "answer": "cos(0.02) ≈ 1 (since L(x) = 1 - 0*x = 1 for small x; more precisely 1 - 0*0.02 = 1)"},
            {"problem": "If y = x^4 and x = 1, dx = 0.02, find dy", "answer": "dy = 4x^3 * dx = 4(1)(0.02) = 0.08"},
        ],
        "common_mistakes": [
            "Choosing a base point a that is not close to the value being approximated",
            "Confusing dy (the differential, an approximation) with delta y (the exact change)",
            "Forgetting that the approximation degrades as x moves farther from a",
        ],
        "builds_toward": ["newtons-method", "mean-value-theorem"],
    },

    "mean-value-theorem": {
        "id": "7.3",
        "slug": "mean-value-theorem",
        "title": "The Mean Value Theorem",
        "chapter": 7,
        "chapter_title": "Applications of Derivatives — Part 1",
        "subject": "calc-1",
        "prerequisites": ["higher-order-derivatives", "chain-rule"],
        "estimated_time": "30 min",
        "difficulty": "intermediate",
        "teaching_content": (
            "CHUNK 1: Rolle's Theorem\n"
            "Before the Mean Value Theorem (MVT), we state a special case called Rolle's Theorem.\n\n"
            "Rolle's Theorem: If f is continuous on [a, b], differentiable on (a, b), and "
            "f(a) = f(b), then there exists at least one c in (a, b) such that f'(c) = 0.\n\n"
            "Geometric meaning: if a continuous, smooth curve starts and ends at the same height, "
            "it must have a horizontal tangent somewhere in between. Think of a hill — to go up "
            "and come back down, there must be a peak (or valley) where the slope is zero.\n\n"
            "Example: f(x) = x^2 - 4x on [0, 4].\n"
            "f(0) = 0, f(4) = 16-16 = 0. So f(0) = f(4), Rolle's applies.\n"
            "f'(x) = 2x - 4 = 0 gives x = 2. Indeed c = 2 is in (0, 4).\n"
            "---\n"
            "CHUNK 2: The Mean Value Theorem\n\n"
            "The MVT generalizes Rolle's theorem by removing the requirement f(a) = f(b).\n\n"
            "Mean Value Theorem: If f is continuous on [a, b] and differentiable on (a, b), "
            "then there exists at least one c in (a, b) such that:\n"
            "f'(c) = [f(b) - f(a)] / (b - a)\n\n"
            "Geometric meaning: the instantaneous rate of change (slope of tangent) at some "
            "point c equals the average rate of change (slope of secant) over the interval.\n\n"
            "Analogy: if you drive 150 miles in 3 hours (average 50 mph), then at some moment "
            "during the trip your speedometer must have read exactly 50 mph.\n\n"
            "Example: f(x) = x^3 on [1, 3].\n"
            "Average rate: [f(3) - f(1)]/(3-1) = (27-1)/2 = 13.\n"
            "f'(x) = 3x^2. Set 3c^2 = 13: c = sqrt(13/3) ≈ 2.08.\n"
            "This c is in (1, 3), confirming the MVT.\n"
            "---\n"
            "CHUNK 3: Consequences of the MVT\n\n"
            "The MVT has several powerful consequences:\n\n"
            "1. If f'(x) = 0 for all x in an interval, then f is constant on that interval.\n"
            "   (Proof: for any two points, MVT says f(b)-f(a) = f'(c)*(b-a) = 0.)\n\n"
            "2. If f'(x) > 0 for all x in an interval, then f is increasing on that interval.\n"
            "   If f'(x) < 0, then f is decreasing.\n\n"
            "3. If f'(x) = g'(x) for all x, then f(x) = g(x) + C for some constant C.\n"
            "   (Two functions with the same derivative differ by a constant.)\n\n"
            "These consequences form the theoretical backbone for finding extrema (max/min), "
            "analyzing function behavior, and eventually for the Fundamental Theorem of Calculus.\n\n"
            "Example: Show that sin(x) <= x for all x >= 0.\n"
            "Let f(x) = x - sin(x). Then f(0) = 0 and f'(x) = 1 - cos(x) >= 0 for all x.\n"
            "By the MVT consequence, f is non-decreasing, so f(x) >= f(0) = 0, meaning x >= sin(x)."
        ),
        "key_concepts": [
            "Rolle's Theorem: f(a) = f(b) implies f'(c) = 0 for some c in (a,b)",
            "MVT: f'(c) = [f(b)-f(a)]/(b-a) for some c in (a,b)",
            "Requires continuity on [a,b] and differentiability on (a,b)",
            "f' = 0 everywhere implies f is constant",
            "f' > 0 implies f is increasing; f' < 0 implies f is decreasing",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Include a verification problem (find the c), a conceptual question about "
            "what the MVT says, and an application using its consequences (increasing/decreasing)."
        ),
        "practice_problems": [
            {"problem": "Verify the MVT for f(x) = x^2 on [1, 3] by finding c", "answer": "Average rate = (9-1)/2 = 4. f'(c)=2c=4, so c=2, which is in (1,3)."},
            {"problem": "Does Rolle's theorem apply to f(x) = |x| on [-1, 1]? Why or why not?", "answer": "f(-1) = f(1) = 1, continuous on [-1,1], BUT not differentiable at x=0. Rolle's does not apply."},
            {"problem": "If f'(x) > 0 on (2, 5) and f(2) = 3, can f(5) = 1?", "answer": "No. f' > 0 means f is increasing, so f(5) > f(2) = 3."},
        ],
        "common_mistakes": [
            "Forgetting to check both conditions: continuity on [a,b] AND differentiability on (a,b)",
            "Confusing Rolle's theorem with MVT (Rolle's is the special case f(a)=f(b))",
            "Trying to apply MVT to a function with a discontinuity or corner in the interval",
        ],
        "builds_toward": ["lhopitals-rule"],
    },

    "lhopitals-rule": {
        "id": "7.4",
        "slug": "lhopitals-rule",
        "title": "L'Hopital's Rule",
        "chapter": 7,
        "chapter_title": "Applications of Derivatives — Part 1",
        "subject": "calc-1",
        "prerequisites": ["derivatives-of-exponentials", "derivatives-of-logarithms", "quotient-rule"],
        "estimated_time": "35 min",
        "difficulty": "advanced",
        "teaching_content": (
            "CHUNK 1: L'Hopital's Rule for 0/0 and inf/inf\n"
            "When evaluating a limit and you get an indeterminate form 0/0 or inf/inf, "
            "L'Hopital's Rule says:\n\n"
            "lim(x->a) f(x)/g(x) = lim(x->a) f'(x)/g'(x)\n\n"
            "PROVIDED the right-hand limit exists (or is +/- infinity).\n\n"
            "Important: you differentiate the numerator and denominator SEPARATELY — this is "
            "NOT the quotient rule! You are replacing f/g with f'/g', not computing d/dx[f/g].\n\n"
            "Conditions:\n"
            "1. The limit must be an indeterminate form (0/0 or inf/inf).\n"
            "2. f and g must be differentiable near a.\n"
            "3. g'(x) != 0 near a.\n"
            "4. The limit of f'/g' must exist (or be +/- infinity).\n\n"
            "If f'/g' is still 0/0 or inf/inf, you can apply the rule again.\n"
            "---\n"
            "CHUNK 2: Worked Examples — Direct Application\n\n"
            "Example 1: lim(x->0) sin(x)/x\n"
            "This is 0/0. Apply L'Hopital:\n"
            "= lim(x->0) cos(x)/1 = 1\n"
            "(We already knew this, but L'Hopital confirms it easily.)\n\n"
            "Example 2: lim(x->inf) x^2 / e^x\n"
            "This is inf/inf. Apply L'Hopital:\n"
            "= lim(x->inf) 2x / e^x  (still inf/inf, apply again)\n"
            "= lim(x->inf) 2 / e^x = 0\n"
            "Exponentials dominate polynomials!\n\n"
            "Example 3: lim(x->0) (e^x - 1)/x\n"
            "This is 0/0.\n"
            "= lim(x->0) e^x / 1 = 1\n"
            "---\n"
            "CHUNK 3: Other Indeterminate Forms\n\n"
            "L'Hopital's directly handles 0/0 and inf/inf. But other indeterminate forms can "
            "be rewritten to fit:\n\n"
            "0 * inf: Rewrite f*g as f/(1/g) to get 0/0 or inf/inf.\n"
            "inf - inf: Combine fractions to get a single fraction.\n"
            "0^0, 1^inf, inf^0: Take the natural log. If y = f^g, then ln(y) = g*ln(f). "
            "Evaluate lim[g*ln(f)] (which is typically 0*inf, convert to 0/0 or inf/inf). "
            "Then y = e^(that limit).\n\n"
            "Example: lim(x->0+) x*ln(x)  [form: 0 * (-inf)]\n"
            "Rewrite: lim(x->0+) ln(x) / (1/x)  [form: -inf/inf]\n"
            "L'Hopital: = lim(x->0+) (1/x) / (-1/x^2) = lim(x->0+) (-x) = 0\n\n"
            "Example: lim(x->0+) x^x  [form: 0^0]\n"
            "Let y = x^x. Then ln(y) = x*ln(x). We just showed this -> 0.\n"
            "So y -> e^0 = 1."
        ),
        "key_concepts": [
            "L'Hopital: lim f/g = lim f'/g' when the form is 0/0 or inf/inf",
            "Differentiate numerator and denominator SEPARATELY (not the quotient rule)",
            "Can apply repeatedly if result is still indeterminate",
            "Other forms (0*inf, inf-inf, 0^0, 1^inf, inf^0) must be converted first",
            "Must verify the form is actually indeterminate before applying",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Include 0/0 and inf/inf problems, one requiring multiple applications, and "
            "one involving conversion from another indeterminate form (e.g., 0*inf)."
        ),
        "practice_problems": [
            {"problem": "Evaluate lim(x->0) (x - sin(x))/x^3", "answer": "Apply 3 times: lim (1-cos x)/(3x^2) -> lim sin x/(6x) -> lim cos x/6 = 1/6"},
            {"problem": "Evaluate lim(x->inf) ln(x)/x", "answer": "inf/inf, so lim (1/x)/1 = 0"},
            {"problem": "Evaluate lim(x->0+) x^(1/x)", "answer": "Form inf^0 does not arise; actually x->0+ gives 0^inf = 0. (Alternatively, ln(y)=(1/x)ln(x)->-inf, so y->0.)"},
        ],
        "common_mistakes": [
            "Applying L'Hopital when the form is NOT indeterminate (e.g., 1/0 is not 0/0)",
            "Using the quotient rule instead of differentiating top and bottom separately",
            "Applying the rule to a limit that does not meet the conditions",
        ],
        "builds_toward": ["newtons-method"],
    },

    "newtons-method": {
        "id": "7.5",
        "slug": "newtons-method",
        "title": "Newton's Method",
        "chapter": 7,
        "chapter_title": "Applications of Derivatives — Part 1",
        "subject": "calc-1",
        "prerequisites": ["linear-approximation", "chain-rule"],
        "estimated_time": "30 min",
        "difficulty": "intermediate",
        "teaching_content": (
            "CHUNK 1: The Idea Behind Newton's Method\n"
            "Newton's method is an iterative algorithm for finding roots (zeros) of a function "
            "f(x) = 0. It uses linear approximation repeatedly to home in on a root.\n\n"
            "The iteration formula:\n"
            "x_{n+1} = x_n - f(x_n) / f'(x_n)\n\n"
            "How it works:\n"
            "1. Start with an initial guess x_0 near a root.\n"
            "2. Draw the tangent line to f at x_0.\n"
            "3. The tangent line crosses the x-axis at x_1 — this is your next approximation.\n"
            "4. Repeat: draw tangent at x_1 to find x_2, and so on.\n\n"
            "Each iteration typically doubles the number of correct decimal places (quadratic "
            "convergence), making this method extremely efficient.\n"
            "---\n"
            "CHUNK 2: Finding sqrt(2) — A Classic Example\n\n"
            "To find sqrt(2), solve f(x) = x^2 - 2 = 0.\n"
            "f'(x) = 2x\n"
            "x_{n+1} = x_n - (x_n^2 - 2)/(2*x_n)\n\n"
            "Start with x_0 = 1 (a reasonable guess):\n\n"
            "x_1 = 1 - (1 - 2)/(2) = 1 - (-1/2) = 1.5\n"
            "x_2 = 1.5 - (2.25 - 2)/(3) = 1.5 - 0.25/3 = 1.5 - 0.08333 = 1.41667\n"
            "x_3 = 1.41667 - (1.41667^2 - 2)/(2*1.41667)\n"
            "    = 1.41667 - (2.00694 - 2)/2.83334\n"
            "    = 1.41667 - 0.00245 = 1.41422\n\n"
            "After just 3 iterations, we have sqrt(2) ≈ 1.41422, which is correct to 5 "
            "significant digits! (Actual: 1.41421356...)\n"
            "---\n"
            "CHUNK 3: When Newton's Method Fails and Practical Tips\n\n"
            "Newton's method can fail or behave badly when:\n"
            "1. f'(x_n) = 0 — the tangent is horizontal, formula divides by zero.\n"
            "2. The initial guess is too far from the root.\n"
            "3. The function has inflection points near the root that send iterates far away.\n"
            "4. The method cycles between values without converging.\n\n"
            "Example where care is needed: f(x) = x^(1/3)\n"
            "f'(x) = (1/3)*x^(-2/3). Newton iteration:\n"
            "x_{n+1} = x_n - x_n^(1/3) / ((1/3)*x_n^(-2/3)) = x_n - 3*x_n = -2*x_n\n"
            "The iterates diverge! Each step doubles and flips the sign.\n\n"
            "Practical tips:\n"
            "- Choose x_0 close to where you expect a root (use a graph or sign changes).\n"
            "- Stop when |x_{n+1} - x_n| < your desired tolerance.\n"
            "- If it does not converge in ~10 iterations, try a different starting point.\n\n"
            "Example 2: Find a root of f(x) = cos(x) - x (solve cos(x) = x).\n"
            "f'(x) = -sin(x) - 1. Start with x_0 = 0.5:\n"
            "x_1 = 0.5 - (cos(0.5) - 0.5)/(-sin(0.5) - 1)\n"
            "     = 0.5 - (0.8776 - 0.5)/(-0.4794 - 1)\n"
            "     = 0.5 - 0.3776/(-1.4794) = 0.5 + 0.2552 = 0.7552\n"
            "x_2 ≈ 0.7391 (the root is 0.73909... — already close after 2 iterations)"
        ),
        "key_concepts": [
            "x_{n+1} = x_n - f(x_n)/f'(x_n) — the Newton iteration",
            "Uses tangent lines to progressively approximate a root",
            "Quadratic convergence: correct digits roughly double each step",
            "Requires a good initial guess near the root",
            "Can fail if f'(x_n) = 0 or the guess is too far from the root",
        ],
        "available_images": [],
        "quiz_guidelines": (
            "Ask students to perform 2-3 iterations by hand for a polynomial root, "
            "include the sqrt(2) example, and ask about failure conditions."
        ),
        "practice_problems": [
            {"problem": "Use Newton's method with x_0 = 2 to approximate sqrt(5) (solve x^2 - 5 = 0). Do 2 iterations.", "answer": "x_1 = 2 - (4-5)/(4) = 2.25. x_2 = 2.25 - (5.0625-5)/(4.5) = 2.25 - 0.01389 = 2.23611"},
            {"problem": "Find x_1 using Newton's method for f(x) = x^3 - 2x - 5 with x_0 = 2", "answer": "f(2)=-1, f'(2)=10. x_1 = 2 - (-1)/10 = 2.1"},
            {"problem": "Why does Newton's method fail for f(x) = x^(1/3) starting from any x_0 != 0?", "answer": "The iteration gives x_{n+1} = -2*x_n, which diverges (oscillates with growing magnitude)"},
        ],
        "common_mistakes": [
            "Computing f'(x_n) wrong — be careful with the derivative calculation",
            "Forgetting the minus sign in x_{n+1} = x_n - f(x_n)/f'(x_n)",
            "Not checking whether the method is converging (always compare successive iterates)",
        ],
        "builds_toward": [],
    },

}
