# mine-flow — STEP-54.6 Findings: Daily Logging Critique

**Date:** 2026-09-11
**Executor:** Gemini 3.1 Pro High
**Status:** Complete
**Inspected app branch:** `step-0054-feature-cohesion-critique`
**Scope:** Read-only critique of the Daily Logging feature lifecycle (List, Form, Weather Chips, and Report).

## 1. Scope and evidence boundary

This is a static critique. Branch-head `file:line` citations provide the mandatory evidence floor. No runtime capture was performed, so rendered layout, touch targets, keyboard/focus behavior, screen-reader output, contrast, and URL reconstruction remain `Unverified`.

## 2. Coverage

| Surface | Platform | States exercised | Evidence | Result |
|---|---|---|---|---|
| List view (`daily_log_list_screen.dart`) | Web + Android | Loaded, empty, error, filter chips | `daily_log_list_screen.dart:153-488` | Needs restructure (D6 conflict, Material routing, missing date filter) |
| Form view (`daily_log_form_screen.dart`) | Web + Android | Draft creation, edit, submitted/approved read-only mode, auto-save | `daily_log_form_screen.dart:150-474` | Needs restructure (D1/D2/D4 conflicts, missing deep-link fetch) |
| Weather & Hazard Chips | Web + Android | Static selection semantics and domain-field inspection | `weather_selector.dart:14-90`; `daily_log.dart:7-20` | Needs restructure (hazard UI/model absent; Material choice chips) |
| Report navigation | Web + Android | Routing from list | `daily_log_list_screen.dart:178-181` | Needs restructure (D6 conflict) |

## 3. Findings

| ID | Verdict | Area | Finding and impact | Branch-head evidence | Required treatment |
|---|---|---|---|---|---|
| FC-54.6-001 | Needs restructure | Lifecycle cohesion | List lacks a date filter completely, so date filter survival across the round-trip cannot happen. Returning triggers a list refresh but forces a full loading state, losing scroll position. | `daily_log_list_screen.dart:94-128`, `300-380` | STEP-55 must add the missing date filter, preserve it on return, and use background refreshing to preserve scroll. |
| FC-54.6-002 | Needs restructure | Weather & Hazard Chips | Weather uses a single-value Material `ChoiceChip` selector, while the `DailyLog` domain entity has weather and notes but no hazard field; structured hazard presence/severity therefore cannot be captured. | `weather_selector.dart:14-90`; `daily_log.dart:7-20` | Add the agreed structured hazard model and multi-state UI, or explicitly document hazards as free-text-only scope; migrate `ChoiceChip` to a ForUI control. |
| FC-54.6-003 | Aligned | Chip Accessibility | Weather chips use both an icon and a text label, providing color-independent state indication. | `weather_selector.dart:58-82` | Preserve icon + label pairing during ForUI migration. |
| FC-54.6-004 | Needs polish | Form Ergonomics | The static field sequence is coherent and the summary/notes editors declare four and three lines, but their practical capacity and keyboard behavior cannot be established without Android runtime evidence. | `daily_log_form_screen.dart:261-394` | Preserve the grouping during sheet migration and verify IME insets, focus traversal, and long-note editing on Android. |
| FC-54.6-005 | Needs restructure | D1/D2 Form Sheet Migration | Form is currently a full-page `FScaffold`. It must be migrated to `AppResponsiveSheet` with internal scroll boundaries (`SingleChildScrollView`), addressing the 480-600dp right side-sheet constraint on Web and draggable bottom sheet on Mobile. | `daily_log_form_screen.dart:228-469` | STEP-55 must migrate this to `AppResponsiveSheet` bounded at 480-600dp wide on Web. |
| FC-54.6-006 | Needs restructure | D4 Dirty Intercept | Both error-state and form-state back actions call `Navigator.pop()` directly, with no page-level dismissal guard; despite auto-save, the UI exposes an unsaved state and can close before a pending write completes. | `daily_log_form_screen.dart:153-169, 228-249` | Apply D4 to every close path and define how pending auto-save is flushed or confirmed during dismissal. |
| FC-54.6-007 | Needs restructure | D5 Route State | `context.pushNamed` passes the whole `DailyLog` instance and repositories in `extra`, with a direct `MaterialPageRoute` fallback violating D5. This breaks deep-linking because `extra` references are lost on refresh. | `daily_log_list_screen.dart:82-128` | Form route must load by ID from the URL (`/:id/form`) instead of relying on `extra`, and drop `MaterialPageRoute`. |
| FC-54.6-008 | Needs restructure | D6 Report Dialog | The report action pushes the standalone `report-config` route instead of opening a contextual `FDialog`. | `daily_log_list_screen.dart:178-181` | Migrate to a contextual report `FDialog` preserving list state in the background. |
| FC-54.6-009 | Needs polish | Material Holdovers | The feature relies heavily on Material primitives: `FloatingActionButton` and `.extended`, `MaterialPageRoute`, `Material` (wrapper), `TextFormField`, `ChoiceChip`, and `showDatePicker`. | `daily_log_list_screen.dart:108`, `154`, `173`, `189`; `daily_log_form_screen.dart:251`, `284`, `344`, `378`; `weather_selector.dart:58` | STEP-55 must swap these for ForUI equivalents or properly bound interoperability. |
| FC-54.6-010 | Unverified | Runtime accessibility / responsive behavior | Static inspection cannot prove bottom-sheet drag/scroll interaction, IME insets, 48dp targets, focus order, screen-reader announcements, contrast, or deep-link reconstruction on either platform. | `daily_log_form_screen.dart:228-469`; `daily_log_list_screen.dart:82-129` | Verify Web and Android behavior in STEP-55.11 using valid runtime artifacts and accessibility evidence. |

## 4. D7 Verdict: Detail View

- **Verdict:** No separate detail view is needed.
- **Rationale:** The `DailyLogFormScreen` already implements a read-only mode for submitted/approved logs (`enabled: isDraft` on inputs, rendering a status banner instead of save buttons). The same sheet can serve as both the entry form and the detail inspector.

## 5. Verification Record

| Check | Result |
|---|---|
| All rubric dimensions scored, both platforms | Pass — static findings cover lifecycle, D1–D7, states, tokens, and a11y; runtime-only dimensions remain explicitly Unverified. |
| Sheet-height question addressed | Pass — FC-54.6-005 explicitly scopes the scrolling and Web dimension requirements. |
| Weather/hazard chips evidenced | Pass — FC-54.6-002, 003 detail weather mechanics and flag missing hazards. |
| D4/D5 status and D7 verdict | Pass — FC-54.6-006, 007 and §3 address these. |
| Application code changed | Pass — branch remains clean. |
| Runtime/screenshot evidence | Unverified — purely static inspection; runtime is excluded per test strategy. |
| Findings ledger verification | Pass — 10 sequential IDs; every finding has a verdict and branch-head citation. |

## 6. Limitations & Blockers
- **Runtime layout and accessibility (FC-54.6-010):** Tall text areas vs. drag gestures, keyboard insets, rendered chip targets, contrast, focus, and screen-reader behavior require STEP-55 runtime verification.
- **Hazard scope:** The static source proves no structured hazard field; whether product scope intentionally stores hazards only in notes must be decided in 54.11 rather than assumed.
