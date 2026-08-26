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
