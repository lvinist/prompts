# Substep 12.5: Equipment Check Initialization, Sync & Cleanup

**Goal:** Clean up duplicate code, instantiate `EquipmentCheckRepository`, and integrate it with offline sync.

**Context:**
There are duplicate directories: `lib/features/equipment/` and `lib/features/equipment_check/`. The feature is missing from `AppInitializer.dart`, and has no sync registrar.

**Action Plan:**
1. **Clean up duplications**:
   - Delete `lib/features/equipment/`. Retain `lib/features/equipment_check/` as the single source of truth.
   - Fix any import paths pointing to `features/equipment/` to point to `features/equipment_check/` instead.
2. **Create `lib/features/equipment_check/data/sync/equipment_check_sync_registrar.dart`**:
   - Implement `static void registerSyncHandlers(SyncQueueManager manager, EquipmentCheckRepository repository)`.
   - Register handlers for syncing equipment check records (upsert operations).
3. **Update `lib/core/init/app_initializer.dart`**:
   - Open necessary Hive boxes for equipment checks.
   - Instantiate `HiveCacheRepository<EquipmentCheckDto>`, `EquipmentCheckRemoteDataSourceImpl`, and `EquipmentCheckRepositoryImpl`.
   - Call `EquipmentCheckSyncRegistrar.registerSyncHandlers(syncQueueManager, equipmentCheckRepository);`.
   - Update `AppServices` to include `EquipmentCheckRepository` and expose it.
4. **Update `lib/app/router.dart`**:
   - Pass `appServices!.equipmentCheckRepository` to the equipment check routes defined in Substep 12.1.

**Acceptance Criteria:**
- `lib/features/equipment/` no longer exists and project compiles (`flutter analyze` passes).
- `AppInitializer` correctly boots the Equipment Check data layer.
- `EquipmentCheckSyncRegistrar` is registered.
- The UI can consume `appServices!.equipmentCheckRepository` without errors.
