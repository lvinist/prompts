# mine-flow — STEP-8.3: Data Bucket UI Screens & State

> **How to run:** Tell your agent _"run substep 8.3"_ (or _"read and run this file"_).
> A substep is self-contained — it must be executable cold in a fresh chat.

## Context

This is the third substep of **STEP-8 (Data Bucket Integration)**. It builds the **presentation layer** for the Data Bucket feature — the BLoC/Cubit state management, the file browser/list screen with search/filter, the upload form with file picker and metadata fields, and the file detail view.

Substep 8.1 created the data layer (repository, models, datasources) and substep 8.2 created the Google Drive service. This substep wires them together into working UI screens.

## Read these first

- root `.throughstone/local-user.md` — active user's experience level (Level 2) and communication style (Explanatory); if missing, ask the two local-profile questions from `BOOTSTRAP-PROMPT.md` Stage 0, create it, and calibrate explanations/questions to it
- `Code/mine-flow-docs/architecture/03-architecture-overview.md` & `15-native-app-architecture.md` — BLoC/Cubit state management patterns
- `Code/mine-flow-docs/architecture/04-data-model.md` — `GeospatialFile` entity fields (zone, location, acquisition date, etc.)
- `Code/mine-flow-docs/architecture/12-test-strategy.md` — test tiers, coverage priorities
- Existing UI patterns for reference: `lib/features/tracking/presentation/` — follow the same BLoC pattern, widget structure, and routing conventions
- `lib/app/router.dart` — app routing; the Data Bucket screens need routes added here
- The Data Bucket domain entity and repository interface from substep 8.1
- The `GoogleDriveService` API from substep 8.2 (`initialize()`, `uploadFile()`, `isOnline`)

## Scope

**Owns:**

- `lib/features/data_bucket/presentation/bloc/` — file list BLoC, file upload BLoC. **EXTENSIVE REQUIREMENT**: The upload BLoC must handle granular states (uploading, progress percentage, success, error) and communicate these effectively to the UI.
- `lib/features/data_bucket/presentation/pages/` — file browser/list screen, upload form screen, detail view.
- `lib/features/data_bucket/presentation/widgets/` — UI components like file cards, progress indicators, search/filter bars.
- Widget tests for the screens and components.
- **EXTENSIVE REQUIREMENT**: Since we are in STEP 8, you MUST ensure that these screens are properly provided with their dependencies (e.g. `DataBucketRepository`) via a temporary local injection or explain how they are intended to be wired in STEP-10. Do not leave the screens unusable due to missing `BlocProvider` wrappers. Include robust error SnackBars for any exceptions thrown by Drive or Supabase.
- Route additions in `lib/app/router.dart` for the new screens
- Widget tests for form validation and list rendering
- Navigation entry point — a "Data Bucket" nav item in the app's sidebar/drawer

**Does NOT touch:**

- The data layer (substep 8.1) or Drive service (substep 8.2) — they exist and are imported
- SyncQueueManager bindings (substep 8.4)
- Any other feature or core module

## Your task

### 1. Create BLoC/Cubit state management

Create `lib/features/data_bucket/presentation/bloc/`:

**`data_bucket_bloc.dart`** — manages file list state with the following states:

```dart
// States
abstract class DataBucketState {}
class DataBucketInitial extends DataBucketState {}
class DataBucketLoading extends DataBucketState {}
class DataBucketLoaded extends DataBucketState {
  final List<GeospatialFile> files;
  final String? searchQuery;
  final String? filterZoneId;
  final String? filterFileType;
}
class DataBucketError extends DataBucketState {
  final String message;
}
```

Events:

```dart
abstract class DataBucketEvent {}
class LoadFiles extends DataBucketEvent {}
class SearchFiles extends DataBucketEvent { final String query; }
class FilterByZone extends DataBucketEvent { final String? zoneId; }
class FilterByType extends DataBucketEvent { final String? fileType; }
class DeleteFile extends DataBucketEvent { final String fileId; }
class RefreshFiles extends DataBucketEvent {}
```

**`data_bucket_upload_cubit.dart`** — manages single-file upload flow with states:

```dart
// States
abstract class UploadState {}
class UploadIdle extends UploadState {}
class UploadPickingFile extends UploadState {}
class UploadUploading extends UploadState {
  final double progress; // 0.0 to 1.0
  final String fileName;
}
class UploadSuccess extends UploadState {
  final GeospatialFile file;
}
class UploadError extends UploadState {
  final String message;
}
```

The upload Cubit should:

1. Accept a file (from file picker) + metadata fields (zone, coordinates, acquisition date, notes)
2. Call `GoogleDriveService.initialize()` if not initialized
3. Call `GoogleDriveService.isOnline` to check connectivity
4. If online: upload to Drive via `uploadFile()`, then save metadata to Supabase via `DataBucketRepository.saveFile()`
5. If offline: save metadata locally via `DataBucketRepository.saveFile()` (which caches locally and marks for sync)
6. Emit `UploadSuccess` on completion or `UploadError` on failure

### 2. Create screens and pages

**`pages/data_bucket_list_page.dart`** — the main file browser screen:

```
Structure:
┌──────────────────────────────────┐
│  Data Bucket         [+ Upload] │  ← AppBar with upload button
├──────────────────────────────────┤
│  🔍 Search files...              │  ← Search bar (triggers SearchFiles event)
│  [All Types ▼] [All Zones ▼]    │  ← Filter chips/dropdowns
├──────────────────────────────────┤
│  ┌────────────────────────────┐ │
│  │ 📄 survey_plan_01.shp     │ │  ← FileCard widget
│  │ Zone: PIT Rusia           │ │
│  │ 2026-07-15  •  2.4 MB     │ │
│  │ View on Drive →           │ │
│  └────────────────────────────┘ │
│  ┌────────────────────────────┐ │
│  │ 🗺️ topography_section.tiff│ │
│  │ Zone: Soil Bank Sochi     │ │
│  │ 2026-07-10  •  15.8 MB    │ │
│  │ View on Drive →           │ │
│  └────────────────────────────┘ │
│         [Load more...]          │
└──────────────────────────────────┘
```

Key behaviors:

- On init, dispatch `LoadFiles` event
- Empty state: show "No files uploaded yet" with a CTA to upload
- Loading state: show shimmer/skeleton placeholders
- Error state: show error message with retry button
- Each file card shows file name, type icon (based on extension), zone, acquisition date, file size
- "View on Drive" opens the file's `driveLink` in external browser (via `url_launcher` or similar)
- Tapping a file card navigates to the file detail page
- Pull-to-refresh triggers `RefreshFiles`
- Filter chips populate from available zones and file types

**`pages/upload_file_page.dart`** — upload form screen:

```
Structure:
┌──────────────────────────────────┐
│  Upload Geospatial File    [X]  │  ← AppBar with close
├──────────────────────────────────┤
│  📁 Select File                  │  ← Large button that opens file picker
│     (or drag & drop on web)      │     Shows selected file name + size
├──────────────────────────────────┤
│  File metadata:                  │
│  ┌────────────────────────────┐ │
│  │ Zone:  [Dropdown ▼]       │ │  ← Required; populated from zones
│  │ Latitude:  [___________]  │ │  ← Optional; decimal input
│  │ Longitude: [___________]  │ │  ← Optional; decimal input
│  │ Acquisition Date: [📅   ] │ │  ← Optional; date picker
│  │ Notes:                     │ │
│  │ [                        ] │ │  ← Optional; multiline text
│  │ [                        ] │ │
│  └────────────────────────────┘ │
│                                 │
│  [      Upload to Drive       ] │  ← Primary action button
│                                 │  Disabled until file is selected
│                                 │  Shows progress bar during upload
└──────────────────────────────────┘
```

Key behaviors:

- File picker: use `file_picker` package (or existing picker in the project) — allow `.shp`, `.tiff`, `.tif`, `.dxf`, `.dwg`, `.csv`, `.kml`, `.kmz`, `.gpx`, `.pdf`, and any file (for "other")
- Show selected file name and size immediately after picking
- Zone dropdown loads from `Zone` data (reuse existing `ZoneRepository` from STEP-3/7)
- On submit: validate required fields (file selected, zone selected), then call upload Cubit
- Show progress bar during upload (percentage + bytes transferred)
- On success: show success snackbar and navigate back to list page
- On error: show error message with retry option
- If Drive is offline, allow offline mode: "Drive is unreachable. File will be cataloged and uploaded when connectivity returns."

**`pages/file_detail_page.dart`** — file detail view:

```
Structure:
┌──────────────────────────────────┐
│  ← Data Bucket    [⋮ Options]   │  ← AppBar with overflow menu
├──────────────────────────────────┤
│                                  │
│  📄 survey_plan_01.shp           │  ← File icon + name (large)
│                                  │
│  ┌─ Details ─────────────────┐  │
│  │ Type:          Shapefile  │  │
│  │ Size:          2.4 MB     │  │
│  │ Zone:          PIT Rusia  │  │
│  │ Latitude:      -7.1234567 │  │
│  │ Longitude:     112.3456789│  │
│  │ Acquired:      2026-07-15 │  │
│  │ Uploaded:      2026-07-15 │  │
│  │ Uploaded By:   Supervisor │  │
│  └──────────────────────────┘  │
│                                  │
│  [  Open in Google Drive  ️   ]  │  ← Opens driveLink externally
│                                  │
│  Notes:                          │
│  Topography survey of the        │
│  eastern wall of PIT Rusia.      │
│                                  │
└──────────────────────────────────┘
```

Overflow menu options: Delete (with confirmation dialog), Open in Drive.

### 3. Create reusable widgets

**`widgets/file_card.dart`** — card widget used in the list. Shows file icon (based on extension), name, zone, acquisition date, size. Supports tap and swipe-to-delete.

**`widgets/search_bar_widget.dart`** — search bar with debounce (300ms) that fires `SearchFiles` events.

**`widgets/filter_chips.dart`** — row of filter chips/dropdowns for file type and zone.

**`widgets/upload_progress_indicator.dart`** — linear progress bar with percentage/text for active upload.

### 4. Add routes

In `lib/app/router.dart`, add routes for:

- `/data-bucket` → `DataBucketListPage`
- `/data-bucket/upload` → `UploadFilePage`
- `/data-bucket/:id` → `FileDetailPage`

### 5. Add navigation entry

Add a "Data Bucket" item to the app's sidebar/drawer navigation (wherever existing features like Attendance, Equipment Checks, Tracking are listed). Use a folder icon or similar.

## Verification

- **Write widget tests** for:
  - Upload form validation (empty fields show errors, valid fields enable submit)
  - File list rendering (list of files renders correctly, empty state shows placeholder)
  - Search/filter interaction (typing in search bar triggers event after debounce)
  - Upload progress states (idle, uploading with progress, success, error)
- **Name the test files:** `test/features/data_bucket/presentation/pages/data_bucket_list_page_test.dart`, `test/features/data_bucket/presentation/pages/upload_file_page_test.dart`, etc.
- **Run:** `flutter test test/features/data_bucket/`
- **Run timing:** Tests are collected in substep 8.4 for final verification; run them now to verify your work, but they're officially gated in 8.4.

## Keeping the docs true

- If the UI reveals a new concept or domain term (e.g., a specific file categorization), update `architecture/13-glossary.md`.
- If the route structure or navigation pattern adds a significant new surface not captured in `architecture/03-architecture-overview.md`, update the doc.

## Definition of done

- [ ] `DataBucketBloc` and `DataBucketUploadCubit` created with all states and events
- [ ] `DataBucketListPage` created with search, filter, empty/loading/error states, and pull-to-refresh
- [ ] `UploadFilePage` created with file picker, metadata form, validation, progress, and offline mode
- [ ] `FileDetailPage` created with full metadata display, Drive link, and delete option
- [ ] Reusable widgets (`FileCard`, `SearchBarWidget`, `FilterChips`, `UploadProgressIndicator`) created
- [ ] Routes added to `lib/app/router.dart`
- [ ] Navigation entry added to sidebar/drawer
- [ ] Widget tests written for form validation, list rendering, search/filter, and upload states
- [ ] Any architecture doc changes reflected

## Next

When this substep is done, update its status in the STEP-8 PLAN, then run **substep 8.4** — _"run substep 8.4"_ — in a fresh chat. (STEP-8 PLAN: `Upcoming Prompts/mine-flow-STEP-8-PLAN.md`)
