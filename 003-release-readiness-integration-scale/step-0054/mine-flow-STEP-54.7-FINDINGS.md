# mine-flow — STEP-54.7 Findings: Equipment Digital Checks Critique

**Date:** 2026-09-11
**Executor:** Gemini 3.1 Pro High
**Status:** Complete
**Inspected app branch:** `step-0054-feature-cohesion-critique`
**Scope:** Read-only critique of Equipment Digital Checks (history list, SOP form sheet, details, report path) on Web and Android.

## 1. Scope and evidence boundary

This is a static code inspection of the `equipment_check` feature. The mandatory evidence floor is met with branch-head `file:line` citations. No runtime capture or temporary widget test was run in this slice; rendered dimensions, contrast, focus, and screen-reader behavior remain `Unverified`.

**Surfaces inspected:**
- `lib/features/equipment_check/presentation/pages/equipment_history_screen.dart`
- `lib/features/equipment_check/presentation/pages/equipment_check_form_screen.dart`
- `lib/features/equipment_check/presentation/widgets/equipment_check_card.dart`
- `lib/features/equipment_check/presentation/widgets/sop_checklist_item_card.dart`
- `lib/features/equipment_check/presentation/bloc/equipment_check_bloc.dart`

## 2. Findings

| ID | Verdict | Area | Finding and impact | Branch-head evidence | Required treatment |
|---|---|---|---|---|---|
| FC-54.7-001 | Needs restructure | Detail View Lifecycle | No dedicated detail view exists; inspection records expand inline using a Material `ExpansionTile` within the list card. With up to 30 items + remarks, this creates massive list clutter and breaks deep-linkability to specific records. | `equipment_check_card.dart:188-293` | Extract into a dedicated Read-Only Detail Inspector (see D7 Verdict). |
| FC-54.7-002 | Needs polish | Status Band Headers | Status badges manually construct a `Container` with transparency alpha and borders rather than using standard ForUI components, missing standard semantic variations. | `equipment_check_card.dart:95-125` | Replace custom container with `FBadge` using standard semantic colors. |
| FC-54.7-003 | Needs restructure | Form Modality & Dirty Intercept (D1/D2/D4/D5) | The form is a full `FScaffold`; its header back action pops directly, and navigation supplies site/foreman only through `extra`, so the long checklist lacks D1/D2 modality, D4 protection, and reconstructable D5 context. | `equipment_check_form_screen.dart:106-124`; `equipment_history_screen.dart:102-109`; `router.dart:430-444` | Migrate to the responsive sheet, guard every dismissal while checklist data is dirty, and encode necessary equipment/site context in the route. |
| FC-54.7-004 | Needs polish | SOP Checklist Ergonomics | PASS/FAIL are custom `InkWell` + `Container` controls with 8dp vertical padding and no minimum constraints, so source does not guarantee the rubric's 48dp touch target; actual rendered size is runtime-unverified. | `sop_checklist_item_card.dart:94-147` | Replace with standard ForUI selection controls or enforce 48x48dp hit regions, then measure on Android. |
| FC-54.7-005 | Needs restructure | Contextual Report Navigation (D6) | "Buat Laporan Inspeksi Peralatan" is triggered by a Material `FloatingActionButton` that pushes the standalone `report-config` route via `extra`, abandoning current list filters. | `equipment_history_screen.dart:413-426` | Migrate to a D6 contextual `FDialog` preserving list state behind it. Replace Material FABs with ForUI primary actions. |
| FC-54.7-006 | Needs polish | Material Residuals | Heavy reliance on Material widgets: `TextField` in history list, `ExpansionTile`, `FloatingActionButton`, and `InkWell`. | `equipment_history_screen.dart:152`; `equipment_check_card.dart:195` | Strip Material widgets and adopt strict ForUI equivalents (`FTextField`, `FButton`, etc.). |
| FC-54.7-007 | Unverified | Accessibility & Contrast | Static source cannot establish whether alpha status treatments and failed text meet WCAG AA, whether checklist controls render at 48dp, or whether focus/screen-reader traversal remains usable through a long checklist. | `equipment_check_card.dart:95-124`; `sop_checklist_item_card.dart:61-147` | Check contrast, rendered hit regions, focus order, and semantics in the STEP-55.11 technical audit. |

## 3. D7 Verdict (First-class deliverable)

**Feature:** Equipment Digital Checks — Inspection Details
**Current state:** Material `ExpansionTile` inline within the `EquipmentCheckCard` on the history list.

**Verdict: Restructure to a route-backed read-only inspector — right side-sheet on Web; full page on Mobile.**

**Rationale:**
1. **Data Density:** A complete inspection contains 15-30 checklist items, defect notes, equipment metadata (S/N, Type), inspector UUID, and timestamps. Expanding this inline causes massive vertical reflow and makes the parent list unusable.
2. **Deep-linking:** Inline expansion cannot be deep-linked. Inspection records are often shared in incident reports (e.g. "drone failed check X"). A dedicated route (e.g., `/teams/equipment-check/:id`) is mandatory.
3. **Ergonomics:** Detail views are consulted when auditing a failure, not casually scanned. A read-only side-sheet on Web keeps list context visible; a route-backed full page on Mobile gives 15–30 results and defect notes stable reading space without competing with bottom-sheet drag gestures.

## 4. Coverage

| Surface | Platform | States exercised | Evidence | Result |
|---|---|---|---|---|
| Equipment History List | Web + Android | Static file inspection of search, filter chips, list, and FAB report paths | `equipment_history_screen.dart` | Needs restructure (FC-54.7-005) & polish |
| Detail View | Web + Android | Static file inspection of `EquipmentCheckCard` expansion logic | `equipment_check_card.dart` | Needs restructure (FC-54.7-001) |
| SOP Checklist Form | Web + Android | Static file inspection of list traversal, submit gates, and PASS/FAIL item cards | `equipment_check_form_screen.dart`, `sop_checklist_item_card.dart` | Needs restructure (FC-54.7-003) & polish |

## 5. Verification record

- **Lifecycle cohesion:** Traced. List → Form (via `context.pushNamed`), Detail is currently inline, Report is standalone route via FAB.
- **Status band headers:** Checked `EquipmentCheckCard`. Uses custom containers instead of tokens/badges.
- **SOP checklist ergonomics:** Checked `SopChecklistItemCard`. Source does not guarantee 48dp hit targets; rendered size remains Unverified, and D4 is absent.
- **D7 verdict:** Provided with full rationale.
- **Form → sheet migration spec:** Identified D1/D2/D4/D5 gaps for the form.
- **Interaction states, a11y, tokens:** Checked. Material residuals identified. Runtime a11y Unverified.
- **Report path:** Verified present (via FAB), recorded as D6 conflict.
- **Findings ledger:** Pass — 7 sequential IDs; every finding has a verdict and branch-head citation.
- **Code modification:** No application code was modified. App repo is clean.

## 6. Limitations
- `Unverified`: Visual contrast, rendered touch targets, focus order, and screen-reader semantics require the STEP-55.11 runtime technical audit; no runtime artifact or widget-test output is claimed by this ledger.
