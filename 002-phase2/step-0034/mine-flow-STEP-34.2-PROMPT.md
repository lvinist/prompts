# mine-flow — STEP-34.2: Data Bucket UI Refactor

> **How to run:** Tell your agent *"run substep 34.2"* (or *"read and run this file"*).

## Context
This is part of STEP-34. The data models no longer have latitude and longitude. Now we must remove them from the user interface.

## Read these first
- `Code/mine-flow-app/lib/features/data_bucket/presentation/pages/upload_file_page.dart`
- `Code/mine-flow-app/lib/features/data_bucket/presentation/pages/data_bucket_list_page.dart`
- `Code/mine-flow-app/lib/features/data_bucket/presentation/pages/file_detail_page.dart`

## Scope
UI screens within the Data Bucket feature only.

## Your task
1. In `upload_file_page.dart`, remove the text fields or input widgets for latitude and longitude. Remove any associated form controllers.
2. In `data_bucket_list_page.dart`, if lat/lon is displayed in the list tile or metadata, remove it.
3. In `file_detail_page.dart`, remove the display rows for latitude and longitude.

## Verification
- Run `flutter analyze` to ensure no orphaned variables remain.
- Ensure the widget tests for Data Bucket pages (if any) are updated to not expect lat/lon fields.

## Keeping the docs true (always)
- No architecture changes expected here.

## Definition of done
- [ ] Lat/lon inputs removed from upload page.
- [ ] Lat/lon removed from detail and list views.
- [ ] Analyzer passes clean.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user the next action: the next open substep — *"run substep 34.3"*, in a **fresh chat**.
