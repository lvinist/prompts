# mine-flow — STEP-48.12 Findings: Live RLS Evidence

**Date:** 2026-08-30
**Executor:** Gemini 3.1 Pro High
**Branch:** `step-0048-runtime-evidence`

## Accounts and Roles Scope
Based on STEP-48.0 findings:
- Supervisor: `supervisor@mineflow.dev` (`role: supervisor`) exists. `TEST_SUPERVISOR_*` credentials are provided.
- Foreman: `foreman@mineflow.dev` (`role: foreman`) exists. `TEST_FOREMAN_*` credentials are provided.
- Crew: `crew@mineflow.dev` (`role: crew`) exists, but **`TEST_CREW_*` repository secrets are absent**.

**Testable Scope:** The full matrix is **partial**. The supervisor and foreman legs can be verified, as well as the single-user enforcement path. The crew leg cannot be run.

## Verdict
**Verified (Partial).**
Verified: RLS is enforced for roles `supervisor` and `foreman` on tables `zones`, `equipment_checks`, `cut_fill_records`, `land_clearing_records`, `inventory_items`, `geospatial_files`. Reads permitted by policy succeed, and operations forbidden by policy (e.g. foreman `INSERT` into `zones`) are positively refused with a 42501 error.
Unverified: The crew policy paths and cross-role isolation (whether crew can see others' rows), because the `TEST_CREW_*` credentials do not exist in the repository secrets, skipping the crew test leg.

## Refusal Evidence
- **Table:** `zones`
- **Operation:** `INSERT` (`client.from('zones').insert({'name': 'rls-probe-foreman-insert'})`)
- **Role:** `foreman`
- **Exception code/message:** `42501` (`insufficient_privilege`) / "new row violates row-level security policy for table \"zones\""
*(An equivalent refusal was asserted for the anonymous access path when acting as a supervisor).*

## S0 Report Row
**Before:**
```markdown
| Live RLS behavior test (via integration tests) | Unverified (STEP-45.12): test written (`rls_authorization_journey_test.dart`) but skipped because per-role staging credentials (`TEST_FOREMAN_EMAIL`, etc.) were not provided. Cannot verify full matrix (users, zones, attendance_records, etc.) for foreman/supervisor roles. | STEP-45 owner | Test passes when staging credentials are supplied |
```

**After:**
```markdown
| Live RLS behavior test (via integration tests) | Verified (STEP-48.12): test executed (`rls_authorization_journey_test.dart`) against staging. Matrix is partial: supervisor and foreman legs verified with positive assertion of policy refusal (e.g., foreman INSERT into zones refused with 42501). Crew leg unverified because `TEST_CREW_*` credentials are absent. | STEP-48 owner | Test crew leg when crew credentials are supplied |
```

## Security Defects
None found. The assertions correctly expect the `PostgrestException` caused by the database enforcing row-level security policies on denied operations.

## Recommendation for 48.14 (`risks.yml`)
Since the full matrix remains partial, a new deferral risk needs its own row in `risks.yml`.
**Recommendation:** Create a new risk entry (e.g. `RISK-0021`) tracking the unverified `crew` RLS leg and cross-role isolation tests due to absent `TEST_CREW_*` staging credentials.
**Revisit trigger:** "When `TEST_CREW_EMAIL` and `TEST_CREW_PASSWORD` are provisioned in GitHub repository secrets."

## CI Verification
The journey executes in `e2e-web` and `e2e-android`. Test counts: 2 passed (supervisor and foreman matrix, plus single-user path), 1 skipped (crew leg).
Run URL: `https://github.com/lvinist/mine-flow-app/actions/runs/33320708318`
