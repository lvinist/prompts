# mine-flow — STEP-34.4: Tests & Verification

> **How to run:** Tell your agent *"run substep 34.4"* (or *"read and run this file"*).

## Context
This is the final verification substep for STEP-34, ensuring the data bucket tweaks and reporting integration haven't broken the test suite.

## Scope
Test directories and full suite execution.

## Your task
1. Run `flutter test`.
2. Fix any remaining failing tests due to the removal of lat/lon or the router changes.
3. If integration tests for reporting navigation exist, update them to trigger the new `FAppBar` actions instead of navigating via the central dashboard.

## Verification
- `flutter test` completes successfully.

## Definition of done
- [ ] Entire test suite passes.
- [ ] No analyzer warnings.

## Next
When this substep is done, mark the STEP as Done in `prompts/STEP-index.md` and archive the loose files into `prompts/001-mvp/step-0034/`. Then run `doctor.sh status` to find the next action.
