# mine-flow — STEP-33.3: Daily Log & Inventory UI Refactor

> **How to run:** Tell your agent *"run substep 33.3"* (or *"read and run this file"*).

## Context
Continuing the UI updates for the Forms Refactor (STEP-33), this substep focuses on the Field Docs & Teams section: Daily Logging and Inventory. We need to integrate the `CreatableCombobox` widget built in STEP-32 into the Daily Log form for seamless Zone selection, and implement an auto-predict mechanism for item names in the Inventory entry form to speed up field data entry.

## Read these first
- overview.md
- `lib/features/daily_log/presentation/pages/daily_log_list_screen.dart` (or entry form)
- `lib/features/tracking/presentation/pages/inventory_item_entry_screen.dart`
- `lib/core/presentation/widgets/creatable_combobox.dart` (from STEP-32)
- `architecture/07-ui-design-system.md`

## Scope
Updates to the Presentation layer (Widgets, Pages, BLoCs) for Daily Log and Inventory features.

## Your task
1. **Daily Log Zone Combobox**:
   - Locate the form where a user inputs a `Zone` for their daily log.
   - Replace the standard text input or static dropdown with the shared `CreatableCombobox`.
   - Ensure the combobox is wired to the local Zone state (from STEP-32) so users can select existing zones or create new ones dynamically.
   - Update the Daily Log BLoC to handle the selected/created zone string.
2. **Inventory Auto-predict**:
   - Update the `InventoryItemEntryScreen` (or relevant input form) to feature an auto-predict/autocomplete mechanism for the item name field.
   - Using the decision made in the PLAN (Q2), implement the logic to fetch suggestions. If querying historical entries, ensure the BLoC queries the local repository for distinct item names matching the current input prefix.
   - Ensure the UI for the autocomplete dropdown matches the `forui` popover/menu aesthetic.
3. **UI Consistency**:
   - Verify that form spacings, typography, and corner radii respect the design tokens.
   - Ensure semantic labels remain intact.

## Verification
- **Run timing:** Assigned to the final verification substep (33.4). No explicit test runs are required before marking this substep done, but the code must be structurally sound and free of analyzer warnings.

## Keeping the docs true  (always)
- If the auto-predict feature introduces a new local caching strategy, update `architecture/04-data-model.md`.

## Definition of done
- [ ] Daily log entry uses `CreatableCombobox` for Zone.
- [ ] Inventory entry uses an auto-predict text field for Item names.
- [ ] BLoCs updated to handle dynamic inputs.
- [ ] Analyzer passes with zero warnings.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user the next action: *"run substep 33.4"* in a fresh chat.
