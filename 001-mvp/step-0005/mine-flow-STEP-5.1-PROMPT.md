# mine-flow — STEP-5.1: Equipment Checks Domain & Data Layer

> **How to run:** Tell your agent *"run substep 5.1"* (or *"read and run this file"*).

## Context
Substeps 4.1 through 4.5 completed the attendance and daily logging features with offline sync. Substep 5.1 lays the foundational domain entities, DTO serialization, local Hive storage repository, and remote datasource interfaces for SOP-based pre-work and post-work equipment condition checks (`equipment_checks`).

## Read these first
- `Code/mine-flow-docs/architecture/04-data-model.md`
- `Code/mine-flow-docs/architecture/15-native-app-architecture.md`
- `Code/mine-flow-docs/architecture/12-test-strategy.md`
- `Code/mine-flow-app/README.md`
- `Upcoming Prompts/mine-flow-STEP-5-PLAN.md`

## Scope
- **Owns:** `lib/features/equipment/domain/`, `lib/features/equipment/data/`, `test/unit/equipment_check_model_test.dart`, `test/unit/equipment_check_repository_test.dart`.
- **Does NOT touch:** UI presentation screens or BLoC state management (handled in 5.2 and 5.3).

## Your task
1. Define domain entities: `EquipmentCheck`, `CheckItem`, `EquipmentType` (gnss, totalStation, drone), `CheckType` (preWork, postWork), and `CheckStatus` (passed, failed, flagged).
2. Create `EquipmentCheckDto` and `EquipmentCheckDtoAdapter` (Hive typeId: 23) supporting JSON serialization of equipment metadata and item checklist arrays.
3. Implement `EquipmentCheckRepositoryImpl` supporting local-first reads/writes via Hive `equipment_checks_box` and enqueuing sync mutations into `SyncQueueManager`.
4. Write unit tests for model JSON serialization, domain mapping, and local repository CRUD operations.

## Verification
- Run unit tests: `flutter test test/unit/equipment_check_model_test.dart` and `flutter test test/unit/equipment_check_repository_test.dart`.

## Keeping the docs true
- Ensure `EquipmentCheckDtoAdapter` typeId (23) is documented in adapter comments and Hive initialization routines if needed.

## Definition of done
- [x] Domain entities (`EquipmentCheck`, `CheckItem`, `EquipmentType`, `CheckType`, `CheckStatus`) implemented with `equatable`.
- [x] DTO and Hive adapter (typeId 23) implemented.
- [x] `EquipmentCheckRepositoryImpl` implemented with local-first and offline sync queue insertion.
- [x] All unit tests passing cleanly.

## Next
Proceed to **Substep 5.2: SOP Inspection UI & Form Screens**.
