# mine-flow — STEP-39.3: Analyzer and stale-test corrections

> **How to run:** Tell your agent *"run substep 39.3"* (or *"read and run this file"*).

## Context
This substep fixes minor code cleanliness issues (unused imports) found during the audit and investigates app-bar action expectation discrepancies requiring investigation in widget tests. Do not decide yet whether the tests are stale or the implementation regressed.

## Read these first
- `Upcoming Prompts/mine-flow-STEP-39-PLAN.md`
- `Code/mine-flow-app/lib/features/equipment_check/presentation/pages/equipment_history_screen.dart`
- `Code/mine-flow-app/test/features/tracking/presentation/inventory_dashboard_screen_test.dart`
- `Code/mine-flow-app/test/features/data_bucket/presentation/pages/data_bucket_list_page_test.dart`

## Scope
Modify only the files listed above. Do not attempt to fix `equipment_check_form_test.dart` here (that is 39.4).

## Your task
1. Remove the unused import in `equipment_history_screen.dart`.
2. Investigate app-bar action expectation discrepancies (`create_new_inventory_appbar_button` missing in `inventory_dashboard_screen_test.dart`, `upload_file_appbar_button` missing in `data_bucket_list_page_test.dart`). Compare each expectation against the relevant STEP PLAN and substep prompts, current architecture and UI contracts, current route and app-bar implementation, later STEP changes, and the intended user workflow. Only then update tests or restore implementation.
3. Run `flutter analyze` to confirm the analyzer is clean.

## Verification
- Run `flutter analyze` in `Code/mine-flow-app`.
- Run `flutter test test/features/tracking` and `flutter test test/features/data_bucket` to ensure the updated tests pass.

## Keeping the docs true
N/A

## Definition of done
- [ ] `equipment_history_screen.dart` cleaned.
- [ ] App-bar discrepancies investigated and resolved based on intended architecture and workflow.
- [ ] `flutter analyze` passes.
- [ ] Modified tests pass.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user the next action: *"run substep 39.4"*, in a **fresh chat**.
