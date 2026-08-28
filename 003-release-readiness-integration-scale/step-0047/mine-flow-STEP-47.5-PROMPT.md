# mine-flow — STEP-47.5: Local Android build green + emulator boot

> **How to run:** Tell your agent *"run substep 47.5"*. Self-contained; runnable cold.
>
> **Model:** Gemini 3.1 Pro High. This is the STEP's headline deliverable and the first point where
> the whole tree must build together.

## Context

STEP-47's PLAN is `Upcoming Prompts/mine-flow-STEP-47-PLAN.md`. Substeps 47.1–47.4 replaced the
AGP-9-incompatible plugins and migrated the Dart code that broke. This substep proves the actual
goal: **`flutter build apk --debug` exits 0 on this Windows host, and the app reaches the emulator.**

Everything until now was preparation. The whole reason STEP-48's runtime evidence is blocked is that
no APK exists to run.

**Prerequisite:** 47.2, 47.3, and 47.4 must all be done and committed. If any is outstanding, stop —
a build failure here would be unattributable.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-47-PLAN.md` — "Root cause" and **Q4**
- `Upcoming Prompts/mine-flow-STEP-47.0-EVIDENCE.md` — the original failure, host toolchain, baselines
- 47.1's KGP audit table — which plugins still apply KGP and how they guard it
- `Code/mine-flow-app/android/gradle.properties` — the flags in question
- `Code/mine-flow-app/android/settings.gradle.kts` — AGP 9.1.0, KGP 2.4.0, Gradle wrapper 9.3.1
- `Code/mine-flow-app/android/app/build.gradle.kts` — **already** built-in-Kotlin-migrated
  (no `kotlin-android` plugin, uses `kotlin { compilerOptions { jvmTarget } }`), `compileSdk = 37`
- `Code/mine-flow-app/integration_test/app_boots_test.dart` and `integration_test/helpers/app_harness.dart`
- `Code/mine-flow-docs/architecture/12-test-strategy.md` — E2E tier and CI gates
- **ADR-0017** — the expanded E2E tier
- `Code/mine-flow-app/README.md`

## Scope

**Owns:** `android/gradle.properties` (flag posture only), the local build + emulator verification,
and the evidence record.

**Does NOT touch:** `pubspec.yaml`, any `.dart` source (47.2–47.4 own those), `ci.yml` (47.6/47.7),
docs (47.8). **Do not author or modify any journey test** — the 14 staging journeys stay Deferred to
STEP-48. This substep runs `app_boots_test.dart` only.

## Your task

### 1. Confirm the tree is whole

```bash
cd /d/AppDev/mine_flow/Code/mine-flow-app
git log --oneline -5
git status --short
flutter analyze
dart format --output=none --set-exit-if-changed lib/ test/
flutter test 2>&1 | tail -20
```

Gate: analyze **0 issues**, format clean, `flutter test` **≥442 passing**. If any of those is red,
the owning substep (47.2/47.3/47.4) is not actually done — go back rather than building on sand.

### 2. Build the debug APK

```bash
flutter clean
flutter pub get
flutter build apk --debug 2>&1 | tee "$LOCALAPPDATA/Temp/step47-5-apk.log"
```

`flutter clean` matters: 47.0 observed stale `build/file_picker/intermediates/` jars from the
`builtInKotlin=false` experiment. A cached, half-compiled plugin jar can make this build lie in
either direction.

Expected: **exit 0**, plus an APK at `build/app/outputs/flutter-apk/app-debug.apk`. Verify it exists
and note its size — "the command printed no error" is not the same as "an APK was produced".

Gradle may still print `WARNING: Your app uses the following plugins that apply Kotlin Gradle Plugin
(KGP): …`. That warning is **acceptable** if it names only plugins 47.1's audit showed guard the apply
behind an AGP-major check (they apply KGP on AGP 8 and skip it on AGP 9). If it names a plugin that
applies KGP unconditionally, the audit was wrong — stop and report.

**If the build fails:** capture the full error and diagnose before changing anything. Do not reach for
`android.builtInKotlin=false` — 47.0 documented that it gets past configuration and then fails at
`:app:compileDebugJavaWithJavac` with `cannot find symbol: class FilePickerPlugin`. Two failed
attempts at the same fix means stop, diagnose the root cause, and report; per the PLAN, escalation to
Opus 4.8 is allowed at that point.

### 3. Answer Q4 — is STEP-43's Kotlin-daemon workaround still needed?

`android/gradle.properties` carries two Windows-specific lines from STEP-43:

```properties
kotlin.compiler.execution.strategy=in-process
kotlin.incremental=false
```

They existed because the *external* Kotlin daemon crashed on this host ("Daemon compilation failed" /
corrupted incremental caches). AGP 9's built-in Kotlin compiles differently, so the workaround may be
obsolete — or may still be load-bearing.

Test it deliberately:

1. Baseline: build succeeds with the flags present (that is §2).
2. Comment both lines out, `flutter clean`, rebuild.
3. If it succeeds, rebuild **once more without cleaning** — the original failure involved corrupted
   *incremental* caches, so it often shows on the second build, not the first.

**Decision rule:** remove the lines only if two consecutive builds (clean, then incremental) both
succeed without them. Otherwise restore them with a comment recording that removal was tested on
2026-08-28 and still fails. Default to **retaining** — an unnecessary flag costs rebuild speed; a
missing one costs a broken build on the only machine that builds locally.

Also re-examine `android.newDsl=false` and `android.builtInKotlin=true`. `builtInKotlin=true` is
required (it is what makes AGP 9 compile Kotlin without KGP). `newDsl=false` is Flutter's own
compatibility shim (Flutter issue #184838) and Flutter's tooling re-adds it automatically — leave it,
and record why in a comment rather than experimenting with it.

### 4. Boot the app on the emulator

```bash
flutter emulators                       # expect: Pixel_6a
flutter emulators --launch Pixel_6a
# wait for boot, then:
flutter devices                         # expect an emulator-XXXX entry
flutter test integration_test/app_boots_test.dart -d emulator-5554 2>&1 | tee "$LOCALAPPDATA/Temp/step47-5-boot.log"
```

Use the device id `flutter devices` actually reports; `emulator-5554` is the usual default, not a
guarantee.

Success = the harness installs the app, `pumpApp` runs, and `app_boots_test.dart` passes. Note that
`app_harness.dart` only calls `Supabase.initialize` when `isStagingConfigured` is true, so the boot
test works without credentials — the app comes up unauthenticated. That is the correct outcome here.

**RISK-0009 applies** to anything you touch in a test: find `EditableText`, never `TextField`
(flutter/flutter#191095 on Flutter 3.47).

**Do not run the 14 journey tests.** They are `markTestSkipped`-gated without staging credentials and
belong to STEP-48. Running them here produces a pile of skips that could be mistaken for passes —
exactly the confusion STEP-45's record had to be corrected for.

If the emulator cannot be launched or the install fails, capture the error and mark the boot check
**Unverified** with the reason. A green APK build with an Unverified boot is still real progress —
misreporting it as verified is not.

### 5. Record the evidence

Append a "47.5 — local build" section to `Upcoming Prompts/mine-flow-STEP-47.0-EVIDENCE.md` (keeping
all STEP-47 evidence in one place) containing:

- the `flutter build apk --debug` tail showing success, plus the APK path and size
- the exact KGP warning text, if any, and why it is acceptable
- Q4's answer with the results of all three build attempts from §3
- the `app_boots_test.dart` result on `Pixel_6a`, or the Unverified reason
- build wall-clock time (useful context for CI timeouts in 47.7)

### 6. Commit

```bash
git -C /d/AppDev/mine_flow/Code/mine-flow-app status --short
# stage android/gradle.properties only if §3 changed it
git -C /d/AppDev/mine_flow/Code/mine-flow-app commit -m "build(STEP-47.5): local debug APK green under AGP 9 built-in Kotlin"
```

If §3 changed nothing, there may be no app-repo commit — that is fine. Say so; do not manufacture a
commit to look productive.

## Verification

- `flutter build apk --debug` exits 0 and `build/app/outputs/flutter-apk/app-debug.apk` exists.
- Any KGP warning names only plugins that guard their apply behind an AGP-major check.
- `integration_test/app_boots_test.dart` passes on `Pixel_6a`, or is explicitly **Unverified** with a
  reason.
- `flutter analyze` 0 issues, `dart format` clean, `flutter test` ≥442 still hold after the build.
- Q4 answered with three recorded build attempts, not a guess.
- No `.dart` source, `pubspec.yaml`, `ci.yml`, or doc file modified.

This substep is the STEP's whole point, so its evidence bar is the highest: paste real command output.
"The build now works" without an exit code and an APK path is not acceptable.

## Keeping the docs true (always)

Do not write documentation here — 47.8 owns it, and duplicating causes drift. Hand 47.8:

1. Q4's answer, so the `gradle.properties` posture can be documented accurately.
2. The confirmed host prerequisites (`PUB_CACHE` on the SDK's drive, JDK 17 via
   `flutter config --jdk-dir`) with the evidence that they matter → app `README.md` +
   `architecture/09-environments.md`.
3. Whether the AGP-9/built-in-Kotlin posture plus the removal of STEP-43's `dependency_overrides`
   warrants an ADR (Q5). Your build evidence is the deciding input.

No secrets: the debug build needs no `--dart-define` credentials, and the boot test runs
unauthenticated. Do not add real credential values to any command you record.

## Definition of done

- [ ] `flutter clean` + `flutter pub get` + `flutter build apk --debug` exits 0
- [ ] APK exists at `build/app/outputs/flutter-apk/app-debug.apk`; path and size recorded
- [ ] KGP warnings (if any) reconciled against 47.1's audit table
- [ ] Q4 answered by testing all three build variants; `gradle.properties` posture decided and
      commented in-file
- [ ] `app_boots_test.dart` passes on `Pixel_6a`, or is Unverified with a stated reason
- [ ] Analyze / format / test gates still green after the build
- [ ] Evidence appended to `mine-flow-STEP-47.0-EVIDENCE.md`, including build wall-clock time
- [ ] No journey test run, authored, or modified
- [ ] No `.dart`, `pubspec.*`, `ci.yml`, or docs file modified
- [ ] Committed on `step-0047-android-build-chain` (or explicitly noted as no-change)
- [ ] Notes for 47.8 written

## Next

Update 47.5's status in the PLAN, then tell the user the next action: **run substep 47.6** (CI
`e2e-web`: replace `-d chrome` with `flutter drive` + chromedriver) in a fresh chat. 47.7 also
unblocks now and can run in parallel.
