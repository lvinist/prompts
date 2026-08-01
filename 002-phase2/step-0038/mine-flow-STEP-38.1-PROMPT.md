# mine-flow — STEP-38.1: Button and AppBar Consistency

## Substep Prompt

Follow the `mine-flow-STEP-38-PLAN.md` for substep 38.1.
1. Remove any center/body-level add data buttons in Data Bucket, Inventory, Land Clearing, and Cut/Fill list screens.
2. Ensure every Add Data FButton in the FAppBar has both a prefix icon and label.
3. Add the Laporan (Report) icon button to the right of each Add Data FButton.
4. Update the Data Bucket form (`upload_file_page.dart`) to use a standard back-button FAppBar.

## Verification

Update or add widget tests for `data_bucket_list_page` and `inventory_dashboard_screen` to verify the new FAppBar structure. Run `flutter analyze` and `flutter test`.
