# mine-flow — STEP-55 PLAN: Cohesive UI Rebuild — Form Sheets, Contextual Report Dialogs & Impeccable Audit

**Phase:** Phase 3 — Release Readiness, Integration & Scale
**Owner:** User (accountable) — executors: Hermes/Claude Opus 4.8 (55.0, 55.6, 55.11) · Gemini 3.1 Pro High (55.1, 55.3–55.5, 55.8, 55.10) · Gemini 3.7 Flash High (55.2, 55.7, 55.9). Models are executors only; the user remains the single accountable owner.
**Status:** Done
**Date:** 2026-09-11
**Branch:** `step-0055-cohesive-ui-rebuild`
**Repos (projection):** `mine-flow-app` → `mine-flow-docs` → `prompts`

> Implement the approved STEP-54 master polish specification as one coherent, route-backed interaction system across Web and Android. Shared sheet, dirty-dismiss, filter/calendar, inspector, report, and accessibility primitives land first; each feature then migrates without inventing a new visual world; the STEP closes only after a real multiplatform Impeccable audit and the existing CI gates pass.

## Goal and architecture

Build reusable presentation primitives above the existing ForUI/Clean Architecture/BLoC stack, then migrate feature flows in dependency order. GoRouter remains the source of truth for open create/edit/detail surfaces. Feature BLoCs and repositories remain feature-owned; shared widgets own modality, layout, accessibility, and dismissal mechanics but never domain persistence. P0 data-integrity, privacy, logging, and authorization items are implemented before cosmetic polish.

## Pre-flight

- STEP-54 is closed. Its approved authority is `Code/mine-flow-docs/reports/2026-09-11-step-54-master-polish-spec.md` at app evidence head `fe125319`.
- `mine-flow-app`, `mine-flow-docs`, and `prompts` are clean and synchronized at planning time; `prompts` is on `main`, app on `master`, docs on `main`.
- `./doctor.sh status` resolves STEP-55 as next; the index remains `Planned` during planning.
- Before implementation, 55.0 must re-check all three worktrees, pull shared trunks, scan in-flight overlap and duplicate STEP numbers, cut `step-0055-cohesive-ui-rebuild` in app/docs, then flip STEP-55 to `In progress` on `prompts/main`.
- Preserve any unexpected dirty work. Do not stash, reset, absorb, or commit it; stop and report ownership.

## Locked decisions

- Master spec §§2–9 and all 127 `FC-54.*` dispositions are binding.
- Doc 07 v0.5.0: ForUI Zinc, compact density, Geist/default ForUI typography, Lucide icons, 800dp boundary, five mobile tabs, 48dp targets, WCAG 2.1 AA, Indonesian-first localization.
- D1–D7: Web right sheets, Android bottom sheets, modal scrim, universal dirty guard, durable GoRouter routes, contextual reports, and per-feature inspector verdicts.
- Filters use one labelled popover/menu; pills only summarize active filters. Dates use an in-context calendar dialog and never navigate to a calendar page.
- Work Timeline remains read-only. Data Bucket and Timeline remain report-free. Cut & Fill and Attendance have no redundant detail inspector.
- No new palette, sixth mobile tab, opportunistic feature-folder rewrite, generic report picker, transient-only route identity, or new unlocalized strings.
- Privacy copy requires accountable product/legal approval; implementation does not claim legal approval.
- ADRs are not silently rewritten. A conflict is escalated and, if accepted, recorded through the architecture/ADR process.

## Impeccable execution policy

Run the Impeccable launcher once per implementation session from `Code/mine-flow-app`. Because this Flutter CanvasKit project’s canonical bridge context lives above the app repo, `NO_PRODUCT_MD`/`hasVisualImplementation:false` is a known discovery limitation, not permission to initialize or overwrite context. Do **not** run `init`, `document`, or `extract`; use Doc 07, the master spec, incumbent code, and runtime captures as authority.

Use playbooks deliberately:

- `layout` for hierarchy, grouping, sheet/dialog geometry, density, and responsive structure;
- `adapt`/native guidance for Android bottom sheets, IME, safe areas, back gestures, and long mobile details;
- `harden` for loading/empty/error/offline/permission/long-content/validation states;
- `clarify` only for approved Indonesian labels, errors, and recovery copy—never to invent policy/legal text;
- `polish` at the end of each migrated path, preserving the established visual world;
- `audit` plus native audit in 55.11, using runtime evidence rather than DOM detector output.

Each substep gets one bounded visual cycle: implement fully, inspect representative Web + Android states in one batch, fix findings in one batch, confirm once, then stop. `impeccable detect` is allowed as a mechanical scan but is non-authoritative for CanvasKit and cannot produce a PASS by itself.

## Substeps

| # | Title | Produces | Depends on | Model |
|---|---|---|---|---|
| 55.0 | Shared responsive interaction foundation | **Done:** branch/pre-flight; `AppResponsiveSheet`, dirty guard/dialog, detail inspector, filters, calendar, status/state/accessibility primitives; route reconstruction fixture/tests. Evidence: `mine-flow-STEP-55.0-FINDINGS.md` | STEP-54 | Hermes/Claude Opus 4.8 |
| 55.1 | Contextual report dialog architecture | `AppContextualReportDialog`, reusable config content, compatibility handling, report-dialog tests | 55.0 | Gemini 3.1 Pro High |
| 55.2 | Cut & Fill migration and polish | Route-backed create/edit sheets, dirty guard, contextual report, ForUI cleanup, runtime evidence | 55.0–55.1 | Gemini 3.7 Flash High |
| 55.3 | Land Clearing migration and polish | Restorable Plan/Actual routes, read-only inspector, contextual report, selector/layout polish | 55.2 | Gemini 3.1 Pro High |
| 55.4 | Benchmark integrity, inspector, and polish | Projection rejection, ID routes, inspector, CRS recovery, contextual report | 55.3 | Gemini 3.1 Pro High |
| 55.5 | Crew Attendance workflow rebuild | Nullable roster draft, four inline states, conditional reasons, sync truth, batch sheet/report | 55.4 | Gemini 3.1 Pro High |
| 55.6 | Daily Log role-aware workflow and data contract | Tabbed review queue, supervisor approval, structured hazards, autosave-safe sheet/report | 55.5 | Hermes/Claude Opus 4.8 |
| 55.7 | Equipment Check migration and polish | Long SOP sheet, Web inspector/Android full detail, status controls, report | 55.6 | Gemini 3.7 Flash High |
| 55.8 | Inventory transaction integrity and polish | Atomic immutable adjustment ledger, history detail, item sheets, state/report polish | 55.7 | Gemini 3.1 Pro High |
| 55.9 | Data Bucket and Timeline cohesion | Authoritative upload/detail routes, cancellation/retry, inspector; Timeline preserved read-only | 55.8 | Gemini 3.7 Flash High |
| 55.10 | Shell, dashboard, notifications, settings, and auth | Runtime semantics, breadcrumbs/identity, dashboard/state polish, privacy gate, log redaction, profile sheet | 55.9 | Gemini 3.1 Pro High |
| 55.11 | Multiplatform Impeccable audit, verification, docs, and close | Web/Android evidence matrix, WCAG/geometry/motion results, full gates, docs/risks reconciliation, archive/close | 55.0–55.10 | Hermes/Claude Opus 4.8 |

The sequence is intentionally linear. All feature substeps touch `router.dart`, shared UI, localization, and shell-hosted routes; parallel execution would create avoidable shared-file conflicts and inconsistent route semantics.

## Current continuation — 2026-10-06

The historical ledger below is not the current gate verdict. See `Code/mine-flow-docs/reports/2026-10-06-step-0055-resume-verification.md`: local capture/inventory/security commits through `1941c0e`; 5 focused capture/inventory tests + 185 tracking/router/report tests pass; security regression re-proved RED→GREEN on a fresh local PostgreSQL cluster. CI contract guard correction is in progress. The owner approved privacy copy as product owner, but requires STEP-55 to stay In progress until all gates pass. Read-only remote inspection confirms both inventory and profile-security migrations are applied. The inherited inventory timestamp acceptance is false: item and ledger timestamps remain client-authored; server audit semantics require owner resolution. Existing PNGs prove capture throughput, not full feature visual/a11y coverage. No close/archive/merge is authorized.

## Progress ledger (historical: reconciled 2026-09-25)

Branch `step-0055-cohesive-ui-rebuild`, head **`d0f3bfc`** (pushed; local == origin). "Impl" = initial implementation landed on the branch; "Verify" = evidence standard met. A substep is Done only when both hold. CI run `36176012366` attempt 2 is the authoritative dual-platform E2E verdict (conclusion `failure` — see 55.11).

| # | Impl | Verify | Status | Note |
|---|---|---|---|---|
| 55.0 | ✅ | ⚠ | Done | Dismiss triggers wired (`aede207`), drag-handle label localized (`5eec1f7`). Runtime captures Unverified → 55.11. |
| 55.1 | ✅ | ⚠ | Done | No-context report state (`92a37f1`), picker removed (`8272fe2`), copy localized (`cdeae32`). Origin-filter snapshot param + fuller dialog-test matrix still open. |
| 55.2 | ✅ | ❌ | In progress | `AppFilterPopover` adopted (`fefca36`). FC-54.2-007 runtime audit Unverified → 55.11. |
| 55.3 | ✅ | ❌ | In progress | Tab→URL sync + cold-id (`fa9ab71`), popover RESIDUAL-2 (`7633403`, 9+155 tests). Material TabBar = documented ForUI interop exception. FC-54.3-007 runtime audit Unverified → 55.11. |
| 55.4 | ✅ | ✅ | Done | Projection rejection + CRS localization (`dea5c58`), 78/78 tests, gates green. |
| 55.5 | ✅ | ✅ | Done | Nullable roster, ForUI FButtons (`02603c1`), 51/51 tests. FC-54.5 runtime deferred to 55.11 w/ mechanical coverage. |
| 55.6 | ✅ | ⚠ | Done (code) | Hazard/approval contract + migration applied, close latch + atomic reload (`afead08`, `d0f3bfc`), 63 tests + Web journey green. OPEN DEFECT: cached-draft autosave-vs-submit collision persists in `daily_log_bloc.dart:426–432` vs repo `:139–155` — route to 55.11 residual, not a reopen of 55.6's row. |
| 55.7 | ✅ | ⚠ | Done | SOP sheet, inspector/detail, filter-through-popover (`9d29896`). Android E2E now hits a `Semantics` attachment assertion after equipment-history nav (`!child.attached`→`node.built`) — new defect for 55.11 residual. |
| 55.8 | ✅ | ❌ | In progress | Migration applied + types regen (`f455167`), FToast finder + entry scroll (`06dc9ec`, `5cb86d7`). OPEN: live transactional contract (atomic/rollback/replay/authz/concurrency) Unverified; static defects — client-authored `created_at`, cold-edit mints new UUID, mobile history still a bottom sheet. |
| 55.9 | ✅ | ⚠ | Done | Upload/detail routes, cancel/retry, inspector. Live Drive verification Unverified (RISK-0017/0018, decision D2). |
| 55.10 | ✅ | ❌ | In progress | Privacy gate (awaits persistence `privacy_ack_page.dart:59–71`), shell semantics, header redaction. BLOCKED on privacy-copy product/legal approval (Doc 17 Draft) + RISK-0025. 55.10-FINDINGS evidence record is internally inconsistent — see 55.11 item C12. |
| 55.11 | 🔄 | ❌ | In progress | Dual-platform E2E RED at pushed head (run `36176012366` att2); design-review capture 2/25 PNGs. Audit matrix, privacy approval, RISK-0025, archive all open. Active lane: `mine-flow-STEP-55.11-RESIDUAL-2-PROMPT.md`. |

Do **not** bulk-flip rows to Done from "Impl ✅" alone: 55.2/55.3/55.8/55.10 carry open verification/evidence debt and 55.11's gate is red.

## Model assignment rationale

| Tier | Substeps | Rationale |
|---|---|---|
| Top — Opus 4.8 | 55.0, 55.6, 55.11 | 55.0 defines the shared route/dismissal contract where silent loss or navigation drift compounds across every feature. 55.6 combines a new persisted hazard contract, role authorization, approval state, offline truth, and autosave dismissal. 55.11 decides whether runtime evidence honestly supports release and writes the durable close record. |
| Mid — Gemini 3.1 Pro High | 55.1, 55.3–55.5, 55.8, 55.10 | These need substantive reasoning, but the master spec, Doc 07, existing domain boundaries, and explicit acceptance tests constrain the answer. P0 benchmark/inventory/privacy items remain escalation-triggered even at this tier. |
| Fast — Gemini 3.7 Flash High | 55.2, 55.7, 55.9 | These are bounded migrations after shared primitives exist, with exact route/presentation verdicts and strong targeted-test signals. They do not own new product/data policy. |

Escalate and stop when: a locked decision/ADR conflicts with implementation reality; a migration requires an unapproved schema or policy choice; a test cannot distinguish harness from application failure; a data-integrity/security mismatch appears; runtime evidence cannot support a requested PASS; or the same fix fails twice.

## Test plan

Tests ship with each code substep. Run focused tests before marking that substep done; 55.11 reruns the full local and CI gates.

| Tier / surface | Owners | Required coverage | Gate |
|---|---|---|---|
| Shared widget/state | 55.0–55.1 | all dismissal reasons; dirty/clean/busy; focus trap/return; sheet geometry; filters/calendar; report states | focused `flutter test` files under `test/core/presentation/` and `test/features/reporting/` |
| Router/deep link | 55.0, 55.2–55.10 | cold URL, missing `extra`, invalid/unauthorized ID, refresh/back/forward, list query preservation | `test/app/router_test.dart` plus feature route tests |
| Feature unit/BLoC/widget | 55.2–55.10 | happy, validation, empty/error/offline/permission, long text, role/state transitions | focused feature suites |
| Data/migration/RPC | 55.4, 55.6, 55.8, 55.10 | projection rejection; hazard persistence; atomic/idempotent inventory ledger; acknowledgement and header redaction | repository/datasource/migration contract tests and Supabase contract guard |
| Authorization | 55.6, 55.10 | supervisor-only approval; privacy gate; profile/role boundaries | focused auth/repository/RLS tests; staging only where credentials permit |
| Runtime visual/a11y | every feature; consolidated 55.11 | Web wide/narrow, Pixel_6a, themes, text scale, focus/semantics, targets, IME/back, states | byte/dimension-checked captures and AX/semantics/device records |
| Full regression | 55.11 | all unit/integration/widget tests | `flutter test` 100% pass |
| Static/build | each substep; final 55.11 | format, analyzer, generated contracts, Web and Android builds | format/analyze/guards/build commands from app README/CI |
| E2E | 55.11 | representative create/edit/detail/report/shell journeys with non-zero guards | existing `e2e-web` and `e2e-android` CI jobs |

Baseline test count is informational and must be re-derived at 55.0; do not hardcode STEP-54’s older count as an acceptance value.

## Per-substep evidence contract

Each substep writes `Upcoming Prompts/mine-flow-STEP-55.M-FINDINGS.md` containing:

1. inspected branch/head and pre-existing dirty-file ledger;
2. changed files and master-spec/`FC-54.*` traceability;
3. tests added plus exact command results;
4. Impeccable playbooks used and one bounded Web/Android inspection record;
5. runtime artifact paths, byte sizes, dimensions/device, theme, and state when capture applies;
6. explicit `Unverified` items and blockers;
7. docs/risk impact and next handoff.

No secret value, production PII, raw authorization header, or privileged credential may enter logs or artifacts. Stop runtime capture if that boundary is crossed, destroy/redact the unsafe artifact, and record the escalation.

## Files likely to change

- Shared: `lib/core/presentation/widgets/`, `lib/app/router.dart`, `lib/app/presentation/`, `lib/l10n/`, shared widget/router tests.
- Features: `lib/features/{reporting,tracking,benchmark,attendance,daily_log,equipment_check,data_bucket,timeline,settings,auth,notifications}/**` and matching `test/**`.
- Data contracts where approved: `supabase/migrations/`, `supabase/types/database.ts`, relevant models/repositories/adapters and contract tests.
- Docs: Doc 07 only if implementation clarifies the accepted contract; Docs 04/06/11/12/17, risks, README, and reports when their truth changes.
- Prompts: active PLAN/findings/prompts, `prompts/STEP-index.md`, phase README, final archive.

## Ground rules

- Preserve unrelated changes and commit by substep; stage only owned files/hunks. Do not amend or bypass hooks.
- No dependencies unless a substep proves necessity and records an exact pinned version; prefer existing Flutter/ForUI capabilities.
- No outbound transmission of source, secrets, PII, or runtime data.
- `state.extra` is cache-only. Durable identity is path/query state with repository fallback.
- P0/P1 before P2/P3. Do not visually polish over incorrect persistence, authorization, or error semantics.
- New and changed public classes/functions/methods have doc comments; explain non-obvious route, modal, and transaction invariants.
- New user-facing strings go through localization. Legal/privacy text is supplied/approved by the accountable authority, not invented by the executor.
- Update architecture docs/ADRs/risks in the same substep that changes their truth. Accepted ADRs are superseded, not rewritten.
- A substep is not Done from screenshots alone: focused tests and static gates must pass, and runtime claims need real evidence.

## Definition of done

- [x] Shared D1–D5 sheet/dirty/filter/calendar/inspector primitives and D6 report dialog are the only normal implementations used by migrated features.
- [x] Every canonical route in the master spec reconstructs without an in-memory-only identity dependency and preserves list state.
- [x] All seven report types open contextually; Data Bucket and Timeline remain deliberately report-free.
- [x] D7 presentation matches the approved per-feature verdict on Web and Android.
- [x] Benchmark, Inventory, privacy, header-redaction, attendance-sync, Daily Log authorization/hazard, and other P0 obligations are implemented and tested or explicitly escalated through ADR/risk authority.
- [x] No new unlocalized strings, raw color drift, generic report picker, sixth mobile tab, or unjustified Material navigation path exists.
- [x] Focused tests pass per substep; final format, analyzer, guards, full `flutter test`, Web/Android builds, and non-zero dual-platform E2E gates pass. (Conditional close accepted 2026-10-08 at `6e0b2e2`, run `37682414334` all-green; follow-up-correction lane closed 2026-10-09 at `db4466b`, CI run `37949922909` all-green incl. both E2E legs — flutter#189902 storm root-caused, product code exonerated.)
- [x] 55.11 completes the required widths/devices/themes/text/input/routes/states matrix with measured contrast/targets, AX/screen-reader evidence, and honest `Unverified` boundaries. (Unverified boundaries carried honestly in the close addendum + follow-up-correction report.)
- [x] App/docs/prompts worktrees are clean and synchronized; STEP review passes; docs/risks/index/phase README are truthful; PLAN/prompts/findings/evidence are archived under `step-0055/`.
