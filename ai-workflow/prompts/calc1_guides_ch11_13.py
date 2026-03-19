"""
calc1_guides_ch11_13.py
Calculus 1 topic guides: Chapters 11-13
  Ch 11: The Fundamental Theorem of Calculus
  Ch 12: Integration Techniques
  Ch 13: Applications of Integration
"""

CALC1_GUIDES_CH11_13: dict[str, dict] = {

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 11: The Fundamental Theorem of Calculus
    # ══════════════════════════════════════════════════════════════════════════

    "ftc-part-1": {
        "id": "11.1",
        "slug": "ftc-part-1",
        "title": "The Fundamental Theorem of Calculus, Part 1",
        "chapter": "fundamental-theorem",
        "chapter_title": "The Fundamental Theorem of Calculus",
        "subject": "calc-1",
        "prerequisites": ["the-definite-integral", "antiderivatives"],
        "estimated_time": "12-15 minutes",
        "difficulty": "Medium",

        "teaching_content": (
            "CHUNK 1 — The big idea:\n\n"
            "FTC Part 1 says: if you take a definite integral and let the upper limit vary, "
            "then differentiate, you get back the original function.\n\n"
            "Formally: If f is continuous on [a, b], define F(x) = integral from a to x of f(t) dt.\n"
            "Then F'(x) = f(x).\n\n"
            "In words: the derivative of an accumulation function is the original function. "
            "Differentiation undoes integration!\n\n"
            "---\n\n"
            "CHUNK 2 — Basic examples:\n\n"
            "Example 1: d/dx [integral from 0 to x of t^3 dt] = x^3\n"
            "Just replace t with x!\n\n"
            "Example 2: d/dx [integral from 2 to x of cos(t) dt] = cos(x)\n\n"
            "Example 3: d/dx [integral from 1 to x of e^(t^2) dt] = e^(x^2)\n"
            "Even though we can't evaluate this integral in closed form, we can differentiate it!\n\n"
            "---\n\n"
            "CHUNK 3 — With the chain rule:\n\n"
            "If the upper limit is a function g(x) instead of just x:\n"
            "d/dx [integral from a to g(x) of f(t) dt] = f(g(x)) * g'(x)\n\n"
            "Example: d/dx [integral from 0 to x^2 of sin(t) dt]\n"
            "= sin(x^2) * d/dx[x^2] = sin(x^2) * 2x = 2x*sin(x^2)\n\n"
            "Example: d/dx [integral from 1 to e^x of ln(t) dt]\n"
            "= ln(e^x) * d/dx[e^x] = x * e^x\n\n"
            "---\n\n"
            "CHUNK 4 — When BOTH limits are functions:\n\n"
            "Split: integral from g(x) to h(x) = integral from a to h(x) - integral from a to g(x)\n\n"
            "Example: d/dx [integral from x to x^2 of t^3 dt]\n"
            "= (x^2)^3 * 2x - x^3 * 1 = 2x^7 - x^3"
        ),

        "key_concepts": [
            "ftc_part_1_statement",
            "accumulation_function",
            "derivative_undoes_integral",
            "ftc_with_chain_rule",
            "variable_upper_limit",
            "both_limits_variable",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: basic FTC Part 1, FTC with chain rule, both limits variable. "
            "Mix: 2 MC, 3 free response."
        ),

        "practice_problems": [
            {"problem": "d/dx [integral from 0 to x of sqrt(1+t^4) dt]", "answer": "sqrt(1+x^4)"},
            {"problem": "d/dx [integral from 1 to x^3 of cos(t) dt]", "answer": "cos(x^3) * 3x^2"},
            {"problem": "d/dx [integral from x to 0 of t^2 dt]", "answer": "-x^2 (flip limits, negate)"},
        ],

        "common_mistakes": [
            "Forgetting the chain rule when the upper limit is not just x",
            "Not negating when the variable is in the LOWER limit",
            "Trying to evaluate the integral first — FTC Part 1 lets you skip that",
        ],

        "builds_toward": ["ftc-part-2", "net-change-theorem"],
    },

    "ftc-part-2": {
        "id": "11.2",
        "slug": "ftc-part-2",
        "title": "The Fundamental Theorem of Calculus, Part 2",
        "chapter": "fundamental-theorem",
        "chapter_title": "The Fundamental Theorem of Calculus",
        "subject": "calc-1",
        "prerequisites": ["ftc-part-1", "antiderivatives"],
        "estimated_time": "12-15 minutes",
        "difficulty": "Medium",

        "teaching_content": (
            "CHUNK 1 — The evaluation theorem:\n\n"
            "If f is continuous on [a, b] and F is ANY antiderivative of f, then:\n\n"
            "integral from a to b of f(x) dx = F(b) - F(a)\n\n"
            "We write this as F(x) |_a^b = F(b) - F(a) (the evaluation bar).\n\n"
            "This is huge! Instead of computing Riemann sums, just find an antiderivative and subtract.\n\n"
            "---\n\n"
            "CHUNK 2 — Worked examples:\n\n"
            "Example 1: integral from 1 to 3 of 2x dx\n"
            "Antiderivative: F(x) = x^2\n"
            "= x^2 |_1^3 = 3^2 - 1^2 = 9 - 1 = 8\n\n"
            "Example 2: integral from 0 to pi of sin(x) dx\n"
            "F(x) = -cos(x)\n"
            "= -cos(x) |_0^pi = -cos(pi) - (-cos(0)) = -(-1) - (-1) = 1 + 1 = 2\n\n"
            "Example 3: integral from 1 to e of (1/x) dx\n"
            "F(x) = ln(x)\n"
            "= ln(x) |_1^e = ln(e) - ln(1) = 1 - 0 = 1\n\n"
            "Example 4: integral from 0 to 4 of (3x^2 - 2x + 1) dx\n"
            "F(x) = x^3 - x^2 + x\n"
            "= (64 - 16 + 4) - (0 - 0 + 0) = 52\n\n"
            "---\n\n"
            "CHUNK 3 — Why it works:\n\n"
            "FTC Part 2 connects the two branches of calculus:\n"
            "- Differential calculus (derivatives, rates of change)\n"
            "- Integral calculus (accumulation, area)\n\n"
            "The antiderivative F 'accumulates' the values of f. The difference F(b) - F(a) "
            "gives the total accumulation from a to b.\n\n"
            "Note: You don't need the +C for definite integrals. It cancels: "
            "(F(b) + C) - (F(a) + C) = F(b) - F(a)."
        ),

        "key_concepts": [
            "ftc_part_2_evaluation",
            "evaluation_bar_notation",
            "find_antiderivative_then_subtract",
            "no_plus_c_for_definite_integrals",
            "connection_between_diff_and_int_calculus",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: evaluate definite integrals of polynomials, trig, exponential, 1/x. "
            "Mix: 2 MC, 3 free response."
        ),

        "practice_problems": [
            {"problem": "integral from 0 to 2 of (x^3 + 1) dx", "answer": "x^4/4 + x |_0^2 = (4+2) - 0 = 6"},
            {"problem": "integral from 0 to pi/2 of cos(x) dx", "answer": "sin(x) |_0^{pi/2} = 1 - 0 = 1"},
            {"problem": "integral from 1 to 4 of (1/sqrt(x)) dx", "answer": "2*sqrt(x) |_1^4 = 4 - 2 = 2"},
        ],

        "common_mistakes": [
            "Subtracting in the wrong order: it's F(b) - F(a), not F(a) - F(b)",
            "Forgetting to evaluate the antiderivative at BOTH endpoints",
            "Getting the antiderivative wrong — always check by differentiating",
            "Adding +C in definite integrals (unnecessary, it cancels)",
        ],

        "builds_toward": ["net-change-theorem", "u-substitution-definite", "area-between-curves"],
    },

    "net-change-theorem": {
        "id": "11.3",
        "slug": "net-change-theorem",
        "title": "The Net Change Theorem",
        "chapter": "fundamental-theorem",
        "chapter_title": "The Fundamental Theorem of Calculus",
        "subject": "calc-1",
        "prerequisites": ["ftc-part-2"],
        "estimated_time": "10-12 minutes",
        "difficulty": "Medium",

        "teaching_content": (
            "CHUNK 1 — The theorem:\n\n"
            "integral from a to b of F'(x) dx = F(b) - F(a)\n\n"
            "The integral of a rate of change gives the NET change.\n\n"
            "This is really just FTC Part 2 read differently: if you integrate a derivative, "
            "you get the total change in the original function.\n\n"
            "---\n\n"
            "CHUNK 2 — Displacement vs. distance:\n\n"
            "If v(t) is velocity:\n\n"
            "Displacement = integral from a to b of v(t) dt\n"
            "(Net change in position — can be negative if you go backwards.)\n\n"
            "Total distance = integral from a to b of |v(t)| dt\n"
            "(Always positive — counts ALL movement regardless of direction.)\n\n"
            "Example: v(t) = t - 2 on [0, 4].\n"
            "Displacement = integral from 0 to 4 of (t-2) dt = [t^2/2 - 2t] |_0^4 = (8-8) - 0 = 0\n"
            "(You ended where you started!)\n\n"
            "Distance = integral from 0 to 2 of |t-2| dt + integral from 2 to 4 of |t-2| dt\n"
            "= integral from 0 to 2 of (2-t) dt + integral from 2 to 4 of (t-2) dt\n"
            "= [2t - t^2/2]|_0^2 + [t^2/2 - 2t]|_2^4 = 2 + 2 = 4\n\n"
            "---\n\n"
            "CHUNK 3 — Real-world applications:\n\n"
            "If R(t) = rate of water flow (gallons/min):\n"
            "integral from 0 to 10 of R(t) dt = total gallons that flowed in 10 minutes.\n\n"
            "If P'(t) = rate of population growth (people/year):\n"
            "integral from 2020 to 2025 of P'(t) dt = P(2025) - P(2020) = net population change."
        ),

        "key_concepts": [
            "net_change_theorem",
            "integral_of_rate_equals_net_change",
            "displacement_vs_distance",
            "absolute_value_for_total_distance",
            "real_world_rate_integration",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: displacement from velocity, distance vs displacement, "
            "net change from rate function. Mix: 2 MC, 3 free response."
        ),

        "practice_problems": [
            {"problem": "v(t) = 3t^2 - 6t. Find displacement on [0, 3].", "answer": "integral = [t^3 - 3t^2]|_0^3 = (27-27) - 0 = 0"},
            {"problem": "Water flows at R(t) = 2t + 1 gal/min. How much flows in 5 minutes?", "answer": "integral from 0 to 5 of (2t+1) dt = [t^2+t]|_0^5 = 30 gallons"},
        ],

        "common_mistakes": [
            "Confusing displacement (signed) with distance (unsigned)",
            "Forgetting absolute value when computing total distance",
            "Not splitting the integral at points where velocity changes sign",
        ],

        "builds_toward": ["area-between-curves", "average-value"],
    },

    "properties-of-definite-integrals": {
        "id": "11.4",
        "slug": "properties-of-definite-integrals",
        "title": "Properties of Definite Integrals",
        "chapter": "fundamental-theorem",
        "chapter_title": "The Fundamental Theorem of Calculus",
        "subject": "calc-1",
        "prerequisites": ["the-definite-integral", "ftc-part-2"],
        "estimated_time": "8-10 minutes",
        "difficulty": "Easy",

        "teaching_content": (
            "CHUNK 1 — Core properties:\n\n"
            "1. integral from a to a of f(x) dx = 0 (zero width = zero area)\n\n"
            "2. integral from a to b of f(x) dx = -integral from b to a of f(x) dx (reverse limits, flip sign)\n\n"
            "3. integral from a to b of c*f(x) dx = c * integral from a to b of f(x) dx (pull out constants)\n\n"
            "4. integral from a to b of [f(x) + g(x)] dx = integral of f + integral of g (split sums)\n\n"
            "5. integral from a to c of f(x) dx = integral from a to b of f(x) dx + integral from b to c of f(x) dx "
            "(split at intermediate point b)\n\n"
            "---\n\n"
            "CHUNK 2 — Comparison properties:\n\n"
            "6. If f(x) >= 0 on [a, b], then integral from a to b of f(x) dx >= 0\n\n"
            "7. If f(x) >= g(x) on [a, b], then integral of f >= integral of g\n\n"
            "8. If m <= f(x) <= M on [a, b], then m(b-a) <= integral of f dx <= M(b-a)\n"
            "(The integral is bounded by the smallest and largest rectangle.)\n\n"
            "---\n\n"
            "CHUNK 3 — Even and odd function shortcuts:\n\n"
            "If f is even (f(-x) = f(x)) and the interval is [-a, a]:\n"
            "integral from -a to a of f(x) dx = 2 * integral from 0 to a of f(x) dx\n\n"
            "If f is odd (f(-x) = -f(x)) and the interval is [-a, a]:\n"
            "integral from -a to a of f(x) dx = 0\n\n"
            "Example: integral from -3 to 3 of x^3 dx = 0 (x^3 is odd)\n"
            "Example: integral from -2 to 2 of x^2 dx = 2 * integral from 0 to 2 of x^2 dx = 2*(8/3) = 16/3"
        ),

        "key_concepts": [
            "zero_width_integral",
            "reversing_limits",
            "linearity_of_integrals",
            "additivity_over_intervals",
            "comparison_properties",
            "even_odd_function_shortcuts",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: apply properties to compute integrals, even/odd shortcuts, "
            "comparison bounds. Mix: 3 MC, 2 free response."
        ),

        "practice_problems": [
            {"problem": "If integral from 0 to 5 of f(x) dx = 7, find integral from 5 to 0 of f(x) dx.", "answer": "-7 (reverse limits)"},
            {"problem": "integral from -pi to pi of sin(x) dx", "answer": "0 (sin is odd, symmetric interval)"},
        ],

        "common_mistakes": [
            "Forgetting the negative sign when reversing limits",
            "Trying to split products: integral of f*g ≠ (integral of f)*(integral of g)",
            "Misidentifying even/odd: x^2 is even, x^3 is odd, x^2 + x is neither",
        ],

        "builds_toward": ["u-substitution-definite", "area-between-curves"],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 12: Integration Techniques
    # ══════════════════════════════════════════════════════════════════════════

    "u-substitution-indefinite": {
        "id": "12.1",
        "slug": "u-substitution-indefinite",
        "title": "U-Substitution (Indefinite Integrals)",
        "chapter": "integration-techniques",
        "chapter_title": "Integration Techniques",
        "subject": "calc-1",
        "prerequisites": ["basic-antidifferentiation", "chain-rule"],
        "estimated_time": "15-18 minutes",
        "difficulty": "Medium",

        "teaching_content": (
            "CHUNK 1 — The idea:\n\n"
            "U-substitution is the chain rule in reverse.\n\n"
            "Chain rule: d/dx[F(g(x))] = F'(g(x)) * g'(x) = f(g(x)) * g'(x)\n"
            "Reverse: integral of f(g(x)) * g'(x) dx = F(g(x)) + C\n\n"
            "We let u = g(x) (the 'inner function'), then du = g'(x) dx.\n"
            "The integral becomes integral of f(u) du — usually much simpler!\n\n"
            "---\n\n"
            "CHUNK 2 — Step-by-step method:\n\n"
            "1. Choose u (usually the inner function of a composition)\n"
            "2. Compute du = u' dx\n"
            "3. Solve for dx (or rearrange to match what you have)\n"
            "4. Substitute everything to u and du\n"
            "5. Integrate in terms of u\n"
            "6. Substitute back to x\n\n"
            "---\n\n"
            "CHUNK 3 — Worked examples:\n\n"
            "Example 1: integral of 2x * cos(x^2) dx\n"
            "Let u = x^2, du = 2x dx\n"
            "= integral of cos(u) du = sin(u) + C = sin(x^2) + C\n\n"
            "Example 2: integral of x * sqrt(x^2 + 1) dx\n"
            "Let u = x^2 + 1, du = 2x dx, so x dx = du/2\n"
            "= (1/2) integral of sqrt(u) du = (1/2) * (2/3) u^(3/2) + C = (1/3)(x^2+1)^(3/2) + C\n\n"
            "Example 3: integral of e^(3x) dx\n"
            "Let u = 3x, du = 3 dx, dx = du/3\n"
            "= (1/3) integral of e^u du = (1/3) e^u + C = (1/3) e^(3x) + C\n\n"
            "Example 4: integral of tan(x) dx = integral of sin(x)/cos(x) dx\n"
            "Let u = cos(x), du = -sin(x) dx\n"
            "= -integral of (1/u) du = -ln|u| + C = -ln|cos(x)| + C = ln|sec(x)| + C\n\n"
            "---\n\n"
            "CHUNK 4 — How to choose u:\n\n"
            "Good choices for u:\n"
            "- The expression inside a power, root, or function: (3x+1)^5 → u = 3x+1\n"
            "- The denominator: 1/(x^2+4) → u = x^2+4\n"
            "- The exponent: e^(5x) → u = 5x\n\n"
            "Check: after choosing u, does du (or a constant multiple of it) appear in the integral?\n"
            "If yes, you've found the right u."
        ),

        "key_concepts": [
            "u_substitution_as_reverse_chain_rule",
            "choosing_u",
            "computing_du",
            "substituting_and_integrating",
            "back_substitution",
            "adjusting_constants",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: basic u-sub, u-sub with constant adjustment, choose correct u, "
            "trig u-sub. Mix: 2 MC, 3 free response."
        ),

        "practice_problems": [
            {"problem": "integral of (2x+1)^4 dx", "answer": "u=2x+1, du=2dx. (1/2)*(u^5/5)+C = (2x+1)^5/10 + C"},
            {"problem": "integral of x*e^(x^2) dx", "answer": "u=x^2, du=2x dx. (1/2)e^u + C = (1/2)e^(x^2) + C"},
            {"problem": "integral of cos(x)/sqrt(sin(x)) dx", "answer": "u=sin(x), du=cos(x)dx. 2*sqrt(u)+C = 2*sqrt(sin(x))+C"},
        ],

        "common_mistakes": [
            "Choosing u such that du doesn't appear in the integral at all",
            "Forgetting to substitute ALL x's — no x should remain after substitution",
            "Forgetting to back-substitute from u to x at the end",
            "Not adjusting for constant multiples (if du = 2x dx but you have x dx, factor out 1/2)",
        ],

        "builds_toward": ["u-substitution-definite", "integrals-exp-log"],
    },

    "u-substitution-definite": {
        "id": "12.2",
        "slug": "u-substitution-definite",
        "title": "U-Substitution with Definite Integrals",
        "chapter": "integration-techniques",
        "chapter_title": "Integration Techniques",
        "subject": "calc-1",
        "prerequisites": ["u-substitution-indefinite", "ftc-part-2"],
        "estimated_time": "10-12 minutes",
        "difficulty": "Medium",

        "teaching_content": (
            "CHUNK 1 — Two approaches:\n\n"
            "Method 1 (change limits): Convert EVERYTHING to u, including the limits.\n"
            "If u = g(x), then when x = a → u = g(a), when x = b → u = g(b).\n"
            "Evaluate entirely in u — no back-substitution needed!\n\n"
            "Method 2 (back-substitute): Find the indefinite integral (back-substitute to x), "
            "then evaluate at original limits. Works but is more steps.\n\n"
            "---\n\n"
            "CHUNK 2 — Method 1 example:\n\n"
            "integral from 0 to 2 of x * sqrt(x^2 + 1) dx\n"
            "u = x^2 + 1, du = 2x dx, x dx = du/2\n"
            "When x = 0: u = 1. When x = 2: u = 5.\n\n"
            "= (1/2) integral from 1 to 5 of sqrt(u) du\n"
            "= (1/2) * [2/3 * u^(3/2)] |_1^5\n"
            "= (1/3) [5^(3/2) - 1^(3/2)]\n"
            "= (1/3) [5*sqrt(5) - 1]\n\n"
            "---\n\n"
            "CHUNK 3 — Method 2 on the same problem:\n\n"
            "Indefinite: (1/3)(x^2+1)^(3/2) + C (from earlier)\n"
            "Evaluate: (1/3)(5)^(3/2) - (1/3)(1)^(3/2) = (1/3)(5*sqrt(5) - 1) ✓ Same answer.\n\n"
            "---\n\n"
            "CHUNK 4 — Important warning:\n\n"
            "NEVER use x-limits with a u-integral! If you changed to u, the limits must be u-values. "
            "This is the most common error with this technique."
        ),

        "key_concepts": [
            "changing_limits_with_u_sub",
            "back_substitute_method",
            "converting_limits",
            "no_mixing_x_limits_with_u",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: definite integral with u-sub (change limits), choose method. "
            "Mix: 2 MC, 3 free response."
        ),

        "practice_problems": [
            {"problem": "integral from 0 to pi of sin(x)*cos(x) dx using u = sin(x)", "answer": "u limits: 0 to 0. Answer = 0 (or split at pi/2)"},
            {"problem": "integral from 1 to 2 of 1/(3x-1) dx", "answer": "u=3x-1. Limits: 2 to 5. (1/3)ln|u||_2^5 = (1/3)(ln5-ln2)"},
        ],

        "common_mistakes": [
            "Using x-limits on a u-integral (the #1 error!)",
            "Forgetting to convert BOTH limits to u-values",
            "Converting limits backwards (confusing which is lower/upper)",
        ],

        "builds_toward": ["integrals-exp-log", "area-between-curves"],
    },

    "integrals-exp-log": {
        "id": "12.3",
        "slug": "integrals-exp-log",
        "title": "Integrals of Exponential and Logarithmic Functions",
        "chapter": "integration-techniques",
        "chapter_title": "Integration Techniques",
        "subject": "calc-1",
        "prerequisites": ["u-substitution-indefinite", "derivatives-of-exponentials", "derivatives-of-logarithms"],
        "estimated_time": "10-12 minutes",
        "difficulty": "Medium",

        "teaching_content": (
            "CHUNK 1 — Key formulas:\n\n"
            "integral of e^x dx = e^x + C\n"
            "integral of a^x dx = a^x / ln(a) + C\n"
            "integral of (1/x) dx = ln|x| + C (absolute value is important!)\n\n"
            "---\n\n"
            "CHUNK 2 — With u-substitution:\n\n"
            "Example 1: integral of e^(5x) dx\n"
            "u = 5x, du = 5 dx → = (1/5)e^(5x) + C\n\n"
            "Example 2: integral of x * e^(x^2) dx\n"
            "u = x^2, du = 2x dx → = (1/2)e^(x^2) + C\n\n"
            "Example 3: integral of (3x^2)/(x^3 + 5) dx\n"
            "u = x^3 + 5, du = 3x^2 dx → = ln|x^3 + 5| + C\n\n"
            "---\n\n"
            "CHUNK 3 — The 1/x pattern:\n\n"
            "Whenever you see f'(x)/f(x), the integral is ln|f(x)| + C.\n\n"
            "integral of tan(x) dx = integral of sin(x)/cos(x) dx = -ln|cos(x)| + C = ln|sec(x)| + C\n"
            "integral of cot(x) dx = integral of cos(x)/sin(x) dx = ln|sin(x)| + C\n\n"
            "This pattern appears constantly in calculus."
        ),

        "key_concepts": [
            "integral_of_e_to_x",
            "integral_of_a_to_x",
            "integral_of_1_over_x",
            "absolute_value_in_ln",
            "f_prime_over_f_pattern",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: basic exp integral, u-sub with exp, 1/x pattern, tan/cot integrals. "
            "Mix: 2 MC, 3 free response."
        ),

        "practice_problems": [
            {"problem": "integral of 2^x dx", "answer": "2^x / ln(2) + C"},
            {"problem": "integral of e^(-x) dx", "answer": "-e^(-x) + C"},
            {"problem": "integral of (2x)/(x^2+3) dx", "answer": "ln|x^2+3| + C (u=x^2+3)"},
        ],

        "common_mistakes": [
            "Forgetting the absolute value in ln|x| (matters when x could be negative)",
            "Writing integral of 1/x = ln(x) instead of ln|x|",
            "Forgetting the 1/ln(a) factor for a^x integrals",
        ],

        "builds_toward": ["integrals-trig", "integrals-inverse-trig"],
    },

    "integrals-trig": {
        "id": "12.4",
        "slug": "integrals-trig",
        "title": "Integrals of Trigonometric Functions",
        "chapter": "integration-techniques",
        "chapter_title": "Integration Techniques",
        "subject": "calc-1",
        "prerequisites": ["derivatives-of-trig", "u-substitution-indefinite"],
        "estimated_time": "10-12 minutes",
        "difficulty": "Medium",

        "teaching_content": (
            "CHUNK 1 — The six basic trig integrals:\n\n"
            "integral of sin(x) dx = -cos(x) + C\n"
            "integral of cos(x) dx = sin(x) + C\n"
            "integral of sec^2(x) dx = tan(x) + C\n"
            "integral of csc^2(x) dx = -cot(x) + C\n"
            "integral of sec(x)*tan(x) dx = sec(x) + C\n"
            "integral of csc(x)*cot(x) dx = -csc(x) + C\n\n"
            "These come directly from reversing the six trig derivative formulas.\n\n"
            "---\n\n"
            "CHUNK 2 — Additional important integrals:\n\n"
            "integral of tan(x) dx = ln|sec(x)| + C\n"
            "integral of cot(x) dx = ln|sin(x)| + C\n"
            "integral of sec(x) dx = ln|sec(x) + tan(x)| + C\n"
            "integral of csc(x) dx = -ln|csc(x) + cot(x)| + C\n\n"
            "The sec(x) integral is tricky — it uses the multiply-by-conjugate trick:\n"
            "Multiply by (sec(x) + tan(x))/(sec(x) + tan(x)), then u = sec(x) + tan(x).\n\n"
            "---\n\n"
            "CHUNK 3 — With chain rule (u-sub):\n\n"
            "Example: integral of sin(3x) dx\n"
            "u = 3x, du = 3 dx → = -(1/3)cos(3x) + C\n\n"
            "Example: integral of sec^2(5x) dx\n"
            "u = 5x, du = 5 dx → = (1/5)tan(5x) + C\n\n"
            "Example: integral of cos(x) * sin^4(x) dx\n"
            "u = sin(x), du = cos(x) dx → = sin^5(x)/5 + C"
        ),

        "key_concepts": [
            "six_basic_trig_integrals",
            "integral_of_tan_and_cot",
            "integral_of_sec_and_csc",
            "trig_integrals_with_u_sub",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: basic trig integrals, trig with u-sub, tan/cot integrals. "
            "Mix: 3 MC, 2 free response."
        ),

        "practice_problems": [
            {"problem": "integral of cos(4x) dx", "answer": "(1/4)sin(4x) + C"},
            {"problem": "integral of sin(x)*cos^3(x) dx", "answer": "u=cos(x), du=-sin(x)dx. -cos^4(x)/4 + C"},
        ],

        "common_mistakes": [
            "Forgetting the negative sign: integral of sin = -cos, not +cos",
            "Confusing sec^2 (integrates to tan) with sec (integrates to ln|sec+tan|)",
        ],

        "builds_toward": ["integrals-inverse-trig"],
    },

    "integrals-inverse-trig": {
        "id": "12.5",
        "slug": "integrals-inverse-trig",
        "title": "Integrals Resulting in Inverse Trig Functions",
        "chapter": "integration-techniques",
        "chapter_title": "Integration Techniques",
        "subject": "calc-1",
        "prerequisites": ["derivatives-of-inverse-trig", "u-substitution-indefinite"],
        "estimated_time": "10-12 minutes",
        "difficulty": "Hard",

        "teaching_content": (
            "CHUNK 1 — The three key patterns:\n\n"
            "integral of 1/sqrt(1 - x^2) dx = arcsin(x) + C\n"
            "integral of 1/(1 + x^2) dx = arctan(x) + C\n"
            "integral of 1/(x*sqrt(x^2 - 1)) dx = arcsec(|x|) + C\n\n"
            "These come from reversing the inverse trig derivatives.\n\n"
            "---\n\n"
            "CHUNK 2 — Generalized forms (with a):\n\n"
            "integral of 1/sqrt(a^2 - x^2) dx = arcsin(x/a) + C\n"
            "integral of 1/(a^2 + x^2) dx = (1/a)*arctan(x/a) + C\n\n"
            "Example: integral of 1/sqrt(9 - x^2) dx\n"
            "a = 3 → = arcsin(x/3) + C\n\n"
            "Example: integral of 1/(4 + x^2) dx\n"
            "a = 2 → = (1/2)*arctan(x/2) + C\n\n"
            "---\n\n"
            "CHUNK 3 — Recognizing the pattern:\n\n"
            "The key is recognizing the form. Look for:\n"
            "- 1/sqrt(constant - x^2) → arcsin\n"
            "- 1/(constant + x^2) → arctan\n\n"
            "Sometimes you need to complete the square first:\n"
            "integral of 1/(x^2 + 6x + 13) dx\n"
            "= integral of 1/((x+3)^2 + 4) dx\n"
            "u = x+3, a = 2 → = (1/2)*arctan((x+3)/2) + C"
        ),

        "key_concepts": [
            "arcsin_integral_pattern",
            "arctan_integral_pattern",
            "generalized_forms_with_a",
            "completing_the_square_for_integrals",
            "recognizing_inverse_trig_patterns",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: basic inverse trig integrals, generalized form, "
            "completing the square. Mix: 2 MC, 3 free response."
        ),

        "practice_problems": [
            {"problem": "integral of 1/sqrt(1-4x^2) dx", "answer": "(1/2)*arcsin(2x) + C (u=2x)"},
            {"problem": "integral of 1/(25+x^2) dx", "answer": "(1/5)*arctan(x/5) + C"},
        ],

        "common_mistakes": [
            "Not recognizing the pattern because constants are different from 1",
            "Forgetting the 1/a factor in the arctan formula",
            "Confusing sqrt(a^2 - x^2) with sqrt(x^2 - a^2)",
        ],

        "builds_toward": ["area-between-curves", "volumes-disk-washer"],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 13: Applications of Integration
    # ══════════════════════════════════════════════════════════════════════════

    "area-between-curves": {
        "id": "13.1",
        "slug": "area-between-curves",
        "title": "Area Between Curves",
        "chapter": "applications-of-integration",
        "chapter_title": "Applications of Integration",
        "subject": "calc-1",
        "prerequisites": ["ftc-part-2", "u-substitution-definite"],
        "estimated_time": "12-15 minutes",
        "difficulty": "Medium",

        "teaching_content": (
            "CHUNK 1 — Area between two curves (horizontal slices):\n\n"
            "Area = integral from a to b of [f(x) - g(x)] dx\n\n"
            "where f(x) >= g(x) on [a, b] (f is on top, g is on bottom).\n\n"
            "Step 1: Find intersection points (set f(x) = g(x), solve for x) → these give a and b.\n"
            "Step 2: Determine which function is on top.\n"
            "Step 3: Integrate (top - bottom).\n\n"
            "---\n\n"
            "CHUNK 2 — Example:\n\n"
            "Find the area between y = x^2 and y = x.\n\n"
            "Step 1: x^2 = x → x^2 - x = 0 → x(x-1) = 0 → x = 0 and x = 1.\n"
            "Step 2: On [0, 1], x >= x^2, so x is on top.\n"
            "Step 3: A = integral from 0 to 1 of (x - x^2) dx\n"
            "= [x^2/2 - x^3/3] |_0^1 = 1/2 - 1/3 = 1/6\n\n"
            "---\n\n"
            "CHUNK 3 — When curves cross:\n\n"
            "If curves cross within [a, b], split into separate integrals for each region.\n\n"
            "Or use: Area = integral from a to b of |f(x) - g(x)| dx\n"
            "This always gives positive area regardless of which is on top.\n\n"
            "---\n\n"
            "CHUNK 4 — Integrating with respect to y:\n\n"
            "Sometimes it's easier to slice horizontally.\n"
            "Area = integral from c to d of [right(y) - left(y)] dy\n\n"
            "Example: Area between x = y^2 and x = y + 2.\n"
            "Intersections: y^2 = y + 2 → y^2 - y - 2 = 0 → (y-2)(y+1) = 0 → y = -1, 2\n"
            "Right: x = y+2. Left: x = y^2.\n"
            "A = integral from -1 to 2 of [(y+2) - y^2] dy = [y^2/2 + 2y - y^3/3] |_{-1}^{2} = 9/2"
        ),

        "key_concepts": [
            "area_as_integral_of_top_minus_bottom",
            "finding_intersection_points",
            "determining_which_is_on_top",
            "splitting_when_curves_cross",
            "integrating_with_respect_to_y",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: area between polynomial curves, determine top/bottom, "
            "integrate with respect to y. Mix: 2 MC, 3 free response."
        ),

        "practice_problems": [
            {"problem": "Area between y = x^2 and y = 4", "answer": "Intersect at x = -2, 2. A = integral from -2 to 2 of (4-x^2) dx = 32/3"},
            {"problem": "Area between y = sqrt(x) and y = x/2", "answer": "Intersect at x=0, x=4. A = integral from 0 to 4 of (sqrt(x)-x/2) dx = 4/3"},
        ],

        "common_mistakes": [
            "Subtracting in the wrong order (getting negative area)",
            "Not finding ALL intersection points",
            "Forgetting to split when the top/bottom function switches",
        ],

        "builds_toward": ["volumes-disk-washer", "volumes-shells"],
    },

    "volumes-disk-washer": {
        "id": "13.2",
        "slug": "volumes-disk-washer",
        "title": "Volumes by Disk and Washer Methods",
        "chapter": "applications-of-integration",
        "chapter_title": "Applications of Integration",
        "subject": "calc-1",
        "prerequisites": ["area-between-curves"],
        "estimated_time": "15-18 minutes",
        "difficulty": "Hard",

        "teaching_content": (
            "CHUNK 1 — Disk method (solid, no hole):\n\n"
            "When you rotate a region around an axis, you get a solid of revolution.\n\n"
            "Rotating around the x-axis:\n"
            "V = pi * integral from a to b of [R(x)]^2 dx\n"
            "where R(x) = the distance from the curve to the axis of rotation.\n\n"
            "Example: Rotate y = sqrt(x) from x=0 to x=4 around the x-axis.\n"
            "R(x) = sqrt(x)\n"
            "V = pi * integral from 0 to 4 of (sqrt(x))^2 dx = pi * integral of x dx = pi * [x^2/2]|_0^4 = 8*pi\n\n"
            "---\n\n"
            "CHUNK 2 — Washer method (with a hole):\n\n"
            "When there's a gap between the region and the axis:\n"
            "V = pi * integral from a to b of ([R(x)]^2 - [r(x)]^2) dx\n"
            "R(x) = outer radius, r(x) = inner radius.\n\n"
            "Example: Rotate the region between y = x^2 and y = x around the x-axis.\n"
            "On [0,1]: outer = x (farther from axis), inner = x^2.\n"
            "V = pi * integral from 0 to 1 of (x^2 - x^4) dx\n"
            "= pi * [x^3/3 - x^5/5]|_0^1 = pi*(1/3 - 1/5) = 2*pi/15\n\n"
            "---\n\n"
            "CHUNK 3 — Rotating around other lines:\n\n"
            "If rotating around y = k (instead of y = 0):\n"
            "R(x) = |f(x) - k| (distance from curve to line of rotation)\n\n"
            "Example: Rotate y = x^2 around y = 4 from x = 0 to 2.\n"
            "R(x) = 4 - x^2\n"
            "V = pi * integral from 0 to 2 of (4-x^2)^2 dx\n\n"
            "---\n\n"
            "CHUNK 4 — Rotating around the y-axis:\n\n"
            "Solve for x in terms of y, then integrate with respect to y.\n"
            "V = pi * integral from c to d of [R(y)]^2 dy"
        ),

        "key_concepts": [
            "solid_of_revolution",
            "disk_method",
            "washer_method_outer_minus_inner",
            "rotation_around_x_axis",
            "rotation_around_y_axis",
            "rotation_around_other_lines",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: disk method, washer method, rotation around non-axis line. "
            "Mix: 2 MC, 3 free response."
        ),

        "practice_problems": [
            {"problem": "Rotate y = x^3 around x-axis from x=0 to x=2. Find volume.", "answer": "V = pi * integral from 0 to 2 of x^6 dx = pi * [x^7/7]|_0^2 = 128*pi/7"},
            {"problem": "Rotate region between y = x and y = x^2 around x-axis. Volume?", "answer": "V = pi * integral from 0 to 1 of (x^2 - x^4) dx = 2*pi/15"},
        ],

        "common_mistakes": [
            "Forgetting the pi out front",
            "Not squaring the radius (writing pi*R instead of pi*R^2)",
            "Confusing outer and inner radius in washer problems",
            "Not adjusting radius when rotating around a line other than an axis",
        ],

        "builds_toward": ["volumes-shells"],
    },

    "volumes-shells": {
        "id": "13.3",
        "slug": "volumes-shells",
        "title": "Volumes by Cylindrical Shells",
        "chapter": "applications-of-integration",
        "chapter_title": "Applications of Integration",
        "subject": "calc-1",
        "prerequisites": ["volumes-disk-washer"],
        "estimated_time": "12-15 minutes",
        "difficulty": "Hard",

        "teaching_content": (
            "CHUNK 1 — The shell method:\n\n"
            "Instead of slicing perpendicular to the axis, wrap thin cylindrical shells around it.\n\n"
            "Rotating around the y-axis, integrating with respect to x:\n"
            "V = 2*pi * integral from a to b of (radius) * (height) dx\n"
            "V = 2*pi * integral from a to b of x * f(x) dx\n\n"
            "Each shell has:\n"
            "- radius = x (distance from the y-axis)\n"
            "- height = f(x)\n"
            "- thickness = dx\n\n"
            "---\n\n"
            "CHUNK 2 — When to use shells vs disks:\n\n"
            "Rule of thumb:\n"
            "- Rotating around x-axis → disks/washers in dx, shells in dy\n"
            "- Rotating around y-axis → shells in dx, disks/washers in dy\n\n"
            "Use shells when the disk/washer method would require solving for x.\n\n"
            "---\n\n"
            "CHUNK 3 — Example:\n\n"
            "Rotate y = x^2 from x = 0 to x = 2 around the y-axis.\n\n"
            "Shell method:\n"
            "V = 2*pi * integral from 0 to 2 of x * x^2 dx = 2*pi * integral of x^3 dx\n"
            "= 2*pi * [x^4/4]|_0^2 = 2*pi * 4 = 8*pi\n\n"
            "Compare: disk method would need x = sqrt(y), integrate from y=0 to y=4.\n"
            "V = pi * integral from 0 to 4 of y dy = pi * [y^2/2]|_0^4 = 8*pi ✓ Same answer.\n\n"
            "---\n\n"
            "CHUNK 4 — Shell method around other axes:\n\n"
            "Around x = k: radius = |x - k|, height = f(x)\n"
            "V = 2*pi * integral of |x - k| * f(x) dx"
        ),

        "key_concepts": [
            "cylindrical_shell_method",
            "shell_radius_and_height",
            "shells_vs_disks_when_to_use",
            "rotation_around_y_axis_with_shells",
            "shells_around_other_axes",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: shell method setup, choose shells vs disks, "
            "rotation around y-axis. Mix: 2 MC, 3 free response."
        ),

        "practice_problems": [
            {"problem": "Rotate y = sqrt(x) from x=0 to x=4 around y-axis using shells.", "answer": "V = 2*pi * integral from 0 to 4 of x*sqrt(x) dx = 2*pi * integral of x^(3/2) dx = 2*pi * [2x^(5/2)/5]|_0^4 = 128*pi/5"},
        ],

        "common_mistakes": [
            "Forgetting the 2*pi (not just pi like disk method)",
            "Using the wrong radius (it's distance to the AXIS OF ROTATION)",
            "Confusing when to use shells vs disks",
        ],

        "builds_toward": ["average-value"],
    },

    "average-value": {
        "id": "13.4",
        "slug": "average-value",
        "title": "Average Value of a Function",
        "chapter": "applications-of-integration",
        "chapter_title": "Applications of Integration",
        "subject": "calc-1",
        "prerequisites": ["ftc-part-2"],
        "estimated_time": "8-10 minutes",
        "difficulty": "Easy",

        "teaching_content": (
            "CHUNK 1 — The formula:\n\n"
            "The average value of f on [a, b] is:\n\n"
            "f_avg = (1/(b - a)) * integral from a to b of f(x) dx\n\n"
            "Think of it as: total accumulation divided by the length of the interval.\n\n"
            "Analogy: The average of test scores is the sum of all scores divided by the number of tests. "
            "This is the continuous version — sum becomes integral, count becomes interval length.\n\n"
            "---\n\n"
            "CHUNK 2 — Examples:\n\n"
            "Example 1: Average value of f(x) = x^2 on [0, 3].\n"
            "f_avg = (1/3) * integral from 0 to 3 of x^2 dx = (1/3) * [x^3/3]|_0^3 = (1/3)(9) = 3\n\n"
            "Example 2: Average temperature T(t) = 70 + 10*sin(pi*t/12) over [0, 24].\n"
            "T_avg = (1/24) * integral from 0 to 24 of [70 + 10*sin(pi*t/12)] dt\n"
            "= (1/24) * [70t - 10*(12/pi)*cos(pi*t/12)]|_0^24\n"
            "= (1/24) * [1680 - (120/pi)(1 - 1)] = 1680/24 = 70°F\n\n"
            "---\n\n"
            "CHUNK 3 — Mean Value Theorem for Integrals:\n\n"
            "If f is continuous on [a, b], there exists c in [a, b] such that:\n"
            "f(c) = f_avg = (1/(b-a)) * integral from a to b of f(x) dx\n\n"
            "In other words: the function actually HITS its average value at some point.\n\n"
            "This is the integral version of the Mean Value Theorem."
        ),

        "key_concepts": [
            "average_value_formula",
            "total_divided_by_interval_length",
            "mean_value_theorem_for_integrals",
            "function_hits_average_value",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: compute average value, apply MVT for integrals, "
            "interpret average value. Mix: 2 MC, 3 free response."
        ),

        "practice_problems": [
            {"problem": "Average value of f(x) = sin(x) on [0, pi].", "answer": "(1/pi) * integral of sin(x) dx from 0 to pi = (1/pi)(2) = 2/pi"},
            {"problem": "Average value of f(x) = e^x on [0, 2].", "answer": "(1/2)(e^2 - 1) ≈ 3.195"},
        ],

        "common_mistakes": [
            "Forgetting the 1/(b-a) factor",
            "Confusing average value with the midpoint value",
        ],

        "builds_toward": ["calc1-review"],
    },

    "calc1-review": {
        "id": "13.5",
        "slug": "calc1-review",
        "title": "Course Review and What Comes Next",
        "chapter": "applications-of-integration",
        "chapter_title": "Applications of Integration",
        "subject": "calc-1",
        "prerequisites": ["average-value", "volumes-shells"],
        "estimated_time": "15-20 minutes",
        "difficulty": "Medium",

        "teaching_content": (
            "CHUNK 1 — The big picture of Calculus 1:\n\n"
            "You've learned two BIG ideas and how they connect:\n\n"
            "1. DIFFERENTIATION — finding rates of change\n"
            "   - Limits → Continuity → Derivative definition → Rules → Applications\n"
            "   - You can find slopes, rates, optimize, and analyze functions.\n\n"
            "2. INTEGRATION — finding accumulations\n"
            "   - Antiderivatives → Riemann sums → Definite integrals → FTC → Techniques → Applications\n"
            "   - You can find areas, volumes, averages, and net changes.\n\n"
            "3. THE FUNDAMENTAL THEOREM — they're inverses of each other!\n"
            "   - Differentiation undoes integration and vice versa.\n\n"
            "---\n\n"
            "CHUNK 2 — Key derivative formulas to remember:\n\n"
            "Power: d/dx[x^n] = n*x^(n-1)\n"
            "Product: d/dx[fg] = f'g + fg'\n"
            "Quotient: d/dx[f/g] = (f'g - fg')/g^2\n"
            "Chain: d/dx[f(g(x))] = f'(g(x))*g'(x)\n"
            "Trig: d/dx[sin] = cos, d/dx[cos] = -sin, d/dx[tan] = sec^2\n"
            "Exp/Log: d/dx[e^x] = e^x, d/dx[ln x] = 1/x\n\n"
            "---\n\n"
            "CHUNK 3 — Key integration formulas:\n\n"
            "Power: integral of x^n = x^(n+1)/(n+1) + C (n ≠ -1)\n"
            "1/x: integral of (1/x) = ln|x| + C\n"
            "Exp: integral of e^x = e^x + C\n"
            "Trig: integral of sin = -cos, integral of cos = sin\n"
            "U-sub: the chain rule in reverse\n"
            "FTC: integral from a to b of f dx = F(b) - F(a)\n\n"
            "---\n\n"
            "CHUNK 4 — What comes in Calculus 2:\n\n"
            "- More integration techniques: integration by parts, partial fractions, trig substitution\n"
            "- Improper integrals (infinite limits)\n"
            "- Sequences and series (infinite sums)\n"
            "- Taylor and Maclaurin series (polynomial approximations)\n"
            "- Parametric and polar curves\n"
            "- Arc length and surface area\n\n"
            "You now have a strong foundation. Everything in Calc 2 builds on what you learned here."
        ),

        "key_concepts": [
            "big_picture_differentiation",
            "big_picture_integration",
            "ftc_connects_both",
            "key_derivative_formulas",
            "key_integration_formulas",
            "preview_of_calculus_2",
        ],

        "available_images": [],

        "quiz_guidelines": (
            "Test: mixed derivative and integral problems, conceptual questions "
            "about FTC, applied problems combining skills. Mix: 3 MC, 2 free response."
        ),

        "practice_problems": [
            {"problem": "Find d/dx[integral from 0 to x^2 of sin(t) dt].", "answer": "sin(x^2) * 2x (FTC Part 1 with chain rule)"},
            {"problem": "integral from 1 to e of (2/x + 3x) dx", "answer": "[2*ln(x) + 3x^2/2]|_1^e = 2 + 3e^2/2 - 3/2"},
        ],

        "common_mistakes": [
            "Mixing up derivative and integral formulas (especially signs for trig)",
            "Forgetting +C on indefinite integrals",
            "Not recognizing when to use u-substitution vs direct integration",
        ],

        "builds_toward": [],
    },
}
