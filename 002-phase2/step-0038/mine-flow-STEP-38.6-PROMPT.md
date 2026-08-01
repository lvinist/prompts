# mine-flow — STEP-38.6: Attendance Form Extraction

## Substep Prompt

Follow the `mine-flow-STEP-38-PLAN.md` for substep 38.6.
1. Extract the inline attendance form from `attendance_screen.dart` to a new `AttendanceFormPage` (`attendance_form_page.dart`).
2. Update the UI to display the employee name and position instead of employee ID.
3. Add a new route `AppRoutes.attendanceForm` (`'/teams/attendance/form'`) and configure it in `router.dart`.
4. Update `attendance_screen.dart` to navigate to the new form page.

## Verification

Add widget tests for `attendance_form_page` to verify rendering and fields. Run `flutter analyze` and `flutter test`.
