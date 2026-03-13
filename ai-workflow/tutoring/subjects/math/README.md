# Math Subject Module

This folder contains all tutoring behavior and rules specific to **math**.
It is the first subject module and serves as a template for future subjects.

## File Descriptions

| File | Responsibility |
|---|---|
| `index.ts` | Combines all math pieces into one exported `mathModule` object |
| `subject_rules.ts` | Core teaching rules the AI must follow when tutoring math |
| `topic_router.ts` | Classifies an incoming question into a math topic (e.g. algebra, geometry) |
| `teaching_strategies.ts` | Defines how to approach teaching: step-by-step, concept explanation, answer checking |
| `common_mistakes.ts` | A list of frequent student mistakes the AI should watch for |
| `response_patterns.ts` | Reusable language patterns: openers, guided questions, and closers |
| `evaluator.ts` | Evaluates a student's response and returns a simple pass/score/issues result |
