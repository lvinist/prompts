# Substep 12.2: Tracking Offline Sync Wiring

**Goal:** Connect the existing tracking sync logic to the global sync manager.

**Context:** 
`lib/features/tracking/data/sync/tracking_sync_registrar.dart` is fully implemented. However, a review of `lib/core/init/app_initializer.dart` shows that `TrackingSyncRegistrar.registerSyncHandlers()` is never called, leaving cut/fill, land clearing, and inventory offline events unprocessed.

**Action Plan:**
1. **Update `lib/core/init/app_initializer.dart`**:
   - Locate section `--- 5. Register feature sync handlers ---`.
   - Call `TrackingSyncRegistrar.registerSyncHandlers(syncQueueManager, trackingRepository);` below the existing `DataBucketSyncRegistrar` call.
   - Ensure imports for `tracking_sync_registrar.dart` are added.

**Acceptance Criteria:**
- `TrackingSyncRegistrar` is actively wired in `AppInitializer`.
- Integration tests confirm that `TrackingRepository` sync operations resolve without errors during initialization.
