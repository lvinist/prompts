# mine-flow — STEP-29 PLAN: Impeccable/Throughstone Bridge & Doc Reconciliation

**Phase:** Phase 2 — Impeccable UI Rebuild
**Owner:** Antigravity
**Status:** In progress
**Date:** 2026-07-22
**Branch:** `step-0029-impeccable-bridge`
**Repos (projection):** `mine-flow-docs`, `mine-flow-app`

> Formalizes the UI tokens into the architecture docs, reconciles the conflict between Impeccable's root-level context files and the project's living architecture, and creates a bridge script to sync them safely.

## Motivation
The Impeccable UI workflow relies on `DESIGN.md` and `PRODUCT.md` at the workspace root as its unversioned input contract. However, `METHOD.md` §7 flags root files as a hygiene violation, and the project's canonical UI direction (`architecture/07-ui-design-system.md`) drifted from `DESIGN.md`. This STEP formalizes the UI direction (ForUI package + FThemes.zinc), resolves the conflict, explicitly defers redundant Phase 2 polish work until the ForUI rebuild, and automates the sync between the canonical docs and the Impeccable bridge files.

## Decisions already locked
- root `.throughstone/local-user.md` — read **Experience level** before user-facing
  questions or explanations, and read **Communication style** before planning discussions;
  keep that file as the personal local source of truth for both values.
- `registries/risks.yml` — review relevant accepted risks/debt before planning work that
  touches their area.
- The Test Strategy architecture doc (`architecture/*-test-strategy.md`) — use it to decide
  which test tiers this STEP must add or update and which command or CI gate proves the STEP
  is done.
- ADR-0007 — Re-scope Phase 2 to Impeccable UI Rebuild.
- architecture/07-ui-design-system.md — Current UI architecture to be updated to v0.2.0.

## Substeps

| # | Title | Produces | Depends on | Open questions |
|---|-------|----------|------------|----------------|
| 29.1 | Update Architecture 07-doc to v0.2.0 | `architecture/07-ui-design-system.md` v0.2.0 | | |
| 29.2 | ADR-0008, METHOD.md §7 Amendment & Close STEP-28.3 | `adr/ADR-0008-impeccable-bridge.md`, `METHOD.md`, risk register | 29.1 | |
| 29.3 | Impeccable Bridge Script | `scripts/impeccable-bridge.ps1` | 29.2 | |

## Test plan

| Test tier / surface | Substep(s) | Tests to create or update | Run timing | Command / gate | Notes |
|---------------------|------------|---------------------------|------------|----------------|-------|
| Integration / tooling | 29.3 | Test bridge script locally | Per substep | Execute `.\Code\mine-flow-docs\scripts\impeccable-bridge.ps1` | Manual verification that `DESIGN.md` and `PRODUCT.md` generate correctly |

## Open questions

## Ground rules
- **Calibrate communication from root `.throughstone/local-user.md`.** Substep prompts
  should read the recorded **Experience level** and adjust explanations/questions
  accordingly. STEP planning should use the saved **Communication style** as the default
  verbosity. If the file is missing, ask the two local-profile questions from
  `BOOTSTRAP-PROMPT.md` Stage 0, create it, and continue. An explicit style request in chat
  overrides the profile for this session only. Don't copy either value into this PLAN.
- **Plan interactively.** Before this PLAN is finalized, confirm scope with the user and ask
  clarifying questions for ambiguous requirements, sequencing, dependencies, ownership, or
  repo boundaries. When a planning decision is needed, offer appropriate options with brief
  pros and cons. Respect the saved communication style while still asking the questions
  needed to make the STEP coherent.
- **Tests ship with the code.** Every substep that writes or changes code also writes or updates
  the relevant tests for it (unit, integration, API/contract, e2e, security/authorization,
  migration/data, performance, or project-specific). The PLAN chooses whether tests run as each
  substep completes or in a dedicated final verification substep; either way, the named test
  command or CI gate must pass before the STEP is Done. Override per substep only with a stated
  reason.
- **Code is documented as it's written.** Every class, function, and method gets a docstring;
  comment the *why* of non-obvious logic (see `coding-standards/README.md`).
- **Accepted risks stay visible.** If this STEP accepts a risk or defers tech debt, add or
  update `registries/risks.yml` with severity, owner, and revisit trigger. Reference an
  architecture decision/section, ADR, issue/follow-up STEP, incident report under
  `reports/incidents/`, or check-in report under `reports/` instead of duplicating detail; create
  that source first if it doesn't already exist.

## Definition of done
- [x] 07-ui-design-system.md updated to v0.2.0.
- [x] ADR-0008 recorded and METHOD.md updated.
- [x] impeccable-bridge.ps1 created and verified.
- [x] STEP-28.3 explicitly deferred/closed in index.
- [x] The STEP test plan is complete: each code-changing substep either added/updated its
      relevant tests or records why tests were not applicable.
- [x] All tests named in the STEP test plan pass at the end of this STEP — ideally the full
      suite (unit + integration/API/e2e/security as applicable).
- [x] STEP review passed; prompts/STEP-index.md updated; STEP archived to prompts/.
