# mine-flow — STEP-8.4: Offline Queue & Test Verification

> **How to run:** Tell your agent _"run substep 8.4"_ (or _"read and run this file"_).
> A substep is self-contained — it must be executable cold in a fresh chat.

## Context

This is the fourth and final substep of **STEP-8 (Data Bucket Integration)**. It **integrates the Data Bucket feature with the existing offline sync infrastructure** (`SyncQueueManager`) and then **runs the complete test suite** to verify everything works end-to-end.

Substep 8.1 created the data layer (models, datasources, repository). Substep 8.2 created the Google Drive service. Substep 8.3 created the presentation layer (BLoCs, screens, widgets). This substep:

1. Wires the Data Bucket repository's offline fallback into `SyncQueueManager`
2. Ensures all unit, widget, and integration tests are written and passing
3. Verifies the STEP as a whole meets the definition of done

## Read these first

- root `.throughstone/local-user.md` — active user's experience level (Level 2) and communication style (Explanatory); if missing, ask the two local-profile questions from `BOOTSTRAP-PROMPT.md` Stage 0, create it, and calibrate explanations/questions to it
- `Code/mine-flow-docs/architecture/12-test-strategy.md` — test tiers, coverage priorities, mocking strategy, CI gates
- Existing SyncQueueManager implementation: `lib/core/offline/` — examine the pattern used in other features (e.g., tracking, attendance, equipment checks) for how they register their sync operations
- Existing test patterns: `test/features/tracking/` — follow the same test structure (unit tests for models/repositories, widget tests for screens, mock setup)
- The STEP-8 PLAN (`Upcoming Prompts/mine-flow-STEP-8-PLAN.md`) — final Definition of Done checklist

## Scope

**Owns:**

- `lib/features/data_bucket/data/sync/` — sync registrar that binds the Data Bucket repository's offline operations into `SyncQueueManager`
- Completing any missing unit/widget/integration tests for all previous substeps
- Running the full Data Bucket test suite
- Final verification that the STEP is ready for review

**Does NOT touch:**

- Any code or logic from substeps 8.1, 8.2, or 8.3 (they are complete)
- Any other feature or core module outside Data Bucket

## Your task

### 1. Create SyncQueueManager binding

Create `lib/features/data_bucket/data/sync/` (following the pattern from other features, e.g., `lib/features/tracking/data/sync/`):

**`data_bucket_sync_registrar.dart`** — registers the Data Bucket's offline sync operations with `SyncQueueManager`:

```dart
/// Registers Data Bucket metadata sync operations with the offline queue.
///
/// When a geospatial file's metadata is saved offline (because Drive was
/// unreachable during upload), the save is queued here. On connectivity
/// restoration, the SyncQueueManager flushes pending metadata saves to
/// Supabase.
class DataBucketSyncRegistrar {
  final SyncQueueManager syncQueueManager;
  final DataBucketRepository dataBucketRepository;

  DataBucketSyncRegistrar({
    required this.syncQueueManager,
    required this.dataBucketRepository,
  });

  /// Registers sync handlers for Data Bucket operations.
  /// Must be called during app initialization (alongside other registrars).
  Future<void> register() async {
    // Register a handler for 'data_bucket_metadata_sync' operations
    syncQueueManager.registerHandler(
      operationType: 'data_bucket_metadata_sync',
      handler: _handleMetadataSync,
    );
  }

  Future<SyncResult> _handleMetadataSync(SyncQueueItem item) async {
    try {
      // Parse the pending operation from item.payload
      // Execute the sync (e.g., upsert metadata to Supabase)
      await dataBucketRepository.syncPendingUploads();
      return SyncResult.success();
    } catch (e) {
      return SyncResult.failure(e.toString());
    }
  }
}
```

Follow the exact pattern established by other feature sync registrars (e.g., `TrackingSyncRegistrar` from STEP-7.5) — match the `registerHandler` signature, `SyncResult` type, and `SyncQueueItem` payload format.

### 2. Initialize the registrar

Add `DataBucketSyncRegistrar` initialization to the app's startup flow (wherever other feature registrars are initialized — check `main.dart` or an initialization module):

```dart
// Inside the app initialization sequence:
final dataBucketRegistrar = DataBucketSyncRegistrar(
  syncQueueManager: syncQueueManager,
  dataBucketRepository: getIt<DataBucketRepository>(),
);
await dataBucketRegistrar.register();
```

**EXTENSIVE REQUIREMENT (LESSON FROM STEP 7)**:
In a previous step, Deepseek created a SyncRegistrar but *failed* to actually call `.register()` anywhere in the application code, leaving it as dead code. You MUST ensure that this `DataBucketSyncRegistrar` is actively registered. If there is no global `injection_container.dart` yet, you MUST create a temporary bootstrapper or clearly document exactly how and where it is instantiated so that the integration tests genuinely execute the registered code.

### 3. Complete all tests

Audit the test directory `test/features/data_bucket/` and ensure every test tier from the STEP-8 Test Plan is covered. Create or update any missing tests:

**Unit tests (from substep 8.1):**

- `test/features/data_bucket/data/models/geospatial_file_model_test.dart` — model serialization/deserialization
- `test/features/data_bucket/data/repositories/data_bucket_repository_impl_test.dart` — repository CRUD with offline fallback

**Unit tests (from substep 8.2):**

- `test/core/network/google_drive_service_test.dart` — initialization, upload, error handling, isOnline

**Widget tests (from substep 8.3):**

- `test/features/data_bucket/presentation/pages/data_bucket_list_page_test.dart` — file list rendering, search/filter, empty/loading/error states
- `test/features/data_bucket/presentation/pages/upload_file_page_test.dart` — form validation, upload flow, offline mode
- `test/features/data_bucket/presentation/pages/file_detail_page_test.dart` — detail display, delete action

**Integration tests (this substep):**

- `test/features/data_bucket/data/sync/data_bucket_sync_registrar_test.dart` — verify sync handler registration and execution
- `test/features/data_bucket/data/repositories/data_bucket_repository_sync_test.dart` — end-to-end flow: save offline → queue → sync → verify in remote

**Coverage checklist (per Test Strategy):**

- Happy path: file upload → Drive success → metadata saved → listed
- Empty/missing: no files uploaded, empty search results, missing optional metadata fields
- Error paths: Drive offline → metadata queued locally, Drive auth failure → user-friendly error, invalid file type → validation error
- Edge cases: very large file names, special characters in notes, coordinates at extremes (-90/90 lat, -180/180 lon)
- Offline: metadata enqueued when offline, queue flushed on reconnect, no crash during sync failure

### 4. Run the full test suite

```bash
flutter test test/features/data_bucket/
```

Fix any failures. Aim for all tests passing before proceeding.

Also run the broader test suite to ensure no regressions:

```bash
flutter test
```

Fix any regressions caused by the new code (e.g., route changes in `lib/app/router.dart` could affect navigation tests, new dependencies could affect analysis).

### 5. Verify STEP Definition of Done

Check each item from the STEP-8 PLAN's Definition of Done:

- [x] Substep 8.1: Supabase migration created for `geospatial_files` table; domain & data layers implemented.
- [x] Substep 8.2: Google Drive service implemented with service account auth, upload with progress, and graceful error handling.
- [x] Substep 8.3: Data Bucket UI complete — file list with search/filter, upload form with metadata fields, file detail view.
- [x] Substep 8.4: Offline sync queue bound for metadata; full test suite passes.
- [ ] `flutter test` passes cleanly for data_bucket feature tests.
- [ ] All new code is documented; interface contracts doc updated for Drive boundary if new patterns emerged.
- [ ] STEP review passed; `prompts/STEP-index.md` updated; STEP archived to `prompts/`.

## Verification

- **Run:** `flutter test test/features/data_bucket/` — all tests pass
- **Run:** `flutter test` — full suite passes with no regressions
- **Run:** `flutter analyze` — no new warnings or errors

## Keeping the docs true

- If the sync queue binding reveals a new operation type or integration pattern not captured in `architecture/11-interface-contracts.md`, update that doc.
- If the offline/online strategy for the Data Bucket differs from what's described in the architecture overview or infrastructure docs, update them and bump the Version Log.

## Definition of done

- [ ] `DataBucketSyncRegistrar` created and registered in app startup
- [ ] All unit, widget, and integration tests for the Data Bucket feature are written and passing
- [ ] `flutter test test/features/data_bucket/` passes cleanly
- [ ] `flutter test` (full suite) passes with no regressions
- [ ] `flutter analyze` passes with no new warnings
- [ ] Any architecture doc changes reflected
- [ ] STEP-8 PLAN Definition of Done confirmed complete

## Next

When this substep is done:

1. Update its status in the STEP-8 PLAN.
2. Update `prompts/STEP-index.md` — mark STEP-8 as **Done** and add the substep rows.
3. Gather the STEP-8 files from `Upcoming Prompts/` into a new `prompts/001-mvp/step-0008/` folder.
4. Tell the user the next action: the next `Planned` STEP — **STEP-9: Tier 3 - Reporting, Timeline & Polish** — or a Check-in STEP if one is due. (See `METHOD.md` §10 next-action resolver.)
