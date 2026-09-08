# STEP 48.3: Auth & Session Runtime Evidence

## Definition of Done (Runtime Gates)
- [x] **Compile CI Fix**: `e2e-web` compiles without relative import failures on `auth_journey_test.dart`.
- [x] **Web Run**: The Web CI runner successfully executes `auth_journey_test.dart` and reports it passing.
- [x] **Android Run**: The Android CI runner successfully executes `auth_journey_test.dart` and reports it passing.
- [x] **Methodology Check**: No other journeys were modified.

## CI Evidence
- **Run URL:** https://github.com/lvinist/mine-flow-app/actions/runs/33252282454
- **Web (e2e-web):**
  - Result: **Passed** for `auth_journey_test.dart`. (Overall run failed due to other journeys: 6 test suites passed, 10 failed).
- **Android (e2e-android):**
  - Result: **Passed** for `auth_journey_test.dart`. (Overall run failed due to other journeys: 10 tests passed, 13 failed, 2 skipped).

## Security & Session Observations
- **Session restore**: Works as expected. The test correctly exercises `flutter_secure_storage` v11 key handling (RISK-0008) and successfully restores the session against a live backend.
- **Invalid login**: App stays on the login screen and no token is stored, verifying threat model expectations.
- **Logout**: Session is correctly cleared upon sign out.

## Fixes Applied
- **Web Compilation Failure**: The `flutter drive` runner for Web compiles tests into `.dart_tool/flutter_build/...` using the directory of `--target` as the root boundary. Since the integration test files inside `integration_test/journeys/` used relative imports `../helpers/app_harness.dart` which point outside this root, the web compiler failed with "File not found". I fixed this universally by modifying `.github/workflows/ci.yml` to generate a lightweight wrapper script (`run_web_wrapper.dart`) at the root of `integration_test/`. Targeting this script correctly frames the project root for the web compiler, allowing relative imports down into `journeys/` and `helpers/` to resolve properly without modifying any test files.
