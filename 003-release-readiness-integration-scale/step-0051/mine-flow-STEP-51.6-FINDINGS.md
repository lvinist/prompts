# mine-flow — STEP-51.6 FINDINGS: Material-import sweep & residue check

**Substep:** 51.6 — Material import sweep and residue check
**Date:** 2026-09-09
**Branch:** `step-0051-ui-debt-closure`
**Status:** Complete pending owner commit; sibling 51.8 test file remains dirty and excluded

## Scope and method

Removed residual `package:flutter/material.dart` imports from `lib/` where the file uses
only Flutter core widgets or ForUI components. Files that still use a Material primitive
retain the import with the justification comment:

```dart
// Material: this file uses a Material primitive with no ForUI equivalent.
```

Repeatable inventory command:

```bash
grep -rl "package:flutter/material.dart" lib --include='*.dart' | wc -l
```

The final command output is **47** importers. A heuristic inventory was cross-checked
with `flutter analyze`; the 47 survivors are the analyzer-proven Material cases, not
an assumption based on symbol names. The analyzer-proven survivors include app/theme
classes, date and time picker APIs, Material navigation controls, dropdowns, chips,
progress indicators, `InkWell`, `Material`, `IconButton`, and Material text-field
appearance APIs.

## Residue checks

Anchored searches in `lib/` returned zero matches for all four migrated families:

```text
(^|[^A-Za-z])showSnackBar(       0
(^|[^A-Za-z])SnackBar(           0
(^|[^A-Za-z])Scaffold(           0
(^|[^A-Za-z])AppBar(              0
(^|[^A-Za-z])CircularProgressIndicator( 0
```

The anchored patterns avoid false positives from `FScaffold(` and other replacement
names containing a legacy token.

## Verification

- `flutter analyze` — **No issues found**.
- `dart format --set-exit-if-changed lib` — **238 files, 0 changed**.
- `flutter test` — **550 passed, 5 skipped, 0 failed**.
- `git diff --check` — no LF-owned line-ending churn remains. Git still reports the
  repository's existing CRLF-convention files as trailing whitespace in added lines;
  those files were preserved byte-for-byte apart from their import/comment edits.

## Concurrency ledger

`test/features/tracking/presentation/cut_fill_form_screen_test.dart` was dirty before
this substep and belongs to 51.8 (CF-014 citation). It was not edited or staged by
51.6. Its CRLF diff remains excluded from this substep and must be handled by its owner.

No behavior, tests, or integration-test files were changed by 51.6.

## Handoff

The next open substep is **51.9** (dead-file disposition), followed by **51.10**
(verification and close). The PLAN progress row should be updated to Done with this
findings file and the final importer count.
