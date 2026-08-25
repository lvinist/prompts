# mine-flow — STEP-43.7: file_picker v9 → v11 API Migration

> **How to run:** Tell your agent: **"Read and run `Upcoming Prompts/mine-flow-STEP-43.7-PROMPT.md`."**
> This substep is self-contained — executable cold in a fresh chat.
> **Assigned model:** Sonnet 4.6 Thinking

## Context

`file_picker` v11 replaced the `FilePicker.platform.*` instance API with static `FilePicker.*` methods. All call sites need updating.

See: `Code/mine-flow-docs/reports/2026-08-13-flutter-dependency-ci-audit.md` — Section 3.4.

**Known state:**
- pubspec.yaml has `file_picker: ^9.0.0`.
- Call sites use `FilePicker.platform.pickFiles(...)` pattern.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-43-PLAN.md`
- `.throughstone/local-user.md`
- `Code/mine-flow-app/pubspec.yaml`
- Search codebase for `FilePicker.platform` to find all call sites

## Scope

**Own:** Upgrade file_picker to v11, migrate all call sites to static API.

**Do not:** Change any other packages. Change business logic.

## Your task

### 1. Upgrade in pubspec.yaml

Change:
```yaml
file_picker: ^9.0.0
```
To:
```yaml
# NOTE: Upgraded from ^9.0.0 to ^11.0.3. API breaking change: FilePicker.platform.*
# replaced with static FilePicker.* calls. Migrated in STEP-43.
file_picker: ^11.0.3
```

### 2. Migrate call sites

Search for all `FilePicker.platform.pickFiles` and `FilePicker.platform.` usages in `lib/` and `test/`. Replace with the static API equivalent:

- `FilePicker.platform.pickFiles(...)` → `FilePicker.pickFiles(...)`
- `FilePicker.platform.clearTemporaryFiles()` → `FilePicker.clearTemporaryFiles()` (if used)

The likely file is `lib/features/data_bucket/presentation/pages/upload_file_page.dart`.

### 3. Verify

```powershell
flutter pub get
flutter analyze
flutter test
```

All should pass.

### 4. Commit

```powershell
git add pubspec.yaml pubspec.lock lib/
git commit -m "deps(STEP-43.7): upgrade file_picker ^11.0.3, migrate to static API"
git push
```

## Verification

- `file_picker: ^11.0.3` in pubspec.yaml.
- No `FilePicker.platform.` references remain.
- `flutter pub get`, `flutter analyze`, `flutter test` all pass.

## Definition of done

- [ ] `file_picker` upgraded to `^11.0.3`.
- [ ] All `FilePicker.platform.*` migrated to `FilePicker.*`.
- [ ] `flutter pub get`, `flutter analyze`, `flutter test` pass.
- [ ] Committed and pushed on `step-0043-flutter-upgrade`.

## Next

After committing, continue in the same chat to **substep 43.8**: `Upcoming Prompts/mine-flow-STEP-43.8-PROMPT.md`.
