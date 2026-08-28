# mine-flow — STEP-45.12: Live RLS / authorization E2E against staging

**Recommended model:** Gemini 3.1 Pro (security-sensitive per-role authorization matrix; closes the STEP-44 deferral).

> **How to run:** *"run substep 45.12"*. Self-contained; runnable cold.

## Context

Closes the STEP-44 S0 deferral: the "Live RLS behavior test" was skipped in STEP-44 for lack of
live staging credentials and explicitly assigned to the STEP-45 owner. This substep signs in as each
role and asserts the RLS matrix at runtime. Depends on 45.3. Read
`Upcoming Prompts/mine-flow-STEP-45-PLAN.md` (Q6 — per-role test accounts).

## Read these first
- `Upcoming Prompts/mine-flow-STEP-45-PLAN.md` — Q6.
- `Code/mine-flow-docs/reports/security/2026-08-26-step-0044-s0-security-baseline-report.md` — the
  RLS matrix, the deferred-row it left, and the "Intentionally skipped / Live RLS behavior test" row.
- `Code/mine-flow-app/supabase/migrations/` — the RLS policies (9 tables per S0).
- `Code/mine-flow-docs/architecture/06-security-threat-model.md`, `16-identity-auth.md`.
- STEP-46 findings — CF-001..005 (auth foundation) and CF-024 (Drive-file delete no role gate),
  CF-019..023 (destructive-action role gates) — remediated; this substep confirms authorization at
  the backend (RLS) layer, not just the client gate.

## Scope

Owns `integration_test/journeys/rls_authorization_journey_test.dart` and the update to the S0 report's
deferred RLS row. Does **not** re-run a full security review (that is an S1/S2 STEP, not this one).

## Your task

1. For each role (foreman / supervisor / any others in the matrix), sign in against staging and, for
   the covered tables, assert that read / write / update / delete are **allowed or denied per the S0
   RLS matrix** — real backend responses, not client-side gating.
2. Focus on the risk rows: attribution tables (correct-author enforcement), destructive deletes
   (supervisor-only where the matrix says so), and any cross-tenant/site isolation the matrix asserts.
3. **Update the S0 report:** change the deferred "Live RLS behavior test" row to reflect the live
   result (passed / discrepancies found), citing this STEP.
4. If per-role staging accounts are unavailable (Q6), mark the journey **Unverified**, record exactly
   which roles/tables could not be tested, and leave the S0 deferral open with the reason — do not
   claim RLS is verified.

## Verification
- RLS journey runs per role against staging (or Unverified w/ reason).
- S0 report's deferred RLS row updated with the live outcome.
- `flutter analyze` 0 / format clean. Commit on the STEP-45 branch (test) and docs branch (report).

## Keeping the docs true (always)
- Any RLS discrepancy vs `architecture/06-security-threat-model.md` is a finding → record for 45.15
  and, if a control gap, add/raise a `registries/risks.yml` row.

## Definition of done
- [ ] Per-role RLS matrix verified at runtime against staging, or Unverified with the specific gaps named.
- [ ] STEP-44 S0 deferred RLS row updated with the live result.
- [ ] analyze 0 / format clean; files documented.

## Next
Run substep 45.13 (`go_router` v16→v17 deep-link validation) in a fresh chat.
