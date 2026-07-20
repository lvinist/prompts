# mine-flow — STEP-5.3: Inspection History & Summary Screen

> **How to run:** Tell your agent *"run substep 5.3"* (or *"read and run this file"*).

## Context
Substep 5.2 built the SOP inspection form and state management. Substep 5.3 builds the inspection history list screen, providing site foremen and surveyors with a searchable, filterable log of past equipment condition checks.

## Read these first
- `Code/mine-flow-docs/architecture/07-ui-design-system.md`
- `Code/mine-flow-docs/architecture/15-native-app-architecture.md`
- `Code/mine-flow-docs/architecture/12-test-strategy.md`
- `Upcoming Prompts/mine-flow-STEP-5-PLAN.md`

## Scope
- **Owns:** `lib/features/equipment/presentation/screens/equipment_history_screen.dart`, `lib/features/equipment/presentation/widgets/equipment_check_card.dart`, `test/widget/equipment_history_screen_test.dart`.
- **Does NOT touch:** Offline sync manager bindings (handled in 5.4).

## Your task
1. Implement `EquipmentHistoryScreen` displaying a timeline list of completed equipment checks.
2. Add filter chips for Equipment Type (All, GNSS, Total Station, Drone) and Status (All, Passed, Flagged/Failed).
3. Create `EquipmentCheckCard` rendering equipment name, inspector ID, check date, pre/post badge, and status indicator.
4. Write widget tests verifying history list rendering, filter chip application, and card detail view expansion.

## Verification
- Run widget tests: `flutter test test/widget/equipment_history_screen_test.dart`.

## Keeping the docs true
- Re-use common filter chip and status badge components from `lib/core/presentation/widgets/`.

## Definition of done
- [x] `EquipmentHistoryScreen` implemented with search and status/type filter chips.
- [x] `EquipmentCheckCard` built with status styling and condition breakdown.
- [x] Widget tests passing cleanly.

## Next
Proceed to **Substep 5.4: Offline Sync Integration & Verification**.
