# mine-flow — STEP-54.5: Teams Suite 1 — Crew Attendance Critique

> **How to run:** Tell your agent *"run substep 54.5"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.

**Assigned model: Gemini 3.1 Pro High.** Real design critique, bounded by blueprint D1–D8, Doc 07, and the 54.1 rubric; consolidation at 54.11 catches weak findings.

## Context

STEP-54 critiques each feature as a cohesive lifecycle (List → Form sheet → Detail → Report dialog) across Web (desktop) and Android. This substep covers **Crew Attendance** — the daily roster, status badges (present/absent/late etc.), check-in flow, and the attendance summary report. This is a high-frequency *field* workflow (foremen on Android in low-connectivity conditions mark crews daily), so mobile ergonomics and offline-state honesty carry extra weight here.

Preconditions: 54.0 (clean trunk, branch `step-0054-feature-cohesion-critique`), 54.1 (rubric in `mine-flow-STEP-54.1-FINDINGS.md`).

## Read these first

- `Upcoming Prompts/mine-flow-STEP-54-PLAN.md` — STEP PLAN (evidence standard, D1–D8, ground rules)
- `Upcoming Prompts/mine-flow-STEP-54.1-FINDINGS.md` — **the rubric**. Apply it exactly; IDs are `FC-54.5-NNN`.
- `Code/mine-flow-docs/reports/2026-09-10-step-54-55-design-blueprint.md` — D1–D8; blueprint §54.5 names this feature's surfaces
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` — UI canon
- `Code/mine-flow-docs/architecture/04-data-model.md` — attendance statuses and crew semantics
- `Code/mine-flow-app/README.md` + `ARCHITECTURE.md` — offline-first posture (Hive, sync-on-reconnect)
- root `.throughstone/local-user.md`

## Scope

**Surfaces** (paths as of 2026-09-10; re-locate on the branch head — under `lib/features/attendance/`):
- List: `lib/features/attendance/presentation/pages/attendance_screen.dart` (roster)
- Form: `lib/features/attendance/presentation/pages/attendance_form_page.dart` (check-in)
- Status badges: locate the badge widget(s) (likely shared or under the feature's widgets/)
- Report path: navigation from roster to the reporting pages / `pdf_service.dart` — trace the actual path (contextual per D6 or redirect?); attendance summary report
- BLoC states: `lib/features/attendance/presentation/bloc/`

**Does NOT touch:** application code (read-only), other features, the rubric.

## Your task

Apply every 54.1 rubric dimension, both platforms — with deliberate extra weight on Android (the primary field device for this feature):

1. **Lifecycle cohesion:** Roster → check-in sheet → back → summary report. Does marking a crew member return you to the roster with state intact (scroll position, date, filters)?
2. **Status badges:** are statuses visually distinguishable beyond color alone (icon/label — color-blind accessibility)? Consistent badge component across roster, form, and report?
3. **Check-in ergonomics on mobile:** touch-target sizes in the roster row; one-hand reachability of the primary check-in action; how many taps to mark one member present; bulk actions (mark-all) presence/absence and their undo story.
4. **Offline state honesty:** what does the UI show when a check-in is queued offline vs. synced (indeterminate/failed states)? A silently-unsynced check-in is a data-trust defect — record its current-state evidence precisely.
5. **Form → sheet migration spec:** D1/D2 changes; D4 dirty-intercept status; D5 deep-link gap — the router shows `attendance/form` exists; verify and critique its semantics (does it carry member/date context in the URL?).
6. **Report dialog:** D6 conformance — pre-bound attendance ReportType, roster filters/date preserved behind the dialog.
7. **Interaction states, a11y, tokens:** all rubric dimensions; anchored-grep residual Material.
8. **D7 verdict:** does attendance need a detail view (per-member history?) or roster+form suffices for MVP scope?

## Verification (evidence standard — mandatory)

- Every finding: `FC-54.5-NNN` ID, verdict (`Aligned`/`Needs polish`/`Needs restructure`/`Unverified`), `file:line` citation, one-sentence why (Explanatory style).
- Runtime optional and honest: name the command, report artifact byte-size + pixel dimensions; 1×1-placeholder class = harness-defect call-out. Unverifiable → `Unverified` + blocker.
- No code changes: app repo `git status` clean at the end.
- Findings file: `Upcoming Prompts/mine-flow-STEP-54.5-FINDINGS.md` — coverage table, findings table, verification record, limitations.

## Keeping the docs true  (always)

- Findings only — no doc edits (54.11 consolidates). Escalate (and record) on: D1–D8/ADR conflicts, runtime contradicting Doc 07, unevidenced runtime claims, same classification problem twice. **Offline-sync honesty findings** are named escalation triggers — a check-in that looks saved but isn't synced is a data-integrity class, not polish.
- Accepted-risk-shaped discoveries go to findings for 54.11's reconciliation.

## Definition of done

- [ ] All rubric dimensions scored, both platforms, with the Android/offline lens applied in depth.
- [ ] Badge color-independence and offline-state honesty explicitly evidenced.
- [ ] D4/D5 status and D7 verdict recorded.
- [ ] Coverage/findings/verification/limitations tables present with IDs and citations.
- [ ] No application code or docs modified.

## Next

Update the PLAN's substep table (54.5 → Done) and tell the user: *"run substep 54.6"* — in a **fresh chat**.
