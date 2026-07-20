# mine-flow — STEP-8 PLAN: Tier 2 - Data Bucket Integration

**Phase:** Phase 1 — MVP
**Owner:** Antigravity
**Status:** In progress
**Date:** 2026-07-18
**Branch:** `step-0008-data-bucket-integration`
**Repos (projection):** `mine-flow-app`, `mine-flow-docs`, `prompts`

> Integrates Google Drive API for uploading heavy geospatial files (.shp, .tiff) and saves associated metadata (location, zone, acquisition date) to Supabase. Implements the Data Bucket feature — a searchable file registry with a file upload flow, browser/filter UI, and offline metadata queueing.

## Motivation

Mining and survey operations regularly produce geospatial files (shapefiles, GeoTIFFs) that are too large for Supabase storage and must live on Google Drive. Currently there is no structured way to catalog these files by location, zone, or acquisition date. This STEP delivers the **Data Bucket** — a feature that lets supervisors upload geospatial files from within the app (or link existing ones), attach structured metadata, and search/filter the file registry. The architecture doc defines `GeospatialFile` as a core entity (Many-to-One with Zone); this STEP brings it to life.

## Decisions already locked

- root `.throughstone/local-user.md` — read **Experience level** (Level 2 - Basic) before user-facing questions/explanations, and read **Communication style** (Explanatory) before planning discussions.
- `Code/mine-flow-docs/architecture/04-data-model.md` — `GeospatialFile` entity: UUID PK, `site_id`, `zone_id` (FK to Zone), Drive file ID/link, file name, file type (.shp, .tiff), location coordinates, acquisition timestamp, upload timestamp, notes.
- `Code/mine-flow-docs/architecture/03-architecture-overview.md` & `15-native-app-architecture.md` — Clean Architecture layout (`domain`, `data`, `presentation`), BLoC/Cubit state management, repository pattern with `SyncQueueManager` offline sync.
- `Code/mine-flow-docs/architecture/08-infrastructure-deployment.md` — Geospatial files stored on Google Drive using standard Google APIs; Drive API accessed via the `googleapis` Dart package.
- `Code/mine-flow-docs/architecture/11-interface-contracts.md` — App ↔ Google Drive boundary uses the official `googleapis` package as the contract of record.
- `Code/mine-flow-docs/architecture/12-test-strategy.md` — Unit tests for repositories and BLoCs, Widget tests for upload form and file browser, integration verification for sync.
- **Google Drive auth:** Service account (server-to-server) — no per-user OAuth consent; the app authenticates via a service account key to a shared Drive folder.
- **Graceful degradation:** On Drive API failure, the app shows a "try again later" message and allows queuing metadata for later sync; the core app never crashes from Drive unavailability.

## Substeps

| #   | Title                             | Produces                                                                                                                                                                                                                     | Depends on    | Open questions |
| --- | --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | -------------- |
| 8.1 | Data Bucket Domain & Data Layer   | Supabase migration for `geospatial_files` table; `lib/features/data_bucket/domain/` (entities, repository interface); `lib/features/data_bucket/data/` (models, Supabase datasource, Hive adapters (use TypeId 7), repository impl). EXPLICIT REQUIREMENT: Fully implement `SyncQueueManager` enqueueing in the repository for offline mutations. | None          | None           |
| 8.2 | Google Drive Integration Service  | `lib/core/network/google_drive_service.dart` — Drive API client using service account auth (`googleapis_auth`); file picker integration; upload with chunking/progress callback; file search/lookup; Drive outage/timeout handling and automatic retry logic. | 8.1           | None           |
| 8.3 | Data Bucket UI Screens & State    | `lib/features/data_bucket/presentation/` — BLoC/Cubit for file list + upload; file browser/list screen with search/filter; upload form (file picker + metadata fields); file detail view. EXPLICIT REQUIREMENT: Handle large file selection, display upload progress, and strictly handle error SnackBars. | 8.1, 8.2      | None           |
| 8.4 | Offline Queue & Test Verification | SyncQueueManager binding (`DataBucketSyncRegistrar`) for metadata-only offline queue; EXPLICIT REQUIREMENT: Ensure `registerSyncHandlers` is actually integrated and tested; `test/features/data_bucket/` unit, widget & integration test suites; `flutter test` passes clean. | 8.1, 8.2, 8.3 | None           |

## Test plan

| Test tier / surface | Substep(s) | Tests to create or update                                                        | Run timing  | Command / gate                            | Notes                                              |
| ------------------- | ---------- | -------------------------------------------------------------------------------- | ----------- | ----------------------------------------- | -------------------------------------------------- |
| Unit                | 8.1, 8.4   | Model serialization, Hive adapter mapping, repository CRUD with offline fallback | Substep 8.4 | `flutter test test/features/data_bucket/` | Cover metadata validation, empty/missing fields    |
| Widget / UI         | 8.3, 8.4   | Upload form validation, file list rendering, search/filter interaction           | Substep 8.4 | `flutter test test/features/data_bucket/` | Cover form states, list empty/loading/error states |
| Integration / data  | 8.4        | Repository + sync queue integration, mock Drive service layer                    | Substep 8.4 | `flutter test test/features/data_bucket/` | Verify metadata syncs; Drive calls are mocked      |
| Sync / offline      | 8.4        | Offline metadata enqueue, queue flush on reconnect                               | Substep 8.4 | `flutter test test/features/data_bucket/` | Verify SyncQueueManager integration                |

## Ground rules

- **Calibrate communication from root `.throughstone/local-user.md`.**
- **CRITICAL**: Be incredibly rigorous with Clean Architecture principles. Do not leave dead code. If you create a `SyncRegistrar`, ensure you provide instructions or code on how it connects to the global `SyncQueueManager`.
- **Tests ship with the code.** Test cases cover normal entry, boundary conditions, file type validation, missing coordinates, offline queueing, and Drive error handling. Ensure tests assert that offline mutations are properly DEQUEUED and processed, not just enqueued.
- **Hive Type IDs**: Previous features used Type IDs 4, 5, 6, 10, 11, 12. Use **Type ID 7** for `GeospatialFileModelAdapter`. Do not conflict with existing IDs.
- **Code is documented as it's written.**
- **Accepted risks stay visible.** The Drive service account key is a secret — add to `.env.example` and document its setup, never commit the actual key.

## Definition of done

- [ ] Substep 8.1: Supabase migration created for `geospatial_files` table; domain & data layers implemented.
- [ ] Substep 8.2: Google Drive service implemented with service account auth, upload with progress, and graceful error handling.
- [ ] Substep 8.3: Data Bucket UI complete — file list with search/filter, upload form with metadata fields, file detail view.
- [ ] Substep 8.4: Offline sync queue bound for metadata; full test suite passes.
- [ ] `flutter test` passes cleanly for data_bucket feature tests.
- [ ] All new code is documented; interface contracts doc updated for Drive boundary if new patterns emerged.
- [ ] STEP review passed; `prompts/STEP-index.md` updated; STEP archived to `prompts/`.
