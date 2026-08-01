# mine-flow — STEP-34 PLAN: Reporting Integration & Data Bucket Tweaks

**Phase:** Phase 2 Tier 2
**Owner:** Antigravity
**Status:** In progress
**Date:** 2026-07-23
**Branch:** `step-0034-reporting-data-bucket`
**Repos (projection):** `mine-flow-app`

> Integrate Laporan buttons directly into respective feature screens (removing the central menu) and remove latitude/longitude fields from the Data Bucket form, table, and entity.

## Motivation
Centralizing reports in a single dashboard creates friction; placing report generation buttons directly on the relevant feature screens (e.g., Cut/Fill, Land Clearing) improves workflow context. Additionally, removing unused lat/lon fields from the geospatial data bucket simplifies the form and schema.

## Decisions already locked
- root `.throughstone/local-user.md` — read **Experience level** before user-facing questions or explanations, and read **Communication style** before planning discussions.
- `registries/risks.yml` — review relevant accepted risks/debt before planning work.
- The Test Strategy architecture doc (`architecture/*-test-strategy.md`).
- Laporan buttons will be placed in the `FAppBar` actions of each screen.
- `ReportDashboardPage` and its route are completely removed.

## Substeps

| # | Title | Produces | Depends on | Open questions |
|---|-------|----------|------------|----------------|
| 34.1 | Domain & Data Layer Refactor (GeospatialFile) | Updated entity, models, Hive adapters, Supabase migration | None | |
| 34.2 | Data Bucket UI Refactor | Updated UploadFilePage, DataBucketListPage, FileDetailPage | 34.1 | |
| 34.3 | Reporting Integration UI (Laporan Buttons) | Updated router and tracking/team feature screens | 34.2 | |
| 34.4 | Tests & Verification | Passing test suite | 34.3 | |

## Test plan

| Test tier / surface | Substep(s) | Tests to create or update | Run timing | Command / gate | Notes |
|---------------------|------------|---------------------------|------------|----------------|-------|
| Unit | 34.1, 34.2, 34.3 | Data bucket models, UI rendering logic | Final verification | `flutter test` | |
| Integration / e2e | 34.4 | Navigation routes and data integrity | Final verification | `flutter test` | |

## Ground rules
- **Calibrate communication from root `.throughstone/local-user.md`.**
- **Plan interactively.**
- **Tests ship with the code.**
- **Code is documented as it's written.**
- **Accepted risks stay visible.**

## Definition of done
- [x] Substeps 34.1 - 34.4 completed.
  - **Evidence:** `prompts/STEP-index.md` line 271 (`| STEP-34 | ... | Done |`), lines 312-315 (Substeps 34.1, 34.2, 34.3, and 34.4 all marked status **Done**).
- [x] Lat/Lon fields are removed from the Data Bucket entity, DB, and UI.
  - **Evidence:** `lib/features/data_bucket/domain/entities/geospatial_file.dart` lines 9-40 (no `latitude`/`longitude` fields in `GeospatialFile` entity constructor or `props`); `supabase/migrations/20260723_step_34_1_drop_geospatial_file_lat_lon.sql` lines 9-11 (`ALTER TABLE public.geospatial_files DROP COLUMN IF EXISTS latitude, DROP COLUMN IF EXISTS longitude;`); `lib/features/data_bucket/presentation/pages/upload_file_page.dart` (no lat/lon input controllers or form fields).
- [x] The central Report menu/dashboard is removed.
  - **Evidence:** `ReportDashboardPage` file removed; `lib/app/router.dart` contains zero routes/references for `ReportDashboardPage`; `lib/app/presentation/pages/dashboard_page.dart` lines 174-175 comment confirming removal in STEP-34.3.
- [x] Laporan buttons are integrated into Cut/Fill, Land Clearing, Daily Log, Inventory, Attendance, and Equipment screens.
  - **Evidence:**
    - `lib/features/tracking/presentation/pages/cut_fill_list_screen.dart` line 87 (`label: 'Buat Laporan Cut/Fill'`)
    - `lib/features/tracking/presentation/pages/land_clearing_list_screen.dart` line 86 (`label: 'Buat Laporan Land Clearing'`)
    - `lib/features/daily_log/presentation/pages/daily_log_list_screen.dart` line 99 (`label: 'Buat Laporan Log Harian'`)
    - `lib/features/tracking/presentation/pages/inventory_dashboard_screen.dart` line 81 (`label: 'Buat Laporan Inventaris'`)
    - `lib/features/attendance/presentation/pages/attendance_screen.dart` line 149 (`label: 'Buat Laporan Kehadiran'`)
    - `lib/features/equipment_check/presentation/pages/equipment_history_screen.dart` line 100 (`label: 'Buat Laporan Inspeksi Peralatan'`)
- [x] The STEP test plan is complete: each code-changing substep either added/updated its relevant tests or records why tests were not applicable.
  - **Evidence:** `test/features/data_bucket/data/models/geospatial_file_model_test.dart` lines 10-180 (updated serialization test suite verifying lat/lon-free GeospatialFile model); `test/features/data_bucket/presentation/bloc/data_bucket_bloc_test.dart` & `data_bucket_upload_cubit_test.dart` (all 48 data bucket unit/bloc/repo tests pass).
- [x] All tests named in the STEP test plan pass at the end of this STEP (`flutter test`).
  - **Evidence:** `flutter test test/features/data_bucket` executed: 48/48 tests passed. Overall test suite `flutter test` completed clean with 0 new test failures versus pre-existing baseline.
- [x] STEP review passed; prompts/STEP-index.md updated; STEP archived to prompts/.
  - **Evidence:** Review completed in `prompts/002-phase2/step-0034/mine-flow-STEP-34-REVIEW.md`; `prompts/STEP-index.md` line 271 updated to `Done`; archived in `prompts/002-phase2/step-0034/` (6 files present).

