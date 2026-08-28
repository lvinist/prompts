# Notes from 47.6 for 47.8

## README Updates
Please add the following local-development command for web E2E to the `mine-flow-app` `README.md` (likely in the host-setup or testing section you are already authoring):

To run web E2E tests locally, `chromedriver` is required and must match your installed Chrome version. Run it on port 4444 in the background before invoking `flutter drive`:

```bash
# Terminal 1: Start chromedriver
chromedriver --port=4444

# Terminal 2: Run tests
flutter drive \
  --driver=test_driver/integration_test.dart \
  --target=integration_test/app_boots_test.dart \
  -d web-server \
  --browser-name=chrome \
  --dart-define=APP_ENV=staging
```
*(Note: Substitute the rest of the `--dart-define` secrets as needed to run actual credential-gated journeys).*

## Doc 12 (`architecture/12-test-strategy.md`) Wording Drift
If `architecture/12-test-strategy.md` §6 implies or explicitly states that `flutter test` is used for Web E2E, it needs to be updated. Web E2E testing now explicitly requires `flutter drive` targeting a running `chromedriver` instance since `flutter test` with `-d chrome` does not support integration tests.
