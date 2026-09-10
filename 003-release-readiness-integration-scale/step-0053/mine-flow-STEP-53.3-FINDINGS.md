# mine-flow — STEP-53.3 Findings: Safe Dependency and Lockfile Maintenance

**Date:** 2026-09-10
**Executor:** Antigravity (Gemini 2.5 Pro)
**Substep:** 53.3
**Status:** Complete

---

## 1. Executive Summary

This substep executed targeted compatible dependency upgrades for all direct packages
that had available minor/patch updates within their declared `^` constraint ranges.
Five direct packages and seven of their transitive packages were upgraded. One test
adaptation was required: `file_picker_platform_interface` 3.3.0 introduced a new
abstract method `lengthSync()` on `PlatformFile`, which `FakePlatformFile` in the
upload page test had to implement.

All 550/550 unit/widget tests pass. `pubspec.yaml` is unchanged. Zero
`dependency_overrides`. Lockfile is synchronized. Remaining outdated items are all
confirmed SDK-pinned (not upgradeable without a Flutter SDK channel change). RISK-0020
updated to `monitoring`.

---

## 2. Pre-Upgrade State

### 2.1 Branch and HEAD

- **Branch:** `step-0053-dependency-maintenance`
- **HEAD:** `be44843` (ci(STEP-52): wire TEST_CREW_* into E2E CI jobs)
- **Working tree:** clean (nothing to commit)

### 2.2 `flutter pub outdated` (pre-upgrade — direct and upgradable transitive items)

| Package | Current | Upgradable | Latest | Notes |
|---------|---------|------------|--------|-------|
| `file_picker` (direct) | 12.1.2 | **12.2.0** | 12.2.0 | Targeted |
| `flutter_secure_storage` (direct) | 11.0.0 | **11.1.0** | 11.1.0 | Targeted |
| `go_router` (direct) | 18.0.0 | **18.0.1** | 18.0.1 | Targeted |
| `lucide_icons_flutter` (direct) | 3.1.17 | **3.1.19** | 3.1.19 | Targeted |
| `build_runner` (dev, direct) | 2.16.0 | **2.16.1** | 2.16.1 | Targeted |
| `archive` (transitive) | 4.0.9 | *4.0.9* | 4.2.0 | SDK-pinned — deferred |
| `package_config` (transitive) | 2.2.0 | *2.2.0* | 3.0.0 | SDK-pinned — deferred |
| `qr` (transitive) | 3.0.2 | *3.0.2* | 4.0.0 | SDK-pinned — deferred |
| `material_color_utilities` (transitive) | 0.13.0 | *0.13.0* | 0.13.1 | SDK-pinned — deferred |
| `_fe_analyzer_shared`, `analyzer`, `test`, `test_api`, `test_core` (dev transitive) | various | *same* | newer | SDK dev-pinned — deferred |

---

## 3. Upgrade Applied

### 3.1 Command

```
flutter pub upgrade file_picker flutter_secure_storage go_router lucide_icons_flutter build_runner
```

Targeted upgrade against named packages only — does not rewrite the full resolution graph.

### 3.2 Packages Changed (12 total)

#### Direct upgrades (5)

| Package | Before | After | Type |
|---------|--------|-------|------|
| `file_picker` | 12.1.2 | **12.2.0** | direct main |
| `flutter_secure_storage` | 11.0.0 | **11.1.0** | direct main |
| `go_router` | 18.0.0 | **18.0.1** | direct main |
| `lucide_icons_flutter` | 3.1.17 | **3.1.19** | direct main |
| `build_runner` | 2.16.0 | **2.16.1** | direct dev |

#### Transitive co-upgrades (7)

| Package | Before | After | Reason |
|---------|--------|-------|--------|
| `android_file_picker` | 1.0.3 | **1.1.1** | Pulled by `file_picker` 12.2.0 |
| `file_picker_darwin` | 1.0.4 | **1.1.0** | Pulled by `file_picker` 12.2.0 |
| `file_picker_linux` | 1.0.2 | **1.1.0** | Pulled by `file_picker` 12.2.0 |
| `file_picker_platform_interface` | 3.2.0 | **3.3.0** | Pulled by `file_picker` 12.2.0 |
| `file_picker_web` | 3.0.3 | **3.1.0** | Pulled by `file_picker` 12.2.0 |
| `windows_file_picker` | 1.1.0 | **1.2.0** | Pulled by `file_picker` 12.2.0 |
| `flutter_secure_storage_platform_interface` | 2.0.3 | **2.1.0** | Pulled by `flutter_secure_storage` 11.1.0 |

### 3.3 pubspec.yaml Changes

**None.** All upgraded packages were within their declared `^` constraint ranges.
`pubspec.yaml` was not modified.

### 3.4 Lockfile

Only `pubspec.lock` was updated. Zero `dependency_overrides` before and after. All
package sources remain `hosted` from `pub.dev`. No unexpected new packages appeared.

---

## 4. API Change: `file_picker_platform_interface` 3.3.0

`file_picker_platform_interface` 3.3.0 added `int? lengthSync()` as a new abstract
method to the `PlatformFile` base class. The `FakePlatformFile` in
`test/features/data_bucket/presentation/pages/upload_file_page_test.dart` (line 36)
extends `PlatformFile` and had to implement this method.

### 4.1 Compilation error before fix

```
Error: The non-abstract class 'FakePlatformFile' is missing implementations for these members:
  - PlatformFile.lengthSync
```

### 4.2 Fix applied

```dart
// file_picker_platform_interface 3.3.0 added this abstract method.
// The fake always has the size at construction, so return it directly.
@override
int? lengthSync() => _size;
```

**Location:** `test/features/data_bucket/presentation/pages/upload_file_page_test.dart` —
added after the existing `Future<int> length() async => _size;` override.

This is the correct implementation: the fake's `_size` is always known at construction
(it represents the nominal file size), matching the `lengthSync` contract.

**Application code modified:** None. No `PlatformFile` subclass exists in production code.

---

## 5. Vetting Notes (per dependency runbook Parts 2–3)

All upgrades are within the same semantic-version major. No ADR-0006 / offline storage
boundary changes. No new packages introduced. All sources confirmed `pub.dev` hosted.

| Package | Version change | Nature | Safety assessment |
|---------|---------------|--------|-------------------|
| `file_picker` | 12.1.2→12.2.0 | Minor | New `lengthSync()` abstract on `PlatformFile` — backward compatible for production code (no PlatformFile subclasses in app code). Test fake required update. |
| `flutter_secure_storage` | 11.0.0→11.1.0 | Minor | Patch/minor release; RISK-0008 (v9→v11 skip) posture unchanged. |
| `go_router` | 18.0.0→18.0.1 | Patch | Bug-fix release; route API unchanged per RISK-0006 evidence. |
| `lucide_icons_flutter` | 3.1.17→3.1.19 | Patch | Icon additions; no breaking changes to icon-reference API. |
| `build_runner` | 2.16.0→2.16.1 | Patch | Dev tool only; no application surface impact. |

No automated vulnerability advisory scanning performed (no `dart pub audit` or
equivalent available locally). Package provenance confirmed via pub.dev hosted source.
No license changes expected within minor/patch upgrades from established packages.
No advisories known for any upgraded package at time of this substep.

---

## 6. Deferred Updates

The following packages were reviewed and deferred. They are genuinely not upgradeable
within the current Flutter SDK version (3.47.1 / Dart 3.13.1) constraint.

| Package | Current | Available | Deferral reason |
|---------|---------|-----------|-----------------|
| `archive` | 4.0.9 | 4.2.0 | SDK-pinned: Flutter SDK 3.47.x constrains `archive` below 4.2.0 |
| `package_config` | 2.2.0 | 3.0.0 | SDK-pinned: Flutter SDK constrains below 3.0.0 |
| `qr` | 3.0.2 | 4.0.0 | SDK-pinned: Flutter SDK constrains below 4.0.0 |
| `material_color_utilities` | 0.13.0 | 0.13.1 | SDK-pinned: Flutter SDK constrains below 0.13.1 |
| `_fe_analyzer_shared` | 103.0.0 | 107.0.0 | SDK dev-pinned |
| `analyzer` | 13.3.0 | 14.3.0 | SDK dev-pinned |
| `test` / `test_api` / `test_core` | various | newer | SDK dev-pinned |

These residuals will resolve naturally with a future Flutter SDK upgrade. They are
tracked under RISK-0020 (now `monitoring`).

---

## 7. Verification Record

| Check | Command | Result |
|-------|---------|--------|
| Upgrade command | `flutter pub upgrade file_picker flutter_secure_storage go_router lucide_icons_flutter build_runner` | Exit 0 — 12 dependencies changed |
| Post-upgrade pub outdated | `flutter pub outdated` | Direct deps: all up-to-date ✅; transitive residuals SDK-pinned (see §6) |
| Dependency tree | `flutter pub deps --style=compact` | All sources pub.dev hosted; zero overrides ✅ |
| `pubspec.yaml` diff | `git diff -- pubspec.yaml` | **Empty** — no manifest changes ✅ |
| `pubspec.lock` diff | `git diff -- pubspec.lock` | 12 package versions updated, all within declared ranges ✅ |
| Dart format | `dart format --output=none --set-exit-if-changed .` | 330 files, 0 changed — **clean** ✅ |
| Focused file_picker test | `flutter test test/features/data_bucket/...upload_file_page_test.dart` | **6/6 passed** ✅ |
| Full test suite | `flutter test` | **550/550 passed, 0 failed, 0 skipped** ✅ |
| `flutter analyze` | Not run | No source files changed (only lock + one test file) |
| Contract guard | Not run | Deferred to 53.4 final gate |
| L10n guard | Not run | Deferred to 53.4 final gate |
| Build / E2E | Not run | Credential/device/tool availability — deferred to 53.4 (Unverified) |
| Secrets | — | No `.env` values read, printed, or committed ✅ |
| Unrelated files | `git diff` | Only `pubspec.lock` and test file staged ✅ |

---

## 8. RISK-0020 Recommendation

**Status change: `open` → `monitoring`.**

STEP-53.3 resolved all direct dependency drift:

- **Resolved (this substep):** `file_picker`, `flutter_secure_storage`, `go_router`,
  `lucide_icons_flutter`, `build_runner`, and 7 co-upgraded transitives.
- **SDK-pinned residuals (deferred, confirmed):** `archive`, `package_config`, `qr`,
  `material_color_utilities`, `_fe_analyzer_shared`, `analyzer`, `test` family.

The residuals require a Flutter SDK version upgrade to resolve — they are not
independently upgradeable without a SDK channel change, which is outside scope for
this STEP.

**Revisit trigger:** unchanged — when upgrading Flutter SDK in the future.

---

## 9. Decisions

| Decision | Outcome |
|----------|---------|
| `dependency_overrides` | Zero before and after ✅ |
| Major version crossings | None — all upgrades stayed within declared `^` major ✅ |
| `forui` version | Unchanged at `0.26.0` (pin required per RISK-0009; 53.2 findings) ✅ |
| `hive_ce` version | Unchanged at `2.19.3` (per ADR-0006 / RISK-0007; 53.1 findings) ✅ |
| Flutter SDK / channel change | Not performed (out of scope) ✅ |
| Hive-to-another-engine migration | Not performed (out of scope, requires separate STEP) ✅ |

---

## 10. Source Changes Summary

| File | Change |
|------|--------|
| `pubspec.lock` | 12 package versions updated (lockfile sync; manifest unchanged) |
| `test/features/data_bucket/presentation/pages/upload_file_page_test.dart` | Added `int? lengthSync() => _size;` to `FakePlatformFile` for `file_picker_platform_interface` 3.3.0 API |
| `Code/mine-flow-docs/registries/risks.yml` | RISK-0007 → `monitoring`; RISK-0009 → `monitoring` with updated triggers and refs; RISK-0020 → `monitoring` with description of resolved drift vs SDK residuals |
| `Upcoming Prompts/mine-flow-STEP-53-PLAN.md` | 53.2 and 53.3 status rows updated to Done; 53.3 DoD item checked |
| `prompts/STEP-index.md` | Substep 53.2 and 53.3 rows updated to Done with evidence |

Application code (`lib/`): **None modified.**
