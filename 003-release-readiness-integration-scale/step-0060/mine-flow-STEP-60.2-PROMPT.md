# mine-flow — STEP-60.2: Risk Verdicts, Register Update & Batch-STEP Close

> **How to run:** "run substep 60.2". Cold-runnable.
> **Assigned model tier: STRONGEST** (the batch's final risk/dependency verdict: a
  mis-stated posture silently corrupts the durable record — honesty is the deliverable).

## Context

Final substep of STEP-60 and of the whole 56–60 batch: write the RISK-0007/0009/0020
verdicts from live evidence, update the register, run the close sequence.
STEP PLAN: `Upcoming Prompts/mine-flow-STEP-60-PLAN.md`;
evidence: `mine-flow-STEP-60.0-FINDINGS.md` + `mine-flow-STEP-60.1-FINDINGS.md`.

## Read these first

- 60.0/60.1 FINDINGS (the evidence base).
- `registries/risks.yml` RISK-0007/0009/0020 (each row's own criteria + revisit
  triggers — the verdict must answer THOSE, in the row's own vocabulary).
- `Upcoming Prompts/.step56-60-overnight-orchestration-state.md` (owner push/merge
  policy + batch state).
- `prompts/STEP-index.md` STEP-60 row + substep table.

## Scope

**Owns:** risks.yml verdict updates (monitoring/kept-open/closed per evidence, each
cited); full-suite run if 60.1 changed deps (+ CI gate at the pushed/owner-approved
head, verdict recorded honestly); Doc 11/12 cross-refs if the dependency posture
description changed; STEP-60 close sequence; batch-end FINDINGS summarizing all five
STEPs' states for the owner's morning review.

**Does NOT touch:** production, ADR decisions (hive_ce keep/migrate stays ADR-0001's
authority — this STEP records status, optionally parks an owner escalation with
evidence), app code beyond nothing (this is verdict/bookkeeping).

## Your task

1. Verdicts, per row, from live evidence: RISK-0007 (hive_ce release cadence vs the
   >6-months trigger → keep-monitoring / escalated-with-evidence), RISK-0009 (stable
   version vs ≥3.48 trigger → not-fired-recorded, or fired → the retest evidence from
   60.1), RISK-0020 (SDK-pinned residuals → unchanged-record). Update status/evidence/
   revisit cells; flip none without criteria met.
2. Full suite + gates (if 60.1 changed deps) with exact counts; CI gate per owner
   policy at the recorded head sha (verify the run exists for THAT sha before reading
   it — the `?head_sha=` precondition).
3. Close sequence for STEP-60: index row + substep table, PLAN flip + checklist,
   archive to `prompts/003-release-readiness-integration-scale/step-0060/`, prompts
   trunk commit + push.
4. **Batch-end record**: a FINDINGS section summarizing the five-STEP batch state —
   each STEP's status (closed / parked-at-gate / open), every owner decision pending
   (57.1 ADR gate, merge/push dispositions, parked hygiene items), and the exact next
   actions for the owner's morning review.

## Verification

- Every register edit cites fetched evidence (version, date, sha, run id).
- Full suite + CI verdicts honest (infra-reds adjudicated, evidence holes named).
- `check.sh` 0 fails; duplicate scan empty; archive verified; prompts trunk pushed.
- The batch-end record's owner-decision list is complete (grep the batch FINDINGS for
  "parked"/"owner" and reconcile against it).

## Definition of done

- [ ] RISK-0007/0009/0020 verdicts recorded with live evidence; register consistent.
- [ ] STEP-60 closed per the standard sequence; batch-end record written.
- [ ] All pending owner decisions enumerated for the morning review.

## Next

Report to parent. The parent delivers the final batch report to the owner: what closed,
what parks at which gate, and the exact list of decisions awaiting the owner.
