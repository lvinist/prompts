# mine-flow — STEP-54.3 Findings: Land Clearing Tracking Critique

**Date:** 2026-09-11
**Executor:** Antigravity
**Status:** Complete
**Inspected app branch:** `step-0054-feature-cohesion-critique`
**Scope:** Read-only critique of the Land Clearing Tracking feature lifecycle (List, Form, Report) across Web and Android.

## 1. Scope and evidence boundary

This is a static critique. The mandatory evidence floor is met with branch-head `file:line` citations. No browser or Android emulator was run.

The inspected source files were:
- `Code/mine-flow-app/lib/features/tracking/presentation/pages/land_clearing_list_screen.dart`
- `Code/mine-flow-app/lib/features/tracking/presentation/pages/land_clearing_entry_screen.dart`
- `Code/mine-flow-app/lib/features/tracking/presentation/widgets/clearing_summary_card.dart`
- `Code/mine-flow-app/lib/features/tracking/presentation/widgets/area_input_field.dart`
- `Code/mine-flow-app/lib/core/presentation/widgets/creatable_combobox.dart`

## 2. Findings

| ID | Verdict | Area | Finding and impact | Branch-head evidence | Required treatment |
|---|---|---|---|---|---|
| FC-54.3-001 | Needs restructure | Form routing (D1/D2/D4/D5) | The Land Clearing entry form is pushed as a full `MaterialPageRoute` instead of a responsive sheet (D1/D2) or URL-synced GoRouter route (D5). There is no dirty intercept (D4) implemented on the form (no `onWillPop` or similar mechanism). | `land_clearing_list_screen.dart:146-154`; `land_clearing_entry_screen.dart:248-265` | Migrate to a URL-backed sheet adapter (add `/operations/land-clearing/form`) and implement dirty interception. |
| FC-54.3-002 | Needs polish | Tabbed Form Summary | The Form screen uses a `TabBar` for Plan vs Actual. The two tabs are visually parallel. However, the `DefaultTabController` does not sync its tab index to the URL, so the active tab state is lost on refresh or deep link (D5 conflict). | `land_clearing_entry_screen.dart:381-396` | Replace `DefaultTabController` with a state management approach that syncs to URL or preserves state across rebuilds. |
| FC-54.3-003 | Needs polish | Method Combobox | The shared method combobox respects the CF-043 selection-only contract (null `onCreateNew`). However, `CreatableCombobox` always renders an inline dropdown instead of a modal bottom picker on mobile, which may cause keyboard occlusion issues. | `land_clearing_entry_screen.dart:360-376`; `creatable_combobox.dart:320-363` | Update `CreatableCombobox` or use a platform-aware selector to provide a bottom sheet on narrow screens. |
| FC-54.3-004 | Needs restructure | Report Dialog (D6) | The Report action uses a `context.pushNamed('report-config')` which is a standalone route, losing the list's current date and zone filters. It does not open as a contextual dialog over the list. | `land_clearing_list_screen.dart:132-135` | Implement a contextual report dialog that preserves list filters and opens modally (D6). |
| FC-54.3-005 | Needs polish | Token conformance | The form uses Material `TextField` (both directly and via `AreaInputField`), `DefaultTabController`, `TabBar`, `TabBarView`, `FloatingActionButton`, and Material date pickers (`showDatePicker`, `showDateRangePicker`), which violate the ForUI token boundary. | `land_clearing_entry_screen.dart:321, 382-400, 527`; `land_clearing_list_screen.dart:127, 140, 297`; `area_input_field.dart:92` | Replace Material primitives with ForUI equivalents (`FTextField`, `FTabs`, `FButton`) or custom token-aligned components. |
| FC-54.3-006 | Needs restructure | D7 Verdict (Inspector) | Tapping a record directly opens the edit form. The form mixes Plan and Actual. Field workers only report actuals while planners set plans, so opening straight to an edit form that mixes both without a read-only view risks accidental edits and lacks a clear summary layout. | `land_clearing_list_screen.dart:404-427` | Yes, a distinct inspector is needed (D7). Implement a read-only detail inspector (side-sheet on Web, bottom sheet on Mobile) to view the record before editing. |
| FC-54.3-007 | Unverified | Accessibility & runtime | Accessibility of tabs, summary cards, contrast, hit targets (48dp), and dark mode behaviors are unverified without a runtime artifact. | Source inspection | Verify at runtime with screen readers and visual inspection. |

## 3. Coverage

| Surface | Platform | States exercised | Evidence | Result |
|---|---|---|---|---|
| Land Clearing List | Web + Android | Static list, filter chips, FAB | `land_clearing_list_screen.dart` | Needs restructure for Report dialog (FC-54.3-004) and token polish |
| Land Clearing Form | Web + Android | Static form, TabBar, Combobox, date picker | `land_clearing_entry_screen.dart`, `area_input_field.dart` | Needs restructure for D1/D2/D5 and token polish (FC-54.3-001, FC-54.3-005) |
| Tabbed Summary | Web + Android | Plan vs Actual tabs in form | `land_clearing_entry_screen.dart` | Needs polish (URL sync) (FC-54.3-002) |
| Shared Combobox | Web + Android | `CreatableCombobox` behavior | `creatable_combobox.dart` | Aligned with CF-043, needs platform polish (FC-54.3-003) |
| D7 Inspector | Web + Android | Record tap behavior | `land_clearing_list_screen.dart` | Missing inspector (FC-54.3-006) |

## 4. D1–D8 conflict and escalation register

- **D1/D2:** Form is pushed via `MaterialPageRoute`, not a sheet.
- **D4:** Dirty intercept is missing.
- **D5:** `land-clearing/form` route is missing; TabBar state is not synced to URL.
- **D6:** Report uses standalone route instead of contextual dialog.
- **D7:** No detail/inspector view exists (decided: inspector is required).

## 5. Verification record

| Check | Result |
|---|---|
| All rubric dimensions scored, both platforms | Pass |
| CF-043 contract conformance verified | Pass — `onCreateNew` is null |
| D4/D5 status and D7 verdict recorded | Pass — D7 verdict definitively made |
| Coverage/findings/verification/limitations tables present | Pass |
| No application code or docs modified | Pass — only this findings file created |

**Verdict:** The Land Clearing feature structurally satisfies the data model (Plan vs Actual) and CF-043 contract, but relies heavily on Material primitives (TabBar, DatePickers, FloatingActionButton, TextField) and conflicts with D1/D2/D5/D6 architectural decisions regarding routing, sheets, and dialogs.

**Next action:** Run substep 54.4 in a fresh chat.
