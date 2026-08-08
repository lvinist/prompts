# mine-flow — STEP-41.5: Audit Fix — Guard Correctness & CI Hardening

> **How to run:** Tell your agent: **"Read and run `Upcoming Prompts/mine-flow-STEP-41.5-PROMPT.md`."**
> Run only after 41.1 – 41.4 are all committed and `prompts/STEP-index.md` shows all four substeps as Done.
> This substep is self-contained — executable cold in a fresh chat.

## Context

A post-implementation audit (2026-08-08, Antigravity / Claude Sonnet 4.6 Thinking) identified the following
actionable issues in the STEP-41 artifacts. These are **correctness and robustness fixes only** — no new
features, no scope expansion.

**Blocking fix (ISSUE-4):**
The regex in `tool/check_l10n_baseline.dart` (line 71) does **not** match
`Text("double-quoted string")`. A developer who writes `Text("Laporan Harian")` in a new, non-exempt
presentation file passes the guard silently. The guard is therefore incomplete as a correctness gate.

**Robustness fixes (ISSUE-8, ISSUE-1, ISSUE-5, ISSUE-6):**
- `ci.yml` checkout step uses default `fetch-depth: 1`, which can make `git diff HEAD^` fail for a
  single-commit push — the guard's CI fallback branch becomes unreliable (ISSUE-8).
- `tool/check_supabase_contracts.dart` line 29 uses `line.length > 3` as a fragile `git status
  --porcelain` parser. A two-character file path or a line with unusual whitespace can be silently skipped
  (ISSUE-1).
- `tool/check_l10n_baseline.dart` line 104 uses `path.contains(exempt)` which can false-exempt a file
  whose path merely *contains* a known exempt filename (ISSUE-5).
- `tool/check_l10n_baseline.dart` line 25 references `tool/generate_l10n_exempt_list.dart`, a script
  that does not exist in the repository (ISSUE-6).

**Out of scope for this substep** (accepted, documented, and tracked elsewhere):
- ISSUE-2: committed-but-unpushed migration gap — accepted gap, STEP-42 scope.
- ISSUE-3: fully mitigated by ISSUE-8 fix.
- ISSUE-7: CI-mode contract test coverage — low-priority research spike, not blocking STEP-42.
- ISSUE-9: `STAGING_*` secrets absent — blocked on STEP-42 by design.
- ISSUE-10: Doc 07 note about localization scaffold — record in this report; fix if trivially true, skip
  if it would require re-opening the architecture session.

## Read these first

Before starting, read silently (do not summarize):
- `.throughstone/local-user.md`
- `Code/mine-flow-docs/AGENTS.md` → `Code/mine-flow-docs/METHOD.md` §§1, 6, 10
- `prompts/STEP-index.md` (confirm STEP-41 substeps 41.1–41.4 are all `Done`)
- `Code/mine-flow-app/tool/check_l10n_baseline.dart`
- `Code/mine-flow-app/tool/check_supabase_contracts.dart`
- `Code/mine-flow-app/.github/workflows/ci.yml`
- `Code/mine-flow-app/test/tool/check_l10n_baseline_test.dart`
- `Code/mine-flow-app/test/tool/check_supabase_contracts_test.dart`
- `Code/mine-flow-docs/reports/2026-08-03-step-0041-release-readiness-reconciliation.md`
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` (§§4–6 — localization requirements)

## Scope

**Own:**
- `tool/check_l10n_baseline.dart` — regex fix, `contains` → `endsWith` fix, remove ghost script reference.
- `tool/check_supabase_contracts.dart` — porcelain parser hardening.
- `.github/workflows/ci.yml` — add `fetch-depth: 2` to the `Checkout` step.
- `test/tool/check_l10n_baseline_test.dart` — add a double-quote fixture test case.
- `Code/mine-flow-docs/reports/2026-08-03-step-0041-release-readiness-reconciliation.md` — append
  a STEP-41.5 closure section.
- `prompts/STEP-index.md` — add substep 41.5 row, mark Done.

**Do not:**
- Add new packages or dependencies.
- Rewrite or restructure the tools beyond the named fixes.
- Alter the `_legacyExemptFiles` list (adding or removing entries is a future localization migration STEP).
- Change any test that was previously passing unrelated to these guards.
- Provision staging, run remote Supabase commands, or read `.env`.
- Alter architecture docs or ADRs unless ISSUE-10 can be resolved with a single sentence addition
  (see task 8 below).

---

## Your task

### 1. Confirm worktree state

```powershell
# Code/mine-flow-app — expect: step-0041-release-readiness-baseline, clean worktree
git status --short --branch
git log --oneline -6

# Code/mine-flow-docs — expect: step-0041-release-readiness-baseline, clean worktree
git status --short --branch
git log --oneline -4
```

If either repo has uncommitted changes unrelated to this substep, document them and do not touch them.

---

### 2. Fix ISSUE-4 — l10n guard regex (BLOCKING)

**File:** `Code/mine-flow-app/tool/check_l10n_baseline.dart`

**Problem:** The current regex does not match `Text("double-quoted string")`. Due to the way the
pattern is constructed, the character class `[^'"]` excludes both single and double quotes, making
it impossible for the double-quote alternate to match the string content.

**Fix:** Replace the single regex declaration with two alternating patterns joined by `|`, one for
each quote style. Update the field and its docstring:

```dart
/// Pattern that detects hardcoded user-facing string literals in Text() calls.
/// Matches both single-quoted and double-quoted forms:
///   Text('some label')  — single-quote form
///   Text("some label")  — double-quote form
///
/// Excluded by design:
/// - Strings shorter than 2 chars — not meaningful copy.
/// - Empty strings: Text('') or Text("") — not user-facing copy.
/// - Variables: Text(someVar) — no surrounding quote characters.
/// - Comment lines (filtered separately before matching).
final _hardcodedTextPattern = RegExp(
  r"""Text\s*\(\s*'[^']{2,}'|Text\s*\(\s*"[^"]{2,}"""",
);
```

Verify the fix mentally before writing:
- `Text('Input Absensi')` → matches single-quote branch ✓
- `Text("Laporan Harian")` → matches double-quote branch ✓
- `Text('')` and `Text("")` → no match (zero-length content) ✓
- `Text(someVariable)` → no match (no quote characters) ✓
- `Text('ab')` → matches (`{2,}` means 2 or more) ✓ — preserve the original minimum.

After editing, run `dart run tool/check_l10n_baseline.dart` from `Code/mine-flow-app/` and confirm
exit code 0 (all current violations are in the known exempt list).

---

### 3. Fix ISSUE-5 — exempt path matching (`contains` → `endsWith`)

**File:** `Code/mine-flow-app/tool/check_l10n_baseline.dart`

**Problem:** The `isExempt` check uses `path.endsWith(exempt) || path.contains(exempt)`. The
`contains` branch can false-exempt a file whose path merely contains a known exempt filename as a
substring (e.g., `login_page.dart_backup.dart` would match the `login_page.dart` exempt entry).

**Fix:** Remove the `|| path.contains(exempt)` branch:

```dart
final isExempt = _legacyExemptFiles.any(
  (exempt) => path.endsWith(exempt),
);
```

`endsWith` is sufficient because `_legacyExemptFiles` entries are relative paths
(`lib/features/.../login_page.dart`) and the scanned `path` is a workspace-relative path —
`endsWith` gives an exact suffix match.

---

### 4. Fix ISSUE-6 — remove ghost script reference

**File:** `Code/mine-flow-app/tool/check_l10n_baseline.dart`

**Problem:** The doc comment above `_legacyExemptFiles` references
`dart run tool/generate_l10n_exempt_list.dart`, a script that does not exist in the repository.

**Fix:** Replace the inaccurate comment block with accurate maintenance instructions:

```dart
/// IMPORTANT: This list must be COMPLETE and accurate.
/// To discover which presentation files currently have hardcoded Text() literals, run:
///   dart run tool/check_l10n_baseline.dart
/// and read its [ERROR] output — those files need to be added here (temporarily)
/// or migrated to AppLocalizations.
///
/// When migrating a file to AppLocalizations, remove it from this list.
/// When adding a NEW presentation file, do NOT add it here — use AppLocalizations
/// from day one so it is enforced by this guard immediately.
///
/// TODO: All files in this list need AppLocalizations migration.
/// Remove each file when it is migrated. Tracked in RISK-0004.
```

---

### 5. Fix ISSUE-1 — harden porcelain parser in contract guard

**File:** `Code/mine-flow-app/tool/check_supabase_contracts.dart`

**Problem:** The local-mode loop uses `if (line.length > 3)` to filter blank lines from
`git status --porcelain` output. This is a fragile heuristic — it guards against empty lines
but does so with an arbitrary length check rather than explicit intent, and misses the
`.trim()` needed for Windows CRLF line endings.

**Fix:** Replace the length guard with an explicit minimum length check and extract the path
with `.trim()`:

```dart
for (var line in statusOutput.split('\n')) {
  // Porcelain v1 format: "XY path"
  // XY = 2-char status code, index 2 = space, path starts at index 3.
  // Skip blank lines (trailing newline or empty output).
  if (line.length < 4) continue;
  final path = line.substring(3).trim().replaceAll('\\', '/');
  if (path.startsWith(migrationsDirPath)) migUncommitted = true;
  if (path.startsWith(generatedFilePath)) typeUncommitted = true;
}
```

The `.trim()` on the extracted path also handles Windows CRLF line endings.

---

### 6. Fix ISSUE-8 — add `fetch-depth: 2` to CI checkout

**File:** `Code/mine-flow-app/.github/workflows/ci.yml`

**Problem:** The `Checkout` step in the `test` job uses `actions/checkout@v4` with no
`fetch-depth`, defaulting to `fetch-depth: 1` (shallow clone with only the latest commit).
The Supabase contract guard falls back to `git diff HEAD^` when `GITHUB_BASE_REF` is
not set (e.g., direct pushes to a branch). With only 1 commit in the clone, `HEAD^` does not
exist and the `git diff` command fails.

**Fix:** Add `fetch-depth: 2` to the `test` job's `Checkout` step only:

```yaml
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 2
```

The `build-android` job does not invoke the contract guard, so its `Checkout` step does not
require this change. Leave it unchanged (default `fetch-depth: 1`).

---

### 7. Update `check_l10n_baseline_test.dart` — add double-quote fixture test

**File:** `Code/mine-flow-app/test/tool/check_l10n_baseline_test.dart`

Add a third test case inside the `check_l10n_baseline guard` group immediately after the
existing failing-string test. This proves ISSUE-4 is resolved:

```dart
test('fails when a non-exempt file has a double-quoted hardcoded string', () async {
  final tempDir = Directory(
    'lib/features/_test_l10n_guard_temp_dq_/presentation/pages',
  );
  final tempFile = File('${tempDir.path}/temp_dq_screen.dart');
  try {
    tempDir.createSync(recursive: true);
    tempFile.writeAsStringSync('''
import 'package:flutter/material.dart';

class TempDqScreen extends StatelessWidget {
  const TempDqScreen({super.key});
  @override
  Widget build(BuildContext context) {
    return Text("Double Quoted Hardcoded String");
  }
}
''');
    final result = await Process.run(
      'dart',
      ['run', 'tool/check_l10n_baseline.dart'],
      workingDirectory: Directory.current.path,
      runInShell: true,
    );
    expect(result.exitCode, 1,
        reason: 'Guard should fail for double-quoted hardcoded strings.\n'
            'stdout: ${result.stdout}');
    expect(result.stdout.toString(), contains('[ERROR]'));
    expect(result.stdout.toString(), contains('temp_dq_screen.dart'));
  } finally {
    if (tempDir.existsSync()) tempDir.deleteSync(recursive: true);
  }
});
```

---

### 8. Handle ISSUE-10 (Doc 07 localization note) — narrow fix only

Open `Code/mine-flow-docs/architecture/07-ui-design-system.md`. Locate §§4–6 (localization
requirement section).

If you can add the following note without restructuring the section or re-opening the
architecture session, add it as a block quote immediately after the localization requirement
statement:

```markdown
> **Phase 3 status (STEP-41.3):** The `AppLocalizations` scaffold (`l10n.yaml`, baseline ARB
> files, generated delegate) was established. Full migration of the ~27 legacy presentation
> files is tracked as RISK-0004 and must be completed before a public multi-language release.
```

If adding this note would require restructuring the section significantly, **skip it** and
record "ISSUE-10 deferred" in the report with the reason. Do not force-fit it.

If you do add the note, bump the doc's Version Log:
`vX.Y → STEP-41.5: Added Phase 3 localization scaffold status note (ISSUE-10 audit fix).`

---

### 9. Run the full verification gate

From `Code/mine-flow-app/`, run each command and record actual exit code and summary:

```powershell
# 1. Dependencies
flutter pub get

# 2. Formatting — includes tool/ directory this time
dart format --output=none --set-exit-if-changed lib/ test/ tool/

# 3. Static analysis
flutter analyze

# 4. Contract guard
dart run tool/check_supabase_contracts.dart

# 5. l10n guard
dart run tool/check_l10n_baseline.dart

# 6. Focused guard tests
flutter test test/tool/check_l10n_baseline_test.dart --reporter=compact
flutter test test/tool/check_supabase_contracts_test.dart --reporter=compact

# 7. Full test suite
flutter test --reporter=compact 2>&1 | tail -3
```

**Acceptance criteria:**
- All commands exit 0.
- `check_l10n_baseline_test.dart`: **3 tests** passing (was 2).
- `check_supabase_contracts_test.dart`: **3 tests** passing (unchanged).
- Full suite: ≥ 433 tests (STEP-41.4 baseline); zero new failures.

If `flutter analyze` flags issues introduced by this substep, fix them before committing.
Pre-existing issues from before STEP-41.5 must be documented, not fixed here.

---

### 10. Update the reconciliation report

Append a **STEP-41.5 Audit Fix — Closure** section to
`Code/mine-flow-docs/reports/2026-08-03-step-0041-release-readiness-reconciliation.md`:

```markdown
## STEP-41.5 Audit Fix — Closure

**Date:** YYYY-MM-DD
**Audit source:** Post-implementation audit, Antigravity (Claude Sonnet 4.6 Thinking), 2026-08-08.

### Fixes applied

| Issue ID | Severity | File | Fix applied |
|----------|----------|------|-------------|
| ISSUE-4  | High     | `tool/check_l10n_baseline.dart`        | Regex rewritten as two alternates; double-quoted `Text("…")` now detected |
| ISSUE-5  | Low      | `tool/check_l10n_baseline.dart`        | `path.contains(exempt)` removed; `endsWith` only |
| ISSUE-6  | Low      | `tool/check_l10n_baseline.dart`        | Ghost script reference replaced with accurate maintenance instructions |
| ISSUE-1  | Low      | `tool/check_supabase_contracts.dart`   | Porcelain parser hardened: `length < 4` guard + `.trim()` on extracted path |
| ISSUE-8  | Medium   | `.github/workflows/ci.yml`             | `fetch-depth: 2` added to `test` job `Checkout` step |

### Issues not fixed (accepted / deferred)

| Issue ID | Reason |
|----------|--------|
| ISSUE-2 | Accepted gap: committed-but-unpushed migration changes not caught. Tracked in report; STEP-42 scope. |
| ISSUE-3 | Resolved transitively by ISSUE-8 fix. |
| ISSUE-7 | CI-mode contract test coverage: low priority, not blocking. Deferred. |
| ISSUE-9 | `STAGING_*` secrets absent by design; STEP-42 provisions them. |
| ISSUE-10 | [State: resolved with note in Doc 07 § / deferred — reason] |

### 41.5 Verification gate

| Command | Working Dir | Exit Code | Result Summary |
|---------|-------------|-----------|----------------|
| `flutter pub get` | `Code/mine-flow-app` | 0 | — |
| `dart format --output=none ... lib/ test/ tool/` | `Code/mine-flow-app` | 0 | No issues |
| `flutter analyze` | `Code/mine-flow-app` | 0 | 0 issues |
| `dart run tool/check_supabase_contracts.dart` | `Code/mine-flow-app` | 0 | WARNING + bypass |
| `dart run tool/check_l10n_baseline.dart` | `Code/mine-flow-app` | 0 | OK |
| `flutter test test/tool/check_l10n_baseline_test.dart` | `Code/mine-flow-app` | 0 | 3 tests |
| `flutter test test/tool/check_supabase_contracts_test.dart` | `Code/mine-flow-app` | 0 | 3 tests |
| `flutter test` (full suite) | `Code/mine-flow-app` | 0 | N tests, 0 failures |
```

Fill in actual values for N, the date, and the ISSUE-10 row.

---

### 11. Update `prompts/STEP-index.md`

Add substep **41.5** to the STEP-41 substep table, immediately after the `41.4` row:

```markdown
| 41.5 | Audit Fix — Guard Correctness & CI Hardening | Done | Fixed ISSUE-4 (l10n regex catches double-quoted strings), ISSUE-8 (CI fetch-depth), ISSUE-1/5/6 (guard robustness); 3 l10n tests, 3 contract tests passing |
```

---

### 12. Commit

Three commits across the three repos:

**`Code/mine-flow-app/`** (on `step-0041-release-readiness-baseline`):
```
fix(STEP-41.5): fix l10n guard regex, CI fetch-depth, and guard robustness

- Rewrite _hardcodedTextPattern to match both single- and double-quoted
  Text() literals — was silently missing double-quoted strings (ISSUE-4).
- Remove path.contains(exempt) false-exemption path; use endsWith only (ISSUE-5).
- Replace ghost script reference with accurate maintenance instructions (ISSUE-6).
- Harden check_supabase_contracts.dart porcelain parser: length < 4 guard
  and .trim() on extracted path to handle CRLF line endings (ISSUE-1).
- Add fetch-depth: 2 to CI test job checkout step (ISSUE-8).
- Add double-quote fixture test to check_l10n_baseline_test.dart (now 3 tests).
```

**`Code/mine-flow-docs/`** (on `step-0041-release-readiness-baseline`):
```
docs(STEP-41.5): append audit-fix closure to reconciliation report
```

**`prompts/`** (on `main`):
```
chore(STEP-41.5): add substep 41.5 row to STEP-index.md
```

---

## Verification checklist (Definition of Done)

- [ ] ISSUE-4 fixed: `Text("double-quoted")` is detected by the l10n guard.
- [ ] New test `fails when a non-exempt file has a double-quoted hardcoded string` passes.
- [ ] ISSUE-5 fixed: `path.endsWith(exempt)` only (no `contains` branch).
- [ ] ISSUE-6 fixed: ghost script comment replaced with accurate maintenance instructions.
- [ ] ISSUE-1 fixed: porcelain parser uses `length < 4` + `.trim()` on extracted path.
- [ ] ISSUE-8 fixed: `fetch-depth: 2` in `test` job checkout; `build-android` job unchanged.
- [ ] `check_l10n_baseline_test.dart`: 3 tests passing.
- [ ] `check_supabase_contracts_test.dart`: 3 tests passing (count unchanged).
- [ ] Full `flutter test` suite: exit 0; ≥ 433 tests; zero new failures.
- [ ] `flutter analyze`: 0 issues.
- [ ] `dart format --output=none ... lib/ test/ tool/`: 0 issues.
- [ ] Reconciliation report appended with STEP-41.5 section and filled-in actual results.
- [ ] `prompts/STEP-index.md` has substep 41.5 row marked Done.
- [ ] ISSUE-10 either resolved (with note in Doc 07) or explicitly deferred in report.
- [ ] Both repo worktrees clean after commit.

## Keeping the docs true

Do not edit `DESIGN.md` or `PRODUCT.md`. Do not alter the `_legacyExemptFiles` list contents.
Do not weaken the localization requirement in Doc 07. If ISSUE-10 is skipped, record that
decision accurately in the report — do not claim it was fixed.

## Next

After all definition-of-done items are checked, start a **fresh chat** and begin
**STEP-42: Staging Environment & Promotion Pipeline**
(the next `Planned` STEP in `prompts/STEP-index.md`).
