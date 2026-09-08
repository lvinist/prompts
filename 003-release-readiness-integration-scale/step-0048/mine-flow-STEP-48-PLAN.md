# mine-flow — STEP-48 PLAN: Runtime Evidence — resolve STEP-45's carried-forward findings

**Phase:** Phase 3 — Release Readiness, Integration & Scale
**Owner:** User (single accountable owner; model lanes are executors)
**Status:** Done (closed by substep 48.15 on 2026-09-08)
**Branch:** `step-0048-runtime-evidence`
**Repos:** `mine-flow-app`, `mine-flow-docs`, `prompts`

## Close-state reconciliation

This close-state PLAN records the final scope and evidence after the remediation wave. The authoritative execution records are the substep findings files and the branch-head CI record in `mine-flow-STEP-48.26-FINDINGS.md` §0.

STEP-48 consumed the runtime-evidence deferrals from STEP-45. It repaired the journey suite, staging schema and fixtures, synchronization contracts, CI evidence guards, and two audit findings, then verified the branch head in CI. It does not claim delivery of deliberately deferred Drive behavior, crew RLS credentials, true browser cold-start deep links, screen-reader behavior, or valid screenshot artifacts.

## Locked decisions

- CI is the authoritative E2E gate; local runs are for iteration and local/static verification.
- A green job is insufficient without non-zero executed counts and named skips.
- Drive upload, abandon/cancel, and large-file behavior remain out of scope by decision D2 (`RISK-0017`/`RISK-0018`).
- Offline-first relaunch evidence is Android-scoped per Doc 15 §1; the web leg records its supported Part B coverage and named platform limitation.
- No secrets are recorded. The test credentials and staging access token are referenced only by name in durable records.
- Generated `DESIGN.md` and `PRODUCT.md` are not hand-edited.

## Substeps and final status

| # | Title | Status | Evidence |
|---|---|---|---|
| 48.0 | Credential and toolchain pre-flight | Done | `mine-flow-STEP-48.0-FINDINGS.md`; staging accounts/secrets and proof-of-life run |
| 48.1 | Journey-integrity repair audit | Done | `mine-flow-STEP-48.1-FINDINGS.md`; fake green and stubs removed, all journey files audited |
| 48.2 | CI gate expansion and evidence artifacts | Done | `mine-flow-STEP-48.2-FINDINGS.md`; full journey targets and CI workflow wiring |
| 48.3 | Auth and session runtime evidence | Done | `mine-flow-STEP-48.3-FINDINGS.md`; branch-head run 34225431645 |
| 48.4 | Attendance and daily-log runtime evidence | Done | `mine-flow-STEP-48.4-FINDINGS.md`; persistence fixes confirmed at branch head |
| 48.5 | Cut/fill and land-clearing runtime evidence | Done | `mine-flow-STEP-48.5-FINDINGS.md`; branch-head journeys passed |
| 48.6 | Inventory and equipment-check runtime evidence | Done | `mine-flow-STEP-48.6-FINDINGS.md`; invalid write keys removed and journeys passed |
| 48.7 | Benchmark journey and NR-006 | Deferred | Benchmark journey passed; true browser cold-start deep link remains RISK-0019 |
| 48.8 | Reporting and PDF runtime evidence | Done | `mine-flow-STEP-48.8-FINDINGS.md`; journey and NR-001 controls passed; PDF operational follow-up remains RISK-0014 |
| 48.9 | Timeline and notifications runtime evidence | Done | `mine-flow-STEP-48.9-FINDINGS.md`; journeys passed |
| 48.10 | Offline/sync Part A | Done | `mine-flow-STEP-48.10-FINDINGS.md`; Android field path and server-side LWW evidence |
| 48.11 | Deep-link validation and RISK-0006 | Done | `mine-flow-STEP-48.11-FINDINGS.md`; in-process route matrix and unavailable Drive route state passed |
| 48.12 | Live RLS evidence | Deferred | Supervisor/foreman paths passed; crew and cross-role isolation remain RISK-0021 |
| 48.13 | Runtime design review | Deferred | Harness ran, but screenshot artifacts are invalid/unavailable and screen-reader evidence is absent |
| 48.14 | Risk-register reconciliation | Done | `mine-flow-STEP-48.14-FINDINGS.md`; residual risks recorded |
| 48.15 | Docs-true sweep, index correction, and close | Done | `mine-flow-STEP-48.15-FINDINGS.md`; docs/index/archive close record |
| 48.16 | Branch-head failure triage | Done | `mine-flow-STEP-48.16-FINDINGS.md`; failure classes assigned |
| 48.17 | Staging schema completion | Done | `mine-flow-STEP-48.17-FINDINGS.md`; migrations applied and types regenerated |
| 48.18 | Datasource column-name reconciliation | Done | `mine-flow-STEP-48.18-FINDINGS.md` |
| 48.19 | Write-path dual-key purge | Done | `mine-flow-STEP-48.19-FINDINGS.md` |
| 48.20 | Staging fixture and seed alignment | Done | `mine-flow-STEP-48.20-FINDINGS.md` |
| 48.21 | Journey finder repair | Done | `mine-flow-STEP-48.21-FINDINGS.md` |
| 48.22 | UI and harness defect fixes | Done | `mine-flow-STEP-48.22-FINDINGS.md` |
| 48.23 | Persistence and offline-integrity defects | Done | `mine-flow-STEP-48.23-FINDINGS.md` |
| 48.24 | Local full-gate re-run | Done | `mine-flow-STEP-48.24-FINDINGS.md`; local gate handed off GO |
| 48.25 | Git object-store repair and wave commit | Done | `mine-flow-STEP-48.25-FINDINGS.md`; branch fast-forward pushed |
| 48.26 | Branch-head CI gate | Done | `mine-flow-STEP-48.26-FINDINGS.md` §0; run 34225431645 GO |
| 48.27 | Post-gate contract remediation | Done | `mine-flow-STEP-48.27-FINDINGS.md`; residual contract fixes and TZ sweep |
| 48.28 | Registry and documentation truth repair | Done | `mine-flow-STEP-48.28-FINDINGS.md`; YAML guard and registry repair |
| 48.29 | Evidence-guard hardening | Done | `mine-flow-STEP-48.29-FINDINGS.md`; Android/web execution guards and l10n guard |
| 48.30 | Dead-affordance and shadow-file cleanup | Done | `mine-flow-STEP-48.30-FINDINGS.md`; selection-only combobox and shadow deletions |

## Final verification evidence

- `flutter analyze`: exit 0, no issues.
- `dart format --set-exit-if-changed .`: initial run changed only untracked `run_web_wrapper.dart`; the final code tree was verified format-clean by the prior exact-tree gate and CI. The scratch wrapper is not part of the deliverable.
- `flutter test`: final rerun exit 0, **553 tests passed, 0 failed**. The immediately preceding full run exposed the known intermittent Hive `setUpAll` failure in `test/integration/attendance_daily_log_sync_test.dart`; its isolated rerun passed 3/3, and the exact full suite was rerun successfully.
- Branch-head CI: [run 34225431645](https://github.com/lvinist/mine-flow-app/actions/runs/34225431645), commit `d53fb7e21f2299eb6b65a3aa4e72dc48d851a1eb`; `test`, `build-android`, `e2e-web`, and `e2e-android` all succeeded.
- Android: 24 passed, 2 named skips, 0 failed; 17/17 APK installs; execution guard reported 24 executed.
- Web: 16/16 loop files returned `result:true`, 22 execution markers, 3 named skips; execution guard reported 22 executed.
- `./doctor.sh check`: 0 failures, 1 pre-existing workspace-root hygiene warning.
- Duplicate STEP/ADR scans and repository `git diff --check` pass for the owned changes.

## Remaining limitations and ownership

The Phase 4 gate is **not fully satisfied for release-readiness purposes**. The branch-head four-job execution gate is green, but these items remain explicitly open: Drive behavior (`RISK-0017`/`RISK-0018`), crew RLS and cross-role isolation (`RISK-0021`), true browser cold-start/reload deep links (`RISK-0019`), screen-reader accessibility (`RISK-0023`), valid screenshot-backed design-review evidence, and the PDF operational regression follow-up (`RISK-0014`). The user must decide whether to accept these residuals before opening Phase 4 planning.

## Archive contents

On completion, this PLAN, all substep prompts, and all findings files are gathered under `prompts/003-release-readiness-integration-scale/step-0048/`. The durable design-review report remains under `Code/mine-flow-docs/reports/`; it is not moved into the prompt history archive.
