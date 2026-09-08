# mine-flow — STEP-48.21: Journey Finder Repair (`Too many elements`, `No element`)

> **How to run:** tell your agent *"run substep 48.21"*. Self-contained — runnable cold.

**Assigned model: Gemini 3.7 Flash High.** Procedural work with an unambiguous signal: each failure
names its own cause, and the fix is confirmed by the error no longer appearing. The one rule that
needs holding onto is that **no assertion may be weakened** to reach green — a deleted `expect` is
the same offence as a fabricated result. **Escalate to Opus 4.8** if a finder cannot be made
unambiguous without changing what the test proves, if the widget the finder looks for genuinely does
not exist (that is an app-defect, not a finder problem), or if the same fix fails twice.

## Why this substep exists

Branch-head CI run [`33327930159`](https://github.com/lvinist/mine-flow-app/actions/runs/33327930159)
failed both E2E jobs. Three of those failures are the journeys being wrong about the app, not the app
being wrong:

```
Bad state: Too many elements
  … get single → controller.dart:932 state → showKeyboard → enterText
  integration_test/journeys/cut_fill_journey_test.dart:90

Bad state: Too many elements
  … same stack
  integration_test/journeys/land_clearing_journey_test.dart:83

Bad state: No element
  … get first → finders.dart:1383 → controller.dart tap
  integration_test/journeys/notifications_journey_test.dart:139
```

**`Too many elements`** comes from `tester.enterText`, which calls `.single` on the finder's matches.
Both sites use the same pattern:

```dart
final bcmField = find.descendant(
  of: find.widgetWithText(Expanded, 'Volume (BCM)'),
  matching: find.byType(EditableText),
);
await tester.enterText(bcmField, '100');
```

`find.byType(EditableText)` under an `Expanded` matched more than one editable. Note that targeting
`EditableText` rather than `TextField` is **deliberate and must stay** — it is the RISK-0009 finder
rule (flutter/flutter#191095 crashes widget tests when a text field sits under `MergeSemantics` under
forui 0.26). The fix is a narrower *ancestor* or a stable key, never a switch back to `TextField`.

**`No element`** comes from `find.bySemanticsLabel('Tutup notifikasi').first` at
`notifications_journey_test.dart:139` — no widget in the tree carries that semantics label. Two very
different causes, and you must distinguish them: either the label was never added to the widget (an
**accessibility gap in the app**, which is a finding, not a test fix), or the control is off-screen /
not yet built. Check the widget source before touching the test.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — the 2026-08-31 amendment, the honesty rule, and the
  inherited **RISK-0009 finder rule**.
- **`Upcoming Prompts/mine-flow-STEP-48.16-FINDINGS.md`** — your scope: the `BH-nnn` rows classified
  **test-defect**. Only those.
- `Upcoming Prompts/mine-flow-STEP-48.5-FINDINGS.md` (cut/fill + land clearing),
  `…-48.9-FINDINGS.md` (timeline + notifications) — what those substeps believed they verified, and
  the finder patterns they used.
- `Upcoming Prompts/mine-flow-STEP-48.1-FINDINGS.md` — the journey-integrity audit. It set the
  standard: 22 `markTestSkipped` calls each followed by `return`, 25 `testWidgets` blocks each
  carrying a real assertion. Do not regress that count.
- root `.throughstone/local-user.md` — Experience level 2, Explanatory.
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` — the UI contract. If the widget the
  finder wants does not exist and the doc says it should, that is an app-defect.
- The three journey files, in full, plus the screens they drive:
  - `lib/features/tracking/presentation/pages/` (cut/fill and land-clearing forms)
  - `lib/features/notifications/presentation/` (the notification card and its dismiss control)

## Rules

1. **Never weaken an assertion.** Not by deleting an `expect`, not by swapping `findsOneWidget` for
   `findsWidgets`, not by wrapping a check in `if (finder.evaluate().isNotEmpty)`. If a check cannot
   pass, that is a finding, not a formatting problem.
2. **Never switch a text-field finder to `TextField`.** RISK-0009 stands: target `EditableText`.
   Narrow the *ancestor* instead.
3. **`.first` and `.last` are usually a smell.** They make a test pass while hiding which of N widgets
   it actually drove. Prefer a finder that matches exactly one thing. If you must disambiguate
   positionally, say in a comment why the position is stable.
4. **If the widget is missing, the app is wrong.** A semantics label that no widget carries is an
   accessibility defect (relevant to **RISK-0023**, screen-reader accessibility unverified). Adding
   the label to the widget is the correct fix — and it is a `lib/` change, so record it as such and
   check whether 48.22 already owns that file.

## Your task

### 1. Reproduce each failure locally

Boot the emulator and run each affected journey on its own so you see the error, not just read about
it:

```bash
flutter test integration_test/journeys/cut_fill_journey_test.dart -d emulator-5554 \
  --dart-define=SUPABASE_URL=… --dart-define=SUPABASE_ANON_KEY=… \
  --dart-define=TEST_USER_EMAIL=… --dart-define=TEST_USER_PASSWORD=…
```

Take the `--dart-define` values from the user or the CI workflow's secret **names** — never print a
value. If a journey now fails *earlier* for a schema or fixture reason, that is 48.17–48.20's scope:
confirm they have run, and if their work is not yet in your working tree, say so rather than guessing.

### 2. Make each finder match exactly one widget

For the two `enterText` sites, first find out **what** the extra match is. Print the match count and
identify each candidate before choosing a fix:

```dart
final candidates = find.descendant(
  of: find.widgetWithText(Expanded, 'Volume (BCM)'),
  matching: find.byType(EditableText),
);
debugPrint('candidates: ${candidates.evaluate().length}');
```

Then fix it at the right level, in order of preference:

1. a narrower, semantically meaningful ancestor (the specific `FTextField`, the labelled field
   wrapper) — best, because it says what it means;
2. a `Key` added to the widget in `lib/` — durable, and makes the test independent of layout, but it
   is an app change, so note it;
3. positional disambiguation with a comment justifying stability — last resort.

For `find.bySemanticsLabel('Tutup notifikasi')`, first grep `lib/` for the label:

```bash
grep -rn "Tutup notifikasi" lib/
```

- **Label absent** → add it to the dismiss control (a `Semantics` label or the button's own
  `semanticLabel`). Note it as an app-side accessibility fix and link it to RISK-0023.
- **Label present but not found** → the control is off-screen or built lazily. Use
  `tester.ensureVisible` before the tap, and remember the known ForUI pitfall: `ensureVisible` does
  **not** reliably scroll inside `FSidebar`/`OverflowBox`, so the reliable fix there is
  `tester.binding.setSurfaceSize(const Size(1024, 1200))` for that test. If you tap N such controls
  in a loop, `ensureVisible` each one before its tap.

### 3. Sweep for the same class

These three are the instances that fired. Others are waiting behind them. Grep every journey and
widget test for the risky patterns and fix or justify each:

```bash
grep -rn "\.first\b\|\.last\b\|find.byType(EditableText)\|bySemanticsLabel" integration_test/
```

For each hit, state whether it is provably unambiguous. A journey that only passes because the screen
happens to have one text field today will fail the next time a field is added — that is precisely how
this branch-head run went red.

### 4. Do not fix out of scope

If a journey fails after your finder fix for a reason 48.16 classified as app-defect, persistence
defect, or fixture drift, **stop and record it**. Name the owning substep. A finder substep that
starts editing `lib/` business logic has lost its boundary — the exception is a `Key` or a semantics
label added purely for testability/accessibility, which is expected and should be called out
explicitly.

## Verification

- Each of the three named failures reproduced locally before the fix and gone after it, with the
  command and output recorded.
- No `expect` removed, and no matcher loosened. State this explicitly, and support it: the assertion
  count per journey file should be **≥** what 48.1 recorded.
- `EditableText` still targeted (RISK-0009 honoured); no `find.byType(TextField)` introduced.
- Every `.first`/`.last` that remains carries a comment justifying it.
- Semantics-label outcome classified: app-side fix (with RISK-0023 noted) or test-side visibility fix.
- The same-class sweep completed across `integration_test/`.
- `flutter analyze` → 0 issues; `dart format --set-exit-if-changed .` → clean; `flutter test` green
  (the `attendance_daily_log_sync_test.dart` / `equipment_check_sync_test.dart` Hive `setUpAll` flake
  is known: re-run isolated and say so).
- Cut/fill, land-clearing, and notifications journeys run locally with ran-vs-skipped counts recorded.

## Scope

**In scope:** finders and waits inside `integration_test/`; `Key`s and semantics labels added to `lib/`
purely for testability or accessibility; the same-class sweep.

**Not in scope:** migrations (48.17), query column names (48.18), write-path key sets (48.19), seed
and fixture data (48.20), layout/overflow and Material-ancestor defects (48.22), persistence and
offline defects (48.23), `risks.yml` edits.

## Definition of done

- [ ] `cut_fill_journey_test.dart` and `land_clearing_journey_test.dart` `enterText` finders match
      exactly one widget; `Too many elements` gone.
- [ ] `notifications_journey_test.dart:139` resolved; cause classified as app-side label gap or
      test-side visibility.
- [ ] No assertion weakened; assertion counts stated and compared to 48.1's baseline.
- [ ] RISK-0009 finder rule honoured throughout.
- [ ] Same-class sweep of `integration_test/` complete; every remaining `.first`/`.last` justified.
- [ ] `flutter analyze` 0, `dart format` clean, `flutter test` green (flake diagnosed).
- [ ] Three journeys run locally; counts recorded; any out-of-scope failure named with its owner.
- [ ] `mine-flow-STEP-48.21-FINDINGS.md` written; PLAN progress table updated.
- [ ] Committed on `step-0048-runtime-evidence`.

## Next

Tell the user the next action is *"run substep 48.22"* (UI/harness defect fixes) in a **fresh chat**.
Flag any `lib/` file you touched, since 48.22 and 48.23 work in the same tree.
