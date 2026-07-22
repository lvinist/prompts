# Substep 30.1: Core Shell & Auth (ForUI)

**Scope:** `pubspec.yaml`, `lib/app/app.dart`, `lib/app/presentation/` (Shell/Navigation), `LoginPage`, `DashboardPage`.

## 1. Craft
- Add `forui` to `pubspec.yaml`.
- Update `app.dart` to wrap `MaterialApp.router` with `FTheme(data: FThemes.zinc.light)`.
- Rebuild the navigation shell (`lib/app/presentation/`) to use `FScaffold` and `FSidebar`. 
- **Important Contract for STEP-31:** Define a structured interface (e.g., `AppNavGroup` / `AppNavItem`) that the shell consumes, so STEP-31 can easily regroup the navigation items later without touching layout code.
- Rebuild `LoginPage` and `DashboardPage` using `FCard`, `FButton`, and `FTextField`.

## 2. Polish
- Apply `forui` spacing and typography tokens. 
- Remove all hardcoded `Colors.*` and `TextStyle` from these files (referencing the violations in `mine-flow-STEP-28.1-AUDIT.md`).

## 3. Audit
- Run existing widget tests for Auth and Dashboard. Fix any broken widget finders (e.g. `ElevatedButton` -> `FButton`).
- Ensure no logic, state, or data-fetching changes occurred.
