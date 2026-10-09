# mine-flow — STEP-57.1: Doc 06 Threat Review + ADR for Foreman Zone-INSERT Policy (OWNER GATE)

> **How to run:** "run substep 57.1". Cold-runnable.
> **Assigned model tier: STRONGEST** (security-surface design; honesty of the threat
> analysis is the deliverable).

## Context

The owner chose approach B: grant foremen INSERT on `public.zones` via a new RLS policy so
inline zone creation (CreatableCombobox in daily-log, cut/fill, land clearing, benchmark)
works in the field. This is a security-surface change — who may create zones — and per the
STEP-57 PLAN it requires a Doc 06 threat review and an ADR BEFORE any migration is written.
**The owner pre-answered the design gate on 2026-10-10 (~02:20)** — see
`.step56-60-overnight-orchestration-state.md` §Owner decisions (Q1: site-scoped policy via
`current_user_site_id()` helper; Q2: `created_by` column + server-side BEFORE INSERT
trigger + foreman UPDATE scoped to own rows; Q3: foreman-only; Q4: staging apply
authorized; Q5: run to completion, branches unpushed/unmerged). This substep therefore
writes the threat review and the ADR **recording those answers as the accepted decision**
(ADR status: Accepted, citing the owner decision block + date) and does NOT stop — 57.2
follows the same night. The threat review must still be written honestly: analyze the
approved design's residual risks, don't rubber-stamp.
STEP PLAN: `Upcoming Prompts/mine-flow-STEP-57-PLAN.md`.

## Read these first

- `Code/mine-flow-docs/architecture/06-security-threat-model.md` — the threat model.
- `Code/mine-flow-docs/architecture/04-data-model.md` — zones table + relationships.
- `supabase/migrations/20260718000002_rls_policies.sql` — existing policy inventory
  (supervisor_zones_all, zones_read_active; `current_user_role()` helper).
- `Code/mine-flow-docs/templates/adr-template.md`; `adr/README.md` (next free ADR number).
- `registries/risks.yml` RISK-0030, RISK-0021 (crew RLS precedent), RISK-0025 (prod-blocked).
- `lib/features/daily_log/presentation/widgets/zone_picker.dart` +
  `lib/features/zone/` — the product surface that creates zones client-side.
- Offline sync queue behavior for zones (`zones_update` sync items) — grep the sync
  registrar for the zones lane.

## Scope

**Owns:** (a) threat review section added to Doc 06 (v-log bump); (b) ADR draft
(expected ADR-0020 — verify next free number) proposing the policy with options; (c) new
risk-register entry (or RISK-0030 amendment) for the residual risk the policy accepts;
(d) FINDINGS. Docs repo branch `step-0057-zone-insert-policy`.

**Does NOT touch:** app code, migrations, pubspec, `STEP-index.md` status cells. No SQL
lands in this substep — the ADR may quote a *proposed* policy body as a design artifact.

## Your task

1. **Enumerate the surface:** every caller that can create a zone client-side
   (grep `CreatableCombobox` + zone repository create paths); who authenticates as
   foreman; what fields a client-created zone carries (id? uuid-gen, site_id, name,
   category, description, created_by?).
2. **Threat review (Doc 06 section):** for each scenario — zone spam/unbounded growth,
   cross-site injection (site_id spoofing), category abuse, name collisions, soft-delete
   coherence, offline-queue replay duplication, privilege interplay with
   `supervisor_zones_all` (FOR ALL can shadow INSERT policies — analyze policy
   evaluation order explicitly).
3. **ADR** with the policy proposal. **The owner pre-answered the three questions on
   2026-10-10 (~02:20)** — write the ADR as **Accepted**, citing the decision block in
   `.step56-60-overnight-orchestration-state.md` §Owner decisions as the acceptance
   authority (record the date). The locked answers:
   - Q1 WITH CHECK scope: **site-scoped** — new `current_user_site_id()` helper
     (SECURITY DEFINER, mirrors `current_user_role()`), policy `FOR INSERT TO
     authenticated WITH CHECK (public.current_user_role() = 'foreman' AND site_id =
     public.current_user_site_id())`.
   - Q2 upsert/UPDATE: **`created_by UUID` column added to zones + BEFORE INSERT
     trigger setting `created_by = auth.uid()` server-side (unspoofable) + foreman
     UPDATE policy scoped to own rows (`created_by = auth.uid()`)** — required because
     the offline sync upserts (`INSERT .. ON CONFLICT DO UPDATE`) and needs UPDATE
     privilege too; this also gives the audit trail and stops foremen overwriting
     supervisor-created zones.
   - Q3 crew: **foreman-only**; crew stays read-only.
   The ADR must still document the considered alternatives (role-only policy, broad
   UPDATE, app-side insert-only sync change) and why the chosen shape wins. Do not
   invent answers for anything else the ADR template asks — mark those as noted
   consequences of the locked design.
4. **Risk register:** add/annotate the residual-risk row (e.g. "foreman-created zones
   unmoderated" — severity, revisit trigger = supervisor review UX if ever demanded).
5. FINDINGS: evidence, options table, the three Q dispositions, parked-owner-gate status.

## Verification

Docs-only (no code): `check.sh` 0 fails; ADR number non-duplicate against `adr/README.md`
registry (check.sh covers it); Doc 06 v-log bumped with a "no code change" note;
`git diff --check` clean; CRLF preserved on touched files.

## Definition of done

- [ ] Doc 06 threat-review section + v-log bump; ADR written **Accepted** (owner
      pre-answered 2026-10-10; cite the decision block); risk row added/annotated;
      FINDINGS complete.
- [ ] No migration/SQL applied; no app changes.
- [ ] Record states the design is owner-locked (not executor-inferred).

## Next

Report to parent. Next: 57.2 (migration implementation + staging apply — the owner
pre-authorized the staging apply, Q4) runs immediately after parent verification.
