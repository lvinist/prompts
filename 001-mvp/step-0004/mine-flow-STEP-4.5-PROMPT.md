# mine-flow — STEP-4.5: Offline Sync Integration & Verification

> **How to run:** Tell your agent *"run substep 4.5"* (or *"read and run this file"*).

## Context
Substeps 4.1 through 4.4 built the data, domain, state management, and presentation UI for crew attendance and daily logging. Substep 4.5 binds `AttendanceRepository` and `DailyLogRepository` to the `SyncQueueManager` offline synchronization engine, ensuring offline-created records sync automatically when network connectivity is restored, and verifies the full STEP-4 test suite.

## Read these first
- `Code/mine-flow-docs/architecture/15-native-app-architecture.md`
- `Code/mine-flow-docs/architecture/12-test-strategy.md`
- `Code/mine-flow-app/README.md`
- `Upcoming Prompts/mine-flow-STEP-4-PLAN.md`

## Scope
- **Owns:** `lib/core/offline/sync_queue_manager.dart` bindings, `test/integration/attendance_daily_log_sync_test.dart`.
- **Does NOT touch:** Database schema definitions.

## Your task
1. Register `AttendanceRecord` and `DailyLog` sync event handlers inside `SyncQueueManager`.
2. Implement payload serialization for offline sync items of attendance and daily logs.
3. Handle last-write-wins timestamp conflict resolution during sync execution.
4. Write integration tests for offline creation → sync queue insertion → remote sync flush.
5. Execute full Flutter test suite to verify no regressions.

## Verification
- Write integration tests in `test/integration/attendance_daily_log_sync_test.dart`.
- Run full test suite: `flutter test`.

## Keeping the docs true
- Update `prompts/STEP-index.md` status.

## Definition of done
- [ ] Attendance and Daily Log offline sync event handlers registered in `SyncQueueManager`.
- [ ] Integration test verifying offline queue to remote sync passing.
- [ ] Entire Flutter test suite (`flutter test`) passing cleanly.
- [ ] STEP-4 files gathered and archived to `prompts/001-mvp/step-0004/`.

## Next
STEP-4 complete! Proceed to **STEP-5: Tier 1 - Equipment Digital Checks**.
