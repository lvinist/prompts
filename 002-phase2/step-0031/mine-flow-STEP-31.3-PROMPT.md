# mine-flow — STEP-31.3: Dashboard Cleanup & Regrouping Wiring

> **How to run:** Tell your agent *"run substep 31.3"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat. Write it so
> nothing depends on the conversation that produced it.

## Context
With the AppShell UI implemented (31.2), the navigation needs to wire up the actual feature screens into the five defined branches. The old `dashboard_page.dart` needs to be cleaned up to serve as the landing page for the first branch (Dashboard).

## Read these first
- overview.md
- architecture/07-ui-design-system.md
- coding-standards/README.md

## Scope
Wiring the existing routes into the 5 new groupings within the `StatefulShellRoute`. Refactoring `DashboardPage`.

## Your task
1. Update `lib/app/router.dart` to nest the existing routes under the correct StatefulShellBranch.
   - **Dashboard**: `DashboardPage` (reworked)
   - **Tools**: Data Bucket
   - **Operations**: Cut/Fill, Land Clearing (Benchmark DB is later)
   - **Teams**: Crew Attendance, Digital Equipment Check, Daily Log, Inventory
   - **Settings**: Setup an empty placeholder route for Settings (to be implemented in STEP-35)
   - *Note: Leave Reports, Timeline, and Notifications as standalone full-screen routes or integrate them into Dashboard as you see fit if they don't belong in the 5 main shell tabs.*
2. Refactor `DashboardPage` (`lib/app/presentation/pages/dashboard_page.dart`). Since it previously held all feature cards, pare it down or transform it to serve solely as the root dashboard (Stats, Reports access, Timeline access, Notifications access).
3. Ensure that when a user clicks a nav item in the sidebar/bottom navbar, the shell switches to the correct branch.

## Verification
- Test that all routes correctly resolve within their branch.
- Run timing: defer to 31.4.

## Keeping the docs true (always)
- N/A

## Definition of done
- [ ] All features are nested correctly under the 5 shell branches (or left as standalone routes if appropriate).
- [ ] `DashboardPage` is refactored to align with the new navigation paradigm.
- [ ] Tapping a tab navigates to the correct feature group without losing shell context.
- [ ] Tests pass (or deferred to 31.4).
- [ ] Docstrings added.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user the next action: *"run substep 31.4"*, in a **fresh chat**.
