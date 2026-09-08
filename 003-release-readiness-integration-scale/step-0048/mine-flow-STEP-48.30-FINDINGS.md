# mine-flow — STEP-48.30 FINDINGS: Dead-affordance & shadow-file cleanup

**Substep:** 48.30 — audit §G-4 (dead `Tambah` tile, 3 of 5 call sites) + §G-6 (two shadowing `lib/` files)
**Date:** 2026-09-08
**Owner model (per PLAN):** GPT 5.6 Luna slot — executed by Hermes (Claude) session
**Status:** Implementation complete; all local gates green. Committed `bb32c92` on `step-0048-runtime-evidence` (unpushed — push is 48.25's lane).

## 1. G-4 — `CreatableCombobox` is now selection-only-capable

**Re-derivation (pre-edit, current tree):** exactly as the prompt states —
`grep -rn 'CreatableCombobox' lib | grep -v creatable_combobox.dart` returns the 5 call sites;
`grep -rn 'onCreateNew' lib` shows only `zone_picker.dart:121` passes a handler
(`cut_fill_form_screen.dart:436`, `land_clearing_entry_screen.dart:372`, `:485` pass none).

**API decision:** no new parameter. "Creatable" is inferred from `onCreateNew != null` — a separate
`bool creatable` could contradict the handler's presence and is one more knob to get wrong. The
nullable-callback inference keeps all 5 call sites type-safe with the safe default (selection-only),
which is exactly the prompt's option-2 allowance.

**Implementation:** the query-only predicate `_queryMatchesNone` was folded into
`_canCreateNew` (`creatable_combobox.dart:102–115`), which additionally requires
`widget.onCreateNew != null`. Because **every** consumer read that getter through the
`hasAddNew` local — the tile render (`:332`), the dropdown-visibility condition (`:310`),
the keyboard `totalOptions` arithmetic (`:180`), and the Enter-on-add-new path (`:203`) —
gating at the source fixes the pointer path, the keyboard path, and the empty-dropdown
behaviour in one move. Swept for stale references: `grep -rn '_queryMatchesNone' lib test integration_test`
→ no matches.

**Latent crash found and fixed by the new keyboard test:** with zero options
(selection-only + no-match query), ArrowDown hit `(_highlightedIndex + 1).clamp(0, -1)` →
`ArgumentError: Invalid argument(s): 0` from `int.clamp` (observed in the first post-fix run,
stack at `creatable_combobox.dart:184`). This state was unreachable before G-4 — the dead tile
always counted as one option. Both arrow keys now return `ignored` when `totalOptions == 0`
(`:184–192`); Enter is naturally safe (both branches fall through to `ignored`).

**Docstring contract updated:** the `## Behaviour` block now states the selection-only
mode explicitly (no create tile, no keyboard create entry, no-match query shows no matching
options), and the `onCreateNew` parameter doc says what null means. Public API surface unchanged.

**Empty-state decision:** selection-only no-match keeps the pre-existing behaviour — the dropdown
hides entirely (`filtered.isEmpty && !hasAddNew`). Doc 07 has no empty-state pattern
(`grep -i 'empty.state|no results|no match'` → 0 hits), adding copy would trip the l10n guard,
and a silent empty dropdown is the lesser defect vs. a lying button. Recorded for STEP-51 if
it wants an empty-state line when it merges the Plan/Actual controls.

**Tests (RED first, then GREEN):**
- `shows no Add new tile when query matches no existing item` — **failed pre-fix**
  (`Expected: no matching candidates / Actual: Found 1 widget with text "Tambah "Fig""`), passes post-fix.
- `keyboard Enter on a no-match query neither creates nor clears the field` — **failed pre-fix**
  (`Expected: 'Fig' / Actual: ''` — Enter fired `_createNew` and cleared the field), passes post-fix.
- The two existing creation-path tests now pass an explicit handler (the harness previously
  defaulted a handler in, masking the bug); `zone_picker.dart` is untouched
  (`git diff HEAD -- lib/features/daily_log/presentation/widgets/zone_picker.dart` → empty) and the
  journeys' zone `Tambah` assertions never referenced the method/material fields (verified:
  the land-clearing journey only *selects* `Excavator` from the method combobox, it never taps a
  `Tambah` tile there).
- `cut_fill_form_screen.dart`'s off-list `materialType` append (`:425–435`) preserved — the file
  received **zero edits**; tracking suite green.

## 2. Call sites — fixed with zero edits

All three defective sites already omit `onCreateNew`; the widget-level gate removes their dead
tile. Verification per the prompt's "shared widget test + grep" allowance: the grep above proves
no site passes a handler, and the selection-only widget tests pin the behaviour those sites now get.
Only `zone_picker.dart:121` passes a handler, and its creation path stays green
(creation tests + full suite).

## 3. G-6 — both shadow files deleted, non-use proven

Proof (all run pre-delete on the current tree):

- `router.dart:25–26` imports only the live paths
  (`app/presentation/pages/app_shell.dart`, `features/settings/presentation/pages/settings_page.dart`).
- Repo-wide path grep across `lib test integration_test test_driver tool`: the dead paths appear
  **only** as inert exemption-list strings in `tool/check_l10n_baseline.dart:86–87` (not imports —
  matched by `path.endsWith()` against files being scanned, and no longer present after deletion).
- Class-consumer grep: every `SettingsPage` reference resolves to the feature file via `router.dart:476`;
  every live `AppShell` reference (`router.dart:123`, `test/app/app_shell_test.dart:45`,
  `test/app/router_test.dart:54`, 3 journeys) imports the `pages/` file.
- Relative-import sweep (any `import` mentioning the basenames outside the live paths): 0 hits.

Deleted with `git rm` on the branch: `lib/app/presentation/pages/settings_page.dart` (630 B) and
`lib/app/presentation/widgets/app_shell.dart` (6,416 B). Side effect recorded: the audit's last
raw `TextStyle(fontSize: 24)` (CF-089) lived in the dead settings placeholder —
`grep -rn 'fontSize: 24' lib` now returns **0 matches**; STEP-46's token cleanup is genuinely complete.

**l10n-guard housekeeping note:** `tool/check_l10n_baseline.dart:86–87` still lists both deleted
paths in `_legacyExemptFiles` (inert — guard output went from 48 to **46 exempt**, exactly the two
deleted files; `[OK]` unchanged). That file is 48.29's concurrent lane, so I did not touch it;
removing the two stale entries is a one-line cleanup for 48.15/STEP-51.

## 4. Remaining 5 unreferenced files — recommendations (report-only; nothing deleted)

| File | Verified unreferenced by | Recommendation |
|---|---|---|
| `lib/features/tracking/tracking.dart` | 0 imports of `tracking/tracking.dart` / `../tracking.dart` anywhere | Delete in STEP-51 (its `data/data.dart` + `domain/domain.dart` twins are imported only by the dead barrels) |
| `lib/features/benchmark/benchmark.dart` | 0 imports of `benchmark/benchmark.dart` / `../benchmark.dart` (the audit's `benchmark.dart` grep hits were `entities/benchmark.dart` basename noise) | Delete in STEP-51 |
| `lib/features/data_bucket/data_bucket.dart` | 0 imports outside `features/data_bucket/` itself | Delete in STEP-51 |
| `lib/features/data_bucket/data/data.dart`, `.../domain/domain.dart`, `lib/features/tracking/data/data.dart`, `.../domain/domain.dart` | imported only by the two dead feature barrels | Delete together with their barrels (one PR atomically) |
| `lib/features/notifications/presentation/widgets/notification_badge.dart` | 0 imports anywhere | Keep pending product intent — or delete in STEP-51 if the notifications feature confirms it has no planned use |
| `lib/features/reporting/presentation/widgets/report_type_card.dart` | 0 imports anywhere | Keep pending product intent — or delete in STEP-51 (reporting now uses the migrated report-type picker page) |

## 5. Evidence

| Gate | Result |
|---|---|
| `flutter test test/widget/widgets/creatable_combobox_test.dart` | **13/13** (11 baseline + 2 new); new tests observed RED pre-fix |
| `flutter test test/features/tracking/ test/app/` | **118/118** |
| `flutter test` (full, post-delete) | **542/542** — baseline 540 (48.29 findings) + 2 new; delta exact |
| `flutter analyze` | No issues found |
| `dart format --output=none --set-exit-if-changed lib/ test/` | 0 changed |
| `dart run tool/check_l10n_baseline.dart` | `[OK]` — 14 scanned / 46 exempt (48→46 = the 2 deleted files) |
| `dart run tool/check_supabase_contracts.dart` | `[OK]` |
| `git diff --check` (owned files) | clean |

## 6. Line endings (owned files only)

The patch tool wrote `test/widget/widgets/creatable_combobox_test.dart` with CRLF churn
(295 CRs vs 0 at repo HEAD; `git diff --check` flagged every line). Normalized to LF
(`sed -i 's/\r$//'`), independently re-proven: CRs = 0, true diff +61/−3, focused suite re-run green.
`creatable_combobox.dart` was 0 CRs throughout. Excluded concurrent files preserved byte-for-byte;
their CR state (already CRLF at HEAD for the l10n dart files, pre-existing churn from 48.29's lane):

```
lib/l10n/app_localizations.dart:     HEAD CRs=146  worktree CRs=158
lib/l10n/app_localizations_en.dart:  HEAD CRs=16   worktree CRs=22
lib/l10n/app_localizations_id.dart:  HEAD CRs=16   worktree CRs=22
lib/l10n/app_en.arb / app_id.arb:    0 / 0
```

## 7. Concurrency boundary — preserved

- App repo post-commit tree: **exactly 48.25's lane** — 29 modified + 2 untracked
  (`test/tool/check_e2e_executed_test.dart`, `tool/ci/`), unchanged from session start.
- `Code/mine-flow-docs`: only the pre-existing `architecture/04-data-model.md` edit — untouched.
- `prompts/`: only the pre-existing STEP-50/STEP-51 edits — untouched (no commits, no index changes).
- No `.env` reads, no secrets, no staging mutation, no remote calls, no push.

## 8. Commit

`bb32c92` — `fix(core,app): selection-only CreatableCombobox; delete shadow settings/app-shell files (STEP-48.30)`
(4 files: 2 deletions, `creatable_combobox.dart` +45/−? incl. guard + docs, test +61/−3 true).
Staged set verified `git diff --cached --name-status` = exactly the 4 owned files before commit;
`git diff --cached --check` clean.

## 9. Explicitly left to STEP-51 (not silently absorbed)

- CF-043's structural half: constraining `method` to the enumerated set and merging the Plan/Actual
  comboboxes into one shared control — **untouched** (both tabs still hold two independent
  comboboxes over `record.method`; only the dead affordance is gone).
- The 5 (+4 twin) unreferenced barrel/widget files — recommendations in §4.
- The two stale l10n-guard exemption entries for the deleted files (§3).
- CF-087's Material remainder and 46.4 test debt — per STEP-51's reservation.
- Journeys' zone-creation assertions, `zone_picker.dart`, Doc 07 — untouched.

## 10. What's next

This was the last audit substep. The code-touching wave re-enters the gate sequence: **48.24**
(local full gate) → **48.25** (commit/push — now also carries `bb32c92`) → **48.26** (branch-head
CI verdict) → **48.15** (docs-true close). STEP-48 remains `In progress`.
