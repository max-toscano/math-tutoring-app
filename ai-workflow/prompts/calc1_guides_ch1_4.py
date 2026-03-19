"""
calc1_guides_ch1_4.py
Calculus 1 topic guides: Chapters 1-4
  Ch 1: Functions and Their Properties (precalculus review)
  Ch 2: Limits — The Foundation of Calculus
  Ch 3: Continuity
  Ch 4: Defining the Derivative
"""

CALC1_GUIDES_CH1_4: dict[str, dict] = {

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 1: Functions and Their Properties
    # ══════════════════════════════════════════════════════════════════════════

    "functions-and-notation": {
        "id": "1.1",
        "slug": "functions-and-notation",
        "title": "Functions and Function Notation",
        "chapter": "functions-review",
        "chapter_title": "Functions and Their Properties",
        "subject": "calc-1",
        "prerequisites": [],
        "estimated_time": "10-15 minutes",
        "difficulty": "Easy",

        "teaching_content": (
            "CHUNK 1 — What is a function?\n\n"
            "A function is a rule that assigns EXACTLY ONE output to each input. "
            "Think of it like a machine: you put a number in, and exactly one number comes out.\n\n"
            "We write f(x) = 2x + 3. Here:\n"
            "- f is the name of the function\n"
            "- x is the input (also called the independent variable)\n"
            "- 2x + 3 is the rule that tells us what to do with x\n"
            "- f(x) is the output (also called the dependent variable)\n\n"
            "Example: If f(x) = 2x + 3, then f(4) = 2(4) + 3 = 8 + 3 = 11.\n\n"
            "---\n\n"
            "CHUNK 2 — Evaluating functions:\n\n"
            "To evaluate a function means to plug a value in for x and compute the result.\n\n"
            "Example 1: f(x) = x^2 - 5x + 6. Find f(3).\n"
            "f(3) = (3)^2 - 5(3) + 6 = 9 - 15 + 6 = 0\n\n"
            "Example 2: g(t) = sqrt(t + 4). Find g(5).\n"
            "g(5) = sqrt(5 + 4) = sqrt(9) = 3\n\n"
            "Example 3: Evaluate f(a + h) where f(x) = x^2.\n"
            "f(a + h) = (a + h)^2 = a^2 + 2ah + h^2\n"
            "This is VERY important — you'll see f(a + h) constantly in calculus when we define derivatives.\n\n"
            "---\n\n"
            "CHUNK 3 — The vertical line test:\n\n"
            "How do you know if a graph represents a function? Use the vertical line test: "
            "if ANY vertical line crosses the graph more than once, it is NOT a function.\n\n"
            "Why? Because that would mean one input (the x-value) produces two different outputs.\n\n"
            "For example: y = x^2 passes the test (parabola). But x^2 + y^2 = 1 (a circle) fails — "
            "at x = 0, y can be +1 or -1.\n\n"
            "---\n\n"
            "CHUNK 4 — Function notation details:\n\n"
            "Different letters are just names. f(x), g(x), h(t), P(n) are all functions.\n\n"
            "f(x) does NOT mean f times x. It means 'f evaluated at x'.\n\n"
            "The difference quotient: [f(x + h) - f(x)] / h\n"
            "This expression is the backbone of calculus. We'll use it to define the derivative.\n\n"
            "Example: f(x) = 3x + 1\n"
            "f(x + h) = 3(x + h) + 1 = 3x + 3h + 1\n"
            "f(x + h) - f(x) = (3x + 3h + 1) - (3x + 1) = 3h\n"
            "[f(x + h) - f(x)] / h = 3h / h = 3"
        ),

        "key_concepts": [
            "function_definition",
            "input_output_relationship",
            "function_notation_f_of_x",
            "evaluating_functions",
            "vertical_line_test",
            "difference_quotient_intro",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: evaluate f(a), evaluate f(a+h), vertical line test, "
            "difference quotient computation. Mix: 3 MC, 2 free response."
        ),

        "practice_problems": [
            {"problem": "If f(x) = x^2 + 1, find f(-2).", "answer": "(-2)^2 + 1 = 4 + 1 = 5"},
            {"problem": "If g(x) = 2x - 7, find g(x + h).", "answer": "2(x + h) - 7 = 2x + 2h - 7"},
            {"problem": "Does x = y^2 represent y as a function of x?", "answer": "No — e.g. x=4 gives y=2 or y=-2"},
        ],

        "common_mistakes": [
            "Treating f(x) as f times x instead of function notation",
            "Forgetting to substitute into EVERY occurrence of x when evaluating",
            "Not squaring correctly: (a+h)^2 is NOT a^2 + h^2",
            "Confusing the difference quotient with the derivative (it's not the derivative yet)",
        ],

        "builds_toward": ["domain-and-range", "combining-functions", "derivative-at-a-point"],
    },

    "domain-and-range": {
        "id": "1.2",
        "slug": "domain-and-range",
        "title": "Domain and Range",
        "chapter": "functions-review",
        "chapter_title": "Functions and Their Properties",
        "subject": "calc-1",
        "prerequisites": ["functions-and-notation"],
        "estimated_time": "10-15 minutes",
        "difficulty": "Easy",

        "teaching_content": (
            "CHUNK 1 — What are domain and range?\n\n"
            "Domain = all possible INPUT values (x-values) for the function.\n"
            "Range = all possible OUTPUT values (y-values) the function produces.\n\n"
            "Think of it this way: the domain is 'what can I put in?' and the range is 'what can come out?'\n\n"
            "---\n\n"
            "CHUNK 2 — Finding the domain:\n\n"
            "Most functions work for all real numbers. You only need to worry about restrictions:\n\n"
            "Rule 1: You can't divide by zero.\n"
            "  f(x) = 1/(x - 3) → Domain: all reals except x = 3\n\n"
            "Rule 2: You can't take the square root of a negative number (in real numbers).\n"
            "  g(x) = sqrt(x - 2) → Need x - 2 >= 0, so x >= 2. Domain: [2, infinity)\n\n"
            "Rule 3: You can't take the log of zero or a negative number.\n"
            "  h(x) = ln(x + 5) → Need x + 5 > 0, so x > -5. Domain: (-5, infinity)\n\n"
            "Combine rules when needed:\n"
            "  k(x) = sqrt(x) / (x - 4) → Need x >= 0 AND x ≠ 4. Domain: [0, 4) union (4, infinity)\n\n"
            "---\n\n"
            "CHUNK 3 — Finding the range:\n\n"
            "The range is harder to find algebraically. Key strategies:\n\n"
            "1. Read it from the graph (look at the y-values covered).\n"
            "2. Use known shapes: y = x^2 has range [0, infinity). y = sin(x) has range [-1, 1].\n"
            "3. Solve for x in terms of y, then find which y-values work.\n\n"
            "Example: f(x) = x^2 + 3. The smallest value of x^2 is 0, so the smallest output "
            "is 0 + 3 = 3. Range: [3, infinity).\n\n"
            "---\n\n"
            "CHUNK 4 — Interval notation:\n\n"
            "( ) means 'not included' (open). [ ] means 'included' (closed).\n"
            "infinity always gets a parenthesis (you can never reach infinity).\n\n"
            "Examples:\n"
            "- All reals: (-infinity, infinity)\n"
            "- x > 3: (3, infinity)\n"
            "- -2 <= x < 5: [-2, 5)\n"
            "- x ≠ 0: (-infinity, 0) union (0, infinity)"
        ),

        "key_concepts": [
            "domain_definition",
            "range_definition",
            "division_by_zero_restriction",
            "square_root_restriction",
            "logarithm_restriction",
            "interval_notation",
            "combining_domain_restrictions",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: find domain of rational function, find domain of square root, "
            "interval notation, find range from graph or known shape. Mix: 2 MC, 3 free response."
        ),

        "practice_problems": [
            {"problem": "Find the domain of f(x) = 1 / (x^2 - 9).", "answer": "All reals except x = 3 and x = -3. In interval notation: (-inf, -3) U (-3, 3) U (3, inf)"},
            {"problem": "Find the domain of g(x) = sqrt(5 - x).", "answer": "5 - x >= 0, so x <= 5. Domain: (-inf, 5]"},
            {"problem": "What is the range of h(x) = |x| + 2?", "answer": "[2, infinity) since |x| >= 0"},
        ],

        "common_mistakes": [
            "Forgetting that denominators can't be zero",
            "Writing x > 0 instead of x >= 0 for sqrt(x) (zero IS allowed under a square root)",
            "Using brackets with infinity: [3, infinity] is wrong — always use (3, infinity)",
            "Confusing domain (x-values) with range (y-values)",
        ],

        "builds_toward": ["combining-functions", "what-is-continuity", "idea-of-a-limit"],
    },

    "combining-functions": {
        "id": "1.3",
        "slug": "combining-functions",
        "title": "Combining Functions",
        "chapter": "functions-review",
        "chapter_title": "Functions and Their Properties",
        "subject": "calc-1",
        "prerequisites": ["functions-and-notation", "domain-and-range"],
        "estimated_time": "10-12 minutes",
        "difficulty": "Easy",

        "teaching_content": (
            "CHUNK 1 — Arithmetic operations on functions:\n\n"
            "Given f(x) and g(x), you can create new functions:\n"
            "- (f + g)(x) = f(x) + g(x)\n"
            "- (f - g)(x) = f(x) - g(x)\n"
            "- (f * g)(x) = f(x) * g(x)\n"
            "- (f / g)(x) = f(x) / g(x), where g(x) ≠ 0\n\n"
            "Example: f(x) = x^2, g(x) = 3x + 1\n"
            "(f + g)(x) = x^2 + 3x + 1\n"
            "(f * g)(x) = x^2(3x + 1) = 3x^3 + x^2\n\n"
            "---\n\n"
            "CHUNK 2 — Composition of functions:\n\n"
            "Composition means plugging one function INTO another.\n\n"
            "(f ∘ g)(x) = f(g(x)) — 'f of g of x'\n\n"
            "Read inside-out: first apply g, then apply f to the result.\n\n"
            "Example: f(x) = x^2, g(x) = x + 3\n"
            "f(g(x)) = f(x + 3) = (x + 3)^2 = x^2 + 6x + 9\n"
            "g(f(x)) = g(x^2) = x^2 + 3\n\n"
            "Notice: f(g(x)) ≠ g(f(x)) in general! Order matters.\n\n"
            "---\n\n"
            "CHUNK 3 — Why composition matters for calculus:\n\n"
            "The chain rule (coming in Chapter 6) is all about differentiating compositions. "
            "You need to be able to identify 'inner' and 'outer' functions.\n\n"
            "Example: h(x) = sqrt(x^2 + 1)\n"
            "This is a composition: outer = sqrt(·), inner = x^2 + 1\n"
            "So h(x) = f(g(x)) where f(u) = sqrt(u), g(x) = x^2 + 1\n\n"
            "Example: h(x) = sin(3x)\n"
            "Outer = sin(·), inner = 3x\n\n"
            "Being able to decompose functions this way is a critical skill for calculus."
        ),

        "key_concepts": [
            "sum_difference_of_functions",
            "product_quotient_of_functions",
            "composition_definition",
            "order_matters_in_composition",
            "decomposing_composite_functions",
            "inner_and_outer_functions",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: arithmetic ops on functions, compute f(g(x)), compute g(f(x)), "
            "decompose a composite function. Mix: 2 MC, 3 free response."
        ),

        "practice_problems": [
            {"problem": "f(x) = 2x+1, g(x) = x^2. Find f(g(3)).", "answer": "g(3) = 9, f(9) = 19"},
            {"problem": "If h(x) = (3x - 1)^4, identify inner and outer functions.", "answer": "Outer: u^4, Inner: 3x - 1"},
            {"problem": "f(x) = x+2, g(x) = x-2. Find f(g(x)).", "answer": "f(x-2) = (x-2)+2 = x"},
        ],

        "common_mistakes": [
            "Confusing f(g(x)) with f(x)*g(x) — composition is NOT multiplication",
            "Assuming f(g(x)) = g(f(x)) — order matters",
            "Not distributing correctly when expanding compositions",
            "Failing to identify inner/outer functions for chain rule preparation",
        ],

        "builds_toward": ["transformations", "chain-rule"],
    },

    "transformations": {
        "id": "1.4",
        "slug": "transformations",
        "title": "Transformations of Functions",
        "chapter": "functions-review",
        "chapter_title": "Functions and Their Properties",
        "subject": "calc-1",
        "prerequisites": ["functions-and-notation"],
        "estimated_time": "10-12 minutes",
        "difficulty": "Easy",

        "teaching_content": (
            "CHUNK 1 — Vertical and horizontal shifts:\n\n"
            "Starting from y = f(x):\n"
            "- y = f(x) + k → shifts UP by k units (k > 0)\n"
            "- y = f(x) - k → shifts DOWN by k units\n"
            "- y = f(x - h) → shifts RIGHT by h units (note: minus means right!)\n"
            "- y = f(x + h) → shifts LEFT by h units\n\n"
            "Example: y = (x - 2)^2 + 3 is the parabola y = x^2 shifted RIGHT 2, UP 3.\n\n"
            "Memory trick: horizontal shifts feel 'backwards' — (x - 2) moves right.\n\n"
            "---\n\n"
            "CHUNK 2 — Reflections:\n\n"
            "- y = -f(x) → reflects across the x-axis (flips upside down)\n"
            "- y = f(-x) → reflects across the y-axis (flips left-right)\n\n"
            "Example: y = -x^2 opens downward (reflected across x-axis).\n"
            "Example: y = (-x)^3 = -x^3 (reflected across y-axis, same as x-axis reflection for odd functions).\n\n"
            "---\n\n"
            "CHUNK 3 — Stretches and compressions:\n\n"
            "- y = a*f(x), |a| > 1 → vertical stretch (taller)\n"
            "- y = a*f(x), 0 < |a| < 1 → vertical compression (shorter)\n"
            "- y = f(bx), |b| > 1 → horizontal compression (narrower)\n"
            "- y = f(bx), 0 < |b| < 1 → horizontal stretch (wider)\n\n"
            "Example: y = 3*sin(x) has amplitude 3 (vertical stretch).\n"
            "Example: y = sin(2x) completes a cycle in pi instead of 2*pi (horizontal compression).\n\n"
            "---\n\n"
            "CHUNK 4 — Putting it all together:\n\n"
            "General form: y = a*f(b(x - h)) + k\n"
            "Order of operations for graphing:\n"
            "1. Horizontal shift by h\n"
            "2. Horizontal scale by 1/b\n"
            "3. Vertical scale by a (and reflect if a < 0)\n"
            "4. Vertical shift by k\n\n"
            "Example: y = -2*(x + 1)^2 + 5\n"
            "Start with y = x^2 → shift left 1 → vertical stretch by 2 → "
            "reflect across x-axis → shift up 5. Vertex at (-1, 5), opens down."
        ),

        "key_concepts": [
            "vertical_shifts",
            "horizontal_shifts",
            "reflections_x_axis",
            "reflections_y_axis",
            "vertical_stretch_compression",
            "horizontal_stretch_compression",
            "combining_transformations",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: identify shift direction, write equation from description, "
            "identify vertex after transformations, order of transformations. Mix: 3 MC, 2 free response."
        ),

        "practice_problems": [
            {"problem": "Describe the transformation: y = (x + 4)^2 - 7", "answer": "y = x^2 shifted LEFT 4, DOWN 7"},
            {"problem": "y = -sqrt(x) is y = sqrt(x) with what transformation?", "answer": "Reflected across the x-axis"},
            {"problem": "Start with y = |x|. Write the equation shifted right 3, stretched vertically by 2.", "answer": "y = 2|x - 3|"},
        ],

        "common_mistakes": [
            "Thinking (x - 2) shifts LEFT — it actually shifts RIGHT",
            "Confusing vertical and horizontal stretches (a vs b)",
            "Applying transformations in the wrong order",
            "Forgetting the negative sign creates a reflection",
        ],

        "builds_toward": ["polynomial-rational-functions", "graphing-sine-cosine", "curve-sketching"],
    },

    "polynomial-rational-functions": {
        "id": "1.5",
        "slug": "polynomial-rational-functions",
        "title": "Polynomial and Rational Functions",
        "chapter": "functions-review",
        "chapter_title": "Functions and Their Properties",
        "subject": "calc-1",
        "prerequisites": ["functions-and-notation", "domain-and-range"],
        "estimated_time": "12-15 minutes",
        "difficulty": "Medium",

        "teaching_content": (
            "CHUNK 1 — Polynomials:\n\n"
            "A polynomial is a sum of terms of the form a*x^n where n is a non-negative integer.\n"
            "f(x) = a_n*x^n + a_{n-1}*x^{n-1} + ... + a_1*x + a_0\n\n"
            "Degree = highest power of x. Leading coefficient = coefficient of that highest power.\n\n"
            "End behavior (what happens as x → +/- infinity):\n"
            "- Even degree, positive leading coeff: up on both ends\n"
            "- Even degree, negative leading coeff: down on both ends\n"
            "- Odd degree, positive leading coeff: down left, up right\n"
            "- Odd degree, negative leading coeff: up left, down right\n\n"
            "Zeros (roots): values of x where f(x) = 0. A degree-n polynomial has at most n real zeros.\n\n"
            "---\n\n"
            "CHUNK 2 — Rational functions:\n\n"
            "A rational function is a ratio of polynomials: f(x) = P(x) / Q(x).\n\n"
            "Key features:\n"
            "- Domain: all reals except where Q(x) = 0\n"
            "- Vertical asymptotes: x-values where Q(x) = 0 but P(x) ≠ 0\n"
            "- Holes: x-values where BOTH P(x) = 0 and Q(x) = 0 (common factor cancels)\n"
            "- Horizontal asymptote:\n"
            "  * degree(P) < degree(Q): y = 0\n"
            "  * degree(P) = degree(Q): y = (leading coeff of P)/(leading coeff of Q)\n"
            "  * degree(P) > degree(Q): no horizontal asymptote (may have slant asymptote)\n\n"
            "---\n\n"
            "CHUNK 3 — Why this matters for calculus:\n\n"
            "Limits at infinity → horizontal asymptotes. We'll formalize this.\n"
            "Vertical asymptotes → limits that blow up to +/- infinity.\n"
            "Zeros of polynomials → critical points, x-intercepts for curve sketching.\n"
            "Factoring → essential for limit evaluation and simplification.\n\n"
            "Example: f(x) = (x^2 - 4)/(x - 2) = (x+2)(x-2)/(x-2) = x + 2 for x ≠ 2.\n"
            "This has a HOLE at x = 2, not a vertical asymptote. The limit as x → 2 exists and equals 4."
        ),

        "key_concepts": [
            "polynomial_degree_leading_coefficient",
            "end_behavior",
            "zeros_of_polynomials",
            "rational_function_definition",
            "vertical_asymptotes",
            "horizontal_asymptotes",
            "holes_vs_asymptotes",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: end behavior, find vertical/horizontal asymptotes, "
            "identify hole vs asymptote, domain of rational function. Mix: 3 MC, 2 free response."
        ),

        "practice_problems": [
            {"problem": "What is the end behavior of f(x) = -2x^3 + x?", "answer": "Odd degree, negative leading coeff: rises left, falls right"},
            {"problem": "Find the vertical asymptote of g(x) = 3/(x+5).", "answer": "x = -5"},
            {"problem": "Find the horizontal asymptote of h(x) = (2x^2+1)/(3x^2-x).", "answer": "y = 2/3 (same degree, ratio of leading coefficients)"},
        ],

        "common_mistakes": [
            "Confusing holes with vertical asymptotes",
            "Forgetting to check if a factor cancels before declaring a vertical asymptote",
            "Getting end behavior backwards for negative leading coefficients",
            "Saying degree(P) > degree(Q) gives HA of y = 0 (it's the other way around)",
        ],

        "builds_toward": ["limits-involving-infinity", "curve-sketching"],
    },

    "transcendental-functions-review": {
        "id": "1.6",
        "slug": "transcendental-functions-review",
        "title": "Trig, Exponential, and Logarithmic Functions",
        "chapter": "functions-review",
        "chapter_title": "Functions and Their Properties",
        "subject": "calc-1",
        "prerequisites": ["functions-and-notation", "domain-and-range"],
        "estimated_time": "12-15 minutes",
        "difficulty": "Medium",

        "teaching_content": (
            "CHUNK 1 — Trig functions review:\n\n"
            "The six trig functions: sin, cos, tan, csc, sec, cot.\n\n"
            "Key values to know:\n"
            "sin(0) = 0, sin(pi/6) = 1/2, sin(pi/4) = sqrt(2)/2, sin(pi/3) = sqrt(3)/2, sin(pi/2) = 1\n"
            "cos(0) = 1, cos(pi/6) = sqrt(3)/2, cos(pi/4) = sqrt(2)/2, cos(pi/3) = 1/2, cos(pi/2) = 0\n\n"
            "Key identity: sin^2(x) + cos^2(x) = 1\n\n"
            "Important limits (you'll prove these in Chapter 2):\n"
            "lim[x→0] sin(x)/x = 1\n"
            "lim[x→0] (1 - cos(x))/x = 0\n\n"
            "---\n\n"
            "CHUNK 2 — Exponential functions:\n\n"
            "f(x) = a^x where a > 0, a ≠ 1.\n\n"
            "The most important base: e ≈ 2.71828 (Euler's number).\n"
            "f(x) = e^x is THE exponential function in calculus.\n\n"
            "Properties:\n"
            "- e^0 = 1\n"
            "- e^x is always positive\n"
            "- e^x is always increasing\n"
            "- As x → -infinity, e^x → 0\n"
            "- As x → +infinity, e^x → infinity\n\n"
            "Why e? Because d/dx[e^x] = e^x — it is its own derivative!\n\n"
            "---\n\n"
            "CHUNK 3 — Logarithmic functions:\n\n"
            "The logarithm is the INVERSE of the exponential.\n"
            "y = ln(x) means e^y = x.\n\n"
            "Key properties:\n"
            "- ln(1) = 0 (because e^0 = 1)\n"
            "- ln(e) = 1\n"
            "- ln(e^x) = x and e^(ln(x)) = x\n"
            "- Domain of ln(x): (0, infinity)\n"
            "- Range of ln(x): (-infinity, infinity)\n\n"
            "Log rules:\n"
            "- ln(ab) = ln(a) + ln(b)\n"
            "- ln(a/b) = ln(a) - ln(b)\n"
            "- ln(a^n) = n*ln(a)\n\n"
            "These rules are essential for logarithmic differentiation in Chapter 6.\n\n"
            "---\n\n"
            "CHUNK 4 — The relationship between exp and ln:\n\n"
            "e^x and ln(x) are inverses — they 'undo' each other.\n"
            "Graphically: ln(x) is e^x reflected across the line y = x.\n\n"
            "Solving equations:\n"
            "e^x = 5 → x = ln(5)\n"
            "ln(x) = 3 → x = e^3\n"
            "2^x = 10 → x = ln(10)/ln(2) ≈ 3.32"
        ),

        "key_concepts": [
            "trig_values_at_key_angles",
            "pythagorean_identity",
            "euler_number_e",
            "exponential_function_properties",
            "natural_logarithm",
            "log_rules",
            "exp_and_ln_are_inverses",
            "solving_exponential_equations",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: trig values at standard angles, properties of e^x, log rules, "
            "inverse relationship of exp and ln. Mix: 3 MC, 2 free response."
        ),

        "practice_problems": [
            {"problem": "Simplify ln(e^7).", "answer": "7"},
            {"problem": "Solve e^(2x) = 20.", "answer": "2x = ln(20), x = ln(20)/2 ≈ 1.498"},
            {"problem": "What is sin(pi/4) + cos(pi/4)?", "answer": "sqrt(2)/2 + sqrt(2)/2 = sqrt(2) ≈ 1.414"},
        ],

        "common_mistakes": [
            "Thinking ln(a + b) = ln(a) + ln(b) — WRONG, log rules are for products not sums",
            "Confusing e^x with x*e — they are completely different",
            "Forgetting the domain of ln(x) is x > 0",
            "Not knowing key trig values — these must be memorized",
        ],

        "builds_toward": ["derivatives-of-trig", "derivatives-of-exponentials", "derivatives-of-logarithms"],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 2: Limits — The Foundation of Calculus
    # ══════════════════════════════════════════════════════════════════════════

    "idea-of-a-limit": {
        "id": "2.1",
        "slug": "idea-of-a-limit",
        "title": "The Idea of a Limit",
        "chapter": "limits",
        "chapter_title": "Limits — The Foundation of Calculus",
        "subject": "calc-1",
        "prerequisites": ["functions-and-notation"],
        "estimated_time": "10-15 minutes",
        "difficulty": "Easy",

        "teaching_content": (
            "CHUNK 1 — What is a limit?\n\n"
            "A limit asks: 'What value does f(x) APPROACH as x gets closer and closer to some number c?'\n\n"
            "We write: lim[x→c] f(x) = L\n\n"
            "This means: as x approaches c (from both sides), f(x) gets closer and closer to L.\n\n"
            "CRITICAL: The limit is about what f(x) APPROACHES, not what f(c) actually equals. "
            "The function doesn't even need to be defined at c!\n\n"
            "---\n\n"
            "CHUNK 2 — Intuitive examples:\n\n"
            "Example 1: f(x) = 2x + 1. What is lim[x→3] f(x)?\n"
            "As x → 3: f(2.9) = 6.8, f(2.99) = 6.98, f(2.999) = 6.998\n"
            "The limit is 7. (And f(3) = 7 too — the function is 'well-behaved'.)\n\n"
            "Example 2: f(x) = (x^2 - 1)/(x - 1). What is lim[x→1] f(x)?\n"
            "f(1) is undefined (0/0). But simplify: (x^2-1)/(x-1) = (x+1)(x-1)/(x-1) = x+1 for x ≠ 1.\n"
            "As x → 1: f(0.9) = 1.9, f(0.99) = 1.99, f(0.999) = 1.999\n"
            "The limit is 2, even though f(1) doesn't exist!\n\n"
            "---\n\n"
            "CHUNK 3 — One-sided limits:\n\n"
            "lim[x→c^-] f(x) = limit from the LEFT (x approaches c from values less than c)\n"
            "lim[x→c^+] f(x) = limit from the RIGHT (x approaches c from values greater than c)\n\n"
            "The two-sided limit lim[x→c] f(x) exists ONLY if both one-sided limits exist AND are equal.\n\n"
            "Example: f(x) = |x|/x\n"
            "From the left (x < 0): |x|/x = -x/x = -1 → lim[x→0^-] = -1\n"
            "From the right (x > 0): |x|/x = x/x = 1 → lim[x→0^+] = 1\n"
            "Since -1 ≠ 1, lim[x→0] |x|/x does NOT exist.\n\n"
            "---\n\n"
            "CHUNK 4 — When limits don't exist:\n\n"
            "A limit fails to exist if:\n"
            "1. Left and right limits are different (as above)\n"
            "2. The function oscillates wildly (e.g., sin(1/x) as x → 0)\n"
            "3. The function blows up to infinity (e.g., 1/x^2 as x → 0)\n\n"
            "When the function approaches +infinity or -infinity, we sometimes write "
            "lim[x→c] f(x) = infinity. Technically the limit 'does not exist' as a finite number, "
            "but saying it equals infinity tells us HOW it fails."
        ),

        "key_concepts": [
            "limit_definition_intuitive",
            "limit_vs_function_value",
            "one_sided_limits",
            "left_limit_right_limit",
            "two_sided_limit_existence",
            "when_limits_dont_exist",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: evaluate simple limits, one-sided limits, determine if two-sided limit exists, "
            "limit of function undefined at a point. Mix: 3 MC, 2 free response."
        ),

        "practice_problems": [
            {"problem": "Find lim[x→2] (3x - 1).", "answer": "3(2) - 1 = 5"},
            {"problem": "Does lim[x→0] (1/x) exist?", "answer": "No — from the left it → -infinity, from the right it → +infinity"},
            {"problem": "If lim[x→5^-] f(x) = 3 and lim[x→5^+] f(x) = 3, what is lim[x→5] f(x)?", "answer": "3 (both sides agree)"},
        ],

        "common_mistakes": [
            "Thinking the limit must equal f(c) — the function doesn't even need to be defined at c",
            "Forgetting to check both sides for the two-sided limit",
            "Saying lim = infinity means the limit 'exists' — technically it doesn't as a finite number",
            "Plugging in the exact value c when the function is undefined there",
        ],

        "builds_toward": ["limits-from-graphs-tables", "limit-laws", "what-is-continuity"],
    },

    "limits-from-graphs-tables": {
        "id": "2.2",
        "slug": "limits-from-graphs-tables",
        "title": "Finding Limits from Graphs and Tables",
        "chapter": "limits",
        "chapter_title": "Limits — The Foundation of Calculus",
        "subject": "calc-1",
        "prerequisites": ["idea-of-a-limit"],
        "estimated_time": "8-12 minutes",
        "difficulty": "Easy",

        "teaching_content": (
            "CHUNK 1 — Reading limits from graphs:\n\n"
            "To find lim[x→c] f(x) from a graph:\n"
            "1. Trace the curve from the LEFT toward x = c. Where does it head? That's lim[x→c^-].\n"
            "2. Trace the curve from the RIGHT toward x = c. Where does it head? That's lim[x→c^+].\n"
            "3. If they match, that's the limit.\n\n"
            "Important: Look at where the curve is HEADING, not whether there's a dot at that point.\n"
            "- An open circle at a point means the function is NOT defined there, but the limit can still exist.\n"
            "- A filled dot might be at a different y-value than where the curve approaches.\n\n"
            "---\n\n"
            "CHUNK 2 — Reading limits from tables:\n\n"
            "Make a table of x-values approaching c from both sides and compute f(x):\n\n"
            "Example: lim[x→0] sin(x)/x\n"
            "x:      -0.1     -0.01    -0.001   |  0.001   0.01    0.1\n"
            "f(x):   0.9983   0.99998  0.9999998|  0.9999998 0.99998 0.9983\n\n"
            "The values approach 1 from both sides, so lim[x→0] sin(x)/x = 1.\n\n"
            "Warning: Tables can be misleading! They only suggest the limit — they don't prove it.\n\n"
            "---\n\n"
            "CHUNK 3 — Combining graph reading with function values:\n\n"
            "For piecewise functions, you often need to read the limit and the function value separately.\n\n"
            "Example: f(x) = { x + 1 if x < 2, 5 if x = 2, x^2 if x > 2 }\n"
            "lim[x→2^-] f(x) = 2 + 1 = 3 (use x + 1 piece)\n"
            "lim[x→2^+] f(x) = 2^2 = 4 (use x^2 piece)\n"
            "Since 3 ≠ 4, lim[x→2] f(x) does NOT exist.\n"
            "Note: f(2) = 5, but that's irrelevant to the limit."
        ),

        "key_concepts": [
            "reading_limits_from_graphs",
            "open_vs_closed_circles",
            "limits_from_tables",
            "piecewise_function_limits",
            "tables_suggest_not_prove",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: read limit from described graph, evaluate piecewise limit, "
            "table-based limit estimation. Mix: 3 MC, 2 free response."
        ),

        "practice_problems": [
            {"problem": "If a graph approaches y=4 from the left of x=1 and y=4 from the right, with an open circle at (1,4) and a dot at (1,6), what is lim[x→1] f(x)?", "answer": "4 (the limit is about approach, not the actual value)"},
            {"problem": "f(x) = { 2x if x < 1, 3 if x >= 1 }. Find lim[x→1] f(x).", "answer": "lim from left = 2(1) = 2, lim from right = 3. Limit does not exist."},
        ],

        "common_mistakes": [
            "Reading the function value instead of where the graph approaches",
            "Confusing open circles (undefined) with the limit value",
            "Not checking BOTH sides of a piecewise function at the boundary",
        ],

        "builds_toward": ["limit-laws", "what-is-continuity"],
    },

    "limit-laws": {
        "id": "2.3",
        "slug": "limit-laws",
        "title": "Limit Laws and Algebraic Techniques",
        "chapter": "limits",
        "chapter_title": "Limits — The Foundation of Calculus",
        "subject": "calc-1",
        "prerequisites": ["idea-of-a-limit"],
        "estimated_time": "15-20 minutes",
        "difficulty": "Medium",

        "teaching_content": (
            "CHUNK 1 — The limit laws:\n\n"
            "If lim[x→c] f(x) = L and lim[x→c] g(x) = M, then:\n\n"
            "1. Sum: lim[x→c] [f(x) + g(x)] = L + M\n"
            "2. Difference: lim[x→c] [f(x) - g(x)] = L - M\n"
            "3. Product: lim[x→c] [f(x) * g(x)] = L * M\n"
            "4. Quotient: lim[x→c] [f(x)/g(x)] = L/M, provided M ≠ 0\n"
            "5. Power: lim[x→c] [f(x)]^n = L^n\n"
            "6. Root: lim[x→c] [f(x)]^(1/n) = L^(1/n) (if L > 0 for even n)\n"
            "7. Constant: lim[x→c] k = k\n"
            "8. Identity: lim[x→c] x = c\n\n"
            "---\n\n"
            "CHUNK 2 — Direct substitution:\n\n"
            "For polynomials and most 'nice' functions, the limit IS the function value:\n"
            "lim[x→c] f(x) = f(c)\n\n"
            "This works for polynomials, rational functions (where defined), "
            "trig functions, exponentials, and logarithms.\n\n"
            "Example: lim[x→3] (x^2 + 2x - 1) = 9 + 6 - 1 = 14. Done!\n\n"
            "But what if direct substitution gives 0/0? That's called an indeterminate form. "
            "You need algebraic manipulation.\n\n"
            "---\n\n"
            "CHUNK 3 — Algebraic techniques for 0/0:\n\n"
            "Technique 1 — Factor and cancel:\n"
            "lim[x→2] (x^2 - 4)/(x - 2) = lim[x→2] (x+2)(x-2)/(x-2) = lim[x→2] (x+2) = 4\n\n"
            "Technique 2 — Rationalize:\n"
            "lim[x→0] (sqrt(x+4) - 2)/x\n"
            "Multiply top and bottom by (sqrt(x+4) + 2):\n"
            "= lim[x→0] [(x+4) - 4] / [x(sqrt(x+4) + 2)]\n"
            "= lim[x→0] x / [x(sqrt(x+4) + 2)]\n"
            "= lim[x→0] 1 / (sqrt(x+4) + 2)\n"
            "= 1 / (sqrt(4) + 2) = 1/4\n\n"
            "Technique 3 — Common denominator (for complex fractions):\n"
            "lim[x→0] [(1/(x+3)) - (1/3)] / x\n"
            "Combine the top: [3 - (x+3)] / [3(x+3)] = -x / [3(x+3)]\n"
            "So the limit = lim[x→0] [-x / (3(x+3))] / x = lim[x→0] -1/[3(x+3)] = -1/9\n\n"
            "---\n\n"
            "CHUNK 4 — Strategy for evaluating limits:\n\n"
            "Step 1: Try direct substitution.\n"
            "Step 2: If you get 0/0, try algebraic manipulation (factor, rationalize, simplify).\n"
            "Step 3: After manipulation, try direct substitution again.\n"
            "Step 4: If you get a nonzero number / 0, the limit is +/- infinity (or DNE).\n"
            "Step 5: If nothing works, try a table or graph."
        ),

        "key_concepts": [
            "limit_laws_sum_product_quotient",
            "direct_substitution",
            "indeterminate_form_0_over_0",
            "factoring_and_canceling",
            "rationalizing_technique",
            "complex_fraction_technique",
            "limit_evaluation_strategy",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: direct substitution, factor and cancel 0/0, rationalize, "
            "identify indeterminate forms. Mix: 2 MC, 3 free response."
        ),

        "practice_problems": [
            {"problem": "Find lim[x→-1] (x^2 + 3x + 2)/(x + 1).", "answer": "Factor: (x+1)(x+2)/(x+1) = x+2. At x=-1: 1"},
            {"problem": "Find lim[x→4] (sqrt(x) - 2)/(x - 4).", "answer": "Rationalize: 1/(sqrt(x)+2). At x=4: 1/4"},
            {"problem": "Find lim[x→5] (x^2 - 25)/(x - 5).", "answer": "Factor: (x+5)(x-5)/(x-5) = x+5. At x=5: 10"},
        ],

        "common_mistakes": [
            "Stopping at 0/0 and saying 'the limit does not exist' — 0/0 means MORE WORK needed",
            "Canceling factors without checking that the problematic value makes them zero",
            "Forgetting to rationalize: multiply by conjugate on BOTH top and bottom",
            "Not simplifying completely before substituting again",
        ],

        "builds_toward": ["limits-involving-infinity", "squeeze-theorem", "what-is-continuity", "derivative-at-a-point"],
    },

    "limits-involving-infinity": {
        "id": "2.4",
        "slug": "limits-involving-infinity",
        "title": "Limits Involving Infinity",
        "chapter": "limits",
        "chapter_title": "Limits — The Foundation of Calculus",
        "subject": "calc-1",
        "prerequisites": ["limit-laws"],
        "estimated_time": "12-15 minutes",
        "difficulty": "Medium",

        "teaching_content": (
            "CHUNK 1 — Limits at infinity (horizontal asymptotes):\n\n"
            "lim[x→infinity] f(x) asks: what does f(x) approach as x gets very large?\n\n"
            "For rational functions P(x)/Q(x):\n"
            "- degree(P) < degree(Q): limit = 0\n"
            "- degree(P) = degree(Q): limit = (leading coeff of P)/(leading coeff of Q)\n"
            "- degree(P) > degree(Q): limit = +/- infinity (no horizontal asymptote)\n\n"
            "Example: lim[x→inf] (3x^2 + 1)/(5x^2 - 2x) = 3/5\n\n"
            "Trick: Divide every term by the highest power of x in the denominator.\n"
            "= lim[x→inf] (3 + 1/x^2)/(5 - 2/x) = (3 + 0)/(5 - 0) = 3/5\n\n"
            "---\n\n"
            "CHUNK 2 — Infinite limits (vertical asymptotes):\n\n"
            "lim[x→c] f(x) = infinity means f(x) grows without bound as x → c.\n\n"
            "This happens when the denominator → 0 but the numerator → nonzero.\n\n"
            "Example: lim[x→0^+] 1/x = +infinity (positive values getting huge)\n"
            "         lim[x→0^-] 1/x = -infinity (negative values getting huge in magnitude)\n\n"
            "To determine +infinity vs -infinity, check the SIGN of the expression near c.\n\n"
            "Example: lim[x→3^+] 1/(x-3)\n"
            "When x is slightly > 3: x-3 is small and POSITIVE, so 1/(x-3) → +infinity.\n\n"
            "---\n\n"
            "CHUNK 3 — Key limits to know:\n\n"
            "lim[x→inf] 1/x = 0\n"
            "lim[x→inf] 1/x^n = 0 for any n > 0\n"
            "lim[x→inf] e^x = infinity\n"
            "lim[x→-inf] e^x = 0\n"
            "lim[x→inf] ln(x) = infinity\n"
            "lim[x→0^+] ln(x) = -infinity\n\n"
            "Growth rates: Exponentials beat polynomials beat logarithms.\n"
            "lim[x→inf] x^n / e^x = 0 for any n (exponential wins)\n"
            "lim[x→inf] ln(x) / x = 0 (polynomial wins over log)"
        ),

        "key_concepts": [
            "limits_at_infinity",
            "horizontal_asymptotes_via_limits",
            "rational_function_limit_rules",
            "divide_by_highest_power_technique",
            "infinite_limits",
            "vertical_asymptotes_via_limits",
            "sign_analysis_for_infinite_limits",
            "growth_rate_hierarchy",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: limit at infinity of rational function, identify horizontal asymptote, "
            "infinite limit with sign analysis, growth rate comparison. Mix: 3 MC, 2 free response."
        ),

        "practice_problems": [
            {"problem": "Find lim[x→inf] (4x^3 - x)/(2x^3 + 5).", "answer": "Same degree: 4/2 = 2"},
            {"problem": "Find lim[x→2^-] 1/(x-2)^2.", "answer": "+infinity (squared denominator is always positive)"},
            {"problem": "Which grows faster: x^100 or e^x?", "answer": "e^x (exponential always beats polynomial)"},
        ],

        "common_mistakes": [
            "Saying infinity - infinity = 0 (it's indeterminate)",
            "Forgetting to check the sign for infinite limits",
            "Confusing limit AT infinity with infinite limit",
            "Not dividing by the highest power in the denominator",
        ],

        "builds_toward": ["lhopitals-rule", "curve-sketching"],
    },

    "squeeze-theorem": {
        "id": "2.5",
        "slug": "squeeze-theorem",
        "title": "The Squeeze Theorem",
        "chapter": "limits",
        "chapter_title": "Limits — The Foundation of Calculus",
        "subject": "calc-1",
        "prerequisites": ["limit-laws"],
        "estimated_time": "10-12 minutes",
        "difficulty": "Medium",

        "teaching_content": (
            "CHUNK 1 — The Squeeze Theorem statement:\n\n"
            "If g(x) <= f(x) <= h(x) for all x near c (except possibly at c), and\n"
            "lim[x→c] g(x) = lim[x→c] h(x) = L,\n"
            "then lim[x→c] f(x) = L.\n\n"
            "In other words: if you can trap f between two functions that both approach L, "
            "then f must approach L too. It's 'squeezed' to L.\n\n"
            "---\n\n"
            "CHUNK 2 — The most important application: lim[x→0] sin(x)/x = 1\n\n"
            "We can't evaluate this directly (0/0). But using geometry of the unit circle:\n\n"
            "For 0 < x < pi/2: cos(x) <= sin(x)/x <= 1\n\n"
            "Since lim[x→0] cos(x) = 1 and lim[x→0] 1 = 1,\n"
            "by the Squeeze Theorem: lim[x→0] sin(x)/x = 1.\n\n"
            "This is one of the most important limits in calculus — it's used to prove "
            "that d/dx[sin(x)] = cos(x).\n\n"
            "---\n\n"
            "CHUNK 3 — Another key limit: lim[x→0] (1 - cos(x))/x = 0\n\n"
            "Proof using algebra:\n"
            "(1 - cos(x))/x * (1 + cos(x))/(1 + cos(x)) = (1 - cos^2(x)) / [x(1 + cos(x))]\n"
            "= sin^2(x) / [x(1 + cos(x))]\n"
            "= [sin(x)/x] * [sin(x)/(1 + cos(x))]\n"
            "→ 1 * [0/(1+1)] = 0\n\n"
            "---\n\n"
            "CHUNK 4 — When to use the Squeeze Theorem:\n\n"
            "Use it when:\n"
            "- The function oscillates (like sin or cos) but is being dampened\n"
            "- You can bound the function above and below by simpler functions\n\n"
            "Example: lim[x→0] x^2 * sin(1/x)\n"
            "sin(1/x) oscillates wildly between -1 and 1 as x → 0.\n"
            "But: -x^2 <= x^2 * sin(1/x) <= x^2\n"
            "Since lim[x→0] (-x^2) = 0 and lim[x→0] x^2 = 0,\n"
            "by Squeeze: lim[x→0] x^2 * sin(1/x) = 0."
        ),

        "key_concepts": [
            "squeeze_theorem_statement",
            "bounding_functions",
            "sinx_over_x_limit",
            "one_minus_cosx_over_x_limit",
            "when_to_use_squeeze",
            "oscillating_functions_with_damping",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: state the Squeeze Theorem, apply it to x^n*sin(1/x), "
            "evaluate lim sin(x)/x variants. Mix: 2 MC, 3 free response."
        ),

        "practice_problems": [
            {"problem": "Find lim[x→0] x*cos(1/x).", "answer": "0 (squeeze between -|x| and |x|)"},
            {"problem": "Find lim[x→0] sin(5x)/(5x).", "answer": "1 (same form as sin(u)/u with u = 5x → 0)"},
            {"problem": "Find lim[x→0] sin(3x)/x.", "answer": "Rewrite as 3 * sin(3x)/(3x) = 3 * 1 = 3"},
        ],

        "common_mistakes": [
            "Trying to use the Squeeze Theorem when bounds don't converge to the same limit",
            "Saying lim[x→0] sin(1/x) = 0 — it actually doesn't exist (no damping factor)",
            "Confusing sin(x)/x (→ 1) with x/sin(x) (also → 1, by reciprocal)",
            "Forgetting the factor when computing lim sin(kx)/x = k",
        ],

        "builds_toward": ["derivatives-of-trig", "epsilon-delta"],
    },

    "epsilon-delta": {
        "id": "2.6",
        "slug": "epsilon-delta",
        "title": "The Formal Definition of a Limit",
        "chapter": "limits",
        "chapter_title": "Limits — The Foundation of Calculus",
        "subject": "calc-1",
        "prerequisites": ["idea-of-a-limit", "limit-laws"],
        "estimated_time": "15-20 minutes",
        "difficulty": "Hard",

        "teaching_content": (
            "CHUNK 1 — The epsilon-delta definition:\n\n"
            "lim[x→c] f(x) = L means:\n\n"
            "For every epsilon > 0, there exists a delta > 0 such that:\n"
            "if 0 < |x - c| < delta, then |f(x) - L| < epsilon.\n\n"
            "In plain English: No matter how close you want f(x) to be to L (within epsilon), "
            "I can find a range around c (within delta) where all x-values in that range "
            "produce f(x) values within epsilon of L.\n\n"
            "---\n\n"
            "CHUNK 2 — Understanding the pieces:\n\n"
            "- epsilon (ε) = how close we want f(x) to be to L (the 'tolerance')\n"
            "- delta (δ) = how close x needs to be to c to achieve that tolerance\n"
            "- 0 < |x - c| means x is NEAR c but NOT EQUAL to c\n"
            "- |f(x) - L| < epsilon means f(x) is within epsilon of L\n\n"
            "The challenger picks ANY epsilon > 0 (no matter how tiny).\n"
            "You must find a delta that works for that epsilon.\n\n"
            "---\n\n"
            "CHUNK 3 — A simple proof:\n\n"
            "Prove: lim[x→3] (2x + 1) = 7\n\n"
            "Given epsilon > 0, we need |f(x) - 7| < epsilon when 0 < |x - 3| < delta.\n\n"
            "|f(x) - 7| = |(2x + 1) - 7| = |2x - 6| = 2|x - 3|\n\n"
            "We need 2|x - 3| < epsilon, i.e., |x - 3| < epsilon/2.\n\n"
            "So choose delta = epsilon/2.\n\n"
            "Proof: If 0 < |x - 3| < delta = epsilon/2, then\n"
            "|f(x) - 7| = 2|x - 3| < 2 * (epsilon/2) = epsilon. ✓\n\n"
            "---\n\n"
            "CHUNK 4 — Why this matters:\n\n"
            "The epsilon-delta definition makes limits RIGOROUS. It eliminates vague phrases "
            "like 'gets closer and closer.' It's the foundation for proving all the theorems in calculus.\n\n"
            "Most Calculus 1 courses don't require many epsilon-delta proofs, but understanding "
            "the definition helps you grasp why limits work and when they fail."
        ),

        "key_concepts": [
            "epsilon_delta_definition",
            "epsilon_as_tolerance",
            "delta_as_neighborhood",
            "structure_of_epsilon_delta_proof",
            "finding_delta_in_terms_of_epsilon",
            "why_formal_definition_matters",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: interpret the definition, identify epsilon and delta in context, "
            "simple linear epsilon-delta proof. Mix: 3 MC, 2 free response."
        ),

        "practice_problems": [
            {"problem": "In the definition, what does 0 < |x - c| mean?", "answer": "x is close to c but NOT equal to c"},
            {"problem": "For lim[x→2] (5x) = 10, find delta in terms of epsilon.", "answer": "|5x - 10| = 5|x-2| < epsilon, so delta = epsilon/5"},
        ],

        "common_mistakes": [
            "Thinking epsilon and delta must be small — they just must be positive",
            "Forgetting the 0 < part (x cannot equal c)",
            "Trying to find a specific number for delta — it should be in terms of epsilon",
            "Confusing the order: epsilon is given FIRST, then you find delta",
        ],

        "builds_toward": ["what-is-continuity", "derivative-at-a-point"],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 3: Continuity
    # ══════════════════════════════════════════════════════════════════════════

    "what-is-continuity": {
        "id": "3.1",
        "slug": "what-is-continuity",
        "title": "What Is Continuity?",
        "chapter": "continuity",
        "chapter_title": "Continuity",
        "subject": "calc-1",
        "prerequisites": ["idea-of-a-limit", "limit-laws"],
        "estimated_time": "10-12 minutes",
        "difficulty": "Easy",

        "teaching_content": (
            "CHUNK 1 — The three conditions for continuity:\n\n"
            "A function f is continuous at x = c if ALL THREE conditions hold:\n\n"
            "1. f(c) is DEFINED (c is in the domain)\n"
            "2. lim[x→c] f(x) EXISTS\n"
            "3. lim[x→c] f(x) = f(c) (the limit equals the function value)\n\n"
            "Informally: you can draw the graph without lifting your pen.\n\n"
            "If ANY of these fails, f is discontinuous at c.\n\n"
            "---\n\n"
            "CHUNK 2 — Examples:\n\n"
            "Continuous: f(x) = x^2 at x = 3.\n"
            "1. f(3) = 9 ✓\n"
            "2. lim[x→3] x^2 = 9 ✓\n"
            "3. 9 = 9 ✓\n\n"
            "Discontinuous: f(x) = (x^2-1)/(x-1) at x = 1.\n"
            "1. f(1) is undefined (0/0) ✗ → fails condition 1\n"
            "Even though lim[x→1] f(x) = 2 exists, the function isn't continuous.\n\n"
            "Discontinuous: g(x) = { x+1 if x < 2, 5 if x = 2 }\n"
            "lim[x→2^-] g(x) = 3, but g(2) = 5. So lim ≠ f(c) → fails condition 3.\n\n"
            "---\n\n"
            "CHUNK 3 — Functions that are always continuous:\n\n"
            "These functions are continuous EVERYWHERE in their domain:\n"
            "- Polynomials: continuous on (-infinity, infinity)\n"
            "- Rational functions: continuous except where denominator = 0\n"
            "- sin(x), cos(x): continuous everywhere\n"
            "- e^x: continuous everywhere\n"
            "- ln(x): continuous on (0, infinity)\n"
            "- sqrt(x): continuous on [0, infinity)\n\n"
            "Combinations (sums, products, compositions) of continuous functions are continuous."
        ),

        "key_concepts": [
            "three_conditions_for_continuity",
            "continuity_at_a_point",
            "checking_each_condition",
            "functions_continuous_on_domain",
            "continuity_of_combinations",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: check three conditions, identify which condition fails, "
            "identify always-continuous functions. Mix: 3 MC, 2 free response."
        ),

        "practice_problems": [
            {"problem": "Is f(x) = |x| continuous at x = 0?", "answer": "Yes — f(0) = 0, lim = 0, they match"},
            {"problem": "f(x) = 1/x. Is it continuous at x = 0?", "answer": "No — f(0) is undefined (condition 1 fails)"},
        ],

        "common_mistakes": [
            "Only checking the limit and forgetting to verify f(c) is defined",
            "Thinking a function is discontinuous just because it has a sharp corner",
            "Confusing 'not defined' with 'limit doesn't exist'",
        ],

        "builds_toward": ["types-of-discontinuities", "intermediate-value-theorem", "differentiability-vs-continuity"],
    },

    "types-of-discontinuities": {
        "id": "3.2",
        "slug": "types-of-discontinuities",
        "title": "Types of Discontinuities",
        "chapter": "continuity",
        "chapter_title": "Continuity",
        "subject": "calc-1",
        "prerequisites": ["what-is-continuity"],
        "estimated_time": "8-10 minutes",
        "difficulty": "Easy",

        "teaching_content": (
            "CHUNK 1 — Removable discontinuity (hole):\n\n"
            "The limit exists, but either f(c) is undefined or f(c) ≠ the limit.\n\n"
            "Example: f(x) = (x^2-4)/(x-2) at x = 2.\n"
            "lim[x→2] f(x) = 4, but f(2) is undefined.\n"
            "We could 'remove' the discontinuity by defining f(2) = 4.\n\n"
            "On a graph: this looks like a hole (open circle).\n\n"
            "---\n\n"
            "CHUNK 2 — Jump discontinuity:\n\n"
            "The left and right limits both exist but are DIFFERENT.\n\n"
            "Example: f(x) = { 1 if x < 0, 2 if x >= 0 }\n"
            "lim[x→0^-] f(x) = 1, lim[x→0^+] f(x) = 2.\n"
            "The function 'jumps' from 1 to 2.\n\n"
            "On a graph: you see a break — the graph jumps from one level to another.\n\n"
            "---\n\n"
            "CHUNK 3 — Infinite discontinuity:\n\n"
            "The function approaches +infinity or -infinity from one or both sides.\n\n"
            "Example: f(x) = 1/x at x = 0.\n"
            "lim[x→0^+] = +infinity, lim[x→0^-] = -infinity.\n\n"
            "On a graph: vertical asymptote.\n\n"
            "---\n\n"
            "CHUNK 4 — Summary:\n\n"
            "| Type | Limit exists? | f(c) defined? | Example |\n"
            "| Removable | Yes | No or wrong | (x^2-4)/(x-2) at x=2 |\n"
            "| Jump | One-sided yes, two-sided no | Maybe | piecewise step |\n"
            "| Infinite | No (approaches infinity) | No | 1/x at x=0 |"
        ),

        "key_concepts": [
            "removable_discontinuity",
            "jump_discontinuity",
            "infinite_discontinuity",
            "classifying_discontinuities",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: classify given discontinuity, identify from graph description. Mix: 3 MC, 2 free response."
        ),

        "practice_problems": [
            {"problem": "Classify the discontinuity of f(x) = |x|/x at x = 0.", "answer": "Jump (left limit = -1, right limit = 1)"},
            {"problem": "f(x) = (x-3)/(x^2-9) at x = 3. What type?", "answer": "Removable (factor: 1/(x+3), limit = 1/6)"},
        ],

        "common_mistakes": [
            "Calling a vertical asymptote a 'jump' — it's an infinite discontinuity",
            "Thinking all 0/0 situations are removable — only if the limit exists after simplification",
        ],

        "builds_toward": ["continuity-on-interval", "what-is-continuity"],
    },

    "continuity-on-interval": {
        "id": "3.3",
        "slug": "continuity-on-interval",
        "title": "Continuity on an Interval",
        "chapter": "continuity",
        "chapter_title": "Continuity",
        "subject": "calc-1",
        "prerequisites": ["what-is-continuity"],
        "estimated_time": "8-10 minutes",
        "difficulty": "Easy",

        "teaching_content": (
            "CHUNK 1 — Continuity on open and closed intervals:\n\n"
            "f is continuous on an open interval (a, b) if it's continuous at every point in (a, b).\n\n"
            "f is continuous on a closed interval [a, b] if:\n"
            "1. f is continuous on (a, b)\n"
            "2. lim[x→a^+] f(x) = f(a) (right-continuous at left endpoint)\n"
            "3. lim[x→b^-] f(x) = f(b) (left-continuous at right endpoint)\n\n"
            "---\n\n"
            "CHUNK 2 — Building continuous functions:\n\n"
            "Theorem: If f and g are continuous at c, then so are:\n"
            "f + g, f - g, f * g, f/g (if g(c) ≠ 0), f ∘ g\n\n"
            "This means: sums, products, quotients, and compositions of continuous functions "
            "are continuous (at all points where they're defined).\n\n"
            "Example: f(x) = e^(sin(x)) is continuous everywhere because:\n"
            "sin(x) is continuous everywhere, and e^u is continuous everywhere.\n\n"
            "---\n\n"
            "CHUNK 3 — Making piecewise functions continuous:\n\n"
            "Example: Find k so that f(x) = { x^2 if x <= 2, kx + 1 if x > 2 } is continuous at x = 2.\n\n"
            "We need lim[x→2^-] f(x) = lim[x→2^+] f(x) = f(2).\n"
            "Left: lim[x→2^-] x^2 = 4.\n"
            "Right: lim[x→2^+] (kx+1) = 2k+1.\n"
            "f(2) = 4 (using the x^2 piece).\n"
            "Set 2k + 1 = 4 → k = 3/2."
        ),

        "key_concepts": [
            "continuity_on_open_interval",
            "continuity_on_closed_interval",
            "endpoint_continuity",
            "continuity_of_combinations",
            "making_piecewise_continuous",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: check interval continuity, find k for piecewise continuity, "
            "composition of continuous functions. Mix: 2 MC, 3 free response."
        ),

        "practice_problems": [
            {"problem": "On what interval is f(x) = sqrt(9 - x^2) continuous?", "answer": "[-3, 3] (including endpoints with one-sided continuity)"},
            {"problem": "Find c so that f(x) = { 3x+c if x<1, x^2 if x>=1 } is continuous.", "answer": "3(1)+c = 1^2, so 3+c = 1, c = -2"},
        ],

        "common_mistakes": [
            "Forgetting endpoint checks for closed intervals",
            "Not using the correct piece of the piecewise function for each side",
        ],

        "builds_toward": ["intermediate-value-theorem", "mean-value-theorem"],
    },

    "intermediate-value-theorem": {
        "id": "3.4",
        "slug": "intermediate-value-theorem",
        "title": "The Intermediate Value Theorem",
        "chapter": "continuity",
        "chapter_title": "Continuity",
        "subject": "calc-1",
        "prerequisites": ["what-is-continuity", "continuity-on-interval"],
        "estimated_time": "10-12 minutes",
        "difficulty": "Medium",

        "teaching_content": (
            "CHUNK 1 — The theorem:\n\n"
            "If f is continuous on [a, b] and N is any number between f(a) and f(b), "
            "then there exists at least one c in (a, b) such that f(c) = N.\n\n"
            "In plain English: a continuous function that goes from f(a) to f(b) must hit "
            "every value in between. No skipping!\n\n"
            "Analogy: If you drive from 0 mph to 60 mph, you must pass through every speed "
            "in between — you can't teleport from 30 to 50.\n\n"
            "---\n\n"
            "CHUNK 2 — Using IVT to show a root exists:\n\n"
            "The most common application: show that f(x) = 0 has a solution in some interval.\n\n"
            "Example: Show that x^3 + x - 1 = 0 has a solution in [0, 1].\n\n"
            "Let f(x) = x^3 + x - 1.\n"
            "f(0) = 0 + 0 - 1 = -1 (negative)\n"
            "f(1) = 1 + 1 - 1 = 1 (positive)\n\n"
            "Since f is continuous (it's a polynomial) and f(0) < 0 < f(1), "
            "by IVT there exists c in (0, 1) where f(c) = 0.\n\n"
            "---\n\n"
            "CHUNK 3 — Important details:\n\n"
            "- IVT requires continuity. A discontinuous function CAN skip values.\n"
            "- IVT guarantees existence, not uniqueness. There might be multiple c values.\n"
            "- IVT doesn't tell you what c is — just that it exists.\n"
            "- The converse is NOT true: a function can hit every value without being continuous.\n\n"
            "To actually FIND c, you'd use methods like bisection or Newton's method."
        ),

        "key_concepts": [
            "intermediate_value_theorem_statement",
            "continuity_requirement",
            "using_ivt_for_root_existence",
            "sign_change_implies_root",
            "existence_not_uniqueness",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: apply IVT to show root exists, identify when IVT applies, "
            "explain why continuity is needed. Mix: 2 MC, 3 free response."
        ),

        "practice_problems": [
            {"problem": "Show cos(x) = x has a solution in [0, pi/2].", "answer": "f(x) = cos(x)-x. f(0)=1>0, f(pi/2)=-pi/2<0. By IVT, root exists."},
            {"problem": "Can you apply IVT to f(x) = 1/x on [-1, 1]?", "answer": "No — f is not continuous on [-1,1] (discontinuous at x=0)"},
        ],

        "common_mistakes": [
            "Applying IVT without checking continuity first",
            "Saying IVT tells you the exact value of c — it only guarantees existence",
            "Thinking IVT only works for finding zeros — it works for any intermediate value",
        ],

        "builds_toward": ["mean-value-theorem", "absolute-extrema"],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 4: Defining the Derivative
    # ══════════════════════════════════════════════════════════════════════════

    "tangent-lines-rates-of-change": {
        "id": "4.1",
        "slug": "tangent-lines-rates-of-change",
        "title": "Tangent Lines and Rates of Change",
        "chapter": "defining-the-derivative",
        "chapter_title": "Defining the Derivative",
        "subject": "calc-1",
        "prerequisites": ["idea-of-a-limit", "functions-and-notation"],
        "estimated_time": "12-15 minutes",
        "difficulty": "Medium",

        "teaching_content": (
            "CHUNK 1 — From secant lines to tangent lines:\n\n"
            "A secant line passes through TWO points on a curve.\n"
            "Slope of secant through (a, f(a)) and (b, f(b)):\n"
            "m_sec = [f(b) - f(a)] / (b - a)\n\n"
            "This is the AVERAGE rate of change of f from a to b.\n\n"
            "Now imagine sliding b closer and closer to a. The secant line rotates "
            "and approaches the TANGENT line — the line that just touches the curve at one point.\n\n"
            "The slope of the tangent line at x = a is:\n"
            "m_tan = lim[b→a] [f(b) - f(a)] / (b - a)\n\n"
            "---\n\n"
            "CHUNK 2 — Average vs. instantaneous rate of change:\n\n"
            "Average rate of change = slope of secant = [f(b) - f(a)] / (b - a)\n"
            "Instantaneous rate of change = slope of tangent = lim[h→0] [f(a+h) - f(a)] / h\n\n"
            "(We substituted b = a + h, so b - a = h, and as b → a, h → 0.)\n\n"
            "Real-world example: Your car's odometer says you traveled 120 miles in 2 hours.\n"
            "Average speed = 120/2 = 60 mph.\n"
            "But your speedometer gives your instantaneous speed at any moment — that's a derivative!\n\n"
            "---\n\n"
            "CHUNK 3 — Computing a tangent line slope:\n\n"
            "Example: Find the slope of the tangent to f(x) = x^2 at x = 3.\n\n"
            "m = lim[h→0] [f(3+h) - f(3)] / h\n"
            "  = lim[h→0] [(3+h)^2 - 9] / h\n"
            "  = lim[h→0] [9 + 6h + h^2 - 9] / h\n"
            "  = lim[h→0] [6h + h^2] / h\n"
            "  = lim[h→0] (6 + h)\n"
            "  = 6\n\n"
            "Tangent line: y - 9 = 6(x - 3), or y = 6x - 9.\n\n"
            "---\n\n"
            "CHUNK 4 — The tangent line equation:\n\n"
            "Once you have the slope m at x = a:\n"
            "Tangent line: y - f(a) = m(x - a)\n\n"
            "This is point-slope form with point (a, f(a)) and slope m."
        ),

        "key_concepts": [
            "secant_line",
            "average_rate_of_change",
            "tangent_line_as_limit_of_secants",
            "instantaneous_rate_of_change",
            "limit_definition_of_slope",
            "tangent_line_equation",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: compute tangent slope via limit, write tangent line equation, "
            "distinguish average vs instantaneous rate. Mix: 2 MC, 3 free response."
        ),

        "practice_problems": [
            {"problem": "Find the slope of the tangent to f(x) = x^2 at x = 1 using the limit definition.", "answer": "lim[h→0] [(1+h)^2-1]/h = lim[h→0] (2h+h^2)/h = 2"},
            {"problem": "Write the equation of the tangent line to f(x) = x^3 at x = 2.", "answer": "f(2) = 8, m = lim[h→0] [(2+h)^3-8]/h = 12. Line: y - 8 = 12(x - 2)"},
        ],

        "common_mistakes": [
            "Confusing secant (two points) with tangent (one point, limit process)",
            "Forgetting to expand (a+h)^2 = a^2 + 2ah + h^2 correctly",
            "Not canceling h before taking the limit (which would give 0/0)",
        ],

        "builds_toward": ["derivative-at-a-point", "derivative-as-a-function"],
    },

    "derivative-at-a-point": {
        "id": "4.2",
        "slug": "derivative-at-a-point",
        "title": "The Derivative at a Point",
        "chapter": "defining-the-derivative",
        "chapter_title": "Defining the Derivative",
        "subject": "calc-1",
        "prerequisites": ["tangent-lines-rates-of-change"],
        "estimated_time": "12-15 minutes",
        "difficulty": "Medium",

        "teaching_content": (
            "CHUNK 1 — The formal definition:\n\n"
            "The derivative of f at x = a is:\n\n"
            "f'(a) = lim[h→0] [f(a + h) - f(a)] / h\n\n"
            "This is exactly the tangent line slope from the previous lesson, now given the name 'derivative.'\n\n"
            "Alternative form (using x instead of h):\n"
            "f'(a) = lim[x→a] [f(x) - f(a)] / (x - a)\n\n"
            "Both forms are equivalent. Use whichever is easier for the problem.\n\n"
            "---\n\n"
            "CHUNK 2 — Computing derivatives from the definition:\n\n"
            "Example 1: f(x) = 3x^2 - 2x. Find f'(1).\n\n"
            "f'(1) = lim[h→0] [f(1+h) - f(1)] / h\n"
            "f(1+h) = 3(1+h)^2 - 2(1+h) = 3(1 + 2h + h^2) - 2 - 2h = 3 + 6h + 3h^2 - 2 - 2h = 1 + 4h + 3h^2\n"
            "f(1) = 3(1) - 2(1) = 1\n"
            "f'(1) = lim[h→0] [(1 + 4h + 3h^2) - 1] / h = lim[h→0] (4h + 3h^2)/h = lim[h→0] (4 + 3h) = 4\n\n"
            "Example 2: f(x) = sqrt(x). Find f'(4).\n\n"
            "f'(4) = lim[h→0] [sqrt(4+h) - 2] / h\n"
            "Rationalize: multiply by (sqrt(4+h) + 2)/(sqrt(4+h) + 2)\n"
            "= lim[h→0] [(4+h) - 4] / [h(sqrt(4+h) + 2)]\n"
            "= lim[h→0] h / [h(sqrt(4+h) + 2)]\n"
            "= lim[h→0] 1 / (sqrt(4+h) + 2) = 1/(2+2) = 1/4\n\n"
            "---\n\n"
            "CHUNK 3 — What the derivative means:\n\n"
            "f'(a) tells you:\n"
            "1. The slope of the tangent line at x = a\n"
            "2. The instantaneous rate of change of f at x = a\n"
            "3. The best linear approximation to f near x = a\n\n"
            "If f'(a) > 0: f is increasing at x = a\n"
            "If f'(a) < 0: f is decreasing at x = a\n"
            "If f'(a) = 0: f has a horizontal tangent at x = a (potential extremum)"
        ),

        "key_concepts": [
            "limit_definition_of_derivative",
            "h_form_vs_x_form",
            "computing_derivative_from_definition",
            "rationalizing_for_root_derivatives",
            "derivative_as_slope",
            "derivative_as_rate_of_change",
            "sign_of_derivative_meaning",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: compute f'(a) from limit definition, interpret derivative sign, "
            "use alternative form. Mix: 2 MC, 3 free response."
        ),

        "practice_problems": [
            {"problem": "Find f'(2) for f(x) = x^3 using the limit definition.", "answer": "lim[h→0] [(2+h)^3 - 8]/h = lim[h→0] (12h+6h^2+h^3)/h = 12"},
            {"problem": "Find f'(9) for f(x) = sqrt(x) using the limit definition.", "answer": "1/(2*sqrt(9)) = 1/6 (rationalize technique)"},
        ],

        "common_mistakes": [
            "Algebra errors when expanding (a+h)^n",
            "Forgetting to subtract f(a) after computing f(a+h)",
            "Not canceling h — if h remains in the denominator at the limit step, you made an error",
            "Confusing f'(a) (derivative at a point) with f'(x) (derivative function)",
        ],

        "builds_toward": ["derivative-as-a-function", "power-rule"],
    },

    "derivative-as-a-function": {
        "id": "4.3",
        "slug": "derivative-as-a-function",
        "title": "The Derivative as a Function",
        "chapter": "defining-the-derivative",
        "chapter_title": "Defining the Derivative",
        "subject": "calc-1",
        "prerequisites": ["derivative-at-a-point"],
        "estimated_time": "10-12 minutes",
        "difficulty": "Medium",

        "teaching_content": (
            "CHUNK 1 — From derivative at a point to derivative function:\n\n"
            "Instead of computing f'(a) for a specific a, replace a with x:\n\n"
            "f'(x) = lim[h→0] [f(x + h) - f(x)] / h\n\n"
            "This gives you a NEW function f'(x) — the derivative function — that tells you "
            "the slope at ANY point.\n\n"
            "Example: f(x) = x^2\n"
            "f'(x) = lim[h→0] [(x+h)^2 - x^2] / h = lim[h→0] [2xh + h^2]/h = lim[h→0] (2x + h) = 2x\n\n"
            "Now you can find the slope anywhere: f'(1) = 2, f'(3) = 6, f'(-5) = -10.\n\n"
            "---\n\n"
            "CHUNK 2 — Notation:\n\n"
            "There are several notations for the derivative. They all mean the same thing:\n\n"
            "f'(x) — Lagrange notation (prime notation)\n"
            "dy/dx — Leibniz notation (looks like a fraction, but it's a single symbol)\n"
            "d/dx[f(x)] — operator notation ('d/dx' means 'differentiate with respect to x')\n"
            "Df(x) — operator notation (less common)\n\n"
            "Leibniz notation dy/dx is especially useful because it reminds you WHICH variable "
            "you're differentiating with respect to, and it works well with the chain rule.\n\n"
            "---\n\n"
            "CHUNK 3 — Graphing the derivative:\n\n"
            "Given the graph of f(x), you can sketch f'(x):\n\n"
            "- Where f is increasing → f'(x) > 0 (above x-axis)\n"
            "- Where f is decreasing → f'(x) < 0 (below x-axis)\n"
            "- Where f has a horizontal tangent → f'(x) = 0 (crosses x-axis)\n"
            "- Where f is steep → |f'(x)| is large\n"
            "- Where f is flat → f'(x) is near 0\n\n"
            "Example: f(x) = x^2 is a parabola. f'(x) = 2x is a straight line through the origin."
        ),

        "key_concepts": [
            "derivative_function_definition",
            "computing_derivative_function",
            "prime_notation",
            "leibniz_notation",
            "graphing_derivative_from_function",
            "relationship_between_f_and_f_prime",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: compute f'(x) from definition, identify notation, "
            "sketch f' from graph of f. Mix: 3 MC, 2 free response."
        ),

        "practice_problems": [
            {"problem": "Find f'(x) for f(x) = 3x + 7 using the limit definition.", "answer": "lim[h→0] [3(x+h)+7 - (3x+7)]/h = lim[h→0] 3h/h = 3"},
            {"problem": "If f is increasing on (0,2) and decreasing on (2,4), describe f' on these intervals.", "answer": "f' > 0 on (0,2), f' < 0 on (2,4), f'(2) = 0"},
        ],

        "common_mistakes": [
            "Thinking dy/dx is a fraction you can always separate — it's a symbol for the derivative",
            "Confusing f' with the slope at a specific point vs the slope function",
            "When sketching f' from f, confusing increasing/decreasing with concave up/down",
        ],

        "builds_toward": ["power-rule", "interpreting-the-derivative", "increasing-decreasing"],
    },

    "differentiability-vs-continuity": {
        "id": "4.4",
        "slug": "differentiability-vs-continuity",
        "title": "Differentiability vs. Continuity",
        "chapter": "defining-the-derivative",
        "chapter_title": "Defining the Derivative",
        "subject": "calc-1",
        "prerequisites": ["derivative-at-a-point", "what-is-continuity"],
        "estimated_time": "8-10 minutes",
        "difficulty": "Medium",

        "teaching_content": (
            "CHUNK 1 — The key theorem:\n\n"
            "If f is differentiable at x = a, then f is continuous at x = a.\n\n"
            "In other words: differentiability IMPLIES continuity.\n\n"
            "But the CONVERSE IS FALSE: continuity does NOT imply differentiability.\n"
            "A function can be continuous but not differentiable.\n\n"
            "---\n\n"
            "CHUNK 2 — Where differentiability fails:\n\n"
            "A function is NOT differentiable at x = a if:\n\n"
            "1. Sharp corner/cusp: f(x) = |x| at x = 0.\n"
            "   Left derivative = -1, right derivative = +1. They don't match.\n\n"
            "2. Vertical tangent: f(x) = x^(1/3) at x = 0.\n"
            "   f'(0) = lim[h→0] h^(1/3)/h = lim[h→0] 1/h^(2/3) = infinity. Not finite.\n\n"
            "3. Discontinuity: If f isn't continuous at a, it can't be differentiable there.\n\n"
            "---\n\n"
            "CHUNK 3 — Summary:\n\n"
            "differentiable → continuous (always true)\n"
            "continuous → differentiable (NOT always true)\n\n"
            "Analogy: Being a college student implies you're a student. "
            "But being a student doesn't imply you're in college.\n\n"
            "In practice: most functions you encounter in calculus ARE differentiable except "
            "at isolated points (corners, cusps, vertical tangents)."
        ),

        "key_concepts": [
            "differentiable_implies_continuous",
            "continuous_does_not_imply_differentiable",
            "sharp_corners",
            "vertical_tangents",
            "checking_differentiability",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: state the theorem, give examples of continuous but not differentiable, "
            "check differentiability at corners. Mix: 3 MC, 2 free response."
        ),

        "practice_problems": [
            {"problem": "Is f(x) = |x - 3| differentiable at x = 3?", "answer": "No — sharp corner at x=3 (left derivative = -1, right = 1)"},
            {"problem": "If f is differentiable at x = 5, must it be continuous at x = 5?", "answer": "Yes — differentiability implies continuity"},
        ],

        "common_mistakes": [
            "Thinking continuous → differentiable (it doesn't!)",
            "Forgetting to check BOTH one-sided derivatives for corners",
            "Thinking |x| is not differentiable anywhere (it's only the corner at x=0 that fails)",
        ],

        "builds_toward": ["interpreting-the-derivative", "mean-value-theorem"],
    },

    "interpreting-the-derivative": {
        "id": "4.5",
        "slug": "interpreting-the-derivative",
        "title": "Interpreting the Derivative",
        "chapter": "defining-the-derivative",
        "chapter_title": "Defining the Derivative",
        "subject": "calc-1",
        "prerequisites": ["derivative-as-a-function"],
        "estimated_time": "10-12 minutes",
        "difficulty": "Easy",

        "teaching_content": (
            "CHUNK 1 — Units of the derivative:\n\n"
            "If f has units and x has units, then f'(x) has units of [f-units] / [x-units].\n\n"
            "Example: If s(t) gives position in meters and t is in seconds,\n"
            "then s'(t) is velocity in meters/second.\n\n"
            "Example: If C(q) gives cost in dollars and q is in items,\n"
            "then C'(q) is marginal cost in dollars/item.\n\n"
            "---\n\n"
            "CHUNK 2 — Reading derivative values:\n\n"
            "f'(a) = 3 means: at x = a, f is increasing at a rate of 3 units of output "
            "per 1 unit of input.\n\n"
            "f'(a) = -2 means: at x = a, f is decreasing at a rate of 2 units of output "
            "per 1 unit of input.\n\n"
            "f'(a) = 0 means: at x = a, f is momentarily neither increasing nor decreasing.\n\n"
            "Example: The population P(t) of a city at year t has P'(2020) = 5000.\n"
            "Interpretation: In 2020, the population was growing at about 5000 people per year.\n\n"
            "---\n\n"
            "CHUNK 3 — Position, velocity, acceleration:\n\n"
            "If s(t) = position at time t, then:\n"
            "- s'(t) = v(t) = velocity (rate of change of position)\n"
            "- s''(t) = v'(t) = a(t) = acceleration (rate of change of velocity)\n\n"
            "Speed = |v(t)| (always positive).\n"
            "Object moving right/up: v(t) > 0.\n"
            "Object moving left/down: v(t) < 0.\n"
            "Object speeding up: v and a have the same sign.\n"
            "Object slowing down: v and a have opposite signs."
        ),

        "key_concepts": [
            "derivative_units",
            "interpreting_derivative_value",
            "positive_negative_zero_derivative",
            "position_velocity_acceleration",
            "speed_vs_velocity",
            "speeding_up_vs_slowing_down",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: give units of derivative, interpret f'(a), "
            "determine if object speeds up/slows down. Mix: 3 MC, 2 free response."
        ),

        "practice_problems": [
            {"problem": "If f(x) gives temperature in °F and x is time in hours, what are the units of f'(x)?", "answer": "°F per hour"},
            {"problem": "v(t) = -3 and a(t) = -5. Is the object speeding up or slowing down?", "answer": "Speeding up (both negative = same sign)"},
            {"problem": "f'(7) = 0. What does this tell you about f at x = 7?", "answer": "The tangent line is horizontal; f has a potential local max or min"},
        ],

        "common_mistakes": [
            "Confusing speed (always positive) with velocity (can be negative)",
            "Thinking f'(a) = 0 always means a max or min (could be an inflection point)",
            "Saying the object slows down when velocity is negative (it depends on acceleration too)",
            "Forgetting units when interpreting derivatives in applied problems",
        ],

        "builds_toward": ["related-rates", "increasing-decreasing", "linear-approximation"],
    },
}
