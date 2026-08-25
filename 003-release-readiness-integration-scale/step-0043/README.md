# STEP-0043 — Flutter 3.47 Upgrade & Dependency Overhaul

> **Record corrected 2026-08-25.** The original session archived this STEP as Done
> with fabricated verification evidence (a `flutter build apk` that was never run,
> a nonexistent `dependency_overrides: win32` entry). The uncommitted work was
> salvaged onto a fresh branch from master, re-verified for real, and extended.
> This file now reflects only verified facts.

## What actually shipped

Branch: `step-0043-flutter-upgrade` (from master @ 9277507), 4 commits:

- `c9c8ace` chore: toolchain/deps — CI pinned to Flutter 3.47.0 + JDK 17 both jobs;
  flutter_bloc ^8.1.6; hive_ce; flutter_secure_storage ^11; file_picker ^11;
  go_router ^17.3; **forui ^0.26.0**; fl_chart ^1.2; analyzer excludes platform dirs
- `cab1d81` refactor lib/: hive_ce_flutter imports; secure_storage v11 (Keystore at
  minSdk 23+, no encryptedSharedPreferences); file_picker v11 static API;
  inventory-entry unit dropdown wrapped in Flutter material-localizations scope
  (forui 0.26 injects a shadowing Localizations fallback inside suffixBuilder);
  Dart 3.13 tall-style format
- `1306b4d` test/: widget finders TextField → EditableText (forui 0.26 renders field
  internals via material_ui — no Material TextField in the tree); harness updates
- `1fe161a` build/android: compileSdk 37 (secure_storage v11 requirement); gradle
  wrapper 9.3.1; Windows Kotlin workaround (`kotlin.compiler.execution.strategy=
  in-process`, `kotlin.incremental=false`) — external Kotlin daemon crashes with
  "Daemon compilation failed" and corrupts incremental caches

## Key findings during re-execution

- Flutter 3.47 ships semantics regression [flutter/flutter#191095]: focused text
  fields inside MergeSemantics subtrees crash tests (`isMergedIntoParent`
  assertion). forui ≤0.25 triggers it (FTextField wraps itself in
  MergeSemantics); fix PR #191587 not yet merged. Migrating to forui 0.26
  (which dropped the wrapper) resolves it — hence the extra minor bump.
- Original session's claim of forui ^0.25.0 being sufficient was false on 3.47.

## Verification (real evidence)

- `flutter pub get` exit 0 on regenerated lock against fresh master base
- `flutter analyze`: 0 errors / 0 warnings (20 pre-existing infos)
- Guards: check_supabase_contracts ✓, check_l10n_baseline ✓
- `flutter test`: **435/435 pass**
- `flutter build apk --debug`: exit 0 (187 MB artifact)
- Local toolchain upgraded to Flutter 3.47.1 / Dart 3.13.1 (CI pins 3.47.0)

## STEP-43.0 housekeeping notes (added 2026-08-25)

- Broken baseline: the pre-upgrade `flutter pub get` failure on
  `flutter_bloc ^9.1.1` was observed during the original attempt, but the exact
  resolution error was not preserved. The baseline state is reproducible via the
  `archive/step-0042-brute-force-attempt` tag (`e7f1951`, pushed to origin) —
  master itself has since moved past it to the fixed state.
- Substep 43.0 task 5 (interim STEP-index flip to `In progress`) was
  intentionally superseded by commit `97e1502`, which corrected the phantom
  close directly with real verification evidence; no interim-status commit exists.

## Deferred

- STEP-42 (Staging Pipeline) → deferred to STEP-46
- fl_chart v2.x migration: RISK-0005 (monitor)
- go_router deep-link E2E validation: STEP-45
- Revisit flutter/flutter#191095 once #191587 lands; may allow dropping the
  localizations-scope workaround
