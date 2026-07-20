# STEP-12 PLAN: Complete MVP Functional Wiring & Sync

**Status:** Done
**Branch:** `step-0012-functional-wiring`
**Test Tiers:** Integration (routing, initialization, BLoC provision, sync integration)

## Objective
Wire orphaned UI screens into the application router, register missing offline sync handlers in the `AppInitializer`, create missing sync registrars, and clean up duplicate folders. The codebase has functional domain and UI layers for several features that are completely unreachable from the UI and lack sync initialization. This STEP bridges those gaps.

## Constraints & Rules
- **Do not rewrite existing domain or UI logic** unless necessary for integration. The UI files already exist.
- **Ensure all screens are actually reachable.** Adding a route to `router.dart` is not enough; it must be linked from `DashboardPage`'s Quick Navigation or similar accessible UI element.
- **Offline Sync is mandatory.** Every feature listed below must have a `SyncRegistrar` that is explicitly registered inside `lib/core/init/app_initializer.dart`.
- **Extra Extensive but Concise:** Follow the exact file paths and operations described in the substep prompts. Do not guess.

## Substeps

- [x] **12.1 Router & UI Shell Integration**
      *(Wire Cut/fill, Land clearing, Crew attendance, Daily logging, Inventory, and Equipment check into `router.dart` and `dashboard_page.dart`)*
- [x] **12.2 Tracking Offline Sync Wiring**
      *(Register the existing `TrackingSyncRegistrar` in `AppInitializer`)*
- [x] **12.3 Attendance Wiring & Offline Sync**
      *(Create `AttendanceSyncRegistrar` and register it)*
- [x] **12.4 Daily Logging Initialization & Offline Sync**
      *(Wire `DailyLogRepository` in `AppInitializer`, create `DailyLogSyncRegistrar` and register it)*
- [x] **12.5 Equipment Check Initialization, Sync & Cleanup**
      *(Remove `equipment` folder duplicate in favor of `equipment_check`, wire `EquipmentCheckRepository` in `AppInitializer`, create `EquipmentCheckSyncRegistrar` and register it)*

## Definition of Done
When STEP-12 completes:
1. Every core capability listed in `overview.md` is accessible via the app navigation.
2. Every core capability initializes its data layer successfully in `AppInitializer.dart`.
3. Every core capability is registered with the `SyncQueueManager` via its own `SyncRegistrar`.
4. Integration tests verify the new routes and `AppInitializer` dependency injection.
