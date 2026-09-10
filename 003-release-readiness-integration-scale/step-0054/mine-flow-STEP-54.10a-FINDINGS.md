# mine-flow — STEP-54.10a Findings: Impeccable-Skill Runtime Capture & a11y Evidence Closure

**Date:** 2026-09-11
**Executor:** Hermes/Claude Opus 4.8 (local script + browser-automation harness)
**Status:** Complete — evidence closure (review-only; no fixes)
**Inspected app branch:** `step-0054-feature-cohesion-critique`
**App revision:** `fe12531` (unchanged; repo left clean)
**Flutter / toolchain:** Flutter 3.47.1 stable · Dart 3.13.1 · `forui` ^0.26 (RISK-0009 pin) · Chrome 152 (harness) · AVD `Pixel_6a`
**Capture routes:** (1) Browser-Use CDP `Page.captureScreenshot` against `flutter run -d web-server` (authorized second route); (2) `adb exec-out screencap` against the `Pixel_6a` emulator.

## 1. Scope and evidence boundary

This substep produces **runtime evidence only** — no critique of its own, no application-code, doc, ADR, `risks.yml`, or bridge-file edits (`DESIGN.md` / `PRODUCT.md` untouched). It supersedes the `Unverified` runtime claims in the 54.1–54.10 findings and feeds 54.11's evidence appendix.

- **Static citations** are given for every claim that has a source counterpart.
- **Runtime claims** are backed by byte-and-pixel-measured artifacts (§2) or by the `flt-semantics`/browser AX trees (§3). Nothing is inferred from source alone.
- **The skill's mechanical detector is blind on this codebase** and is recorded as such (§4); a "no anti-patterns" result is explicitly **not** verification.
- The resolved skill canon is Doc 07 itself (ADR-0008); no canon conflict was found.

### 1.1 Pre-flight correction (`roots.json`) — recorded

`.impeccable/live/roots.json` originally resolved `appRoot/repoRoot/contextRoot` to the **workspace root** (`D:\AppDev\mine_flow`), so `context` reported `hasVisualImplementation: false, platform: null`. It was backed up (`.scratch-tmp/54.10a/roots.json.orig`) and repointed at `Code/mine-flow-app`.

**Correction detail (important for the next executor):** editing `roots.json` alone does **not** change `impeccable context` output — `context` re-derives roots from the **command cwd / git root**, not from the manifest (the manifest is consumed by the `live-*` helpers). The effective, reproducible fix is to run helper commands **from the child app cwd** (or with `--target Code/mine-flow-app`):

- from the workspace root → `projectRoot = D:\AppDev\mine_flow`, `hasVisualImplementation: false`
- from `Code/mine-flow-app` (or `--target Code/mine-flow-app`) → `projectRoot = repoRoot = D:\AppDev\mine_flow\Code\mine-flow-app` ✅ **app visible**

`hasVisualImplementation` stays `false` in both cases because the app is CanvasKit (no web dev-server config, DOM, or CSS to detect) — consistent with §4. From the app cwd, `productPath/designPath` resolve `null` because the ADR-0008 bridge files live at the workspace root, **above** the app repo's git root; they were not moved (forbidden).

## 2. Coverage & capture inventory

`flutter run -d web-server --web-port=8080 --web-hostname=127.0.0.1` with the README `--dart-define` recipe (`APP_ENV=local`); compile → served in **75.1 s**. Helper commands run from `Code/mine-flow-app`. Credentials used: the `.env` `TEST_SUPERVISOR_*` account (values never printed). Web viewports: **desktop 1258×566** (harness default) and **narrow 412×915** (CDP `Emulation.setDeviceMetricsOverride`, `mobile=true`). Themes: **dark** (browser `prefers-color-scheme: dark`) and **light** (in-app Settings → “Terang”).

| # | Artifact (in `Upcoming Prompts/step-54.10a-evidence/`) | Surface | Platform / viewport | Theme | Bytes | Dimensions |
|---|---|---|---|---|---|---|
| 01 | `login-desktop-dark-01.png` | Login | Web desktop 1258×566 | dark | 19,553 | 1258×566 |
| 02 | `dashboard-desktop-dark-02.png` | Shell + Dashboard | Web desktop | dark | 48,181 | 1258×566 |
| 03 | `dashboard-desktop-light-03.png` | Shell + Dashboard | Web desktop | light | 47,754 | 1258×566 |
| 04 | `settings-desktop-light-04.png` | Settings | Web desktop | light | 52,125 | 1258×566 |
| 05 | `dashboard-narrow-light-05.png` | Shell + Dashboard | Web narrow 412×915 | light | 32,628 | 412×915 |
| 06 | `dashboard-narrow-dark-06.png` | Shell + Dashboard | Web narrow | dark | 33,525 | 412×915 |
| 07 | `form-narrow-dark-07.png` | Benchmark form sheet | Web narrow | dark | 46,137 | 412×915 |
| 08 | `form-narrow-light-08.png` | Benchmark form sheet | Web narrow | light | 45,804 | 412×915 |
| 09 | `form-desktop-dark-09.png` | Benchmark form sheet | Web desktop | dark | 53,340 | 1258×566 |
| 10 | `form-desktop-light-10.png` | Benchmark form sheet | Web desktop | light | 52,946 | 1258×566 |
| 11 | `report-desktop-dark-11.png` | Report (type picker) | Web desktop | dark | 28,998 | 1258×566 |
| 12 | `report-desktop-light-12.png` | Report (type picker) | Web desktop | light | 29,490 | 1258×566 |
| 13 | `report-narrow-dark-13.png` | Report (type picker) | Web narrow | dark | 28,881 | 412×915 |
| 14 | `report-narrow-light-14.png` | Report (type picker) | Web narrow | light | 28,610 | 412×915 |
| 15 | `settings-desktop-dark-logout-15.png` | Settings + logout dialog | Web desktop | dark | 58,294 | 1258×566 |
| 16 | `login-desktop-dark-16.png` | Login (post-logout) | Web desktop | dark | 19,553 | 1258×566 |
| 17 | `login-narrow-dark-17.png` | Login | Web narrow | dark | 18,393 | 412×915 |
| 18 | `login-desktop-light-18.png` | Login | Web desktop | light | 19,427 | 1258×566 |
| 19 | `login-narrow-light-19.png` | Login | Web narrow | light | 18,218 | 412×915 |
| 20 | `android-login-portrait-20.png` | Login | **Android Pixel_6a portrait** | system/dark-boot | 71,067 | 1080×2400 |

**Producing command, every Web artifact:** `Page.bringToFront` → `Page.captureScreenshot(→ .png)` via the Browser-Use harness against `http://127.0.0.1:8080`. **Android:** `flutter run -d emulator-5554 … && adb -s emulator-5554 exec-out screencap -p`.

**Byte/dimension honesty:** the smallest artifact is **18,218 bytes**; every artifact's dimensions equal its stated viewport (no upscaling, no 1×1). **No artifact is in the 68-byte / 1×1 placeholder class** (RISK-0015/0016/0023/RISK-0024) — these replace that class with real captures. `login-desktop-dark-01` and `-16` are byte-identical (19,553) across two independent runs, showing the route is deterministic.

| Surface | Platform | Themes | States exercised | Evidence | Result |
|---|---|---|---|---|---|
| Login | Web desktop + narrow | light, dark | idle, disabled submit, filled | artifacts 01/16/17/18/19; AX tree §3.2 | Needs restructure (003, 004, 005, 017) |
| Shell (sidebar + header) | Web desktop | light, dark | expanded sidebar, header controls | artifacts 02/03; AX tree §3.3 | **Needs restructure — chrome invisible to AT (001, 002)** |
| Dashboard/KPI | Web desktop + narrow | light, dark | zero-data KPIs | artifacts 02/03/05/06; AX tree | Needs restructure (009) |
| Bottom navigation | Web narrow | light, dark | 5 items | artifacts 05/06; AX tree §3.3 | **Aligned (007)** |
| Benchmark form | Web desktop + narrow | light, dark | new-entry form | artifacts 07–10 | evidence for existing D1/D2 conflict (014) |
| Report | Web desktop + narrow | light, dark | type picker, 7 types | artifacts 11–14 | evidence for existing D6 conflict (015) |
| Settings (+logout dialog) | Web desktop | light, dark | theme/locale/support/logout dialog | artifacts 04/15 | Needs polish (profile 013) |
| Login | **Android Pixel_6a** | system-light | idle | artifact 20 | captured; shell leg aborted (016) |

## 3. Accessibility record (Doc 07 WCAG 2.1 AA target; rubric §2.4)

Semantics enabled by clicking `flt-semantics-placeholder` (`aria-label="Enable accessibility"`). Two independent trees were read: the `flt-semantics` DOM and the browser's authoritative `Accessibility.getFullAXTree`.

### 3.1 Login form — `flt-semantics` (16 nodes) and AX tree

`flt-semantics` nodes: container `role=group` at `[405,28,448,510]`; “mine-flow” title `[445,148,368,68]` (no role); “Sistem Monitoring & Manajemen Tambang”; “Email” label `[445,280,36,17]`; email field `[445,303,368,44]` (no role/name); “Kata Sandi” label; password field `[445,386,368,44]` (no role/name); **“Show password” `role=button`, `tabindex=0`, rect `[769,388,40,40]`**; “Masuk” `role=button`, `aria-disabled=true`, `[445,454,368,44]`.

Browser AX tree (7 non-generic nodes): `RootWebArea "mine-flow"` → `group` → `form` → `button "Masuk"`, `textbox "admin@mineflow.id"`, `textbox ""`, `button "Show password"`.

- Email textbox accessible name = **`admin@mineflow.id`** — its placeholder/hint, not “Email” (`login_page.dart:120-149`).
- Password textbox accessible name = **empty**.
- No `heading` node — the “mine-flow” title is not a page heading (confirms FC-54.10-021).
- `document.documentElement.lang = "en"` while the entire surface is Indonesian.

### 3.2 Login focus order

`flt-semantics` focusable set = **only** `button "Show password"` (`tabindex=0`). The native `<input>` elements are separately focusable (`tabIndex=0`) and carry `aria-label` `admin@mineflow.id` (email) and `null` (password), so keyboard reach exists via the inputs; the Flutter semantics layer contributes no field-name association.

### 3.3 Authenticated shell

- **Desktop dashboard AX tree = 4 nodes:** `RootWebArea "mine-flow"`, `group`, `heading "Dashboard"`, `group "Statistik ringkasan"`. **Zero navigation, links, buttons, or header controls.** The sidebar (`FSidebar`, `app_shell.dart:285-365`) and the global header (`GlobalAppHeader`) produce **no** `flt-semantics` nodes and **no** AX nodes, despite source `Semantics(label: …)` at `global_app_header.dart:82-83, 195-196, 269-270, 312-313, 336-337, 361-362, 387-388`. Enabling semantics and resizing did not add them (stayed at 11 `flt-semantics` nodes).
- **Narrow dashboard AX tree = 9 nodes:** `RootWebArea`, then **`button "Dashboard Tab 1 of 5"`, `"Tools Tab 2 of 5"`, `"Operations Tab 3 of 5"`, `"Teams Tab 4 of 5"`, `"Settings Tab 5 of 5"`**, `group`, `heading "Dashboard"`, `group "Statistik ringkasan"`. The mobile bottom bar is correctly labelled; its focus order is exactly those five tabs. **The mobile header still exposes no controls**, and **there is no Notifications tab.**

### 3.4 WCAG 2.1 AA scoring (what the tree actually exposes)

| Criterion | Runtime result |
|---|---|
| 1.3.1 Info & Relationships | Fail on desktop shell (no landmarks/nav exposed); pass for the mobile tab bar |
| 2.4.6 / 1.3.1 Headings | Login “mine-flow” has no heading role (fail); Dashboard has `heading "Dashboard"` (pass) |
| 2.4.1/2.4.3 Navigation & focus order | Desktop: no navigation in the tree (fail); mobile: 5 tabs in order (pass) |
| 3.1.1 Language of Page | Fail — `lang="en"` with Indonesian content |
| 4.1.2 Name, Role, Value | Login password field has no name; shell controls have no role/name (fail) |
| 2.5.5/2.5.8 Target size | Several controls < 48dp (§4 findings) |
| 1.4.3 Contrast | **Unverified** (no contrast measurement run) |

## 4. Detector honesty pass (`impeccable detect`)

| Probe | Command | Result |
|---|---|---|
| Dart source (dir) | `impeccable detect --json lib/` (from app cwd) | `[]` — **3 bytes, exit 0** |
| Dart source (file) | `impeccable detect --json lib/app/presentation/pages/app_shell.dart` | `[]` — **3 bytes, exit 0** |
| Live URL | `impeccable detect --json http://127.0.0.1:8080` | exit 2 — **1 hit**, `wide-tracking / "letter-spacing: 6.25em on body text"` |
| In-page overlay | inject `http://localhost:8400/detect.js`, call `impeccableDetect()` | 2 hits: `wide-tracking` on `<p>` (hidden) and `dark-glow #ffba00` on `body` |
| Blank page | same inject on `about:blank` | `[impeccable] No anti-patterns found.` |

**The 6.25em hit is a confirmed false positive.** The flagged node is Flutter's own hidden text-measurement probe: `<p aria-hidden="true" style="position:fixed; bottom:100%; visibility:hidden; opacity:0; pointer-events:none; …">` with computed `letter-spacing: 100px` (= 6.25em at the 16px default) and `offsetParent: null`. There is **no** `letter-spacing` in the app's `web/` or `lib/` (0 matches); the 5 Dart `letterSpacing` values are `-0.3, 0.3, 0.5, 0.8, 0.5` logical px. **Cause:** every rule is DOM/CSS-based, and CanvasKit renders into a single `<canvas>` inside `flt-glass-pane`'s shadow root (`canvasCount=1` at top level, context type `2d`) with no app DOM/CSS. **A clean detector result is therefore not design verification** — this is the finding, not a pass.

## 5. Findings

| ID | Verdict | Area | Finding and why it is a defect | Evidence (runtime + source) |
|---|---|---|---|---|
| FC-54.10a-001 | **Needs restructure** | Desktop shell navigation | The entire desktop sidebar navigation is absent from the accessibility tree, so a screen-reader or keyboard-only user cannot reach any of the nine feature workflows. The rubric's a11y dimension requires navigation landmarks with meaningful semantics; the app renders them visually but exposes none. | AX tree = 4 nodes (§3.3); 11 `flt-semantics` with no nav node; `app_shell.dart:285-365`; artifacts 02/03 |
| FC-54.10a-002 | **Needs restructure** | Global header controls | Search, theme toggle, notifications, and profile produce no semantics in either layout, although each has a source `Semantics(label: …)`. The intent exists in code but does not survive to the runtime tree, so these controls are unusable by AT. | AX tree has no such nodes (§3.1/3.3); `global_app_header.dart:82-83,195-196,269-270,312-313,336-337,361-362,387-388`; artifacts 02/03 |
| FC-54.10a-003 | **Needs restructure** | Login form naming | The password textbox exposes an empty accessible name and the email textbox is named by its placeholder (`admin@mineflow.id`) rather than its visible label, so AT users cannot tell the fields apart (WCAG 4.1.2). | AX tree §3.1; `login_page.dart:120-149`; artifacts 01/18 |
| FC-54.10a-004 | **Needs polish** | Login heading | The “mine-flow” title has no heading role, so there is no page-title landmark to announce (WCAG 1.3.1/2.4.6); the dashboard does produce `heading "Dashboard"`, so headings work elsewhere. | AX tree §3.1; confirms FC-54.10-021 |
| FC-54.10a-005 | **Needs restructure** | Document language | `document.documentElement.lang = "en"` while every captured surface is Indonesian, so screen readers pronounce the content in the wrong language (WCAG 3.1.1). | `lang` read at runtime; all artifacts |
| FC-54.10a-006 | **Needs polish** | Touch-target size | Several controls are below the 48dp target: “Show password” 40×40, “Masuk” 368×44, login field rows 44 (DOM inputs 50), Settings locale buttons 44, and both logout-dialog buttons 44 (Batal 62×44, Keluar 73×44). The Settings theme buttons (68) and support rows (46) are borderline/pass. | Semantics rects §3.1 + Settings dump; artifacts 01/04/15 |
| FC-54.10a-007 | **Aligned** | Mobile primary navigation | The runtime exposes exactly five labelled tabs (`Dashboard… Settings`, “Tab N of 5”) with a correct focus order, satisfying Doc 07 §4 on mobile — and standing in clear contrast to the desktop sidebar (001). | AX tree §3.3; `app_shell.dart:47-57` |
| FC-54.10a-008 | **Needs restructure** | Notifications reachability | Neither layout exposes a Notifications entry: the mobile five-item bar has no Notifications tab, and the desktop bell produces no semantics. This runtime-confirms FC-54.10-006 / FC-54.1-001. | AX trees §3.3; `app_shell.dart:397-398`; `app_shell.dart:47-57` |
| FC-54.10a-009 | **Needs restructure** | Dashboard KPI interactivity | The four KPI cards expose no role and no action (only the group label “Statistik ringkasan”), so the promised “shortcuts” do not exist for any user; runtime-confirms FC-54.10-001. | AX tree §3.3; vision of artifact 02; `dashboard_page.dart:143-231` |
| FC-54.10a-010 | **Needs polish** | System theme reactivity | In `ThemeMode.system` the app does not re-render when the OS/browser theme changes: emulating `prefers-color-scheme: light` left the frame unchanged (mean RGB stayed dark, artifact bytes ~identical), and `app.dart:44-48` reads `PlatformDispatcher.instance.platformBrightness` inside a `BlocBuilder` that only rebuilds on a `SettingsCubit` emit. A user who switches OS theme while the app is open sees no update. | mean-RGB evidence (§2); `app.dart:44-48`; `settings_page.dart` theme modes |
| FC-54.10a-011 | **Aligned** | Theme structural consistency | Both themes render every surface with matching structure: light artifacts average ~RGB(255,248,255) and dark ~RGB(22,14,24), with the same layout and no clipping/overlap observed at either viewport. | artifacts 02–19; mean-RGB per artifact |
| FC-54.10a-012 | **Unverified** | Colour contrast | WCAG contrast ratios were not measured; artifacts exist but no ratio computation was run. Blocker: no contrast tooling executed in this pass — do not claim AA contrast from these PNGs. | — |
| FC-54.10a-013 | **Unverified** | Motion & reduced-motion | Doc 07's 150–200ms motion and reduced-motion honouring could not be evidenced with a still-capture harness. Blocker: no frame-timing/reduced-motion probe available. | — |
| FC-54.10a-014 | **Needs restructure** | Form presentation (D1/D2) | The benchmark entry form renders as a **full pushed page** at both viewports, not the locked right-side sheet (Web, D1) or bottom sheet (Android, D2), and no scrim/modal is present — despite the route being URL-backed. Corroborates FC-54.1-005; STEP-55 owns the fix. | artifacts 07–10; `router.dart:290-299` |
| FC-54.10a-015 | **Needs restructure** | Report presentation (D6) | “Reports” resolves to a standalone `/reports/config` route showing a type picker outside the shell (no sidebar/bottom bar), not the contextual `FDialog` bound to a list's `ReportType`; opening it loses the originating feature/filter context. Corroborates FC-54.1-006. | artifacts 11–14; `router.dart:489-509` |
| FC-54.10a-016 | **ESCALATION — secrets boundary** | Android run / logging | The Android debug run's **own FINEST-level logging emitted the full 208-char Supabase anon key in cleartext** (`apikey` + `Authorization` headers) on two log lines, matching `.env` `SUPABASE_ANON_KEY` by hash. Per the substep's hard boundary, the run was **stopped**. (Anon keys are publishable by design, but the boundary is explicit and the logging is a hygiene signal.) The raw log was destroyed; a redacted copy is kept at `.scratch-tmp/54.10a/android-run.redacted.log`. | hash-equality check (value never printed); `.env` |
| FC-54.10a-017 | **ESCALATION — privacy compliance** | Login consent | The In-app Privacy Notice is **still absent** at runtime: no link, checkbox, or first-use gate on the login surface in either theme/viewport, and the AX tree exposes none — RISK-0011 / DR-0003 / Doc 17 §3 remain open and this is a **pre-release gate**. | artifacts 01/17/18/19; AX tree §3.1; `risks.yml:RISK-0011` |
| FC-54.10a-018 | **Needs polish** | Header identity | The desktop header profile is hardcoded to **“Pengguna” / “Foreman”** for every session, while the authenticated account is a Supervisor and Settings shows the real **“Alex Supervisor / Supervisor”**. Every user is shown a wrong name and role on the shared shell. | `global_app_header.dart:416,423`; Settings dump §2; vision of artifact 02 |
| FC-54.10a-019 | **Needs restructure** | Detector no-signal | The skill's mechanical detector cannot see this UI: `[]` on Dart source, and its only live hit (`wide-tracking 6.25em`) is a false positive on a hidden Flutter text-measurement `<p>`. A “no anti-patterns found” result must never be reported as design verification for this app. | §4; CanvasKit shadow-DOM canvas proof |

## 6. D7 / D1–D8 note

This substep does **not** re-decide D7. It adds runtime support to the existing D1/D2 (form is a full page, not a sheet — FC-54.10a-014) and D6 (report is a standalone route, not a contextual dialog — FC-54.10a-015) conflicts already recorded in 54.1/54.11's scope.

## 7. Verification record

| Check | Result |
|---|---|
| `roots.json` repointed at `Code/mine-flow-app`; app visible to `context` | Pass — `projectRoot/repoRoot = …\Code\mine-flow-app` from app cwd; manifest-only edit does not affect `context` (§1.1, recorded) |
| Web captures — shell + shared surfaces, both viewports, both themes, byte/dim honest | Pass — 19 artifacts; none in the placeholder class |
| Android leg genuinely captured | **Partial** — login portrait captured (1080×2400, 71,067 B); authenticated shell leg aborted on the secrets boundary (016) |
| `flt-semantics` + AX tree + focus order for login and shell; scored vs WCAG 2.1 AA | Pass — §3 |
| Detector no-signal recorded with false-positive example + CanvasKit cause | Pass — §4 |
| Every finding has ID, verdict, why, and evidence/blocker | Pass — FC-54.10a-001..019 |
| Application code / docs / ADRs / `risks.yml` modified | Pass — none; app repo `git status --short` clean; `web/index.html` not injected |
| live-server stopped · Flutter (web) stopped · emulator stopped · ports 8080/8400/8099/5554 free | Pass — child `dart`/`python` PIDs terminated after the parents were killed |

## 8. Limitations (blockers named)

- **Android authenticated shell — `Unverified`.** Blocked by FC-54.10a-016: the run was halted on the secrets boundary, so only the Android **login** surface was captured. Do not treat the narrow Web layout as Android evidence.
- **Contrast (FC-54.10a-012)** and **motion/reduced-motion (FC-54.10a-013)** remain `Unverified`.
- **Theme change only reproducible in-app.** `prefers-color-scheme` emulation is ignored by the app (FC-54.10a-010); light captures were produced via Settings → “Terang”.
- **Two Web artifacts are deterministic duplicates** (01 = 16); this is expected for the static login route.
- **Skill runtime state:** `.impeccable/live/roots.json` was rewritten (repointed; originally `resolvedFrom: fallback`) and `.impeccable/live/server.json` was created by `live-server` and removed by `live-server stop`. `live-server stop` reported `config_missing` for `.impeccable/live/config.json` (never created), so no `<script>` was ever injected into app files — `web/index.html` is untouched. No other skill state was written.

## 9. Escalations to the user

1. **FC-54.10a-016 (secrets boundary):** the Android debug run logged the full Supabase anon key in cleartext. I stopped the run and destroyed the raw log. Recommendation: treat the app's FINEST HTTP-header logging as a defect to suppress in non-debug builds (STEP-55.11 audit or a small ticket).
2. **FC-54.10a-017 (privacy):** the In-app Privacy Notice is confirmed absent at runtime. This is RISK-0011's pre-release gate — surfaced here at a live surface, not left as a table row.

## 10. Cleanup record

- `impeccable live-server stop` → stopped (port 8400); `adb -s emulator-5554 emu kill` → emulator down.
- Flutter web-server and the throwaway localhost server were stopped; orphaned child `dart`/`python` processes holding 8080/8099 were terminated by PID (the exact parent-kill failure mode the prompt warns about).
- **Ports 8080 / 8400 / 8099 / 5554: verified free.** App repo `git status --short`: **clean.** No application code, docs, ADRs, or `risks.yml` were modified.

**Next action:** update `STEP-54-PLAN.md` (54.10a → Done), then run **substep 54.11** in a **fresh chat**.
