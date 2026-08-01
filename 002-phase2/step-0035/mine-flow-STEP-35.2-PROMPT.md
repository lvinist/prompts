# mine-flow — STEP-35.2: State Management & App Wiring

> **How to run:** Tell your agent *"run substep 35.2"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat. Write it so
> nothing depends on the conversation that produced it.

## Context
This is substep 35.2 of STEP-35 (Settings Page Feature). With the Hive domain and data layer implemented in 35.1, this substep builds the presentation state management (`SettingsBloc` or `Cubit`) and wires it into the app's root so that changes to the theme and language reflect instantly across the UI.

## Read these first
- `Upcoming Prompts/mine-flow-STEP-35-PLAN.md` (the STEP PLAN)
- `architecture/07-ui-design-system.md`
- `mine-flow-app/lib/app/app.dart`

## Scope
This substep owns the State Management (Bloc/Cubit) for Settings and its integration into `MaterialApp`/`AppShell`. It does NOT build the Settings Page UI itself.

## Your task
1. Create `SettingsState` and `SettingsCubit` (or `SettingsBloc`) in `lib/features/settings/presentation/bloc/`. 
   - State should expose current `ThemeMode` and `Locale`.
   - Cubit should expose methods like `updateThemeMode()` and `updateLocale()`.
   - On initialization, it should load the saved preferences from `SettingsRepository`.
2. Update `lib/app/app.dart` (or the equivalent root application widget):
   - Wrap `MaterialApp` (or inject the Bloc above it) with a `BlocBuilder` (or `BlocProvider` + `BlocBuilder`) for `SettingsCubit`.
   - Map the `SettingsCubit`'s `ThemeMode` to the app's `themeMode` property.
   - Map the `SettingsCubit`'s `Locale` to the app's `locale` property.

## Verification
- Tests are deferred to the final verification substep (35.4).
- Run `flutter analyze` to ensure there are no syntax or lint errors.

## Definition of done
- [ ] `SettingsCubit` / `SettingsBloc` created and functional.
- [ ] App root wrapped to listen to Theme and Locale changes.
- [ ] Analyzer passes cleanly on the modified files.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user the next action: *"run substep 35.3"*, in a **fresh chat**.
