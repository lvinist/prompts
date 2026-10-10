# mine-flow — STEP-61.1 PROMPT: Apply All Five Doc-Review Fixes + GitHub Release Tag

**Executor:** Hermes subagent (vc/deepseek-v4.1)
**Date authored:** 2026-10-10
**Model assignment:** mid tier (mechanical edits bounded by written authority — the owner
decisions are locked in the PLAN; do not re-ask any question, do not widen scope)

## Working style (non-negotiable)

Short replies every turn; verify-then-edit file by file; commit per repo only after its
read-back passes. Never compose one huge final message.

## Context

You know nothing else — trust this prompt plus what you verify on disk. Workspace:
`D:/AppDev/mine_flow` (Windows; bash/MSYS shell; native tools need `D:/`-style
forward-slash paths, never `/d/...`). Three repos, all currently clean and synced:
`prompts/` (main @ `575fcbc`), `Code/mine-flow-docs` (main @ `798a752`),
`Code/mine-flow-app` (master @ `c4f4030` — read-only for this STEP, no code changes).

Read first: `Upcoming Prompts/mine-flow-STEP-61-PLAN.md` (authority: locked decisions),
`Upcoming Prompts/mine-flow-DRAFT-milestone-doc-review-STEP-56-60-FINDINGS.md`
(evidence per finding, incl. §7 parent addendum).

All five fixes below were **owner-approved 2026-10-10** — apply exactly this scope,
nothing more, nothing less. If a fact on disk contradicts a claim (e.g. a "stranded"
file is missing), record the discrepancy in FINDINGS and skip that item — never invent.

## Fixes to apply (in this order)

### Fix 1 (C1) — Phase-3 README backfill, in `prompts/` repo

File: `prompts/003-release-readiness-integration-scale/README.md` — **CRLF convention
file** (verify with `tr -cd '\r' < file | wc -c` == line count before AND after).
Append five rows to the STEP table, matching the existing 4-column shape
(`| STEP-N | Title | Substeps | Date |`), before the trailing
`<!-- Add a row when a STEP's folder is moved into this phase on completion. -->`:

- STEP-56 | Phase-3 Close-Out: Release Notes & User-Facing Docs | 56.1..56.2 | 2026-10-10
- STEP-57 | Staging Zone Seed & Foreman Zone-Insert Policy | 57.0..57.4 | 2026-10-10
- STEP-58 | Doc-Drift Reconciliation, Risk-Register Sweep & Workspace Hygiene | 58.1..58.3 | 2026-10-10
- STEP-59 | OS Process-Death Restoration for All Form Features (FC-54.5-013) | 59.0..59.4 | 2026-10-10
- STEP-60 | Dependency & Security Maintenance Sweep | 60.0..60.2 | 2026-10-10

(Substep ranges are to be read back from the `### STEP-N substeps` tables and archive
folders in `prompts/STEP-index.md` — trust those over this list if they differ; record
any mismatch in FINDINGS.)

### Fix 2 (C5/S4) — Complete STEP-60 archival, in `prompts/` repo

1. Move (not copy) the three files from `Upcoming Prompts/` into
   `prompts/003-release-readiness-integration-scale/step-0060/`:
   `mine-flow-STEP-60.0-PROMPT.md`, `mine-flow-STEP-60.1-PROMPT.md`,
   `mine-flow-STEP-60.2-PROMPT.md`.
2. Add a `### STEP-60 substeps` table to `prompts/STEP-index.md` near the other STEP-5x
   substep tables (LF convention), modeled on the STEP-58 block:

```
### STEP-60 substeps

> PLAN: `prompts/003-release-readiness-integration-scale/step-0060/mine-flow-STEP-60-PLAN.md` (archived).
> Work on branch `step-0060-dependency-security-sweep` in `mine-flow-app` and `mine-flow-docs`; `prompts/` trunk for bookkeeping.
> Closed 2026-10-10 (owner-approved merge): merged at `c4f4030`; CI run 38058477936 ALL-GREEN.

| # | Title | Status | Evidence / deliverables |
|---|---|---|---|
| 60.0 | Dependency inventory + advisory scan | Done | `pub outdated` snapshot (17 direct, 63 transitive); no advisories; read-only at `4c74e87` |
| 60.1 | Bounded compatibility/lockfile work | Done | 19 safe in-constraint upgrades (13 direct + 6 co-upgrades); hive_ce 2.19.3→2.20.2 (lockfile-only within ^2.19.3, owner 60-Q4); forui ^0.26 pin kept (owner 60-Q5); pubspec.yaml untouched |
| 60.2 | Risk verdicts + register update + close | Done | RISK-0007/0009/0020 verdicts evidence-cited (docs `798a752`); merged at `c4f4030`; CI 38058477936 ALL-GREEN; STEP closed |
```

3. Verify the step-0060 archive folder now holds 7 files (PLAN, FINDINGS, 60.0/60.1
   FINDINGS, 60.0/60.1/60.2 PROMPTS) and `Upcoming Prompts/` no longer holds the
   60.x PROMPT files.
4. Sweep the remaining STEP-60 scratch copies: `mine-flow-STEP-60-PLAN.md`,
   `mine-flow-STEP-60-FINDINGS.md`, `mine-flow-STEP-60.0-FINDINGS.md`,
   `mine-flow-STEP-60.1-FINDINGS.md` in `Upcoming Prompts/` are byte-identical
   (verified by `cmp` in the review) to the archived copies — **delete them** (archive
   is the record; scratch is swept after archival, per the STEP-58.3 hygiene
   convention). Before deleting each, re-run `cmp` against the archived copy and
   record the identical verdict; if any differs, do NOT delete it — record the
   divergence in FINDINGS instead.

### Fix 3 (C3) — Trim the stale STEP-58 evidence cell, in `prompts/` repo

In `prompts/STEP-index.md` STEP-58 row: delete the sentence
`Branch step-0058-doc-drift-registry-sweep local, unpushed (owner review gates merge).`
and replace with
`(merged to docs `main` at `2a88aa0`, owner-approved 2026-10-10; branch deleted).`
Re-read the row first and preserve its exact CRLF convention (verify CR count).

### Fix 4 (C2 + C4) — Docs repo edits, on `Code/mine-flow-docs` main

4a. `reports/release-notes-v1.3.0-phase-3-completion.md` (CRLF — preserve):
- **Known Issues:** remove the now-resolved lines: (a) the RISK-0030 foreman zone
  creation / "Assigned to STEP-57" line, (b) the "OS restoration beyond attendance
  pending (STEP-59)" line, (c) the "Seeded-zone round-trip (STEP-56 lane)" fragment
  inside the last line (keep RISK-0025 production rollout + production migration in
  that line — they are genuinely open). Keep RISK-0025 and RISK-0031 lines.
- **References:** replace `STEP-41 through STEP-55` with `STEP-41 through STEP-60`;
  update "Related STEPs" to name STEP-56..60; set "Released version/tag" to
  `v1.3.0 (GitHub release on mine-flow-app, tagged at c4f4030)`;
  set "Released tag" line accordingly; keep CI run `37949922909` for the STEP-55
  close but add the batch close runs: STEP-57 `38030561898` (at `63deed7`), STEP-59
  `38049230677` (at `4c74e87`), STEP-60 `38058477936` (at `c4f4030`).
- **Documentation section:** update the last line to say user-facing doc
  reconciliation completed via STEP-56.2 and this review (STEP-61) tightened the
  record.

4b. `overview.md` (C4): at lines ~69 and ~71, change the parenthetical labels
`(Phase 2: integrate with survey tools.)` → `(Phase 3: integrate with survey tools.)`
and `(Phase 2.)` → `(Phase 3.)` for the multi-site deferral. Re-read the file first;
if the exact strings moved, re-locate by content (grep "Phase 2"). Also check line ~31
("deferred to multi-site phase") needs no change — it does not name a phase number.
Preserve the file's EOL convention (check CR bytes before/after).

### Fix 5 (C2) — GitHub release `v1.3.0`, on `lvinist/mine-flow-app`

After the docs commit (4a) exists:
1. `cd D:/AppDev/mine_flow/Code/mine-flow-app` — create tag `v1.3.0` (annotated,
   message "mine-flow v1.3.0 — Phase 3 Completion") at
   `c4f40302153f992871965a7926eb321182ea0c4c` and push it:
   `git tag -a v1.3.0 c4f4030 -m "..." && git push origin v1.3.0`.
2. Create the GitHub release via API with token from
   `GCM_INTERACTIVE=never GIT_TERMINAL_PROMPT=0 printf 'protocol=https\nhost=github.com\n\n' | git credential fill`
   (extract `password=`; NEVER print it, never write it anywhere):
   `POST /repos/lvinist/mine-flow-app/releases` with
   `{"tag_name":"v1.3.0","target_commitish":"c4f40302153f992871965a7926eb321182ea0c4c","name":"v1.3.0 — Phase 3 Completion","body":<release-notes file content>,"draft":false,"prerelease":false}`.
3. **Read-back:** GET the release; record `html_url`, verify `tag_name`, and verify the
   body matches the committed file (compare first/last lines; full compare via
   `cmp` of the file against a re-fetched body is ideal).

## Commit / push protocol

- `prompts/` repo: commit fixes 1–3 (may be one commit; message
  `docs(61.1): apply milestone doc-review remediation — README backfill 56..60, STEP-58 cell trim, STEP-60 archival completion`).
  Push `main` (fast-forward only; if rejected, pull --ff-only and retry).
- `docs` repo: commit fix 4 (message
  `docs(61.1): release-notes known-issues/References true-up + overview Phase-2→3 terminology (milestone doc review C2/C4)`).
  Push `main` (fast-forward only).
- Before each commit: `git diff --check`; staged set contains ONLY the files this substep
  owns. After each push: verify `main` == `origin/main`.
- Do NOT touch the app repo's code, branches, or anything beyond the tag; do NOT
  modify `Code/mine-flow-app` working tree files.

## Output

Append/produce FINDINGS: `Upcoming Prompts/mine-flow-STEP-61.1-FINDINGS.md` —
per fix: what changed (files, line counts), read-back evidence (CRLF counts, cmp,
API read-back with release URL), commit shas + push state. Mark anything you could not
verify as **Unverified** with its blocker. End with a SHORT summary: fix count, commit
shas, release URL, any discrepancies.
