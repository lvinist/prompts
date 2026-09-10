# mine-flow — STEP-54.3: Operations Suite 2 — Land Clearing Tracking Critique

> **How to run:** Tell your agent *"run substep 54.3"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.

**Assigned model: Gemini 3.1 Pro High.** Real design critique, bounded by blueprint D1–D8, Doc 07, and the 54.1 rubric; consolidation at 54.11 catches weak findings.

## Context

STEP-54 critiques each feature as a cohesive lifecycle (List → Form sheet → Detail → Report dialog) across Web (desktop) and Android. This substep covers **Land Clearing Tracking**, an Operations feature with a distinctive structure: a tabbed Plan vs. Actual summary and a shared method combobox (the STEP-51 CF-043 deliverable — one shared selection-only combobox above the tabs, with enumerated-set validation).

Preconditions: 54.0 (clean trunk, branch `step-0054-feature-cohesion-critique`), 54.1 (rubric in `mine-flow-STEP-54.1-FINDINGS.md`).

## Read these first

- `Upcoming Prompts/mine-flow-STEP-54-PLAN.md` — STEP PLAN (evidence standard, D1–D8, ground rules)
- `Upcoming Prompts/mine-flow-STEP-54.1-FINDINGS.md` — **the rubric**. Apply it exactly; IDs are `FC-54.3-NNN`.
- `Code/mine-flow-docs/reports/2026-09-10-step-54-55-design-blueprint.md` — D1–D8; blueprint §54.3 names this feature's surfaces
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` — UI canon
- `prompts/STEP-index.md` STEP-51 row + `prompts/003-release-readiness-integration-scale/step-0051/` findings — the CF-043 combobox contract this feature must honor (selection-only, enumerated-set validation)
- `Code/mine-flow-docs/architecture/04-data-model.md` — clearing-area semantics (plan vs actual areas, methods)
- `Code/mine-flow-app/README.md` + `ARCHITECTURE.md`
- root `.throughstone/local-user.md`

## Scope

**Surfaces** (paths as of 2026-09-10; re-locate on the branch head — under `lib/features/tracking/`):
- List: `lib/features/tracking/presentation/pages/land_clearing_list_screen.dart` (tabbed Plan/Actual summary)
- Form: `lib/features/tracking/presentation/pages/land_clearing_entry_screen.dart`
- Widgets: `lib/features/tracking/presentation/widgets/clearing_summary_card.dart`, `area_input_field.dart`
- Shared method combobox (the CF-043 deliverable — locate it; likely a shared widget under `lib/features/tracking/presentation/widgets/` or `lib/core/`)
- Report path: navigation from this list to the reporting pages / `pdf_service.dart` — trace the actual path (contextual per D6 or redirect?)
- BLoC states: `lib/features/tracking/presentation/bloc/`

**Does NOT touch:** application code (read-only), other features, the rubric.

## Your task

Apply every 54.1 rubric dimension, both platforms (Web desktop, Android portrait):

1. **Lifecycle cohesion:** List (tabs) → Form → back → Report. Does the selected tab (Plan vs Actual) survive the form round-trip? Do filters survive the report dialog per D6?
2. **Tabbed summary critique:** Plan vs Actual tabs — are the two tabs visually and semantically parallel (same columns, same density, same empty/error states)? Tab switching: URL-synced or lost on refresh (D5)?
3. **Shared method combobox:** verify it matches the CF-043 contract (selection-only, enumerated set, no free text); critique its platform behavior (dropdown on desktop, modal picker on mobile?), its empty/error states, and its consistency with the other selection widgets in the app.
4. **Form → sheet migration spec:** what must change for D1/D2 (right sheet Web, bottom sheet Mobile); D4 dirty-intercept status today; D5 deep-link gap (does `land-clearing/form` exist? router shows `land-clearing` without a form subroute — confirm).
5. **Interaction states, a11y, tokens:** all rubric dimensions; anchored-grep any residual Material.
6. **Report dialog:** D6 conformance — pre-bound ReportType, filters preserved.
7. **D7 verdict:** detail view needed or list+form suffices?

## Verification (evidence standard — mandatory)

- Every finding: `FC-54.3-NNN` ID, verdict (`Aligned`/`Needs polish`/`Needs restructure`/`Unverified`), `file:line` citation, one-sentence why (Explanatory style).
- Runtime optional and honest: name the command, report artifact byte-size + pixel dimensions; 1×1-placeholder class = harness-defect call-out. Unverifiable → `Unverified` + blocker.
- No code changes: app repo `git status` clean at the end.
- Findings file: `Upcoming Prompts/mine-flow-STEP-54.3-FINDINGS.md` — coverage table, findings table, verification record, limitations.

## Keeping the docs true  (always)

- Findings only — no doc edits (54.11 consolidates). Escalate (and record) on: D1–D8/ADR conflicts, runtime contradicting Doc 07, unevidenced runtime claims, same classification problem twice.
- Accepted-risk-shaped discoveries go to findings for 54.11's reconciliation.

## Definition of done

- [ ] All rubric dimensions scored, both platforms, including the tabbed summary and combobox specifically.
- [ ] CF-043 contract conformance explicitly verified with citations.
- [ ] D4/D5 status and D7 verdict recorded.
- [ ] Coverage/findings/verification/limitations tables present with IDs and citations.
- [ ] No application code or docs modified.

## Next

Update the PLAN's substep table (54.3 → Done) and tell the user: *"run substep 54.4"* — in a **fresh chat**.
