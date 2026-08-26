## Batch D — S13–S16

### F-D01 | P1 | S13 InventoryDashboardScreen
**File:** `lib/features/tracking/presentation/pages/inventory_dashboard_screen.dart`
**Lines:** 427–431
**Category:** Destructive delete with no confirmation and no role gate
**Evidence:**
```dart
onDelete: () {
  context.read<InventoryBloc>().add(
    DeleteInventoryItemEvent(item.id),
  );
},
```
Tapping delete on an inventory card dispatches the deletion immediately — no `showDialog` confirmation, no undo, no role check, and no snackbar acknowledging what was removed. Compare `SettingsPage`, which does gate its logout behind a confirm dialog, so the codebase clearly knows the pattern. Inventory rows are stock records for a live site; a mis-tap on a dense two-column grid of cards permanently removes one with no recovery path and no record of who did it. Doc `overview.md` distinguishes supervisor/foreman/crew, and destructive stock mutation is exactly the kind of action that should be supervisor-only.
**Severity:** P1

---

### F-D02 | P1 | S15 EquipmentHistoryScreen
**File:** `lib/features/equipment_check/presentation/pages/equipment_history_screen.dart`
**Lines:** 307–314
**Category:** Destructive delete of a safety inspection record, unconfirmed and ungated
**Evidence:**
```dart
onDelete: () async {
  await widget.repository.deleteEquipmentCheck(
    check.id,
  );
  if (context.mounted) {
    _onFilterChanged(context);
  }
},
```
Worse than F-D01 on two counts. First, an equipment SOP inspection is a **safety record** — the evidence that a GNSS unit, total station, or drone was verified fit for work — and it is deleted on a single tap with no confirmation and no role check. Second, this call bypasses the BLoC entirely and hits `widget.repository` directly from the widget layer, so the deletion is invisible to `EquipmentCheckBloc`: there is no loading state, and a thrown exception is completely unhandled (no try/catch, no error state, no snackbar). A failed delete silently appears to succeed because `_onFilterChanged` simply reloads and the row is still there, which reads to the user as a broken button rather than a failure.
**Severity:** P1

---

### F-D03 | P1 | S16 EquipmentCheckFormScreen
**File:** `lib/features/equipment_check/presentation/pages/equipment_check_form_screen.dart`
**Lines:** 32–33, and `lib/app/router.dart` 376–380
**Category:** SOP checklist defaults every item to PASSED
**Evidence:** `EquipmentCheckBloc.getDefaultChecklist` (`equipment_check_bloc.dart:29–50+`) constructs every `CheckItem` with `isPassed: true`:
```dart
CheckItem(id: 'gnss_battery', label: 'Level Baterai & Catu Daya', isPassed: true),
CheckItem(id: 'gnss_antenna', label: 'Koneksi Antena & Kabel RTK', isPassed: true),
```
and the submit handler (`_onSubmitEquipmentCheck`, line 206) writes the state as-is with no requirement that any item was actually touched. A foreman can open the form and hit "Simpan Inspeksi SOP (5/5 Lolos)" without inspecting anything, and the stored record is indistinguishable from a genuine full pass. A safety checklist must start in an un-answered state and require an explicit per-item verdict; pre-ticking every box inverts the control's entire purpose and makes the resulting audit trail worthless. This is the most serious finding in the batch because it produces confidently wrong safety data rather than merely failing.
**Severity:** P1

---

### F-D04 | P1 | S16 EquipmentCheckFormScreen
**File:** `lib/features/equipment_check/presentation/pages/equipment_check_form_screen.dart`
**Lines:** 173–181, 237–257
**Category:** No validation — serial number is optional, so an inspection can be filed against no equipment
**Evidence:** The serial-number `TextField` has no validator, the screen has no `Form`/`GlobalKey<FormState>` at all, and the submit button is gated only on `loadedState.isSubmitting`:
```dart
onPress: loadedState.isSubmitting
    ? null
    : () => bloc.add(const SubmitEquipmentCheckEvent()),
```
`EquipmentCheck.serialNumber` is nullable and `_onSubmitEquipmentCheck` performs no checks before calling `repository.saveEquipmentCheck`. The result is a persisted inspection record that does not identify which physical unit was inspected — unusable for the fleet-history purpose the screen exists to serve, and it will surface in `EquipmentHistoryScreen`'s search (which matches on `check.serialNumber`) as an untraceable row.
**Severity:** P1

---

### F-D05 | P1 | S15 EquipmentHistoryScreen
**File:** `lib/features/equipment_check/presentation/pages/equipment_history_screen.dart`
**Lines:** 337–340
**Category:** Wrong report type — equipment screen requests an inventory report
**Evidence:**
```dart
onPressed: () => context.pushNamed(
  'report-config',
  extra: ReportType.inventory,
),
```
The FAB is labelled `'Buat Laporan Inspeksi Peralatan'` ("Create Equipment Inspection Report") but passes `ReportType.inventory`. Per `lib/features/reporting/domain/entities/report_type.dart` there are only three types — `attendance`, `cutFill`, `inventory` — so no equipment report type exists at all, and this button silently generates an inventory report from the `inventory_items` table (`displayName: 'Laporan Inventaris'`). The user asks for an inspection report and receives a stock report with a different title. Either `ReportType` needs an `equipmentCheck` member or the button should not exist; the current state is a labelled action that does something else.
**Severity:** P1

---

### F-D06 | P1 | S14 InventoryItemEntryScreen
**File:** `lib/features/tracking/presentation/bloc/inventory/inventory_bloc.dart`
**Lines:** 184–210
**Category:** Save performs no validation — blank-named, zero-quantity items persist
**Evidence:** `_onSaveItem` goes straight from `isSaving: true` to `_repository.saveInventoryItem(currentState.item)` with no field checks:
```dart
emit(currentState.copyWith(isSaving: true, clearError: true));
try {
  await _repository.saveInventoryItem(currentState.item);
```
The screen wraps its fields in a `Form` with `_formKey` (line 51, 259–260) but never calls `_formKey.currentState!.validate()`, and none of the `FTextField`s declare a validator. The form initialises `quantityOnHand: 0.0` and an empty name, so pressing "Simpan Item Inventori" on an untouched form creates a nameless zero-stock row. The unused `_formKey` makes this look like validation was intended and dropped rather than deliberately omitted.
**Severity:** P1

---

### F-D07 | P2 | S14 InventoryItemEntryScreen
**File:** `lib/features/tracking/presentation/pages/inventory_item_entry_screen.dart`
**Lines:** 94–105
**Category:** Silently discarded numeric input — unparseable quantity keeps the previous value
**Evidence:**
```dart
_quantityController.addListener(() {
  final parsed = double.tryParse(_quantityController.text);
  if (parsed != null) {
    context.read<InventoryBloc>().add(QuantityOnHandChangedEvent(parsed));
  }
});
```
When parsing fails the listener does nothing at all — no error, no state change. So if the user clears the field or types something invalid, the BLoC silently retains the last valid number while the input box shows something different. The user then saves believing the visible (empty or malformed) value is what is stored. Combined with F-D06's absent validation, the field can disagree with the persisted record with no indication. The identical pattern repeats on `_thresholdController` (lines 100–105), so the minimum-stock threshold that drives the low-stock warning banner can silently diverge too. Also note neither field restricts sign: a negative quantity parses fine and is accepted.
**Severity:** P2

---

### F-D08 | P2 | S13 InventoryDashboardScreen
**File:** `lib/features/tracking/presentation/pages/inventory_dashboard_screen.dart`
**Lines:** 447–454
**Category:** Filter chips render as identical buttons — selection state is invisible
**Evidence:**
```dart
Widget _buildFilterChip({
  required String label,
  required bool selected,
  required VoidCallback onSelected,
  required FThemeData theme,
}) {
  return FButton(onPress: onSelected, child: Text(label));
}
```
`selected` and `theme` are accepted and then completely ignored — every chip renders as the same default `FButton` regardless of state. The category filter is the primary way to narrow a long stock list, and the user has no way to see which category is active (or that "Semua" is). Because the callback also toggles, a user can end up filtered to a category with no visual cue, see a short list, and conclude stock is missing. The parameters being present but unused shows the styling was intended and never implemented; contrast `SettingsPage._ThemeOption`, which does switch `FButtonVariant` on selection.
**Severity:** P2

---

### F-D09 | P2 | S15 EquipmentHistoryScreen
**File:** `lib/features/equipment_check/presentation/pages/equipment_history_screen.dart`
**Lines:** 107–132
**Category:** Un-debounced search fires a full repository reload on every keystroke
**Evidence:**
```dart
onChanged: (_) => _onFilterChanged(context),
```
`_onFilterChanged` dispatches `LoadEquipmentHistoryEvent`, which re-queries the repository. There is no debounce, so typing a ten-character serial number issues ten sequential loads; each emits `EquipmentCheckLoading`, so the list flickers to a spinner on every character and the results the user is reading are repeatedly torn down. The codebase already has a debounced pattern (`features/data_bucket/presentation/widgets/*` uses a 300ms debounce), so this is an inconsistency as well as a performance problem — and on a field device on a weak connection it is the difference between usable and unusable search.
**Severity:** P2

---

### F-D10 | P2 | S15 EquipmentHistoryScreen
**File:** `lib/features/equipment_check/presentation/pages/equipment_history_screen.dart`
**Lines:** 113–121
**Category:** Search clear button never appears
**Evidence:**
```dart
suffixIcon: _searchController.text.isNotEmpty
    ? IconButton(icon: const Icon(Icons.clear), ...)
    : null,
```
The conditional reads `_searchController.text`, but nothing rebuilds the widget when the controller's text changes — `onChanged` calls `_onFilterChanged`, which dispatches a BLoC event and never calls `setState`. The `TextField` lives outside the `BlocBuilder` (which starts at line 250), so the surrounding `Column` is not rebuilt by state emissions either. The clear affordance is therefore dead code that appears only if some unrelated rebuild happens to occur, leaving the user to backspace a long serial number by hand.
**Severity:** P2

---

### F-D11 | P2 | S13 InventoryDashboardScreen
**File:** `lib/features/tracking/presentation/pages/inventory_dashboard_screen.dart`
**Lines:** 410–426
**Category:** Stock adjustment result is never reflected in the list
**Evidence:** `onAdjustStock` opens `StockAdjustmentDialog` and dispatches `AdjustStockEvent`, but unlike the two `Navigator.push(...).then(...)` paths on the same screen (lines 124–133 and 399–408) there is no follow-up `LoadInventoryItemsEvent`. Whether the adjusted quantity appears depends entirely on whether `AdjustStockEvent`'s handler re-emits a full `InventoryItemsLoaded`; the two sibling flows on this screen explicitly do not trust that and reload manually. The user adjusts stock, the dialog closes, and the card may still show the old number — the natural next action being to adjust it again. Uncertain — recommend 46.3 confirmation of `AdjustStockEvent`'s emission behaviour.
**Severity:** P2

---

### F-D12 | P2 | S13 InventoryDashboardScreen
**File:** `lib/features/tracking/presentation/pages/inventory_dashboard_screen.dart`
**Lines:** 90–139
**Category:** Two-FAB `Row` can overflow at narrow width
**Evidence:** The `floatingActionButton` slot holds a `Row` containing a circular FAB, a 16dp gap, and a `FloatingActionButton.extended` whose label is `'Tambah Item'`. Flutter positions the FAB slot against the screen edge with a fixed margin and does not constrain a `Row` inside it to the viewport, so at 360dp with enlarged OS text scaling the extended FAB's intrinsic width plus the report FAB can exceed the available space and overflow. Doc 07 §5 requires the UI to respond to OS text scaling, and this is the exact place unbounded intrinsic width bites. The same two-FAB-`Row` construction appears on S15 (lines 326–370), so both screens share the risk.
**Severity:** P2

---

### F-D13 | P2 | S16 EquipmentCheckFormScreen
**File:** `lib/features/equipment_check/presentation/pages/equipment_check_form_screen.dart`
**Lines:** 88–98
**Category:** Material `AppBar` with a primary-coloured bar, contradicting the design system
**Evidence:**
```dart
: AppBar(
    title: Text('Inspeksi SOP Peralatan', ...),
    elevation: 0,
    backgroundColor: theme.colors.primary,
    foregroundColor: theme.colors.primaryForeground,
  ),
```
Doc 07 §3/§6 makes ForUI the component vocabulary and STEP-37/STEP-38 explicitly worked on appbar consistency; sibling screens use `FHeader` (S13 line 72) or a plain `AppBar` with no colour override (S14 lines 175, 256). This screen alone paints a solid primary-colour header, so navigating from the equipment history list into the form changes the header's colour and weight mid-flow. Three different header treatments across four screens in one batch is a visible inconsistency on the app's densest workflow.
**Severity:** P2

---

### F-D14 | P2 | S16 EquipmentCheckFormScreen
**File:** `lib/features/equipment_check/presentation/pages/equipment_check_form_screen.dart`
**Lines:** 173–181, 223–232
**Category:** Material `TextField`/`InputDecoration` where the design system specifies `FTextField`
**Evidence:** Both inputs on this screen are Material `TextField`s with `InputDecoration(labelText:, hintText:, prefixIcon:)`. Doc 07 §3 names `FTextField` and "ForUI outline input fields adhering to compact spacing" as the contract, and S14 uses `FTextField` throughout for the same kind of data entry. The consequence is not merely cosmetic: Material inputs bring their own floating-label behaviour, focus ring, and density that will not match the ForUI Zinc fields the user just used on the previous screen, and they will not follow the design system's radii or border tokens in either theme. Same class of issue on S15's search field (lines 107–130, with a hand-rolled `OutlineInputBorder(borderRadius: 8)`).
**Severity:** P2

---

### F-D15 | P2 | S15 EquipmentHistoryScreen
**File:** `lib/features/equipment_check/presentation/pages/equipment_history_screen.dart`
**Lines:** 140–241, 268–271, 246
**Category:** Material `FilterChip`, `FilledButton`, and `Divider` in a ForUI screen
**Evidence:** Seven Material `FilterChip`s drive the type and status filters, the error state's retry uses Material `FilledButton(onPressed:, ...)`, and a Material `Divider` separates the header. The file's own doc comment claims "Migrated to ForUI in Substep 30.3: ... FilledButton replaced with FIconButton" — the `FilledButton` at line 268 shows that migration was incomplete, so the comment now misdescribes the code. `FilterChip` also carries Material's selected-state fill, which is the one place on this screen where selection *is* visible, creating an odd contrast with S13's invisible chips (F-D08): two screens in the same batch present the same control with opposite affordances.
**Severity:** P2

---

### F-D16 | P2 | S13/S14/S16 (inventory + equipment)
**File:** `lib/features/tracking/presentation/pages/inventory_item_entry_screen.dart`, `lib/features/equipment_check/presentation/pages/equipment_check_form_screen.dart`
**Lines:** inventory 141–154; equipment 102–119
**Category:** Material `SnackBar` used for all success and error feedback
**Evidence:** Both forms report outcomes via `ScaffoldMessenger.of(context).showSnackBar(SnackBar(..., backgroundColor: theme.colors.destructive))`. STEP-37 was dedicated to purging residual Material widgets and `MaterialBanner` specifically, but snackbars were left behind across the app (the same pattern appears in `SettingsPage._showSnackError`). These are the only channel by which a save failure reaches the user, so they matter more than typical chrome: they render with Material elevation and motion inside ForUI surfaces, and the destructive-red fill is applied as a raw background rather than through a semantic ForUI alert component.
**Severity:** P2

---

### F-D17 | P2 | S14 InventoryItemEntryScreen
**File:** `lib/features/tracking/presentation/pages/inventory_item_entry_screen.dart`
**Lines:** 294–316
**Category:** Material `DropdownButtonFormField` inside an `FCard`, with no validator
**Evidence:** The category selector is a Material `DropdownButtonFormField<String>` wrapped in an `FCard` + 12dp `Padding` to make it look like a ForUI control. Doc 07 §3 names `FSelect` for this role. Because it is a `FormField` inside a `Form` whose `validate()` is never called (F-D06), its `validator` slot is also empty, so category is silently optional even though `InventoryBloc.categories` implies a closed set. The visual mismatch is compounded by the unit `DropdownButton` immediately below (lines 354–386), which needed an explicit `Localizations` re-injection workaround to survive inside `FTextField.suffixBuilder` — a strong signal that Material dropdowns are being forced into ForUI containers rather than replaced.
**Severity:** P2

---

### F-D18 | P2 | S14 InventoryItemEntryScreen
**File:** `lib/features/tracking/presentation/pages/inventory_item_entry_screen.dart`
**Lines:** 156–160
**Category:** Timed auto-pop races the user
**Evidence:**
```dart
Future.delayed(const Duration(milliseconds: 600), () {
  if (context.mounted) {
    Navigator.of(context).pop();
  }
});
```
The screen closes itself 600ms after a successful save, on a timer that is never cancelled in `dispose`. If the user has already navigated (back button, or tapping something else in that window) the delayed callback still fires and pops whatever route is now current, removing a screen the user did not ask to leave. Tying navigation to a wall-clock delay rather than to the state transition also means the success snackbar is cut off mid-appearance on slower frames.
**Severity:** P2

---

### F-D19 | P3 | S13/S14 (inventory)
**File:** `lib/features/tracking/presentation/pages/inventory_dashboard_screen.dart`, `lib/features/tracking/presentation/pages/inventory_item_entry_screen.dart`
**Lines:** dashboard 288–298; entry 293, 336, 349, 352
**Category:** Off-scale spacing and radii
**Evidence:** The low-stock banner uses `EdgeInsets.symmetric(horizontal: 14, vertical: 12)` with `BorderRadius.circular(10)`; the entry screen uses `EdgeInsets.all(12.0)` inside `FCard`, `EdgeInsetsDirectional.only(end: 4)`, `EdgeInsets.symmetric(horizontal: 8)` and `BorderRadius.circular(6)`. Doc 07 §2 defines a compact scale (4/8/12/16/20/24/32); 14 is off it, and 10dp/6dp radii are hand-picked rather than ForUI standard radii (§2 "Shape & Elevation"). Minor individually, but they are why the two screens read as slightly differently proportioned from their ForUI siblings.
**Severity:** P3

---

### F-D20 | P3 | S13 InventoryDashboardScreen
**File:** `lib/features/tracking/presentation/pages/inventory_dashboard_screen.dart`
**Lines:** 293, 296
**Category:** Hardcoded alpha values instead of semantic tokens
**Evidence:** `theme.colors.destructive.withAlpha(25)` for the banner fill and `.withAlpha(76)` for its border. The base colour is correctly a theme token, but the two magic alphas (roughly 10% and 30%) are hand-derived and will not necessarily produce a WCAG 2.1 AA compliant surface in dark mode, where `destructive` differs. Doc 07 §5 targets AA contrast "supported out-of-the-box by ForUI Zinc" — deriving custom translucent surfaces steps outside that guarantee for the app's most urgent alert.
**Severity:** P3

---

### F-D21 | P3 | S13 InventoryDashboardScreen
**File:** `lib/features/tracking/presentation/pages/inventory_dashboard_screen.dart`
**Lines:** 84–88
**Category:** Motion duration exceeds the design contract
**Evidence:** `AnimatedSwitcher(duration: const Duration(milliseconds: 250), switchInCurve: Curves.easeOutQuart, ...)`. Doc 07 §5 specifies 150–200ms; 250ms is over. Same class of deviation as the dashboard's 300ms switcher, so a single sweep should settle both rather than fixing them screen by screen.
**Severity:** P3

---

### F-D22 | P3 | S13 InventoryDashboardScreen
**File:** `lib/features/tracking/presentation/pages/inventory_dashboard_screen.dart`
**Lines:** 15–18, 194–214
**Category:** Dead and duplicated layout constants
**Evidence:** `_kSidePaddingWide` is declared as `EdgeInsets.symmetric(horizontal: 32)` and then used only as `_kSidePaddingWide.horizontal / 2` (line 207) to recover the number 32 that is already hardcoded as `sidePad = isWide ? 32.0 : ...` on line 200. `_kBreakMobile`/`_kBreakTablet` (600/900) also coexist with a separate inline `MediaQuery...width >= 800` desktop test on line 65, so the screen has three different breakpoints deciding related things. Harmless at runtime but it makes the responsive behaviour hard to reason about and is why the header appears/disappears at a different width than the grid changes column count.
**Severity:** P3

---

### F-D23 | P3 | S14 InventoryItemEntryScreen
**File:** `lib/features/tracking/presentation/pages/inventory_item_entry_screen.dart`
**Lines:** 58, 82, 119, 129
**Category:** Dead focus-node plumbing
**Evidence:** `_nameFocusNode` is created, registered with `_nameFocusNode.addListener(_onNameFocusChanged)`, attached via a `Focus` wrapper (line 272), and disposed — but the handler is an empty method: `void _onNameFocusChanged() {}`. This is the remains of the STEP-33 item auto-predict feature: the focus hook that would show or hide a suggestion list exists with no body, so the auto-predict affordance the PLAN describes has no visible behaviour on focus. Worth confirming against the STEP-33 intent rather than deleting. Uncertain — recommend 46.3 confirmation.
**Severity:** P3

---

### F-D24 | P2 | S13–S16 (aggregate)
**File:** all four screens
**Lines:** throughout
**Category:** Hardcoded Indonesian user-facing strings (known debt, RISK-0004)
**Evidence:** All four files are on the `_legacyExemptFiles` list in `tool/check_l10n_baseline.dart`, and all four route every user-visible label directly through `Text('...')` — headers (`'Inventori'`, `'Riwayat Inspeksi Peralatan'`, `'Inspeksi SOP Peralatan'`, `'Item Inventori'`), field labels, hints, empty states, buttons, and the interpolated banner `'${state.lowStockCount} item dengan stok rendah perlu perhatian.'`. Recorded once per batch rather than per string, per the aggregate instruction. Two details worth carrying into remediation: the filter labels mix languages (`'Passed / Operasional'`, `'Flagged / Perbaikan'`, `'Semua Tipe'`), and `InventoryBloc.categories` plus `_unitOptions` are hardcoded Indonesian **data** lists rather than UI strings, so localizing them touches persisted values and needs a decision, not just an ARB entry.
**Severity:** P2

---
