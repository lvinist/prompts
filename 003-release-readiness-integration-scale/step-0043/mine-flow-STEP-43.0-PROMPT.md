# mine-flow — STEP-43.0: Git Housekeeping & Clean Branch

> **How to run:** Tell your agent: **"Read and run `Upcoming Prompts/mine-flow-STEP-43.0-PROMPT.md`."**
> This substep is self-contained — executable cold in a fresh chat.
> **Assigned model:** Gemini 3.7 Flash High

## Context

STEP-43 redoes the Flutter 3.47 upgrade from a clean master base. The previous attempt accumulated 7 brute-force CI fix commits on `step-0042-staging-pipeline` that are inconsistent and incomplete. This substep preserves the real STEP-42 work, creates a clean branch for STEP-43, and establishes the broken baseline.

**Known state (as of 2026-08-25):**
- `Code/mine-flow-app` is on `step-0042-staging-pipeline` (HEAD: `e7f1951`). Master is at `9277507` (STEP-41 merged).
- The branch has 11 commits diverging from master: 3 real STEP-42 commits + 8 brute-force CI fixes.
- No `step-0043-flutter-upgrade` branch exists locally or on remote.
- 434 tests passing on master. `flutter analyze` clean on master.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-43-PLAN.md`
- `.throughstone/local-user.md`

## Scope

**Own:** Tag old branch state, note STEP-42 real commits, create clean `step-0043-flutter-upgrade` from master, verify broken baseline.

**Do not:** Fix any dependencies. Change any code. Touch pubspec.yaml.

## Your task

### 1. Tag the old branch for safekeeping

```powershell
D:
cd D:\AppDev\mine_flow\Code\mine-flow-app
git tag archive/step-0042-brute-force-attempt step-0042-staging-pipeline
```

This preserves the old state so nothing is lost.

### 2. Note the real STEP-42 commits

These 3 commits are the real STEP-42 work we'll cherry-pick later in substep 43.11:
- `b42ae17` — feat(STEP-42.1): add supabase config.toml, rename migration, and patch seed.sql
- `0ad1a05` — feat(STEP-42.2): commit generated Supabase types and harden contract guard
- `8b5867d` — docs(STEP-42.3): add SUPABASE_PROJECT_REF and STAGING_* keys to .env.example

Record these SHA hashes.

### 3. Create clean STEP-43 branch from master

```powershell
git checkout master
git checkout -b step-0043-flutter-upgrade
```

### 4. Verify the broken baseline

```powershell
flutter pub get
```

This should **fail** because `flutter_bloc: ^9.1.1` doesn't exist on pub.dev. Record the exact error message. This establishes that master is genuinely broken and needs STEP-43.

### 5. Update STEP-index

In `D:\AppDev\mine_flow\prompts\STEP-index.md`, update the STEP-43 row:
- Status: `In progress` (it was incorrectly marked Done)
- Owner: current model assignments

Commit and push on prompts trunk:
```powershell
cd D:\AppDev\mine_flow\prompts
git add STEP-index.md
git commit -m "fix(STEP-43): correct status to In progress (code never merged)"
git push
```

## Verification

- `archive/step-0042-brute-force-attempt` tag exists pointing to `e7f1951`.
- Current branch is `step-0043-flutter-upgrade` based on master (`9277507`).
- `flutter pub get` fails with a `flutter_bloc` version resolution error.
- STEP-index STEP-43 row shows `In progress`.

## Definition of done

- [ ] Old branch state preserved via git tag.
- [ ] 3 real STEP-42 commit SHAs recorded.
- [ ] Clean `step-0043-flutter-upgrade` branch created from master.
- [ ] Broken baseline verified (`flutter pub get` fails).
- [ ] STEP-index corrected to `In progress`.

## Next

After completing, start a fresh chat and run **substep 43.1**: `Upcoming Prompts/mine-flow-STEP-43.1-PROMPT.md`.
