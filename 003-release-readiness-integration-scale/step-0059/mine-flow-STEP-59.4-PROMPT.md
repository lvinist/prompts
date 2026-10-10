# mine-flow — STEP-59.4: Cross-Feature Verification, Docs & Close

> **How to run:** "run substep 59.4". Cold-runnable.
> **Assigned model tier: STRONGEST** (the final verdict: restoration claims must be
  verified at the real surfaces, and the close record must be honest about what is
  and isn't proven).

## Context

STEP-59's final substep: run the full verification matrix across all restored forms,
reconcile docs, and run the STEP-close sequence per owner push policy.
STEP PLAN: `Upcoming Prompts/mine-flow-STEP-59-PLAN.md`.

## Read these first

- All 59.x FINDINGS files (the evidence base).
- `architecture/12-test-strategy.md` (final gate tiers) + Doc 15/03 for the docs delta.
- `Upcoming Prompts/.step56-60-overnight-orchestration-state.md` (push/merge policy).
- `prompts/STEP-index.md` STEP-59 row + substep table (twin-table rule).

## Scope

**Owns:** full-suite + gates run at the branch head; restoration matrix summary
(feature × roundtrip/fallback/reload verdicts); Doc 15 (or Doc 03) restoration section
update + v-log bump; index/PLAN/archive close sequence; findings/close record.

**Does NOT touch:** product code (verification only — a red here routes back to the
owning 59.x lane, it is not fixed here), migrations, production.

## Your task

1. Full gates at head: `flutter test` (full suite), `flutter analyze`, format check
   (touched files), l10n + contract guards. Record exact counts.
2. Restoration matrix: re-run the per-feature restartAndRestore roundtrips as one
   focused matrix; verify no feature's claims rest on the `getRestorationData`
   harness-artifact pattern.
3. Docs: update the native-app-architecture (or overview) restoration description to
   the all-forms reality (v-log bump; "code change: restoration extended, see STEP-59").
4. Close sequence: index row + substep table (valid status words only), PLAN flip +
   checklist, archive to `prompts/003-release-readiness-integration-scale/step-0059/`,
   prompts trunk commit + push, app/docs branch disposition per owner policy
   (local until owner review; CI gate at the owner-approved push, verdict recorded).
5. FINDINGS/close record: every sha, test count, matrix, parked items.

## Verification

- Full suite green (or honestly adjudicated with cited reproduction); matrix complete
  for all 7 surfaces (or parked-ambiguous recorded per the 59.0 dispositions).
- `check.sh` 0 fails; duplicate scan empty; archive verified (file count + status).
- No verdict cites a child self-report without parent-side re-verification.

## Definition of done

- [ ] Full gates recorded; restoration matrix 7/7 dispositioned.
- [ ] Docs reconciled with v-log; index/PLAN/archive consistent; prompts trunk pushed.
- [ ] Close record written; branch disposition recorded per owner policy.

## Next

Report to parent. STEP-59 closes; parent reports batch status to the owner.
