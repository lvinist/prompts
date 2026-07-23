# mine-flow — STEP-31.2: Navigation Shell UI (Desktop & Mobile)

> **How to run:** Tell your agent *"run substep 31.2"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat. Write it so
> nothing depends on the conversation that produced it.

## Context
In 31.1, the routing foundation was laid. This substep implements the actual UI for the `AppShell`. On desktop/tablet, it should display a collapsible sidebar. On mobile, it should display a ForUI `FBottomNavigationBar` with a collapsible menu icon instead of a traditional hamburger. It must also incorporate the Theme Toggle (dark/light) and a basic Profile Card within the shell.

## Read these first
- overview.md
- architecture/07-ui-design-system.md
- coding-standards/README.md
- `mine-flow-app/README.md`
- *forui documentation for `FBottomNavigationBar` and equivalent sidebar components*

## Scope
Implementation of the visual shell component responsive logic. No feature wiring yet (that's 31.3).

## Your task
1. Implement responsive layout logic in `lib/app/presentation/pages/app_shell.dart`. Use a breakpoint (e.g., `800px`) to switch between Desktop/Tablet (Sidebar) and Mobile (Bottom Navbar).
2. Desktop Sidebar:
   - Use ForUI tokens for colors/typography.
   - Include the five main groupings: Dashboard, Tools, Operations, Teams, Settings.
   - Include a Profile Card at the top or bottom of the sidebar.
   - Include the Theme Toggle button.
3. Mobile Bottom Navbar:
   - Use `FBottomNavigationBar` from `forui`.
   - Add a collapsible menu icon instead of a traditional hamburger icon for overflowing options or the sidebar drawer.
   - Move the Theme Toggle to an appbar or bottom sheet accessible from the mobile view if necessary.

## Verification
- Unit test responsive switching in `app_shell_test.dart` (mocking viewport sizes).
- Run timing: defer full coverage to 31.4.

## Keeping the docs true (always)
- No architecture doc changes expected.

## Definition of done
- [ ] Responsive `AppShell` switches layout based on breakpoint.
- [ ] Desktop uses ForUI-styled sidebar with theme toggle and profile, showing the 5 groupings.
- [ ] Mobile uses `FBottomNavigationBar` and a collapsible menu icon.
- [ ] Tests pass (or deferred to 31.4).
- [ ] Docstrings added.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user the next action: *"run substep 31.3"*, in a **fresh chat**.
