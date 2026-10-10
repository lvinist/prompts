# mine-flow — STEP-58.1: Architecture-Doc Triple-Agreement Audit & Fixes

> **How to run:** "run substep 58.1". Cold-runnable.
> **Assigned model tier: mid** (mechanical reconciliation across 16 docs with a fixed
  rubric; bounded by written authority).

## Context

After the STEP-48..55 arc, architecture docs can drift three ways at once: the doc
header's `**Version:**`/`**Last updated:**`, the doc's own `## Version Log` newest row,
and `architecture/README.md`'s index-table version column. The header is not authority —
the Version Log is. This substep reconciles all 16 docs to that rule.
STEP PLAN: `Upcoming Prompts/mine-flow-STEP-58-PLAN.md`.

## Read these first

- `Code/mine-flow-docs/architecture/README.md` (index table, version column).
- Every `architecture/*.md` header + `## Version Log` (16 docs: 01–13, 15–17 + README).
- STEP-index evidence cells for STEP-48..55 (what each doc should reflect).
- The 2026-10-06/08 reports (`step-0055-resume-verification`, `close-addendum`,
  `follow-up-correction`) for Doc 04/11 timestamp-contract and Doc 06/07 deltas.

## Scope

**Owns:** for each of the 16 architecture docs: compare header vs Version-Log newest
row vs README index column; fix the two non-authority places to match the authority
(Version Log). If the Version Log itself is missing a row for a change that landed (e.g.
Doc 04 v0.1.10 / Doc 11 v0.3.2 timestamp-contract reconciliation at `ff896a5`), add the
v-log row from the commit/report evidence and then align header + index. Branch
`step-0058-doc-drift-registry-sweep` (docs repo).

**Does NOT touch:** doc *content* beyond the header/v-log/index reconciliation (no
semantic rewrites — those are findings, parked); ADRs; registries; app code.

## Your task

1. Build a three-column table for all 16 docs: header version/date, v-log newest row,
   README index version. (Scripted extraction is fine; verify EOL preservation.)
2. For each disagreement: the Version Log's newest row is current truth — fix header +
   README column to match. If content changed without a v-log row, derive the row from
   the STEP-index/report evidence (cite the source report + commit), then align.
3. Pure reconciliation edits record "docs-only reconciliation, no code change" in the
   v-log note.
4. FINDINGS: the full table (before/after), every fix with file+reason, and parked
   semantic-drift observations (if any) for the owner/STEP-58.2.

## Verification

- `check.sh` 0 fails (its required-fields pass is necessary but NOT sufficient — the
  triple agreement is this substep's own gate).
- `git diff --stat` shows only header/v-log/README-index line changes; `git diff --check`
  clean; CRLF preserved per file (CR counts before/after).
- Re-derive: re-read all 16 after edits — triple agreement holds.

## Definition of done

- [ ] 16/16 docs triple-agreement green, recorded in FINDINGS table.
- [ ] Fixes committed on the STEP branch (single lane commit); nothing semantic changed.
- [ ] Parked observations listed for 58.2.

## Next

Report to parent. Next: 58.2 (risk-register sweep) after parent verification.
