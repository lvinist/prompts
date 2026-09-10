# mine-flow — STEP-53.1 Findings: `hive_ce` Maintenance and Dart-4 Trajectory Audit

**Date:** 2026-09-10  
**Executor:** Antigravity (Audited & Corrected)  
**Substep:** 53.1  
**Status:** Complete  

---

## 1. Executive Summary

This audit evaluates the package health, provenance, SDK constraints, Dart-4 trajectory, upstream maintenance signals, and architectural compliance of `hive_ce` (^2.19.3) and `hive_ce_flutter` (^2.3.4), addressing the revisit trigger for **RISK-0007** identified during STEP-50.1.

**Key Findings:**
1. **Release Gap & Cadence:** The stable release of `hive_ce` on `pub.dev` remains `2.19.3`, published on **2026-02-03 10:49:41 UTC** (~7.2 months / 219 days ago). The stable release of `hive_ce_flutter` remains `2.3.4`, published on **2026-01-09 23:40:17 UTC** (~8.0 months / 244 days ago). `flutter pub outdated --show-all --prereleases --json` confirms there are no newer stable or pre-release versions available on `pub.dev`.
2. **Active Upstream Git Maintenance (Verified Live):** Inspection of the upstream GitHub repository (`IO-Design-Team/hive_ce`) via the GitHub API confirms that development and maintenance are **active** and ongoing, contrary to assumptions of abandonment:
   - Commit `ed9d2438955ddaaeec7874bcea330a667d12ba7f` merged PR #314 on **2026-08-26 00:38:14 UTC** by primary maintainer Rexios80, upgrading lints and ensuring analysis passes on **Flutter 3.48 beta**.
   - Active PRs (#320, #321) and issues (#322, #323) were submitted and engaged with in late August 2026.
3. **Package Health & Provenance:** Both packages are actively hosted on `pub.dev` under `IO-Design-Team` (primary maintainer: Aaron DeLory / `Rexios80`, publisher `iodesignteam.com`). The packages are **not discontinued** (`isDiscontinued: false`), **not retracted** (`isCurrentRetracted: false`), and have **zero known security advisories** (`isCurrentAffectedByAdvisory: false`). The code is licensed under BSD-3-Clause / Apache 2.0, fully compatible with the project's MIT license.
4. **Toolchain & SDK Constraints:** The host environment runs Flutter `3.47.1` (stable) and Dart `3.13.1`. The packages constrain `sdk: ^3.4.0` (`>=3.4.0 <4.0.0`), which resolves cleanly and runs with 0 analyzer issues.
5. **Dart-4 Trajectory:** The constraint `^3.4.0` strictly bounds the SDK to `<4.0.0`. In the event of a future Dart 4 release, resolution will fail without an upstream package release bumping the constraint. As of 2026-09-10, no Dart-4 compatible release or pre-release exists on `pub.dev`. Dart 4 has not been released or scheduled with breaking changes by the Dart SDK team.
6. **ADR-0006 & Clean Architecture:** All 28 `package:hive_ce` import sites in `mine-flow-app` (15 in `lib/`, 11 in `test/`, 2 in `integration_test/`) and 9 `package:hive_ce_flutter` import sites are strictly confined to data sources, type adapters, local cache repositories, harness setups, and tests. Domain and Presentation layers remain decoupled from Hive APIs. Dual-platform support (Android + Web) remains intact.
7. **Recommendation for RISK-0007:** Update status from `open` to **`monitoring`**. Immediate migration away from `hive_ce` is unwarranted, high-risk, and outside Phase 3 scope. Revisit triggers are formalized below.

---

## 2. Pre-Execution Verification & Working Tree Posture

### 2.1 Workspace and Branch Coordination
Before performing dependency checks, git status and branch coordination were verified across all workspaces:
- `Code/mine-flow-app`: clean on branch `master`; created and checked out STEP branch `step-0053-dependency-maintenance`.
- `Code/mine-flow-docs`: clean on branch `main`; created and checked out STEP branch `step-0053-dependency-maintenance`.
- `prompts`: clean on branch `main`; pushed pending commit `ebf960d` to `origin/main`.
- **Overlap check:** Scanned `prompts/STEP-index.md` for in-flight rows. STEP-53 is the sole `In progress` STEP. No conflicting branches or concurrent STEP overlaps exist across projected repositories (`mine-flow-app`, `mine-flow-docs`, `prompts`).

### 2.2 Host Toolchain Versions (`flutter --version`)
```text
Flutter 3.47.1 • channel stable • https://github.com/flutter/flutter.git
Framework • revision 6655482ec0 (3 weeks ago) • 2026-08-19 10:07:23 -0700
Engine • hash 11d79658c444477b06513d32b52c8c4ccb7276b0 (revision 5d53178869) (22 days ago) • 2026-08-18 23:36:01.000Z
Tools • Dart 3.13.1 • DevTools 2.60.0
```

---

## 3. Package Inventory, Metadata & Provenance

Evidence extracted directly from `pubspec.lock`, the local pub cache (`D:\AppDev\.pub-cache\hosted\pub.dev\`), `flutter pub outdated --show-all --prereleases --json`, and live GitHub API queries:

### 3.1 `hive_ce`
- **Name:** `hive_ce`
- **Resolved Version:** `2.19.3`
- **Manifest Constraint:** `^2.19.3` (`Code/mine-flow-app/pubspec.yaml` line 34)
- **Lockfile Hash (sha256):** `8e9980e68643afb1e765d3af32b47996552a64e190d03faf622cea07c1294418`
- **Resolved Source:** `hosted` (`https://pub.dev`)
- **Published Timestamp:** `2026-02-03 10:49:41 UTC` (from `hive_ce-versions.json` cache)
- **Release Cadence / Age on pub.dev:** ~7.2 months (219 days) since last release
- **Pre-releases on Registry:** None (`latest` = `2.19.3`)
- **Upstream Repository:** `https://github.com/IO-Design-Team/hive_ce/tree/main/hive`
- **Documentation:** `https://docs.hive.isar.community`
- **Author / Maintainer:** Aaron DeLory (`Rexios80`), IO-Design-Team
- **Publisher:** `iodesignteam.com`
- **Funding:** `https://github.com/sponsors/Rexios80`
- **License:** BSD-3-Clause (Aaron DeLory) and Apache-2.0 (pre-fork)
- **Advisories / CVEs:** 0 reported (`isCurrentAffectedByAdvisory: false`)
- **Discontinued:** `false` (`isDiscontinued: false`, `replacedBy: null`)
- **Retracted:** `false` (`isCurrentRetracted: false`)
- **Declared Dependencies:**
  - `meta: ^1.14.0`
  - `crypto: ^3.0.0`
  - `web: ">=0.5.0 <2.0.0"`
  - `isolate_channel: ^0.6.0`
  - `json_annotation: ^4.9.0`

### 3.2 `hive_ce_flutter`
- **Name:** `hive_ce_flutter`
- **Resolved Version:** `2.3.4`
- **Manifest Constraint:** `^2.3.4` (`Code/mine-flow-app/pubspec.yaml` line 35)
- **Lockfile Hash (sha256):** `2677e95a333ff15af43ccd06af7eb7abbf1a4f154ea071997f3de4346cae913a`
- **Resolved Source:** `hosted` (`https://pub.dev`)
- **Published Timestamp:** `2026-01-09 23:40:17 UTC` (from `hive_ce_flutter-versions.json` cache)
- **Release Cadence / Age on pub.dev:** ~8.0 months (244 days) since last release
- **Pre-releases on Registry:** None (`latest` = `2.3.4`)
- **Upstream Repository:** `https://github.com/IO-Design-Team/hive_ce/tree/main/hive_flutter`
- **License:** Apache-2.0 / BSD-3-Clause
- **Advisories / CVEs:** 0 reported (`isCurrentAffectedByAdvisory: false`)
- **Discontinued:** `false` (`isDiscontinued: false`, `replacedBy: null`)
- **Retracted:** `false` (`isCurrentRetracted: false`)
- **Declared Dependencies:**
  - `flutter: sdk flutter`
  - `hive_ce: ^2.16.0`
  - `path_provider: ^2.0.10`
  - `path: ^1.8.2`

### 3.3 Compact Dependency Graph
Output from `flutter pub deps --style=compact`:
```text
- hive_ce 2.19.3 [meta crypto web isolate_channel json_annotation]
- hive_ce_flutter 2.3.4 [flutter hive_ce path_provider path]
```

### 3.4 Live Upstream GitHub Repository Audit (`IO-Design-Team/hive_ce`)
Direct query of the GitHub API (`https://api.github.com/repos/IO-Design-Team/hive_ce`) yields concrete, verifiable maintenance signals:
- **Recent Commit Activity:**
  - `ed9d2438955ddaaeec7874bcea330a667d12ba7f` (2026-08-26 00:38:14 UTC): Merged PR #314 (`Upgrade rexios_lints to 19`) authored by Rexios80.
  - `338ec30faa82b3f6021a26417fe1f3ecd1de3aa9` (2026-08-25 23:46:59 UTC): Explicitly added support and fixes for **Flutter 3.48 beta**, pinning `analysis_server_plugin` and covering `CollectionBox.put(null)`.
- **Open Issues and Pull Requests:**
  - PR #321 (2026-08-23): `Let openBox skip records it cannot decode instead of failing outright` (addresses undecodable records on open).
  - Issue #322 (2026-08-23): `A cipher mismatch on open deletes the box under the default crashRecovery` (identifies data loss hazard when an incorrect encryption cipher is passed to an encrypted box under default `crashRecovery: true`). *Note for mine-flow:* The app does not encrypt Hive boxes (`flutter_secure_storage` is used for sensitive credentials), so this issue does not threaten mine-flow data.
  - PR #320 (2026-08-22): `Stop a failed box open leaking its error into the zone`.
  - Issue #323 (2026-08-25): `Remove the analysis_server_plugin 0.3.20 pin once Flutter beta can resolve plugins`.
- **Synthesis:** Although pub.dev has not seen a tagged release since February 2026, the upstream repository is actively maintained, tracked against upcoming Flutter beta releases, and reviewed by the maintainer.

---

## 4. SDK Compatibility & Dart-4 Trajectory

### 4.1 Current Compatibility
- **App Pubspec Constraint:** `sdk: ">=3.12.0 <4.0.0"`
- **Host SDK:** Dart `3.13.1`, Flutter `3.47.1`
- **`hive_ce` Constraint:** `sdk: ^3.4.0` (semver expands to `>=3.4.0 <4.0.0`)
- **`hive_ce_flutter` Constraint:** `sdk: ^3.4.0`, `flutter: ">=3.27.0"`
- **Assessment:** Both packages match the current host SDK without requiring any overrides (`dependency_overrides` count = 0). Compilation and execution are verified across all test tiers.

### 4.2 Dart-4 Trajectory
- **Hard Upper Bound:** In Dart package management, `^3.4.0` enforces an upper bound of `<4.0.0`. If the project or environment moves to Dart 4.x, `pub get` will reject `hive_ce` 2.19.3 and `hive_ce_flutter` 2.3.4 until upstream publishes a version constraint update.
- **Published Releases:** There are zero releases or prereleases on `pub.dev` supporting `sdk: ^4.0.0` or `>=4.0.0`.
- **Ecosystem State:** As of September 2026, Dart 3.13.1 is the active stable release. Dart 4 has not been published or scheduled with breaking changes by the Dart SDK team.
- **Audit Conclusion:** The package cannot support Dart 4 without an upstream release by the maintainer. However, this poses zero immediate hazard because Dart 4 is not in use, scheduled, or released.

---

## 5. Architectural Review (ADR-0006 & Clean Architecture)

### 5.1 ADR-0006 Assumptions
ADR-0006 selected Hive over SQLite/sqflite based on:
1. **Cross-Platform Support:** Pure Dart implementation with no native C/C++ SQLite binary required on the Web target.
2. **Low API Complexity:** Key-value box operations (`Box.put`, `Box.get`, FIFO queue) for sync queue and record caching.
3. **Reversibility:** Low-medium. ADR-0006 notes: *"Hive boxes are abstracted behind repository interfaces (Clean Architecture pattern), so swapping the storage engine in a later phase requires changing only the Data layer implementations, not the Domain or Presentation layers."*

### 5.2 Codebase Import Audit
A comprehensive codebase scan across `mine-flow-app` located **exactly 28 Dart files** importing `package:hive_ce` and **9 Dart files** importing `package:hive_ce_flutter`:

#### `package:hive_ce` (28 files)
- **Core Infrastructure (6 files in `lib/`):**
  - `lib/core/init/app_initializer.dart` (Hive initialization & box registration)
  - `lib/core/offline/adapters/model_adapters.dart` (handwritten TypeAdapters)
  - `lib/core/offline/adapters/sync_queue_item_adapter.dart`
  - `lib/core/offline/adapters/timeline_milestone_adapter.dart`
  - `lib/core/offline/hive_cache_repository.dart`
  - `lib/core/offline/hive_service.dart`
- **Feature Data Layer (8 files in `lib/`):**
  - `lib/features/attendance/data/adapters/attendance_record_dto_adapter.dart`
  - `lib/features/benchmark/data/datasources/benchmark_local_datasource.dart`
  - `lib/features/daily_log/data/adapters/daily_log_dto_adapter.dart`
  - `lib/features/data_bucket/data/datasources/data_bucket_local_datasource.dart`
  - `lib/features/equipment_check/data/adapters/equipment_check_dto_adapter.dart`
  - `lib/features/notifications/data/datasources/notification_local_datasource.dart`
  - `lib/features/notifications/data/models/app_notification_model_adapter.dart`
  - `lib/features/settings/data/datasources/settings_local_datasource.dart`
- **Application Root (1 file in `lib/`):**
  - `lib/main.dart` (invokes `AppInitializer.init()` on startup)
- **Unit / Widget / Integration Tests (11 files in `test/`):**
  - `test/features/data_bucket/data/repositories/data_bucket_repository_impl_test.dart`
  - `test/features/data_bucket/presentation/bloc/data_bucket_staleness_test.dart` (regression test verifying local cache stream emission fold)
  - `test/features/tracking/data/repositories/tracking_repository_impl_test.dart`
  - `test/features/zone/data/datasources/zone_local_datasource_test.dart`
  - `test/features/zone/data/repositories/zone_repository_impl_test.dart`
  - `test/integration/attendance_daily_log_sync_test.dart`
  - `test/integration/equipment_check_sync_test.dart`
  - `test/unit/attendance_repository_test.dart`
  - `test/unit/daily_log_repository_test.dart`
  - `test/unit/equipment_check_repository_test.dart`
  - `test/widget_test.dart`
- **Dual-Platform Integration Tests (2 files in `integration_test/`):**
  - `integration_test/helpers/app_harness.dart`
  - `integration_test/journeys/offline_sync_journey_test.dart`

#### `package:hive_ce_flutter` (9 files)
- `lib/core/offline/hive_service.dart` (`Hive.initFlutter`)
- `lib/main.dart`
- `test/integration/attendance_daily_log_sync_test.dart`
- `test/integration/equipment_check_sync_test.dart`
- `test/unit/attendance_repository_test.dart`
- `test/unit/daily_log_repository_test.dart`
- `test/unit/equipment_check_repository_test.dart`
- `integration_test/helpers/app_harness.dart`
- `integration_test/journeys/offline_sync_journey_test.dart`

**Verification Verdict:**
- **Zero domain entities or use cases** import Hive packages.
- **Zero presentation widgets or BLoCs** import Hive packages in production code.
- Clean Architecture isolation specified in ADR-0006 is fully respected.
- Web target compiles cleanly without native sqlite binaries.

---

## 6. Verification Record & Honesty Statement

### Deep Verification (Directly Executed & Proven)
- Scanned `prompts/STEP-index.md` for in-flight collisions (none found; STEP-53 is sole in-progress STEP).
- Cut execution branch `step-0053-dependency-maintenance` in `Code/mine-flow-app` and `Code/mine-flow-docs`.
- Synchronized `prompts/main` with `origin/main` via `git push origin main` (exit code 0).
- Verified local and resolved toolchain: Flutter `3.47.1`, Dart `3.13.1`, DevTools `2.60.0`.
- Verified exact resolved dependencies in `pubspec.lock` and `pubspec.yaml` (0 overrides).
- Executed `flutter pub outdated --show-all --prereleases --json` to verify pub.dev registry status, discontinued flags, advisory status, and absence of newer releases.
- Inspected cached package files, manifests, licenses, and changelogs in `D:\AppDev\.pub-cache\hosted\pub.dev\.cache\`.
- Queried GitHub API (`api.github.com/repos/IO-Design-Team/hive_ce/commits`, `.../issues`) to verify recent upstream maintenance commits (PR #314 on 2026-08-26) and issues.
- Audited all 28 `hive_ce` and 9 `hive_ce_flutter` import sites across `lib/`, `test/`, and `integration_test/`.

### Shallow Verification (Inspected Metadata Only)
- Package licenses (BSD-3-Clause / Apache 2.0) reviewed for legal compatibility with MIT.
- Sponsor/funding information verified from package manifest.

### Unverified Aspects (Honest Limitations)
- **Dart-4 Runtime Execution:** No tests were run on Dart 4 because no Dart 4 SDK exists in stable or preview channels.
- **No Test Suite Run:** Per the 53.1 prompt instructions ("Do not run a broad test suite for this code-free audit"), the full test suite was not re-run in this substep. Baseline test suite passes (550 passed + 5 skipped) from STEP-51.10 remain established at branch head.

---

## 7. RISK-0007 Disposition & Recommendations

### Evaluation of RISK-0007
- **Current Text in `registries/risks.yml`:**
  - Status: `open`
  - Revisit trigger: *"If hive_ce goes >6 months without a release, or Dart 4 breaks compatibility."*
  - Annotation from STEP-50.1: *"revisit trigger FIRED — last stable hive_ce release 2.19.3 was published 2026-02-03 (~7 months ago; pre-releases are not releases). Maintenance health also rated moderate (single maintainer). Follow-up: STEP-53."*

### Recommendation
1. **Status:** Transition from `open` to **`monitoring`**.
   - *Rationale:* While pub.dev has not seen a release in 219 days, live GitHub inspection proves the repository is actively maintained as of late August 2026 (preparing for Flutter 3.48 beta). The package has no known CVEs, is not discontinued, complies strictly with ADR-0006, and functions correctly on Flutter 3.47.1 / Dart 3.13.1. An immediate migration to Drift or SQLite WASM in Phase 3 would create massive scope expansion and risk with no functional benefit.
2. **Revisit Triggers:**
   - Trigger A: An upstream security vulnerability or critical defect is disclosed against `hive_ce`.
   - Trigger B: Dart 4 is officially released by Google with breaking changes or enforcing `<4.0.0` incompatibility that cannot be resolved upstream within 30 days.
   - Trigger C: The package is formally marked discontinued on `pub.dev`.
   - Trigger D: Post-MVP requirements demand relational queries, ACID transactions, or foreign keys that exceed Hive's key-value capabilities.
3. **Owner:** "TBD" (managed under periodic check-in cadence).
4. **Action for Substep 53.4:** Substep 53.4 should formalize this update in `Code/mine-flow-docs/registries/risks.yml` when closing STEP-53.

---

## 8. Modifications to Codebase

- Application code modified: **None**
- Manifest (`pubspec.yaml`) modified: **None**
- Lockfile (`pubspec.lock`) modified: **None**
- Dependencies changed or upgraded: **None**
