# mine-flow — STEP-49.5: Push fork, open upstream PR, close STEP-49

> **How to run:** Tell your agent *"run substep 49.5"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.

**Assigned model: Hermes (top tier — Claude Opus 4.8 or equivalent).** This is the STEP's
closing substep: it executes an **external write to a third-party repository** (fork +
PR against `mherschberg/Throughstone`), writes the durable close record, and gives the
STEP's terminal gate verdict. A wrong PR body or a mis-claimed merge state is silent and
public — the judgement call is the deliverable.

## Context

Substeps 49.0–49.4 authored and validated the five guards on
`step-0049-template-hardening` in the local Throughstone clone (`D:\AppDev\Throughstone`),
with smoke-test evidence (init exit 0, check.sh exit 0, per-guard markers) and a
CHANGELOG entry. This substep takes the changeset public and closes STEP-49.

**Host facts (verified at planning, 2026-09-09):**
- `gh` CLI is **not installed**. Fork creation and PR submission go through the
  **browser** (the Hermes desktop browser tool, or the user manually) using the user's
  GitHub session — never guessed credentials.
- Upstream: `https://github.com/mherschberg/Throughstone` (HEAD at planning:
  `c815347e4d080278667e05459f3241a9db407238`; 49.0 recorded the sha actually branched).
- User decisions: fork + PR (changes benefit all future projects); local clone stays at
  `D:\AppDev\Throughstone`, outside the workspace, not registered in `registries/repos.yml`;
  mine-flow's local scaffold copies are **not** updated (adoption happens later via
  `UPDATING-THROUGHSTONE.md` manual mode).

## Read these first

- Root `.throughstone/local-user.md`.
- `Upcoming Prompts/mine-flow-STEP-49-PLAN.md` — Definition of done is your gate checklist.
- Findings from 49.0–49.4 — the complete evidence chain (landing map, per-guard edits,
  smoke logs). Your close record cites these; do not re-derive, but **spot-check the
  load-bearing claims** (branch exists and holds the commits; smoke log exists and says
  exit 0) — the close substep applies Guard ② to itself.
- `Code/mine-flow-docs/UPDATING-THROUGHSTONE.md` §8 (apply/branch rules) and §10 — the
  sanctioned contribution shape.
- `prompts/README.md` — the close/archive recipe (gather PLAN + prompts + findings to
  `prompts/003-release-readiness-integration-scale/step-0049/`, index row → Done).

## Scope

**Owns:** fork creation, branch push, PR submission, review iteration, the STEP-49 close
record, index/bookkeeping updates, and the user handoff.

**Does NOT touch:** mine-flow application code; `Code/mine-flow-docs/` content beyond
what STEP bookkeeping requires (none expected); upstream's history (no force-push).

## Your task

1. **Pre-flight (read-only, before any write):**
   - `git -C D:/AppDev/Throughstone status` clean; `git log --oneline` shows 49.1–49.4's
     commits on `step-0049-template-hardening`; record the branch-head sha.
   - Check upstream for movement: `git ls-remote origin` — if upstream's default branch
     advanced past 49.0's recorded base, rebase the branch (or note the divergence and
     flag it in the PR; your judgement, recorded either way).
   - Spot-check the evidence: the smoke log file exists and records exit 0; the
     CHANGELOG diff exists.
2. **Create the fork** (browser, user's GitHub session): fork
   `mherschberg/Throughstone` to the user's account. If the browser session is not
   authenticated, **stop and ask the user** — never guess credentials. Record the fork URL.
3. **Push the branch** to the fork: add the fork as remote `fork`, push
   `step-0049-template-hardening`. (Git Credential Manager's GitHub PAT works for HTTPS
   pushes on this host — precedent from STEP-47.7's log fetching.)
4. **Open the PR** against `mherschberg/Throughstone` (browser, or the GitHub
   compare-URL flow `https://github.com/mherschberg/Throughstone/compare/main...<user>:step-0049-template-hardening`):
   - Title: process-guards summary, e.g. *"Add STEP-close honesty, phantom-close,
     pre-flight, and trunk-hygiene guards from downstream field experience"*.
   - Body: one short paragraph per guard — the failure mode (with the mine-flow STEP-45
     evidence story as the motivating example), the guard, the landing files. Link the
     smoke-test evidence claim (init + check.sh exit 0 on a scratch project). Note that
     the changes are additive to existing rules, and that a downstream project
     (mine-flow) earned these the hard way and intends to adopt them via
     UPDATING-THROUGHSTONE manual mode.
   - **Record the PR URL.**
5. **Handle the review loop:** if upstream requests changes, iterate on the same PR/branch
   (default). If the PR is unmerged at close time, that is **not** a STEP failure —
   record its state honestly (open, review pending) and note the follow-up trigger
   (check PR status at the next check-in).
6. **Close the STEP (mine-flow bookkeeping):**
   - Gather `Upcoming Prompts/mine-flow-STEP-49-*.md` (PLAN + 6 prompts + 5 findings +
     this record) into `prompts/003-release-readiness-integration-scale/step-0049/`.
   - Update `prompts/STEP-index.md`: STEP-49 row → **Done** with a summary naming the
     five guards, the fork/PR URL, the smoke evidence, and the honest state of the PR
     (merged/open). Keep status vocabulary exact. Commit on `prompts/main` and push.
   - Phase README row for STEP-49 if the phase table carries one.
   - Run the duplicate-STEP scan and `scripts/check.sh` (via
     `Code/mine-flow-docs/scripts/check.sh`) — both clean.
   - Update the PLAN's substep table (all Done) and its Status → Done.
7. **Write the close record** (`Upcoming Prompts/mine-flow-STEP-49.5-FINDINGS.md` —
   which becomes the close record): pre-flight results, fork/PR URLs, PR state,
   bookkeeping commits, gate verdict, residuals (e.g. PR unmerged; mine-flow local
   adoption deferred by decision), and the next action per METHOD.md §10.

## Verification

- Fork exists and holds the pushed branch (verify: `git ls-remote fork` shows the sha).
- PR URL recorded and its state verified **by reading the PR page** (not assumed).
- `prompts/STEP-index.md` STEP-49 row reads Done with the PR URL; duplicate scan empty;
  `check.sh` exit 0.
- `Upcoming Prompts/` no longer holds loose STEP-49 files (all gathered); workspace
  root carries only cited evidence logs per house hygiene rules.
- **Honesty gate (self-application):** any part of this substep that could not be
  completed (e.g. PR submission blocked on authentication) leaves the STEP **not Done**
  or Done-with-recorded-residual — never a claimed success without the PR URL.

## Keeping the docs true

The close record is the durable source the index row cites. mine-flow's local scaffold
copies remain untouched by decision; if the PR merges later, adoption is a future
"check for Throughstone updates" pass, not this STEP's scope. No new risks accepted
(no `registries/risks.yml` edit expected — record that explicitly in the close record).

## Definition of done

- [ ] Fork created and branch pushed; `git ls-remote fork` verifies the sha.
- [ ] PR opened against upstream; URL recorded; state read from the page.
- [ ] STEP-49 gathered to `prompts/003-…/step-0049/`; index row Done with evidence links;
      duplicate scan empty; `check.sh` exit 0; prompts committed and pushed.
- [ ] Close record written with gate verdict, residuals, and next action.
- [ ] User told the next action in a **fresh chat** (next Planned STEP per the resolver).

## Next

This is the final substep. After the close record: tell the user the next action per
`METHOD.md` §10 — the next `Planned` STEP (STEP-51 per the index, or the resolver's
verdict), in a fresh chat.
