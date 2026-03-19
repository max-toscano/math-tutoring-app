/**
 * math.ts — Math curriculum: all math subjects and topics.
 *
 * One of potentially many curriculum files (math, chemistry, physics, etc.).
 * Each curriculum file exports a SUBJECTS array following the shared types from index.ts.
 *
 * Trigonometry uses the chapter hierarchy (13 chapters × 4-6 sub-chapters = 73 lessons).
 * Calculus 1 uses the chapter hierarchy (13 chapters × 4-6 sub-chapters = 66 lessons).
 * Other subjects use a flat topic list (7 topics each).
 */

import { Colors } from '../Colors';
import type { Subject } from './index';

export const MATH_SUBJECTS: Subject[] = [
  {
    slug: 'trigonometry',
    name: 'Trigonometry',
    emoji: '🔺',
    color: Colors.orange,
    bgColor: '#FFF4E6',
    description: 'Full course — 13 chapters',
    topics: [], // chaptered subject — topics live inside chapters
    chapters: [
      {
        slug: 'angles-and-measurement',
        name: 'Foundations — Angles and Their Measurement',
        description: 'Degrees, radians, arc length, and angular speed',
        topics: [
          { slug: 'what-is-an-angle', name: 'What Is an Angle?', description: 'Defining angles, initial and terminal sides, standard position' },
          { slug: 'degree-measure', name: 'Degree Measure', description: 'Degrees, minutes, seconds, and DMS conversions' },
          { slug: 'radian-measure', name: 'Radian Measure', description: 'Defining radians and why they matter' },
          { slug: 'converting-degrees-radians', name: 'Converting Between Degrees and Radians', description: 'The conversion factor pi/180 and its applications' },
          { slug: 'arc-length-sector-area', name: 'Arc Length and Sector Area', description: 'Formulas s = r*theta and A = (1/2)*r^2*theta' },
          { slug: 'angular-linear-speed', name: 'Angular and Linear Speed', description: 'Relating angular velocity to linear velocity' },
        ],
      },
      {
        slug: 'right-triangle-trig',
        name: 'Right Triangle Trigonometry',
        description: 'SOH-CAH-TOA, special triangles, and applications',
        topics: [
          { slug: 'six-trig-ratios', name: 'The Six Trigonometric Ratios', description: 'Sin, cos, tan, csc, sec, cot from a right triangle' },
          { slug: 'evaluating-trig-acute', name: 'Evaluating Trig Functions of Acute Angles', description: 'Computing exact values using triangles' },
          { slug: 'special-right-triangles', name: 'Special Right Triangles', description: '30-60-90 and 45-45-90 triangles' },
          { slug: 'cofunctions-complementary', name: 'Cofunctions and Complementary Angles', description: 'sin(A) = cos(90 - A) and related identities' },
          { slug: 'solving-right-triangles', name: 'Solving Right Triangles', description: 'Finding all sides and angles given partial information' },
          { slug: 'right-triangle-applications', name: 'Applications of Right Triangle Trigonometry', description: 'Angles of elevation/depression, bearings, real-world problems' },
        ],
      },
      {
        slug: 'unit-circle',
        name: 'The Unit Circle',
        description: 'Defining trig functions for any angle',
        topics: [
          { slug: 'defining-unit-circle', name: 'Defining the Unit Circle', description: 'x^2 + y^2 = 1 and coordinates as trig values' },
          { slug: 'trig-any-angle', name: 'Trig Functions for Any Angle', description: 'Extending definitions beyond acute angles' },
          { slug: 'reference-angles', name: 'Reference Angles', description: 'Finding the reference angle in any quadrant' },
          { slug: 'memorizing-unit-circle', name: 'Memorizing the Unit Circle', description: 'Patterns and tricks for quick recall' },
          { slug: 'quadrantal-angles', name: 'Quadrantal Angles', description: 'Trig values at 0, 90, 180, 270 degrees' },
          { slug: 'unit-circle-expressions', name: 'Using the Unit Circle to Evaluate Expressions', description: 'Combining unit circle values in complex expressions' },
        ],
      },
      {
        slug: 'trig-as-functions',
        name: 'Trigonometric Functions as Functions',
        description: 'Domain, range, even/odd, periodicity',
        topics: [
          { slug: 'domain-and-range', name: 'Domain and Range', description: 'Input/output restrictions for each trig function' },
          { slug: 'even-odd-trig', name: 'Even and Odd Trig Functions', description: 'Symmetry properties: cos(-x) = cos(x), sin(-x) = -sin(x)' },
          { slug: 'periodicity', name: 'Periodicity', description: 'Period of each trig function and why it matters' },
          { slug: 'fundamental-identities-intro', name: 'Fundamental Identities — First Look', description: 'Pythagorean, reciprocal, and quotient identities' },
        ],
      },
      {
        slug: 'graphing-trig',
        name: 'Graphs of Trigonometric Functions',
        description: 'Amplitude, period, phase shift, and modeling',
        topics: [
          { slug: 'graphing-sine-cosine', name: 'Graphing Sine and Cosine', description: 'Basic shapes, key points, and one full cycle' },
          { slug: 'amplitude-vertical-shift', name: 'Transformations — Amplitude and Vertical Shift', description: 'Stretching vertically and shifting up/down' },
          { slug: 'period-phase-shift', name: 'Transformations — Period and Phase Shift', description: 'Compressing horizontally and shifting left/right' },
          { slug: 'graphing-tan-cot', name: 'Graphing Tangent and Cotangent', description: 'Vertical asymptotes, period pi, and transformations' },
          { slug: 'graphing-sec-csc', name: 'Graphing Secant and Cosecant', description: 'Reciprocal graphs from sine and cosine' },
          { slug: 'sinusoidal-modeling', name: 'Sinusoidal Modeling', description: 'Modeling real-world periodic data with trig functions' },
        ],
      },
      {
        slug: 'inverse-trig',
        name: 'Inverse Trigonometric Functions',
        description: 'Arcsine, arccosine, arctangent and compositions',
        topics: [
          { slug: 'restricted-domains', name: 'Why Inverses Require Restricted Domains', description: 'The horizontal line test and one-to-one functions' },
          { slug: 'arcsine', name: 'Arcsine', description: 'Domain [-1,1], range [-pi/2, pi/2], and evaluation' },
          { slug: 'arccosine', name: 'Arccosine', description: 'Domain [-1,1], range [0, pi], and evaluation' },
          { slug: 'arctangent', name: 'Arctangent', description: 'Domain all reals, range (-pi/2, pi/2), and evaluation' },
          { slug: 'inverse-csc-sec-cot', name: 'Inverse Cosecant, Secant, and Cotangent', description: 'Definitions, domains, and ranges of the remaining inverses' },
          { slug: 'compositions-trig-inverse', name: 'Compositions of Trig and Inverse Trig Functions', description: 'Simplifying expressions like sin(arccos(x))' },
        ],
      },
      {
        slug: 'trig-identities',
        name: 'Trigonometric Identities',
        description: 'Proving identities and advanced formulas',
        topics: [
          { slug: 'fundamental-identities-review', name: 'Review of Fundamental Identities', description: 'Pythagorean, reciprocal, quotient — full toolkit' },
          { slug: 'proving-identities', name: 'Proving (Verifying) Identities', description: 'Strategies for showing two sides are equal' },
          { slug: 'sum-difference-identities', name: 'Sum and Difference Identities', description: 'sin(A +/- B), cos(A +/- B), tan(A +/- B)' },
          { slug: 'double-angle-identities', name: 'Double-Angle Identities', description: 'sin(2A), cos(2A), tan(2A) and their derivations' },
          { slug: 'half-angle-identities', name: 'Half-Angle Identities', description: 'sin(A/2), cos(A/2), tan(A/2) formulas' },
          { slug: 'product-sum-identities', name: 'Product-to-Sum and Sum-to-Product Identities', description: 'Converting between products and sums of trig functions' },
        ],
      },
      {
        slug: 'trig-equations',
        name: 'Trigonometric Equations',
        description: 'Solving equations and finding all solutions',
        topics: [
          { slug: 'basic-trig-equations', name: 'Solving Basic Trig Equations', description: 'Finding solutions on [0, 2pi) and general solutions' },
          { slug: 'single-trig-function', name: 'Equations Involving a Single Trig Function', description: 'Algebraic techniques for isolating trig expressions' },
          { slug: 'equations-requiring-identities', name: 'Equations Requiring Identities', description: 'Using identities to simplify before solving' },
          { slug: 'multiple-angle-equations', name: 'Equations with Multiple Angles', description: 'Solving sin(2x) = ..., cos(3x) = ..., etc.' },
          { slug: 'equations-inverse-trig', name: 'Equations Involving Inverse Trig Functions', description: 'Working with arcsin, arccos, arctan in equations' },
          { slug: 'trig-equation-applications', name: 'Applications of Trig Equations', description: 'Real-world problems requiring trig equation solutions' },
        ],
      },
      {
        slug: 'law-of-sines-cosines',
        name: 'The Laws of Sines and Cosines',
        description: 'Solving oblique triangles',
        topics: [
          { slug: 'when-right-triangle-fails', name: "When Right-Triangle Methods Aren't Enough", description: 'Recognizing when you need the law of sines or cosines' },
          { slug: 'law-of-sines', name: 'The Law of Sines', description: 'a/sin(A) = b/sin(B) = c/sin(C) and AAS/ASA cases' },
          { slug: 'ambiguous-case', name: 'The Ambiguous Case — Deep Dive', description: 'SSA and when 0, 1, or 2 triangles exist' },
          { slug: 'law-of-cosines', name: 'The Law of Cosines', description: 'c^2 = a^2 + b^2 - 2ab*cos(C) and SAS/SSS cases' },
          { slug: 'triangle-area', name: 'Area of a Triangle', description: "Heron's formula and A = (1/2)*ab*sin(C)" },
          { slug: 'oblique-triangle-applications', name: 'Applications of Oblique Triangles', description: 'Navigation, surveying, and real-world triangle problems' },
        ],
      },
      {
        slug: 'vectors-and-trig',
        name: 'Vectors and Trigonometry',
        description: 'Vector operations, dot product, and applications',
        topics: [
          { slug: 'intro-to-vectors', name: 'Introduction to Vectors', description: 'Magnitude, direction, and geometric representation' },
          { slug: 'vector-operations', name: 'Vector Operations', description: 'Addition, subtraction, and scalar multiplication' },
          { slug: 'unit-vectors-direction', name: 'Unit Vectors and Direction Angles', description: 'Finding unit vectors and angles with the positive x-axis' },
          { slug: 'dot-product', name: 'The Dot Product', description: 'Definition, properties, and finding angles between vectors' },
          { slug: 'vector-projections-work', name: 'Vector Projections and Work', description: 'Projecting one vector onto another and computing work' },
          { slug: 'vector-applications', name: 'Applications of Vectors', description: 'Force, velocity, and other physical applications' },
        ],
      },
      {
        slug: 'polar-and-complex',
        name: 'Polar Coordinates and Complex Numbers',
        description: 'Polar form, complex numbers, and De Moivre\'s theorem',
        topics: [
          { slug: 'polar-coordinate-system', name: 'The Polar Coordinate System', description: 'Plotting points with (r, theta) and multiple representations' },
          { slug: 'polar-rectangular-conversion', name: 'Converting Between Polar and Rectangular', description: 'x = r*cos(theta), y = r*sin(theta) and the reverse' },
          { slug: 'polar-equation-graphs', name: 'Graphs of Polar Equations', description: 'Circles, roses, cardioids, limacons, and lemniscates' },
          { slug: 'complex-trig-form', name: 'Complex Numbers in Trigonometric (Polar) Form', description: 'z = r(cos(theta) + i*sin(theta))' },
          { slug: 'complex-multiply-divide', name: 'Multiplication and Division in Trigonometric Form', description: 'Multiply magnitudes, add/subtract angles' },
          { slug: 'demoivres-theorem', name: "De Moivre's Theorem and Roots of Complex Numbers", description: 'Powers and nth roots of complex numbers' },
        ],
      },
      {
        slug: 'parametric-and-applications',
        name: 'Parametric Equations and Trig Applications',
        description: 'Parametric curves, projectile motion, and harmonic motion',
        topics: [
          { slug: 'parametric-basics', name: 'Parametric Equations — Basics', description: 'Defining x(t) and y(t), eliminating the parameter' },
          { slug: 'parametric-trig-curves', name: 'Parametric Curves with Trigonometric Functions', description: 'Circles, ellipses, and Lissajous figures' },
          { slug: 'projectile-motion', name: 'Projectile Motion', description: 'Modeling trajectories with parametric trig equations' },
          { slug: 'simple-harmonic-motion', name: 'Simple Harmonic Motion', description: 'Springs, pendulums, and sinusoidal position functions' },
          { slug: 'combining-sinusoidal', name: 'Combining Sinusoidal Functions', description: 'Adding sinusoids with different frequencies and phases' },
        ],
      },
      {
        slug: 'additional-topics',
        name: 'Additional Topics and Course Wrap-Up',
        description: 'Calculus bridge, review, and problem-solving strategies',
        topics: [
          { slug: 'trig-substitution-preview', name: 'Trigonometric Substitution Preview', description: 'A bridge to calculus — how trig helps with integration' },
          { slug: 'hyperbolic-trig-intro', name: 'Hyperbolic Trig Functions — Brief Introduction', description: 'sinh, cosh, tanh and their connection to exponentials' },
          { slug: 'common-mistakes', name: 'Common Mistakes and How to Avoid Them', description: 'The most frequent trig errors and how to fix them' },
          { slug: 'problem-solving-strategies', name: 'Problem-Solving Strategies — Summary', description: 'A toolkit of approaches for any trig problem' },
          { slug: 'course-review', name: 'Course Review and Final Assessment Guide', description: 'Comprehensive review of all 13 chapters' },
        ],
      },
    ],
  },
  {
    slug: 'calc-1',
    name: 'Calculus 1',
    emoji: '∫',
    color: Colors.secondary,
    bgColor: '#FFF0F0',
    description: 'Full course — 13 chapters',
    topics: [],
    chapters: [
      {
        slug: 'functions-review',
        name: 'Functions and Their Properties',
        description: 'Domain, range, composition, transformations, and function types',
        topics: [
          { slug: 'functions-and-notation', name: 'Functions and Function Notation', description: 'What a function is, evaluating functions, vertical line test' },
          { slug: 'domain-and-range', name: 'Domain and Range', description: 'Finding input/output restrictions algebraically and graphically' },
          { slug: 'combining-functions', name: 'Combining Functions', description: 'Arithmetic operations and composition of functions' },
          { slug: 'transformations', name: 'Transformations of Functions', description: 'Shifts, reflections, stretches, and compressions' },
          { slug: 'polynomial-rational-functions', name: 'Polynomial and Rational Functions', description: 'Behavior, zeros, asymptotes, and end behavior' },
          { slug: 'transcendental-functions-review', name: 'Trig, Exponential, and Logarithmic Functions', description: 'Key properties and graphs you need for calculus' },
        ],
      },
      {
        slug: 'limits',
        name: 'Limits — The Foundation of Calculus',
        description: 'Intuitive and algebraic limits, limits at infinity, and the Squeeze Theorem',
        topics: [
          { slug: 'idea-of-a-limit', name: 'The Idea of a Limit', description: 'What it means for f(x) to approach L as x approaches c' },
          { slug: 'limits-from-graphs-tables', name: 'Finding Limits from Graphs and Tables', description: 'Reading limits visually and numerically' },
          { slug: 'limit-laws', name: 'Limit Laws and Algebraic Techniques', description: 'Sum, product, quotient laws, factoring, rationalizing, and direct substitution' },
          { slug: 'limits-involving-infinity', name: 'Limits Involving Infinity', description: 'Horizontal asymptotes, vertical asymptotes, and end behavior' },
          { slug: 'squeeze-theorem', name: 'The Squeeze Theorem', description: 'Bounding a function to find its limit, key examples like sin(x)/x' },
          { slug: 'epsilon-delta', name: 'The Formal Definition of a Limit', description: 'Epsilon-delta proofs — making limits rigorous' },
        ],
      },
      {
        slug: 'continuity',
        name: 'Continuity',
        description: 'Continuous functions, types of discontinuities, and the Intermediate Value Theorem',
        topics: [
          { slug: 'what-is-continuity', name: 'What Is Continuity?', description: 'The three conditions: f(c) exists, limit exists, they are equal' },
          { slug: 'types-of-discontinuities', name: 'Types of Discontinuities', description: 'Removable, jump, and infinite discontinuities' },
          { slug: 'continuity-on-interval', name: 'Continuity on an Interval', description: 'Left/right continuity, continuous on [a, b], common continuous functions' },
          { slug: 'intermediate-value-theorem', name: 'The Intermediate Value Theorem', description: 'If f is continuous on [a,b], it takes every value between f(a) and f(b)' },
        ],
      },
      {
        slug: 'defining-the-derivative',
        name: 'Defining the Derivative',
        description: 'Tangent lines, the limit definition, differentiability, and interpretation',
        topics: [
          { slug: 'tangent-lines-rates-of-change', name: 'Tangent Lines and Rates of Change', description: 'From secant lines to tangent lines — average vs. instantaneous rate' },
          { slug: 'derivative-at-a-point', name: 'The Derivative at a Point', description: 'The limit definition f\'(a) = lim[h->0] (f(a+h) - f(a))/h' },
          { slug: 'derivative-as-a-function', name: 'The Derivative as a Function', description: 'Computing f\'(x) for all x, derivative graphs, and notation' },
          { slug: 'differentiability-vs-continuity', name: 'Differentiability vs. Continuity', description: 'Differentiable implies continuous, but not the reverse' },
          { slug: 'interpreting-the-derivative', name: 'Interpreting the Derivative', description: 'Units, real-world meaning, and reading derivative graphs' },
        ],
      },
      {
        slug: 'differentiation-rules',
        name: 'Differentiation Rules',
        description: 'Power rule, product rule, quotient rule, and derivatives of trig functions',
        topics: [
          { slug: 'power-rule', name: 'The Power Rule', description: 'd/dx[x^n] = n*x^(n-1) for any real n' },
          { slug: 'constant-sum-difference-rules', name: 'Constant Multiple, Sum, and Difference Rules', description: 'Linearity of the derivative — break apart sums, pull out constants' },
          { slug: 'product-rule', name: 'The Product Rule', description: 'd/dx[f*g] = f\'*g + f*g\' — when two functions are multiplied' },
          { slug: 'quotient-rule', name: 'The Quotient Rule', description: 'd/dx[f/g] = (f\'*g - f*g\')/g^2 — when one function divides another' },
          { slug: 'derivatives-of-trig', name: 'Derivatives of Trigonometric Functions', description: 'd/dx[sin x] = cos x, d/dx[cos x] = -sin x, and all six trig derivatives' },
          { slug: 'higher-order-derivatives', name: 'Higher-Order Derivatives', description: 'Second, third, and nth derivatives — acceleration and beyond' },
        ],
      },
      {
        slug: 'chain-rule-and-advanced',
        name: 'The Chain Rule and Advanced Differentiation',
        description: 'Chain rule, implicit differentiation, inverse trig, exponential, and log derivatives',
        topics: [
          { slug: 'chain-rule', name: 'The Chain Rule', description: 'd/dx[f(g(x))] = f\'(g(x))*g\'(x) — differentiating compositions' },
          { slug: 'implicit-differentiation', name: 'Implicit Differentiation', description: 'Finding dy/dx when y is not isolated — circles, ellipses, and more' },
          { slug: 'derivatives-of-inverse-trig', name: 'Derivatives of Inverse Trig Functions', description: 'd/dx[arcsin x] = 1/sqrt(1-x^2) and the rest of the family' },
          { slug: 'derivatives-of-exponentials', name: 'Derivatives of Exponential Functions', description: 'd/dx[e^x] = e^x, d/dx[a^x] = a^x * ln(a) — the magic of e' },
          { slug: 'derivatives-of-logarithms', name: 'Derivatives of Logarithmic Functions', description: 'd/dx[ln x] = 1/x, d/dx[log_a(x)] = 1/(x*ln a)' },
          { slug: 'logarithmic-differentiation', name: 'Logarithmic Differentiation', description: 'Taking ln of both sides to differentiate tricky products and powers' },
        ],
      },
      {
        slug: 'applications-of-derivatives-1',
        name: 'Applications of Derivatives — Part 1',
        description: 'Related rates, linear approximation, Mean Value Theorem, and L\'Hopital\'s Rule',
        topics: [
          { slug: 'related-rates', name: 'Related Rates', description: 'Using the chain rule to connect rates of change in real-world problems' },
          { slug: 'linear-approximation', name: 'Linear Approximation and Differentials', description: 'Using the tangent line to approximate function values near a point' },
          { slug: 'mean-value-theorem', name: 'The Mean Value Theorem', description: 'There exists a c where the instantaneous rate equals the average rate' },
          { slug: 'lhopitals-rule', name: "L'Hopital's Rule", description: 'Evaluating 0/0 and infinity/infinity limits by differentiating top and bottom' },
          { slug: 'newtons-method', name: "Newton's Method", description: 'Using tangent lines to approximate roots of equations' },
        ],
      },
      {
        slug: 'analyzing-functions',
        name: 'Analyzing Functions with Derivatives',
        description: 'Increasing/decreasing, concavity, inflection points, and curve sketching',
        topics: [
          { slug: 'increasing-decreasing', name: 'Increasing and Decreasing Functions', description: 'Using the sign of f\'(x) to determine where a function rises or falls' },
          { slug: 'first-derivative-test', name: 'The First Derivative Test', description: 'Classifying local extrema by sign changes in f\'(x)' },
          { slug: 'concavity-second-derivative', name: 'Concavity and the Second Derivative', description: 'f\'\'(x) > 0 means concave up, f\'\'(x) < 0 means concave down' },
          { slug: 'second-derivative-test', name: 'The Second Derivative Test', description: 'Using f\'\'(c) to classify critical points as local max or min' },
          { slug: 'curve-sketching', name: 'Curve Sketching — Putting It All Together', description: 'Domain, intercepts, symmetry, asymptotes, first/second derivative analysis' },
        ],
      },
      {
        slug: 'optimization',
        name: 'Optimization',
        description: 'Finding absolute extrema and solving applied optimization problems',
        topics: [
          { slug: 'absolute-extrema', name: 'Absolute (Global) Extrema', description: 'Absolute max and min values on closed intervals and open domains' },
          { slug: 'closed-interval-method', name: 'The Closed Interval Method', description: 'Evaluate f at critical points and endpoints to find absolute extrema' },
          { slug: 'applied-optimization', name: 'Applied Optimization Problems', description: 'Maximize area, minimize cost, optimize dimensions — real-world problems' },
          { slug: 'optimization-strategies', name: 'Optimization Problem-Solving Strategies', description: 'Draw a picture, write one equation, find the domain, then optimize' },
        ],
      },
      {
        slug: 'intro-to-integration',
        name: 'Introduction to Integration',
        description: 'Antiderivatives, sigma notation, Riemann sums, and the definite integral',
        topics: [
          { slug: 'antiderivatives', name: 'Antiderivatives', description: 'Finding F(x) such that F\'(x) = f(x) — reversing differentiation' },
          { slug: 'basic-antidifferentiation', name: 'Basic Antidifferentiation Rules', description: 'Power rule in reverse, trig antiderivatives, and the +C constant' },
          { slug: 'sigma-notation', name: 'Sigma Notation and Summation Formulas', description: 'Compact notation for sums, key formulas for sum of i, i^2, i^3' },
          { slug: 'riemann-sums', name: 'Riemann Sums and Area Under a Curve', description: 'Left, right, and midpoint sums — approximating area with rectangles' },
          { slug: 'the-definite-integral', name: 'The Definite Integral', description: 'The limit of Riemann sums — integral from a to b of f(x) dx' },
        ],
      },
      {
        slug: 'fundamental-theorem',
        name: 'The Fundamental Theorem of Calculus',
        description: 'The two parts of the FTC, net change, and properties of integrals',
        topics: [
          { slug: 'ftc-part-1', name: 'The Fundamental Theorem of Calculus, Part 1', description: 'd/dx[integral from a to x of f(t) dt] = f(x) — derivatives undo integrals' },
          { slug: 'ftc-part-2', name: 'The Fundamental Theorem of Calculus, Part 2', description: 'Integral from a to b of f(x) dx = F(b) - F(a) — evaluate definite integrals' },
          { slug: 'net-change-theorem', name: 'The Net Change Theorem', description: 'The integral of a rate of change gives the net change' },
          { slug: 'properties-of-definite-integrals', name: 'Properties of Definite Integrals', description: 'Linearity, additivity, comparison, and reversing limits' },
        ],
      },
      {
        slug: 'integration-techniques',
        name: 'Integration Techniques',
        description: 'U-substitution for indefinite and definite integrals, and key integral formulas',
        topics: [
          { slug: 'u-substitution-indefinite', name: 'U-Substitution (Indefinite Integrals)', description: 'The chain rule in reverse — choosing u, finding du, and substituting' },
          { slug: 'u-substitution-definite', name: 'U-Substitution with Definite Integrals', description: 'Changing the limits of integration when you substitute' },
          { slug: 'integrals-exp-log', name: 'Integrals of Exponential and Logarithmic Functions', description: 'Integral of e^x, a^x, 1/x, and combinations with u-sub' },
          { slug: 'integrals-trig', name: 'Integrals of Trigonometric Functions', description: 'Integral of sin, cos, sec^2, csc^2, sec*tan, csc*cot' },
          { slug: 'integrals-inverse-trig', name: 'Integrals Involving Inverse Trig Functions', description: 'Recognizing arcsin, arctan, and arcsec patterns in integrands' },
        ],
      },
      {
        slug: 'applications-of-integration',
        name: 'Applications of Integration',
        description: 'Area between curves, volumes of revolution, and average value',
        topics: [
          { slug: 'area-between-curves', name: 'Area Between Curves', description: 'Integral of (top - bottom) dx or (right - left) dy' },
          { slug: 'volumes-disk-washer', name: 'Volumes by Disk and Washer Methods', description: 'Rotating regions around an axis — pi * integral of [R(x)]^2 dx' },
          { slug: 'volumes-shells', name: 'Volumes by Cylindrical Shells', description: '2*pi * integral of x*f(x) dx — when disks are inconvenient' },
          { slug: 'average-value', name: 'Average Value of a Function', description: 'f_avg = (1/(b-a)) * integral from a to b of f(x) dx' },
          { slug: 'calc1-review', name: 'Course Review and What Comes Next', description: 'Comprehensive review of Calculus 1 and preview of Calculus 2' },
        ],
      },
    ],
  },
  {
    slug: 'calc-2',
    name: 'Calculus 2',
    emoji: '∬',
    color: Colors.primary,
    bgColor: Colors.primaryLight,
    description: 'Integration, series & sequences',
    topics: [
      {
        slug: 'integration-techniques',
        name: 'Integration Techniques',
        description: 'Integration by parts, partial fractions, and trig substitution',
      },
      {
        slug: 'improper-integrals',
        name: 'Improper Integrals',
        description: 'Evaluate integrals with infinite limits or discontinuities',
      },
      {
        slug: 'sequences-series',
        name: 'Sequences & Series',
        description: 'Convergence, divergence, and partial sums',
      },
      {
        slug: 'convergence-tests',
        name: 'Convergence Tests',
        description: 'Ratio, root, comparison, integral, and alternating series tests',
      },
      {
        slug: 'taylor-maclaurin',
        name: 'Taylor & Maclaurin Series',
        description: 'Power series representations and approximations',
      },
      {
        slug: 'parametric-polar',
        name: 'Parametric & Polar Curves',
        description: 'Parametric equations, polar graphs, and area in polar coordinates',
      },
      {
        slug: 'arc-length-surface-area',
        name: 'Arc Length & Surface Area',
        description: 'Compute lengths of curves and surface areas of revolution',
      },
    ],
  },
  {
    slug: 'calc-3',
    name: 'Calculus 3',
    emoji: '∭',
    color: Colors.teal,
    bgColor: '#E8F8F7',
    description: 'Multivariable calculus & vectors',
    topics: [
      {
        slug: 'vectors-vector-functions',
        name: 'Vectors & Vector Functions',
        description: 'Dot product, cross product, vector-valued functions, and space curves',
      },
      {
        slug: 'partial-derivatives',
        name: 'Partial Derivatives',
        description: 'Partial differentiation, gradients, directional derivatives, and the chain rule',
      },
      {
        slug: 'multiple-integrals',
        name: 'Multiple Integrals',
        description: 'Double and triple integrals, change of order, and applications',
      },
      {
        slug: 'vector-fields',
        name: 'Vector Fields',
        description: 'Conservative fields, potential functions, curl, and divergence',
      },
      {
        slug: 'line-surface-integrals',
        name: 'Line & Surface Integrals',
        description: 'Work, flux, and parameterized surface integrals',
      },
      {
        slug: 'fundamental-theorems',
        name: "Green's, Stokes' & Divergence Theorems",
        description: 'The three big theorems connecting integrals in higher dimensions',
      },
      {
        slug: 'coordinate-systems',
        name: 'Cylindrical & Spherical Coordinates',
        description: 'Convert and integrate in cylindrical and spherical coordinate systems',
      },
    ],
  },
  {
    slug: 'diff-eq',
    name: 'Differential Equations',
    emoji: 'δ',
    color: Colors.green,
    bgColor: '#EAFAF1',
    description: 'ODEs, Laplace & systems',
    topics: [
      {
        slug: 'first-order-odes',
        name: 'First Order ODEs',
        description: 'Separable, linear, exact, and Bernoulli equations',
      },
      {
        slug: 'second-order-odes',
        name: 'Second Order Linear ODEs',
        description: 'Homogeneous and non-homogeneous with constant coefficients',
      },
      {
        slug: 'laplace-transforms',
        name: 'Laplace Transforms',
        description: 'Transform, inverse transform, and solving IVPs with Laplace',
      },
      {
        slug: 'systems-of-odes',
        name: 'Systems of ODEs',
        description: 'Matrix methods, eigenvalue approach, and phase portraits',
      },
      {
        slug: 'series-solutions',
        name: 'Series Solutions',
        description: 'Power series methods for solving ODEs near ordinary points',
      },
      {
        slug: 'numerical-methods',
        name: 'Numerical Methods',
        description: "Euler's method, improved Euler, and Runge-Kutta approximations",
      },
      {
        slug: 'applications',
        name: 'Applications',
        description: 'Population models, circuits, mechanical vibrations, and mixing problems',
      },
    ],
  },
  {
    slug: 'linear-algebra',
    name: 'Linear Algebra',
    emoji: '⊿',
    color: '#9B59B6',
    bgColor: '#F5EEF8',
    description: 'Matrices, vectors & transformations',
    topics: [
      {
        slug: 'systems-row-reduction',
        name: 'Systems of Equations & Row Reduction',
        description: 'Gaussian elimination, RREF, and solution sets',
      },
      {
        slug: 'matrix-operations',
        name: 'Matrix Operations & Inverses',
        description: 'Addition, multiplication, transpose, and finding inverses',
      },
      {
        slug: 'determinants',
        name: 'Determinants',
        description: 'Cofactor expansion, properties, and applications of determinants',
      },
      {
        slug: 'vector-spaces',
        name: 'Vector Spaces & Subspaces',
        description: 'Span, linear independence, basis, dimension, and rank',
      },
      {
        slug: 'eigenvalues-eigenvectors',
        name: 'Eigenvalues & Eigenvectors',
        description: 'Characteristic equation, diagonalization, and applications',
      },
      {
        slug: 'orthogonality',
        name: 'Orthogonality & Least Squares',
        description: 'Orthogonal projection, Gram-Schmidt, and least squares fitting',
      },
      {
        slug: 'linear-transformations',
        name: 'Linear Transformations',
        description: 'Kernel, range, matrix representation, and change of basis',
      },
    ],
  },
];
