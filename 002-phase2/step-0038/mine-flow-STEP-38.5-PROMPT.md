# mine-flow — STEP-38.5: Breadcrumbs and Benchmark Navigation Fix

## Substep Prompt

Follow the `mine-flow-STEP-38-PLAN.md` for substep 38.5.
1. In `global_app_header.dart`, apply a map to breadcrumb segments so they show title-cased names without hyphens (e.g., "Daily Log" instead of "daily-log").
2. In `router.dart`, update `AppRoutes.benchmarkDb` to `'/operations/benchmark-db'` to match the nested GoRouter path.
3. Add Benchmark DB to the sidebar in `app_shell.dart` under the Operations section.

## Verification

Ensure tests pass and navigation to Benchmark DB from the Group Landing Page works correctly. Run `flutter analyze` and `flutter test`.
