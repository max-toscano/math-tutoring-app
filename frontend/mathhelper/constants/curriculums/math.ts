/**
 * math.ts — Math curriculum: all math subjects and topics.
 *
 * One of potentially many curriculum files (math, chemistry, physics, etc.).
 * Each curriculum file exports a SUBJECTS array following the shared types from index.ts.
 *
 * Trigonometry uses the chapter hierarchy (13 chapters × 4-6 sub-chapters = 73 lessons).
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
    description: 'Limits, derivatives & integrals',
    topics: [
      {
        slug: 'limits-continuity',
        name: 'Limits & Continuity',
        description: 'Evaluate limits algebraically and graphically, understand continuity',
      },
      {
        slug: 'definition-of-derivative',
        name: 'Definition of the Derivative',
        description: 'Limit definition, tangent lines, and rates of change',
      },
      {
        slug: 'differentiation-rules',
        name: 'Differentiation Rules',
        description: 'Power, product, quotient, and chain rules',
      },
      {
        slug: 'applications-of-derivatives',
        name: 'Applications of Derivatives',
        description: 'Related rates, optimization, curve sketching, L\'Hopital\'s rule',
      },
      {
        slug: 'intro-to-integration',
        name: 'Introduction to Integration',
        description: 'Antiderivatives, Riemann sums, and definite integrals',
      },
      {
        slug: 'fundamental-theorem',
        name: 'Fundamental Theorem of Calculus',
        description: 'Connect differentiation and integration, evaluate definite integrals',
      },
      {
        slug: 'basic-integration',
        name: 'Basic Integration Techniques',
        description: 'U-substitution and basic integration formulas',
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
