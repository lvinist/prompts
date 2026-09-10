# mine-flow — STEP-54.6: Teams Suite 2 — Daily Logging Critique

> **How to run:** Tell your agent *"run substep 54.6"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.

**Assigned model: Gemini 3.1 Pro High.** Real design critique, bounded by blueprint D1–D8, Doc 07, and the 54.1 rubric; consolidation at 54.11 catches weak findings.

## Context

STEP-54 critiques each feature as a cohesive lifecycle (List → Form sheet → Detail → Report dialog) across Web (desktop) and Android. This substep covers **Daily Logging** — the timeline of log entries with weather/hazard chips, the structured log entry form, and the daily log report. This feature carries the densest structured-entry form in the app (weather conditions, hazards, work notes) and is the workflow STEP-48's design review exercised most (its screenshots — later retracted as placeholders — covered the daily-log list and form).

Preconditions: 54.0 (clean trunk, branch `step-0054-feature-cohesion-critique`), 54.1 (rubric in `mine-flow-STEP-54.1-FINDINGS.md`).

## Read these first

- `Upcoming Prompts/mine-flow-STEP-54-PLAN.md` — STEP PLAN (evidence standard, D1–D8, ground rules)
- `Upcoming Prompts/mine-flow-STEP-54.1-FINDINGS.md` — **the rubric**. Apply it exactly; IDs are `FC-54.6-NNN`.
- `Code/mine-flow-docs/reports/2026-09-10-step-54-55-design-blueprint.md` — D1–D8; blueprint §54.6 names this feature's surfaces
- `Code/mine-flow-docs/reports/2026-08-30-step-0048-runtime-design-review.md` — prior review coverage of daily-log list/form (note which claims were retracted as placeholder-evidence — re-deriving them honestly is exactly this STEP's job)
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` — UI canon
- `Code/mine-flow-docs/architecture/04-data-model.md` — log entry structure (weather, hazards, notes)
- `Code/mine-flow-app/README.md` + `ARCHITECTURE.md`
- root `.throughstone/local-user.md`

## Scope

**Surfaces** (paths as of 2026-09-10; re-locate on the branch head — under `lib/features/daily_log/`):
- List: `lib/features/daily_log/presentation/pages/daily_log_list_screen.dart`
- Form: `lib/features/daily_log/presentation/pages/daily_log_form_screen.dart`
- Weather/hazard chips: locate the chip widgets (feature widgets/ or shared)
- Report path: navigation from list to the reporting pages / `pdf_service.dart` — trace the actual path (contextual per D6 or redirect?)
- BLoC states: `lib/features/daily_log/presentation/bloc/`

**Does NOT touch:** application code (read-only), other features, the rubric.

## Your task

Apply every 54.1 rubric dimension, both platforms (Web desktop, Android portrait):

1. **Lifecycle cohesion:** List → log entry form → back → report. State survival across the round-trip (date filter, scroll position); edit flow (form pre-fill).
2. **Weather/hazard chips:** selection semantics (multi-select? exclusive?), visual state when selected vs. not, color-independence (icon+label, not color alone), touch targets on mobile. Are hazard levels (severity) expressed, or just presence?
3. **Structured entry ergonomics:** the form's information architecture — field grouping, ordering vs. actual field-work sequence, keyboard-type correctness on mobile (numeric fields getting numeric keyboards), free-text areas sized for note-length content.
4. **Form → sheet migration spec:** this is the app's densest form — spec its D1/D2 migration specifically addressing **sheet height**: scrollable content within a bottom sheet on mobile, within the 480–600dp right sheet on Web; D4 dirty-intercept status (long notes are exactly where accidental dismissal hurts most); D5 deep-link gap — the router shows `daily-log/form` exists; verify and critique its URL semantics.
5. **Report dialog:** D6 conformance — pre-bound daily-log ReportType, list date filters preserved behind the dialog.
6. **Interaction states, a11y, tokens:** all rubric dimensions; anchored-grep residual Material.
7. **D7 verdict:** detail view for individual log entries (read view distinct from edit form?) or list+form suffices?

## Verification (evidence standard — mandatory)

- Every finding: `FC-54.6-NNN` ID, verdict (`Aligned`/`Needs polish`/`Needs restructure`/`Unverified`), `file:line` citation, one-sentence why (Explanatory style).
- Runtime optional and honest: name the command, report artifact byte-size + pixel dimensions; 1×1-placeholder class = harness-defect call-out. Unverifiable → `Unverified` + blocker.
- No code changes: app repo `git status` clean at the end.
- Findings file: `Upcoming Prompts/mine-flow-STEP-54.6-FINDINGS.md` — coverage table, findings table, verification record, limitations.

## Keeping the docs true  (always)

- Findings only — no doc edits (54.11 consolidates). Escalate (and record) on: D1–D8/ADR conflicts, runtime contradicting Doc 07, unevidenced runtime claims, same classification problem twice.
- Accepted-risk-shaped discoveries go to findings for 54.11's reconciliation.

## Definition of done

- [ ] All rubric dimensions scored, both platforms, with the dense-form/sheet-height question addressed in depth.
- [ ] Weather/hazard chip semantics and color-independence explicitly evidenced.
- [ ] D4/D5 status and D7 verdict recorded.
- [ ] Coverage/findings/verification/limitations tables present with IDs and citations.
- [ ] No application code or docs modified.

## Next

Update the PLAN's substep table (54.6 → Done) and tell the user: *"run substep 54.7"* — in a **fresh chat**.
