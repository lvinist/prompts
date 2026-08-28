# mine-flow — STEP-45 PLAN: Release-Candidate E2E & Runtime Design Review

**Phase:** Phase 3 — Release Readiness, Integration & Scale
**Owner:** Antigravity (execution); record corrected 2026-08-28 by Hermes (Claude Opus 4.8)
**Status:** Done — runtime evidence deferred to STEP-48        <!-- Planned → In progress → Done. The executor flips to In progress right after cutting the branch. -->
**Closure note (2026-08-28):** the harness, CI gate and all 15 journey tests were authored and
committed (`flutter analyze` 0 issues, `dart format` clean). The **runtime evidence this STEP
existed to produce was not obtained**: 14 of 15 journeys were never executed (no staging
credentials), every runtime design-review item is Unverified, and only NR-001 of the six
STEP-46 Needs-Runtime findings was resolved. NR-002..006 are carried forward as RISK-0015..0019;
RISK-0006 and RISK-0011 remain open. See the corrected substep table in `prompts/STEP-index.md`
and the Definition of done below. **STEP-48 owns the real verification; Phase 4 stays closed
until it passes.**
**Date:** 2026-08-27
**Branch:** `step-0045-rc-e2e-design-review`   <!-- same name in every repo this STEP touches -->
**Repos (projection):** `mine-flow-app` (primary; harness, journeys, CI), then `mine-flow-docs` (test-strategy/observability doc bumps + ADR + risk updates), then `prompts` (index flip + archive). Merge order: app → docs → prompts.

> STEP-45 builds the project's first real device/browser end-to-end (E2E) test harness with the
> `integration_test` package and exercises **every Tier-1 and Tier-2 feature** as an automated
> critical-journey test, including the field-critical full offline/sync journey. The same suite
> runs on **both Chrome (web) and the `Pixel_6a` Android emulator as CI gates**. Alongside the
> automated suite it captures the runtime Impeccable design-review evidence (responsive,
> accessible, localized UI) that could not be settled statically, and it resolves or explicitly
> carries forward the six "Needs-Runtime" findings inherited from STEP-46 plus the two runtime
> items deferred here by STEP-43 (`go_router` v17 deep-link) and STEP-44 (live RLS behavior).
> It is the last release-readiness gate before a production release is considered.

## Motivation

Every STEP through STEP-44 has verified behavior with **mocked boundaries** — unit and
`test/integration/` (BLoC ↔ mocked repository) tests. Nothing in the project has ever driven the
real UI against a real (staging) Supabase backend, on a real Android runtime or a real browser.
Three release-blocking classes of question remain open and are only answerable at runtime:

1. **Do the critical user journeys actually work end-to-end** against staging — not just against
   mocks — on the two shipping surfaces (Android APK for field foremen, Flutter Web for office
   supervisors)?
2. **Does the field-critical offline/sync path hold** under a real airplane-mode → queue →
   reconnect → conflict-resolution cycle against live staging data? This is the single most
   important behavior for the product (offline-first field data entry) and has never been
   exercised outside mocked unit tests.
3. **Do the runtime-only design and behavior questions resolve favorably** — the six STEP-46
   "Needs-Runtime" findings (NR-001…006), the STEP-43 `go_router` v16→v17 deep-link validation
   (RISK-0006/0009), and the STEP-44 live RLS/authorization behavior test (S0 baseline deferral)?

STEP-45 is the release-candidate gate: after it, either the app is E2E-verified on both surfaces
with runtime design evidence on file, or the remaining gaps are explicitly carried forward as
named risks before anyone considers cutting a production release.

## Decisions already locked

- **Pre-locked planning answers** (`Upcoming Prompts/mine-flow-STEP-45-DECISIONS.md`, user, 2026-08-26) — carried in, not re-asked:
  - Real automated E2E via the `integration_test` package (matches `architecture/12-test-strategy.md` §1/§5, which already names `integration_test` as the e2e tier and a Staging Supabase target).
  - Full runtime access is expected: staging Supabase credentials + `Pixel_6a` Android emulator + Chrome. Impeccable design-review items are therefore planned as **verifiable**, not Unverified — but any item that genuinely cannot be run (e.g. staging credentials never supplied) must be reported as **Unverified**, never as success.
  - Full offline journey depth: airplane-mode entry, queue persistence, reconnect, conflict resolution against real staging data.
- **STEP-45 scope confirmation** (user, this planning session, 2026-08-27):
  - **Coverage:** cover **all** Tier-1 and Tier-2 features as automated E2E journeys (auth, attendance, daily logging, cut/fill, land clearing, inventory, equipment checks, benchmark, data bucket, reporting, timeline, notifications) plus the offline/sync journey — the largest accepted scope.
  - **Platform:** run the **full `integration_test` suite on both Chrome and the `Pixel_6a` emulator as CI gates** (heavier CI setup accepted).
  - **Granularity:** split the STEP into **small, per-area substeps** (15 substeps below) rather than a few large ones.
- **`architecture/12-test-strategy.md`** — §1 (test pyramid), §5 (E2E lives in-app via `integration_test`, runs against a Staging Supabase project), §6 (CI gates). **This STEP materially expands the E2E tier and adds a dual-platform E2E CI gate; the doc's "few E2E tests" guidance and §6 CI-gate list must be updated (Version Log bump) and the expansion recorded in an ADR** — see substep 45.15 and "Keeping the docs true".
- **`architecture/10-observability.md`** and **`architecture/09-environments.md`** — the staging target, `--dart-define` config path, and where E2E evidence/logs are recorded.
- **`registries/risks.yml`** — review before touching each area:
  - **RISK-0006** (`go_router` v15→v17; full E2E deep-link validation *deferred to STEP-45*) → substep 45.13.
  - **RISK-0009** (Flutter 3.47 semantics regression #191095; forui pinned ≥0.26) → informs how integration-test finders target `EditableText`, and any semantics assertions in the design-review substep.
  - **RISK-0011** (in-app privacy notice absent — pre-release gate) → confirm at runtime whether first-login shows/should show it; note in findings, do not silently close.
  - **RISK-0014** (reporting datasource still on legacy cut/fill columns; net = cut − fill) → the reporting E2E (45.9) must not assert corrected semantics that RISK-0014 says are not yet implemented; verify the *current* documented behavior and flag drift.
- **STEP-46 confirmed finding register** (`prompts/003-release-readiness-integration-scale/step-0046/mine-flow-STEP-46.3-FINDINGS.md`) — the six **Needs-Runtime** items are the explicit runtime checklist for this STEP:
  - **NR-001** (S23 ReportConfigPage — PDF over a real dataset; cancel/progress; mid-run config change) → 45.9.
  - **NR-002** (S01 LoginPage — light-mode rendering on device) → 45.14.
  - **NR-003** (S03 GroupLandingPage — sidebar active-state on group routes on web) → 45.14.
  - **NR-004** (S21 UploadFilePage — real Drive upload + abandon/cancel behavior) → 45.8.
  - **NR-005** (S21 UploadFilePage — large-file OOM threshold on a mid-range device) → 45.8.
  - **NR-006** (S18 BenchmarkForm — deep-link / route-registration behavior on web; CF-097) → 45.7.
- **STEP-44 S0 security baseline** (`reports/security/2026-08-26-step-0044-s0-security-baseline-report.md`) — "Live RLS behavior test" explicitly deferred to the STEP-45 owner / STEP-45 E2E pass → substep 45.12.

## Disk facts confirmed at planning time (2026-08-27)

- `Code/mine-flow-app` has **no** `integration_test/` directory and **no** `integration_test` dev dependency (`pubspec.yaml` confirmed). The existing `test/integration/` tier is BLoC/repository integration with mocked boundaries — **not** device E2E. This STEP creates the harness from scratch.
- `flutter devices` reports Windows, Chrome, Edge; `flutter emulators` reports `Pixel_6a`; `adb devices` is empty (emulator not booted).
- Flutter 3.47.1 local, **3.47.0 pinned in CI** (`.github/workflows/ci.yml`).
- Staging web served from GitHub Pages at base href `/mine-flow-app/staging/` (`gh-pages-staging` branch). Staging APK is the `staging-apk-<sha>` CI artifact. CI already injects `STAGING_*` secrets into the `test` and `build-android` jobs.
- `lib/l10n/` ships `app_en.arb` + `app_id.arb`; `tool/check_l10n_baseline.dart` and `tool/check_supabase_contracts.dart` are existing CI gates that must keep passing.
- No local `.env` — only `.env.example`. **Staging credentials must be supplied to the executor before the staging-backed substeps (45.3+ against real backend, 45.8 Drive, 45.12 RLS) can produce non-Unverified evidence.**

## Substeps

> Split into small per-area substeps per the locked granularity decision. 45.1–45.2 build the
> harness and CI gate; 45.3–45.11 are the E2E journeys (one area cluster each) covering every
> Tier-1/Tier-2 feature + the offline journey; 45.12–45.14 are the runtime-only verifications and
> design review; 45.15 reconciles findings, updates docs/risks, and closes the STEP.

| #     | Title | Produces | Depends on | Open questions |
|-------|-------|----------|------------|----------------|
| 45.1  | Reservation, branch & `integration_test` harness scaffold | `step-0045-*` branches in all 3 repos; index row flipped In progress; `integration_test/` dir; `integration_test` + `flutter_driver`/test runner dev deps in `pubspec.yaml`; a shared `integration_test/helpers/` (app bootstrap, staging config via `--dart-define`, login helper, offline toggle helper); one passing smoke journey (`app_boots_test.dart`) run locally on Chrome | — | Q1 (staging creds availability) |
| 45.2  | Dual-platform E2E CI gate (Chrome + `Pixel_6a`) | New `e2e-web` and `e2e-android` CI jobs (or a matrix) running the full `integration_test` suite on Chrome and on a booted `Pixel_6a` emulator, wired with `STAGING_*` secrets; jobs required before `deploy-staging`; documented emulator-boot + `flutter test integration_test` invocation | 45.1 | Q2 (emulator in CI runner cost/time) |
| 45.3  | Auth & session E2E journey | `integration_test/journeys/auth_journey_test.dart` — real login against staging, session restore on relaunch, logout clears session; asserts no hardcoded-credential prefill path succeeds silently | 45.1 | — |
| 45.4  | Attendance & Daily Logging E2E journeys | `attendance_journey_test.dart`, `daily_log_journey_test.dart` — create/edit an attendance record and a daily log against staging; correct author/attribution persisted (guards against CF-006/007/009) | 45.3 | — |
| 45.5  | Cut/Fill & Land Clearing E2E journeys | `cut_fill_journey_test.dart`, `land_clearing_journey_test.dart` — create/edit/list entries; assert **current documented** volume/area semantics only (respect RISK-0014; do not assert un-shipped corrections) | 45.3 | Q3 (which semantics are canonical for assertions) |
| 45.6  | Inventory & Equipment Checks E2E journeys | `inventory_journey_test.dart`, `equipment_check_journey_test.dart` — item entry + stock adjust; SOP checklist submit with a genuine non-default state (guards CF-017 all-PASS default) | 45.3 | — |
| 45.7  | Benchmark E2E + route-registration/deep-link (NR-006, CF-097) | `benchmark_journey_test.dart` — create a benchmark with CRS/coords persisted; on **web**, open `/operations/benchmark-db/form` directly and via the in-app button; register the `form` GoRoute under `benchmark-db` if the runtime confirms the CF-097 fix is needed; assert the form stays in the shell and is deep-linkable | 45.3 | NR-006 outcome may add a router code change |
| 45.8  | Data Bucket E2E + real Drive upload + large-file behavior (NR-004, NR-005) | `data_bucket_journey_test.dart` — with Drive wired, upload a real file on Android and web; test back/close mid-upload (abandon) and confirm record/Drive state; find the practical large-file ceiling on `Pixel_6a` and set the size guard accordingly | 45.3 | Q4 (Drive service-account creds for staging); NR-004/005 may add cancel affordance + guard tuning |
| 45.9  | Reporting / PDF E2E over a real dataset (NR-001) | `reporting_journey_test.dart` — generate each report type over the largest available staging dataset; measure duration; attempt navigate-away and mid-run config change; decide + implement whether a cancel/progress affordance is warranted; confirm CF-030/CF-073 fixes hold at runtime | 45.3 | NR-001 outcome may add progress/cancel UI |
| 45.10 | Timeline & Notifications E2E journeys | `timeline_journey_test.dart`, `notifications_journey_test.dart` — timeline renders staging data across the date range; notification list + banner render and dismiss; rule-engine-triggered notification appears end-to-end | 45.3 | — |
| 45.11 | **Field-critical offline/sync full journey** | `offline_sync_journey_test.dart` — enter data in airplane mode (connectivity forced offline), confirm queue persistence across an app relaunch, reconnect, confirm sync drains the queue, and force + resolve a conflict against real staging data; asserts `SyncQueueManager` retry/backoff behavior at runtime | 45.4–45.6 (needs entry journeys) | Q5 (how to force conflict deterministically on staging) |
| 45.12 | Live RLS / authorization E2E against staging (STEP-44 deferral) | `rls_authorization_journey_test.dart` — sign in as each role and assert reads/writes/deletes are allowed/denied per the RLS matrix in the S0 report; documents live behavior vs the static review; updates the S0 report's deferred row | 45.3 | Q6 (test-user accounts per role on staging) |
| 45.13 | `go_router` v16→v17 deep-link validation (RISK-0006/0009) | `deep_link_journey_test.dart` (web) — direct-load and reload every top-level and `:id` route; confirm shell persistence, redirects, and no observer regressions; updates RISK-0006 status | 45.7 (shares route work) | — |
| 45.14 | Runtime Impeccable design review (responsive / a11y / localized) | `reports/2026-…-step-0045-runtime-design-review.md` + captured screenshots across mobile/tablet/desktop breakpoints, light/dark themes, and `id`/`en` locales; resolves **NR-002** (login light-mode) and **NR-003** (sidebar active-state on group routes); records a11y (semantics/focus/contrast) runtime checks; confirms RISK-0011 privacy-notice status at runtime | 45.3 | RISK-0011 runtime status |
| 45.15 | Findings reconciliation, docs, risks & STEP close | NR-001…006 each resolved-or-carried-forward with evidence; new runtime findings registered; `architecture/12-test-strategy.md` bumped (expanded E2E tier + dual-platform gate) + **ADR** for the scope expansion; `architecture/10-observability.md`/`09-environments.md` touched if E2E evidence location changed; `registries/risks.yml` updated (RISK-0006/0009/0011/0014 statuses); full verification gate; branches merged app→docs→prompts; STEP archived; index flipped Done | 45.2–45.14 | — |

## Model assignments (per substep)

> Available models: **Gemini 3.1 Pro**, **Gemini 3.7 Flash High**, **Opus 4.8**.
> **Opus 4.8 is reserved** — no substep mandates it. Only 45.11 flags it as an *escalation* if the
> offline conflict-resolution logic can't be gotten right on Pro. Rationale: 45.3 establishes the
> harness+login+journey template, after which the pure pattern-following CRUD journeys (45.4, 45.6,
> 45.10) are cheap Flash-High work; everything involving infra/CI setup, semantic/RISK-sensitive
> assertions, code changes with product decisions, security, routing, visual judgment, or the
> high-stakes multi-repo close stays on Pro.

| Substep | Model | Why |
|---------|-------|-----|
| 45.1 Harness scaffold | **Gemini 3.1 Pro** | Infra bootstrap (app-boot mirroring, helpers, dep wiring) sets the foundation everything else reuses — get it right once. |
| 45.2 Dual-platform CI gate | **Gemini 3.1 Pro** | CI workflow + emulator-in-CI decision (Q2); YAML/job-graph correctness with real trade-offs. |
| 45.3 Auth & session journey | **Gemini 3.1 Pro** | First journey — defines the reusable pattern and `loginAsStagingUser`; also security-adjacent. |
| 45.4 Attendance & daily log | **Gemini 3.7 Flash High** | Straightforward CRUD journeys following the 45.3 template; well-specified. |
| 45.5 Cut/Fill & land clearing | **Gemini 3.1 Pro** | RISK-0014 semantic subtlety — must assert *current documented* semantics, not un-shipped corrections. |
| 45.6 Inventory & equipment | **Gemini 3.7 Flash High** | Pattern journeys; guards are concrete (CF-017/019/054). |
| 45.7 Benchmark + deep-link | **Gemini 3.1 Pro** | May add a `router.dart` route change (NR-006/CF-097); needs judgment + user check-in. |
| 45.8 Data bucket + Drive | **Gemini 3.1 Pro** | Real Drive auth, abandon/cancel behavior, large-file guard tuning — code + product decisions. |
| 45.9 Reporting / PDF | **Gemini 3.1 Pro** | NR-001 progress/cancel decision + RISK-0014 sensitivity. |
| 45.10 Timeline & notifications | **Gemini 3.7 Flash High** | Read-mostly journeys; simplest of the feature set. |
| 45.11 Offline / sync full journey | **Gemini 3.1 Pro** (escalate to **Opus 4.8** only if needed) | Field-critical and the most subtle: deterministic conflict forcing, cross-platform airplane-mode, retry/backoff. Try Pro first; escalate to Opus **only** if the conflict-resolution logic can't be gotten right. |
| 45.12 Live RLS / authorization | **Gemini 3.1 Pro** | Security-sensitive per-role authorization matrix; closes the STEP-44 deferral. |
| 45.13 go_router deep-link | **Gemini 3.1 Pro** | Routing/redirect/shell-persistence reasoning across every route; touches RISK-0006. |
| 45.14 Runtime design review | **Gemini 3.1 Pro** | Visual/a11y/localization judgment and evidence curation; resolves NR-002/003. |
| 45.15 Reconcile, docs, risks & close | **Gemini 3.1 Pro** | High-stakes: findings reconciliation, doc/ADR/risk updates, multi-repo merge, archive. |

**Summary:** Flash High → 45.4, 45.6, 45.10 (3 substeps). Pro → the other 12. Opus → held in reserve
(45.11 escalation only). If staging credentials are unavailable and journeys reduce to Unverified
bookkeeping, those substeps can drop to Flash High regardless of the table above.

## Test plan

> This STEP **is** a testing STEP: its primary deliverable is the `integration_test` E2E tier
> itself. Per-substep, each journey test is written and must pass locally (on Chrome, and on the
> `Pixel_6a` emulator where the journey is platform-relevant) before the substep is marked done.
> The dedicated final gate (45.15) re-runs the full suite on **both** platforms plus the existing
> unit/integration suites and static gates.

| Test tier / surface | Substep(s) | Tests to create or update | Run timing | Command / gate | Notes |
|---------------------|------------|---------------------------|------------|----------------|-------|
| E2E / user flow (web) | 45.3–45.14 | `integration_test/journeys/*_test.dart` | Per substep, then final | `flutter test integration_test -d chrome` (staging `--dart-define`s) | New tier; runs against Staging Supabase per Doc 12 §5 |
| E2E / user flow (Android) | 45.3–45.14 | same suite | Per substep (platform-relevant) + final | `flutter test integration_test -d <Pixel_6a id>` | Emulator booted first; NR-005 large-file measured here |
| Offline / sync | 45.11 | `offline_sync_journey_test.dart` | Per substep + final | both platforms | Field-critical; forces connectivity offline via helper |
| Security / authorization | 45.12 | `rls_authorization_journey_test.dart` | Per substep + final | staging, per-role sign-in | Closes STEP-44 deferred live-RLS item |
| Contract / localization (existing) | 45.1, 45.15 | keep `tool/check_supabase_contracts.dart`, `tool/check_l10n_baseline.dart` green | Every push (existing gates) | existing CI jobs | Must not regress |
| Unit + widget + `test/integration/` (existing) | 45.15 | no new; must stay green | Final gate | `flutter test` | Regression floor: current 442 passing (one known order-dependent flake, non-reproducible in isolation) |
| Static / format / analyze (existing) | every substep + 45.15 | — | Per substep + final | `dart format --set-exit-if-changed lib/ test/`, `flutter analyze` (0 issues) | House gate |
| Build smoke (existing) | 45.15 | — | Final | `flutter build apk --debug`, `flutter build web --release` | Windows Kotlin workaround in `android/gradle.properties` stays |

## Open questions

- **Q1 (owner: user/executor):** Are the staging Supabase URL + anon key available to the executor's environment (and CI secrets already set)? Staging-backed journeys report **Unverified** without them — they are not skipped silently.
- **Q2 (owner: executor):** Booting an Android emulator in GitHub Actions is heavy (KVM/`reactivecircus/android-emulator-runner`). Confirm the runner supports it or the `e2e-android` gate runs on a self-hosted/nightly runner instead of every push. Decide in 45.2; record the decision. -> **Decision:** Run on every push (slower PR feedback, but higher safety).
- **Q3 (owner: user):** For cut/fill and land-clearing assertions, which semantics are canonical *right now* given RISK-0014 (legacy columns, net = cut − fill)? Assert the current shipped behavior; do not assert the un-implemented correction.
- **Q4 (owner: user/executor):** Are staging Google Drive **service-account** credentials (`STAGING_GOOGLE_DRIVE_SERVICE_ACCOUNT_EMAIL`/`_FOLDER_ID`) available for a real upload in 45.8? If not, NR-004/005 are reported Unverified with the reason.
- **Q5 (owner: executor):** How is a sync conflict forced deterministically on staging in 45.11 (e.g. two clients editing the same row, or a seeded server-side change during offline)? Decide and document the method.
- **Q6 (owner: user):** Are per-role staging test accounts (foreman / supervisor / etc.) available for the RLS matrix in 45.12? Needed for real authorization evidence.

## Ground rules

- **Calibrate communication from root `.throughstone/local-user.md`** (Level 2, Explanatory). Substep prompts explain the *why* of E2E/CI mechanics and offer options with brief pros/cons where a runtime decision is needed. Don't copy the profile values into prompts.
- **Plan/execute interactively.** Where a runtime finding forces a code change (NR-004/005/006, NR-001), surface the options to the user before implementing rather than picking silently — the STEP-46 register flagged these as product/behavior decisions.
- **Honest evidence over claimed success.** Any journey that cannot run for lack of credentials/runtime access is reported **Unverified** with the blocking reason — never as a pass. Screenshot/log evidence backs every runtime claim in 45.14 and the findings reconciliation.
- **Tests ship with the code.** Every runtime fix (route registration, size guard, cancel affordance) lands with the journey/widget test that proves it. Per-substep run timing, with a full dual-platform re-run in 45.15.
- **Code is documented as it's written.** Every new helper/test file and any changed production code carries docstrings; comment the *why* of non-obvious offline/sync or emulator-timing logic.
- **Never touch `.env` / secrets.** Staging values are injected via `--dart-define` and CI secrets only; reference by key name. Commit only `.env.example` changes if new keys are needed.
- **Accepted risks stay visible.** Any runtime gap that can't close in this STEP (e.g. Drive creds unavailable, emulator gate deferred to nightly) is added/updated in `registries/risks.yml` with severity, owner, and revisit trigger, referencing this STEP's report.
- **Respect the shared trunk.** Edit only STEP-45's own rows in `prompts/STEP-index.md`; never re-sort. Reservation is already in place (row exists as Planned); the executor flips it to In progress right after cutting the branch and pushes the flip.

## Definition of done

> **Completion audit (2026-08-28, Hermes/Claude Opus 4.8).** Checked against disk, not the
> execution narrative. `[x]` = genuinely met. `[~]` = partially met, gap named. `[ ]` = not met
> and carried to **STEP-48**.

- [x] `integration_test` harness exists in `mine-flow-app` with shared helpers (app bootstrap, staging config, login, offline toggle) and a passing smoke journey. — *`app_boots_test.dart` itself skips without credentials, but the harness/helpers are real and committed.*
- [~] Automated E2E journeys exist and pass for **every** Tier-1/Tier-2 feature: auth, attendance, daily logging, cut/fill, land clearing, inventory, equipment checks, benchmark, data bucket, reporting, timeline, notifications. — *All 15 journeys **exist** (analyze 0 / format clean); **none passed against staging** — 14 are gated behind `markTestSkipped('Unverified: Staging credentials absent')`. → STEP-48.*
- [~] The **field-critical offline/sync full journey** (airplane-mode → queue persistence across relaunch → reconnect → conflict resolution) passes against staging, or is reported Unverified with the specific blocking reason. — *Reported Unverified **with reasons** (creds absent; local Android build broken → STEP-47; web integration tests unsupported locally). Part B of the test verifies the SyncQueueManager contract unconditionally on-device.*
- [~] The full `integration_test` suite runs on **both Chrome and the `Pixel_6a` emulator as CI gates**, required before `deploy-staging` (Q2 decision recorded if the Android gate is moved to nightly/self-hosted). — *`e2e-web` + `e2e-android` jobs are wired and gate `deploy-staging`; Q2 decided (every push). **Never observed green** — no CI run has executed them. → STEP-48.*
- [ ] Live RLS/authorization E2E (45.12) run per role against staging; the STEP-44 S0 deferred row is updated with the live result (or Unverified + reason). — *S0 row updated to **Unverified**; no per-role staging accounts exist. → STEP-48 (partial: single test user only).*
- [ ] `go_router` v16→v17 deep-link validation (45.13) complete; RISK-0006 status updated. — *Test authored; RISK-0006 still `open` (E2E unverified). → STEP-48.*
- [ ] Runtime Impeccable design-review report captured with evidence across breakpoints, themes, and `id`/`en` locales; **NR-002** and **NR-003** resolved; RISK-0011 privacy-notice runtime status recorded. — *Report exists but **every item is Unverified**; no screenshots captured; NR-002/003 carried forward (RISK-0015/0016); RISK-0011 still an open pre-release gate. → STEP-48.*
- [~] All six STEP-46 Needs-Runtime findings (**NR-001…006**) are each resolved (with the code fix + test) or explicitly carried forward as a named risk with a revisit trigger — none left silent. — *Met in the bookkeeping sense: **NR-001 resolved**; NR-002..006 carried forward as RISK-0015..0019 with triggers. None silent, but 5 of 6 remain unresolved. → STEP-48.*
- [x] The STEP test plan is complete: each code-changing substep added/updated its relevant tests or recorded why not applicable.
- [~] All tests named in the STEP test plan pass at the end (full E2E on both platforms + existing unit/integration suites + static/format/analyze + build smoke), or blockers are recorded as Unverified with reasons. — *`flutter analyze` 0 issues and `dart format` clean verified 2026-08-28; unit/integration suite re-run at close. **E2E on both platforms: not run.** **Build smoke: local `flutter build apk --debug` FAILS** (AGP 9 + `package_info_plus` `compileSdk` null) → STEP-47.*
- [x] `architecture/12-test-strategy.md` Version Log bumped for the expanded E2E tier + dual-platform CI gate, with an **ADR** recording the scope expansion; `architecture/10-observability.md`/`09-environments.md` updated if E2E evidence location changed; `registries/risks.yml` updated (RISK-0006/0009/0011/0014). — *Doc 12 v1.1, Doc 09 v0.3.0, ADR-0017, RISK-0015..0019 added.*
- [x] STEP review passed; `prompts/STEP-index.md` updated (STEP-45 → Done, substep table filled); STEP archived to `prompts/003-release-readiness-integration-scale/step-0045/`. — *Substep table **corrected** 2026-08-28 to show Unverified rows rather than blanket `Done`.*

**Unmet items are the scope of STEP-48** (runtime evidence), which depends on **STEP-47**
(Android build chain). Phase 4 planning stays closed until STEP-48 passes.

