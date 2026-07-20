# Substep 12.3: Attendance Wiring & Offline Sync

**Goal:** Implement and register the missing SyncRegistrar for Attendance.

**Context:**
Crew attendance operates offline in `AttendanceRepositoryImpl`, but there is no `AttendanceSyncRegistrar` to handle dequeuing sync queue items when back online.

**Action Plan:**
1. **Create `lib/features/attendance/data/sync/attendance_sync_registrar.dart`**:
   - Follow the pattern from `DataBucketSyncRegistrar` or `TrackingSyncRegistrar`.
   - Implement `static void registerSyncHandlers(SyncQueueManager manager, AttendanceRepository repository)`.
   - Register handlers for syncing attendance events (e.g., matching the entity types used when `AttendanceRepositoryImpl` queues an item).
2. **Update `lib/core/init/app_initializer.dart`**:
   - Call `AttendanceSyncRegistrar.registerSyncHandlers(syncQueueManager, attendanceRepository);` in the `--- 5. Register feature sync handlers ---` section.

**Acceptance Criteria:**
- `attendance_sync_registrar.dart` exists and handles appropriate data types.
- `AppInitializer.dart` registers it without errors.
