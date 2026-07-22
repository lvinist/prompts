# mine-flow — STEP-29.3: Impeccable Bridge Script

> **How to run:** Tell your agent *"run substep 29.3"* (or *"read and run this file"*).

## Context
Impeccable needs `PRODUCT.md` and `DESIGN.md` at the workspace root to function, but these drift from the canonical architecture. To solve this, we are creating a bridge script that regenerates them from `07-ui-design-system.md` immediately before Impeccable runs.

## Read these first
- architecture/07-ui-design-system.md

## Scope
- Create `Code/mine-flow-docs/scripts/impeccable-bridge.ps1`.

## Your task
1. Create `Code/mine-flow-docs/scripts/impeccable-bridge.ps1` (a PowerShell script).
2. The script should read `Code/mine-flow-docs/architecture/07-ui-design-system.md` and extract the design and product rules (e.g. ForUI direction, Tokens, components).
3. The script writes this extracted content into `DESIGN.md` and `PRODUCT.md` at the workspace root.
4. Add a comment header in the script explaining its purpose as the bridge for the Impeccable UI workflow.
5. Provide instructions in the terminal output when the script runs.

## Verification
- Run `.\Code\mine-flow-docs\scripts\impeccable-bridge.ps1` in PowerShell.
- Verify that `DESIGN.md` and `PRODUCT.md` are updated correctly at the workspace root.

## Keeping the docs true (always)
The script itself keeps the docs true by preventing drift.

## Definition of done
- [ ] Code this substep wrote or changed is covered by the relevant tests named above, and
      those tests either pass now or are assigned to the STEP's final verification substep.
- [ ] New/changed classes, functions, and methods carry docstrings.
- [ ] Any architecture decision this substep changed is reflected in the docs.
- [ ] Any accepted risk or deferred technical debt created or changed by this substep is
      recorded in `registries/risks.yml` or explicitly marked not applicable.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user the next
action: run the STEP's review.
