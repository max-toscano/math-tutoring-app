# Inconsistencies Audit

Last updated: 2026-04-10

## Dependencies / Requirements Inconsistencies

1. High: Python dependency manifest drift between root and app manifests.
- Evidence: [requirements.txt](../../requirements.txt) and [app/requirements.txt](../../app/requirements.txt) are nearly duplicated, but [app/requirements.txt](../../app/requirements.txt) includes google-api-python-client while [requirements.txt](../../requirements.txt) originally did not.
- Impact: If install/deploy uses [requirements.txt](../../requirements.txt), web search functionality can fail at runtime.
- Runtime evidence: [app/tools/math/web_search.py](../../app/tools/math/web_search.py) imports googleapiclient.discovery.build.

2. High: No Python lockfile for reproducible installs.
- Evidence: No Poetry/Pipenv/pip-tools lock artifact exists in repo; Python packages are not frozen.
- Current state: Frontend has [frontend/mathhelper/package-lock.json](../../frontend/mathhelper/package-lock.json), but backend has no equivalent lock.
- Impact: Different environments may resolve different dependency versions and break unexpectedly.

3. Medium: Python requirements use unbounded minimum versions.
- Evidence: Both [requirements.txt](../../requirements.txt) and [app/requirements.txt](../../app/requirements.txt) use operators like >= for major libraries.
- Impact: Future upstream major releases can introduce breaking changes without code changes in this repo.

4. Medium: Duplicate Python manifests create ongoing maintenance risk.
- Evidence: [requirements.txt](../../requirements.txt) and [app/requirements.txt](../../app/requirements.txt) overlap heavily and can drift.
- Impact: Confusion over canonical install path, accidental production mismatch, onboarding friction.

5. Low: Local Python version consistency not explicitly enforced beyond deployment runtime file.
- Evidence: [runtime.txt](../../runtime.txt) specifies python-3.12.8 for deployment, but no local tool version file is present.
- Impact: Team members can run different local Python versions and encounter subtle dependency behavior differences.

## Environment / Configuration Inconsistencies

1. High: Backend local port conventions conflict across code and examples.
- Evidence: [app/main.py](../../app/main.py) assumes localhost:8001, [frontend/mathhelper/services/api.ts](../../frontend/mathhelper/services/api.ts) defaults to localhost:8002, and [frontend/mathhelper/.env.example](../../frontend/mathhelper/.env.example) suggests localhost:8000.
- Impact: Default local setup can point frontend to the wrong backend and cause connection failures.

2. Medium: Backend env loading strategy is split across two different load paths.
- Evidence: [app/main.py](../../app/main.py) calls load_dotenv() from process context, while [app/config.py](../../app/config.py) explicitly loads app/.env.
- Impact: Different launch directories can produce different effective configs.

3. Medium: Backend can run in bypass-auth mode by default.
- Evidence: [app/config.py](../../app/config.py) sets DEV_MODE default true; [app/api/middleware/auth.py](../../app/api/middleware/auth.py) returns test_student_001 if DEV_MODE or JWKS client missing.
- Impact: Misconfigured non-dev environments can accidentally accept requests without real auth.

4. Medium: Required env vars are implicit and fail at runtime rather than startup.
- Evidence: [app/config.py](../../app/config.py) reads OPENAI_API_KEY/DATABASE_URL/SUPABASE vars without upfront validation; [app/db/session.py](../../app/db/session.py) raises only when DB dependency is requested.
- Impact: Service can boot but fail on first real request path.

5. Medium: Frontend startup hard-fails on missing Supabase env vars.
- Evidence: [frontend/mathhelper/lib/supabase.ts](../../frontend/mathhelper/lib/supabase.ts) throws at import-time if EXPO_PUBLIC_SUPABASE_URL or EXPO_PUBLIC_SUPABASE_ANON_KEY are missing.
- Impact: App fails early with no degraded mode, increasing setup friction.

## API / Data Contract Inconsistencies

1. High: Mode taxonomy is inconsistent between active service logic and legacy state/notes logic.
- Evidence: [app/services/mode_service.py](../../app/services/mode_service.py) uses auto/explain/guide_me/hint/check_answer, while [app/memory/session.py](../../app/memory/session.py) and [supabase/migrations/007_agent_sessions.sql](../../supabase/migrations/007_agent_sessions.sql) still assume socratic/direct/concept_first.
- Impact: Session analytics and personalization can drift from actual mode behavior.

2. Medium: Long-term learning-note heuristics still key off legacy mode labels.
- Evidence: [app/memory/long_term.py](../../app/memory/long_term.py) generates notes for direct and concept_first.
- Impact: New mode usage may not be reflected correctly in learning notes.

3. Medium: Session context instruction references a non-existent resolver tool.
- Evidence: [app/memory/session.py](../../app/memory/session.py) says to use get_hint_strategy, but no corresponding tool is present in the current toolset.
- Impact: Prompt instructions can create ambiguous behavior and reduce determinism in mode selection.

## Documentation / Structure Inconsistencies

1. High: Top-level architecture docs do not match current repository structure.
- Evidence: [README.md](../../README.md) describes backend and ai-workflow as top-level source locations, but runtime code lives under [app/](../../app/).
- Impact: New contributors can follow docs and end up in the wrong directories.

2. High: Backend folder README describes boundaries that current implementation does not follow.
- Evidence: [backend/README.md](../../backend/README.md) says backend should call into ai-workflow, while orchestration/subject/tool logic currently lives under [app/](../../app/).
- Impact: Architectural intent and real code ownership are out of sync.

3. Low: Claim that each folder has starter docs is not consistently true for active implementation roots.
- Evidence: [README.md](../../README.md) says each folder has docs, but [app/](../../app/) has no dedicated README.
- Impact: Practical setup knowledge is fragmented.

## Onboarding Process Critique

1. High: There is no single "Start Here" onboarding path for first-time contributors.
- Evidence: [README.md](../../README.md) now clarifies architecture and entrypoints, but does not provide a complete first-run sequence with prerequisites, backend+frontend startup order, and validation checkpoints.
- Onboarding impact: New contributors must infer setup sequence across multiple files, increasing drop-off and support overhead.

2. High: Contributor docs are split between current-state and legacy-state narratives without explicit onboarding labels.
- Evidence: [backend/README.md](../../backend/README.md) and [frontend/README.md](../../frontend/README.md) describe intended architecture boundaries, while runtime setup is in [app/README.md](../../app/README.md) and app-level code under [app/](../../app/).
- Onboarding impact: Students can follow "correct" docs and still end up in non-runtime directories.

3. High: Frontend onboarding lacks a local setup guide in the active app folder.
- Evidence: [frontend/mathhelper/](../../frontend/mathhelper/) has no README, while frontend-specific requirements are spread across [frontend/mathhelper/package.json](../../frontend/mathhelper/package.json) and [frontend/mathhelper/.env.example](../../frontend/mathhelper/.env.example).
- Onboarding impact: Frontend contributors are missing a canonical install/run/env checklist in the folder they actually work in.

4. Medium: Environment setup is documented, but not as a fail-fast checklist.
- Evidence: Backend and frontend env templates exist ([app/.env.example](../../app/.env.example), [frontend/mathhelper/.env.example](../../frontend/mathhelper/.env.example)), but there is no centralized matrix of required vs optional keys, expected defaults, and what breaks when each is missing.
- Onboarding impact: New contributors hit runtime errors before understanding which config is mandatory.

5. Medium: There is no explicit "definition of done" for first successful local setup.
- Evidence: No documented smoke-test sequence covering backend health, auth/session start, first chat roundtrip, and close-session flow.
- Onboarding impact: Contributors can start services but still fail integration and not know where the issue is.

6. Medium: Toolchain expectations are implicit rather than contributor-facing.
- Evidence: Python version is pinned in [runtime.txt](../../runtime.txt), frontend uses Expo/React Native stack in [frontend/mathhelper/package.json](../../frontend/mathhelper/package.json), but no onboarding section specifies expected local Node/npm and Python setup commands.
- Onboarding impact: Environment mismatch issues become common in first-week contributor experience.

7. Low: Current run log captures assistant changes, but onboarding docs do not tell contributors how to maintain this convention.
- Evidence: [log/run-log.md](../../log/run-log.md) exists and is used, but no documented contribution rule references it.
- Onboarding impact: Process consistency can degrade as more contributors join.

### Onboarding Readiness Summary

- Current state: Better than baseline, but still mentor-assisted rather than self-serve.
- Biggest blockers for student contributors: missing frontend README, missing unified first-run checklist, and mixed legacy/current documentation paths.
- Fastest onboarding wins: add a single root "Start Here" workflow and a dedicated [frontend/mathhelper/README.md](../../frontend/mathhelper/) with env + run + smoke test steps.

## Open Decisions

1. Canonical backend dependency source.
- Option A: Keep only [requirements.txt](../../requirements.txt).
- Option B: Keep only [app/requirements.txt](../../app/requirements.txt).
- Option C: Keep both with automated sync.

2. Port standardization policy.
- Option A: 8001 everywhere.
- Option B: 8000 everywhere.
- Option C: 8002 everywhere.

3. Auth safety default policy.
- Option A: Keep DEV_MODE default true.
- Option B: Default DEV_MODE false and require explicit opt-in.

4. Mode compatibility policy.
- Option A: Fully migrate to new mode names.
- Option B: Add mapping layer for backward compatibility.
- Option C: Revert to legacy names globally.

5. Documentation source-of-truth policy.
- Option A: Update docs to current app/ architecture.
- Option B: Restructure code to match documented split.
- Option C: Keep both narratives temporarily with explicit labels.
