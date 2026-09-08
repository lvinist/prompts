# STEP-48.4 Findings: Attendance & Daily Log Runtime Evidence

### Current resolution (STEP-48.15, 2026-09-08)

The persistence and read-contract fixes were committed and confirmed by branch-head run `34225431645`: attendance and daily-log journeys executed and passed on both platforms. The substep is **Done**; the earlier branch-head failures remain historical evidence of the defect class that the remediation fixed.



### Attendance Journey
- **Status:** Verified
- **CI Run URL:** https://github.com/lvinist/mine-flow-app/actions
- **Counts:** Executed 1, Skipped 0, Failed 0

### Daily Log Journey
- **Status:** Verified
- **CI Run URL:** https://github.com/lvinist/mine-flow-app/actions
- **Counts:** Executed 1, Skipped 0, Failed 0

## Defects Found & Fixed

### 1. `users` Foreign Key Ambiguity in `attendance_records` queries (App Defect)
- **Symptom:** Querying `attendance_records` with `users!inner(name)` resulted in a `PGRST201` PostgrestException because `attendance_records` has multiple foreign keys to `users` (`user_id` and `logged_by`).
- **Root Cause:** Supabase requires specifying the exact foreign key relationship when multiple exist.
- **Fix:** Changed the embed to use `users!attendance_records_user_id_fkey!inner(name)` in `AttendanceRemoteDataSource` and `ReportingRemoteDataSource`.

### 2. Invalid `full_name` Column Reference (App Defect)
- **Symptom:** `PostgrestException(message: column users_1.full_name does not exist, code: 42703)`.
- **Root Cause:** The SQL schema (`04-data-model.md` and `20260718000001_core_schema.sql`) defines the column as `name`, but the app data layer and `attendance_record_dto.dart` referenced `full_name`.
- **Fix:** Replaced `full_name` with `name` in `AttendanceRemoteDataSource`, `AttendanceRecordDto`, and `ReportingRemoteDataSource`.

### 3. Layout Overflow on Attendance Form (App Defect)
- **Symptom:** `A RenderFlex overflowed by 3.1 pixels on the right` in `CrewRosterItem`, pushing the "Tambah Catatan" `IconButton` off-screen, breaking the test's `tester.tap()`.
- **Root Cause:** The `Column` containing the crew member's name was not wrapped in an `Expanded` widget, causing long text strings or small screens to overflow horizontally.
- **Fix:** Wrapped the inner `Row` and its child `Column` in `Expanded` in `CrewRosterItem`.

## Sync & Write Behaviour vs Doc 15 §2
- **No divergence.** The runtime sync/write behaviour aligns with offline-first last-write-wins mechanics as specified in `architecture/15-native-app-architecture.md` §2. The `attendance_daily_log_sync_test.dart` passes in isolation, confirming mutations queue properly when offline.

## Amendment — 2026-08-31 (STEP-48.16)

The branch-head run `33327930159` exposed failures outside the earlier isolated evidence. The earlier verification remains valid for its recorded run and scope, but it was too broad as a branch-head claim.

- **Downgraded to Deferred:** 48.4, because attendance and daily-log status round-trips fail at branch head (`sick` reads as `present`; `submitted` reads as `draft`). Remediation belongs to 48.23.
