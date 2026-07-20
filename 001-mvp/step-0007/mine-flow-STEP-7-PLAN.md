# mine-flow — STEP-7 PLAN: Tier 2 - Field Tracking & Measurement

**Phase:** Phase 1 — MVP
**Owner:** Antigravity
**Status:** In progress
**Date:** 2026-07-18
**Branch:** `step-0007-field-tracking-measurement`
**Repos (projection):** `mine-flow-app`, `mine-flow-docs`, `prompts`

> Implements manual entry forms, data models, repository layers, offline caching, UI presentation screens, and sync queue integration for Cut/Fill volume tracking, Land Clearing area tracking, and Inventory tracking.

## Motivation

Field operations at mining and excavation sites require precise tracking of material movement (cut/fill m³), cleared land area (m² or hectares), and consumable/equipment inventory on site. This STEP delivers Tier 2 tracking capabilities in `mine-flow-app`, giving foremen and site engineers digital tools to log volume, clearing progress, and inventory levels offline or online.

## Decisions already locked

- root `.throughstone/local-user.md` — read **Experience level** (Level 2 - Basic) before user-facing questions/explanations, and read **Communication style** (Explanatory) before planning discussions.
- `Code/mine-flow-docs/architecture/04-data-model.md` — entities: `CutFillRecord`, `LandClearingRecord`, `InventoryItem`; UUID primary keys; `site_id` dimension; Supabase Postgres storage with Hive local offline caching.
- `Code/mine-flow-docs/architecture/03-architecture-overview.md` & `15-native-app-architecture.md` — Clean Architecture layout (`domain`, `data`, `presentation`), BLoC/Cubit state management, repository pattern with `SyncQueueManager` offline sync.
- `Code/mine-flow-docs/architecture/12-test-strategy.md` — Unit tests for repositories and BLoCs, Widget tests for form inputs and state rendering, integration verification for sync.

## Substeps

| #   | Title                                   | Produces                                                                                                                                        | Depends on         | Open questions |
| --- | --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | -------------- |
| 7.1 | Field Tracking Domain & Data Layer      | `lib/features/tracking/domain/`, `lib/features/tracking/data/` (CutFill, LandClearing, Inventory entities, models, repositories, Hive adapters) | None               | None           |
| 7.2 | Cut/Fill Volume Tracking UI & State     | `lib/features/tracking/presentation/pages/cut_fill_*`, BLoCs/Cubits, forms & history views                                                      | 7.1                | None           |
| 7.3 | Land Clearing Area Tracking UI & State  | `lib/features/tracking/presentation/pages/land_clearing_*`, BLoCs/Cubits, forms & history views                                                 | 7.1                | None           |
| 7.4 | Inventory Tracking UI & State           | `lib/features/tracking/presentation/pages/inventory_*`, BLoCs/Cubits, item management & quantity forms                                          | 7.1                | None           |
| 7.5 | Offline Sync Integration & Verification | Offline sync queue bindings, `test/features/tracking/` unit & widget test suites                                                                | 7.1, 7.2, 7.3, 7.4 | None           |

## Test plan

| Test tier / surface | Substep(s)         | Tests to create or update                                                    | Run timing  | Command / gate                         | Notes                                       |
| ------------------- | ------------------ | ---------------------------------------------------------------------------- | ----------- | -------------------------------------- | ------------------------------------------- |
| Unit                | 7.1, 7.5           | Model serialization, Hive adapter mapping, Repository offline fallback logic | Substep 7.5 | `flutter test test/features/tracking/` | Verify entity conversion & offline storage  |
| Widget / UI         | 7.2, 7.3, 7.4, 7.5 | Form validation, BLoC state rendering, volume & area calculations            | Substep 7.5 | `flutter test test/features/tracking/` | Verify field validation & UI responsiveness |
| Sync / Integration  | 7.5                | Offline queue enqueue and sync execution                                     | Substep 7.5 | `flutter test test/features/tracking/` | Verify SyncQueueManager integration         |

## Ground rules

- **Calibrate communication from root `.throughstone/local-user.md`.**
- **Tests ship with the code.** Test cases cover normal entry, boundary conditions, zero/negative volume checks, unit conversions, offline queueing.
- **Code is documented as it's written.**
- **Accepted risks stay visible.**

## Definition of done

- [x] Substep 7.1 domain and data layers implemented for Cut/Fill, Land Clearing, and Inventory tracking.
- [x] Substep 7.2 UI screens and state management completed for Cut/Fill volume logging and historical tracking.
- [x] Substep 7.3 UI screens and state management completed for Land Clearing area tracking.
- [x] Substep 7.4 UI screens and state management completed for Inventory item tracking and stock adjustments.
- [x] Substep 7.5 offline sync queue integrated and unit/widget tests passing.
- [x] `flutter test` passes cleanly for tracking feature tests (77/77).
- [ ] STEP review passed; `prompts/STEP-index.md` updated; STEP archived to `prompts/`.
