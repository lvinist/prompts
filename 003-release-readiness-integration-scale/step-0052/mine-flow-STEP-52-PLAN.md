# mine-flow — STEP-52 PLAN: Security Baseline re-check (post-STEP-48)

**Phase:** Phase 3 — Release Readiness, Integration & Scale
**Owner:** Antigravity
**Status:** In progress
**Date:** 2026-09-10
**Branch:** `step-0052-security-baseline-recheck`
**Repos (projection):** `mine-flow-app`, `mine-flow-docs`, `prompts` (merge order: app → docs → prompts)

> Re-run of the S0 Security Baseline from `runbooks/security-review.md` and `runbooks/security-review-s0-checklist.md`.
> The initial 2026-08-26 baseline (commit `5536191`, STEP-44) was invalidated per its own cadence rule by subsequent
> major CI and infrastructure changes: STEP-45 added the dual-platform E2E gate, STEP-47 overhauled the build chain,
> and STEP-48 expanded the staging schema, fixtures, and secrets surface. This review verifies secrets handling across
> the new E2E and staging surfaces, re-audits RLS across all 11 tables (including `timeline_milestones` and `benchmarks`),
> re-checks RISK-0011..0013, adjudicates RISK-0021 (crew RLS), and updates the durable security review ledger.

## Motivation

The S0 Security Baseline established in STEP-44 (2026-08-26) explicitly recorded its invalidation trigger:
*"Before production release or after any major CI/hosting/ownership change"*. Since STEP-44, three major STEPs altered
the system's security and CI surfaces:
1. **STEP-45** added the dual-platform E2E test gate, introducing new GitHub Actions workflows (`e2e-web`, `e2e-android`),
   headless Chrome/chromedriver runners, and an Android emulator runner.
2. **STEP-47** modernized the Android build chain (AGP 9, Kotlin 2.4, JDK 17, AGP-9 native plugins) and revised CI workflows.
3. **STEP-48** introduced staging test user credentials (`TEST_USER_*`, `TEST_SUPERVISOR_*`, `TEST_FOREMAN_*`), Google Drive
   secrets in CI, staging database seed fixtures, and two new Supabase tables (`timeline_milestones` and `benchmarks`)
   postdating STEP-44's "all 9 tables covered" audit claim.

Running this S0 re-check now ensures that the project's security guardrails, secrets isolation, and authorization
boundaries remain intact and verified before release candidates proceed to production.

## Decisions already locked

- **S0 checklist contract** — Follow `Code/mine-flow-docs/runbooks/security-review.md` and
  `Code/mine-flow-docs/runbooks/security-review-s0-checklist.md`.
- **Honesty rule** — Unverified items (e.g. GitHub UI settings without `gh` CLI access, or missing credentials)
  must be recorded honestly as `Accepted Risk`, `Deferred`, or `Unverified locally`, never disguised as passes.
- **Local user profile** — Root `.throughstone/local-user.md`: Level 2 (Basic coding experience), Explanatory style.
- **Registries as source of truth** — `registries/security-reviews.yml` records the durable ledger;
  `registries/risks.yml` tracks accepted risks and deferrals.
- **Status vocabulary** — Allowed status values: `Planned`, `In progress`, `Done`, `Deferred`, `Abandoned`, `N/A`.
- **No application feature creep** — Security review, configuration hygiene, registry updates, and verification only.

## Substeps

| # | Title | Produces | Depends on | Open questions |
|---|-------|----------|------------|----------------|
| 52.1 | Security baseline surface audit & risk adjudication (Done) | E2E/staging secrets audit; 11-table RLS audit; RISK-0011..0013 & RISK-0021 adjudication; `.env.example` sync; completed S0 checklist in `Upcoming Prompts/mine-flow-STEP-52.1-FINDINGS.md` | STEP-51 close | None |
| 52.2 | S0 report, registry & doc updates, verification & close | Canonical report `reports/security/2026-09-10-step-0052-s0-security-baseline-report.md`; `security-reviews.yml` & `risks.yml` updates; Doc 06 v0.3.0; test verification gate; STEP close & archival | 52.1 | None |

**Substep status:** 52.1 **Done** (2026-09-10) — all audits executed, `.env.example` updated (`6fbce5e`), `.github/workflows/ci.yml` wired with `TEST_CREW_*` (`be44843`), 11/11 tables audited (FINDING-52.1-01 privilege escalation hole identified), RISK-0021 adjudicated, 34-row checklist completed, findings in `Upcoming Prompts/mine-flow-STEP-52.1-FINDINGS.md`. Next up: 52.2.

## Test plan

| Test tier / surface | Substep(s) | Tests to create or update | Run timing | Command / gate | Notes |
|---------------------|------------|---------------------------|------------|----------------|-------|
| Contract checks | 52.2 | None (re-verify existing) | Substep 52.2 | `dart run tool/check_supabase_contracts.dart` | Verifies Supabase schema contract |
| Localization baseline | 52.2 | None (re-verify existing) | Substep 52.2 | `dart run tool/check_l10n_baseline.dart` | Verifies l10n compliance guard |
| Static analysis | 52.2 | None | Substep 52.2 | `flutter analyze` | 0 errors, 0 warnings required |
| Full unit/widget suite | 52.2 | None | Substep 52.2 | `flutter test` | Must pass clean (550 passed, 5 skipped baseline) |

## Open questions

- **Q1 (adjudicated in 52.1):** Does the crew RLS policy model provide complete isolation across all 11 tables despite `TEST_CREW_*` secrets being absent from CI?
  *Disposition:* Static SQL policy review confirms complete table-by-table isolation (read-only on operational data, own-row filtering on attendance, zero write access elsewhere). Runtime automated CI execution remains deferred until GitHub secrets are provisioned.
- **Q2 (adjudicated in 52.1):** Do the two post-STEP-44 tables (`timeline_milestones` and `benchmarks`) enable and enforce RLS properly?
  *Disposition:* Both tables have `ENABLE ROW LEVEL SECURITY` with full supervisor access, foreman select/insert/update, crew select-only, and zero unauthenticated access.

## Ground rules

- **Review and verification only.** No code refactors or new features.
- **Durable records live in docs.** The completed baseline report lives in `Code/mine-flow-docs/reports/security/`, not in `Upcoming Prompts/`.
- **No secrets in tracked files.** Real keys and credentials are never written to disk or commit messages.
- **Append-only registries.** Follow formatting rules in `registries/risks.yml` and `registries/security-reviews.yml`.

## Definition of done

- [ ] All 11 Supabase tables audited for RLS coverage and policy correctness.
- [ ] Secrets handling across the CI/E2E workflows (`.github/workflows/ci.yml`), `.env.example`, and seed scripts audited.
- [ ] E2E `TEST_*` credential variables documented in `.env.example`.
- [ ] Risks RISK-0011, RISK-0012, RISK-0013, and RISK-0021 formally adjudicated with evidence.
- [ ] All 34 rows of the S0 checklist completed with explicit status, owner, date, evidence, and revisit trigger.
- [ ] Substep 52.1 FINDINGS written to `Upcoming Prompts/mine-flow-STEP-52.1-FINDINGS.md`.
- [ ] Canonical S0 Baseline Report published at `Code/mine-flow-docs/reports/security/2026-09-10-step-0052-s0-security-baseline-report.md`.
- [ ] `registries/security-reviews.yml` updated with S0 entry.
- [ ] `registries/risks.yml` updated with risk adjudications.
- [ ] `architecture/06-security-threat-model.md` updated and Version Log bumped.
- [ ] Verification gate passes: `flutter analyze` clean, contract & l10n guards pass, `flutter test` green.
- [ ] Index and phase README updated, branches merged, files archived to `prompts/003-release-readiness-integration-scale/step-0052/`.
