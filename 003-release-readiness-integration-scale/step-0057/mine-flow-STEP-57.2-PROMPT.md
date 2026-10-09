# mine-flow — STEP-57.2: Foreman Zones-INSERT Policy Migration + Staging Apply + RLS Tests

> **How to run:** "run substep 57.2". Cold-runnable.
> **Assigned model tier: STRONGEST** (authorization change; silent failure corrupts the
> security posture — the policy must be proven deny-by-default elsewhere).
>
> **PRECONDITION — SATISFIED:** the owner pre-approved the design on 2026-10-10
> (~02:20) and pre-authorized the staging apply (Q4): see
> `.step56-60-overnight-orchestration-state.md` §Owner decisions. The 57.1 ADR records
> the acceptance. Implement exactly the locked design (site-scoped INSERT policy +
> `created_by` column + trigger + own-rows UPDATE policy). If the ADR is missing or
> contradicts the locked design, STOP and report the discrepancy.

## Context

Implements the owner-approved foreman zone-INSERT RLS policy as a new migration, applies
it to staging, and pins authorization tests. STEP PLAN:
`Upcoming Prompts/mine-flow-STEP-57-PLAN.md`. Authority: the approved ADR (57.1).

## Read these first

- The approved ADR (57.1 output; `adr/` in docs hub).
- `supabase/migrations/20260718000002_rls_policies.sql` + `20260718000001_core_schema.sql`
  (zones columns; `current_user_role()` definition).
- `tool/check_supabase_contracts.dart` + `supabase/types/database.ts` conventions.
- `integration_test/journeys/rls_authorization_journey_test.dart` — existing RLS E2E.
- `Upcoming Prompts/mine-flow-STEP-57.0-FINDINGS.md` — staging seed state.

## Scope

**Owns:** migration `supabase/migrations/20261011000001_step_57_foreman_zones_insert.sql`
(or next free date-prefixed number — verify), staging apply, RLS tests, contract guard
run, `database.ts` regen if columns/typing change, findings. App repo branch
`step-0057-zone-insert-policy`; docs repo same-name branch for any doc deltas.

**Does NOT touch:** production (blocked, RISK-0025), existing applied migrations,
product UI code (the CreatableCombobox already issues inserts), other features.

## Your task

1. Write the migration implementing EXACTLY the owner-locked design (57.1 ADR):
   - `ALTER TABLE public.zones ADD COLUMN IF NOT EXISTS created_by UUID;`
   - `CREATE OR REPLACE FUNCTION public.current_user_site_id()` — SECURITY DEFINER,
     mirrors `current_user_role()` (SELECT site_id FROM public.users WHERE id =
     auth.uid() AND deleted_at IS NULL).
   - BEFORE INSERT trigger on zones setting `created_by = auth.uid()` server-side
     (unspoofable; leave NULL-safe for system inserts if any — follow the ADR).
   - `CREATE POLICY foreman_zones_insert ON public.zones FOR INSERT TO authenticated
     WITH CHECK (public.current_user_role() = 'foreman' AND site_id =
     public.current_user_site_id());`
   - `CREATE POLICY foreman_zones_update_own ON public.zones FOR UPDATE TO
     authenticated USING (public.current_user_role() = 'foreman' AND created_by =
     auth.uid()) WITH CHECK (same);` — required because the offline sync upserts
     (INSERT..ON CONFLICT DO UPDATE) need UPDATE privilege.
   - Guard first: assert no existing policy name collides (`CREATE POLICY` fails
     loudly on duplicate — intended).
2. Apply to staging: `supabase db push --linked` — **owner-pre-authorized (Q4)**.
   Staging ref/creds from `.env` (SUPABASE_PROJECT_REF etc. — never print values).
   If the apply fails on auth/conflicts, park per failure policy and record Unverified.
3. Live-verify the role matrix (owner-pre-authorized): foreman test user INSERT
   succeeds (throwaway zone with unique marker name; note `created_by` gets set by the
   trigger — verify it equals the foreman's id); foreman UPDATE of OWN row succeeds /
   UPDATE of a supervisor-created row DENIED (the own-rows scope — this is the new
   matrix leg vs the original prompt); crew INSERT denied (42501); anonymous denied;
   supervisor behavior unchanged. Probe via REST with each role's staging creds;
   record status codes only, never values.
4. Tests: extend the RLS journey (or unit-tier RLS suite) with foreman-allow /
   crew-deny / supervisor-unaffected / anon-deny cases; run focused suite + full
   `flutter analyze` + `tool/check_supabase_contracts.dart` (exit 0).
5. `database.ts` regen only if the schema shape changed (policy-only → usually no);
   if regenerated, it must be the reviewed-typegen path (guard snapshot validation).
6. FINDINGS: migration path + sha, apply evidence, probe codes, test counts, gates.

## Verification

- Migration file committed on branch; `git status` shows only owned files.
- Live probes: foreman INSERT 201/created; crew 42501; anon 42501; supervisor
  pre-existing behavior unchanged.
- Focused RLS suite green; `flutter analyze` 0; contract guard exit 0.
- No production endpoint touched; no secrets printed.

## Definition of done

- [ ] Migration on branch + applied to staging + live-verified role matrix.
- [ ] RLS tests green; gates green; findings complete with role-matrix evidence.
- [ ] Committed (branch only, not pushed); parked for owner review per batch policy.

## Next

Report to parent. Next: 57.3 (E2E closure + CI gate) once the parent verifies 57.2.
