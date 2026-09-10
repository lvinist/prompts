# mine-flow — STEP-54.11: Master Polish Specification, Doc 07 Bump & STEP Close

> **How to run:** Tell your agent *"run substep 54.11"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.

**Assigned model: Hermes/Claude Opus 4.8.** This substep writes the durable specification STEP-55 executes 1:1 across twelve substeps and gives STEP-54's final verdict. An incoherent or internally contradictory spec is the most expensive quiet failure available in this STEP — every STEP-55 executor reads only their slice, so ambiguity surfaces as divergent implementations, discovered late.

## Context

All ten critique substeps (54.1–54.10) are complete, each with a findings file under `Upcoming Prompts/`. This substep consolidates them into the master polish specification, bumps Doc 07 to carry the interaction contracts, reconciles risks, and closes STEP-54.

Preconditions: 54.0–54.10 all Done in the PLAN's substep table, each with findings on disk. **Re-derive the findings' claims from disk before consolidating** — spot-check at minimum: the D7 verdicts, the D5 gap lists, and every `Needs restructure` finding's citation still resolves on the branch head.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-54-PLAN.md` — the STEP PLAN (definition of done, evidence standard)
- All findings files: `Upcoming Prompts/mine-flow-STEP-54.{0..10}-FINDINGS.md`
- `Code/mine-flow-docs/reports/2026-09-10-step-54-55-design-blueprint.md` — D1–D8 and the STEP-55 substep roadmap your spec must feed
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` — Doc 07 v0.4.0 (you are bumping it)
- `Code/mine-flow-docs/architecture/12-test-strategy.md` — what STEP-55's audit gate will demand
- `Code/mine-flow-docs/registries/risks.yml` — for reconciliation (RISK-0004, RISK-0011, RISK-0015/0016/0023 candidates)
- `Code/mine-flow-docs/METHOD.md` §5–§6 — archive/close conventions
- root `.throughstone/local-user.md`

## Scope

**Owns:**
1. The master polish spec: `Code/mine-flow-docs/reports/2026-XX-step-54-master-polish-spec.md` (XX = actual run date).
2. The Doc 07 bump to **v0.5.0** (Version Log entry; new sections for the interaction contracts).
3. Risk reconciliation: any new accepted risks / deferrals surfaced by 54.2–54.10 into `registries/risks.yml`.
4. STEP close: index row → Done, PLAN status header, archive to `prompts/003-release-readiness-integration-scale/step-0054/`, phase README row, `./doctor.sh check`.

**Does NOT touch:** application code (read-only — STEP-55 writes it), ADRs (a D1–D8 conflict needing an ADR is an escalation, not a silent edit), archived STEP-53 history.

## Your task

### Part A — Re-derive and reconcile (before writing anything)

1. Read every findings file; build a consolidated findings ledger (all `FC-54.*-NNN` IDs, verdicts, one-line summaries).
2. Spot-check citations: for every `Needs restructure` verdict, re-resolve its `file:line` on the branch head. A citation that no longer resolves is a blocker to resolve (re-locate or strike the finding) before it enters the spec.
3. Reconcile conflicts between substeps' findings (e.g. two substeps judging the same shared widget differently): pick the better-evidenced verdict, record the adjudication.
4. Collect the D7 verdicts into one table; if any feature lacks one, go derive it from that feature's findings before proceeding (do not leave blanks).

### Part B — The master polish spec (`reports/2026-XX-step-54-master-polish-spec.md`)

Structure it so each STEP-55 substep can execute from its own section without reading the whole:

1. **Reusable sheet contract** (feeds 55.0): `AppResponsiveSheet` behavior spec — Web right side-sheet 480–600dp (D1), Mobile modal bottom sheet (D2), scrim (D3), the universal dirty-check intercept flow with exact "Lanjut Mengedit" / "Buang Perubahan" dialog copy (D4), PopScope/ESC/back-gesture interception points, and the GoRouter deep-link adapter contract (D5) with the **full per-feature route table** (consolidating every substep's D5 gap list — create vs. edit URL semantics included).
2. **Contextual report dialog architecture** (feeds 55.1): the `FDialog`-based refactor of `report_config_page.dart` — pre-bound ReportType per feature (D6), filter-preservation contract, per-feature report inventory (including the deliberate absences 54.4/54.7/54.9 recorded).
3. **Per-feature polish backlog** (feeds 55.2–55.10): one section per feature, each a table of its findings → spec items, ordered (restructure → polish → token), each item carrying its finding ID(s) and enough specificity that an implementer doesn't re-derive the critique.
4. **D7 verdict table**: feature → inspector-sheet vs. full-page vs. N/A → rationale → which STEP-55 substep implements it.
5. **Design tokens & component gaps** (feeds 55.0/55.11): token additions/changes Doc 07 needs, any missing shared components the critiques imply (e.g. a shared badge/chip family if attendance + inventory + equipment diverge today).
6. **A11y & platform acceptance criteria** (feeds 55.11): the concrete, checkable bar for the audit — contrast, touch targets ≥ 48dp, semantics, per-platform layout ranges.
7. **Evidence appendix**: per-substep coverage summary; every `Unverified` item listed with its blocker (STEP-55.11's audit owes these a real runtime verdict).

### Part C — Doc 07 bump (v0.4.0 → v0.5.0)

Add to Doc 07: the sheet/dialog/dirty-check interaction contracts (summarized; the report carries detail), the responsive breakpoint canon as verified, and the D7 detail-view pattern. Bump the Version Log with author/date/changes. Keep it the *canon*, not a duplicate of the spec report — cross-reference.

### Part D — Risk reconciliation & close

1. New/changed accepted risks from the critiques → `registries/risks.yml` rows (severity, owner, revisit trigger, referencing the spec report).
2. Present the spec to the user for review (this is the STEP's review gate — the user reviews the master spec before close).
3. On approval: flip the STEP-54 index row to `Done` with a close summary; update the PLAN status header; gather `Upcoming Prompts/mine-flow-STEP-54-*` files into `prompts/003-release-readiness-integration-scale/step-0054/`; update the phase README row; commit and push `prompts/main`; run the duplicate scan; run `./doctor.sh check`.
4. The step-0054 branch in app + docs: these repos saw no code changes — merge/delete per the user's direction (the docs branch carries the report + Doc 07 + risks changes; the app branch is a no-change branch — confirm with the user, likely merge docs, delete app branch).

## Verification

- Every spec item traces to at least one finding ID; every `Needs restructure` finding's citation re-resolved.
- No finding was dropped silently: the consolidated ledger accounts for every `FC-54.*-NNN` (spec'd, deferred-with-reason, or escalated).
- Doc 07 v0.5.0 committed on the docs repo with Version Log entry; `scripts/check.sh` passes.
- STEP-54 row `Done` on pushed `prompts/main`; duplicate scan empty; archive folder complete (PLAN + 13 prompt/findings files).
- STEP-55's PLAN can be authored from the spec alone (sanity-check by reading 55.0/55.1's blueprint rows against your spec sections).

## Keeping the docs true  (always)

- Doc 07 bump is the doc-true action of this STEP — the interaction contracts become canon here.
- Never rewrite an accepted ADR: a D1–D8 conflict discovered during consolidation becomes an escalation to the user (possible ADR), never a silent spec deviation.
- Secrets stay out; findings quote no `.env` values.

## Definition of done

- [ ] Consolidated findings ledger complete; every finding ID accounted for.
- [ ] Master polish spec published under `reports/` with all seven sections.
- [ ] Doc 07 bumped to v0.5.0 with Version Log entry; `scripts/check.sh` green.
- [ ] Risks reconciled; user review of the spec recorded.
- [ ] Index row Done; archive complete; duplicate scan empty; `./doctor.sh check` passes.
- [ ] Step-0054 branches handled per user direction.

## Next

The STEP is closed. Tell the user the next action: **author STEP-55's PLAN + substep prompts** (it is the reserved, blueprint-mapped implementation STEP) — in a **fresh chat**. Note the check-in cadence: last check-in at STEP-50; a check-in is due around STEP-60–70 per the resolver, and STEP-55's completion is a sensible pre-STEP-56 checkpoint to reassess.
