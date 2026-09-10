# mine-flow - STEP-51.9 FINDINGS: Dead-file disposition

**Substep:** 51.9 - dead-file disposition and orphan sweep  
**Date:** 2026-09-09  
**Status:** Implementation complete; verification gates run below.  
**Owner decision:** User confirmed deletion of both product-intent widgets.

## Scope and concurrency boundary

The app worktree already contained the sibling STEP-51 migration edits across the `lib/` tree. This substep staged only the eleven explicitly owned deletions and the l10n guard cleanup. No other modified or untracked file was reverted, normalized, or staged.

## Dispositions

All candidates were checked with exact `(import|export|part)` path matching across `lib/`, `test/`, `integration_test/`, and `main.dart`. Each had zero references before deletion.

| File | Disposition | Reason |
|---|---|---|
| `lib/features/tracking/tracking.dart` | Deleted | Dead feature barrel; zero exact references. |
| `lib/features/benchmark/benchmark.dart` | Deleted | Dead feature barrel; basename matches were entity noise; zero exact references. |
| `lib/features/data_bucket/data_bucket.dart` | Deleted | Dead feature barrel; zero exact references. |
| `lib/features/tracking/data/data.dart` | Deleted | Barrel twin imported only by the dead tracking barrel. |
| `lib/features/tracking/domain/domain.dart` | Deleted | Barrel twin imported only by the dead tracking barrel. |
| `lib/features/data_bucket/data/data.dart` | Deleted | Barrel twin imported only by the dead data-bucket barrel. |
| `lib/features/data_bucket/domain/domain.dart` | Deleted | Barrel twin imported only by the dead data-bucket barrel. |
| `lib/features/data_bucket/data/models/hive/geospatial_file_hive_adapter.dart` | Deleted | Duplicate never-registered adapter; feature copy used typeId 13, while the registered core adapter remains typeId 7. |
| `lib/app/presentation/models/app_nav_model.dart` | Deleted | Dead navigation model; shell owns its live private sidebar configuration. |
| `lib/features/notifications/presentation/widgets/notification_badge.dart` | Deleted | Zero exact references; user confirmed no planned product use for this lane. |
| `lib/features/reporting/presentation/widgets/report_type_card.dart` | Deleted | Zero exact references; report type picker is the live surface. |

The two stale entries for the already-deleted STEP-48 shadow files were removed from `tool/check_l10n_baseline.dart`:

- `lib/app/presentation/pages/settings_page.dart`
- `lib/app/presentation/widgets/app_shell.dart`

## Duplicate and orphan checks

- Exact references to every deleted path after deletion: **0**.
- Hive registration: only `GeospatialFileModelAdapter` in `lib/core/offline/adapters/model_adapters.dart`, typeId **7**, registered by `hive_service.dart`; no feature duplicate remains.
- The broad orphan sweep surfaced six candidates requiring classification, not deletion:
  - `core/data/models/attendance_record_model.dart`
  - `core/data/models/daily_log_model.dart`
  - `core/data/models/equipment_check_model.dart`
  - `core/data/models/geospatial_file_model.dart`
  - `l10n/app_localizations_en.dart`
  - `l10n/app_localizations_id.dart`
  The four model files are consumed through barrel exports; the two localization files are generated localization outputs. They were not touched.
- `lib/features/all_dart_files.txt` contains stale path inventory text mentioning two deleted files; it is not an import/export/part reference and was outside this substep's code scope.

## Verification

- `dart format --set-exit-if-changed lib/ tool/check_l10n_baseline.dart`: **0 changed** (228 files checked).
- `flutter analyze`: **No issues found**.
- `dart run tool/check_l10n_baseline.dart`: **[OK]**, 13 non-exempt scanned / 45 legacy exempt.
- `flutter test`: **550 passed, 5 skipped, 0 failed**.

## Staged boundary

The staged set contains exactly the eleven owned deletions. The l10n guard edit remains the only additional owned file and is to be staged with the same substep change. The sibling's modified files remain unstaged and preserved.

## Next

After these gates pass, run substep **51.10** in a fresh chat for full verification and STEP close.
