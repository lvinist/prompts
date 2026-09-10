# mine-flow — STEP-52.1: Security Baseline Surface Audit & Risk Adjudication

> **How to run:** Tell your agent *"run substep 52.1"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.

## Context

The S0 Security Baseline established in STEP-44 (2026-08-26, commit `5536191`) was invalidated by major CI,
infrastructure, and schema additions in STEP-45 (dual-platform E2E gate), STEP-47 (build chain & CI modernization),
and STEP-48 (staging schema, seed fixtures, secrets surface, and two new tables `timeline_milestones` and `benchmarks`).

This substep conducts the comprehensive security audit across all new surfaces, re-verifies RLS coverage across all 11
tables, adjudicates outstanding risks RISK-0011..0013 and RISK-0021, synchronizes `.env.example`, and completes the
S0 decision checklist.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-52-PLAN.md` (the whole STEP plan)
- Root `.throughstone/local-user.md` (calibrate communication: Level 2, Explanatory)
- `Code/mine-flow-docs/runbooks/security-review.md` (S0 procedure)
- `Code/mine-flow-docs/runbooks/security-review-s0-checklist.md` (34-item S0 checklist)
- `Code/mine-flow-docs/reports/security/2026-08-26-step-0044-s0-security-baseline-report.md` (previous S0 baseline)
- `Code/mine-flow-docs/registries/security-reviews.yml` (review ledger)
- `Code/mine-flow-docs/registries/risks.yml` (RISK-0011, RISK-0012, RISK-0013, RISK-0021)
- `Code/mine-flow-app/.github/workflows/ci.yml` (CI workflows & secrets injection)
- `Code/mine-flow-app/supabase/migrations/*.sql` (all 9 database migration files)

## Scope

**Owns:**
1. Verifying git branches across repos (`step-0052-security-baseline-recheck`).
2. Auditing CI secrets handling across `.github/workflows/ci.yml`, test runners, and `.env.example`.
3. Updating `Code/mine-flow-app/.env.example` to document E2E `TEST_*` credential variables.
4. Comprehensive RLS audit across all 11 tables (`users`, `zones`, `attendance_records`, `equipment_checks`, `daily_logs`, `cut_fill_records`, `land_clearing_records`, `inventory_items`, `geospatial_files`, `timeline_milestones`, `benchmarks`).
5. Adjudication of RISK-0021 (crew RLS / cross-role isolation).
6. Re-check of RISK-0011 (in-app privacy notice), RISK-0012 (free-tier backups), and RISK-0013 (ops cluster).
7. Evaluation and completion of all 34 rows in the S0 checklist (`runbooks/security-review-s0-checklist.md`).
8. Producing `Upcoming Prompts/mine-flow-STEP-52.1-FINDINGS.md` with complete evidence citations and findings.

**Does NOT touch:**
- Application feature code (`lib/` remains untouched).
- Writing the final published report in `Code/mine-flow-docs/reports/security/` (owned by 52.2).

## Verification & Handoff

- Substep findings recorded in `Upcoming Prompts/mine-flow-STEP-52.1-FINDINGS.md`.
- Status of 52.1 marked `Done` in `mine-flow-STEP-52-PLAN.md` and `prompts/STEP-index.md`.
- Next action: *\"run substep 52.2\"* (S0 report finalization, registry updates, verification gate & close).
