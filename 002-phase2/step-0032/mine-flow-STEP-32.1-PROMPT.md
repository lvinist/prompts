# mine-flow — STEP-32.1: Zone Hive Adapter & Local Storage

> **How to run:** Tell your agent *"run substep 32.1"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat. Write it so
> nothing depends on the conversation that produced it.

## Context
We are implementing a dynamic `CreatableCombobox` for Zones in Phase 2 Tier 2. To support offline creation and dynamic reading of zones (which are currently hardcoded mock data in `zone_picker.dart`), we need to persist zones locally using Hive. 
In this substep, we will create the Hive adapter for `ZoneModel` and ensure `ZoneRepository` (or the local data source) is wired up to store and retrieve zones.

## Read these first
- `overview.md`
- `architecture/04-data-model.md`
- `ADR-0004-offline-first-sync.md`
- `ADR-0006-local-storage-hive.md`
- `lib/core/data/models/zone_model.dart`
- `lib/core/domain/entities/zone_entity.dart`
- `Code/mine-flow-app/README.md`

## Scope
This substep ONLY handles the local data layer (Hive adapter generation, local data source/repository updates for `Zone`). Do NOT touch the UI or BLoC in this substep.

## Your task
1. Create `ZoneHiveAdapter` or update `ZoneModel` to support Hive serialization (e.g., using `hive_generator` if that's the established pattern, or manual TypeAdapter).
2. Register the Zone adapter in `hive_registrar.dart` or wherever Hive adapters are registered.
3. Update or create the local data source (`ZoneLocalDataSource`) to provide `getZones()` and `saveZone(ZoneModel)` methods using a dedicated Hive box for Zones.
4. Ensure `ZoneRepository` has methods to fetch all zones and save a newly created zone locally.

## Verification
- Write unit tests for `ZoneLocalDataSource` and `ZoneRepository` to verify that zones can be saved to and retrieved from the local Hive box.
- Run `flutter test` on the new tests to verify.

## Keeping the docs true (always)
If you add a new Hive box, ensure `ADR-0006` or `04-data-model.md` are updated if they specifically list the active boxes.

## Definition of done
- [ ] Hive TypeAdapter for Zone created and registered.
- [ ] `ZoneLocalDataSource` and `ZoneRepository` methods for saving and fetching zones are implemented.
- [ ] Unit tests for the local storage logic are written and pass.
- [ ] New/changed classes carry docstrings.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user the next action: *"run substep 32.2"*, in a **fresh chat**.
