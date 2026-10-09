# mine-flow — STEP-57 PLAN: Staging Zone Seed Closure & Foreman Zone-Insert Policy (RISK-0030)

**Phase:** Phase 3 — Release Readiness, Integration & Scale (post-milestone follow-up lane)
**Owner:** Hermes (frontier orchestration; subagents execute, parent verifies)
**Status:** In progress
**Date:** 2026-10-10
**Branch:** `step-0057-zone-insert-policy` (app + docs repos)
**Repos (projection):** `mine-flow-app`, `mine-flow-docs`, `prompts`

> Close RISK-0030 both ways. Approach A (idempotent staging seed) is ALREADY DELIVERED:
> migration `supabase/migrations/20261008000001_step_56_staging_zone_seed.sql` committed at
> `be682b7` on master (2026-10-08, prior session, pre-reservation naming) and live-verified
> on staging 2026-10-10 (row `6e60b2e2-0000-4000-8000-000000005656` "Pit Alpha", created
> 2026-10-07). This STEP reconciles that record, then delivers approach B — the foreman
> zone-INSERT RLS policy the owner chose 2026-10-10 — as a properly threat-reviewed
> security-surface change, and closes the daily-log E2E loop with CI evidence.

## Motivation

RISK-0030: foreman INSERT into `public.zones` is refused by RLS (42501), so the inline
zone CreatableCombobox path in daily-log (and cut/fill, land clearing, benchmark) can never
complete a staging round-trip; the queued sync item fails and the dependent insert hits
`daily_logs_zone_id_fkey` (23503). The seed unblocks the E2E journey's FK target, but the
product path (foreman creating a zone inline) stays broken until a policy exists. The
owner chose BOTH: seed (A, done) AND foreman INSERT policy (B, this STEP's core).

## Decisions already locked

- **Owner 2026-10-10:** pursue approach A (seed — delivered) AND approach B (foreman INSERT
  policy). B requires a Doc 06 threat review + risk-register entry before implementation.
- **Owner 2026-10-10 (batch policy):** park lane + FINDINGS + continue on failure;
  pushes to origin allowed for prompts trunk only; app/docs STEP branches stay local
  until owner review.
- The seed migration filename says `step_56` — it predates tonight's reservation and is
  landed applied history. **Never rename, rewrite, or duplicate it.** New migrations use
  `step_57` naming (`202610…000001_step_57_…`).
- Applied migrations are immutable history — the policy ships as a NEW migration.
- `registries/risks.yml` RISK-0030: close only after authorization defined, migration
  landed, and the daily_log Android journey passes in CI.
- ADR-0001…0019 exist; the new decision gets the next free number (verify against
  `adr/README.md` at authoring time — expect ADR-0020).
- Standing boundaries: no `.env` value printing; staging only (production blocked,
  RISK-0025); no PII in artifacts.

## Substeps

| # | Title | Produces | Depends on | Open questions |
|---|-------|----------|------------|----------------|
| 57.0 | RISK-0030 record reconciliation + approach-A verification | Updated risks.yml (A delivered, evidence); FINDINGS | — | none |
| 57.1 | Doc 06 threat review + ADR for foreman zone-INSERT policy | ADR-0020 (draft→owner gate); Doc 06 v-log bump; risk-register entry | 57.0 | policy shape details (see Q1–Q3) |
| 57.2 | Policy migration + staging apply + RLS tests | Migration `…step_57_foreman_zones_insert.sql`; applied+live-verified staging; RLS tests green | 57.1 owner approval | none |
| 57.3 | E2E closure: daily_log journey + CI gate | Green daily_log journeys (web+Android) at branch head; RISK-0030 close evidence | 57.2 | none |
| 57.4 | Docs/registry reconciliation + STEP close bookkeeping | risks.yml RISK-0030 closed; interface-contract/ADR cross-refs; index flip; archive | 57.3 | none |

**Open questions resolved at 57.1 owner gate (2026-10-10 ~02:20, per `.step56-60-overnight-orchestration-state.md`):**
|- Q1 Scope of WITH CHECK: **site-scoped** — `WITH CHECK (site_id = current_user_site_id())` (new SECURITY DEFINER helper mirroring `current_user_role()`). |
|- Q2 Zone-creation hygiene: **`created_by UUID` column + server-side `BEFORE INSERT` trigger (`auth.uid()`, unspoofable) + foreman UPDATE scope to own rows (`created_by = auth.uid()`)**. |
|- Q3 Scope: **foreman-only** (crew stays read-only). |

> NOTE: Owner Q5 (2026-10-10 ~02:20) superseded the original park-gate — the owner authorized running STEP-57 to completion overnight, with ADR written Accepted citing the decision block. Q5 also parks the CI-gate leg: branches stay unpushed until morning review; RISK-0030 closes only after full-green CI at the merged head.

## Test plan

| Test tier / surface | Substep(s) | Tests | Run timing | Command / gate |
|---------------------|------------|-------|------------|----------------|
| Security / authorization (RLS) | 57.2 | Extend `integration_test/journeys/rls_authorization_journey_test.dart` (or its unit-tier sibling) for foreman INSERT allow/deny + supervisor unaffected | per substep | focused RLS suite |
| Migration / data | 57.2 | Idempotency re-run of policy migration; live staging read-back probe (REST) | per substep | curl probe, 0 error |
| End-to-end | 57.3 | `daily_log_journey_test.dart` web + Android (seeded zone path + inline-create path) | final verification | local runs + full CI gate |
| Contract | 57.2 | `tool/check_supabase_contracts.dart` | per substep | exit 0 |

## Ground rules

- Same orchestration model as STEP-56 (parent verifies everything; child summaries never
  trusted alone). Tier assignments per prompt header.
- 57.1 output is an owner gate: the ADR draft + policy shape parks for owner approval
  BEFORE 57.2 implements. If running unattended, STOP after 57.1 and park (this is the
  batch's built-in owner decision point — do not infer Q1–Q3 defaults).
- Android E2E pre-flight: check `adb devices`, relaunch emulator if dead (SDK
  platform-tools adb), serialize device runs; use `.step55.11i-run-android.sh` runner.
- Line-ending discipline for docs/registry YAML edits (CRLF-convention files — targeted
  patches only, verify CR counts).

## Definition of done

- [x] 57.0: risks.yml reflects approach A delivered (evidence-cited) — DONE (docs commit 3e6b9ea)
- [x] 57.1: ADR-0020 accepted (owner-approved), Doc 06 updated with v-log bump — DONE (docs commit f202da9)
- [x] 57.2: Policy migration applied on staging + live-verified; RLS tests green — DONE (app commit fc4b984)
- [x] 57.3: daily_log journey green web+Android locally at head fc4b984; CI gate PARKED per owner Q5 — DONE (local evidence only)
- [x] 57.4: RISK-0030 updated with 57.2/57.3 evidence + revisit_trigger; index row In progress + conditional-close evidence cell; substep table added; PLAN flipped; archive moved; prompts trunk pushed — DONE (docs commit 33eb300; this close record)
- [x] Index + substep table + PLAN + archive reconciled and consistent
- [x] Prompts trunk pushed; app/docs branch disposition recorded per owner policy (unpushed)
- [x] RISK-0030 stays open (CI gate parked); close record written with every sha cited

> **Conditional close posture:** All local evidence is green at fc4b984. RISK-0030 remains `open` (CI gate parked per owner Q5). Close requires the owner-approved push of the merged head + a full-green CI run at the merged head (e2e-android job executing `daily_log_journey_test.dart`).
