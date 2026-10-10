# mine-flow — STEP-61.2 PROMPT: Verification + STEP-61 Close

**Executor:** Hermes subagent (vc/deepseek-v4.1)
**Date authored:** 2026-10-10
**Model assignment:** mid tier (bookkeeping bounded by the PLAN's locked decisions and
61.1's on-disk results; the final close verdict is re-verified parent-side)

## Working style (non-negotiable)

Short replies every turn; write FINDINGS incrementally; never one huge final message.

## Context

Workspace `D:/AppDev/mine_flow` (bash/MSYS; native tools need `D:/`-style paths).
61.1 has completed. Read first, in order:

1. `Upcoming Prompts/mine-flow-STEP-61-PLAN.md` — locked decisions + close protocol.
2. `Upcoming Prompts/mine-flow-STEP-61.1-FINDINGS.md` — what 61.1 landed, commit shas.
3. `Upcoming Prompts/mine-flow-DRAFT-milestone-doc-review-STEP-56-60-FINDINGS.md` —
   the originating review (for the close record's cross-references).

Re-derive 61.1's claims on disk before trusting them: verify each commit exists and
contains what the FINDINGS says (`git show --stat`), each trunk is synced
(`main` == `origin/main`), and the release exists (API read-back).

## Tasks

1. **Gates (run all, record every result):**
   - `bash Code/mine-flow-docs/scripts/check.sh` from workspace root → expect 0 fails;
     record warnings verbatim (pre-existing warnings allowed, document them).
   - Duplicate STEP scan: `grep -oE '^\|[[:space:]]*STEP-[0-9]+' prompts/STEP-index.md |
     grep -oE 'STEP-[0-9]+' | sort | uniq -d` → expect empty.
   - `git diff --check` in all three repos → expect clean.
   - Phase-3 README: CR-byte count == line count (CRLF preserved through the backfill).
   - `git -C Code/mine-flow-app tag -l v1.3.0` exists and points at
     `c4f40302153f992871965a7926eb321182ea0c4c`; remote release read-back: GET
     `/repos/lvinist/mine-flow-app/releases/tags/v1.3.0` (token via
     `git credential fill`, never printed) → record `html_url`, verify body's first
     heading matches `reports/release-notes-v1.3.0-phase-3-completion.md` at docs HEAD.
2. **STEP-61 close bookkeeping (all pre-approved by the owner 2026-10-10):**
   - `prompts/STEP-index.md`: STEP-61 row status **Planned → In progress → Done** —
     write the final Done cell with the close evidence: the five fixes, both repo
     commit shas, release `v1.3.0` URL, gates results. Preserve the row's CRLF
     convention (the index file is LF — verify before/after).
   - Add a `### STEP-61 substeps` table (LF, modeled on the STEP-58 block) with rows
     61.1 (fixes + release) and 61.2 (this close), both Done with evidence.
   - `Upcoming Prompts/mine-flow-STEP-61-PLAN.md`: flip **Status: Planned → Done**
     and tick any checklist items with the actual evidence.
   - Archive move: move `mine-flow-STEP-61-PLAN.md`, `mine-flow-STEP-61.1-PROMPT.md`,
     `mine-flow-STEP-61.2-PROMPT.md`, and the 61.1/61.2 FINDINGS into
     `prompts/003-release-readiness-integration-scale/step-0061/`. After the move,
     re-open the destination files and verify status/paths (stale bytes survive moves).
   - Commit the archive + index flip on `prompts/main`
     (`docs(61.2): STEP-61 closed Done — milestone doc-review remediation applied`),
     `git diff --cached --check`, push (fast-forward only).
3. **FINDINGS:** `Upcoming Prompts/mine-flow-STEP-61.2-FINDINGS.md` — gate results
   table, close record, archive verification, run attribution. Anything not
   re-derivable on disk = **Unverified** with its blocker, never "done".

## Boundaries

- No application code, no `lib/`/`test/` edits, no risk-register edits, no status
  changes to any STEP other than 61.
- Never print or store the GitHub token.
- Do not touch the draft review artifacts' §1–7 content (they are the originating
  record; the archive copies ride along as evidence if the PLAN moves them — they are
  NOT part of step-0061's archive set unless the PLAN says so; leave them in
  `Upcoming Prompts/`).
- Pushes are pre-approved for exactly: `prompts/main` and `docs main` bookkeeping
  commits from 61.1/61.2 and the `v1.3.0` tag. Nothing else.

## End

Reply SHORT: gates pass/fail table, STEP-61 closed Done (with commit shas), release
URL, anything Unverified.
