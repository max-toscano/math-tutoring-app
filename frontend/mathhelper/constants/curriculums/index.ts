/**
 * curriculums/index.ts — Shared types and combined exports for all curriculums.
 *
 * Each curriculum file (math.ts, chemistry.ts, physics.ts, etc.) exports its
 * own SUBJECTS array. This index re-exports them and merges into ALL_SUBJECTS
 * so the rest of the app can import from one place.
 *
 * To add a new curriculum:
 *   1. Create a new file like chemistry.ts exporting CHEMISTRY_SUBJECTS
 *   2. Import it here and spread it into ALL_SUBJECTS
 */

// ─── Shared Types ───────────────────────────────────────────────────────────

export interface Topic {
  /** URL-friendly ID, e.g. "integration-techniques" */
  slug: string;
  /** Display name, e.g. "Integration Techniques" */
  name: string;
  /** One-line description shown on the subtopic card */
  description: string;
}

export interface Chapter {
  /** URL-friendly ID, e.g. "right-triangle-trig" */
  slug: string;
  /** Display name, e.g. "Right Triangle Trigonometry" */
  name: string;
  /** One-line description shown on the chapter card */
  description: string;
  /** Ordered list of sub-chapter topics within this chapter */
  topics: Topic[];
}

export interface Subject {
  /** URL-friendly ID, e.g. "calc-2" */
  slug: string;
  /** Display name, e.g. "Calculus 2" */
  name: string;
  /** Emoji shown on the card */
  emoji: string;
  /** Accent color for cards, progress bars, headers */
  color: string;
  /** Light background tint for emoji badge */
  bgColor: string;
  /** Short description shown under the subject name */
  description: string;
  /** Ordered list of chapters (for chaptered subjects like Trigonometry) */
  chapters?: Chapter[];
  /** Ordered list of topics (for flat subjects like Calc 1) */
  topics: Topic[];
}

// ─── Curriculum imports ─────────────────────────────────────────────────────

import { MATH_SUBJECTS } from './math';

export { MATH_SUBJECTS } from './math';

// When you add more curriculums, export them here too:
// export { CHEMISTRY_SUBJECTS } from './chemistry';
// export { PHYSICS_SUBJECTS } from './physics';

// ─── Combined ───────────────────────────────────────────────────────────────

/** All subjects across all curriculums. */
export const ALL_SUBJECTS: Subject[] = [
  ...MATH_SUBJECTS,
  // ...CHEMISTRY_SUBJECTS,
  // ...PHYSICS_SUBJECTS,
];

// ─── Lookup helpers ─────────────────────────────────────────────────────────

/** Check if a subject uses chapter hierarchy */
export function hasChapters(subject: Subject): boolean {
  return (subject.chapters?.length ?? 0) > 0;
}

/** Find a subject by its slug, e.g. getSubject('calc-2') */
export function getSubject(slug: string): Subject | undefined {
  return ALL_SUBJECTS.find((s) => s.slug === slug);
}

/** Find a chapter within a subject */
export function getChapter(subjectSlug: string, chapterSlug: string): Chapter | undefined {
  return getSubject(subjectSlug)?.chapters?.find((c) => c.slug === chapterSlug);
}

/** Find a topic within a subject (flat subjects only) */
export function getTopic(subjectSlug: string, topicSlug: string): Topic | undefined {
  return getSubject(subjectSlug)?.topics.find((t) => t.slug === topicSlug);
}

/** Find a topic within a specific chapter */
export function getChapterTopic(
  subjectSlug: string,
  chapterSlug: string,
  topicSlug: string,
): Topic | undefined {
  return getChapter(subjectSlug, chapterSlug)?.topics.find((t) => t.slug === topicSlug);
}

/** Get total topic count for a subject (works for both flat and chaptered) */
export function getTotalTopicCount(subject: Subject): number {
  if (hasChapters(subject)) {
    return subject.chapters!.reduce((sum, ch) => sum + ch.topics.length, 0);
  }
  return subject.topics.length;
}

/** Get all subject slugs (useful for validation) */
export function getAllSubjectSlugs(): string[] {
  return ALL_SUBJECTS.map((s) => s.slug);
}
