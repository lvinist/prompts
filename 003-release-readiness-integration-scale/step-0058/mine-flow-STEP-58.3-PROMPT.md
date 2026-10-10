# mine-flow — STEP-58.3: Upstream PR #206 Recheck + Workspace-Root Hygiene

> **How to run:** "run substep 58.3". Cold-runnable.
> **Assigned model tier: fast** (mechanical checks with clear gates; ambiguity parks).

## Context

Two residual record items: (1) STEP-49's residual says recheck upstream Throughstone
PR #206 at the next check-in (state: open as of 2026-10-10 — re-verify live); (2)
`check.sh` warns on workspace-root debris (DESIGN.md NUL ORIGINAL_REQUEST.md PRODUCT.md
PROJECT.md scratch .agent .agents .gemini .hermes .impeccable .scratch-tmp). Hygiene per
METHOD §7: durable content moves into the docs repo; ambiguous items park for the owner.
STEP PLAN: `Upcoming Prompts/mine-flow-STEP-58-PLAN.md`.

## Read these first

- `prompts/STEP-index.md` STEP-49 row (the residual + fork/PR context).
- `Code/mine-flow-docs/METHOD.md` §7 (workspace hygiene rules).
- `Code/mine-flow-docs/registries/repos.yml` (repo inventory — where content belongs).
- `Upcoming Prompts/.step56-60-overnight-orchestration-state.md` (batch push policy).

## Scope

**Owns:** (a) live PR #206 state fetch + record update (STEP-49 row's residual note or a
dated addendum — the index evidence cell, NOT a status flip); (b) debris classification:
each root item inspected (size, mtime, content head) → move-to-docs-repo / keep-as-
pointer / park-for-owner; (c) hygiene report + FINDINGS.

**Does NOT touch:** app code, the upstream repo itself (no comments/pushes), registries'
risk rows (58.2 owns), anything deleted without owner approval.

## Your task

1. PR #206: fetch state via GitHub API (`repos/mherschberg/Throughstone/pulls/206` —
   state, merged, head sha); record in the STEP-49 index evidence cell as a dated
   addendum note on the docs branch (or prompts trunk if the row edit demands it —
   the index lives in prompts, so: targeted CRLF-safe patch + commit + push, per
   trunk rules).
2. **Concurrent-lane adoption — owner authorized (2026-10-10 ~03:00, Q4):** the docs
   worktree carries a concurrent session's uncommitted hygiene move: 8 deleted
   tracked files under `prompts/phase-2/step-0038/` + untracked
   `reports/archive/step-0038/` and `reports/archive/workspace-root-context/`.
   First re-verify byte-identity: each archived file must equal the deleted tracked
   blob (`git show HEAD:<old-path> | tr -d '\r' | cmp -s - <(tr -d '\r' < <archived>)`
   — or byte-exact if EOLs match) and the workspace-root originals are gone. If
   ANY file differs, park that file and report. If all identical: stage the
   deletions + the archive additions as ONE dedicated commit ATTRIBUTED to the
   concurrent session (message: `docs(hygiene): adopt concurrent session's archive
   move — step-0038 prompts + workspace-root context into reports/archive/ (adopted
   per owner 2026-10-10; content verified byte-identical)`). Do NOT mix it with
   your own 58.3 changes.
3. Debris classification, item by item (owner disposition for the known two, Q3):
   - `DESIGN.md`, `PRODUCT.md` — **owner chose: move into the docs repo under
     `reports/bridge/` AND update `scripts/impeccable-bridge.ps1`'s output path**
     (both files are auto-generated from Doc 07 by that script — the header says so;
     fix the source so regenerations land in the repo). Verify the script's path
     constant, patch it, move the files, commit as your own 58.3 lane.
   - `scratch/`, `.scratch-tmp/` — list contents; classify each child (recent =
     in-flight lane → keep + note; old = park for owner sweep approval).
   - `.agent`, `.agents`, `.gemini`, `.hermes`, `.impeccable` — tool/agent state
     dirs; inspect names/sizes only; typically per-machine pointers (keep, document)
     unless check.sh demands otherwise — record, don't delete.
4. Hygiene report: `Code/mine-flow-docs/reports/2026-10-11-step-0058-workspace-hygiene.md`
   (actual run date), listing per-item disposition + evidence, including the adopted
   concurrent-lane commit sha and the bridge-script change.
5. FINDINGS: PR state + date, adoption commit sha, disposition table, check.sh
   warning delta (before/after).

## Verification

- PR #206 state fetched live (not from memory) with a fetch timestamp.
- Every moved file: `git status` clean post-move in both repos (source gone, destination
  committed); nothing deleted outright.
- `check.sh` re-run: hygiene warning shrunk or each remaining item documented as
  intentional (pointer/tool state).
- CRLF discipline on the prompts index patch; duplicate scan empty.

## Definition of done

- [ ] PR #206 state recorded with fetch date in the index.
- [ ] Debris dispositioned: moved-and-committed / kept-as-pointer / parked-for-owner —
      each with evidence.
- [ ] Hygiene report + FINDINGS complete; check.sh warning delta recorded.

## Next

Report to parent. This is STEP-58's last substep → parent verifies all three, then the
STEP-58 close sequence (index flip, archive, prompts trunk push) runs — subject to the
owner's review policy.
