# mine-flow — STEP-58 PLAN: Doc-Drift Reconciliation, Risk-Register Sweep & Workspace Hygiene

**Phase:** Phase 3 — Release Readiness, Integration & Scale (post-milestone follow-up lane)
**Owner:** Hermes (frontier orchestration; subagents execute, parent verifies)
**Status:** Done
**Date:** 2026-10-10
**Branch:** `step-0058-doc-drift-registry-sweep` (docs repo; prompts trunk commits)
**Repos (projection):** `mine-flow-docs`, `prompts`

> Reconcile the durable state records after the Phase-3 close: architecture-doc
> header/Version-Log/README-index triple agreement, risk-register row-by-row
> status-vs-evidence sweep (incl. the known stale-open RISK-0026), the upstream
> Throughstone PR #206 recheck, and workspace-root hygiene. Review-and-verification
> only — no application code.

## Motivation

The STEP-48..55 arc moved fast; several state records lag: the index says 55.4 landed
benchmark projection rejection (Done) while risks.yml RISK-0026 still reads open; doc
headers can drift from their own Version Logs and the hub README index (the three-place
agreement rule); check.sh reports workspace-root debris (DESIGN.md NUL ORIGINAL_REQUEST.md
PRODUCT.md PROJECT.md scratch .agent .agents .gemini .hermes .impeccable .scratch-tmp) and
PyYAML absence blocks registry parsing checks; upstream PR #206 is still open (recheck
due at next check-in per STEP-49's residual). None of these are product defects — they're
record-truth defects that cheapen every future session's disk-state trust.

## Decisions already locked

- No application code in this STEP; docs hub + prompts only.
- Registry YAML edits preserve CRLF/EOL convention; targeted patches; `check.sh` after.
- ADRs are superseded, never rewritten.
- The l10n guard's `lib/core/presentation/` blind spot is a known record — do not widen
  guard scope here (owner decision, separate lane).
- Disposition of workspace-root debris follows METHOD §7: durable content moves into the
  docs repo; per-machine pointers and `Upcoming Prompts/` stay. Files are classified
  before moving — `.hermes`, `.agent`, `.gemini`, `.agents` are agent/tool state, likely
  keep-or-relocate-as-pointers, not docs content. When classification is ambiguous, park
  and list for the owner rather than delete.

## Substeps

| # | Title | Produces | Depends on | Open questions |
|---|-------|----------|------------|----------------|
| 58.1 | Architecture-doc triple-agreement audit + fixes | Per-doc header/v-log/README-index reconciliation (16 docs); fixes committed | — | none |
| 58.2 | Risk-register row-by-row sweep | risks.yml evidence-cited status trues-up (incl. RISK-0026); PyYAML install attempt; sweep report | 58.1 | disposition of monitor-status rows = owner review list |
| 58.3 | Upstream PR #206 recheck + workspace hygiene | PR state recorded; debris classified/moved/parked; hygiene report | — | none (park ambiguous items) |

## Test plan

No code — mechanical gates only: `check.sh` 0 fails; `git diff --check` clean; EOL
preserved per file; duplicate STEP scan empty; registry YAML parses (after PyYAML install
attempt, or by manual indentation check).

## Ground rules

- Orchestration model as STEP-56/57 (subagents execute, parent verifies parent-side).
- Every register flip cites evidence (commit sha / report path); no flip from prose
  memory. Stale-open rows whose fix landed cross-STEP get the fixing commit cited.
- STEP-49's residual "recheck PR #206 at next check-in" is satisfied by 58.3 (record
  state: open as of 2026-10-10 — re-verify live at execution time).
- Hygiene moves are reversible (git); nothing is deleted without an owner-parked list.

## Definition of done

- [ ] All 16 architecture docs pass triple agreement; fixes committed with v-log notes
      ("no code change" where applicable).
- [ ] risks.yml rows verified against disk evidence; RISK-0026 dispositioned (closed or
      evidence-cited kept-open); sweep report written.
- [ ] PR #206 state recorded with fetch date; debris dispositioned or parked.
- [ ] `check.sh` 0 fails (warnings allowed if pre-existing/document); STEP archived.
