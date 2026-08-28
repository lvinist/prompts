# mine-flow — STEP-47 PLAN: Android Build Chain Remediation (AGP 9 / local device builds)

**Phase:** Phase 3 — Release Readiness, Integration & Scale
**Owner:** Hermes (planning) → per-substep model assignment in the substep table
**Status:** Done (closed 2026-08-29 by 47.9)
**Date:** 2026-08-28
**Branch:** `step-0047-android-build-chain` (same name in `mine-flow-app`, `mine-flow-docs`, `prompts`)
**Repos (projection):** `mine-flow-app` (primary), `mine-flow-docs`, `prompts` — merge order: app → docs → prompts

> STEP-47 restores a buildable Android surface. The local `flutter build apk --debug` and CI's
> `build-android`, `e2e-android`, and `e2e-web` jobs are all red. The root cause is a dependency
> graph that predates AGP 9: two plugins still apply the Kotlin Gradle Plugin unconditionally, and
> they are welded to the rest of the graph through `win32`, so the fix is a coordinated
> dependency sweep — not a Gradle flag. STEP-48's runtime evidence cannot start until this passes.

---

## Motivation

STEP-43 upgraded the toolchain to Flutter 3.47 / AGP 9.1.0 / KGP 2.4.0 and left the
`android.newDsl=false` + `android.builtInKotlin=true` opt-out flags in `android/gradle.properties`.
That combination has never produced a local APK. STEP-45 then authored 15 `integration_test`
journeys that could not be executed on a device, and 14 of them are still `Deferred`/Unverified
in `prompts/STEP-index.md`. STEP-48 owns that runtime evidence, but it is blocked on two things
STEP-47 delivers: a debug APK that builds, and CI E2E jobs that actually invoke the harness.

### Root cause — established from real runs, not inference

Two `flutter build apk --debug` runs on this host (2026-08-28) produced the following.

**With `android.builtInKotlin=true` (current committed state):**

```
* Where: D:\AppDev\.pub-cache\hosted\pub.dev\package_info_plus-9.0.1\android\build.gradle line: 26
> Failed to apply plugin 'kotlin-android'
  The 'org.jetbrains.kotlin.android' plugin is no longer required for Kotlin support since AGP 9.0.
+ com.android.builder.errors.EvalIssueException: project ':package_info_plus' does not
  specify `compileSdk` in build.gradle
```

The `compileSdk` complaint is a *consequence*, not a second bug: `apply plugin: 'kotlin-android'`
throws before the `android { }` block on line 30 is ever evaluated, so `compileSdk` is never set.
The earlier hypothesis in the reservation outline — "the `flutter` extension is not populated in
plugin subprojects, so `flutter.compileSdkVersion` resolves null" — is **wrong** and must not be
carried into implementation. `FlutterExtension.kt:23` hardcodes `compileSdkVersion = 36` and the
extension resolves fine; the plugin block simply never runs.

**With `android.builtInKotlin=false` (tried, then reverted — do not re-try):**

Configuration now succeeds and Gradle warns
`Your app uses the following plugins that apply Kotlin Gradle Plugin (KGP): file_picker, package_info_plus`,
but the build fails later at compile:

```
GeneratedPluginRegistrant.java:34: error: cannot find symbol
  flutterEngine.getPlugins().add(new com.mr.flutter.plugin.filepicker.FilePickerPlugin());
symbol: class FilePickerPlugin
Execution failed for task ':app:compileDebugJavaWithJavac'
```

Inspecting the intermediates shows why: `file_picker` 11.0.3's classes compiled into
`build/file_picker/intermediates/built_in_kotlinc/…` (AGP's built-in compiler ran anyway), but
`compile_library_classes_jar/…/classes.jar` — the jar `:app` compiles against — contains only
`R.class`. The legacy-KGP opt-out and AGP 9's built-in Kotlin disagree about which jar carries the
Kotlin output. **The flag cannot fix this. The plugins must be upgraded.**

### Why this becomes a full dependency sweep

`package_info_plus` ≥10.2.0 and `file_picker` ≥12 are the AGP-9-native versions, and both are
constrained through `win32`:

| Package | Requires |
|---|---|
| `package_info_plus` 9.x | `win32 ^5.5.3` |
| `flutter_secure_storage` 11 → `flutter_secure_storage_windows` 4.2.2 | `win32 ^6.0.1` |
| `file_picker` 12 → `windows_file_picker` | `win32 ^6.3.0` |

STEP-43 papered over the first two rows with `dependency_overrides: flutter_secure_storage_windows: 4.0.0`.
That override is what pins `win32` to 5.x, and it makes every partial upgrade unresolvable.
Verified with real `flutter pub get` runs in a scratch project:

- `package_info_plus ^10.2.1` + the override → **fails** (`fss_windows <4.2.0` needs win32 ^5.5.4).
- `file_picker ^12.1.1` + `package_info_plus ^9.0.1` → **fails** (`windows_file_picker` needs win32 ^6.3.0).
- Both upgraded **and the override deleted** → **resolves**: `file_picker` 12.1.2,
  `android_file_picker` 1.0.3, `windows_file_picker` 1.1.0, `package_info_plus` 10.2.1,
  `flutter_secure_storage_windows` 4.2.2, `win32` 6.4.0, **zero `dependency_overrides`**.

With the graph open, `flutter pub upgrade --major-versions` then resolves 7 further major bumps
cleanly (`flutter_bloc` 9, `bloc_test` 10, `go_router` 18, `googleapis` 17, `googleapis_auth` 2,
`proj4dart` 3, `flutter_lints` 6) and leaves *all direct dependencies up to date*. The user
approved sweeping these in the same STEP rather than leaving 27 packages stale.

**Post-sweep KGP audit (verified against the resolved lock):** only three plugins still apply KGP
and **all three guard it behind an AGP-major check**, so built-in Kotlin can stay enabled:
`android_file_picker` 1.0.3 (checks AGP major *and* the `android.builtInKotlin` property),
`battery_plus` 7.1.1 (`if (agpMajor < 9)`), `package_info_plus` 10.2.1 (`if (agpMajor < 9)`).

### CI is red for a second, independent reason

`ci.yml` line 140 runs `flutter test integration_test -d chrome`. Flutter does not support that —
locally it answers *"Web devices are not supported for integration tests yet"*. A `test_driver/integration_test.dart`
already exists, unused. The `e2e-web` job needs `flutter drive` + chromedriver. `e2e-android`'s
failure is presumed to be the same APK build failure inside the emulator runner, but the
authoritative CI logs are **not readable without a token** (`GET .../jobs/<id>/logs` → 403), so
47.0 must confirm it rather than assume.

---

## Decisions already locked

- root `.throughstone/local-user.md` — Experience level 2, Explanatory communication style.
  Substep prompts explain *why*, not just *what*.
- **ADR-0017** (expanded E2E tier) — the `integration_test` tier and its CI gates are settled;
  STEP-47 fixes how they are invoked, it does not renegotiate the tier.
- **`architecture/12-test-strategy.md` §6 CI Gates** — the gate set is authoritative. Adding a
  chromedriver step is an invocation fix; changing which gates exist would need a doc bump.
- **`architecture/09-environments.md`** — staging credentials come from `--dart-define`/repo
  secrets. STEP-47 does not add, read, or print any credential.
- **RISK-0008** — `flutter_secure_storage` v9→v11 skipped the v10 key migration, accepted as
  dev-only. This STEP keeps `flutter_secure_storage` at ^11.0.0; it must not silently change the
  Keystore posture. Deleting the `flutter_secure_storage_windows` override *raises* that package
  4.0.0 → 4.2.2, which is a Windows-desktop-only surface — note it, don't hide it.
- **RISK-0009** — flutter/flutter#191095 semantics regression: widget/integration finders target
  `EditableText`, never `TextField`. `forui` must stay ≥0.26. Any test touched in this STEP keeps
  that pattern.
- **STEP-43's Windows Kotlin-daemon workaround** in `android/gradle.properties`
  (`kotlin.compiler.execution.strategy=in-process`, `kotlin.incremental=false`) — retain unless a
  substep proves with evidence that built-in Kotlin makes it unnecessary.
- **`android/app/build.gradle.kts` is already migrated** to built-in Kotlin: it has no
  `kotlin-android` plugin and already uses the `kotlin { compilerOptions { jvmTarget } }` block.
  The app module needs no migration work — only the plugins do.
- Host prerequisites already fixed and to be *documented*, not re-litigated: `PUB_CACHE` must sit
  on the same drive as the SDK and project (`D:\AppDev\.pub-cache`), and JDK 17 (Temurin) is wired
  via `flutter config --jdk-dir`. Flutter SDK version skew (3.47.0 vs 3.47.1) was ruled out.

---

## Substeps

Model column: **Flash** = Gemini 3.7 Flash High, **Pro** = Gemini 3.1 Pro High. Escalate a substep
to Opus 4.8 only if it fails twice with a diagnosed-but-unresolved root cause; record the
escalation in the substep's status line.

| # | Title | Model | Produces | Depends on | Open questions | Status |
|---|-------|-------|----------|------------|----------------|--------|
| 47.0 | Pre-flight: baseline evidence & CI failure diagnosis | Flash | `mine-flow-STEP-47.0-EVIDENCE.md` — verbatim local failure, per-job CI conclusions, host toolchain versions, confirmation that repo secrets exist | — | Q1 (answered) | **Done** |
| 47.1 | Dependency graph remediation (pubspec + lock, override deletion) | Pro | `pubspec.yaml`/`pubspec.lock` resolving with zero `dependency_overrides`; KGP audit table | 47.0 | — | **Done** |
| 47.2 | `file_picker` 12 federated-API migration | Pro | `upload_file_page.dart` migrated off `FilePickerResult`/`withData`; widget + cubit tests | 47.1 | Q2 | **Done** |
| 47.3 | `bloc` 9 / `flutter_bloc` 9 / `bloc_test` 10 migration | Pro | 53 bloc source files + 11 `bloc_test` suites compiling and green | 47.1 | — | **Done** |
| 47.4 | `go_router` 18, `googleapis` 17, `proj4dart` 3, `flutter_lints` 6 migration | Pro | router, Drive service, CRS utils clean; `flutter analyze` 0 issues under lints 6 | 47.1 | Q3 (answered) | **Done** |
| 47.5 | Local Android build green + emulator boot | Pro | `flutter build apk --debug` exits 0; `app_boots_test.dart` runs on `Pixel_6a`; gradle.properties posture recorded | 47.2, 47.3, 47.4 | Q4 (answered) | **Done** |
| 47.6 | CI `e2e-web`: replace `-d chrome` with `flutter drive` + chromedriver | Pro | `ci.yml` `e2e-web` job green | 47.5 | — | **Done** |
| 47.7 | CI `build-android` + `e2e-android` green | Flash → **Opus 4.8** (escalated: Gemini 3.7 Flash High and 3.1 Pro High both failed this substep across 8 red runs) | both jobs green on the STEP branch | 47.5 | — | **Done** — run `33192242889`: `test`/`build-android`/`e2e-web`/`e2e-android` all **success**. `build-android` needed no change (fixed by 47.1–47.5). `e2e-android` root cause: `android-emulator-runner` splits `script:` on newlines into separate dash `sh -c` calls, so the `\` continuation was passed to `flutter test` as a stray path → "Integration tests and unit tests cannot be run in a single invocation". Fixed by a one-line script; target narrowed to `app_boots_test.dart` (boot-only, per this PLAN's test plan). **E2E green is a harness gate only: 0 passed, 1 skipped, `Unverified: Staging credentials absent`** — `app_boots_test.dart` did not execute its assertions (no `TEST_USER_EMAIL`/`TEST_USER_PASSWORD`), so that DoD line is **Unverified**, credential-blocked → STEP-48 |
| 47.8 | Documentation: host prerequisites, ADR, risks register | Flash | app `README.md` host-setup section, `architecture/09-environments.md` bump, ADR if posture changed, `registries/risks.yml` rows | 47.5, 47.6, 47.7 | Q5 (answered: ADR-0018 written) | **Done** |
| 47.9 | Final verification & STEP close | Pro | full gate run, index flip, archive to `prompts/003-…/step-0047/` | all | — | **Done** — closed 2026-08-29 by Hermes/Claude Opus 4.8 (not Pro). Gate: analyze 0, format clean, 448 tests, both guards, APK exit 0, web release exit 0, `pub outdated` clean, zero overrides; emulator boot re-confirmed (harness ran, assertions skipped — credentials); CI run `33195382106` on `e3cd9ed3` all four jobs green. Repaired a 47.8 defect: `registries/risks.yml` had a 194-line accidental duplicate paste (RISK-0012..0019 + truncated RISK-0019) that made it unparseable — de-duplicated, 20 unique ids, `yaml.safe_load` clean |

47.2, 47.3, and 47.4 all depend only on 47.1 and touch disjoint file sets — they may run in
parallel, but each must leave `flutter analyze` no worse than it found it, and 47.5 is the first
point where the whole tree must compile together.

---

## Test plan

**Run timing: per substep.** This STEP changes 14+ dependency majors across 53 bloc files, 21
router files, and the file-picker surface. Batching verification to the end would make a
regression's origin unattributable. Every substep runs its named command before it may be marked
done; 47.9 re-runs the full gate as the closing proof.

Baseline to beat, from STEP-46.4: `flutter analyze` **0 issues**, `flutter test` **442 passing**
(one known order-dependent flake, non-reproducible in isolation). A drop below 442 is a
regression, not a flake, unless proven otherwise by an isolated re-run.

| Test tier / surface | Substep(s) | Tests to create or update | Run timing | Command / gate | Notes |
|---|---|---|---|---|---|
| Static analysis | 47.1–47.4, 47.9 | — | Per substep | `flutter analyze` (must be 0 issues) | `flutter_lints` 6 adds `strict_top_level_inference` + `unnecessary_underscores`; new findings are 47.4's to fix |
| Format gate | every code substep | — | Per substep | `dart format --output=none --set-exit-if-changed lib/ test/` | mirrors CI |
| Unit / widget | 47.2, 47.3, 47.4 | `test/features/data_bucket/presentation/bloc/data_bucket_upload_cubit_test.dart`; a new widget test for the migrated picker path; all 11 `bloc_test` suites | Per substep | `flutter test` (≥442 passing) | |
| Contract guards | 47.1, 47.9 | — | Per substep | `dart run tool/check_supabase_contracts.dart`; `dart run tool/check_l10n_baseline.dart` | contract guard rejects stub types by content |
| Build smoke — Android | 47.5, 47.7 | — | Per substep | `flutter build apk --debug` locally **and** CI `build-android` | the STEP's headline deliverable |
| Build smoke — Web | 47.4, 47.9 | — | Per substep | `flutter build web --release` | `go_router` 18 migrated to material_ui/cupertino_ui; web is the other shipped surface |
| End-to-end — Android | 47.5, 47.7 | none authored here | Per substep | `flutter test integration_test/app_boots_test.dart -d emulator-5554` | **boot-only**. The 14 staging journeys stay Deferred → STEP-48 |
| End-to-end — Web | 47.6 | none authored here | Per substep | `flutter drive --driver=test_driver/integration_test.dart --target=integration_test/app_boots_test.dart -d web-server` | chromedriver must be running |

**Explicit non-goal:** STEP-47 does **not** try to make the 14 staging journeys pass. They are
`markTestSkipped`-gated when credentials are absent, so a green E2E job here means *the harness
runs and skips honestly*, not *the journeys are verified*. Claiming otherwise would repeat exactly
the failure this project corrected in STEP-45.

---

## Open questions

- **Q1 (47.0, owner: executing agent):** are `STAGING_SUPABASE_URL`, `STAGING_SUPABASE_ANON_KEY`,
  and `STAGING_GOOGLE_DRIVE_CLIENT_ID` actually present as repo secrets? CI job logs are 403
  without a token, so this must be established from the workflow run's behaviour or by asking the
  user — never by assuming.
- **Q2 (47.2) — RESOLVED at planning: collapse to a single pick.** `file_picker` 12 removed
  `FilePickerResult` and deprecated `withData`. `upload_file_page.dart` currently calls `pickFiles`
  **twice** — once with `withData: false` to check size (CF-078's memory cap), once with
  `withData: true` to read bytes — a v11 workaround for having no lazy byte access. Version 12's
  `length()` + `readAsBytes()` remove the need, so 47.2 uses one `pickFile()`, checks the cap via
  `length()`, and calls `readAsBytes()` only if it passes. CF-078's intent (never load an oversized
  file into memory) is preserved and asserted by a boundary test; the cap value, message text, and
  toast styling stay byte-identical. This is a user-visible change (one pick instead of two) and is
  recorded in the STEP close.
- **Q3 (47.4) — RESOLVED with evidence.** `go_router` 18 "migrates to material_ui and cupertino_ui" did *not* require app-code changes. Verified via `grep` and a clean `flutter test test/app` run.
- **Q4 (47.5, owner: executing agent):** once built-in Kotlin owns compilation, is STEP-43's
  `kotlin.compiler.execution.strategy=in-process` / `kotlin.incremental=false` workaround still
  needed on this Windows host? Test both ways and record the result. Default to retaining it.
- **Q5 (47.8, owner: executing agent):** does the AGP/Kotlin posture change warrant a new ADR, or
  is it a Version Log bump on `09-environments.md`? Deleting a `dependency_overrides` entry that a
  prior STEP deliberately added is a reversal of a recorded decision — lean toward an ADR.

---

## Ground rules

- **Calibrate communication from root `.throughstone/local-user.md`** (Experience level 2,
  Explanatory). Explain the reasoning behind a dependency decision; don't just list commands.
- **Plan interactively.** Where a substep hits a real fork (Q2, Q4, Q5), present options with
  brief pros/cons rather than picking silently.
- **Evidence over claims.** Paste the actual command output into the substep's status note. The
  wording "the build should now work" is not acceptable; either it exited 0 or it did not. If
  something cannot be run, mark it **Unverified** with the reason — never as a pass. This STEP
  exists partly because a prior close reported 15/15 Done for work that never ran.
- **One dependency change at a time within a substep.** When a migration breaks something, the
  bisect must stay cheap. Commit per substep on the STEP branch — do not accumulate a three-repo
  uncommitted close (the exact failure mode STEP-45 left behind, and STEP-49's lesson #4).
- **Do not re-try the eliminated hypotheses.** `android.builtInKotlin=false` (breaks
  `compileDebugJavaWithJavac`), cross-drive `PUB_CACHE` (fixed), Flutter 3.47.0-vs-.1 skew (ruled
  out), JDK version (Temurin 17 already wired). The reservation outline's "flutter extension not
  populated in plugin subprojects" theory is disproven — ignore it.
- **Do not downgrade AGP.** The user rejected the AGP 8.11.x path; Flutter 3.47 warns below AGP
  9.0.1 (`DependencyVersionChecker.kt:103`) and AGP 10 forces this migration regardless.
- **Tests ship with the code.** Every code-changing substep runs its named tests before it is done.
- **Code is documented as it's written** — docstrings on new/changed members; comment the *why*.
- **Secrets stay untouched.** Do not read, print, or echo `.env` values or repo secrets. Refer to
  them by name. Do not mutate remote Supabase state.
- **Accepted risks stay visible.** New or changed risk → a row in `registries/risks.yml` with
  severity, owner, and revisit trigger, pointing at an ADR/report rather than duplicating detail.
- **`git status` must be clean of unrelated work before branching.** If another owner's
  uncommitted work is present, stop and report it — never stash, reset, or absorb it.

---

## Definition of done

> **Closed 2026-08-29 by 47.9.** Each box below is ticked only where a real command or CI run
> proved it; the one line that could not be satisfied is left unticked with its reason, per this
> PLAN's own "Evidence over claims" ground rule.

- [x] `flutter build apk --debug` exits 0 **on this Windows host** — 95.5s clean at close, APK
      194 MB at `build/app/outputs/flutter-apk/app-debug.apk`; evidence in
      `mine-flow-STEP-47.0-EVIDENCE.md` §2/§9.
- [x] `pubspec.yaml` contains **no `dependency_overrides`**, and `flutter pub outdated` reports
      `all dependencies are up-to-date` for direct and dev dependencies (SDK-pinned transitives
      recorded as RISK-0020).
- [x] No plugin in the resolved graph applies KGP unconditionally; audit table recorded in 47.1
      (`android_file_picker` 1.0.3, `battery_plus` 7.1.1, `package_info_plus` 10.2.1 — all
      AGP-major-guarded).
- [x] `flutter analyze` 0 issues; `dart format` gate clean (302 files, 0 changed); `flutter test`
      **448 passing** (≥442), one non-reproducible order-dependent flake proven flaky by
      isolation ×2 + a clean full re-run and a file identical to `master`.
- [x] `flutter build web --release` succeeds — exit 0 at close.
- [x] `integration_test/app_boots_test.dart` reaches the app on the `Pixel_6a` emulator locally:
      APK built, installed, harness ran. **Its assertions did not execute** — `All tests skipped`,
      `Unverified: Staging credentials absent`.
- [x] CI `build-android`, `e2e-android`, and `e2e-web` all **green** on the STEP branch — run
      `33195382106` (final commit `e3cd9ed3`), plus `test`; all four success.
      (E2E green = harness executes; the 14 staging journeys remain Deferred.)
- [x] Host prerequisites (PUB_CACHE drive rule, JDK 17) documented in the app `README.md` and
      `architecture/09-environments.md` v0.4.0 with a matching Version Log row.
- [x] ADR-0018 records the AGP-9/built-in-Kotlin posture and the removal of STEP-43's
      `flutter_secure_storage_windows` override (Q5 answered: ADR, not just a Version Log bump).
- [x] `registries/risks.yml` updated: RISK-0008 amended for the `flutter_secure_storage_windows`
      4.0.0 → 4.2.2 bump (Windows-desktop surface only), RISK-0006 re-worded for go_router 18,
      RISK-0020 added. *(47.9 also repaired an accidental duplicate paste in this file that made
      it unparseable — see the 47.9 substep row.)*
- [x] The STEP test plan is complete: each code-changing substep ran its tests; 47.3's outcome is
      an explicit "no change required", verified rather than skipped.
- [ ] **Not satisfiable in STEP-47 — credential-blocked, carried to STEP-48:** `app_boots_test.dart`
      confirmed *executed* (not skipped) on a device or in CI. Its guard is `isStagingConfigured`,
      which needs `TEST_USER_EMAIL` + `TEST_USER_PASSWORD`; neither exists in `ci.yml` or locally.
      Both local and CI runs report `0 passed, 1 skipped`. Recorded as Unverified, not ticked.
- [x] STEP review passed; `prompts/STEP-index.md` STEP-47 row flipped to Done with a substep
      table; PLAN + all substep prompts archived to
      `prompts/003-release-readiness-integration-scale/step-0047/`.
- [x] No `.env`/secret value was read or printed; no remote Supabase state mutated. The one remote
      effect of the close is `deploy-staging` firing on the merge to `master`, flagged to the user
      for consent beforehand.

---

## Version Log

| Version | Date | Change |
|---|---|---|
| v0.1 | 2026-08-28 | Initial plan. Root cause established by two real local builds; dependency resolution verified in scratch projects; scope confirmed with user (full sweep + all three CI jobs green). |
| v0.2 | 2026-08-29 | Closed by 47.9. Status → Done. Definition of done reconciled against real evidence: 13 of 14 lines ticked; the "`app_boots_test.dart` executed (not skipped)" line left **unticked** as credential-blocked → STEP-48. Substep statuses assigned from each substep's own evidence rather than its optimism. |
