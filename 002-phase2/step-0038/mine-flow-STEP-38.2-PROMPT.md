# mine-flow — STEP-38.2: Cut/Fill and Land Clearing Form Fixes

## Substep Prompt

Follow the `mine-flow-STEP-38-PLAN.md` for substep 38.2.
1. Fix field labels for BCM ("Volume Cut", "m³ (BCM)") and LCM ("Volume Fill", "m³ (LCM)") in `cut_fill_form_screen.dart`.
2. Convert Cut/Fill BCM and LCM fields to a 2-column layout in one row.
3. Remove +/- steppers from Cut/Fill and Plan/Actual fields.
4. Replace Zona fields with `CreatableCombobox` using `ZoneRepository` in Cut/Fill, Land Clearing, and Data Bucket (if present).
5. Replace Metode Clearing with `CreatableCombobox` (defaults: Excavator, Bulldozer, Chainsaw).

## Verification

Update widget tests to assert steppers are absent and CreatableComboboxes are used. Run `flutter analyze` and `flutter test`.
