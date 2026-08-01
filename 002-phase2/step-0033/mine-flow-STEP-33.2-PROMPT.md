# mine-flow — STEP-33.2: Operations Tracking UI Refactor

> **How to run:** Tell your agent *"run substep 33.2"* (or *"read and run this file"*).

## Context
Following the data model polish in 33.1, this substep updates the user interface for the core Operations Tracking tools: Cut/Fill and Land Clearing. The forms must now capture BCM/LCM volumes, material types, clearing methods, and distinguish between plan and actual values. All UI updates must strictly adhere to the `forui` and `shadcn-admin` styling paradigms established in Phase 2 Tier 2.

## Read these first
- overview.md
- architecture/07-ui-design-system.md
- `lib/features/tracking/presentation/pages/cut_fill_list_screen.dart`
- `lib/features/tracking/presentation/pages/land_clearing_summary_screen.dart`
- `lib/features/tracking/presentation/widgets/` (relevant form widgets/dialogs)

## Scope
Updates to the Presentation layer (Widgets, Pages, BLoCs) for Cut/Fill and Land Clearing features to surface the data model changes introduced in 33.1.

## Your task
1. **Cut/Fill UI Updates**:
   - Update the Cut/Fill entry form/dialog to feature two separate volumetric input fields: Bank Cubic Meters (BCM) and Loose Cubic Meters (LCM), replacing the generic volume input.
   - Add a dropdown/combobox for `Material Type` selection.
   - Update the `CutFillListScreen` summary cards and list tiles to display these new data points clearly, adhering to the spacing and typography tokens.
   - Ensure the respective BLoC correctly binds the new form inputs to the updated `CutFillMeasurement` entity.
2. **Land Clearing UI Updates**:
   - Update the Land Clearing entry form to include a combobox for `Method` selection.
   - Replace the single area field with two input fields: `Plan Area` and `Actual Area`.
   - Update the `LandClearingSummaryScreen` to visualize plan vs actual metrics (e.g., using a progress bar or comparative stat cards) and display the method in the list view.
   - Update the respective BLoC to bind these inputs.
3. **UI Consistency**:
   - Ensure all new inputs use `FTextField` / ForUI components.
   - Ensure semantic labels are updated for accessibility.

## Verification
- **Run timing:** Assigned to the final verification substep (33.4). No explicit test runs are required before marking this substep done, but the code must be structurally sound and free of analyzer warnings.

## Keeping the docs true  (always)
- Update any form documentation in `coding-standards/` if new patterns emerge for ForUI integration.

## Definition of done
- [ ] Cut/Fill form features BCM, LCM, and Material Type inputs.
- [ ] Land Clearing form features Plan Area, Actual Area, and Method inputs.
- [ ] List screens and summary cards correctly display the new data.
- [ ] BLoCs updated to handle the new state structures.
- [ ] Analyzer passes with zero warnings.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user the next action: *"run substep 33.3"* in a fresh chat.
