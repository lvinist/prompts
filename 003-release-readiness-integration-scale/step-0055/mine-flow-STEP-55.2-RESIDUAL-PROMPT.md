# mine-flow — STEP-55.2 RESIDUAL: Cut & Fill filter adoption + runtime-evidence note

> **How to run:** Tell your agent "run 55.2 residual fix only". Execute cold in a fresh chat.
>
> **Assigned model: Gemini 3.7 Flash High.** Same tier as 55.2 — bounded adoption of tested 55.0/55.1 primitives.

## Context

Cut & Fill is fully migrated on branch `step-0055-cohesive-ui-rebuild` (commit `a74b20a` also carries 55.3's work — history stays as-is; this lane makes its own single commit). Routes, cold-ID fetch with validation, D4 guard, contextual `ReportType.cutFill` prefill, direct-to-edit with no inspector, ForUI cleanup, and formula preservation are all proved green (bloc 13, form 12, list 5, tracking+reporting 134). The audit (2026-09-19, index row 55.2) left two residuals. Fix only those.

## Residual scope (exact — nothing else)

From the index row 55.2:

1. Adopt the shared `AppFilterPopover` in the Cut & Fill list (`lib/features/tracking/presentation/pages/cut_fill_list_screen.dart`, today `ZoneFilterDropdown` + chips). One labelled `Filter` entry, grouped criteria (date range via `AppCalendarDialog.showRange`, zone), `Terapkan` / `Reset filter` / `Batal`, active-filter summary only (no permanent pill row, no overflow). Preserve list BLoC/data, scroll, query params (`from`, `to`, `zoneId`), and invoker focus. No route change while the menu is open.
2. `FC-54.2-007` runtime audit stays **Unverified at this lane** (no Impeccable binary; consolidated evidence is 55.11's lane — Web covered, Android deferred per the close report). Do not fabricate captures. Record the deferral explicitly; add only mechanical coverage (popover open/apply/reset/cancel, focus return, narrow layout) to the widget tests.

## Read first

- `Upcoming Prompts/mine-flow-STEP-55-PLAN.md`
- Master spec §§2.8 (filter/calendar contract), 4.1 items 5–6, Doc 07 §§3–4
- `Upcoming Prompts/mine-flow-STEP-55.2-FINDINGS.md` + `mine-flow-STEP-55.0-FINDINGS.md` (popover contract + adoption recipe)
- `lib/features/tracking/presentation/pages/cut_fill_list_screen.dart` (current filter UI ~lines 327-390, 485+)
- `lib/core/presentation/widgets/app_interaction_primitives.dart` (`AppFilterPopover`, `AppCalendarDialog`)
- `test/features/tracking/presentation/cut_fill_list_screen_test.dart` (extend)

## Pre-flight (do not skip)

1. `git status --short --branch` + `git log --oneline -5` in `Code/mine-flow-app` (expect `step-0055-cohesive-ui-rebuild`). Preserve untracked 55.11 files. Never stash/reset/absorb.
2. Confirm no sibling is mid-edit in the CF list/form files (`git diff --name-only`). If the tree shows LC or other-lane dirt, leave it alone.

## Likely files (ownership boundary)

- ALLOWED: `lib/features/tracking/presentation/pages/cut_fill_list_screen.dart`, `test/features/tracking/presentation/cut_fill_list_screen_test.dart`, ARB via project workflow only if a new visible string proves necessary, `Upcoming Prompts/mine-flow-STEP-55.2-FINDINGS.md` (append only).
- FORBIDDEN: `land_clearing_*`, reporting dialog internals, `lib/app/router.dart` (CF routes already registered — no router change in this lane), benchmark/attendance/daily-log/equipment/inventory/data-bucket/shell files.

## Tests and verification

- `flutter test test/features/tracking/presentation/cut_fill_list_screen_test.dart test/features/tracking/presentation/cut_fill_bloc_test.dart test/features/tracking/presentation/cut_fill_form_screen_test.dart`
- `dart format --output=none --set-exit-if-changed <touched files>`
- `flutter analyze`
- If ARB touched: `dart run tool/check_l10n_baseline.dart`. Plus `dart run tool/check_supabase_contracts.dart` (expect pass, no schema change).
- Record exact commands + counts. Commit ONE commit `fix(55.2): ...`, stage only CF-owned hunks.

## Boundaries and escalation

- No inspector, no schema, no report-type, no formula change, no local modal. Dirty guard stays on the real `hasUnsavedChanges`.
- Stop if popover can't meet the locked interaction without a material workaround, or the same fix fails twice. Never print secrets.

## Definition of done

- CF list filters go through the shared popover with calendar dialog, query preservation, and mechanical tests; runtime `FC-54.2-007` explicitly deferred to 55.11; gates green; FINDINGS has a dated "Residual fix (55.2)" section.

## Next

Report the exact replacement evidence-cell line for index row 55.2 — including whether the row is now flippable to Done (do **not** flip it yourself). Tell the user to run the 55.3 residual in a fresh chat.
