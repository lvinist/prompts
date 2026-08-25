# mine-flow — STEP-43.9: go_router v17 Compatibility Check

> **How to run:** Tell your agent: **"Read and run `Upcoming Prompts/mine-flow-STEP-43.9-PROMPT.md`."**
> This substep is self-contained — executable cold in a fresh chat.
> **Assigned model:** Sonnet 4.6 Thinking

## Context

`go_router` jumped from `^15.1.2` to `^17.3.0` (two major versions). The v16 and v17 changelogs mention breaking changes to the observer API. This substep verifies that `lib/app/router.dart` doesn't use any removed APIs.

See: `Code/mine-flow-docs/reports/2026-08-13-flutter-dependency-ci-audit.md` — Section 3.1.

**Known state:**
- go_router already bumped to `^17.3.0` in substep 43.4.
- `flutter analyze` passed in 43.4 — but this substep does a focused review.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-43-PLAN.md`
- `.throughstone/local-user.md`
- `Code/mine-flow-app/lib/app/router.dart`

## Scope

**Own:** Review go_router v16/v17 breaking changes against the app's router code. Fix any issues. If no issues, document the verification.

**Do not:** Refactor routing. Add new routes.

## Your task

### 1. Review router.dart

Read `lib/app/router.dart` and check for:
- `GoRouter.observers` or `navigatorObservers` — this is the main v17 breaking change
- Any deprecated `GoRoute` constructor parameters
- `ShellRoute` or `StatefulShellRoute` API changes

### 2. Search for go_router imports

Search the entire codebase for `package:go_router/` imports and verify each usage.

### 3. Run verify

```powershell
flutter analyze
flutter test
```

If both pass with 0 issues and 0 failures, the migration is clean.

### 4. Commit (only if changes needed)

If changes were needed:
```powershell
git add -A
git commit -m "fix(STEP-43.9): adapt router.dart for go_router v17 breaking changes"
git push
```

If no changes needed, document this in the commit for 43.10.

## Verification

- `flutter analyze` exits 0.
- `flutter test` passes.
- No deprecated go_router APIs remain.

## Definition of done

- [ ] go_router v17 compatibility verified against router.dart.
- [ ] `flutter analyze` and `flutter test` pass.
- [ ] Any breaking changes resolved, or documented as clean migration.

## Next

After completing, start a fresh chat and run **substep 43.10**: `Upcoming Prompts/mine-flow-STEP-43.10-PROMPT.md`.
