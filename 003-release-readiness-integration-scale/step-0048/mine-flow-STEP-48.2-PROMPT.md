# mine-flow — STEP-48.2: CI Gate Expansion & Evidence Artifacts

> **How to run:** tell your agent *"run substep 48.2"*. Self-contained — runnable cold.

**Assigned model: Gemini 3.1 Pro High.** Workflow surgery with real traps — the
`android-emulator-runner` newline-splitting behaviour, `dash` without `pipefail`, `flutter drive`'s
single-`--target` limit, and a zero-executed guard that has to distinguish an honest individual skip
from a skip-only run. All of it is bounded by written constraints (this prompt and the existing
comments in `ci.yml`), so it needs careful reasoning rather than the heaviest tier. **Escalate to Opus
4.8** if the guard cannot be made to distinguish those two cases without becoming fragile, or if
expanding the targets surfaces a failure you cannot attribute to a specific journey.


## Context

Read `Upcoming Prompts/mine-flow-STEP-48-PLAN.md`, then the findings from
`mine-flow-STEP-48.0-FINDINGS.md` (credentials, gate verdict) and
`mine-flow-STEP-48.1-FINDINGS.md` (journey repairs).

CI is the **authoritative** evidence surface for STEP-48 (PLAN decision D1). Right now it proves
nothing about the journeys, because both E2E jobs deliberately target a single file:

- `.github/workflows/ci.yml` `e2e-web` → `--target=integration_test/app_boots_test.dart`
- `.github/workflows/ci.yml` `e2e-android` → `flutter test integration_test/app_boots_test.dart`

Both carry STEP-47 comments saying so explicitly: *"Only run the boot smoke test; STEP-48 expands
this target list once credentials are wired up to allow real verification instead of fake greens."*
That is this substep's mandate, quoted from the workflow itself.

Neither job passes `TEST_USER_EMAIL` or `TEST_USER_PASSWORD`, so `isStagingConfigured` is false
and even `app_boots_test.dart` skips. Both jobs still exit 0.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — decision D1 (CI authoritative), the honesty
  rule, and Q3 (the phantom `STAGING_GOOGLE_DRIVE_CLIENT_ID`).
- `Upcoming Prompts/mine-flow-STEP-48.0-FINDINGS.md` — which secrets now exist, by name.
- root `.throughstone/local-user.md` — Experience level 2, Explanatory.
- `Code/mine-flow-app/.github/workflows/ci.yml` — the whole file, especially `test`,
  `build-android`, `e2e-web`, `e2e-android`, `deploy-staging`.
- `Code/mine-flow-docs/architecture/12-test-strategy.md` v1.2 §CI gates.
- `Code/mine-flow-docs/architecture/09-environments.md` v0.4.0 §2 and §4.
- `Code/mine-flow-app/integration_test/helpers/staging_config.dart` — every define the suite reads.

## Scope

**In scope:** `ci.yml` only. Expanding both E2E jobs to the full journey set, injecting the
`TEST_USER_*` secrets, uploading logs and screenshots as artifacts, and making the two jobs'
`--dart-define` sets identical so a journey cannot pass on one platform for a configuration reason.

**Not in scope:** editing test files (48.1 did that), running journeys for per-area evidence
(48.3–48.12), the design-review capture target (48.13 authors it; you make sure CI *can* run it),
risk rows (48.14), docs (48.15). Do not touch `deploy-staging` / `deploy-production` beyond what
the gate change requires.

## Critical CI constraints (learned the hard way — do not rediscover)

**`reactivecircus/android-emulator-runner` splits its `script:` input on newlines** and runs each
line as its own `sh -c`. A trailing `\` continuation is therefore passed to `flutter test` as a
test path, which mixes a non-`integration_test` path into the run and trips *"Integration tests
and unit tests cannot be run in a single invocation."* The existing job carries a long comment
about exactly this. **Keep each command on ONE line.** The shell is `dash`: no `set -o pipefail`,
hence the existing `> log 2>&1; status=$?; cat log; exit $status` idiom rather than a pipe to `tee`.

**Web E2E must use `flutter drive`.** `flutter test integration_test -d chrome` answers *"Web
devices are not supported for integration tests yet"* on Flutter 3.47.x. The `e2e-web` job already
does the right thing (`flutter drive --driver=test_driver/integration_test.dart --target=… -d
web-server --browser-name=chrome`) — note that `flutter drive` takes **one `--target` at a time**,
so multiple journeys mean either a loop over targets or an aggregating entrypoint.

**Choose one aggregation strategy and state why.** Two workable options:

1. **Loop over targets** — a shell loop per journey file, accumulating failures and exiting
   non-zero if any failed. Verbose logs, clear per-journey attribution, slower (one app build per
   target on web).
2. **An aggregating entrypoint** — e.g. `integration_test/all_journeys_test.dart` that imports and
   calls each journey's `main()`. One build, much faster, but a crash in one journey can take down
   the rest and attribution gets muddier.

Recommended: **loop on web** (attribution matters more than minutes for evidence work) and
`flutter test integration_test/` **directory form on Android** (`flutter test` accepts a directory
and reports per-file results) — but confirm the directory form works on the emulator before
relying on it, and keep it on one line.

## Your task

### 1. Inject the credentials into both E2E jobs

Add to `e2e-web` and `e2e-android`, matching the names 48.0 confirmed:

```
--dart-define=TEST_USER_EMAIL=${{ secrets.TEST_USER_EMAIL }}
--dart-define=TEST_USER_PASSWORD=${{ secrets.TEST_USER_PASSWORD }}
```

Plus, only if 48.0 created per-role accounts, the four `TEST_FOREMAN_*` / `TEST_SUPERVISOR_*`
defines that `staging_config.dart` reads.

The two jobs must end up with the **same** define set. A journey that passes on Android and skips
on web because one job forgot a define is a false signal.

### 2. Resolve the phantom Drive define (Q3)

`ci.yml` passes `secrets.STAGING_GOOGLE_DRIVE_CLIENT_ID`, which does not exist in the repository's
secrets — it resolves to an empty string. Apply 48.0's recorded answer: normally **remove it from
the E2E jobs** (Drive is out of STEP-48's scope per D2). Leave `deploy-staging` /
`deploy-production` alone — they use the service-account secrets, which do exist.

### 3. Expand the targets

Point both jobs at the full journey set plus `app_boots_test.dart`, per your chosen aggregation
strategy. Requirements:

- **A skipped test must not silently count as success.** After the run, assert on the real counts:
  parse the log and fail the job if zero tests executed. A job that reports `0 tests passed, N
  skipped` and exits 0 is the exact failure this whole STEP exists to eliminate. Add that check
  explicitly — for example, grep the log for an executed-count pattern and `exit 1` when it is
  zero. State in a comment why the check exists.
- **`data_bucket_journey_test.dart` will legitimately skip** (Drive deferred, D2). Your
  zero-executed check must tolerate *individual* honest skips while still failing when *nothing*
  ran. Decide the rule, implement it, and document it in a comment.
- Give the jobs a realistic `timeout-minutes`. Fourteen journeys on an emulator is far more than a
  boot test — the current `e2e-web` step timeout is 15 minutes and `e2e-android`'s job timeout is
  30. Raise both to a bound you have reasoned about, and say what you based it on.

### 4. Upload evidence artifacts

Evidence must survive the run. Add or extend `actions/upload-artifact@v4` steps with `if: always()`:

- full test logs for both jobs (the Android job already does this — extend it);
- the chromedriver log (already present on failure — make it `always()`);
- a screenshots directory for 48.13's design-review capture, so the mechanism exists before that
  substep needs it. Note that images which must be **durable** get committed to
  `Code/mine-flow-docs/reports/design-review/` (PLAN decision D4) — CI artifacts expire, so they
  are a convenience, not the archive.

Set a `retention-days` you can justify.

### 5. Keep the gate wired

`deploy-staging` has `needs: [build-android, e2e-web, e2e-android]`. Confirm that still holds
after your edits, so a red journey blocks staging deployment. Do not weaken the gate to get a
green pipeline — if journeys fail, that is a finding for the owning substep, not a reason to
loosen CI.

### 6. Prove the workflow actually works

Commit on `step-0048-runtime-evidence`, push, and **watch a real run**. You are not verifying the
journeys here (that is 48.3–48.12) — you are verifying that the *harness executes them*.

Success for this substep: a run where `e2e-web` and `e2e-android` show a **non-zero executed test
count**. Journey failures are expected and fine at this stage; record them and hand them to their
owning substeps.

CI logs are readable without the `gh` CLI: the GitHub PAT lives in Git Credential Manager
(`printf 'protocol=https\nhost=github.com\n\n' | git credential fill`) and works as a Bearer
token. `/actions/jobs/<id>/logs` returns a 302 to Azure Blob Storage, which **rejects** the GitHub
auth header — capture the `redirect_url` and fetch it bare, without the Authorization header.

### 7. Record what you observed

`Upcoming Prompts/mine-flow-STEP-48.2-FINDINGS.md`:

- the diff summary of `ci.yml` and the reasoning behind the aggregation strategy;
- the run URL, per-job status, and the **actual executed / skipped / failed counts** per job;
- a table of every journey and how it behaved in that first real CI run — this is the triage list
  48.3–48.12 work from;
- the zero-executed guard's exact rule and the timeout values chosen, with justification.

## Verification

- `ci.yml` parses (the run starting at all is the proof; a YAML error fails immediately).
- Both E2E jobs carry an identical `--dart-define` set including `TEST_USER_*`.
- No `${{ secrets.STAGING_GOOGLE_DRIVE_CLIENT_ID }}` reference remains in the E2E jobs.
- The `e2e-android` `script:` block is still **one line per command** — no `\` continuations.
- A pushed CI run exists in which both E2E jobs report a non-zero executed test count.
- The zero-executed guard demonstrably works: it must be able to fail. If nothing executed, the
  job must be red.
- `deploy-staging` still `needs` all three upstream jobs.
- No secret value appears in any log, comment, or committed file.

## Keeping the docs true

`architecture/09-environments.md` §4 currently states that a green E2E gate *"proves only that the
test harness executes… The actual 14 staging journeys remain Deferred to STEP-48."* Once this
substep lands, that sentence is on its way to being false. **Do not rewrite it here** — 48.15 owns
the doc sweep and will rewrite it against the full evidence. Note in your findings that the
sentence is now stale so 48.15 cannot miss it.

Likewise, if the real E2E shape ends up differing from `architecture/12-test-strategy.md` v1.2
(for instance if you introduce an aggregating entrypoint the doc does not describe), record it for
48.15 rather than editing the doc now.

## Definition of done

- [ ] `TEST_USER_EMAIL` / `TEST_USER_PASSWORD` (and per-role defines if applicable) injected into
      both E2E jobs, with identical define sets.
- [ ] Phantom `STAGING_GOOGLE_DRIVE_CLIENT_ID` resolved per 48.0's answer.
- [ ] Both jobs target the full journey set; aggregation strategy chosen and justified in a comment.
- [ ] A zero-executed-tests guard added that makes a skip-only run **red**, with its rule
      documented and its tolerance for `data_bucket`'s honest skip explicit.
- [ ] Log and screenshot artifacts uploaded with `if: always()` and a justified retention.
- [ ] `deploy-staging`'s dependency on all three jobs intact.
- [ ] A real pushed CI run observed with **non-zero executed counts** in both E2E jobs; URL and
      counts recorded.
- [ ] `Upcoming Prompts/mine-flow-STEP-48.2-FINDINGS.md` written, including the per-journey triage
      table.
- [ ] Committed on `step-0048-runtime-evidence`.

## Next

Tell the user the next action is *"run substep 48.3"* (auth & session runtime evidence) in a
**fresh chat**, and update 48.2's status in the STEP PLAN. Mention that 48.3 is the gating journey
— everything else depends on login working.
