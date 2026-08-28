# mine-flow — STEP-45 pre-locked planning decisions

**Status:** not yet planned. STEP-46 runs first (user decision, 2026-08-26), because STEP-46's
confirmed finding register becomes STEP-45's explicit "verify these on device/staging" list.

These answers were given by the user during the STEP-45 planning conversation that was
deferred. Carry them into the STEP-45 PLAN when it is authored — do not re-ask.

| Decision | Locked answer |
|---|---|
| Sequencing | Run STEP-46 first, then return to STEP-45. |
| E2E harness | Add the `integration_test` package and write **real automated E2E journeys** (matches `architecture/12-test-strategy.md` §1, which already names `integration_test` as the e2e tier). Largest scope accepted. |
| Runtime access | Staging Supabase credentials + `Pixel_6a` Android emulator + Chrome — full runtime evidence is expected to be obtainable, so Impeccable design-review items should not be planned as Unverified. |
| Offline/sync depth | Full offline journey: airplane-mode entry, queue persistence, reconnect, and conflict resolution against real staging data. |

## Facts confirmed from disk while planning (2026-08-26)

- `Code/mine-flow-app` has **no** `integration_test/` directory and **no** `integration_test`
  dev dependency in `pubspec.yaml`. The existing `test/integration/` tier is BLoC/repository
  integration with mocked boundaries, not device E2E. STEP-45 must create the harness.
- `flutter devices` reports Windows, Chrome, Edge; `flutter emulators` reports `Pixel_6a`;
  `adb devices` is currently empty (emulator not booted).
- Flutter 3.47.1 local, 3.47.0 in CI.
- Staging web is served from GitHub Pages at base href `/mine-flow-app/staging/`
  (`gh-pages-staging` branch); staging APK is the `staging-apk-<sha>` CI artifact.
- No `.env` exists locally — only `.env.example`. Staging credentials must be supplied before
  the staging-backed substeps can run.
- Open items already deferred *to* STEP-45 by earlier STEPs (must appear in its scope):
  - `go_router` v16→v17 deep-link E2E validation (RISK-0009, `reports/2026-08-25-step-0043-upgrade-report.md`).
  - Live RLS behavior test against staging (`reports/security/2026-08-26-step-0044-s0-security-baseline-report.md`).
  - The STEP-46 "Needs runtime check" register.
