# mine-flow — STEP-43.4: Core Package Version Bumps

> **How to run:** Tell your agent: **"Read and run `Upcoming Prompts/mine-flow-STEP-43.4-PROMPT.md`."**
> This substep is self-contained — executable cold in a fresh chat.
> **Assigned model:** Gemini 3.1 Pro High

## Context

STEP-43.3 hardened the CI workflow. This substep bumps the remaining core packages that are multiple versions behind but have no breaking API changes.

See: `Code/mine-flow-docs/reports/2026-08-13-flutter-dependency-ci-audit.md` — Sections 3.1, 3.2, 3.6, Priority 3.

**Known state:**
- `flutter pub get` passes (flutter_bloc fixed in 43.1).
- Packages still at old versions: go_router, supabase_flutter, connectivity_plus, build_runner.
- SDK constraint: `>=3.12.2 <4.0.0`.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-43-PLAN.md`
- `.throughstone/local-user.md`
- `Code/mine-flow-app/pubspec.yaml`

## Scope

**Own:** Bump go_router, supabase_flutter, connectivity_plus, build_runner, and SDK constraint.

**Do not:** Migrate hive, file_picker, flutter_secure_storage, forui, or fl_chart (those are in 43.5–43.8). Change any Dart code.

## Your task

### 1. Bump packages in pubspec.yaml

Change:
- `go_router: ^15.1.2` → `go_router: ^17.3.0`
- `supabase_flutter: ^2.9.2` → `supabase_flutter: ^2.17.1`
- `connectivity_plus: ^6.1.4` → `connectivity_plus: ^7.3.1`
- `build_runner: ^2.3.0` → `build_runner: ^2.4.0`
- SDK constraint: `>=3.12.2 <4.0.0` → `>=3.12.0 <4.0.0`

### 2. Verify

```powershell
flutter pub get
flutter analyze
```

Both should exit 0. `flutter analyze` may show new warnings from upgraded packages — fix any that appear.

### 3. Commit

```powershell
git add pubspec.yaml pubspec.lock
git commit -m "deps(STEP-43.4): bump go_router ^17.3.0, supabase_flutter ^2.17.1, connectivity_plus ^7.3.1, build_runner ^2.4.0"
git push
```

## Verification

- All 4 packages bumped to target versions.
- SDK constraint is `>=3.12.0 <4.0.0`.
- `flutter pub get` exits 0.
- `flutter analyze` exits 0.

## Definition of done

- [ ] go_router `^17.3.0`, supabase_flutter `^2.17.1`, connectivity_plus `^7.3.1`, build_runner `^2.4.0`.
- [ ] SDK constraint `>=3.12.0 <4.0.0`.
- [ ] `flutter pub get` and `flutter analyze` both exit 0.
- [ ] Committed and pushed on `step-0043-flutter-upgrade`.

## Next

After committing, start a fresh chat and run **substep 43.5**: `Upcoming Prompts/mine-flow-STEP-43.5-PROMPT.md`.
