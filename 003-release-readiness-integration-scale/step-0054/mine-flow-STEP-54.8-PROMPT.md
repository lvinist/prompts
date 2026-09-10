# mine-flow — STEP-54.8: Teams Suite 4 — Inventory Management Critique

> **How to run:** Tell your agent *"run substep 54.8"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.

**Assigned model: Gemini 3.1 Pro High.** Real design critique, bounded by blueprint D1–D8, Doc 07, and the 54.1 rubric; consolidation at 54.11 catches weak findings.

## Context

STEP-54 critiques each feature as a cohesive lifecycle (List → Form sheet → Detail → Report dialog) across Web (desktop) and Android. This substep covers **Inventory Management** — the stock dashboard, item entry, stock adjustment modal, and inventory report. This feature has an unusual code placement you must know up front: **inventory lives under `lib/features/tracking/`** (shared feature module with cut/fill and land clearing), not its own `lib/features/inventory/` directory — its model lives in `lib/core/data/models/inventory_item_model.dart`. Keep the critique honest about this structure; if it creates cohesion problems (shared BLoC concerns, import tangles), that's a finding, not a fact to hide.

Preconditions: 54.0 (clean trunk, branch `step-0054-feature-cohesion-critique`), 54.1 (rubric in `mine-flow-STEP-54.1-FINDINGS.md`).

## Read these first

- `Upcoming Prompts/mine-flow-STEP-54-PLAN.md` — STEP PLAN (evidence standard, D1–D8, ground rules)
- `Upcoming Prompts/mine-flow-STEP-54.1-FINDINGS.md` — **the rubric**. Apply it exactly; IDs are `FC-54.8-NNN`.
- `Code/mine-flow-docs/reports/2026-09-10-step-54-55-design-blueprint.md` — D1–D8; blueprint §54.8 names this feature's surfaces
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` — UI canon
- `Code/mine-flow-docs/architecture/04-data-model.md` — inventory item semantics (stock levels, units, adjustments)
- `Code/mine-flow-app/README.md` + `ARCHITECTURE.md`
- root `.throughstone/local-user.md`

## Scope

**Surfaces** (paths as of 2026-09-10; re-locate on the branch head — under `lib/features/tracking/`):
- Dashboard: `lib/features/tracking/presentation/pages/inventory_dashboard_screen.dart`
- Item entry: `lib/features/tracking/presentation/pages/inventory_item_entry_screen.dart`
- Stock adjustment: `lib/features/tracking/presentation/pages/stock_adjustment_dialog.dart` (already a dialog — critique it against D6's `FDialog` language)
- Widgets: `lib/features/tracking/presentation/widgets/inventory_card.dart`, `inventory_summary_card.dart`
- Model: `lib/core/data/models/inventory_item_model.dart`
- Report path: navigation from dashboard to the reporting pages / `pdf_service.dart` — trace the actual path (contextual per D6 or redirect?); inventory report
- BLoC states: `lib/features/tracking/presentation/bloc/` (shared with cut/fill & land clearing — note the coupling)

**Does NOT touch:** application code (read-only), other features, the rubric.

## Your task

Apply every 54.1 rubric dimension, both platforms (Web desktop, Android portrait):

1. **Lifecycle cohesion:** dashboard → item entry → back; dashboard → stock adjustment → back; dashboard → report. All three loops traced; state survival each time.
2. **Stock dashboard:** how stock health (low/out/reorder) is expressed — thresholds visible? color-independence? summary-card vs. per-item detail balance.
3. **Item entry form → sheet migration spec:** D1/D2 changes; D4 dirty-intercept status; D5 deep-link gap — the router shows `teams/inventory` without a form subroute (verify) — record the gap.
4. **Stock adjustment modal:** already a dialog — critique it as the in-app precedent for D6's contextual-dialog language: scrim, sizing on each platform, keyboard handling on mobile (quantity entry), confirm/cancel ergonomics, and whether adjustment history is visible from it.
5. **Module placement:** `inventory` under `tracking` with shared BLoC — is there coupling-driven UI incoherence (e.g. tracking state leaking into inventory screens' loading/error states)? Record as a finding if so; 54.11 decides whether to spec a move (STEP-55 scope) or accept.
6. **Report dialog:** D6 conformance — pre-bound inventory ReportType, dashboard filters preserved.
7. **Interaction states, a11y, tokens:** all rubric dimensions; anchored-grep residual Material.
8. **D7 verdict:** detail view per item (stock history?) or dashboard+entry suffices?

## Verification (evidence standard — mandatory)

- Every finding: `FC-54.8-NNN` ID, verdict (`Aligned`/`Needs polish`/`Needs restructure`/`Unverified`), `file:line` citation, one-sentence why (Explanatory style).
- Runtime optional and honest: name the command, report artifact byte-size + pixel dimensions; 1×1-placeholder class = harness-defect call-out. Unverifiable → `Unverified` + blocker.
- No code changes: app repo `git status` clean at the end.
- Findings file: `Upcoming Prompts/mine-flow-STEP-54.8-FINDINGS.md` — coverage table, findings table, verification record, limitations.

## Keeping the docs true  (always)

- Findings only — no doc edits (54.11 consolidates). Escalate (and record) on: D1–D8/ADR conflicts, runtime contradicting Doc 07, unevidenced runtime claims, same classification problem twice. **Stock-count integrity findings** (adjustment applied twice, silent failure losing an adjustment) are data-integrity class — escalate prominently, do not bury as polish.
- Accepted-risk-shaped discoveries go to findings for 54.11's reconciliation.

## Definition of done

- [ ] All rubric dimensions scored, both platforms, including the stock-adjustment-dialog-as-D6-precedent critique.
- [ ] Module placement (inventory-under-tracking) assessed and recorded.
- [ ] D4/D5 status and D7 verdict recorded.
- [ ] Coverage/findings/verification/limitations tables present with IDs and citations.
- [ ] No application code or docs modified.

## Next

Update the PLAN's substep table (54.8 → Done) and tell the user: *"run substep 54.9"* — in a **fresh chat**.
