# mine-flow — STEP-48.24: Local Full-Gate Re-run

> **How to run:** tell your agent *"run substep 48.24"*. Self-contained — runnable cold.

**Assigned model: Gemini 3.7 Flash High.** Procedural work with an unambiguous pass/fail signal: run
the gates, run every journey on both platforms, record the real counts. No design decisions, no code
authorship. The one thing that requires care is the difference between a flake and a regression.
**Escalate to Opus 4.8** if a journey fails and you cannot tell whether it is a flake or a regression,
if a previously-passing journey has newly broken (a remediation substep caused a regression), or if a
fix attempt fails twice.

## Why this substep exists

Substeps 48.17–48.23 each fixed a slice of the branch-head failures and each verified its own slice.
Nobody has yet run **everything together** since the fixes landed. That is exactly the gap that
produced the red branch-head gate in the first place: fifteen files verified one at a time, then a
different result when run as a suite.

48.26 spends a full CI run — two emulator/browser jobs, up to an hour — to get the authoritative
verdict. Your job is to catch locally whatever would have made that run red, so 48.26 gets a clean
answer instead of another triage cycle.

You are **not** authorised to close anything. You produce evidence and a recommendation: ready for
48.25 (git repair) and 48.26 (CI), or not, and why.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — the 2026-08-31 amendment, the honesty rule, decision
  **D1** (CI is authoritative; local is for iteration), and the Test plan section.
- **Every remediation findings file that exists**: `…-48.16-` through `…-48.23-FINDINGS.md`. You need,
  for each:
  - what it fixed,
  - what it left **Deferred** and why (those journeys may legitimately still skip or fail),
  - what it handed forward to another substep.
- root `.throughstone/local-user.md` — Experience level 2, Explanatory.
- `Code/mine-flow-app/.github/workflows/ci.yml` — the `e2e-web` and `e2e-android` steps. Mirror the
  **same** invocations locally so your results predict CI's. Read the comment block above the Android
  `script:` input: `reactivecircus/android-emulator-runner` splits that input on newlines and runs each
  line through its own `sh -c`, so the whole command is on one physical line for a reason. Do not
  reformat it.
- `Code/mine-flow-docs/architecture/12-test-strategy.md` — the tier definitions and the dual-platform
  gate.

## Known conditions — do not rediscover these

- **Web E2E must use `flutter drive`.** `flutter test integration_test -d chrome` answers *"Web devices
  are not supported for integration tests yet"* on Flutter 3.47.x. CI loops per file with
  `flutter drive --driver=test_driver/integration_test.dart --target=<wrapper> -d web-server
  --browser-name=chrome`; chromedriver must be running on port 4444.
- **Known flake:** `test/integration/attendance_daily_log_sync_test.dart` and
  `test/integration/equipment_check_sync_test.dart` fail intermittently in a full-suite run on Hive
  `setUpAll`, and are green in isolation and on a clean re-run. That is a *diagnosis*, not a licence —
  see below.
- **`flutter analyze` exits non-zero on any issue, including infos.** Measure the command's own exit
  code (`cmd; echo $?`), never through a pipe — a pipe reports the last command's status and masks
  failure.
- **A green job is not evidence.** `flutter test` exits 0 when every test calls `markTestSkipped`, and
  `flutter drive` prints `All tests passed.` for a file whose only test skipped. Always extract the
  ran-vs-skipped split.
- **The baseline is 448 passing** unit/widget/integration tests as of STEP-47, plus whatever the
  remediation substeps added. If your count is *lower* than the sum of the baseline and the additions,
  tests were deleted — find out which and by whom.

## Your task

### 1. Confirm the tree you are testing

```bash
cd Code/mine-flow-app && git log --oneline -15 && git status --short
```

Every remediation substep's changes must be present in the working tree, and you must know which are
committed vs. only on disk.

**Known blocker (do not be surprised by it):** as of 48.23 the `mine-flow-app` **git object store is
corrupt** — a bad pack (`pack-52610b3e…`) plus ~30 corrupt loose objects — so `git add`/`commit`
fail and the two most recent commits (48.18 `09e4821`, 48.19 `d143167`) have unreadable tree objects.
The repair is **48.25's** job, deliberately sequenced *after* this substep. That means: **you cannot
rely on `git` to tell you the tree is clean, and you cannot commit.** Test the **working tree on
disk** — it is intact and is the source of truth — and record the git state honestly (corrupt,
uncommitted work present on disk). Do **not** attempt to repair git here; do not `gc`, `repack`,
`index-pack`, or delete packs. If a gate or test needs a file that the corruption deleted from disk
(notably `supabase/types/database.ts`), record it as blocked-on-48.25 rather than working around it.

Do the same inspection in `Code/mine-flow-docs`.

### 2. Static gates

```bash
cd Code/mine-flow-app
flutter analyze; echo "analyze exit: $?"
dart format --set-exit-if-changed .; echo "format exit: $?"
dart run tool/check_supabase_contracts.dart; echo "contracts exit: $?"
```

All three must exit 0. The contract guard matters because 48.17 changed migrations and regenerated
`supabase/types/database.ts`; if it fails now, the artifact and the migrations have drifted apart.

### 3. Unit / widget / integration suite

```bash
flutter test
```

Record the exact final line (`NN tests passed`, plus any failures). Then:

- **If a test fails, do not report the suite as green.** Determine flake vs regression:
  1. Re-run that file in isolation. Green in isolation + green on a clean full re-run = consistent with
     the known Hive flake; say so explicitly and name the file.
  2. Red in isolation, or red repeatedly = a **regression**. Identify which remediation substep's change
     caused it (`git log -p` on the file and its dependencies) and report it. Do not fix another
     substep's regression silently — report it, and only fix it if it is a one-line obvious slip, in
     which case say so plainly.
- Compare the count to the expected baseline plus additions. Explain any shortfall.

### 4. Every journey, both platforms

Run **all fifteen** `integration_test` files, not only the ones that were failing — a fix can break a
neighbour, and that is the failure mode this substep exists to catch.

Android (emulator booted first; `flutter emulators --launch Pixel_6a`, then confirm with
`flutter devices`):

```bash
flutter test integration_test/ -d emulator-5554 \
  --dart-define=SUPABASE_URL=… --dart-define=SUPABASE_ANON_KEY=… \
  --dart-define=TEST_USER_EMAIL=… --dart-define=TEST_USER_PASSWORD=… \
  --dart-define=TEST_SUPERVISOR_EMAIL=… --dart-define=TEST_SUPERVISOR_PASSWORD=… \
  --dart-define=TEST_FOREMAN_EMAIL=… --dart-define=TEST_FOREMAN_PASSWORD=… \
  --dart-define=APP_ENV=staging
```

Web (chromedriver on 4444, then per file as CI does).

Ask the user for the credential values, or read them from the environment if they are already exported.
**Never print a value.** Reference secrets by name only, in every log, findings file, and report.

Produce a per-file table:

| Journey file | Android: passed / failed / skipped | Web: passed / failed / skipped | Skip reason (verbatim) | Expected? |
|---|---|---|---|---|

"Expected?" means: does a remediation findings file explain this outcome? A skip with a named reason
that 48.20 or 48.23 recorded as Deferred is expected. A skip nobody predicted is a finding — and a
*pass* nobody predicted deserves a second look too, in case the test went vacuous.

Cross-check the totals against the branch-head baseline: Android was `14 passed, 10 failed, 2 skipped`.
State the new triple and the delta.

### 5. Verify the skips are honest

For every skipped test, confirm the pattern 48.1 established: `markTestSkipped('<named reason>')`
immediately followed by `return;`, so no assertion after it is silently bypassed. And confirm no test
passes **vacuously** — a body of `print(...)` plus `expect(true, isTrue)` manufactures a green.
48.1 removed one of those from `deep_link_journey_test.dart`; verify none has crept back:

```bash
grep -rn "expect(true" integration_test/
grep -rnc "markTestSkipped" integration_test/
```

### 6. Predict CI

State plainly whether a branch-head CI run would now pass all four jobs, and what could still differ
between your host and CI:

- CI's emulator is a freshly created API-33 `pixel_6a` AVD, not your local `Pixel_6a`;
- CI's chromedriver version tracks whatever `setup-chrome` installs;
- CI runs `e2e-web` and `e2e-android` after `test`, on the pushed commit, with a 60-minute timeout;
- CI's `e2e-web` has a **zero-executed guard** — if the aggregated log shows nothing passed and nothing
  failed, the job fails deliberately. Confirm your run would not trip it.

Recommend **go** or **no-go** for 48.25. A no-go with a named blocker is a perfectly good outcome and
far better than burning an hour of CI to rediscover it.

## Verification

- Tree confirmed clean and containing every remediation commit; shas recorded.
- `flutter analyze`, `dart format`, and the contract guard each recorded with their own exit code.
- `flutter test` count recorded and reconciled against baseline + additions.
- Any failure classified flake-vs-regression with the isolation evidence shown.
- All fifteen journeys run on Android and on web; the per-file table is complete.
- Every skip's verbatim reason recorded and matched to a findings file, or flagged.
- No vacuous pass; grep evidence included.
- New triple stated against the `14/10/2` baseline.
- Explicit go/no-go recommendation for 48.25.
- No secret value anywhere in the output.

## Scope

**In scope:** running gates and journeys, recording counts, classifying flake vs regression, verifying
skip honesty, and recommending go/no-go.

**Not in scope:** fixing defects (they belong to 48.17–48.23 — report and route), authoring or
modifying tests, migrations, staging mutation, doc edits, `risks.yml`, running CI (48.25), and closing
the STEP (48.15).

## Definition of done

- [ ] Tree state confirmed; all remediation commits present; both repos clean.
- [ ] `flutter analyze` 0, `dart format` clean, contract guard 0 — each with its exit code recorded.
- [ ] `flutter test` result recorded; every failure classified flake-vs-regression with evidence.
- [ ] All fifteen journeys run on both platforms; per-file ran/failed/skipped table complete.
- [ ] Every skip reason verbatim and reconciled with a findings file.
- [ ] Vacuous-pass check clean.
- [ ] New Android/web triples stated against the branch-head baseline, with the delta explained.
- [ ] CI-vs-local differences named; zero-executed guard considered.
- [ ] Go/no-go recommendation for the CI gate (48.26), with named blockers if no-go.
- [ ] Git corruption state recorded; **no** repair attempted here (that is 48.25); files blocked on it named.
- [ ] `mine-flow-STEP-48.24-FINDINGS.md` written; PLAN progress table updated.
- [ ] Nothing else modified — `git status` proves it.

## Next

Regardless of go/no-go on the **test** evidence, the next action is **"run substep 48.25"** (the
`mine-flow-app` git repair) in a **fresh chat** — the corrupt object store must be repaired and this
wave's work committed before any CI run is possible. Hand 48.25 your findings: which changes are
uncommitted-on-disk, whether `supabase/types/database.ts` is present, and your go/no-go on the test
evidence itself.

If your test evidence is **no-go** for reasons *other* than git (a real regression in a journey or
the suite), name the remediation substep that must re-run first — that fix should land **before**
48.25 commits, so the repaired history is correct in one pass.
