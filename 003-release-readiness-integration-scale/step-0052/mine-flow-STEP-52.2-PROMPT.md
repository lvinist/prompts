# mine-flow — STEP-52.2: S0 Report Finalization, Registry & Doc Updates, Verification & Close

> **How to run:** Tell your agent *"run substep 52.2"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.

## Context

Substep 52.1 completed the full security surface audit, evaluated all 34 checklist items, verified RLS across all 11
tables, adjudicated RISK-0021, re-checked RISK-0011..0013, and documented all findings in `Upcoming Prompts/mine-flow-STEP-52.1-FINDINGS.md`.

This substep publishes the canonical S0 Security Baseline Report, updates the security review ledger and risk register,
synchronizes architecture documentation, runs the full verification gate, and closes STEP-52.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-52-PLAN.md` (the whole STEP plan)
- `Upcoming Prompts/mine-flow-STEP-52.1-FINDINGS.md` (52.1 audit findings and completed S0 table)
- `Code/mine-flow-docs/templates/reports/security/s0-security-baseline-report-template.md` (report template)
- `Code/mine-flow-docs/registries/security-reviews.yml` (review ledger to update)
- `Code/mine-flow-docs/registries/risks.yml` (risk register to update)
- `Code/mine-flow-docs/architecture/06-security-threat-model.md` (threat model doc to update)

## Scope

**Owns:**
1. Publishing canonical report `Code/mine-flow-docs/reports/security/2026-09-10-step-0052-s0-security-baseline-report.md`.
2. Updating `Code/mine-flow-docs/registries/security-reviews.yml` with S0 last_run entry.
3. Updating `Code/mine-flow-docs/registries/risks.yml` with risk updates/adjudications.
4. Updating `Code/mine-flow-docs/architecture/06-security-threat-model.md` (table count bump to 11, Version Log bump to v0.3.0).
5. Running verification gates: `dart run tool/check_supabase_contracts.dart`, `dart run tool/check_l10n_baseline.dart`, `flutter analyze`, and `flutter test`.
6. Gathering STEP files from `Upcoming Prompts/` into `prompts/003-release-readiness-integration-scale/step-0052/`.
7. Updating phase `README.md` and `prompts/STEP-index.md` to mark STEP-52 `Done`.
8. Merging git branches and telling the user what's next.

## Verification & Handoff

- Full verification suite passes clean.
- STEP-52 marked `Done` in `prompts/STEP-index.md`.
- Next action: *\"start STEP-53 (Dependency Maintenance)\"* per `doctor.sh status`.
