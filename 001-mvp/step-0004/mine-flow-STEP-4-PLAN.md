# mine-flow — STEP-4 PLAN: Tier 1 - Attendance & Daily Logging

**Phase:** Phase 1 — MVP  
**Owner:** Antigravity  
**Status:** In progress  
**Date:** 2026-07-18  
**Branch:** `step-0004-attendance-daily-logging`  
**Repos (projection):** `mine-flow-app`  

> Implements the core domain logic, local Hive caching, BLoC/state management, and responsive Flutter UI screens for field crew attendance tracking and daily operations logging, including offline synchronization integration.

## Motivation
Field foremen and site supervisors need a fast, reliable mobile/web interface to record crew attendance and log daily operational progress (weather, zone, work summary, notes). Because mining sites often experience limited or intermittent connectivity, attendance records and daily log entries must save locally to Hive storage and queue seamlessly into the background sync engine.

## Decisions already locked
- **User Profile:** `Level 2 - Basic coding experience`, `Explanatory` communication style ([local-user.md](file:///d:/AppDev/mine_flow/.throughstone/local-user.md)).
- **Data Model:** `attendance_records` and `daily_logs` tables in Supabase Postgres schema with UUID keys, soft deletes, and `site_id` multi-tenancy ([04-data-model.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/04-data-model.md)).
- **Identity & Auth:** Supabase Auth with RBAC roles (`supervisor`, `foreman`, `crew`) ([16-identity-auth.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/16-identity-auth.md)).
- **Native App Architecture:** Clean Architecture with Hive offline storage engine and event-driven `SyncQueueManager` background sync ([15-native-app-architecture.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/15-native-app-architecture.md)).
- **UI Design System:** Mine Flow dark theme design system (`AppTheme`, custom cards, field status badges) ([07-ui-design-system.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/07-ui-design-system.md)).
- **Test Strategy:** Unit testing for repositories/mappers and widget testing for Flutter screen components ([12-test-strategy.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/12-test-strategy.md)).

## Substeps

| # | Title | Produces | Depends on | Open questions |
|---|-------|----------|------------|----------------|
| 4.1 | Attendance Domain & Data Layer | `lib/features/attendance/domain/`, `lib/features/attendance/data/` | STEP-3 | None |
| 4.2 | Crew Attendance UI Screens & State | `lib/features/attendance/presentation/` | Substep 4.1 | None |
| 4.3 | Daily Logging Domain & Data Layer | `lib/features/daily_log/domain/`, `lib/features/daily_log/data/` | STEP-3 | None |
| 4.4 | Daily Logging UI Screens & State | `lib/features/daily_log/presentation/` | Substep 4.3 | None |
| 4.5 | Offline Sync Integration & Verification | `test/`, Sync Queue bindings | Substeps 4.1-4.4 | None |

## Test plan

| Test tier / surface | Substep(s) | Tests to create or update | Run timing | Command / gate | Notes |
|---------------------|------------|---------------------------|------------|----------------|-------|
| Unit / Model | 4.1, 4.3 | Entity & DTO serialization for attendance & daily logs | Per substep | `flutter test test/unit/attendance_log_test.dart` | Tests models & mappers |
| Unit / Storage | 4.1, 4.3 | Hive local CRUD for attendance & daily log storage boxes | Per substep | `flutter test test/unit/hive_attendance_daily_log_test.dart` | Tests offline storage |
| Widget / UI | 4.2, 4.4 | Widget tests for attendance roster toggle & daily log form | Per substep | `flutter test test/widget/attendance_daily_log_ui_test.dart` | Tests presentation widgets |
| Integration / Sync | 4.5 | Offline sync queue registration & verification | Final verification | `flutter test` | Full test suite gate |

## Open questions
- None.

## Ground rules
- **Calibrate communication:** Explanatory tone, code comments explaining *why*, step-by-step verification.
- **Tests ship with code:** Every substep includes unit or widget test cases.
- **Clean Architecture:** Keep domain entities decoupled from Supabase/Hive dependencies using DTO mappers.
- **Secrets:** Keep `.env.example` placeholder keys clean without committing real credentials.

## Definition of done
- [x] Attendance domain entities, DTOs, Hive storage adapters, and repository implemented.
- [x] Attendance UI screens (crew roster, status toggling, summary view) built and tested.
- [x] Daily log domain entities, DTOs, Hive storage adapters, and repository implemented.
- [x] Daily log UI screens (weather, zone selector, summary notes, draft status) built and tested.
- [ ] Attendance and Daily Log repositories integrated into `SyncQueueManager`.
- [ ] All unit, widget, and integration tests passing (`flutter test`).
- [ ] `prompts/STEP-index.md` updated and STEP-4 archived to `prompts/001-mvp/step-0004/`.
