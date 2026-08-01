# mine-flow — STEP-36.2: Benchmark UI & BLoC

> **How to run:** Tell your agent *"run substep 36.2"* (or *"read and run this file"*).

## Context
This is the second substep for STEP-36. We are building the presentation layer (BLoC and UI screens) for the Benchmark Database feature using the `forui` package (Phase 2 design system).

## Read these first
- architecture/07-ui-design-system.md
- coding-standards/README.md

## Scope
- Create `BenchmarkBloc` (or Cubit) for state management.
- Create `BenchmarkListScreen` and `BenchmarkFormScreen`.
- Integrate the CRS utility (from 36.1) so Lat/Lon fields are automatically calculated based on entered Northing/Easting and selected CRS.
- Ensure all UI strictly uses the ForUI design system (`FThemes.zinc`, `FButton`, `FCard`, `FTextField`, etc.).
- Do NOT implement offline sync queue logic yet (that is 36.3).

## Your task
1. **State Management**: Create `BenchmarkBloc` that handles fetching, adding, updating, and deleting benchmarks. It should also manage form state, automatically updating Latitude and Longitude when Northing, Easting, or the selected CRS changes.
2. **UI Screens**:
   - Create `BenchmarkListScreen` displaying a list/table of benchmarks. Use ForUI styling.
   - Create `BenchmarkFormScreen` for creating/editing a benchmark. 
   - Add a Combobox for selecting the CRS (e.g., 'UTM Zone 51S', 'UTM Zone 50S' etc., with a logical default).
   - The Latitude and Longitude fields should be read-only and automatically populated based on the calculated values from the CRS utility.
   - Use `CreatableCombobox` if appropriate for categorical fields (like `code` or `orde`).
3. Ensure navigation is wired up (e.g., adding to the operations/sidebar menu).

## Verification
- **Write widget tests** for `BenchmarkListScreen` and `BenchmarkFormScreen` ensuring correct rendering, interactions, and that the Lat/Lon fields correctly auto-update.
- **Write unit tests** for `BenchmarkBloc`.
- Run timing: Run `flutter test test/features/benchmark/presentation/` before marking this substep done.

## Keeping the docs true (always)
- Follow Phase 2 ForUI migration guidelines strictly.

## Definition of done
- [ ] `BenchmarkBloc` implemented and tested.
- [ ] UI screens implemented using ForUI and tested.
- [ ] Lat/Lon automatic calculation works correctly in the form.
- [ ] Tests pass.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user the next action: *"run substep 36.3"*, in a fresh chat.
