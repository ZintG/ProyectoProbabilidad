# BRIEFING — 2026-11-20T22:10:00Z

## Mission
Extract and systematically document the complete official specification, technical requirements, and grading rubric for the UC Probabilidad n-gram project from `proyecto_S01_probabilidad.pdf`, `decisiones_informe.md`, and `S01/`.

## 🔒 My Identity
- Archetype: specification-miner
- Roles: Spec Miner
- Working directory: /home/simon/Documentos/UC-Probabilidad
- State folder: /home/simon/Documentos/UC-Probabilidad/.agents/teamwork/spec_miner_1/
- Original parent: 8d66cf00-fc5f-47c5-93dc-455db5750ff5
- Milestone: Specification and Rubric Extraction

## 🔒 Key Constraints
- Read-only: DO NOT modify any project files (source code, tests, docs outside state folder).
- State folder isolation: Only write to `/home/simon/Documentos/UC-Probabilidad/.agents/teamwork/spec_miner_1/`.
- Prioritize authoritative sources: `proyecto_S01_probabilidad.pdf`, `decisiones_informe.md`, `S01/`.
- Comprehensive extraction: Cover all sections, questions, n-gram models, smoothing techniques, metrics, constraints, formatting rules, and official grading rubric points.
- Communicate findings via `send_message` to parent.

## Current Parent
- Conversation ID: 8d66cf00-fc5f-47c5-93dc-455db5750ff5
- Updated: 2026-11-20T21:59:20Z

## Task Summary
- **What to build**: Comprehensive `spec.md` containing all specifications, constraints, metrics, and grading rubric, plus `handoff.md`.
- **Success criteria**: Detailed, unambiguous, verifiable specification covering 100% of the project prompt and evaluation criteria.
- **Interface contracts**: `DISPATCH.md`, `ORIGINAL_REQUEST.md`
- **Code layout**: Read-only workspace.

## Key Decisions Made
- Extracted and fully decoded `proyecto_S01_probabilidad.pdf` into `pdf_full.txt`.
- Structured complete requirement matrix (28 features, 12 edge cases, 11 theoretical questions, 6 rubric criteria + bonus).
- Validated alignment against `decisiones_informe.md` and `S01/` terminological registry.
- Generated `spec.md` and 5-component `handoff.md`. Task completed.

## Artifact Index
- `/home/simon/Documentos/UC-Probabilidad/.agents/teamwork/spec_miner_1/spec.md` — Authoritative specification and rubric document
- `/home/simon/Documentos/UC-Probabilidad/.agents/teamwork/spec_miner_1/handoff.md` — 5-component hard handoff report
- `/home/simon/Documentos/UC-Probabilidad/.agents/teamwork/spec_miner_1/progress.md` — Progress tracker and liveness heartbeat
- `/home/simon/Documentos/UC-Probabilidad/.agents/teamwork/spec_miner_1/pdf_full.txt` — Full textual dump of official prompt PDF
