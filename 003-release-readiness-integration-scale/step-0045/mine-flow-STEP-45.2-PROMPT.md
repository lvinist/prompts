# mine-flow — STEP-45.2: Dual-platform E2E CI gate (Chrome + `Pixel_6a`)

**Recommended model:** Gemini 3.1 Pro (CI workflow + emulator-in-CI trade-off decision).

> **How to run:** *"run substep 45.2"*. Self-contained; runnable cold.

## Context

Second substep of STEP-45. The `integration_test` harness exists (45.1). This substep makes the
full E2E suite a **CI gate on both Chrome and the `Pixel_6a` Android emulator** — the user's locked
platform decision (heavier CI setup accepted). Read `Upcoming Prompts/mine-flow-STEP-45-PLAN.md`
(Q2 covers emulator-in-CI cost).

## Read these first
- `Upcoming Prompts/mine-flow-STEP-45-PLAN.md` — locked platform decision + Q2.
- `Code/mine-flow-app/.github/workflows/ci.yml` — existing jobs (`test`, `build-android`,
  `deploy-staging`, `deploy-production`) and how `STAGING_*` secrets are injected.
- `Code/mine-flow-docs/architecture/12-test-strategy.md` §6 (CI gates) and
  `architecture/09-environments.md` (promotion flow, staging).
- `integration_test/helpers/` from 45.1.

## Scope

Owns: CI workflow changes to run the E2E suite on Chrome and on a booted `Pixel_6a` emulator,
gating `deploy-staging` behind them. Does **not** author feature journeys (45.3+).

## Your task

1. **Add an `e2e-web` job** to `ci.yml`: sets up Flutter `3.47.0` (match existing pins), installs
   deps, then runs `flutter test integration_test -d chrome --dart-define=SUPABASE_URL=...` etc.
   with the `STAGING_*` secrets (same env block shape as the `test` job). Use headless Chrome
   suitable for CI.
2. **Add an `e2e-android` job**: boot the `Pixel_6a` emulator in CI (use
   `reactivecircus/android-emulator-runner` — it handles KVM/AVD) and run
   `flutter test integration_test` on the emulator with the same `--dart-define`s.
   **Decision point (Q2):** GitHub-hosted runners can run the KVM emulator but it is slow. Decide
   with the user whether the Android E2E gate runs **on every push** or on a **nightly/`workflow_dispatch`
   schedule** (or a self-hosted runner). Record the decision in the PLAN and a comment in `ci.yml`.
3. **Gate `deploy-staging`** so it `needs:` the E2E job(s) that run per-push (at minimum `e2e-web`;
   `e2e-android` too if it runs per-push). Keep the existing `build-android` dependency chain intact.
4. **Keep existing gates** (`check_supabase_contracts.dart`, `check_l10n_baseline.dart`, format,
   analyze, `flutter test`) unchanged and still required.
5. **Validate the workflow** locally as far as possible: `act` or a YAML lint / `flutter test
   integration_test -d chrome` locally to prove the command shape works. If you can't run the full
   emulator in CI from here, prove the `e2e-web` path locally and mark the Android CI path
   **Unverified until the first CI run** with the reason — do not claim a green CI run you didn't observe.

## Verification
- `ci.yml` parses (YAML valid); job dependency graph is correct (`deploy-staging` needs the E2E gate).
- `flutter test integration_test -d chrome` runs locally with staging `--dart-define`s (or Unverified w/ reason).
- Q2 decision recorded in PLAN + `ci.yml` comment.
- No change to existing passing gates.

## Keeping the docs true (always)
- The CI-gate list in `architecture/12-test-strategy.md` §6 now includes a dual-platform E2E gate —
  the doc bump + ADR for this expansion is done in **45.15**; note the exact new gates here so 45.15
  records them accurately.

## Definition of done
- [ ] `e2e-web` and `e2e-android` jobs added; `deploy-staging` gated behind the per-push E2E job(s).
- [ ] Q2 (per-push vs nightly/self-hosted Android emulator) decided with the user and recorded.
- [ ] `e2e-web` command proven locally (or Unverified w/ reason); Android CI path documented.
- [ ] Existing gates unchanged and still required.

## Next
Run substep 45.3 (Auth & session E2E journey) in a fresh chat.
