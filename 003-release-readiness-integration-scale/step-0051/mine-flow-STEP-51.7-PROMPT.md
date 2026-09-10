# mine-flow — STEP-51.7: CF-043 structural half — one shared method control

> **How to run:** Tell your agent *"run substep 51.7"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.
>
> **Assigned model: Gemini 3.1 Pro High.** This is a behaviour-carrying form redesign
> bounded by ADR-0015's plan/actual model, plus a widget test that must assert the *shared
> state* semantics — judgement about what the assertion should prove, not a mechanical swap.

## Context

STEP-51 closes UI debt from STEP-46. CF-043's structural half is still open: the
land-clearing entry screen has **two independent `CreatableCombobox<String>` controls both
writing `record.method`** — at
`lib/features/tracking/presentation/pages/land_clearing_entry_screen.dart:373` and `:486`
(line numbers as of 2026-09-09; re-locate on the branch head), both fed by
`_clearingMethods` (defined `:98`). The register (STEP-46.3) asked to (a) constrain
`method` to the enumerated set and (b) use one shared control instead of two.

Note: STEP-48.30 already removed the dead `Tambah "…"` affordance and reported this
residual. Read the PLAN and **51.1's findings** (which re-verified the defect's presence).

## Read these first

- `Upcoming Prompts/mine-flow-STEP-51-PLAN.md` (decisions D2/D3, ground rules)
- `Upcoming Prompts/mine-flow-STEP-51.1-FINDINGS.md` (CF-043 verification + register
  appendix context)
- Root `.throughstone/local-user.md`
- `Code/mine-flow-docs/adr/ADR-0015-plan-actual-date-zone-separation.md` (the plan/actual
  model this control must follow)
- `Code/mine-flow-docs/architecture/07-ui-design-system.md`
- `Code/mine-flow-docs/architecture/12-test-strategy.md`
- The screen: `lib/features/tracking/presentation/pages/land_clearing_entry_screen.dart`
- Its bloc: `lib/features/tracking/presentation/bloc/land_clearing/` (find
  `MethodChangedEvent`)
- `Code/mine-flow-app/README.md`

## Scope

**Owns:** the land-clearing entry screen's method control; the
`MethodChangedEvent`/normalisation path if needed; a widget test for the shared-value
semantics.

**Does NOT touch:** other fields on that screen; the land-clearing list screen; data model
or persistence (`record.method` stays a string — constraining is UI/bloc-level validation
per the register's intent, **unless** ADR-0015's model dictates otherwise, in which case
escalate before changing the model); any other CF finding (51.8's lane).

## Your task

1. **Constrain the method to the enumerated set.** The control must offer
   `_clearingMethods` and reject/normalize values outside it (decide with ADR-0015 in
   view: the register's phrase is "constrain `method` to the enumerated set"). If
   constraining requires a schema/model change rather than UI-level validation — **stop and
   escalate**; that changes the data model and needs an ADR, not a substep decision.
2. **Collapse two controls into one shared control.** Both tabs (plan/actual per
   ADR-0015) edit the same normalised `record.method` through one control — not two
   comboboxes that can drift. Preserve the existing label ('Metode Clearing') and icon.
3. **Widget test:** assert that editing the method on one tab is reflected on the other —
   the shared-value semantics is exactly what the old design broke. Also assert an
   out-of-set value cannot be committed (the constraint half). Cite `CF-043` in a comment
   on the test.

## Verification

- `flutter test` full suite → green, count+delta stated (+2 or more new cases).
- `flutter analyze` → 0; `dart format --set-exit-if-changed` → clean.
- Grep: exactly **one** `CreatableCombobox` (or its replacement) bound to
  `record.method` in that file.
- The new widget test fails against the pre-change code (sanity-check the test proves
  something: stash/checkout dance or just reason it through and state how).

## Keeping the docs true

CF-043 is recorded in the STEP-46.3 register; 51.1's appendix already states the residual.
On completion your findings note CF-043's structural half is closed — 51.10 finalizes the
register. If you had to change the data model (you should not, without escalation), that's
an ADR + Doc 04 update.

## Definition of done

- [ ] One shared method control; `record.method` constrained to `_clearingMethods`.
- [ ] Widget test asserts shared-value semantics + constraint, citing CF-043.
- [ ] `flutter analyze` 0, format clean, full `flutter test` green with count+delta.
- [ ] Findings `Upcoming Prompts/mine-flow-STEP-51.7-FINDINGS.md`; PLAN row updated.

## Escalation (to Opus 4.8 — record in findings if fired)

- Any change that would touch the data model/schema (ADR territory).
- ADR-0015's plan/actual model appearing to contradict the register's ask.
- Data-integrity-shaped results (method values not round-tripping).
- Same fix failing twice.

## Next

Tell the user the next open substep (51.8/51.9 if not done, else 51.10). In a
**fresh chat**.
