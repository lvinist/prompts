# mine-flow — STEP-32.2: Shared CreatableCombobox Widget

> **How to run:** Tell your agent *"run substep 32.2"* (or *"read and run this file"*).

## Context
Following the Phase 2 ForUI migration, we need a shared combobox widget that adheres to the `forui` styling (`FThemes.zinc`) and allows users to type and dynamically create a new option if it doesn't exist in the list. This is a common pattern for field data entry where the predefined list might be incomplete.

## Read these first
- `architecture/07-ui-design-system.md`
- `Code/mine-flow-app/README.md`
- ForUI documentation on `FSelect` and `FTextField` (if available, otherwise refer to Phase 2 implementations in `lib/features/`).

## Scope
This substep ONLY creates the reusable presentation widget `CreatableCombobox` in a shared location (e.g., `lib/core/presentation/widgets/creatable_combobox.dart`). It does NOT wire the widget to the specific Zone feature or modify `ZonePicker`.

## Your task
1. Create `CreatableCombobox<T>` in `lib/core/presentation/widgets/`.
2. The widget should accept a list of generic items `T`, a `labelBuilder` function (to display the item), an `onChanged` callback, and an `onCreateNew` callback (when the user types an option not in the list and hits enter or selects an "Add 'X'" tile).
3. The widget must adhere to the `FThemes.zinc` styling (e.g., using `FTextField` as the search anchor, and standard borders/spacing per Doc 07).
4. Ensure keyboard accessibility and clean focus management.

## Verification
- Write widget tests for `CreatableCombobox` to verify that existing options can be selected and that typing a new string triggers `onCreateNew`.
- Run `flutter test` for these tests.

## Definition of done
- [ ] `CreatableCombobox` widget implemented using `forui` tokens.
- [ ] Widget tests created and passing.
- [ ] Docstrings added.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user the next action: *"run substep 32.3"*, in a **fresh chat**.
