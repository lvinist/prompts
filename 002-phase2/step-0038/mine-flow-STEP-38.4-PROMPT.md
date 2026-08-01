# mine-flow — STEP-38.4: Inventory Form and Land Clearing Tab Layout

## Substep Prompt

Follow the `mine-flow-STEP-38-PLAN.md` for substep 38.4.
1. In `inventory_item_entry_screen.dart`, merge the Jumlah and Satuan inputs into a single row using a numeric text field and a unit dropdown/select.
2. In `land_clearing_entry_screen.dart`, restructure the form into a tabbed layout (Plan tab, Actual tab) using `DefaultTabController` and `TabBarView` (styled with ForUI).

## Verification

Update widget tests for both screens to verify the new layout and tab structure. Run `flutter analyze` and `flutter test`.
