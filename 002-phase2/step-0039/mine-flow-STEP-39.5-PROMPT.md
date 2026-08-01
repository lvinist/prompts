# mine-flow — STEP-39.5: Low-battery sync implementation and tests

> **How to run:** Tell your agent *"run substep 39.5"* (or *"read and run this file"*).

## Context
This substep implements the owner-approved low-battery hybrid operating rule. This rule prevents background synchronization from draining a field worker's battery when they are running low, while ensuring data is securely queued and manually syncable if needed.

## Read these first
- `Upcoming Prompts/mine-flow-STEP-39-PLAN.md` (read the exact state table carefully)
- `Code/mine-flow-app/lib/core/offline/sync_queue_manager.dart`
- `Code/mine-flow-app/test/integration/sync_queue_manager_test.dart`

## Scope
Modify `sync_queue_manager.dart` and its tests to inject and respect the battery state. Add the `battery_plus` dependency.

## Your task
1. Add `battery_plus` to `Code/mine-flow-app/pubspec.yaml` (use the version vetted in 39.2).
2. Create an injectable battery abstraction (e.g., `BatteryStateProvider`) so unit tests do not call platform channels directly.
3. Implement the exact state table defined in the PLAN:
   - Pause automatic sync if Battery Saver is ON OR raw battery <= 20%.
   - Charging bypasses the pause.
   - Manual user-triggered sync proceeds.
   - Fallbacks: OS saver unavailable -> rely on level. Level unavailable -> rely on OS saver. Both unavailable (e.g. web) -> proceed.
   - Queued operations stay in Hive.
   - Sync resumes on the next tick automatically.
4. Update or write unit tests in `sync_queue_manager_test.dart` to verify every condition of the state table using mocked battery states.

## Verification
- Run `flutter test test/integration/sync_queue_manager_test.dart`.

## Keeping the docs true
- Ensure any added logic is properly documented with docstrings.

## Definition of done
- [ ] `battery_plus` dependency added.
- [ ] Low-battery hybrid rule implemented per state table with `battery_plus` abstraction.
- [ ] Sync unit tests pass verifying all states.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user the next action: *"run substep 39.6"*, in a **fresh chat**.
