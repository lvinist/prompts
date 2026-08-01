# mine-flow — STEP-38 PLAN: Phase 2 Tier 2 UI/UX Bug Fixes

**Phase:** Phase 2 Tier 2  
**Owner:** Gemini 3.1 Pro High  
**Status:** Planned  
**Date:** 2026-07-25  
**Branch:** `step-0038-phase2-tier2-bugfixes`  
**Repos (projection):** `mine-flow-app`

> 19 UI/UX bugs identified after the STEP-37 residual Material purge. No
> architecture change — these are presentational and interaction-level fixes
> in the feature screens already rebuilt under Phase 2 Tier 2.

---

## Motivation

After completing STEP-37 (Residual Impeccable Material Purge), a visual and
interaction review revealed 19 bugs across Data Bucket, Land Clearing, Cut/Fill,
Inventory, Attendance, Equipment Check, Breadcrumbs, Language, and navigation
layers. These bugs affect usability and consistency and must be resolved before
Phase 2 can be considered complete.

---

## Decisions already locked

- Root `.throughstone/local-user.md` — read **Experience level** before
  user-facing questions or explanations, and **Communication style** before
  planning discussions.
- `architecture/07-ui-design-system.md` v0.2.0 — all UI must use ForUI
  components (`FButton`, `FCard`, etc.) and semantic color tokens.
- `ADR-0008-impeccable-bridge.md` — token standardization rules are binding.
- `architecture/12-test-strategy.md` — test tiers apply; every substep that
  changes code either updates its tests or states the reason it doesn't need to.
- **`FButton` is the canonical button widget.** Do not introduce raw
  `ElevatedButton`, `TextButton`, or `OutlinedButton`.
- **Zone/Zona field** must source its values from the shared `ZoneRepository`
  (wired in STEP-32) using `CreatableCombobox` — matching the Daily Log form pattern.
- **Language configuration** lives in `SettingsCubit` / `SettingsRepository`
  (STEP-35). Fix must wire the locale change through the existing state
  management layer — do not duplicate locale state.
- **Attendance form** is embedded in `attendance_screen.dart`. It should
  become a separate `AttendanceFormPage` pushed via GoRouter using the
  standard shell pattern.

---

## Bug Inventory

| #  | Area               | Bug description                                                                                      | Substep |
|----|--------------------|------------------------------------------------------------------------------------------------------|---------|
| 1  | Data Bucket        | Add button should be FButton in FAppBar, not a center button; remove upload button from center       | 38.1    |
| 2  | Data Bucket        | Form (upload) should use a back-button appbar (like Cut/Fill and Land Clearing)                     | 38.1    |
| 3  | Zona field         | Zona on Land Clearing, Cut/Fill, Data Bucket forms should use CreatableCombobox (zone source)        | 38.2    |
| 4  | Language           | Language configuration is not correctly implemented (locale not applied from Settings)               | 38.3    |
| 5  | Inventory          | Add button should be FButton in FAppBar, not a center button                                         | 38.1    |
| 6  | Inventory form     | Jumlah and Satuan fields should be merged into a single row (amount + unit dropdown)                 | 38.4    |
| 7  | Breadcrumbs        | Breadcrumb segments should not show hyphen characters (e.g. Daily-log should be Daily Log)           | 38.5    |
| 8  | Attendance form    | Form should be on a separate page/sheet, not integrated inline                                        | 38.6    |
| 9  | Attendance form    | Form should display employee name and position, not employee ID                                       | 38.6    |
| 10 | Cut/Fill form      | BCM field label: Cut Volume with unit m3 (BCM); LCM field label: Fill Volume with unit m3 (LCM)      | 38.2    |
| 11 | Cut/Fill form      | Cut and Fill fields should be in the same row (2-column layout)                                       | 38.2    |
| 12 | Cut/Fill form      | Remove +/- stepper buttons on Cut and Fill fields                                                     | 38.2    |
| 13 | Cut/Fill form      | Remove +/- stepper buttons on Plan and Actual fields                                                  | 38.2    |
| 14 | Land Clearing form | Form should use a tabbed layout (Plan tab / Actual tab), not a single scrollable form                 | 38.4    |
| 15 | Land Clearing form | Metode Clearing field should use CreatableCombobox with defaults: Excavator, Bulldozer, Chainsaw      | 38.2    |
| 16 | Equipment Check    | Form is broken on mobile (layout overflow / unusable on narrow screen)                                | 38.7    |
| 17 | All FButtons       | Every FButton that adds data should show both its icon and label (prefix icon + label text)           | 38.1    |
| 18 | Laporan button     | Should be shown as an icon-only button to the right of the Add Data FButton                           | 38.1    |
| 19 | Benchmark nav      | Benchmark page navigation is broken — route path mismatch; fix routing                               | 38.5    |

---

## Substeps

| #    | Title                                    | Produces                                                                             | Depends on | Risk         |
|------|------------------------------------------|--------------------------------------------------------------------------------------|------------|--------------|
| 38.1 | Button and AppBar Consistency            | data_bucket_list_page, inventory_dashboard_screen, land_clearing_list_screen, cut_fill_list_screen, Laporan buttons, upload_file_page | — | Low |
| 38.2 | Cut/Fill and Land Clearing Form Fixes    | cut_fill_form_screen.dart, land_clearing_entry_screen.dart, Zone combobox wiring     | —          | Low-Moderate |
| 38.3 | Language Configuration Fix               | app.dart, settings_cubit.dart, locale wiring                                         | —          | Moderate     |
| 38.4 | Inventory Form and Land Clearing Tabs    | inventory_item_entry_screen.dart, land_clearing_entry_screen.dart                    | 38.2       | Moderate     |
| 38.5 | Breadcrumbs and Benchmark Navigation Fix | global_app_header.dart, router.dart, app_shell.dart                                  | —          | Low          |
| 38.6 | Attendance Form Extraction               | attendance_form_page.dart (new), attendance_screen.dart refactor, router.dart        | —          | Moderate     |
| 38.7 | Equipment Check Mobile Layout Fix        | equipment_check_form_screen.dart                                                     | —          | Moderate     |

> Substeps 38.1, 38.3, 38.5, 38.7 are independent of each other.
> Substep 38.4 depends on 38.2 (Land Clearing tabs depend on form refactor base).
> Substep 38.6 is independent.
> Run 38.1, 38.3, 38.5, 38.7 in parallel; do 38.2 first, then 38.4.

---

## Substep Detail

### 38.1 — Button and AppBar Consistency

**Goal:** Ensure every Add Data action is an FButton in the FAppBar (not a
centered button in the body), every FButton shows its icon and label, and the
Laporan (Report) button appears as a secondary icon button beside the Add button.

**Affected screens:**
- lib/features/data_bucket/presentation/pages/data_bucket_list_page.dart
- lib/features/tracking/presentation/pages/inventory_dashboard_screen.dart
- lib/features/tracking/presentation/pages/land_clearing_list_screen.dart
- lib/features/tracking/presentation/pages/cut_fill_list_screen.dart
- lib/features/data_bucket/presentation/pages/upload_file_page.dart (appbar fix)

**Actions per screen:**

data_bucket_list_page.dart:
- Remove any center/body-level upload/add button.
- Add an FButton (primary, with prefix icon upload_file and label Text Tambah File) to the FAppBar actions.
- Add the Laporan icon button to the right of the Add button using FButtonStyle.ghost, icon assessment_outlined.
- If a true icon-only variant exists in ForUI, use it; otherwise use an IconButton with ForUI color tokens (no Material styling).

inventory_dashboard_screen.dart:
- Remove any center/body-level add item button.
- Add FButton with prefix icon add and label Text Tambah Item to FAppBar actions.
- Add the Laporan icon button beside it.

land_clearing_list_screen.dart and cut_fill_list_screen.dart:
- Verify the FAppBar add-data FButton shows both icon and label. If the button is icon-only today, add the label text.
- Add the Laporan icon button beside the Add button if missing.

upload_file_page.dart (Data Bucket form):
- Replace whatever is currently used as the top navigation control with a standard back-button appbar pattern matching Cut/Fill and Land Clearing forms:
  FAppBar with title Upload File and leading FButton ghost style with icon arrow_back that calls context.pop().

**Definition of Done:**
- [ ] No screen has an add-data button in the body/center of the screen.
- [ ] Every add-data FButton in the FAppBar shows both its icon and label.
- [ ] Laporan icon button appears to the right of each add-data FButton.
- [ ] Data Bucket form (upload_file_page.dart) has a back-button appbar.
- [ ] flutter analyze clean after this substep.

---

### 38.2 — Cut/Fill and Land Clearing Form Fixes

**Goal:** Fix field labels, remove stepper controls, add 2-column layout for
Cut/Fill, wire Zona and Metode Clearing with CreatableCombobox.

**Affected files:**
- lib/features/tracking/presentation/pages/cut_fill_form_screen.dart
- lib/features/tracking/presentation/pages/land_clearing_entry_screen.dart

**Cut/Fill form (cut_fill_form_screen.dart):**

Field label and unit fixes (Bug 10):
- Find the BCM field. Change its label/hint to Volume Cut and display its unit as m3 (BCM) as a label above or inline suffix.
- Find the LCM field. Change its label/hint to Volume Fill and display its unit as m3 (LCM).

2-column layout for Cut/Fill fields (Bug 11):
- Wrap the BCM and LCM FTextField widgets in a Row with two Expanded children separated by a SizedBox width 12 gap.

Remove +/- steppers on Cut/Fill fields (Bug 12):
- Find any Row with IconButton(+), TextField, IconButton(-) pattern on BCM and LCM fields; replace with plain FTextField.

Remove +/- steppers on Plan/Actual fields (Bug 13):
- Same pattern removal for Plan and Actual quantity fields.

Zona field — wire CreatableCombobox (Bug 3 for Cut/Fill):
- Replace the existing Zona FTextField/DropdownButton with CreatableCombobox sourced from ZoneRepository via BLoC/Cubit.
- Wire the ZoneRepository dependency the same way Daily Log does (read STEP-32 and STEP-33 for the established pattern).

**Land Clearing form (land_clearing_entry_screen.dart):**

Zona field — wire CreatableCombobox (Bug 3 for Land Clearing):
- Same pattern as above — replace Zona input with CreatableCombobox using ZoneRepository.

Metode Clearing field — wire CreatableCombobox (Bug 15):
- Replace existing input with CreatableCombobox with label Metode Clearing, default items Excavator, Bulldozer, Chainsaw.
- If CreatableCombobox requires a create callback, pass a no-op or null if the widget supports it — document inline.

Data Bucket Zona field (Bug 3 for Data Bucket):
- In lib/features/data_bucket/presentation/pages/upload_file_page.dart.
- If a Zona / site zone field exists on the upload form, replace it with CreatableCombobox using ZoneRepository.
- If no such field exists, note it in the substep completion comment and skip.

**Definition of Done:**
- [ ] Cut/Fill BCM field label = Volume Cut, suffix/unit = m3 (BCM).
- [ ] Cut/Fill LCM field label = Volume Fill, suffix/unit = m3 (LCM).
- [ ] BCM and LCM fields share a single row (2 columns).
- [ ] No +/- stepper buttons on BCM, LCM, Plan, or Actual fields.
- [ ] Zona field on Cut/Fill form uses CreatableCombobox sourced from ZoneRepository.
- [ ] Zona field on Land Clearing form uses CreatableCombobox sourced from ZoneRepository.
- [ ] Metode Clearing field uses CreatableCombobox with defaults Excavator, Bulldozer, Chainsaw.
- [ ] Data Bucket Zona field handled (wired or explicitly noted as non-existent).
- [ ] flutter analyze clean after this substep.

---

### 38.3 — Language Configuration Fix

**Goal:** Ensure that the language setting selected in the Settings page is
actually applied to the Flutter app locale at runtime.

**Affected files:**
- lib/app/app.dart
- lib/features/settings/presentation/bloc/settings_cubit.dart
- Possibly lib/features/settings/data/settings_local_datasource.dart

**Diagnosis steps (perform first, then fix):**
1. Read lib/features/settings/presentation/bloc/settings_cubit.dart to confirm a language/locale field exists in SettingsEntity.
2. Read lib/app/app.dart to check if MaterialApp/FTheme wrapper reads the locale from SettingsCubit.
3. Check that flutter_localizations is in pubspec.yaml and that supportedLocales includes Indonesian (id) and English (en).

**Fix pattern (if locale is not wired):**
- In app.dart, wrap with BlocBuilder SettingsCubit SettingsState to rebuild MaterialApp.router with locale from settingsState.settings.locale.
- supportedLocales should be Locale en and Locale id.
- localizationsDelegates should include GlobalMaterialLocalizations, GlobalWidgetsLocalizations, GlobalCupertinoLocalizations.

**If SettingsEntity lacks a locale field:**
- Add Locale locale to SettingsEntity with a default of Locale en.
- Update SettingsLocalDatasource to persist and retrieve it.
- Update SettingsCubit.updateLanguage(String langCode) to emit a state with the new locale.

**Definition of Done:**
- [ ] SettingsEntity includes a locale (or languageCode) field.
- [ ] app.dart reads the locale from SettingsCubit and passes it to MaterialApp.router.
- [ ] Changing language in Settings page visibly changes the app locale on next hot-reload (or immediately if locale propagation is reactive).
- [ ] pubspec.yaml includes flutter_localizations in dependencies.
- [ ] flutter analyze clean after this substep.

---

### 38.4 — Inventory Form and Land Clearing Tab Layout

**Goal:**
- Inventory item entry form: merge the Jumlah (amount) and Satuan (unit) inputs into a single row.
- Land Clearing entry form: convert the single scrollable form into a tabbed layout with a Plan tab and an Actual tab.

**Depends on:** 38.2 (Land Clearing form already refactored for field fixes)

**Affected files:**
- lib/features/tracking/presentation/pages/inventory_item_entry_screen.dart
- lib/features/tracking/presentation/pages/land_clearing_entry_screen.dart

**Inventory form — Jumlah + Satuan merged row (Bug 6):**

Reference design: Picture 1 from the user request — a FTextField for amount on the left, and a unit dropdown (kg, pcs, m, etc.) on the right, inside a single labeled container.

Implementation: Replace separate Jumlah and Satuan fields with a Column that has label Jumlah, then a Row with Expanded FTextField (hint Masukkan jumlah, keyboardType number) and a DropdownButton with options pcs, kg, m, m2, m3, liter.

If ForUI provides a combined field pattern use it. Otherwise the Row pattern is acceptable. The DropdownButton must use ForUI color tokens (no raw colors), or be replaced with FSelect if available.

**Land Clearing form — Tabbed layout (Bug 14):**

Convert land_clearing_entry_screen.dart to use DefaultTabController + TabBar + TabBarView with two tabs: Plan and Actual.
- Plan tab contains: tanggal rencana, target area (ha), zona (CreatableCombobox), metode clearing (CreatableCombobox).
- Actual tab contains: tanggal aktual, realisasi area (ha), zona, metode clearing (same fields, different controllers/events).
- The Submit button remains at the bottom of the screen (outside the tab view).

ForUI FTabBar should be used if available; otherwise use Material TabBar styled with ForUI color tokens (underline color = theme.colors.primary).

**Definition of Done:**
- [ ] Inventory entry: Jumlah and Satuan are in one row — numeric field + unit selector.
- [ ] Inventory entry: no raw colors on the unit selector.
- [ ] Land Clearing entry: two tabs rendered — Plan and Actual.
- [ ] Each tab shows the correct subset of fields.
- [ ] Submit button is outside/below the tab view and works for both tabs.
- [ ] flutter analyze clean after this substep.

---

### 38.5 — Breadcrumbs and Benchmark Navigation Fix

**Goal:**
- Fix breadcrumb labels so route segment names do not contain hyphens (e.g. daily-log becomes Daily Log).
- Fix the Benchmark DB navigation — route path mismatch currently prevents the page from loading.

**Affected files:**
- lib/app/presentation/widgets/global_app_header.dart (breadcrumb rendering)
- lib/app/router.dart (benchmark route path fix)
- lib/app/presentation/pages/app_shell.dart (benchmark sidebar entry)

**Breadcrumb fix (Bug 7):**

In global_app_header.dart, the breadcrumb segments are derived from the current URI path. Apply a display-name map before rendering:

```
const _kSegmentLabels = const {
  'cut-fill': 'Cut Fill',
  'land-clearing': 'Land Clearing',
  'daily-log': 'Daily Log',
  'data-bucket': 'Data Bucket',
  'equipment-check': 'Equipment Check',
  'benchmark-db': 'Benchmark DB',
  'upload': 'Upload File',
};
```

Create a helper function _segmentLabel(String segment) that looks up _kSegmentLabels[segment] or falls back to splitting on hyphen and title-casing each word. Use this function when rendering each breadcrumb crumb instead of the raw segment string.

**Benchmark navigation fix (Bug 19):**

Root cause: AppRoutes.benchmarkDb = '/benchmark-db' is an absolute path, but the route is declared as a nested route under /operations (path segment benchmark-db), making the actual navigable path /operations/benchmark-db.

Fix:
1. In router.dart, update AppRoutes.benchmarkDb to '/operations/benchmark-db'.
2. Verify the GroupLandingPage in Branch 2 references the correct new constant.
3. In app_shell.dart, add a Benchmark DB sidebar entry in the Operations _SidebarSection with branchIndex 2, route AppRoutes.benchmarkDb, label Benchmark DB, icon Icons.trip_origin_outlined, activeIcon Icons.trip_origin.

**Definition of Done:**
- [ ] Breadcrumb segments never show a hyphen character; they show title-case labels.
- [ ] Navigating to benchmark-db from Operations group landing page works.
- [ ] Benchmark DB entry appears in the desktop sidebar under Operations.
- [ ] AppRoutes.benchmarkDb is /operations/benchmark-db.
- [ ] flutter analyze clean after this substep.

---

### 38.6 — Attendance Form Extraction

**Goal:** Extract the inline attendance form from attendance_screen.dart into a separate AttendanceFormPage, pushed via GoRouter. The form must display the employee name and position (not employee ID).

**Affected files:**
- lib/features/attendance/presentation/pages/attendance_screen.dart
- lib/features/attendance/presentation/pages/attendance_form_page.dart (NEW)
- lib/app/router.dart

**New route:**
- Add static const attendanceForm = '/teams/attendance/form' to AppRoutes.
- Under the attendance GoRoute in router.dart, add a subroute with path form, name attendance-form, that builds AttendanceFormPage with repository and siteId from extra.

**attendance_form_page.dart (new):**
- Use standard Scaffold with FAppBar (back button appbar).
- Show employee name (from Employee.name) and position (from Employee.position or Employee.role) in the form, not the raw employee ID.
- Load the employee list from AttendanceRepository or pass the employee as extra.
- On save, pop with result and have attendance_screen.dart reload.

**attendance_screen.dart refactor:**
- Remove the inline form widgets from the page.
- Replace the inline form trigger with context.push(AppRoutes.attendanceForm, extra: siteId info).

**Definition of Done:**
- [ ] AttendanceFormPage exists as a standalone page at route /teams/attendance/form.
- [ ] The form shows employee name and position, not employee ID.
- [ ] attendance_screen.dart no longer contains inline form widgets.
- [ ] Back button on AttendanceFormPage pops correctly.
- [ ] flutter analyze clean after this substep.

---

### 38.7 — Equipment Check Mobile Layout Fix

**Goal:** Fix the broken mobile layout of the Equipment Check form screen (equipment_check_form_screen.dart), as shown in Picture 2 (overflow, widgets cut off, unusable on narrow screen).

**Affected file:**
- lib/features/equipment_check/presentation/pages/equipment_check_form_screen.dart

**Diagnosis steps (perform first):**
1. Run the app on a narrow viewport (less than 400dp wide) or use Flutter device preview to reproduce the overflow.
2. Identify which widget causes the overflow — likely a Row that does not wrap, a fixed-width container, or a non-scrollable column.

**Common fixes:**
- If the device type tab row (GNSS Receiver, Total Station, Drone/UAV) overflows horizontally: wrap it in SingleChildScrollView(scrollDirection: Axis.horizontal).
- If the pre/post work toggle row overflows: use Wrap or constrain to ConstrainedBox with maxWidth 480.
- If the SOP checklist items overflow: verify sop_checklist_item_card.dart uses Expanded or Flexible correctly inside Row widgets.
- If the submit button is cut off: wrap the body Column in a SingleChildScrollView.

**Key constraint:** Do not change the logical structure (tab selection, pre/post check toggle, checklist items). Only fix layout constraints.

**Definition of Done:**
- [ ] Equipment Check form renders without overflow warnings on narrow mobile (less than 400dp).
- [ ] All interactive elements (type tabs, pre/post toggle, checklist, submit button) are reachable by scrolling on mobile.
- [ ] No visual regressions on desktop/tablet (800dp and above).
- [ ] flutter analyze clean after this substep.

---

## Test plan

| Test tier | Substep(s) | Tests to create or update | Command |
|-----------|------------|---------------------------|---------|
| Widget | 38.1 | data_bucket_list_page_test.dart — assert center button absent, FAppBar FButton present | flutter test test/features/data_bucket |
| Widget | 38.1 | inventory_dashboard_screen_test.dart — assert center button absent, FAppBar FButton present | flutter test test/features/tracking |
| Widget | 38.2 | cut_fill_form_screen_test.dart — assert stepper buttons absent, BCM/LCM labels correct | flutter test test/features/tracking |
| Widget | 38.2 | land_clearing_entry_screen_test.dart — assert CreatableCombobox for Zona and Metode | flutter test test/features/tracking |
| Widget | 38.4 | inventory_item_entry_screen_test.dart — assert Jumlah and Satuan in one Row | flutter test test/features/tracking |
| Widget | 38.4 | land_clearing_entry_screen_test.dart — assert two tabs rendered | flutter test test/features/tracking |
| Widget | 38.6 | attendance_form_page_test.dart (create) — assert name and position fields present | flutter test test/features/attendance |
| Widget | 38.7 | equipment_check_form_screen_test.dart — assert no RenderFlex overflow in narrow viewport | flutter test test/features/equipment_check |
| Integration | all | Full suite — no new failures | flutter test |
| Analyzer | all | Zero issues | flutter analyze |

> If a test file does not exist for a changed widget, create a minimal smoke test: pump the widget with required stubs, assert it renders without error, and assert the banned/required pattern.

---

## Ground rules

- Calibrate communication from root .throughstone/local-user.md. Experience level and communication style govern how you explain decisions.
- Tests ship with the code. Per-substep widget tests are expected; full suite runs at the end of each substep.
- No scope creep. If a new bug is found during execution, note it in a comment and file it as a new substep — do not widen this STEP.
- Diagnosis before fix. For 38.3, 38.7 especially — read the file first, diagnose the root cause, then apply the minimal fix.
- ForUI-first. Use ForUI components; only fall back to Material when ForUI has a genuine gap, and always use ForUI color tokens.
- Accepted risks stay visible. Update registries/risks.yml if any fix is deferred or leaves a documented limitation.

---

## Definition of done

- [ ] 38.1 complete: FAppBar FButton with icon and label on all list screens; Laporan icon button beside each; Data Bucket form has back-button appbar.
- [ ] 38.2 complete: Cut/Fill and Land Clearing form field fixes applied; CreatableCombobox for Zona and Metode Clearing wired.
- [ ] 38.3 complete: Language setting propagates to MaterialApp locale; SettingsEntity has a locale field; changing language in Settings is reflected.
- [x] 38.4 complete: Inventory form has merged Jumlah+Satuan row; Land Clearing entry has Plan/Actual tabs.
- [ ] 38.5 complete: Breadcrumbs show clean labels (no hyphens); Benchmark DB navigation works; sidebar has Benchmark entry.
- [ ] 38.6 complete: AttendanceFormPage is a standalone route; shows name and position; attendance_screen.dart no longer has inline form.
- [ ] 38.7 complete: Equipment Check form renders without overflow on mobile; all controls reachable.
- [ ] flutter analyze clean globally.
- [ ] flutter test zero new failures vs. STEP-37 baseline (387 passing, 27 pre-existing).
- [ ] prompts/STEP-index.md updated: STEP-38 row and all substep rows flipped to Done.
- [ ] STEP archived to prompts/002-phase2/step-0038/.
