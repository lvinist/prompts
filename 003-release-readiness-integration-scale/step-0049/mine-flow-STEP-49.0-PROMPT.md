# mine-flow — STEP-49.0: Upstream recon — clone, verify layout, map the five guards to landing sites

> **How to run:** Tell your agent *"run substep 49.0"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.

**Assigned model: Gemini 3.7 Flash High.** Procedural recon with unambiguous pass/fail
signals (repo reachable or not, files exist or not). Escalate if the upstream layout
differs materially from the expected docs-hub mapping — see Escalation below.

## Context

STEP-49 feeds mine-flow's earned process-failure modes back into the **Throughstone
scaffold** (the template mine-flow was bootstrapped from) as template guards. This is the
first substep: locate and clone the template repo, verify its layout matches what
`UPDATING-THROUGHSTONE.md` describes, and produce the per-guard landing-site map that
substeps 49.1–49.3 will implement against. No template edits happen in this substep.

- PLAN: `Upcoming Prompts/mine-flow-STEP-49-PLAN.md` (read it first).
- The five guards with their evidence: `Upcoming Prompts/mine-flow-STEP-47-48-49-RESERVATION-OUTLINE.md` §STEP-49.
- Upstream (verified reachable 2026-09-09, HEAD `c815347e4d080278667e05459f3241a9db407238`): `https://github.com/mherschberg/Throughstone`.

## Read these first

- Root `.throughstone/local-user.md` (calibrate explanations to Experience level).
- `Code/mine-flow-docs/UPDATING-THROUGHSTONE.md` — §1–§4: the upstream-source convention,
  file buckets, manual mode, and the `docs-hub` area mapping
  (upstream `Code/mine-flow-docs/` ↔ local docs hub).
- `Upcoming Prompts/mine-flow-STEP-47-48-49-RESERVATION-OUTLINE.md` — §STEP-49 in full.
- `prompts/README.md` — the STEP-planning conventions you are feeding back into.

## Scope

**Owns:** cloning upstream to `D:\AppDev\Throughstone`, verifying layout, reading
`CHANGELOG.md`/`README.md`/`METHOD.md` upstream, and authoring the landing-site map +
verify-loop design notes.

**Does NOT touch:** `Code/mine-flow-app/`, `Code/mine-flow-docs/` (no local scaffold
edits — user decision 2026-09-09), `prompts/STEP-index.md`, any upstream file's content.

## Your task

1. **Clone** `https://github.com/mherschberg/Throughstone` to `D:\AppDev\Throughstone`
   (outside the mine_flow workspace — it must NOT sit under `D:\AppDev\mine_flow`).
   Record the resolved HEAD sha. Do **not** create the fork yet (Q1 default: fork happens
   at 49.5; revisit only if the user says otherwise).
2. **Verify the layout** against `UPDATING-THROUGHSTONE.md` §4's mapping: does upstream
   carry `Code/mine-flow-docs/` containing `METHOD.md`, `AGENTS.md`,
   `prompts/README.md`-equivalent, `templates/` (step-plan-template, substep-prompt-template,
   planning-session), `runbooks/collaboration.md`-equivalent, `scripts/` (init.sh, check.sh)?
   Note any file that upstream names differently or lacks. If the `docs-hub` area mapping
   does not hold, **stop and escalate** (below) — do not improvise a different mapping.
3. **Read** upstream `CHANGELOG.md` (if present), `README.md`, and the current close/status
   rules in its METHOD-equivalent. Determine: does upstream already carry any of the five
   guards (even partially)? Which upstream version/release would our changes ride against?
4. **Author the landing-site map** — a table in your findings file, one row per guard:
   | Guard | Upstream file(s) to edit | Kind (process doc / template / script) | Conflict risk (has upstream changed this area since our bootstrap?) | Notes |
   Expected mapping (verify, don't assume):
   - ① Unverified-vs-Done honesty gate → step-plan-template close/DoD section, substep-prompt-template, METHOD close rules, possibly `templates/step-index-seed.md` status vocabulary.
   - ② Phantom-close detection → step-plan-template Definition-of-done checklist + METHOD close rules (branch/commit/artifact existence checks against disk).
   - ③ Credential/host-toolchain pre-flight → planning-session.md + METHOD STEP-planning rules (runtime/E2E STEPs must front-load a pre-flight substep).
   - ④ Commit-per-substep discipline → collaboration runbook + prompts/README recipe.
   - ⑤ Trunk-reservation recovery → collaboration runbook (dirty STEP-index on a STEP branch + the recovery recipe).
5. **Design the verify loop for 49.4** (notes only): how a scratch `init.sh` run can
   exercise the modified templates — which generated files should contain the new guard
   text, and what `check.sh` must still pass on. Also check whether upstream ships any
   test harness for its templates that we should run instead.

## Verification

- `git -C D:/AppDev/Throughstone rev-parse HEAD` returns the recorded sha; `git status` clean.
- Findings file `Upcoming Prompts/mine-flow-STEP-49.0-FINDINGS.md` exists with: clone
  sha, layout-verification table, per-guard landing-site map, existing-guard overlap
  check, target upstream version, verify-loop design notes.
- No file outside `D:\AppDev\Throughstone` and `Upcoming Prompts/` was modified.
- **Unverified rule:** anything you could not verify (e.g. upstream CI state, whether the
  maintainer accepts PRs) is reported as Unverified with the exact reason — never as success.
- Escalation triggers (record in findings if fired): upstream layout materially diverges
  from the docs-hub mapping; upstream already carries a conflicting version of any guard;
  the clone cannot be created (network/auth).

## Keeping the docs true

No architecture decisions change. This substep writes only the findings file (scratch
workspace, not a repo). If recon disproves a PLAN assumption (e.g. landing sites), record
it in the findings file and flag the PLAN for update in the next substep — do not edit the
PLAN silently.

## Definition of done

- [ ] Clone exists at `D:\AppDev\Throughstone` on upstream default branch, clean, sha recorded.
- [ ] Layout verified against `UPDATING-THROUGHSTONE.md` §4 mapping (or escalation recorded).
- [ ] Per-guard landing-site map authored with conflict-risk assessment.
- [ ] Existing-guard overlap check recorded (none / partial / conflicting, per guard).
- [ ] Verify-loop design notes for 49.4 recorded.
- [ ] Findings file saved; no out-of-scope file touched.

## Next

Update the PLAN's substep table (49.0 → Done) and tell the user the next action: *"run
substep 49.1"* in a **fresh chat**.
