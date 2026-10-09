# mine-flow — STEP-55.3 RESIDUAL-2: adopt the shared popover in the Land Clearing list

> **How to run:** Tell your agent "run 55.3 residual-2 fix only". Execute cold in a fresh chat.
>
> **Assigned model: Gemini 3.1 Pro High.** Same tier as 55.3 — bounded adoption of tested 55.0/55.2 primitives.

## Context

The 2026-09-21 residual review re-verified the 55.3 residual lane against disk: two-way tab↔URL sync is implemented (`_resolveTabIndex`/`_syncTabToRoute` with `context.replace`, `didUpdateWidget` driving the tab controller), the FTabs interop justification header is present (three named FTabs gaps: nested-Localizations insertion, horizontal-only labels with 130px overflow, no independent query-string listening), cold-ID validation + recoverable `AppStatePanel` are in the BLoC and both screens, and the `FC-54.3` traceability was rewritten with counts (focused 33: entry 15, deep-link 6, bloc 12; full tracking 146; format/analyze/supabase-contracts clean; CRLF convention preserved). That work is verified complete and was committed as `fa9ab71` (plus `fefca36` for 55.2) — both unpushed.

One deviation from the docs was found:

- **The Land Clearing list still uses `ZoneFilterDropdown` + `_buildFilterChip` rows** (`lib/features/tracking/presentation/pages/land_clearing_list_screen.dart:327,342,350,485`). Master spec §1 review item 9 and the primitive table say popover-first filtering applies to "**all list/dashboard surfaces**" (user review gate). The 55.2 residual lane adopted the shared `AppFilterPopover` in the Cut & Fill list (committed `fefca36`, proven by 11 list-screen tests including popover open/apply/reset/cancel, focus return, and narrow-mobile layout) — but no lane adopted it in the LC list. The 55.3 residual prompt's scope did not name the LC list (its ALLOWED list only touched it "if inspector entry needs touch"), so the adoption fell through the gap between lanes. This is a fix-completeness failure of the audit wave, not new scope.

## Residual scope (exact — nothing else)

1. Adopt the shared `AppFilterPopover` in the Land Clearing list, mirroring the proven Cut & Fill pattern (committed `fefca36` — read its `cut_fill_list_screen.dart` implementation as the recipe, do not reinvent):
   - One labelled `Filter` entry opening `showAppFilterPopover` with an `AppFilterPopover` body;
   - Grouped criteria: date range via `AppCalendarDialog.showRange`, zone via `ZoneFilterDropdown` backed by `ZoneCubit` (as applicable to LC's list filters — LC's spec acceptance only requires preserving date/zone filters, spec §140 route table);
   - Popover actions `Terapkan` / `Reset filter` / `Batal` wired to the list's filter state: apply and reset commit + reload + dismiss; cancel dismisses without mutating;
   - Active-filter summary only (single-line, no permanent pill row, no horizontal overflow);
   - Preserve list BLoC state, scroll position, invoker focus return, query parameters, and the existing contextual `ReportType.landClearing` report integration. No route navigation while the menu is open.
2. Extend `test/features/tracking/presentation/land_clearing_list_screen_test.dart` (or create it if absent — verify first) with mechanical coverage mirroring the CF tests: popover open, apply, reset, cancel, focus return, narrow mobile (360x640) layout without overflow.
3. `FC-54.3-007` runtime audit stays **Unverified at this lane** (same 55.11 deferral as 55.0–55.2). Do not fabricate captures.

## Read first

- `Upcoming Prompts/mine-flow-STEP-55-PLAN.md` (ground rules, evidence contract)
- `Code/mine-flow-docs/reports/2026-09-11-step-54-master-polish-spec.md` §1 item 9, §140 route table, primitive table (popover-first = all list surfaces)
- `Upcoming Prompts/mine-flow-STEP-55.2-FINDINGS.md` (the proven CF adoption — recipe source)
- `Upcoming Prompts/mine-flow-STEP-55.3-FINDINGS.md` (baseline + residual fix 2026-09-21)
- `lib/features/tracking/presentation/pages/cut_fill_list_screen.dart` (committed `fefca36` — the proven pattern)
- `lib/features/tracking/presentation/pages/land_clearing_list_screen.dart` (current filter UI ~lines 320-360, 485+)
- `lib/core/presentation/widgets/app_interaction_primitives.dart` (`AppFilterPopover`, `AppCalendarDialog`, 55.0's adoption recipe in FINDINGS)

## Pre-flight (do not skip)

1. `git status --short --branch` + `git log --oneline -5` in `Code/mine-flow-app` (expect `step-0055-cohesive-ui-rebuild`). Preserve untracked 55.11 files. Never stash/reset/absorb.
2. **As of the 2026-09-21 review, the tree carried uncommitted 55.0/55.1 residual lanes** (primitives file + test; router report-config hunks + reporting files + tests) and two unpushed commits (`fefca36` fix(55.2), `fa9ab71` fix(55.3)). The 55.0/55.1 residual work is verified complete (review 2026-09-21) — if still dirty, commit it FIRST one-commit-per-substep (`fix(55.0): ...`, `fix(55.1): ...`), or obtain the owner's decision. Never bundle lanes.
3. This lane touches the primitives file's `AppFilterPopover` API only as a consumer — no API change. If a sibling is mid-edit in the LC files, wait or confirm clean (`git diff --name-only`).

## Likely files (ownership boundary)

- ALLOWED: `lib/features/tracking/presentation/pages/land_clearing_list_screen.dart`, `test/features/tracking/presentation/land_clearing_list_screen_test.dart`, ARB via project workflow only if a new visible string proves necessary (note: the shared popover's `Terapkan`/`Reset filter`/`Batal` strings already exist at HEAD in `app_interaction_primitives.dart` — a new LC-specific string is unlikely), `Upcoming Prompts/mine-flow-STEP-55.3-FINDINGS.md` (append only).
- FORBIDDEN: `cut_fill_*`, `land_clearing_entry_screen.dart`/`land_clearing_inspector_screen.dart` (55.3 residual lane owns those — do not touch), reporting dialog internals, `lib/app/router.dart` (no router change in this lane), benchmark/attendance/daily-log/equipment/inventory/data-bucket/shell files.

## Tests and verification

- `flutter test test/features/tracking/presentation/land_clearing_list_screen_test.dart test/features/tracking/presentation/cut_fill_list_screen_test.dart`
- `flutter test test/features/tracking/` (full suite — expect 146+ the new LC popover cases)
- `dart format --output=none --set-exit-if-changed <touched files>`
- `flutter analyze`
- `dart run tool/check_l10n_baseline.dart` if ARB touched; `dart run tool/check_supabase_contracts.dart` (expect pass, no schema change).
- Record exact commands + counts. Commit ONE commit `fix(55.3): ...` (or a distinct `fix(55.3-residual-2)` subject if the owner prefers), stage only LC-owned files.

## Boundaries and escalation

- No inspector change, no schema, no report-type change, no formula change, no local modal invention, no entry-screen edit. Dirty guard stays on the real `hasUnsavedChanges`.
- Stop if the popover can't meet the locked interaction in the LC list without a Material workaround, or if the same fix fails twice. Never print secrets.

## Definition of done

- LC list filters go through the shared popover with calendar dialog, query preservation, focus return, and mechanical tests mirroring the CF suite; runtime `FC-54.3-007` explicitly deferred to 55.11; gates green; FINDINGS has a dated "Residual fix 2 (55.3)" section with commands/counts.

## Next

Report the exact replacement evidence-cell line for index row 55.3 — including whether the row is now flippable to Done (do **not** flip it yourself). Tell the user the 55.0–55.3 residual-2 set is complete and to review all four FINDINGS addenda, then run the next lane (55.4+) or the 55.11 audit.
