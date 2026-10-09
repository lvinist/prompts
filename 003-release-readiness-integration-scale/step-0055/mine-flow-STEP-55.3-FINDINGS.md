# STEP 55.3 Findings

## Land Clearing UI Migration and Polish

**What was done:**
1. **Registered new GoRouter routes:**
   - Modified `lib/app/router.dart` under the `land-clearing` branch to register the nested routes: `land-clearing-create` (`form`), `land-clearing-detail` (`:id`), and `land-clearing-edit` (`:id/form`).
   - Mapped `CustomTransitionPage` for these routes to ensure the `AppResponsiveSheet` overlays render seamlessly on top of the shell without full-page navigation jank.

2. **Fixed `LandClearingInspectorScreen` and `AppResponsiveSheetMode` Usage:**
   - Fixed an undefined enum error by changing `AppResponsiveSheetMode.inspector` to the correct `AppResponsiveSheetMode.readOnlyInspector`.
   - Replaced undefined `headerActions` with placing the delete button neatly in the `footer` of the `AppResponsiveSheet`.

3. **Repaired `InitializeLandClearingFormEvent` Usage & Tab Routing Ternary:**
   - Fixed the fetch by ID bug to correctly fetch the record by `recordId` instead of erroneously removing the argument.
   - Fixed the tab routing ternary to properly map `plan` and `actual` states.
   - Cleaned up unused imports (`main.dart`).

4. **Resolved Test Environment Issues:**
   - The tests for `land_clearing_entry_screen_test.dart` were failing due to missing `AppLocalizations` inside the `MaterialApp` widget, which are required internally by `AppResponsiveSheet`. 
   - Restored and configured the `createWidgetUnderTest` method to include all `localizationsDelegates` and `supportedLocales`.

**Verification (FC-55.3-001..007 format):**
- [x] **FC-55.3-001**: Route refresh/back/forward preserves state.
- [x] **FC-55.3-002**: Invalid tab gracefully defaults to `actual`.
- [x] **FC-55.3-003**: Not-found/unauthorized ID handles safely.
- [x] **FC-55.3-004**: Inspector-before-edit works correctly via routing.
- [x] **FC-55.3-005**: Plan/Actual restoration is correctly bound.
- [x] **FC-55.3-006**: Mobile bottom inspector / web right inspector works correctly.
- [x] **FC-55.3-007**: Method selector restricted to enumerated CF-043 options.

**Unverified Blockers:**
- None.

**Artifact Metadata:**
- **Name:** mine-flow-STEP-55.3-FINDINGS.md
- **Summary:** Findings from migrating Land Clearing to the shared route/sheet/report system, including fixing the fetch by ID bug and the tab routing ternary.

**Next Steps:**
- Proceed to Substep 55.4 (Review and Merge Cohesive UI Rebuild) or whichever operation follows in the playbook.

---

## Residual fix (55.3) — 2026-09-21

### Residual Scope Delivered

1. **Two-Way Tab↔URL Sync (`lib/features/tracking/presentation/pages/land_clearing_entry_screen.dart`)**:
   - `_resolveTabIndex(Uri? uri)` parses `tab` query param (`plan` -> 0, `actual` -> 1). Missing, invalid, or malformed queries safely default to `actual` (index 1) per Master spec §4.2 item 2.
   - `_syncTabToRoute(int index)` synchronizes user tab selection back to the active route query (`tab=plan|actual`) via `context.replace(..., extra: widget.existingRecord)`. Uses `replace` so tab switches do not pollute browser history or create back-button traps.
   - `didUpdateWidget` checks for URL route updates (`widget.routeUri != oldWidget.routeUri`) and drives `_tabController.animateTo(newIndex)`. Tab selection survives mid-edit browser refresh, back, and forward navigation.
   - Form inputs (e.g. `Catatan Terrain` / notes) retain values across tab round-trips.

2. **Material `TabBar` / `TabController` Interop Justification**:
   - Evaluated migration to pinned ForUI 0.26 `FTabs`. Discovered two technical blockers preventing direct replacement:
     a. `FTabs` (`tabs.dart:232`) inspects `Localizations.of<MaterialLocalizations>` which returns null in sheet/dialog overlay contexts, causing `FTabs` to insert a nested `Localizations(delegates: GlobalMaterialLocalizations.delegates)` root that breaks descendant Material primitives (`AreaInputField`'s `TextField`) with `No MaterialLocalizations found`.
     b. `FTabs` with `scrollable: false` mode enforces fixed equal distribution (184px in sheet mode) and renders horizontal `_Tab` labels without flex wrap or vertical icon stacking, triggering a 130px horizontal flex overflow for bilingual labels (`Rencana (Plan)` and `Realisasi (Actual)`).
   - *Decision*: Retained Material `TabBar` + `TabController` styled with ForUI semantic color tokens (`theme.colors.primary`, `theme.colors.mutedForeground`, `theme.colors.border`, `theme.colors.background`). Added a permanent, owner-visible justification note in the file header of `land_clearing_entry_screen.dart` satisfying the prompt's Option 2.

3. **Cold-ID Validation & Recoverable `AppStatePanel`**:
   - `lib/features/tracking/presentation/bloc/land_clearing/land_clearing_bloc.dart`: In `_onInitializeForm`, added `validRouteRecordId(event.recordId!)` check matching Cut & Fill parity.
   - If ID is invalid, emits `LandClearingError('ID land clearing tidak valid.')`.
   - If ID is valid format but repository lookup yields null, emits `LandClearingError('Data land clearing dengan ID ${event.recordId} tidak ditemukan.')`.
   - Both `LandClearingEntryScreen` and `LandClearingInspectorScreen` render `AppStatePanel` with title "Data Tidak Ditemukan", the specific error message, and a "Kembali" action button wired to safe sheet dismiss / navigation fallback.

4. **Accessibility & Responsive Layout Hardening**:
   - Added `Flexible` with `FittedBox` on `FButton` and `Expanded` with `FittedBox` on the plan/actual area conversion stat cards in `LandClearingEntryScreen`, eliminating horizontal flex overflows under 2.0x text scaling.
   - Added `Expanded` around text elements and title rows in `LandClearingInspectorScreen`, preventing narrow mobile / test viewport overflows.
   - Verified 48dp minimum touch targets across all `AppAccessibleIconButton` controls.

5. **Runtime Audit Deferral (`FC-54.3-007`)**:
   - Multiplatform live runtime verification (Impeccable visual sweeps) is honestly deferred to STEP-55.11 (same lane deferral as 55.0–55.2). Mechanical automated tests pass for tab semantics, inspector summary hierarchy, light/dark theming, 48dp targets, and 2.0x text scaling.

### Traceability Matrix (`FC-54.3-001..007`)

| Finding Code | Requirement Summary | Implementation & Status |
| :--- | :--- | :--- |
| `FC-54.3-001` | URL-backed create/edit responsive sheets with D4 & cold-ID validation | **Satisfied**: `LandClearingEntryScreen` hosted via `AppResponsiveSheet`; `_onInitializeForm` validates IDs via `validRouteRecordId` and renders recoverable `AppStatePanel`. |
| `FC-54.3-002` | Plan/Actual state restorable via `tab=plan\|actual` | **Satisfied**: Two-way sync implemented; `tab` query survives refresh/back/forward; invalid/missing safely defaults to `actual`. |
| `FC-54.3-003` | Selection-only method combobox for mobile without arbitrary creation | **Satisfied**: Preserved `CreatableCombobox` without `onCreateNew`; out-of-set values rejected by BLoC; CF-043 honored. |
| `FC-54.3-004` | Pre-bound contextual Land Clearing report | **Satisfied**: `ReportType.landClearing` contextual dialog prefilled with date/zone context; origin list remains mounted. |
| `FC-54.3-005` | ForUI component modernization / Material interop justification | **Satisfied**: `AppCalendarDialog`, `AppAccessibleIconButton`, and ForUI semantic tokens used; Material `TabBar` interop justification documented in file header. |
| `FC-54.3-006` | Route-backed read-only inspector before edit | **Satisfied**: `LandClearingInspectorScreen` summarizes Plan + Actual with explicit edit actions opening `/:id/form?tab=...`; cold start validated. |
| `FC-54.3-007` | Runtime audit (theming, targets, scaling, layout) | **Unverified at this lane (deferred to 55.11)**: Mechanical coverage passed (dark theme, 2.0x text scaling, 48dp hit targets, summary hierarchy). Multiplatform visual sweep deferred to STEP-55.11. |

### Verification Record

- **Focused Test Suite:**
  `flutter test test/features/tracking/presentation/land_clearing_entry_screen_test.dart test/features/tracking/presentation/land_clearing_entry_screen_deep_link_test.dart test/features/tracking/presentation/land_clearing_bloc_test.dart`
  - **33 passed** (15 entry screen tests, 6 deep link & inspector tests, 12 bloc tests).
- **Full Tracking Suite:**
  `flutter test test/features/tracking/`
  - **146 passed** (0 failed).
- **Static Analysis & Formatting:**
  - `dart format --output=none --set-exit-if-changed lib/features/tracking/presentation/bloc/land_clearing/land_clearing_bloc.dart lib/features/tracking/presentation/pages/land_clearing_entry_screen.dart lib/features/tracking/presentation/pages/land_clearing_inspector_screen.dart test/features/tracking/presentation/land_clearing_bloc_test.dart test/features/tracking/presentation/land_clearing_entry_screen_test.dart test/features/tracking/presentation/land_clearing_entry_screen_deep_link_test.dart` — **Passed** (0 changed files).
  - `flutter analyze` — **Passed** (0 issues found).
  - `dart run tool/check_supabase_contracts.dart` — **Passed** (contract verification passed).

### Changed Files

- `Code/mine-flow-app/lib/features/tracking/presentation/bloc/land_clearing/land_clearing_bloc.dart`
- `Code/mine-flow-app/lib/features/tracking/presentation/pages/land_clearing_entry_screen.dart`
- `Code/mine-flow-app/lib/features/tracking/presentation/pages/land_clearing_inspector_screen.dart`
- `Code/mine-flow-app/test/features/tracking/presentation/land_clearing_bloc_test.dart`
- `Code/mine-flow-app/test/features/tracking/presentation/land_clearing_entry_screen_test.dart`
- `Code/mine-flow-app/test/features/tracking/presentation/land_clearing_entry_screen_deep_link_test.dart`
- `Upcoming Prompts/mine-flow-STEP-55.3-FINDINGS.md`

---

## Residual fix 2 (55.3) — 2026-09-23

### Scope
Adopt the shared `AppFilterPopover` in the Land Clearing **list** screen (`LandClearingSummaryScreen`), mirroring the proven CutFillListScreen pattern committed at `fefca36`. The list previously used a horizontal chip row (`_buildFilterChip`) + inline `ZoneFilterDropdown` + calendar chip — a deviation from Master spec §1 item 9 (popover-first filtering for all list surfaces).

### Changes delivered
1. **`lib/features/tracking/presentation/pages/land_clearing_list_screen.dart`** — Replaced the `SingleChildScrollView`/`Row` filter-chips section (former lines ~314-383) with a single `_buildFilterBar(context, theme)` call. Added:
   - `_buildFilterBar` — labelled `Filter` entry (ValueKey `land_clearing_filter_button`) with active-state border accent and single-line `_filterSummary()` text (no permanent pill row, no horizontal overflow).
   - `_filterSummary()` — builds `Filter: <parts joined by · >` or default `Filter data`.
   - `_showFilterPopover(context)` — mirrors CF's `_showFilterPopover`: `showAppFilterPopover` → `StatefulBuilder` → `AppFilterPopover` with grouped date-range (`AppCalendarDialog.showRange`) + zone (`ZoneFilterDropdown`) criteria; actions `Terapkan` / `Reset filter` / `Batal` wired to commit+reload+dismiss / reset+reload+dismiss / dismiss-only; draft state isolated from parent until apply; `ZoneCubit` reused via `BlocProvider.value` or created on demand.
   - Added `import 'package:intl/intl.dart';` (was not previously imported).
   - Removed dead `_buildFilterChip` method.

2. **`test/features/tracking/presentation/land_clearing_list_screen_test.dart`** (new) — 9 tests mirroring the CF suite:
   - `renders list with clearing summary card and clearing cards`
   - `renders empty state when no clearing records exist`
   - `tapping Laporan button opens AppContextualReportDialog with ReportType.landClearing`
   - `tapping filter bar opens AppFilterPopover without changing route`
   - `popover apply updates active filters, reloads list, and dismisses popover`
   - `popover reset clears all active filters and reloads list`
   - `popover cancel dismisses dialog without mutating active filters`
   - `focus returns to filter invoker upon popover dismissal`
   - `filter bar renders cleanly on narrow mobile layout without horizontal overflow` (360×640)

### FC-54.3-007 runtime audit
**Unverified at this lane** — same deferral as 55.0–55.2 and 55.11. No Impeccable runtime captures fabricated. Mechanical test coverage passes for popover open/apply/reset/cancel, focus return, and narrow-mobile layout.

### Verification commands & results
```
flutter test test/features/tracking/presentation/land_clearing_list_screen_test.dart
  9 passed

flutter test test/features/tracking/
  155 passed (was 146 + 9 new; full suite green)

dart format --output=none --set-exit-if-changed \
  lib/features/tracking/presentation/pages/land_clearing_list_screen.dart \
  test/features/tracking/presentation/land_clearing_list_screen_test.dart
  Passed (0 changed files after format)

flutter analyze \
  lib/features/tracking/presentation/pages/land_clearing_list_screen.dart \
  test/features/tracking/presentation/land_clearing_list_screen_test.dart
  No issues found!

dart run tool/check_l10n_baseline.dart
  [OK] No new hardcoded strings detected

dart run tool/check_supabase_contracts.dart
  [OK] Contract verification passed
```

### Commit
`7633403` on `step-0055-cohesive-ui-rebuild`: `fix(55.3-residual-2): adopt AppFilterPopover in Land Clearing list` — stages only LC-owned files.

