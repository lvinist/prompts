# mine-flow — STEP-34.1: Domain & Data Layer Refactor (GeospatialFile)

> **How to run:** Tell your agent *"run substep 34.1"* (or *"read and run this file"*).

## Context
This is part of STEP-34. We need to remove the unused latitude and longitude fields from the GeospatialFile data models because they are no longer needed in the Data Bucket feature.

## Read these first
- overview.md
- `Code/mine-flow-app/lib/features/data_bucket/domain/entities/geospatial_file.dart`
- `Code/mine-flow-app/lib/features/data_bucket/data/models/geospatial_file_model.dart`
- `Code/mine-flow-app/lib/features/data_bucket/data/models/geospatial_file_adapter.dart`

## Scope
Updates to the domain entity and data models for GeospatialFile. Does NOT include UI changes yet.

## Your task
1. Edit `geospatial_file.dart` to remove the `latitude` and `longitude` fields entirely.
2. Edit `geospatial_file_model.dart` to remove `latitude` and `longitude` from the JSON serialization and object instantiation.
3. Edit `geospatial_file_adapter.dart` to ignore or remove the lat/lon fields from Hive serialization, ensuring we don't break existing boxes (or increment the adapter type if needed).
4. Update `Code/supabase/migrations/` (if there's a schema) or create a script/note to drop these columns from the `geospatial_files` table in Supabase.

## Verification
- Unit tests for the data bucket models must be updated to remove lat/lon assertions.
- Verify `flutter test test/features/data_bucket` passes (assigned to final verification substep).

## Keeping the docs true (always)
- Update any architecture docs if Data Bucket schema is heavily documented (e.g., `architecture/04-data-model.md`), bumping version.

## Definition of done
- [ ] Lat/lon removed from entity and model.
- [ ] JSON and Hive serialization updated.
- [ ] Unit tests for data bucket updated.
- [ ] Architecture docs updated if necessary.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user the next action: the next open substep — *"run substep 34.2"*, in a **fresh chat**.
