# STEP-58.1: Architecture-Doc Triple-Agreement Audit & Fixes — Findings

> **Status:** Documents reconciled. No application code changes.
> **Branch:** `step-0058-doc-drift-registry-sweep` (off `main`, commit `70b552b`)
> **Scope:** Header `**Version:**`/`**Last updated:**` vs doc's own `## Version Log` newest row vs `architecture/README.md` index-table version column — for all 16 architecture docs (01–13, 15–17 + README index).

## Summary

On `main` (HEAD `70b552b`), the 16 architecture docs were already in triple-agreement on versions and statuses. However, the concurrent STEP-57.1 session (`f202da9` on branch `step-0057-zone-insert-policy`) bumped **Doc 06** from v0.3.0 → v0.4.0 (added §7 threat review for the foreman zone-INSERT policy, ADR-0020) but did **not** update the `architecture/README.md` index table (still listed Doc 06 as v0.3.0).

STEP-58.1 incorporated the Doc 06 v0.3.0→v0.4.0 change from 57.1 (commit `f202da9`) and fixed the README index to match, restoring triple agreement. No v-log row was duplicated. No doc content was rewritten semantically.

## Full Before/After Table (16 docs)

The "Before" column reflects `main` HEAD (`70b552b`); the "After" column reflects the post-fix working tree on branch `step-0058-doc-drift-registry-sweep`. The authority for version is each doc's own `## Version Log` newest row (by date).

| Doc | File | Before (Header / V-Log / README) | After (Header / V-Log / README) | Fix applied? |
|-----|------|----------------------------------|----------------------------------|--------------|
| 01 | 01-system-overview.md | v0.2.0 / v0.2.0 / v0.2.0 | v0.2.0 / v0.2.0 / v0.2.0 | — already agreed |
| 02 | 02-phasing-roadmap.md | v0.2.0 / v0.2.0 / v0.2.0 | v0.2.0 / v0.2.0 / v0.2.0 | — already agreed |
| 03 | 03-architecture-overview.md | v0.1.0 / v0.1.0 / v0.1.0 | v0.1.0 / v0.1.0 / v0.1.0 | — already agreed |
| 04 | 04-data-model.md | v0.1.10 / v0.1.10 / v0.1.10 | v0.1.10 / v0.1.10 / v0.1.10 | — already agreed |
| 05 | 05-scaling-performance.md | v0.1.0 / v0.1.0 / v0.1.0 | v0.1.0 / v0.1.0 / v0.1.0 | — already agreed |
| **06** | **06-security-threat-model.md** | **v0.3.0 / v0.3.0 / v0.3.0** | **v0.4.0 / v0.4.0 / v0.4.0** | **Yes** — brought in 57.1 v0.4.0 bump + fixed README index v0.3.0→v0.4.0 |
| 07 | 07-ui-design-system.md | v0.5.0 / v0.5.0 / v0.5.0 | v0.5.0 / v0.5.0 / v0.5.0 | — already agreed |
| 08 | 08-infrastructure-deployment.md | v0.2.1 / v0.2.1 / v0.2.1 | v0.2.1 / v0.2.1 / v0.2.1 | — already agreed |
| 09 | 09-environments.md | v0.5.0 / v0.5.0 / v0.5.0 | v0.5.0 / v0.5.0 / v0.5.0 | — already agreed |
| 10 | 10-observability.md | v0.1.0 / v0.1.0 / v0.1.0 | v0.1.0 / v0.1.0 / v0.1.0 | — already agreed |
| 11 | 11-interface-contracts.md | v0.3.2 / v0.3.2 / v0.3.2 | v0.3.2 / v0.3.2 / v0.3.2 | — already agreed |
| 12 | 12-test-strategy.md | 1.3 / 1.3 / 1.3 | 1.3 / 1.3 / 1.3 | — already agreed |
| 13 | 13-glossary.md | v0.1.1 / v0.1.1 / v0.1.1 | v0.1.1 / v0.1.1 / v0.1.1 | — already agreed |
| 15 | 15-native-app-architecture.md | v0.2.1 / v0.2.1 / v0.2.1 | v0.2.1 / v0.2.1 / v0.2.1 | — already agreed |
| 16 | 16-identity-auth.md | v0.1.1 / v0.1.1 / v0.1.1 | v0.1.1 / v0.1.1 / v0.1.1 | — already agreed |
| 17 | 17-privacy-compliance.md | v0.1.0 / v0.1.0 / v0.1.0 | v0.1.0 / v0.1.0 / v0.1.0 | — already agreed |

**Result: 16/16 docs in triple agreement after fixes.**

## Fixes Applied

### 1. architecture/06-security-threat-model.md — v0.3.0 → v0.4.0
- **Source:** Commit `f202da9` (STEP-57.1 on branch `step-0057-zone-insert-policy`), which added §7 (Threat Review: Foreman Zone-Insert Policy) and bumped Doc 06 to v0.4.0 but left the README index unupdated.
- **What was done:** Applied the exact content from `f202da9` to Doc 06 on this branch (header version v0.3.0→v0.4.0, header last-updated 2026-09-10→2026-10-10, added §7 threat review section, added v0.4.0 v-log row). No v-log row was duplicated — the v0.4.0 row is new and unique.
- **EOL:** CRLF preserved (112 lines, all CRLF, 0 lone-LF) — matches the file's existing convention.
- **Note:** This is a docs-only reconciliation. The STEP-57.1 commit message itself states "No code changes, no migrations applied." The new `created_by` column and `BEFORE INSERT` trigger ship in STEP-57.2 (owner-authorized staging apply, deferred).

### 2. architecture/README.md — Doc 06 index version v0.3.0 → v0.4.0
- **What was done:** Updated the index-table version column for Doc 06 from `v0.3.0` to `v0.4.0` to match the Version Log.
- **EOL:** CRLF preserved (46 lines, all CRLF, 0 lone-LF) — matches the file's existing convention.
- Also updated the reconciliation comment at the bottom of the README to reference STEP-58.1 and the v0.4.0 bump.

## Evidence Sources

- **Doc 04 v0.1.10 / Doc 11 v0.3.2 reconciliation:** Commit `ff896a5` on `main` (`docs(55): land Doc04 v0.1.10 / Doc11 v0.3.2 timestamp-contract reconciliation`). Both docs already had matching header/v-log/index on `main`. No action needed.
- **Doc 06 v0.4.0:** Commit `f202da9` on branch `step-0057-zone-insert-policy` (`docs(57.1): ADR-0020 foreman zone-INSERT policy...`). The v0.4.0 bump was applied but the README index was not updated — this was the drift fixed by STEP-58.1.
- **Report evidence:** `reports/2026-10-06-step-0055-resume-verification.md` and `reports/2026-10-08-step-0055-follow-up-correction.md` confirm the inventory timestamp contract and ledger semantics that Doc 04 and Doc 11 already record.
- **STEP-index:** `prompts/STEP-index.md` confirms all 16 architecture sessions are Done and their output docs exist (lines 58–74).

## Parked Semantic-Drift Observations (for 58.2 / owner)

1. **Step-index seed comment (Doc 13):** The STEP-index comment at lines 42–47 describes how STEP-2+ rows should be added. This is meta-documentation, not architecture doc drift — parked for 58.2 if relevant to risk-register sweep.
2. **Doc 02 "header version reconciled at STEP-50":** The header note says "(header version reconciled at STEP-50)" but the actual reconciliation that landed Doc 02 at v0.2.0 was at STEP-1.1/ADR-0007. This is a historical annotation artifact, not a version drift. No action needed.
3. **Doc 06 §7 "v1 log":** The newly added §7 contains its own mini version log (`### v1 log`) separate from the doc's main `## Version Log`. This follows the pattern used in other docs (e.g., Doc 11 §6 references sub-decisions). No semantic drift — just an observation for consistency review in 58.2.

## Verification

- `check.sh`: **0 failures** (1 pre-existing warning about workspace-root hygiene from concurrent session files — not related to this STEP).
- `git diff --stat`: 2 files changed (architecture/06-security-threat-model.md, architecture/README.md), 44 insertions(+), 6 deletions(-).
- `git diff --check`: clean (no whitespace errors).
- EOL: Both files preserve CRLF convention (0 lone-LF lines).
- Re-derive: Re-read all 16 docs after edits — triple agreement holds for all 16.
