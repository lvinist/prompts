# mine-flow — STEP-51 PLAN: UI Debt Closure — CF-087 Material remainder & STEP-46.4 regression coverage

**Phase:** Phase 3 — Release Readiness, Integration & Scale
**Owner:** Gemini 3.7 Flash High (51.4, 51.5, 51.6, 51.9) · Gemini 3.1 Pro High (51.2, 51.3, 51.7, 51.8) · Hermes/Claude Opus 4.8 (51.1, 51.10)
*(Executors only — the user remains the accountable owner per `runbooks/collaboration.md`'s "one owner per STEP" rule; models are execution tiering, not a split of ownership.)*
**Status:** Closed 2026-09-10 — all substeps Done; branch merged to `master` as `79df486`; close evidence in `mine-flow-STEP-51.10-FINDINGS.md` (this folder)
**Date:** 2026-09-05 (authored) · 2026-09-09 (kickoff decisions locked, prompts authored)
**Branch:** `step-0051-ui-debt-closure`
**Repos (projection):** `mine-flow-app`, `mine-flow-docs`, `prompts` (merge order: app → docs → prompts)

> This STEP exists because STEP-46 booked as complete two things it did not finish. It is a
> **debt-closure STEP**, not a new feature: its scope is harvested from a mechanical audit
> (`Code/mine-flow-docs/reports/2026-09-05-step-45-47-implementation-audit.md`), and its first
> substep's job is to make the register tell the truth before any code moves.

## Motivation

STEP-46 was a two-pass UI/UX audit that confirmed 97 findings and closed with "all 97 fixed". The
2026-09-05 implementation audit re-derived every claim on disk. Most held. Two did not:

**CF-087 "Residual Material widgets" is roughly half done.** The register entry names "dialogs,
alerts/snackbars, headers, selects, buttons". What actually shipped were the dialogs, buttons, tiles,
dividers and chips — real work, genuinely at zero. What did not ship (current `lib/`, files/hits):

| Family | Files | Hits | forui 0.26 equivalent, already in the pinned version |
|---|---|---|---|
| `SnackBar(` | 13 | 35 | `FToast` / `FToaster` — `widgets/toast/` |
| `Scaffold(` | 25 | 37 (`FScaffold(` 3) | `FScaffold` — `widgets/scaffold.dart` |
| `CircularProgressIndicator(` | 22 | 25 | `FCircularProgress` — `widgets/progresses/` |
| `AppBar(` | 14 | 19 (`FHeader` 9) | root/nested header — `widgets/header/` |

~116 call sites across ~30 files, with **73 of 240** `lib/` files still importing
`package:flutter/material.dart`. Nothing is blocked: every replacement exists in forui 0.26.0.
(By contrast CF-088, the icon migration, is genuinely complete: `Icons.` is 0, `LucideIcons.` is 291.)

**STEP-46.4's "add tests for each fix" is largely unfulfilled.** The register assigns an explicit test
tier to **84 of 97** findings — 80 of them "Widget test" — and only 13 say "No test feasible". The
STEP-46 merge `040def9` moved the suite from 361 to 369 cases (**+8 net**, matching the claimed
434→442) and added **zero new test files**. **13** of 97 CF ids are cited anywhere under `test/`
(34 counting `integration_test/`). The prompt's own escape hatch
`// TODO(STEP-46.4): test not written because …` is used **0** times. The fixes are real and were
spot-verified; they are simply unguarded, so the next refactor can silently undo any of them.

Two smaller items ride along because they are the same debt and the same files:

- **CF-043's structural half.** STEP-48.30 removes the dead `Tambah "…"` affordance, but the register
  also asked to "constrain method to the enumerated set" and "use one shared control, not two" —
  `land_clearing_entry_screen.dart:372` and `:485` still hold two independent comboboxes writing the
  same `record.method`.
- **Five unreferenced `lib/` files** (`tracking.dart`, `benchmark.dart`, `data_bucket.dart`,
  `data/data.dart`, `domain/domain.dart` barrels plus `notification_badge.dart`,
  `report_type_card.dart`) need a disposition. 48.30 deletes only the two *shadowing* files and
  reports these.

## Pre-flight reality check (facts established 2026-09-05; **re-verified 2026-09-09**)

- App repo on `master` at `64b054a` (STEP-48/50 merged), clean, synced with origin; prompts repo
  clean on `main`; no `step-0051` branch exists yet.
- **Counts re-verified 2026-09-09 (holding within noise of the audit):** `SnackBar(` 35 sites /
  13 files (`showSnackBar(` 35 + `SnackBar(` ctor 35 — a naive grep reads 70), `Scaffold(` 24
  files, `AppBar(` 14 files, `CircularProgressIndicator(` 22 files; **71** `lib/` files import
  `package:flutter/material.dart` (audit said 73); `Icons.` still 0 (282 are `LucideIcons.`).
- **CF-043 confirmed present:** two independent `CreatableCombobox<String>` writing
  `record.method` at `lib/features/tracking/presentation/pages/land_clearing_entry_screen.dart:373`
  and `:486`, both fed by `_clearingMethods` (defined `:98`).
- **Dead-file list NOT resolved (corrected 2026-09-09 by 51.1 — the earlier claim was false):**
  the pre-flight previously said "all 7 candidate files already deleted by 48.30." Wrong:
  48.30 deleted only the two shadowing files and *recommended* the rest for STEP-51; the
  verification had checked the audit's literal top-level paths (`lib/tracking.dart` etc.),
  which never existed — basename noise. All real files still exist. True disposition list:
  3 dead feature barrels (`features/tracking/tracking.dart`, `features/benchmark/benchmark.dart`,
  `features/data_bucket/data_bucket.dart`), their 4 barrel-twin `data/data.dart` /
  `domain/domain.dart` files, a duplicate never-registered `GeospatialFileModelAdapter`
  (`features/data_bucket/data/models/hive/geospatial_file_hive_adapter.dart`, typeId 13 vs the
  registered typeId 7 in core), two product-intent widgets (`notification_badge.dart`,
  `report_type_card.dart` — 48.30 parked the owner decision), and a new find:
  `lib/app/presentation/models/app_nav_model.dart` (unreferenced since STEP-30.1). See
  `Upcoming Prompts/mine-flow-STEP-51.1-FINDINGS.md` §5 — **51.9 is a real deletion job, not
  verify-and-record.**
- **46.4 debt re-verified:** 13 of 97 CF ids cited under `test/` (23 under `integration_test/`);
  no `TODO(STEP-46.4)` markers exist.
- Original 2026-09-05 baseline: `flutter analyze` 0 issues; `dart format` 0 changed; `flutter test`
  **513 passed** (pre-STEP-48/49/50; current suite is **553** at `b9bcce5` — the STEP-51 baseline).
- The STEP-46 findings register lives at
  `prompts/003-release-readiness-integration-scale/step-0046/mine-flow-STEP-46.3-FINDINGS.md`.
  It is an **archived** file: amend by appendix, never rewrite in place.
- forui 0.26.0 pinned; pub cache verified at `D:/AppDev/.pub-cache` (`forui-0.26.0`, `forui_lucide-0.26.0/0.26.1`).

## Hard dependency

**STEP-48 must close first.** It owns `step-0048-runtime-evidence` with ~26 uncommitted app files, and
its branch-head CI gate is the release gate. A large Material sweep landing mid-wave would make every
subsequent gate diff unreadable and would collide with 48.29/48.30's edits to the same files. Do not
cut `step-0051-ui-debt-closure` until STEP-48 is `Done` and merged to `master`.

## Decisions (locked at kickoff, 2026-09-09)

| # | Question | Decision |
|---|---|---|
| D1 | Re-scope CF-087 honestly first, or just sweep? | **Re-scope first** (user decision 2026-09-05, confirmed 2026-09-09). Substep 51.1 writes an appendix to the STEP-46.3 register recording what CF-087 actually delivered and what remains, so the record stops claiming completion. Sweeping without that leaves a second false "all fixed" behind. |
| D2 | Sweep granularity | **Per feature**, one substep per family, so each diff is reviewable and each can be reverted independently. Not one 30-file commit. |
| D3 | Test bar for the sweep | Widget test wherever **behaviour** changes — dialogs, toasts, selects, anything with a dismiss/timeout/callback. Pure container swaps (`Scaffold`→`FScaffold`) need no new test but must not break existing ones. |
| D4 | 46.4 test debt scope | Cover the **behaviour-carrying** findings, not all 84. Every uncovered finding gets an explicit one-line reason in the appendix — the discipline the original prompt's `TODO(STEP-46.4)` hatch was for and which was never used. |
| D5 | ADR needed? | Probably not: Doc 07 §3/§6 already makes ForUI the vocabulary, so this is compliance, not a decision. Write an ADR only if a family has **no** ForUI equivalent and a documented Material exception is chosen. |
| D6 | 51.9 dead-file disposition, given all files are already deleted | **Keep 51.9 as a cheap verify-and-record substep** (user decision 2026-09-09) — *premise falsified by 51.1: the files were never deleted; 51.9 is now the real deletion substep (see pre-flight correction + 51.1 findings §5).* Original intent stands: explicit dispositions, no silent deletions, sweep for new unreferenced files. |
| D7 | Model assignment | Confirmed 2026-09-09: Opus 4.8 → 51.1, 51.10; Gemini 3.1 Pro High → 51.2, 51.3, 51.7, 51.8; Gemini 3.7 Flash High → 51.4, 51.5, 51.6, 51.9 (see "Model assignment"). |

## Substep progress

| # | Status | Evidence |
|---|---|---|
| 51.1 | Done | `Upcoming Prompts/mine-flow-STEP-51.1-FINDINGS.md` — 114-site inventory, 97/97 coverage matrix, D6 premise falsified (real deletion list for 51.9); register appendix pushed `6e6a65d`; branch cut, index `In progress` pushed `4f69cf9`; baselines: analyze 0 issues, test 548+5skip. |
| 51.2 | Done | `Upcoming Prompts/mine-flow-STEP-51.2-FINDINGS.md` — 35 `SnackBar` sites across 13 files migrated to `FToast`/`FToaster`; pushed `85ad657`; baselines: test 548+5skip. |
| 51.3 | Done | `Upcoming Prompts/mine-flow-STEP-51.3-FINDINGS.md` — 19 `AppBar` sites across 14 files migrated to `FHeader` root/nested (pushed screens keep back affordance via explicit prefix; colored equipment-check band via style delta); committed `59f595f`; analyze 0, format clean, test 550+5skip/0 failed; concurrent 51.5 hunks excluded via staged-index split. |
| 51.4 | Done | `Upcoming Prompts/mine-flow-STEP-51.4-FINDINGS.md` — 35 `Scaffold` sites across 24 files migrated to `FScaffold`; Material ancestor and FAB Stack patterns implemented; `Scaffold(` hits in `lib/` at 0; committed `b706f9c`; analyze 0 issues, format clean. |
| 51.7 | Done | `Upcoming Prompts/mine-flow-STEP-51.7-FINDINGS.md` — CF-043 structural half closed: one shared `CreatableCombobox` above `TabBar` (per-tab copies removed), `_validateAndSave` enumerated-set guard added, 3 widget tests (structural + shared-value semantics + constraint); committed `281432f`; flutter analyze 0 issues (changed files), **full suite 550+5skip/0 failed** (+2 net). |
| 51.8 | Done | `Upcoming Prompts/mine-flow-STEP-51.8-FINDINGS.md` — CF-014 pinned (citation added to the existing cut-fill form test, committed `605ebe0` after stranded-deliverable resume + CRLF repair); of 57 will-cover findings: CF-043 already covered by 51.7, the other 55 escalated as mis-triaged-for-batch with recorded one-line reasons (consolidated for 51.10's register appendix). Citation count 14→15 unique CF ids under `test/`; focused test + analyze + format green; prior session's full-suite 550-green claim carried forward, re-verification left to 51.10 gate. |
| 51.5 | Done | `Upcoming Prompts/mine-flow-STEP-51.5-FINDINGS.md` — 25 `CircularProgressIndicator` sites across 22 files migrated to `FCircularProgress` (all indeterminate; sized via `.xs/.sm/.lg` variants, explicit in-button colours preserved via style delta); no test finders matched the type; committed `69c6b44`; analyze 0, format clean, full suite 550+5skip/0 failed (no delta). Ran concurrent to 51.3/51.4; shared-file hunks split cleanly (51.3's commit `59f595f` carries zero 51.5 insertions, verified). |
| 51.6 | Done | `Upcoming Prompts/mine-flow-STEP-51.6-FINDINGS.md` — residual Material imports reduced to 47 analyzer-proven justified survivors; repeatable inventory recorded; four migrated families at anchored zero; analyze clean, format clean, full suite 550+5skip |
| 51.9 | Done | `Upcoming Prompts/mine-flow-STEP-51.9-FINDINGS.md` — deleted 11 exact-path-unreferenced files (including both owner-confirmed product-intent widgets), removed 2 stale l10n exemptions; exact-reference sweep 0, only core Hive adapter typeId 7 remains; format clean, analyze 0 issues, l10n guard `[OK]` (13 scanned / 45 exempt), full suite 550 passed + 5 skipped / 0 failed. |

## Substeps (locked 2026-09-09; prompts authored — see `Upcoming Prompts/mine-flow-STEP-51.M-PROMPT.md`)

| # | Title | Model | Produces | Depends on |
|---|-------|-------|----------|------------|
| 51.1 | Register re-scope & sweep inventory (gate) | **Opus 4.8** | Appendix to the STEP-46.3 register stating CF-087's real delivered/remaining split and CF-043's residual half; a per-file inventory of the ~116 sites with its ForUI target and a behaviour-change flag; the 46.4 coverage matrix (which of 84 tiered findings are covered, which will be, which will not and why); dead-file disposition record (D6) | STEP-48 `Done` ✅ |
| 51.2 | `SnackBar` → `FToast`/`FToaster` (13 files) | **Gemini 3.1 Pro** | Toast host wired once; all 35 sites migrated; widget tests where dismissal/duration/action behaviour is asserted; `ScaffoldMessenger` uses retired with it | 51.1 |
| 51.3 | `AppBar` → ForUI header (14 files) | **Gemini 3.1 Pro** | 19 sites migrated to the header pattern the 9 existing `FHeader` uses already establish; back/action affordances preserved; existing screen tests green | 51.1 |
| 51.4 | `Scaffold` → `FScaffold` (24 files) | **Gemini 3.7 Flash** | 37 sites migrated; the 3 existing `FScaffold` uses are the reference; watch for the known "Material ancestor" class (48.22 hit it twice) and for `ScaffoldMessenger` removal ordering vs 51.2 | 51.2 |
| 51.5 | `CircularProgressIndicator` → `FCircularProgress` (22 files) | **Gemini 3.7 Flash** | 25 sites migrated; loading-state tests that match on the widget type updated | 51.1 |
| 51.6 | Material-import sweep & residue check | **Gemini 3.7 Flash** | `flutter/material.dart` imports reduced to the files that genuinely need Material primitives, each justified in a comment; a repeatable inventory command recorded so the next audit does not have to re-derive it | 51.2–51.5 |
| 51.7 | CF-043 structural half | **Gemini 3.1 Pro** | `method` constrained to `_clearingMethods`; one shared control instead of two independent comboboxes, per ADR-0015's plan/actual model; widget test asserting both tabs edit one normalised value | 51.1 |
| 51.8 | 46.4 regression coverage | **Gemini 3.1 Pro** | The tests D4 scopes, each naming its CF id in a comment so the citation count becomes meaningful; per-finding reasons for anything left uncovered | 51.1 |
| 51.9 | Dead-file disposition (verify & record) | **Gemini 3.7 Flash** | Deletions verified on disk; dispositions recorded (all 7 candidates already deleted by 48.30); sweep for any *new* unreferenced `lib/` files; no shadowing duplicates reintroduced | 51.1 |
| 51.10 | Verification & close | **Opus 4.8** | Full gates green; Doc 07 conformance re-checked; register appendix final; index row + substep table; PLAN archived to `prompts/003-release-readiness-integration-scale/step-0051/` | 51.2–51.9 |

### Model assignment rationale (per `references/model-assignment-and-substep-tiering.md`)

2 of 10 substeps at the top tier — the minimum defensible, mirroring the STEP-47/49 precedent
(`Gemini 3.7 Flash High (x) · Gemini 3.1 Pro High (y) · Hermes/Claude Opus 4.8 (z)`).

- **51.1 (Opus):** the honesty gate — it decides what the durable record says and where the sweep's
  boundary sits. Getting it wrong reproduces STEP-46's defect one level up: a wrong inventory means
  every downstream substep sweeps the wrong set or, worse, the register gets a second false
  "complete". A wrong answer here is silent and expensive.
- **51.10 (Opus):** the closing substep judges whether the debt is actually closed, writes the durable
  record, and gives the gate verdict. It must be willing to leave rows open rather than declare
  victory — a judgement call about honesty that is itself the deliverable.
- **51.2/51.3/51.7/51.8 (Pro):** behaviour-carrying migrations and test authoring. Each is bounded by
  a written authority (Doc 07, ADR-0015, the STEP-46.3 register, the coverage matrix) but needs real
  judgement about what an assertion should prove — e.g. whether a toast test asserts dismissal
  duration or only presence, or which of 84 findings carry behaviour worth pinning.
- **51.4/51.5/51.6/51.9 (Flash):** mechanical swaps with an unambiguous pass/fail signal — analyzer,
  existing tests, and a grep count that must reach zero. Engineering volume (37 `Scaffold` sites) is
  not judgement risk.

**Escalation rule (all substeps):** escalate to Opus if a failure cannot be classified as
test-defect vs application-defect, if runtime behaviour appears to contradict an accepted ADR or
Doc 07, on any data-integrity-shaped result, if tempted to mark a verdict PASS the evidence cannot
support, or if **the same fix fails twice**. Record the escalation in the substep's findings.

## Test plan

| Tier / surface | Substep(s) | Tests | Gate |
|---|---|---|---|
| Widget | 51.2, 51.3, 51.7, 51.8 | New tests where behaviour changes + the D4-scoped 46.4 coverage | `flutter test` |
| Widget (regression only) | 51.4, 51.5, 51.6, 51.9 | None authored; existing must not regress | `flutter test` |
| Static | every substep | — | `flutter analyze` 0, `dart format --set-exit-if-changed`, l10n guard, contract guard |
| E2E | 51.10 | None authored | The dual-platform CI gate must stay green — a Material→ForUI swap changes finders, and STEP-48's journeys assert on widget types and semantics labels. **Re-run the branch-head gate before close.** |

Known traps, inherited: use `tester.binding.setSurfaceSize` rather than assuming 768px (ForUI sidebar
pitfall); target `find.byType(EditableText)` not `TextField` (flutter/flutter#191095 under forui 0.26);
scope form finders to the screen, not `.at(0)` — 48.22 lost two sessions to a desktop header search
field matching first.

## Ground rules

- **Do not weaken or delete an assertion to make a test pass.** A Material→ForUI swap that breaks a
  test means the test was asserting on Material; update what it looks for, not what it proves.
- **Re-scope before sweeping.** The register is the durable record; leaving it claiming completion
  while a new STEP quietly finishes the job is the same defect this STEP was created to fix.
- **Archived findings are immutable** — append an appendix to the STEP-46.3 register, never rewrite it.
- **Keep the docs true.** If a family has no ForUI equivalent, that is a documented exception with an
  ADR, not a silent Material survivor.
- One feature group per commit. No drive-by refactors inside a sweep commit.
- Calibrate communication from root `.throughstone/local-user.md` (Level 2, Explanatory).

## Definition of done

- [ ] The STEP-46.3 register carries an appendix stating what CF-087 delivered and what remained, so
      no reader is told it was complete.
- [ ] `SnackBar(`, `AppBar(`, `Scaffold(`, `CircularProgressIndicator(` are zero in `lib/` — or each
      survivor is justified in a comment and, if it is a design decision, in an ADR.
- [ ] `flutter/material.dart` imports reduced to justified cases, with the inventory command recorded.
- [ ] CF-043 fully satisfied: enumerated method, one shared control, widget test.
- [ ] The 46.4 coverage matrix is complete: every tiered finding either covered by a CF-id-citing test
      or carrying a one-line reason it is not.
- [ ] The 5 unreferenced `lib/` files dispositioned.
- [ ] `flutter analyze` 0, formatter clean, both guards OK, `flutter test` green with the count and
      delta stated, and a **branch-head CI run with all four jobs green and non-zero executed counts**.
- [ ] `prompts/STEP-index.md`: STEP-51 `Done` with its substep table; PLAN archived to
      `prompts/003-release-readiness-integration-scale/step-0051/`; phase README row added.
- [ ] The user is told the next action and to start a fresh chat for it.
