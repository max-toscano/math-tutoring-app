# math-tutoring-app

This repository contains an AI-powered tutoring application where students can chat with an AI tutor.

The codebase is organized into clearly separated layers so that the **frontend UI**, **backend API**, and **tutoring intelligence (AI workflow)** can evolve independently while sharing common contracts and types.

## Top-level structure

- `frontend/` – Student-facing app (mobile/web) with screens, navigation, UI components, and API client. No tutoring reasoning logic lives here.
- `backend/` – API, auth, sessions, progress tracking, and data access. Orchestrates requests to the AI workflow and database.
- `ai-workflow/` – Tutoring intelligence layer: orchestration, state, teaching modes, prompts, evaluators, and guardrails.
- `shared/` – Shared TypeScript types, schemas, constants, and API contracts reused across all layers.
- `docs/` – Architecture and product documentation, plus future planning/roadmap notes.

Each folder has its own `README.md` and/or starter files describing its responsibility and how it should be extended.

