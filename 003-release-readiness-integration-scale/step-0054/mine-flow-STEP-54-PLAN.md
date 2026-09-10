# mine-flow — STEP-54 PLAN: Multiplatform Impeccable Feature-Cohesion Critique & Polish Spec

**Phase:** Phase 3 — Release-readiness & integration scale
**Owner:** User (accountable) — executors: Hermes/Claude Opus 4.8 (54.0, 54.1, 54.10a, 54.11) · Gemini 3.1 Pro High (54.2–54.10). The models are executors only; the user remains the single accountable owner per `runbooks/collaboration.md`.
**Status:** Complete
**Date:** 2026-09-10
**Branch:** `step-0054-feature-cohesion-critique` (same name in every repo it touches; cut only after the 54.0 pre-flight gate is clean)
**Repos (projection):** `mine-flow-app` (read-only for critique; branch cut for spec-adjacent doc artifacts only) → `mine-flow-docs` (report + Doc 07 bump) → `prompts` (index/bookkeeping)

> Deliver a cohesive end-to-end design critique of all 9 features and the app shell across Web (desktop) and Android, and consolidate it into the master polish specification + design-token contract that STEP-55 implements 1:1. **This STEP writes no application code** — its deliverables are findings files, a rubric, and the master spec.

## Motivation

The 2026-09-10 design blueprint (`Code/mine-flow-docs/reports/2026-09-10-step-54-55-design-blueprint.md`) locked the interaction world (D1–D8: right side-sheet on Web, bottom sheet on Mobile, modal scrim, universal dirty-check intercept, GoRouter deep-link sync, contextual `FDialog` reports) but each feature's screens were built STEP-by-STEP and have never been critiqued *as cohesive lifecycles* (List → Form sheet → Detail → Report dialog) nor *cross-platform*. STEP-54 produces the per-feature critique and the unified specification STEP-55 executes; skipping it would let STEP-55 implement a pattern library onto screens whose information design, states, and platform behavior were never audited.

## Pre-flight (resolved at planning time, verified by 54.0)

- **STEP-53 merge reconciliation (54.0 complete):** Per the user's decision, app `master` was fast-forwarded to the recorded head `fe12531` and docs `main` to `891ce66`; both original STEP-53 branches were deleted. Later corrections `226aa00` and `30b0b06` were preserved on explicit backup branches and not merged. The untracked `.step53-logs/` evidence was archived in `Code/mine-flow-docs/reports/test-results/2026-09-10-step-0053-evidence/`.
- `Upcoming Prompts/` verified empty at planning time (STEP-53 fully archived).
- `prompts/STEP-index.md` duplicate scan: empty at planning time.

## Decisions already locked

- **Blueprint D1–D8** (`reports/2026-09-10-step-54-55-design-blueprint.md` §2) — every critique substep evaluates *against* these decisions; a critique may surface a conflict, but overturning a locked decision is an ADR-level escalation (see Escalation), never a silent local deviation.
- **Doc 07 — UI/Design System v0.4.0** (`architecture/07-ui-design-system.md`): ForUI Zinc canon, compact density, Geist typography, Lucide icons, sidebar (Web) + 5-item bottom bar (Android), WCAG 2.1 AA target, ID locale, 150–200ms motion. Critiques cite Doc 07 sections, not taste.
- **D7 (per-feature detail views):** STEP-54 itself decides side-sheet inspector vs. full page per feature — this is the STEP's one open design question class; 54.11 consolidates the per-feature verdicts.
- **ADR-0017** (dual-platform E2E gate) and Test Strategy doc v1.3 — runtime evidence expectations follow their platform split (Chrome + Pixel_6a).
- **RISK-0015/0016/0023** (design-review screenshot placeholders): "a screenshot file exists" is NOT visual evidence. See Evidence standard.
- root `.throughstone/local-user.md` — read Experience level / Communication style before user-facing questions.
- `registries/risks.yml` — review rows touching UI/l10n (RISK-0004 l10n migration) when a critique surfaces strings.

## Evidence standard (applies to every critique substep)

**Hybrid** (user decision, 2026-09-10):

1. **Static code inspection is the mandatory floor.** Every finding cites `file:line` in `Code/mine-flow-app/lib/...` (paths as of the branch head the substep inspects; re-locate on the tree you actually have). A finding without a code citation is a hypothesis, not a finding.
2. **Runtime capture is used where the existing harness works**, with honesty about which harness produced it: name the command (`flutter drive` web-server recipe, Android emulator run), the artifact path, and **the artifact's byte size and pixel dimensions** — anything suspiciously small (the 68-byte / 1×1 class from STEP-48) must be reported as *harness-defect*, not as visual evidence. **54.10a adds a second authorized capture route**: the project-vendored Impeccable skill's browser stack (`.agent/skills/impeccable/`), independent of the `flutter drive` harness. Its mechanical detector is DOM/CSS-based and returns **no signal** on this CanvasKit app — a clean detector result is therefore *not* evidence of design quality.
3. **Runtime claims that cannot be evidenced are recorded as `Unverified`** with the blocker named — never as success, never silently omitted. Fixing the capture harness is **out of scope** for STEP-54 (it is STEP-55.11 audit territory); record the gap and move on.

## Substeps

| # | Title | Produces | Depends on | Model | Open questions |
|---|-------|----------|------------|-------|----------------|
| 54.0 | Pre-flight: STEP-53 merge reconciliation & clean trunk | Done — findings `Upcoming Prompts/mine-flow-STEP-54.0-FINDINGS.md`; app/docs trunks pushed, evidence archived, STEP-54 branches cut | — | Hermes/Claude Opus 4.8 | Resolved: archive evidence; merge only recorded STEP-53 heads |
| 54.1 | Critique rubric, token vocabulary & shell/navigation foundation critique | Done — `mine-flow-STEP-54.1-FINDINGS.md`: reusable rubric, `FC-54.1-NNN` IDs/verdicts, shell critique, complete nine-feature D5 route-gap enumeration; no app code changed | 54.0 | Hermes/Claude Opus 4.8 | none (rubric is the deliverable) |
| 54.2 | Operations 1 — Cut & Fill Volume Tracking critique | Done — `mine-flow-STEP-54.2-FINDINGS.md`: list (table/cards), entry form sheet spec, PDF report dialog, per-platform verdicts | 54.1 | Gemini 3.1 Pro High | D7 detail-view verdict |
| 54.3 | Operations 2 — Land Clearing Tracking critique | Done — `mine-flow-STEP-54.3-FINDINGS.md`: Plan/Actual tabs, shared method combobox, entry sheet, report dialog | 54.1 | Gemini 3.1 Pro High | D7 detail-view verdict |
| 54.4 | Operations 3 — Benchmark Database critique | Done — `mine-flow-STEP-54.4-FINDINGS.md`: spatial validation bug, D1/D2 form layout, Material holdovers, D5 route gap, CRS UX, D7 verdict | 54.1 | Gemini 3.1 Pro High | D7 detail-view verdict (read-only inspector) |
| 54.5 | Teams 1 — Crew Attendance critique | Done — `mine-flow-STEP-54.5-FINDINGS.md`: 13 findings; offline-sync trust signal escalated; no separate D7 detail view | 54.1 | Gemini 3.1 Pro High | Resolved |
| 54.6 | Teams 2 — Daily Logging critique | Done — `mine-flow-STEP-54.6-FINDINGS.md`: 10 findings; structured hazard gap; existing read-only form mode is the D7 detail surface | 54.1 | Gemini 3.1 Pro High | Resolved |
| 54.7 | Teams 3 — Equipment Digital Checks critique | Done — `mine-flow-STEP-54.7-FINDINGS.md`: 7 findings; route-backed Web inspector / Mobile full-page D7 verdict | 54.1 | Gemini 3.1 Pro High | Resolved |
| 54.8 | Teams 4 — Inventory Management critique | Done — `mine-flow-STEP-54.8-FINDINGS.md`: 11 findings; adjustment-reason/history data-integrity escalation; read-only stock-history D7 detail | 54.1 | Gemini 3.1 Pro High | Resolved |
| 54.9 | Tools & Timeline — Data Bucket & Work Timeline critique | Done — mine-flow-STEP-54.9-FINDINGS.md: file repository (list/upload/detail inspector), milestone sheet | 54.1 | Gemini 3.1 Pro High | D7: file-detail inspector is explicitly open here |
| 54.10 | System Utilities — Dashboard, Notifications, Settings & Auth critique | Done — `mine-flow-STEP-54.10-FINDINGS.md`: KPI tap-through gap, notification mobile reachability, login privacy notice absence (RISK-0011 escalated), settings profile read-only; 24 findings FC-54.10-001..024 | 54.1 | Antigravity (Claude Sonnet 4.6 Thinking) | none |
| 54.10a | Impeccable-skill runtime capture & a11y evidence closure | Done — `mine-flow-STEP-54.10a-FINDINGS.md`: 19 byte/dimension-honest Web captures (shell, login, dashboard, benchmark form, report × desktop/narrow × light/dark) + an Android login portrait; the `flt-semantics`/browser-AX a11y record (desktop sidebar + global header expose **no** semantics; mobile 5 labelled tabs); the detector no-signal finding with false-positive proof; 19 findings `FC-54.10a-001..019`; escalations: RISK-0011 privacy notice absent, and the app logging the anon key | 54.10 | Hermes/Claude Opus 4.8 | none (evidence closure, review-only) |
| 54.11 | Master polish spec, Doc 07 bump & STEP close | Done — `reports/2026-09-11-step-54-master-polish-spec.md`: 127/127 findings reconciled; Doc 07 v0.5.0; risks updated; accountable-user review approved after requested interaction refinements | 54.2–54.10a | Hermes/Claude Opus 4.8 | Resolved |

## Model assignment

| Tier | Substeps | Why this tier |
|---|---|---|
| Top — Hermes/Claude Opus 4.8 | 54.0, 54.1, 54.10a, 54.11 | 54.0 touches shared-trunk git state another STEP left inconsistent — misclassifying the unmerged ledgers silently corrupts trunk. 54.1's rubric + findings-ID scheme is inherited by all 10 later substeps; a wrong rubric is a silent, compounding failure. 54.11 writes the durable spec STEP-55 executes 1:1 and gives the STEP's final verdict — an incoherent spec is the most expensive quiet failure available here. 54.10a must run on a harness with local script + browser-automation access — it drives the project-vendored skill at `.agent/skills/impeccable/`, so a prose-only executor cannot run it at all. |
| Mid — Gemini 3.1 Pro High | 54.2–54.10 | Real design critique, but bounded by written authority: blueprint D1–D8, Doc 07, the 54.1 rubric, and the STEP-48 findings format. Failure modes (a missed finding, a weak citation) are caught by 54.11's consolidation and STEP-55's implementation. |
| Cheapest tier | none | Design critique has no mechanical pass/fail signal; nothing in this STEP is procedural. |

**Escalation rule (all substeps, always):** escalate to the user (and record the escalation in the findings file) on: (a) a critique that conflicts with a locked decision D1–D8 or an accepted ADR — ADRs are superseded deliberately, never retrofitted to match critique output; (b) runtime behaviour that contradicts Doc 07's canon; (c) 54.0 discovering the STEP-53 state is not what this PLAN's pre-flight section describes (e.g. additional unmerged commits, remote divergence); (d) being tempted to record a runtime claim the harness cannot actually evidence; (e) the same classification problem recurring twice — stop, diagnose, escalate.

## Test plan

| Test tier / surface | Substep(s) | Tests to create or update | Run timing | Command / gate | Notes |
|---------------------|------------|---------------------------|------------|----------------|-------|
| Static analysis / format (regression guard) | 54.0 | none (no code written) | at 54.0 | `flutter analyze` + `dart format --output=none --set-exit-if-changed .` on the reconciled trunk | Proves the merge didn't regress the 53.4-verified baseline (550/550 was verified pre-merge on the branch) |
| Full unit/integration suite | 54.0 | none | at 54.0 | `flutter test` (expect 550/550) | Same purpose; recorded in 54.0 findings |
| Docs integrity | 54.11 | none | at close | `./doctor.sh check` (validates statuses, no duplicate STEP numbers) | The STEP's gate |

**Why no new tests:** STEP-54 writes findings/spec documents, not code. Per the Test Strategy doc, tests ship with code; STEP-55 owns the test plan for everything this STEP specifies. `flutter analyze`/`flutter test` at 54.0 exist solely to prove the STEP-53 merge is sound, not to test STEP-54 output.

## Ground rules

- **No application code.** `Code/mine-flow-app/lib/**` is read-only for 54.1–54.11. The only app-repo writes allowed: none. If a critique substep believes code must change, it writes a spec item, not a diff.
- **Findings format:** every critique substep produces `Upcoming Prompts/mine-flow-STEP-54.M-FINDINGS.md` following the STEP-48 runtime-design-review table shape (Coverage / Findings with IDs / Verification record / Limitations), with findings IDs `FC-54.M-NNN`.
- **Evidence standard** as defined above: static citation floor, honest runtime capture, explicit Unverified.
- **54.10a skill boundary:** only `context`, `detect`, `critique-storage`, `live-server` (+`stop`) may run. `init`/`document`/`extract` would rewrite the ADR-0008-protected `DESIGN.md`/`PRODUCT.md`; `install`/`link` write harness manifests; every mutating design command (`polish`, `bolder`, `animate`, …) is STEP-55's lane. No hook installation. Findings only — 54.10a must not attempt a fix.
- **Communication:** calibrate from root `.throughstone/local-user.md` (Explanatory style, Level 2) — critiques explain *why* a pattern is a defect, not just that it is.
- **Accepted risks surfaced by critiques** (e.g. "cannot fix X without breaking Y") go to `registries/risks.yml` with owner + revisit trigger, referencing the findings file — via 54.11 consolidation, not per-substep edits.
- **One substep = one fresh chat.** Prompts are self-contained; each updates the STEP PLAN progress row when done.

## Definition of done

- [x] 54.0 has reconciled STEP-53 (both branches merged or user-directed alternative recorded), trunk is clean, and the STEP-54 branch exists in every projected repo.
- [x] Every critique substep 54.1–54.10 has a findings file with per-platform coverage, file:line-cited findings, D7 verdict (where applicable), and explicit Unverified markers where runtime evidence is unavailable.
- [x] 54.10a has recorded byte/dimension-honest Web captures, the `flt-semantics` a11y record, and the detector no-signal finding; its `Unverified` items are enumerated for 54.11's evidence appendix.
- [x] 54.11 has published the master polish spec under `reports/`, bumped Doc 07 to v0.5.0 with a Version Log entry, and reconciled any new accepted risks into `registries/risks.yml`.
- [x] `./doctor.sh check` passes; duplicate STEP-number scan empty.
- [x] STEP review passed (user reviews the master spec); `prompts/STEP-index.md` updated to Done; STEP archived to `prompts/003-release-readiness-integration-scale/step-0054/`.
- [x] The STEP test plan is complete: no code was written; the 54.0 merge-regression run is recorded in its findings file.
