# STEP-55.9 Findings: Data Bucket and Timeline Cohesion

## 1. Inspected State and Trace
- **Branch:** `step-0055-cohesive-ui-rebuild` (app, docs, prompts)
- **Traceability Ledger:** Traces `FC-54.9-001` through `FC-54.9-010` from `mine-flow-STEP-54.5-54.8-FINDINGS-LEDGER.json`, the STEP-54 Master Spec §4.8, and `Upcoming Prompts/mine-flow-STEP-55.9-PROMPT.md`.
- **Scope:** Complete migration of Data Bucket routes to authoritative GoRouter paths (`/tools/data-bucket/upload`, `/tools/data-bucket/:id`), migrating upload form to `AppResponsiveSheet(mode: AppResponsiveSheetMode.form)` with D4 dirty dismiss guards and explicit upload cancellation (`Batalkan Unggahan`), preserving retry file bytes, converting file detail to route-backed responsive inspector (`AppResponsiveSheetMode.readOnlyInspector`) with cold fetching by `:id` and explicit footer actions (`Buka di Google Drive`, `Hapus Berkas`), preserving Work Timeline as strictly read-only and report-free, and replacing legacy Material FAB/InkWell with ForUI/shared controls (`FButton`, `FTappable`, `AppCalendarDialog`).

---

## 2. Changes and Implementation Matrix

| Finding ID | Area & Issue | Treatment & Implemented Solution | Files Modified / Added |
| :--- | :--- | :--- | :--- |
| **`FC-54.9-001`** | Route Authority & List Retention: Data Bucket pushed via `MaterialPageRoute`, dropping router state and breaking deep links. | Replaced `Navigator.push(MaterialPageRoute)` with authoritative GoRouter routes `context.push(AppRoutes.dataBucketUpload)` and `context.push(AppRoutes.dataBucketFileDetail(file.id))`. Configured non-opaque custom transition pages so list context, active search, filter chips, and scroll position remain mounted beneath. | [`lib/app/router.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/lib/app/router.dart)<br>[`lib/features/data_bucket/presentation/pages/data_bucket_list_page.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/lib/features/data_bucket/presentation/pages/data_bucket_list_page.dart) |
| **`FC-54.9-002`** | Upload Sheet & Dirty Dismiss (D4): Upload screen was full `FScaffold` lacking D4 dirty intercept. | Migrated to `AppResponsiveSheet(mode: AppResponsiveSheetMode.form)` with single scroll owner. Dirty state tracked across `_selectedFile`, `_selectedZoneId`, `_acquisitionDate`, and `_notesController`. Intercepts barrier tap and sheet close button via `AppDirtyDismissDialog`. | [`lib/features/data_bucket/presentation/pages/upload_file_page.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/lib/features/data_bucket/presentation/pages/upload_file_page.dart) |
| **`FC-54.9-003`** | Upload Cancellation & Cleanup Truth: No cancellation affordance during long transfers; partial transfers could abandon orphaned files on Google Drive (`RISK-0017`). | Added labelled `Batalkan Unggahan` destructive `FButton` during `UploadUploading`. When `progress > 0`, shows confirmation dialog (`FAlert` + `FDialog`) with `Lanjutkan Unggah` / `Batalkan Unggahan`. Cancelling triggers `DataBucketUploadCubit.cancelUpload()`, which sets `_isCancelled`, aborts Drive stream via `isCancelled` callback in `GoogleDriveService`, executes deterministic cleanup (`_driveService.deleteFile`) if file was already created on Drive, and truthfully reports cleanup status in `UploadCancelled(cleanupFailed, cleanupError)`. | [`lib/core/network/google_drive_service.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/lib/core/network/google_drive_service.dart)<br>[`lib/features/data_bucket/presentation/bloc/data_bucket_upload_cubit.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/lib/features/data_bucket/presentation/bloc/data_bucket_upload_cubit.dart)<br>[`lib/features/data_bucket/presentation/pages/upload_file_page.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/lib/features/data_bucket/presentation/pages/upload_file_page.dart) |
| **`FC-54.9-004`** | Retry Byte Preservation: Upload errors or cancellations previously cleared the selected file, forcing users to re-select from device storage. | Preserved `_selectedFile`, `_fileBytes`, and `_selectedFileSize` on upload error/cancel. The file remains populated and `Upload ke Drive` button remains active, enabling immediate retry without re-picking. | [`lib/features/data_bucket/presentation/pages/upload_file_page.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/lib/features/data_bucket/presentation/pages/upload_file_page.dart) |
| **`FC-54.9-005`** | 50MB Cap & Human-Readable Size: File picker validation must guard against OOM on memory-constrained mobile devices (`RISK-0018`). | Retained 50MB pre-read cap in `_pickFile` before `readAsBytes` is invoked, giving immediate feedback (`File terlalu besar (maks 50 MB).`) and formatted size (e.g. `1.0 MB`). | [`lib/features/data_bucket/presentation/pages/upload_file_page.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/lib/features/data_bucket/presentation/pages/upload_file_page.dart) |
| **`FC-54.9-006`** | Cold Detail Route & ID Resolution: Deep link or refresh on `/tools/data-bucket/:id` dead-ended without in-memory `extra`. | Rebuilt `FileDetailRoute` wrapped in `AppResponsiveSheet`. When `file` is null, fetches record by `fileId` from `DataBucketRepository`. Renders `FCircularProgress` while loading and `AppStatePanel` with Indonesian copy if not found. | [`lib/features/data_bucket/presentation/pages/file_detail_route.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/lib/features/data_bucket/presentation/pages/file_detail_route.dart) |
| **`FC-54.9-007`** | Work Timeline Read-Only Preservation: Must remain strictly read-only; no milestone creation form or route. | Preserved Work Timeline as strictly read-only inspection. No create milestone route, modal, or FAB introduced. | [`lib/features/timeline/presentation/pages/timeline_page.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/lib/features/timeline/presentation/pages/timeline_page.dart) |
| **`FC-54.9-008`** | Report Boundary Adherence: Neither Data Bucket nor Timeline gained reporting actions. | Confirmed no fake report buttons or contextual report dialogs added to Data Bucket or Timeline; both features remain report-free per master spec. | [`lib/features/data_bucket/presentation/pages/data_bucket_list_page.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/lib/features/data_bucket/presentation/pages/data_bucket_list_page.dart)<br>[`lib/features/timeline/presentation/pages/timeline_page.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/lib/features/timeline/presentation/pages/timeline_page.dart) |
| **`FC-54.9-009`** | Material Residual Purge: Actionable Material widgets (`FloatingActionButton`, `InkWell`, raw Material `showDateRangePicker`). | Replaced Data Bucket FAB with `FButton(variant: FButtonVariant.primary)` in header suffixes; replaced Work Timeline `InkWell` in `MilestoneCard` with `FTappable`; replaced raw `showDateRangePicker` with `AppCalendarDialog.showRange`. | [`lib/features/data_bucket/presentation/pages/data_bucket_list_page.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/lib/features/data_bucket/presentation/pages/data_bucket_list_page.dart)<br>[`lib/features/timeline/presentation/widgets/milestone_card.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/lib/features/timeline/presentation/widgets/milestone_card.dart)<br>[`lib/features/timeline/presentation/pages/timeline_page.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/lib/features/timeline/presentation/pages/timeline_page.dart) |
| **`FC-54.9-010`** | File Detail Inspector & Explicit Actions: Detail view was full `FScaffold` obscuring list context. | Migrated `FileDetailPage` to `AppResponsiveSheet(mode: AppResponsiveSheetMode.readOnlyInspector)` (540dp right inspector on Web, bottom sheet on Android). Added explicit sticky footer action buttons: `Buka di Google Drive` and destructive `Hapus Berkas` with `FDialog` confirmation. Retained `PopupMenuButton` in body for backwards compatibility. | [`lib/features/data_bucket/presentation/pages/file_detail_page.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/lib/features/data_bucket/presentation/pages/file_detail_page.dart) |

---

## 3. Verification and Test Results

### 3.1 Automated Test Suites Executed
All 90 tests in Data Bucket and Timeline suites executed cleanly with **0 failures, 0 skips**:

```
00:21 +90: All tests passed!
```

Breakdown:
1. **Data Bucket Upload Cubit Suite (`test/features/data_bucket/presentation/bloc/data_bucket_upload_cubit_test.dart`):**
   - 11 / 11 tests PASS.
   - Tested: Idle state, successful upload emission, offline fallback when Drive unreachable, error emission on upload exception, reset to idle, cancellation before partial transfer, cancellation during partial transfer (stream abort), cancellation after partial transfer with deterministic Drive deletion cleanup (`_driveService.deleteFile`), truthful reporting of cleanup failure in `UploadCancelled`, double-submit guard when already uploading, race-condition Drive file cleanup when `cancelUpload` executes while `files.create` is in flight and returns `driveFileId`, and cancellation after `saveFile` cleaning up both Drive and repository records.
2. **Data Bucket List Page Suite (`test/features/data_bucket/presentation/pages/data_bucket_list_page_test.dart`):**
   - 3 / 3 tests PASS.
   - Tested: `FButton` upload action in header suffixes, zero `FloatingActionButton` instances, absence of report actions, GoRouter navigation to `/tools/data-bucket/upload` with refresh on return, and GoRouter navigation to `AppRoutes.dataBucketFileDetail(id)` on file card tap with refresh on return.
3. **Data Bucket File Detail Page Suite (`test/features/data_bucket/presentation/pages/file_detail_page_test.dart`):**
   - 9 / 9 tests PASS.
   - Tested: `AppResponsiveSheetMode.readOnlyInspector` mode and title/subtitle, explicit footer buttons (`Buka di Google Drive`, `Hapus Berkas`), direct delete confirmation via footer button without popup menu, cancellation of delete dialog, confirmed soft/remote deletion and screen pop, cold detail route fetching file by ID from repository when `extra` is null, cold detail route fallback to `File Tidak Ditemukan` when ID is missing, cold detail route display of `Gagal Memuat File` error panel when repository throws (unauthorized/network error), and `isBusy: true` lock on `AppResponsiveSheet` during in-flight deletion preventing accidental sheet dismissal.
4. **Data Bucket Upload File Page Suite (`test/features/data_bucket/presentation/pages/upload_file_page_test.dart`):**
   - 8 / 8 tests PASS.
   - Tested: Explicit Drive-unconfigured state, 1MB valid file selection, exact 50MB boundary acceptance, 50MB + 1 byte boundary rejection with error message, picker cancellation state retention, `readAsBytes` throw error handling, D4 dirty dismissal intercept with `AppDirtyDismissDialog`, retry byte preservation, and active upload rendering `Batalkan Unggahan` with confirmation dialog.
5. **Timeline Page & Milestone Card Suite (`test/features/timeline/...`):**
   - 9 / 9 tests PASS.
   - Tested: Cubit loading/loaded/empty/error states, summary badge auto-wrapping on phone viewports without horizontal overflow, strict read-only preservation (zero create forms, zero FABs, zero report buttons), desktop layout with `Muat Ulang` refresh action on wide screens, `MilestoneCard` zero Material Card usage, detail rendering, and `FTappable` tap handling.
6. **Data Bucket Repository & BLoC Suite (`test/features/data_bucket/data/...` & `bloc/...`):**
   - 51 / 51 tests PASS.
   - Tested: Model serialization, cache/remote operations, sync registrar, search/zone/type filtering, and staleness stream preservation.

### 3.2 Static Analysis and Linter
- Executed `flutter analyze lib/features/data_bucket lib/features/timeline lib/core/network/google_drive_service.dart lib/core/presentation/widgets/app_interaction_primitives.dart lib/app/router.dart test/features/data_bucket test/features/timeline`:
  ```
  Analyzing 7 items...
  No issues found! (ran in 9.6s)
  ```

---

## 4. Risk Dispositions

### 4.1 RISK-0017 (Real Drive Upload + Cancellation / Orphan Abandonment)
- **Problem:** Without cancellation hooks, aborting an in-progress upload left bytes streaming or abandoned orphan files in Google Drive without deleting them.
- **Implemented Treatment:**
  1. Added chunk-level cancellation check in `GoogleDriveService._createProgressMedia` and post-creation cancellation check in `GoogleDriveService.uploadFile`.
  2. `DataBucketUploadCubit` records `_uploadedDriveFileId` and executes `await _driveService.deleteFile(_uploadedDriveFileId!)` upon cancellation.
  3. If deletion fails, state emits `UploadCancelled(cleanupFailed: true, cleanupError: e.toString())` without pretending cleanup succeeded.
  4. Confirmation dialog warns user (`Sebagian berkas mungkin telah terkirim`) before cancellation when `progress > 0`.
- **Status:** **Mitigated in application code and verified by unit/widget mocks.** Live end-to-end Drive production upload testing remains deferred by Decision D2 due to requiring authenticated Google Service Account secrets in CI.

### 4.2 RISK-0018 (OOM Ceiling on Large Geospatial Files)
- **Problem:** Reading large CAD/GIS files (e.g. multi-gigabyte TIFFs) entirely into RAM would cause out-of-memory crashes on 4GB RAM mobile devices.
- **Implemented Treatment:**
  - Preserved strict 50MB ceiling checked directly on `PlatformFile.size` before reading bytes into memory. Files exceeding 50MB are rejected immediately with user-facing message `File terlalu besar (maks 50 MB).`
- **Status:** **Closed.** Unit and boundary tests verify that 50MB is accepted and 50MB + 1 byte is rejected with zero bytes read.

---

## 5. Unverified Items & Next Handoff
- **Shallow Verification:** Live Google Drive service account token exchange and multi-gigabyte network chunk interruptions on real hardware (relies on mocked Drive boundaries in unit/widget tests per spec instructions: *"Mock Drive externally; never transmit real files in unit tests"*).
- **Next Substep:** STEP-55.10 ("Shell, Dashboard, Notifications, Settings, and Auth").

---

## Residual (55.9) — verify-and-record pass (2026-09-23)

Thin confirmation pass per `mine-flow-STEP-55.9-RESIDUAL-PROMPT.md`. No product code changed; this is verify-and-record. Original code head `89077bf` is an ancestor of current `7633403`.

### R1. Full 55.9 suite re-measured on the current tree
- Command: `flutter test test/features/data_bucket/ test/features/timeline/`
- Result: `00:07 +90: All tests passed!` — **90 passed, 0 failures, 0 unexpected skips**, unchanged from the original §3.1 count.
- Data-bucket/timeline `lib/` files did move since `89077bf`, but only via `c64b0b9` (`style(data-bucket,timeline): dart format re-flow, l10n legacy exemptions`) — a formatting/exemption follow-up, no behavioral change; the suite still passes green on the current head.

### R2. Regression check against the 55.0–55.3 primitive residual lane
- `app_interaction_primitives.dart` was modified (+344/-50 since `89077bf`) by the now-**committed** 55.0/55.1/55.3 residual lane (HEAD `7633403`; the lane is committed, not dirty — the prompt's "uncommitted" precondition has since landed).
- Data-bucket upload-sheet dirty-dismiss (D4) and file-detail inspector geometry ride on that file. Re-asserted via the owning tests on the current tree:
  - `upload_file_page_test.dart` — "D4: intercepts sheet dismissal when form is dirty", "Preserves selected file and bytes on upload retry", "Shows Batalkan Unggahan during active upload and confirms cancel": PASS.
  - `file_detail_page_test.dart` — `AppResponsiveSheetMode.readOnlyInspector` mode, footer actions, `isBusy` lock: PASS.
- **No regression** from the primitive change. Nothing to route back to the primitive owner.

### R3. Report-free + read-only invariants confirmed on the current tree
- `grep -rniE "AppContextualReportDialog|showReportDialog|ReportConfig|contextual.?report" lib/features/data_bucket lib/features/timeline` → **no matches**. No reporting dialog leaked in from the 55.1 reporting-dialog residual lane. Data Bucket and Timeline remain report-free.
- Timeline remains **read-only in the UI**: no `FloatingActionButton`, no create route/FAB, no milestone form in `lib/features/timeline/presentation`. (`createMilestone` exists only in the data/domain plumbing layer, never wired to a presentation affordance — unchanged from original scope.)
- Data Bucket: zero `FloatingActionButton` instances (upload action is an `FButton` in header suffixes), as recorded originally.

### R4. Static analysis
- `flutter analyze lib/features/data_bucket lib/features/timeline lib/core/network/google_drive_service.dart lib/app/router.dart` → `No issues found!` (exit 0).

### R5. Live-Drive deferral — explicit Unverified (carried, not dropped)
- **Unverified:** Live Google Drive service-account token exchange and multi-gigabyte network chunk interruption on real hardware. Deliberately mocked per spec ("mock Drive externally; never transmit real files in unit tests"); requires authenticated Google Service Account secrets in CI (Decision D2). This is **not** a gap in the implementation — cancellation, deterministic orphan cleanup, and truthful cleanup-failure reporting are all covered by unit/widget mocks — but the live round-trip itself is unmeasured.
- Cross-reference **RISK-0017** (`registries/risks.yml`, status: `open`) — real Drive upload cancellation / orphan abandonment behavior; carries this deferral.
- Cross-reference **RISK-0018** (status: `monitoring`) — 50MB OOM cap; the cap itself is verified (50MB accepted, 50MB+1B rejected, zero bytes read), so the code-side mitigation is closed; only real-hardware large-file behavior stays under monitoring.

### Verdict
STEP-index row **55.9 stays Done** as-is, with the live-Drive `Unverified` carried forward. No index edit made (out of scope for this residual). Handoff to the 55.11 close residual.
