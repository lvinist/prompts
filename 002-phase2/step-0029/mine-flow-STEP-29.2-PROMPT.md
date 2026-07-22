# mine-flow — STEP-29.2: ADR-0008, METHOD.md §7 Amendment & Close STEP-28.3

> **How to run:** Tell your agent *"run substep 29.2"* (or *"read and run this file"*).

## Context
We need to document the conflict between Impeccable's input files (`DESIGN.md` / `PRODUCT.md`) and the canonical architecture docs, and explicitly amend the hygiene rule in `METHOD.md` §7 to allow those two files at the root. We also need to officially defer the 28.1 UI audit findings to the upcoming ForUI rebuild (STEP-30+) instead of fixing them now.

## Read these first
- adr/README.md
- METHOD.md
- prompts/STEP-index.md
- registries/risks.yml

## Scope
- Write `ADR-0008`.
- Update `METHOD.md`.
- Update `prompts/STEP-index.md` and `registries/risks.yml`.

## Your task
1. Draft `Code/mine-flow-docs/adr/ADR-0008-impeccable-bridge.md` using the ADR template. Document the `DESIGN.md`/`07-doc` conflict and the resolution: `07-doc` is canonical, root files are generated bridged context for Impeccable. Add a note that this amends ADR-0007's silence on UI tokens.
2. Add the ADR to `adr/README.md`.
3. Edit `Code/mine-flow-docs/METHOD.md` §7 (Workspace-root hygiene). Add a named exception for `DESIGN.md` and `PRODUCT.md`, stating they are the Impeccable unversioned input contract and are allowed at the root.
4. Add an entry to `Code/mine-flow-docs/registries/risks.yml` noting that the STEP-28.1 UI spacing/color drift bugs are intentionally deferred (Tech Debt) because the screens will be rebuilt with ForUI in STEP-30+.
5. Update `prompts/STEP-index.md`: Change the status of STEP-28 to explicitly denote that Bug Fixes (28.3) were deferred to STEP-30+.

## Verification
- N/A - Docs only substep.

## Keeping the docs true (always)
This substep updates ADR, risks, METHOD, and index.

## Definition of done
- [ ] Code this substep wrote or changed is covered by the relevant tests named above, and
      those tests either pass now or are assigned to the STEP's final verification substep.
- [ ] New/changed classes, functions, and methods carry docstrings.
- [ ] Any architecture decision this substep changed is reflected in the docs.
- [ ] Any accepted risk or deferred technical debt created or changed by this substep is
      recorded in `registries/risks.yml` or explicitly marked not applicable.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user the next
action: the next open substep — *"run substep 29.3"*, in a **fresh chat**.
