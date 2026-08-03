# mine-flow — STEP-40.2: Migrate 2 `AttendanceScreen` tests to `AttendanceFormPage`

This prompt is self-contained. Execute it directly and independently.

## Context & Failing Tests
**Failures resolved:** 2 tests in `test/widget/attendance_screen_test.dart`
- `should update summary counts when status chip is toggled`
- `should call saveAttendanceBatch when save button is pressed`

**Root Cause:**
In STEP-38, the bulk-edit functionality for attendance was extracted into a dedicated `AttendanceFormPage` (`/teams/attendance/form`). The `AttendanceScreen` was changed to show a **read-only** attendance roster history. The legacy tests are still targeting `AttendanceScreen` expecting it to be interactive. Because `CrewRosterItem(readOnly: true)` is used, tapping the `StatusToggleChips` has no effect (the 'Belum Disimpan' badge never appears), and the `Simpan Absensi (N Kru)` button no longer exists on `AttendanceScreen` (it lives in `AttendanceFormPage`).

## Implementation Approach
**Fix:** Migrate these two tests to target `AttendanceFormPage` instead of `AttendanceScreen`.
- Set up the test to pump `AttendanceFormPage` (you may need to mock the appropriate BLoC/Cubit states to provide initial records so the form is populated).
- Verify that toggling the status chip triggers the unsaved changes state.
- Verify that pressing the save button calls the expected repository or bloc method (`saveAttendanceBatch` equivalent).

## Files to Touch
- `Code/mine-flow-app/test/widget/attendance_screen_test.dart` (rename to `attendance_form_page_test.dart` if appropriate, or keep/split it)

## Verification Gate
Run this command to verify the substep is complete:
`flutter test test/widget/attendance_screen_test.dart` (and any new test file if you split them).
