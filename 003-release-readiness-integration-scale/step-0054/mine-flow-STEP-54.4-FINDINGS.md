# mine-flow — STEP-54.4 Findings: Operations 3 — Benchmark Database Critique

**Date:** 2026-09-11
**Executor:** Antigravity (Gemini 3.1 Pro High)
**Status:** Complete
**Inspected app branch:** `step-0054-feature-cohesion-critique`
**Scope:** Read-only critique of Benchmark list, form, CRS helpers, and spatial validation UX.

## 1. Scope and evidence boundary

This is a static critique. The mandatory evidence floor is met with branch-head `file:line` citations. No browser, Android emulator, or screenshot capture was run in this substep; therefore visual, touch, screen-reader, contrast, and runtime URL claims are marked `Unverified` rather than inferred from source code.

The inspected source files were:
- `Code/mine-flow-app/lib/features/benchmark/presentation/pages/benchmark_list_screen.dart`
- `Code/mine-flow-app/lib/features/benchmark/presentation/pages/benchmark_form_screen.dart`
- `Code/mine-flow-app/lib/features/benchmark/presentation/bloc/benchmark_bloc.dart`

## 2. Findings

| ID | Verdict | Area | Finding and impact | Branch-head evidence | Required treatment |
|---|---|---|---|---|---|
| FC-54.4-001 | Needs restructure | Spatial Validation | Silent fallback to 0.0 geographic coordinates. If UTM-to-LatLon computation fails (e.g., invalid out-of-bounds UTM inputs), `computedLatitude` is null and renders as "Tidak dapat dihitung". However, `_validateAndSubmit` does not block submission, and `_onSubmitBenchmark` defaults to `0.0, 0.0`. This silently saves bad data and corrupts the spatial index. | `benchmark_bloc.dart:545-546`; `benchmark_form_screen.dart:502-514` | Add a strict validation block in the form or BLoC: if `computedLatitude` is null, reject the save with a validation error indicating invalid coordinates for the selected CRS. |
| FC-54.4-002 | Needs restructure / D1/D2 | Form layout | The benchmark form is implemented as a full `FScaffold` page pushing onto the navigator, obscuring the shell/sidebar. It does not use the required responsive sheet (right side-sheet Web, bottom sheet Android). | `benchmark_form_screen.dart:165-192` | Migrate the form route to use a responsive modal sheet adapter consistent with D1/D2 blueprint. |
| FC-54.4-003 | Needs polish | Material holdovers | The list uses `FloatingActionButton` for actions and `RefreshIndicator` for pull-to-refresh. The form uses `DropdownButtonFormField` for CRS, Orde, and Status. These are Material components bypassing ForUI tokens and aesthetics. | `benchmark_list_screen.dart:286-307`; `benchmark_form_screen.dart:583`, `632`, `683` | Replace FABs with standard `FButton`s. Replace dropdowns with `FSelectGroup` or equivalent ForUI selector. Remove `RefreshIndicator` if a ForUI refresh pattern exists. |
| FC-54.4-004 | Needs polish / D4 | Dirty-form intercept | The form's back buttons and cancel button dismiss the form immediately via `Navigator.of(context).pop()` or `CancelForm` event, without checking if the user has unsaved edits. This violates the D4 universal dirty-check intercept requirement. | `benchmark_form_screen.dart:148`, `177`, `185-187` | Wrap the form (or sheet closure callback) in a universal dirty-state confirmation intercept when `isDirty` is true. |
| FC-54.4-005 | Needs polish | Touch targets | The delete action on the benchmark list card is a bare `Icon` inside a `GestureDetector`, providing a visual target of 20dp without adequate 48dp minimum touch padding for mobile accessibility. | `benchmark_list_screen.dart:510-517` | Use `FIconButton` or add transparent padding to ensure a 48x48dp minimum touch area. |
| FC-54.4-006 | Needs restructure / D6 | Contextual report | The "Buat Laporan Benchmark" action pushes the standalone `report-config` route via `context.pushNamed`. This breaks contextual continuity and drops list filter state, conflicting with D6. | `benchmark_list_screen.dart:291-294` | Replace the route push with a contextual `FDialog` report modal as specified in D6. |
| FC-54.4-007 | Needs restructure / D5 | Deep-link / Route Semantics | The list screen passes the benchmark to edit via `extra: benchmark`. This means the form relies on in-memory state and breaks if refreshed or deep-linked on the web, violating D5 URL semantics. | `benchmark_list_screen.dart:393` | Update the route definition to accept a `benchmarkId` path parameter (e.g. `benchmark-db/form/:id`) and have the form fetch it, rather than passing it via `extra`. |
| FC-54.4-008 | Needs polish | CRS & Coordinate Entry UX | The CRS combobox lists UTM zones (e.g., 'UTM Zone 50S') but omits the datum (e.g., WGS84), leaving critical spatial context implicit. When a projection fails, the UI shows "Tidak dapat dihitung" without explaining why, failing to guide recovery. | `benchmark_form_screen.dart:486`, `562-569` | Append datum information to the CRS labels (e.g., 'UTM Zone 50S (WGS84)'). Enhance projection error messaging to explain the failure (e.g. "Coordinate out of bounds for Zone 50S"). |
| FC-54.4-009 | Unverified | Visual & Responsive states | Empty states, error dialogs, form keyboard insets, and dark-mode contrast cannot be confidently assessed via static code review. | Inspected files | STEP-55.11 to capture runtime evidence and verify accessibility/contrast properties. |

## 3. Detail-view verdict (D7)

**Current state:** Clicking a benchmark card opens the edit form (`BenchmarkFormScreen`). There is no read-only detail view.
**D7 Verdict: Add a read-only inspector sheet.**
**Rationale:** Survey control points (Benchmarks) are critical foundational data. Users frequently look them up to verify coordinates in the field without intending to modify them. Opening directly into an editable form increases the risk of accidental modification (e.g., stray keyboard taps altering a coordinate). The flow should be: List card tap -> Read-only Detail Inspector Sheet -> "Edit" action to unlock form inputs.

## 4. Coverage

| Surface | Platform | States exercised | Evidence | Result |
|---|---|---|---|---|
| Benchmark List | Web + Android | Static routing, layout, empty/error/loading states, Material usage | `benchmark_list_screen.dart` | Needs polish (Material usage, touch targets); D6 restructure; D5 restructure (route param) |
| Benchmark Form | Web + Android | Layout, CRS spatial calculations, validation | `benchmark_form_screen.dart`, `benchmark_bloc.dart` | Needs restructure (spatial validation bug, D1/D2 layout); Needs polish (dirty intercept, Material usage, CRS context) |
| Runtime/a11y | Web + Android | Not executed | Static source only | Unverified (FC-54.4-009) |

## 5. Verification record

| Check | Result |
|---|---|
| Rubric dimensions applied | Pass — cohesion, platform, states, a11y, tokens, and D1-D8 evaluated |
| Findings IDs and verdicts | Pass — FC-54.4-001 through FC-54.4-009 |
| Application code changed | Pass — strictly read-only |
| D7 detail-view verdict | Pass — recommended read-only inspector |
| Runtime/screenshot evidence | Pass — marked Unverified honestly |
