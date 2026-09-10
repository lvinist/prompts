# mine-flow — STEP-54.9–54.10a Consolidated Findings Ledger Slice

**Built:** 2026-09-11
**Branch verified:** `step-0054-feature-cohesion-critique` (`Code/mine-flow-app`)
**Inputs:** `mine-flow-STEP-54.9-FINDINGS.md`, `mine-flow-STEP-54.10-FINDINGS.md`, `mine-flow-STEP-54.10a-FINDINGS.md`
**Scope:** Part A ledger slice for STEP-54.11; findings reconciliation only. No application code or durable docs were changed.

## 1. Completeness and verdict totals

The slice accounts for **53 unique findings**: 10 from 54.9, 24 from 54.10, and 19 from 54.10a. Verdict totals are **18 Needs restructure**, **15 Needs polish**, **12 Aligned**, **5 Unverified**, and **3 escalations**. IDs are contiguous within each source range and no duplicates were found.

| Source | Expected range | Count | Result |
|---|---:|---:|---|
| STEP-54.9 | `FC-54.9-001..010` | 10 | Complete |
| STEP-54.10 | `FC-54.10-001..024` | 24 | Complete |
| STEP-54.10a | `FC-54.10a-001..019` | 19 | Complete |

## 2. Consolidated ledger

| ID | Verdict | Area | One-line summary | Evidence |
|---|---|---|---|---|
| FC-54.9-001 | Needs restructure | Data Bucket: D5 form routing | The list page opens Upload and Detail pages via `Navigator.push(MaterialPageRoute(...))` rather than GoRouter named routes, even though `/tools/data-bucket/upload` and `/:id` exist. | `data_bucket_list_page.dart:320-334`, `367-379` |
| FC-54.9-002 | Needs restructure | Data Bucket: D1/D2 Sheet Modality & D4 Interception | The Upload form is a full-page push (`FScaffold` on mobile, no header on desktop) without a `PopScope`. | `upload_file_page.dart:73`, `310-336` |
| FC-54.9-003 | Needs restructure | Data Bucket: Upload Cancellation | Upload progress exists, but the back action is disabled during upload and no explicit cancellation action is available. | `upload_file_page.dart:328` |
| FC-54.9-004 | Aligned | Data Bucket: Upload Failure Recovery | Upload errors display a toast with a "Coba Lagi" action that retries `_submitUpload()` without requiring the user to re-select the file, as `_fileBytes` is preserved in state. | `upload_file_page.dart:291-303` |
| FC-54.9-005 | Aligned | Data Bucket: File-size feedback | Enforces a `_kMaxFileSizeBytes` check before reading into memory, and displays a formatted size under the selected file icon prior to commit. | `upload_file_page.dart:178-188`, `472-478` |
| FC-54.9-006 | Aligned | Data Bucket: Lifecycle Cohesion | List → Form/Detail → Back loops properly execute a `RefreshFiles()` event upon returning, avoiding stale data. | `data_bucket_list_page.dart:333`, `377` |
| FC-54.9-007 | Aligned | Work Timeline: Read-only Cohesion | Timeline exposes only a date-range selector and milestone cards. | `timeline_page.dart:64-80`, `timeline_page.dart:238-275`, `milestone_card.dart:35` |
| FC-54.9-008 | Aligned | Report Path (Both Features) | Deliberate absence of a report action in both Data Bucket (documented as "no meaningful report type") and Work Timeline. | `data_bucket_list_page.dart:360-362`, `timeline_page.dart:90-130` |
| FC-54.9-009 | Needs polish | Token conformance | Both features utilize `FTheme` tokens (no raw colors found) and rely on a transparent `Material` wrapper for `PopupMenuButton` interoperability, but `DataBucketListPage` still uses a Material `FloatingActionButton.extended` for the upload action, `UploadFilePage` uses Material `showDatePicker` and `InputDecorator` for the acquisition date field, and `MilestoneCard` uses `InkWell` instead of `FTappable`. | `data_bucket_list_page.dart:362-383`, `upload_file_page.dart:211-216`, `383-398`, `milestone_card.dart:35` |
| FC-54.9-010 | Unverified | Accessibility & Tokens | Keyboard focus and a11y contrast remain untested at runtime. | `file_detail_page.dart:102`, `data_bucket_list_page.dart:84` |
| FC-54.10-001 | Needs restructure | Dashboard: Tap-through absent | The four stat cards display KPI values but have no tap/navigation action. | `dashboard_page.dart:143-231` |
| FC-54.10-002 | Needs restructure | Dashboard: KPI set missing five features | Only four KPIs are aggregated (Attendance, CutFill, EquipmentCheck, Notifications). | `dashboard_cubit.dart:3-7, 50-55`; `dashboard_state.dart:10-13` |
| FC-54.10-003 | Needs restructure | Dashboard: Error state undifferentiated from loading | `DashboardStatus.failure` produces value `'-'` — identical to the loading skeleton. | `dashboard_page.dart:60-93` |
| FC-54.10-004 | Needs polish | Dashboard: No refresh mechanism | `loadDashboardStats` is called once at route build. | `router.dart:142`; `dashboard_page.dart:54-131` |
| FC-54.10-005 | Needs restructure | Dashboard: No empty/first-use state | After first boot, a user with no data sees `0` for all KPIs — indistinguishable from a day with genuine zero activity. | `dashboard_page.dart:56-58` |
| FC-54.10-006 | Needs restructure | Notification center: Unreachable from Android | Notifications are only reachable through the mobile header on Dashboard; the persistent five-tab bar has no Notifications entry. | `app_shell.dart:397-398`; `global_app_header.dart:333-345`; `app_shell.dart:47-57` |
| FC-54.10-007 | Aligned | Notification center: Loading/empty/error states | All three states covered: `FCircularProgress` (loading), icon+label (empty), semantic error container (error). | `notification_list_page.dart:79-219, 241-301` |
| FC-54.10-008 | Aligned | Notification center: Read/unread and dismiss | `GestureDetector.onTap` marks as read; `FButton.icon` per card dismisses; "Tutup Semua" batch-dismisses. | `notification_list_page.dart:398-404, 468-473, 141-147` |
| FC-54.10-009 | Needs polish | Notification center: No unread badge on entry icon | Desktop bell icon renders bare `LucideIcons.inbox` with no count badge. | `global_app_header.dart:333-345` |
| FC-54.10-010 | Needs polish | Notification center: GestureDetector vs FTappable | Notification card tap area uses `GestureDetector` (Material-adjacent primitive). | `notification_list_page.dart:398` |
| FC-54.10-011 | Needs polish | Notification center: Warning mapped to `secondary` token | `NotificationSeverity.warning` maps to `theme.colors.secondary` — a muted neutral on the Zinc palette, not a warning amber. | `notification_list_page.dart:328, 350` |
| FC-54.10-012 | Needs restructure | Settings: Profile is read-only, no edit flow | `_ProfileCard` displays name and role as plain `Text` with no edit affordance. | `settings_page.dart:408-453` |
| FC-54.10-013 | Aligned | Settings: Theme toggle — all three modes | Light, Dark, System modes all present and wired to `SettingsCubit.updateThemeMode` via `_ThemeOption`. | `settings_page.dart:147-186` |
| FC-54.10-014 | Aligned | Settings: Locale switcher wired | English/Indonesian toggle wired to `SettingsCubit.updateLocale`; partial-translation caveat disclosed in UI copy per RISK-0004. | `settings_page.dart:85-135` |
| FC-54.10-015 | Needs polish | Settings: Logout dialog uses FAlert inside FDialog | `showFDialog > FDialog > FAlert` doubles the container chrome — `FDialog` provides background/border; `FAlert` adds another border-left, icon, and text layout. | `settings_page.dart:326-358` |
| FC-54.10-016 | Needs polish | Settings: Hardcoded support contact details | Support email and WhatsApp number are hardcoded in source, not environment-configurable. | `settings_page.dart:226, 241, 293-299, 314` |
| FC-54.10-017 | Needs polish | Settings: CircleAvatar Material primitive | `_ProfileCard` uses `CircleAvatar` (Material); `FAvatar` is the ForUI equivalent as of forui 0.24.x+. | `settings_page.dart:417-425` |
| FC-54.10-018 | ESCALATION — Privacy compliance gap | Login: Privacy notice ABSENT (RISK-0011 / DR-0003) | Privacy notice/first-use consent is absent statically; this is a pre-release compliance gate. | `login_page.dart:68-175`; `risks.yml:RISK-0011:297-321`; grep `lib/features/auth/` → 0 matches |
| FC-54.10-019 | Needs polish | Login: No keyboard submit on password field | `FTextField.password` has no `textInputAction: TextInputAction.done` or `onSubmitted` callback. | `login_page.dart:141-149` |
| FC-54.10-020 | Needs polish | Login: Error banner has no dismiss | Auth error banner persists until the next login attempt; no dismiss icon, no auto-clear on next keystroke. | `login_page.dart:109-126` |
| FC-54.10-021 | Needs polish | Login: Missing semantic header | The page has no `Semantics(header: true)` on the `mine-flow` title text and no form-landmark label. | `login_page.dart:91-97, 82-84` |
| FC-54.10-022 | Aligned | Settings: Logout flow — session terminated before route change | `AuthCubit.signOut()` is awaited before `context.go(AppRoutes.login)` (CF-004 compliance). | `settings_page.dart:361-366` |
| FC-54.10-023 | Unverified | Accessibility and visual states — all four surfaces | WCAG contrast, 48dp targets, focus traversal, text scaling, and dark-mode correctness cannot be verified statically. | `dashboard_page.dart:40-48, 169-172`; `notification_list_page.dart:361-479`; `settings_page.dart:31-283`; `login_page.dart:68-175` |
| FC-54.10-024 | Unverified | l10n posture — all four surfaces | All four surfaces use hardcoded Indonesian/English strings; zero `AppLocalizations` calls found across all four files. | grep `AppLocalizations` in each file → 0 results; `risks.yml:RISK-0004` |
| FC-54.10a-001 | Needs restructure | Desktop shell navigation | The entire desktop sidebar navigation is absent from the accessibility tree, so a screen-reader or keyboard-only user cannot reach any of the nine feature workflows. | AX tree = 4 nodes (§3.3); 11 `flt-semantics` with no nav node; `app_shell.dart:285-365`; artifacts 02/03 |
| FC-54.10a-002 | Needs restructure | Global header controls | Search, theme toggle, notifications, and profile produce no semantics in either layout, although each has a source `Semantics(label: …)`. | AX tree has no such nodes (§3.1/3.3); `global_app_header.dart:82-83,195-196,269-270,312-313,336-337,361-362,387-388`; artifacts 02/03 |
| FC-54.10a-003 | Needs restructure | Login form naming | The password textbox exposes an empty accessible name and the email textbox is named by its placeholder (`admin@mineflow.id`) rather than its visible label, so AT users cannot tell the fields apart (WCAG 4.1.2). | AX tree §3.1; `login_page.dart:120-149`; artifacts 01/18 |
| FC-54.10a-004 | Needs polish | Login heading | The “mine-flow” title has no heading role, so there is no page-title landmark to announce (WCAG 1.3.1/2.4.6); the dashboard does produce `heading "Dashboard"`, so headings work elsewhere. | AX tree §3.1; confirms FC-54.10-021 |
| FC-54.10a-005 | Needs restructure | Document language | `document.documentElement.lang = "en"` while every captured surface is Indonesian, so screen readers pronounce the content in the wrong language (WCAG 3.1.1). | `lang` read at runtime; all artifacts |
| FC-54.10a-006 | Needs polish | Touch-target size | Several controls are below the 48dp target: “Show password” 40×40, “Masuk” 368×44, login field rows 44 (DOM inputs 50), Settings locale buttons 44, and both logout-dialog buttons 44 (Batal 62×44, Keluar 73×44). | Semantics rects §3.1 + Settings dump; artifacts 01/04/15 |
| FC-54.10a-007 | Aligned | Mobile primary navigation | The runtime exposes exactly five labelled tabs (`Dashboard… Settings`, “Tab N of 5”) with a correct focus order, satisfying Doc 07 §4 on mobile — and standing in clear contrast to the desktop sidebar (001). | AX tree §3.3; `app_shell.dart:47-57` |
| FC-54.10a-008 | Needs restructure | Notifications reachability | Neither layout exposes a Notifications entry: the mobile five-item bar has no Notifications tab, and the desktop bell produces no semantics. | AX trees §3.3; `app_shell.dart:397-398`; `app_shell.dart:47-57` |
| FC-54.10a-009 | Needs restructure | Dashboard KPI interactivity | The four KPI cards expose no role and no action (only the group label “Statistik ringkasan”), so the promised “shortcuts” do not exist for any user; runtime-confirms FC-54.10-001. | AX tree §3.3; vision of artifact 02; `dashboard_page.dart:143-231` |
| FC-54.10a-010 | Needs polish | System theme reactivity | In `ThemeMode.system` the app does not re-render when the OS/browser theme changes: emulating `prefers-color-scheme: light` left the frame unchanged (mean RGB stayed dark, artifact bytes ~identical), and `app.dart:44-48` reads `PlatformDispatcher.instance.platformBrightness` inside a `BlocBuilder` that only rebuilds on a `SettingsCubit` emit. | mean-RGB evidence (§2); `app.dart:44-48`; `settings_page.dart` theme modes |
| FC-54.10a-011 | Aligned | Theme structural consistency | Both themes render every surface with matching structure: light artifacts average ~RGB(255,248,255) and dark ~RGB(22,14,24), with the same layout and no clipping/overlap observed at either viewport. | artifacts 02–19; mean-RGB per artifact |
| FC-54.10a-012 | Unverified | Colour contrast | WCAG contrast ratios were not measured; artifacts exist but no ratio computation was run. | — |
| FC-54.10a-013 | Unverified | Motion & reduced-motion | Doc 07's 150–200ms motion and reduced-motion honouring could not be evidenced with a still-capture harness. | — |
| FC-54.10a-014 | Needs restructure | Form presentation (D1/D2) | The benchmark entry form renders as a full pushed page at both viewports, not the locked right-side sheet (Web, D1) or bottom sheet (Android, D2), and no scrim/modal is present — despite the route being URL-backed. | artifacts 07–10; `router.dart:290-299` |
| FC-54.10a-015 | Needs restructure | Report presentation (D6) | “Reports” resolves to a standalone `/reports/config` route showing a type picker outside the shell (no sidebar/bottom bar), not the contextual `FDialog` bound to a list's `ReportType`; opening it loses the originating feature/filter context. | artifacts 11–14; `router.dart:489-509` |
| FC-54.10a-016 | ESCALATION — secrets boundary | Android run / logging | Android debug HTTP logging emitted the Supabase anon key in full; raw output was destroyed and the run stopped. | hash-equality check (value never printed); `.env` |
| FC-54.10a-017 | ESCALATION — privacy compliance | Login consent | Runtime captures and AX output confirm the privacy notice/consent gate is absent. | artifacts 01/17/18/19; AX tree §3.1; `risks.yml:RISK-0011` |
| FC-54.10a-018 | Needs polish | Header identity | The desktop header profile is hardcoded to “Pengguna” / “Foreman” for every session, while the authenticated account is a Supervisor and Settings shows the real “Alex Supervisor / Supervisor”. | `global_app_header.dart:416,423`; Settings dump §2; vision of artifact 02 |
| FC-54.10a-019 | Needs restructure | Detector no-signal | The CanvasKit UI is invisible to the DOM/CSS detector; its only URL hit was a hidden-probe false positive. | §4; CanvasKit shadow-DOM canvas proof |

## 3. Reconciliation and adjudication

No findings conflict in a way that requires one to be struck. The runtime pass mostly confirms or narrows the static findings. Keep every ID for traceability, but map the overlaps below to single STEP-55 work items so they are not implemented twice.

| Finding | Adjudication |
|---|---|
| FC-54.10-001 | Confirmed and strengthened by runtime FC-54.10a-009; keep both IDs and implement one KPI-interactivity work item. |
| FC-54.10-006 | Confirmed and broadened by runtime FC-54.10a-008; one cross-platform notification-reachability work item owns both IDs. |
| FC-54.10-018 | Same compliance gap as runtime FC-54.10a-017; keep both IDs, with 54.10a supplying runtime proof. |
| FC-54.10-021 | Confirmed by runtime FC-54.10a-004; treat the runtime verdict as the stronger evidence and retain both IDs. |
| FC-54.10-023 | Partially closed by 54.10a: focus/semantics, touch targets, and theme structure now have verdicts; contrast and motion remain Unverified. |
| FC-54.10-024 | Static hardcoded-string finding remains; runtime locale switching was not exercised, so the runtime-effect portion remains Unverified. |

Additional scope adjudications:
- **Data Bucket D7:** retain the 54.9 verdict: Web right-side inspector and Mobile bottom-sheet inspector, with the `/:id` route preserved and the list rendered beneath it.
- **Work Timeline:** retain the read-only decision and deliberate report absence; no milestone-entry sheet is required for this release.
- **Detector result:** FC-54.10a-019 is an evidence-method constraint, not an application feature backlog item. Carry it into the master spec's evidence appendix and STEP-55.11 audit procedure.
- **Anon-key logging:** FC-54.10a-016 remains a separate hygiene escalation; do not merge it into the privacy-consent gate.

## 4. Needs-restructure citation re-resolution

All **18** `Needs restructure` findings were checked against the current app branch. Source ranges still resolve; runtime-only claims retain their artifact/AX evidence. No finding was struck or relocated.

| ID | Branch-head result |
|---|---|
| FC-54.9-001 | Pass — list still uses MaterialPageRoute at 320–334 and 367–379 while named child routes exist at router.dart:183–215. |
| FC-54.9-002 | Pass — upload remains a full FScaffold at 310–336; no PopScope is present in the file. |
| FC-54.9-003 | Pass — upload back action remains disabled while uploading at 326–330; no cancel action is exposed. |
| FC-54.10-001 | Pass — _StatCard remains presentation-only at 143–231 with no action callback. |
| FC-54.10-002 | Pass — DashboardCubit still fetches exactly four sources at 49–55 and emits four KPI fields at 57–64. |
| FC-54.10-003 | Pass — failure still uses the same '-' value path as loading at dashboard_page.dart:56–93. |
| FC-54.10-005 | Pass — initial/loading remain conflated at 56–58 and success zero has no first-use branch. |
| FC-54.10-006 | Pass — mobile header remains dashboard-only at app_shell.dart:397–398 and the five tabs remain 47–57. |
| FC-54.10-012 | Pass — profile remains display-only at settings_page.dart:408–453. |
| FC-54.10a-001 | Pass — desktop shell still builds the sidebar/header at app_shell.dart:300–370; runtime AX evidence remains authoritative for the missing exposure. |
| FC-54.10a-002 | Pass — source Semantics wrappers still exist in global_app_header.dart; runtime AX evidence remains authoritative because they do not survive rendering. |
| FC-54.10a-003 | Pass — login fields remain at login_page.dart:128–149; runtime AX names remain authoritative. |
| FC-54.10a-005 | Pass — runtime-only language observation; all-artifact evidence remains the citation because no app source sets the Web document language here. |
| FC-54.10a-008 | Pass — source reachability remains app_shell.dart:47–57,397–398; runtime AX evidence confirms neither effective entry is exposed. |
| FC-54.10a-009 | Pass — _StatCard remains non-actionable at dashboard_page.dart:143–231; runtime AX evidence confirms no role/action. |
| FC-54.10a-014 | Pass — benchmark form is still a GoRoute page builder at router.dart:290–299; runtime artifacts prove full-page presentation. |
| FC-54.10a-015 | Pass — report config remains a standalone type-picker/page route at router.dart:489–509; runtime artifacts prove context loss. |
| FC-54.10a-019 | Pass — runtime detector/CanvasKit finding; no branch-head source relocation is required. |

## 5. Evidence debt carried to STEP-55.11

| Finding | Remaining blocker / audit obligation |
|---|---|
| FC-54.9-010 | Data Bucket keyboard traversal and contrast were not run; verify on Chrome and Pixel_6a. |
| FC-54.10-023 | 54.10a closed semantics/focus, touch-target sampling, and theme-structure portions; text scaling and comprehensive per-surface accessibility still require audit. |
| FC-54.10-024 | Source confirms hardcoded strings; exercise the locale toggle at runtime and record exactly which labels change. |
| FC-54.10a-012 | Measure WCAG contrast ratios; screenshots alone are not a pass. |
| FC-54.10a-013 | Measure motion timing and test reduced-motion behavior; still captures cannot verify either. |
| Android authenticated shell | Capture remains unavailable because the Android run crossed the secrets/logging boundary (FC-54.10a-016); narrow Web evidence must not substitute for Android. |

## 6. Verification record

| Check | Result |
|---|---|
| Ledger extraction | Pass — 53 rows parsed from the three findings tables. |
| ID uniqueness and continuity | Pass — no duplicate or missing IDs in the three declared ranges. |
| Verdict accounting | Pass — 18 restructure + 15 polish + 12 aligned + 5 unverified + 3 escalations = 53. |
| `Needs restructure` citations | Pass — all 18 re-resolved or retained as explicit runtime evidence; §4. |
| Cross-substep overlap | Pass — six overlap/adjudication entries recorded; no contradictory finding dropped. |
| D7/report decisions in this slice | Pass — Data Bucket inspector retained; Work Timeline detail/report decisions explicit. |
| App repo cleanliness | Pass — `git status --short --branch` shows only the expected branch header and no changes. |
| Docs repo cleanliness | Pass — no changes. |
| Existing prompts change preserved | Pass — the pre-existing `prompts/STEP-index.md` modification was not touched. |

## 7. Slice handoff

Feed all 53 IDs into STEP-54.11's master ledger. Convert overlaps into shared spec items while preserving every source ID. The two user-facing gates remain explicit: **privacy notice/consent before release** (FC-54.10-018 + FC-54.10a-017) and **redaction/suppression of HTTP authorization-header logging before another Android evidence run** (FC-54.10a-016).
