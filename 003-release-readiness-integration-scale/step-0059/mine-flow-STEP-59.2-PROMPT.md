# mine-flow — STEP-59.2: Daily Log + Equipment Check Draft Restoration

> **How to run:** "run substep 59.2". Cold-runnable.
> **Assigned model tier: mid** (same bounded pattern as 59.1; daily log's
  hazard/approval contract adds a validation wrinkle — follow the 59.0 design).

## Context

Same implementation pattern for the daily log form (hazard/approval contract, zone
picker state) and equipment check sheet (SOP checklist state). The daily-log form has
a role-aware approval contract from 55.6 — the draft snapshot must not bypass or
pre-fulfill approval/hazard validation; it restores *entry*, not *authorization*.
STEP PLAN: `Upcoming Prompts/mine-flow-STEP-59-PLAN.md`; design:
`Upcoming Prompts/mine-flow-STEP-59.0-FINDINGS.md`.

## Read these first

- 59.0 FINDINGS (design for these two features, incl. any parked ambiguity —
  if the equipment SOP mid-signoff state was parked, implement only the unambiguous
  part and record the parked piece).
- 59.1's landed pattern (commit on the branch) — reuse the snapshot/restore idioms.
- `lib/features/daily_log/` (form + hazard contract) and `lib/features/equipment_check/`.
- 55.6 hazard contract migration + tests (don't regress the approval flow).

## Scope

**Owns:** draft snapshot + restore for both forms (per 59.0 design + any parked notes);
roundtrip/router/fallback tests; findings. Branch `step-0059-os-restoration-forms`.

**Does NOT touch:** hazard/approval validation logic, RLS/sync, other features,
route plumbing.

## Your task

1. Implement per design: daily log draft (work done, conditions, notes, selected zone id,
   hazard fields as *entered* — validation re-runs on restore, never trusts the
   snapshot); equipment check (per 59.0's design; if mid-signoff was parked, snapshot
   only item check states + remarks, and record the parked piece).
2. Tests: roundtrip equality, restartAndRestore per form (URL + sheet + draft survive),
   version-mismatch fallback, hazard-validation-reruns-on-restore case (snapshot with
   an invalid hazard value → restore rejects as fresh input would).
3. Focused suites + analyze + format-on-touched; one lane commit (`59.2`); FINDINGS.

## Verification

Same gates as 59.1 plus: hazard validation provably re-runs post-restore (test);
approval flow untouched (existing 55.6 tests green).

## Definition of done

- [ ] Both forms restore entry (not authorization) across process death, test-proven.
- [ ] All new + existing suites green; analyze clean; lane committed; FINDINGS complete.

## Next

Report to parent. Next: 59.3 (benchmark + inventory + data bucket).
