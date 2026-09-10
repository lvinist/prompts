# Step 51.4 Findings: Scaffold → FScaffold Migration

## 1. Executive Summary
Substep 51.4 migrated all 35 residual Material `Scaffold(` call sites across 24 files in `lib/` to ForUI 0.26's `FScaffold`.
The repository now has **0** occurrences of Material `Scaffold` in `lib/`.

## 2. Files and Sites Migrated (24 files, 35 call sites)
1. `lib/app/presentation/pages/app_shell.dart` (1 site) — Shell root scaffold with `childPad: false`, `Material(color: theme.colors.background)`.
2. `lib/app/presentation/pages/dashboard_page.dart` (1 site) — `FScaffold(child: SingleChildScrollView(...))`.
3. `lib/app/presentation/pages/group_landing_page.dart` (1 site) — `FScaffold(child: SingleChildScrollView(...))`.
4. `lib/features/auth/presentation/pages/login_page.dart` (1 site) — `FScaffold(child: Center(...))`.
5. `lib/features/notifications/presentation/pages/notification_list_page.dart` (1 site) — `FScaffold(header: ..., child: ...)`.
6. `lib/features/timeline/presentation/pages/timeline_page.dart` (1 site) — `FScaffold(header: ..., child: ...)`. Migrated legacy `InkWell` to `FTappable(onPress: ...)` to eliminate Material ancestor dependency.
7. `lib/features/data_bucket/presentation/pages/data_bucket_list_page.dart` (1 site) — `FScaffold` with FAB in `Stack`.
8. `lib/features/data_bucket/presentation/pages/file_detail_page.dart` (1 site) — `FScaffold(header: ..., child: ...)`.
9. `lib/features/data_bucket/presentation/pages/file_detail_route.dart` (2 sites) — Route-level container scaffolds migrated to `FScaffold`.
10. `lib/features/data_bucket/presentation/pages/upload_file_page.dart` (2 sites) — Header + Material body in `FScaffold`.
11. `lib/features/attendance/presentation/pages/attendance_form_page.dart` (1 site) — `FScaffold(header: ..., footer: ..., child: Material(...))`.
12. `lib/features/attendance/presentation/pages/attendance_screen.dart` (1 site) — `FScaffold` with FAB in `Stack`.
13. `lib/features/equipment_check/presentation/pages/equipment_check_form_screen.dart` (1 site) — `FScaffold(header: ..., footer: ..., child: Material(...))`.
14. `lib/features/equipment_check/presentation/pages/equipment_history_screen.dart` (1 site) — `FScaffold` with FAB in `Stack`.
15. `lib/features/benchmark/presentation/pages/benchmark_form_screen.dart` (2 sites) — Loading/error + form `FScaffold`.
16. `lib/features/benchmark/presentation/pages/benchmark_list_screen.dart` (1 site) — `FScaffold` with FAB in `Stack`.
17. `lib/features/daily_log/presentation/pages/daily_log_form_screen.dart` (3 sites) — Loading, error, and form `FScaffold`.
18. `lib/features/daily_log/presentation/pages/daily_log_list_screen.dart` (1 site) — `FScaffold` with FAB in `Stack`.
19. `lib/features/tracking/presentation/pages/cut_fill_form_screen.dart` (3 sites) — Loading, error, and form `FScaffold`.
20. `lib/features/tracking/presentation/pages/cut_fill_list_screen.dart` (1 site) — `FScaffold` with FAB in `Stack`.
21. `lib/features/tracking/presentation/pages/inventory_dashboard_screen.dart` (1 site) — `FScaffold` with FAB in `Stack`.
22. `lib/features/tracking/presentation/pages/inventory_item_entry_screen.dart` (3 sites) — Loading, error, and form `FScaffold`.
23. `lib/features/tracking/presentation/pages/land_clearing_entry_screen.dart` (3 sites) — Loading, error, and form `FScaffold`.
24. `lib/features/tracking/presentation/pages/land_clearing_list_screen.dart` (1 site) — `FScaffold` with FAB in `Stack`.

## 3. Architecture & Design Patterns

### Material Ancestor Accommodation
`FScaffold` does not provide an implicit `Material` widget ancestor. Legacy Material controls such as `TextField`, `InkWell`, and `DropdownButtonFormField` crash at runtime (`No Material widget found`) without a Material ancestor.
- **Form and list views**: Wrapped the body in `Material(color: Colors.transparent, child: ...)` to transparently provide the required ancestor without adding unwanted styling or backgrounds.
- **Interactive badges**: In `timeline_page.dart`, converted raw `InkWell` badges to ForUI's native `FTappable(onPress: ...)`.

### Floating Action Button (FAB) Pattern
`FScaffold` does not take a `floatingActionButton` parameter. For list screens with primary/secondary action buttons (FABs):
- Embedded the body and the FABs within a `Stack`:
  ```dart
  child: Stack(
    children: [
      Positioned.fill(
        child: Material(
          color: Colors.transparent,
          child: <bodyWidget>,
        ),
      ),
      Positioned(
        right: 16,
        bottom: 16,
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [ ...<FABs>... ],
        ),
      ),
    ],
  )
  ```
- This preserved all existing semantics, hero tags, layouts, and test finders (`find.widgetWithText(FloatingActionButton, ...)`).

## 4. Verification Evidence
- **Scaffold Grep**:
  `git grep -nE '([^F]|^)Scaffold\(' lib` → **0 hits**.
- **Static Analysis**:
  `flutter analyze` → **0 issues** ("No issues found!").
- **Code Formatting**:
  `dart format --set-exit-if-changed .` → **Clean** (0 changed).
- **Commit**:
  Committed to `step-0051-ui-debt-closure` as `b706f9c` (`refactor(STEP-51.4): migrate residual Scaffold to FScaffold across lib/ (CF-087)`).
- **Test Suite**:
  `flutter test` → Green (550 passed, 5 skipped, 0 failed), baseline maintained with 0 regressions.
