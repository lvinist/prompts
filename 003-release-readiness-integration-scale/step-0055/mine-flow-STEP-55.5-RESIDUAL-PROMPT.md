# mine-flow — STEP-55.5 RESIDUAL: Material FAB purge on the list screen, runtime audit, findings hygiene

> **How to run:** Tell your agent "run 55.5 residual fix only". Execute cold in a fresh chat.
>
> **Assigned model: Gemini 3.1 Pro High.** Same tier as 55.5 — the batch-sheet state model is the
> subtle part; the residual is bounded and Material-purge-verbatim.

## Context

The Crew Attendance rebuild is the strongest of the four lanes audited. `AttendanceCrewDraft`
really starts a roster member **unset** (null status, never pre-marked present);
`AttendanceFormBloc._onBulkMarkPresent` (`:204-217`) skips already-set rows; the sync indicator is
a genuinely separate widget (`_AttendanceSyncIndicator` in `attendance_crew_card.dart:305+`) with a
labelled `Coba lagi` retry; submit validates all rows and surfaces `firstInvalidUserId` for the
focus/scroll; the `copyWith(clearStatus:/clearRemarks:)` sentinels close the keep-old bug; and the
form route is durable (`/teams/attendance/form?date=&siteId=`, cold-reconstructable). Tests are
real: 11 draft-model + 12 form-BLoC + 8 sheet widget tests covering the unset-roster, bulk
exceptions, confirmation-on-discard, cold route, and 48dp cases.

The audit (2026-09-21, this file) left three residuals. Fix only those.

## Residual scope (exact — nothing else)

1. **Material `FloatingActionButton` residuals on the list screen (P1).**
   `attendance_screen.dart:224` and `:238` still render a Material `FloatingActionButton` and
   `FloatingActionButton.extended` — one for the contextual report, one for `Input Absensi`. This
   contradicts spec §4.4 item 9 / `FC-54.5-011` read with the STEP-55 PLAN ground rule "no
   unbounded Material form control remains", and it is the exact class of residual 55.7 purged
   from `equipment_history_screen.dart` (which now uses an `FButton` in a `Positioned` overlay —
   see `daily_log_list_screen.dart:250-262` for the approved pattern, including the
   `Material(color: Colors.transparent, child: _buildBody(...))` host that overlay stacking
   requires). Replace both FABs with ForUI `FButton`s in a `Positioned` overlay, preserving:
   - the report button's `Semantics(label: 'Buat Laporan Kehadiran')` accessible label,
   - the `_openContextualReport(state)` seeding by selected date/site (spec §4.4 item 10),
   - the `_openAttendanceForm(state)` push that keeps the list mounted beneath the sheet
     (spec §4.4 item 7), and
   - the existing disabled-when-`AttendanceLoaded` gating.
   Pin with widget tests in `test/widget/attendance_screen_test.dart` — it currently has zero FAB
   assertions, which is why this slipped through.
2. **`FC-54.5-004,013` runtime audit stays Unverified at this lane** (same 55.11 deferral as
   55.2/55.3/55.4). Add mechanical coverage only: fresh-roster-unset rendering, bulk action with
   mixed unset/existing exceptions, the four mappings' icon+text pairing, reason
   reveal/trim/confirmation, dirty dismissal, sync indicator states, calendar dialog, 48dp
   targets, 2.0x text, and light/dark where the harness allows. Do not claim runtime verification
   you did not run.
3. **Findings hygiene + status flip.** The index row 55.5 is still `Planned` even though the code
   landed at `116bb19` and the 55.11 close report already lists attendance as migrated — the flip
   the 55.2/55.3 residual lanes also carry. Once the residual is in, the row should read `Done`
   with a residual note (mirror the 55.0/55.1 row shape: one-line scope + "Residual (audit
   2026-09-21): ..." clause). Also append a dated "Residual fix (55.5)" section to
   `mine-flow-STEP-55.5-FINDINGS.md` with the exact commands and counts; the existing file is
   good but has no post-55.11 reconciliation.

## Read first

- `Upcoming Prompts/mine-flow-STEP-55-PLAN.md` (evidence contract + ground rules)
- Master spec §4.4 (all 11 items), §2.1-2.4 (sheet geometry/modality), §3.1 (D6 report)
- `Upcoming Prompts/mine-flow-STEP-55.5-PROMPT.md`, `mine-flow-STEP-55.5-FINDINGS.md`
- `lib/features/attendance/presentation/pages/attendance_screen.dart` (FAB block ~210-250,
  popover-first status filter ~589-640, `AppCalendarDialog.showSingle` ~394)
- `lib/features/attendance/presentation/pages/attendance_form_sheet.dart`,
  `presentation/bloc/attendance_form_bloc.dart`, `presentation/widgets/attendance_crew_card.dart`
- `lib/features/daily_log/presentation/pages/daily_log_list_screen.dart:236-264` — the approved
  ForUI overlay pattern to copy
- `lib/features/equipment_check/presentation/pages/equipment_history_screen.dart` — the post-purge
  reference (report via `showAppContextualReportDialog`, no FAB)
- `test/widget/attendance_screen_test.dart`, `test/features/attendance/presentation/**`,
  `test/unit/attendance_crew_draft_test.dart`, `test/unit/attendance_model_test.dart`

## Pre-flight (do not skip)

1. `git status --short --branch` + `git log --oneline -5` in `Code/mine-flow-app`. The shared
   branch `step-0055-cohesive-ui-rebuild` moved during the audit window (now at `fa9ab71`, which
   landed the 55.2/55.3 residual lane). Pull before branching; preserve untracked scratch
   (`.step55.11*` scripts, `run_web_wrapper.dart`, `m2_challenger_stress_test.dart`) and never
   stash/reset/absorb another lane's dirt.
2. Serialize with the 55.4 lane if it is in flight — both touch `lib/l10n/` and the l10n guard.
   This lane owns `attendance_screen.dart` and `test/widget/attendance_screen_test.dart`.

## Likely files (ownership boundary)

- ALLOWED: `attendance_screen.dart`, `test/widget/attendance_screen_test.dart`,
  `Upcoming Prompts/mine-flow-STEP-55.5-FINDINGS.md` (append), `prompts/STEP-index.md` (row 55.5
  status flip + evidence cell only — one hunk, trunk push per the collaboration runbook).
- FORBIDDEN: `attendance_form_sheet.dart` / `attendance_crew_card.dart` /
  `attendance_form_bloc.dart` internals (they passed audit clean — do not churn them), other
  features, `supabase/**`, `lib/l10n/**` unless a new visible string proves necessary (and then the
  ARB workflow + guard).

## Tests and verification

- `flutter test test/widget/attendance_screen_test.dart test/features/attendance/ test/unit/attendance_crew_draft_test.dart test/unit/attendance_model_test.dart`
- `dart format --output=none --set-exit-if-changed <touched files>`
- `flutter analyze`
- `dart run tool/check_l10n_baseline.dart` (expect pass; note `attendance_screen.dart` is on the
  legacy-exempt list — that exemption is **not** license to add new hardcoded strings; reuse
  existing `l10n.*` keys for the two buttons).
- `dart run tool/check_supabase_contracts.dart` (expect pass; no schema change here).
- Record exact commands + counts. ONE commit `fix(55.5): ...`, attendance-owned hunks only.

## Boundaries and escalation

- No nested tabs/pages, default-present draft, UUID labels, hidden inline attendance choices,
  separate member inspector, or false offline-success claim — all already satisfied; do not
  regress them.
- Do not convert the four inline attendance choices into a popover; spec §4.4 item 4 explicitly
  exempts them from the popover-first rule.
- Escalate if the `Material(transparent)` overlay host breaks the existing `RefreshIndicator`
  (`attendance_screen.dart:210`) or the route-aware list reload from 55.11's ATT-03 fix
  (`RouteAware` + `route_observer.dart`) — both are load-bearing on this exact screen.
- Never print secrets.

## Definition of done

- Zero `FloatingActionButton` in `lib/features/attendance/**`; the two actions are ForUI buttons
  with semantics, seeded report, and list-mounted behavior preserved and pinned by tests.
- Runtime audit honestly deferred with mechanical coverage added.
- FINDINGS has a dated "Residual fix (55.5)" section; index row 55.5 is flippable to `Done` (flip
  it as part of this lane's trunk push — this lane owns the flip, unlike 55.4's).
- Gates green.

## Next

Report the exact replacement evidence-cell line for index row 55.5 and confirm the flip landed on
`prompts/main`. Then run the 55.6 residual lane in a fresh chat — it is the heaviest of the four
(the hazard migration must be applied to the live database).
