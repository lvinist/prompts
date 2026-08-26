## Batch F — S20–S23

### F-F01 | P1 | S23 ReportConfigPage — route caller audit
**File:** `lib/app/router.dart`
**Lines:** 426–442
**Category:** Route dead-end audit — all eight callers verified safe; the fallback is unreachable but the route is orphaned
**Evidence:** The route builds its page from `state.extra` with a bare fallback:
```dart
builder: (BuildContext context, GoRouterState state) {
  final reportType = state.extra as ReportType?;
  if (reportType == null) {
    return const Scaffold(
      body: Center(child: Text('Jenis laporan tidak ditemukan.')),
    );
  }
```
A full grep of `lib/` for `reportConfig`, `'/reports/config'`, and `'report-config'` finds exactly eight call sites, **all of which pass a `ReportType`**:

| Caller | Passes | Correct? |
|---|---|---|
| `attendance_screen.dart:163` | `ReportType.attendance` | yes |
| `cut_fill_list_screen.dart:108` | `ReportType.cutFill` | yes |
| `land_clearing_list_screen.dart:107` | `ReportType.cutFill` | plausible (no land-clearing type exists) |
| `inventory_dashboard_screen.dart:102` | `ReportType.inventory` | yes |
| `data_bucket_list_page.dart:110` | `ReportType.cutFill` | **wrong — see F-F02** |
| `daily_log_list_screen.dart:116` | `ReportType.attendance` | wrong (logged in batch B) |
| `equipment_history_screen.dart:338` | `ReportType.inventory` | wrong (logged in batch D) |
| `benchmark_list_screen.dart:90` | `ReportType.inventory` | wrong (logged in batch E) |

So the null fallback is not reachable from any in-app navigation today — good. The real finding is what that audit exposes: `/reports/config` is a **standalone route outside every `StatefulShellBranch`**, and there is no sidebar or bottom-nav entry for it (`app_shell.dart`'s `_kSidebarSections` has no Reports item; STEP-34 deliberately removed the central Laporan menu). The only way in is a per-feature FAB. Consequences: the page is not reachable at all on a fresh load of `/reports/config` (a bookmark or a shared link hits the fallback text and cannot recover), pushing it outside the shell drops the sidebar on web, and there is no way for a supervisor to reach reporting without first navigating into an unrelated feature screen. A reporting surface with no navigation entry is a discoverability failure for a primary product capability.
**Severity:** P1

---

### F-F02 | P1 | S20 DataBucketListPage
**File:** `lib/features/data_bucket/presentation/pages/data_bucket_list_page.dart`
**Lines:** 101–113
**Category:** Report FAB on a file browser generates an unrelated cut/fill report
**Evidence:**
```dart
Semantics(
  label: 'Buat Laporan Data Bucket',
  button: true,
  child: FloatingActionButton(
    heroTag: 'report_data_bucket_btn',
    ...
    onPressed: () =>
        context.pushNamed('report-config', extra: ReportType.cutFill),
```
The button is announced to screen readers as "Create Data Bucket Report" and opens a screen titled "Konfigurasi Laporan Volume Cut/Fill" that queries the `cut_fill_records` table. There is no data-bucket report type in `ReportType` (only `attendance`, `cutFill`, `inventory`), and a file inventory has nothing to do with earthwork volumes — this is the least defensible of the four mislabelled report FABs because the two domains are entirely unrelated. Either the file browser should not offer a report button, or `ReportType` needs a member for it.
**Severity:** P1

---

### F-F03 | P1 | S22 FileDetailPage — URL-addressable route cannot restore itself
**File:** `lib/app/router.dart`
**Lines:** 178–196
**Category:** Deep-link dead end on the web build
**Evidence:**
```dart
GoRoute(
  path: ':id',
  name: 'data-bucket-detail',
  builder: (BuildContext context, GoRouterState state) {
    final extra = state.extra as Map<String, dynamic>?;
    final file = extra?['file'] as GeospatialFile?;
    if (file == null) {
      return const Scaffold(
        body: Center(child: Text('File tidak ditemukan.')),
      );
    }
```
The route declares an `:id` path parameter and then never reads it — `state.pathParameters['id']` is ignored entirely, and the page is reconstructed purely from an in-memory `GeospatialFile` handed over in `extra`. `extra` does not survive a page reload, a bookmark, a shared link, or browser back/forward after a refresh, because it is not serialised into the URL. On the web build — the supervisor surface per Doc 07 §4, where `/mine-flow-app/staging/#/tools/data-bucket/<uuid>` looks like a perfectly good shareable link — the URL renders "File tidak ditemukan." with no retry, no navigation, and no way back except browser-back. A supervisor who bookmarks a survey file, or emails the link to a colleague, gets a dead page for a file that exists. The fix is available and cheap: the id is already in the path, so the route should fetch by id from `DataBucketRepository` (with `extra` as a fast path) rather than treating the id as decoration. Note that `FileDetailPage` is in practice only ever reached via `Navigator.push` from the list (`data_bucket_list_page.dart:345–353`), which bypasses go_router entirely — so the registered route is effectively write-only, which is how the defect went unnoticed.
**Severity:** P1

---

### F-F04 | P1 | S21 UploadFilePage
**File:** `lib/features/data_bucket/presentation/pages/upload_file_page.dart`
**Lines:** 49–55
**Category:** Silent fallback to a `GoogleDriveService` constructed with empty credentials
**Evidence:**
```dart
final gDrive =
    driveService ??
    GoogleDriveService(
      serviceAccountEmail: '',
      serviceAccountKey: '',
      driveFolderId: '',
    );
```
When no `driveService` is injected, the page builds one with three empty strings instead of failing fast or reading the configured service. The router's upload route (`router.dart:163–177`) passes `extra?['driveService'] as GoogleDriveService?` — i.e. **null** unless a caller supplied one — and the actual in-app caller, `data_bucket_list_page.dart:120–128`, constructs `UploadFilePage(repository:, siteId:)` with no `driveService` at all. So the production path always hits this fallback. The user picks a file, fills in metadata, presses "Upload ke Drive", and the upload fails at the network boundary with whatever `DriveUploadException` an unauthenticated request produces, surfaced as a raw `'Gagal mengunggah file: …'` snackbar. Compare the sibling helpers `_defaultDataBucketRepository()`/`_defaultTimelineRepository()` in the same router, which correctly resolve from `appServices` and throw `UnimplementedError` when unwired — this page should do the same (`appServices?.driveService`) rather than fabricating an unusable client. The `// In STEP-10, this will be wired via the DI container` comment confirms this is unfinished wiring that reached the primary user path.
**Severity:** P1

---

### F-F05 | P1 | S21 UploadFilePage
**File:** `lib/features/data_bucket/presentation/pages/upload_file_page.dart`
**Lines:** 278–296, 158–159
**Category:** Zone marked required but never validated; the label only appears while uploading
**Evidence:**
```dart
if (isUploading)
  Padding(
    padding: const EdgeInsets.only(bottom: 6),
    child: Text('Zona *', ...),
  )
else
  ZonePicker(
    selectedZoneId: _selectedZoneId,
    onZoneSelected: (zoneId) { setState(() { _selectedZoneId = zoneId; }); },
  ),
```
The branches are inverted in effect: the `'Zona *'` label — the only thing marking zone as required — is shown **only during upload**, when the field is gone and it is too late to act; in the editable state the picker appears with no label and no required marker. And `_submitUpload` (line 159) calls `_formKey.currentState!.validate()`, but `ZonePicker` is not a `FormField`, so nothing validates `_selectedZoneId`. A geospatial file can be uploaded with no zone, which makes it unfilterable in the list's zone filter (`_computeFilters` only collects non-null `zoneId`s) and unattributable to a location — for spatial data, the zone is most of its value. There are no other validators in the form either, so `validate()` currently always returns true and the guard is decorative.
**Severity:** P1

---

### F-F06 | P1 | S21 UploadFilePage
**File:** `lib/features/data_bucket/presentation/pages/upload_file_page.dart`
**Lines:** 250–259, 209–232
**Category:** In-flight upload can be abandoned with no cancellation
**Evidence:** The header back button is correctly disabled during upload:
```dart
FButton(
  variant: FButtonVariant.ghost,
  onPress: isUploading ? null : () => Navigator.of(context).pop(),
  child: const Icon(Icons.arrow_back),
),
```
but that is the only exit that is guarded. Android's system back gesture, the web browser's back button, and — above 800dp — the entire header (which is `null` on desktop, so there is no back button at all) all bypass it. There is no `PopScope`/`WillPopScope`, no `onWillPop`, and `DataBucketUploadCubit` exposes no cancel: `uploadFile` runs a `_driveService.uploadFile` with a progress callback and no `CancelToken`. Leaving the page disposes the cubit's provider while the Drive request is still in flight, so the file may or may not land in Drive and may or may not be persisted to the repository, with no record either way and no feedback to the user. On a field connection a large GeoTIFF upload is long enough that this is the normal case, not the edge case. There is also no cancel button offered anywhere during the upload — only a progress bar.
**Severity:** P1

---

### F-F07 | P1 | S20 DataBucketListPage
**File:** `lib/features/data_bucket/presentation/pages/data_bucket_list_page.dart`
**Lines:** 360–364
**Category:** Delete has no role gate, and the swipe path destroys a Drive file behind a single dialog
**Evidence:**
```dart
onDelete: () {
  context.read<DataBucketBloc>().add(
    DeleteFile(file.id),
  );
},
```
`FileCard` wires this to a `Dismissible` (`file_card.dart:66`, `onDismissed: (_) => onDelete?.call()`) with a confirm dialog at line 50 — so a confirmation does exist, better than the inventory/equipment/daily-log delete paths. Two problems remain. First, no role check anywhere: any user, including `crew`, can permanently delete a shared geospatial file. Second, the confirmation copy on the swipe path is just `'Yakin ingin menghapus "${file.fileName}"?'`, which does not say the file is removed **from Google Drive** as well as the database — the detail page's dialog does say that explicitly (`file_detail_page.dart:64–67`), so the more dangerous, easier-to-trigger swipe gesture carries the weaker warning. Deleting a survey deliverable from shared Drive storage is not recoverable from within the app.
**Severity:** P1

---

### F-F08 | P2 | S22 FileDetailPage
**File:** `lib/features/data_bucket/presentation/pages/file_detail_page.dart`
**Lines:** 289–301
**Category:** Failed Drive link opens nothing and reports nothing
**Evidence:**
```dart
final uri = Uri.tryParse(file.driveLink);
if (uri != null) {
  await launchUrl(uri, mode: LaunchMode.externalApplication);
}
```
Two silent-failure paths. `Uri.tryParse` returning null falls through the `if` with no `else`, so a malformed link produces a completely inert tap. And `launchUrl` is called without checking `canLaunchUrl` and without try/catch, so a link that cannot be handled either throws an unhandled `PlatformException` or returns false that nobody reads. Compare `SettingsPage`, which does gate on `canLaunchUrl` and shows an error snackbar. "Buka di Google Drive" is the primary action on this screen — the whole point of the Data Bucket is getting to the file — and when it fails the user gets no indication whatsoever that anything happened.
**Severity:** P2

---

### F-F09 | P2 | S22 FileDetailPage
**File:** `lib/features/data_bucket/presentation/pages/file_detail_page.dart`
**Lines:** 327–349, 179–186
**Category:** File-type colour switch maps seven of nine cases to the same token
**Evidence:**
```dart
case '.shp':  return theme.colors.primary;
case '.tiff': case '.tif': return theme.colors.primary;
case '.dxf':  case '.dwg': return theme.colors.primary;
case '.csv':  return theme.colors.primary;
case '.kml':  case '.kmz': return theme.colors.primary;
case '.gpx':  return theme.colors.primary;
case '.pdf':  return theme.colors.destructive;
```
The file header renders a 64px icon in this colour. Every geospatial type resolves to `primary`, so the switch is an eleven-branch no-op that exists to produce one colour, while `.pdf` — the least significant type in a geospatial bucket — is the only one highlighted, and it is highlighted in the **destructive/error** colour, which reads as "this file is broken". The header comment says STEP-30.4 replaced `Colors.blue/teal/orange/green/purple/indigo/red/grey` with FTheme tokens; the replacement collapsed a deliberate per-type palette into one token without removing the now-pointless branching, and picked a semantically wrong token for the one case that differs.
**Severity:** P2

---

### F-F10 | P2 | S23 ReportConfigPage
**File:** `lib/features/reporting/presentation/widgets/date_range_selector.dart`
**Lines:** 31–35, 44–52
**Category:** Date-range label desynchronises from the actual range on entry and on cancel
**Evidence:**
```dart
_currentRange = widget.initialRange;
_selectedOption = 'Minggu Ini';
```
`initState` hardcodes the displayed option to "Minggu Ini" (This Week) regardless of what `initialRange` actually is. `ReportCubit` initialises `_dateRange = DateRangeFilter.currentWeek()`, so this happens to agree on a first visit — but `setDateRange` persists on the cubit across visits, so returning to the page after choosing "Year-to-Date" shows the dropdown reading "Minggu Ini" while the cubit still holds the YTD range. The same desync happens on cancel: if the user picks "Kustom" and dismisses the picker, the code resets `_selectedOption = 'Minggu Ini'` (line ~78) **without** calling `_updateRange`, so the label claims This Week while the effective range is whatever it was before. The user then generates a PDF over a period different from the one the UI displays, and nothing in the output contradicts them. For an operational report used to reconcile work, a silently wrong period is worse than an obvious error.
**Severity:** P2

---

### F-F11 | P2 | S23 ReportConfigPage
**File:** `lib/features/reporting/presentation/pages/report_config_page.dart`
**Lines:** 122–135, 45–50
**Category:** Zone filter offered as a free-text ID field, only for one report type
**Evidence:**
```dart
if (widget.reportType == ReportType.cutFill) ...[
  Text('ID Zona (Opsional)', ...),
  FTextField(
    control: FTextFieldControl.managed(controller: _zoneController),
    hint: 'Biarkan kosong untuk semua zona',
  ),
],
```
The user is asked to type a raw zone **ID** by hand, with no picker, no validation, and no feedback when the value matches nothing — the listener just forwards the trimmed string to `cubit.setZoneFilter`. A `ZonePicker` widget already exists and is used by the daily-log form and the upload page, so the correct control is available in the codebase. A typo silently produces an empty report rather than an error, which is indistinguishable from "no work in this period". Additionally the field appears only for `cutFill`, so attendance and inventory reports cannot be scoped by zone at all — an asymmetry with no stated rationale.
**Severity:** P2

---

### F-F12 | P2 | S23 ReportConfigPage
**File:** `lib/features/reporting/presentation/pages/report_config_page.dart`
**Lines:** 154–170, 176–223
**Category:** No feedback that a long PDF generation is running beyond a spinner in the button, and no cancel
**Evidence:** The generate button swaps its label for a 20×20 `CircularProgressIndicator` while `state is ReportLoading`, and that is the entire in-flight affordance:
```dart
FButton(
  onPress: isLoading ? null : () => cubit.generateReport(siteId: defaultSiteId),
  child: isLoading
      ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(strokeWidth: 2))
      : Text('Buat Laporan', ...),
),
```
A project-to-date PDF over a full dataset is a slow, non-cancellable operation: there is no progress indication, no estimate, no cancel, and nothing preventing the user from navigating away mid-generation (which discards the result silently, since the cubit dies with the route). The date-range and zone controls also remain fully interactive during generation — only the button is disabled — so a user can change the range while a report for the previous range is being produced, then receive a PDF that does not match the visible configuration.
**Severity:** P2

---

### F-F13 | P2 | S21 UploadFilePage
**File:** `lib/features/data_bucket/presentation/pages/upload_file_page.dart`
**Lines:** 106–142, 219–231
**Category:** No file-size limit, and the retry action re-runs a full upload from a snackbar
**Evidence:** `_pickFile` restricts extensions and passes `withData: true`, which loads the **entire file into memory** as `_fileBytes`, with no size check anywhere before or after:
```dart
final result = await FilePicker.pickFiles(
  type: FileType.custom,
  allowedExtensions: ['shp','tiff','tif','dxf','dwg','csv','kml','kmz','gpx','pdf'],
  withData: true,
);
```
GeoTIFFs and point clouds routinely run to hundreds of megabytes; on a mid-range Android field device this is an out-of-memory crash with no warning, and on web it blocks the isolate while the bytes are read. Nothing communicates a maximum size to the user, and the extension list shown in the picker UI (line 418) omits `.kmz` even though it is accepted. Separately, the error path offers `SnackBarAction(label: 'Coba Lagi', onPressed: _submitUpload)` — a snackbar action that silently re-initiates a full multi-megabyte upload, is easy to hit while reaching for something else, and outlives the visual context of the failure it refers to.
**Severity:** P2

---

### F-F14 | P2 | S20 DataBucketListPage
**File:** `lib/features/data_bucket/presentation/pages/data_bucket_list_page.dart`
**Lines:** 241–245, 61–74
**Category:** `setState` inside a post-frame callback on every load — rebuild loop risk
**Evidence:**
```dart
if (state is DataBucketLoaded) {
  // Compute filters on first load
  WidgetsBinding.instance.addPostFrameCallback((_) {
    _computeFilters(state.files);
  });
```
The comment says "on first load" but there is no guard — this schedules on **every** build where the state is loaded, and `_computeFilters` unconditionally calls `setState`, which triggers another build, which schedules another callback. It converges only because `_availableZones`/`_availableTypes` settle to equal values and the widget stops changing visibly; the callback churn continues regardless. It also means the filter chip row can appear one frame after the list, so the content visibly jumps on load. Deriving `_availableZones`/`_availableTypes` from the state during build (or in the bloc) removes the whole mechanism. Uncertain whether it actually loops indefinitely in practice — recommend 46.3 confirmation.
**Severity:** P2

---

### F-F15 | P2 | S20/S22
**File:** `lib/features/data_bucket/presentation/pages/data_bucket_list_page.dart`, `lib/features/data_bucket/presentation/pages/file_detail_page.dart`
**Lines:** list 345–358; detail 82–107
**Category:** Detail-page delete bypasses the BLoC and reports success it has not verified
**Evidence:** The detail page's delete calls the repository directly from the widget:
```dart
await repository.deleteFile(file.id);
if (context.mounted) {
  ScaffoldMessenger.of(context).showSnackBar(
    SnackBar(content: Text('"${file.fileName}" berhasil dihapus.')),
  );
  Navigator.of(context).pop();
}
```
There is a try/catch here (unlike the equipment-check equivalent), so failures do surface. The problem is architectural: `DataBucketBloc` has a `DeleteFile` event that the list screen uses, and this path sidesteps it, so the bloc's state is stale until the list's `onTap` continuation fires `RefreshFiles` on return. Because the deletion is not part of the bloc lifecycle there is no loading state — the button stays live during the Drive round-trip and can be triggered twice — and the success snackbar is shown on a route that is popped in the same frame, so the confirmation is destroyed as it appears and the user lands back on the list with no feedback.
**Severity:** P2

---

### F-F16 | P2 | S22 FileDetailPage
**File:** `lib/features/data_bucket/presentation/pages/file_detail_page.dart`
**Lines:** 226, 239–240, 247–267
**Category:** Raw internal identifiers shown to the user, in a row that overflows at narrow width
**Evidence:**
```dart
if (file.zoneId != null) _detailRow(context, 'Zona', file.zoneId!),
...
if (file.uploadedBy != null)
  _detailRow(context, 'Diunggah Oleh', file.uploadedBy!),
```
`zoneId` and `uploadedBy` are raw identifiers (a zone UUID/code and a user id), displayed under human labels "Zona" and "Diunggah Oleh" ("Uploaded By") with no resolution to a zone name or a person's name. The user sees a UUID where they expect a colleague's name. Layout-wise, `_detailRow` gives the label a fixed `SizedBox(width: 130)` and the value an `Expanded` — the value wraps safely, but at 360dp with enlarged OS text scaling the 130dp fixed label leaves ~200dp for values like a full MIME type (`application/vnd.google-earth.kml+xml`), and the label itself has no `overflow` handling so "Tanggal Akuisisi" can clip inside its fixed box. Doc 07 §5 requires the UI to respond to OS text scaling.
**Severity:** P2

---

### F-F17 | P3 | S21 UploadFilePage
**File:** `lib/features/data_bucket/presentation/pages/upload_file_page.dart`
**Lines:** 309–324, 144–156
**Category:** Date field built from Material `InputDecorator` with hand-formatted output
**Evidence:** The acquisition-date control is an `InkWell` wrapping a Material `InputDecorator` with an `OutlineInputBorder`, and the date is assembled by string padding:
```dart
'${_acquisitionDate!.year}-${_acquisitionDate!.month.toString().padLeft(2, '0')}-${_acquisitionDate!.day.toString().padLeft(2, '0')}'
```
Doc 07 §3 names ForUI inputs, and `intl`'s `DateFormat` is already a dependency used across the app (attendance, daily log, timeline) — so this is both a component deviation and an unlocalised, hand-rolled ISO format sitting next to an Indonesian label. The same padLeft construction is duplicated twice more in `file_detail_page.dart` (lines 231, 237). `showDatePicker` here also does not pass a locale, unlike the timeline's picker, so the calendar language depends on ambient localizations rather than the app setting.
**Severity:** P3

---

### F-F18 | P3 | S20–S23 (aggregate)
**File:** all four screens
**Lines:** list 82–97, 188, 202, 263, 322; upload 134–139, 212–230, 311–317; detail 40–140, 156–166, 222; report 63–76, 142
**Category:** Residual Material widgets and off-scale radii where the design system specifies ForUI
**Evidence:** Recorded as one aggregate row per instruction. Across the batch: Material `AppBar` + `PopupMenuButton` + `ListTile` + `AlertDialog` on S22; `FilledButton.icon` with `RoundedRectangleBorder(circular(12))` as the primary Drive action on S22; Material `SnackBar` for every outcome on S20/S21/S22; `InputDecorator`/`OutlineInputBorder` on S21; Material `Divider`, `InkWell`, `CircularProgressIndicator`, and `RefreshIndicator` throughout; `BorderRadius.circular(16)` on the empty/error icon chips of S20 (off the ForUI standard radii of Doc 07 §2). Worth noting the batch is unusually *good* on structure — S20 and S21 use `FHeader`, S23 uses `FScaffold` + `FHeader`, and all four define named spacing constants on the 4/8/12/16/24 scale — so these are stragglers from the STEP-37 Material purge rather than an unmigrated screen. The visible effect is that the file-detail screen (Material `AppBar` + overflow menu) looks like a different app from the file list it was pushed from.
**Severity:** P3

---

### F-F19 | P3 | S20–S23 (aggregate)
**File:** all four screens
**Lines:** throughout
**Category:** Hardcoded Indonesian user-facing strings (known debt, RISK-0004)
**Evidence:** All four files sit on the `_legacyExemptFiles` list in `tool/check_l10n_baseline.dart` and route every label through a literal — headers (`'Data Bucket'`, `'Upload File'`, `'Detail File'`, `'Konfigurasi ${reportType.displayName}'`), buttons (`'Upload ke Drive'`, `'Buka di Google Drive'`, `'Buat Laporan'`, `'Bagikan PDF'`, `'Cetak'`, `'Muat Ulang'`, `'Hapus'`, `'Batal'`), empty and error states, validation messages (`'Silakan pilih file terlebih dahulu.'`, `'Gagal membaca file. Silakan coba lagi.'`), and interpolated strings (`'${displayFiles.length} file'`, `'File "${state.file.fileName}" berhasil diunggah!'`). Two details for remediation: `ReportType.displayName` and `DateRangeFilter`'s preset names (`'Minggu Ini'`, `'Bulan Ini'`, `'Year-to-Date'`, `'Project-to-Date'`, `'Kustom'`) are Indonesian strings held in **domain/entity** code rather than the presentation layer, so localizing them means touching the domain model; and those preset names are already mixed-language, with two Indonesian and two English options in the same dropdown.
**Severity:** P3

---
