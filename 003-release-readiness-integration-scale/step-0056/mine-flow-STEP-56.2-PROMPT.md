# mine-flow — STEP-56.2: User-Facing Docs & Phase-Record Reconciliation — DRAFT

> **How to run:** "run substep 56.2". Cold-runnable; read this file plus the PLAN cold.
>
> **Assigned model tier: mid** (mechanical-to-moderate reconciliation bounded by written
> authority: templates, registries, and the phase README table; no silent-failure surface).

## Context

STEP-56's second half: reconcile the user-facing and phase-level records that per-STEP
engineering discipline left stale, as part of the METHOD §5 milestone doc review. A known
defect exists to fix: the Phase-3 README summary table is **missing its STEP-55 row** (the
folder `prompts/003-release-readiness-integration-scale/step-0055/` was archived at
prompts commit `41d25cb`, but the table ends at STEP-54). Additionally, the owner wants a
draft list of what user-facing documentation gaps exist, parked for morning review.
STEP PLAN: `Upcoming Prompts/mine-flow-STEP-56-PLAN.md`; 56.1 (release notes) precedes
this substep on the same branch.

## Read these first

- `prompts/003-release-readiness-integration-scale/README.md` — the phase roster table
  (CRLF file — preserve endings on edit).
- `prompts/003-release-readiness-integration-scale/step-0055/` — the archived STEP-55
  artifacts (confirm substep range for the row: 55.0..55.11).
- `Code/mine-flow-docs/overview.md` — the product surface description; check its
  "What it does" / phase status language against Phase-3 outcomes.
- `Code/mine-flow-docs/METHOD.md` §5 "Milestone doc review" — what this review covers.
- `Code/mine-flow-docs/architecture/README.md` — the doc index (version columns) — read-only
  cross-check that no architecture doc claims a *pending* Phase-3 item as still open.
- `Upcoming Prompts/mine-flow-STEP-56.1-FINDINGS.md` — what 56.1 already produced (avoid
  duplicating the release notes' content).

## Scope

**Owns:** (a) adding the missing STEP-55 row to the phase-3 README table in `prompts/`;
(b) a drift check of `overview.md`'s user-facing claims against Phase-3 outcomes, with a
draft gap list; (c) `Upcoming Prompts/mine-flow-STEP-56.2-FINDINGS.md`.
Branch: same `step-0056-phase3-release-notes` (docs repo) for any docs-hub edit; the
README fix belongs to `prompts/` on its `main` — follow the shared-trunk rule:
read-immediately-before-edit, single targeted patch, commit on `prompts/main`
(dedicated small commit), push (this is the append-only history trunk, not a publish —
the reservation commit `4e513b8` precedent).

**Does NOT touch:** application code, architecture docs' *content* (this STEP is not the
doc-drift reconciliation — that's STEP-58; here only *user-facing* staleness), release
notes content, `registries/risks.yml`, `STEP-index.md` rows' status cells.

## Your task

1. **Fix the phase-3 README table:** insert after the STEP-54 row:
   `| STEP-55 | Cohesive UI Rebuild — Form Sheets, Contextual Report Dialogs & Impeccable Audit | 55.0..55.11 | 2026-10-09 |`
   — preserving the file's CRLF convention exactly (targeted patch; verify
   `git diff --stat` shows 1 insertion; count CRLF pairs before/after).
2. **overview.md drift check (read + list, mostly read-only):** compare its described
   capabilities/phase language against Phase-3 shipped outcomes (staging-backed E2E,
   security baseline, the UI rebuild). If a *user-facing* claim is stale or missing
   (e.g. the "Phase 2: integrate with survey tools" deferral language vs. where the
   project actually stands), record it as a draft gap item. **Do not rewrite overview.md
   wholesale** — park the gap list in the FINDINGS file for the owner. Exception: if a
   single line is *unambiguously* wrong (says something contradicts the STEP-index),
   make the one-line fix on the docs STEP branch and name it in FINDINGS.
3. **User-facing docs gap list (draft, parked):** enumerate what a user/ operator would
   need that engineering docs don't provide (e.g., a user guide for the new form-sheet
   behaviors, the privacy notice copy — flagged as pending legal approval, release-notes
   publish channel). Each gap: one line, owner-decision needed or not.
4. Write `Upcoming Prompts/mine-flow-STEP-56.2-FINDINGS.md` with: the README fix diff
   summary + commit sha, the overview.md verdict (per-checked-claim), the gap list,
   gate outputs, and "parked for owner review".

## Verification

Docs-only — no tests apply (stated reason: no code). Mechanical gates:

- `prompts/` README fix: `git diff --stat` = 1 file, 1 insertion; CRLF pair count
  unchanged+1 for the new row; duplicate STEP scan still empty; push succeeded and
  `prompts/main` synced with `origin/main`.
- Docs branch (if any overview.md one-liner): `git diff --check` clean; only the named
  line changed.
- Workspace `check.sh`: 0 fails (pre-existing warnings allowed, documented).
- Read-back: the new README row matches the archived folder's actual substep range
  (55.0..55.11 — verify against the folder's file names, don't trust this prompt).

**Run timing:** run gates before marking done. Commits: `prompts/main` gets
`docs(56.2): add missing STEP-55 row to Phase-3 README table`; docs branch (if touched)
gets its own commit. No merges to docs `main`, no pushes of the docs branch, no
status flips.

## Keeping the docs true

This substep *is* the doc-truth work for the phase record. No architecture decisions
change; no new risks created. If the overview check surfaces a *security or contract*
drift item, do not fix — list it for STEP-58's reconciliation instead.

## Definition of done

- [ ] Phase-3 README table includes the STEP-55 row; committed + pushed on `prompts/main`;
      diff proven = 1 insertion; CRLF preserved.
- [ ] overview.md drift verdict recorded per claim (fixed-one-liner / parked-gap /
      accurate-as-is).
- [ ] Gap list drafted and parked in FINDINGS.
- [ ] No status flips; docs branch not merged/pushed; STEP-56 stays Planned until the
      owner's morning review.

## Next

Report to the parent orchestrator: 56.2 complete + parked. The parent verifies, then
STEP-56 is complete pending the owner's morning review of the parked drafts (release
notes, gap list, any one-line fixes). The owner's approval authorizes: publish/push of
the docs branch, STEP-56 status flip to Done, and archive.
