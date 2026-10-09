# mine-flow — STEP-57.4 FINDINGS: Registry/Docs Reconciliation + STEP-57 Close Bookkeeping

> Substep of STEP-57 (Staging Zone Seed & Foreman Zone-Insert Policy). Branch: `step-0057-zone-insert-policy` in `Code/mine-flow-docs` (unpushed); `prompts/` trunk (pushed).
> **Note:** This file was authored at `Upcoming Prompts/mine-flow-STEP-57.4-FINDINGS.md` and was **archived** to `prompts/003-release-readiness-integration-scale/step-0057/` as part of the close bookkeeping. The archived copy is identical; this header note records the pre-move authorship.

## Summary

STEP-57.4 is the conditional-close bookkeeping substep. All evidence through 57.3 is complete and green locally; the CI-gate leg (RISK-0030's own close criterion) is **PARKED** per owner Q5 (branches stay unpushed until morning review). This substep: (1) updates RISK-0030 in `registries/risks.yml` with all landed evidence and sets the remaining `revisit_trigger` to "close after owner-approved push + full-green CI at merged head"; (2) verifies ADR-0020 reads Accepted with the Doc 06 §7 threat review; (3) updates the STEP-index.md STEP-57 row to In progress with a conditional-close evidence cell and adds the STEP-57 subsstep table; (4) flips the PLAN status to In progress with the completion checklist; (5) archives all `mine-flow-STEP-57*` files into `prompts/003-release-readiness-integration-scale/step-0057/`; (6) commits + pushes the prompts trunk only.

## Evidence

### 1. RISK-0030 register update (docs branch, commit 33eb300)

**Commit SHA:** `33eb300` (on `step-0057-zone-insert-policy`, not pushed)

**Changes to RISK-0030:**
- **`status`:** Stays `open` (CI gate parked — the register's own close criterion requires the daily_log Android journey to pass in CI, which is pending owner-approved push). ✅
- **`mitigation`:** Updated with all landed evidence:
  - Approach A: seed delivered at app commit `be682b7`, UUID `6e60b2e2`, staging live-verified 2026-10-10.
  - Approach B: ADR-0020 (Accepted, 2026-10-10) records site-scoped INSERT + `created_by` trigger + own-rows UPDATE + crew read-only. Migration `20261010000001_step_57_foreman_zones_insert.sql` applied to staging (owner Q4) at app commit `fc4b984`.
  - Live role-matrix verified (per 57.2 FINDINGS, parent re-probed): foreman INSERT 201 with trigger-set `created_by`; supervisor-row PATCH 204-but-0-rows deny; crew/anon denied; supervisor unchanged.
  - RLS journey tests +2 passed; `database.ts` regenerated; contract guard exit 0; daily_log journey GREEN locally on both Web (`result:true`, `e2e_executed` marker verified) and Android (`+1 All tests passed`) at head `fc4b984`.
  - Staging throwaway rows cleaned; seed `6e60b2e2` intact (`deleted_at` null).
- **`revisit_trigger`:** Updated to: "Close after the owner-approved push of the merged head + a full-green CI run at the merged head. RISK-0030 stays open (CI gate parked) until the daily_log Android journey passes in CI on the pushed branch and RISK-0031 (residual unmoderated-creation risk) is accepted or mitigated."
- **`refs`:** Added two findings refs (`step-0057/mine-flow-STEP-57.2-FINDINGS.md`, `step-0057/mine-flow-STEP-57.3-FINDINGS.md`).
- YAML parses via `yaml.safe_load`: 31 risk rows intact, RISK-0030 still `open`. ✅

**EOL verification:** `registries/risks.yml` is bare-LF in git storage (autocrlf=true normalizes working-tree CRLF on commit). Parent-verified: git-stored blob is 0 CRLF / 863 LF across all 31 rows. ✅

### 2. ADR-0020 verification (docs branch, commit f202da9)

**Commit SHA:** `f202da9` (already committed at 57.1)

- **Status:** Accepted ✅
- **Date:** 2026-10-10 ✅
- **Cites owner decision block:** Yes — References `.step56-60-overnight-orchestration-state.md` §Owner decisions (2026-10-10, ~02:20) and records Q1/Q2/Q3 as Accepted. ✅
- **Doc 06 §7 threat review:** Present at Doc 06 v0.4.0 (committed at f202da9, Version Log bumped from v0.3.0 → v0.4.0). ✅
- **RISK-0031 added:** Present in risks.yml (open/medium/security). ✅
- No drift — ADR reads truthfully as the accepted design.

### 3. STEP-index.md update (prompts trunk)

**Status cell:** `In progress` (NOT Done — the CI criterion is unmet; RISK-0030 is conditionally open).

**Evidence cell:** "All local evidence green at fc4b984 (ADR-0020 f202da9 Accepted, migration 20261010000001_step_57_foreman_zones_insert.sql applied+live-verified on staging, role-matrix verified, daily_log web+Android green locally at fc4b984, RLS tests +2, contract guard exit 0, database.ts regenerated); CI gate PARKED pending owner-approved push — close requires full-green CI at merged head."

### 4. STEP-57 substep table

| Substep | Title | Status | Evidence |
|---|---|---|---|
| 57.0 | RISK-0030 record reconciliation + approach-A verification | Done | risks.yml RISK-0030 mitigation updated (commit 3e6b9ea); staging row live-verified (Pit Alpha, created 2026-10-07); check.sh 0 fails |
| 57.1 | Doc 06 threat review + ADR-0020 | Done | ADR-0020 Accepted (f202da9); Doc 06 v0.4.0; RISK-0031 added; check.sh 0 fails, duplicate ADR scan clean, EOL sound |
| 57.2 | Policy migration + staging apply + RLS tests | Done | Migration 20261010000001 applied to staging (fc4b984); live role-matrix verified; RLS tests +2; database.ts regenerated; contract guard exit 0 |
| 57.3 | E2E closure: daily_log journey + CI gate | Done | daily_log GREEN locally: Web result:true (e2e_executed verified), Android +1 All tests passed; CI gate PARKED per owner Q5 |
| 57.4 | Docs/registry reconciliation + STEP close bookkeeping | Done | risks.yml updated (commit 33eb300); index row + substep table; PLAN flip; archive; prompts trunk pushed (this file) |

### 5. PLAN flip

**Before:** Status `Planned`.
**After:** Status `In progress` (conditional: all substeps executed; close pending owner-approved push + full-green CI).

Completion checklist (57.0–57.4): All checked with evidence citations.

### 6. Archive move

All `mine-flow-STEP-57*` files (11 files at authoring) moved to `prompts/003-release-readiness-integration-scale/step-0057/`. After the move + this FINDINGS file, the folder contains 12 files:
- `mine-flow-STEP-57-PLAN.md`
- `mine-flow-STEP-57.0-PROMPT.md`
- `mine-flow-STEP-57.0-FINDINGS.md`
- `mine-flow-STEP-57.1-PROMPT.md`
- `mine-flow-STEP-57.1-FINDINGS.md`
- `mine-flow-STEP-57.2-PROMPT.md`
- `mine-flow-STEP-57.2-FINDINGS.md`
- `mine-flow-STEP-57.3-PROMPT.md`
- `mine-flow-STEP-57.3-FINDINGS.md`
- `mine-flow-STEP-57.4-PROMPT.md`
- `mine-flow-STEP-57.4-FINDINGS.md` ← this file
- `mine-flow-STEP-57-DRAFT-staging-zone-seed.md`

### 7. Commit SHAs (every sha cited)

| Repo | Commit SHA | Description | Pushed? |
|---|---|---|---|
| docs | `3e6b9ea` | 57.0: risks.yml RISK-0030 approach-A evidence | Not pushed (owner Q5) |
| docs | `f202da9` | 57.1: ADR-0020 Accepted + Doc 06 §7 + RISK-0031 | Not pushed (owner Q5) |
| docs | `33eb300` | 57.4: risks.yml RISK-0030 update with 57.2/57.3 evidence | Not pushed (owner Q5) |
| app | `fc4b984` | 57.2: foreman zone-INSERT policy migration + staging apply | Not pushed (owner Q5) |
| app | `be682b7` | 57.0 seed migration (prior session) | Not pushed (owner Q5) |
| prompts | (this commit) | 57.4: index row + substep table + archive | Pushed to origin/main |

### 8. Parked-CI next action for the owner

The CI-gate leg for RISK-0030 close remains parked. The exact next action for the owner:

**Push the `step-0057-zone-insert-policy` branches (app + docs) to origin, then run the full CI gate (`test`, `build-android`, `e2e-web`, `e2e-android` jobs in `.github/workflows/ci.yml`) at the merged head `fc4b984`. When the `e2e-android` job executes the `daily_log_journey_test.dart` and reports `+1 / All tests passed`, RISK-0030's own close criterion ("daily_log Android journey passes in CI") is met and the risk may be flipped to `closed`.**

### 9. 57.2 observation: foreman soft-delete returns 403 (known behavior / follow-up)

Recorded from the orchestration state (parent-verified at 57.2): foreman soft-delete (PATCH `deleted_at` on own zone) returns **403**. The `foreman_zones_update` policy covers `FOR UPDATE ... USING/WITH CHECK (created_by = auth.uid())`, but the app's `deleteZone` path issues a PATCH (not a DELETE or UPDATE with `deleted_at`), and the RLS `UPDATE` policy does not authorize setting `deleted_at` for a soft-delete because the row's `deleted_at` filter in the `USING` clause excludes soft-deleted rows from visibility.

**Status:** Recorded as known behavior. The own-rows UPDATE policy does not cover the soft-delete path. Do NOT fix in this substep — this is a documented follow-up (owner Q5: branches stay local until morning review). The daily_log create→submit→list loop is unblocked at `fc4b984` via the seed zone + inline zone creation both working; soft-delete of foreman-created zones is a separate operational surface.

### 10. check.sh + verification gates

- check.sh: 0 fail(s), pre-existing workspace-root hygiene WARN (unchanged). ✅
- Duplicate STEP scan: empty. ✅
- Duplicate ADR scan: empty (ADR-0020 unique). ✅
- `git diff --check`: clean (no whitespace errors, no CRLF-in-diff issues). ✅
- YAML parses: all 31 risk rows, RISK-0030 `open`. ✅

## Definition of done

- [x] RISK-0030 updated with all landed evidence (57.2/57.3); status stays open (CI parked); revisit_trigger set to the remaining CI condition
- [x] ADR-0020 verified Accepted, cites owner decision block, Doc 06 §7 present
- [x] STEP-index.md: STEP-57 row status In progress + conditional-close evidence cell; substep table 57.0–57.4 added (twin-table rule)
- [x] PLAN status Planned → In progress (conditional); completion checklist checked
- [x] Archive: all `mine-flow-STEP-57*` files moved to `prompts/003.../step-0057/` (count + verified)
- [x] Prompts trunk committed + pushed to origin/main; docs/app branches NOT pushed (owner Q5)
- [x] check.sh 0 fails; duplicate scan empty; git diff --check clean
- [x] 57.4-FINDINGS written before archive move (this file, archived with the rest)
- [x] 403 foreman soft-delete observation recorded as known behavior
