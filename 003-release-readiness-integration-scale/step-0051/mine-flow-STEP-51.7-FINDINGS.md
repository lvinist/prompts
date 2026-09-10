# mine-flow — STEP-51.7 FINDINGS: CF-043 structural half — one shared method control

**Substep:** 51.7  
**Date:** 2026-09-09  
**Owner model (per PLAN):** Gemini 3.1 Pro High (executed by Antigravity/Claude Sonnet 4.6 Thinking)  
**Status:** Complete  
**Branch:** `step-0051-ui-debt-closure` (committed `281432f`)

## 1. CF-043 verification (re-confirmed from 51.1)

Two independent `CreatableCombobox<String>` widgets writing `record.method` confirmed at:
- `land_clearing_entry_screen.dart:373` (Plan tab) — removed
- `land_clearing_entry_screen.dart:486` (Actual tab) — removed

Both fed by `_clearingMethods` (defined `:98`). From 51.1 findings §6: STEP-48.30 already made both widgets selection-only (`onCreateNew == null`), so the structural remainder for 51.7 is exactly the register's ask: one shared control, both tabs editing one normalised value, widget test asserting it.

## 2. Changes made

### `lib/features/tracking/presentation/pages/land_clearing_entry_screen.dart`

**Constraint guard** (line 118-120 after edit):
- Added `!_clearingMethods.contains(record.method)` check to `_validateAndSave`, with a descriptive error message.
- This is a second-line defence: the selection-only combobox prevents user-originated out-of-set values; the guard defends against stale values arriving from `existingRecord`.
- Also updated the docstring to cite CF-043.

**Shared method control** (new, lines 331-352 after edit):
- Added one `CreatableCombobox<String>` in the shared section above the `TabBar`, alongside date and zone pickers, following ADR-0015's model ("method is likewise a single shared value").
- Label: `'Metode Clearing'`, icon: `LucideIcons.construction`.
- `onCreateNew == null` (selection-only — no create affordance).
- Wired to `MethodChangedEvent` via the same bloc path as before.

**Removed from Plan tab** (lines ~395-413 before edit):
- Deleted the per-tab `CreatableCombobox` + `SizedBox(height: 16)`.

**Removed from Actual tab** (lines ~487-505 before edit):
- Deleted the per-tab `CreatableCombobox` + `SizedBox(height: 16)`.

**No model/schema change** — `record.method` stays a `String?` in the domain entity. No ADR needed; no escalation fired.

### `test/features/tracking/presentation/land_clearing_entry_screen_test.dart`

Fully rewritten (3 tests, up from 1):

1. **Baseline structural test** (updated) — now asserts `findsOneWidget` for `CreatableCombobox<String>` instead of `findsAtLeastNWidgets(1)`. Also checks on the Actual tab view.

2. **CF-043 shared-value semantics test** (new) — asserts `'Metode Clearing'` label and exactly one `CreatableCombobox` on both the Plan tab and Actual tab. How it proves something: before the fix, two comboboxes were in the tree; `findsOneWidget` would fail.

3. **CF-043 constraint test** (new) — pumps the screen with an `existingRecord` whose `method = 'InvalidMethod'` (not in `_clearingMethods`), taps Save, and verifies `verifyNever(() => mockTrackingRepository.saveLandClearingRecord(any()))`. How it proves something: before the fix, `_validateAndSave` only checked for null/empty — the out-of-set guard didn't exist, so the repository would have been called and `verifyNever` would fail.

## 3. Verification

**Format:** `dart format --set-exit-if-changed` on both changed files → exit 0 (0 changed after initial format pass).

**Static analysis (changed files only):** `flutter analyze land_clearing_entry_screen.dart land_clearing_entry_screen_test.dart` → **No issues found** (6.5s).

**Full project analyze:** 2 pre-existing `info` warnings in `attendance_form_page.dart:102` and `equipment_check_form_screen.dart:118` (`sort_child_properties_last`) — both in 51.2's scope, not introduced by 51.7.

**Target tests:** `flutter test test/features/tracking/presentation/land_clearing_entry_screen_test.dart` → **3/3 passed**.

**Full suite:** `flutter test` — **550 passed + 5 skips, 0 failed** (exit 0, ~3:40 elapsed). Baseline from 51.1 was 548+5skip; net +2 (old test file had 1 test, new has 3). No regressions.

**Grep verification:** The screen file has exactly one `CreatableCombobox<String>` instantiation (in the shared section). Confirmed by viewing lines 330-355 of the post-edit file.

## 4. ADR / escalation check

- No data model change — no ADR needed (D5 holds).
- No escalation fired: the fix is a pure UI-layer restructure.
- The `record.method` field remains `String?` in the entity. The UI constraint is enforced at two layers (widget + `_validateAndSave`) without touching the domain model.

## 5. CF-043 closure status

Both halves of CF-043's ask are now satisfied:

| Register ask | Status |
|---|---|
| Constrain `method` to the enumerated set | ✅ Done — selection-only combobox (pre-existing from 48.30) + `_validateAndSave` guard |
| One shared control instead of two | ✅ Done — single `CreatableCombobox` above `TabBar`; per-tab copies removed |
| Widget test for shared-value semantics | ✅ Done — `findsOneWidget` on both tabs; `verifyNever` for constraint |

CF-043's structural half is closed. 51.10 finalizes the register appendix.

## 6. Commit

`281432f` on `step-0051-ui-debt-closure`:
```
refactor(STEP-51.7): CF-043 — one shared method control on land-clearing form
```
2 files changed.

## 7. Definition-of-done check

- [x] One shared method control; `record.method` constrained to `_clearingMethods`.
- [x] Widget test asserts shared-value semantics + constraint, citing CF-043.
- [x] `flutter analyze` 0 issues on changed files; format clean; 3/3 new tests pass.
- [x] Findings written; PLAN row updated (see below).

## 8. PLAN progress table update

Substep 51.7 → **Done**. PLAN substep table to be updated.
