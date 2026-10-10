# mine-flow — STEP-58.2: Risk-Register Row-by-Row Sweep

> **How to run:** "run substep 58.2". Cold-runnable.
> **Assigned model tier: mid** (evidence-cited status truing; judgment bounded by each
  row's own close criteria — the final risk verdict is owner-reviewed).

## Context

Sweep `registries/risks.yml` row-by-row: every row's status re-derived against disk
evidence (code at HEAD, reports, register criteria). Known stale-open candidate:
RISK-0026 (benchmark sentinel coordinates) — the STEP-index records 55.4 as Done with
projection rejection + tests landed; verify the fix at HEAD and close or keep-open with
cited evidence. Also attempt the PyYAML install so `check.sh`'s registry parse stops
warning. STEP PLAN: `Upcoming Prompts/mine-flow-STEP-58-PLAN.md`.

## Read these first

- `Code/mine-flow-docs/registries/risks.yml` — every row RISK-0001..0030 (read fully).
- `prompts/STEP-index.md` — STEP rows for evidence cross-referencing.
- `Code/mine-flow-app` HEAD state for each fix the rows reference (grep the tree,
  `git log` for fixing commits).
- 58.1's FINDINGS (any doc-level evidence relevant to rows).

## Scope

**Owns:** risks.yml status/evidence truing-up per row (evidence-cited flips only);
sweep report `Code/mine-flow-docs/reports/2026-10-11-step-0058-risk-sweep.md` (name for
the actual run date); PyYAML availability fix; FINDINGS.

**Does NOT touch:** app code, architecture docs (58.1 owns those), risk *policy*
(severity/semitry changes = owner list, not executor edits), production.

## Your task

1. For each row: re-derive `status` against its own `revisit_trigger`/`closed` criteria
   and disk evidence. Classification rubric:
   - fix landed at HEAD + criteria met → flip to closed (cite commit sha + test evidence).
   - criteria NOT met (e.g. production-verification conditions) → keep open/monitoring,
     update evidence cell to current state (e.g. RISK-0025 stays open — production
     blocked by owner; annotate, don't close).
   - stale-open like RISK-0026: verify the 55.4 fix in code (projection rejection tests,
     fallback removal — grep benchmark feature + tests), then close citing the commit.
2. PyYAML: **owner authorized the install (2026-10-10 ~03:00, Q1)** — run
   `pip install pyyaml` (miniconda base) and re-run `check.sh`; the registry parse
   warnings should clear. If the install fails (no network/permissions), record the
   host limitation and do a manual indentation/parse check instead — never claim the
   parse passed without either.
3. Sweep policy — **owner authorized autonomous evidence-cited closes (Q2)**: flip a
   row to `closed` ONLY when the row's OWN close criteria are verifiably met on disk,
   citing commit sha + report path in the `closed:` block. Exempt: RISK-0030 (its CI
   criterion is parked per STEP-57 Q5 — annotate, don't close). Judgment-call rows
   (criteria arguably met but ambiguous) park for the owner. Every kept-open row gets
   its evidence cell trued to current state.
3. Write the sweep report: per-row verdict, evidence, flips made, owner-list of
   policy-level items (severity changes, keep-vs-close judgment calls) parked for review.
   (Numbering note: the two "3./4." blocks above — the earlier item 3 rubric list is part
   of task item 1's classification; keep the sequential order when executing.)
4. FINDINGS with the report path + row counts (rows swept, flipped, kept, parked).

## Verification

- `check.sh` 0 fails; registry YAML parses (PyYAML now available or manual check).
- Every flip has a cited commit/report; no flip cites chat memory.
- `git diff` confined to risks.yml (+ report file); CRLF preserved; `git diff --check`
  clean.

## Definition of done

- [ ] All rows RISK-0001..0030 swept with recorded verdicts; RISK-0026 dispositioned.
- [ ] Sweep report written; owner-parked list explicit.
- [ ] PyYAML state resolved or documented; check.sh clean.

## Next

Report to parent. Next: 58.3 (PR #206 recheck + workspace hygiene).
