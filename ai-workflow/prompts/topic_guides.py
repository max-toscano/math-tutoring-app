"""
topic_guides.py
Structured teaching content for all curricula.

Each topic guide contains everything the prompt builder needs to assemble
a phase-aware system prompt: teaching content (chunked), key concepts (for quiz
coverage), practice problems, quiz guidelines, and common mistakes.

The prompt builder reads from TOPIC_GUIDES[slug] and injects the
relevant sections into the system prompt based on the current phase.

Currently covers:
  - Trigonometry: Chapter 1 (Foundations — Angles and Their Measurement)
  - Calculus 1: All 13 chapters (66 topics)
"""

# ─── Types ──────────────────────────────────────────────────────────────────
# Each topic guide follows this structure:
#
#   id:                     "1.1" — human-readable position
#   slug:                   "what-is-an-angle" — matches frontend + backend slugs
#   title:                  Display name
#   chapter:                Chapter slug
#   chapter_title:          Chapter display name
#   subject:                "trigonometry"
#   prerequisites:          List of topic slugs the student should have completed
#   estimated_time:         "8-12 minutes"
#   difficulty:             "Easy" | "Medium" | "Hard"
#   teaching_content:       The full teaching material, broken into labeled chunks
#   key_concepts:           Concept slugs — the quiz MUST test each of these
#   available_images:       [{id, description}] — image IDs the AI can reference
#   quiz_guidelines:        What the quiz should cover and question mix
#   practice_problems:      Example problems with answers for the practice phase
#   common_mistakes:        Typical student errors the AI should watch for
#   builds_toward:          Topic slugs that depend on this knowledge


# ─── Chapter 1: Foundations — Angles and Their Measurement ──────────────────

TOPIC_GUIDES: dict[str, dict] = {

    # ── 1.1 What Is an Angle? ──────────────────────────────────────────────
    "what-is-an-angle": {
        "id": "1.1",
        "slug": "what-is-an-angle",
        "title": "What Is an Angle?",
        "chapter": "angles-and-measurement",
        "chapter_title": "Foundations — Angles and Their Measurement",
        "subject": "trigonometry",
        "prerequisites": [],
        "estimated_time": "8-12 minutes",
        "difficulty": "Easy",

        "teaching_content": (
            "CHUNK 1 — What an angle actually is:\n\n"
            "An angle is formed when two rays (or line segments) share a common "
            "starting point. That shared starting point is called the vertex. The "
            "two rays are called the sides of the angle.\n\n"
            "Think of it like opening a book — the spine is the vertex, and the "
            "two covers are the sides. How far you open the book is the angle.\n\n"
            "Key vocabulary:\n"
            "- Vertex — the point where the two rays meet\n"
            "- Sides — the two rays that form the angle\n"
            "- Interior — the space between the two sides\n\n"
            "We name angles using three points (like angle ABC where B is the vertex), "
            "or just by the vertex letter (angle B), or with a number (angle 1).\n\n"
            "---\n\n"
            "CHUNK 2 — Standard position and rotation:\n\n"
            "In trigonometry, we place angles on the coordinate plane in standard position:\n"
            "- The vertex sits at the origin (0, 0)\n"
            "- One side lies along the positive x-axis — this is called the initial side "
            "(it never moves)\n"
            "- The other side is called the terminal side — this is the side that rotates\n\n"
            "The angle measures HOW MUCH the terminal side has rotated away from the "
            "initial side.\n\n"
            "Direction of rotation matters:\n"
            "- Counterclockwise rotation = positive angle\n"
            "- Clockwise rotation = negative angle\n\n"
            "This is a convention in math — counterclockwise is the 'positive' direction. "
            "A 90 degree angle means the terminal side rotated 90 degrees counterclockwise "
            "from the positive x-axis. A -90 degree angle means it rotated 90 degrees "
            "clockwise.\n\n"
            "---\n\n"
            "CHUNK 3 — Types of angles:\n\n"
            "Angles are classified by their size:\n"
            "- Acute angle — greater than 0 degrees and less than 90 degrees\n"
            "- Right angle — exactly 90 degrees (marked with a small square)\n"
            "- Obtuse angle — greater than 90 degrees and less than 180 degrees\n"
            "- Straight angle — exactly 180 degrees (a flat line)\n"
            "- Reflex angle — greater than 180 degrees and less than 360 degrees\n\n"
            "Two special angle relationships:\n"
            "- Complementary angles — two angles that add up to 90 degrees "
            "(they 'complete' a right angle)\n"
            "- Supplementary angles — two angles that add up to 180 degrees "
            "(they 'supplement' to a straight line)\n\n"
            "Example: If one angle is 35 degrees, its complement is 55 degrees "
            "(because 35 + 55 = 90) and its supplement is 145 degrees "
            "(because 35 + 145 = 180)."
        ),

        "key_concepts": [
            "angle_definition",
            "vertex_and_sides",
            "standard_position",
            "initial_side_terminal_side",
            "positive_negative_rotation",
            "angle_types_acute_right_obtuse_straight_reflex",
            "complementary_angles",
            "supplementary_angles",
        ],

        "available_images": [
            {"id": "1_1_angle_parts_labeled", "description": "An angle with vertex, initial side, and terminal side clearly labeled"},
            {"id": "1_1_positive_negative_rotation", "description": "Two angles showing counterclockwise (+) and clockwise (-) rotation"},
            {"id": "1_1_angle_types", "description": "Five angles: acute, right, obtuse, straight, reflex, each labeled"},
            {"id": "1_1_complementary_supplementary", "description": "Two diagrams showing angles adding to 90 degrees and 180 degrees"},
        ],

        "quiz_guidelines": (
            "Test: identifying vertex/sides, standard position, positive vs negative "
            "rotation, classifying angles by measurement, finding complements/supplements. "
            "Mix: 3 MC, 2 free response."
        ),

        "practice_problems": [
            {"problem": "What is the complement of 53 degrees?", "answer": "37 degrees"},
            {"problem": "A terminal side rotated clockwise 45 degrees. Is the angle positive or negative?", "answer": "Negative, -45 degrees"},
            {"problem": "Classify the angle 200 degrees.", "answer": "Reflex angle"},
        ],

        "common_mistakes": [
            "Thinking an angle must be less than 360 degrees",
            "Confusing which ray is the initial vs terminal side",
            "Forgetting that negative angles rotate clockwise",
            "Mixing up complementary (sum to 90) and supplementary (sum to 180)",
        ],

        "builds_toward": ["degree-measure", "radian-measure", "standard_position"],
    },

    # ── 1.2 Degree Measure ─────────────────────────────────────────────────
    "degree-measure": {
        "id": "1.2",
        "slug": "degree-measure",
        "title": "Degree Measure",
        "chapter": "angles-and-measurement",
        "chapter_title": "Foundations — Angles and Their Measurement",
        "subject": "trigonometry",
        "prerequisites": ["what-is-an-angle"],
        "estimated_time": "10-15 minutes",
        "difficulty": "Easy",

        "teaching_content": (
            "CHUNK 1 — The degree system:\n\n"
            "Degrees are the most common unit for measuring angles. The system works "
            "like this:\n"
            "- One full rotation (all the way around) = 360 degrees\n"
            "- A half rotation (straight line) = 180 degrees\n"
            "- A quarter rotation (right angle) = 90 degrees\n\n"
            "Why 360? The ancient Babylonians used a base-60 number system, and 360 is "
            "close to the number of days in a year. It also has many factors, making it "
            "easy to divide evenly.\n\n"
            "---\n\n"
            "CHUNK 2 — Degrees, minutes, and seconds (DMS):\n\n"
            "Degrees can be subdivided:\n"
            "- 1 degree = 60 minutes (symbol: ')\n"
            "- 1 minute = 60 seconds (symbol: \")\n\n"
            "An angle written as 47 degrees 23' 15\" means 47 degrees, 23 minutes, "
            "15 seconds. This is DMS notation.\n\n"
            "Converting DMS to decimal degrees:\n"
            "47 degrees 23' 15\" -> 47 + 23/60 + 15/3600 = 47.3875 degrees\n\n"
            "Converting decimal degrees to DMS:\n"
            "72.425 degrees -> 72 degrees (whole part), 0.425 * 60 = 25.5 -> 25', "
            "0.5 * 60 = 30 -> 30\" -> 72 degrees 25' 30\"\n\n"
            "---\n\n"
            "CHUNK 3 — Coterminal angles:\n\n"
            "Coterminal angles share the same terminal side in standard position. Find "
            "them by adding or subtracting 360 degrees.\n\n"
            "45 degrees and 405 degrees are coterminal (405 - 360 = 45).\n"
            "45 degrees and -315 degrees are coterminal (45 - 360 = -315).\n\n"
            "To find a coterminal angle between 0 degrees and 360 degrees: keep adding "
            "or subtracting 360 degrees until you land in range.\n\n"
            "Example: 750 degrees -> 750 - 360 = 390 -> 390 - 360 = 30 degrees\n"
            "Example: -200 degrees -> -200 + 360 = 160 degrees\n\n"
            "Every angle has infinitely many coterminal angles."
        ),

        "key_concepts": [
            "full_rotation_360",
            "why_360_degrees",
            "dms_notation",
            "dms_to_decimal_conversion",
            "decimal_to_dms_conversion",
            "coterminal_angles",
            "finding_coterminal_in_range",
        ],

        "available_images": [
            {"id": "1_2_full_half_quarter_rotation", "description": "Three circles showing 360 degrees, 180 degrees, 90 degrees"},
            {"id": "1_2_dms_breakdown", "description": "1 degree broken into 60 minutes, 1 minute broken into 60 seconds"},
            {"id": "1_2_coterminal_angles", "description": "Coordinate plane showing 45 degrees, 405 degrees, -315 degrees sharing a terminal side"},
        ],

        "quiz_guidelines": (
            "Test: full/half/quarter rotation values, DMS to decimal, decimal to DMS, "
            "finding coterminal angle, determining if two angles are coterminal. "
            "Mix: 2 MC, 3 free response."
        ),

        "practice_problems": [
            {"problem": "Convert 52 degrees 30' to decimal degrees.", "answer": "52.5 degrees"},
            {"problem": "Find a positive coterminal angle for -80 degrees.", "answer": "280 degrees"},
            {"problem": "Are 400 degrees and 40 degrees coterminal?", "answer": "Yes (400 - 360 = 40)"},
        ],

        "common_mistakes": [
            "Dividing minutes by 100 instead of 60 when converting DMS to decimal",
            "Adding 360 when the angle is already positive (getting further from 0-360 range)",
            "Forgetting that coterminal angles can be negative",
            "Confusing DMS subdivisions: 1 degree = 60 minutes, not 100",
        ],

        "builds_toward": ["radian-measure", "converting-degrees-radians", "coterminal_angles"],
    },

    # ── 1.3 Radian Measure ─────────────────────────────────────────────────
    "radian-measure": {
        "id": "1.3",
        "slug": "radian-measure",
        "title": "Radian Measure",
        "chapter": "angles-and-measurement",
        "chapter_title": "Foundations — Angles and Their Measurement",
        "subject": "trigonometry",
        "prerequisites": ["what-is-an-angle", "degree-measure"],
        "estimated_time": "10-15 minutes",
        "difficulty": "Easy",

        "teaching_content": (
            "CHUNK 1 — What is a radian?\n\n"
            "A radian is a different way to measure angles — one that comes from the "
            "circle itself. Definition: 1 radian is the angle you get when the arc "
            "length equals the radius.\n\n"
            "Picture a circle with radius r. Measure out an arc along the edge that is "
            "exactly r units long. The central angle that covers that arc is exactly "
            "1 radian. 1 radian is approximately 57.3 degrees.\n\n"
            "---\n\n"
            "CHUNK 2 — Radians and the full circle:\n\n"
            "Circumference = 2*pi*r. If 1 radian covers an arc of length r, then: "
            "2*pi*r / r = 2*pi radians in a full circle.\n\n"
            "The key relationship: pi radians = 180 degrees\n\n"
            "From this:\n"
            "- Full rotation: 2*pi rad = 360 degrees\n"
            "- Half rotation: pi rad = 180 degrees\n"
            "- Quarter rotation: pi/2 rad = 90 degrees\n"
            "- pi/3 rad = 60 degrees, pi/4 rad = 45 degrees, pi/6 rad = 30 degrees\n\n"
            "---\n\n"
            "CHUNK 3 — Why radians matter:\n\n"
            "1. Simpler formulas — Arc length is just s = r*theta (no conversion factor)\n"
            "2. Calculus needs them — d/dx sin(x) = cos(x) only works in radians\n"
            "3. They're dimensionless — a radian is a ratio (arc / radius), units cancel\n\n"
            "Notation: When an angle has no degree symbol, it's in radians. theta = 2 "
            "means 2 radians, not 2 degrees.\n\n"
            "---\n\n"
            "CHUNK 4 — Common radian values to know:\n\n"
            "0 degrees = 0, 30 degrees = pi/6, 45 degrees = pi/4, 60 degrees = pi/3, "
            "90 degrees = pi/2, 120 degrees = 2*pi/3, 135 degrees = 3*pi/4, "
            "150 degrees = 5*pi/6, 180 degrees = pi, 270 degrees = 3*pi/2, "
            "360 degrees = 2*pi\n\n"
            "Pattern: the denominator tells you the slice size (6 -> 30 degrees, "
            "4 -> 45 degrees, 3 -> 60 degrees). The numerator counts how many slices."
        ),

        "key_concepts": [
            "radian_definition",
            "arc_length_equals_radius",
            "full_revolution_2pi",
            "pi_equals_180_degrees",
            "why_radians_matter",
            "radians_are_dimensionless",
            "common_radian_values",
            "no_symbol_means_radians",
        ],

        "available_images": [
            {"id": "1_3_radian_definition", "description": "Circle with radius r, arc of length r, 1 radian angle labeled"},
            {"id": "1_3_full_circle_2pi", "description": "Circle showing approximately 6.28 radius-length arcs fitting around circumference"},
            {"id": "1_3_common_radian_values", "description": "Circle with key angles marked in both degrees and radians"},
        ],

        "quiz_guidelines": (
            "Test: definition of 1 radian, how many radians in full circle, pi = 180 degrees "
            "relationship, recognizing common radian values, why radians are used. "
            "Mix: 3 MC, 2 free response."
        ),

        "practice_problems": [
            {"problem": "How many radians in a half rotation?", "answer": "pi (approximately 3.14159)"},
            {"problem": "What does 1 radian mean geometrically?", "answer": "The angle where the arc length equals the radius"},
            {"problem": "Is pi/4 bigger or smaller than 1 radian?", "answer": "Smaller (pi/4 is approximately 0.785)"},
        ],

        "common_mistakes": [
            "Thinking pi radians = 360 degrees (it's 180 degrees)",
            "Writing the degree symbol when giving an answer in radians",
            "Confusing pi/3 (60 degrees) with pi/6 (30 degrees)",
            "Not recognizing that an angle without a degree symbol is in radians",
        ],

        "builds_toward": ["converting-degrees-radians", "arc-length-sector-area", "angular-linear-speed"],
    },

    # ── 1.4 Converting Between Degrees and Radians ─────────────────────────
    "converting-degrees-radians": {
        "id": "1.4",
        "slug": "converting-degrees-radians",
        "title": "Converting Between Degrees and Radians",
        "chapter": "angles-and-measurement",
        "chapter_title": "Foundations — Angles and Their Measurement",
        "subject": "trigonometry",
        "prerequisites": ["degree-measure", "radian-measure"],
        "estimated_time": "10-12 minutes",
        "difficulty": "Easy",

        "teaching_content": (
            "CHUNK 1 — The conversion factor:\n\n"
            "Everything comes from: pi radians = 180 degrees\n\n"
            "Two conversion factors:\n"
            "- Degrees to Radians: multiply by pi/180\n"
            "- Radians to Degrees: multiply by 180/pi\n\n"
            "How to remember: Degrees to Radians = divide by 180 (going to a smaller "
            "number). Radians to Degrees = multiply by 180 (going to a bigger number).\n\n"
            "---\n\n"
            "CHUNK 2 — Degrees to radians (worked examples):\n\n"
            "Example 1: 60 degrees * (pi/180) = 60*pi/180 = pi/3 radians\n"
            "Example 2: 150 degrees * (pi/180) = 150*pi/180 = 5*pi/6 radians\n"
            "Example 3: 200 degrees * (pi/180) = 200*pi/180 = 10*pi/9 radians\n\n"
            "Tip: The simplification step is just reducing a fraction.\n\n"
            "---\n\n"
            "CHUNK 3 — Radians to degrees (worked examples):\n\n"
            "Example 1: (pi/4) * (180/pi) = 180/4 = 45 degrees\n"
            "Example 2: (5*pi/3) * (180/pi) = 900/3 = 300 degrees\n"
            "Example 3: 2 radians * (180/pi) = 360/pi approximately 114.59 degrees "
            "(no pi to cancel — decimal answer)\n\n"
            "---\n\n"
            "CHUNK 4 — Common mistakes:\n\n"
            "Mistake 1: Not simplifying. 120*pi/180 should be reduced to 2*pi/3.\n"
            "Mistake 2: Multiplying by wrong factor. If your radians answer is huge, "
            "you multiplied by 180 instead of dividing.\n"
            "Mistake 3: The pi only cancels when the radian value already contains pi.\n\n"
            "Quick check: 90 degrees is approximately 1.57 rad, 1 rad is approximately "
            "57 degrees. If your answer doesn't pass a reasonableness check, redo it."
        ),

        "key_concepts": [
            "pi_over_180_conversion_factor",
            "180_over_pi_conversion_factor",
            "degrees_to_radians_method",
            "radians_to_degrees_method",
            "simplifying_radian_fractions",
            "pi_cancellation",
            "conversion_without_pi",
            "reasonableness_check",
        ],

        "available_images": [
            {"id": "1_4_conversion_diagram", "description": "Two-way arrow: Degrees <-> Radians, with *pi/180 and *180/pi labeled"},
            {"id": "1_4_common_conversions_table", "description": "Full table of common angles in both degrees and radians"},
        ],

        "quiz_guidelines": (
            "Test: deg->rad standard angle, deg->rad non-standard, rad->deg with pi, "
            "rad->deg without pi, identifying correct conversion factor. "
            "Mix: 2 MC, 3 free response."
        ),

        "practice_problems": [
            {"problem": "Convert 270 degrees to radians.", "answer": "3*pi/2"},
            {"problem": "Convert 2*pi/3 to degrees.", "answer": "120 degrees"},
            {"problem": "A student converts 45 degrees and gets 45*pi. What went wrong?", "answer": "They forgot to divide by 180"},
        ],

        "common_mistakes": [
            "Multiplying by 180 instead of dividing (or vice versa)",
            "Forgetting to simplify the fraction after multiplying by pi/180",
            "Expecting pi to cancel when converting a pure number (like 2 radians) to degrees",
            "Leaving answer as 120*pi/180 instead of reducing to 2*pi/3",
        ],

        "builds_toward": ["arc-length-sector-area", "angular-linear-speed", "six-trig-ratios"],
    },

    # ── 1.5 Arc Length and Sector Area ─────────────────────────────────────
    "arc-length-sector-area": {
        "id": "1.5",
        "slug": "arc-length-sector-area",
        "title": "Arc Length and Sector Area",
        "chapter": "angles-and-measurement",
        "chapter_title": "Foundations — Angles and Their Measurement",
        "subject": "trigonometry",
        "prerequisites": ["radian-measure", "converting-degrees-radians"],
        "estimated_time": "12-15 minutes",
        "difficulty": "Medium",

        "teaching_content": (
            "CHUNK 1 — Arc length formula:\n\n"
            "An arc is a portion of a circle's circumference. If you know the radius "
            "and central angle (in radians):\n\n"
            "s = r * theta\n\n"
            "Where s = arc length, r = radius, theta = central angle IN RADIANS.\n\n"
            "Why: 1 radian = angle where arc equals radius. So arc scales linearly "
            "with the angle.\n\n"
            "Example 1: r = 5 cm, theta = pi/3 -> s = 5*(pi/3) = 5*pi/3 "
            "approximately 5.24 cm\n"
            "Example 2: r = 10 in, theta = 2 -> s = 10*2 = 20 inches\n\n"
            "If the angle is in degrees, convert to radians first.\n\n"
            "---\n\n"
            "CHUNK 2 — Finding radius or angle from arc length:\n\n"
            "theta = s/r (find the angle)\n"
            "r = s/theta (find the radius)\n\n"
            "Example 3: Arc is 12 cm, radius is 8 cm. theta = 12/8 = 1.5 radians "
            "(approximately 85.9 degrees)\n"
            "Example 4: Arc is 6*pi m, angle is pi/2. r = 6*pi / (pi/2) = 12 meters\n\n"
            "---\n\n"
            "CHUNK 3 — Sector area formula:\n\n"
            "A sector is a 'pizza slice' — the region between two radii and an arc.\n\n"
            "A = (1/2) * r^2 * theta\n\n"
            "Why: Full circle area is pi*r^2. Sector is fraction theta/(2*pi) of full "
            "circle. So A = (theta/(2*pi)) * (pi*r^2) = (1/2)*r^2*theta.\n\n"
            "Example 5: r = 6 cm, theta = pi/4 -> A = (1/2)*(36)*(pi/4) = 9*pi/2 "
            "approximately 14.14 cm^2\n"
            "Example 6: Pizza diameter 16 in, slice angle 45 degrees. Convert: "
            "45 degrees = pi/4. r = 8. A = (1/2)*(64)*(pi/4) = 8*pi "
            "approximately 25.13 sq in\n\n"
            "---\n\n"
            "CHUNK 4 — Applications:\n\n"
            "Clock: 10-inch minute hand, 25 minutes. theta = (25/60)*(2*pi) = 5*pi/6. "
            "s = 10*(5*pi/6) = 50*pi/6 approximately 26.18 inches.\n\n"
            "Wiper: 18 inches, sweeps 120 degrees = 2*pi/3. Arc: s = 18*(2*pi/3) = 12*pi. "
            "Area cleaned: A = (1/2)*(324)*(2*pi/3) = 108*pi.\n\n"
            "Always check: angle must be in radians before using formulas."
        ),

        "key_concepts": [
            "arc_length_formula_s_equals_r_theta",
            "angle_must_be_in_radians",
            "finding_angle_from_arc_length",
            "finding_radius_from_arc_length",
            "sector_area_formula",
            "sector_as_fraction_of_circle",
            "degree_to_radian_before_formula",
            "real_world_arc_length_applications",
        ],

        "available_images": [
            {"id": "1_5_arc_length_diagram", "description": "Circle with r, theta, and arc s labeled, formula shown"},
            {"id": "1_5_sector_area_diagram", "description": "Shaded pizza-slice sector with r, theta, s, formula A = (1/2)*r^2*theta"},
            {"id": "1_5_clock_example", "description": "Clock face showing minute hand sweep with arc highlighted"},
        ],

        "quiz_guidelines": (
            "Test: arc length given r and theta in radians, arc length with degrees "
            "(must convert), finding angle or radius from other values, sector area, "
            "applied problem. Mix: 2 MC, 3 free response."
        ),

        "practice_problems": [
            {"problem": "r = 9 cm, theta = 2*pi/3. Find the arc length.", "answer": "6*pi approximately 18.85 cm"},
            {"problem": "r = 5, theta = 72 degrees. Find the sector area.", "answer": "Convert 72 degrees = 2*pi/5. A = (1/2)*(25)*(2*pi/5) = 5*pi"},
            {"problem": "Arc length = 15, radius = 6. Find the central angle in radians.", "answer": "theta = 15/6 = 2.5 radians"},
        ],

        "common_mistakes": [
            "Using degrees in s = r*theta without converting to radians first",
            "Confusing arc length (s = r*theta) with sector area (A = (1/2)*r^2*theta)",
            "Forgetting to square the radius in the sector area formula",
            "Using diameter instead of radius in the formulas",
        ],

        "builds_toward": ["angular-linear-speed", "defining-unit-circle", "arc-length-surface-area"],
    },

    # ── 1.6 Angular and Linear Speed ───────────────────────────────────────
    "angular-linear-speed": {
        "id": "1.6",
        "slug": "angular-linear-speed",
        "title": "Angular and Linear Speed",
        "chapter": "angles-and-measurement",
        "chapter_title": "Foundations — Angles and Their Measurement",
        "subject": "trigonometry",
        "prerequisites": ["radian-measure", "arc-length-sector-area"],
        "estimated_time": "12-15 minutes",
        "difficulty": "Medium",

        "teaching_content": (
            "CHUNK 1 — Angular speed:\n\n"
            "When something spins, it covers angle per unit time. This is angular speed.\n\n"
            "omega = theta/t\n\n"
            "Where omega = angular speed, theta = angle in radians, t = time. "
            "Units: rad/s.\n\n"
            "Example 1: 10 full rotations in 5 seconds. theta = 10 * 2*pi = 20*pi. "
            "omega = 20*pi/5 = 4*pi rad/s.\n\n"
            "Converting RPM to rad/s: omega = RPM * 2*pi/60\n"
            "Example 2: 3000 RPM -> omega = 3000 * 2*pi/60 = 100*pi rad/s\n\n"
            "---\n\n"
            "CHUNK 2 — Linear speed:\n\n"
            "A point on the edge of a spinning object travels actual distance. "
            "Linear speed = distance/time.\n\n"
            "Since arc length s = r*theta: v = s/t = r*theta/t = r*(theta/t) = r*omega\n\n"
            "v = r * omega\n\n"
            "Where v = linear speed, r = radius (distance from center), "
            "omega = angular speed.\n\n"
            "---\n\n"
            "CHUNK 3 — The relationship:\n\n"
            "All points on a spinning object share the same omega, but have different "
            "v depending on distance from center.\n\n"
            "Example 3: Merry-go-round at 2 rad/s. Child at r=3: v = 6 m/s. "
            "Child at r=5: v = 10 m/s. Same angular speed, different linear speeds.\n\n"
            "---\n\n"
            "CHUNK 4 — Applications:\n\n"
            "Car tire: radius 14 in, 800 RPM. omega = 800 * 2*pi/60 = 80*pi/3 rad/s. "
            "v = 14 * 80*pi/3 = 1120*pi/3 in/s approximately 66.7 mph after unit "
            "conversion.\n\n"
            "Gears: When meshed, linear speed at edges is equal. r1*omega1 = r2*omega2. "
            "Smaller gear spins faster.\n\n"
            "Earth: 1 rotation in 24 hours -> omega = 2*pi/24 = pi/12 rad/hr. "
            "At equator (r approximately 3960 mi): v approximately 1036.7 mph. "
            "At 40 degrees latitude: v approximately 793.9 mph."
        ),

        "key_concepts": [
            "angular_speed_definition",
            "omega_equals_theta_over_t",
            "rpm_to_radians_conversion",
            "linear_speed_definition",
            "v_equals_r_omega",
            "same_angular_different_linear",
            "radius_affects_linear_speed",
            "gear_speed_relationship",
            "real_world_speed_applications",
        ],

        "available_images": [
            {"id": "1_6_angular_speed_diagram", "description": "Spinning wheel with theta and omega = theta/t labeled"},
            {"id": "1_6_linear_vs_angular", "description": "Disk with two points at different radii, same omega, different v"},
            {"id": "1_6_gear_relationship", "description": "Two meshed gears, smaller one faster, equal linear speed at contact"},
        ],

        "quiz_guidelines": (
            "Test: angular speed from rotations and time, RPM to rad/s, linear speed "
            "(v=r*omega), comparing linear speeds at different radii, applied problem. "
            "Mix: 2 MC, 3 free response."
        ),

        "practice_problems": [
            {"problem": "A fan spins at 120 RPM. Find omega in rad/s.", "answer": "4*pi rad/s"},
            {"problem": "Ferris wheel r=25 ft, omega = pi/10 rad/s. Find the rider's linear speed.", "answer": "5*pi/2 approximately 7.85 ft/s"},
            {"problem": "Gear A: r=6 cm, omega=100 rad/s. Gear B: r=10 cm. Find omega for Gear B.", "answer": "60 rad/s (r1*omega1 = r2*omega2)"},
        ],

        "common_mistakes": [
            "Forgetting to convert RPM to rad/s (must multiply by 2*pi/60)",
            "Using degrees per second instead of radians per second in v = r*omega",
            "Thinking all points on a spinning object have the same linear speed",
            "Mixing up which gear spins faster (smaller gear = faster angular speed)",
        ],

        "builds_toward": ["six-trig-ratios", "defining-unit-circle", "simple-harmonic-motion"],
    },
}


# ─── Helper Functions ───────────────────────────────────────────────────────

def get_topic_guide(slug: str) -> dict | None:
    """Look up a topic guide by its slug. Returns None if not found."""
    return TOPIC_GUIDES.get(slug)


def get_chapter_guides(chapter_slug: str) -> list[dict]:
    """Get all topic guides for a chapter, sorted by id."""
    guides = [g for g in TOPIC_GUIDES.values() if g["chapter"] == chapter_slug]
    return sorted(guides, key=lambda g: g["id"])


def get_key_concepts(slug: str) -> list[str]:
    """Get the key concept slugs for a topic. Returns empty list if not found."""
    guide = TOPIC_GUIDES.get(slug)
    return guide["key_concepts"] if guide else []


# ─── Merge Calculus 1 Topic Guides ─────────────────────────────────────────
# Each chapter range is in its own file to keep files manageable.

try:
    from prompts.calc1_guides_ch1_4 import CALC1_GUIDES_CH1_4
    TOPIC_GUIDES.update(CALC1_GUIDES_CH1_4)
except ImportError:
    pass

try:
    from prompts.calc1_guides_ch5_7 import CALC1_GUIDES_CH5_7
    TOPIC_GUIDES.update(CALC1_GUIDES_CH5_7)
except ImportError:
    pass

try:
    from prompts.calc1_guides_ch8_10 import CALC1_GUIDES_CH8_10
    TOPIC_GUIDES.update(CALC1_GUIDES_CH8_10)
except ImportError:
    pass

try:
    from prompts.calc1_guides_ch11_13 import CALC1_GUIDES_CH11_13
    TOPIC_GUIDES.update(CALC1_GUIDES_CH11_13)
except ImportError:
    pass
