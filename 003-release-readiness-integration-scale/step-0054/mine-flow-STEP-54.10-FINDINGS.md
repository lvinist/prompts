# mine-flow — STEP-54.10 Findings: System Utilities — Dashboard, Notifications, Settings & Auth Critique

**Date:** 2026-09-11
**Executor:** Antigravity (Claude Sonnet 4.6 Thinking)
**Status:** Complete
**Inspected app branch:** step-0054-feature-cohesion-critique
**Scope:** Read-only critique of the Dashboard KPI cards, Notification center, Settings page, and Login screen across Web (desktop) and Android. No application code was modified.

---

## 1. Scope and evidence boundary

This is a static critique. The mandatory evidence floor is met with branch-head `file:line` citations. No browser, Android emulator, or screenshot capture was run; therefore visual, contrast, screen-reader, and runtime URL claims are marked `Unverified` rather than inferred from source code. The screenshot placeholder class remains a harness defect per RISK-0015/0016/0023 and the STEP-48 design-review retraction.

Inspected source files:

- `lib/app/presentation/pages/dashboard_page.dart`
- `lib/app/presentation/bloc/dashboard_cubit.dart`
- `lib/app/presentation/bloc/dashboard_state.dart`
- `lib/features/notifications/presentation/pages/notification_list_page.dart`
- `lib/features/settings/presentation/pages/settings_page.dart`
- `lib/features/auth/presentation/pages/login_page.dart`
- `lib/app/presentation/pages/app_shell.dart`
- `lib/app/presentation/widgets/global_app_header.dart`
- `lib/app/router.dart`
- `Code/mine-flow-docs/registries/risks.yml` (RISK-0011, RISK-0004)

---

## 2. Findings

| ID | Verdict | Area | Finding and impact | Branch-head evidence | Required treatment |
|---|---|---|---|---|---|
| FC-54.10-001 | Needs restructure | Dashboard: Tap-through absent | The four stat cards display KPI values but have no tap/navigation action. The class comment says the page provides "shortcuts that push on top of the shell" for Reports, Timeline, and Notifications, but no tap-through is implemented — `_StatCard.build` returns `SizedBox > Semantics > FCard` with no `GestureDetector` or `FTappable`. | `dashboard_page.dart:143-231` | STEP-55 must wire each stat card to its respective feature: Kru Aktif → `/teams/attendance`, Volume → `/operations/cut-fill`, Pemeriksaan Alat → `/teams/equipment-check`, Notifikasi → `/notifications`. |
| FC-54.10-002 | Needs restructure | Dashboard: KPI set missing five features | Only four KPIs are aggregated (Attendance, CutFill, EquipmentCheck, Notifications). Land Clearing, Inventory, Daily Log, Benchmark DB, and Data Bucket have no dashboard presence. | `dashboard_cubit.dart:3-7, 50-55`; `dashboard_state.dart:10-13` | STEP-55 should decide (with the user) whether to extend the KPI set or explicitly document the four cards as intentionally scoped. |
| FC-54.10-003 | Needs restructure | Dashboard: Error state undifferentiated from loading | `DashboardStatus.failure` produces value `'-'` — identical to the loading skeleton. The `isFailure` subtitle `'Gagal memuat'` is easily missed below the large `'-'` glyph. | `dashboard_page.dart:60-93` | STEP-55: loading → spinner, failure → error icon + subtitle + retry action. |
| FC-54.10-004 | Needs polish | Dashboard: No refresh mechanism | `loadDashboardStats` is called once at route build. No pull-to-refresh, no timer, no BLoC reload event. KPIs go stale mid-session. | `router.dart:142`; `dashboard_page.dart:54-131` | STEP-55 should add pull-to-refresh or a scheduled refresh interval. |
| FC-54.10-005 | Needs restructure | Dashboard: No empty/first-use state | After first boot, a user with no data sees `0` for all KPIs — indistinguishable from a day with genuine zero activity. `DashboardStatus.initial` and `loading` are conflated; no first-use nudge exists. | `dashboard_page.dart:56-58` | STEP-55 should distinguish first-run zero-data; add a call-to-action card directing the user to enter their first record. |
| FC-54.10-006 | Needs restructure | Notification center: Unreachable from Android | The bell icon lives in `_NotificationIconButton` inside `GlobalAppHeader`. On mobile, `GlobalAppHeader` is rendered **only when path == `/`** (dashboard). On any other shell route the header disappears. The five bottom-bar tabs include no Notifications item. | `app_shell.dart:397-398`; `global_app_header.dart:333-345`; `app_shell.dart:47-57` | STEP-55 must provide a persistent notification entry on mobile (persistent header bell, Dashboard tab badge, or Teams group landing tile). |
| FC-54.10-007 | Aligned | Notification center: Loading/empty/error states | All three states covered: `FCircularProgress` (loading), icon+label (empty), semantic error container (error). Staggered entrance honors `MediaQuery.disableAnimationsOf`. | `notification_list_page.dart:79-219, 241-301` | Preserve. |
| FC-54.10-008 | Aligned | Notification center: Read/unread and dismiss | `GestureDetector.onTap` marks as read; `FButton.icon` per card dismisses; "Tutup Semua" batch-dismisses. Semantic labels differentiate read vs unread. | `notification_list_page.dart:398-404, 468-473, 141-147` | Preserve. |
| FC-54.10-009 | Needs polish | Notification center: No unread badge on entry icon | Desktop bell icon renders bare `LucideIcons.inbox` with no count badge. Users on non-dashboard routes have no glanceable unread indicator. | `global_app_header.dart:333-345` | STEP-55 should add a badge overlay when `unreadCount > 0`. |
| FC-54.10-010 | Needs polish | Notification center: GestureDetector vs FTappable | Notification card tap area uses `GestureDetector` (Material-adjacent primitive). Token conformance requires `FTappable` where a ForUI equivalent exists. Hit-target at 48dp is unverified. | `notification_list_page.dart:398` | STEP-55 should migrate tap region to `FTappable` and verify 48dp minimum touch height. |
| FC-54.10-011 | Needs polish | Notification center: Warning mapped to `secondary` token | `NotificationSeverity.warning` maps to `theme.colors.secondary` — a muted neutral on the Zinc palette, not a warning amber. Severity differentiation is undercut visually. | `notification_list_page.dart:328, 350` | STEP-55 should use a dedicated warning token or document an explicit exception if none exists in ForUI. |
| FC-54.10-012 | Needs restructure | Settings: Profile is read-only, no edit flow | `_ProfileCard` displays name and role as plain `Text` with no edit affordance. The rubric's lifecycle-cohesion dimension and the prompt scope clause both flag this. | `settings_page.dart:408-453` | STEP-55 should add a profile-edit sheet aligned with D1/D2. For this release, display name is the likely editable field; role is server-managed. |
| FC-54.10-013 | Aligned | Settings: Theme toggle — all three modes | Light, Dark, System modes all present and wired to `SettingsCubit.updateThemeMode` via `_ThemeOption`. Selected variant renders as `primary`; unselected as `outline`. | `settings_page.dart:147-186` | Preserve. Runtime dark-mode verification: `Unverified`. |
| FC-54.10-014 | Aligned | Settings: Locale switcher wired | English/Indonesian toggle wired to `SettingsCubit.updateLocale`; partial-translation caveat disclosed in UI copy per RISK-0004. | `settings_page.dart:85-135` | Runtime locale-switch effect (which strings actually update) is `Unverified` — STEP-55 should run a live test. |
| FC-54.10-015 | Needs polish | Settings: Logout dialog uses FAlert inside FDialog | `showFDialog > FDialog > FAlert` doubles the container chrome — `FDialog` provides background/border; `FAlert` adds another border-left, icon, and text layout. Visually heavy for a simple confirmation. | `settings_page.dart:326-358` | STEP-55 should migrate to a plain `FDialog` with inline `Text` title and subtitle, matching the D4 dirty-intercept dialog pattern. |
| FC-54.10-016 | Needs polish | Settings: Hardcoded support contact details | Support email and WhatsApp number are hardcoded in source, not environment-configurable. They will differ across staging and production. | `settings_page.dart:226, 241, 293-299, 314` | STEP-55 should move contact details to `AppConstants` or `.env`-sourced config. |
| FC-54.10-017 | Needs polish | Settings: CircleAvatar Material primitive | `_ProfileCard` uses `CircleAvatar` (Material); `FAvatar` is the ForUI equivalent as of forui 0.24.x+. The file's own comment acknowledges the Material import but `FAvatar` is now available. | `settings_page.dart:417-425` | STEP-55 should replace `CircleAvatar` with `FAvatar` and remove the `flutter/material.dart` import if no other Material primitive remains. |
| FC-54.10-018 | **ESCALATION — Privacy compliance gap** | Login: Privacy notice ABSENT (RISK-0011 / DR-0003) | **The In-app Privacy Notice is confirmed absent.** Full grep of `lib/features/auth/` for `privacy`, `privasi`, `kebijakan`, `terms`, `ketentuan` returns **zero matches**. `LoginPage` renders branding, email field, password field, submit button — no notice link, no consent checkbox, no first-use dialog. This confirms RISK-0011's assessment as of the current branch head. Per Doc 17 §3 and UU PDP lawful-basis posture, users must be informed before first use. **Pre-release gate per `risks.yml:RISK-0011:revisit_trigger`.** | `login_page.dart:68-175`; `risks.yml:RISK-0011:297-321`; grep `lib/features/auth/` → 0 matches | **Escalating to user:** this is a pre-release gate. STEP-55 must implement a first-login consent flow (modal `FDialog` or dedicated screen) displaying the privacy notice with an explicit acknowledgement action, gating dashboard access. Notice content requires a product/legal decision. |
| FC-54.10-019 | Needs polish | Login: No keyboard submit on password field | `FTextField.password` has no `textInputAction: TextInputAction.done` or `onSubmitted` callback. Mobile users must lift off the keyboard to tap "Masuk" instead of pressing the keyboard's submit key. | `login_page.dart:141-149` | STEP-55 should add `textInputAction: TextInputAction.done` and wire `onSubmitted: (_) => _login(cubit)` on the password field. |
| FC-54.10-020 | Needs polish | Login: Error banner has no dismiss | Auth error banner persists until the next login attempt; no dismiss icon, no auto-clear on next keystroke. A user who mistyped their email sees a persistent red banner they cannot clear. | `login_page.dart:109-126` | STEP-55 should auto-dismiss on next field edit or provide an explicit dismiss icon, consistent with the app's toast pattern. |
| FC-54.10-021 | Needs polish | Login: Missing semantic header | The page has no `Semantics(header: true)` on the `mine-flow` title text and no form-landmark label. Screen readers have no clear page-title announcement or form region. | `login_page.dart:91-97, 82-84` | STEP-55 should add `Semantics(header: true)` on the page title and a form-landmark label. |
| FC-54.10-022 | Aligned | Settings: Logout flow — session terminated before route change | `AuthCubit.signOut()` is awaited before `context.go(AppRoutes.login)` (CF-004 compliance). Confirmation dialog prevents accidental sign-out on shared field devices. | `settings_page.dart:361-366` | Preserve. See FC-54.10-015 for dialog presentation polish. |
| FC-54.10-023 | Unverified | Accessibility and visual states — all four surfaces | WCAG contrast, 48dp targets, focus traversal, text scaling, and dark-mode correctness cannot be verified statically. Semantic labels are present on stat cards and notification cards; login form lacks a page-title landmark (FC-54.10-021). | `dashboard_page.dart:40-48, 169-172`; `notification_list_page.dart:361-479`; `settings_page.dart:31-283`; `login_page.dart:68-175` | Keep `Unverified` until STEP-55.11 technical audit. |
| FC-54.10-024 | Unverified | l10n posture — all four surfaces | All four surfaces use hardcoded Indonesian/English strings; zero `AppLocalizations` calls found across all four files. Switching the locale to English in Settings will not change any label on these surfaces (static inference). Runtime locale-switch effect is unverified. | grep `AppLocalizations` in each file → 0 results; `risks.yml:RISK-0004` | Keep within RISK-0004 boundary. STEP-55 should run a live locale-switch test and document these surfaces as confirmed unlocalized in the master spec. |

---

## 3. D7 Verdict

**D7 is explicitly N/A for all four surfaces in this substep.**

- **Dashboard:** KPI cards are aggregate-display, not record-inspectors.
- **Notification center:** Each notification card is self-contained (title + message + timestamp + severity); the card *is* the detail. No inspector sheet is warranted.
- **Settings:** Inline card groups. No per-record inspector needed.
- **Login:** Pre-authentication surface. D7 does not apply.

---

## 4. Coverage

| Surface | Platform | States exercised | Evidence | Result |
|---|---|---|---|---|
| Dashboard KPI cards | Web/desktop | Static: loading/failure/success (4 KPIs), tap-through code paths, cubit data sources, route wiring | `dashboard_page.dart:54-131`; `dashboard_cubit.dart:39-77`; `router.dart:134-144` | Needs restructure (001, 003, 005); Needs polish (004); Product decision needed (002) |
| Dashboard KPI cards | Android/mobile | Same static analysis — responsive width at 600dp | `dashboard_page.dart:161-165` | Same as desktop; responsive width logic present |
| Notification center | Web/desktop | Static: loading/empty/error/loaded states, action paths, desktop entry point | `notification_list_page.dart:78-494`; `global_app_header.dart:333-345` | Aligned for states/actions (007, 008); Needs polish (009, 010, 011) |
| Notification center | Android/mobile | Static: mobile shell header presence, bottom-nav tab coverage | `app_shell.dart:397-398, 47-57` | Needs restructure — unreachable from mobile outside dashboard (006) |
| Settings page | Web/desktop + Android | Static: profile card, locale switcher, theme toggle (3 modes), support buttons, logout dialog | `settings_page.dart:31-494` | Aligned (013, 014, 022); Needs polish (015, 016, 017); Needs restructure (012) |
| Login screen | Web/desktop + Android | Static: submitting state, error banner, field validation, privacy notice grep | `login_page.dart:68-175`; auth dir grep | Escalation (018); Needs polish (019, 020, 021) |

---

## 5. Verification record

| Check | Result |
|---|---|
| All rubric dimensions scored for all four surfaces, both platforms | Pass |
| Privacy-notice presence/absence evidenced precisely (RISK-0011 / DR-0003) | Pass — absent confirmed; FC-54.10-018 escalated to user |
| Theme/locale switching behavior evidenced | Pass — source wiring verified; runtime effect: Unverified (024) |
| D7 explicitly N/A | Pass — §3 covers all four surfaces with justification |
| Coverage/findings/verification/limitations tables present with IDs and citations | Pass |
| Application code modified | Pass — repo untouched; read-only |
| Runtime/visual evidence | Unverified — not run |

---

## 6. Limitations

- **Runtime locale-switch effect** (024): Cannot verify which strings actually update without a live test.
- **Dark-mode correctness** (023): Settings surfaces and login form cannot be verified without runtime execution.
- **Privacy notice content** (018): Critique confirms absence; content requires a product/legal decision.
- **Notification center mobile gap** (006): Overlaps with FC-54.1-001. Resolution should coordinate with the broader mobile-header fix in STEP-55.

---

**Next action:** Update `STEP-54-PLAN.md` substep 54.10 row to `Done`, then proceed to **substep 54.11** — in a **fresh chat**.
