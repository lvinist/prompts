# STEP-30 PLAN: Phase 2 Tier 2 - ForUI Migration

**Status:** Planned
**Branch:** `step-0030-forui-migration`

## Objective

Migrate all 15 Phase 1 Tier 1 screens from hand-rolled Material `ThemeData` to the `forui` package (using `FTheme` and `FThemes.zinc` with no brand color overrides), per `architecture/07-ui-design-system.md` v0.2.0.
This acts as Tier 2 Step 0, laying the foundation for all subsequent Phase 2 QoL and feature work.

## Hard Constraints

- Add `forui` to `pubspec.yaml` (Dart >=3.12.2 environment is compatible).
- The root must be `FTheme(data: FThemes.zinc.light/dark)`, wrapping the `MaterialApp` (which is retained only for routing/localization).
- Every visible surface must use ForUI widgets (e.g., `FButton`, `FCard`, `FTextField`, `FTabs`, `FScaffold`, `FSidebar`, `FBadge`).
- **No raw Material theming:** No custom `ColorScheme`, `Colors.*`, or hardcoded `TextStyle` anywhere in scope.
- **Bugfixes Included:** This STEP folds in and resolves the outstanding styling/spacing/color violations identified in `mine-flow-STEP-28.1-AUDIT.md` (e.g., hardcoded `Colors.red`, `TextStyle`, non-standard padding).
- **No logic changes:** Do not alter BLoC state, data fetching, or business logic.

## Interface Contract (for STEP-31)

- Substep 30.1 will define a shared `AppNavigationShell` widget that accepts a structured list of `AppNavGroup` and `AppNavItem` objects. Under the hood, it renders `FSidebar` on desktop and a bottom nav on mobile. STEP-31 will rely entirely on updating this data structure to achieve the Navigation Regrouping.

## Substeps

- [ ] **30.1** Core Shell & Auth (Pubspec, `FTheme` root, `AppNavigationShell`, `LoginPage`, `DashboardPage`)
- [ ] **30.2** Operations & Tracking (`CutFillListScreen`, `LandClearingSummaryScreen`, `InventoryDashboardScreen`)
- [ ] **30.3** Teams & Field Docs (`AttendanceScreen`, `DailyLogListScreen`, `EquipmentHistoryScreen`)
- [ ] **30.4** Reports, Data Bucket & Notifications (`TimelinePage`, `ReportDashboardPage`, `ReportConfigPage`, `DataBucketListPage`, `UploadFilePage`, `FileDetailPage`, `NotificationListPage`)
- [ ] **30.5** Analyzer Clean-up
- [x] **30.6** Final Cross-Screen Material Purge & CI Gate

## Test Strategy

- **Tier:** Integration & Widget Testing.
- **Action:** Ensure existing widget and integration tests pass with the new ForUI widget tree. Update test finders where ForUI widgets replace Material widgets (e.g., `find.byType(FButton)` instead of `find.byType(ElevatedButton)`).
- **CI Gate:** The final verification in 30.6 must run and pass `flutter test`. Golden tests (pixel-perfect snapshot testing) are explicitly skipped per the "Less focus on UI layout code" strategy in `architecture/12-test-strategy.md`.
