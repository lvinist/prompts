# mine-flow — STEP-39.2.F2: Substep 39.2 Completion Corrections

> **How to run:** Tell your agent *"run substep 39.2.F2"* (or *"read and run this file"*).

## Context
Substeps 39.2 and 39.2.F1 were executed but left three gaps that must be closed
before substep 39.2 can be marked complete:

1. **`battery_plus` version constraint never recorded.** The supply-chain review
   determined `^7.1.1` is the correct constraint, but ADR-0010 only mentions
   `battery_plus` generically. Substep 39.5 (implementation) needs an
   unambiguous, recorded constraint to depend on.
2. **`registries/risks.yml` was not updated.** The original 39.2 prompt
   (task 3) required reviewing risks. RISK-0003 ("Phase 2 UI spacing and color
   drift bugs deferred") is still `open` even though ADR-0009 formalized the
   UI drift decisions. Its status and mitigation need reconciliation.
3. **STEP-39 PLAN Definition of Done not updated.** The 39.2 and 39.2.F1
   checkboxes are still unchecked.

## Read these first
- `Upcoming Prompts/mine-flow-STEP-39-PLAN.md` — current PLAN (especially the
  DoD section and the substep 39.2 row)
- `Code/mine-flow-docs/adr/ADR-0010-low-battery-sync-rule.md` — needs the
  version constraint
- `Code/mine-flow-docs/registries/risks.yml` — needs RISK-0003 reconciliation
- `Upcoming Prompts/mine-flow-STEP-39.2-PROMPT.md` — original requirements
  (compare task 3 and task 4 against what was actually delivered)

## Scope
Documentation only. Do **not** modify implementation code.

## Your task

### 1. Pin `battery_plus ^7.1.1` in ADR-0010
Add a `## Dependency Constraint` section (or append to Consequences) in
`Code/mine-flow-docs/adr/ADR-0010-low-battery-sync-rule.md` recording:

```
- **Package:** `battery_plus`
- **Constraint:** `^7.1.1`
- **Vetted against:** Flutter ≥ 3.22.0, Dart ≥ 3.4.0 <4.0.0, Java 17,
  Kotlin 2.2.0, AGP ≥ 8.12.1, Gradle ≥ 8.13, compile SDK API 34+, iOS 12.0+
- **App baseline:** Flutter 3.44.5, Dart 3.12.2
```

This ensures substep 39.5 can pick up the constraint without re-deriving it.

### 2. Reconcile RISK-0003 in `registries/risks.yml`
RISK-0003 tracks "Phase 2 UI spacing and color drift bugs deferred."
ADR-0009 (accepted in 39.2) formalized the two largest drift items (Geist font
and 5-item nav). Evaluate:

- If the remaining spacing/color drift bugs catalogued in the STEP-28.1 audit
  have been addressed by the ForUI rebuild (STEP-30) and subsequent STEPs,
  **close** RISK-0003 with date `2026-07-29` and reason
  `"UI drift formalized in ADR-0009; remaining items resolved in STEP-30+ ForUI rebuild."`.
- If drift bugs **remain** beyond what ADR-0009 and the ForUI rebuild cover,
  **amend** RISK-0003's `mitigation` and `refs` to reference ADR-0009, and
  update `revisit_trigger` to target the specific remaining items.

Use your judgment based on the current codebase state.

### 3. Update STEP-39 PLAN Definition of Done
In `Upcoming Prompts/mine-flow-STEP-39-PLAN.md`, mark:
- `[x] 39.2` — completed
- `[x] 39.2.F1` — completed

### 4. Commit
Commit all changes to the `step-0039-check-in` branch in `Code/mine-flow-docs`
with message: `docs(39.2.F2): pin battery_plus constraint, reconcile RISK-0003, update DoD`

## Verification
- Confirm ADR-0010 now contains a concrete version constraint.
- Confirm `risks.yml` RISK-0003 status is either `closed` or has updated
  mitigation/refs.
- Confirm STEP-39 PLAN DoD shows 39.2 and 39.2.F1 as `[x]`.
- Run `links.sh` or equivalent link validation if available.

## Definition of done
- [ ] ADR-0010 records `battery_plus ^7.1.1` with compatibility matrix.
- [ ] RISK-0003 reconciled (closed or amended with ADR-0009 reference).
- [ ] STEP-39 PLAN DoD checkboxes for 39.2 and 39.2.F1 marked complete.
- [ ] Changes committed and pushed on `step-0039-check-in`.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the
user the next action: *"run substep 39.3"*, in a **fresh chat**.
