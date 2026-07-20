# mine-flow — STEP-11.1: Responsive UI Shell & Navigation

> **How to run:** Tell your agent *"run substep 11.1"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat. Write it so
> nothing depends on the conversation that produced it.

## Context
Phase 1 (MVP) implemented all core features, but the global navigation shell was left as a temporary placeholder grid in `router.dart`. The architecture calls for a `shadcn-admin` inspired responsive shell: a collapsible left sidebar on desktop/web, and a bottom tab bar on mobile. We need to implement this shell and wire it up to our existing routes.

## Read these first
- overview.md
- architecture/07-ui-design-system.md
- `lib/app/router.dart`
- `lib/app/theme/app_theme.dart`

## Scope
Implement the main application shell using `GoRouter`'s `ShellRoute` (or `StatefulShellRoute`). Replace the root `/` navigation with this shell. Ensure it is responsive. Add a dark/light mode toggle.

## Your task
1. Refactor `lib/app/router.dart` to use a `StatefulShellRoute` (or standard `ShellRoute` if simpler) for the main authenticated area of the app.
2. Create `lib/app/presentation/widgets/app_shell.dart` containing the responsive layout:
   - Use `LayoutBuilder` to detect screen width.
   - For wide screens (> 600px), display a collapsible `NavigationRail` or custom sidebar on the left.
   - For narrow screens, display a `NavigationBar` (bottom tabs).
3. The navigation options should include: Dashboard (`/`), Data Bucket (`/data-bucket`), Reports (`/reports`), Timeline (`/timeline`), and Notifications (`/notifications`).
4. Add a dark/light mode toggle button (either in the sidebar footer or top app bar) that updates a global theme state (e.g. via a new or existing Cubit).
5. Update `main.dart` or `app.dart` to listen to the theme state so the toggle actually works.

## Verification
- Run `flutter analyze` to ensure no new warnings.
- Run `flutter test` to ensure existing tests pass. Update `router.dart` tests if necessary.
- Verify visually by resizing the window if possible, or explain how the `LayoutBuilder` guarantees responsiveness.

## Keeping the docs true  (always)
- Since this fulfills the UI design system mandate, no architecture docs need changing.

## Definition of done
- [ ] `ShellRoute` is active in `router.dart`.
- [ ] `app_shell.dart` provides responsive sidebar/bottom nav.
- [ ] Theme toggle is implemented and functional.
- [ ] Tests pass.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user the next action: *"run substep 11.2"*, in a **fresh chat**.
