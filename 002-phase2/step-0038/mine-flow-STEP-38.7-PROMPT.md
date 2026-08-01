# mine-flow — STEP-38.7: Equipment Check Mobile Layout Fix

## Substep Prompt

Follow the `mine-flow-STEP-38-PLAN.md` for substep 38.7.
1. Diagnose layout overflow issues in `equipment_check_form_screen.dart` on narrow viewports (e.g., `< 400dp`).
2. Apply layout fixes such as wrapping horizontal lists in `SingleChildScrollView`, using `Wrap`, or constraining widths to prevent RenderFlex overflow.
3. Ensure the core logical structure (tabs, toggles, checklist) remains unchanged.

## Verification

Update widget tests to use a narrow logical screen size and assert no RenderFlex overflow occurs. Run `flutter analyze` and `flutter test`.
