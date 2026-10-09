# mine-flow — STEP-55.4–55.7 Independent Audit (2026-09-21)

**Auditor:** Hermes (independent of the four executors)
**Scope:** implementation verification of STEP-55 substeps 55.4, 55.5, 55.6, 55.7 — code and
evidence only, status cells not trusted.
**App head at audit:** `cb9d510` → `fa9ab71` during the session (the 55.2/55.3 residual lane landed
mid-audit; none of the four audited lanes were touched by it).
**Branch:** `step-0055-cohesive-ui-rebuild`

## Method

Read every claimed file and its tests against the master spec section for that substep
(`Code/mine-flow-docs/reports/2026-09-11-step-54-master-polish-spec.md` §§4.3–4.6) and the
STEP-55 PLAN's evidence contract. Ran the gates the substeps claim (analyze, the two tool guards,
the equipment detail suite, the l10n guard) and probed the live Supabase database directly. Where a
test asserted a global rather than the implementation, the test was temporarily modified to expose
the gap and then reverted.

## Summary verdict

| Substep | Claimed | Actual | Residuals |
|---|---|---|---|
| 55.4 Benchmark | Done | **Mostly done.** P0 projection rejection is real and correct; routes, read-only inspector, contextual report all present. | 4 + hygiene |
| 55.5 Attendance | Planned (code landed) | **Strongest lane.** Nullable draft, bulk exceptions, sync indicator, batch validation, cold route all genuinely implemented and tested. | 3 |
| 55.6 Daily Log | Done | **Well built but does not run against the database it targets.** Migration committed, never applied; contract artifact stale. | 4 + hygiene |
| 55.7 Equipment | Done | **Complete by static gates, one authorization control is silently dead in production.** | 3 |

The pattern across the four: **the code is consistently better than the findings files that
describe it, and the findings files are consistently worse than the PLAN's evidence contract
requires** (55.4 and 55.6 carry no test counts, commands, or file lists). Two of the four defects
found are the kind static gates cannot see: an unapplied migration, and an identifier that
resolves to a process global instead of the session the widget was supposed to read.

## Findings per substep

### 55.4 — Benchmark (PARTIAL)

**Implemented and verified:**
- `FC-54.4-001` P0: `_computeLatLon` (`benchmark_bloc.dart:356-383`) rejects NaN/infinite and
  out-of-±90/±180 results → null; `_onSubmitBenchmark` (`:586-636`) refuses to save on null and
  emits `BenchmarkError`. There is no `0.0, 0.0` fallback on the submit path.
- Routes: `benchmark-form`, `benchmark-detail`, `benchmark-edit` (`router.dart:526-587`), both
  detail and edit accept a path `:id` and fall back to fetch by ID.
- D7 inspector: `AppResponsiveSheetMode.readOnlyInspector`, Edit isolated behind `_openEdit`.
- `FC-54.4-006`: `showAppContextualReportDialog(ReportType.benchmark)` at
  `benchmark_list_screen.dart:87`.

**Residuals:**
1. The CRS recovery message (spec §4.3 item 4 / `FC-54.4-008`) is a hardcoded Indonesian literal
   duplicated in `benchmark_bloc.dart:604` and `benchmark_form_screen.dart:521`, and the three
   benchmark presentation files are on the l10n guard's legacy-exempt list, so the guard does not
   enforce them.
2. The only projection-rejection test seeds `computedLatitude: null` rather than driving
   `_computeLatLon` to null from malformed/out-of-zone input; spec §4.3 item 1 requires that
   coverage.
3. No benchmark cold-route tests exist in `test/app/router_test.dart` (cut-fill and equipment-check
   have them).
4. `FC-54.4-009` runtime audit unverified (55.11 deferral).

### 55.5 — Attendance (STRONG)

**Implemented and verified:** unset-on-load roster draft; bulk action skips set rows
(`attendance_form_bloc.dart:204-217`); four inline choices with 48dp targets; sync indicator as a
separate widget with labelled retry; submit validates all rows and focuses the first invalid;
`copyWith(clearStatus:/clearRemarks:)` sentinels; durable `?date=&siteId=` route; contextual
report; AppFilterPopover status filter; AppCalendarDialog; no member inspector. Test coverage
matches the spec's list (11 + 12 + 8 tests).

**Residuals:**
1. `attendance_screen.dart:224` and `:238` still render Material `FloatingActionButton` and
   `FloatingActionButton.extended` (the report and `Input Absensi` actions) — the exact residual
   55.7 purged from `equipment_history_screen.dart`. `test/widget/attendance_screen_test.dart` has
   zero FAB assertions.
2. `FC-54.5-004,013` runtime audit unverified (55.11 deferral).
3. Index row 55.5 is still `Planned` though the code landed at `116bb19`; FINDINGS has no
   post-55.11 reconciliation.

### 55.6 — Daily Log (WELL BUILT, DOES NOT RUN AGAINST ITS TARGET DATABASE)

**Implemented and verified:** the hazard contract is real end-to-end — migration
`20260912000001_step_55_6_daily_log_hazard_contract.sql` (coherence CHECK, `SECURITY DEFINER`
transition trigger enforcing draft→submitted→approved, supervisor-only approval with
`approved_by = auth.uid()`, approved immutability, foreman own-draft RLS), matching Dart
(`HazardAssessment.isValid`/`normalized()`, `approveDailyLog` rejections), and `Doc 04` v0.1.8.
Tabs are `FTabs` with counts and role defaults; approval is supervisor + submitted-only; autosave
flushes before close (`daily_log_form_sheet.dart:147-168`). 14 + 18 + 9 tests.

**Residuals:**
1. **P0 — the migration was never applied to the live database.** Probed directly:
   `GET /rest/v1/daily_logs?select=hazard_state` →
   `42703 column daily_logs.hazard_state does not exist`; a hazard-bearing insert →
   `PGRST204 Could not find the 'hazard_state' column of 'daily_logs' in the schema cache`. Every
   hazard-bearing Daily Log write fails at the server. `20260913000001_step_55_8_inventory_transactions.sql`
   is likewise unapplied (`inventory_transactions` absent from the live schema cache).
2. **`supabase/types/database.ts` is stale**: `daily_logs.Row` omits all four hazard columns though
   the migration has been committed since 2026-09-13.
3. The contract guard (`check_supabase_contracts.dart`) cannot detect this — it checks artifact
   shape and migration/artifact commit pairing, not artifact-vs-database agreement. It passed
   during this audit while the drift was live.
4. The `Setujui Log` confirmation is still a Material `AlertDialog` with `TextButton`/
   `FilledButton` (`daily_log_list_screen.dart:169-191`) while the delete path on the same screen
   already uses the shared `confirmDestructiveAction` helper.
5. `FC-54.6-010` runtime/authorization audit unverified (55.11 deferral).

### 55.7 — Equipment Check (COMPLETE STATICALLY, ONE CONTROL IS DEAD IN PRODUCTION)

**Implemented and verified:** route-backed detail fetching by ID; `ExpansionTile` removed;
read-only inspector with `mobileFullPage` override; not-found and access-denied panels; D4 dirty
guard; 48dp dual icon+text PASS/FAIL; session-derived foreman identity; contextual report
preserving list state; zero actionable Material residuals. 27 focused tests pass and were re-run
during this audit (8/8 green on the detail suite).

**Residuals:**
1. **P1 — `equipment_check_detail_screen.dart:237` reads `final user = authCubit?.state.user;` but
   `authCubit` is not a field, parameter, local, or import of that file.** It resolves only
   because `auth_cubit.dart:16` declares a process-wide global set in `main.dart:60`; `dart
   analyze` therefore reports "No issues found" and cannot see the defect. The tests pass only
   because `test/widget/equipment_check_detail_screen_test.dart` seeds that global in `setUp`.
   Proven by modification: removing the seed flipped 4 of 8 tests to fail, including the
   supervisor-only delete ones. `main.dart` never provides the cubit into the widget tree for this
   route and the screen never reads it from the tree, so the `isSupervisor` footer gate is
   unverified against the actual authenticated session in a routed context. (The global itself is
   legitimate production state — `currentUserId()`, `isAuthorizedSite()`, and the router redirect
   all read it; the defect is the screen's resolution path.)
2. `FC-54.7-007` runtime audit unverified (55.11 deferral).
3. FINDINGS attributes a widget-tree assertion ("zero ElevatedButton/Card/TextButton") to
   Impeccable, and the file admits `impeccable` was never runnable in its environment.

## Gates re-run this audit

| Gate | Command | Result |
|---|---|---|
| Static analysis (file) | `dart analyze lib/features/equipment_check/presentation/pages/equipment_check_detail_screen.dart` | `No issues found!` — **despite the defect above** |
| Equipment detail suite | `flutter test test/widget/equipment_check_detail_screen_test.dart` | 8/8 pass (with the global seeded) |
| l10n guard | `dart run tool/check_l10n_baseline.dart` | `[OK]` — 22 scanned / 47 exempt |
| Contract guard | `dart run tool/check_supabase_contracts.dart` | `[OK] Contract verification passed` — **while the artifact disagrees with the live DB** |
| Live DB probe | `GET .../rest/v1/daily_logs?select=hazard_state` | `400 — column does not exist` |

## Notes for the residual lanes

- The four lanes are file-level independent **except** `lib/l10n/` and
  `tool/check_l10n_baseline.dart` (55.4 and 55.5 both) and `supabase/**` + `tool/` (55.6 alone).
  Serialize the shared-file pair.
- 55.6 is the only lane that changes shared infrastructure (a database). It needs the user's
  `supabase login` and a `db push` coordination step; the residual prompt escalates rather than
  working around missing credentials.
- Index rows: 55.4, 55.6, 55.7 read `Done`; 55.5 reads `Planned`. The residual prompts instruct the
  executors to report the replacement evidence-cell line and (for 55.5 only, whose code is landed
  and clean apart from the FAB) to flip. The 55.6 evidence cell must record the migration-drift
  incident regardless of the fix's outcome.
