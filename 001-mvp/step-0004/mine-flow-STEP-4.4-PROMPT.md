# mine-flow — STEP-4.4: Daily Logging UI Screens & State

> **How to run:** Tell your agent *"run substep 4.4"* (or *"read and run this file"*).

## Context
Substep 4.3 built the Daily Log data layer. Substep 4.4 creates the presentation layer for structured daily field log entry, allowing foremen to select zones, record weather conditions, detail operations summaries, and submit logs.

## Read these first
- `Code/mine-flow-docs/architecture/07-ui-design-system.md`
- `Code/mine-flow-docs/architecture/15-native-app-architecture.md`
- `Code/mine-flow-app/README.md`
- `Upcoming Prompts/mine-flow-STEP-4-PLAN.md`

## Scope
- **Owns:** `lib/features/daily_log/presentation/` (BLoC/Cubit, form screens, widgets, weather selector, zone picker).
- **Does NOT touch:** Core data models or Supabase migration files.

## Your task
1. Implement `DailyLogBloc` / state manager handling state transitions (`DailyLogInitial`, `DailyLogLoading`, `DailyLogSaved`, `DailyLogSubmitted`, `DailyLogError`).
2. Build `DailyLogFormScreen` (log date picker, zone dropdown, weather condition selector, work summary text area, operational notes).
3. Build `DailyLogListScreen` (history list of logs with status indicators for draft/submitted/approved).
4. Add auto-draft saving indicator for field safety.
5. Write widget tests for `DailyLogFormScreen` and input validation.

## Verification
- Write widget tests in `test/widget/daily_log_screen_test.dart`.
- Run: `flutter test test/widget/daily_log_screen_test.dart`.

## Keeping the docs true
- Ensure UI design tokens follow `07-ui-design-system.md`.

## Definition of done
- [ ] BLoC/state management created for daily log flow.
- [ ] Form UI for daily operational logging built with validation.
- [ ] List screen for reviewing draft and submitted logs created.
- [ ] Widget tests passing (`flutter test`).

## Next
Update STEP-4 PLAN and run **Substep 4.5**.
