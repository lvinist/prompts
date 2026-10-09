# mine-flow — STEP-57.0: RISK-0030 Record Reconciliation & Approach-A Verification

> **How to run:** "run substep 57.0". Cold-runnable.
> **Assigned model tier: mid** (record reconciliation bounded by on-disk evidence).

## Context

A prior session delivered the staging zone seed (approach A) BEFORE STEP-57 was reserved:
migration `supabase/migrations/20261008000001_step_56_staging_zone_seed.sql` at app commit
`be682b7` (master), and the live staging row exists (verified 2026-10-10). The records
(risks.yml, STEP-index) still describe the seed as future/draft work. This substep
reconciles the record and pins the verified evidence, so 57.1+ plans from truth.
STEP PLAN: `Upcoming Prompts/mine-flow-STEP-57-PLAN.md`.

## Read these first

- `Code/mine-flow-docs/registries/risks.yml` — RISK-0030 row (and RISK-0025 for the
  production-blocked boundary).
- `Upcoming Prompts/mine-flow-STEP-57-DRAFT-staging-zone-seed.md` — the original draft
  (now historical; A is delivered, B is this STEP).
- `Code/mine-flow-app/supabase/migrations/20261008000001_step_56_staging_zone_seed.sql`.
- `prompts/STEP-index.md` — STEP-55 row + 55.11 evidence cells (seed mentions).

## Scope

**Owns:** (a) re-deriving approach-A evidence from disk + live staging; (b) updating
risks.yml RISK-0030 (status stays open; description/mitigation updated to record A
delivered with evidence; revisit_trigger narrowed to B + journey); (c) FINDINGS file.
Docs repo branch `step-0057-zone-insert-policy`.

**Does NOT touch:** app code, migrations, `STEP-index.md` status cells, the seed file.

## Your task

1. Verify on disk: migration file exists at `be682b7` in master history
   (`git log --oneline -- <path>`), content idempotent (`ON CONFLICT (id) DO NOTHING`),
   fixed UUID `6e60b2e2-0000-4000-8000-000000005656`, site `f47ac10b-…479`
   (cross-check `lib/core/constants/app_constants.dart` defaultSiteId).
2. Live-probe staging (REST via `.env` SUPABASE_URL/ANON_KEY — never print values):
   authenticated test-user GET `zones?id=eq.6e60b2e2-…` → row present = applied.
   Also record `created_at`.
3. Patch risks.yml RISK-0030: add to mitigation/description "Approach A delivered
   (migration 20261008000001, commit be682b7, staging live-verified 2026-10-10)";
   keep status `open` (B pending). Targeted patch; preserve CRLF; verify
   `git diff --stat` minimal.
4. Write `Upcoming Prompts/mine-flow-STEP-57.0-FINDINGS.md` with evidence (commands +
   outputs summarized, probe result, diff summary).

## Verification

- `git -C Code/mine-flow-docs diff --check` clean; diff = risks.yml only.
- YAML still parses (python yaml if available; else visual indent check + check.sh).
- `./check.sh` 0 fails.
- Live probe output recorded in FINDINGS (id + created_at only — no PII).

## Definition of done

- [ ] risks.yml updated with A-delivered evidence; RISK-0030 still open (B pending).
- [ ] FINDINGS carries disk + live evidence; no values/secrets printed.
- [ ] Committed on `step-0057-zone-insert-policy` (docs repo), not pushed.

## Next

Report to parent orchestrator. Next: 57.1 (threat review + ADR) — which is an owner gate:
its output parks for owner approval before 57.2 implements anything.
