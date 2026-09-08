# mine-flow — STEP-48.30: Dead-affordance & shadow-file cleanup (CreatableCombobox create tile, duplicate lib/ files)

> **How to run:** tell your agent *"run substep 48.30"*. Self-contained — runnable cold in a fresh chat.
>
> Inside STEP-48. Does **not** close the STEP, archive it, or authorize Phase 4.

## Context

Two small, concrete defects the STEP-45/46/47 implementation audit tripped over
(`Code/mine-flow-docs/reports/2026-09-05-step-45-47-implementation-audit.md` §G-4 partial, §G-6).

**1. `CreatableCombobox` ships a control that does nothing at 3 of its 5 call sites.**

The widget renders an "add new" tile whenever the typed query matches no item:
`_queryMatchesNone` (`lib/core/presentation/widgets/creatable_combobox.dart:96–102`) gates a
`_ListTile(label: 'Tambah "$query"', …)` at `:313–320`, and tapping it runs `_createNew` (`:152–156`),
which clears the field, unfocuses, and calls `widget.onCreateNew?.call(text)` — a **null-aware** call.
`onCreateNew` is optional (`:36`, `:61`) and only one call site passes it:

| Call site | `onCreateNew` |
|---|---|
| `lib/features/daily_log/presentation/widgets/zone_picker.dart:112–122` | ✅ `_handleCreateZone` |
| `lib/features/tracking/presentation/pages/cut_fill_form_screen.dart:436` (material type) | ❌ absent |
| `lib/features/tracking/presentation/pages/land_clearing_entry_screen.dart:372` (Plan tab, method) | ❌ absent |
| `lib/features/tracking/presentation/pages/land_clearing_entry_screen.dart:485` (Actual tab, method) | ❌ absent |

So on three forms a user types something not in the list, sees a tappable `Tambah "…"` row, taps it,
and the field silently empties. The widget has no way to express "selection only, no creation" — the
tile's visibility is derived from the query alone, never from whether a handler exists.

Two boundaries to respect:

- **The zone combobox is fine.** STEP-48.20's staging `42501` came from the zone control, whose
  `onCreateNew` works and correctly hit the `supervisor_zones_all` policy. That verdict stands; do not
  "fix" zone creation.
- **CF-043's other half is not yours.** The register (STEP-46.3 findings, CF-043) also asked to
  "constrain method to the enumerated set" and "use one shared control, not two" — the Plan/Actual tabs
  still hold two independent comboboxes over the same `record.method`. That restructuring is
  **STEP-51**. You remove the dead affordance; you do not merge the two controls or redesign the tabs.
  Note that `cut_fill_form_screen.dart:425–435` deliberately appends an off-list `record.materialType`
  to its options so existing rows still display — preserve that behaviour.

**2. Two files in `lib/` shadow the ones actually routed.**

Of 240 `lib/` Dart files, 7 are referenced by no `import`/`export`/`part` anywhere and 17 are
unreachable from `lib/main.dart`. Two are genuine traps because a same-named, same-classed file *is*
in use:

| Dead file | Live file it shadows | Evidence |
|---|---|---|
| `lib/app/presentation/pages/settings_page.dart` (630 B) | `lib/features/settings/presentation/pages/settings_page.dart` (19 KB) | dead one's own header: `// Placeholder Settings page for STEP-31.1 scaffold … will be implemented in STEP-35`; `router.dart:26` imports the feature one; `test/features/settings/presentation/settings_page_test.dart:17` too |
| `lib/app/presentation/widgets/app_shell.dart` (6.4 KB) | `lib/app/presentation/pages/app_shell.dart` (13 KB) | `router.dart:25`, `test/app/app_shell_test.dart:16`, `test/app/router_test.dart:13`, and 3 journeys import the `pages/` one |

Both define a class with the same name as the live file, which is how a future edit lands in the wrong
one. The placeholder also holds the last raw `TextStyle(fontSize: 24)` outside `pdf_service.dart` —
i.e. STEP-46's CF-089 token cleanup looks complete only because this file is invisible to anything
that renders.

The other five unreferenced files are unimported barrel/`export` files (`tracking.dart`,
`benchmark.dart`, `data_bucket.dart`, `data/data.dart`, `domain/domain.dart`) plus
`notification_badge.dart` and `report_type_card.dart` — **out of scope**: barrels are a deliberate
convention in some codebases, and the two widgets may be intended for imminent use. Report them,
recommend, do not delete.

## Read these first

- `Code/mine-flow-docs/reports/2026-09-05-step-45-47-implementation-audit.md` — §G-4, §G-6.
- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — the audit-substep block, the honesty rule, and the
  concurrency boundary.
- `prompts/003-release-readiness-integration-scale/step-0046/mine-flow-STEP-46.3-FINDINGS.md` —
  CF-043 (and CF-044, already done) so you can see exactly which half you are and are not doing.
- `Code/mine-flow-app/lib/core/presentation/widgets/creatable_combobox.dart` — the whole file,
  including the STEP-48.22 `GestureDetector`/`FTappable`/`Semantics` comments; those fixes are load
  bearing for the cut/fill and land-clearing journeys.
- `Code/mine-flow-app/test/widget/widgets/creatable_combobox_test.dart` — existing coverage, notably
  `shows Add new tile when query matches no existing item`, `calls onCreateNew when Add new tile is
  tapped`, and `shows no Add new tile when query exactly matches existing item`. Your change must keep
  the creation path tested **and** add the selection-only case.
- The four call sites in the table above.
- `Code/mine-flow-app/lib/app/router.dart` — confirm which `SettingsPage` / `AppShell` are wired.
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` — the UI contract, if you need to justify
  what a non-creatable combobox should look like.
- Journeys that drive these controls: `integration_test/journeys/cut_fill_journey_test.dart:112–117`
  and `land_clearing_journey_test.dart:108–113` **assert the `Tambah "<zone>"` tile appears** — but for
  the **zone** picker, not the method one. Read them before changing anything so you do not break a
  green journey.

## Pre-flight and concurrency boundary

- `Code/mine-flow-app` has ~26 modified files + 1 untracked test from 48.23/48.27 awaiting 48.25's
  commit lane. **Preserve every one.** None of them is in your scope; if your change would touch one,
  stop and report rather than absorbing it.
- `Code/mine-flow-docs`: `architecture/04-data-model.md` is modified (48.23/48.27) — do not touch.
- `prompts/STEP-index.md` carries STEP-50's edit and STEP-51's reservation — do not modify `prompts/`.
- No `.env` reads, no secrets, no staging mutation, no remote calls.
- Deleting files is the one irreversible-feeling action here: prove non-use before deleting, and prefer
  `git rm` on the branch (recoverable from history) over anything clever.

## Scope

### In scope

1. **Give `CreatableCombobox` a truthful create affordance.**
   - The tile must not render when the widget cannot honour it. The obvious minimal change is to gate
     the tile on `widget.onCreateNew != null` in `_queryMatchesNone`'s consumers (`:221`, `:291`,
     `:313`) and in `_onKeyEvent`'s `hasAddNew`/`totalOptions` arithmetic (`:164–191`) so keyboard
     Enter cannot select a nonexistent option either. Sweep **all** uses of `hasAddNew`, not just the
     visual one — a keyboard-only path that still fires `_createNew` is the same bug wearing a
     different hat.
   - Consider whether an explicit `bool creatable` reads better than inferring from a nullable
     callback; either is acceptable, but the API must make "selection only" expressible and the
     docstring must say so. If you add a parameter, do not make it required (5 call sites, and the
     default must be the safe one).
   - Decide what a no-match query should show in selection-only mode: currently the dropdown hides
     entirely when `filtered.isEmpty && !hasAddNew` (`:291`). A silent empty dropdown is a lesser
     defect than a lying button, but if Doc 07 or the audit suggests an empty-state line, say which
     you chose and why. Do not add unlocalized copy without checking the l10n guard
     (`tool/check_l10n_baseline.dart` — and note 48.29 may have just made that guard multi-line-aware,
     so a new `Text('…')` in a non-exempt file will now fail CI).
2. **Fix the three call sites** so none renders a dead tile: `cut_fill_form_screen.dart:436`,
   `land_clearing_entry_screen.dart:372`, `:485`. Preserve `cut_fill_form_screen`'s off-list
   `materialType` append. Leave `zone_picker.dart` alone.
3. **Delete the two shadow files** after proving non-use:
   - `lib/app/presentation/pages/settings_page.dart`
   - `lib/app/presentation/widgets/app_shell.dart`
   Proof = a repo-wide search for the path and for the class name across `lib/`, `test/`,
   `integration_test/`, `test_driver/`, `tool/`, plus `flutter analyze` clean and the full suite green
   after removal. If either turns out to have a live consumer, **do not delete it** — report the
   consumer and stop; that is an escalation, not a judgement call.
4. **Add regression coverage.**
   - Widget test: a `CreatableCombobox` without a create handler shows **no** `Tambah "…"` tile for a
     no-match query, and Enter on a no-match query does not invoke creation.
   - Keep the existing creation-path tests green (they must still prove the zone-style behaviour).
   - A cheap structural test that the deleted paths stay deleted is optional; if you add one, keep it
     honest (asserting a file's absence is weak — prefer asserting the routed widget is the one the
     router builds, which `test/app/router_test.dart` may already do).
5. **Report the remaining 5 unreferenced files** with a recommendation each (delete / keep as barrel /
   wire up), for STEP-51 or a later cleanup. No deletions beyond the two named.

### Out of scope

- CF-043's structural half: constraining `method` to the enumerated set, merging the Plan/Actual
  controls, or changing `_clearingMethods`. **STEP-51.**
- CF-087's Material remainder, 46.4's test debt — **STEP-51.**
- `registries/risks.yml`, ADR/index truth (48.28); CI/l10n guards (48.29).
- The other 5 unreferenced files and the 15 files unreachable-but-referenced.
- Any change to the journeys' zone-creation assertions, or to `zone_picker.dart`.
- Running or judging the branch-head CI gate (48.26); pushing (48.25).

## Your task

1. Re-derive both findings on the current tree before editing: print the 5 call sites and which pass
   `onCreateNew`; print the shadow files' sizes, their class names, and every importer of the live and
   dead paths. Quote real output.
2. Write the failing test first for the combobox (no handler ⇒ no tile), watch it fail, then implement.
3. Sweep `hasAddNew` / `_queryMatchesNone` for every consumer including the keyboard path; re-run the
   existing combobox tests to prove the creation path still works.
4. Fix the three call sites. Run the tracking widget tests.
5. Prove the shadow files are unused, delete them, re-run analyze + full suite.
6. Run the local gates; commit with specific-file staging only.
7. Write `Upcoming Prompts/mine-flow-STEP-48.30-FINDINGS.md` including the 5-file recommendation table
   and an explicit note of what you left to STEP-51.

## Verification

```bash
cd Code/mine-flow-app
grep -rn 'CreatableCombobox' lib --include='*.dart' | grep -v 'creatable_combobox.dart'
grep -rn 'onCreateNew' lib --include='*.dart'
grep -rn 'app/presentation/pages/settings_page\|app/presentation/widgets/app_shell' lib test integration_test test_driver tool

flutter test test/widget/widgets/creatable_combobox_test.dart
flutter test test/features/tracking/ test/app/
flutter analyze
dart format --output=none --set-exit-if-changed lib/ test/
dart run tool/check_l10n_baseline.dart
dart run tool/check_supabase_contracts.dart
flutter test
```

Required evidence:

- The new widget test observed **failing before** the fix and passing after.
- No `Tambah "…"` tile at any of the three call sites (state how you verified — widget test per site,
  or the shared widget test plus a grep proving no site passes a handler).
- Existing combobox creation tests still green; `zone_picker.dart` unchanged.
- Both shadow files' non-use proven by search output, then deleted; `flutter analyze` 0 and the full
  suite green afterwards.
- `flutter test` count stated (local baseline 513 with 48.23/48.27's uncommitted pins present) with the
  delta explained.
- l10n guard `[OK]` (especially if you added any user-facing string).
- `git status --short` for all three repos showing the concurrent files untouched.
- No secrets read or printed.

## Keeping the docs true

If you change `CreatableCombobox`'s public API, its docstring is the contract — update the "## Behaviour"
section, not just the parameter list. If the selection-only empty state introduces a visible UI state
that `architecture/07-ui-design-system.md` does not cover, either follow the doc's existing empty-state
pattern or note the divergence for 48.15/STEP-51; do not edit Doc 07 to bless a new pattern in a
cleanup substep. Archived findings files are immutable — append, never rewrite.

## Definition of done

- [ ] `CreatableCombobox` cannot render a create tile it cannot honour, including via the keyboard path.
- [ ] The three call sites render no dead affordance; `zone_picker.dart` and the journeys' zone
      assertions are untouched and green.
- [ ] `cut_fill_form_screen.dart`'s off-list `materialType` behaviour preserved.
- [ ] New widget test proves selection-only mode; the creation-path tests still prove creation.
- [ ] `lib/app/presentation/pages/settings_page.dart` and `lib/app/presentation/widgets/app_shell.dart`
      deleted with non-use proven, or kept with the live consumer named.
- [ ] `flutter analyze` 0, formatter clean, l10n + contract guards OK, `flutter test` green.
- [ ] The remaining 5 unreferenced files reported with a recommendation each; nothing else deleted.
- [ ] CF-043's structural half explicitly handed to STEP-51, not silently absorbed or silently dropped.
- [ ] Concurrent 48.23/48.27 app files, the Doc 04 edit, and `prompts/STEP-index.md` untouched.
- [ ] `mine-flow-STEP-48.30-FINDINGS.md` written with real command output.

## Next

This is the last audit substep. The code-touching wave then re-enters the gate sequence: **48.24**
(local full gate) → **48.25** (commit/push) → **48.26** (branch-head CI verdict) → **48.15** (docs-true
close) once 48.26 is GO. STEP-48 remains `In progress` until then.
