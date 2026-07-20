# mine-flow — STEP-4.2: Crew Attendance UI Screens & State

> **How to run:** Tell your agent *"run substep 4.2"* (or *"read and run this file"*).

## Context
Substep 4.1 implemented the Attendance data layer and domain models. Substep 4.2 builds the responsive Flutter presentation layer (state management via BLoC/Cubit or Riverpod/Provider, UI widgets, and screens) allowing foremen and supervisors to view site crew members, toggle attendance statuses, and submit daily attendance records.

## Read these first
- `Code/mine-flow-docs/architecture/07-ui-design-system.md`
- `Code/mine-flow-docs/architecture/15-native-app-architecture.md`
- `Code/mine-flow-app/README.md`
- `Upcoming Prompts/mine-flow-STEP-4-PLAN.md`

## Scope
- **Owns:** `lib/features/attendance/presentation/` (BLoC/Cubit, screens, widgets, status chips, summary cards).
- **Does NOT touch:** Core data models or Supabase migration files.

## Your task
1. Implement `AttendanceBloc` / state manager handling state transitions (`AttendanceLoading`, `AttendanceLoaded`, `AttendanceSubmitting`, `AttendanceError`).
2. Build `AttendanceScreen` (Crew roster list, date selector, quick-toggle status buttons, search filter).
3. Build `AttendanceSummaryCard` showing counts of Present, Absent, Sick, and Leave crew members.
4. Add field-friendly UI controls (large touch targets, high contrast dark theme badges).
5. Write widget tests for `AttendanceScreen` and status toggle controls.

## Verification
- Write widget tests in `test/widget/attendance_screen_test.dart`.
- Run: `flutter test test/widget/attendance_screen_test.dart`.

## Keeping the docs true
- Ensure UI design tokens follow `07-ui-design-system.md`.

## Definition of done
- [ ] BLoC/state management created for attendance flow.
- [ ] Responsive Flutter attendance screen and crew roster built.
- [ ] Status toggle chips (Present, Absent, Sick, Leave) functional.
- [ ] Widget tests passing (`flutter test`).

## Next
Update STEP-4 PLAN and run **Substep 4.3**.
