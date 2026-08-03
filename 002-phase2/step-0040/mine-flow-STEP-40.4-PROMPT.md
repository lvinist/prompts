# mine-flow — STEP-40.4: Fix smoke test `widget_test.dart` `FAccessibilityScope` crash

This prompt is self-contained. Execute it directly and independently.
*Note: Ensure STEP-40.1 has been completed first, as it establishes the proper `FTheme` wrapper pattern for tests.*

## Context & Failing Tests
**Failures resolved:** 1 test in `test/widget_test.dart`
- `app launches without crashing`

**Root Cause:**
The smoke test simply pumps `MineFlowApp()` and expects it to render without throwing exceptions. However, the initial route is `LoginPage`, which uses an `FButton`. The `FButton` requires an `FAccessibilityScope` (provided by an `FTheme` ancestor). The production `app.dart` injects `FTheme` via the `MaterialApp.router` `builder` parameter. This should make it available to the routed pages, but the smoke test is crashing with `Null check operator used on a null value` at `FAccessibilityScope.focusHighlightOf`. It's likely that the test environment requires an explicit outer `FTheme` wrapper, or the `FTheme` in `app.dart` needs adjustment for test pumping.

## Implementation Approach
**Fix:** Resolve the `FAccessibilityScope` crash in the smoke test.
- First, check how `FTheme` is provided in `app.dart` and see if the test can simply be wrapped in an `FTheme(data: FTheme.neutral.light, child: ...)` during `pumpWidget`.
- Alternatively, adjust `MineFlowApp` in `app.dart` if the `FTheme` placement is genuinely wrong (though prefer fixing the test wrapper if possible, just like in 40.1).

## Files to Touch
- `Code/mine-flow-app/test/widget_test.dart`
- `Code/mine-flow-app/lib/app/app.dart` (only if a production change is strictly necessary)

## Verification Gate
Run this command to verify the substep is complete:
`flutter test test/widget_test.dart`
