# mine-flow — STEP-43.11: STEP-42 Rebase & Close

> **How to run:** Tell your agent: **"Read and run `Upcoming Prompts/mine-flow-STEP-43.11-PROMPT.md`."**
> This substep is self-contained — executable cold in a fresh chat.
> **Assigned model:** Gemini 3.7 Flash High

## Context

STEP-43 is merged to master. The old `step-0042-staging-pipeline` branch has 3 real STEP-42 commits mixed with 8 brute-force CI fix commits. This substep creates a clean STEP-42 branch by cherry-picking only the real commits onto the new master base.

**Known state:**
- Master now has all STEP-43 dependency upgrades.
- Old branch tagged at `archive/step-0042-brute-force-attempt`.
- Real STEP-42 commits to cherry-pick:
  - `b42ae17` — feat(STEP-42.1): add supabase config.toml, rename migration, and patch seed.sql
  - `0ad1a05` — feat(STEP-42.2): commit generated Supabase types and harden contract guard
  - `8b5867d` — docs(STEP-42.3): add SUPABASE_PROJECT_REF and STAGING_* keys to .env.example

## Read these first

- `Upcoming Prompts/mine-flow-STEP-43-PLAN.md`
- `Upcoming Prompts/mine-flow-STEP-42-PLAN.md`
- `.throughstone/local-user.md`

## Scope

**Own:** Cherry-pick STEP-42 real commits onto new master. Resolve conflicts. Verify. Force-push clean branch.

**Do not:** Continue STEP-42 substeps (42.4+). Change application feature code.

## Your task

### 1. Delete old local branch and create fresh one

```powershell
D:
cd D:\AppDev\mine_flow\Code\mine-flow-app
git checkout master
git branch -D step-0042-staging-pipeline
git checkout -b step-0042-staging-pipeline
```

### 2. Cherry-pick the 3 real STEP-42 commits

```powershell
git cherry-pick b42ae17
git cherry-pick 0ad1a05
git cherry-pick 8b5867d
```

If conflicts occur (likely in `pubspec.yaml`, `ci.yml`, `tool/check_supabase_contracts.dart`):
- For `pubspec.yaml`: keep the STEP-43 package versions, accept STEP-42's structural additions (generated types path, etc.)
- For `ci.yml`: keep the STEP-43 Flutter 3.47.0 pin and JDK 17 setup, accept STEP-42's new jobs if any
- For other files: accept the STEP-42 change, verify it compiles

After resolving each conflict, continue the cherry-pick:
```powershell
git add -A
git cherry-pick --continue
```

### 3. Verify the rebased branch

Run the full verification gate:

```powershell
flutter pub get
flutter analyze
flutter test
flutter build apk --debug
```

All must pass.

### 4. Force-push the clean branch

```powershell
git push --force-with-lease origin step-0042-staging-pipeline
```

This replaces the old 11-commit mess with a clean 3-commit branch on the new STEP-43 base.

### 5. Verify CI passes

The push triggers CI. Monitor the GitHub Actions run. It should pass (CI now has correct Flutter 3.47.0 pin and JDK 17).

### 6. Update STEP-index

In `prompts/STEP-index.md`:
- STEP-42 row: Status → `In progress`
- Confirm substep table still accurate for 42.1–42.3 (those are the cherry-picked commits)

```powershell
cd D:\AppDev\mine_flow\prompts
git add STEP-index.md
git commit -m "index(STEP-42): mark In progress on clean rebased branch"
git push
```

## Verification

- `step-0042-staging-pipeline` branch has exactly 3 commits above master.
- `flutter pub get`, `flutter analyze`, `flutter test`, `flutter build apk --debug` all pass.
- GitHub Actions CI passes on the pushed branch.
- STEP-index shows STEP-42 as `In progress`.

## Definition of done

- [ ] Old branch replaced with clean 3-commit branch on STEP-43 master.
- [ ] All cherry-pick conflicts resolved.
- [ ] Full verification gate passes locally.
- [ ] Branch force-pushed to remote.
- [ ] CI passes on GitHub.
- [ ] STEP-index updated to `In progress`.

## Next

STEP-43 is now fully complete. STEP-42 continues from substep 42.4. Start a fresh chat and run the next STEP-42 substep: `Upcoming Prompts/mine-flow-STEP-42.4-PROMPT.md`.
