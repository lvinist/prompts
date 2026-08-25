# mine-flow — STEP-43.8: forui + fl_chart Upgrade

> **How to run:** Tell your agent: **"Read and run `Upcoming Prompts/mine-flow-STEP-43.8-PROMPT.md`."**
> This substep is self-contained — executable cold in a fresh chat.
> **Assigned model:** Sonnet 4.6 Thinking

## Context

`forui` needs bumping from `^0.24.2` to `^0.25.0` (minor but may have breaking widget changes). `fl_chart` needs migrating from exact pin `0.69.2` to `^1.2.0` (full API rewrite from 0.x to 1.x). The fl_chart migration is the main risk.

See: `Code/mine-flow-docs/reports/2026-08-13-flutter-dependency-ci-audit.md` — Section 3.5.

**Known state:**
- pubspec.yaml has `forui: ^0.24.2` and `fl_chart: 0.69.2` (exact pin).
- `fl_chart` is used in timeline chart widgets.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-43-PLAN.md`
- `.throughstone/local-user.md`
- `Code/mine-flow-app/pubspec.yaml`
- Search for all files importing `package:fl_chart/` to identify affected code
- Search for all files importing `package:forui/` that may be affected by 0.24 → 0.25 changes

## Scope

**Own:** Upgrade forui and fl_chart, fix any API breakages.

**Do not:** Change unrelated business logic. Add new features.

## Your task

### 1. Upgrade in pubspec.yaml

Change:
```yaml
forui: ^0.24.2
fl_chart: 0.69.2
```
To:
```yaml
forui: ^0.25.0
fl_chart: ^1.2.0
```

### 2. Run pub get and analyze

```powershell
flutter pub get
flutter analyze
```

If `flutter analyze` shows errors from `fl_chart` API changes (renamed classes, removed methods, changed constructors), fix each one by consulting the fl_chart 1.0 migration guide or release notes.

Common fl_chart 0.x → 1.x changes:
- `LineChartBarData` constructor changes
- `FlSpot` may have API changes
- `BarChartGroupData` may have API changes
- Tooltip styling API changes

For `forui` 0.24 → 0.25: check for widget constructor changes (new required parameters, removed parameters).

### 3. Run full test suite

```powershell
flutter test
```

Fix any test failures related to the upgraded packages.

### 4. Commit

```powershell
git add -A
git commit -m "deps(STEP-43.8): upgrade forui ^0.25.0, fl_chart ^1.2.0 (0.x to 1.x migration)"
git push
```

## Verification

- `forui: ^0.25.0` and `fl_chart: ^1.2.0` in pubspec.yaml.
- `flutter pub get`, `flutter analyze`, `flutter test` all pass.
- No deprecated fl_chart 0.x API remains.

## Definition of done

- [ ] `forui` upgraded to `^0.25.0`.
- [ ] `fl_chart` migrated from `0.69.2` to `^1.2.0`.
- [ ] All fl_chart API breakages resolved.
- [ ] `flutter pub get`, `flutter analyze`, `flutter test` pass.
- [ ] Committed and pushed on `step-0043-flutter-upgrade`.

## Next

After committing, continue in the same chat to **substep 43.9**: `Upcoming Prompts/mine-flow-STEP-43.9-PROMPT.md`.
