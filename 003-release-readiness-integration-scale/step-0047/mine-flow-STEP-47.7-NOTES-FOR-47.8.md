# Notes from 47.7 for 47.8

## 1. CI Flutter pin changed: 3.47.0 → 3.47.1

`.github/workflows/ci.yml` now pins `flutter-version: "3.47.1"` in all five Flutter jobs
(`test`, `build-android`, `e2e-web`, `e2e-android`, `deploy-staging`, `deploy-production`),
matching the local host recorded in 47.0 §1.

This belongs in `architecture/09-environments.md`'s parity section as an environment fact.
Please state it as parity, **not** as a fix: `build-android` was already green on 3.47.0
(run `33179964952`, commit `85819ab2`), and the `flutter_tools` guard that produced the
`e2e-android` failure is byte-identical between the two tags
(`git diff 3.47.0..3.47.1 -- packages/flutter_tools/lib/src/commands/test.dart` → empty).
Claiming the bump fixed anything would be wrong.

## 2. E2E is green **as a harness gate**; the journeys remain Deferred

This is the sentence STEP-47's index row needs, or a future reader sees three green checks
and concludes STEP-48 is unnecessary. Suggested wording:

> CI `build-android`, `e2e-web`, and `e2e-android` are green as **harness gates**: the debug
> APK builds under AGP 9, the emulator boots, the app installs, and the `integration_test`
> harness runs and reports honestly. Both E2E jobs target `app_boots_test.dart` only, and
> that test **self-skips** with `Unverified: Staging credentials absent` because
> `TEST_USER_EMAIL`/`TEST_USER_PASSWORD` are not configured. **No journey — and not even app
> boot — is runtime-verified.** All 14 staging journeys remain Deferred to STEP-48.

Exact `e2e-android` split from run `33192242889`: **0 tests passed, 1 skipped**, skip reason
verbatim `Unverified: Staging credentials absent`.

## 3. The 47.7 Definition-of-done line that cannot be satisfied

The 47.7 prompt asked to confirm `app_boots_test.dart` *actually executed (not skipped)*.
It did not, and it cannot on CI today: its guard is `isStagingConfigured`, which needs
`TEST_USER_EMAIL` + `TEST_USER_PASSWORD`, and neither is wired into `ci.yml`. Recorded as
**Unverified** in the evidence file (§10) — credential-blocked, not code-blocked. If the
STEP-47 index row or PLAN checklist repeats that line, it should carry the same qualifier.

## 4. Doc 12 §6 CI Gates — wording drift (adds to 47.6's note)

47.6 already flagged that Web E2E needs `flutter drive` + chromedriver rather than
`flutter test -d chrome`. Add for Android: the emulator job runs a **single** test file, not
the directory. `architecture/12-test-strategy.md` §6's line "Dual-Platform E2E Tests (Chrome
and Pixel 6a)" is still accurate about *which platforms* gate the merge, but the gate's
current *depth* is boot-smoke-only on both. Worth a clause so the doc isn't read as claiming
journey coverage.

## 5. Q5 input — ADR scope

47.7 changed no dependency and no Gradle posture, so it adds nothing to the
`flutter_secure_storage_windows` override reversal question. One security-adjacent fact for
whatever ADR or Version Log entry you write: 47.7 **removed** a workflow-wide
`permissions: contents: write` that a debug commit (`5d62579b`) had added. Only
`deploy-staging` and `deploy-production` need write, and both already declare it at job
scope. Least-privilege restored, not newly granted.

## 6. Housekeeping for STEP close (47.9, not 47.8)

`refs/heads/ci-logs` (`cad3677e`) exists on `origin` — residue from the removed
`Push log to branch` debug step, which force-pushed it on every run. Delete it at close.

## 7. Reusable diagnostic fact (worth a line in the app README's CI section)

CI job logs *are* readable from this host without `gh`: the GitHub PAT is already in Git
Credential Manager (`git credential fill` for `host=github.com`), and
`GET /repos/<owner>/<repo>/actions/jobs/<id>/logs` accepts it as a Bearer token. The
endpoint 302-redirects to Azure blob storage, which rejects a request still carrying the
GitHub `Authorization` header, so the redirect must be followed with a bare request. 47.0
recorded logs as inaccessible (403) and every subsequent CI failure was diagnosed by
guesswork until this was found — which is why `e2e-android` took eight red runs.
