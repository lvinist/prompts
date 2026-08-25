# mine-flow — STEP-43 PLAN: Flutter 3.47 Upgrade & Dependency Overhaul (Redo)

**Phase:** Phase 3 — Release Readiness, Integration & Scale
**Owner:** See model assignments per substep below
**Status:** Planned
**Date:** 2026-08-25
**Branch:** `step-0043-flutter-upgrade`
**Repos (projection):** `mine-flow-app`, `mine-flow-docs`, `prompts` (completion archive only)

> Redo the Flutter 3.47 upgrade from a clean master base, verifying every change locally before pushing to CI. The previous STEP-43 was marked Done in the STEP-index but the code changes were never merged to any branch — master is still at STEP-41. The `step-0042-staging-pipeline` branch accumulated 7 brute-force CI fix commits that partially overlap with STEP-43 scope but are inconsistent and incomplete. This PLAN starts fresh from master, applies fixes in dependency order with local verification gates at every substep, and concludes with a clean rebase of the real STEP-42 work.

---

## Background

The Android CI build has been broken since the `step-0042-staging-pipeline` branch was created. An audit report (`Code/mine-flow-docs/reports/2026-08-13-flutter-dependency-ci-audit.md`) identified 5 interrelated root causes:

1. **`flutter_bloc: ^9.1.1`** — version does not exist on pub.dev (latest is 8.1.6). `flutter pub get` fails immediately.
2. **Split Flutter versions in CI** — `test` job pinned to 3.32.x, `build-android` wildcarded to `3.x` (resolved to 3.47.0). `forui ^0.24.2` requires Flutter ≥ 3.44.0, so the `test` job fails at `pub get`.
3. **AGP 9.0.1 vs Flutter 3.47's requirement for AGP ≥ 9.1.0** — Flutter 3.47's Gradle plugin hard-rejects AGP < 9.1.0.
4. **No JDK pinning in CI** — AGP 9.x requires JDK 17; unpinned runners are non-deterministic.
5. **Transitive dependency conflicts** — `flutter_secure_storage` v11 pulls `win32 ^6.0.1` which breaks `file_picker` (needs `win32 ^5.x`); `hive`/`hive_flutter` are unmaintained.

The previous attempt tried to fix these by pushing to CI and waiting 10+ minutes per iteration (7 cycles, ~2 hours, no resolution). This redo builds and verifies locally.

---

## Decisions locked (pre-answered by project owner)

- **Approach:** Cherry-pick only the 3 real STEP-42 commits from the old branch; discard the 7 brute-force CI fix commits.
- **STEP-42 status:** Resume immediately after STEP-43 merges (do not keep deferred to STEP-46).
- **`compileSdk = 36` in `build.gradle.kts`:** From the brute-force; Sonnet should verify the correct value for Flutter 3.47 + AGP 9.1.0 and either keep or revert to `flutter.compileSdkVersion` (dynamic).
- **`flutter_secure_storage` skip-v10:** Acceptable since there are no production users — direct v9 → v11 skip, documented as accepted risk.

---

## Current repository state (as of 2026-08-25)

- **`Code/mine-flow-app`**: on `step-0042-staging-pipeline` (diverged from master with 11 commits / 123 files changed). Master is at commit `9277507` (STEP-41 merged).
- **`Code/mine-flow-docs`**: current.
- **`prompts`**: STEP-43 row says Done but code was never merged. Must be corrected.
- **Old `step-0042` real commits to preserve:**
  - `b42ae17` — feat(STEP-42.1): add supabase config.toml, rename migration, and patch seed.sql
  - `0ad1a05` — feat(STEP-42.2): commit generated Supabase types and harden contract guard
  - `8b5867d` — docs(STEP-42.3): add SUPABASE_PROJECT_REF and STAGING_* keys to .env.example
- **Old brute-force commits to discard:** `3174ea2` through `e7f1951` (8 commits)

---

## Model assignments

| Model | Substeps | Rationale |
|-------|----------|-----------|
| **Gemini 3.7 Flash High** | 43.0 (Git housekeeping) | Purely mechanical git commands |
| **Gemini 3.1 Pro High** | 43.1–43.4 (Foundation fixes) | Well-defined but needs careful version compatibility awareness |
| **Sonnet 4.6 Thinking** | 43.5–43.9 (Hard migrations) | Requires reading migration guides, judgment calls across many files, transitive conflict resolution |
| **Gemini 3.1 Pro High** | 43.10 (Full verification & risk docs) | Systematic verification and documentation |
| **Gemini 3.7 Flash High** | 43.11 (STEP-42 rebase & close) | Mechanical git cherry-pick and conflict resolution |

---

## Scope boundaries

### In scope
1. Git housekeeping: tag old branch, create clean STEP-43 branch from master.
2. Fix `flutter_bloc` and `bloc_test` versions.
3. Upgrade AGP 9.0.1 → 9.1.0, KGP 2.3.20 → 2.4.0, set explicit `minSdk = 23`.
4. CI workflow: pin Flutter 3.47.0, add JDK 17 Temurin to both jobs.
5. Bump go_router, supabase_flutter, connectivity_plus, build_runner, SDK constraint.
6. Migrate `hive`/`hive_flutter` → `hive_ce`/`hive_ce_flutter` across 26 Dart files.
7. Upgrade `flutter_secure_storage` v9 → v11, handle `win32` transitive conflict.
8. Migrate `file_picker` v9 → v11 (static API).
9. Upgrade `forui` and `fl_chart` to latest.
10. Verify `go_router` v17 compatibility.
11. Full local verification gate including `flutter build apk --debug`.
12. Risk register updates (RISK-0005 through RISK-0008).
13. Clean rebase of STEP-42 real commits on merged STEP-43.

### Explicitly out of scope
- Any application feature changes.
- Staging environment provisioning (STEP-42/46).
- Security/privacy controls (STEP-44).
- E2E journeys or runtime design review (STEP-45).

---

## Substeps

| # | Title | Owner | Produces | Depends on | Local gate |
|---|-------|-------|----------|------------|------------|
| 43.0 | Git Housekeeping & Clean Branch | Flash High | Tagged old branch; clean `step-0043-flutter-upgrade` from master | None | `flutter pub get` fails (establishes broken baseline) |
| 43.1 | Fix Impossible Dependency | Pro High | `pubspec.yaml`: flutter_bloc `^8.1.6`, bloc_test `^9.1.5` | 43.0 | `flutter pub get` exits 0 |
| 43.2 | Android Build Chain Upgrade | Pro High | AGP 9.1.0, KGP 2.4.0, minSdk 23, verify compileSdk | 43.1 | `flutter pub get` exits 0 |
| 43.3 | CI Workflow Hardening | Pro High | JDK 17 Temurin both jobs; Flutter 3.47.0 pinned | 43.2 | YAML valid |
| 43.4 | Core Package Version Bumps | Pro High | go_router ^17.3.0, supabase_flutter ^2.17.1, connectivity_plus ^7.3.1, build_runner ^2.4.0, SDK >=3.12.0 | 43.3 | `flutter pub get` + `flutter analyze` exit 0 |
| 43.5 | Hive → hive_ce Migration | Sonnet 4.6 Thinking | 26 files migrated; pubspec swapped | 43.4 | `flutter pub get` → `flutter analyze` → `flutter test` all pass |
| 43.6 | flutter_secure_storage v9 → v11 | Sonnet 4.6 Thinking | pubspec ^11.0.0; encryptedSharedPreferences removed; dependency_overrides for win32 conflict | 43.5 | `flutter pub get` → `flutter analyze` pass |
| 43.7 | file_picker v9 → v11 API Migration | Sonnet 4.6 Thinking | pubspec ^11.0.3; all FilePicker.platform.* → static API | 43.6 | `flutter pub get` → `flutter analyze` → `flutter test` pass |
| 43.8 | forui + fl_chart Upgrade | Sonnet 4.6 Thinking | forui ^0.25.0, fl_chart ^1.2.0 | 43.7 | `flutter analyze` → `flutter test` pass |
| 43.9 | go_router v17 Compatibility Check | Sonnet 4.6 Thinking | Verify router.dart unchanged; doc any breaking change | 43.8 | `flutter analyze` clean |
| 43.10 | Full Verification Gate & Risk Register | Pro High | All 7 local gates pass including `flutter build apk --debug`; RISK-0005–0008; STEP archived | 43.9 | Full CI-equivalent gate passes locally |
| 43.11 | STEP-42 Rebase & Close | Flash High | Cherry-pick 3 STEP-42 commits on merged STEP-43 master; verify; push | 43.10 merged to master | `flutter build apk --debug` + `flutter test` pass on rebased branch |

---

## Test plan

| Surface | Substep | Gate | Notes |
|---------|---------|------|-------|
| Dependency resolution | 43.1 | `flutter pub get` → exit 0 | First gate after fixing flutter_bloc |
| Android build chain | 43.2 | `flutter pub get` → exit 0 | AGP/KGP/minSdk |
| CI config validity | 43.3 | Manual YAML review | No local CI runner |
| Static analysis | 43.4 | `flutter analyze` → 0 issues | After all core bumps |
| Hive migration | 43.5 | `flutter test` → 434+ tests, 0 failures | Largest migration scope |
| Secure storage | 43.6 | `flutter analyze` → 0 issues | encryptedSharedPreferences removed |
| File picker API | 43.7 | `flutter test` → 0 failures | Static API migration |
| Chart/UI libs | 43.8 | `flutter analyze` + `flutter test` | fl_chart 0.x → 1.x |
| Router compat | 43.9 | `flutter analyze` clean | go_router v17 |
| **APK build** | **43.10** | **`flutter build apk --debug` → exit 0** | **The critical gate** |
| Contract guard | 43.10 | `dart run tool/check_supabase_contracts.dart` → pass | Must not regress |
| l10n guard | 43.10 | `dart run tool/check_l10n_baseline.dart` → pass | Must not regress |
| Formatting | 43.10 | `dart format --output=none --set-exit-if-changed lib/ test/` | Clean |
| Rebase verification | 43.11 | Full gate on rebased STEP-42 branch | No regressions from cherry-pick |

---

## Ground rules

- **Build locally before pushing.** Every substep has a local verification gate. Do not push until it passes.
- **One commit per substep.** Clean, atomic commits. No multi-substep squashes.
- **Evidence over assertion.** Record actual command output (exit codes, test counts, error messages).
- **The audit report is your map.** Reference `Code/mine-flow-docs/reports/2026-08-13-flutter-dependency-ci-audit.md` for every fix — it has the root-cause analysis.
- **Calibrate from root `.throughstone/local-user.md`.**
- **Windows PowerShell:** switch drive with `D:` then `cd`; run `.sh` scripts via `& "C:\Program Files\Git\bin\sh.exe"`.

---

## Definition of done

- [ ] `flutter_bloc` corrected to `^8.1.6`; `bloc_test` to `^9.1.5`.
- [ ] AGP 9.1.0, KGP 2.4.0, `minSdk = 23` in build config.
- [ ] CI pinned to Flutter 3.47.0 with JDK 17 Temurin in both jobs.
- [ ] go_router, supabase_flutter, connectivity_plus, build_runner bumped.
- [ ] `hive`/`hive_flutter` → `hive_ce`/`hive_ce_flutter` across 26 files.
- [ ] `flutter_secure_storage` v11; `encryptedSharedPreferences` removed; `dependency_overrides` for win32.
- [ ] `file_picker` v11; static API migration.
- [ ] `forui` ^0.25.0; `fl_chart` ^1.2.0.
- [ ] `go_router` v17 compatibility confirmed.
- [ ] `flutter pub get` exit 0; `flutter analyze` 0 issues; `flutter test` 434+ tests 0 failures.
- [ ] **`flutter build apk --debug` exit 0** (locally verified).
- [ ] RISK-0005–0008 in `registries/risks.yml`.
- [ ] STEP-43 merged to master; STEP-index updated.
- [ ] STEP-42 real commits cherry-picked on new base; full verification passes.
- [ ] Old brute-force branch replaced with clean rebased branch.
