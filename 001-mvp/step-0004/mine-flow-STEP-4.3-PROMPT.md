# mine-flow — STEP-4.3: Daily Logging Domain & Data Layer

> **How to run:** Tell your agent *"run substep 4.3"* (or *"read and run this file"*).

## Context
Substeps 4.1 and 4.2 completed crew attendance tracking. Substep 4.3 establishes the domain models, DTOs, Hive local storage Adapters, and repository implementation for structured Daily Operations Logging (`daily_logs`).

## Read these first
- `overview.md`
- `Code/mine-flow-docs/architecture/04-data-model.md`
- `Code/mine-flow-docs/architecture/15-native-app-architecture.md`
- `Code/mine-flow-docs/architecture/12-test-strategy.md`
- `Code/mine-flow-app/README.md`
- `Upcoming Prompts/mine-flow-STEP-4-PLAN.md`

## Scope
- **Owns:** `lib/features/daily_log/domain/` (entities, repository interface), `lib/features/daily_log/data/` (DTOs, mappers, Hive adapters, repository implementation).
- **Does NOT touch:** UI presentation widgets, attendance code, background sync queue registration.

## Your task
1. Implement `DailyLog` entity and `LogStatus` enum (`draft`, `submitted`, `approved`) in domain.
2. Implement `DailyLogDto` with JSON serialization to/from Supabase Postgres `daily_logs` schema.
3. Build Hive storage box adapter for `DailyLogDto` for local caching and offline persistence.
4. Implement `DailyLogRepository` supporting auto-save of draft logs and submitted state transitions.
5. Create unit tests for models, mappers, Hive adapters, and repository operations.

## Verification
- Write unit tests in `test/unit/daily_log_repository_test.dart` and `test/unit/daily_log_model_test.dart`.
- Run: `flutter test test/unit/daily_log_repository_test.dart test/unit/daily_log_model_test.dart`.

## Keeping the docs true
- Ensure entity structures remain aligned with `04-data-model.md`.

## Definition of done
- [ ] Domain entities and repository interface defined.
- [ ] DTO mappers and Hive adapters generated/built for `DailyLog`.
- [ ] Repository implementation handles offline caching and status transitions.
- [ ] All daily log unit tests pass (`flutter test`).

## Next
Update STEP-4 PLAN and run **Substep 4.4**.
