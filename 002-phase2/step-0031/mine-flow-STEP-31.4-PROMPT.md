# mine-flow — STEP-31.4: Test Suite Verification & Fixes

> **How to run:** Tell your agent *"run substep 31.4"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat. Write it so
> nothing depends on the conversation that produced it.

## Context
This is the final verification substep for STEP-31. The AppShell has been implemented, responsive UI created, and feature routes regrouped. This substep ensures all tests are updated to reflect the new `StatefulShellRoute` paradigm and that the app passes its CI gates.

## Read these first
- overview.md
- architecture/12-test-strategy.md
- coding-standards/README.md

## Scope
Test updates only. No feature code should be written in this substep unless it is a bug fix directly required to make tests pass.

## Your task
1. Update any existing widget tests for `DashboardPage` to account for its new scoped role.
2. Add widget tests for `AppShell` verifying that it renders `Sidebar` on wide screens and `FBottomNavigationBar` on narrow screens.
3. Add router tests verifying that the 3 branches resolve correctly and maintain state.
4. Run the full `flutter test` suite. Fix any pre-existing router mock errors caused by the shell route migration.

## Verification
- Run `flutter test`. All tests must pass.

## Keeping the docs true (always)
- If the testing paradigm for routing changed, update `12-test-strategy.md`, though standard flutter testing applies.

## Definition of done
- [ ] `AppShell` is fully covered by widget tests.
- [ ] `DashboardPage` tests are updated.
- [ ] Router tests verify the 3 branches.
- [ ] `flutter test` passes with zero failures.
- [ ] STEP review is prepared.

## Next
When this substep is done, update its status in the STEP PLAN.
This is the last substep. Tell the user to run the **STEP review** (PR/code review + doc drift check), gather all STEP files from `Upcoming Prompts/` into `prompts/002-public-beta/step-0031/` (or whichever Phase folder applies), mark STEP-31 `Done` in `prompts/STEP-index.md`, and ask for the next action.
