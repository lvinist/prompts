# STEP-46.2 — Screenshot Visual Review Findings

Generated: 2026-08-27
Screens reviewed: 24 (S01–S24, complete application router surface)
Screenshots saved to: `prompts/003-release-readiness-integration-scale/step-0046/screenshots/`
Total visual candidates: 50 (P1: 8 · P2: 27 · P3: 15)

---

## Executive Summary

Pass 1b conducted an open-ended visual review of all 24 routed screens in `mine-flow` running rendered in Chrome at 1280x800 desktop resolution across both Light and Dark themes.

### Key Visual & UX Patterns Identified:
1. **Isolated Full-Screen Traps (S23, S24):** `ReportConfigPage` (S23) and `NotificationListPage` (S24) are pushed on top of the shell with no app bar, no back button, and no close affordance. On web, users cannot navigate back without browser-level controls.
2. **Broken Direct Routing (S18, S22):** Direct URL navigation to `/operations/benchmark-db/form` displays GoRouter's 404 "Page Not Found", and `/tools/data-bucket/:id` renders a dead "File tidak ditemukan" screen due to missing route registration or missing in-memory route extras.
3. **Severe WCAG Contrast Failures (S23, S21):** The "Buat Laporan" button on S23 renders white text on a light grey container, failing WCAG 2.1 AA contrast requirements.
4. **Disproportionate Unconstrained Elements on Desktop (S06, S08, S12, S14):** Form submit buttons stretch to the full 1280px viewport width instead of adhering to a card-constrained layout.
5. **Systemic Mixed-Language Headings & Chips:** Almost every screen pairs English navigation titles (`Operations`, `Teams`, `Active Crew`, `Cut / Fill`, `Fuel / Lubricants`) with Indonesian body text and subtitles, while selecting "English" in Settings changes almost nothing.
6. **Data & Unit Contradictions (S11, S02):** Land Clearing summary mixes square meters (`m²`) with hectares (`Ha`) in the same card; Dashboard stat card totals double-count BCM/LCM.

---

## Findings Register

### S01 — LoginPage

#### V-001 | P2 | S01 LoginPage
**Screenshot:** `screenshots/S01-login.png`
**Category:** Typography & Copywriting — Typo in main product tagline
**Observation:** The subtitle beneath the app title "mine-flow" reads `"Sistem Monitoring & Manajamen Tambang"`. "Manajamen" is misspelled (should be "Manajemen"). As the introductory text on the first screen of the application, this spelling error is immediately visible to any first-time user.
**Severity:** P2

---

#### V-002 | P1 | S01 LoginPage
**Screenshot:** `screenshots/S01-login.png`
**Category:** Security / UX — Hardcoded production credentials pre-populated in form fields
**Observation:** The login card loads with plaintext pre-populated values: email input displays `"admin@mineflow.id"` and password displays masked bullet points for `password123`. A field crew member or foreman opening the app is presented with an administrator account already typed in, which both exposes internal credentials and bypasses individual identity selection.
**Severity:** P1

---

#### V-003 | P3 | S01 LoginPage
**Screenshot:** `screenshots/S01-login.png`, `screenshots/S01-login-dark.png`
**Category:** Theme & Visual Consistency — Unresponsive theme rendering on login card
**Observation:** The login screen does not adapt to the theme toggle or system brightness preference; it renders a fixed dark card on a dark zinc background in both light and dark mode contexts, lacking a theme toggle or brand border treatment consistent with the inner application shell.
**Severity:** P3

---

### S02 — DashboardPage

#### V-004 | P2 | S02 DashboardPage
**Screenshot:** `screenshots/S02-dashboard.png`
**Category:** Layout & Content — Dead "Akses Cepat" section with missing navigation tiles
**Observation:** The bottom section displays the heading `"Akses Cepat"` and descriptive subtitle `"Laporan, timeline, dan notifikasi"`, followed by completely empty blank space. A new user expects quick-action shortcuts or navigation cards for reports, timeline, and alerts, but the region contains zero interactive elements.
**Severity:** P2

---

#### V-005 | P2 | S02 DashboardPage
**Screenshot:** `screenshots/S02-dashboard.png`
**Category:** Localization & Terminology — Inconsistent mixed language across cards and headings
**Observation:** The stat summary cards use English titles and subtitles (`"Active Crew"` / `"0 crew today"`, `"Cut / Fill Volume"` / `"Today's total volume"`, `"Equipment Checks"` / `"0 checks today"`, `"Notifications"` / `"0 unread"`), while the section heading below is in Indonesian (`"Akses Cepat"` / `"Laporan, timeline, dan notifikasi"`), and the sidebar mixes English and Indonesian.
**Severity:** P2

---

#### V-006 | P3 | S02 DashboardPage
**Screenshot:** `screenshots/S02-dashboard.png`
**Category:** Layout & Grid Balance — Asymmetric orphan card in 3-column desktop grid
**Observation:** The dashboard stat cards are arranged in a 3-column grid. With 4 total metric cards, the first row contains three cards ("Active Crew", "Cut / Fill Volume", "Equipment Checks") while the second row contains a single orphan card ("Notifications") on the far left, leaving 66% of the row width vacant and visually unbalanced.
**Severity:** P3

---

### S03 — GroupLandingPage

#### V-007 | P2 | S03 GroupLandingPage (/tools variant)
**Screenshot:** `screenshots/S03-group-landing-tools.png`
**Category:** Layout — Single isolated card with excessive empty negative space
**Observation:** On `/tools`, the group landing screen renders only a single feature tile ("Data Bucket") in a 3-column grid layout, leaving over 70% of the screen area completely empty on 1280px desktop.
**Severity:** P2

---

#### V-008 | P2 | S03 GroupLandingPage (all variants)
**Screenshot:** `screenshots/S03-group-landing-operations.png`, `screenshots/S03-group-landing-teams.png`, `screenshots/S03-group-landing-tools.png`
**Category:** Localization & Terminology — English group headers paired with Indonesian descriptions
**Observation:** Every group landing screen pairs an English group title with an Indonesian subtitle (`"Operations"` / `"Manajemen pelacakan operasi lapangan"`, `"Teams"` / `"Kehadiran kru dan dokumentasi harian"`, `"Tools"` / `"Alat dan utilitas tambahan"`). In Teams, the tiles mix English labels (`"Attendance"`, `"Daily Log"`, `"Inventory"`, `"Equipment Check"`) with a hybrid Indonesian/English label (`"Timeline Pekerjaan"`).
**Severity:** P2

---

#### V-009 | P2 | S03 GroupLandingPage (all variants)
**Screenshot:** `screenshots/S03-group-landing-operations.png`
**Category:** Navigation & Shell State — Missing active state highlight in left sidebar
**Observation:** When navigating to group landing URLs (`/operations`, `/teams`, `/tools`), none of the sidebar items in the respective category are highlighted as active. The sidebar only highlights specific leaf routes (e.g. Dashboard), leaving the user with no visual cue in the sidebar indicating their current section.
**Severity:** P2

---

### S04 — SettingsPage

#### V-010 | P2 | S04 SettingsPage
**Screenshot:** `screenshots/S04-settings.png`
**Category:** Layout & Viewport — Destructive action card clipped below viewport boundary
**Observation:** On a standard 1280x800 desktop viewport, the bottom card (the red-tinted "Keluar / Logout" section) is cut off at the bottom edge. Users must scroll down to see the full logout card and version number, which reduces discoverability.
**Severity:** P2

---

#### V-011 | P2 | S04 SettingsPage
**Screenshot:** `screenshots/S04-settings.png`
**Category:** Localization & State — Language selector toggle does not translate interface
**Observation:** When "English" is selected in the "Bahasa / Language" segment, the rest of the Settings page remains entirely in Indonesian (`"Pengaturan"`, `"Preferensi"`, `"Dukungan"`, `"Hubungi tim support jika ada kendala teknis."`, `"Terang"`, `"Gelap"`, `"Sistem"`). The UI gives no visual feedback that translations are incomplete or that the toggle had minimal effect.
**Severity:** P2

---

#### V-012 | P3 | S04 SettingsPage
**Screenshot:** `screenshots/S04-settings.png`
**Category:** Privacy & Information Architecture — Personal contact details displayed as support channel
**Observation:** The support card displays a personal contact email (`alvin.geomatics@gmail.com`) and personal mobile phone number (`+62 851-5604-2854`) rather than an institutional or helpdesk channel (`support@mineflow.id`), exposing developer PII in the shipped UI.
**Severity:** P3

---

### S05 — AttendanceScreen

#### V-013 | P2 | S05 AttendanceScreen
**Screenshot:** `screenshots/S05-attendance-empty.png`, `screenshots/S05-attendance.png`
**Category:** Data & Workflow — Read-only list screen lacks direct inline status editing
**Observation:** The Attendance screen displays date navigation, summary metrics (`Hadir`, `Alpha`, `Sakit`, `Izin`), and search, but functions strictly as a read-only viewer. To mark or edit attendance, a supervisor must navigate away to the separate "Input Absensi" form screen.
**Severity:** P2

---

#### V-014 | P3 | S05 AttendanceScreen
**Screenshot:** `screenshots/S05-attendance-empty.png`
**Category:** Search & Field Labels — Search placeholder references technical "Kru ID"
**Observation:** The search bar placeholder text is `"Cari Kru ID atau Catatan..."`. Field supervisors searching for workers naturally search by person name (e.g. "Budi", "Joko"), but the placeholder implies search operates only on synthetic ID codes ("KRU-001").
**Severity:** P3

---

### S06 — AttendanceFormPage

#### V-015 | P2 | S06 AttendanceFormPage
**Screenshot:** `screenshots/S06-attendance-form-empty.png`
**Category:** Layout & Component Sizing — Full-screen width button on wide desktop viewport
**Observation:** The empty state action button `"Muat Daftar Kru Default"` stretches across the entire 1280px width of the content area. On desktop viewports, an unconstrained full-width button looks disproportionately stretched and violates the compact card-based framing used elsewhere in the design system.
**Severity:** P2

---

#### V-016 | P1 | S06 AttendanceFormPage
**Screenshot:** `screenshots/S06-attendance-form-empty.png`
**Category:** Functional Flow / Data Integrity — Mock roster loader in production user path
**Observation:** In the empty state, the primary call to action is `"Muat Daftar Kru Default"`, which generates synthetic test identities (`KRU-001` through `KRU-008`). A field foreman looking to input today's real attendance is offered no manual "Tambah Anggota Kru" or real user lookup action.
**Severity:** P1

---

### S07 — DailyLogListScreen

#### V-017 | P2 | S07 DailyLogListScreen
**Screenshot:** `screenshots/S07-daily-log-list.png`
**Category:** Navigation & Reporting — Misleading report action button
**Observation:** The PDF floating action button in the bottom right is intended for daily logs, but triggers the attendance report generation flow instead (`ReportType.attendance`), resulting in an mismatched document title and data type for the user.
**Severity:** P2

---

#### V-018 | P3 | S07 DailyLogListScreen
**Screenshot:** `screenshots/S07-daily-log-list.png`
**Category:** Breadcrumbs & Casing — Single-level breadcrumb path
**Observation:** The breadcrumbs read `Teams > Daily Log`. When filtering by status chips (`Draft`, `Terkirim`, `Disetujui`), the breadcrumb does not reflect the filtered context.
**Severity:** P3

---

### S08 — DailyLogFormScreen

#### V-019 | P2 | S08 DailyLogFormScreen
**Screenshot:** `screenshots/S08-daily-log-form.png`
**Category:** Navigation & Breadcrumbs — Missing "Form" breadcrumb segment and back navigation
**Observation:** When entering the Daily Log form, the breadcrumb trail remains `Teams > Daily Log` (unlike Attendance which shows `Teams > Attendance > Form`). There is no back button or breadcrumb link in the header to return to the list screen, forcing the user to use the sidebar.
**Severity:** P2

---

#### V-020 | P2 | S08 DailyLogFormScreen
**Screenshot:** `screenshots/S08-daily-log-form.png`
**Category:** Form Styling & Component Consistency — Underline input styling diverges from ForUI outlined inputs
**Observation:** The multiline input fields for `"Ringkasan Pekerjaan *"` and `"Catatan Tambahan & K3 (Safety)"` use unbordered bottom-underline text fields rather than the structured, 1px bordered `FCard`/`FTextField` containers specified in Doc 07 §3.
**Severity:** P2

---

#### V-021 | P3 | S08 DailyLogFormScreen
**Screenshot:** `screenshots/S08-daily-log-form.png`
**Category:** Layout & Spacing — Submit button stretches full width without card constraint
**Observation:** The `"Kirim Log Harian"` button spans the entire width of the page rather than adhering to a centered max-width constraint (e.g. `maxWidth: 600` or within a form card).
**Severity:** P3

---

### S09 — CutFillListScreen

#### V-022 | P2 | S09 CutFillListScreen
**Screenshot:** `screenshots/S09-cut-fill-list.png`, `screenshots/S09-cut-fill-dark.png`
**Category:** Localization & Units — Mixed language metric card labels
**Observation:** The summary card header is Indonesian (`"Rekapitulasi Volume"`), but the metric subtitles are English (`"Total BCM"`, `"Total LCM"`, `"Net Cut"`). Furthermore, the filter chips use Indonesian (`"Semua Zona"`, `"Zona"`, `"Pilih Tanggal"`).
**Severity:** P2

---

#### V-023 | P3 | S09 CutFillListScreen
**Screenshot:** `screenshots/S09-cut-fill-list.png`
**Category:** Breadcrumbs & Casing — Inconsistent spacing in breadcrumb path
**Observation:** The breadcrumbs display `Operations > Cut Fill` (without slash), while the sidebar and list title display `Cut / Fill` (with slash).
**Severity:** P3

---

### S10 — CutFillFormScreen

#### V-024 | P2 | S10 CutFillFormScreen
**Screenshot:** `screenshots/S10-cut-fill-form.png`
**Category:** Layout & Viewport — Submit action button pushed below fold on desktop
**Observation:** On 1280x800 resolution, the form fields (Tanggal, Zona, Volume Cut/Fill, Elevasi, Tipe Material, Net Volume, Catatan) take up the full vertical space, pushing the `"Simpan Pengukuran"` button completely below the bottom edge. Users must scroll down to discover and click the save button.
**Severity:** P2

---

#### V-025 | P2 | S10 CutFillFormScreen
**Screenshot:** `screenshots/S10-cut-fill-form.png`
**Category:** Navigation & Breadcrumbs — Missing "Form" breadcrumb segment
**Observation:** Like S08, the breadcrumb trail remains `Operations > Cut Fill` without indicating that the user is on an entry form screen, and lacks a back button in the header.
**Severity:** P2

---

### S11 — LandClearingListScreen

#### V-026 | P1 | S11 LandClearingListScreen
**Screenshot:** `screenshots/S11-land-clearing-list.png`
**Category:** Data & Units — Contradictory measurement units within the same summary card
**Observation:** In `"Rekapitulasi Land Clearing"`, the first two metrics (`Rencana` and `Aktual`) display values in square meters (`0.0 m²`), while the third metric (`Total`) displays values in hectares (`0.00 Ha`). Displaying disparate units side-by-side without clear conversion context causes confusion for supervisors tracking site progress.
**Severity:** P1

---

#### V-027 | P2 | S11 LandClearingListScreen
**Screenshot:** `screenshots/S11-land-clearing-list.png`
**Category:** Navigation & FAB — Mislabelled report button
**Observation:** The PDF floating action button on this screen opens `report-config` with `ReportType.cutFill` rather than a land clearing report type, generating a document titled "Laporan Volume Cut/Fill" with irrelevant earthwork columns.
**Severity:** P2

---

### S12 — LandClearingEntryScreen

#### V-028 | P2 | S12 LandClearingEntryScreen
**Screenshot:** `screenshots/S12-land-clearing-entry.png`
**Category:** Navigation & Breadcrumbs — Missing "Entry/Form" breadcrumb segment
**Observation:** The breadcrumbs display `Operations > Land Clearing` without an `> Entry` or `> Form` segment, giving no hierarchy context.
**Severity:** P2

---

#### V-029 | P2 | S12 LandClearingEntryScreen
**Screenshot:** `screenshots/S12-land-clearing-entry.png`
**Category:** Terminology & Bilingualism — Mixed English/Indonesian tab labels
**Observation:** The top tabs are labelled with bilingual parenthetical terms: `"Rencana (Plan)"` and `"Realisasi (Actual)"`, and the conversion card displays `"Plan (m²) -> Plan (Ha)"`. This contrasts with other forms that use single-language Indonesian terminology.
**Severity:** P2

---

#### V-030 | P3 | S12 LandClearingEntryScreen
**Screenshot:** `screenshots/S12-land-clearing-entry.png`
**Category:** Layout — Full-width button stretching across desktop screen
**Observation:** The `"Simpan Land Clearing"` button spans 100% of the available horizontal desktop space (1280px), creating an excessively wide touch/click target.
**Severity:** P3

---

### S13 — InventoryDashboardScreen

#### V-031 | P2 | S13 InventoryDashboardScreen
**Screenshot:** `screenshots/S13-inventory-dashboard.png`
**Category:** Layout & Overflow — Category filter chips horizontally clipped without scroll cue
**Observation:** The category filter chip row (`Semua`, `Fuel / Lubricants`, `Explosives / Blasting`, `Spare Parts`, `Consumables`, `Safety Equipment`, `Tools`, ...) extends beyond the right edge of the 1280px viewport. The last chip is clipped halfway with no scrollbar or fade gradient to indicate that additional categories exist to the right.
**Severity:** P2

---

#### V-032 | P2 | S13 InventoryDashboardScreen
**Screenshot:** `screenshots/S13-inventory-dashboard.png`
**Category:** Localization & Terminology — English category labels on Indonesian screen
**Observation:** Every category filter chip except `"Semua"` uses English industry terminology (`Fuel / Lubricants`, `Explosives / Blasting`, `Spare Parts`, `Consumables`, `Safety Equipment`, `Tools`), while the screen counter (`0 item`) and empty state message (`Belum ada item inventori`) are in Indonesian.
**Severity:** P2

---

### S14 — InventoryItemEntryScreen

#### V-033 | P2 | S14 InventoryItemEntryScreen
**Screenshot:** `screenshots/S14-inventory-item-entry.png`
**Category:** Navigation & Breadcrumbs — Missing "Form" breadcrumb segment
**Observation:** The breadcrumbs show `Teams > Inventory` with no form indicator or back navigation in the header.
**Severity:** P2

---

#### V-034 | P3 | S14 InventoryItemEntryScreen
**Screenshot:** `screenshots/S14-inventory-item-entry.png`
**Category:** Layout — Full-width submit button on wide screen
**Observation:** `"Simpan Item Inventori"` button spans the full width of the screen.
**Severity:** P3

---

### S15 — EquipmentHistoryScreen

#### V-035 | P2 | S15 EquipmentHistoryScreen
**Screenshot:** `screenshots/S15-equipment-history.png`
**Category:** Layout — Two stacked rows of filter chips consume excessive vertical space
**Observation:** The screen places two separate rows of filter chips (Row 1: Type filters `Semua Tipe`, `GNSS Receiver`, `Total Station`, `Drone / UAV`; Row 2: Status filters `Semua Status`, `Passed / Operasional`, `Flagged / Perbaikan`) directly below the search bar. This consumes significant vertical height before any list content is rendered.
**Severity:** P2

---

#### V-036 | P2 | S15 EquipmentHistoryScreen
**Screenshot:** `screenshots/S15-equipment-history.png`
**Category:** Localization & Terminology — Bilingual slash formatting in status chips
**Observation:** Status chips use English/Indonesian dual terms (`Passed / Operasional`, `Flagged / Perbaikan`), whereas other feature screens use purely Indonesian chips (`Disetujui`, `Perlu Perbaikan`).
**Severity:** P2

---

### S16 — EquipmentCheckFormScreen

#### V-037 | P1 | S16 EquipmentCheckFormScreen
**Screenshot:** `screenshots/S16-equipment-check-form.png`
**Category:** UX / Form Defaults — SOP checklist pre-populates all items as "PASS"
**Observation:** When the inspection form opens, all SOP checklist items are defaulted to "PASS", and the top status banner immediately displays `"OPERASIONAL (PASSED) — 5 dari 5 Item SOP Lolos Check"`. Pre-filling positive inspection results encourages "rubber-stamping" by equipment operators without actually performing physical checks.
**Severity:** P1

---

#### V-038 | P2 | S16 EquipmentCheckFormScreen
**Screenshot:** `screenshots/S16-equipment-check-form.png`
**Category:** Layout & Viewport — Submit button and notes pushed below fold
**Observation:** On 1280x800 resolution, the extensive SOP list pushes the notes text area and the final submit button below the fold, requiring scrolling.
**Severity:** P2

---

### S17 — BenchmarkListScreen

#### V-039 | P3 | S17 BenchmarkListScreen
**Screenshot:** `screenshots/S17-benchmark-list.png`
**Category:** Typography & Casing — Inconsistent capitalization between sidebar and breadcrumbs
**Observation:** The sidebar navigation displays `"Benchmark DB"` (uppercase "DB"), while the top breadcrumb bar displays `"Benchmark Db"` (lowercase "b").
**Severity:** P3

---

### S18 — BenchmarkFormScreen

#### V-040 | P1 | S18 BenchmarkFormScreen
**Screenshot:** `screenshots/S18-benchmark-form.png`
**Category:** Navigation & Routing — Route `/operations/benchmark-db/form` returns 404 Page Not Found
**Observation:** Navigating to the benchmark form URL (`/operations/benchmark-db/form`) renders GoRouter's unstyled 404 error page: `"Page Not Found — GoException: no routes for location: /operations/benchmark-db/form"`. The route is defined as a constant in `AppRoutes` but was not registered in `appRouter`.
**Severity:** P1

---

#### V-041 | P2 | S18 BenchmarkFormScreen
**Screenshot:** `screenshots/S18-benchmark-form.png`
**Category:** Typography & Copywriting — Misspelling in section card headers
**Observation:** Two card headers spell "Koordinat" incorrectly as `"Kordinat"` (`"Kordinat Proyeksi (UTM)"` and `"Kordinat Geografis (Otomatis)"`). Standard Indonesian spelling is "Koordinat" (with double 'o').
**Severity:** P2

---

### S19 — TimelinePage

#### V-042 | P2 | S19 TimelinePage
**Screenshot:** `screenshots/S19-timeline.png`
**Category:** UX & Capabilities — Empty state prompts user to add milestones, but no creation button exists
**Observation:** The empty state text reads `"Data akan muncul setelah Anda menambahkan milestone dan mencatat progres."`, yet the screen contains no "+ Milestone" button, FAB, or action to create a milestone.
**Severity:** P2

---

#### V-043 | P3 | S19 TimelinePage
**Screenshot:** `screenshots/S19-timeline.png`
**Category:** Localization — Untranslated date format in dropdown selector
**Observation:** The period dropdown displays dates in day/month numerical format (`28/07 - 27/08`) without year or locale month names.
**Severity:** P3

---

### S20 — DataBucketListPage

#### V-044 | P2 | S20 DataBucketListPage
**Screenshot:** `screenshots/S20-data-bucket-list.png`
**Category:** Navigation & Reporting — Misrouted report FAB
**Observation:** The PDF floating action button on Data Bucket triggers `ReportType.cutFill`, generating a Cut/Fill report rather than a geospatial file inventory catalog.
**Severity:** P2

---

### S21 — UploadFilePage

#### V-045 | P2 | S21 UploadFilePage
**Screenshot:** `screenshots/S21-upload-file.png`
**Category:** Visual State & Disabled Styling — Disabled submit button lacks contrast
**Observation:** The `"Upload ke Drive"` button is permanently disabled when no file is selected, but renders as a dark grey rectangular block with low-contrast black text, making the button label difficult to read.
**Severity:** P2

---

### S22 — FileDetailPage

#### V-046 | P1 | S22 FileDetailPage
**Screenshot:** `screenshots/S22-file-detail.png`
**Category:** Navigation & Deep Linking — Direct URL navigation fails with "File tidak ditemukan"
**Observation:** The route `/tools/data-bucket/:id` relies entirely on in-memory `extra['file']` state. Navigating directly via browser URL renders a dead screen reading `"File tidak ditemukan."` with no way to load file metadata from the repository using the `:id` parameter.
**Severity:** P1

---

### S23 — ReportConfigPage

#### V-047 | P1 | S23 ReportConfigPage
**Screenshot:** `screenshots/S23-report-config.png`
**Category:** Navigation & Shell Isolation — Fullscreen route has no back or dismiss action
**Observation:** The Report Config screen renders as an isolated full-screen page outside the navigation shell. It contains no back button, no close icon, and no header navigation. If opened, a desktop user has no UI mechanism to return to the application except the browser's native Back button.
**Severity:** P1

---

#### V-048 | P2 | S23 ReportConfigPage
**Screenshot:** `screenshots/S23-report-config.png`
**Category:** Accessibility & Contrast — "Buat Laporan" button has illegible low-contrast text
**Observation:** The `"Buat Laporan"` submit button renders white text on a light grey background, severely violating WCAG 2.1 AA contrast requirements (failing the minimum 4.5:1 ratio).
**Severity:** P2

---

### S24 — NotificationListPage

#### V-049 | P1 | S24 NotificationListPage
**Screenshot:** `screenshots/S24-notification-list.png`
**Category:** Navigation & Shell Isolation — Fullscreen page renders bare empty state with no exit navigation
**Observation:** The `/notifications` route is pushed completely outside the AppShell. When empty, it renders a completely blank black screen with only a centered bell icon and `"Tidak ada notifikasi"`. There is no app bar, no back button, no sidebar, and no close button, trapping the user on the screen.
**Severity:** P1

---

### Cross-Screen & Systemic Themes

#### V-050 | P3 | Cross-Screen (Systemic)
**Screenshot:** `screenshots/S02-dashboard-dark.png`, `screenshots/S03-group-landing-dark.png`
**Category:** Iconography — Material icon glyphs used instead of Lucide icons
**Observation:** All navigation icons in the sidebar (`groups_outlined`, `moving_outlined`, `build_outlined`, `notifications_active_outlined`, `terrain`) and action buttons use Material icon glyphs with varying line weights and filled/outlined styles, rather than the clean line-art Lucide icons specified in Doc 07 §5.
**Severity:** P3

---

## Review Completion Matrix

| Screen | Route | Screenshot Status | Visual Findings |
|---|---|---|---|
| S01 LoginPage | `/login` | Captured (Light + Dark) | V-001 (P2), V-002 (P1), V-003 (P3) |
| S02 DashboardPage | `/` | Captured (Light + Dark) | V-004 (P2), V-005 (P2), V-006 (P3) |
| S03 GroupLandingPage | `/operations`, `/teams`, `/tools` | Captured (3 groups + Dark) | V-007 (P2), V-008 (P2), V-009 (P2) |
| S04 SettingsPage | `/settings` | Captured (Light + Dark) | V-010 (P2), V-011 (P2), V-012 (P3) |
| S05 AttendanceScreen | `/teams/attendance` | Captured (Empty + Populated + Dark) | V-013 (P2), V-014 (P3) |
| S06 AttendanceFormPage | `/teams/attendance/form` | Captured (Empty + Seeded) | V-015 (P2), V-016 (P1) |
| S07 DailyLogListScreen | `/teams/daily-log` | Captured | V-017 (P2), V-018 (P3) |
| S08 DailyLogFormScreen | (Pushed from S07) | Captured | V-019 (P2), V-020 (P2), V-021 (P3) |
| S09 CutFillListScreen | `/operations/cut-fill` | Captured (Light + Dark) | V-022 (P2), V-023 (P3) |
| S10 CutFillFormScreen | (Pushed from S09) | Captured | V-024 (P2), V-025 (P2) |
| S11 LandClearingListScreen | `/operations/land-clearing` | Captured | V-026 (P1), V-027 (P2) |
| S12 LandClearingEntryScreen | (Pushed from S11) | Captured | V-028 (P2), V-029 (P2), V-030 (P3) |
| S13 InventoryDashboardScreen | `/teams/inventory` | Captured | V-031 (P2), V-032 (P2) |
| S14 InventoryItemEntryScreen | (Pushed from S13) | Captured | V-033 (P2), V-034 (P3) |
| S15 EquipmentHistoryScreen | `/teams/equipment-check` | Captured | V-035 (P2), V-036 (P2) |
| S16 EquipmentCheckFormScreen | `/teams/equipment-check/form` | Captured | V-037 (P1), V-038 (P2) |
| S17 BenchmarkListScreen | `/operations/benchmark-db` | Captured | V-039 (P3) |
| S18 BenchmarkFormScreen | `/operations/benchmark-db/form` | Captured | V-040 (P1), V-041 (P2) |
| S19 TimelinePage | `/teams/timeline` | Captured | V-042 (P2), V-043 (P3) |
| S20 DataBucketListPage | `/tools/data-bucket` | Captured | V-044 (P2) |
| S21 UploadFilePage | `/tools/data-bucket/upload` | Captured | V-045 (P2) |
| S22 FileDetailPage | `/tools/data-bucket/:id` | Captured | V-046 (P1) |
| S23 ReportConfigPage | `/reports/config` | Captured | V-047 (P1), V-048 (P2) |
| S24 NotificationListPage | `/notifications` | Captured | V-049 (P1) |
| Global Themes & Iconography | Systemic | Captured | V-050 (P3) |

---
