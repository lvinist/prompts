# mine-flow — STEP-35.1: Domain & Data Layer for Settings

> **How to run:** Tell your agent *"run substep 35.1"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat. Write it so
> nothing depends on the conversation that produced it.

## Context
This is substep 35.1 of STEP-35 (Settings Page Feature). We are building a new settings screen. This substep handles the foundation: the domain definitions and local storage for user preferences (Theme and Language) using Hive.

## Read these first
- `Upcoming Prompts/mine-flow-STEP-35-PLAN.md` (the STEP PLAN)
- `architecture/04-data-model.md`
- `architecture/07-ui-design-system.md`
- `coding-standards/README.md`
- `mine-flow-app/README.md`

## Scope
This substep owns the Domain (Entity/Repository interfaces) and Data Layer (Repository implementation + Hive Datasource) for Settings. It does NOT touch the Presentation layer or UI wiring.

## Your task
1. Create `SettingsEntity` or `SettingsModel` (if needed) to encapsulate `ThemeMode` (light, dark, system) and `Locale` (en, id).
2. Create `SettingsRepository` interface in `lib/features/settings/domain/repositories/` with methods to:
   - `getThemeMode()` and `saveThemeMode(ThemeMode mode)`
   - `getLocale()` and `saveLocale(Locale locale)`
3. Create `SettingsLocalDataSource` in `lib/features/settings/data/datasources/` using Hive to read/write these preferences. (Key: `'settings_box'`).
4. Create `SettingsRepositoryImpl` in `lib/features/settings/data/repositories/` that calls the local data source.
5. Register the repository and data source in the dependency injection container (if applicable, or make sure they can be instantiated easily).

## Verification
- Tests are deferred to the final verification substep (35.4).
- Run `flutter analyze` to ensure there are no syntax or lint errors.

## Keeping the docs true (always)
- Since this adds a new domain package `settings`, ensure the `Architecture Overview` or relevant index docs aren't silently outdated, though a settings domain is fairly standard.

## Definition of done
- [ ] Domain and Data layer files created for settings preferences.
- [ ] Hive box logic implemented for Theme and Locale.
- [ ] Analyzer passes cleanly on the new files.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user the next action: *"run substep 35.2"*, in a **fresh chat**.
