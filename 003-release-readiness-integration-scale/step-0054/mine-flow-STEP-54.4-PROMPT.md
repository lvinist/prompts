# mine-flow — STEP-54.4: Operations Suite 3 — Benchmark Database Critique

> **How to run:** Tell your agent *"run substep 54.4"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.

**Assigned model: Gemini 3.1 Pro High.** Real design critique, bounded by blueprint D1–D8, Doc 07, and the 54.1 rubric; consolidation at 54.11 catches weak findings.

## Context

STEP-54 critiques each feature as a cohesive lifecycle (List → Form sheet → Detail → Report dialog) across Web (desktop) and Android. This substep covers the **Benchmark Database** — the geospatial reference-data feature: a benchmark list, coordinate entry, CRS (coordinate reference system) projection helpers, and spatial validation UX. Unlike the operational features, this is a curated reference database (supervisor-curated, occasionally field-consulted), so its usage pattern and critique lens differ: precision entry and trust in validation matter more than high-frequency entry speed.

Preconditions: 54.0 (clean trunk, branch `step-0054-feature-cohesion-critique`), 54.1 (rubric in `mine-flow-STEP-54.1-FINDINGS.md`).

## Read these first

- `Upcoming Prompts/mine-flow-STEP-54-PLAN.md` — STEP PLAN (evidence standard, D1–D8, ground rules)
- `Upcoming Prompts/mine-flow-STEP-54.1-FINDINGS.md` — **the rubric**. Apply it exactly; IDs are `FC-54.4-NNN`.
- `Code/mine-flow-docs/reports/2026-09-10-step-54-55-design-blueprint.md` — D1–D8; blueprint §54.4 names this feature's surfaces
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` — UI canon
- `Code/mine-flow-docs/architecture/04-data-model.md` — benchmark/coordinate/CRS semantics
- `Code/mine-flow-app/README.md` + `ARCHITECTURE.md`
- root `.throughstone/local-user.md`

## Scope

**Surfaces** (paths as of 2026-09-10; re-locate on the branch head — under `lib/features/benchmark/`):
- List: `lib/features/benchmark/presentation/pages/benchmark_list_screen.dart`
- Form: `lib/features/benchmark/presentation/pages/benchmark_form_screen.dart` (coordinate entry)
- CRS projection helpers and spatial validation: locate them (`lib/features/benchmark/` data/domain layers and any widgets; also check `lib/core/` for shared geo/projection services)
- Report path: this feature may not have a ReportType of its own — verify and record either way (the blueprint's D6 covers features with reports; a reference database may legitimately lack one, but that must be a recorded decision, not an accident)
- BLoC states: `lib/features/benchmark/presentation/bloc/`

**Does NOT touch:** application code (read-only), other features, the rubric.

## Your task

Apply every 54.1 rubric dimension, both platforms (Web desktop, Android portrait):

1. **Lifecycle cohesion:** List → Form (create/edit) → back. Is there a detail view at all — and is that right (this is the D7 exemplar for reference data)?
2. **Coordinate entry UX:** how are lat/long (or easting/northing) entered — separate fields, combined, paste support, degree/decimal formats? Critique precision-entry ergonomics per platform (keyboard types on mobile: numeric vs signed numeric; copy-paste on desktop).
3. **CRS helpers:** how does the UI expose projection selection and on-the-fly conversion? Are units and datum visible *before* commit (a silent mis-projection is a data-integrity defect, not a UI nit)? Critique error messaging when a projection fails or is ambiguous.
4. **Spatial validation UX:** when validation fails (out-of-site polygon, duplicate benchmark, malformed coordinates), what does the user see, and can they recover without losing input (D4-adjacent)?
5. **Form → sheet migration spec:** D1/D2 changes; D4 dirty-intercept status (coordinate entry is exactly where accidental dismissal hurts); D5 deep-link gap — note the router already shows `benchmark-db/form` exists; verify and critique its URL semantics (create vs edit mode in the URL?).
6. **Interaction states, a11y, tokens:** all rubric dimensions; anchored-grep residual Material.
7. **D7 verdict:** side-sheet inspector vs. full page for benchmark detail — give a verdict + rationale.

## Verification (evidence standard — mandatory)

- Every finding: `FC-54.4-NNN` ID, verdict (`Aligned`/`Needs polish`/`Needs restructure`/`Unverified`), `file:line` citation, one-sentence why (Explanatory style).
- Runtime optional and honest: name the command, report artifact byte-size + pixel dimensions; 1×1-placeholder class = harness-defect call-out. Unverifiable → `Unverified` + blocker.
- No code changes: app repo `git status` clean at the end.
- Findings file: `Upcoming Prompts/mine-flow-STEP-54.4-FINDINGS.md` — coverage table, findings table, verification record, limitations.

## Keeping the docs true  (always)

- Findings only — no doc edits (54.11 consolidates). Escalate (and record) on: D1–D8/ADR conflicts, runtime contradicting Doc 07, unevidenced runtime claims, same classification problem twice. **Data-integrity-shaped findings** (silent mis-projection, coordinate round-trip loss) are named escalation triggers — call them out prominently, do not bury them as polish items.
- Accepted-risk-shaped discoveries go to findings for 54.11's reconciliation.

## Definition of done

- [ ] All rubric dimensions scored, both platforms, with coordinate/CRS/validation UX critiqued in depth.
- [ ] Report-path presence/absence verified and recorded as a deliberate decision.
- [ ] D4/D5 status and D7 verdict recorded.
- [ ] Coverage/findings/verification/limitations tables present with IDs and citations.
- [ ] No application code or docs modified.

## Next

Update the PLAN's substep table (54.4 → Done) and tell the user: *"run substep 54.5"* — in a **fresh chat**.
