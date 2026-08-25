# mine-flow — STEP-43.1: Fix Impossible Dependency

> **How to run:** Tell your agent: **"Read and run `Upcoming Prompts/mine-flow-STEP-43.1-PROMPT.md`."**
> This substep is self-contained — executable cold in a fresh chat.
> **Assigned model:** Gemini 3.1 Pro High

## Context

STEP-43.0 created a clean branch from master and verified that `flutter pub get` fails because `flutter_bloc: ^9.1.1` doesn't exist on pub.dev (latest is 8.1.6). This substep fixes that impossible constraint and its companion `bloc_test` version.

See: `Code/mine-flow-docs/reports/2026-08-13-flutter-dependency-ci-audit.md` — Section 3.1, Finding: `flutter_bloc ^9.1.1` does not exist.

**Known state:**
- On branch `step-0043-flutter-upgrade` based on master.
- `flutter pub get` fails.
- pubspec.yaml has `flutter_bloc: ^9.1.1` (non-existent) and `bloc_test: ^10.0.0`.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-43-PLAN.md`
- `.throughstone/local-user.md`
- `Code/mine-flow-app/pubspec.yaml`
- `Code/mine-flow-docs/reports/2026-08-13-flutter-dependency-ci-audit.md` (Section 3.1)

## Scope

**Own:** Fix `flutter_bloc` and `bloc_test` version constraints in pubspec.yaml.

**Do not:** Change any other packages. Change any Dart code. Touch CI or Gradle files.

## Your task

### 1. Confirm branch state

```powershell
D:
cd D:\AppDev\mine_flow\Code\mine-flow-app
git status --short --branch
git log --oneline -3
```

Confirm you are on `step-0043-flutter-upgrade` based on master.

### 2. Fix flutter_bloc and bloc_test

In `pubspec.yaml`:
- Change `flutter_bloc: ^9.1.1` → `flutter_bloc: ^8.1.6`
- Change `bloc_test: ^10.0.0` → `bloc_test: ^9.1.5`

These are the correct companion versions: `flutter_bloc` 8.x works with `bloc_test` 9.x.

### 3. Verify

```powershell
flutter pub get
```

This should now exit 0. Record the output showing dependencies resolved.

### 4. Commit

```powershell
git add pubspec.yaml pubspec.lock
git commit -m "fix(STEP-43.1): correct flutter_bloc ^9.1.1 (non-existent) to ^8.1.6"
```

Do NOT push yet. We push after substep 43.3 (CI hardening) so the first push has a valid CI config.

## Verification

- `flutter pub get` exits 0.
- `pubspec.yaml` shows `flutter_bloc: ^8.1.6` and `bloc_test: ^9.1.5`.
- No other packages changed.

## Definition of done

- [ ] `flutter_bloc` corrected to `^8.1.6` in pubspec.yaml.
- [ ] `bloc_test` corrected to `^9.1.5` in pubspec.yaml.
- [ ] `flutter pub get` exits 0.
- [ ] Committed on `step-0043-flutter-upgrade`.

## Next

After committing, continue in the same chat to **substep 43.2**: `Upcoming Prompts/mine-flow-STEP-43.2-PROMPT.md`.
