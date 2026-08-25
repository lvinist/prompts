# mine-flow — STEP-43.6: flutter_secure_storage v9 → v11

> **How to run:** Tell your agent: **"Read and run `Upcoming Prompts/mine-flow-STEP-43.6-PROMPT.md`."**
> This substep is self-contained — executable cold in a fresh chat.
> **Assigned model:** Sonnet 4.6 Thinking

## Context

`flutter_secure_storage` jumped from v9 to v11 with breaking changes. v10 included a data migration step; since mine-flow has no production users, we skip v10 and go directly to v11. This also introduces a transitive `win32` version conflict that needs a dependency override.

See: `Code/mine-flow-docs/reports/2026-08-13-flutter-dependency-ci-audit.md` — Section 3.3.

**Known state:**
- pubspec.yaml has `flutter_secure_storage: ^9.2.4`.
- `lib/core/security/secure_storage_service.dart` uses `encryptedSharedPreferences: true` (deprecated in v11).
- `file_picker: ^9.0.0` is still at v9 (migrated later in 43.7) — but even after v11 migration, a transitive `win32` conflict exists.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-43-PLAN.md`
- `.throughstone/local-user.md`
- `Code/mine-flow-app/pubspec.yaml`
- `Code/mine-flow-app/lib/core/security/secure_storage_service.dart`

## Scope

**Own:** Upgrade flutter_secure_storage to v11, remove deprecated API, add dependency override for win32 conflict.

**Do not:** Upgrade file_picker (43.7). Change any other business logic.

## Your task

### 1. Upgrade in pubspec.yaml

Change:
```yaml
flutter_secure_storage: ^9.2.4
```
To:
```yaml
# NOTE: Upgraded from ^9.2.4 directly to ^11.0.0 (STEP-43). Dev environment only.
# minSdk raised to 23 per v11 requirement. See RISK-0008.
flutter_secure_storage: ^11.0.0
```

### 2. Add dependency override for win32 conflict

At the bottom of pubspec.yaml, add (or update) the `dependency_overrides` section:

```yaml
# Dependency overrides to resolve transitive win32 version conflict (STEP-43):
# flutter_secure_storage ^11.0.0 pulls in flutter_secure_storage_windows ^4.2.2
# which requires win32 ^6.0.1, conflicting with file_picker (uses win32 ^5.9.0).
# Fix: override flutter_secure_storage_windows to 4.0.0 (win32 ^5.x compatible).
# Android target: Windows FFI code is never executed in production or in unit tests;
# this only affects Windows desktop support, which is out of scope. (STEP-43, RISK-0008)
dependency_overrides:
  flutter_secure_storage_windows: 4.0.0
```

### 3. Remove deprecated encryptedSharedPreferences

In `lib/core/security/secure_storage_service.dart`, find any usage of `encryptedSharedPreferences: true` in the `AndroidOptions` or similar and remove it. In v11, Android secure storage uses EncryptedSharedPreferences by default — the option was removed.

### 4. Verify

```powershell
flutter pub get
flutter analyze
```

Both should exit 0. `flutter analyze` will catch if any removed APIs are still referenced.

### 5. Commit

```powershell
git add pubspec.yaml pubspec.lock lib/core/security/secure_storage_service.dart
git commit -m "deps(STEP-43.6): upgrade flutter_secure_storage ^11.0.0, remove encryptedSharedPreferences, add win32 override"
git push
```

## Verification

- `flutter_secure_storage: ^11.0.0` in pubspec.yaml.
- `dependency_overrides` section has `flutter_secure_storage_windows: 4.0.0`.
- No reference to `encryptedSharedPreferences` in secure_storage_service.dart.
- `flutter pub get` exits 0.
- `flutter analyze` exits 0.

## Definition of done

- [ ] `flutter_secure_storage` upgraded to `^11.0.0`.
- [ ] `dependency_overrides` added for `flutter_secure_storage_windows: 4.0.0`.
- [ ] `encryptedSharedPreferences` removed from `secure_storage_service.dart`.
- [ ] `flutter pub get` and `flutter analyze` pass.
- [ ] Committed and pushed on `step-0043-flutter-upgrade`.

## Next

After committing, continue in the same chat to **substep 43.7**: `Upcoming Prompts/mine-flow-STEP-43.7-PROMPT.md`.
