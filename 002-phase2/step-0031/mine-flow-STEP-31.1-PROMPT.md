# mine-flow — STEP-31.1: Shell Routing & Scaffolding

> **How to run:** Tell your agent *"run substep 31.1"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat. Write it so
> nothing depends on the conversation that produced it.

## Context
We are implementing a persistent responsive navigation shell for Phase 2 Tier 2. The current `DashboardPage` uses standard `GoRoute` pushes which replace the entire screen. This substep is responsible for setting up `StatefulShellRoute` in `go_router` and scaffolding the `AppShell` widget that will persist across the main tabs.

## Read these first
- overview.md
- architecture/07-ui-design-system.md
- coding-standards/README.md
- `mine-flow-app/README.md`

## Scope
This substep ONLY creates the `StatefulShellRoute` architecture in `lib/app/router.dart` and scaffolds a basic `AppShell` widget in `lib/app/presentation/pages/app_shell.dart`. It does NOT implement the final ForUI sidebar or bottom navbar yet (that's 31.2).

## Your task
1. Modify `lib/app/router.dart` to use `StatefulShellRoute.indexedStack`.
2. Define the five main branches matching our feature groupings:
   - Branch 1: Dashboard
   - Branch 2: Tools (Data Bucket)
   - Branch 3: Operations (Cut/fill, Land Clearing, Benchmark DB)
   - Branch 4: Teams (Attendance, Eq Check, Daily Log, Inventory)
   - Branch 5: Settings
3. Create `lib/app/presentation/pages/app_shell.dart` containing an `AppShell` stateless widget. It should receive the `navigationShell` from the router and display a basic `Scaffold` where the `body` is the current branch.

## Verification
- Run `flutter test` to ensure router modification doesn't break basic initialization tests.
- Run timing: defer full coverage of shell transitions to 31.4.

## Keeping the docs true (always)
- Update repo architecture doc if routing paradigm changes are significant, though this is purely implementation of standard `go_router`.

## Definition of done
- [ ] `lib/app/router.dart` successfully implements `StatefulShellRoute` with 5 branches.
- [ ] `lib/app/presentation/pages/app_shell.dart` is created and displays the current branch.
- [ ] Tests pass (or are deferred to 31.4).
- [ ] Docstrings added to new components.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user the next action: *"run substep 31.2"*, in a **fresh chat**.
