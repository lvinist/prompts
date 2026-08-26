## Batch C — S09–S12

### F-C01 | P1 | S11 LandClearingSummaryScreen
**File:** `lib/features/tracking/presentation/widgets/clearing_summary_card.dart`
**Lines:** 68-76
**Category:** unit label contradicts value
**Evidence:**
```dart
Expanded(
  child: _StatItem(
    label: 'Total (Ha)',
    value:
        '${(totalPlanArea + totalActualArea).toStringAsFixed(2)} Ha',
    icon: Icons.terrain,
    isBold: true,
  ),
),
```
The card is fed `totalPlanArea` and `totalActualArea` in square metres (see `LandClearingBloc._onLoadRecords`, which folds `r.planArea` / `r.actualArea` raw). The third stat is labelled `Total (Ha)` and suffixed `Ha` but never divides by 10,000 — the widget even declares `totalPlanAreaHa`/`totalActualAreaHa` getters at lines 17-20 that are dead code. A site with 50,000 m² planned and 48,000 m² cleared renders "98000.00 Ha" on the land-clearing summary the supervisor reads first. That is off by four orders of magnitude and reported in the wrong unit; anyone using this figure for progress or contractor payment is reading a number ~10,000× too large.
**Severity:** P1

---

### F-C02 | P1 | S11 LandClearingSummaryScreen
**File:** `lib/features/tracking/presentation/widgets/clearing_summary_card.dart`
**Lines:** 71-72
**Category:** total sums two non-additive columns
**Evidence:**
```dart
value:
    '${(totalPlanArea + totalActualArea).toStringAsFixed(2)} Ha',
```
Separate from the unit error in F-C01, adding plan area to actual area is not a meaningful quantity in any earthworks reporting sense: plan and actual describe *the same* ground, once as target and once as achieved. The correct "total" is either total actual cleared, or a plan-vs-actual variance/percentage. As written, a zone fully cleared exactly to plan reports double its real area, so the headline "total" on this screen always overstates cleared land by roughly 2×, and it disagrees with the two stats printed immediately to its left. The same invalid arithmetic is baked into the entity as `LandClearingRecord.totalArea => planArea + actualArea` (`land_clearing_record.dart:39`) and `totalAreaHa` (line 42), so any other consumer inherits it.
**Severity:** P1

---

### F-C03 | P1 | S11 LandClearingSummaryScreen
**File:** `lib/features/tracking/presentation/pages/land_clearing_list_screen.dart`
**Lines:** 101-109
**Category:** report button generates the wrong report
**Evidence:**
```dart
child: FloatingActionButton(
  heroTag: 'report_land_clearing_btn',
  ...
  onPressed: () =>
      context.pushNamed('report-config', extra: ReportType.cutFill),
  child: const Icon(Icons.picture_as_pdf_outlined),
),
```
The Semantics label one line above says `'Buat Laporan Land Clearing'`, but the extra passed to `report-config` is `ReportType.cutFill` — copy-pasted from S09. A foreman who taps the PDF button on the Land Clearing screen is silently taken into cut/fill report configuration and will produce and distribute a volume report believing it is a land-clearing report. There is no visible cue that the wrong type was selected because the destination screen is driven entirely by this `extra`.
**Severity:** P1

---

### F-C04 | P1 | S09 CutFillListScreen
**File:** `lib/features/tracking/presentation/pages/cut_fill_list_screen.dart`
**Lines:** 253-272
**Category:** hardcoded placeholder written as a real filter value
**Evidence:**
```dart
_buildFilterChip(
  label: _selectedZoneId ?? 'Zona',
  selected: _selectedZoneId != null,
  onSelected: () {
    setState(() {
      _selectedZoneId = _selectedZoneId == null
          ? 'Zona A'
          : null;
    });
    context.read<CutFillBloc>().add(
      LoadCutFillRecordsEvent(
        siteId: widget.siteId,
        zoneId: _selectedZoneId,
        ...
```
The "Zona" filter does not open a zone picker; it toggles the literal string `'Zona A'` into `_selectedZoneId` and sends it to the repository as a real zone id. On any site whose zones are not literally named "Zona A" — and zone ids are UUID-shaped elsewhere in this app (`ZonePicker`/`ZoneCubit`) — the query returns nothing and the screen renders an empty list plus a `0.0 m³` summary. A supervisor cannot distinguish that from "no measurements recorded in this zone", so a hardcoded stub presents itself as authoritative zero volume data. Identical code exists in S11 at `land_clearing_list_screen.dart:252-271`.
**Severity:** P1

---

### F-C05 | P1 | S11 LandClearingSummaryScreen
**File:** `lib/features/tracking/presentation/pages/land_clearing_list_screen.dart`
**Lines:** 252-271
**Category:** hardcoded placeholder written as a real filter value
**Evidence:**
```dart
setState(() {
  _selectedZoneId = _selectedZoneId == null
      ? 'Zona A'
      : null;
});
context.read<LandClearingBloc>().add(
  LoadLandClearingRecordsEvent(
    siteId: widget.siteId,
    zoneId: _selectedZoneId,
```
Same defect as F-C04 on the land-clearing screen: the zone chip hardcodes `'Zona A'` rather than resolving a real zone, so filtering by zone silently produces an empty record list and a zeroed plan/actual summary that looks like genuine "nothing cleared here" data. Reported separately because it is a different screen and file and would be fixed independently.
**Severity:** P1

---

### F-C06 | P1 | S09 CutFillListScreen
**File:** `lib/features/tracking/presentation/pages/cut_fill_list_screen.dart`
**Lines:** 418-422
**Category:** destructive action with no confirmation and no role gate
**Evidence:**
```dart
onDelete: () {
  context.read<CutFillBloc>().add(
    DeleteCutFillRecordEvent(record.id),
  );
},
```
Tapping delete on a card dispatches the delete immediately: no confirmation dialog, no undo, and no check of the acting user's role. The bloc handler (`cut_fill_bloc.dart:230-250`) calls `_repository.deleteCutFillRecord` and, on success, does not emit anything — it just re-dispatches a load — so the user gets no acknowledgement either. Cut/fill volume is the primary survey record this app exists to hold; a mis-tap by any foreman permanently removes a measurement with no prompt. The same pattern is at `land_clearing_list_screen.dart:416-420`.
**Severity:** P1

---

### F-C07 | P1 | S11 LandClearingSummaryScreen
**File:** `lib/features/tracking/presentation/pages/land_clearing_list_screen.dart`
**Lines:** 416-420
**Category:** destructive action with no confirmation and no role gate
**Evidence:**
```dart
onDelete: () {
  context.read<LandClearingBloc>().add(
    DeleteLandClearingRecordEvent(record.id),
  );
},
```
As F-C06, on the land-clearing list: an unconfirmed, unguarded, unacknowledged delete of a clearing record. Listed separately because it is a distinct screen/file fix.
**Severity:** P1

---

### F-C08 | P1 | S10 CutFillFormScreen
**File:** `lib/features/tracking/presentation/pages/cut_fill_form_screen.dart`
**Lines:** 249-280
**Category:** Cut/Fill labels bound to BCM/LCM fields (measurement semantics)
**Evidence:**
```dart
Expanded(
  child: VolumeInputField(
    label: 'Volume Cut',
    unit: 'm³ (BCM)',
    ...
    value: record.bcmVolume,
    onChanged: (value) { ... BcmVolumeChangedEvent(value) ... },
  ),
),
const SizedBox(width: 12),
Expanded(
  child: VolumeInputField(
    label: 'Volume Fill',
    unit: 'm³ (LCM)',
    ...
    value: record.lcmVolume,
```
BCM (bank cubic metres, in-situ) and LCM (loose cubic metres, after swell) are two *measurement bases for the same material*, related by a swell factor; cut and fill are two *different earthwork operations*. This form presents them as if BCM ≡ cut and LCM ≡ fill, so a surveyor who records a cut in loose measure, or a fill in bank measure, has no field to put it in and will enter it in the wrong one. Everything downstream inherits the confusion: `CutFillRecord.netVolume => bcmVolume - lcmVolume` (`cut_fill_record.dart:41`) subtracts loose from bank without any swell factor, and `CutFillBloc._onLoadRecords` (lines 47-58) assigns `totalBcm` to `totalCutM3` and `totalLcm` to `totalFillM3` and calls the difference `totalNetM3`. The "Net Volume" number this screen prints in display type (lines 401-406) is therefore arithmetic on mixed units and is not a valid volume. Uncertain whether the intended model is cut/fill or BCM/LCM — recommend 46.3 confirmation.
**Severity:** P1

---

### F-C09 | P1 | S09 CutFillListScreen
**File:** `lib/features/tracking/presentation/widgets/volume_summary_card.dart`
**Lines:** 43-72
**Category:** summary card conflates BCM and LCM in a single net figure
**Evidence:**
```dart
_StatItem(label: 'Total BCM', value: '${totalCutM3.toStringAsFixed(1)} m³', ...),
_StatItem(label: 'Total LCM', value: '${totalFillM3.toStringAsFixed(1)} m³', ...),
_StatItem(label: netLabel, value: '${totalNetM3.toStringAsFixed(1)} m³', isBold: true, ...),
```
The bold headline stat is `totalNetM3`, which the bloc computes as `totalBcm - totalLcm` (`cut_fill_bloc.dart:47-49`). Subtracting a loose-measure total from a bank-measure total yields a quantity with no physical meaning, yet it is the most visually prominent number on S09 and is labelled `Net Cut` / `Net Fill` — implying it is a cut-versus-fill balance, which it is not. Note also the parameter names (`totalCutM3`, `totalFillM3`) disagree with the labels rendered (`Total BCM`, `Total LCM`), which is how the conflation stays invisible to a reader of either file alone. This is the same class of dimensional error already found in the dashboard cubit, occurring independently here.
**Severity:** P1

---

### F-C10 | P1 | S10 CutFillFormScreen
**File:** `lib/features/tracking/presentation/pages/cut_fill_form_screen.dart`
**Lines:** 307-317
**Category:** existing value not loaded into field on edit
**Evidence:**
```dart
TextField(
  decoration: const InputDecoration(
    hintText: 'Contoh: -2.5 (meter)',
  ),
  onChanged: (text) {
    final parsed = double.tryParse(text);
    context.read<CutFillBloc>().add(
      ElevationChangeChangedEvent(parsed),
    );
  },
),
```
The elevation-change field has no `controller` and no `initialValue`, so when a foreman opens an existing record for edit the field renders blank even though `record.elevationChange` holds a value. The field looks unfilled and optional, inviting the user to leave it empty — but leaving it empty does not clear it either, because `CutFillRecord.copyWith` uses `elevationChange ?? this.elevationChange` and the bloc passes the parsed `null` straight through, so a null can never overwrite a stored number. Net effect: previously recorded elevation change is invisible on the edit screen and cannot be corrected to empty, and if the user types anything the old value is silently replaced by something they entered without seeing what it replaced.
**Severity:** P1

---

### F-C11 | P1 | S10 CutFillFormScreen
**File:** `lib/features/tracking/presentation/pages/cut_fill_form_screen.dart`
**Lines:** 128-156
**Category:** error state retry is a dead end
**Evidence:**
```dart
if (state is CutFillError) {
  return Scaffold(
    ...
      FButton(
        onPress: () {
          context.read<CutFillBloc>().add(
            const SaveCutFillRecordEvent(),
          );
        },
        child: const Text('Coba Lagi'),
      ),
```
`CutFillError` is only reachable from `_onInitializeForm` failing (a save failure sets `errorMessage` on `CutFillFormState` instead). The retry button dispatches `SaveCutFillRecordEvent`, whose handler opens with `if (currentState is! CutFillFormState) return;` — so pressing "Coba Lagi" does literally nothing, emits nothing, and shows no feedback. The screen is a terminal dead end: the only escape is the back gesture, and on a wide layout (`> 800`) there is not even an AppBar back button rendered. The correct retry would re-dispatch `InitializeCutFillFormEvent`. Identical defect in S12 at `land_clearing_entry_screen.dart:135-163`.
**Severity:** P1

---

### F-C12 | P1 | S12 LandClearingEntryScreen
**File:** `lib/features/tracking/presentation/pages/land_clearing_entry_screen.dart`
**Lines:** 151-158
**Category:** error state retry is a dead end
**Evidence:**
```dart
FButton(
  onPress: () {
    context.read<LandClearingBloc>().add(
      const SaveLandClearingRecordEvent(),
    );
  },
  child: const Text('Coba Lagi'),
),
```
As F-C11: `LandClearingError` here means form initialisation failed, and `_onSaveRecord` returns immediately unless the state is already `LandClearingFormState`, so "Coba Lagi" is inert. The foreman sees an error, taps retry, nothing happens, and with `width > 800` there is no AppBar to navigate back from. Filed separately from F-C11 because it is a different screen and file.
**Severity:** P1

---

### F-C13 | P1 | S12 LandClearingEntryScreen
**File:** `lib/features/tracking/presentation/pages/land_clearing_entry_screen.dart`
**Lines:** 310-331
**Category:** free text into a field the backend expects enumerated
**Evidence:**
```dart
CreatableCombobox<String>(
  items: _clearingMethods,
  labelBuilder: (method) => method,
  label: 'Metode Clearing',
  hint: 'Pilih atau tambah metode clearing...',
  initialValue: record.method ?? '',
  selectedItem: record.method,
  ...
  onCreateNew: (value) {
    context.read<LandClearingBloc>().add(
      MethodChangedEvent(value),
    );
  },
),
```
`_clearingMethods` is a fixed three-item list (`'Excavator'`, `'Bulldozer'`, `'Chainsaw'`, lines 78-82), but `onCreateNew` feeds arbitrary user text straight into `record.method` with no normalisation, no trim, and no persistence of the new option. Method is a categorical dimension anyone will later group and report on; free text guarantees `excavator`, `Excavator `, `Exca`, and `Bulldozer + Chainsaw` all coexist as distinct categories, and any backend enum/check constraint on this column rejects the save with only a raw exception string surfaced in a SnackBar. The same combobox is duplicated on the Actual tab (lines 499-520) with its own independent free-text entry into the *same* field.
**Severity:** P1

---

### F-C14 | P1 | S12 LandClearingEntryScreen
**File:** `lib/features/tracking/presentation/pages/land_clearing_entry_screen.dart`
**Lines:** 184-209, 216-293, 405-482
**Category:** Plan and Actual tabs edit the same shared fields
**Evidence:**
```dart
child: DefaultTabController(
  length: 2,
  ...
      Tab(text: 'Rencana (Plan)', ...),
      Tab(text: 'Realisasi (Actual)', ...),
```
with both tabs rendering, independently, the same `record.clearingDate` picker and the same `ZonePicker(selectedZoneId: record.zoneId, ...)` dispatching `ClearingDateChangedEvent` / `ZoneChangedEvent`. Only `planArea` and `actualArea` (and, per F-C13, `method` twice) actually differ between tabs. A supervisor reasonably reads the two tabs as "planned date/zone" versus "actual date/zone" — mining plans routinely slip by days — but changing the date on the Actual tab silently rewrites the date shown on the Plan tab, and vice versa. There is exactly one date and one zone on the record. Users will believe they recorded a plan-versus-actual date variance that the model cannot hold.
**Severity:** P1

---

### F-C15 | P1 | S10 CutFillFormScreen
**File:** `lib/features/tracking/presentation/pages/cut_fill_form_screen.dart`
**Lines:** 178-180, 444-459
**Category:** form declares validation that never runs
**Evidence:**
```dart
child: Form(
  key: _formKey,
  child: Column(
...
  child: FButton(
    key: const Key('save_cut_fill_button'),
    onPress: state.isSaving
        ? null
        : () {
            context.read<CutFillBloc>().add(
              const SaveCutFillRecordEvent(),
            );
          },
```
`_formKey` is created and attached but `_formKey.currentState!.validate()` is never called anywhere in the file, and no field declares a `validator`. Save dispatches unconditionally. Combined with the bloc, which persists whatever is in the record without checks, there is nothing preventing a record with zone unset (`zoneId: ''` from `InitializeCutFillFormEvent`), both volumes at their `0.0` defaults, and no material type from being written as a real measurement. A zero-volume, zone-less cut/fill record then enters the summary totals and the PDF report as legitimate data. The same unused `_formKey` pattern is at `land_clearing_entry_screen.dart:75, 182-183, 622-639`.
**Severity:** P1

---

### F-C16 | P1 | S12 LandClearingEntryScreen
**File:** `lib/features/tracking/presentation/pages/land_clearing_entry_screen.dart`
**Lines:** 75, 182-183, 622-639
**Category:** form declares validation that never runs
**Evidence:**
```dart
final _formKey = GlobalKey<FormState>();
...
body: Form(
  key: _formKey,
...
      child: FButton(
        key: const Key('save_land_clearing_button'),
        onPress: state.isSaving ? null : () { ... SaveLandClearingRecordEvent() ... },
```
As F-C15: the `Form` is decorative, `validate()` is never invoked, and no `AreaInputField` supplies a validator. A clearing record can be saved with `planArea`/`actualArea` still at their `0.0` initial values, `zoneId: ''`, and `method: null`, and it will be counted in the S11 plan/actual totals. Separate entry because it is a different screen and file.
**Severity:** P1

---

### F-C17 | P1 | S10 CutFillFormScreen
**File:** `lib/features/tracking/presentation/pages/cut_fill_form_screen.dart`
**Lines:** 42-55
**Category:** empty attribution written on insert
**Evidence:**
```dart
BlocProvider(
  create: (context) => CutFillBloc(repository: repository)
    ..add(
      InitializeCutFillFormEvent(
        siteId: siteId,
        zoneId: initialZoneId ?? existingRecord?.zoneId ?? '',
        foremanId: foremanId,
        ...
```
`foremanId` arrives here from S09, which received it from `app/router.dart` as the literal `foremanId: ''`. The bloc stores it verbatim as the record's attribution — `measuredBy: event.foremanId` (`cut_fill_bloc.dart:82`) — so every measurement created through this path is persisted with an empty-string surveyor. Nothing on the screen displays or requests the surveyor, so there is no point at which the user could notice or correct it. Cut/fill volumes are the app's core record and become unattributable: no one can be asked to re-verify a suspect number, and any per-foreman report or audit trail is empty. `zoneId` gets the same treatment, defaulting to `''` when no zone is passed. The identical path exists in S12 (`land_clearing_entry_screen.dart:48-54` → `clearedBy: event.foremanId`, `land_clearing_bloc.dart:84`).
**Severity:** P1

---

### F-C18 | P1 | S12 LandClearingEntryScreen
**File:** `lib/features/tracking/presentation/pages/land_clearing_entry_screen.dart`
**Lines:** 46-55
**Category:** empty attribution written on insert
**Evidence:**
```dart
create: (context) => LandClearingBloc(repository: repository)
  ..add(
    InitializeLandClearingFormEvent(
      siteId: siteId,
      zoneId: initialZoneId ?? existingRecord?.zoneId ?? '',
      foremanId: foremanId,
```
As F-C17 on the clearing side: `foremanId` originates as `''` in the router, is passed through S11 untouched, and is written as `clearedBy: event.foremanId` (`land_clearing_bloc.dart:84`). Every land-clearing record created from the tab bar has a blank "cleared by". Filed separately because it is a distinct screen and file.
**Severity:** P1
