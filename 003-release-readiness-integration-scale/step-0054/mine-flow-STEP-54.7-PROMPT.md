# mine-flow — STEP-54.7: Teams Suite 3 — Equipment Digital Checks Critique

> **How to run:** Tell your agent *"run substep 54.7"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.

**Assigned model: Gemini 3.1 Pro High.** Real design critique, bounded by blueprint D1–D8, Doc 07, and the 54.1 rubric; consolidation at 54.11 catches weak findings.

## Context

STEP-54 critiques each feature as a cohesive lifecycle (List → Form sheet → Detail → Report dialog) across Web (desktop) and Android. This substep covers **Equipment Digital Checks** — equipment history with status band headers, the SOP checklist inspection form, and inspection details. Blueprint D7 explicitly names this feature as an open detail-view question ("Equipment Check records" — side-sheet inspector vs. full page), so the D7 verdict here is a first-class deliverable, not a footnote.

Preconditions: 54.0 (clean trunk, branch `step-0054-feature-cohesion-critique`), 54.1 (rubric in `mine-flow-STEP-54.1-FINDINGS.md`).

## Read these first

- `Upcoming Prompts/mine-flow-STEP-54-PLAN.md` — STEP PLAN (evidence standard, D1–D8, ground rules)
- `Upcoming Prompts/mine-flow-STEP-54.1-FINDINGS.md` — **the rubric**. Apply it exactly; IDs are `FC-54.7-NNN`.
- `Code/mine-flow-docs/reports/2026-09-10-step-54-55-design-blueprint.md` — D1–D8, especially **D7's explicit mention of Equipment Check records**
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` — UI canon
- `Code/mine-flow-docs/architecture/04-data-model.md` — equipment check structure (SOP arrays, statuses, defects)
- `Code/mine-flow-app/README.md` + `ARCHITECTURE.md`
- root `.throughstone/local-user.md`

## Scope

**Surfaces** (paths as of 2026-09-10; re-locate on the branch head — under `lib/features/equipment_check/`):
- List: `lib/features/equipment_check/presentation/pages/equipment_history_screen.dart` (status band headers)
- Form: `lib/features/equipment_check/presentation/pages/equipment_check_form_screen.dart` (SOP checklist)
- Inspection details: locate the detail surface (part of the history screen? a route? verify) — this is the D7 exemplar
- Report path: verify whether this feature has a ReportType (blueprint doesn't name one for it — record presence/absence as a deliberate decision either way)
- BLoC states: `lib/features/equipment_check/presentation/bloc/`

**Does NOT touch:** application code (read-only), other features, the rubric.

## Your task

Apply every 54.1 rubric dimension, both platforms (Web desktop, Android portrait):

1. **Lifecycle cohesion:** equipment history → new check (SOP form) → back → inspection details. Trace all paths; where does the loop break?
2. **Status band headers:** how equipment status (OK / needs-attention / out-of-service or similar) is expressed — band semantics, color-independence, consistency with the badge language of other features (attendance, inventory).
3. **SOP checklist form:** the checklist ergonomics on mobile — item grouping, pass/fail/NA control sizes and reachability, defect-note entry when an item fails, progress indication through a long SOP. Is a partially-completed checklist recoverable (D4: accidental dismissal of a 30-item checklist is the worst-case dirty-loss in the app)?
4. **D7 verdict (first-class deliverable):** inspection details as side-sheet inspector vs. full page. Consider: how much content an inspection record holds (SOP results + defect notes + metadata), how often details are consulted vs. entered, and platform split (inspector sheet on Web pairs naturally with D1; on Mobile a full page may be right). Give a verdict + rationale 54.11 can consolidate without re-deriving.
5. **Form → sheet migration spec:** D1/D2 changes for the SOP form; D4 dirty-intercept status today; D5 deep-link gap — the router shows `equipment-check/form` exists; verify and critique its semantics (does the URL carry the equipment context?).
6. **Interaction states, a11y, tokens:** all rubric dimensions; anchored-grep residual Material.
7. **Report path:** presence/absence verified and recorded as a deliberate decision.

## Verification (evidence standard — mandatory)

- Every finding: `FC-54.7-NNN` ID, verdict (`Aligned`/`Needs polish`/`Needs restructure`/`Unverified`), `file:line` citation, one-sentence why (Explanatory style).
- Runtime optional and honest: name the command, report artifact byte-size + pixel dimensions; 1×1-placeholder class = harness-defect call-out. Unverifiable → `Unverified` + blocker.
- No code changes: app repo `git status` clean at the end.
- Findings file: `Upcoming Prompts/mine-flow-STEP-54.7-FINDINGS.md` — coverage table, findings table, verification record, limitations.

## Keeping the docs true  (always)

- Findings only — no doc edits (54.11 consolidates). Escalate (and record) on: D1–D8/ADR conflicts, runtime contradicting Doc 07, unevidenced runtime claims, same classification problem twice.
- Accepted-risk-shaped discoveries go to findings for 54.11's reconciliation.

## Definition of done

- [ ] All rubric dimensions scored, both platforms, with the SOP-checklist mobile ergonomics addressed in depth.
- [ ] **D7 verdict for inspection details recorded with full rationale** (a 54.11 consolidation input).
- [ ] D4 dirty-intercept status (partial-checklist recovery included) and D5 status recorded.
- [ ] Report-path presence/absence recorded as a deliberate decision.
- [ ] Coverage/findings/verification/limitations tables present with IDs and citations.
- [ ] No application code or docs modified.

## Next

Update the PLAN's substep table (54.7 → Done) and tell the user: *"run substep 54.8"* — in a **fresh chat**.
