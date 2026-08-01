# mine-flow — STEP-39.2: Architecture, ADR, dependency, risk, and bridge reconciliation

> **How to run:** Tell your agent *"run substep 39.2"* (or *"read and run this file"*).

## Context
This substep updates the architecture documentation to reflect the owner decisions locked in 39.1. It reconciles the UI design system drift and sets up the supply chain approval for the battery dependency.

## Read these first
- `Upcoming Prompts/mine-flow-STEP-39-PLAN.md`
- `Code/mine-flow-docs/architecture/07-ui-design-system.md`
- `Code/mine-flow-docs/architecture/15-native-app-architecture.md`
- `Code/mine-flow-docs/adr/README.md`
- `Code/mine-flow-docs/registries/risks.yml`

## Scope
Modify documentation, ADRs, risk registries, and generated bridge files. Do not modify implementation code in this substep.

## Your task
1. Update `07-ui-design-system.md` and `15-native-app-architecture.md` with the locked Typography (Geist) and Mobile Navigation (5 items) decisions. Bump their Version Logs.
2. Create `Code/mine-flow-docs/adr/ADR-0009-ui-design-system-drift.md` (Accepted) documenting these UI changes.
3. Review `registries/risks.yml` for any open UI/UX or battery syncing risks and update them.
4. Perform the dependency supply-chain review for `battery_plus` (version `^6.0.0` or `^5.0.3` as compatible) and document its approval for use in 39.5.
5. Regenerate `DESIGN.md` and `PRODUCT.md` at the repository root.
6. Run the Impeccable bridge generation to normalize UI tokens if applicable.
7. Validate all modified documentation and links.

## Verification
- Run documentation link checks if available.
- Compare bridge output to ensure no unexpected deletions.

## Keeping the docs true
This substep is exclusively dedicated to keeping the docs true.

## Definition of done
- [ ] Architecture docs updated and Version Logs bumped.
- [ ] ADR-0009 created.
- [ ] Risks reviewed.
- [ ] `battery_plus` vetted and supply-chain review complete.
- [ ] `DESIGN.md` and `PRODUCT.md` regenerated.
- [ ] Normalized bridge comparison passed.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user the next action: *"run substep 39.3"*, in a **fresh chat**.
