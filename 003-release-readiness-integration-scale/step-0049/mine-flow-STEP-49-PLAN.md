# mine-flow — STEP-49 PLAN: Throughstone Template Hardening (process feedback)

**Phase:** Phase 3 — Release Readiness, Integration & Scale
**Owner:** User (accountable). Executors: Gemini 3.7 Flash High (49.0, 49.4) · Gemini 3.1 Pro High (49.1–49.3) · Hermes (Claude Opus 4.8 or equivalent top tier, 49.5 only)
**Status:** Done (closed 2026-09-09; upstream PR #206 Open)
**Date:** 2026-09-09
**Branch:** `step-0049-template-hardening` — in the **Throughstone clone only**; `prompts` and `mine-flow-docs` are touched for STEP bookkeeping (this PLAN, the index row, the close record) on `main`, not on a STEP branch
**Repos (projection):** Throughstone template repo (`D:\AppDev\Throughstone`, outside the workspace, not registered in `registries/repos.yml`), `prompts`

> Feed mine-flow's earned failure modes back into the Throughstone scaffold as template guards, so the next bootstrapped project cannot repeat them. **No mine-flow application code, and no edits to `Code/mine-flow-docs`'s local stamped scaffold copies** — mine-flow adopts the guards later through `UPDATING-THROUGHSTONE.md` manual mode in a future "check for Throughstone updates" pass (user decision, 2026-09-09).

## Motivation

mine-flow paid real costs for five process failure modes (recorded with evidence in
`Upcoming Prompts/mine-flow-STEP-47-48-49-RESERVATION-OUTLINE.md` §STEP-49):

1. **Phantom closes.** An executing agent closed 15/15 substeps `Done` while 14 staging
   journeys had never executed (`markTestSkipped('Unverified: Staging credentials absent')`)
   and every design-review item was Unverified. The record lied; nothing mechanical caught it.
2. **Stranded multi-repo closes.** STEP-45's close sat uncommitted across three repos, making
   `git switch main` impossible and blocking STEP reservation entirely.
3. **No pre-flight.** Runtime/E2E STEPs authored 14 journey tests before anyone proved the
   credentials and a working build/device existed — producing a wall of skipped tests.
4. **Multi-agent trunk hygiene gaps.** The dirty-`STEP-index.md`-on-a-STEP-branch failure
   mode and its recovery recipe exist only in mine-flow's private agent notes, not the scaffold.

Throughstone already has the hook for this: `UPDATING-THROUGHSTONE.md` §3 manual mode
compares scaffold/process material (`METHOD.md`, `AGENTS.md`, `templates/`, `runbooks/`,
`scripts/`) against the upstream release. This STEP is the *contribution* leg of that
process: author the guards upstream (fork + PR), not a local application of them.

**Verified facts this plan builds on (2026-09-09):**
- Upstream exists and is reachable: `https://github.com/mherschberg/Throughstone`,
  HEAD `c815347e4d080278667e05459f3241a9db407238` (live `git ls-remote`).
- No `throughstone*` clone exists under `D:\AppDev` yet (the STEP-49 index row's "to be
  located" is now resolved by `UPDATING-THROUGHSTONE.md` §1–§4).
- All three mine-flow repos are clean and in sync with remotes; `prompts/main` has no
  divergence; duplicate STEP-number scan empty.
- `gh` CLI is **not installed** on this host — fork creation and PR submission go through
  the browser (49.5) or an equivalent non-interactive authenticated path.

## Decisions already locked

- **User decisions (2026-09-09, captured this planning session):**
  - Changes reach upstream via **fork + PR**, with a local clone at `D:\AppDev\Throughstone`
    (outside the workspace, not registered in `registries/repos.yml`).
  - **Upstream only** — mine-flow's local scaffold copies are *not* edited by this STEP.
  - Model tiering: **only 49.5 on the top tier**; 49.1–49.3 run on the mid tier.
- `UPDATING-THROUGHSTONE.md` (§2 file buckets, §3 manual mode) — the guards land in
  **process docs and templates** buckets only; no project state is touched.
- `Code/mine-flow-docs/UPDATING-THROUGHSTONE.md` §10 — a scaffold change that alters
  METHOD.md / templates and shapes future planning sessions **is a tracked STEP**; this
  reservation already satisfies that.
- root `.throughstone/local-user.md` — executor prompts read Experience level /
  Communication style from it.
- `registries/risks.yml` — reviewed; no mine-flow risk rows are affected by this STEP
  (the guards are upstream template content; mine-flow adoption is deferred by decision).

## Substeps

| # | Title | Status | Model | Produces | Depends on | Open questions |
|---|-------|--------|-------|----------|------------|----------------|
| 49.0 | Upstream recon: clone, verify layout, map the five guards to landing sites | Done | Gemini 3.7 Flash High | Clone at `D:\AppDev\Throughstone`; `mine-flow-STEP-49.0-FINDINGS.md` with per-guard landing-site table + verify-loop design notes | — | Fork at clone time or at 49.5? (default: clone upstream first, add fork remote at 49.5) |
| 49.1 | Guard ① honesty gate + Guard ② phantom-close detection (templates + METHOD.md) | Done | Gemini 3.1 Pro High | Template edits (step-plan, substep-prompt, STEP-index/close rules), findings file | 49.0 | Wording of the mechanical gate clause (proposed in prompt; needs runtime readability) |
| 49.2 | Guard ③ credential/host-toolchain pre-flight substep (planning-session + METHOD.md) | Done | Gemini 3.1 Pro High | Planning-session + METHOD.md edits, findings file | 49.0 | None — pattern fully specified by STEP-47.0/47.5 |
| 49.3 | Guard ④ commit-per-substep + Guard ⑤ trunk-reservation recovery (collaboration + prompts/README) | Done | Gemini 3.1 Pro High | Collaboration runbook + prompts/README edits, findings file | 49.0 | None — recipe already proven in mine-flow |
| 49.4 | Scaffold smoke validation + CHANGELOG entry | Done | Gemini 3.7 Flash High | `init.sh` scratch-project run log; `check.sh` exit 0; upstream CHANGELOG.md entry; findings file | 49.1–49.3 | None |
| 49.5 | Push fork, open upstream PR, close STEP-49 | Done | Hermes (top tier) | Fork + PR (browser; `gh` absent), commit plan, STEP close record in `prompts/`, index row Done | 49.4 | PR body wording; merge policy if upstream requests changes (default: iterate on the same PR) |

> The Throughstone worktree is shared state across substeps 49.0–49.4: **each substep
> commits its own edits on `step-0049-template-hardening`** (Guard ④'s discipline applied to
> this STEP itself). One owner (the user) across all substeps; the models are executors,
  not owners (per `runbooks/collaboration.md` "one owner per STEP" — human accountability,
  model executorship).

## Model assignment

| Tier | Substeps | Justification |
|---|---|---|
| Cheap / fast | 49.0, 49.4 | Procedural with unambiguous pass/fail: clone-or-not, exit codes, a scratch `init.sh` run. 49.4's smoke test is run-and-report. |
| Mid | 49.1, 49.2, 49.3 | Real authoring work, but bounded by written authorities: the five guarded failure modes have documented evidence and proven recipes from mine-flow STEPs 45/47/48; the landing sites are enumerated by 49.0. |
| Top (1 of 6) | 49.5 | The closing substep writes the durable record, executes the external write (fork + PR to someone else's repository — a "judgement call about honesty and presentation is the deliverable"), and gives the STEP's terminal gate verdict. A wrong PR body or a mis-claimed merge state is silent and public. |

Per the tiering rule (2–4 top-tier substeps per ~16), 1 of 6 is deliberately conservative:
the user chose this at planning (2026-09-09). The honesty-semantics authoring in 49.1 is
bounded by mine-flow's documented recipes (STEP-48.26's status-from-latest-findings rule,
STEP-50's audit pattern) — the wording risk is real but the semantic target is written down;
mid tier suffices with named escalation triggers.

**Escalation triggers** (named per substep in the prompts; all require recording in that
substep's findings file): upstream layout differs materially from the docs-hub mapping
(49.0); a guard wording that changes what a *status column* means rather than adding a
check (49.1) — that is a METHOD-semantics change, escalate before authoring; a smoke-test
failure that is not trivially attributable (49.4); any fork/PR write that cannot be
completed non-interactively without leaking credentials (49.5).

## Test plan

| Test tier / surface | Substep(s) | Tests to create or update | Run timing | Command / gate | Notes |
|---|---|---|---|---|---|
| Scaffold smoke (project-specific) | 49.4 | Scratch-project init from the modified template | Final verification | `bash init.sh` in `$LOCALAPPDATA/Temp` scratch dir → exit 0; then `./doctor.sh check` / `scripts/check.sh` inside the scratch project → exit 0 | This STEP touches no mine-flow application code; the flutter suite is out of scope. |
| Static consistency | 49.4 | CHANGELOG entry exists and names all five guards | Final verification | grep in clone | |
| (N/A — no app code) | all | None | — | — | Genuinely code-free for mine-flow; template edits are validated by 49.4's smoke test, not by flutter tests. |

## Open questions

- Q1 (49.0): add the fork remote at clone time (you create the fork now) or at 49.5
  (default — avoids a stale fork if planning changes). Owner: user.
- Q2 (49.1): exact wording of the honesty-gate clause — proposed in the 49.1 prompt,
  final call is the executor's with escalation if it changes status semantics.

## Ground rules

- **No mine-flow application code, no local scaffold edits.** `Code/mine-flow-docs`
  gets nothing from this STEP; the only mine-flow artifacts are the PLAN, substep
  prompts/findings in `Upcoming Prompts/`, and the `prompts/` close record.
- **Calibrate communication from root `.throughstone/local-user.md`.**
- **Each substep commits its own edits** to the Throughstone clone's
  `step-0049-template-hardening` branch (Guard ④ discipline, applied to this STEP).
- **Honesty rule (the STEP's own subject matter):** a substep may not be marked Done if
  its evidence file says Unverified for a required deliverable — the prompt template's
  Unverified convention (report, never claim success) applies to every substep here.
- **Secrets:** never read/print `.env` values or GitHub credentials; the fork/PR uses the
  browser session or a named non-interactive auth path, never a guessed credential.
- **Upstream etiquette:** PR is one coherent changeset against a pinned upstream ref;
  no force-push, no rewrite of upstream history; iterate on review feedback in-place.

## Definition of done

- [x] The five guards from the reservation outline are authored in the Throughstone clone,
      each landing in the scaffold file its guard class calls for (per 49.0's mapping table).
- [x] Scratch-project smoke test passed: `init.sh` → exit 0, generated project's
      `check.sh` → exit 0, run log preserved in the findings file.
- [x] Upstream CHANGELOG.md carries an entry naming all five guards.
- [x] Fork pushed and PR opened against `mherschberg/Throughstone` (PR URL recorded in the
      close record), or the failure is honestly recorded as Unverified/blocked with the
      exact blocker.
- [x] No file under `Code/mine-flow-app/`, `Code/mine-flow-docs/` (beyond bookkeeping), or
      `prompts/` (beyond STEP-49 bookkeeping) was modified.
- [x] STEP review passed; `prompts/STEP-index.md` STEP-49 row updated to Done with evidence
      links; PLAN + prompts + findings gathered to
      `prompts/003-release-readiness-integration-scale/step-0049/`.
- [x] Next action communicated per METHOD.md §10 (fresh chat for the next Planned STEP).
