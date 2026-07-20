# mine-flow — STEP-7.5: Offline Sync Integration & Verification

> **How to run:** Tell your agent *"run substep 7.5"* (or *"read and run this file"*).

## Context
This is substep 7.5 of STEP-7 (Tier 2 - Field Tracking & Measurement). In this substep, you will integrate the Cut/Fill, Land Clearing, and Inventory features with `SyncQueueManager` for offline sync support, and write automated test suites to verify tracking functionality.

## Read these first
- `overview.md`
- `Code/mine-flow-docs/architecture/04-data-model.md`
- `Code/mine-flow-docs/architecture/12-test-strategy.md`
- `Upcoming Prompts/mine-flow-STEP-7-PLAN.md`

## Scope
- Sync Integration (`lib/features/tracking/data/sync/`):
  - Register `CutFillRecord`, `LandClearingRecord`, and `InventoryItem` offline sync actions with `SyncQueueManager`.
  - Implement sync processors to replay queued offline transactions to Supabase when network connectivity returns.
- Automated Test Suite (`test/features/tracking/`):
  - `domain/entities_test.dart`: Test entity properties, immutability, and helpers.
  - `data/models_test.dart`: Test JSON serialization (`fromJson`/`toJson`) and Hive model conversions.
  - `data/repositories/tracking_repository_impl_test.dart`: Test repository caching and offline fallback behaviors using mock data sources.
  - `presentation/cut_fill_bloc_test.dart`, `land_clearing_bloc_test.dart`, `inventory_bloc_test.dart`: Unit tests for BLoC state management and event processing.

## Your task
1. Implement sync queue action handlers for Cut/Fill, Land Clearing, and Inventory data modifications in offline mode.
2. Register sync queue processors with `SyncQueueManager`.
3. Create unit tests for domain entities, models, repositories, and BLoCs.
4. Execute `flutter test test/features/tracking/` to verify tests pass cleanly.

## Verification
- Run `flutter test test/features/tracking/` and confirm all tests pass without errors.
- Confirm offline sync queue payloads are correctly structured.

## Definition of done
- [ ] Offline sync processors registered and wired to `SyncQueueManager`.
- [ ] Unit and widget tests created under `test/features/tracking/`.
- [ ] `flutter test test/features/tracking/` passes cleanly.

## Next
**Before finishing this task, you MUST do the bookkeeping:**
1. Open `prompts/STEP-index.md` and change the Status of Substep 7.5 from `Planned` to `Done`. Update the Output / Deliverables column with the paths you created.
2. Open `Upcoming Prompts/mine-flow-STEP-7-PLAN.md` and check off `[x] Substep 7.5` in the Definition of done section.
3. Finally, gather the PLAN and substep prompt files from `Upcoming Prompts/` into `prompts/001-mvp/step-0007/`, and notify the user that STEP-7 is completed.
