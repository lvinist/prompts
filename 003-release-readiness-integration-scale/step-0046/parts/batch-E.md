## Batch E — S17–S19, S24

### F-E01 | P1 | S17 BenchmarkListScreen / S18 BenchmarkFormScreen
**File:** `lib/features/benchmark/domain/entities/benchmark.dart`
**Lines:** 22–34 (entity), `benchmark_form_screen.dart` 252–257, 440–447
**Category:** Selected CRS / UTM zone is never persisted
**Evidence:** The form asks the surveyor to choose a coordinate reference system:
```dart
static const _crsOptions = [
  'UTM Zone 50S', 'UTM Zone 51S', 'UTM Zone 52S',
  'UTM Zone 50N', 'UTM Zone 51N', 'UTM Zone 52N',
];
```
but the `Benchmark` entity has no CRS field at all — `id, bmId, northing, easting, orthoHeight, code, orde, geom, latitude, longitude, ellipsHeight, status`. `form.crsIdentifier` exists only in the transient `BenchmarkFormState`, where it is used to compute `latitude`/`longitude`, and is then discarded on save.

A UTM northing/easting pair is meaningless without its zone: the same numeric pair identifies six different physical locations across the six options offered, and Indonesia genuinely spans zones 46–54. So the stored record cannot be re-projected, cannot be validated, and cannot be safely edited later — reopening a benchmark in the form re-derives lat/lon from whatever CRS the combobox happens to default to, silently rewriting the geographic coordinates of an existing control point. For survey control that field crews set out from, storing coordinates without their datum/zone is the most serious defect in this batch: the data is not recoverable after the fact.
**Severity:** P1

---

### F-E02 | P1 | S24 NotificationListPage
**File:** `lib/features/notifications/presentation/pages/notification_list_page.dart`
**Lines:** 378–385
**Category:** Notification title uses `primaryForeground` on a near-background surface
**Evidence:**
```dart
Text(
  notification.title,
  style: theme.typography.body.sm.copyWith(
    fontWeight: notification.isRead ? FontWeight.normal : FontWeight.w600,
    color: theme.colors.primaryForeground,
  ),
),
```
`primaryForeground` is the token for text drawn **on** a filled primary surface. The card's background is `_bgColor(theme)`, which is `primary.withValues(alpha: 0.1)`, `primary.withValues(alpha: 0.05)`, or plain `background` — all effectively page-background. In ForUI Zinc light mode `primaryForeground` is near-white, so the notification's title renders near-white on a near-white card: the headline of every alert is invisible or barely legible, while the message body directly beneath it (correctly using `mutedForeground`) is readable. This is both a functional failure of the alert surface and a straightforward WCAG 2.1 AA contrast violation against the target in Doc 07 §5.
**Severity:** P1

---

### F-E03 | P1 | S24 NotificationListPage
**File:** `lib/features/notifications/presentation/pages/notification_list_page.dart`
**Lines:** 278–309
**Category:** Critical and warning severities render identically, and neither reads as urgent
**Evidence:**
```dart
Color _iconColor(FThemeData theme) {
  switch (notification.severity) {
    case NotificationSeverity.critical: return theme.colors.primary;
    case NotificationSeverity.warning:  return theme.colors.primary;
    case NotificationSeverity.info:     return theme.colors.mutedForeground;
  }
}
```
All three helpers (`_iconColor`, `_bgColor`, `_borderColor`) map `critical` and `warning` to the same `primary` token; the only difference anywhere is a background alpha of 0.1 vs 0.05, which is imperceptible. `theme.colors.destructive` is available and is used elsewhere on this very screen (the error state, line 172). The consequence: a critical alert — the notification types include `equipmentCheckReminder`, `lowInventory`, `missingAttendance`, `overdueMilestone`, all of which have operational consequences — is visually indistinguishable from an ordinary warning, and both are painted in the app's neutral brand colour rather than an alert colour. The severity field exists in the domain model and is effectively not communicated to the user.
**Severity:** P1

---

### F-E04 | P1 | S17/S19/S24 (shared pattern, three screens)
**File:** `benchmark_list_screen.dart`, `timeline_page.dart`, `notification_list_page.dart`
**Lines:** benchmark 64–77; timeline 91–115; notifications 48–83
**Category:** Screen-level actions vanish entirely on the web/desktop layout
**Evidence:** All three screens follow this shape:
```dart
appBar: MediaQuery.of(context).size.width > 800
    ? null
    : AppBar(title: ..., actions: [ ... ]),
```
Suppressing the mobile header above 800dp is intentional — the app shell provides a header on web. But each screen puts **real, non-duplicated actions** inside `actions:` and loses them with the bar:
- S24 loses `'Tutup Semua'` (Dismiss All), the only bulk-dismiss control on the notification surface.
- S19 loses the `Icons.refresh` reload, the only way to refresh timeline data without changing the date range.
- S18 loses `'Batal'` (Cancel) from the benchmark form (line 158–170).

Doc 07 §4 makes the collapsible sidebar the **supervisor** surface, so these controls disappear precisely for the role most likely to need them, and nothing in the shell replaces them. On web there is no way at all to dismiss all notifications or force a timeline refresh. Raised once as a class because the fix is one pattern (move actions into the page body or into the shell header) applied at three sites.
**Severity:** P1

---

### F-E05 | P1 | S18 BenchmarkFormScreen
**File:** `lib/features/benchmark/presentation/pages/benchmark_form_screen.dart`
**Lines:** 414–430
**Category:** Edit mode silently drops zero and negative elevations
**Evidence:**
```dart
_orthoHeightController.text = form.orthoHeight > 0
    ? form.orthoHeight.toString()
    : '';
_ellipsHeightController.text = form.ellipsHeight > 0
    ? form.ellipsHeight.toString()
    : '';
```
`orthoHeight` is documented in the entity as "Orthometric height (elevation above geoid) in metres" and `ellipsHeight` as height above the ellipsoid. Both are legitimately **negative or zero** — an ellipsoidal height below the ellipsoid is routine in Indonesia (geoid separation there is negative over much of the archipelago), and a benchmark at sea level is 0. The `> 0` guard blanks those fields when the record is opened for editing. The user sees an empty elevation box on a benchmark that has one; because the controller listeners only fire on a parseable value (F-E06), the blank field does not clear the bloc value, so the displayed form and the stored record disagree with no warning. If the user does type over it, the original elevation is gone. The same guard is applied to `northing`/`easting`, which is less dangerous in southern-hemisphere UTM (false northing keeps them positive) but is still wrong in principle.
**Severity:** P1

---

### F-E06 | P1 | S18 BenchmarkFormScreen
**File:** `lib/features/benchmark/presentation/pages/benchmark_form_screen.dart`
**Lines:** 73–99, 392–400
**Category:** No validation on a survey-control form; unparseable coordinates silently discarded
**Evidence:** There is no `Form`, no `GlobalKey<FormState>`, no validator on any field, and the submit button has no guard whatsoever:
```dart
FButton(
  onPress: () => context.read<BenchmarkBloc>().add(const SubmitBenchmark()),
  child: Text(isEditing ? 'Simpan' : 'Tambah Benchmark'),
),
```
Every numeric listener follows the discard-on-failure pattern:
```dart
_northingController.addListener(() {
  final parsed = double.tryParse(_northingController.text);
  if (parsed != null) {
    context.read<BenchmarkBloc>().add(FormNorthingChanged(parsed));
  }
});
```
So a benchmark can be saved with a blank `bmId`, coordinates of 0/0, and no elevation; and if the user clears or mistypes a coordinate the bloc keeps the previous value while the field shows something else. There is also no in-flight guard on the submit button, so a double-tap on a slow sync dispatches `SubmitBenchmark` twice. A control point with a wrong or zero coordinate is worse than a missing one: crews will set out from it. Note this is the same silent-discard idiom found in `InventoryItemEntryScreen`, so it is a shared pattern rather than a one-off.
**Severity:** P1

---

### F-E07 | P1 | S17 BenchmarkListScreen
**File:** `lib/features/benchmark/presentation/pages/benchmark_list_screen.dart`
**Lines:** 89–93
**Category:** Report button requests the wrong report, with the mismatch admitted in a comment
**Evidence:**
```dart
onPressed: () => context.pushNamed(
  'report-config',
  extra: ReportType
      .inventory, // Or ReportType.cutFill depending on original intent, original had inventory.
),
```
The FAB is labelled `'Buat Laporan Benchmark'` and passes `ReportType.inventory`, whose `displayName` is `'Laporan Inventaris'` and whose data source is the `inventory_items` table. `ReportType` has only `attendance`, `cutFill`, `inventory` — there is no benchmark report type — so this button opens a report configuration screen titled "Konfigurasi Laporan Inventaris" and produces a stock report. The trailing comment shows the author knew the mapping was arbitrary and shipped it anyway. (The same wrong-type pattern exists on other screens' report FABs; this one is filed because it is this screen's own defect.)
**Severity:** P1

---

### F-E08 | P2 | S17 BenchmarkListScreen
**File:** `lib/features/benchmark/presentation/pages/benchmark_list_screen.dart`
**Lines:** 413–435
**Category:** List omits elevation — the primary reason to look up a benchmark
**Evidence:** The card shows `bmId`, then `'N: … E: …'` at two decimals, then optionally `'Kode: … Orde: …'`. `orthoHeight` and `ellipsHeight` are never displayed. A benchmark's height is half of what a control point is *for*: a crew checking a levelling reference needs the elevation, and having to tap into the edit form to read it — an editable form, on a record that should be read-only in the field — invites accidental modification. The 2-decimal (centimetre) coordinate display is appropriate; the omission is the problem, together with there being no read-only detail view anywhere in the feature.
**Severity:** P2

---

### F-E09 | P2 | S17 BenchmarkListScreen
**File:** `lib/features/benchmark/presentation/pages/benchmark_list_screen.dart`
**Lines:** 251–258
**Category:** Success state flashes the empty state before reloading
**Evidence:**
```dart
if (state is BenchmarkSuccess) {
  WidgetsBinding.instance.addPostFrameCallback((_) {
    if (context.mounted) {
      context.read<BenchmarkBloc>().add(const LoadBenchmarks());
    }
  });
  return _emptyState(context, theme);
}
```
After any successful create, edit, or delete the screen renders "Belum ada benchmark" ("No benchmarks yet") for one frame plus the round-trip of the reload it schedules. On a slow device or a cold cache read the user watches their entire benchmark database appear to vanish immediately after saving a record — the most alarming possible feedback for a successful write. Returning the previous list, or a loading indicator, would avoid it.
**Severity:** P2

---

### F-E10 | P2 | S17 BenchmarkListScreen
**File:** `lib/features/benchmark/presentation/pages/benchmark_list_screen.dart`
**Lines:** 402–403, 444–451
**Category:** Delete target is a 20dp icon nested inside the card's own tap handler
**Evidence:** The whole card is a `GestureDetector(onTap: onTap, ...)` that opens the edit form, and the delete affordance is a second `GestureDetector` wrapping a bare `Icon(Icons.delete_outline, size: 20, ...)` inside it. The icon has no padding, so its hit area is roughly 20×20dp — well under the ~44dp minimum for touch, and Doc 07 §2 explicitly calls for "touch targets accessible for field workers using mobile devices". A near-miss lands on the parent card instead and opens the edit form, and a near-hit deletes. Neither `GestureDetector` provides focus, hover, or pressed feedback, so a keyboard user on web cannot reach or see either action. Credit where due: this screen *does* confirm the deletion (lines 358–381), unlike the delete paths on the inventory, equipment, and daily-log screens.
**Severity:** P2

---

### F-E11 | P2 | S18 BenchmarkFormScreen
**File:** `lib/features/benchmark/presentation/pages/benchmark_form_screen.dart`
**Lines:** 262–281, 356–374
**Category:** `TextInputType.number` instead of `numberWithOptions(decimal: true)` on coordinate fields
**Evidence:** All four numeric fields — Northing, Easting, Ortho Height, Ellips Height — declare `keyboardType: TextInputType.number`, while their hints promise decimals (`hint: '0.00'`). On Android `TextInputType.number` raises an integer keypad that may not expose a decimal separator, so a surveyor cannot type `9412345.67` on the device this app targets. Elsewhere in the codebase the correct form is used (`InventoryItemEntryScreen` uses `TextInputType.numberWithOptions(decimal: true)` for quantities), so this is an inconsistency as well as a functional block: the fields that most need sub-metre precision are the ones whose keyboard may refuse to provide it. Worth device confirmation. Uncertain — recommend 46.3 confirmation.
**Severity:** P2

---

### F-E12 | P2 | S18 BenchmarkFormScreen
**File:** `lib/features/benchmark/presentation/pages/benchmark_form_screen.dart`
**Lines:** 152–153, 304–322
**Category:** Computed latitude/longitude presented as placeholder hint text, not as values
**Evidence:**
```dart
final latText = form.computedLatitude?.toStringAsFixed(6) ?? '-';
...
FTextField(
  enabled: false,
  label: const Text('Latitude'),
  hint: latText,
),
```
The auto-computed geographic coordinates are injected into the `hint` slot of a disabled field. A hint is a placeholder: it renders in muted placeholder styling, is not the field's value, is not selectable or copyable, and is not exposed to assistive technology as content. So the derived WGS84 coordinate — the number a user would want to copy into a GPS or a map — looks greyed-out and provisional and cannot be copied. When the computation fails it shows `'-'`, indistinguishable from an empty placeholder, giving no signal that the projection did not resolve.
**Severity:** P2

---

### F-E13 | P2 | S18 BenchmarkFormScreen
**File:** `lib/features/benchmark/presentation/pages/benchmark_form_screen.dart`
**Lines:** 162–169, 119–125
**Category:** "Batal" may not close the form
**Evidence:** The header's cancel button dispatches a bloc event rather than popping:
```dart
FButton(
  variant: FButtonVariant.ghost,
  onPress: () => context.read<BenchmarkBloc>().add(const CancelForm()),
  child: const Text('Batal'),
),
```
The only `Navigator.of(context).pop()` in this file is in the listener branch for `BenchmarkSuccess` (line 124). Unless `CancelForm`'s handler emits `BenchmarkSuccess` — which would be wrong, since it would also fire a success snackbar for a cancellation — pressing Batal leaves the user on the form. Combined with F-E04 (the whole header disappears above 800dp) the web user has no cancel affordance at all and must use browser-back. Uncertain on `CancelForm`'s emission — recommend 46.3 confirmation.
**Severity:** P2

---

### F-E14 | P2 | S19 TimelinePage
**File:** `lib/features/timeline/presentation/pages/timeline_page.dart`
**Lines:** 342–370
**Category:** Empty state promises an action the app does not offer, and often does not render
**Evidence:**
```dart
if (state.milestones.isEmpty && state.progressData.isEmpty)
  ... Text('Belum ada data timeline'),
      Text('Data akan muncul setelah Anda menambahkan\nmilestone dan mencatat progres.'),
```
Two problems. First, the copy tells the user to add milestones, but this screen — and, as far as the routed surface goes, the whole app — provides no create-milestone action: there is no FAB, no header add button, and `MilestoneCard` is display-only. The user is instructed to do something they cannot do. Second, the guard requires **both** collections to be empty, and the block sits at the very end of a `ListView` after the chart and the stat badges. So a site with progress data but no milestones gets three "0" badges and no explanation, and when the message does appear it is below a rendered (empty) chart rather than in place of the content.
**Severity:** P2

---

### F-E15 | P2 | S19 TimelinePage
**File:** `lib/features/timeline/presentation/pages/timeline_page.dart`
**Lines:** 279–299
**Category:** "Berjalan" and "Selesai" stat badges are the same colour
**Evidence:**
```dart
_StatBadge(color: theme.colors.primary, label: 'Berjalan', count: activeMilestones.length),
_StatBadge(color: theme.colors.primary, label: 'Selesai', count: completedMilestones.length),
_StatBadge(color: theme.colors.destructive, label: 'Terlambat', count: overdueMilestones.length),
```
In-progress and completed work share `primary`, so the at-a-glance summary of schedule health collapses to "some blue, some red". The section headings below repeat the same choice (`'Selesai'` in `primary`, `'Aktif'` with no colour), so nothing on the screen visually separates work that is running from work that is done. Same underlying issue as F-E03 on notifications: distinct domain states mapped onto one token.
**Severity:** P2

---

### F-E16 | P2 | S24 NotificationListPage
**File:** `lib/features/notifications/presentation/pages/notification_list_page.dart`
**Lines:** 221–239, 241–245
**Category:** Stagger animation far exceeds the motion budget and races `dispose`
**Evidence:**
```dart
_controller = AnimationController(duration: const Duration(milliseconds: 350), vsync: this);
...
Future.delayed(_kStaggerStep * widget.index, _controller.forward);
```
Doc 07 §5 caps motion at "150-200ms fades". Each card animates for 350ms, and the 40ms-per-index stagger means the tenth notification only starts at 400ms and finishes at 750ms; a 20-item inbox takes about 1.15s to fully appear. On the alert surface — where the user opened the screen specifically to read something — content arrives visibly late. Separately, the `Future.delayed` is never cancelled: `dispose()` disposes the controller (line 243) but a pending callback still calls `forward()` on it, throwing if the user leaves the screen or the list rebuilds within the stagger window. There is also no reduced-motion check, which Doc 07 §5 requires the UI to honour.
**Severity:** P2

---

### F-E17 | P2 | S19 TimelinePage
**File:** `lib/features/timeline/presentation/pages/timeline_page.dart`
**Lines:** 138–139, 62–69
**Category:** Date-range label omits the year and the picker allows a year into the future
**Evidence:**
```dart
dateLabel:
    '${DateFormat('dd/MM').format(_startDate)} - ${DateFormat('dd/MM').format(_endDate)}',
```
The only indication of which period the chart covers is `dd/MM - dd/MM`. A range that spans a year boundary — or any historical range — is ambiguous, and "01/03 - 15/03" gives no way to tell this year's March from last year's. Meanwhile `showDateRangePicker` sets `lastDate: DateTime.now().add(const Duration(days: 365))`, so a user can select a range entirely in the future and get an empty chart with no explanation that they are looking at a period that has not happened. The picker also hardcodes `locale: const Locale('id', 'ID')` rather than following the app's active locale, so it stays Indonesian when the user selects English in Settings.
**Severity:** P2

---

### F-E18 | P2 | S17/S18 (benchmark search + status)
**File:** `lib/features/benchmark/presentation/pages/benchmark_list_screen.dart`
**Lines:** 174–184, 269–306
**Category:** Search cannot find a benchmark by coordinate, and the search field is double-framed
**Evidence:** The filter matches only `bmId`, `code`, and `orde`:
```dart
.where((b) =>
    b.bmId.toLowerCase().contains(query) ||
    b.code.toLowerCase().contains(query) ||
    b.orde.toLowerCase().contains(query))
```
There is no status filter and no way to search by northing/easting, which is how a surveyor in the field actually identifies a point they are standing near. There is also no filter for `status`, so destroyed benchmarks stay mixed in with active ones in the list a crew scrolls. Presentationally, the field is an `FTextField` nested inside a hand-built `Container` with its own `muted.withValues(alpha: 0.3)` fill, `BorderRadius.circular(6)`, and its own leading search icon — so the ForUI field's border renders inside a second, differently-radiused frame, which is why this search box looks unlike every other input in the app.
**Severity:** P2

---

### F-E19 | P3 | S17 BenchmarkListScreen
**File:** `lib/features/benchmark/presentation/pages/benchmark_list_screen.dart`
**Lines:** 472–485
**Category:** Hardcoded hex status colours and an untranslated raw status string
**Evidence:**
```dart
case 'active':    chipColor = const Color(0xFF16A34A); break;
case 'destroyed': chipColor = theme.colors.destructive; break;
case 'replaced':  chipColor = const Color(0xFFCA8A04); break;
```
Two raw hex literals (a green and an amber) sit alongside a correctly-tokenised `destructive`, so two thirds of the status palette bypasses the theme and will not adapt in dark mode or meet the AA contrast the Zinc theme guarantees (Doc 07 §2/§5). The chip also renders `status` verbatim, so the user sees the raw database values `active` / `destroyed` / `replaced` in English on an otherwise Indonesian screen. `status` is a bare `String` on the entity rather than an enum, which is why nothing constrains it to those three values.
**Severity:** P3

---

### F-E20 | P3 | S17–S19, S24 (aggregate)
**File:** all four screens
**Lines:** benchmark list 66–77, 152–165, 361–381; benchmark form 121–133, 140, 158, 285, 461–477; timeline 93–115, 181–193, 236; notifications 47–83, 409–415
**Category:** Residual Material widgets where the design system specifies ForUI
**Evidence:** Recorded as one aggregate row per instruction. Across the batch: Material `AppBar` on all four screens; `FilledButton` / `FilledButton.icon` with hand-rolled `RoundedRectangleBorder(borderRadius: circular(10))` as the error-retry on S17 and S19; `AlertDialog` for the benchmark delete confirmation; `DropdownButtonFormField` with `InputDecoration`/`OutlineInputBorder(circular(8))` for all three comboboxes on S18 (Doc 07 §3 names `FSelect`); bare `SnackBar`s on S18; Material `Divider`, `InkWell`, and `IconButton` throughout. STEP-37 was a dedicated Material purge and STEP-38 worked on appbar consistency, so these are stragglers from those sweeps — the visible effect is that headers, dialogs, and dropdowns change shape and radius as the user moves between these screens and their ForUI siblings.
**Severity:** P3

---

### F-E21 | P3 | S17–S19, S24 (aggregate)
**File:** all four screens
**Lines:** throughout
**Category:** Off-scale radii and spacing
**Evidence:** Doc 07 §2 defines the compact scale (4/8/12/16/20/24/32) and ForUI standard radii. Deviations in this batch: `circular(6)` on the benchmark search container and status chip, `circular(10)` on both retry buttons, `circular(16)` on the icon chips of three error/empty states, `EdgeInsets.symmetric(horizontal: 12, vertical: 10)` inside `_CrsCombobox`, `EdgeInsets.all(12.0)` inside the three `FCard`s on S18, `width: 3` left border and `width: 40/height: 40` icon box on the notification card, and `Duration(milliseconds: 40)`/`350` for motion. S24 is the interesting case: it defines a correct `_kSpacing4/8/12/16` scale in constants and then still hardcodes `circular(16)`, `width: 40`, and `width: 3` — and declares `_kSpacing6` (off-scale) at the very bottom of the file, after its use site. Individually trivial; collectively this is why these screens read as slightly differently proportioned from each other.
**Severity:** P3

---

### F-E22 | P3 | S17–S19, S24 (aggregate)
**File:** all four screens
**Lines:** throughout
**Category:** Hardcoded Indonesian user-facing strings (known debt, RISK-0004)
**Evidence:** All four files are on the `_legacyExemptFiles` list in `tool/check_l10n_baseline.dart` and route every label through a literal `Text('...')` — headers (`'Benchmark DB'`, `'Form Benchmark'`, `'Timeline Pekerjaan'`, `'Notifikasi'`), buttons (`'Tambah Benchmark'`, `'Muat Ulang'`, `'Tutup Semua'`, `'Coba Lagi'`, `'Batal'`), field labels (`'Northing (m)'`, `'Ortho Height (m)'`, `'Kordinat Proyeksi (UTM)'`), empty and error states, and interpolated strings (`'${displayBenchmarks.length} benchmark'`, `'Yakin ingin menghapus ${benchmark.bmId}?'`, `'$label $count'`). Two details for remediation: `_formatTime` in S24 (lines 426–433) builds relative timestamps from hardcoded Indonesian fragments (`'Baru saja'`, `'menit yang lalu'`) rather than a localized date library, and the `_crsOptions` / `_ordeOptions` / status values are hardcoded **data** lists (`'UTM Zone 51S'`, `'1st Order'`, `'active'`) that reach the UI directly, so localizing them touches persisted values and needs a decision rather than an ARB entry.
**Severity:** P3

---

### F-E23 | P3 | S17 BenchmarkListScreen
**File:** `lib/app/router.dart`
**Lines:** 77
**Category:** Declared route constant with no registered `GoRoute`
**Evidence:**
```dart
static const benchmarkForm = '/operations/benchmark-db/form';
```
No `GoRoute` anywhere in `router.dart` registers a `form` child under `benchmark-db` — the only registration is the `benchmark-db` leaf itself (lines 258–265), and the form is reached instead by an imperative `Navigator.of(context).push(MaterialPageRoute(builder: (_) => BenchmarkFormScreen(...)))` at `benchmark_list_screen.dart:347–356`. So the constant is dead, and the form is not URL-addressable: on the web build it cannot be deep-linked, bookmarked, or reloaded, and it is pushed onto the root navigator outside the `StatefulShellRoute`, so the shell's sidebar disappears while editing. `AppRoutes.equipmentCheckForm` and `attendanceForm`, by contrast, are properly registered. Not user-visible as a crash, but it is a routing inconsistency that will bite the deep-link E2E validation already deferred to STEP-45 (RISK-0009).
**Severity:** P3

---
