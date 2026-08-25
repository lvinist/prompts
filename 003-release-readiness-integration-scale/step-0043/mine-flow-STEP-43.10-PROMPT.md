# mine-flow — STEP-43.10: Full Verification Gate & Risk Register

> **How to run:** Tell your agent: **"Read and run `Upcoming Prompts/mine-flow-STEP-43.10-PROMPT.md`."**
> This substep is self-contained — executable cold in a fresh chat.
> **Assigned model:** Gemini 3.1 Pro High

## Context

All dependency migrations are complete (43.1–43.9). This substep runs the complete CI-equivalent verification gate locally — including the critical `flutter build apk --debug` that was never run locally before — and updates the risk register.

**Known state:**
- All package upgrades and migrations committed on `step-0043-flutter-upgrade`.
- Individual substeps verified `flutter pub get`, `flutter analyze`, and `flutter test` incrementally.
- `flutter build apk --debug` has NOT been run yet locally.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-43-PLAN.md`
- `.throughstone/local-user.md`
- `Code/mine-flow-docs/registries/risks.yml`

## Scope

**Own:** Run the full CI-equivalent gate locally. Update risk register. Archive STEP. Merge to master.

**Do not:** Make any code changes unless a gate fails (then fix and re-run).

## Your task

### 1. Full local verification gate

Run these in order. ALL must pass:

```powershell
D:
cd D:\AppDev\mine_flow\Code\mine-flow-app

# 1. Dependency resolution
flutter pub get

# 2. Contract guard
dart run tool/check_supabase_contracts.dart

# 3. Localization guard
dart run tool/check_l10n_baseline.dart

# 4. Formatting
dart format --output=none --set-exit-if-changed lib/ test/

# 5. Static analysis
flutter analyze

# 6. Test suite
flutter test

# 7. THE CRITICAL GATE - Android APK build
flutter build apk --debug
```

Record exit code and key output for every command.

If any gate fails:
- Diagnose the error locally (not by pushing to CI)
- Fix it
- Re-run all gates from the beginning
- Commit the fix with message: `fix(STEP-43.10): <what was fixed>`

### 2. Update risk register

In `Code/mine-flow-docs/registries/risks.yml`, add or update:

- **RISK-0005:** `fl_chart` v1.2.0 migration — API rewrite from 0.x, low severity if tests pass, monitor for regression.
- **RISK-0006:** `go_router` v17 observer API change — app doesn't use observers, low severity, revisit if adding navigation analytics.
- **RISK-0007:** `hive_ce` community fork — hive_ce is actively maintained but not by the original author, monitor community health.
- **RISK-0008:** `flutter_secure_storage` v11 skip-v10 data migration — no production users, dev data only, acceptable for current phase. Must revisit before production release if existing user data exists.

Commit risk register changes on the docs branch `step-0043-flutter-upgrade`:
```powershell
cd D:\AppDev\mine_flow\Code\mine-flow-docs
git checkout -b step-0043-flutter-upgrade
git add registries/risks.yml
git commit -m "risk(STEP-43.10): add RISK-0005 through RISK-0008 for dependency upgrades"
git push -u origin step-0043-flutter-upgrade
```

### 3. Update the audit report

Append a "STEP-43 Resolution Evidence" section to `Code/mine-flow-docs/reports/2026-08-13-flutter-dependency-ci-audit.md` documenting:
- All Priority 1 items resolved
- Exact command outputs from the verification gate
- Package versions confirmed
- APK build success evidence

### 4. Archive the STEP

The archive already exists at `prompts/003-release-readiness-integration-scale/step-0043/README.md`. Update it to reflect the actual work done (the redo, with correct dates and verification results).

### 5. Merge to master

```powershell
# mine-flow-app:
cd D:\AppDev\mine_flow\Code\mine-flow-app
git checkout master
git merge step-0043-flutter-upgrade --no-ff -m "merge(STEP-43): Flutter 3.47 Upgrade & Dependency Overhaul"
git push

# mine-flow-docs:
cd D:\AppDev\mine_flow\Code\mine-flow-docs
git checkout main
git merge step-0043-flutter-upgrade --no-ff -m "merge(STEP-43): risk register and audit report updates"
git push
```

### 6. Update STEP-index

In `prompts/STEP-index.md`:
- STEP-43 row: Status → `Done`
- STEP-42 row: Remove "Deferred" status, set to `Planned` (unblocked now)

```powershell
cd D:\AppDev\mine_flow\prompts
git add STEP-index.md
git commit -m "index(STEP-43): mark Done; unblock STEP-42"
git push
```

## Verification

- All 7 local gate commands exit 0.
- `flutter build apk --debug` exits 0 (APK produced at `build/app/outputs/flutter-apk/app-debug.apk`).
- RISK-0005–0008 present in risks.yml.
- STEP-43 merged to master in mine-flow-app.
- STEP-index shows STEP-43 Done, STEP-42 Planned.

## Definition of done

- [ ] `flutter pub get` exit 0.
- [ ] `dart run tool/check_supabase_contracts.dart` pass.
- [ ] `dart run tool/check_l10n_baseline.dart` pass.
- [ ] `dart format` clean.
- [ ] `flutter analyze` 0 issues.
- [ ] `flutter test` 434+ tests, 0 failures.
- [ ] **`flutter build apk --debug` exit 0.**
- [ ] RISK-0005–0008 in risks.yml.
- [ ] Audit report updated with resolution evidence.
- [ ] STEP-43 merged to master.
- [ ] STEP-index updated.

## Next

After merging, start a fresh chat and run **substep 43.11**: `Upcoming Prompts/mine-flow-STEP-43.11-PROMPT.md`.
