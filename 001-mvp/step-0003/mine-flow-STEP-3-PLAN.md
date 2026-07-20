# mine-flow — STEP-3 PLAN: Core Data Layer & Authentication

**Phase:** Phase 1 — MVP  
**Owner:** Antigravity  
**Status:** Done  
**Date:** 2026-07-18  
**Branch:** `step-0003-core-data-auth`  
**Repos (projection):** `mine-flow-app`  

> Implements the core database schema, Row-Level Security (RLS) policies, Supabase user authentication, Hive offline caching, and data synchronization layer for the Mine Flow mobile/web client.

## Motivation
Mine Flow requires a secure, multi-tenant database schema and robust authentication before building field operation modules (attendance, daily logs, checks). Foremen operating in remote mine locations without persistent cellular coverage require an offline-first storage engine (Hive) and a background synchronization queue with timestamp-based last-write-wins conflict resolution.

## Decisions already locked
- **User Profile:** `Level 2 - Basic coding experience`, `Explanatory` communication style ([local-user.md](file:///d:/AppDev/mine_flow/.throughstone/local-user.md)).
- **Data Model:** Supabase PostgreSQL owns structured data; UUID primary keys for all entities; `site_id` column included on all operational tables for Phase 2 multi-tenancy readiness ([04-data-model.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/04-data-model.md)).
- **Identity & Auth:** Supabase Auth (Email/Password); 3 RBAC roles (`supervisor`, `foreman`, `crew`); Supervisor-only user account creation via Supabase Edge Function; JWT tokens in secure storage ([16-identity-auth.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/16-identity-auth.md)).
- **Native App Architecture:** Hive chosen for on-device offline caching; `flutter_secure_storage` for tokens; offline-first write pattern with background event-based sync ([15-native-app-architecture.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/15-native-app-architecture.md)).
- **Test Strategy:** Unit & integration tests for data models, Auth repository, and sync queue using `mocktail` ([12-test-strategy.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/12-test-strategy.md)).

## Substeps

| # | Title | Produces | Depends on | Open questions |
|---|-------|----------|------------|----------------|
| 3.1 (Done) | Supabase SQL Schema Migrations & RLS Policies | `supabase/migrations/20260718000001_core_schema.sql`, `20260718000002_rls_policies.sql` | Doc 04, Doc 16 | None |
| 3.2 (Done) | Supabase Auth Edge Function & Flutter Auth Repository | `supabase/functions/create-user/`, `lib/features/auth/` | Substep 3.1 | None |
| 3.3 (Done) | Core Data Layer Models & DTO Mappers | `lib/core/data/models/`, `lib/core/domain/entities/` | Substep 3.1 | None |
| 3.4 (Done) | Hive Offline Caching & Local Storage Engine | `lib/core/offline/hive_service.dart`, Hive Adapters | Substep 3.3 | None |
| 3.5 (Done) | Repository Sync Engine & Test Verification | `lib/core/offline/sync_queue_manager.dart`, `test/` | Substeps 3.2-3.4 | None |

## Test plan

| Test tier / surface | Substep(s) | Tests to create or update | Run timing | Command / gate | Notes |
|---------------------|------------|---------------------------|------------|----------------|-------|
| Unit / DTO | 3.3 | Entity & DTO JSON serialization tests | Per substep | `flutter test test/unit/models_test.dart` | Validates JSON to/from Supabase |
| Unit / Storage | 3.4 | Hive local storage box CRUD & adapter tests | Per substep | `flutter test test/unit/hive_storage_test.dart` | Tests offline caching engine |
| Integration / Auth | 3.2 | Auth repository login/logout/token recovery | Per substep | `flutter test test/integration/auth_repository_test.dart` | Mocks Supabase Client |
| Integration / Sync | 3.5 | Sync queue priority & conflict resolution tests | Final verification | `flutter test` | Tests last-write-wins sync logic |

## Open questions
- None.

## Ground rules
- **Calibrate communication:** Explanatory tone, code comments explaining *why*, step-by-step verification.
- **Tests ship with code:** Every substep includes relevant unit/integration test cases.
- **Clean Architecture:** Keep domain entities decoupled from Supabase/Hive dependencies using DTO mappers.
- **Secrets:** Never commit API keys or service role secrets; use `.env.example` placeholder keys.

## Definition of done
- [x] Supabase SQL migrations and RLS policies created for core schema.
- [x] Supabase Edge Function `create-user` created for Supervisor account provisioning.
- [x] Flutter Auth repository implemented with `flutter_secure_storage` session management.
- [x] Domain entities and DTO mappers built for all 9 entities.
- [x] Hive offline caching initialized with custom adapters and storage boxes.
- [x] Background sync queue manager implemented with timestamp-based conflict resolution.
- [x] All unit and integration tests passing (`flutter test`).
- [x] `prompts/STEP-index.md` updated and STEP-3 archived to `prompts/001-mvp/step-0003/`.
