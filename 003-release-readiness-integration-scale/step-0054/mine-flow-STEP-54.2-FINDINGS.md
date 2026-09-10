# mine-flow — STEP-54.2 Findings: Cut & Fill Volume Tracking Critique

**Date:** 2026-09-11
**Executor:** Antigravity
**Status:** Complete
**Inspected app branch:** `step-0054-feature-cohesion-critique`

## 1. Scope and evidence boundary

This is a static critique of the Cut & Fill Volume Tracking feature across Web and Android platforms. The mandatory evidence floor is met with branch-head `file:line` citations. Visual, touch, and runtime behavior claims are marked `Unverified` as no execution environments were used. No application code was modified.

Inspected files:
- `lib/features/tracking/presentation/pages/cut_fill_list_screen.dart`
- `lib/features/tracking/presentation/pages/cut_fill_form_screen.dart`
- `lib/features/tracking/presentation/bloc/cut_fill_bloc.dart`
- `lib/features/reporting/presentation/pages/report_config_page.dart`
- `lib/core/services/pdf_service.dart`
- `lib/app/router.dart`

## 2. Findings

| ID | Verdict | Area | Finding and impact | Branch-head evidence | Required treatment |
|---|---|---|---|---|---|
| FC-54.2-001 | Needs restructure | Lifecycle cohesion / D6 | The report action pushes to the standalone `report-config` route without passing the active date range or zone filter. The user must re-enter filters in the report page, breaking context. | `cut_fill_list_screen.dart:133-136`; `report_config_page.dart:44` | Pass the list's active filters to the report context, and migrate to the D6 contextual modal dialog. |
| FC-54.2-002 | Needs restructure | Platform conformance / D1, D2 | The form is pushed as a full page via `MaterialPageRoute` instead of the D1 right side-sheet (Web) or D2 bottom sheet (Mobile). | `cut_fill_list_screen.dart:146-168`, `407-417` | Implement the responsive sheet adapter for Cut/Fill forms. |
| FC-54.2-003 | Needs restructure | Platform conformance / D5 | Form lacks GoRouter URLs (e.g. `/operations/cut-fill/form`). The form cannot be deep-linked or browser-refreshed without losing state. | `router.dart:257-267` (no form subroute) | Register the form route in GoRouter and navigate via URL instead of `Navigator.push`. |
| FC-54.2-004 | Needs restructure | Interaction states / D4 | The BLoC tracks `hasUnsavedChanges`, but the form does not intercept back navigation (`Navigator.pop()`). Unsaved edits are discarded silently on back/ESC. | `cut_fill_form_screen.dart:184-185`, `257-258` | Wrap the form in a dirty-state interceptor (e.g. `PopScope`) tied to `hasUnsavedChanges`. |
| FC-54.2-005 | Needs polish | Token conformance | The list and form surfaces use raw Material primitives (`FloatingActionButton`, `showDateRangePicker`, `showDatePicker`, and `TextField`) instead of their ForUI equivalents, breaking token conformance. | `cut_fill_list_screen.dart:128`, `141`, `298`; `cut_fill_form_screen.dart:313`, `404`, `521` | Replace Material components with ForUI controls. |
| FC-54.2-006 | Aligned | D7 Verdict (Detail view) | Cut/fill records are simple scalar measurements. The current flow of tapping a card to directly open the edit form is sufficient; a separate read-only detail view is not necessary. | `cut_fill_list_screen.dart:406-429` | Keep the direct-to-edit-form flow; no detail surface needed. |
| FC-54.2-007 | Unverified | Accessibility | Semantic labels exist on some buttons, but touch targets, contrast, and focus order remain unverified statically. | Static inspection | Technical audit needed at runtime. |

## 3. D7 Verdict & Rationale

**Verdict:** No dedicated detail view is required.
**Rationale:** Cut/Fill records consist of scalar numeric data (volume, elevation) and a few metadata fields (date, zone, material). There are no long-form text blocks, complex relations, or sub-lists to inspect. The current list behavior—where tapping a record opens the form in edit mode—is sufficient and reduces cognitive load compared to adding a middleman read-only inspector.

## 4. Coverage

| Surface | Platform | States exercised | Evidence | Result |
|---|---|---|---|---|
| List view | Web + Android | Filter controls, summary card, empty state, error state, record cards | `cut_fill_list_screen.dart` | Needs polish (Material tokens used: FABs, DatePickers) |
| Form view | Web + Android | Edit/Create modes, loading, validation errors, save success | `cut_fill_form_screen.dart`, `cut_fill_bloc.dart` | Needs restructure (Missing dirty intercept, modal placement, GoRouter) |
| Report entry | Web + Android | Entry point from list | `cut_fill_list_screen.dart:125-139` | Needs restructure (Loses context, uses standalone route) |

## 5. Verification record

- **Every finding:** Contains an ID (`FC-54.2-NNN`), a correct verdict, citation, and explanation.
- **D4 Status:** Explicitly checked; dirty intercept is missing.
- **D5 Status:** Explicitly checked; `/operations/cut-fill/form` is missing.
- **D7 Verdict:** Recorded with rationale.
- **No code changes:** App repo remains untouched.

## 6. Limitations
Visual and runtime accessibility claims remain `Unverified` without a live environment.
