## ai-workflow

This folder contains the **tutoring intelligence layer**.

- Responsible for tutoring workflows, orchestration, state, subject/mode logic, and prompt templates.
- Implements policies, guardrails, evaluators, and response formatting.
- Exposes a clean, typed interface that the `backend/` can call without knowing prompt details.
- Must **not** depend directly on UI concerns from `frontend/`.

