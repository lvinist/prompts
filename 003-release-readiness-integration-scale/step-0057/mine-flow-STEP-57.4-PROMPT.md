# mine-flow — STEP-57.4: Registry/Docs Reconciliation + STEP-57 Close Bookkeeping

> **How to run:** "run substep 57.4". Cold-runnable.
> **Assigned model tier: mid** (bookkeeping bounded by the register's own close criteria;
  the close verdict cites only verified evidence).

## Context

Final substep: close RISK-0030 per its own register criteria (authorization defined ✓
ADR; migration landed ✓ 57.2; daily_log Android journey passes in CI ✓ 57.3), reconcile
docs, and run the STEP-close sequence. STEP PLAN: `Upcoming Prompts/mine-flow-STEP-57-PLAN.md`.

## Read these first

- `Code/mine-flow-docs/registries/risks.yml` RISK-0030 (close criteria) + the residual
  policy-risk row from 57.1.
- All `Upcoming Prompts/mine-flow-STEP-57.*-FINDINGS.md` — the evidence the close cites.
- `Code/mine-flow-docs/architecture/06-security-threat-model.md` + the ADR (57.1).
- `prompts/STEP-index.md` STEP-57 row + `### STEP-57 substeps` table (both need the
  outcome; editing the index touches TWO summaries — see the twin-table pitfall).
- `Upcoming Prompts/.step56-60-overnight-orchestration-state.md` — owner push policy.

## Scope

**Owns:** risks.yml RISK-0030 close (status/`closed:` block with date+reason+evidence),
ADR flip to Accepted (owner-gated — see task), Doc 06/04 cross-refs if needed, index
row + substep-table update, PLAN status/checklist flip, archive move into
`prompts/003-release-readiness-integration-scale/step-0057/`, merge/branch-delete per
owner policy, FINDINGS.

**Does NOT touch:** production, applied migrations, app code.

## Your task

1. RISK-0030 disposition — **owner Q5 makes the CI-gate leg conditional:** the register's
   own close criteria require the daily_log Android journey to "pass in CI". Local
   evidence is complete (57.3) but CI is parked pending the owner-approved push.
   Therefore: update the row with all landed evidence (ADR id, migration filename+sha,
   local journey results) and set `revisit_trigger` to the remaining condition
   ("close after the owner-approved push + full-green CI run at the merged head") —
   do NOT flip to `closed` unless a full-green CI run exists; if it does (owner pushed
   between sessions), close with the run id cited.
2. ADR state: Accepted (owner pre-answered 2026-10-10; 57.1 wrote it so) — verify it
   reads that way and cites the decision block; fix only if it drifted.
3. Index: STEP-57 row status cell + evidence cell (valid values only:
   Planned/In progress/Done/Deferred/Abandoned/N/A), substep table rows 57.0–57.4
   statuses + evidence. Then `./check.sh` + duplicate scan.
4. PLAN header status flip + completion checklist; archive
   `Upcoming Prompts/mine-flow-STEP-57*` → `prompts/003-release-readiness-integration-scale/step-0057/`
   (preserve filenames; verify moved-in files' final status/artifact count after the move).
   **If RISK-0030 could not close (CI parked), the STEP records a conditional close:
   index row Done with the evidence cell naming the parked CI push explicitly.**
5. Merge per owner policy: app/docs branches merge to trunks and delete ONLY on owner
   approval (batch policy: branches stay local; the owner decides merge timing at the
   morning review). Prompts trunk commits (index + archive) DO push to origin.
6. FINDINGS + close record with every commit sha.

## Verification

- `check.sh` 0 fails; duplicate scan empty; `git diff --check` clean pre-commit.
- Archive: folder contains PLAN + 5 prompts + 6 findings files (count + verify).
- risks.yml parses; closed block complete; no evidence cell cites an Unverified claim
  as Done.
- Branch/merge state matches the owner policy recorded in the orchestration state file.

## Definition of done

- [ ] RISK-0030 closed with criteria-mapped evidence; ADR state truthful.
- [ ] Index + substep table + PLAN + archive all reconciled and consistent.
- [ ] Prompts trunk pushed; app/docs branch disposition recorded per owner policy.
- [ ] Close record written with every sha cited.

## Next

Report to parent. STEP-57 closes; the parent reports batch status to the owner.
