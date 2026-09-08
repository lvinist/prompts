# mine-flow — STEP-48.2 Findings

**Date:** 2026-08-29  
**Executor:** Gemini 3.1 Pro High  
**Branch:** `step-0048-runtime-evidence`  

## 1. CI Workflow Expansion

### Aggregation Strategy
- **Web (`e2e-web`):** Uses a shell `for` loop over all `integration_test/app_boots_test.dart` and `integration_test/journeys/*_test.dart`. We chose this because `flutter drive` only accepts a single `--target`, and looping gives clear per-journey attribution (though it costs slightly more time).
- **Android (`e2e-android`):** Uses the directory form `flutter test integration_test/`. This is supported out of the box by `flutter test` on Android and provides robust per-file reporting without requiring shell loops over a single one-liner.

### Zero-Executed Guard
To ensure skipped tests do not silently pass CI:
- **Web:** We aggregate all iteration logs into `all_web.log`. We grep for `grep -qE "\+[1-9]|\-[1-9]|All tests passed|Some tests failed" all_web.log`. If this check fails, the job exits 1.
- **Android:** We grep the final `integration_test.log` for the same pattern `grep -qE "\+[1-9]|\-[1-9]|All tests passed|Some tests failed" integration_test.log`.
- **Honest skips:** These checks tolerate individual skips (e.g., `data_bucket_journey_test.dart`) perfectly because as long as at least *one* other test file produces execution output (passing or failing), the regex will match and the pipeline will not fail on zero-execution.

### Timeout Adjustments
- `e2e-web` was increased from 15 to 60 minutes.
- `e2e-android` was increased from 30 to 60 minutes.
*Justification:* 14 integration test journeys (some with significant navigation and waits) executed sequentially across the devices necessitate a higher timeout bound.

### Artifacts & Secrets
- `TEST_USER_EMAIL`, `TEST_USER_PASSWORD`, `TEST_SUPERVISOR_EMAIL`, `TEST_SUPERVISOR_PASSWORD`, `TEST_FOREMAN_EMAIL`, `TEST_FOREMAN_PASSWORD` injected uniformly into both jobs.
- Removed dead phantom `STAGING_GOOGLE_DRIVE_CLIENT_ID`.
- `web-screenshots` and `android-screenshots` artifacts configured for subsequent UI design-review substeps with 7-day retention.

## 2. Real CI Run Status

- **Run URL:** https://github.com/lvinist/mine-flow-app/actions/runs/33247672976
- **e2e-web Executed:** Yes (app_boots_test.dart passed; others failed with compilation/resolution errors due to flutter drive path scoping).
- **e2e-android Executed:** Yes. The job ran for exactly 30m before hitting the old `timeout-minutes: 30` bound. During this time, it ran 8 journeys and successfully captured their execution. (I have proactively pushed a commit to raise the timeout to 60m for future runs). All 8 journeys failed with `pumpAndSettle timed out` exceptions, indicating infinite animations (like loading spinners) are blocking the integration tests.

## 3. Journey Triage Table (First Run)

| Journey File | Web Status | Android Status |
|---|---|---|
| `auth_journey_test.dart` | Failed (Compile Error) | Interrupted (Timeout) |
| `attendance_journey_test.dart` | Failed (Compile Error) | Failed (pumpAndSettle timeout) |
| `daily_log_journey_test.dart` | Failed (Compile Error) | Failed (pumpAndSettle timeout) |
| `cut_fill_journey_test.dart` | Failed (Compile Error) | Failed (pumpAndSettle timeout) |
| `land_clearing_journey_test.dart` | Failed (Compile Error) | Interrupted (Timeout) |
| `inventory_journey_test.dart` | Failed (Compile Error) | Failed (pumpAndSettle timeout) |
| `equipment_check_journey_test.dart` | Failed (Compile Error) | Failed (pumpAndSettle timeout) |
| `benchmark_journey_test.dart` | Failed (Compile Error) | Failed (pumpAndSettle timeout) |
| `data_bucket_journey_test.dart` | Failed (Compile Error) | Interrupted (Timeout) |
| `reporting_journey_test.dart` | Failed (Compile Error) | Failed (pumpAndSettle timeout) |
| `timeline_journey_test.dart` | Failed (Compile Error) | Interrupted (Timeout) |
| `notifications_journey_test.dart` | Failed (Compile Error) | Interrupted (Timeout) |
| `offline_sync_journey_test.dart` | Failed (Compile Error) | Interrupted (Timeout) |
| `rls_authorization_journey_test.dart` | Failed (Compile Error) | Interrupted (Timeout) |
| `deep_link_journey_test.dart` | Failed (Compile Error) | Failed (pumpAndSettle timeout) |
| `app_boots_test.dart` | Passed | Passed / Interrupted |

## 4. Documentation Notes for STEP-48.15
- `architecture/09-environments.md` §4 needs update: the CI `e2e-web` and `e2e-android` now execute the 14 staging journeys instead of just `app_boots_test.dart`.
- `architecture/12-test-strategy.md` v1.2: E2E gate section must note that web is aggregated via loop due to single `--target` limits.
