# mine-flow — STEP-33.4: Tests & Verification

> **How to run:** Tell your agent *"run substep 33.4"* (or *"read and run this file"*).

## Context
This is the final substep for STEP-33 (Forms Refactor & Data Model Polish). In the previous substeps, we updated the Data Models, Repositories, and UI Presentation layers for Cut/Fill, Land Clearing, Daily Log, and Inventory tracking. Now, we must ensure all pieces wire together correctly from end-to-end (Form submission -> BLoC state -> Repository -> Sync Queue -> Local Storage / Supabase).

## Read these first
- `architecture/12-test-strategy.md`
- `Upcoming Prompts/mine-flow-STEP-33-PLAN.md`

## Scope
Writes and updates tests across all affected features and ensures the CI suite is fully passing.

## Your task
1. **Update Unit & Widget Tests**:
   - Update `test/features/tracking/presentation/` widget tests for Cut/Fill and Land Clearing forms to simulate input on the new fields (BCM, LCM, Material Type, Method, Plan Area, Actual Area).
   - Update BLoC tests to assert correct state emission with the new data payloads.
   - Update `test/features/daily_log/` and `test/features/tracking/` widget tests to verify the Combobox and Auto-predict behaviors.
2. **Integration Verification**:
   - Run the full integration test suite or explicitly write tests asserting that a full form submission successfully maps to the updated domain entities and is queued for sync.
3. **Execution**:
   - Run `flutter test`. Ensure all tests in the project pass successfully. If there are pre-existing test failures that were noted in prior steps (e.g. from the ForUI migration), evaluate whether they relate to these forms and fix them if they do.

## Verification
- **Run timing:** Run tests before marking this substep done.
- Command: `flutter test`
- All tests must pass.

## Keeping the docs true  (always)
- Ensure the Test Strategy doc remains accurate. If any new testing patterns for `CreatableCombobox` or auto-predict widgets were introduced, document them.

## Definition of done
- [ ] Widget and BLoC tests updated to reflect the new form inputs.
- [ ] `flutter test` completes successfully with 100% pass rate for the modified files.
- [ ] No analyzer warnings remain.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user to review the STEP, archive the files into `prompts/002-phase2-tier2/step-0033/`, and run `./doctor.sh status` to find the next STEP.
