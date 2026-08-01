# mine-flow — STEP-35.4: Verification & Polish

> **How to run:** Tell your agent *"run substep 35.4"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat. Write it so
> nothing depends on the conversation that produced it.

## Context
This is the final substep (35.4) of STEP-35 (Settings Page Feature). The domain, data, and presentation layers are complete. This substep is responsible for validating the feature using automated tests, polishing any rough edges in the UI, and verifying compliance with the project constraints.

## Read these first
- `Upcoming Prompts/mine-flow-STEP-35-PLAN.md` (the STEP PLAN)
- `architecture/12-test-strategy.md`

## Scope
This substep owns the testing and final verification of the Settings feature.

## Your task
1. **Unit Tests:** Write tests for `SettingsRepositoryImpl` and `SettingsCubit` in `test/features/settings/`. Mock the Hive local data source.
2. **Widget Tests:** Write a basic widget test for `SettingsPage` to ensure it renders without exceptions and that key sections (Profile, Language, Theme, Logout, Support) exist on the screen.
3. **Run all tests:** Execute `flutter test test/features/settings/` and ensure they pass.
4. **Analyzer check:** Run `flutter analyze` across the whole project. Address any remaining warnings or linting issues introduced during STEP-35.
5. **A11y & Responsive Check:** Ensure `SettingsPage` meets the accessibility requirements (semantic labels) and responsive bounds (e.g. `ConstrainedBox` for desktop layout scaling) as defined in Phase 2 rebuilds.

## Verification
- Tests must pass.
- `flutter analyze` must report no issues.

## Definition of done
- [ ] Unit and widget tests written and passing.
- [ ] `flutter analyze` is clean.
- [ ] Accessibility and responsiveness validated for the new UI.

## Next
When this substep is done, update its status in the STEP PLAN.
Since this is the final substep, mark STEP-35 as **Done** in `prompts/STEP-index.md`, move the `Upcoming Prompts` files into `prompts/001-mvp/step-0035/` (wait, this is Phase 2 Tier 2, so `prompts/002-.../step-0035/` or equivalent phase folder), and run `doctor.sh status` to find the next action.
