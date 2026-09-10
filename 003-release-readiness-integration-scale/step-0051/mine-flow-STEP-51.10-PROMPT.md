# mine-flow — STEP-51.10: Verification & close

> **How to run:** Tell your agent *"run substep 51.10"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.
>
> **Assigned model: Hermes/Claude Opus 4.8.** The closing substep judges whether the debt
> is actually closed, writes the durable record, and gives the gate verdict. It must be
> willing to leave rows open rather than declare victory — a judgement call about honesty
> that is itself the deliverable, and a wrong "Done" here reproduces STEP-46's defect.

## Context

STEP-51 closes CF-087's Material remainder, CF-043's structural half, and STEP-46.4's test
debt. Substeps 51.1–51.9 are Done (verify each from its findings file and the PLAN's
progress table — not from chat history). This substep runs the full verification, re-checks
Doc 07 conformance, finalizes the register appendix, and closes the STEP.

Read the PLAN (`Upcoming Prompts/mine-flow-STEP-51-PLAN.md`) in full — its Definition of
Done is your checklist. Then each `Upcoming Prompts/mine-flow-STEP-51.M-FINDINGS.md`.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-51-PLAN.md` (definition of done = your checklist)
- All `Upcoming Prompts/mine-flow-STEP-51.M-FINDINGS.md` (M = 1..9)
- Root `.throughstone/local-user.md`
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` (conformance re-check)
- `Code/mine-flow-docs/architecture/12-test-strategy.md`
- `Code/mine-flow-docs/reports/2026-09-05-step-45-47-implementation-audit.md` (the debt's
  origin — your close record references it)
- `prompts/003-release-readiness-integration-scale/step-0046/mine-flow-STEP-46.3-FINDINGS.md`
  (the register + 51.1's appendix)
- `Code/mine-flow-app/README.md`

## Scope

**Owns:** the full local gate run; the branch-head CI gate; Doc 07 conformance re-check;
finalizing the register appendix; the STEP-index row + substep table; archiving the STEP
files; merge/push/close per the project's commit lane.

**Does NOT touch:** application code except to fix a gate failure attributable to STEP-51's
own changes (a pre-existing failure is recorded and routed, not absorbed).

## Your task

1. **Verify every PLAN Definition-of-Done item from disk.** Each checklist item: evidence
   or it didn't happen. Where a substep claimed a count, re-derive it (the four family
   greps, the CF-id citation count, the Material-import inventory). Discrepancies between
   findings and disk are *your* findings to write — a substep's claim is not evidence.
2. **Full local gates:** `flutter analyze` (0), `dart format --set-exit-if-changed` (clean),
   l10n guard, contract guard, `flutter test` full suite (state count + delta vs the 553
   baseline; adjudicate any order-dependent flake per the known Hive flake procedure —
   isolated re-run before classifying).
3. **Branch-head CI gate:** push the branch head if not pushed; confirm a run exists for
   the exact sha (`/actions/runs?head_sha=<sha>` — `"total_count": 0` means nothing to
   read, do not improvise a verdict); all four jobs (`test`, `build-android`, `e2e-web`,
   `e2e-android`) green **with non-zero executed counts** (STEP-47's lesson: a green job
   whose tests all skipped is an evidence hole, not a pass). A Material→ForUI swap changes
   finders — expect E2E sensitivity; a journey failure caused by a finder/semantics change
   is STEP-51's to fix, not to waive.
4. **Doc 07 conformance re-check:** spot-check the migrated surfaces against Doc 07's
   patterns (toast host, header usage, scaffold usage). Confirm D5 held: no family needed a
   Material exception without an ADR — or, if one did, that the ADR exists and the appendix
   documents it.
5. **Finalize the register appendix:** fold in 51.8's per-finding reasons and 51.9's
   dispositions so the STEP-46.3 register appendix is complete: CF-087 delivered/remaining
   → now-closed state; CF-043 closed; 46.4 coverage matrix outcome (cited count before/
   after; every tiered finding covered or reason'd).
6. **Close the STEP:** commit any residue (per-substep lanes already committed their own
   work — do not create a mixed wave commit; see the PLAN's ground rules), merge
   `step-0051-ui-debt-closure` to `master` in `mine-flow-app` (app → docs → prompts order),
   update `prompts/STEP-index.md` (STEP-51 `Done` + substep table + owner-model string in
   the STEP-47/49 format), gather all STEP-51 files from `Upcoming Prompts/` into
   `prompts/003-release-readiness-integration-scale/step-0051/`, add the phase README row,
   duplicate-scan, push. Delete the step branch after merge.
7. **Write the close record:** `Upcoming Prompts/mine-flow-STEP-51.10-FINDINGS.md` →
   archived with the STEP; it cites the CI run URL, the test count, the grep zeros, the
   citation delta, and names anything **not** delivered (an honest close leaves rows open
   rather than claiming them).

## Verification

- Every PLAN Definition-of-Done checkbox satisfied **from disk evidence**, or explicitly
  marked not-delivered with a reason and a follow-up owner.
- CI run URL cited; all four jobs green with non-zero executed counts.
- Register appendix complete; index row `Done` with substep table; STEP archived; duplicate
  scan empty; `prompts/main` pushed.
- Workspace root: only the STEP's own files were in `Upcoming Prompts/`; nothing else
  disturbed.

## Keeping the docs true

This substep *is* the docs-true pass for STEP-51. If any checklist item cannot be honestly
ticked, the STEP stays `In progress` with the gap named — tell the user and stop. A
phantom close is the one failure this project's history (STEP-46) already taught.

## Definition of done

- [ ] All PLAN checkboxes verified from disk or honestly marked not-delivered.
- [ ] Local gates green with counts stated; CI gate green with non-zero executions, run URL cited.
- [ ] Register appendix final; CF-087/CF-043/46.4 ledger closed or explicitly residual.
- [ ] STEP-51 `Done` in index with substep table; files archived to
      `prompts/003-release-readiness-integration-scale/step-0051/`; phase README row.
- [ ] Branch merged & deleted; `prompts/main` pushed; duplicate scan empty.
- [ ] Close record written; user told the next action (next `Planned` STEP: **STEP-52**,
      Security Baseline re-check) and to start a **fresh chat**.

## Next

Per METHOD.md §10: report the next action — *"start STEP-52 (Security Baseline re-check)"*
in a fresh chat — and note the check-in cadence (next check-in ~STEP-60–70).
