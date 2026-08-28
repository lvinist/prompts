# mine-flow — STEP-47.6: CI `e2e-web` — replace `-d chrome` with `flutter drive` + chromedriver

> **How to run:** Tell your agent *"run substep 47.6"*. Self-contained; runnable cold.
>
> **Model:** Gemini 3.1 Pro High. Small diff, but it is CI-only work with a slow feedback loop, so
> getting the invocation right on the first push matters.

## Context

STEP-47's PLAN is `Upcoming Prompts/mine-flow-STEP-47-PLAN.md`. The `e2e-web` CI job has **never
passed**. It is not a credential problem or a test problem — the command itself is unsupported:

```yaml
# .github/workflows/ci.yml, e2e-web job, ~line 140
flutter test integration_test -d chrome \
  --dart-define=SUPABASE_URL=... (etc.)
```

Flutter answers *"Web devices are not supported for integration tests yet"*. `flutter test` cannot
drive a browser; web integration tests require `flutter drive` against a **chromedriver** process.

The repo already contains the driver entrypoint, unused since STEP-45 authored it:

```dart
// test_driver/integration_test.dart
import 'package:integration_test/integration_test_driver.dart';
Future<void> main() => integrationDriver();
```

So this substep is a wiring fix: start chromedriver, invoke `flutter drive`, keep the same
`--dart-define` credential surface.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-47-PLAN.md`
- `Upcoming Prompts/mine-flow-STEP-47.0-EVIDENCE.md` — §7 records the local rejection message and
  Q1's answer on whether the staging secrets exist
- `Code/mine-flow-app/.github/workflows/ci.yml` — the `e2e-web` job and, for style, `e2e-android`
- `Code/mine-flow-app/test_driver/integration_test.dart`
- `Code/mine-flow-app/integration_test/app_boots_test.dart` and `integration_test/helpers/app_harness.dart`
  + `integration_test/helpers/staging_config.dart` — how `isStagingConfigured` gates the journeys
- `Code/mine-flow-docs/architecture/12-test-strategy.md` §6 — the authoritative CI gate list
- **ADR-0017** — the expanded E2E tier this job implements
- `Code/mine-flow-docs/architecture/09-environments.md` §2 — credentials come from repo secrets via
  `--dart-define`
- `Code/mine-flow-app/README.md`

## Scope

**Owns:** the `e2e-web` job in `.github/workflows/ci.yml`, and the app `README.md` line describing how
to run web E2E locally **only if** 47.8 has not already covered it (coordinate; do not both edit it).

**Does NOT touch:** `build-android` / `e2e-android` (47.7), any `.dart` file, `pubspec.yaml`,
`android/**`, `architecture/*` docs. **Do not modify a journey test** to make the job green — the 14
staging journeys stay Deferred to STEP-48.

## Your task

### 1. Confirm the failure mode locally

```bash
cd /d/AppDev/mine_flow/Code/mine-flow-app
flutter test integration_test -d chrome 2>&1 | tail -5
```

Expect *"Web devices are not supported for integration tests yet"*. This is the justification for the
change; have it in hand.

### 2. Decide what "green" means for this job

Be deliberate, because it is the difference between an honest gate and a decorative one.

`integration_test/helpers/staging_config.dart` gates the journeys on `isStagingConfigured`. Without
credentials the journeys call `markTestSkipped('Unverified: Staging credentials absent')` and the run
exits 0 with skips. So:

- **Green with credentials** = the browser launched, the app booted, and the journeys ran for real.
- **Green without credentials** = the harness executed and the journeys skipped honestly.

Both are legitimate outcomes for **STEP-47**, whose deliverable is *the job works*. Neither means the
journeys are verified — that is STEP-48's job. Your CI change must therefore **not** hide skips: the
job log has to show which tests ran and which skipped, so nobody can later read a green check as
runtime evidence. If `flutter drive` output hides skip lines, add `--verbose` or echo the summary.

### 3. Rewrite the job

Replace the `Run E2E tests on Chrome` step. The shape:

```yaml
      - name: Setup Chrome
        uses: browser-actions/setup-chrome@v1
        with:
          chrome-version: stable
          install-chromedriver: true      # verify this input exists at the pinned action version

      - name: Start chromedriver
        run: |
          chromedriver --port=4444 &
          # wait for the port instead of a blind sleep
          for i in $(seq 1 30); do
            curl -sf http://localhost:4444/status && break
            sleep 1
          done
          curl -sf http://localhost:4444/status

      - name: Run E2E tests on Chrome (driver)
        run: |
          flutter drive \
            --driver=test_driver/integration_test.dart \
            --target=integration_test/app_boots_test.dart \
            -d web-server \
            --browser-name=chrome \
            --dart-define=SUPABASE_URL=${{ secrets.STAGING_SUPABASE_URL }} \
            --dart-define=SUPABASE_ANON_KEY=${{ secrets.STAGING_SUPABASE_ANON_KEY }} \
            --dart-define=GOOGLE_DRIVE_CLIENT_ID=${{ secrets.STAGING_GOOGLE_DRIVE_CLIENT_ID }} \
            --dart-define=APP_ENV=staging
```

Decisions to make explicitly, not by copying the snippet blindly:

- **`install-chromedriver`** — confirm `browser-actions/setup-chrome@v1` actually accepts that input.
  If not, install chromedriver separately (e.g. `nanasess/setup-chromedriver`) and pin the version to
  match the installed Chrome major. A chromedriver/Chrome major mismatch is the most common failure
  here.
- **`-d web-server` vs `-d chrome`** — `web-server` runs headless against the driver, which is what a
  CI runner wants. If you use `-d chrome`, add `--headless`.
- **Target scope.** `flutter drive` takes **one** `--target` at a time. Start with
  `integration_test/app_boots_test.dart` only — the boot smoke test, which needs no credentials and
  proves the harness works. Do **not** loop all 15 journeys in this substep: a loop over
  credential-gated journeys produces a long green log full of skips, which is precisely the misleading
  artifact this project is trying to stop producing. Note in the job's YAML comment that STEP-48
  extends the target list once credentials are wired.
- **Job timeout.** Add a `timeout-minutes` so a hung browser fails fast instead of burning the
  runner's default 6 hours.
- **Failure diagnostics.** On failure, upload the driver log as an artifact — CI job logs need a token
  to read via API (47.0 hit HTTP 403), so an artifact is what makes the next failure debuggable.

### 4. Try it locally first if you can

Local chromedriver is **not** installed (47.0 confirmed `-d chrome` is rejected; chromedriver was
absent during planning). If you can install it for the host Chrome major, a local dry run saves CI
round-trips:

```bash
chromedriver --port=4444 &
flutter drive --driver=test_driver/integration_test.dart \
  --target=integration_test/app_boots_test.dart \
  -d web-server --browser-name=chrome
```

If you cannot install it, say so and verify in CI instead. Do **not** install chromedriver globally on
the user's machine without asking — that is an environment change they did not request.

### 5. Push and verify in CI

```bash
git -C /d/AppDev/mine_flow/Code/mine-flow-app add .github/workflows/ci.yml
git -C /d/AppDev/mine_flow/Code/mine-flow-app commit -m "ci(STEP-47.6): drive web E2E via flutter drive + chromedriver"
git -C /d/AppDev/mine_flow/Code/mine-flow-app push -u origin step-0047-android-build-chain
```

Then watch the run. Per-job conclusions are readable without a token:

```bash
curl -s "https://api.github.com/repos/lvinist/mine-flow-app/actions/runs?per_page=3&branch=step-0047-android-build-chain" \
  | python -c "import json,sys; [print(r['id'], r['conclusion'], r['html_url']) for r in json.load(sys.stdin)['workflow_runs']]"
curl -s "https://api.github.com/repos/lvinist/mine-flow-app/actions/runs/<RUN_ID>/jobs" \
  | python -c "import json,sys; [print(j['name'], j['conclusion'], [s['name'] for s in j['steps'] if s['conclusion']=='failure']) for j in json.load(sys.stdin)['jobs']]"
```

Log **bodies** need auth (403 without a token). If the job fails and you cannot read the log, use the
uploaded artifact from §3, or ask the user to paste the failing tail. Budget for 2–3 iterations;
chromedriver setup rarely lands first try.

Record the run URL and the per-job conclusion. A green ✅ with the run URL is the evidence; "should
work now" is not.

## Verification

- CI `e2e-web` conclusion is **success**, with the run URL recorded.
- The job log shows the boot target actually executing (and any skips explicitly listed).
- `chromedriver --port=4444` readiness is confirmed by polling `/status`, not a blind `sleep`.
- `timeout-minutes` set; failure artifact upload configured.
- No journey test file modified; no `.dart` file modified at all.
- `build-android` and `e2e-android` conclusions are unchanged by this edit (they are 47.7's).

If `e2e-web` cannot be made green — for example a chromedriver/Chrome mismatch on the runner image
that has no clean fix — mark it **Unverified** with the exact error and stop. The user's scope
decision was that all three jobs go green, so an unfixable blocker is a conversation, not something
to paper over with `continue-on-error`. **Never** add `continue-on-error: true` to make a red job look
green.

## Keeping the docs true (always)

`architecture/12-test-strategy.md` §6 lists the CI gates. This substep changes **how** the web E2E gate
is invoked, not which gates exist — so no doc change is required. But if you conclude the doc's wording
implies `flutter test` for web E2E, that wording is now wrong: report it to **47.8**, which owns doc
updates for this STEP. Do not edit `architecture/*` here.

Also hand 47.8: the local-development command for web E2E (chromedriver prerequisite + the
`flutter drive` line) belongs in the app `README.md` host-setup section it is already writing.

No secrets: the `--dart-define` values come from repo secrets by reference. Never echo a secret, and
never paste one into the workflow file as a literal.

## Definition of done

- [ ] `e2e-web` uses `flutter drive --driver=test_driver/integration_test.dart` with an explicit target
- [ ] chromedriver installed at a version matching the runner's Chrome major, readiness polled
- [ ] Target is the boot smoke test only; a YAML comment notes STEP-48 extends the list
- [ ] `timeout-minutes` set; failure diagnostics uploaded as an artifact
- [ ] Skips are visible in the log — a green run cannot be mistaken for journey verification
- [ ] No `continue-on-error`, no modified journey test, no `.dart` change
- [ ] CI `e2e-web` green on `step-0047-android-build-chain`, run URL recorded (or Unverified with the
      exact error)
- [ ] Committed and pushed on the STEP branch
- [ ] Notes for 47.8 written (README local command; any Doc 12 wording drift)

## Next

Update 47.6's status in the PLAN, then tell the user the next action: **run substep 47.7**
(`build-android` + `e2e-android` green) in a fresh chat — or, if 47.7 is already done, **47.8**.
