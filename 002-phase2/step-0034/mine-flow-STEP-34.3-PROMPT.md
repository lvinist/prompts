# mine-flow — STEP-34.3: Reporting Integration UI (Laporan Buttons)

> **How to run:** Tell your agent *"run substep 34.3"* (or *"read and run this file"*).

## Context
This is part of STEP-34. We are removing the central Report Dashboard and moving the "Laporan" action into the `FAppBar` actions of individual feature screens to improve the user workflow.

## Read these first
- `Code/mine-flow-app/lib/app/router.dart`
- `Code/mine-flow-app/lib/features/tracking/presentation/pages/cut_fill_list_screen.dart`
- `Code/mine-flow-app/lib/features/tracking/presentation/pages/land_clearing_list_screen.dart` (or summary screen)
- `Code/mine-flow-app/lib/features/daily_log/presentation/pages/daily_log_list_screen.dart`
- `Code/mine-flow-app/lib/features/tracking/presentation/pages/inventory_dashboard_screen.dart`
- `Code/mine-flow-app/lib/features/attendance/presentation/pages/attendance_screen.dart`
- `Code/mine-flow-app/lib/features/equipment_check/presentation/pages/equipment_history_screen.dart`

## Scope
App router and the `FAppBar` for the 6 primary feature screens.

## Your task
1. Remove `ReportDashboardPage` file, and its route (`AppRoutes.reports`) from `lib/app/router.dart`.
2. Add a "Laporan" icon button (using ForUI's `FButton.icon` or standard action inside `FAppBar.actions`) to the 6 screens listed above.
3. Wire the button to `context.pushNamed(AppRoutes.reportConfig, extra: ReportType.<type>)` matching each screen's context.

## Verification
- Run `flutter analyze` to ensure no route or import errors.
- Tests will be verified in 34.4.

## Keeping the docs true (always)
- No architecture changes expected here, just UI workflow updates.

## Definition of done
- [ ] Central report menu removed.
- [ ] Laporan action added to `FAppBar` in the 6 feature screens.
- [ ] Analyzer passes clean.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user the next action: the next open substep — *"run substep 34.4"*, in a **fresh chat**.
