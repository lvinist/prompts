# mine-flow — STEP-40.1: Fix `FTheme` wrappers in `daily_log_screen_test.dart`

This prompt is self-contained. Execute it directly and independently.

## Context & Failing Tests
**Failures resolved:** 4 tests in `test/widget/daily_log_screen_test.dart`
- `should render all form fields, weather selector, and auto save indicator`
- `should show validation error when submitting with empty summary`
- `should call submitDailyLog when form is valid and submit button pressed`
- `should select weather chip and trigger auto-save`

**Root Cause:**
The test helpers (`buildFormScreenWidget()` and `buildListScreenWidget()`) in `daily_log_screen_test.dart` wrap the screen in a `MaterialApp(theme: ThemeData(...))` but omit the `FTheme` wrapper. ForUI's `FButton` and other interactive widgets call `FAccessibilityScope.focusHighlightOf(context)` during initialization. Without an `FTheme` ancestor injecting `FAccessibilityScope` into the widget tree, these widgets crash with `Null check operator used on a null value`.

## Implementation Approach
**Fix:** Add `FTheme` to the affected test widget trees via `MaterialApp`'s `builder` parameter (or wrap the test screen directly).
- Look at `attendance_screen_test.dart` for the correct pattern (e.g. `MaterialApp(builder: (_, child) => FTheme(data: FTheme.neutral.light, child: child!))`).
- Apply this `FTheme` wrapper to the test setup in `test/widget/daily_log_screen_test.dart`.

## Files to Touch
- `Code/mine-flow-app/test/widget/daily_log_screen_test.dart`

## Verification Gate
Run this command to verify the substep is complete:
`flutter test test/widget/daily_log_screen_test.dart`
