## backend

This folder contains the **API and application backend**.

- Handles HTTP APIs, auth, sessions, and persistence.
- Orchestrates data flow between the frontend, database, and `ai-workflow/`.
- Must **not** contain deep tutoring prompt logic or AI reasoning.
- Calls into the `ai-workflow/` layer using typed clients and shared contracts from `shared/`.

