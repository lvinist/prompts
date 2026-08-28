# mine-flow — STEP-47.0: Pre-flight — baseline evidence & CI failure diagnosis

> **How to run:** Tell your agent *"run substep 47.0"* (or *"read and run this file"*).
> This file is self-contained; it does not depend on the chat that produced it.
>
> **Model:** Gemini 3.7 Flash High. This substep gathers and records facts — no code changes.

## Context

STEP-47 restores the Android build chain. Its PLAN is
`Upcoming Prompts/mine-flow-STEP-47-PLAN.md` — read it before starting.

This is the STEP's pre-flight. STEP-49's lesson #3 is that runtime STEPs must prove their
toolchain and credentials *before* doing work that assumes them. STEP-45 skipped that and produced
14 tests that never ran. So 47.0 writes down the exact starting state, so that every later substep
can be measured against it and nobody has to re-derive it.

It also settles one thing the planning session could **not**: why CI's three Android/web jobs are
failing. GitHub's job-log endpoint returns HTTP 403 without a token, so the failures were inferred,
not read. This substep replaces inference with evidence.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-47-PLAN.md` — the STEP PLAN, especially "Root cause" and
  "CI is red for a second, independent reason"
- root `.throughstone/local-user.md` — Experience level 2, Explanatory. Write the evidence file so
  a reader who is not a Gradle expert can follow it.
- `Code/mine-flow-docs/architecture/09-environments.md` — where staging credentials come from
- `Code/mine-flow-docs/architecture/12-test-strategy.md` §6 — the authoritative CI gate list
- `Code/mine-flow-app/README.md` — current setup instructions (you will find them incomplete)
- `Code/mine-flow-app/.github/workflows/ci.yml` — all five jobs

## Scope

**Owns:** collecting and writing down evidence. Creating the STEP branch.

**Does NOT touch:** `pubspec.yaml`, `pubspec.lock`, any `.dart` file, `android/gradle.properties`,
`ci.yml`. No fixes in this substep — later substeps own those.

## Your task

### 1. Create the STEP branch in all three repos

Same branch name everywhere. First confirm each repo is clean; if any repo has uncommitted work
that is not yours, **stop and report it** — do not stash, reset, or commit it.

```bash
cd /d/AppDev/mine_flow
git -C Code/mine-flow-app  status --short --branch
git -C Code/mine-flow-docs status --short --branch
git -C prompts             status --short --branch
```

Note: `Code/mine-flow-app` uses `master` as its trunk; the other two use `main`. Then:

```bash
git -C Code/mine-flow-app  switch -c step-0047-android-build-chain
git -C Code/mine-flow-docs switch -c step-0047-android-build-chain
git -C prompts             switch -c step-0047-android-build-chain
```

### 2. Record the host toolchain

```bash
flutter --version
dart --version
java -version              # expect Temurin 17
flutter config             # confirm jdk-dir points at the JDK 17 install
echo "$PUB_CACHE"          # expect D:\AppDev\.pub-cache — same drive as SDK and project
flutter doctor -v
flutter emulators
```

Capture the versions verbatim. The `PUB_CACHE` drive rule and the JDK 17 pin are real
prerequisites discovered the hard way; 47.8 documents them, and this is the evidence it cites.

### 3. Reproduce the local build failure and capture it verbatim

```bash
cd /d/AppDev/mine_flow/Code/mine-flow-app
flutter build apk --debug 2>&1 | tee "$LOCALAPPDATA/Temp/step47-baseline-apk.log"
```

Expect failure. The PLAN predicts, from a real run on 2026-08-28:

- `Failed to apply plugin 'kotlin-android'` in
  `.pub-cache/hosted/pub.dev/package_info_plus-9.0.1/android/build.gradle` line 26
- followed by `project ':package_info_plus' does not specify compileSdk` — a *consequence* of the
  first error, because the `android { }` block on line 30 never evaluates

**If what you see differs from that, say so explicitly.** A changed failure mode changes the STEP.

Do **not** try `android.builtInKotlin=false`. It was already tried and reverted: it gets past
configuration but then fails at `:app:compileDebugJavaWithJavac` with
`cannot find symbol: class FilePickerPlugin`, because `file_picker` 11.0.3's Kotlin output does not
land in the jar `:app` compiles against. Re-running it wastes ~3 minutes and proves nothing new.

### 4. Record the current baseline gates (these must not regress)

```bash
flutter analyze
dart format --output=none --set-exit-if-changed lib/ test/
flutter test
dart run tool/check_supabase_contracts.dart
dart run tool/check_l10n_baseline.dart
```

Expected from STEP-46.4: analyze **0 issues**, `flutter test` **442 passing**. Record the actual
numbers — they are the bar for the rest of the STEP.

### 5. Diagnose the three failing CI jobs

The most recent `master` run is `3b45176` (2026-08-28), conclusion `failure`. Per-job conclusions
are readable without auth:

```bash
curl -s "https://api.github.com/repos/lvinist/mine-flow-app/actions/runs?per_page=5&branch=master" \
  | python -c "import json,sys; [print(r['id'], r['head_sha'][:8], r['conclusion']) for r in json.load(sys.stdin)['workflow_runs']]"
curl -s "https://api.github.com/repos/lvinist/mine-flow-app/actions/runs/<RUN_ID>/jobs" \
  | python -c "import json,sys; [print(j['name'], j['conclusion'], [s['name'] for s in j['steps'] if s['conclusion']=='failure']) for j in json.load(sys.stdin)['jobs']]"
```

Known so far: `Lint, analyze & test` **success**; `Build Android APK` **failure** at "Build Android
debug APK"; `E2E Tests (Android)` **failure** at "Run E2E tests on Android emulator"; `E2E Tests
(Web)` **failure** at "Run E2E tests on Chrome". History shows `build-android` was **green through
2026-08-26** (`55361914`) and first went red on `3b45176` — the commit that added
`package_info_plus: ^9.0.1` and `integration_test`. That timing is strong evidence CI fails for the
same reason the local build does.

**Log bodies need auth** (`GET /actions/jobs/<id>/logs` → 403). Try, in order, until one works:

1. `gh` CLI, if the user has it authenticated (it was **not** on PATH during planning).
2. A `GITHUB_TOKEN`/`GH_TOKEN` already exported in the environment —
   `curl -sL -H "Authorization: Bearer $GITHUB_TOKEN" …`. Do not print the token.
3. Ask the user to paste the failing step's log tail, or to open the run URL:
   `https://github.com/lvinist/mine-flow-app/actions/runs/33163983709`.

If none works, record the CI root cause as **Unverified (log access unavailable)** plus the
timing-based inference — clearly labelled as inference. Do not write it up as confirmed.

### 6. Answer Q1 — do the staging secrets exist?

`ci.yml` reads `secrets.STAGING_SUPABASE_URL`, `secrets.STAGING_SUPABASE_ANON_KEY`, and
`secrets.STAGING_GOOGLE_DRIVE_CLIENT_ID`. Establish whether they are actually configured. Evidence
that counts: a green historical `e2e-web`/`e2e-android` run, a secrets listing the user provides, or
the user's direct answer. A missing secret does not block STEP-47 (the journeys self-skip), but
STEP-48 depends on it, so the answer belongs on the record now.

**Never print a secret value.** Refer to them by name only.

### 7. Confirm the `e2e-web` invocation bug

`ci.yml` line 140 runs `flutter test integration_test -d chrome`. Confirm locally that Flutter
rejects this:

```bash
flutter test integration_test -d chrome 2>&1 | tail -5
```

Expected: *"Web devices are not supported for integration tests yet"*. Also confirm that
`test_driver/integration_test.dart` exists (it does) and is referenced nowhere in `ci.yml` — that
unused driver is what 47.6 will wire up.

### 8. Write the evidence file

Create `Upcoming Prompts/mine-flow-STEP-47.0-EVIDENCE.md` with these sections:

1. **Host toolchain** — Flutter/Dart/Java/Gradle versions, `PUB_CACHE`, JDK dir, emulators
2. **Local APK failure** — the verbatim error block, plus one plain-language paragraph explaining
   that the `compileSdk` message is a knock-on effect of the plugin-apply failure
3. **Baseline gates** — analyze/format/test/contract-guard results as numbers
4. **CI per-job status** — table of job → conclusion → failing step, with the run URL
5. **CI root cause** — Confirmed (with log excerpt) or Unverified (with the inference labelled)
6. **Q1 staging secrets** — Present / Absent / Unverified, by name only
7. **`e2e-web` invocation** — the verbatim rejection message
8. **Hypotheses already eliminated** — carry forward the PLAN's list so no later substep re-tries them

Commit it:

```bash
git -C prompts add "../Upcoming Prompts/mine-flow-STEP-47.0-EVIDENCE.md" 2>/dev/null || true
# Upcoming Prompts/ lives at the workspace root and is not itself a repo; if it is untracked
# there, keep the file in place and note in the PLAN that it will be archived at close (47.9).
```

If `Upcoming Prompts/` is outside version control on this machine (expected — see
`prompts/README.md`: it is "a workspace folder for the in-flight STEP, not generally a repo"), do
**not** force it into a repo. It gets archived into `prompts/003-…/step-0047/` at close.

## Verification

This substep writes no code, so it has no unit tests — its deliverable *is* evidence. It is done
when:

- All commands in §2–§7 have been run and their real output recorded.
- Every claim in the evidence file traces to a command output or an explicit user answer.
- Anything that could not be run is labelled **Unverified** with the reason.

Self-check before finishing: does the evidence file contain any sentence you could not point at a
command output for? If yes, delete it or mark it as inference.

## Keeping the docs true (always)

This substep changes no architecture decision, so no `architecture/*` doc changes here. It does
surface undocumented host prerequisites (PUB_CACHE drive rule, JDK 17) — **do not** document them
yet; 47.8 owns that, and doing it twice creates drift. Just make sure the evidence file captures
them clearly enough for 47.8 to cite.

No secrets in the repo: the evidence file names secrets, never their values.

## Definition of done

- [ ] Branch `step-0047-android-build-chain` created in `mine-flow-app`, `mine-flow-docs`, `prompts`,
      each from a clean tree
- [ ] Host toolchain recorded verbatim
- [ ] Local `flutter build apk --debug` failure reproduced and captured; any deviation from the
      PLAN's predicted failure flagged
- [ ] Baseline analyze / format / test / contract-guard numbers recorded
- [ ] Per-job CI status table recorded with run URL; root cause Confirmed or explicitly Unverified
- [ ] Q1 (staging secrets) answered by name, never by value
- [ ] `e2e-web`'s `-d chrome` rejection confirmed locally
- [ ] `mine-flow-STEP-47.0-EVIDENCE.md` written in `Upcoming Prompts/`
- [ ] No code, dependency, or workflow file modified by this substep
- [ ] No `.env` or secret value read or printed

## Next

When this substep is done, update its status in `Upcoming Prompts/mine-flow-STEP-47-PLAN.md`, then
tell the user the next action: **run substep 47.1** in a fresh chat.
