# mine-flow — STEP-3.3: Core Data Layer Models & DTO Mappers

> **How to run:** Tell your agent *"run substep 3.3"* (or *"read and run this file"*).

## Context
This is the third substep of [mine-flow-STEP-3-PLAN.md](file:///d:/AppDev/mine_flow/prompts/001-mvp/step-0003/mine-flow-STEP-3-PLAN.md).
In this substep, we implement domain entities and Data Transfer Objects (DTOs) for all 9 core entities, with bidirectional serialization to/from Supabase PostgreSQL JSON formats.

## Read these first
- [04-data-model.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/04-data-model.md) — Entities, relationships, field requirements, UUIDs
- [13-glossary.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/13-glossary.md) — Domain terminology definitions
- [12-test-strategy.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/12-test-strategy.md) — Model unit testing standards
- [README.md](file:///d:/AppDev/mine_flow/Code/mine-flow-app/README.md) — Architecture layout

## Scope
- **In Scope:**
  - Domain Entities in `lib/core/domain/entities/`:
    - `UserEntity`
    - `ZoneEntity`
    - `AttendanceRecordEntity`
    - `EquipmentCheckEntity`
    - `DailyLogEntity`
    - `CutFillRecordEntity`
    - `LandClearingRecordEntity`
    - `InventoryItemEntity`
    - `GeospatialFileEntity`
  - DTO Models in `lib/core/data/models/`:
    - `UserModel`
    - `ZoneModel`
    - `AttendanceRecordModel`
    - `EquipmentCheckModel`
    - `DailyLogModel`
    - `CutFillRecordModel`
    - `LandClearingRecordModel`
    - `InventoryItemModel`
    - `GeospatialFileModel`
  - Serialization methods: `fromJson()`, `toJson()`, `toDomain()`, `fromDomain()`.
  - Unit tests in `test/unit/models_test.dart` for all 9 entity models.
- **Out of Scope:**
  - Offline Hive caching adapters (handled in Substep 3.4).

## Your task
1. Create immutable Domain Entities using `equatable` under `lib/core/domain/entities/`.
2. Create Data Models (DTOs) under `lib/core/data/models/` implementing JSON mapping to convert database rows from Supabase into Domain Entities.
3. Ensure all models handle:
   - Nullable fields cleanly.
   - ISO-8601 DateTime strings converting to Dart `DateTime`.
   - Enum string conversions (e.g. `UserRole`, `AttendanceStatus`, `LogStatus`).
   - `siteId` default fallbacks.
4. Write comprehensive unit tests in `test/unit/models_test.dart` verifying JSON parsing, equality, and domain entity mapping for all 9 entities.

## Verification
- Run test suite: `flutter test test/unit/models_test.dart` inside `d:/AppDev/mine_flow/Code/mine-flow-app/`.

## Keeping the docs true
- Ensure all entity property names strictly match the field names defined in [04-data-model.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/04-data-model.md) and [13-glossary.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/13-glossary.md).

## Definition of done
- [x] 9 Domain Entities created in `lib/core/domain/entities/`.
- [x] 9 Data Models (DTOs) with `fromJson`, `toJson`, `toDomain`, and `fromDomain` created in `lib/core/data/models/`.
- [x] Unit test suite created in `test/unit/models_test.dart` and 100% passing.

## Next
Update status in STEP-3 PLAN, then tell the user to proceed to *"run substep 3.4"* in a fresh chat.
