# mine-flow — STEP-11.4: Code Quality Polish (Lint Fixes)

> **How to run:** Tell your agent *"run substep 11.4"* (or *"read and run this file"*).

## Context
During the STEP-10 check-in, 92 non-fatal Flutter analyzer warnings were found (recorded as RISK-0002). These are mostly `prefer_const_constructors`, `prefer_const_literals_to_create_immutables`, and deprecated method usages like `Color.withOpacity()` instead of `Color.withValues()`. We need to fix these before calling Phase 1 truly complete.

## Read these first
- `registries/risks.yml` (RISK-0002)

## Scope
Perform a global lint fix pass across the `mine-flow-app` codebase.

## Your task
1. Run `flutter analyze` in `Code/mine-flow-app` to get the list of warnings.
2. Fix all `prefer_const_constructors` and `prefer_const_literals_to_create_immutables` warnings.
3. Fix all deprecated usages, particularly `Color.withOpacity()` -> `Color.withValues(alpha: ...)`.
4. Ensure `flutter analyze` returns "No issues found!".
5. Update `registries/risks.yml` to mark RISK-0002 as `closed`, adding the current date and reason ("Fixed in STEP-11").

## Verification
- `flutter analyze` must return 0 issues.
- `flutter test` must pass.

## Keeping the docs true  (always)
- `registries/risks.yml` updated.

## Definition of done
- [ ] 0 analyzer warnings.
- [ ] RISK-0002 closed.
- [ ] Tests pass.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user the next action: *"run substep 11.5"*, in a **fresh chat**.
