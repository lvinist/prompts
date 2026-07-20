# mine-flow — STEP-5.2: SOP Inspection UI & Form Screens

> **How to run:** Tell your agent *"run substep 5.2"* (or *"read and run this file"*).

## Context
Substep 5.1 established the domain entities and repository for equipment digital checks. Substep 5.2 builds the user-facing Flutter presentation UI and BLoC state management for performing pre-work and post-work SOP condition checks for GNSS, Total Station, and Drone/UAV equipment.

## Read these first
- `Code/mine-flow-docs/architecture/07-ui-design-system.md`
- `Code/mine-flow-docs/architecture/15-native-app-architecture.md`
- `Code/mine-flow-docs/architecture/12-test-strategy.md`
- `Upcoming Prompts/mine-flow-STEP-5-PLAN.md`

## Scope
- **Owns:** `lib/features/equipment/presentation/` (BLoC, SOP inspection form widgets, condition check toggles), `test/widget/equipment_check_form_test.dart`.
- **Does NOT touch:** Inspection history list screen (handled in 5.3).

## Your task
1. Implement `EquipmentCheckBloc` with events (`LoadSopItems`, `ToggleCheckItem`, `UpdateNotes`, `SubmitEquipmentCheck`) and states (`EquipmentCheckInitial`, `EquipmentCheckLoading`, `EquipmentCheckLoaded`, `EquipmentCheckSubmitted`, `EquipmentCheckError`).
2. Build `EquipmentCheckFormScreen` featuring:
   - Equipment Type selector tabs (GNSS, Total Station, Drone/UAV).
   - Check Type toggle (Pre-Work vs Post-Work).
   - Dynamic SOP item checklist cards with Pass / Fail / NA segmented controls.
   - Overall condition summary badge (Passed vs Flagged for Maintenance).
   - Additional remarks/notes text field and Submit button.
3. Write widget tests for form rendering, SOP item status toggling, validation, and submission state.

## Verification
- Run widget tests: `flutter test test/widget/equipment_check_form_test.dart`.

## Keeping the docs true
- Ensure UI components adhere strictly to `AppTheme` colors, card styles, and field status badges.

## Definition of done
- [x] `EquipmentCheckBloc` implemented for SOP checklist state handling.
- [x] `EquipmentCheckFormScreen` built with equipment selector, pre/post-work toggles, and pass/fail checklist cards.
- [x] Widget tests verifying checklist interactions and form submission passing.

## Next
Proceed to **Substep 5.3: Inspection History & Summary Screen**.
