# mine-flow — STEP-38.3: Language Configuration Fix

## Substep Prompt

Follow the `mine-flow-STEP-38-PLAN.md` for substep 38.3.
1. Check `SettingsEntity` and `SettingsLocalDatasource` to ensure a `locale` field exists and is persisted.
2. In `app.dart`, wire `SettingsCubit` so that `MaterialApp.router` uses `settingsState.settings.locale`.
3. Ensure `flutter_localizations` is in dependencies and delegates are configured.

## Verification

Update widget/unit tests if needed. Ensure changing the language in the Settings screen changes the app's locale at runtime. Run `flutter analyze` and `flutter test`.
