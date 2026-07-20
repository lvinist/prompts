# mine-flow — STEP-5.4: Offline Sync Integration & Verification

> **How to run:** Tell your agent *"run substep 5.4"* (or *"read and run this file"*).

## Context
Substeps 5.1 through 5.3 built the domain data layer, SOP inspection form screens, and history list for equipment condition checks. Substep 5.4 registers `EquipmentCheck` sync handlers with `SyncQueueManager`, verifies offline queue creation and background replay, and validates the entire test suite.

## Read these first
- `Code/mine-flow-docs/architecture/15-native-app-architecture.md`
- `Code/mine-flow-docs/architecture/12-test-strategy.md`
- `Code/mine-flow-app/README.md`
- `Upcoming Prompts/mine-flow-STEP-5-PLAN.md`

## Scope
- **Owns:** `lib/core/offline/sync_queue_manager.dart` bindings for `equipment_checks`, `test/integration/equipment_check_sync_test.dart`.
- **Does NOT touch:** Database schema definitions.

## Your task
1. Register `equipment_checks` entity sync event handler in `SyncQueueManager`.
2. Implement JSON payload serialization and deserialization for offline sync queue items of equipment checks.
3. Verify timestamp conflict resolution (last-write-wins) for equipment check mutations.
4. Write integration test `test/integration/equipment_check_sync_test.dart` testing offline creation -> local queue insertion -> remote sync flush.
5. Execute full Flutter test suite (`flutter test`) to verify zero regressions across the codebase.

## Verification
- Write integration tests in `test/integration/equipment_check_sync_test.dart`.
- Run full test suite: `flutter test`.

## Keeping the docs true
- Update `prompts/STEP-index.md` status for STEP-5 and substeps.

## Definition of done
- [x] `equipment_checks` offline sync event handlers registered in `SyncQueueManager`.
- [x] Integration test verifying offline queue to remote sync passing cleanly.
- [x] Entire Flutter test suite (`flutter test`) passing with 0 errors.
- [x] STEP-5 files gathered and archived to `prompts/001-mvp/step-0005/`.

## Next
STEP-5 complete! Proceed to **STEP-6: Mid-Phase Check-in**.
