# mine-flow — STEP-50 PLAN: Phase 3 Check-in (post-STEP-47 dependency overhaul)

**Phase:** Phase 3 — Release Readiness, Integration & Scale
**Owner:** Hermes (Claude Opus 4.8)
**Status:** Done (closed by substep 50.2 on 2026-09-08)
**Date:** 2026-08-29 (PLAN authored) · closed 2026-09-08
**Branch:** `step-0050-phase3-check-in`
**Repos (projection):** `mine-flow-docs`, `prompts` (merge order: docs → prompts)

> Periodic check-in run at the STEP-47 breakpoint. It reconciles the architecture docs
> against the system as it actually is after the Flutter 3.47 upgrade (STEP-43), the security
> and privacy baseline (STEP-44), the staging pipeline (STEP-42), the UI/UX audit (STEP-46)
> and the AGP-9 build-chain remediation plus 9-major dependency sweep (STEP-47); re-evaluates
> conditional-session coverage; reviews the risk register and the security-review gate; and
> runs the full test suite. It writes no application code.

## Motivation

The last check-in was STEP-39/40 (Phase 2 Tier 2), ten STEPs ago — inside the ~10–20 STEP
cadence in `METHOD.md` §5, and `scripts/status.sh` reports the cadence as due. Since then the
project changed shape in ways that are exactly what a check-in exists to catch: the toolchain
and every direct dependency moved (STEP-43, STEP-47), a staging environment and promotion
pipeline appeared (STEP-42), a security/privacy baseline landed (STEP-44), 97 UI findings were
remediated (STEP-46), and an E2E tier was added whose runtime evidence is still outstanding
(STEP-45).

It is sequenced **before** STEP-48 deliberately: STEP-48 must consume a truthful risk register
and accurate environment/test-strategy docs when it goes after the runtime evidence, rather
than discovering drift mid-run.

## Decisions already locked

- **Check-in runbook** — `Code/mine-flow-docs/runbooks/check-in.md` defines both substeps.
  This PLAN points there; no substep prompts are authored (thin STEP, per
  `prompts/README.md` step 5).
- **Honesty rule (STEP-45/47 lesson)** — a substep may not be marked `Done` if its own
  evidence says Unverified. Anything unrunnable in this check-in is recorded as `Unverified`
  or `Deferred` with a reason, never as a pass.
- **Status vocabulary** — index/PLAN status cells accept only
  Planned / In progress / Done / Deferred / Abandoned / N/A (`scripts/check.sh` gate).
- **Local user profile** — root `.throughstone/local-user.md`: Level 2, Explanatory.
- **Registries are the source of truth** for risk and security-review state:
  `registries/risks.yml`, `registries/security-reviews.yml`.
- **No S1/S2 inside a check-in** — if the security gate is due, this STEP files a separate
  Security Review / Audit STEP (`runbooks/check-in.md`, "Security-review gate").
- **Full suite scope (user decision, 2026-08-29):** `flutter test` in `mine-flow-app` is the
  gate for Part 2. Analyzer/format and release-build checks are not part of this check-in's
  bar; the `integration_test` journeys remain STEP-48's business.

## Substeps

| #    | Title | Produces | Depends on | Open questions |
|------|-------|----------|------------|----------------|
| 50.1 | Doc-drift reconciliation, conditional coverage, risks & security gate | `scripts/check.sh` pass; doc fixes with Version-Log bumps; `architecture/README.md` index reconciled; conditional dispositions; `registries/risks.yml` review; S0/S1/S2 gate decision; any follow-up STEP rows | STEP-47 close | Does any STEP-47 dependency change contradict a still-correct doc (→ bug, not doc edit)? |
| 50.2 | Full test run | `flutter test` result recorded in the check-in report (+ durable output under `reports/test-results/` if material) | 50.1 | Known flake: `test/integration/attendance_daily_log_sync_test.dart` (Hive `setUpAll`) fails intermittently full-suite, green isolated — must be diagnosed as flake vs. regression, not waved through |

**Substep status:** 50.1 **Done** (2026-09-08) — report
`Code/mine-flow-docs/reports/2026-09-08-step-0050-check-in-report.md` (note: run date, not the
2026-08-29 PLAN date, per the runbook's YYYY-MM-DD naming rule). Delivered: check.sh 0 failures;
6 doc-drift fixes with version bumps (Doc 11 v0.3.0 + **ADR-0019** TS contract of record, Doc 08
v0.2.1 CI graph, Doc 13 v0.1.1 glossary, Doc 15 v0.2.1 OQ-2, repos.yml posture, app README
contract section — app commit pair `f693328`+`b9bcce5`, the second undoing a CRLF-churn
accident); risk register RISK-0022 close flipped, RISK-0007/RISK-0009 trigger annotations,
RISK-0024 raised; conditional coverage confirmed (3/3 Included, no re-interview triggers);
security gate: S0 invalidated by STEP-45/47/48 CI changes → **STEP-52** (S0 re-check) and
**STEP-53** (dependency maintenance: hive_ce ~7-month trigger, PR 191587 merged-no-stable,
minor pub-outdated drift) reserved on prompts/main `c6012c1`. No new code-vs-doc bug-class
drift found. 50.2 **Done** (2026-09-08) — full `flutter test` at branch head `b9bcce5`
(Flutter 3.47.1 stable, local Windows host): **553 passed / 0 failed / 0 skipped**, elapsed
01:40. Known Hive `setUpAll` flake (`test/integration/attendance_daily_log_sync_test.dart`)
did not reproduce — no failure to dispose. Durable record:
`Code/mine-flow-docs/reports/test-results/2026-09-08-step-0050-full-suite-test-results.md`.
Also executed at close: the workspace-root hygiene disposition from the 50.1 report — ~130
transient debris files deleted, four `step4826_r7_*` logs + `step4824_web_loop.sh` retained
in place (cited by archived STEP-48 records). STEP-50 is **closed**: both substeps Done,
report final, index row flipped, PLAN archived to
`prompts/003-release-readiness-integration-scale/step-0050/`.

No substep prompts are authored for this STEP — the runbook *is* the prompt (`runbooks/check-in.md`
Part 1 → 50.1, Part 2 → 50.2).

## Test plan

| Test tier / surface | Substep(s) | Tests to create or update | Run timing | Command / gate | Notes |
|---------------------|------------|---------------------------|------------|----------------|-------|
| Unit + widget + integration (`mine-flow-app`) | 50.2 | None authored — this STEP writes no application code | Substep 50.2 | `flutter test` | Any failure is a finding: fixed here if small, else filed as a bug STEP. A red suite is not left for later. |
| End-to-end (`integration_test`) | — | — | Not run here | — | Owned by STEP-48; the 14 staging journeys stay Deferred. |

## Open questions

- Q1 (owner: 50.1) — Does `architecture/09-environments.md` v0.4.0 still describe the host
  prerequisites correctly after STEP-47's `dependency_overrides` elimination?
- Q2 (owner: 50.1) — Are RISK-0015..0019 (STEP-45 carry-forwards) correctly parked on STEP-48,
  or has any trigger fired that warrants its own STEP?
- Q3 (owner: 50.1) — Is the S0 baseline (2026-08-26) invalidated by STEP-47's CI/build changes,
  making a re-check due before release?

## Ground rules

- **Review and verification only.** No application code. Doc fixes, registry updates, filed
  follow-ups, and a test run.
- **Both directions on drift.** Stale doc → fix the doc and bump its Version Log; write an ADR
  if a real decision was made in code but never recorded. Code drifted from a still-correct
  doc → file a bug/follow-up STEP; do **not** edit the doc to bless the drift.
- **Generated files are not edited by hand.** Root `DESIGN.md` / `PRODUCT.md` are generated
  from `architecture/07-ui-design-system.md` and `overview.md`.
- **Archived plans and reports are immutable.** Earlier check-in reports and archived STEP
  PLANs are read, never rewritten; this check-in's report records the new current disposition.
- **No secrets.** `.env` values are not read or printed; secret names/placeholders only.
- **Calibrate communication** from root `.throughstone/local-user.md`.

## Definition of done

- [ ] `scripts/check.sh` run and every structural failure it reports fixed.
- [ ] All 16 `architecture/NN-*.md` docs reviewed against the current system in both
      directions; fixes applied with Version-Log bumps; `architecture/README.md` index matches
      the docs on disk.
- [ ] Every `templates/architecture-sessions/conditional-*.md` enumerated with an explicit
      current disposition recorded in the report.
- [ ] Repo READMEs, interface-contract artifacts, and a docstring spot-check swept.
- [ ] `registries/risks.yml` reviewed row by row (RISK-0001..0020); mitigated items closed,
      stale rows updated, fired triggers promoted to follow-up STEPs.
- [ ] Security-review gate (S0/S1/S2) evaluated and the decision recorded; a Security
      Baseline/Review/Audit STEP filed if one is due. `registries/security-reviews.yml` is
      updated only if a review actually ran.
- [ ] Implemented-design-review coverage for UI-heavy STEPs since the last check-in confirmed,
      with any Blocking/Needs-remediation/Unverified result carrying a named owning STEP.
- [ ] Full `flutter test` executed; the result and the disposition of any failure recorded.
- [ ] Check-in report written to
      `Code/mine-flow-docs/reports/2026-08-29-step-0050-check-in-report.md` from
      `templates/reports/check-in-report-template.md`.
- [ ] `prompts/STEP-index.md`: STEP-50 `Done` with its substep table; any spawned follow-up
      STEP rows added; next check-in noted (~10–20 STEPs out).
- [ ] Thin PLAN archived to `prompts/003-release-readiness-integration-scale/step-0050/`;
      phase README row added. The report stays under `reports/`, not in the STEP folder.
