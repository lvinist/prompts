# mine-flow — STEP-29.1: Update Architecture 07-doc to v0.2.0

> **How to run:** Tell your agent *"run substep 29.1"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat. Write it so
> nothing depends on the conversation that produced it.

## Context
This STEP reconciles the UI design system. Currently, `architecture/07-ui-design-system.md` v0.1.0 specifies a custom `ThemeData` (Forest & Stone), which conflicts with the Phase 2 direction (ForUI package + FThemes.zinc) that Impeccable expects. This substep formalizes the ForUI direction by rewriting the 07-doc to v0.2.0.

## Read these first
- overview.md
- architecture/07-ui-design-system.md

## Scope
- Update `architecture/07-ui-design-system.md`.

## Your task
1. Rewrite `architecture/07-ui-design-system.md` to specify the ForUI package + `FThemes.zinc` (default, no brand override) as the canonical design system.
2. Ensure the document clearly states that custom `ThemeData` is replaced by the ForUI defaults.
3. Update the Version from v0.1.0 to v0.2.0.
4. Add a Version Log entry for v0.2.0 under STEP-29.

## Verification
- N/A - Docs only substep.

## Keeping the docs true (always)
Updates `07-ui-design-system.md`.

## Definition of done
- [ ] Code this substep wrote or changed is covered by the relevant tests named above, and
      those tests either pass now or are assigned to the STEP's final verification substep.
- [ ] New/changed classes, functions, and methods carry docstrings.
- [ ] Any architecture decision this substep changed is reflected in the docs (Version Log
      bumped).
- [ ] Any accepted risk or deferred technical debt created or changed by this substep is
      recorded in `registries/risks.yml` or explicitly marked not applicable.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user the next
action: the next open substep — *"run substep 29.2"*, in a **fresh chat**.
