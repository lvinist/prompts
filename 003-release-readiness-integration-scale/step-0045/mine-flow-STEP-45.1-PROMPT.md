# mine-flow — STEP-45.1: Reservation, branch & `integration_test` harness scaffold

**Recommended model:** Gemini 3.1 Pro (infra bootstrap — the foundation every later substep reuses).

> **How to run:** Tell your agent *"run substep 45.1"*. Self-contained; runnable cold in a fresh chat.

## Context

First substep of STEP-45 (Release-Candidate E2E & Runtime Design Review). Read the STEP PLAN:
`Upcoming Prompts/mine-flow-STEP-45-PLAN.md`. This substep reserves the branch, flips the index
row, and creates the `integration_test` harness the rest of the STEP builds on. The project has
**never** had a device/browser E2E tier — `test/integration/` is BLoC↔mock only. You are creating
the harness from scratch.

## Read these first
- root `.throughstone/local-user.md` — Level 2, Explanatory; calibrate explanations.
- `Upcoming Prompts/mine-flow-STEP-45-PLAN.md` — this STEP's PLAN (locked decisions, substeps).
- `Code/mine-flow-docs/architecture/12-test-strategy.md` — §1/§5/§6 (E2E via `integration_test`, Staging Supabase target, CI gates).
- `Code/mine-flow-docs/architecture/09-environments.md` — staging config + `--dart-define` keys.
- `Code/mine-flow-app/README.md` — setup, run commands, `--dart-define` list.
- `Code/mine-flow-app/lib/main.dart` and `lib/app/app.dart` — how the app bootstraps (Hive, Supabase, locale) so the harness can boot it.
- `Code/mine-flow-docs/runbooks/collaboration.md` §3 (branch-per-STEP), and STEP-index reserving rules.

## Scope

Owns: STEP number reservation confirmation, `step-0045-rc-e2e-design-review` branches in all three
repos, index flip to In progress, the `integration_test/` directory, shared helpers, one passing
smoke journey. Does **not** write any feature journey (45.3+) or CI jobs (45.2).

## Your task

1. **Confirm reservation.** STEP-45 row already exists in `prompts/STEP-index.md` (Planned). If any
   other STEP has silently duplicated 45, run the dup scan
   (`grep -oE '^\|[[:space:]]*STEP-[0-9]+' prompts/STEP-index.md | grep -oE 'STEP-[0-9]+' | sort | uniq -d`)
   and reconcile before proceeding. Pull `prompts` main first.
2. **Cut the branch** `step-0045-rc-e2e-design-review` in `mine-flow-app`, `mine-flow-docs`, and
   `prompts` (same name in each).
3. **Flip the index row** for STEP-45 to `In progress` on `prompts` main (per collaboration rules,
   the flip lands on the shared trunk), commit, and push.
4. **Add dev dependencies** to `Code/mine-flow-app/pubspec.yaml`:
   `integration_test` (from Flutter SDK) and the Flutter test driver as needed. Run `flutter pub get`.
5. **Create `integration_test/`** with:
   - `integration_test/helpers/app_harness.dart` — boots the real app widget (mirroring `main.dart`
     init: logging, Hive, Supabase from `--dart-define`), a `pumpApp(tester)` entry point, and a
     `IntegrationTestWidgetsFlutterBinding.ensureInitialized()` guard.
   - `integration_test/helpers/staging_config.dart` — reads `SUPABASE_URL`/`SUPABASE_ANON_KEY`/
     `GOOGLE_DRIVE_*`/`APP_ENV` from `String.fromEnvironment`; exposes an `isStagingConfigured` bool
     so journeys can mark themselves **Unverified** (skip with a clear reason) when creds are absent
     rather than fail opaquely.
   - `integration_test/helpers/login_helper.dart` — a `loginAsStagingUser(tester, role)` helper
     (roles wired in 45.12; stub the role param now).
   - `integration_test/helpers/offline_helper.dart` — a `forceOffline(bool)` helper that drives the
     app's `ConnectivityService` boundary (see `lib/core/network/`) for the 45.11 offline journey.
   - `integration_test/app_boots_test.dart` — the smoke journey: boot the app, assert the first
     screen (login) renders. Target `EditableText` finders, not `TextField` (RISK-0009 semantics
     regression; forui wraps fields).
6. **Run the smoke journey locally on Chrome** with staging `--dart-define`s:
   `flutter test integration_test/app_boots_test.dart -d chrome --dart-define=...`. If staging creds
   are unavailable, run against a locally-mockable boot or report the smoke test as **Unverified**
   with the reason — do not fabricate a pass.

## Verification
- The smoke journey passes on Chrome (or is Unverified with a documented reason).
- `flutter analyze` → 0 issues; `dart format --set-exit-if-changed lib/ test/ integration_test/` clean.
- Existing `flutter test` suite still green (no regression from the pubspec change).
- Name the files created above; commit on the STEP-45 branch.

## Keeping the docs true (always)
- Adding the `integration_test` tier is expected by Doc 12 §5, so no doc change is required *yet*;
  the material E2E-tier expansion + dual-platform gate is documented in **45.15** (Version Log +
  ADR). If you discover the harness forces a boot/config change to `main.dart`/`app.dart` that
  contradicts an architecture doc, note it for 45.15.
- Secrets stay out of the repo — staging values via `--dart-define`/CI only.

## Definition of done
- [ ] STEP-45 branch cut in all 3 repos; index row flipped In progress and pushed; dup scan clean.
- [ ] `integration_test/` harness + helpers + smoke journey created.
- [ ] Smoke journey passes on Chrome (or Unverified with reason).
- [ ] `flutter analyze` 0 issues; format clean; existing `flutter test` green.
- [ ] New files carry docstrings.

## Next
Run substep 45.2 (dual-platform E2E CI gate) in a fresh chat.
