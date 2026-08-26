# STEP-44 — Security, Privacy & Release-Control Baseline

**Status:** Done
**Branch:** `step-0044-security-baseline` (mine-flow-docs)
**Owner:** Antigravity (Claude Sonnet 4.6 Thinking)
**Date:** 2026-08-26

## Scope

Run the S0 Security Baseline review (from `runbooks/security-review.md` and
`runbooks/security-review-s0-checklist.md`) against the current codebase pre-staging.
Documentation and evidence only — no new app features.

## Substeps

| Substep | Title | Status |
|---|---|---|
| 44.1 | STEP reservation & branch setup | Done |
| 44.2 | RLS / authorization behavior audit | Done |
| 44.3 | Account lifecycle verification | Done |
| 44.4 | Privacy notice gap check | Done |
| 44.5 | Secrets posture audit | Done |
| 44.6 | Backup / restore fire-drill record | Done |
| 44.7 | S0 baseline report & registry updates | Done |
| 44.8 | Architecture doc & STEP close | Done |

## Key Findings

- **RLS audit (44.2):** All 9 tables covered. Post-migration schemas (migrations 3/4/5) add columns/drop columns to existing tables — no new tables, no RLS gaps. No remediation migration needed.
- **Account lifecycle (44.3):** `deleted_at` on `users`; supervisors only can DELETE; hard-delete via Supabase Admin API only. Correctly implemented.
- **Privacy notice (44.4):** NOT implemented. RISK-0011 added as pre-release gate.
- **Secrets posture (44.5):** `.env.example` confirmed present (STEP-42). `.env` gitignored. All CI secrets via `secrets.*`. No hardcoded values. GitHub secret scanning status not verified locally → RISK-0013.
- **Backup (44.6):** Supabase free-tier — no automatic backups. Manual procedure documented in S0 report. RISK-0012 added.

## Outputs

- `Code/mine-flow-docs/reports/security/2026-08-26-step-0044-s0-security-baseline-report.md` — full S0 report
- `Code/mine-flow-docs/registries/risks.yml` — RISK-0011, RISK-0012, RISK-0013 added
- `Code/mine-flow-docs/registries/security-reviews.yml` — S0 last_run populated
- `Code/mine-flow-docs/architecture/06-security-threat-model.md` — bumped to v0.2.0

## Verification Gate

| Command | Result |
|---|---|
| `flutter analyze` | No issues found (0 errors, 0 warnings) |
| `flutter test` | 435 tests passing |
