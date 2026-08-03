# mine-flow — STEP-40.3: Fix `SyncQueueManager` retry test timing race

This prompt is self-contained. Execute it directly and independently.

## Context & Failing Tests
**Failures resolved:** 1 test in `test/integration/sync_queue_manager_test.dart`
- `handles retries and marks failed items after exceeding max retries`

**Root Cause:**
The test expects `attemptCounter` to equal `2`, but it is actually `1`.
The `SyncQueueManager` has an `_isProcessing` guard lock. `enqueueMutation()` automatically calls `processQueue()` via an `unawaited()` fire-and-forget call. The test code calls `enqueueMutation()`, waits `100ms`, and then manually calls `await processQueue()` to trigger the retry.
Because 100ms is not a reliable synchronization barrier, the first unawaited `processQueue()` call may not have cleared its `_isProcessing = false` lock by the time the second manual call is made. If the second call hits `if (_isProcessing) return;`, it exits immediately. As a result, the `customSyncHandler` is never called a second time, leaving `attemptCounter` at 1.

## Implementation Approach
**Fix:** Make the test deterministic without relying on wall-clock timing (`Future.delayed`).
- Change the test to explicitly call and wait for `processQueue()` for each attempt, avoiding the race condition.
- You may need to bypass the auto-trigger in `enqueueMutation` for this test, or ensure that you `await` the process correctly so that the lock is released before you trigger the next retry attempt.

## Files to Touch
- `Code/mine-flow-app/test/integration/sync_queue_manager_test.dart`

## Verification Gate
Run this command to verify the substep is complete:
`flutter test test/integration/sync_queue_manager_test.dart`
