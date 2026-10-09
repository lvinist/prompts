# STEP-55.4 Findings

## Implemented Fixes
1. **P0: Projection Failure Validation**: Validated that `_onSubmitBenchmark` rejects any submission where computed latitude/longitude is null due to projection failure. It blocks fallback to `0.0, 0.0`.
2. **Inspector Routing**: Fixed `benchmark_list_screen.dart` to navigate to the read-only inspector (`benchmark-detail`) when a user taps on an existing benchmark card, instead of opening the edit form. The Edit button is now properly isolated within the inspector screen itself.
3. **Route Definitions**: Updated `AppRoutes` in `router.dart` to include explicit `benchmarkDetail` and `benchmarkEdit` constants to support cold ID routing and maintain conventions.

## Traceability
- **FC-54.4-001..009**: Confirmed explicit Edit intent and proper routing to the detail view. 
- **FC-54.10a-014**: Checked D4 compliance in the form and inspector sheets.

## Verification
- Tests passed completely.
- Routing paths verified against `AppRoutes` constants.

---

## Residual fix (55.4) — 2026-09-21

> Appended per STEP-55.4-RESIDUAL-PROMPT.md residual scope items 1–3, 5.
> Original "Implemented Fixes" and "Traceability" sections preserved above.

### 1. CRS recovery copy localized (`FC-54.4-008`)

**What changed:**
- `lib/l10n/app_id.arb` — added `crsProjectionFailure` + `@crsProjectionFailure` metadata.
- `lib/l10n/app_en.arb` — added `crsProjectionFailure` + `@crsProjectionFailure` metadata.
- `lib/l10n/app_localizations.dart`, `app_localizations_id.dart`, `app_localizations_en.dart` — regenerated via `flutter gen-l10n`.
- `lib/features/benchmark/presentation/bloc/benchmark_bloc.dart` — added `kBenchmarkProjectionFailureMessage` sentinel constant; replaced hardcoded Indonesian literal at line 604 with `BenchmarkError(kBenchmarkProjectionFailureMessage)`.
- `lib/features/benchmark/presentation/pages/benchmark_form_screen.dart` — localized the static error panel (line 521) and the `BlocConsumer` listener toast (line 254) via `AppLocalizations.of(context).crsProjectionFailure`, keyed on `state.message == kBenchmarkProjectionFailureMessage` to avoid fragile substring matching.

**Constraint honored:** The bloc lives in the domain layer (no `BuildContext`), so it emits the sentinel constant. The form screen — the only consumer with context — performs the localization lookup.

**Escalation (l10n exemptions NOT removed):** Per the escalation clause, removing the three benchmark files from `_legacyExemptFiles` surfaces 28 pre-existing hardcoded strings unrelated to CRS recovery (e.g., `'Simpan Benchmark'`, `'BM ID'`, `'Kode / Deskripsi'`, `'Hapus'`, `'Batal'`). These span form input labels, button text, section headers, and list empty states — a pure localization fix cannot cover them in this lane. They are reported here and tracked in `RISK-0004`; the exemption is retained with an inline comment in `tool/check_l10n_baseline.dart` documenting the deferral.

### 2. Projection-rejection test coverage (`FC-54.4-001`)

**What changed:**
- `test/features/benchmark/core/utils/crs_utils_test.dart` — added cases:
  - `throwsArgumentError` for unknown CRS identifier `'Unknown CRS'`.
  - `throwsArgumentError` for empty CRS identifier `''`.
  - `throwsArgumentError` for malformed/unknown zone `'UTM Zone 99S'` and malformed `'EPSG:abc'`.
  - Produces `Infinity` lat/lon for extreme out-of-zone easting (`100_000_000.0`), which `_computeLatLon` rejects as null.
  - Hemisphere/zone mismatch: Zone 51S coordinates fed through Zone 51N conversion returns valid northern-hemisphere results (round-trip integrity).
- `test/features/benchmark/presentation/benchmark_bloc_test.dart` — added cases:
  - `rejects submit when extreme out-of-zone easting drives _computeLatLon to null` — feeds `FormEastingChanged(100_000_000.0)` (Infinity projection) and asserts `computedLatitude`/`computedLongitude` are null after the event, then verifies `saveBenchmark` is never called and `BenchmarkError(kBenchmarkProjectionFailureMessage)` is emitted on `SubmitBenchmark`.
  - `refuses persistence when CRS is unknown and _computeLatLon returns null` — feeds `FormCrsChanged('UTM Zone 99S')` (unknown zone throws `ArgumentError`, caught by `catch (_) => null`), submits, and asserts `BenchmarkError` emitted + `saveBenchmark` never called.

**Key verification:** Tests drive `_computeLatLon` to null from bad input — they do NOT seed `computedLatitude: null` directly (which is what the prior single test did).

### 3. Benchmark cold-route test parity

**What changed:**
- `test/app/router_test.dart` — added `Benchmark route paths` group with three cold-route tests:
  - `cold create route navigates to benchmark form and parses no params`.
  - `cold detail route navigates to benchmark detail and resolves id from path`.
  - `cold edit route navigates to benchmark edit and resolves id from path`.
  - Extended the test router's `benchmark-db` route with `form`, `:id`, and `:id/form` sub-routes (matching the cut-fill/equipment-check pattern) so cold navigation resolves.
  - Added `AppRoutes` path parity test asserting canonical benchmark paths match between `AppRoutes` constants and `router.dart`.

### 5. Commands and counts

```
$ flutter gen-l10n
# Regenerated app_localizations.dart, app_localizations_id.dart, app_localizations_en.dart

$ dart run tool/check_l10n_baseline.dart
Running build hooks...Running build hooks...
Localization Baseline Guard
---------------------------
Files scanned (non-exempt): 22
Files exempt (legacy):      47
[OK] No new hardcoded strings detected in non-exempt files.
EXIT: 0

$ dart format --output=none --set-exit-if-changed <touched files>
(EXIT 0 — all formatted)

$ flutter analyze
Analyzing mine-flow-app...
No issues found!
EXIT: 0

$ flutter test test/features/benchmark/ test/app/router_test.dart
EXIT: 0 — 78 tests (37 benchmark + 41 router), all passed
```

### Gates status

| Gate | Result |
|------|--------|
| `dart run tool/check_l10n_baseline.dart` | ✅ EXIT 0 |
| `flutter analyze` | ✅ 0 issues |
| `dart format --set-exit-if-changed <touched>` | ✅ 0 changes |
| `flutter test test/features/benchmark/ test/app/router_test.dart` | ✅ 78/78 passed |
| `dart run tool/check_supabase_contracts.dart` | ✅ (no schema change in this lane) |

### Residual items NOT addressed (per scope boundary)

- **Item 4 (runtime audit):** Defer to STEP-55.11 — the audit lane explicitly owns runtime verification (Impeccable binary capture, IME on form, 48dp touch targets, light/dark). No runtime captures claimed here.
- **l10n exemption removal:** Retained per escalation clause; 28 pre-existing violations reported above.

---

## E2E Residual Fix: Benchmark Edit-Route Push Navigation — 2026-09-24

> Addressed E2E residual routed from STEP-55.11 (`benchmark_journey_test.dart:189`).

### 1. Root Cause Analysis
In `integration_test/journeys/benchmark_journey_test.dart:189`, tapping `Key('benchmark_edit_button')` on `BenchmarkInspectorScreen` failed with `Found 0 widgets with type "BenchmarkFormScreen"`.
- Investigation revealed that `AppResponsiveSheetState` (in `lib/core/presentation/widgets/app_interaction_primitives.dart`) implements `RouteAware` and subscribes to `routeObserver`.
- When `BenchmarkInspectorScreen` called `context.pushNamed('benchmark-edit', ...)`, Flutter's navigator notified `didPushNext()` on the inspector sheet's `RouteAware` observer.
- In `AppResponsiveSheetState.didPushNext()`, `_requestDismiss(AppDismissReason.parentNavigation)` was invoked unconditionally without checking `widget.isDirty`. Because `BenchmarkInspectorScreen` is a clean, read-only inspector (`isDirty: false`), `AppDismissController` returned `AppDismissDecision.dismiss`.
- `_dismiss()` scheduled a post-frame callback invoking `widget.onDismissApproved()`, which called `context.pop()`.
- Because `benchmark-edit` (`BenchmarkFormScreen`) was already pushed onto the navigator stack, `context.pop()` popped `BenchmarkFormScreen` immediately on the next frame, causing it to unmount and leaving 0 widgets in the tree.

### 2. Implemented Fix
- `lib/core/presentation/widgets/app_interaction_primitives.dart`:
  - Guarded `didPushNext()` with `if (widget.isDirty)`, matching the documented contract ("If the sheet is dirty, request dismissal through the shared guard"). Clean sheets remain mounted in the background without popping the pushed route.
  - In `_requestDismiss()`, deferred `AppDirtyDismissDialog.show(context)` to the next event loop turn with `await Future<void>.delayed(Duration.zero)`. When dismiss is triggered via `onPopInvokedWithResult` (e.g. system back or `GoRouter.pop()`), the Flutter `Navigator` is synchronously locked (`_debugLocked == true`). Deferring allows the navigator lock to release before pushing the discard confirmation dialog, preventing `Failed assertion: line 5113 pos 12: '!_debugLocked': is not true.` crashes.
  - In `_dismiss()`, added `WidgetsBinding.instance.scheduleFrame()` before registering `WidgetsBinding.instance.addPostFrameCallback(...)`. Non-visual gestures like tapping the modal barrier do not schedule frames via `setState()` or active animations; explicit frame scheduling ensures the post-frame dismissal callback is guaranteed to execute across both runtime and headless test environments.
- `test/app/router_test.dart`:
  - Added `observers: [routeObserver]` to `_buildTestRouter` to mirror the production router configuration.
  - Added test case `push transition from benchmark inspector to edit form mounts edit view`.
- `test/features/benchmark/presentation/benchmark_navigation_test.dart`: Added dedicated test suite verifying:
  - Direct route resolution to `BenchmarkFormScreen`.
  - Push transition from `BenchmarkInspectorScreen` via `Key('benchmark_edit_button')`.
  - Full journey flow from `BenchmarkListScreen` card tap to inspector and push to `BenchmarkFormScreen`.
  - Pop transition and discard confirmation: approving discard returns to `BenchmarkInspectorScreen` and reloads record data via `LoadBenchmarkById`.
  - Discard cancellation: tapping "Continue editing" preserves dirty `BenchmarkFormScreen` in the widget tree.
  - Submitting `BenchmarkFormScreen` saves changes and returns cleanly to `BenchmarkInspectorScreen`.
  - Android/system back button handling on dirty form without navigator lock assertion.
  - Imperative `GoRouter.pop()` handling on dirty form without navigator lock assertion.
  - Header close button ('X') on dirty `BenchmarkFormScreen` triggers discard dialog and discard approval returns to inspector.
  - Header close button ('X') on clean `BenchmarkInspectorScreen` dismisses sheet and returns to `BenchmarkListScreen`.
  - Modal barrier tap on clean `BenchmarkInspectorScreen` dismisses sheet and returns to `BenchmarkListScreen`.

### 3. Verification Commands and Pass Counts
```
$ dart format --output=none --set-exit-if-changed lib/core/presentation/widgets/app_interaction_primitives.dart test/app/router_test.dart test/features/benchmark/presentation/benchmark_navigation_test.dart
Formatted 3 files (0 changed) in 0.04 seconds.
EXIT: 0

$ flutter analyze
Analyzing mine-flow-app...
No issues found! (ran in 4.1s)
EXIT: 0

$ flutter test test/app/router_test.dart test/features/benchmark/
00:08 +90: All tests passed!
EXIT: 0 — 90 tests (48 benchmark + 42 router), all passed

$ flutter test test/features/benchmark/core/utils/crs_utils_test.dart test/features/benchmark/presentation/benchmark_bloc_test.dart
00:00 +35: All tests passed!
EXIT: 0 — 35 tests, all passed

$ dart run tool/check_l10n_baseline.dart
Files scanned (non-exempt): 21
Files exempt (legacy):      47
[OK] No new hardcoded strings detected in non-exempt files.
EXIT: 0

$ dart run tool/check_supabase_contracts.dart
[OK] Contract verification passed.
EXIT: 0
```

### 4. Gates Status
| Gate | Result |
|------|--------|
| `dart run tool/check_l10n_baseline.dart` | ✅ EXIT 0 |
| `flutter analyze` | ✅ 0 issues |
| `dart format --set-exit-if-changed <touched>` | ✅ 0 changes |
| `flutter test test/app/router_test.dart test/features/benchmark/` | ✅ 90/90 passed |
| `dart run tool/check_supabase_contracts.dart` | ✅ EXIT 0 |


