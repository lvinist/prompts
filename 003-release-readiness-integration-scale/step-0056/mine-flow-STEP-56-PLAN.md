# mine-flow — STEP-56 PLAN: Phase-3 Close-Out — Release Notes & User-Facing Docs

**Phase:** Phase 3 — Release Readiness, Integration & Scale
**Owner:** Hermes (frontier orchestration; subagents execute, parent verifies)
**Status:** Planned
**Date:** 2026-10-10
**Branch:** `step-0056-phase3-release-notes` (docs repo only; no application code, no app branch)
**Repos (projection):** `mine-flow-docs`, `prompts`

> Close out the Phase-3 milestone per METHOD §5 (Milestone doc review): draft release
> notes for v1.3.0 (Phase 3 Completion, STEP-41..55) from
> `templates/release-notes-template.md`, and reconcile the user-facing / phase-level docs
> that the per-STEP engineering discipline doesn't cover. **Draft-only posture: every
> artifact is written and parked for owner review; nothing publishes without the owner's
> morning approval.** This STEP deliberately runs while the owner sleeps — it is
> low-risk, docs-only, reversible, and touches no application code, infrastructure,
> secrets, or remote state.

## Motivation

`doctor.sh status` resolves the project to a milestone: every STEP in the index is final
(Done/Deferred/Abandoned), and the next action is exactly this — release notes + user-facing
doc updates (METHOD §5, §8), then next-phase planning in a fresh chat. Phase 3 delivered the
release-readiness baseline: contract/localization reconciliation, staging environment +
promotion pipeline, security/privacy baselines, dual-platform E2E, the STEP-54/55 UI rebuild,
and a CI-green close at `6e0b2e2`/`db4466b` (run `37949922909`). That arc deserves a
user-readable record; the three prior release notes
(`release-notes-v1.0.0-mvp.md`, `v1.1.0-ui-rebuild.md`, `v1.2.0-phase-2-completion.md`)
set the precedent this STEP follows.

## Decisions already locked

- **Owner decision (2026-10-10, this session):** draft everything, park for owner review
  before any publish. No direct publication.
- **Owner decision (2026-10-10, this session):** overnight failure policy = park lane,
  write FINDINGS, continue to the next independent lane. Nothing halts waiting for the owner.
- METHOD §5 "Milestone doc review" — release notes start from
  `templates/release-notes-template.md`, trimmed to applicable sections; user decides how
  much to do.
- Release-notes naming/versioning precedent: `reports/release-notes-v1.N.0-<milestone>.md`;
  Phase 3 Completion ⇒ **v1.3.0**.
- `registries/risks.yml` — production deployment remains blocked (RISK-0025 release
  condition); release notes must NOT claim production readiness. Owner requires production
  to remain blocked.
- No secrets/PII in artifacts; no reading `.env` values (standing safety boundary).
- Workspace hygiene rules (METHOD §7): durable content lives in the docs repo; scratch
  lives in `Upcoming Prompts/`.

## Substeps

| # | Title | Produces | Depends on | Open questions |
|---|-------|----------|------------|----------------|
| 56.1 | Release notes v1.3.0 (Phase 3 Completion) — draft | `reports/release-notes-v1.3.0-phase-3-completion.md` (draft, parked) | — | none — scope locked by owner |
| 56.2 | User-facing docs & phase-record reconciliation — draft | Phase-3 README STEP-55 row fix; overview.md drift check; user-facing gaps list (draft, parked) | 56.1 | none |

## Test plan

No test tiers apply: this STEP writes no application code. Mechanical gates instead:

| Gate | Substep(s) | Command / check | Notes |
|------|------------|-----------------|-------|
| Workspace/project checks | 56.1, 56.2 | `./check.sh` from workspace root (or `Code/mine-flow-docs/scripts/check.sh`) | 0 fails expected; pre-existing warnings (root debris, PyYAML absent) documented, not fixed here |
| Line-ending discipline | 56.2 | `git diff --stat` must show minimal, intended lines only; `git diff --check` clean | Markdown edits preserve each file's existing EOL convention |
| Duplicate STEP numbers | both | `grep -oE '^\|[[:space:]]*STEP-[0-9]+' prompts/STEP-index.md \| grep -oE 'STEP-[0-9]+' \| sort \| uniq -d` | empty output expected |

## Open questions

None — the owner answered the planning gates on 2026-10-10 (slate approved + reserved at
prompts `4e513b8`; draft-park posture; park-and-continue failure policy).

## Ground rules

- **Draft-only posture.** Every artifact from this STEP is a *draft for owner review*.
  No publish, no release tag, no "shipped" claims in user-facing language until the owner
  approves in the morning.
- **Orchestration model:** the frontier (parent) authors this PLAN and the substep prompts;
  an execution subagent runs each substep cold from its prompt; the parent verifies the
  result parent-side (reads every produced file, re-runs mechanical gates, checks EOL
  discipline) before marking the substep done. Child self-reports are never trusted alone.
- **No code, no app repo.** This STEP touches `mine-flow-docs` and `prompts` only.
  Do not create app branches or run Flutter gates.
- **Line endings:** scripted Markdown edits on tracked files must preserve the file's
  existing EOL convention (CRLF docs-hub convention for some files — verify per file via
  `file`/byte counts before writing; never normalize a whole file).
- **Commits:** each substep's work commits on the docs STEP branch
  `step-0056-phase3-release-notes` with its substep ID in the message. Push to origin is
  deferred to the close/review gate (owner approval) unless the failure policy says otherwise.
- **Accepted risks stay visible.** Production-blocked status (RISK-0025) and known
  unverified residuals (real-device a11y evidence) are stated in the release notes'
  Known Issues, not hidden.

## Definition of done

- [ ] `reports/release-notes-v1.3.0-phase-3-completion.md` exists as a complete draft from
      the template, trimmed to applicable sections, with Known Issues carrying
      production-blocked + unverified-residual status honestly.
- [ ] Phase-3 README table gains its missing STEP-55 row; overview.md checked for
      user-facing staleness; any gaps recorded as a parked list for the owner.
- [ ] `check.sh` 0 fails; duplicate scan empty; `git diff --check` clean for the STEP's files.
- [ ] FINDINGS files for 56.1/56.2 record evidence: files produced, sizes, gate outputs,
      parked-review status.
- [ ] Owner morning-review gate recorded: artifacts remain parked (or owner-approved),
      before any status flip to Done / archive / publish.
