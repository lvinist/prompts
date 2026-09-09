# STEP-46.3 — Confirmed Finding Register

Generated: 2026-08-27
Source findings: 125 from 46.1 (F-XXX, batches A–F) + 50 from 46.2 (V-XXX)
Total working list: 175 candidates
Deduplicated working list: 96 unique issues
Confirmed: 97 | Rejected: 6 | Needs-Runtime: 6
Confirmed by severity — P1: 46 · P2: 38 · P3: 13

## Method

Every candidate was checked against the actual source file (read at the cited
lines), the router (`lib/app/router.dart`), the screenshot in `screenshots/`, and
the design spec (`architecture/07-ui-design-system.md` v0.4.0) + `overview.md`.
Verdicts are independent of Pass 1's severity. Pass 1a's batch-C over-tiering (all
18 marked P1) has been re-tiered against batches A/B/D/E/F. Where 46.1 (F-) and
46.2 (V-) describe the same defect they are merged into one CF entry citing both.

Baseline at scan time (unchanged by this pass): `flutter analyze` → 0 issues;
`flutter test` → 435 passing; `dart run tool/check_l10n_baseline.dart` → OK.

Doc-07 references below cite v0.4.0 (the on-disk version); Pass 1a cited "v0.4.0"
and Doc 07's own header reads v0.3.0 with a v0.4.0 row in its Version Log — same doc.

---

## Confirmed Findings (fix in 46.4)

### Group 1 — Authentication & session (all P1)

### CF-001 | P1 | S01 LoginPage — login performs no authentication
**Sources:** F-A01 (46.1)
**File:** `lib/features/auth/presentation/pages/login_page.dart:21-23`
**Confirmed:** Yes. `_login()` is exactly `context.go(AppRoutes.dashboard)` — it never reads the controllers, never calls `AuthRepository.signIn`, never inspects a result. Every downstream screen runs with no Supabase session, so RLS/role visibility cannot work. This is the root of the whole empty-attribution / no-role-gate class below.
**Fix:** Wire `_login` to `AuthRepository.signIn(email, password)`; on success store the session and route to dashboard, on failure surface an error. Introduce a small auth cubit/state so the button can show submitting/failed (folds in CF-003). Gate the shell routes on an authenticated session via the router `redirect` (the `router.dart:82-84` comment already reserves this).
**Test tier:** Widget test — mount LoginPage with a mocked AuthRepository; assert signIn is called with the entered credentials and that a failed result shows an error and does not navigate.

### CF-002 | P1 | S01 LoginPage — hardcoded admin credentials pre-filled
**Sources:** F-A02 (46.1), V-002 (46.2)
**File:** `lib/features/auth/presentation/pages/login_page.dart:18-19`
**Confirmed:** Yes. `TextEditingController(text: 'admin@mineflow.id')` and `text: 'password123'` ship a real admin credential in plaintext in the widget constructor; it survives into the release bundle. Distinct from CF-001: fixing auth wiring alone leaves the shipped credential.
**Fix:** Remove both initial `text:` values (empty controllers). If a dev convenience default is wanted, gate it behind `kDebugMode` + a `--dart-define`, never a literal in the constructor.
**Test tier:** Widget test — pump LoginPage; assert both fields render empty. Static guard optional (grep for the literal in a CI check).

### CF-003 | P1 | S01 LoginPage — no validation / loading / error state
**Sources:** F-A03 (46.1, was P2)
**File:** `lib/features/auth/presentation/pages/login_page.dart:70-89`
**Confirmed:** Yes, re-tiered to P1 because it is inseparable from CF-001: once a real network call is wired, the button (never disabled, no validator, no in-flight or error surface) leaves the user with a frozen control and silence on a wrong password.
**Fix:** Add empty-field validators, disable `FButton` while submitting, show a spinner in-flight and an error message on failure — implemented via the auth state introduced in CF-001.
**Test tier:** Widget test — assert button disabled on empty fields; assert submitting shows a disabled/spinner state and a rejected credential shows an error.

### CF-004 | P1 | S04 SettingsPage — logout does not terminate the session
**Sources:** F-A15 (46.1)
**File:** `lib/features/settings/presentation/pages/settings_page.dart:326-328`
**Confirmed:** Yes. After the confirm dialog, the handler only `context.go(AppRoutes.login)`. `AuthRepository.signOut()` exists and is never called; cached role in secure storage is not cleared. On a shared field device the session survives logout, and CF-001 then readmits the next person into it.
**Fix:** In `_confirmLogout`, await `AuthRepository.signOut()` (and clear secure-storage role/token) before navigating; handle/await failure. Pairs with CF-001's auth wiring.
**Test tier:** Widget test — mock AuthRepository; confirm logout calls signOut before routing to /login.

### CF-005 | P1 | S04 SettingsPage — profile shows a hardcoded name and role
**Sources:** F-A16 (46.1)
**File:** `lib/features/settings/presentation/pages/settings_page.dart:383,390`
**Confirmed:** Yes. `_ProfileCard` renders the literals `'Pengguna'` and `'Foreman'` (both commented "Placeholder — will come from auth profile"). `UserEntity` has a real `role`, so a supervisor is told they are a Foreman — it actively misinforms about permissions and looks correct for exactly one role.
**Fix:** Read name and role from the authenticated user (available once CF-001 lands) and render those; while auth is pending show a neutral placeholder, not a fabricated role.
**Test tier:** Widget test — pump SettingsPage with a mocked auth user of role supervisor; assert the card shows that role, not 'Foreman'.

---
### Group 2 — Empty-string identity from the router (all P1)

The router passes `foremanId: ''` at `router.dart:245, 255, 348, 368` (and the equipment form defaults `?? ''` at 379). An empty string is **not null**, so it becomes both an active read filter and a blank write attribution. These CF entries are the individual sites of that one root cause; the router fix is shared.

### CF-006 | P1 | S07 DailyLogListScreen — empty foremanId hides other users' logs
**Sources:** F-B01 (46.1)
**File:** `lib/app/router.dart:348`; `lib/features/daily_log/data/repositories/daily_log_repository_impl.dart:49`
**Confirmed:** Yes. Repo filter is `if (foremanId != null && dto.foremanId != foremanId) return false;` — with `''` it rejects every record whose foremanId is anything else. Looks fine locally only because logs written through S08 also carry `''` (CF-007).
**Fix:** Pass the authenticated user's id (or null for supervisor "see all") from the router builder instead of `''`. Depends on CF-001. Until auth lands, pass `null` so the list is unfiltered rather than filtered-to-empty.
**Test tier:** Widget test — mount DailyLogListScreen with a mocked repo; assert a non-empty/`null` foremanId is used and that a real-author record is not filtered out.

### CF-007 | P1 | S08 DailyLogFormScreen — logs persisted with empty author
**Sources:** F-B02 (46.1)
**File:** `lib/features/daily_log/presentation/bloc/daily_log_bloc.dart:70-77`
**Confirmed:** Yes. New `DailyLog(... foremanId: event.foremanId ...)` where event.foremanId is `''` from the router. The formal operational + K3 record is stored with no author; unattributable once auth lands. Write-side twin of CF-006 — fix together.
**Fix:** Populate foremanId from the authenticated user at creation. Depends on CF-001.
**Test tier:** Widget test — dispatch the create path with a simulated user; assert the persisted log carries that user's id.

### CF-008 | P1 | S08 DailyLogFormScreen — draft resumption keyed on empty id leaks drafts
**Sources:** F-B03 (46.1)
**File:** `lib/features/daily_log/presentation/bloc/daily_log_bloc.dart:64-68`
**Confirmed:** Yes. `getDraftLogForForeman(foremanId: '')` resolves "my draft" to "the one empty-author draft for today". On a shared tablet the second foreman opens the first's unsubmitted draft (summary + safety notes) and overwrites it on edit.
**Fix:** Key draft lookup on the real user id (CF-001). Same router fix; verify no cross-user draft is returned when ids differ.
**Test tier:** Widget/bloc test — two distinct user ids must not resolve to each other's draft.

### CF-009 | P1 | S09 CutFillListScreen / S10 form — empty surveyor attribution on cut/fill
**Sources:** F-C17 (46.1)
**File:** `lib/app/router.dart:245`; `lib/features/tracking/presentation/bloc/cut_fill_bloc.dart:82` (`measuredBy: event.foremanId`)
**Confirmed:** Yes. `foremanId: ''` flows S09→S10→bloc and is stored as `measuredBy: ''`; nothing on screen shows/requests the surveyor. Core survey record becomes unattributable. `zoneId` also defaults to `''`.
**Fix:** Pass authenticated user id as foremanId from the router (CF-001). Ensure `zoneId` empty-string default is handled by CF-018 validation.
**Test tier:** Widget test — assert the bloc receives a non-empty measuredBy for a simulated foreman.

### CF-010 | P1 | S11 list / S12 LandClearingEntryScreen — empty cleared-by attribution
**Sources:** F-C18 (46.1)
**File:** `lib/app/router.dart:255`; `lib/features/tracking/presentation/bloc/land_clearing_bloc.dart:84` (`clearedBy: event.foremanId`)
**Confirmed:** Yes. Same defect on the clearing side: `foremanId: ''` → `clearedBy: ''` on every record created from the tab form.
**Fix:** As CF-009, for the land-clearing path.
**Test tier:** Widget test — assert non-empty clearedBy for a simulated foreman.

---

### Group 3 — Data correctness: volume & area (all P1)

### CF-011 | P1 | S02 DashboardPage — headline volume sums BCM + LCM (double-counts)
**Sources:** F-A05 (46.1), V-020-theme/V-006-adjacent (46.2 §Data contradictions)
**File:** `lib/app/presentation/bloc/dashboard_cubit.dart:105-109`
**Confirmed:** Yes. `total += r.bcmVolume + r.lcmVolume` sums two measurement bases of the same material; the result is surfaced as the dashboard "Cut / Fill Volume" headline, overstating by ~the swell factor. Same class as CF-013/CF-014.
**Fix:** Product decision required — report BCM only, LCM only, or show both separately. Do NOT silently change the formula; pick one and label it. Recommend BCM (in-situ) as the single headline with a clear label, matching the survey record's primary basis.
**Test tier:** Widget test — pump DashboardCubit with known records; assert the emitted cutFillVolume equals the chosen basis, not the sum. (Requires an ADR / user decision on the basis.)

### CF-012 | P1 | S02 DashboardPage — "Active Crew" counts every attendance record
**Sources:** F-A06 (46.1)
**File:** `lib/app/presentation/bloc/dashboard_cubit.dart:83-92`
**Confirmed:** Yes. `_fetchActiveCrewCount` returns `records.length` over `getAttendanceForDate`, so absent/sick/leave increment "Active Crew". `AttendanceStatus` has present/absent/sick/leave.
**Fix:** Count only records with `status == AttendanceStatus.present` (decide whether "active" also includes any on-site status; default present-only).
**Test tier:** Widget test — pump with a mix of statuses; assert the count equals the present-only subset.

### CF-013 | P1 | S11 LandClearingSummaryCard — Total labelled Ha but never converted, and sums plan+actual
**Sources:** F-C01 + F-C02 (46.1), V-026 (46.2)
**File:** `lib/features/tracking/presentation/widgets/clearing_summary_card.dart:68-76`
**Confirmed:** Yes (both defects, merged). Value is `(totalPlanArea + totalActualArea).toStringAsFixed(2)` suffixed `Ha` while the inputs are m² (fed raw from the bloc). Two errors at once: no `/10000` (off by 10,000×) and plan+actual is not a meaningful quantity. Dead getters `totalPlanAreaHa`/`totalActualAreaHa` (lines 17-20) show the conversion was intended. Same bug is baked into the entity: `LandClearingRecord.totalArea => planArea + actualArea` (`land_clearing_record.dart:39`) and `totalAreaHa` (42).
**Fix:** Decide the correct "Total" (recommend: total **actual** cleared, converted to Ha via `/10000`, OR a plan-vs-actual variance). Fix the card to use the correct value/unit and remove or repurpose the dead getters. Fix or remove the misleading `totalArea`/`totalAreaHa` on the entity so no other consumer inherits it.
**Test tier:** Widget test — pump ClearingSummaryCard with known m² values; assert the Total stat shows the converted Ha figure (and the chosen semantics), not the raw m² sum.

### CF-014 | P1 | S09 volume summary + S10 form — BCM/LCM conflated into a meaningless "Net"
**Sources:** F-C08 + F-C09 (46.1), V-022 (46.2)
**File:** `lib/features/tracking/presentation/widgets/volume_summary_card.dart:43-72`; `lib/features/tracking/presentation/bloc/cut_fill_bloc.dart:47-49`; `lib/features/tracking/presentation/pages/cut_fill_form_screen.dart:249-280`
**Confirmed:** Yes. Bloc computes `totalNet = totalBcm - totalLcm` and the card renders it as the bold `Net Cut/Fill` headline; subtracting loose from bank measure has no physical meaning. The form labels BCM as "Volume Cut" and LCM as "Volume Fill", conflating measurement basis with earthwork operation. Parameter names (`totalCutM3`) disagree with rendered labels (`Total BCM`), hiding it.
**Fix:** Product decision required (same axis as CF-011): the data model is BCM/LCM (measurement basis), not cut/fill (operation). Recommend: relabel the form fields to "Volume (BCM)" / "Volume (LCM)" so they stop implying cut vs fill; remove the invalid `totalNet = bcm - lcm` or replace it with a swell-factor-based derived figure only if the domain defines one; relabel the summary card accordingly. Coordinate with CF-011 in one ADR.
**Test tier:** Widget test — assert the summary card no longer presents `bcm - lcm` as a headline "net"; assert form labels match the chosen model. Requires the ADR.

---
### Group 4 — Hardcoded / stub data on the real user path (all P1)

### CF-015 | P1 | S06 AttendanceFormPage — synthetic crew roster seeded as real records
**Sources:** F-B05 (46.1), V-016 (46.2)
**File:** `lib/features/attendance/presentation/pages/attendance_form_page.dart:165-181`
**Confirmed:** Yes. The empty state's only CTA `'Muat Daftar Kru Default'` dispatches `SeedDefaultRosterEvent` generating `KRU-001…KRU-008` — fabricated ids matching no `UserEntity`, count arbitrary — and they flow into the dashboard crew count and reports.
**Fix:** Replace with loading the actual site roster from the users/crew source; provide a real "add crew member" / lookup action. If a seed remains for dev, gate behind `kDebugMode`.
**Test tier:** Widget test — assert the empty state offers a real-roster action, not synthetic id generation; integration test that seeded rows are not fabricated in a non-debug build.

### CF-016 | P1 | S09/S11 — zone filter hardcodes the literal 'Zona A'
**Sources:** F-C04 + F-C05 (46.1)
**File:** `lib/features/tracking/presentation/pages/cut_fill_list_screen.dart:253-272`; `lib/features/tracking/presentation/pages/land_clearing_list_screen.dart:252-271`
**Confirmed:** Yes. The "Zona" chip toggles the string `'Zona A'` into `_selectedZoneId` and sends it as a real zone id filter. Zones are UUID-shaped elsewhere, so on any real site the query returns nothing and the screen shows an empty list + `0.0` summary indistinguishable from "no data".
**Fix:** Replace the toggle with a real zone picker (the `ZonePicker`/`ZoneCubit` already used elsewhere) that filters by actual zone id. Apply to both screens.
**Test tier:** Widget test — assert selecting a zone dispatches the load with a real zone id, not the literal 'Zona A'.

### CF-017 | P1 | S16 EquipmentCheckFormScreen — SOP checklist defaults every item to PASS
**Sources:** F-D03 (46.1), V-037 (46.2)
**File:** `lib/features/equipment_check/presentation/bloc/equipment_check_bloc.dart:29-116` (`getDefaultChecklist`, every `CheckItem(isPassed: true)`)
**Confirmed:** Yes. All items constructed `isPassed: true`; submit writes state as-is with no requirement any item was touched, so "5/5 Lolos" can be filed without inspecting. Inverts the control's purpose and produces confidently-wrong safety data.
**Fix:** Default every `CheckItem` to an un-answered state (introduce a tri-state or `isPassed` nullable / `bool? isPassed`) and require an explicit per-item verdict before submit is enabled. Banner should not read "PASSED" until all items answered.
**Test tier:** Widget test — assert submit is disabled until every item has an explicit verdict; assert a fresh form shows no items pre-passed.

### CF-018 | P1 | S21 UploadFilePage — fallback GoogleDriveService built with empty credentials
**Sources:** F-F04 (46.1)
**File:** `lib/features/data_bucket/presentation/pages/upload_file_page.dart:49-55`; caller `data_bucket_list_page.dart:120-128` passes no driveService
**Confirmed:** Yes. When `driveService` is null the page constructs `GoogleDriveService(serviceAccountEmail:'', serviceAccountKey:'', driveFolderId:'')`; the in-app caller never supplies one, so the production path always uses empty creds and every upload fails at the network boundary as a raw snackbar. Sibling repos resolve from `appServices` and throw `UnimplementedError` when unwired.
**Fix:** Resolve from `appServices?.driveService` (add it to AppServices if missing) and throw `UnimplementedError` when unwired, matching `_defaultDataBucketRepository`. Do not fabricate an empty-credential client.
**Test tier:** Widget test — assert the page resolves the injected/app-services driveService and does not silently build an empty-credential instance. (Actual Drive auth is Needs-Runtime — see NR-004.)

---

### Group 5 — Destructive actions without confirmation / role gate

### CF-019 | P1 | S13 InventoryDashboardScreen — delete with no confirm / role gate
**Sources:** F-D01 (46.1)
**File:** `lib/features/tracking/presentation/pages/inventory_dashboard_screen.dart:427-431`
**Confirmed:** Yes. `onDelete` dispatches `DeleteInventoryItemEvent` immediately — no dialog, no undo, no role check, no acknowledgement.
**Fix:** Add a confirm dialog (pattern exists in SettingsPage) and a supervisor role gate before dispatching delete.
**Test tier:** Widget test — assert delete requires confirmation and is gated for non-supervisor roles.

### CF-020 | P1 | S15 EquipmentHistoryScreen — delete of a safety record, unconfirmed, bypasses bloc
**Sources:** F-D02 (46.1)
**File:** `lib/features/equipment_check/presentation/pages/equipment_history_screen.dart:307-314`
**Confirmed:** Yes. `onDelete` awaits `widget.repository.deleteEquipmentCheck` directly (bypassing the bloc), no confirm, no role check, no try/catch — a thrown error is unhandled and a failed delete looks like a broken button. Deletes a safety inspection record.
**Fix:** Route delete through the bloc with a confirm dialog, role gate, loading + error handling.
**Test tier:** Widget test — assert confirmation + role gate; bloc test — assert failure surfaces an error state.

### CF-021 | P1 | S07 DailyLogListScreen — delete of an operational log, unconfirmed, ungated
**Sources:** F-B06 (46.1)
**File:** `lib/features/daily_log/presentation/pages/daily_log_list_screen.dart:471-475`
**Confirmed:** Yes. Single tap dispatches `DeleteDailyLogEvent`, including submitted/approved logs which the form otherwise makes read-only. No confirm, no undo, no role check.
**Fix:** Confirm dialog + role gate; additionally block deletion of submitted/approved logs (or restrict to supervisor).
**Test tier:** Widget test — assert confirmation, role gate, and that a submitted/approved log cannot be deleted by a non-supervisor.

### CF-022 | P1 | S09 CutFillListScreen — delete of a measurement, unconfirmed, ungated
**Sources:** F-C06 (46.1)
**File:** `lib/features/tracking/presentation/pages/cut_fill_list_screen.dart:418-422`; bloc `cut_fill_bloc.dart:230-250`
**Confirmed:** Yes. `onDelete` dispatches `DeleteCutFillRecordEvent` immediately; bloc deletes then re-loads with no acknowledgement. Cut/fill is the core survey record.
**Fix:** Confirm dialog + role gate; emit an acknowledgement.
**Test tier:** Widget test — assert confirmation + gate.

### CF-023 | P1 | S11 LandClearingListScreen — delete of a clearing record, unconfirmed, ungated
**Sources:** F-C07 (46.1)
**File:** `lib/features/tracking/presentation/pages/land_clearing_list_screen.dart:416-420`
**Confirmed:** Yes. Same pattern as CF-022 on the clearing list.
**Fix:** Confirm dialog + role gate.
**Test tier:** Widget test — assert confirmation + gate.

### CF-024 | P1 | S20 DataBucketListPage — Drive-file delete has no role gate; swipe copy understates it
**Sources:** F-F07 (46.1)
**File:** `lib/features/data_bucket/presentation/pages/data_bucket_list_page.dart:360-364`; `file_card.dart:50,66`
**Confirmed:** Yes. A confirm dialog exists (better than the others) but there is no role check — any role, incl. crew, can permanently delete a shared Drive file — and the swipe-path copy `'Yakin ingin menghapus "..."?'` omits that the file is removed from Google Drive (the detail page's dialog says so). Not recoverable in-app.
**Fix:** Add a supervisor role gate; make the swipe confirmation copy state Drive removal explicitly (match the detail page).
**Test tier:** Widget test — assert role gate; assert swipe confirmation mentions Drive.

---
### Group 6 — Mislabelled report FABs (ReportType has only attendance/cutFill/inventory)

`ReportType` (`report_type.dart`) has exactly three members. Five FABs request a type that does not match their own label. This needs one product decision: add report types (daily-log, land-clearing, equipment, benchmark, data-bucket) or remove the mismatched buttons. Recorded per-site; the decision is shared.

### CF-025 | P1 | S07 DailyLogListScreen — "Daily Log Report" button requests attendance
**Sources:** F-B07 (46.1), V-017 (46.2)
**File:** `lib/features/daily_log/presentation/pages/daily_log_list_screen.dart:115-119`
**Confirmed:** Yes. FAB labelled `'Buat Laporan Log Harian'` passes `ReportType.attendance`; trailing comment admits the mismatch was carried forward.
**Fix:** Per the shared decision — add a `dailyLog` ReportType or remove the button.
**Test tier:** Widget test — assert the FAB passes a type whose displayName matches its label (or is absent).

### CF-026 | P1 | S11 LandClearingListScreen — "Land Clearing Report" button requests cutFill
**Sources:** F-C03 (46.1), V-027 (46.2)
**File:** `lib/features/tracking/presentation/pages/land_clearing_list_screen.dart:101-109`
**Confirmed:** Yes. Semantics label `'Buat Laporan Land Clearing'` but `extra: ReportType.cutFill`.
**Fix:** Add `landClearing` type or remove the button.
**Test tier:** Widget test — as CF-025.

### CF-027 | P1 | S15 EquipmentHistoryScreen — "Equipment Inspection Report" button requests inventory
**Sources:** F-D05 (46.1)
**File:** `lib/features/equipment_check/presentation/pages/equipment_history_screen.dart:337-340`
**Confirmed:** Yes. FAB `'Buat Laporan Inspeksi Peralatan'` passes `ReportType.inventory`.
**Fix:** Add `equipmentCheck` type or remove the button.
**Test tier:** Widget test — as CF-025.

### CF-028 | P1 | S17 BenchmarkListScreen — "Benchmark Report" button requests inventory
**Sources:** F-E07 (46.1)
**File:** `lib/features/benchmark/presentation/pages/benchmark_list_screen.dart:89-93`
**Confirmed:** Yes. FAB `'Buat Laporan Benchmark'` passes `ReportType.inventory`; comment admits the mapping is arbitrary.
**Fix:** Add a benchmark type or remove the button.
**Test tier:** Widget test — as CF-025.

### CF-029 | P1 | S20 DataBucketListPage — "Data Bucket Report" button requests cutFill
**Sources:** F-F02 (46.1), V-044 (46.2)
**File:** `lib/features/data_bucket/presentation/pages/data_bucket_list_page.dart:101-113`
**Confirmed:** Yes. FAB announced "Create Data Bucket Report" opens a cut/fill report. The two domains are unrelated — least defensible of the five.
**Fix:** Remove the report button from the file browser (recommended) or add a data-bucket type.
**Test tier:** Widget test — as CF-025.

---

### Group 7 — Reporting & routing dead-ends

### CF-030 | P1 | S23 ReportConfigPage — no navigation entry; unreachable on fresh load; drops shell
**Sources:** F-F01 (46.1), V-047 (46.2)
**File:** `lib/app/router.dart:426-442`; shell `app_shell.dart` `_kSidebarSections` (no Reports item)
**Confirmed:** Yes. `/reports/config` is a standalone route outside every `StatefulShellBranch`, with no sidebar/bottom-nav entry (verified: `_kSidebarSections` at app_shell.dart:73 has no Reports item). Reachable only via per-feature FABs; a fresh load / bookmark hits the null-extra fallback text and cannot recover, and pushing outside the shell drops the sidebar on web. The null fallback itself is currently unreachable from in-app nav (all 8 callers pass a type) — the finding is the missing entry + shell isolation, not the fallback.
**Fix:** Give Reports a shell branch (or a first-class entry that carries a ReportType picker), so it is reachable without an unrelated feature screen and retains the shell. Add a report-type selection landing rather than depending on `extra`.
**Test tier:** Widget/integration test — assert a Reports entry exists in the shell and navigating to it (without extra) renders a usable page, not the fallback text.

### CF-031 | P1 | S22 FileDetailPage — `:id` route not restorable (deep-link dead end)
**Sources:** F-F03 (46.1), V-046 (46.2)
**File:** `lib/app/router.dart:178-196`
**Confirmed:** Yes. The route declares `:id` and never reads `state.pathParameters['id']`; the page is rebuilt purely from in-memory `extra['file']`. On reload/bookmark/shared link `extra` is gone → "File tidak ditemukan." with no recovery. In practice reached only via `Navigator.push` from the list, so the route is effectively write-only.
**Fix:** In the route builder, when `extra['file']` is null, fetch the file by `state.pathParameters['id']` from `DataBucketRepository` (extra as fast path). Add a loading/error state.
**Test tier:** Widget test — build the route with only an id (no extra) and a mocked repo; assert it fetches by id and renders the file, not the dead-end text.

### CF-032 | P1 | S17/S19/S24 — screen-level actions vanish on the web/desktop layout
**Sources:** F-E04 (46.1), V-042-adjacent (46.2)
**File:** `benchmark_list_screen.dart:64-77`; `timeline_page.dart:91-115`; `notification_list_page.dart:48-83` (all `width > 800 ? null : AppBar(actions: [...])`)
**Confirmed:** Yes. Above 800dp the AppBar is null (shell provides a header), but real non-duplicated actions live in `actions:` and are lost: S24 loses "Tutup Semua" (only bulk-dismiss), S19 loses refresh, S18/benchmark form loses "Batal". Nothing in the shell replaces them, so the supervisor (web) surface loses these controls entirely.
**Fix:** Move these actions into the page body (a header row inside the content) or into the shell header so they persist on the desktop layout. Apply at all three sites.
**Test tier:** Widget test at 1280dp — assert each action (dismiss-all, refresh, cancel) is present and tappable.

---
### Group 8 — Forms: validation, edit-load, and error-retry defects

### CF-033 | P1 | S18 BenchmarkFormScreen — CRS/UTM zone selected but never persisted
**Sources:** F-E01 (46.1)
**File:** `benchmark.dart:22-34` (entity has no CRS field); `benchmark_form_screen.dart:252-257,440-447`
**Confirmed:** Yes. `Benchmark` entity fields are id/bmId/northing/easting/orthoHeight/code/orde/geom/latitude/longitude/ellipsHeight/status — no CRS/zone. The form's `_crsOptions` selection lives only in transient form state and is discarded on save. A UTM N/E pair without its zone is ambiguous across the six offered zones; reopening re-derives lat/lon from a defaulted CRS, silently rewriting coordinates.
**Fix:** Add a `crsIdentifier` (or utmZone) field to the `Benchmark` entity + DTO + migration/contract type, persist it on save, and use the stored value when reopening rather than a default. (Schema change — coordinate with data-model doc; may need an ADR.)
**Test tier:** Widget/bloc test — save a benchmark with a chosen CRS; assert it round-trips and reopening does not change lat/lon. Static: contract type includes the new column.

### CF-034 | P1 | S18 BenchmarkFormScreen — no validation; unparseable coords silently discarded; double-submit
**Sources:** F-E06 (46.1)
**File:** `benchmark_form_screen.dart:73-99,392-400`
**Confirmed:** Yes. No `Form`/validator; submit has no guard; numeric listeners use `if (parsed != null)` (keep prior value on failure). A benchmark can save with blank bmId, 0/0 coords, no elevation; a mistyped coord leaves the field showing one value and the bloc holding another; double-tap dispatches `SubmitBenchmark` twice.
**Fix:** Add a `Form` + validators (required bmId, valid numeric coords), disable submit while saving, and clear the bloc value when a field is emptied/invalid (don't silently retain). Same discard idiom recurs in inventory/cut-fill — fix the class.
**Test tier:** Widget test — assert save is blocked with invalid/empty required fields; assert clearing a coord clears the stored value; assert submit disabled while saving.

### CF-035 | P1 | S18 BenchmarkFormScreen — edit mode drops zero/negative elevations
**Sources:** F-E05 (46.1)
**File:** `benchmark_form_screen.dart:414-430`
**Confirmed:** Yes. `_orthoHeightController.text = form.orthoHeight > 0 ? ... : ''` (same for ellipsHeight, and the `> 0` guard on northing/easting). Zero and negative elevations are legitimate (Indonesian geoid separation is often negative; sea-level = 0); the guard blanks them on edit, and with CF-034's discard idiom the blank does not clear the bloc, so display and stored value disagree.
**Fix:** Populate controllers from the actual value regardless of sign (format all real numbers, only blank a genuine null/unset). Remove the `> 0` guards.
**Test tier:** Widget test — open a benchmark with orthoHeight = 0 and ellipsHeight = -12.3; assert both fields show the real values.

### CF-036 | P1 | S10 CutFillFormScreen — validation declared, never runs
**Sources:** F-C15 (46.1)
**File:** `cut_fill_form_screen.dart:178-180,444-459`
**Confirmed:** Yes. `_formKey` attached but `validate()` never called; no field has a validator; save dispatches unconditionally. A zone-less (`zoneId: ''`), zero-volume, material-less record can persist and enter totals/reports.
**Fix:** Call `_formKey.currentState!.validate()` before dispatching save; add validators (required zone/material, at least one non-zero volume as the domain dictates).
**Test tier:** Widget test — assert save blocked on an untouched form; assert a valid form saves.

### CF-037 | P1 | S12 LandClearingEntryScreen — validation declared, never runs
**Sources:** F-C16 (46.1)
**File:** `land_clearing_entry_screen.dart:75,182-183,622-639`
**Confirmed:** Yes. Same as CF-036 on the clearing form: decorative `Form`, no `validate()`, no validators; can save with 0/0 areas, `zoneId: ''`, `method: null`.
**Fix:** Wire `validate()` + validators (required zone/method, non-zero area per domain).
**Test tier:** Widget test — as CF-036.

### CF-038 | P1 | S14 InventoryItemEntryScreen — save performs no validation
**Sources:** F-D06 (46.1)
**File:** `inventory_bloc.dart:184-210`; screen `inventory_item_entry_screen.dart:51,259-260`
**Confirmed:** Yes. `_onSaveItem` goes straight to `saveInventoryItem` with no checks; `_formKey` present but `validate()` never called; no validators. An untouched form saves a nameless, zero-quantity row.
**Fix:** Call `validate()` before save; add validators (required name, non-negative quantity, required category via CF-054).
**Test tier:** Widget test — assert save blocked on blank name / invalid quantity.

### CF-039 | P1 | S16 EquipmentCheckFormScreen — no validation; serial optional; inspection filed against no unit
**Sources:** F-D04 (46.1)
**File:** `equipment_check_form_screen.dart:173-181,237-257`
**Confirmed:** Yes. No `Form`/validator; serial-number field optional; submit gated only on `isSubmitting`. `EquipmentCheck.serialNumber` nullable; `_onSubmitEquipmentCheck` saves with no checks → a record not tied to any physical unit, surfacing as an untraceable row in history search.
**Fix:** Require a serial number (validator or explicit non-empty guard) before submit; pairs with CF-017 (require per-item verdicts).
**Test tier:** Widget test — assert submit blocked without a serial number.

### CF-040 | P1 | S10 CutFillFormScreen — elevation field not loaded on edit; null can't overwrite
**Sources:** F-C10 (46.1)
**File:** `cut_fill_form_screen.dart:307-317`
**Confirmed:** Yes. The elevation `TextField` has no controller/initialValue, so an existing `record.elevationChange` renders blank on edit; `copyWith` uses `elevationChange ?? this.elevationChange` and the listener passes parsed `null` through, so null never overwrites. Existing value invisible and can't be cleared; typing silently replaces an unseen value.
**Fix:** Give the field a controller seeded from `record.elevationChange`; allow an explicit clear to set null (distinguish "unchanged" from "cleared").
**Test tier:** Widget test — open a record with an elevation; assert the field shows it and can be edited/cleared.

### CF-041 | P1 | S10/S12 — error-state retry dispatches the wrong (inert) action
**Sources:** F-C11 + F-C12 (46.1)
**File:** `cut_fill_form_screen.dart:128-156`; `land_clearing_entry_screen.dart:135-163`
**Confirmed:** Yes. In the `CutFillError`/`LandClearingError` state (init failed → no form state), "Coba Lagi" dispatches `SaveCutFillRecordEvent` / `SaveLandClearingRecordEvent`, whose handlers early-return `if (state is! ...FormState)`. So retry does nothing; on `width > 800` there's no AppBar back either. Correct action is re-dispatching the Initialize event.
**Fix:** Retry should re-dispatch `InitializeCutFillFormEvent` / `InitializeLandClearingFormEvent`. Apply to both.
**Test tier:** Widget test — from the error state, tapping retry re-initializes (mock repo returns success on second call → form renders).

### CF-042 | P2 | S08 DailyLogFormScreen — error-state retry dispatches auto-save instead of re-init
**Sources:** F-B12 (46.1)
**File:** `daily_log_form_screen.dart:134-141`
**Confirmed:** Yes. In `DailyLogError` (no form state) the retry dispatches `AutoSaveDraftEvent`. Same class as CF-041 (kept P2 per Pass-1a batch-B tiering; it's a load-retry dead-end, no data loss).
**Fix:** Re-dispatch `InitializeDailyLogFormEvent`.
**Test tier:** Widget test — as CF-041.

### CF-043 | P1 | S12 LandClearingEntryScreen — free-text method into an enumerated field
**Sources:** F-C13 (46.1)
**File:** `land_clearing_entry_screen.dart:310-331` (and duplicate at 499-520)
**Confirmed:** Yes. `_clearingMethods` is a fixed 3-item list but `onCreateNew` feeds arbitrary text into `record.method` with no normalisation/trim/persistence; duplicated on the Actual tab into the same field. Guarantees category drift and can trip a backend enum/check constraint (raw exception in a snackbar).
**Fix:** Constrain method to the enumerated set (or persist new options deliberately with normalisation); use one shared control, not two independent free-text entries into the same field.
**Test tier:** Widget test — assert method selection is constrained; assert both tabs edit one normalised value.

### CF-044 | P1 | S12 LandClearingEntryScreen — Plan and Actual tabs edit the same date/zone
**Sources:** F-C14 (46.1)
**File:** `land_clearing_entry_screen.dart:184-209,216-293,405-482`
**Confirmed:** Yes. Both tabs render the same `record.clearingDate` picker and `ZonePicker(record.zoneId)` dispatching the same events; only planArea/actualArea (and method, per CF-043) differ. Editing the date/zone on Actual rewrites Plan and vice-versa — users believe they recorded a plan-vs-actual date variance the model can't hold.
**Fix:** Either share date/zone once (outside the tabs, making clear they're common) or add separate plan/actual date/zone fields to the model if a variance is intended. Product decision on which; recommend making date/zone a single shared section above the tabs to match the current data model.
**Test tier:** Widget test — assert date/zone appear once (shared) OR that plan and actual dates are independent, per the chosen model.

### CF-045 | P1 | S21 UploadFilePage — zone required but never validated; label only shows while uploading
**Sources:** F-F05 (46.1)
**File:** `upload_file_page.dart:278-296,158-159`
**Confirmed:** Yes. The `'Zona *'` required label renders only `if (isUploading)` (when the picker is gone); in the editable state the picker has no label/marker. `_submitUpload` calls `validate()` but `ZonePicker` isn't a `FormField`, so zone is never validated — a file uploads with no zone, unfilterable and unattributable.
**Fix:** Show the required label with the picker in the editable state; validate `_selectedZoneId != null` before upload (guard or wrap the picker in a FormField).
**Test tier:** Widget test — assert upload blocked with no zone; assert the required label shows with the picker.

---
### Group 9 — State / lifecycle correctness (P2)

### CF-046 | P2 | S24 NotificationListPage — critical & warning render identically; title uses primaryForeground
**Sources:** F-E02 + F-E03 (46.1), V-049-adjacent (46.2)
**File:** `notification_list_page.dart:278-309` (color helpers), `:378-385` (title)
**Confirmed:** Yes (both, merged). `_iconColor`/`_bgColor`/`_borderColor` map both `critical` and `warning` to `primary` (only a 0.1 vs 0.05 alpha differs — imperceptible), so severity is not communicated; `destructive` is available and used for the error state. Separately the title uses `color: theme.colors.primaryForeground` on a near-background card, so in Zinc light mode a near-white title sits on a near-white surface (contrast failure).
**Fix:** Map `critical` → `destructive`, `warning` → a distinct warning/amber token, `info` → muted; use `foreground` (not `primaryForeground`) for the title on the card background.
**Test tier:** Widget test — assert critical vs warning resolve to different colors; assert the title color is a foreground token, not primaryForeground.

### CF-047 | P2 | S17 BenchmarkListScreen — success state flashes the empty state before reloading
**Sources:** F-E09 (46.1)
**File:** `benchmark_list_screen.dart:251-258`
**Confirmed:** Yes. On `BenchmarkSuccess` the builder returns `_emptyState(...)` while scheduling a post-frame `LoadBenchmarks()`. After any create/edit/delete the user sees "Belum ada benchmark" for a frame + the reload round-trip — the DB appears to vanish right after saving.
**Fix:** On success, keep showing the previous list or a loading indicator (don't render the empty state); trigger the reload without swapping to empty.
**Test tier:** Widget test — after a success emission, assert the empty state is not shown when records exist.

### CF-048 | P2 | S06 AttendanceFormPage — success pop fires on any state carrying a successMessage
**Sources:** F-B10 (46.1)
**File:** `attendance_form_page.dart:50-58`; state `attendance_state.dart:88-104` (`clearSuccessMessage`)
**Confirmed:** Yes (with nuance). The listener pops on any `AttendanceLoaded` with non-null `successMessage`. The state DOES have `clearSuccessMessage` and the record-edit path (bloc:98) clears it — so it's not unbounded — but the save path sets `successMessage` (bloc:143) and the listener then shows a snackbar and immediately `context.pop(true)`, tearing down the snackbar with the route so the confirmation is effectively invisible. Corrected from Pass-1a's "no clearSuccess flag" claim.
**Fix:** Scope the pop to the just-completed save (e.g. a one-shot success signal / BlocListener that consumes it), and show the confirmation on the destination (parent) rather than on the page being popped.
**Test tier:** Widget test — assert the pop happens once for a save and not on an unrelated `AttendanceLoaded` emission.

### CF-049 | P2 | S08 DailyLogFormScreen — controller text overwritten during build (caret jump)
**Sources:** F-B14 (46.1)
**File:** `daily_log_form_screen.dart:148-168`
**Confirmed:** Yes. Inside `build`, if `_summaryController.text != log.summary` it resets the controller value with the caret collapsed to the end. With per-keystroke auto-save (CF-050) a lagging state rewrites the field mid-edit and yanks the caret. Same idiom on `_notesController` and 5 controllers in InventoryItemEntry.
**Fix:** Sync controllers in `initState`/on explicit load, not in `build`; or only update when the field is not focused. Fix the shared idiom.
**Test tier:** Widget test — simulate a state emission during editing; assert caret/selection is preserved.

### CF-050 | P2 | S08 DailyLogFormScreen — auto-save dispatched on every keystroke
**Sources:** F-B11 (46.1)
**File:** `daily_log_form_screen.dart:292-299,320-327`
**Confirmed:** Yes. Both multiline fields fire `AutoSaveDraftEvent` on every character; hundreds of repository/sync-queue writes per log and a flickering AutoSaveIndicator. Zone/weather firing the event is fine (discrete).
**Fix:** Debounce the text-field auto-save (or save-on-pause / on-blur); leave the discrete selectors as-is.
**Test tier:** Widget test with fake async — type several chars; assert auto-save is debounced to one dispatch.

### CF-051 | P2 | S14 InventoryItemEntryScreen — timed auto-pop races the user
**Sources:** F-D18 (46.1)
**File:** `inventory_item_entry_screen.dart:156-160`
**Confirmed:** Yes. `Future.delayed(600ms, pop)` not cancelled in `dispose`; if the user already navigated, the callback pops the now-current route.
**Fix:** Navigate on the success state transition (BlocListener) rather than a wall-clock delay, or store and cancel the timer in `dispose`.
**Test tier:** Widget test — assert navigation is tied to the success state and no pop fires after dispose.

### CF-052 | P2 | S13 InventoryDashboardScreen — filter chips ignore `selected`/`theme` (invisible state)
**Sources:** F-D08 (46.1), V-031-adjacent (46.2)
**File:** `inventory_dashboard_screen.dart:447-454`
**Confirmed:** Yes. `_buildFilterChip` accepts `selected`/`theme` and returns a plain `FButton(onPress:, child:)` ignoring both — every chip looks identical, active category invisible.
**Fix:** Switch `FButtonVariant`/style on `selected` (as `SettingsPage._ThemeOption` does).
**Test tier:** Widget test — assert the selected chip renders a distinct variant.

### CF-053 | P2 | S05/S15 — search clear button never appears; search un-debounced
**Sources:** F-B09 + F-D09 + F-D10 (46.1)
**File:** `attendance_screen.dart:408-448`; `equipment_history_screen.dart:107-132,113-121`
**Confirmed:** Yes. `suffixIcon` reads `_searchController.text` but `onChanged` only dispatches a bloc event and never `setState`; the clear button's appearance depends on an unrelated rebuild. EquipmentHistory's search re-queries the repo on every keystroke (no debounce), flickering the list; a debounced pattern exists in data_bucket widgets.
**Fix:** Rebuild on controller changes (listener + setState, or ValueListenableBuilder) so the clear button tracks text; debounce the search dispatch. Apply to both screens.
**Test tier:** Widget test — assert clear button appears when text is entered; assert search dispatch is debounced.

### CF-054 | P2 | S14 InventoryItemEntryScreen — unparseable/negative quantity silently discarded
**Sources:** F-D07 (46.1)
**File:** `inventory_item_entry_screen.dart:94-105` (and threshold 100-105)
**Confirmed:** Yes. `if (parsed != null)` listeners do nothing on failure, so clearing/mistyping leaves the bloc holding the last value while the box shows something else; negatives parse and are accepted. Same threshold field too.
**Fix:** On parse failure clear/flag the bloc value (don't silently retain); reject negatives via validator (pairs with CF-038).
**Test tier:** Widget test — assert an emptied field clears the stored value and a negative is rejected.

### CF-055 | P2 | S20 DataBucketListPage — setState in post-frame callback on every load
**Sources:** F-F14 (46.1)
**File:** `data_bucket_list_page.dart:241-245,61-74`
**Confirmed:** Yes. Comment says "on first load" but there's no guard; `addPostFrameCallback(_computeFilters)` runs on every loaded build and `_computeFilters` calls `setState` unconditionally → schedules another callback. Converges only because values settle; the chip row jumps a frame after the list.
**Fix:** Derive `_availableZones`/`_availableTypes` from the state during build (or in the bloc); remove the post-frame setState.
**Test tier:** Widget test — assert filters are derived without a post-frame setState (no extra rebuild scheduled).

---
### Group 10 — UX / content / accessibility (P2)

### CF-056 | P2 | S01 LoginPage — misspelled tagline "Manajamen"
**Sources:** F-A04 (46.1), V-001 (46.2)
**File:** `login_page.dart:61`
**Confirmed:** Yes. `'Sistem Monitoring & Manajamen Tambang'` — should be "Manajemen". First line on the first screen.
**Fix:** Correct to "Manajemen".
**Test tier:** No test feasible — reason: static copy; covered incidentally by any login widget test. (Optional: assert the corrected string.)

### CF-057 | P2 | S18 BenchmarkFormScreen — misspelled "Kordinat"
**Sources:** F-E-adjacent (46.1 batch E strings), V-041 (46.2)
**File:** `benchmark_form_screen.dart` section headers ("Kordinat Proyeksi (UTM)", "Kordinat Geografis (Otomatis)") — confirmed present in the S18 screenshot
**Confirmed:** Yes (via screenshot). Standard Indonesian is "Koordinat".
**Fix:** Correct both headers to "Koordinat".
**Test tier:** No test feasible — static copy.

### CF-058 | P1 | S04 SettingsPage — WhatsApp link contains a masked placeholder number
**Sources:** F-A17 (46.1)
**File:** `settings_page.dart:292`
**Confirmed:** Yes. Displayed `'+62 851-5604-2854'` but handler launches `Uri.parse('https://wa.me/+628****2854')` — asterisks in the URL. `canLaunchUrl` succeeds for a well-formed https wa.me URL, so the user is sent to WhatsApp with an invalid recipient rather than the graceful error. Kept P1: it's the support escape hatch and displayed vs launched disagree.
**Fix:** Use the real support number (matching the displayed text) in the launch URL, or route support to a shared alias; if the number is a placeholder pending a decision, disable the button until set.
**Test tier:** Widget test — assert the launched URI matches the displayed number (no asterisks).

### CF-059 | P2 | S04 SettingsPage — English locale toggle changes almost nothing
**Sources:** F-A20 (46.1), V-011 (46.2)
**File:** `settings_page.dart:81-120`
**Confirmed:** Yes. `updateLocale(Locale('en'))` is offered but ~27 files remain Indonesian-hardcoded (RISK-0004), so switching to English visibly does nothing with no indication.
**Fix:** Until migration completes, either hide the English option or show an inline note that translation is partial. (Consequence of RISK-0004; user-visible today.)
**Test tier:** Widget test — assert the English option is hidden or accompanied by the partial-translation notice.

### CF-060 | P2 | S02 DashboardPage — dead "Akses Cepat" section (heading + subtitle, no content)
**Sources:** F-A08 (46.1), V-004 (46.2)
**File:** `dashboard_page.dart:149-180` (`SizedBox.shrink()` after the heading)
**Confirmed:** Yes. Heading "Akses Cepat" + subtitle naming reports/timeline/notifications, then nothing (tiles removed in STEP-34.3).
**Fix:** Remove the heading+subtitle with the tiles, or restore quick-access tiles.
**Test tier:** Widget test — assert no empty labelled section (either tiles present or heading absent).

### CF-061 | P2 | S02 DashboardPage — mixed-language stat cards
**Sources:** F-A09 (46.1), V-005 (46.2)
**File:** `dashboard_page.dart:73-92,103-126`
**Confirmed:** Yes. English labels/subtitles ("Active Crew", "Cut / Fill Volume", "Today's total volume") with Indonesian loading/failure text and section. Presentation-consistency defect independent of RISK-0004.
**Fix:** Make the card labels Indonesian (MVP default) consistently; wrap for future l10n.
**Test tier:** No test feasible beyond a string assertion — static copy consistency.

### CF-062 | P2 | S03 GroupLandingPage — English group titles with Indonesian subtitles
**Sources:** F-A14 (46.1), V-008 (46.2)
**File:** `router.dart:139-140,214-215,281-282` and feature labels
**Confirmed:** Yes. "Tools/Operations/Teams" titles + Indonesian subtitles; feature labels English except mixed "Timeline Pekerjaan".
**Fix:** Consistent Indonesian titles/labels (or a deliberate bilingual convention documented in Doc 07). Pairs with CF-063 (guard hole).
**Test tier:** No test feasible beyond string assertion.

### CF-063 | P2 | S03 GroupLandingPage — l10n guard bypassed via router literals
**Sources:** F-A13 (46.1)
**File:** `group_landing_page.dart` (not exempt); strings passed from `router.dart:138-149,213-236,280-315`; guard `tool/check_l10n_baseline.dart`
**Confirmed:** Yes. Verified the guard only scans `Text('...')` in presentation `pages/`/`widgets/` files (`check_l10n_baseline.dart:100-127`); `router.dart` is not a presentation file and `group_landing_page.dart` receives its 14 labels as constructor args, so it passes while shipping hardcoded labels. Any screen can defeat the guard by taking strings from the router.
**Fix:** Route GroupLandingPage's strings through localization (or keep them in-file where the guard sees them), AND extend the guard to catch labels passed to known presentation widgets from `router.dart` (or scan router.dart). Fix both or the hole stays open.
**Test tier:** Static guard — extend `check_l10n_baseline.dart` and add a self-test that a router-supplied literal is caught.

### CF-064 | P2 | S03 GroupLandingPage — no visible focus indicator on keyboard-focusable tile
**Sources:** F-A12 (46.1)
**File:** `group_landing_page.dart:92-124`
**Confirmed:** Yes. Tile is `Focus`(key listener only) wrapping `GestureDetector` — announces `button: true`, activates on Enter/Space, but nothing reacts visually to focus/hover/press. WCAG 2.1 AA "focus visible" failure on primary nav for three shell branches.
**Fix:** Use a real focusable control (`FTile`/`InkWell`/button) with focus/hover/pressed styling instead of a bare gesture recogniser.
**Test tier:** Widget test — focus the tile; assert a focus decoration is present (and Enter/Space still activates).

### CF-065 | P2 | S05 AttendanceScreen — read-only list with a dangling 80dp save-bar spacer
**Sources:** F-B08 (46.1), V-013 (46.2)
**File:** `attendance_screen.dart:281-290` (`CrewRosterItem(readOnly: true)`, `SizedBox(height: 80) // Space for bottom save bar`)
**Confirmed:** Yes. All rows read-only with no callbacks; 80dp reserved for a save bar that doesn't exist on this screen. Reads as a half-finished migration; editing requires the separate form.
**Fix:** Remove the dead spacer; either add inline editing or make the read-only intent explicit (and drop the reserved space).
**Test tier:** Widget test — assert no empty 80dp spacer / that the layout matches the read-only intent.

### CF-066 | P2 | S19 TimelinePage — empty state instructs an action the app doesn't offer; guard requires both empty
**Sources:** F-E14 (46.1), V-042 (46.2)
**File:** `timeline_page.dart:342-370`
**Confirmed:** Yes. Copy tells the user to "add milestones", but no create-milestone action exists anywhere (verified: no FAB/add button in timeline_page; MilestoneCard is display-only). Guard requires both milestones AND progress empty, so a progress-only site sees no explanation.
**Fix:** Either add a create-milestone action (if in scope) or change the copy to not instruct an impossible action; show the empty explanation when milestones are empty regardless of progress.
**Test tier:** Widget test — assert the empty-state copy matches available actions; assert it shows with milestones empty.

### CF-067 | P2 | S19 TimelinePage — "Berjalan" and "Selesai" badges share one color
**Sources:** F-E15 (46.1)
**File:** `timeline_page.dart:279-299`
**Confirmed:** Yes. Active and completed both use `theme.colors.primary`; only overdue differs. Schedule-health summary collapses to "blue/red".
**Fix:** Give in-progress vs completed distinct tokens.
**Test tier:** Widget test — assert the three badges resolve to distinct colors.

### CF-068 | P2 | S18 BenchmarkFormScreen — computed lat/lon shown as placeholder hint, not value
**Sources:** F-E12 (46.1)
**File:** `benchmark_form_screen.dart:152-153,304-322`
**Confirmed:** Yes. Auto-computed coords injected into the `hint` of a disabled `FTextField` — muted styling, not selectable/copyable, not exposed to a11y; shows `'-'` on failure indistinguishably from empty.
**Fix:** Render the computed values as actual (read-only, selectable) field content or a labelled value row; show a clear "could not compute" state on failure.
**Test tier:** Widget test — assert the computed value appears as content (selectable), not as hint.

### CF-069 | P2 | S17 BenchmarkListScreen — list omits elevation; no read-only detail view
**Sources:** F-E08 (46.1)
**File:** `benchmark_list_screen.dart:413-435`
**Confirmed:** Yes. Card shows bmId, N/E, optional code/orde; never `orthoHeight`/`ellipsHeight`. Reading elevation requires opening the editable form (risking edits); no read-only detail exists.
**Fix:** Show elevation on the card (or add a read-only detail view). Recommend adding ortho height to the card.
**Test tier:** Widget test — assert the card displays the elevation for a record that has one.

### CF-070 | P2 | S17 BenchmarkListScreen — search can't find by coordinate; no status filter; double-framed field
**Sources:** F-E18 (46.1)
**File:** `benchmark_list_screen.dart:174-184,269-306`
**Confirmed:** Yes. Filter matches only bmId/code/orde — not northing/easting; no `status` filter (destroyed BMs mixed with active); the `FTextField` sits inside a hand-built Container with its own fill/radius, double-framing it.
**Fix:** Add coordinate substring search and a status filter; remove the outer container so the ForUI field frames itself.
**Test tier:** Widget test — assert a coordinate query matches; assert status filter works; visual: single frame.

### CF-071 | P2 | S22 FileDetailPage — failed Drive link opens/reports nothing
**Sources:** F-F08 (46.1)
**File:** `file_detail_page.dart:289-301`
**Confirmed:** Yes. `Uri.tryParse` null falls through with no else; `launchUrl` called without `canLaunchUrl`/try-catch. The primary action fails silently. SettingsPage shows the correct guarded pattern.
**Fix:** Guard with `canLaunchUrl` + try/catch and show an error snackbar on failure; handle a malformed link.
**Test tier:** Widget test — assert a failing launch surfaces an error.

### CF-072 | P2 | S22 FileDetailPage — raw ids shown for zone/uploaded-by; fixed-width label clips at scale
**Sources:** F-F16 (46.1)
**File:** `file_detail_page.dart:226,239-240,247-267`
**Confirmed:** Yes. `zoneId`/`uploadedBy` shown raw under "Zona"/"Diunggah Oleh"; `_detailRow` label fixed at 130dp with no overflow handling → clips at 360dp + large text scale.
**Fix:** Resolve zone id → name and user id → name; make the label flexible/ellipsized. (Resolution may be Needs-Runtime if it requires a lookup not available client-side — but the layout fix and at least id→name mapping are static.)
**Test tier:** Widget test at 360dp + textScale — assert labels don't clip; assert resolved names when available.

### CF-073 | P2 | S23 ReportConfigPage — date-range label desyncs from actual range
**Sources:** F-F10 (46.1)
**File:** `date_range_selector.dart:31-35,44-52`
**Confirmed:** Yes. `initState` hardcodes `_selectedOption = 'Minggu Ini'` regardless of `initialRange`; on return after choosing YTD the dropdown says "Minggu Ini" while the cubit holds YTD; cancel path resets the label without updating the range. User generates a PDF for a period different from the label.
**Fix:** Derive `_selectedOption` from `initialRange`; on cancel restore the prior label without desyncing.
**Test tier:** Widget test — set initialRange to YTD; assert the label reflects it; assert cancel keeps label and range in sync.

### CF-074 | P2 | S23 ReportConfigPage — zone filter is a raw free-text ID, only for cutFill
**Sources:** F-F11 (46.1)
**File:** `report_config_page.dart:122-135` (verified: `if (widget.reportType == ReportType.cutFill)` gates a free-text `_zoneController`)
**Confirmed:** Yes. Raw zone-ID text field, no picker/validation, silent empty report on typo; only appears for cutFill so attendance/inventory can't be zone-scoped.
**Fix:** Use `ZonePicker` (already in the codebase); offer zone scoping consistently across report types (or document why not).
**Test tier:** Widget test — assert a zone picker is used and that a selected zone scopes the report.

### CF-075 | P2 | S23 ReportConfigPage — "Buat Laporan" button low-contrast (WCAG AA)
**Sources:** V-048 (46.2)
**File:** `report_config_page.dart:154-170`
**Confirmed:** Yes (via screenshot): white/near-white label on a light-grey button — fails AA. Verified the button uses a default `FButton` with a light child style on the config form.
**Fix:** Use dark foreground on the light button, or a primary-colored button with proper foreground; ensure ≥4.5:1.
**Test tier:** No automated contrast test feasible — reason: renders as pixels; verify visually. (Static: ensure the button uses theme foreground tokens, not a hardcoded light color.)

### CF-076 | P2 | S21 UploadFilePage — disabled Upload button low-contrast
**Sources:** V-045 (46.2)
**File:** `upload_file_page.dart` upload button (disabled state)
**Confirmed:** Yes (via 46.2 screenshot review): dark-grey block with low-contrast black text when disabled.
**Fix:** Give the disabled state a legible label contrast (ForUI disabled tokens) and a clearer disabled affordance.
**Test tier:** No automated contrast test feasible — visual verify; ensure disabled styling uses theme tokens.

---
### Group 11 — Remaining confirmed P1/P2

### CF-077 | P1 | S18 BenchmarkFormScreen — coordinate keyboards use integer keypad
**Sources:** F-E11 (46.1)
**File:** `benchmark_form_screen.dart:268,279,362,373` (verified: all four coord fields `keyboardType: TextInputType.number`, hints `'0.00'`)
**Confirmed:** Confirmed at code level as a real inconsistency; kept as CONFIRMED (not NEEDS-RUNTIME) because the fix is unambiguous — `TextInputType.number` can hide the decimal separator on Android while these fields require sub-metre decimals, and the codebase already uses `numberWithOptions(decimal: true)` for inventory. Device-level keypad behaviour is the only runtime aspect; the fix does not depend on it.
**Fix:** Change all four to `TextInputType.numberWithOptions(decimal: true, signed: true)` (signed for legitimate negatives, per CF-035).
**Test tier:** Widget test — assert the coord fields declare a decimal (and signed) keyboard type.

### CF-078 | P2 | S21 UploadFilePage — no file-size limit; whole file into memory; retry re-uploads from snackbar
**Sources:** F-F13 (46.1)
**File:** `upload_file_page.dart:106-142,219-231`
**Confirmed:** Yes. `pickFiles(withData: true)` loads the entire file into `_fileBytes` with no size check; large GeoTIFFs → OOM on device / blocked isolate on web. The extension list omits `.kmz` in the picker UI though it's accepted. Error path offers `SnackBarAction('Coba Lagi', onPressed: _submitUpload)` re-running a full upload.
**Fix:** Enforce a max size before reading; consider streamed upload; align the displayed extension list with the accepted set; make retry re-open the confirmation rather than silently re-uploading. (Actual large-file/OOM behaviour is device-runtime — see NR-005 — but the size guard + list fix are static.)
**Test tier:** Widget test — assert an over-limit file is rejected with a message; assert the extension list matches the accepted set.

### CF-079 | P2 | S21/S22 — detail-page delete bypasses the bloc; success reported before verification
**Sources:** F-F15 (46.1)
**File:** `data_bucket_list_page.dart:345-358`; `file_detail_page.dart:82-107`
**Confirmed:** Yes. The detail page's delete calls `repository.deleteFile` directly (has try/catch, unlike equipment), bypassing the bloc's `DeleteFile`, so there's no loading state (button live during the Drive round-trip → double-trigger) and the success snackbar shows on a route popped the same frame.
**Fix:** Route the delete through `DataBucketBloc.DeleteFile` (loading + error + list refresh) and show feedback on the destination.
**Test tier:** Widget/bloc test — assert delete goes through the bloc with a loading state; assert no double-dispatch.

### CF-080 | P2 | S16 EquipmentCheckFormScreen — submit button/notes below the fold; no in-flight beyond a spinner
**Sources:** F-D-adjacent (46.1), V-038 (46.2)
**File:** `equipment_check_form_screen.dart` (long SOP list pushes submit below fold at 1280x800, per screenshot)
**Confirmed:** Yes (screenshot). The SOP list pushes the notes + submit below the fold. Grouped here as a layout/discoverability issue.
**Fix:** Use a persistent bottom action bar for submit (as attendance form does) so it's always reachable; keep notes visible or clearly scrollable.
**Test tier:** Widget test at 1280x800 — assert the submit control is reachable without the list pushing it off a fixed action bar.

### CF-081 | P2 | S23/S12/etc — form submit buttons stretch full-width on desktop
**Sources:** F-D-adjacent, V-015 + V-021 + V-024 + V-030 + V-034 (46.2)
**File:** attendance form, daily-log form, cut-fill form, land-clearing entry, inventory entry submit buttons
**Confirmed:** Yes (screenshots). On the 1280px desktop layout the primary submit buttons stretch the full content width instead of a card-constrained max width, and several are pushed below the fold (V-024, V-038 overlap CF-080).
**Fix:** Constrain form content (and the submit button) to a max width (e.g. a centered form card ~600px) on wide layouts; keep the submit reachable.
**Test tier:** Widget test at 1280dp — assert the submit button width is constrained (not full viewport).

### CF-082 | P2 | S13 InventoryDashboardScreen — category chip row clips off-screen with no scroll cue
**Sources:** V-031 (46.2)
**File:** `inventory_dashboard_screen.dart` category chip row
**Confirmed:** Yes (screenshot): the chip row extends past the right edge with the last chip half-clipped and no scrollbar/fade cue.
**Fix:** Make the chip row horizontally scrollable with a visible affordance (fade/scrollbar) or wrap on narrow widths.
**Test tier:** Widget test — assert the chip row is scrollable and no chip is clipped without a cue.

### CF-083 | P2 | S13/S15 — two-FAB Row can overflow at narrow width + enlarged text
**Sources:** F-D12 (46.1)
**File:** `inventory_dashboard_screen.dart:90-139`; `equipment_history_screen.dart:326-370`
**Confirmed:** Yes. FAB slot holds a `Row` (circular FAB + gap + extended FAB); the slot isn't width-constrained, so at 360dp + large text scale the intrinsic width can overflow.
**Fix:** Constrain/limit the FAB row (e.g. shrink the extended FAB to icon-only at narrow width, or wrap). Apply to both.
**Test tier:** Widget test at 360dp + textScale 1.3 — assert no overflow in the FAB row.

### CF-084 | P2 | S24 NotificationListPage — stagger animation over budget and races dispose
**Sources:** F-E16 (46.1)
**File:** `notification_list_page.dart:221-245`
**Confirmed:** Yes. 350ms controller + 40ms/index stagger (a 20-item list ~1.15s) exceeds Doc 07 §5's 150–200ms; `Future.delayed(..., _controller.forward)` isn't cancelled, so it can call `forward()` on a disposed controller; no reduced-motion check.
**Fix:** Bring durations within 150–200ms, cap/remove the stagger, cancel the delayed callback in `dispose`, and honor reduced-motion (Doc 07 §5).
**Test tier:** Widget test — assert durations ≤200ms; assert leaving mid-stagger does not throw; assert reduced-motion disables the animation.

---

### Group 12 — P3 confirmed (tokens, motion, Material leftovers, cosmetics)

These are all confirmed against source and fixed in 46.4 per PLAN decision 3 (all P1/P2/P3 in scope). Grouped tersely; each is low-risk and mostly covered by an analyze/token sweep rather than per-item tests.

### CF-085 | P3 | Motion durations exceed the 150–200ms budget (systemic)
**Sources:** F-A10 + F-D21 + F-B17 + F-E21 (46.1)
**Files:** `dashboard_page.dart:94-97` (300ms); `inventory_dashboard_screen.dart:84-88` (250ms); daily-log list & other list `AnimatedSwitcher` (250ms); notifications (350ms, see CF-084).
**Confirmed:** Yes. Doc 07 §5 caps at 150–200ms.
**Fix:** One sweep bringing all `AnimatedSwitcher`/controller durations to ≤200ms.
**Test tier:** Widget test on the dashboard switcher (assert ≤200ms) + manual for the rest; no per-site test.

### CF-086 | P3 | Off-scale spacing/radii (systemic)
**Sources:** F-B17 + F-D19 + F-E21 + F-F18 (46.1), V-related
**Files:** attendance (14dp padding, radius 12/1.5px borders), daily-log (radius 16/10), inventory (14dp, radius 10/6, alpha magic), benchmark (radius 6/10/16), data-bucket (radius 16), etc.
**Confirmed:** Yes. Doc 07 §2 scale is 4/8/12/16/20/24/32 with standard ForUI radii; the cited values are off-scale.
**Fix:** Normalise to the scale/standard radii in a sweep.
**Test tier:** No test feasible — visual/token; verify via review.

### CF-087 | P3 | Residual Material widgets where ForUI is specified (systemic)
**Sources:** F-A11 + F-A18 + F-B15 + F-B16 + F-D13 + F-D14 + F-D15 + F-D16 + F-D17 + F-E20 + F-F18 (46.1), V-020 (46.2)
**Files:** across S02 (Scaffold), S04 (AlertDialog/SnackBar), S05/S07/S08 (SnackBar/AppBar/FilledButton), S13-16 (AppBar/TextField/FilterChip/FilledButton/Divider/DropdownButtonFormField/SnackBar), S17-19/S24 (AppBar/FilledButton/AlertDialog/DropdownButtonFormField/SnackBar/Divider), S20-23 (AppBar/PopupMenu/ListTile/AlertDialog/FilledButton/SnackBar/InputDecorator).
**Confirmed:** Yes. STEP-37/38 purged Material but these remain; Doc 07 §3/§6 makes ForUI the vocabulary. Snackbars, appbars, dialogs, dropdowns (→`FSelect`), and hand-styled FilledButtons are the recurring offenders.
**Fix:** One Material-purge sweep: replace with ForUI equivalents (dialogs, alerts/snackbars, headers, selects, buttons). Large but mechanical; do per-feature to keep diffs reviewable.
**Test tier:** `flutter analyze` clean + targeted widget tests where behaviour changes (dialogs/selects); mostly visual.

### CF-088 | P3 | Material icons where Doc 07 specifies Lucide (systemic)
**Sources:** F-A23 (46.1), V-050 (46.2)
**Files:** repo-wide (`Icons.*` in sidebar, cards, buttons, forms).
**Confirmed:** Yes. Doc 07 §5 specifies Lucide.
**Fix:** One deliberate decision: migrate to Lucide OR amend Doc 07 + log an ADR. Do not do 24 ad-hoc edits.
**Test tier:** No test feasible — visual; requires the decision/ADR first.

### CF-089 | P3 | S04 SettingsPage — raw TextStyle(fontSize: 11) off the typography scale
**Sources:** F-A19 (46.1)
**File:** `settings_page.dart:436`
**Confirmed:** Yes. Bare `TextStyle(fontSize: 11)` bypasses `theme.typography`.
**Fix:** Use a theme typography step; adjust layout if 11px was a fit hack.
**Test tier:** No test feasible — token.

### CF-090 | P3 | S04 SettingsPage — hardcoded app version string
**Sources:** F-A21 (46.1)
**File:** `settings_page.dart:257` (`'mine-flow v0.1.0'`)
**Confirmed:** Yes. Duplicates pubspec; `package_info_plus` not a dep, so it will go stale.
**Fix:** Add `package_info_plus` and read the version at runtime.
**Test tier:** Widget test with a mocked package info (optional).

### CF-091 | P3 | S17 BenchmarkListScreen — hardcoded hex status colors + raw status string
**Sources:** F-E19 (46.1)
**File:** `benchmark_list_screen.dart:472-485`
**Confirmed:** Yes. `Color(0xFF16A34A)`/`Color(0xFFCA8A04)` alongside tokenised `destructive`; renders raw `active`/`destroyed`/`replaced` in English.
**Fix:** Tokenise the status palette (or add semantic tokens) and localise/enumerate the status labels; `status` should be an enum.
**Test tier:** No test feasible beyond a string/token assertion.

### CF-092 | P3 | S13 InventoryDashboardScreen — hardcoded alpha values for banner surface
**Sources:** F-D20 (46.1)
**File:** `inventory_dashboard_screen.dart:293,296` (`withAlpha(25)`/`withAlpha(76)`)
**Confirmed:** Yes. Custom translucent surfaces may not meet AA in dark mode.
**Fix:** Use semantic tokens / a defined alert surface rather than magic alphas.
**Test tier:** No test feasible — token/contrast; visual.

### CF-093 | P3 | S14 InventoryItemEntryScreen — dead focus-node plumbing (auto-predict remnant)
**Sources:** F-D23 (46.1)
**File:** `inventory_item_entry_screen.dart:58,82,119,129` (`_onNameFocusChanged() {}`)
**Confirmed:** Yes. Focus node wired to an empty handler — remnant of STEP-33 auto-predict; the affordance has no behaviour.
**Fix:** Either implement the suggestion behaviour (if in scope) or remove the dead plumbing. Confirm against STEP-33 intent before deleting.
**Test tier:** No test feasible if removed; widget test if implemented.

### CF-094 | P3 | S13 InventoryDashboardScreen — dead/duplicated layout constants; three breakpoints
**Sources:** F-D22 (46.1)
**File:** `inventory_dashboard_screen.dart:15-18,65,194-214`
**Confirmed:** Yes. `_kSidePaddingWide` used only as `.horizontal/2` to recover 32 already hardcoded; `_kBreakMobile/_kBreakTablet` (600/900) coexist with an inline `>= 800` test — header and grid change at different widths.
**Fix:** Consolidate to one breakpoint set and remove dead constants.
**Test tier:** No test feasible — refactor; verify responsive behaviour manually.

### CF-095 | P3 | S22 FileDetailPage — file-type color switch maps 7/9 cases to one token; .pdf uses destructive
**Sources:** F-F09 (46.1)
**File:** `file_detail_page.dart:327-349`
**Confirmed:** Yes. All geospatial types → `primary`; only `.pdf` differs and it uses `destructive` (reads as "broken").
**Fix:** Either restore a per-type palette (tokenised) or collapse to one token and drop the pointless branching; don't use `destructive` for `.pdf`.
**Test tier:** No test feasible — cosmetic.

### CF-096 | P3 | S21/S22 — hand-rolled ISO date formatting + unlocalised pickers
**Sources:** F-F17 (46.1), V-043 (46.2)
**File:** `upload_file_page.dart:309-324,144-156`; `file_detail_page.dart:231,237`; timeline picker locale
**Confirmed:** Yes. `padLeft`-assembled `yyyy-MM-dd` instead of `intl` `DateFormat` (already a dep); `showDatePicker` without a locale; timeline `dd/MM` label omits year.
**Fix:** Use `DateFormat` consistently; pass the active locale to pickers; include the year where ranges span boundaries.
**Test tier:** No test feasible beyond a format assertion.

---
## Rejected Findings (false positives / not actionable defects)

### REJECTED: F-D11 | S13 InventoryDashboardScreen — "stock adjustment never reflected in list"
**Verdict:** NOT a defect. Pass 1a flagged that `AdjustStockEvent` might not reload. Verified: `_onAdjustStock` (`inventory_bloc.dart:238-266`) explicitly re-dispatches `LoadInventoryItemsEvent` with the current filters (the same pattern as `_onDeleteItem`). The adjusted quantity is reloaded. Pass 1a's "recommend confirmation" resolved in the negative.

### REJECTED: V-040 / F-adjacent | S18 BenchmarkFormScreen — "route returns 404 Page Not Found"
**Verdict:** NOT reproducible as described. 46.2 claimed `/operations/benchmark-db/form` renders GoRouter's 404. The captured screenshot `S18-benchmark-form.png` shows a fully-rendered, working benchmark form (verified visually), not a 404. The real, confirmed defect is that `AppRoutes.benchmarkForm` is declared but never registered as a `GoRoute` (the form is reached via `Navigator.push`) — captured as CF-097/NR-006-adjacent below via F-E23. So the routing constant is dead and the form is not deep-linkable, but the screen does not 404 in normal navigation. Downgraded from V-040's P1 "404" to the real issue (see CF-097).

### REJECTED: V-006 | S02 DashboardPage — "asymmetric orphan card in 3-col grid"
**Verdict:** Not a defect worth remediation. A 4-item grid in 3 columns leaving one card on the second row is normal grid behaviour, not a bug. No design-spec rule is violated (Doc 07 §1 favours density, not symmetry). Cosmetic-only; if desired it's a layout preference, not a finding. No action.

### REJECTED: V-003 | S01 LoginPage — "unresponsive theme rendering on login card"
**Verdict:** Not a confirmed defect. The login page uses `FCard`/`FTheme` tokens (`login_page.dart`), which follow the active theme; the "fixed dark card" observation is a screenshot artefact of the capture environment's theme, not evidence the card ignores the toggle. There is no theme toggle ON the login screen by design (it's pre-auth). No code path shows a hardcoded dark card. If a genuine light-mode rendering problem exists it needs runtime confirmation — but as stated (static) it is not substantiated. No action (see NR-002 if login light-mode is to be checked on device).

### REJECTED: V-018 | S07 — "single-level breadcrumb doesn't reflect filter"
**Verdict:** Not a defect. Breadcrumbs reflecting a status-chip filter is not a stated requirement and is atypical; breadcrumbs show route hierarchy, not in-page filter state. No spec violation. No action.

### REJECTED: V-023 / V-039 | breadcrumb casing "Cut Fill" vs "Cut / Fill", "Benchmark Db" vs "Benchmark DB"
**Verdict:** Downgraded to non-actionable-as-filed / folded. These are auto-title-cased breadcrumb segments derived from the route path. Rather than per-string edits, the real fix (if any) is the breadcrumb title-casing logic; the individual casing mismatches are cosmetic and not independently actionable. Folded into CF-088-adjacent polish if the breadcrumb builder is touched; otherwise no action. (Noted, not tracked as separate CF items.)

---

## Needs-Runtime Findings (carry to STEP-45)

### NR-001 | S23 ReportConfigPage — verify PDF generation over a real dataset (no cancel, no progress)
**Sources:** F-F12 (46.1)
**Observation:** The generate flow shows only a button spinner; there's no cancel and navigating away discards the result (cubit dies with the route), and the config controls stay interactive during generation so a range change mid-run can mismatch the output. The UX defects are confirmable statically (and CF-030/CF-073 cover the reachable ones), but whether a project-to-date PDF is actually slow enough to need a progress/cancel affordance — and whether mid-generation config changes corrupt the output — needs a real dataset on staging.
**STEP-45 action:** Generate each report type over the largest available staging dataset; measure duration; attempt navigate-away and mid-run config change; confirm whether cancel/progress is warranted.

### NR-002 | S01 LoginPage — light-mode rendering on a real device
**Sources:** V-003 (46.2, otherwise rejected)
**Observation:** Whether the login card renders correctly in light mode (vs the dark screenshot) can't be settled from static code.
**STEP-45 action:** Load `/login` on device in both themes; confirm the card follows the theme.

### NR-003 | S03 GroupLandingPage — sidebar active-state on group routes
**Sources:** V-009 (46.2)
**Observation:** 46.2 reports no sidebar highlight on `/operations`, `/teams`, `/tools`. The shell computes active state from `GoRouterState.of(context).uri.path` against `_kSidebarSections` items (verified app_shell.dart:264); whether the group landing routes have a matching sidebar entry to highlight depends on the sidebar item set and the running route — confirm on the web build.
**STEP-45 action:** Navigate to each group route on web; confirm whether a sidebar item should highlight and does.

### NR-004 | S21 UploadFilePage — real Google Drive upload (auth + success/failure)
**Sources:** F-F04 (CF-018), F-F06 (46.1)
**Observation:** CF-018 fixes the empty-credential fallback statically, but confirming an actual authenticated upload — and the in-flight cancellation / abandon behaviour (F-F06: no PopScope, no CancelToken, header null on desktop) — requires a wired Drive service and a real file on staging/device.
**STEP-45 action:** With Drive wired, upload a real file; test back/close mid-upload on Android and web; confirm the record/Drive state after abandonment and whether a cancel affordance is needed.

### NR-005 | S21 UploadFilePage — large-file (OOM) behaviour on a mid-range device
**Sources:** F-F13 (CF-078)
**Observation:** CF-078 adds a size guard statically, but the actual out-of-memory threshold for `withData: true` on a mid-range Android device (and isolate-block on web) needs device measurement to set the limit sensibly.
**STEP-45 action:** Attempt uploads of increasing size on a target device; find the practical ceiling; set the guard accordingly.

### NR-006 | S18 BenchmarkForm — deep-link / route-registration behaviour on web
**Sources:** F-E23 (46.1) → CF-097
**Observation:** `AppRoutes.benchmarkForm` is declared but unregistered; the form is pushed via `Navigator.push` outside the shell. Whether this breaks deep-linking, reload, and shell persistence on the web build (and whether it 404s on a direct hit, contra V-040) needs runtime confirmation on staging.
**STEP-45 action:** On web, attempt to open `/operations/benchmark-db/form` directly and via the in-app button; confirm shell persistence and whether the route needs registering.

---

## Summary Table

| ID | Sev | Screen | Short description | Status |
|----|-----|--------|-------------------|--------|
| CF-001 | P1 | S01 | Login performs no authentication | Confirmed |
| CF-002 | P1 | S01 | Hardcoded admin credentials pre-filled | Confirmed |
| CF-003 | P1 | S01 | No validation/loading/error state | Confirmed |
| CF-004 | P1 | S04 | Logout doesn't call signOut | Confirmed |
| CF-005 | P1 | S04 | Hardcoded name/role in profile | Confirmed |
| CF-006 | P1 | S07 | Empty foremanId hides logs | Confirmed |
| CF-007 | P1 | S08 | Logs persisted with empty author | Confirmed |
| CF-008 | P1 | S08 | Draft leak on shared device | Confirmed |
| CF-009 | P1 | S09/S10 | Empty surveyor attribution | Confirmed |
| CF-010 | P1 | S11/S12 | Empty cleared-by attribution | Confirmed |
| CF-011 | P1 | S02 | Dashboard sums BCM+LCM | Confirmed |
| CF-012 | P1 | S02 | Active Crew counts all statuses | Confirmed |
| CF-013 | P1 | S11 | Ha not converted + plan+actual sum | Confirmed |
| CF-014 | P1 | S09/S10 | BCM/LCM conflated as Net | Confirmed |
| CF-015 | P1 | S06 | Synthetic roster seeded as real | Confirmed |
| CF-016 | P1 | S09/S11 | Zone filter hardcodes 'Zona A' | Confirmed |
| CF-017 | P1 | S16 | SOP checklist defaults all PASS | Confirmed |
| CF-018 | P1 | S21 | Empty-credential Drive fallback | Confirmed |
| CF-019 | P1 | S13 | Inventory delete no confirm/gate | Confirmed |
| CF-020 | P1 | S15 | Safety-record delete, bypasses bloc | Confirmed |
| CF-021 | P1 | S07 | Daily-log delete no confirm/gate | Confirmed |
| CF-022 | P1 | S09 | Cut/fill delete no confirm/gate | Confirmed |
| CF-023 | P1 | S11 | Land-clearing delete no confirm/gate | Confirmed |
| CF-024 | P1 | S20 | Drive-file delete no role gate | Confirmed |
| CF-025 | P1 | S07 | Report FAB wrong type (attendance) | Confirmed |
| CF-026 | P1 | S11 | Report FAB wrong type (cutFill) | Confirmed |
| CF-027 | P1 | S15 | Report FAB wrong type (inventory) | Confirmed |
| CF-028 | P1 | S17 | Report FAB wrong type (inventory) | Confirmed |
| CF-029 | P1 | S20 | Report FAB wrong type (cutFill) | Confirmed |
| CF-030 | P1 | S23 | Reports no nav entry / shell drop | Confirmed |
| CF-031 | P1 | S22 | :id route not restorable | Confirmed |
| CF-032 | P1 | S17/S19/S24 | Actions vanish on desktop layout | Confirmed |
| CF-033 | P1 | S18 | CRS/UTM zone never persisted | Confirmed |
| CF-034 | P1 | S18 | No validation; coords discarded; double-submit | Confirmed |
| CF-035 | P1 | S18 | Edit drops zero/negative elevations | Confirmed |
| CF-036 | P1 | S10 | Validation declared, never runs | Confirmed |
| CF-037 | P1 | S12 | Validation declared, never runs | Confirmed |
| CF-038 | P1 | S14 | Save performs no validation | Confirmed |
| CF-039 | P1 | S16 | No validation; serial optional | Confirmed |
| CF-040 | P1 | S10 | Elevation not loaded on edit | Confirmed |
| CF-041 | P1 | S10/S12 | Error retry inert (wrong action) | Confirmed |
| CF-042 | P2 | S08 | Error retry dispatches auto-save | Confirmed |
| CF-043 | P1 | S12 | Free-text into enumerated method | Confirmed |
| CF-044 | P1 | S12 | Plan/Actual tabs share date/zone | Confirmed |
| CF-045 | P1 | S21 | Zone required but never validated | Confirmed |
| CF-046 | P2 | S24 | Severity colors identical; title contrast | Confirmed |
| CF-047 | P2 | S17 | Success flashes empty state | Confirmed |
| CF-048 | P2 | S06 | Success pop tears down confirmation | Confirmed |
| CF-049 | P2 | S08 | Controller overwritten in build (caret) | Confirmed |
| CF-050 | P2 | S08 | Auto-save on every keystroke | Confirmed |
| CF-051 | P2 | S14 | Timed auto-pop races user | Confirmed |
| CF-052 | P2 | S13 | Filter chips ignore selected state | Confirmed |
| CF-053 | P2 | S05/S15 | Clear btn dead; search un-debounced | Confirmed |
| CF-054 | P2 | S14 | Quantity silently discarded/negative | Confirmed |
| CF-055 | P2 | S20 | setState in per-load post-frame | Confirmed |
| CF-056 | P2 | S01 | Typo "Manajamen" | Confirmed |
| CF-057 | P2 | S18 | Typo "Kordinat" | Confirmed |
| CF-058 | P1 | S04 | WhatsApp link has masked number | Confirmed |
| CF-059 | P2 | S04 | English toggle changes nothing | Confirmed |
| CF-060 | P2 | S02 | Dead "Akses Cepat" section | Confirmed |
| CF-061 | P2 | S02 | Mixed-language stat cards | Confirmed |
| CF-062 | P2 | S03 | English titles / ID subtitles | Confirmed |
| CF-063 | P2 | S03 | l10n guard bypassed via router | Confirmed |
| CF-064 | P2 | S03 | No focus indicator on tile | Confirmed |
| CF-065 | P2 | S05 | Dangling 80dp save-bar spacer | Confirmed |
| CF-066 | P2 | S19 | Empty state instructs impossible action | Confirmed |
| CF-067 | P2 | S19 | Berjalan/Selesai badges same color | Confirmed |
| CF-068 | P2 | S18 | Computed lat/lon shown as hint | Confirmed |
| CF-069 | P2 | S17 | List omits elevation; no detail view | Confirmed |
| CF-070 | P2 | S17 | No coord search / status filter; double frame | Confirmed |
| CF-071 | P2 | S22 | Failed Drive link silent | Confirmed |
| CF-072 | P2 | S22 | Raw ids shown; label clips | Confirmed |
| CF-073 | P2 | S23 | Date-range label desyncs | Confirmed |
| CF-074 | P2 | S23 | Zone filter raw free-text ID | Confirmed |
| CF-075 | P2 | S23 | "Buat Laporan" low contrast | Confirmed |
| CF-076 | P2 | S21 | Disabled Upload button low contrast | Confirmed |
| CF-077 | P1 | S18 | Coord fields use integer keypad | Confirmed |
| CF-078 | P2 | S21 | No file-size limit; retry re-uploads | Confirmed |
| CF-079 | P2 | S21/S22 | Detail delete bypasses bloc | Confirmed |
| CF-080 | P2 | S16 | Submit/notes below fold | Confirmed |
| CF-081 | P2 | multi | Full-width submit buttons on desktop | Confirmed |
| CF-082 | P2 | S13 | Category chip row clips, no cue | Confirmed |
| CF-083 | P2 | S13/S15 | Two-FAB Row overflow risk | Confirmed |
| CF-084 | P2 | S24 | Stagger over budget; races dispose | Confirmed |
| CF-085 | P3 | systemic | Motion durations over budget | Confirmed |
| CF-086 | P3 | systemic | Off-scale spacing/radii | Confirmed |
| CF-087 | P3 | systemic | Residual Material widgets | Confirmed |
| CF-088 | P3 | systemic | Material icons vs Lucide | Confirmed |
| CF-089 | P3 | S04 | Raw TextStyle fontSize 11 | Confirmed |
| CF-090 | P3 | S04 | Hardcoded version string | Confirmed |
| CF-091 | P3 | S17 | Hardcoded hex status colors | Confirmed |
| CF-092 | P3 | S13 | Magic alpha banner surface | Confirmed |
| CF-093 | P3 | S14 | Dead focus-node plumbing | Confirmed |
| CF-094 | P3 | S13 | Dead constants; 3 breakpoints | Confirmed |
| CF-095 | P3 | S22 | File-type color switch collapsed | Confirmed |
| CF-096 | P3 | S21/S22 | Hand-rolled dates; unlocalised pickers | Confirmed |
| CF-097 | P3 | S17/S18 | benchmarkForm route constant unregistered | Confirmed |
| REJECTED: F-D11 | — | S13 | Stock adjust does reload | Rejected |
| REJECTED: V-040 | — | S18 | Form does not 404 (real: CF-097) | Rejected |
| REJECTED: V-006 | — | S02 | Grid orphan card is normal | Rejected |
| REJECTED: V-003 | — | S01 | Login theme (→ NR-002) | Rejected |
| REJECTED: V-018 | — | S07 | Breadcrumb+filter not required | Rejected |
| REJECTED: V-023/V-039 | — | S09/S17 | Breadcrumb casing cosmetic | Rejected |
| NR-001 | P2 | S23 | PDF generation over real dataset | Needs-Runtime |
| NR-002 | P3 | S01 | Login light-mode on device | Needs-Runtime |
| NR-003 | P2 | S03 | Sidebar active-state on group routes | Needs-Runtime |
| NR-004 | P1 | S21 | Real Drive upload + abandon | Needs-Runtime |
| NR-005 | P2 | S21 | Large-file OOM threshold | Needs-Runtime |
| NR-006 | P2 | S18 | benchmarkForm deep-link on web | Needs-Runtime |

### CF-097 | P3 | S17/S18 — benchmarkForm route constant declared but never registered
**Sources:** F-E23 (46.1)
**File:** `router.dart:77` (`static const benchmarkForm`); no matching `GoRoute`; form reached via `benchmark_list_screen.dart` `Navigator.push(MaterialPageRoute(...))`
**Confirmed:** Yes. Verified: `router.dart` registers `benchmark-db` (258-265) but no `form` child; the constant is dead and the form is pushed onto the root navigator outside the shell. Not a crash in normal nav (contra V-040) but not URL-addressable/deep-linkable and drops the sidebar while editing.
**Fix:** Register a `form` child route under `benchmark-db` (matching `equipmentCheckForm`/`attendanceForm`) and navigate via it, so the form is deep-linkable and stays in the shell. Runtime deep-link check → NR-006.
**Test tier:** Widget/route test — assert the benchmarkForm route resolves and renders the form within the shell.

---

## Counts by severity (confirmed)

- **P1:** 46
- **P2:** 38
- **P3:** 13
- **Total confirmed:** 97
- **Rejected:** 6 (F-D11, V-040, V-006, V-003, V-018, V-023/V-039)
- **Needs-Runtime:** 6 (NR-001–006)

(Confirmed count 97 > the 175 raw candidates minus rejects because many raw F-/V- pairs merged into single CFs while a few multi-site F- items were kept as one CF; the dedup math: 175 raw → 96 unique issues after merging duplicates and aggregating the systemic P3 rows → 97 CF entries as some aggregates were split back by fix boundary, 6 rejected, 6 needs-runtime. The per-severity split above is the authoritative remediation scope for 46.4.)

## Recommended remediation ordering for 46.4

1. **Auth foundation first** (CF-001–005): everything role/attribution-related depends on it.
2. **Empty-id + attribution** (CF-006–010): fold into the auth wiring (one router change + per-bloc).
3. **Data-correctness ADR** (CF-011, CF-013, CF-014): needs a user/product decision on BCM/LCM & area semantics before code — raise as one ADR.
4. **Destructive-action gating** (CF-019–024): one shared confirm+role-gate helper.
5. **Report-type decision** (CF-025–029 + CF-030): one ReportType decision + a Reports nav entry.
6. **Form validation class** (CF-034–039, CF-045): shared validation pattern.
7. **Remaining P1s** (routing CF-031/CF-032/CF-097, CRS CF-033, edit-load CF-035/CF-040/CF-041, method CF-043, tabs CF-044, roster CF-015, zone-filter CF-016, SOP CF-017, Drive fallback CF-018, WhatsApp CF-058, keypad CF-077).
8. **P2 UX/state**, then **P3 sweeps** (Material purge, tokens, motion, icons) last as low-risk batches.

Note the data-correctness (CF-011/013/014), Plan/Actual model (CF-044), report-type set (CF-025–029), CRS persistence (CF-033, schema), and Lucide-vs-Material (CF-088) items each require a **product/architecture decision** (likely one or more ADRs) before implementation — 46.4 should surface these to the user rather than pick silently.


---

## Appendix — STEP-51 re-scope (2026-09-09)

Appended by STEP-51.1 (branch `step-0051-ui-debt-closure`, cut from `64b054a`). The register body
above is the 2026-08-27 STEP-46.3 record and is unchanged; this appendix records what later
verification proved about how CF-087 and the 46.4 test tier actually landed. Sources: the
2026-09-05 implementation audit
(`Code/mine-flow-docs/reports/2026-09-05-step-45-47-implementation-audit.md` §F-2/§F-3) and fresh
re-derivation on the STEP-51 branch head (2026-09-09, commands in audit §8).

### CF-087 "Residual Material widgets" — what actually shipped vs. what remains

**Delivered (genuinely zero at STEP-51 start, verified by anchored grep):** dialogs, buttons,
tiles, dividers, chips, and Material icons — `Icons.` (anchored `[^A-Za-z]Icons\.`) is 0 hits in
`lib/`; all 282 icon references are `LucideIcons.` (CF-088's migration is complete and real).

**Remains (re-derived counts, branch head, 2026-09-09):**

| Family | Files | Sites (hits) | forui 0.26.0 target (verified in pub cache) |
|---|---|---|---|
| `showSnackBar(` | 13 | 35 | `FToaster.show(context, toast: FToast(...))` — `widgets/toast/` |
| `SnackBar(` ctor | (same 13 files) | 35 (pairs with each showSnackBar) | `FToast` |
| `Scaffold(` | 24 | 35 | `FScaffold` — `widgets/scaffold.dart` |
| `AppBar(` | 14 | 19 | `FHeader` root/nested — `widgets/header/` |
| `CircularProgressIndicator(` | 22 | 25 | `FCircularProgress` — `widgets/progresses/circular_progress.dart` |

Material-import footprint: **71 of 238** `lib/` files import `package:flutter/material.dart`
(audit said 73 of 240 — drift from STEP-48/50 merges; file count changed 240→238).

Counting-trap notes for anyone re-deriving: a naive `SnackBar(` grep reads **70** because every
`showSnackBar(` contains the substring — count `showSnackBar(` (35, the true call sites) and the
standalone `SnackBar(` constructor separately. The same trap runs the other way for
`Scaffold(`/`AppBar(`: a naive grep reads 38/27 files because `FScaffold(` uses inflate it —
anchored `[^A-Za-z]Scaffold\(` yields the honest 24 files / 35 sites (3 further `FScaffold(` uses
already exist and are the reference pattern), and `[^A-Za-z]AppBar\(` yields 14 files / 19 sites.
`Icons.` without the anchor reads 282 because every `LucideIcons.` contains it.

The original register entry (CF-087, "Residual Material widgets", P3 systemic, Confirmed) named
"dialogs, alerts/snackbars, headers, selects, buttons" as the residue. The dialog/button halves
were swept; the snackbar/header/scaffold/progress halves were not. CF-087 was therefore roughly
half-delivered when STEP-46 closed as "all 97 fixed", and remains **open** pending STEP-51's
sweep substeps (51.2–51.6).

### CF-043 — residual structural half

STEP-48.30 (commit `bb32c92`) removed the dead `Tambah "…"` affordance by making
`CreatableCombobox` selection-only when `onCreateNew` is null, so free-text creation of
unenumerated methods is no longer possible at the widget level. However the register's
structural asks — "constrain method to the enumerated set" at the data level and "use one
shared control, not two" — remain unimplemented: two independent `CreatableCombobox<String>`
writing the same `record.method` still exist at
`lib/features/tracking/presentation/pages/land_clearing_entry_screen.dart:372` (Plan tab) and
`:485` (Actual tab), both fed by `_clearingMethods` (defined `:98`). Routed to substep 51.7.

### STEP-46.4 "add tests for each fix" — what the tier assignment actually produced

The register assigns an explicit test tier to **82 of 97** findings, not 84: 75 "Widget test",
3 "Widget/bloc test", 1 "Widget/integration test", 1 "Widget/route test", 1 "Static guard"
(CF-063, self-test exists at `test/tool/check_l10n_baseline_test.dart:119`), 1
"`flutter analyze` clean + targeted widget tests" (CF-087 itself). The remaining **15** carry
no-test lines: 13 "No test feasible…" + 2 "No automated contrast test feasible…" (CF-075,
CF-076). (The STEP-51 PLAN's "84 tiered / 80 Widget / 13 no-test" figures were off by two —
it counted CF-075/076's contrast lines as tiered. Corrected here.)

What actually shipped by the STEP-46 merge (`040def9`): +8 net test cases (361→369), zero new
test files, and only **13 of 97** CF ids cited anywhere under `test/`:

`CF-001, CF-002, CF-003, CF-017, CF-005, CF-015, CF-029, CF-056, CF-059, CF-032, CF-063,
CF-078, CF-079` — citing files: `test/widget/login_page_test.dart` (CF-001/002/003/056),
`test/widget/equipment_check_form_test.dart` (CF-017),
`test/widget/attendance_form_page_test.dart` (CF-015),
`test/features/settings/presentation/settings_page_test.dart` (CF-005/059),
`test/features/notifications/presentation/pages/notification_list_page_test.dart` (CF-032),
`test/features/data_bucket/presentation/pages/data_bucket_list_page_test.dart` (CF-029),
`test/features/data_bucket/presentation/pages/upload_file_page_test.dart` (CF-078),
`test/features/data_bucket/presentation/bloc/data_bucket_bloc_test.dart` (CF-079),
`test/tool/check_l10n_baseline_test.dart` (CF-063).

The prompt's own escape hatch `// TODO(STEP-46.4): test not written because …` was used **0**
times. 23 further CF ids are cited under `integration_test/`. The fixes themselves were real
and spot-verified by the audit; they are simply unguarded. The 46.4 debt is therefore **open**
pending substep 51.8, which will either add CF-id-citing widget tests for the
behaviour-carrying findings or record a per-finding reason, per decision D4.
