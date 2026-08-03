# mine-flow — STEP-40 PLAN: Phase 2 Tier 2 Check-in Test Suite Bug Fixes

**Phase:** Phase 2
**Owner:** Antigravity
**Status:** Done
**Date:** 2026-08-03
**Branch:** `step-0040-check-in-test-suite-bugfixes`
**Repos (projection):** `Code/mine-flow-app`

> This STEP fixes the 8 test failures uncovered during the Phase 2 Tier 2 check-in (STEP-39).
> The check-in report (`reports/2026-07-28-phase2-tier2-check-in-report.md`) documented 7 failures;
> a fresh `flutter test` run confirms **8 failures** (the smoke test `widget_test.dart` is a
> new regression surfaced since STEP-39 closed, likely from a ForUI `FAccessibilityScope` API
> change that also affects the daily log form tests).

## Motivation

STEP-39 fixed test-suite infrastructure issues (semantics renderer, battery abstraction, low-battery
sync logic) but explicitly left 7 failing widget/integration tests for this STEP. The full current
failure set is:

| # | Test file | Test name | Root cause |
|---|-----------|-----------|------------|
| 1 | `test/widget_test.dart` | app launches without crashing | `LoginPage` uses `FButton` but `FAccessibilityScope` is not found in the test widget tree |
| 2 | `test/widget/daily_log_screen_test.dart` | should render all form fields… | `buildFormScreenWidget()` in the test has no `FTheme` wrapper — `FButton` crashes |
| 3 | `test/widget/daily_log_screen_test.dart` | should show validation error… | Same missing `FTheme` wrapper |
| 4 | `test/widget/daily_log_screen_test.dart` | should call submitDailyLog… | Same missing `FTheme` wrapper |
| 5 | `test/widget/daily_log_screen_test.dart` | should select weather chip… | Same missing `FTheme` wrapper |
| 6 | `test/widget/attendance_screen_test.dart` | should update summary counts when status chip is toggled | `AttendanceScreen` renders `CrewRosterItem(readOnly: true)` — tapping `StatusToggleChips` (disabled) has no effect; 'Belum Disimpan' badge never appears; test expects interactive edit that was moved to `AttendanceFormPage` in STEP-38 |
| 7 | `test/widget/attendance_screen_test.dart` | should call saveAttendanceBatch when save button is pressed | `Simpan Absensi (N Kru)` button lives in `AttendanceFormPage`'s bottom bar, not in `AttendanceScreen` |
| 8 | `test/integration/sync_queue_manager_test.dart` | handles retries and marks failed items after exceeding max retries | `Expected: <2>, Actual: <1>` — `_isProcessing` guard on `SyncQueueManager.processQueue()` is still `true` from the `unawaited` first call when the manual second call is made 100 ms later; the item is marked `failed` (retryCount=1) but the second `processQueue()` returns immediately because `_isProcessing` has not yet been cleared |

## Root-cause grouping

### Group A — Missing `FTheme`/`FAccessibilityScope` in test widget trees
**Failures:** 1, 2, 3, 4, 5 (smoke test + 4 daily-log form tests)

`FButton` (and other ForUI tappable widgets) calls `FAccessibilityScope.focusHighlightOf(context)`,
which does a null-asserting lookup of the `FAccessibilityScope` inherited widget injected by `FTheme`.
When a test's `pumpWidget` call doesn't have `FTheme` in the widget tree, the lookup throws
`Null check operator used on a null value`.

- `test/widget_test.dart` pumps `MineFlowApp` directly; the production `app.dart` puts `FTheme`
  in `MaterialApp.router`'s `builder` callback, which means it is available inside router-driven
  pages at runtime — but the smoke test was passing before because the initial route rendered
  without a visible `FButton` at pump time. A code change has since moved or added an `FButton`
  to the initial (login) page that is now hit during `pumpWidget`.
- `test/widget/daily_log_screen_test.dart`'s `buildFormScreenWidget()` and `buildListScreenWidget()`
  wrap with `MaterialApp(theme: ThemeData(useMaterial3: true), …)` but omit the `FTheme` builder —
  unlike `attendance_screen_test.dart` which has `MaterialApp(builder: (_, child) => FTheme(…))`.

**Fix:** Add `FTheme` to the affected test widget trees via `MaterialApp`'s `builder` parameter.
For the smoke test, investigate whether the root `FTheme` in `app.dart` is sufficient or needs
to be moved inside the `builder` callback.

### Group B — `AttendanceScreen` test expectations vs. post-STEP-38 architecture
**Failures:** 6, 7

STEP-38 extracted bulk-edit functionality into a dedicated `AttendanceFormPage`
(`/teams/attendance/form`). The `AttendanceScreen` now shows a **read-only** attendance roster
(history view). The two failing tests in `attendance_screen_test.dart` test:
- Tapping a `StatusToggleChips` widget to trigger `hasUnsavedChanges` → `Belum Disimpan` badge.
- Tapping `Simpan Absensi (2 Kru)` button to call `saveAttendanceBatch`.

Both interactions now belong to `AttendanceFormPage`, not `AttendanceScreen`. The tests must be
migrated to target the correct screen.

**Fix:** Update the two failing tests to target `AttendanceFormPage` with `readOnly: false` roster
items and a populated initial record list so the bottom-bar save button is rendered, verifying the
same user-facing behaviours through the correct widget.

### Group C — `SyncQueueManager` retry test is timing-sensitive
**Failure:** 8

`enqueueMutation()` calls `processQueue()` via `unawaited()`. The test then awaits
`Future.delayed(100 ms)` and immediately calls `processQueue()` again. If the first
`processQueue()` has not yet cleared `_isProcessing = false` (it is a guarded lock), the
second call returns early, and the `customSyncHandler` is never called a second time
(`attemptCounter` stays at 1 instead of reaching 2).

The 100 ms delay is not a reliable synchronisation barrier. The fix should make the test
deterministic without relying on wall-clock timing.

**Fix options (prefer Option A):**
- **Option A (preferred):** Change the test to call `processQueue()` twice with `await` instead
  of relying on the unawaited side-effect. After `enqueueMutation`, call `await
  syncQueueManager.processQueue()` directly to drive the first attempt; then call it again for the
  second attempt. Remove the `Future.delayed`. This avoids the race condition entirely.
- **Option B (production-side):** Replace the `unawaited(processQueue())` guard with a pending-
  future tracker so that a second call can `await` the existing in-flight run rather than
  returning immediately. This is a larger production-code change and should only be done if
  Option A is not feasible.

## Substeps

| # | Title | Produces | Depends on |
|---|-------|----------|------------|
| 40.1 | Fix `FTheme` wrappers in `daily_log_screen_test.dart` (4 form failures) | 4 green daily-log form tests | — |
| 40.2 | Migrate 2 `AttendanceScreen` tests to `AttendanceFormPage` | 2 green attendance tests | — |
| 40.3 | Fix `SyncQueueManager` retry test timing race | 1 green integration test | — |
| 40.4 | Fix smoke test (`widget_test.dart`) `FAccessibilityScope` crash | 1 green smoke test | 40.1 (establishes the FTheme pattern) |
| 40.5 | Full verification and close | All 8 failures resolved, analyzer clean, `flutter test` green | 40.1–40.4 |

## Test plan

| Test tier | Substep | Files to touch | Gate command |
|-----------|---------|----------------|--------------|
| Widget | 40.1 | `test/widget/daily_log_screen_test.dart` | `flutter test test/widget/daily_log_screen_test.dart` |
| Widget | 40.2 | `test/widget/attendance_screen_test.dart` | `flutter test test/widget/attendance_screen_test.dart` |
| Integration | 40.3 | `test/integration/sync_queue_manager_test.dart` | `flutter test test/integration/sync_queue_manager_test.dart` |
| Smoke | 40.4 | `test/widget_test.dart` (+ `lib/app/app.dart` if needed) | `flutter test test/widget_test.dart` |
| All | 40.5 | — | `flutter test` (full suite) + `flutter analyze` |

## Open questions

None — all failures have been diagnosed with confirmed root causes.

## Ground rules

- **Test-first awareness:** each substep's deliverable is a green test file, verified in isolation
  before moving to the next substep.
- **Production-code changes are minimal:** prefer fixing the test over changing production code
  where root cause is in the test. Exception: the smoke test (`widget_test.dart`) may require a
  small production fix in `app.dart` if `FTheme` placement is genuinely wrong.
- **No new features:** this is a pure bug-fix STEP; no UI changes, no new behaviour.
- **Analyzer gate:** `flutter analyze` must remain clean after each substep.

## Definition of done

- [x] 40.1: All 4 `DailyLogFormScreen` widget tests pass.
- [x] 40.2: Both failing `AttendanceScreen` tests pass in their new `AttendanceFormPage` form.
- [x] 40.3: `SyncQueueManager handles retries and marks failed items after exceeding max retries` passes.
- [x] 40.4: `app launches without crashing` smoke test passes.
- [x] 40.5: `flutter test` full suite exits 0 (416+ passing, 0 failing); `flutter analyze` clean.
- [x] STEP archived to `prompts/002-phase2/step-0040/` and index row flipped to **Done**.
