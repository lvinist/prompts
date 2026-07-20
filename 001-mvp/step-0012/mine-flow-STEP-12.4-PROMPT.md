# Substep 12.4: Daily Logging Initialization & Offline Sync

**Goal:** Instantiate `DailyLogRepository` and integrate it with offline sync.

**Context:**
`lib/features/daily_log/` contains domain and data layers, but `DailyLogRepository` is completely missing from `lib/core/init/app_initializer.dart`. Furthermore, no sync registrar exists for it.

**Action Plan:**
1. **Create `lib/features/daily_log/data/sync/daily_log_sync_registrar.dart`**:
   - Implement `static void registerSyncHandlers(SyncQueueManager manager, DailyLogRepository repository)`.
   - Register handlers for syncing daily log records (upsert operations).
2. **Update `lib/core/init/app_initializer.dart`**:
   - Open necessary Hive boxes for daily logs (e.g., `daily_logs`).
   - Instantiate `HiveCacheRepository<DailyLogDto>`, `DailyLogRemoteDataSourceImpl` (ensure this exists, otherwise implement a standard Supabase wrapper for it matching the interface in `daily_log_remote_datasource.dart`), and `DailyLogRepositoryImpl`.
   - Call `DailyLogSyncRegistrar.registerSyncHandlers(syncQueueManager, dailyLogRepository);`.
   - Update the `AppServices` class to include `DailyLogRepository` and expose it.
3. **Update `lib/app/router.dart`**:
   - Pass `appServices!.dailyLogRepository` to the `dailyLog` routes defined in Substep 12.1.

**Acceptance Criteria:**
- `AppInitializer` correctly boots the Daily Log data layer.
- `DailyLogSyncRegistrar` is registered.
- The UI can consume `appServices!.dailyLogRepository` without null pointer exceptions.
