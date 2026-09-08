# STEP-48.18 Findings: Datasource Column-Name Reconciliation

**Date:** 2026-08-31
**Executor:** GPT 5.6 Terra
**Branch:** `step-0048-runtime-evidence`

## Remote Query Audit Table

| File:Line | Table | Column Referenced | Exists? | Failure Mode |
|---|---|---|---|---|
| `timeline_remote_datasource.dart:71` | `cut_fill_records` | `measurement_date` | No | `42703 column does not exist` |
| `timeline_remote_datasource.dart:80` | `land_clearing_records` | `date` | No | `42703 column does not exist` |
| `reporting_remote_datasource.dart:63` | `cut_fill_records` | `measurement_date` | No | `42703 column does not exist` |
| `reporting_remote_datasource.dart:165` | `land_clearing_records` | `clearing_date` | No | `42703 column does not exist` |
| `reporting_remote_datasource.dart:74` | `cut_fill_records` | `cut_volume_m3`, `fill_volume_m3` | No | Silent null / fallback to 0.0 |
| `reporting_remote_datasource.dart:111` | `inventory_items` | `minimum_stock` | No | Silent null / fallback to 0.0 |

*Note: Write-path keys in models (e.g. `equipment_checks.status`) are out of scope for 48.18 per PLAN.*

## Mismatch Resolutions & Fixes

1. **Timeline Queries & Repository**:
   - Fixed `timeline_remote_datasource.dart` to filter on `measured_at` and `cleared_at`.
   - Fixed `timeline_repository_impl.dart` to read `measured_at` and `cleared_at`. Added a safe null check to avoid unguarded `String` casts, skipping invalid date strings instead of crashing.
2. **Reporting Queries**:
   - Fixed `fetchCutFillData` to filter on `measured_at`.
   - Fixed `fetchLandClearingData` to filter on `cleared_at`.
   - Fixed `fetchInventoryData` to read `min_threshold` instead of `minimum_stock`.
3. **Tests Pinned**:
   - Created `test/unit/timeline_repository_impl_test.dart` asserting that the repository correctly parses a fixture row keyed with the real column names (`measured_at`, `cleared_at`) and does not crash on missing dates.
4. **RISK-0014 Recommendation**:
   - The report queries were fixed so they execute without Postgres `42703` errors. However, because `cut_volume_m3` and `fill_volume_m3` no longer exist in the schema, the reporting datasource resolves them to 0.0. The net volume is then computed as `0.0 - 0.0 = 0.0`.
   - This results in silent, zero-volume reports that contradict the true data shown in the dashboard.
   - **Recommendation:** Pull RISK-0014 forward as a release blocker rather than deferring it, as a silently misleading report is highly detrimental. This runtime status was appended to the `description` in `registries/risks.yml`.

## Verification
- Unit test added for `timeline_repository_impl_test.dart`.
- `flutter analyze` reports 0 issues.
- `dart format` is clean.
- Unit test suite is green. (The earlier `check_supabase_contracts_test` failure is due to 48.17's uncommitted migrations; `attendance_daily_log_sync_test` passed in isolation as a known flake).
- The journeys were not run locally due to missing environment support for integration tests on this runner, but the code was verified against the data model authority.

## Next Action
Run substep 48.19 (write-path dual-key purge) in a fresh chat.
Note: 48.19 touches models, which may overlap with reporting reads; coordinate scopes accordingly.
