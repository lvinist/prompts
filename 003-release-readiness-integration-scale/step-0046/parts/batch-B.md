## Batch B — S05–S08

### F-B01 | P1 | S07 DailyLogListScreen
**File:** `lib/app/router.dart`
**Lines:** 344–350
**Category:** Empty `foremanId` becomes an active filter that hides other users' logs
**Evidence:**
```dart
builder: (BuildContext context, GoRouterState state) =>
    DailyLogListScreen(
      repository: appServices!.dailyLogRepository,
      zoneRepository: appServices!.zoneRepository,
      foremanId: '',
      siteId: defaultSiteId,
    ),
```
That `''` flows through `LoadDailyLogsListEvent` → `DailyLogBloc._onLoadDailyLogsList` → `getDailyLogs(foremanId: '')`, and the repository filter is:
```dart
if (foremanId != null && dto.foremanId != foremanId) return false;
```
An empty string is **not null**, so the filter is active and rejects every record whose `foremanId` is anything other than `''`. Any log written by a real identified foreman — a seeded record, a record synced from another device, or any record created once authentication is wired — is silently excluded from the list. The screen shows the "Belum ada data log harian." empty state and the user concludes their work was lost. The bug is invisible in local testing precisely because logs created through this same screen also carry `''` (see F-B02), so the filter matches them and the list looks correct.
**Severity:** P1

---

### F-B02 | P1 | S08 DailyLogFormScreen
**File:** `lib/features/daily_log/presentation/bloc/daily_log_bloc.dart`
**Lines:** 70–77 (and `daily_log_form_screen.dart` 44–50)
**Category:** Daily logs are persisted with empty author attribution
**Evidence:**
```dart
log ??= DailyLog(
  id: _uuid.v4(),
  siteId: event.siteId,
  foremanId: event.foremanId,   // '' from the router, via S07
  logDate: event.logDate,
  status: LogStatus.draft,
  createdAt: DateTime.now(),
);
```
Every daily log created through the app is written to the backend with `foremanId = ''`. The daily log is the site's formal operational record — it carries the work summary and the K3 (safety) notes — and it is being stored with no author. Once real authentication lands, historical records are unattributable, and the `foremanId` column cannot be used for the role-based filtering the data model provides for. This is the write-side twin of F-B01 and both must be fixed together: fixing only the filter would surface records that still have no author.
**Severity:** P1

---

### F-B03 | P1 | S08 DailyLogFormScreen
**File:** `lib/features/daily_log/presentation/bloc/daily_log_bloc.dart`
**Lines:** 64–68
**Category:** Draft resumption keyed on an empty foreman ID — drafts leak between users
**Evidence:**
```dart
log ??= await _repository.getDraftLogForForeman(
  foremanId: event.foremanId,   // ''
  date: event.logDate,
  siteId: event.siteId,
);
```
`getDraftLogForForeman` delegates to `getDailyLogs(foremanId: '', status: draft)`, so "my draft for today" resolves to "the one draft with an empty author for today". On a shared field tablet — the normal deployment for this app — the second foreman to open the form is handed the first foreman's unsubmitted draft, complete with their summary and safety notes, and any edit overwrites it. There is no confirmation, no indication the content came from someone else, and no way to start a fresh log.
**Severity:** P1

---

### F-B04 | P1 | S05 AttendanceScreen / S06 AttendanceFormPage
**File:** `lib/features/attendance/presentation/pages/attendance_screen.dart`
**Lines:** 48 (and `attendance_form_page.dart` 45, 169–171)
**Category:** Hardcoded site UUID literal duplicated in three places
**Evidence:**
```dart
siteId: initialSiteId ?? '00000000-0000-0000-0000-000000000001',
```
The same raw UUID appears at `attendance_screen.dart:48`, `attendance_form_page.dart:45`, and again inside the roster-seeding call at `attendance_form_page.dart:169–171`. `lib/core/constants/app_constants.dart` already defines `defaultSiteId` for exactly this purpose and the router uses it everywhere else, so these are three copies of a value that is supposed to have one definition. Attendance records are written against whichever literal is in scope; if `defaultSiteId` is ever changed for a second site (the Phase-2 "don't foreclose" path the constant is documented for), attendance silently keeps writing to the old site while every other feature moves, and the mismatch surfaces as attendance data vanishing from the dashboard.
**Severity:** P1

---

### F-B05 | P1 | S06 AttendanceFormPage
**File:** `lib/features/attendance/presentation/pages/attendance_form_page.dart`
**Lines:** 165–181
**Category:** Synthetic crew roster seeded as real attendance records
**Evidence:**
```dart
FButton(
  onPress: () {
    context.read<AttendanceBloc>().add(
      SeedDefaultRosterEvent(
        siteId: state.siteId ?? '00000000-0000-0000-0000-000000000001',
        userIds: List.generate(
          8,
          (i) => 'KRU-${(i + 1).toString().padLeft(3, '0')}',
        ),
      ),
    );
  },
  child: const Text('Muat Daftar Kru Default'),
),
```
The empty state's only call to action generates eight fabricated crew IDs (`KRU-001` … `KRU-008`) and seeds them as attendance rows. These are not real users — they do not correspond to any `UserEntity` — yet the button is presented to the user as "Load default crew list", implying a real roster fetched for the site. The count 8 is arbitrary. Every one of those rows then flows into the dashboard's crew count and any attendance report. A production attendance screen needs to load the actual site roster from the users table; a hardcoded generator is a development fixture that reached the primary user path.
**Severity:** P1

---

### F-B06 | P1 | S07 DailyLogListScreen
**File:** `lib/features/daily_log/presentation/pages/daily_log_list_screen.dart`
**Lines:** 471–475
**Category:** Destructive delete of an operational log, unconfirmed and ungated
**Evidence:**
```dart
onDelete: () {
  context.read<DailyLogBloc>().add(
    DeleteDailyLogEvent(log.id),
  );
},
```
A single tap deletes a daily log with no confirmation dialog, no undo, and no role check — including logs already in `submitted` or `approved` state. The form screen carefully makes submitted logs read-only (`enabled: isDraft` on both text fields, the date picker hidden unless draft), so the code clearly intends approved logs to be immutable; the list screen then lets anyone delete them outright. The safety notes and approval trail go with them. `SettingsPage` demonstrates the confirm-dialog pattern the codebase already knows.
**Severity:** P1

---

### F-B07 | P1 | S07 DailyLogListScreen
**File:** `lib/features/daily_log/presentation/pages/daily_log_list_screen.dart`
**Lines:** 115–119
**Category:** Report button generates the wrong report, with the mismatch acknowledged in a comment
**Evidence:**
```dart
onPressed: () => context.pushNamed(
  'report-config',
  extra: ReportType
      .attendance, // original logic used attendance, keeping it
),
```
The FAB is labelled `'Buat Laporan Log Harian'` ("Create Daily Log Report") and requests `ReportType.attendance`, whose `displayName` is `'Laporan Kehadiran'` and whose data source is the `attendance_records` table. `ReportType` has only three members — `attendance`, `cutFill`, `inventory` — so there is no daily-log report type at all. The user asks for a daily-log report and receives an attendance report with a different title and different data. The trailing comment shows the discrepancy was noticed and deliberately carried forward rather than resolved, which makes it a decision to ship a mislabelled action.
**Severity:** P1

---

### F-B08 | P2 | S05 AttendanceScreen
**File:** `lib/features/attendance/presentation/pages/attendance_screen.dart`
**Lines:** 218–291, 283
**Category:** Attendance list is read-only with no way in — the screen cannot do its stated job
**Evidence:** Every roster row is built as `CrewRosterItem(record: record, readOnly: true)` with no `onStatusChanged` or `onRemarksChanged` callback, and the trailing sliver reserves `SizedBox(height: 80)` with the comment `// Space for bottom save bar` — but no bottom save bar exists on this screen (only `AttendanceFormPage` has one). So the screen dedicates 80dp of empty space to a control that was removed, and a supervisor who wants to correct one person's status must go through the separate "Input Absensi" form which re-loads the whole roster. The dangling spacer and the `readOnly: true` together read as a half-finished migration rather than an intentional read-only view.
**Severity:** P2

---

### F-B09 | P2 | S05 AttendanceScreen
**File:** `lib/features/attendance/presentation/pages/attendance_screen.dart`
**Lines:** 408–448, 413
**Category:** Search clear button never appears, and search is un-debounced
**Evidence:**
```dart
suffixIcon: _searchController.text.isNotEmpty
    ? IconButton(icon: const Icon(Icons.clear, size: 18), ...)
    : null,
...
onChanged: (value) {
  context.read<AttendanceBloc>().add(UpdateSearchQueryEvent(value));
},
```
Two defects in one control. The `suffixIcon` condition reads `_searchController.text`, but `onChanged` only dispatches a BLoC event and never calls `setState`; the `TextField` is built inside `_buildSearchAndFilterRow`, which is reached from `_buildBody` under the outer `BlocConsumer`, so it does rebuild on state emission — but only because of the BLoC round-trip, making the clear button's appearance dependent on the bloc emitting, not on the text. Second, every keystroke dispatches a filter event with no debounce. The identical pair of problems exists on `EquipmentHistoryScreen`, so this is a repeated pattern worth fixing as a class. Uncertain on the exact rebuild timing — recommend 46.3 confirmation.
**Severity:** P2

---

### F-B10 | P2 | S06 AttendanceFormPage
**File:** `lib/features/attendance/presentation/pages/attendance_form_page.dart`
**Lines:** 50–58
**Category:** Success pop fires on any state carrying a success message, including a stale one
**Evidence:**
```dart
if (state is AttendanceLoaded && state.successMessage != null) {
  ScaffoldMessenger.of(context).showSnackBar(...);
  context.pop(true);
}
```
The listener pops the route as soon as *any* `AttendanceLoaded` arrives with a non-null `successMessage` — it is not scoped to the batch-save that just completed. Any subsequent emission that preserves `successMessage` (a `copyWith` that does not clear it — and `AttendanceState` has no `clearSuccess` flag in evidence) would pop again. It also pops immediately after showing a snackbar on the page being destroyed, so the confirmation the user is meant to read is torn down with the route; the parent screen shows nothing in its place. The save feedback is effectively invisible.
**Severity:** P2

---

### F-B11 | P2 | S08 DailyLogFormScreen
**File:** `lib/features/daily_log/presentation/pages/daily_log_form_screen.dart`
**Lines:** 292–299, 320–327
**Category:** Auto-save dispatched on every keystroke with no debounce
**Evidence:**
```dart
onChanged: (text) {
  context.read<DailyLogBloc>().add(SummaryChangedEvent(text));
  context.read<DailyLogBloc>().add(const AutoSaveDraftEvent());
},
```
Both multi-line text fields fire `AutoSaveDraftEvent` on every character, and the summary field is a 4-line free-text box where a foreman types a paragraph — hundreds of writes per log. Each one goes through the repository and, per the offline-first design, potentially onto the sync queue. On a field device this is a battery and bandwidth problem, and it makes `AutoSaveIndicator` flicker between saving and saved continuously so it conveys nothing. The zone and weather selectors (lines 240–247, 256–263) fire the same event, which is appropriate there because those are discrete choices; the text fields need a debounce or a save-on-pause.
**Severity:** P2

---

### F-B12 | P2 | S08 DailyLogFormScreen
**File:** `lib/features/daily_log/presentation/pages/daily_log_form_screen.dart`
**Lines:** 134–141
**Category:** Error-state retry button dispatches the wrong action
**Evidence:**
```dart
if (state is DailyLogError) {
  return Scaffold(
    ...
    FButton(
      onPress: () {
        context.read<DailyLogBloc>().add(const AutoSaveDraftEvent());
      },
      child: const Text('Coba Lagi'),
    ),
```
The screen has failed to load — the bloc is in `DailyLogError`, so there is no `DailyLogFormState` and no `log` to save. "Coba Lagi" ("Try again") dispatches an auto-save of a draft that does not exist in state rather than re-dispatching `InitializeDailyLogFormEvent`. Whatever the handler does with no form state, the one thing the button cannot do is retry the load, so the user is stranded on the error screen with a button that appears broken. The same wrong-retry shape appears in `InventoryItemEntryScreen`'s error state (it dispatches `SaveInventoryItemEvent`), so this is a repeated pattern.
**Severity:** P2

---

### F-B13 | P2 | S08 DailyLogFormScreen
**File:** `lib/features/daily_log/presentation/pages/daily_log_form_screen.dart`
**Lines:** 190–191, 237–249, 253–265, 341
**Category:** Validation covers only the text field, not zone or weather
**Evidence:** `_formKey.currentState!.validate()` is correctly called before `SubmitDailyLogEvent` (line 341) — good, and better than the sibling forms — but only `_summaryController`'s `TextFormField` has a validator. `ZonePicker` and `WeatherSelector` are plain widgets outside the `FormField` system, so a log can be submitted with no operational zone and no weather recorded. Zone is the field STEP-33 specifically reworked into a combobox, and weather is operationally relevant to a mining daily log (it explains lost hours). The `*` marker on "Ringkasan Pekerjaan *" signals to the user that only that one field is required, which is consistent with the code but probably not with intent. Uncertain whether zone/weather are meant to be mandatory — recommend 46.3 confirmation.
**Severity:** P2

---

### F-B14 | P2 | S08 DailyLogFormScreen
**File:** `lib/features/daily_log/presentation/pages/daily_log_form_screen.dart`
**Lines:** 148–168, 153–160
**Category:** Controller text overwritten from state during `build`
**Evidence:**
```dart
if (_summaryController.text != (log.summary ?? '')) {
  _summaryController.value = TextEditingValue(
    text: log.summary ?? '',
    selection: TextSelection.collapsed(offset: (log.summary ?? '').length,),
  );
}
```
This runs inside `build`, so any rebuild where the bloc's `log.summary` lags the controller (entirely possible given the per-keystroke auto-save in F-B11 racing an in-flight repository write) rewrites the field and forces the caret to the end of the text. A foreman editing the middle of a summary paragraph gets the cursor yanked to the end mid-sentence. The same pattern is used for `_notesController` here and for five controllers in `InventoryItemEntryScreen` (lines 205–251), so it is a shared idiom worth fixing once.
**Severity:** P2

---

### F-B15 | P2 | S07 DailyLogListScreen
**File:** `lib/features/daily_log/presentation/pages/daily_log_list_screen.dart`
**Lines:** 212–232
**Category:** Material `FilledButton` with hand-rolled styling in a ForUI screen
**Evidence:** The error state's retry is a Material `FilledButton` with `FilledButton.styleFrom(shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)), padding: EdgeInsets.symmetric(horizontal: 24, vertical: 12))`. The file's own header comment claims "Migrated to ForUI in Substep 30.3", and every other button on the screen is ForUI or a FAB, so this one is a straggler from that migration — with a hand-picked 10dp radius that is not a ForUI standard radius (Doc 07 §2). Identical to the `FilledButton` left behind in `EquipmentHistoryScreen`.
**Severity:** P2

---

### F-B16 | P2 | S05–S08 (aggregate)
**File:** all four screens
**Lines:** attendance 81–119; attendance form 51–66; daily log form 94–107
**Category:** Material `SnackBar` and `AppBar` where the design system specifies ForUI
**Evidence:** All success/error feedback across these four screens goes through `ScaffoldMessenger.of(context).showSnackBar(SnackBar(..., backgroundColor: theme.colors.destructive))`, and S05/S07/S08 use Material `AppBar` while S06 uses `FHeader.nested`. Doc 07 §3/§6 makes ForUI the component vocabulary, and STEP-37/STEP-38 explicitly worked on appbar consistency and Material purging. The visible consequence is a header that changes shape when the user taps "Input Absensi" (Material `AppBar` → `FHeader.nested`), and error messages that render with Material elevation and motion on ForUI Zinc surfaces. Recorded as one aggregate row because the fix is a single sweep, not four screen-local edits.
**Severity:** P2

---

### F-B17 | P3 | S05/S07
**File:** `lib/features/attendance/presentation/pages/attendance_screen.dart`, `lib/features/daily_log/presentation/pages/daily_log_list_screen.dart`
**Lines:** attendance 317, 320, 424–443; daily log 98–101, 194, 214–215, 401
**Category:** Off-scale spacing, radii, and motion durations
**Evidence:** Attendance's date header uses `BorderRadius.circular(12)` with a hand-built `Container` border and the search field sets `contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 14)` plus three `OutlineInputBorder`s at radius 12 with `width: 1.5`; the daily log list uses `BorderRadius.circular(16)` for its icon chips, `circular(10)` on the retry button, and `AnimatedSwitcher(duration: 250ms)`. Doc 07 §2 defines the compact scale as 4/8/12/16/20/24/32 (14 is off it) and §5 caps motion at 150–200ms (250ms is over). Individually trivial; collectively they are why these screens read as slightly differently proportioned from their ForUI siblings.
**Severity:** P3

---

### F-B18 | P3 | S05–S08 (aggregate)
**File:** all four screens
**Lines:** throughout
**Category:** Hardcoded Indonesian user-facing strings (known debt, RISK-0004)
**Evidence:** All four files sit on the `_legacyExemptFiles` list in `tool/check_l10n_baseline.dart` and route every label through a literal `Text('...')` — headers (`'Absensi Kru Lapangan'`, `'Input Absensi Kru'`, `'Riwayat Log Harian'`, `'Log Operasional Harian'`), filter chips (`'Semua Status'`, `'Draft'`, `'Terkirim'`, `'Disetujui'`), empty states, buttons, and interpolated strings such as `'Simpan Absensi (${state.records.length} Kru)'` and `'${state.logs.length} log harian'`. Recorded once per batch per the aggregate instruction. One detail for remediation: the `DateFormat('EEEE, d MMMM yyyy', 'id_ID')` calls on S05/S06/S08 hardcode the `id_ID` locale rather than deriving it from the active `Localizations`, so switching the app to English leaves the dates in Indonesian.
**Severity:** P3

---
