# STEP-55.2 Findings — Cut & Fill Migration and Polish

**Date:** 2026-09-11  
**STEP status:** In progress  
**App branch:** `step-0055-cohesive-ui-rebuild`  
**Docs branch:** `step-0055-cohesive-ui-rebuild`  
**Prompts revision:** `main`  

## Delivered

1. **Route-backed Responsive Form Sheet (`AppResponsiveSheet`)**:
   - Migrated Cut & Fill create and edit lifecycle into route-backed responsive sheets.
   - Canonical create route: `/operations/cut-fill/form` (named `cut-fill-create`).
   - Canonical edit route: `/operations/cut-fill/:id/form` (named `cut-fill-edit`).
   - Transparent page transition via `CustomTransitionPage(opaque: false, barrierColor: Color(0x00000000))` keeps the parent list screen mounted, visible, and dimmed beneath the responsive sheet barrier.
   - Enforced D1/D2 responsive geometry: desktop (viewport width >= 800dp) renders right sheet docked at right margin clamped between 480dp and 600dp; mobile (< 800dp) renders bottom sheet.

2. **Cold-Start Edit Support**:
   - `InitializeCutFillFormEvent` now accepts `recordId`.
   - `CutFillBloc` validates `recordId` using `validRouteRecordId` and fetches the record from `TrackingRepository.getCutFillRecordById` when `existingRecord` cache (`extra`) is null.
   - Graceful recovery: if the record is missing or invalid, renders recoverable `AppStatePanel` ("Data Tidak Ditemukan") with "Kembali ke daftar" action button to navigate back safely.

3. **Preserved Direct List → Edit Navigation (D7 Verdict & FC-54.2-006)**:
   - Preserved direct card tap → edit form flow without introducing an intermediate read-only detail inspector.
   - Closing the form sheet restores list context and preserves query filters (`from`, `to`, `zoneId`).

4. **Universal D4 Dirty Guard Integration**:
   - Bound sheet dismissal (scrim tap, ESC/system back, 48dp close icon button) to `AppDismissController` via `state.hasUnsavedChanges` and `state.isSaving`.
   - Modifying inputs (BCM/LCM volumes, elevation change, material, or notes) marks state dirty.
   - Attempting to dismiss while dirty triggers non-dismissible `AppDirtyDismissDialog` ("Perubahan belum disimpan") with explicit "Lanjut Mengedit" and "Buang Perubahan" actions.

5. **Contextual Reporting Integration (`FC-54.2-004`)**:
   - Replaced separate report route push with `showAppContextualReportDialog`.
   - Automatically seeds `ReportType.cutFill`, current active date range (`from` & `to`), and selected `zoneId` from list state into the modal dialog.

6. **Component Modernization & Accessibility**:
   - Replaced floating action buttons (FABs) with ForUI `FButton` actions docked at the list bottom right.
   - Replaced legacy DatePicker with `AppCalendarDialog.showSingle` (form) and `AppCalendarDialog.showRange` (list filter).
   - Replaced legacy text inputs with `FTextField` and `FTextField.multiline` using `FTextFieldControl.managed`.
   - Replaced custom close buttons with `AppAccessibleIconButton` (48dp minimum hit target).
   - Form wrapped with `FormMaxWidth` ensuring readability on wide screens.
   - Preserved bank-equivalent formula calculation: `netVolume = BCM + LCM / (1 + swell)`.

7. **Localization**:
   - Added localized strings in `app_id.arb` and `app_en.arb` for Cut & Fill error, form, and action labels. Committed generated localization artifacts.
   - Zero hardcoded strings in production code; passed `tool/check_l10n_baseline.dart`.

## Traceability Matrix (`FC-54.2-001..007`)

| Finding Code | Requirement Summary | Implementation & Status |
| :--- | :--- | :--- |
| `FC-54.2-001` | Route-backed responsive sheet (`AppResponsiveSheet`) for create & edit | **Satisfied**: `CutFillFormScreen` hosted via `AppResponsiveSheet` with >=800dp right sheet and <800dp bottom sheet. |
| `FC-54.2-002` | Canonical routes: `/operations/cut-fill/form` and `/operations/cut-fill/:id/form` | **Satisfied**: Registered child routes under `cut-fill` in `lib/app/router.dart` and defined in `AppRoutes`. |
| `FC-54.2-003` | Cold-start edit by ID with optional `extra` cache | **Satisfied**: `InitializeCutFillFormEvent(recordId: ...)` fetches from repository when `extra` is absent; handles not-found with `AppStatePanel`. |
| `FC-54.2-004` | Contextual report dialog seeded from active date/zone filters | **Satisfied**: `CutFillListScreen` launches `showAppContextualReportDialog` pre-seeded with `ReportType.cutFill` and active date/zone filters. |
| `FC-54.2-005` | Universal D4 dirty dismiss guard (`hasUnsavedChanges`) | **Satisfied**: Sheet dismiss vectors routed through `AppDismissController`; shows `AppDirtyDismissDialog` when dirty. |
| `FC-54.2-006` | Preserve direct list → edit flow (no separate inspector) | **Satisfied**: D7 decision honored; card tap directly pushes edit sheet without intermediate inspector. |
| `FC-54.2-007` | ForUI modernization; eliminate Material FAB/steppers | **Satisfied**: Actionable Material FABs replaced with `FButton`; numeric steppers eliminated per CF-014; `AppCalendarDialog` used for dates. |

## Verification Record

- **Focused Bloc Tests:**
  `flutter test test/features/tracking/presentation/cut_fill_bloc_test.dart` — **13 passed** (including cold-start fetch, not-found error, and invalid ID).
- **Focused Form Screen Tests:**
  `flutter test test/features/tracking/presentation/cut_fill_form_screen_test.dart` — **12 passed** (renders form, clean dismiss, dirty dismiss dialog with continue/discard, cold edit populate, recoverable error panel, responsive right/bottom sheet geometry, save validation, scrim dismissal, system back dismissal, failed save input retention, routeUri zone pre-selection).
- **Focused List Screen Tests:**
  `flutter test test/features/tracking/presentation/cut_fill_list_screen_test.dart` — **5 passed** (summary & card rendering, empty state, direct edit navigation per D7, filter preservation, contextual report dialog).
- **Router Tests:**
  `flutter test test/app/router_test.dart` — **9 passed** (branch navigation, canonical `AppRoutes` paths, cold create route query extraction, cold edit route ID extraction).
- **Reporting Tests:**
  `flutter test test/features/reporting/` — **12 passed**.
- **Full Tracking Suite:**
  `flutter test test/features/tracking/` — **118 passed**.
- **Static Analysis & Formatting:**
  - `dart format --output=none --set-exit-if-changed .` — **Passed** (0 changed files).
  - `flutter analyze` — **Passed** (0 issues found).
- **Baseline Guards:**
  - `dart run tool/check_l10n_baseline.dart` — **Passed** (16 non-exempt files, 0 errors, no exemptions added).
  - `dart run tool/check_supabase_contracts.dart` — **Passed** (contract verification passed).

## Changed Files

- `Code/mine-flow-app/lib/app/router.dart`
- `Code/mine-flow-app/lib/features/reporting/presentation/widgets/app_contextual_report_dialog.dart`
- `Code/mine-flow-app/lib/features/reporting/presentation/widgets/report_config_content.dart`
- `Code/mine-flow-app/lib/features/tracking/presentation/bloc/cut_fill_bloc.dart`
- `Code/mine-flow-app/lib/features/tracking/presentation/bloc/cut_fill_event.dart`
- `Code/mine-flow-app/lib/features/tracking/presentation/pages/cut_fill_form_screen.dart`
- `Code/mine-flow-app/lib/features/tracking/presentation/pages/cut_fill_list_screen.dart`
- `Code/mine-flow-app/lib/l10n/app_en.arb`
- `Code/mine-flow-app/lib/l10n/app_id.arb`
- `Code/mine-flow-app/lib/l10n/app_localizations.dart`
- `Code/mine-flow-app/lib/l10n/app_localizations_en.dart`
- `Code/mine-flow-app/lib/l10n/app_localizations_id.dart`
- `Code/mine-flow-app/test/app/router_test.dart`
- `Code/mine-flow-app/test/features/reporting/presentation/widgets/app_contextual_report_dialog_test.dart`
- `Code/mine-flow-app/test/features/tracking/presentation/cut_fill_bloc_test.dart`
- `Code/mine-flow-app/test/features/tracking/presentation/cut_fill_form_screen_test.dart`
- `Code/mine-flow-app/test/features/tracking/presentation/cut_fill_list_screen_test.dart`
- `Upcoming Prompts/mine-flow-STEP-55.2-FINDINGS.md`

## Next Handoff

Proceed to **substep 55.3**: Land Clearing Migration and Polish.
Apply responsive sheets (`AppResponsiveSheet`), universal dirty guard (D4), contextual report dialog, and ForUI component modernization across Land Clearing operations.

---

## Residual fix (55.2) — 2026-09-21

### Residual Scope Delivered
1. **Shared `AppFilterPopover` Adoption in Cut & Fill List (`lib/features/tracking/presentation/pages/cut_fill_list_screen.dart`)**:
   - Replaced legacy filter chip row (`_buildFilterChip` + horizontal scrolling chips) with a unified, accessible 48dp minimum-height filter affordance bar.
   - Built popover interaction using `showAppFilterPopover` and `AppFilterPopover` with grouped criteria:
     - Date range selection via `AppCalendarDialog.showRange`.
     - Zone selection via `ZoneFilterDropdown` backed by `ZoneCubit`.
   - Popover actions wired cleanly:
     - `Terapkan` (Apply): commits draft date/zone filters to state, triggers `_reloadList()`, and dismisses popover.
     - `Reset filter`: clears all active date/zone filters, triggers `_reloadList()`, and dismisses popover.
     - `Batal` (Cancel): dismisses popover without applying draft mutations.
   - Active filter summary: single-line summary text (`_filterSummary()`) rendered in the filter affordance (e.g. `'Filter: 1 Mar 2026 - 15 Mar 2026 · Zona: zone-1'`), with zero horizontal scroll overflow.
   - Preserved list BLoC state, scroll position, invoker focus return, query parameters (`from`, `to`, `zoneId`), and contextual reporting integration. No route navigation occurs when opening or closing the filter popover.
2. **Runtime Evidence Deferral Note**:
   - `FC-54.2-007` runtime audit remains **Unverified at this lane** (no Impeccable binary on PATH; consolidated multiplatform runtime evidence is deferred to STEP-55.11 lane per close report). Mechanical widget tests pass for all popover interactions and responsive layouts. No visual captures fabricated.

### Tests & Verification
- `flutter test test/features/tracking/presentation/cut_fill_list_screen_test.dart test/features/tracking/presentation/cut_fill_bloc_test.dart test/features/tracking/presentation/cut_fill_form_screen_test.dart` — **36 passed** (11 list screen, 13 bloc, 12 form screen).
  - New widget tests added for popover open, apply, reset, cancel, focus return, and narrow mobile (360x640) layout without overflow.
- Full tracking suite: `flutter test test/features/tracking/` — **128 passed**.
- `dart format --output=none --set-exit-if-changed lib/features/tracking/presentation/pages/cut_fill_list_screen.dart test/features/tracking/presentation/cut_fill_list_screen_test.dart` — **Passed** (0 changed files).
- `flutter analyze` — **Passed** (0 issues found).
- `dart run tool/check_l10n_baseline.dart` — **Passed** (22 non-exempt files scanned, 0 new hardcoded strings).
- `dart run tool/check_supabase_contracts.dart` — **Passed** (Supabase contracts verified).

### Changed Files
- `Code/mine-flow-app/lib/features/tracking/presentation/pages/cut_fill_list_screen.dart`
- `Code/mine-flow-app/test/features/tracking/presentation/cut_fill_list_screen_test.dart`
- `Upcoming Prompts/mine-flow-STEP-55.2-FINDINGS.md`

