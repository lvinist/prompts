# STEP-46.1 — Code-Level Static Scan Findings

Generated: 2026-08-27
Screens scanned: 24 (S01–S24, full router surface per the STEP-46 PLAN inventory)
Total candidates: 125  (P1: 53 · P2: 52 · P3: 20)

Scope and method: code reading only, no runtime evidence. Each screen file was read
together with its BLoC/Cubit, state class, feature widgets, and `lib/app/router.dart`
construction site, and compared against `Code/mine-flow-docs/architecture/07-ui-design-system.md`
v0.4.0 and `Code/mine-flow-docs/overview.md`. Findings are grouped into six batches of four
screens; IDs are namespaced per batch (F-A01…, F-B01…) and are stable references for 46.3.

## Coverage

| Batch | Screens | Findings |
|---|---|---|
| A | S01 Login, S02 Dashboard, S03 GroupLanding, S04 Settings | 23 |
| B | S05 Attendance, S06 AttendanceForm, S07 DailyLogList, S08 DailyLogForm | 18 |
| C | S09 CutFillList, S10 CutFillForm, S11 LandClearingSummary, S12 LandClearingEntry | 18 |
| D | S13 InventoryDashboard, S14 InventoryItemEntry, S15 EquipmentHistory, S16 EquipmentCheckForm | 24 |
| E | S17 BenchmarkList, S18 BenchmarkForm, S19 Timeline, S24 Notifications | 23 |
| F | S20 DataBucketList, S21 UploadFile, S22 FileDetail, S23 ReportConfig | 19 |

Every screen in the 24-screen inventory produced at least one finding; no `No findings.`
rows were emitted.

## Notes for 46.3 (triage input, not findings)

1. **Batch C severity needs re-tiering.** All 18 of batch C's findings are marked P1. Several
   (dead retry buttons, unvalidated forms) are the same class of defect that batches A/B/D/E/F
   tiered as P2. Re-tier batch C against the others before building the confirmed register, or
   the P1 count will be misleading.
2. **Batch C has no aggregate rows.** Batches A/B/D/E/F each carry one aggregate row for
   hardcoded Indonesian strings (RISK-0004) and one for residual Material widgets. Batch C
   does not, so S09–S12's i18n and Material-leftover debt is under-recorded here even though
   `grep` confirms all four files are on the `_legacyExemptFiles` list and all four use
   Material `SnackBar`/`AppBar` and 250ms `AnimatedSwitcher`s.
3. **Cross-cutting classes worth one remediation decision each**, rather than per-screen fixes:
   - **No real authentication.** `LoginPage._login` only navigates and `SettingsPage` logout
     never calls `AuthRepository.signOut()`. Everything about role gating, RLS behaviour, and
     per-user attribution downstream is contingent on fixing this first (F-A01, F-A02, F-A15).
   - **Empty-string identity flowing from the router.** `foremanId: ''` at `router.dart`
     245, 255, 348, 368, 379 becomes an active filter on read and a blank attribution on
     write across daily log, cut/fill, land clearing, and equipment check
     (F-B01, F-B02, F-B03, F-C04, F-C05, F-C17, F-C18).
   - **Mislabelled report FABs.** Five screens open `report-config` with a `ReportType` that
     does not match their own label, because `ReportType` has only three members
     (F-B07, F-C03, F-D05, F-E07, F-F02). Needs a product decision on whether to add report
     types or remove the buttons.
   - **Destructive actions without confirmation or role gate.** Inventory, equipment check,
     and daily log delete on a single tap (F-D01, F-D02, F-B06, F-C06, F-C07); benchmark and
     data-bucket delete do confirm (F-E10, F-F07) but still have no role check.
   - **Forms that declare validation and never run it.** `_formKey` present, `validate()`
     never called, or called with no validators attached (F-D06, F-C15, F-C16, F-E06, F-F05).
   - **Numeric input silently discarded on parse failure.** `if (parsed != null)` listeners
     keep the previous BLoC value while the field shows something else
     (F-D07, F-E06, and the same idiom in batch C).
   - **Material leftovers after STEP-37.** `SnackBar`, `AppBar`, `AlertDialog`,
     `FilledButton`, `FilterChip`, `DropdownButtonFormField` remain across all six batches.
   - **Motion over the Doc 07 budget.** 250ms `AnimatedSwitcher`s on four list screens, a
     300ms one on the dashboard, and a 350ms + 40ms-stagger entrance on notifications, against
     a stated 150–200ms ceiling.
4. **`tool/check_l10n_baseline.dart` has a scope hole** (F-A13): it scans `Text('...')` in
   presentation files, so `GroupLandingPage` passes the guard while receiving fourteen
   hardcoded labels from `lib/app/router.dart`. The guard reports a coverage figure that is
   not true; fixing the screen without fixing the guard leaves the hole open.
5. **Analyzer and test baseline at scan time**: `flutter analyze` → "No issues found!";
   `flutter test` → 435/435 passing; `dart run tool/check_l10n_baseline.dart` → OK (32
   non-exempt files scanned, 28 legacy files exempt). No analyzer-derived findings were
   appended because the analyzer is clean — every finding here is one static analysis does
   not catch.

---
## Batch A — S01–S04

### F-A01 | P1 | S01 LoginPage
**File:** `lib/features/auth/presentation/pages/login_page.dart`
**Lines:** 21–23
**Category:** Authentication bypass — login performs no authentication
**Evidence:**
```dart
void _login() {
  context.go(AppRoutes.dashboard);
}
```
The submit handler navigates straight to the dashboard. It never calls `AuthRepository.signIn`, never reads the two controllers it maintains, and never inspects a result. `AuthRepository` does exist (`lib/features/auth/data/repositories/auth_repository_impl.dart` wraps `supabaseClient.auth`), so this is an unwired screen rather than a missing capability. Every downstream screen then runs with no Supabase session, which means role-based visibility and RLS-backed reads cannot behave correctly no matter what the rest of the audit finds — any user reaching this page is admitted, and no user is ever identified. This is the single most consequential functional defect on the login surface.
**Severity:** P1

---

### F-A02 | P1 | S01 LoginPage
**File:** `lib/features/auth/presentation/pages/login_page.dart`
**Lines:** 18–19
**Category:** Hardcoded credentials pre-filled into the form
**Evidence:**
```dart
final _emailController = TextEditingController(text: 'admin@mineflow.id');
final _passwordController = TextEditingController(text: 'password123');
```
A real credential pair is compiled into the shipped widget as the initial field value, with the password in plaintext. Even after F-A01 is fixed, this pre-fills an administrator account for anyone who opens the app, and the string survives in the release bundle where it is trivially recoverable. Development convenience values belong in a local fixture or a dart-define, never in a presentation constructor. Note this is distinct from F-A01: fixing the auth wiring without removing these leaves a shipped admin credential.
**Severity:** P1

---

### F-A03 | P2 | S01 LoginPage
**File:** `lib/features/auth/presentation/pages/login_page.dart`
**Lines:** 70–89
**Category:** Missing form validation, loading and error states
**Evidence:** The email and password `FTextField`s have no validator, the form has no empty-field guard, and `FButton(onPress: _login, ...)` is never disabled. There is no in-flight indicator and no error surface for a rejected credential. Because the screen holds no BLoC/Cubit at all, there is no state machine to express *submitting* or *failed* — so once F-A01 wires a real network call the user will get a frozen button with no feedback, and a wrong password will produce silence. The three states need to exist as part of the same fix, not after it.
**Severity:** P2

---

### F-A04 | P2 | S01 LoginPage
**File:** `lib/features/auth/presentation/pages/login_page.dart`
**Lines:** 61
**Category:** Misspelled user-facing tagline
**Evidence:**
```dart
'Sistem Monitoring & Manajamen Tambang',
```
"Manajamen" is a misspelling of the Indonesian "Manajemen". This is the first line of text a user reads on the first screen of the product, and it is spelled wrong in the app's own primary language. Cheap to fix, disproportionately visible.
**Severity:** P2

---

### F-A05 | P1 | S02 DashboardPage
**File:** `lib/app/presentation/bloc/dashboard_cubit.dart`
**Lines:** 105–109
**Category:** Dimensionally invalid arithmetic — BCM and LCM summed together
**Evidence:**
```dart
double total = 0.0;
for (final r in records) {
  total += r.bcmVolume + r.lcmVolume;
}
return total;
```
This total is surfaced on the dashboard as `'${state.cutFillVolume.toStringAsFixed(0)} m³'` under the label "Cut / Fill Volume" / "Today's total volume". BCM (bank cubic metres, material in situ) and LCM (loose cubic metres, the same material after excavation and swell) are two measurements *of the same material in different states*, not two separate quantities. Adding them double-counts every record and inflates the headline figure by roughly the swell factor — for typical overburden that is a 20–35% overstatement presented as a precise whole number. For an app whose stated purpose is monitoring cut/fill volume, the top-line number on the landing screen being an invalid sum is the most serious data-correctness finding in this batch. The correct behaviour requires a product decision (report BCM, report LCM, or show both separately), so remediation must pick one explicitly rather than silently changing the formula.
**Severity:** P1

---

### F-A06 | P1 | S02 DashboardPage
**File:** `lib/app/presentation/bloc/dashboard_cubit.dart`
**Lines:** 83–92
**Category:** Data-binding mismatch — "Active Crew" counts every attendance record
**Evidence:**
```dart
final records = await _attendanceRepository.getAttendanceForDate(
  todayStart,
  siteId: siteId,
);
return records.length;
```
`AttendanceStatus` (`lib/features/attendance/domain/entities/attendance_status.dart`) has four values: `present`, `absent`, `sick`, `leave`. `records.length` counts all of them, so a crew member marked absent, sick, or on leave still increments the figure displayed as "Active Crew" and captioned "N crew today". A supervisor reading the dashboard to judge how many people are on site gets the roster size, not the attendance. The label and the bound value disagree, and the discrepancy grows precisely on the days it matters most.
**Severity:** P1

---

### F-A07 | P1 | S02 DashboardPage
**File:** `lib/app/presentation/bloc/dashboard_cubit.dart`
**Lines:** 78–138
**Category:** Per-fetch error swallowing renders zero as if it were real data
**Evidence:** Each of the four private fetchers wraps its repository call in `try { ... } catch (_) { return 0; }`. Because every failure is absorbed at that inner level, the outer `catch` that emits `DashboardStatus.failure` is effectively unreachable — `Future.wait` never sees a rejection. The consequence is that a total backend outage renders as four confident zeroes with the success-path subtitles ("0 crew today", "Today's total volume"), never as the `'Gagal memuat'` text the UI already implements. The failure branch exists in both cubit and widget but cannot be reached, so the user cannot distinguish "no work logged today" from "the app could not talk to the server" — a dangerous ambiguity for a field-operations dashboard, and one that also makes the `isFailure` UI code dead.
**Severity:** P1

---

### F-A08 | P2 | S02 DashboardPage
**File:** `lib/app/presentation/pages/dashboard_page.dart`
**Lines:** 149–180
**Category:** Dead section — heading and subtitle promise content that was removed
**Evidence:**
```dart
Text('Akses Cepat', ...),
Text('Laporan, timeline, dan notifikasi', ...),
const SizedBox(height: 16),
// Laporan quick access removed in STEP-34.3 — now available as
// an FAppBar action on each individual feature screen.
const SizedBox.shrink(),
```
The section renders a header reading "Quick Access" and a subtitle explicitly naming reports, timeline, and notifications, followed by nothing. STEP-34.3 removed the tiles but left the labels, so the dashboard advertises three destinations and provides zero. A first-time user reads the subtitle as a broken or still-loading region. Either the heading and subtitle go with the tiles, or the tiles come back.
**Severity:** P2

---

### F-A09 | P2 | S02 DashboardPage
**File:** `lib/app/presentation/pages/dashboard_page.dart`
**Lines:** 73–92, 103–126
**Category:** Mixed-language UI within a single component
**Evidence:** The four stat cards use English labels (`'Active Crew'`, `'Cut / Fill Volume'`, `'Equipment Checks'`, `'Notifications'`) and English subtitles (`'${state.activeCrewCount} crew today'`, `"Today's total volume"`, `'${...} checks today'`, `'${...} unread'`), while their loading and failure states use Indonesian (`'Memuat…'`, `'Gagal memuat'`) and the section below is Indonesian (`'Akses Cepat'`, `'Laporan, timeline, dan notifikasi'`). Doc 07 §5 states the MVP ships Indonesian by default. The same card therefore switches language depending on whether the data loaded, which reads as unfinished rather than bilingual. This is a presentation-consistency defect independent of the RISK-0004 migration backlog — the strings are wrong in whichever language the delegate eventually serves.
**Severity:** P2

---

### F-A10 | P3 | S02 DashboardPage
**File:** `lib/app/presentation/pages/dashboard_page.dart`
**Lines:** 94–97
**Category:** Motion duration exceeds the design contract
**Evidence:**
```dart
return AnimatedSwitcher(
  duration: const Duration(milliseconds: 300),
  switchInCurve: Curves.easeOutQuart,
```
Doc 07 §5 specifies "Snappy and subtle (150-200ms fades)". 300ms is 50% over the stated ceiling, and it gates the appearance of the dashboard's primary content on every load, so it is felt on the app's most frequently visited screen.
**Severity:** P3

---

### F-A11 | P3 | S02 DashboardPage
**File:** `lib/app/presentation/pages/dashboard_page.dart`
**Lines:** 32, 34
**Category:** Material `Scaffold` where the design system uses `FScaffold`
**Evidence:** `DashboardPage` returns a bare `Scaffold`, whereas `SettingsPage` (S04) returns `FScaffold` with an `FHeader`. Doc 07 §3/§6 puts ForUI components in charge of page framing and STEP-37 was specifically a Material-purge STEP. Two sibling top-level pages using different scaffolds means padding, background resolution, and header behaviour are not guaranteed to agree between branches of the same shell.
**Severity:** P3

---

### F-A12 | P2 | S03 GroupLandingPage
**File:** `lib/app/presentation/pages/group_landing_page.dart`
**Lines:** 95–106
**Category:** No visible focus indicator on a keyboard-focusable tile
**Evidence:**
```dart
child: Focus(
  onKeyEvent: (node, event) { ... context.push(config.route); ... },
  child: GestureDetector(
    onTap: () => context.push(config.route),
```
The tile is wired for keyboard activation (Enter/Space) and announces `button: true` to semantics, but nothing in the widget reacts visually to focus — `Focus` is used only as a key-event listener, and `GestureDetector` provides no pressed, hover, or focus affordance. A keyboard user on the web build (the supervisor surface per Doc 07 §4) can traverse these tiles and activate them while having no way to see which one is selected. That is a WCAG 2.1 AA "focus visible" failure on the primary navigation surface for three of the five shell branches, and the fix is not cosmetic — the tile needs a real button/`InkWell`/`FTile` with focus styling rather than a bare gesture recogniser.
**Severity:** P2

---

### F-A13 | P2 | S03 GroupLandingPage
**File:** `lib/app/router.dart`
**Lines:** 138–149, 213–236, 280–315
**Category:** Localization guard bypassed by passing literals from the router
**Evidence:** Every user-visible string on this screen arrives as a constructor argument from `router.dart`:
```dart
const GroupLandingPage(
  title: 'Tools',
  subtitle: 'Alat dan utilitas tambahan',
  features: [ FeatureTileConfig(label: 'Data Bucket', description: 'Penyimpanan data geospasial', ...) ],
)
```
`group_landing_page.dart` is deliberately *not* on the `_legacyExemptFiles` list in `tool/check_l10n_baseline.dart`, and the guard passes — because the guard scans `Text('...')` call sites in presentation files and these literals live in `lib/app/router.dart`, which it does not treat as a presentation file. So this screen is nominally localization-clean while shipping fourteen hardcoded labels. That is a hole in the guard as much as in the screen: any future screen can silently defeat the check by receiving its strings from the router. Both the screen and the guard's file scope need fixing, or the guard will keep reporting a coverage figure that is not true.
**Severity:** P2

---

### F-A14 | P2 | S03 GroupLandingPage
**File:** `lib/app/router.dart`
**Lines:** 139–140, 214–215, 281–282
**Category:** Mixed-language UI — English group titles with Indonesian subtitles
**Evidence:** `title: 'Tools'` / `subtitle: 'Alat dan utilitas tambahan'`; `title: 'Operations'` / `subtitle: 'Manajemen pelacakan operasi lapangan'`; `title: 'Teams'` / `subtitle: 'Kehadiran kru dan dokumentasi harian'`. Feature labels are likewise English (`'Cut / Fill'`, `'Land Clearing'`, `'Benchmark DB'`, `'Attendance'`, `'Daily Log'`, `'Inventory'`, `'Equipment Check'`) with Indonesian descriptions, except `'Timeline Pekerjaan'` which is mixed within the single label. Every heading on these three landing pages is in a different language from the sentence directly beneath it. Same class of problem as F-A09 but on the navigation surface, where it is the first thing a crew member sees after the dashboard.
**Severity:** P2

---

### F-A15 | P1 | S04 SettingsPage
**File:** `lib/features/settings/presentation/pages/settings_page.dart`
**Lines:** 326–328
**Category:** Logout does not terminate the session
**Evidence:**
```dart
if (confirm == true && context.mounted) {
  context.go(AppRoutes.login);
}
```
After confirming a destructive "Keluar / Logout" the app only navigates. `AuthRepository.signOut()` exists (`lib/features/auth/data/repositories/auth_repository_impl.dart:71`, calling `supabaseClient.auth.signOut()`) and is never invoked here; neither is the role/token clearing in `lib/core/security/secure_storage_service.dart`. On a shared field device the Supabase session and any cached role therefore survive a logout, and because the login screen admits everyone (F-A01) the next person is placed straight back into the previous user's session context. The user was shown an explicit confirmation dialog promising an action that does not happen.
**Severity:** P1

---

### F-A16 | P1 | S04 SettingsPage
**File:** `lib/features/settings/presentation/pages/settings_page.dart`
**Lines:** 382–394
**Category:** Hardcoded identity and role displayed as the user's own profile
**Evidence:**
```dart
Text(
  'Pengguna', // Placeholder — will come from auth profile
  ...
Text(
  'Foreman', // Placeholder — will come from auth profile
```
The profile card presents a fabricated name and, more seriously, a fabricated **role**. `UserEntity` carries a real `role` field (`'supervisor' | 'foreman' | 'crew'`), so the app has a role concept that this screen contradicts. A supervisor opening Settings is told they are a Foreman. Role is the app's authorization axis, so displaying a fixed wrong value is not a cosmetic placeholder — it actively misinforms the user about what they are permitted to do, and it will look correct to exactly one third of the user base, making the bug easy to miss in casual testing.
**Severity:** P1

---

### F-A17 | P1 | S04 SettingsPage
**File:** `lib/features/settings/presentation/pages/settings_page.dart`
**Lines:** 226, 292
**Category:** Support WhatsApp link contains a masked placeholder number
**Evidence:** The button displays `Text('+62 851-5604-2854')` but the handler launches
```dart
final uri = Uri.parse('https://wa.me/+628****2854');
```
The URL literally contains asterisks — a redacted number committed as if it were real. `canLaunchUrl` will generally succeed for a well-formed `https://wa.me/...` URL, so the user is handed off to WhatsApp with an invalid recipient rather than getting the graceful `'Tidak dapat membuka WhatsApp.'` error. The displayed text and the launched target also disagree, so the failure is invisible in code review of either half alone. This is the support escape hatch for field users with a technical problem, which makes silent breakage costly.
**Severity:** P1

---

### F-A18 | P2 | S04 SettingsPage
**File:** `lib/features/settings/presentation/pages/settings_page.dart`
**Lines:** 304–324
**Category:** Material `AlertDialog` and `SnackBar` in a ForUI screen
**Evidence:** The logout confirmation is a Material `AlertDialog` whose `actions` are `FButton`s, and `_showSnackError` uses `ScaffoldMessenger`/`SnackBar` coloured with `theme.colors.error`. Doc 07 §3/§6 makes ForUI the component vocabulary and STEP-37 was dedicated to purging residual Material widgets (`Card`, `ElevatedButton`, `TextButton`, `MaterialBanner`) — dialogs and snackbars were evidently missed. The mixed idiom means the app's only destructive confirmation renders with Material elevation, shape, and motion inside an otherwise ForUI Zinc surface, and it will not follow the design system's radii or border treatment in either theme.
**Severity:** P2

---

### F-A19 | P2 | S04 SettingsPage
**File:** `lib/features/settings/presentation/pages/settings_page.dart`
**Lines:** 436
**Category:** Raw `TextStyle` with an off-scale font size
**Evidence:**
```dart
Text(label, style: const TextStyle(fontSize: 11)),
```
A bare `TextStyle` bypasses `theme.typography` entirely, so this label inherits neither the Geist family nor any theme colour, and 11px is not a step on the ForUI typography scale — it is a hand-tuned value chosen to make three buttons fit. It is also the only raw `TextStyle` in the file, so it will not follow a future typography change and will not recolour in dark mode the way its siblings do. Doc 07 §2 names the theme typography as the source of truth.
**Severity:** P2

---

### F-A20 | P2 | S04 SettingsPage
**File:** `lib/features/settings/presentation/pages/settings_page.dart`
**Lines:** 81–120
**Category:** Language selector offers a locale the app cannot actually render
**Evidence:** The Preferences card lets the user switch to English via `updateLocale(const Locale('en'))`. Per Doc 07 §5 and RISK-0004, only a baseline ARB catalog exists and 28 presentation files remain on `_legacyExemptFiles` with hardcoded Indonesian strings. Selecting English therefore changes almost nothing: the user gets an app that is still Indonesian everywhere except the handful of migrated strings, with no indication that the toggle did not work. Offering a switch that visibly fails is worse than not offering it — either hide the English option until migration completes, or state in the UI that translation is partial. This is a product-level consequence of RISK-0004 rather than a new defect, but it is user-visible today and belongs in the register.
**Severity:** P2

---

### F-A21 | P3 | S04 SettingsPage
**File:** `lib/features/settings/presentation/pages/settings_page.dart`
**Lines:** 257
**Category:** Hardcoded app version string
**Evidence:** `Text('mine-flow v0.1.0', ...)` duplicates `version: 0.1.0+1` from `pubspec.yaml` as a literal. `package_info_plus` is not a dependency, so there is nothing keeping the two in sync; the displayed version will silently go stale at the first release bump and then misreport which build a field user is running — exactly when a support conversation needs it to be right.
**Severity:** P3

---

### F-A22 | P3 | S04 SettingsPage
**File:** `lib/features/settings/presentation/pages/settings_page.dart`
**Lines:** 211, 226, 275, 292
**Category:** Personal contact details of an individual hardcoded as product support
**Evidence:** `alvin.geomatics@gmail.com` and a personal mobile number are compiled into the app as the support channel, in both the label and the launch handler. For an internal tool this may be intended, but it routes all field support through one person's personal accounts, cannot be changed without a rebuild, and puts an individual's PII in the shipped bundle. Worth an explicit owner decision (shared support alias vs. accepted as-is) rather than passing silently. Uncertain — recommend 46.3 confirmation.
**Severity:** P3

---

### F-A23 | P3 | S01–S04 (systemic, batch-wide)
**File:** `lib/app/presentation/pages/dashboard_page.dart`, `lib/app/presentation/pages/group_landing_page.dart`, `lib/features/settings/presentation/pages/settings_page.dart`, `lib/features/auth/presentation/pages/login_page.dart`
**Lines:** dashboard 104–122; group landing 145–151; settings 138–160, 209–245; login 50
**Category:** Material icon set used where the design contract specifies Lucide
**Evidence:** Every icon in this batch comes from Material — `Icons.groups_outlined`, `Icons.moving_outlined`, `Icons.build_outlined`, `Icons.notifications_active_outlined`, `Icons.chevron_right`, `Icons.light_mode`, `Icons.dark_mode`, `Icons.settings_suggest`, `Icons.email_outlined`, `Icons.chat_outlined`, `Icons.logout`, `Icons.person`, `Icons.terrain`. Doc 07 §5 specifies **Lucide Icons** "for clean, consistent line-art icons". Material's mixed filled/outlined metaphors sit visually apart from the ForUI Zinc surfaces they are placed on, and the inconsistency is systemic rather than local — it is almost certainly repo-wide, so remediation should be a single deliberate sweep with a decision recorded (migrate to Lucide, or amend Doc 07 and log an ADR) rather than 24 screen-local edits. Raised once here rather than per-icon.
**Severity:** P3

---

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
