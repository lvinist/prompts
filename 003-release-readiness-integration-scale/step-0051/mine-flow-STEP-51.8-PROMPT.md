# mine-flow — STEP-51.8: STEP-46.4 regression coverage (the test debt)

> **How to run:** Tell your agent *"run substep 51.8"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.
>
> **Assigned model: Gemini 3.1 Pro High.** Test authoring against a 97-finding register:
> the judgement is which findings carry behaviour worth pinning and what each assertion
> should prove — bounded by 51.1's coverage matrix, but the assertion quality is the
> deliverable.

## Context

STEP-46.4's prompt said "add tests for each fix" with a `// TODO(STEP-46.4)` escape hatch.
Reality (2026-09-09 re-verification): only **13 of 97** CF ids are cited under `test/`
(23 more under `integration_test/`), the STEP-46 merge added ~8 net cases and zero test
files, and the escape hatch was used zero times. The fixes are real but unguarded — the
next refactor can silently undo any of them. This substep writes the missing regression
coverage per decision D4: **behaviour-carrying findings get tests; every uncovered finding
gets an explicit one-line reason** (the discipline the original hatch was for).

**Your work list is 51.1's coverage matrix** (`Upcoming Prompts/mine-flow-STEP-51.1-FINDINGS.md`):
for each of the 84 tiered findings it marks `will cover` or `not covered + reason`. Do not
re-derive the triage; execute it — and if you believe a matrix row is wrong, say so in
findings and act on your better judgement, noting the deviation.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-51-PLAN.md` (decision D4, ground rules)
- `Upcoming Prompts/mine-flow-STEP-51.1-FINDINGS.md` (**the coverage matrix — your work
  list**)
- Root `.throughstone/local-user.md`
- `prompts/003-release-readiness-integration-scale/step-0046/mine-flow-STEP-46.3-FINDINGS.md`
  (the register — each finding's description and tier)
- `Code/mine-flow-docs/architecture/12-test-strategy.md`
- Existing citation patterns: `grep -rn "CF-" test --include='*.dart'` (13 ids — follow
  this comment convention)
- `Code/mine-flow-app/README.md`

## Scope

**Owns:** new/updated `test/` files covering the `will-cover` findings; the per-finding
reason list for anything left uncovered.

**Does NOT touch:** `lib/` code except where a test exposes a genuine STEP-46 fix that
regressed (if you find one, that's a **finding to report**, and a fix only if small and
obviously in-scope — otherwise escalate); `integration_test/` (its 23 cited ids count as
covered already); the register body (51.10 finalizes the appendix).

## Your task

1. **For each `will cover` finding in the matrix:** write a widget/unit test that pins the
   behaviour STEP-46's fix established. Each test carries a `// CF-0NN` comment naming its
   finding — the citation count is the metric this substep exists to move (from 13 to a
   defensible number). Co-locate tests per the existing layout under `test/`.
2. **For each `not covered` finding:** confirm or write its one-line reason (e.g.
   "pure styling, no assertable behaviour", "covered by integration_test journey X").
   These go in your findings file, consolidated for 51.10 to fold into the register
   appendix.
3. **Quality bar:** a test that merely pumps a widget and calls `expect(findsWidgets)`
   proves nothing — each test must assert the behaviour the finding describes (the
   dialog opens, the constrained value rejects, the sorted order holds, …). If you cannot
   write an assertion that would fail if the STEP-46 fix were reverted, that finding
   belongs in `not covered` with that reason, not in a vacuous test.
4. **Known traps** (inherited): `tester.binding.setSurfaceSize` rather than assuming
   768px; target `find.byType(EditableText)` not `TextField` (flutter/flutter#191095 under
   forui 0.26); scope form finders to the screen, not `.at(0)`.

## Verification

- `flutter test` full suite → green; state count and delta (expect a meaningful rise from
  the 51.x running count).
- Citation count re-derived: `grep -roE 'CF-[0-9]+' test --include='*.dart' | cut -d: -f2 | sort -u | wc -l`
  — report the before/after.
- Matrix accounting: every `will cover` row has a passing test; every `not covered` row
  has a reason. The two buckets plus `covered` (pre-existing 13 + integration 23) account
  for all 84 tiered findings.
- `flutter analyze` → 0; `dart format --set-exit-if-changed` → clean.

## Keeping the docs true

Your findings consolidate the per-finding reasons — 51.10 folds them into the register
appendix. Any discovered *regression* of a STEP-46 fix is a findings-level report first.

## Definition of done

- [ ] Every `will cover` finding pinned by a CF-id-citing test that would fail on revert.
- [ ] Every `not covered` finding carries a one-line reason.
- [ ] Full `flutter test` green; count, delta, and citation before/after stated.
- [ ] `flutter analyze` 0, format clean.
- [ ] Findings `Upcoming Prompts/mine-flow-STEP-51.8-FINDINGS.md`; PLAN row updated.

## Escalation (to Opus 4.8 — record in findings if fired)

- A test that exposes a live regression of a STEP-46 fix (fix vs flag is not yours alone).
- A finding whose behaviour you cannot pin without changing `lib/` code.
- Matrix rows you believe are mis-triaged (deviate, but record it).
- Same test failing twice after apparently correct fixes.

## Next

Tell the user the next open substep (51.9 if not done, else 51.10). In a **fresh chat**.
