# mine-flow — STEP-32.3: Integration with ZonePicker & Testing

> **How to run:** Tell your agent *"run substep 32.3"* (or *"read and run this file"*).

## Context
With the Zone data layer supporting Hive persistence (32.1) and the shared `CreatableCombobox` widget built (32.2), we must now integrate them. The `ZonePicker` widget currently uses hardcoded mock data and `DropdownButtonFormField`. We will update it to use our new `CreatableCombobox` and wire it up to a BLoC/Cubit that manages the local Zone state.

## Read these first
- `lib/features/daily_log/presentation/widgets/zone_picker.dart`
- `lib/core/presentation/widgets/creatable_combobox.dart`
- `lib/core/domain/entities/zone_entity.dart`

## Scope
This substep updates the ZonePicker and introduces the necessary state management (BLoC/Cubit) to load zones from the local repository and handle the creation of new zones.

## Your task
1. Create `ZoneCubit` (or BLoC) to manage the list of zones, fetching them from `ZoneRepository`.
2. Add a method to `ZoneCubit` to create a new zone (generate a UUIDv4 for it, save to repository, and update state).
3. Update `ZonePicker` to wrap `CreatableCombobox`. It should listen to `ZoneCubit`, display the loaded zones, and call the create method when `onCreateNew` is triggered.
4. Ensure the UI gracefully handles the loading and empty states.

## Verification
- Write widget/integration tests for `ZonePicker` verifying that the cubit loads zones correctly and that creating a new zone updates the list.
- Run `flutter test` for the updated feature.

## Definition of done
- [ ] `ZoneCubit` created and tested.
- [ ] `ZonePicker` updated to use `CreatableCombobox` and wired to state.
- [ ] Widget/integration tests passing.
- [ ] The STEP 32 tests are fully verified.

## Next
When this substep is done, update its status in the STEP PLAN, mark the STEP as Done in the index, archive it to `prompts/001-mvp/step-0032/` (if Phase 1) or equivalent Phase 2 folder, and tell the user the next action using `doctor.sh status`.
