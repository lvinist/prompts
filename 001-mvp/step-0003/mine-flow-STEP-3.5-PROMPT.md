# mine-flow — STEP-3.5: Repository Sync Engine & Test Verification

> **How to run:** Tell your agent *"run substep 3.5"* (or *"read and run this file"*).

## Context
This is the fifth and final substep of [mine-flow-STEP-3-PLAN.md](file:///d:/AppDev/mine_flow/prompts/001-mvp/step-0003/mine-flow-STEP-3-PLAN.md).
In this substep, we build the offline synchronization engine (`SyncQueueManager`), connect internet connectivity detection (`connectivity_plus`), implement timestamp-based last-write-wins conflict resolution, and run the full test suite to close STEP-3.

## Read these first
- [15-native-app-architecture.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/15-native-app-architecture.md) — Offline syncing strategy, conflict resolution (last-write-wins), connectivity listeners
- [04-data-model.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/04-data-model.md) — Eventual consistency & audit log preservation
- [12-test-strategy.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/12-test-strategy.md) — End-to-end verification requirements
- [mine-flow-STEP-3-PLAN.md](file:///d:/AppDev/mine_flow/prompts/001-mvp/step-0003/mine-flow-STEP-3-PLAN.md) — STEP-3 master plan

## Scope
- **In Scope:**
  - `lib/core/offline/sync_queue_manager.dart`: Background manager listening to connectivity changes. Reads pending `SyncQueueItem` entries from Hive, executes HTTP/Supabase operations in FIFO order, and marks items synchronized.
  - `lib/core/network/network_info.dart`: Connectivity checker service wrapping `connectivity_plus`.
  - Conflict Resolution: Timestamp comparison (last-write-wins) during sync replay.
  - Base Offline-First Repository (`BaseOfflineRepository<T>`) bridging Hive local cache and remote Supabase datasource.
  - Full test suite execution (`flutter test`).
- **Out of Scope:**
  - Feature UI screens (handled in STEP-4, STEP-5, etc.).

## Your task
1. Implement `NetworkInfo` in `lib/core/network/network_info.dart` using `connectivity_plus` to monitor internet availability.
2. Implement `SyncQueueManager` in `lib/core/offline/sync_queue_manager.dart`:
   - Enqueue offline mutations into Hive `sync_queue_box`.
   - Automatically trigger sync processing when device transitions to online state.
   - Replay pending queue items in sequence against Supabase database.
   - Handle retry limits and error logging for failed network requests.
3. Build `BaseOfflineRepository<T>` implementing the offline-first pattern:
   - Read: return local Hive cache immediately; fetch remote in background when online and update cache.
   - Write: write to local Hive cache immediately, push to `SyncQueueManager`, attempt instant remote push if online.
4. Write integration test in `test/integration/sync_queue_manager_test.dart` testing queued offline mutations, online sync execution, and retry behavior.
5. Run full test suite (`flutter test`) and confirm 100% pass rate.
6. Gather STEP-3 files (`mine-flow-STEP-3-PLAN.md`, `mine-flow-STEP-3.1-PROMPT.md` to `3.5-PROMPT.md`) into `prompts/001-mvp/step-0003/`.
7. Update `prompts/STEP-index.md` status of STEP-3 to `Done`.

## Verification
- Run full unit & integration test suite: `flutter test` inside `d:/AppDev/mine_flow/Code/mine-flow-app/`.
- Verify `flutter analyze` passes clean with no static errors.

## Keeping the docs true
- Update `prompts/STEP-index.md` to reflect completed status.
- Ensure all architecture docs match implemented sync signatures.

## Definition of done
- [x] `NetworkInfo` connectivity checker implemented.
- [x] `SyncQueueManager` implemented with FIFO replay and error retries.
- [x] `BaseOfflineRepository` implemented supporting offline-first operations.
- [x] Integration tests in `test/integration/sync_queue_manager_test.dart` passing.
- [x] Full `flutter test` suite passing 100%.
- [x] `flutter analyze` returns zero errors.
- [x] STEP-3 archived to `prompts/001-mvp/step-0003/` and marked `Done` in `prompts/STEP-index.md`.

## Next
Tell the user STEP-3 is complete, run the next-action resolver, and report what to do next in a fresh chat.
