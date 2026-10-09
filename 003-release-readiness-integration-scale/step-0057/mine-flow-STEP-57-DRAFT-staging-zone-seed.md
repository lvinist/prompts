# DRAFT (for owner review) — Staging zone seed for daily-log E2E round-trip

> **Status: DRAFT — not reserved, not run.** This proposes a SEPARATE
> schema/data STEP (next free number is **STEP-56**). It exists because the
> STEP-55.11 RESIDUAL-2 lane is forbidden from touching migrations/RLS/`supabase/**`,
> and the daily-log create-zone staging round-trip cannot be proven without a
> seedable zone. Reserve the STEP number and author the full prompt only on your
> go-ahead (Throughstone: planning does not reserve or flip status).

## Problem

Staging `public.zones` is empty, and foremen have no INSERT policy on `zones`.
Every daily-log sync that references a locally-created zone fails:
- `daily_logs_zone_id_fkey` violation (Postgres 23503) — the zone row the log
  points at does not exist on staging; or
- RLS denial (42501) if a foreman tries to create the zone client-side.

So the daily-log E2E journey's create-zone path can reach the UI but never
completes a verified staging round-trip. STEP-55.11 records it as **Unverified**.

## Two candidate approaches (owner already leaned: SEED)

### A. Seed a stable staging zone (CHOSEN lean)
Add an idempotent seed that guarantees one known zone row exists on staging for
the E2E test site, so journeys reference a real FK target without needing
foreman INSERT rights.

- **Where:** a dedicated seed artifact (NOT a schema migration that alters
  structure) — e.g. `supabase/seed/step56_staging_zone.sql` run against staging
  only, or a documented runbook step in the E2E setup. Decide which during
  authoring; a seed is data, not DDL, and must be idempotent
  (`INSERT ... ON CONFLICT (id) DO NOTHING` on a fixed UUID).
- **Zone identity:** pin a stable UUID + name + category for the test site
  (`site-alpha` / `defaultSiteId`), documented so the journey can reference it.
- **No policy change:** foremen still cannot create zones; the test uses the
  seeded zone. The create-zone *product* path stays separately Unverified
  unless B/below is also chosen.
- **Verification:** daily-log journey selects the seeded zone, submits, and the
  staging read-back succeeds (no 23503). Record run id + head.

### B. Grant foreman INSERT on zones (NOT chosen — recorded for completeness)
A real RLS policy change (`CREATE POLICY insert_zones ... WITH CHECK (...)`).
This is a security-surface change: who may create zones, scoping by site/role,
and the server coherence of a foreman-authored zone. It needs its own threat
review (Doc 06) and a risk-register entry. Only pursue if the product genuinely
requires field-created zones; otherwise seeding (A) is lower blast-radius.

## Boundaries for the eventual STEP
- Staging only; never touch production data.
- Idempotent seed; re-runnable without duplicating rows.
- No secret/PII output; use the staging service connection documented in the
  env/runbook, never inline credentials.
- Seeding is a schema/data STEP owned separately from STEP-55; STEP-55.11's
  close must cite this STEP's id for the create-zone round-trip evidence.

## Open questions for authoring
1. Seed as a tracked `supabase/seed/*.sql` applied by the E2E workflow, or a
   manual pre-flight runbook step? (Affects whether CI can self-provision.)
2. One shared test zone, or one per journey that needs it (cut/fill, land
   clearing, daily-log all reference zones)?
3. Does the product roadmap want foreman-created zones at all (approach B), or
   is a fixed admin-seeded zone set the intended model?
