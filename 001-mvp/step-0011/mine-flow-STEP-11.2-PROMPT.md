# mine-flow — STEP-11.2: Card-based Dashboard Stats

> **How to run:** Tell your agent *"run substep 11.2"* (or *"read and run this file"*).

## Context
Currently, the dashboard (`_DashboardPlaceholder`) is just a grid of navigation icons. We need an actual dashboard that displays summary statistics, styled after `shadcn-admin` (card-based, clean, subtle borders).

## Read these first
- overview.md
- `lib/app/router.dart`
- `lib/app/theme/app_theme.dart`

## Scope
Replace `_DashboardPlaceholder` with a new `DashboardPage` that includes stat summary cards.

## Your task
1. Extract `_DashboardPlaceholder` out of `router.dart` and into `lib/app/presentation/pages/dashboard_page.dart`.
2. Redesign `DashboardPage` to show a top row of summary stat cards (e.g., "Active Crew", "Total Cut/Fill Volume", "Equipment Checks", "Recent Notifications").
3. Since connecting real data might take too much time for a polish step, it is acceptable to use placeholder numbers (dummy data) or wire them up if simple repository methods exist. The goal is the *layout* and *design*.
4. Ensure the stat cards look premium: use `AppTheme` colors, subtle borders, and `Inter` typography.
5. Keep the quick navigation links (Data Bucket, Timeline, etc.) below the stat cards.

## Verification
- Run `flutter analyze`.
- Update any widget tests that expect `_DashboardPlaceholder` to now look for `DashboardPage`.

## Keeping the docs true  (always)
- N/A

## Definition of done
- [ ] `DashboardPage` replaces the placeholder.
- [ ] Includes at least 4 stat summary cards.
- [ ] Tests pass.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user the next action: *"run substep 11.3"*, in a **fresh chat**.
