# mine-flow — STEP-43.5: Hive → hive_ce Migration

> **How to run:** Tell your agent: **"Read and run `Upcoming Prompts/mine-flow-STEP-43.5-PROMPT.md`."**
> This substep is self-contained — executable cold in a fresh chat.
> **Assigned model:** Sonnet 4.6 Thinking

## Context

The `hive` and `hive_flutter` packages are unmaintained (no releases since 2022). The community-maintained successor is `hive_ce` (Hive Community Edition). This substep migrates the entire codebase.

See: `Code/mine-flow-docs/reports/2026-08-13-flutter-dependency-ci-audit.md` — Section 3.2.

**Known state:**
- `flutter pub get` and `flutter analyze` pass.
- 26 Dart files import `package:hive/hive.dart` or `package:hive_flutter/hive_flutter.dart`.
- pubspec.yaml has `hive: ^2.2.3` and `hive_flutter: ^1.1.0`.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-43-PLAN.md`
- `.throughstone/local-user.md`
- `Code/mine-flow-app/pubspec.yaml`
- Search the codebase for all files importing `package:hive/` or `package:hive_flutter/`

## Scope

**Own:** Swap hive/hive_flutter for hive_ce/hive_ce_flutter in pubspec.yaml and all Dart imports.

**Do not:** Change any business logic. Change any API calls. Change any other packages.

## Your task

### 1. Update pubspec.yaml

Replace:
```yaml
hive: ^2.2.3
hive_flutter: ^1.1.0
```

With:
```yaml
# --- Offline storage (ADR-0001: hive_ce is the community-maintained successor
# to the abandoned hive package. Migrated in STEP-43. See RISK-0007.) ---
hive_ce: ^2.19.3
hive_ce_flutter: ^2.3.4
```

### 2. Find and replace all imports

Search the entire `lib/` and `test/` directories for:
- `package:hive/hive.dart` → `package:hive_ce/hive_ce.dart`
- `package:hive_flutter/hive_flutter.dart` → `package:hive_ce_flutter/hive_ce_flutter.dart`
- Any other `package:hive/` → `package:hive_ce/`
- Any other `package:hive_flutter/` → `package:hive_ce_flutter/`

The hive_ce API is wire-compatible with hive — same class names, same TypeAdapter interface, same Box/LazyBox APIs. Only the package import paths change.

Record every file changed.

### 3. Verify thoroughly

```powershell
flutter pub get
flutter analyze
flutter test
```

All must pass. `flutter test` should show 434+ tests, 0 failures.

Also verify no stale imports remain:
```powershell
& "C:\Program Files\Git\bin\sh.exe" -c "grep -r 'package:hive/' lib/ test/ --include='*.dart' -l"
& "C:\Program Files\Git\bin\sh.exe" -c "grep -r 'package:hive_flutter/' lib/ test/ --include='*.dart' -l"
```

Both should return empty (no results).

### 4. Commit

```powershell
git add -A
git commit -m "refactor(STEP-43.5): migrate hive/hive_flutter to hive_ce/hive_ce_flutter (26 files)"
git push
```

## Verification

- No `package:hive/` or `package:hive_flutter/` imports remain in lib/ or test/.
- All replaced with `package:hive_ce/` and `package:hive_ce_flutter/`.
- `flutter pub get` exits 0.
- `flutter analyze` exits 0.
- `flutter test` 434+ tests, 0 failures.

## Definition of done

- [ ] `hive_ce: ^2.19.3` and `hive_ce_flutter: ^2.3.4` in pubspec.yaml.
- [ ] All 26 Dart files migrated to `hive_ce` imports.
- [ ] Zero stale `package:hive/` or `package:hive_flutter/` imports.
- [ ] `flutter pub get`, `flutter analyze`, `flutter test` all pass.
- [ ] Committed and pushed on `step-0043-flutter-upgrade`.

## Next

After committing, continue in the same chat to **substep 43.6**: `Upcoming Prompts/mine-flow-STEP-43.6-PROMPT.md`.
