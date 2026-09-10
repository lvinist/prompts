# mine-flow — STEP-51.1: Register re-scope & sweep inventory (gate)

> **How to run:** Tell your agent *"run substep 51.1"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.
>
> **Assigned model: Hermes/Claude Opus 4.8.** This is the STEP's honesty gate: it decides
> what the durable record says and where the sweep's boundary sits. A wrong inventory means
> every downstream substep sweeps the wrong set, or the register gets a second false
> "complete" — the exact defect this STEP exists to fix. That failure is silent, so it earns
> the top tier.

## Context

STEP-51 closes UI debt the 2026-09-05 implementation audit
(`Code/mine-flow-docs/reports/2026-09-05-step-45-47-implementation-audit.md` §F-2/§F-3)
proved STEP-46 booked as complete: CF-087 (residual Material widgets) is ~half done, and
STEP-46.4's "add tests for each fix" is largely unfulfilled. Read the PLAN first —
`Upcoming Prompts/mine-flow-STEP-51-PLAN.md` — it holds the verified pre-flight counts and
the locked decisions D1–D7.

This substep produces **no application-code changes**. It makes the durable record tell the
truth and builds the inventory the sweep substeps (51.2–51.8) execute against. It also cuts
the STEP branch and flips the index row — the STEP lifecycle starts here.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-51-PLAN.md` (the whole STEP; decisions D1–D7 are locked)
- Root `.throughstone/local-user.md` (calibrate communication)
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` (Doc 07 — ForUI is the vocabulary)
- `prompts/003-release-readiness-integration-scale/step-0046/mine-flow-STEP-46.3-FINDINGS.md`
  (the findings register — the file you will append to)
- `Code/mine-flow-docs/reports/2026-09-05-step-45-47-implementation-audit.md` §F-2/§F-3, §8
  (the audit that exposed the gap; §8 has the reproducible grep commands)
- `Code/mine-flow-app/README.md` (repo you'll branch in)

## Scope

**Owns:** the STEP-46.3 register appendix; the per-file Material→ForUI sweep inventory; the
46.4 coverage matrix; the dead-file disposition record; cutting `step-0051-ui-debt-closure`
in `mine-flow-app`; flipping the STEP-51 index row to `In progress` and pushing that flip
to `prompts/main`.

**Does NOT touch:** any `lib/` or `test/` code (that is 51.2–51.9's lane); the archived
register body (append only — never rewrite an archived file in place); STEP-46's archived
PLAN/prompts.

## Your task

1. **Cut the branch & flip the index.** In `Code/mine-flow-app` (verify: `master` clean,
   synced with origin, HEAD `64b054a` or newer STEP-50 merge), cut
   `step-0051-ui-debt-closure`. In `prompts/` (on `main`, pulled, clean), set STEP-51's row
   to `In progress`, commit (`STEP-51 In progress`), duplicate-scan
   (`grep -oE '^\|[[:space:]]*STEP-[0-9]+' prompts/STEP-index.md | grep -oE 'STEP-[0-9]+' | sort | uniq -d`
   must be empty), push to origin. If the push is rejected: pull, re-check, retry.
2. **Re-derive the counts yourself — do not trust the PLAN's numbers blindly.** The PLAN's
   pre-flight section has the 2026-09-09 counts; re-run the greps (audit §8) on the branch
   head and reconcile any drift in your findings. Known trap: a naive `SnackBar(` grep reads
   70 because `showSnackBar(` contains it — count `showSnackBar(` and the `SnackBar(` ctor
   separately.
3. **Write the register appendix** (D1). Append to
   `prompts/003-release-readiness-integration-scale/step-0046/mine-flow-STEP-46.3-FINDINGS.md`
   an `## Appendix — STEP-51 re-scope (2026-09-…)` stating: what CF-087 actually delivered
   (dialogs, buttons, tiles, dividers, chips — genuinely zero), what remained at STEP-51
   start (the per-family counts with files/hits), CF-043's residual structural half (two
   comboboxes at `land_clearing_entry_screen.dart:373`/`:486` writing one `record.method`),
   and that STEP-46.4's test tier assignment went ~unexecuted (13 of 97 CF ids cited under
   `test/`, zero `TODO(STEP-46.4)` uses). Commit in `prompts/` — note this is an *archive*
   repo edit: appending to an archived file is the sanctioned exception (appendix, never
   rewrite).
4. **Build the sweep inventory** (D2/D3). A table (in your findings file, not the register)
   of every Material call site in the four families — `SnackBar`/`showSnackBar`, `AppBar`,
   `Scaffold`, `CircularProgressIndicator` — with: file:line, ForUI target (`FToast`/
   `FToaster`, `FHeader` root/nested, `FScaffold`, `FCircularProgress`), and a
   behaviour-change flag per D3 (toasts/dialogs/selects with dismiss/timeout/callback = yes;
   pure container swaps = no). Verify the forui 0.26 equivalents exist in the pub cache
   (`D:/AppDev/.pub-cache/hosted/pub.dev/forui-0.26.0/lib/src/widgets/`) before listing them
   as targets.
5. **Build the 46.4 coverage matrix** (D4). For each of the 84 tiered findings in the
   register (80 "Widget test", 4 other tiers): `covered` (a `test/` file already cites the
   CF id), `will cover` (51.8 should write it — behaviour-carrying), or `not covered +
   one-line reason`. The 13 already-cited ids are your `covered` seed; use
   `grep -roE 'CF-[0-9]+' test --include='*.dart' | cut -d: -f2 | sort -u` to re-derive.
6. **Record the dead-file dispositions** (D6). All 7 candidates
   (`lib/tracking.dart`, `lib/benchmark.dart`, `lib/data_bucket.dart`, `lib/data/data.dart`,
   `lib/domain/domain.dart`, `lib/notification_badge.dart`, `lib/report_type_card.dart`)
   were verified deleted 2026-09-09. Confirm on the branch head, record "deleted by
   48.30" per file, and sweep for any *new* unreferenced `lib/` files (files whose basename
   is imported nowhere) so 51.9 has a bounded list.
7. **Write findings:** `Upcoming Prompts/mine-flow-STEP-51.1-FINDINGS.md` — the inventory,
   coverage matrix, dispositions, count reconciliation vs the PLAN, and any escalations.
   Update the PLAN's progress row for 51.1.

## Verification

- Register appendix exists as an appendix (original body byte-identical: prove with
  `git diff` on `prompts/` showing only added lines at the file's end).
- Inventory total reconciles with your fresh grep counts; every discrepancy vs the PLAN's
  numbers is named and explained.
- Coverage matrix accounts for all 84 tiered findings — the three buckets sum to 84.
- `git -C prompts status` clean after commit+push; duplicate scan empty.
- `flutter analyze` untouched (you changed no code — run it anyway to record the baseline:
  expect 0 issues, and `flutter test` expect **553 passed** at branch head; any deviation
  is a pre-existing condition to record, not yours to fix).

## Keeping the docs true

This substep *is* the docs-true work for the register. If you discover a count the audit
got wrong, record it in findings and the appendix — do not silently "correct" the archived
audit report. No ADR expected (D5). No risks.yml changes unless you find a new accepted
debt item.

## Definition of done

- [ ] Branch `step-0051-ui-debt-closure` cut in `mine-flow-app`; index row `In progress`, pushed.
- [ ] Register appendix appended (append-only proven); CF-087/CF-043/46.4 truth recorded.
- [ ] Sweep inventory complete with ForUI targets and behaviour flags.
- [ ] Coverage matrix complete: 84/84 accounted for.
- [ ] Dead-file dispositions recorded.
- [ ] Findings file written; PLAN progress row updated.

## Next

Tell the user: *"run substep 51.2"* (SnackBar→FToast, Gemini 3.1 Pro) in a **fresh chat** —
or, since 51.3/51.5/51.7/51.8 also depend only on 51.1, name them as parallelizable.
