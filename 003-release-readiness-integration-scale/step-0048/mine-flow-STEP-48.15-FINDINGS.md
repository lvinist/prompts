# STEP-48.15 Findings: Docs-True Sweep, Index Correction & STEP Close

**Date:** 2026-08-31
**Branch:** `step-0048-runtime-evidence`
**Status:** **Done** (re-run 2026-09-08)

## Current re-run — 2026-09-08: **DONE / GO close**

The blocking condition recorded below has been discharged by the later remediation wave. Branch-head CI run [34225431645](https://github.com/lvinist/mine-flow-app/actions/runs/34225431645) completed successfully on app commit `d53fb7e21f2299eb6b65a3aa4e72dc48d851a1eb` and was independently fetched from GitHub. The four required jobs all succeeded:

| Job | Result and executed evidence |
|---|---|
| `test` | success — 548 passed, 5 skipped, 0 failed (553 total; skips are guard fixtures) |
| `build-android` | success — debug APK built |
| `e2e-android` | success — 24 passed, 2 named skips, 0 failures; 17/17 APK installs; guard `[OK] Android execution proven: 24 executed.` |
| `e2e-web` | success — 16/16 loop files returned `result:true`; 22 execution markers; 3 named skips; guard `[OK] Web execution proven: 22 executed.` |

The run satisfies the PLAN's branch-head gate. The complete run record and per-file evidence are in `mine-flow-STEP-48.26-FINDINGS.md` §0, with raw job logs retained at the workspace root as `step4826_r7_test_job.log`, `step4826_r7_build_job.log`, `step4826_r7_android_job.log`, and `step4826_r7_web_job.log`.

### Close judgement

- STEP-48 is **Done** for the runtime evidence it delivered: the exercised journeys ran against staging, the Android and web guards proved non-zero execution, and the four-job branch-head gate is green.
- The close does **not** claim that every possible path is delivered. Drive upload/abandon/cancel/large-file behavior remains Deferred by D2 (`RISK-0017`/`RISK-0018`); the crew RLS and cross-role isolation leg remains unverified because `TEST_CREW_*` secrets are absent (`RISK-0021`); true browser cold-start/reload deep-link behavior remains unverified (`RISK-0019`); screen-reader behavior remains unverified (`RISK-0023`); and the design-review screenshot artifacts are not valid evidence (the capture harness ran, but the committed PNGs are placeholders and the latest Android capture uploaded no screenshots).
- The local full gate passed on the exact app tree after an initial known Hive `setUpAll` failure: `flutter analyze` 0 issues, isolated `test/integration/attendance_daily_log_sync_test.dart` 3/3 passed, and the rerun of the full suite passed **553/553**. The initial full-suite result is recorded as a known intermittent flake, not silently counted as green.
- **Close reconciliation (2026-09-08, this session):** two phantom risk closures were reverted — RISK-0015 and RISK-0016 had been flipped to `closed` citing the 48.13 design-review screenshots, but 48.26 §0.5 item 5 proved those PNGs are 1×1 placeholders; both risks are returned to `monitoring`, the design-review report gained a dated retraction amendment, and the STEP-45 blockquote-era `### STEP-47 substeps` header (swallowed by the STEP-48 table insertion) was restored.

### Staging hygiene handed to the user (open user-side items)

Named per the 48.26 §0.7 GO checklist — these are user-owned and were not performed by any STEP-48 substep:

- **Staging access token revocation.** The PAT used for CI log/API reads during the wave (taken from Git Credential Manager; never echoed) should be revoked or rotated by the owner now that the gate is green.
- **Staging write residue.** The wave's diagnostic re-queries found **10 staging `inventory_items` rows saved as `name='150'` with quantity 25** (three created by 48.21/48.22's own web runs on 2026-09-04 at 18:59, 19:14, 19:29 +07, plus the Sep-3 gate run's row and earlier residue) — the shifted-field saves of the now-fixed unscoped-finder defect. The owner may want to clean these from staging; see `mine-flow-STEP-48.21-FINDINGS.md` §"Established (48.22's concurrent diagnosis)".
- **Placeholder design-review PNGs.** The 73 committed artifacts under `reports/design-review/step-0048/` are 1×1 placeholders and are flagged as invalid evidence in RISK-0023; they remain in the tree until a valid capture run replaces them.

The Phase 4 gate is **not fully satisfied for release-readiness purposes** because named release evidence remains deferred, especially design-review artifacts, accessibility, crew RLS, cold-start deep links, and Drive behavior. Recommendation: keep Phase 4 planning closed until the user explicitly accepts those residuals or their owning follow-up work is completed.

## Historical first-pass record — 2026-08-31 (superseded)

The original close attempt below was correctly blocked by red branch-head CI run `33327930159`. It is retained as historical evidence; the current re-run above supersedes its verdict.

| Job | Result |
|---|---|
| Lint, analyze & test | success |
| Build Android APK | success |
| E2E Tests (Android) | **failure** |
| E2E Tests (Web) | **failure** |

The E2E jobs did execute real journeys, but the run recorded **14 passed, 10 failed, 2 skipped** on Android and corresponding failures on Web. This is evidence of active runtime defects and environment/schema drift, not a closeable four-job gate. The run is available at:

`https://github.com/lvinist/mine-flow-app/actions/runs/33327930159`

The branch-head commit was subsequently formatted and committed as `469b2bc` (`style(STEP-48.15): format screenshot capture test`). Because the required CI run was already red and no replacement green run exists, 48.15 remains blocked and the STEP-48 close is not delivered.

## Verification from disk

- Findings files exist for 48.0 through 48.14.
- The findings support these honest substep statuses: 48.0–48.6 Done, 48.7 Deferred, 48.8–48.14 Done except for the explicit residual items recorded in their findings. 48.15 is not Done.
- App branch contains the claimed STEP-48 implementation commits through `90a995c` plus formatting commit `469b2bc`.
- Docs repo has existing uncommitted changes in `reports/2026-08-30-step-0048-runtime-design-review.md`; prompts repo has an existing uncommitted STEP-50 status flip. These were preserved and not absorbed into this close.
- `./doctor.sh check`: 0 failures, 1 pre-existing workspace-root hygiene warning.
- Duplicate STEP and ADR scans are empty; `git diff --check` passes.

## Local final gate

Executed in `Code/mine-flow-app`:

- `flutter analyze`: **No issues found**
- `dart format --set-exit-if-changed .`: **clean** (327 files)
- `flutter test`: **448 passed, 0 failed**

The PDF test output includes existing font fallback warnings for an em dash; they do not fail the suite.

## CI failure classification

The branch-head CI logs show multiple independent blockers, including:

- Android emulator/ADB startup errors before the Android run proceeded.
- Staging schema mismatch: missing `timeline_milestones` and `benchmarks` tables, missing `measurement_date`, `inventory_items.item_name`, and `equipment_checks.status` columns.
- Invalid or incompatible staging fixture values, including empty UUIDs and non-UUID crew identifiers (`KRU-001`, `KRU-002`).
- Runtime widget/test failures including `UnimplementedError`, `pumpAndSettle` timeouts, and StateErrors.
- Web E2E failures across the same staging/schema and runtime surfaces.

These results confirm that the existing 48.7/48.13 residuals are not the only outstanding release-gate issues. The CI run cannot be summarized as a pass merely because some individual journeys passed.

## Docs-true actions intentionally not completed

The following 48.15 close actions were **not** applied because the close gate failed:

- Doc 09 §4 was not rewritten to claim a passing dual-platform runtime gate.
- Doc 12 was not version-bumped.
- STEP-45 rows were not rewritten as settled, because several runtime journeys remain red or Deferred.
- STEP-48 was not marked Done and no phase README row was appended.
- The PLAN and 48.0–48.15 files were not archived.

This avoids converting a red branch-head gate into a phantom close. The correct next implementation action is to triage and repair the CI/staging schema and runtime failures, then rerun the full branch-head gate before resuming 48.15 closure.

## Residual release blockers already established by earlier findings

- `RISK-0011`: privacy notice absent at runtime; pre-release gate remains open.
- `RISK-0019` / `RISK-0022`: benchmark and true cold-start web deep-link evidence remain unresolved; staging lacks `benchmarks`.
- `RISK-0021`: crew RLS leg remains unverified because `TEST_CREW_*` credentials are absent.
- `RISK-0023`: screen-reader accessibility remains unverified.
- Drive upload/cancellation/large-file behavior remains Deferred by decision D2 (`RISK-0017`/`RISK-0018`).
- The authoritative four-job CI run with non-zero executed journey counts and all jobs green does not exist.

## Recommendation

Keep STEP-48 **In progress** and do not open Phase 4. The immediate follow-up should repair the staging contract/seed alignment and the failing journey/runtime harnesses, then produce a new CI run from the resulting branch head. Re-run 48.15 only after that run has `test`, `build-android`, `e2e-web`, and `e2e-android` successful with non-zero executed counts.
