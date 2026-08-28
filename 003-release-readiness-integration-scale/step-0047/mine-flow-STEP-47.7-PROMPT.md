# mine-flow — STEP-47.7: CI `build-android` + `e2e-android` green

> **How to run:** Tell your agent *"run substep 47.7"*. Self-contained; runnable cold.
>
> **Model:** Gemini 3.7 Flash High. Mostly verification and small YAML fixes — the hard work was
> 47.1–47.5. Escalate to Pro if the emulator job needs real debugging.

## Context

STEP-47's PLAN is `Upcoming Prompts/mine-flow-STEP-47-PLAN.md`. Substep 47.5 proved the debug APK
builds locally. This substep proves the same on CI, and gets the Android emulator E2E job green.

CI history (from 47.0, via the public API):

| Commit | Date | `build-android` |
|---|---|---|
| `55361914` | 2026-08-26 | success |
| `040def92` | 2026-08-27 | skipped |
| `3b45176` | 2026-08-28 | **failure** |

`3b45176` is the STEP-45 merge — the commit that added `package_info_plus: ^9.0.1` and
`integration_test`. `package_info_plus` 9.0.1 is exactly the plugin whose unconditional
`apply plugin: 'kotlin-android'` breaks under AGP 9. So CI's failure is almost certainly the same root
cause as the local one, and 47.1–47.5 should have fixed it without any CI change. **Verify that;
don't assume it.**

`e2e-android` (`reactivecircus/android-emulator-runner@v2`, api-level 33, google_apis, x86_64,
pixel_6a) failed at "Run E2E tests on Android emulator" — plausibly the same APK build failure inside
the emulator step, but that was never confirmed because job logs need auth (47.0 got HTTP 403).

## Read these first

- `Upcoming Prompts/mine-flow-STEP-47-PLAN.md`
- `Upcoming Prompts/mine-flow-STEP-47.0-EVIDENCE.md` — CI per-job table, Q1 (do the staging secrets
  exist?), and 47.5's appended local build evidence including wall-clock time
- `Code/mine-flow-app/.github/workflows/ci.yml` — `build-android` and `e2e-android`; 47.6 has just
  reworked `e2e-web`, so rebase/pull before editing
- `Code/mine-flow-docs/architecture/12-test-strategy.md` §6 — CI gates
- `Code/mine-flow-docs/architecture/09-environments.md` §2, §4 — secrets and the promotion flow
  (`deploy-staging` needs `[build-android, e2e-web, e2e-android]`, so all three must pass for staging
  deploys to resume)
- **ADR-0017** — the expanded E2E tier
- `Code/mine-flow-app/integration_test/app_boots_test.dart`, `integration_test/helpers/staging_config.dart`

## Scope

**Owns:** the `build-android` and `e2e-android` jobs in `ci.yml`.

**Does NOT touch:** `e2e-web` (47.6), any `.dart` file, `pubspec.yaml`, `android/**` (47.5 settled the
Gradle posture), docs (47.8). **Do not modify a journey test.** The 14 staging journeys stay Deferred
to STEP-48.

## Your task

### 1. Push and observe before changing anything

47.1–47.5 may already have fixed both jobs. Establish that first.

```bash
cd /d/AppDev/mine_flow/Code/mine-flow-app
git status --short
git pull --ff-only origin step-0047-android-build-chain   # pick up 47.6's ci.yml edit
git push -u origin step-0047-android-build-chain
```

Then read per-job conclusions (no token needed):

```bash
curl -s "https://api.github.com/repos/lvinist/mine-flow-app/actions/runs?per_page=3&branch=step-0047-android-build-chain" \
  | python -c "import json,sys; [print(r['id'], r['conclusion'], r['html_url']) for r in json.load(sys.stdin)['workflow_runs']]"
curl -s "https://api.github.com/repos/lvinist/mine-flow-app/actions/runs/<RUN_ID>/jobs" \
  | python -c "import json,sys; [print(j['name'], j['conclusion'], [s['name'] for s in j['steps'] if s['conclusion']=='failure']) for j in json.load(sys.stdin)['jobs']]"
```

If `build-android` is already green: record the run URL and move to §3. Do not "improve" a passing job.

### 2. If `build-android` still fails

Get the actual error before editing. Log bodies need auth (`GET /actions/jobs/<id>/logs` → 403). Try in
order: an authenticated `gh` CLI; a `GITHUB_TOKEN`/`GH_TOKEN` already exported
(`curl -sL -H "Authorization: Bearer $GITHUB_TOKEN" …`, never printing it); or ask the user for the
failing tail / the run URL.

Differences between CI and the now-working local build, worth checking in this order:

- **Flutter version skew.** CI pins `flutter-version: "3.47.0"`; local is 3.47.1. 47.0 established
  skew was *not* the original cause, but a dependency sweep can change that. If CI fails where local
  passes, this is the first suspect — consider bumping the pin to `3.47.1` for parity, and say so
  explicitly since it changes the CI contract.
- **`pubspec.lock` committed?** The sweep in 47.1 rewrote it. If it is not committed, CI resolves
  differently than local — that alone could reproduce the old failure.
- **Gradle/Kotlin cache.** `subosito/flutter-action@v2` with `cache: true` caches the pub cache, not
  Gradle. A stale Gradle cache is unlikely on a fresh runner but check for a cache action.
- **Build duration.** Record 47.5's local wall-clock time; if CI is near a timeout, add
  `timeout-minutes` rather than letting it die ambiguously.
- **JDK.** Already `java-version: '17'` (Temurin) in all three jobs — matches local. Leave it.

Do **not** add `continue-on-error: true`, and do not disable a gate to reach green.

### 3. `e2e-android`

Once `build-android` passes, this job likely passes too — its emulator step runs `flutter test
integration_test`, which first builds the same APK.

Two things to verify in the log:

1. **The harness actually ran.** `flutter test integration_test` executes every file under
   `integration_test/`, including all 15 journeys. Without staging credentials each one hits
   `markTestSkipped('Unverified: Staging credentials absent')` and the run exits 0. **A green ✅ here
   does NOT mean the journeys were verified.** Confirm from the log which tests ran vs skipped, and
   record that split. This is the single most important honesty check in the substep: STEP-45's record
   had to be corrected precisely because skipped journeys were reported as Done.
2. **`app_boots_test.dart` actually executed** (it needs no credentials). If even that skipped or never
   ran, the harness is not working and green is meaningless.

Add `timeout-minutes` to the emulator job if absent — emulator boots hang, and a hung job that
eventually cancels is indistinguishable from a real failure.

Consider uploading the test output as an artifact on failure, for the same reason as 47.6: API log
access is 403-gated, so an artifact is what makes the next failure debuggable.

**Scope guard:** if the journeys fail *for real* (not skip) because credentials ARE present and staging
data does not match expectations — that is STEP-48's problem, not yours. Record it as a STEP-48 inbound
finding and do not start fixing journeys. If their failure blocks the job from going green, stop and
tell the user: the scope boundary between 47 and 48 needs their decision.

### 4. Record the outcome

Append a "47.7 — CI" section to `Upcoming Prompts/mine-flow-STEP-47.0-EVIDENCE.md`:

- run URL and per-job conclusions for all five jobs (`test`, `build-android`, `e2e-web`,
  `e2e-android`, `deploy-staging`)
- for `e2e-android`: the ran-vs-skipped split, explicitly, with the exact skip reason string
- any `ci.yml` change you made and why
- whether `deploy-staging` now runs (it needs all three of `build-android`, `e2e-web`, `e2e-android`)

**`deploy-staging` caution:** it triggers only on `refs/heads/master`, so it will not fire from the
STEP branch. Do not merge to master just to see it run — that is the STEP close's business (47.9),
under the user's review.

### 5. Commit

```bash
git -C /d/AppDev/mine_flow/Code/mine-flow-app add .github/workflows/ci.yml   # only if changed
git -C /d/AppDev/mine_flow/Code/mine-flow-app commit -m "ci(STEP-47.7): verify build-android and e2e-android green under AGP 9"
git -C /d/AppDev/mine_flow/Code/mine-flow-app push
```

If no `ci.yml` change was needed, there is no commit. Say so plainly — "verified, no change required"
is a perfectly good substep outcome.

## Verification

- CI `build-android` conclusion **success**, run URL recorded.
- CI `e2e-android` conclusion **success**, run URL recorded.
- The ran-vs-skipped split for `e2e-android` is recorded, with the skip reason quoted.
- `app_boots_test.dart` is confirmed to have actually executed.
- `test` and `e2e-web` remain green (you did not regress 47.6's work).
- No `continue-on-error`, no disabled gate, no modified journey test, no `.dart` change.

If a job cannot be made green, mark it **Unverified** with the exact error and stop. Do not report a
red or cancelled job as passing, and do not describe skipped journeys as verified.

## Keeping the docs true (always)

No `architecture/*` edit here — 47.8 owns documentation. Hand it:

1. Whether the CI Flutter pin changed (3.47.0 → 3.47.1). That is an environment fact that belongs in
   `architecture/09-environments.md`'s parity section.
2. The `e2e-android` ran-vs-skipped reality, so the STEP-47 index row can state plainly that CI E2E is
   green **as a harness gate** while the 14 journeys remain Deferred to STEP-48. Without that sentence,
   a future reader sees three green checks and concludes STEP-48 is unnecessary.

No secrets: reference `STAGING_*` secrets by name only; never echo a value, and never write one into
the workflow file.

## Definition of done

- [ ] `build-android` green on the STEP branch, run URL recorded
- [ ] `e2e-android` green on the STEP branch, run URL recorded
- [ ] Ran-vs-skipped split recorded for `e2e-android`, with the exact skip reason
- [ ] `app_boots_test.dart` confirmed executed (not skipped)
- [ ] `timeout-minutes` present on both jobs; failure artifacts uploaded
- [ ] `test` and `e2e-web` still green
- [ ] Any `ci.yml` change justified in the evidence file; no `continue-on-error`; no gate disabled
- [ ] No journey test or `.dart` file modified
- [ ] Evidence appended to `mine-flow-STEP-47.0-EVIDENCE.md`
- [ ] Committed and pushed, or explicitly recorded as no-change
- [ ] Notes for 47.8 written (CI pin change; harness-green vs journeys-Deferred wording)

## Next

Update 47.7's status in the PLAN, then tell the user the next action: **run substep 47.8**
(documentation: host prerequisites, ADR, risks register) in a fresh chat.
