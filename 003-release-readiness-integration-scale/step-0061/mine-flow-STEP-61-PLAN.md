# mine-flow — STEP-61 PLAN: Milestone Doc Review Remediation — STEP-56..60 Batch

**Phase:** Phase 3 — Release Readiness, Integration & Scale (post-milestone remediation)
**Owner:** Hermes (frontier orchestration; subagent executes, parent verifies)
**Status:** Done
**Date:** 2026-10-10
**Branch:** none — direct commits on `main` (docs) and `main` (prompts); owner pre-approved all fixes, pushes, and the GitHub release on 2026-10-10
**Repos (projection):** `mine-flow-docs`, `prompts` (+ a GitHub release on `lvinist/mine-flow-app`; no app-repo code changes)

## Motivation

The 2026-10-10 milestone doc review (draft FINDINGS:
`Upcoming Prompts/mine-flow-DRAFT-milestone-doc-review-STEP-56-60-FINDINGS.md`)
swept the closed STEP-56..60 batch and found record drift: the phase README was never
backfilled past STEP-55, the published v1.3.0 release notes carry Known Issues that
STEP-57/59/60 have since resolved, the STEP-58 index evidence cell still describes a
branch as unpushed although it merged at `2a88aa0`, overview.md still uses pre-re-scope
"Phase 2" terminology, and STEP-60's archive is missing its three per-substep PROMPT
files plus its index substep table. The owner approved all five fixes, the release-notes
publish (GitHub release tag), and execution as this canonical STEP.

## Decisions already locked (owner, 2026-10-10 — do not re-ask)

- **All five findings apply:** C1 (phase README backfill STEP-56..60), C2 (release-notes
  Known Issues cleanup of resolved items + References extension to the batch), C3
  (STEP-58 evidence-cell trim), C4 (overview.md "Phase 2"→"Phase 3" terminology per
  `02-phasing-roadmap.md`), C5/S4 (complete STEP-60 archival: move the 3 stranded
  `60.x-PROMPT.md` files into `step-0060/` + add the STEP-60 substep table).
- **Publish channel:** the release notes (already in docs `reports/`, merged) are to be
  **tagged as a GitHub release `v1.3.0`** on `lvinist/mine-flow-app` at the batch close
  head `c4f40302153f992871965a7926eb321182ea0c4c`, body = the release-notes file.
- **Check-in:** STEP-62 reserved separately (not this STEP's work).
- **Push authority:** commits on `prompts/main` and `docs main` are pre-approved to be
  pushed to origin as part of this STEP, including the STEP-61 close bookkeeping.

## Substeps

| # | Title | Produces | Depends on | Open questions |
|---|-------|----------|------------|----------------|
| 61.1 | Apply all five doc-review fixes + GitHub release tag | Phase-3 README rows 56..60; cleaned release-notes Known Issues + extended References; trimmed STEP-58 cell; overview terminology fix; STEP-60 archive completed (3 PROMPT files moved + substep table); GitHub release `v1.3.0` created; commits pushed on both trunks | — | none (all owner-locked) |
| 61.2 | Verification + STEP-61 close | FINDINGS with read-backs (CRLF counts, dup scan, check.sh, release URL); STEP-61 index flip to Done; PLAN/prompts archive move; final pushes | 61.1 | none |

## Model assignment (per silent-failure tiering)

Mid tier — `vc/deepseek-v4.1` for both substeps: mechanical edits bounded by the written
authority of the FINDINGS dispositions and the locked decisions above. The durable close
verdict is parent-verified after the child returns (frontier parent re-derives every
claim on disk); no data, authorization, or shared architecture can be silently corrupted
because all edits are docs/registry records with read-back gates.

## Test plan

| Test tier / surface | Substep(s) | Tests | Command / gate |
|---------------------|------------|-------|----------------|
| Registry/static gates | 61.2 | check.sh, duplicate STEP scan, `git diff --check` per repo, CRLF read-back on the phase README, `cmp`-verified archive moves | exit 0 / empty / counts match |
| Release read-back | 61.1/61.2 | GitHub release `v1.3.0` exists, tag == `c4f4030…`, body == release-notes content | API GET read-back |

No `flutter test` tiers: this STEP touches no application code, no `lib/`/`test/` files.

## Ground rules

- Read each target file immediately before editing; re-derive each FINDINGS claim on
  disk before acting on it (the review was drafted the same day, but verify anyway —
  e.g. confirm `risks.yml` still shows RISK-0030 `closed` before removing its
  Known-Issues line).
- The phase-3 README is a **CRLF-convention file** — preserve it (CR-byte count must
  equal line count after the edit).
- Never print `.env` values or credentials. The GitHub token comes from
  `git credential fill` and is used only in a curl `Authorization:` header; never echo
  it, never write it to any file.
- Commits: one logical commit per repo per concern; push only after read-backs pass;
  verify each push is a fast-forward (`main` == `origin/main` before pulling the
  trigger, re-pull if not).
- Every claim that cannot be re-derived on disk is recorded **Unverified**, never "done".

## Close record (2026-10-10)

**Closed 2026-10-10 (owner pre-approved):**

- All five fixes (C1–C5/S4) applied and verified by 61.1 FINDINGS
- GitHub release `v1.3.0` tagged at `c4f40302153f992871965a7926eb321182ea0c4c` on `lvinist/mine-flow-app`; API read-back verified (html_url, name, body first heading match)
- Commits: `prompts/` `ca9fbcb`, `docs` `abfc769` — both pushed FF-only, `main == origin/main` verified
- Gates (61.2): check.sh 0 fail(s), 1 warn (pre-existing root-hygiene); duplicate STEP scan clean; `git diff --check` clean in all 3 repos; phase-3 README CRLF 39/39 preserved; release-notes CRLF 102/102 preserved
- STEP-index.md STEP-61 row flipped Done with close evidence; `### STEP-61 substeps` table added
- Archive move: 5 files (PLAN, 2 PROMPTs, 2 FINDINGS) → `prompts/003-release-readiness-integration-scale/step-0061/` — verified at destination
- Final commit `docs(61.2): STEP-61 closed Done — milestone doc-review remediation applied` pushed FF-only to prompts/main
