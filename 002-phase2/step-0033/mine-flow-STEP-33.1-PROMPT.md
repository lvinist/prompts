# mine-flow — STEP-33.1: Data Model & Repository Polish

> **How to run:** Tell your agent *"run substep 33.1"* (or *"read and run this file"*).

## Context
As part of STEP-33 (Forms Refactor & Data Model Polish), we need to update our domain and data layers to support operational precision. Cut/Fill needs explicit volumetric separation (BCM and LCM columns) and material type tracking. Land Clearing needs differentiation between planned and actual values, and Daily Log/Inventory require some minor additions (zone/item constraints). This substep focuses strictly on the data foundation (Domain entities, Supabase remote DTOs, Hive local adapters, and Repositories). UI forms will be addressed in subsequent substeps.

## Read these first
- overview.md
- architecture/04-data-model.md
- architecture/07-ui-design-system.md
- `lib/features/tracking/domain/entities/cut_fill_measurement.dart`
- `lib/features/tracking/domain/entities/land_clearing_measurement.dart`
- `lib/features/daily_log/domain/entities/daily_log.dart`
- `lib/features/tracking/domain/entities/inventory_item.dart`
- `Upcoming Prompts/mine-flow-STEP-33-PLAN.md`

## Scope
Updates Domain Entities, Data Models, Hive adapters, and Supabase serialization for the 4 target features (Cut/Fill, Land Clearing, Daily Log, Inventory). Does not touch UI components, BLoC states, or routing.

## Your task
1. **Update `CutFillMeasurement` (and its Data Models)**:
   - Replace the generic `volume` field with explicit `bcmVolume` (Bank Cubic Meters) and `lcmVolume` (Loose Cubic Meters).
   - Add a `materialType` string/enum field.
   - Regenerate Hive type adapters and ensure Supabase JSON mapping uses the correct snake_case keys (`bcm_volume`, `lcm_volume`, `material_type`).
2. **Update `LandClearingMeasurement` (and its Data Models)**:
   - Add `method` string field for the combobox data.
   - Replace generic `areaCleared` with `planArea` and `actualArea`.
   - Update Hive adapters and Supabase JSON mappings accordingly.
3. **Update `DailyLog` & `InventoryItem`**:
   - Ensure `zone` in `DailyLog` is structured correctly to accept values from the `CreatableCombobox` built in STEP-32.
   - Ensure `InventoryItem` data models are structured to support auto-predict (e.g. tracking historical item names).
4. **Database Migration Script**:
   - If Supabase is strictly typed, write a `.sql` migration script (saved in `supabase/migrations/`) to alter the respective tables to include these new columns and remove the deprecated ones. (Coordinate with the answer to Q1 in the PLAN).

## Verification
- **Run timing:** Run tests before marking this substep done.
- Create or update unit tests in `test/features/tracking/data/models/` and `test/features/daily_log/data/models/` to assert that JSON serialization/deserialization and Hive adapter mapping correctly handle `bcmVolume`, `lcmVolume`, `materialType`, `planArea`, `actualArea`, etc.
- Run `flutter test` targeting the modified model tests to ensure they pass.

## Keeping the docs true  (always)
- Update `architecture/04-data-model.md` to reflect the new entity shapes for tracking measurements.

## Definition of done
- [ ] Entities and data models for Cut/Fill updated to include BCM, LCM, and Material Type.
- [ ] Entities and data models for Land Clearing updated to include Plan vs Actual and Method.
- [ ] Daily Log and Inventory models validated for Combobox/Predictive usage.
- [ ] Hive adapters regenerated successfully via build_runner.
- [ ] Unit tests for updated models pass.
- [ ] Any required Supabase SQL migration script is drafted.
- [ ] Architecture doc updated.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user the next action: *"run substep 33.2"* in a fresh chat.
