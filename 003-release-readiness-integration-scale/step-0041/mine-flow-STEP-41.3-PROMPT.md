# mine-flow — STEP-41.3: Localization Compliance Baseline and Regression Guard

> **How to run:** Tell your agent: **"Read and run `Upcoming Prompts/mine-flow-STEP-41.3-PROMPT.md`."**
> Run only after 41.2 is committed. This substep is self-contained — executable cold in a fresh chat.

## Context

STEP-41 establishes a release-readiness baseline. Its PLAN is at `Upcoming Prompts/mine-flow-STEP-41-PLAN.md`.

`architecture/07-ui-design-system.md` requires Indonesian as the MVP default locale and all user-facing strings to route through a localization layer. The current state (confirmed by 41.1):

- **locale selection works** — `SettingsCubit` drives `MaterialApp.locale`, `supportedLocales: [en, id, en_US, id_ID]`, and Flutter global delegates are wired.
- **`AppLocalizations` does not exist** — no `l10n.yaml`, no `.arb` files, no generated `app_localizations.dart`. `pubspec.yaml` has `generate: true` and `intl: ^0.20.2` declared.
- **UI strings are hardcoded** — screens use `Text('Input Absensi')`, `Text('Pengaturan')`, etc. directly; no `AppLocalizations.of(context).someKey` call exists.

**Your job in 41.3 is to:**
1. Create the minimal Flutter l10n scaffold (`l10n.yaml`, baseline `.arb` files for Indonesian and English).
2. Wire the generated `AppLocalizations` delegate into `app.dart` without changing any existing string literals.
3. Create a deterministic regression guard that detects new hardcoded strings added to presentation files.
4. Write focused tests proving locale configuration and the guard's pass/fail behavior.

**This is not a full localization migration.** Existing hardcoded strings stay as-is. The scaffold creates the infrastructure so future work can migrate them screen-by-screen. The guard prevents new hardcoded strings from being silently added without registering them in the ARB catalog.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-41-PLAN.md`
- `Code/mine-flow-docs/reports/2026-08-03-step-0041-release-readiness-reconciliation.md` (updated by 41.1 and 41.2)
- `.throughstone/local-user.md`
- `Code/mine-flow-app/pubspec.yaml`
- `Code/mine-flow-app/lib/app/app.dart`
- `Code/mine-flow-app/README.md`
- `Code/mine-flow-docs/architecture/07-ui-design-system.md`
- `Code/mine-flow-docs/architecture/12-test-strategy.md`
- `Code/mine-flow-docs/coding-standards/dart.md`
- `Code/mine-flow-docs/registries/risks.yml`

## Scope

**Own:** `l10n.yaml`, baseline `app_id.arb`, `app_en.arb`, `lib/app/app.dart` delegate wiring, `tool/check_l10n_baseline.dart` guard, focused tests, CI addition, reconciliation report and Doc 07 updates.

**Do not:** Translate existing hardcoded strings. Change feature-screen UI behavior or copy. Add languages beyond Indonesian and English. Edit `DESIGN.md`, `PRODUCT.md`, or historical archived STEP artifacts. Bulk-search-and-replace `Text(...)` calls.

## Your task

### 1. Confirm worktree and read updated report

```bash
git status --short --branch   # Code/mine-flow-app — expect clean, step-0041-release-readiness-baseline
git status --short --branch   # Code/mine-flow-docs — expect clean, step-0041-release-readiness-baseline
```

Read the 41.2 section of the updated report to confirm the 41.1/41.2 evidence.

### 2. Check for l10n.yaml side effects before creating anything

The `pubspec.yaml` already has `generate: true`. Before creating `l10n.yaml`, run:

```bash
# From Code/mine-flow-app:
flutter pub get
flutter analyze
flutter test
```

Record the baseline (number of tests, any analyzer issues). This confirms the clean starting state 41.3 will modify.

> **Why:** Flutter's build system, when `generate: true` is present, watches for `l10n.yaml`. Creating it triggers code generation. You need to know the baseline before triggering generation so you can confirm 41.3 doesn't break anything.

### 3. Create the l10n scaffold

**3a. Create `l10n.yaml`** in `Code/mine-flow-app/`:

```yaml
# l10n.yaml — Flutter localization configuration.
# See: https://docs.flutter.dev/ui/accessibility-and-internationalization/internationalization
arb-dir: lib/l10n
template-arb-file: app_id.arb
output-localization-file: app_localizations.dart
output-class: AppLocalizations
nullable-getter: false
```

Notes:
- `template-arb-file: app_id.arb` makes Indonesian the template (authoritative source), matching Doc 07 which mandates Indonesian as the MVP default.
- `nullable-getter: false` — `AppLocalizations.of(context)!` throws if no delegate is in scope, which is the correct failure mode for a missing locale setup.

**3b. Create `Code/mine-flow-app/lib/l10n/app_id.arb`** (Indonesian — the template):

```json
{
  "@@locale": "id",
  "@@last_modified": "2026-08-06",
  "appTitle": "mine-flow",
  "@appTitle": {
    "description": "The name of the application."
  },
  "localizationBaseline": "Dasar Lokalisasi STEP-41",
  "@localizationBaseline": {
    "description": "A sentinel string used by the STEP-41 localization baseline guard. Not displayed to users."
  }
}
```

**3c. Create `Code/mine-flow-app/lib/l10n/app_en.arb`** (English — translation):

```json
{
  "@@locale": "en",
  "@@last_modified": "2026-08-06",
  "appTitle": "mine-flow",
  "localizationBaseline": "STEP-41 Localization Baseline"
}
```

> **Rationale for sentinel key:** `localizationBaseline` is a harmless sentinel that is never shown to users but proves the ARB-to-Dart generation pipeline works end-to-end. It is the minimum required to have a non-empty ARB that generates a real `AppLocalizations` class.

### 4. Run Flutter's l10n generator and verify

```bash
# From Code/mine-flow-app:
flutter gen-l10n
```

This should create `.dart_tool/flutter_gen/gen_l10n/app_localizations.dart` (or similar — the exact output path depends on `output-localization-file` and Flutter version). Confirm the generated file contains both `appTitle` and `localizationBaseline` getters.

> **If `flutter gen-l10n` is not a standalone command in Flutter 3.44.x:** Use `flutter pub get` which triggers generation when `l10n.yaml` and `pubspec.yaml generate: true` are both present. Check `.dart_tool/` for generated files.

Record the exact command that triggers generation and the exact output path.

### 5. Wire the generated delegate into app.dart

Open `Code/mine-flow-app/lib/app/app.dart`. Add the `AppLocalizations.delegate` to `localizationsDelegates`:

```dart
// Add this import at the top:
import 'package:flutter_localizations/flutter_localizations.dart';
// The generated delegate import — adjust path based on actual generated output:
import 'package:mine_flow/l10n/app_localizations.dart';  // or the actual generated path

// In MaterialApp.router's localizationsDelegates:
localizationsDelegates: const [
  AppLocalizations.delegate,          // ← ADD THIS FIRST
  GlobalMaterialLocalizations.delegate,
  GlobalWidgetsLocalizations.delegate,
  GlobalCupertinoLocalizations.delegate,
],
```

> **Important:** Do not change any other part of `app.dart`. The `supportedLocales` list already covers both `en` and `id` — leave it exactly as it is. Do not add `AppLocalizations.supportedLocales` as it may conflict with the explicit list.

After this change:
```bash
flutter analyze
flutter pub get
```

The app must compile cleanly. If the generated delegate import path does not match, inspect the actual generated file path and use the correct import. **Do not add the import as a raw relative path — use the package: prefix.**

### 6. Create `Code/mine-flow-app/tool/check_l10n_baseline.dart`:

```dart
// ignore_for_file: avoid_print
/// Localization regression guard for mine-flow.
///
/// Scans Flutter presentation/app Dart files for hardcoded user-facing
/// string patterns (Text('...') and similar) not found in the ARB catalog.
///
/// Strategy: baseline-manifest model. The known list of files with
/// legacy hardcoded strings is recorded in [_legacyExemptFiles]. New
/// files NOT in this list are scanned. Any [Text('...')] usage in a
/// non-exempt file causes a CI failure.
///
/// MAINTENANCE: When a file is migrated to AppLocalizations, remove it
/// from [_legacyExemptFiles]. When a new presentation file is added,
/// it must use AppLocalizations from day one — it will not be auto-exempt.
///
/// Run: dart run tool/check_l10n_baseline.dart
import 'dart:io';

/// Files that currently have legacy hardcoded strings and are explicitly
/// exempted from the guard until they are migrated in a future STEP.
///
/// IMPORTANT: Before committing, generate the actual list by running:
///   dart run tool/generate_l10n_exempt_list.dart
/// or by running the scan manually (see STEP-41.3 prompt, task 6).
/// This list must be COMPLETE — any non-exempt file with a Text('...')
/// literal will cause CI to fail immediately.
///
/// TODO(STEP-??): All files in this list need AppLocalizations migration.
/// Remove each file when it is migrated.
const List<String> _legacyExemptFiles = [
  // *** REPLACE THIS WITH THE OUTPUT OF THE SCAN DESCRIBED IN TASK 6a ***
  // Run: find lib -name '*.dart' -path '*/presentation/*' | sort
  // Then for each file, check if it uses Text('...') with a literal string.
  // Every file that does must be listed here.
];

/// Pattern that detects Text('...') or Text("...") usage — a proxy
/// for hardcoded user-facing strings.
///
/// Excluded by design:
/// - Empty strings: Text('') — not user-facing copy
/// - Identifiers: Text(someVariable) — variable, not literal  
/// - Strings shorter than 2 chars — not meaningful copy
/// - Comment lines
final _hardcodedTextPattern = RegExp(r"Text\s*\(\s*['\"][^'\"]{2,}['\"]");

void main() {
  print('Localization Baseline Guard');
  print('---------------------------');

  final presentationDirs = [
    'lib/app/presentation',
    'lib/features',
  ];

  final violations = <String>[];
  int filesScanned = 0;
  int filesExempt = 0;

  for (final dirPath in presentationDirs) {
    final dir = Directory(dirPath);
    if (!dir.existsSync()) continue;

    for (final entity in dir.listSync(recursive: true)) {
      if (entity is! File) continue;
      final path = entity.path.replaceAll(r'\', '/');
      if (!path.endsWith('.dart')) continue;

      // Only check presentation-layer files (pages + widgets, not blocs)
      final isPresentation = path.contains('/presentation/pages/') ||
          path.contains('/presentation/widgets/') ||
          path.contains('/app/presentation/pages/') ||
          path.contains('/app/presentation/widgets/');
      if (!isPresentation) continue;

      // Skip exempt (legacy) files
      final isExempt = _legacyExemptFiles.any(
        (exempt) => path.endsWith(exempt) || path.contains(exempt),
      );
      if (isExempt) {
        filesExempt++;
        continue;
      }

      filesScanned++;
      final content = entity.readAsStringSync();
      final lines = content.split('\n');
      for (var i = 0; i < lines.length; i++) {
        final line = lines[i];
        // Skip comment lines
        if (line.trimLeft().startsWith('//')) continue;
        if (_hardcodedTextPattern.hasMatch(line)) {
          violations.add('$path:${i + 1}  ${line.trim()}');
        }
      }
    }
  }

  print('Files scanned (non-exempt): $filesScanned');
  print('Files exempt (legacy):      $filesExempt');
  print('');

  if (violations.isEmpty) {
    print('[OK] No new hardcoded strings detected in non-exempt files.');
    exit(0);
  }

  print('[ERROR] Hardcoded string literals found in non-exempt files:');
  for (final v in violations) {
    print('  $v');
  }
  print('');
  print('To fix: use AppLocalizations.of(context).yourKey instead of Text(\'...\').');
  print('If this file must remain legacy temporarily, add it to _legacyExemptFiles');
  print('in tool/check_l10n_baseline.dart with a TODO referencing the migration STEP.');
  exit(1);
}
```

> **Critical step before using the guard:** The `_legacyExemptFiles` list in the script above starts empty. You must populate it with the actual list of files that currently use `Text('...')` with a literal string. Use this process:
>
> **6a. Scan for actual violating files:**
> ```bash
> # From Code/mine-flow-app — find all presentation page/widget files:
> find lib -name '*.dart' \( -path '*/presentation/pages/*' -o -path '*/presentation/widgets/*' \) | sort
> ```
>
> For each file in the output, check if it contains `Text('...')` patterns (you can read each file or run a targeted search). Every file that does must be added to `_legacyExemptFiles`. Files that only use variables (`Text(someVar)`) do not need to be exempted.
>
> **6b. Add all violating files to `_legacyExemptFiles`.** The `lib/` prefix should match what `entity.path` returns — verify by running the guard and checking its output. The guard will report any file it finds that isn't exempt, so you can iterate: run the guard, add the reported files to the exempt list, repeat until the guard exits 0 with a plausible exempt count.
>
> **6c. Verify the guard passes:**

After populating the exempt list and creating the file, run:
```bash
dart run tool/check_l10n_baseline.dart
```

Expected: `[OK] No new hardcoded strings detected in non-exempt files.`


### 7. Add the l10n guard to CI

Open `Code/mine-flow-app/.github/workflows/ci.yml`. Add a `Check Localization Baseline` step **after** `Check Supabase Contract` and **before** `Check formatting`:

```yaml
      - name: Check Localization Baseline
        run: dart run tool/check_l10n_baseline.dart
```

Ensure the step uses no secrets and no environment variables.

### 8. Write focused tests

Create `Code/mine-flow-app/test/app/locale_configuration_test.dart`:

```dart
/// Tests for the locale and localization configuration of [MineFlowApp].
///
/// Verifies:
/// 1. [SettingsCubit] correctly drives the app locale.
/// 2. The [AppLocalizations] delegate resolves both 'id' and 'en' locales.
/// 3. The sentinel baseline key is accessible via [AppLocalizations].
library;

import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mine_flow/l10n/app_localizations.dart';  // Adjust import if needed

void main() {
  group('AppLocalizations delegate', () {
    test('supports Indonesian locale', () async {
      final delegate = AppLocalizations.delegate;
      expect(await delegate.load(const Locale('id')), isNotNull);
    });

    test('supports English locale', () async {
      final delegate = AppLocalizations.delegate;
      expect(await delegate.load(const Locale('en')), isNotNull);
    });

    testWidgets('resolves baseline sentinel key in Indonesian', (tester) async {
      late AppLocalizations l10n;
      await tester.pumpWidget(
        MaterialApp(
          locale: const Locale('id'),
          supportedLocales: const [Locale('id'), Locale('en')],
          localizationsDelegates: const [
            AppLocalizations.delegate,
            GlobalMaterialLocalizations.delegate,
            GlobalWidgetsLocalizations.delegate,
          ],
          home: Builder(builder: (context) {
            l10n = AppLocalizations.of(context)!;
            return const SizedBox();
          }),
        ),
      );
      await tester.pumpAndSettle();
      expect(l10n.localizationBaseline, isNotEmpty);
      expect(l10n.appTitle, 'mine-flow');
    });

    testWidgets('resolves baseline sentinel key in English', (tester) async {
      late AppLocalizations l10n;
      await tester.pumpWidget(
        MaterialApp(
          locale: const Locale('en'),
          supportedLocales: const [Locale('id'), Locale('en')],
          localizationsDelegates: const [
            AppLocalizations.delegate,
            GlobalMaterialLocalizations.delegate,
            GlobalWidgetsLocalizations.delegate,
          ],
          home: Builder(builder: (context) {
            l10n = AppLocalizations.of(context)!;
            return const SizedBox();
          }),
        ),
      );
      await tester.pumpAndSettle();
      expect(l10n.localizationBaseline, isNotEmpty);
      expect(l10n.appTitle, 'mine-flow');
    });
  });
}
```

Also create `Code/mine-flow-app/test/tool/check_l10n_baseline_test.dart`:

```dart
/// Tests for the l10n baseline guard (tool/check_l10n_baseline.dart).
///
/// Runs the guard as a subprocess to verify its pass and fail behavior.
/// Requires a clean git worktree in Code/mine-flow-app.
library;

import 'dart:io';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('check_l10n_baseline guard', () {
    test('passes with the current codebase (all new violations exempt)', () async {
      final result = await Process.run(
        'dart',
        ['run', 'tool/check_l10n_baseline.dart'],
        workingDirectory: Directory.current.path,
      );
      expect(result.exitCode, 0,
          reason: 'Guard should pass when no non-exempt violations exist.\n'
              'stdout: ${result.stdout}\nstderr: ${result.stderr}');
      expect(result.stdout.toString(), contains('[OK]'));
    });

    test('fails when a non-exempt presentation file has a hardcoded string', () async {
      // Create a temporary non-exempt presentation file with a hardcoded string.
      final tempDir = Directory('lib/features/_test_l10n_guard_temp_/presentation/pages');
      final tempFile = File('${tempDir.path}/temp_screen.dart');
      try {
        tempDir.createSync(recursive: true);
        tempFile.writeAsStringSync('''
import 'package:flutter/material.dart';

class TempScreen extends StatelessWidget {
  const TempScreen({super.key});
  @override
  Widget build(BuildContext context) {
    return Text('Hardcoded String That Should Fail');
  }
}
''');

        final result = await Process.run(
          'dart',
          ['run', 'tool/check_l10n_baseline.dart'],
          workingDirectory: Directory.current.path,
        );
        expect(result.exitCode, 1,
            reason: 'Guard should fail when a non-exempt file has hardcoded strings.\n'
                'stdout: ${result.stdout}');
        expect(result.stdout.toString(), contains('[ERROR]'));
        expect(result.stdout.toString(), contains('temp_screen.dart'));
      } finally {
        // Always clean up, even if assertion fails.
        if (tempDir.existsSync()) tempDir.deleteSync(recursive: true);
      }
    });
  });
}
```

### 9. Run all checks

```bash
# From Code/mine-flow-app:
flutter pub get
flutter gen-l10n          # or let pub get trigger it; verify generated files exist
dart format --output=none --set-exit-if-changed lib/ test/
flutter analyze
flutter test test/app/locale_configuration_test.dart
flutter test test/tool/check_l10n_baseline_test.dart
flutter test              # full suite — confirm no regressions
git diff --check
```

Record all results. If `flutter test` introduces new failures unrelated to 41.3, document them as pre-existing and do not fix them in this substep.

### 10. Update Doc 07 and reconciliation report

**Doc 07 (`architecture/07-ui-design-system.md`):**
- Find the localization section. Update to reflect the current truth: locale selection works; `AppLocalizations` delegate now exists as a minimal scaffold at `lib/l10n/`; full screen-by-screen migration remains incomplete.
- Add a version log entry: `v1.x → STEP-41.3: Established minimal l10n scaffold (l10n.yaml, ARB baseline, AppLocalizations delegate). Full string migration deferred to a future STEP.`

**Reconciliation report:**
- Add a **41.3 Verification** section with:
  - `l10n.yaml` created: yes, path given.
  - ARB files created: `app_id.arb`, `app_en.arb`, keys listed.
  - `AppLocalizations` wired into `app.dart`: yes.
  - Guard `tool/check_l10n_baseline.dart`: created, passing-condition result, failing-condition result.
  - CI step added: yes, name given.
  - Tests: `locale_configuration_test.dart` (N tests), `check_l10n_baseline_test.dart` (2 tests).
  - Full test suite result after 41.3 changes.
  - Update localization matrix row to: **Partially evidenced** — scaffold exists; full migration incomplete; guard prevents regressions in new files.

**`registries/risks.yml`:**
Add a row (to be finalized in 41.4):
```yaml
- id: RISK-XXXX    # use next available number
  title: "Full Indonesian localization migration incomplete"
  severity: medium
  owner: TBD
  description: >
    All user-facing strings in presentation files are currently hardcoded
    (Indonesian/English). The AppLocalizations scaffold (STEP-41.3) provides
    the infrastructure and prevents new regressions in non-exempt files, but
    the ~35 legacy presentation files remain on the exempt list.
    Must be resolved before a public multi-language release.
  revisit_trigger: "Before any public multi-language release or when a new screen is added."
  source: "Code/mine-flow-docs/reports/2026-08-03-step-0041-release-readiness-reconciliation.md"
```

### 11. Commit

Commit all changes on `step-0041-release-readiness-baseline`:
- `Code/mine-flow-app`: `l10n.yaml`, `lib/l10n/app_id.arb`, `lib/l10n/app_en.arb`, updated `lib/app/app.dart`, `tool/check_l10n_baseline.dart`, `test/app/locale_configuration_test.dart`, `test/tool/check_l10n_baseline_test.dart`, updated `ci.yml`.
- `Code/mine-flow-docs`: updated `architecture/07-ui-design-system.md`, updated reconciliation report, updated `registries/risks.yml`.

Use a commit message like: `feat(STEP-41.3): establish l10n scaffold, baseline guard, and AppLocalizations delegate`.

## Verification

- `flutter gen-l10n` (or `flutter pub get`) generates `AppLocalizations` without errors.
- `flutter analyze` reports 0 issues.
- `dart format` reports 0 changes needed.
- `flutter test test/app/locale_configuration_test.dart` — all 4 tests pass.
- `flutter test test/tool/check_l10n_baseline_test.dart` — both tests pass.
- `flutter test` (full suite) — same count as before 41.3 (or higher if new tests added), no new failures.
- `dart run tool/check_l10n_baseline.dart` exits 0.
- `git diff --check` clean in both repos.
- Worktrees clean (no temp files, no untracked generated files that should be gitignored).

> **Gitignore check:** Flutter's build system generates files in `.dart_tool/flutter_gen/`. Verify these are already gitignored (Flutter's default `.gitignore` should cover `.dart_tool/`). The `lib/l10n/` ARB source files and the generated `app_localizations.dart` (if output to `lib/`) **should be committed**. Verify by running `git status` and confirming the right files appear.

## Keeping the docs true

Doc 07 must reflect the actual localization posture after this substep. The prior claim that all strings route through a localization layer was aspirational — update it to be accurate. The version log entry makes the history traceable. Do not downgrade the requirement (it must still say full migration is required), but state the current implementation truth.

## Definition of done

- [ ] `l10n.yaml`, `lib/l10n/app_id.arb`, `lib/l10n/app_en.arb` created and committed.
- [ ] `AppLocalizations.delegate` wired into `app.dart`; app compiles and analyzes cleanly.
- [ ] `tool/check_l10n_baseline.dart` passes with the actual codebase and fails with the intentional temp-file fixture.
- [ ] CI has a `Check Localization Baseline` step; no secrets required.
- [ ] `locale_configuration_test.dart` (4 tests) and `check_l10n_baseline_test.dart` (2 tests) pass.
- [ ] Full `flutter test` suite passes with no new failures.
- [ ] Doc 07 version log updated; reconciliation report has 41.3 section; risks.yml has l10n migration risk row.
- [ ] Changes committed on `step-0041-release-readiness-baseline`; worktrees clean.

## Next

After committing, start a fresh chat and run **substep 41.4**: `Upcoming Prompts/mine-flow-STEP-41.4-PROMPT.md`.
