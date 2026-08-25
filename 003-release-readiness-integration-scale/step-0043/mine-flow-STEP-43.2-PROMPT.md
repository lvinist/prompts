# mine-flow — STEP-43.2: Android Build Chain Upgrade

> **How to run:** Tell your agent: **"Read and run `Upcoming Prompts/mine-flow-STEP-43.2-PROMPT.md`."**
> This substep is self-contained — executable cold in a fresh chat.
> **Assigned model:** Gemini 3.1 Pro High

## Context

STEP-43.1 fixed the impossible `flutter_bloc` constraint. `flutter pub get` now passes. This substep upgrades the Android build chain (AGP, KGP, minSdk) to match Flutter 3.47's requirements.

See: `Code/mine-flow-docs/reports/2026-08-13-flutter-dependency-ci-audit.md` — Section 2, Findings AND-1 and AND-2.

**Known state:**
- `flutter pub get` passes.
- `android/settings.gradle.kts`: AGP `9.0.1`, KGP `2.3.20`.
- `android/app/build.gradle.kts`: `compileSdk = flutter.compileSdkVersion`, no explicit `minSdk`.
- `android/gradle.properties`: does NOT have `flutter.compileSdkVersion=36` (that was on the brute-force branch only).

## Read these first

- `Upcoming Prompts/mine-flow-STEP-43-PLAN.md`
- `.throughstone/local-user.md`
- `Code/mine-flow-app/android/settings.gradle.kts`
- `Code/mine-flow-app/android/app/build.gradle.kts`
- `Code/mine-flow-app/android/gradle.properties`
- `Code/mine-flow-docs/reports/2026-08-13-flutter-dependency-ci-audit.md` (Section 2)

## Scope

**Own:** Upgrade AGP, KGP, set explicit minSdk in Android build files.

**Do not:** Change CI workflow. Change pubspec.yaml. Change any Dart code.

## Your task

### 1. Upgrade AGP and KGP

In `android/settings.gradle.kts`:
- Change `id("com.android.application") version "9.0.1"` → `version "9.1.0"`
- Change `id("org.jetbrains.kotlin.android") version "2.3.20"` → `version "2.4.0"`

### 2. Set explicit minSdk

In `android/app/build.gradle.kts`, inside the `defaultConfig` block:
- Add (or update): `minSdk = 23`
- Add a comment: `// flutter_secure_storage v11 requires minSdk >= 23 (STEP-43, RISK-0008)`

### 3. Verify compileSdk

Check what `compileSdk` is set to on this branch. On master, it should be `compileSdk = flutter.compileSdkVersion` (dynamic, set by Flutter). Do NOT add a hardcoded `compileSdk = 36` or `flutter.compileSdkVersion=36` in gradle.properties — let Flutter's tooling manage it. If it's already hardcoded to 36 (from the brute-force branch), revert to `flutter.compileSdkVersion`.

### 4. Verify

```powershell
flutter pub get
```

Should still exit 0. The Gradle changes don't affect `pub get` but we confirm no regression.

### 5. Commit

```powershell
git add android/
git commit -m "build(STEP-43.2): upgrade AGP 9.1.0, KGP 2.4.0, explicit minSdk 23"
```

## Verification

- `android/settings.gradle.kts` shows AGP `9.1.0`, KGP `2.4.0`.
- `android/app/build.gradle.kts` shows `minSdk = 23`.
- `compileSdk` uses `flutter.compileSdkVersion` (dynamic), not hardcoded 36.
- `gradle.properties` does NOT have `flutter.compileSdkVersion=36`.
- `flutter pub get` exits 0.

## Definition of done

- [ ] AGP bumped to 9.1.0.
- [ ] KGP bumped to 2.4.0.
- [ ] `minSdk = 23` explicit in build.gradle.kts.
- [ ] `compileSdk` is dynamic (flutter.compileSdkVersion), not hardcoded.
- [ ] Committed on `step-0043-flutter-upgrade`.

## Next

After committing, continue in the same chat to **substep 43.3**: `Upcoming Prompts/mine-flow-STEP-43.3-PROMPT.md`.
