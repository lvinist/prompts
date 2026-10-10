# mine-flow — STEP-59.3: Benchmark + Inventory + Data-Bucket Draft Restoration

> **How to run:** "run substep 59.3". Cold-runnable.
> **Assigned model tier: mid** (same pattern; benchmark's projection/CRS recovery and
  data-bucket's Drive-upload adjacency each have a wrinkle — follow 59.0's dispositions).

## Context

Final implementation lane: benchmark form (CRS/projection fields — note 55.4's
projection-rejection contract: a restored draft must re-validate, never restore
sentinel coordinates), inventory form, and data-bucket metadata form (Drive upload
adjacency — if 59.0 parked the half-uploaded-file case, implement the unambiguous
metadata-entry snapshot only and record the parked piece).
STEP PLAN: `Upcoming Prompts/mine-flow-STEP-59-PLAN.md`; design:
`Upcoming Prompts/mine-flow-STEP-59.0-FINDINGS.md`.

## Read these first

- 59.0 FINDINGS (designs + parked dispositions for these three).
- 59.1/59.2 landed patterns (commits on the branch).
- `lib/features/benchmark/` (55.4 projection contract + crs_utils tests),
  `lib/features/inventory/` (or wherever the inventory form lives at HEAD),
  `lib/features/data_bucket/` (Drive upload flow boundary).

## Scope

**Owns:** draft snapshot + restore for the three forms per design; roundtrip/router/
fallback tests (incl. projection re-validation case); findings. Branch
`step-0059-os-restoration-forms`.

**Does NOT touch:** projection/CRS validation logic, Drive upload logic, other
features, route plumbing, migrations.

## Your task

1. Implement per design: benchmark draft (control-point entries re-validated on restore —
   a snapshot containing values that would fail projection must restore to the form and
   fail validation exactly as fresh input); inventory draft; data-bucket metadata draft
   (per 59.0's disposition).
2. Tests: roundtrip equality ×3, restartAndRestore ×3, version-mismatch fallback ×3,
   projection-revalidation case, existing suites green.
3. Format/analyze/gates; one lane commit (`59.3`); FINDINGS.

## Verification

Same gates as 59.1/59.2 plus: projection contract unregressed (55.4 tests green);
no Drive boundary touched (grep diff for drive/upload call sites — zero expected).

## Definition of done

- [ ] All three forms restore drafts, test-proven; parked pieces recorded if any.
- [ ] Suites green; analyze clean; lane committed; FINDINGS complete.

## Next

Report to parent. Next: 59.4 (cross-feature verification, docs, close).
