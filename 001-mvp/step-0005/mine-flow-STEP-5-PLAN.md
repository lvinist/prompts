# mine-flow — STEP-5 PLAN: Tier 1 - Equipment Digital Checks

**Phase:** Phase 1 — MVP
**Owner:** Antigravity
**Status:** Done
**Date:** 2026-07-18
**Branch:** `step-0005-equipment-digital-checks`
**Repos (projection):** `mine-flow-app`

> Implements SOP-based digital condition checks (pre-work & post-work) for GNSS receivers, Total Stations, and Drones/UAVs with local Hive caching, responsive Flutter UI, and background sync queue integration.

## Motivation
Field foremen, survey crews, and drone pilots require digital SOP checklists before and after operating critical site equipment. Paper-based or missing inspection logs lead to safety hazards, uncalibrated survey measurements, and untracked equipment wear. Implementing digital checks with offline-first persistence ensures that condition reports are captured even in remote mine sectors with no network connectivity.

## Decisions already locked
- **User Profile:** `Level 2 - Basic coding experience`, `Explanatory` communication style ([local-user.md](file:///d:/AppDev/mine_flow/.throughstone/local-user.md)).
- **Data Model:** `equipment_checks` table in Supabase Postgres schema with JSONB `checklist` payload, UUID keys, soft deletes, and `site_id` multi-tenancy ([04-data-model.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/04-data-model.md)).
- **Native App Architecture:** Clean Architecture with Hive local caching box (`equipment_checks_box`) and `SyncQueueManager` offline background sync ([15-native-app-architecture.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/15-native-app-architecture.md)).
- **UI Design System:** Mine Flow dark theme design system (`AppTheme`, custom cards, status badges, condition toggles) ([07-ui-design-system.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/07-ui-design-system.md)).
- **Test Strategy:** Unit tests for model serialization/mapping and Hive storage, widget tests for SOP checklist UI forms and history lists, and integration tests for offline sync queue execution ([12-test-strategy.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/12-test-strategy.md)).

## Substeps

| # | Title | Produces | Depends on | Open questions |
|---|-------|----------|------------|----------------|
| 5.1 | Equipment Checks Domain & Data Layer | `lib/features/equipment/domain/`, `lib/features/equipment/data/` | STEP-3 | None |
| 5.2 | SOP Inspection UI & Form Screens | `lib/features/equipment/presentation/` | Substep 5.1 | None |
| 5.3 | Inspection History & Summary Screen | `lib/features/equipment/presentation/` | Substep 5.2 | None |
| 5.4 | Offline Sync Integration & Verification | `test/`, `SyncQueueManager` bindings | Substeps 5.1-5.3 | None |

## Test plan

| Test tier / surface | Substep(s) | Tests to create or update | Run timing | Command / gate | Notes |
|---------------------|------------|---------------------------|------------|----------------|-------|
| Unit / Model | 5.1 | DTO & Entity serialization for equipment checks | Per substep | `flutter test test/unit/equipment_check_model_test.dart` | Tests models & mappers |
| Unit / Repository | 5.1 | Hive local CRUD for equipment checks | Per substep | `flutter test test/unit/equipment_check_repository_test.dart` | Tests offline storage repo |
| Widget / UI | 5.2, 5.3 | Widget tests for SOP checklist form & inspection history screen | Per substep | `flutter test test/widget/equipment_check_screen_test.dart` | Tests presentation widgets |
| Integration / Sync | 5.4 | Equipment checks sync queue registration & integration verification | Final verification | `flutter test` | Full test suite gate |

## Open questions
- None.

## Ground rules
- **Calibrate communication:** Explanatory tone, code comments explaining *why*, step-by-step verification.
- **Tests ship with code:** Every substep includes unit, widget, or integration test cases.
- **Clean Architecture:** Keep domain entities decoupled from Supabase/Hive dependencies using DTO mappers.
- **Secrets:** Keep `.env.example` placeholder keys clean without committing real credentials.

## Definition of done
- [x] Equipment checks domain entities, DTOs, Hive storage adapters, and repository implemented.
- [x] SOP inspection UI screens (equipment selector, pre/post-work checklist toggles, notes) built and tested.
- [x] Inspection history list screen (filtered by equipment type, date, and status) built and tested.
- [x] Equipment checks repositories integrated into `SyncQueueManager` with per-entity handler.
- [x] All unit, widget, and integration tests passing (`flutter test`).
- [x] `prompts/STEP-index.md` updated and STEP-5 archived to `prompts/001-mvp/step-0005/`.
