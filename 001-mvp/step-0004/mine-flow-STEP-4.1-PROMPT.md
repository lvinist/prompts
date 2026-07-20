# mine-flow — STEP-4.1: Attendance Domain & Data Layer

> **How to run:** Tell your agent *"run substep 4.1"* (or *"read and run this file"*).

## Context
STEP-4 implements Tier 1 field operations (Attendance and Daily Logging). This substep (4.1) establishes the Clean Architecture domain entities, data transfer objects (DTOs), Hive local storage Adapters, and repository implementation for crew attendance logging.

## Read these first
- `overview.md`
- `Code/mine-flow-docs/architecture/04-data-model.md`
- `Code/mine-flow-docs/architecture/15-native-app-architecture.md`
- `Code/mine-flow-docs/architecture/12-test-strategy.md`
- `Code/mine-flow-app/README.md`
- `Upcoming Prompts/mine-flow-STEP-4-PLAN.md`

## Scope
- **Owns:** `lib/features/attendance/domain/` (entities, repository interface), `lib/features/attendance/data/` (DTOs, mappers, Hive adapters, repository implementation).
- **Does NOT touch:** UI presentation widgets, BLoC/State management, daily log tables, background sync queue registration.

## Your task
1. Implement `AttendanceRecord` entity and `AttendanceStatus` enum (`present`, `absent`, `sick`, `leave`) in domain.
2. Implement `AttendanceRecordDto` with JSON serialization to/from Supabase Postgres `attendance_records` schema.
3. Build Hive storage box adapter for `AttendanceRecordDto` for offline local caching.
4. Implement `AttendanceRepository` enforcing local-first write and read pattern with fallback to local cache.
5. Create unit tests for models, mappers, Hive caching, and repository operations.

## Verification
- Write unit tests in `test/unit/attendance_repository_test.dart` and `test/unit/attendance_model_test.dart`.
- Run: `flutter test test/unit/attendance_repository_test.dart test/unit/attendance_model_test.dart`.

## Keeping the docs true
- Ensure entity structures remain aligned with `04-data-model.md`.

## Definition of done
- [ ] Domain entities and repository interface defined.
- [ ] DTO mappers and Hive adapters generated/built for `AttendanceRecord`.
- [ ] Repository implementation handles offline caching and online remote sync data sources.
- [ ] All attendance unit tests pass (`flutter test`).

## Next
Update STEP-4 PLAN and run **Substep 4.2**.
