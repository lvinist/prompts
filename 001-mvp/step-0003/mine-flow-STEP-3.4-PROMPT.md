# mine-flow — STEP-3.4: Hive Offline Caching & Local Storage Engine

> **How to run:** Tell your agent *"run substep 3.4"* (or *"read and run this file"*).

## Context
This is the fourth substep of [mine-flow-STEP-3-PLAN.md](file:///d:/AppDev/mine_flow/prompts/001-mvp/step-0003/mine-flow-STEP-3-PLAN.md).
In this substep, we configure Hive local storage engine boxes and TypeAdapters for on-device offline caching of operational records and the pending synchronization queue.

## Read these first
- [15-native-app-architecture.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/15-native-app-architecture.md) — On-device storage engine decision (Hive)
- [04-data-model.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/04-data-model.md) — Offline-first local writes and timestamp consistency
- [12-test-strategy.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/12-test-strategy.md) — Offline storage testing standards
- [README.md](file:///d:/AppDev/mine_flow/Code/mine-flow-app/README.md) — App repository structure

## Scope
- **In Scope:**
  - `lib/core/offline/hive_service.dart`: Initialization service for Hive boxes, path resolution, and box lifecycle management.
  - Hive TypeAdapters for core entities and sync queue items in `lib/core/offline/adapters/`.
  - Hive storage boxes:
    - `attendance_box`
    - `equipment_checks_box`
    - `daily_logs_box`
    - `cut_fill_box`
    - `land_clearing_box`
    - `inventory_box`
    - `sync_queue_box`
  - `lib/core/offline/models/sync_queue_item.dart`: Data structure for pending offline transactions (`id`, `entityType`, `action` [CREATE/UPDATE/DELETE], `payloadJson`, `timestamp`, `syncStatus`).
  - Unit tests in `test/unit/hive_storage_test.dart`.
- **Out of Scope:**
  - Network sync queue manager (handled in Substep 3.5).

## Your task
1. Configure `HiveService` in `lib/core/offline/hive_service.dart`:
   - Initialize Hive for Flutter/Web (`Hive.initFlutter()`).
   - Register all TypeAdapters.
   - Open typed boxes safely with error recovery if box data is corrupted.
2. Implement `SyncQueueItem` model with Hive TypeAdapter (`typeId: 10`).
3. Build TypeAdapters or Hive storage helpers for entity models.
4. Implement generic `HiveCacheRepository<T>` providing `get()`, `getAll()`, `put()`, `delete()`, `clear()`.
5. Write unit tests in `test/unit/hive_storage_test.dart` verifying Hive box initialization, record caching, retrieval, and queue persistence.

## Verification
- Run test suite: `flutter test test/unit/hive_storage_test.dart` inside `d:/AppDev/mine_flow/Code/mine-flow-app/`.

## Keeping the docs true
- Confirm [15-native-app-architecture.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/15-native-app-architecture.md) accurately reflects Hive initialization and TypeAdapter registry choices.

## Definition of done
- [x] `HiveService` implemented for cross-platform local box storage.
- [x] `SyncQueueItem` model created with Hive TypeAdapter.
- [x] Typed Hive boxes configured for all operational data entities.
- [x] Unit tests created in `test/unit/hive_storage_test.dart` and 100% passing.

## Next
Update status in STEP-3 PLAN, then tell the user to proceed to *"run substep 3.5"* in a fresh chat.
