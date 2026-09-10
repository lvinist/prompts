# mine-flow — STEP-51.3 FINDINGS: `AppBar` → ForUI header (14 files, 19 sites)

**Substep:** 51.3 — AppBar→FHeader migration (CF-087)
**Date:** 2026-09-09
**Owner model (per PLAN):** Gemini 3.1 Pro High (executed by Hermes in this session, with user approval implied by "run substep 51.3")
**Status:** Complete — all 19 sites migrated, grep zero, gates green.
**Branch:** `step-0051-ui-debt-closure`, commit `59f595f`.

## 1. Re-derived inventory (branch head after 51.2/51.4/51.7 landed)

The 51.1 inventory (19 sites / 14 files) held exactly on the post-51.4 head:
`grep -rnE '[^A-Za-z]AppBar\(' lib` → 19 hits. Line numbers drifted +2–5 (51.4's
FScaffold wrap reflowed the same files), re-located on head before each edit.

## 2. Migration design (from route topology + in-repo exemplars)

In-repo reference patterns confirmed first: 7 bare `FHeader(` uses on shell-tab
roots (settings, report_config, report_type_picker, data_bucket_list,
cut_fill_list, inventory_dashboard, land_clearing_list) and 2 `FHeader.nested`
with ghost-button back prefix (attendance_form, upload_file) — the latter
wrapped in `PreferredSize(kToolbarHeight)` where height-capped.

Classification from `lib/app/router.dart` + call sites:

- **Shell-tab roots → bare `FHeader`** (title start-aligned, no back affordance
  — deliberate, matching the 7 existing exemplars): attendance_screen
  ('Absensi Kru Lapangan' + FBadge suffix), benchmark_list, daily_log_list,
  equipment_history, timeline.
- **Pushed screens → `FHeader.nested` + explicit back prefix** (Material
  `AppBar` was auto-implying the back button via `automaticallyImplyLeading`
  on all of these routes — dropping it silently would be a navigation
  regression; the explicit prefix preserves it): benchmark_form (2 states),
  daily_log_form (2 states), cut_fill_form (2), inventory_item_entry (2),
  land_clearing_entry (2), file_detail, upload_file null-state, notifications
  (pushed from `global_app_header.dart:340`), equipment_check_form.

Actions → `suffixes`; leading back → `prefixes` ghost `FButton` with
`LucideIcons.arrowLeft`.

## 3. Per-site notes

- **attendance_screen** — `actions:[FBadge]` → `suffixes:[FBadge]` (wrapper
  Padding/Center dropped; FHeader lays out suffixes itself).
- **benchmark_form** — loading state + form state both nested; form state keeps
  the 'Batal' cancel action as a suffix.
- **daily_log_form** — error + form states nested; `AutoSaveIndicator` moves
  from AppBar action to FHeader suffix (it's a plain Container — no Material
  dependency, verified).
- **file_detail** — leading IconButton + PopupMenuButton actions. The
  PopupMenuButton needs a Material ancestor under FHeader → transparent
  `Material` wrap, the same accommodation 51.4 established for FScaffold
  bodies. Dialog (showFDialog/FDialog) untouched.
- **equipment_check_form** — the only colored AppBar in the app
  (`backgroundColor: theme.colors.primary`, `foregroundColor:
  primaryForeground`). Preserved via the style-delta API, verified in pub cache
  before use:
  `style: FHeaderStyleDelta.delta(decoration: DecorationDelta.boxDelta(color:
  theme.colors.primary), titleTextStyle: TextStyleDelta.delta(color:
  theme.colors.primaryForeground))`. Also needed the lucide import added (the
  file had none).
- **upload_file null-state** (gDrive == null) — nested + back; the main
  upload state was already `FHeader.nested` (exemplar).
- **daily_log_list** — `scrolledUnderElevation: 0.5` dropped: FHeader has no
  scroll-elevation API; the header band is already flat (elevation 0
  equivalent).
- All `elevation: 0` args dropped (FHeader decoration has no elevation).
- Titles/semantics preserved verbatim — no semantics-label changes (STEP-48
  journey surface checked: no journey or widget test references `AppBar`,
  back finders, or header-specific finders; only `AutoSaveIndicator` is
  type-asserted in tests, and it survives untouched).

## 4. Concurrent-sibling handling (51.5 in flight)

The 51.5 executor (CPI→FCircularProgress) was working the same files
concurrently. Every overlap was classified before commit:

- 7 files: sibling's CPI hunks fully separate from my header hunks → my hunks
  staged via `git apply --cached` on a byte-safe patch (built from
  `git diff` in binary mode — Python `text=True` universal newlines had
  stripped CRLF and broken the first attempt).
- 5 files (benchmark_form, daily_log_form, cut_fill_form,
  inventory_item_entry, land_clearing_entry): my header wrap and sibling's
  loading-state CPI swap share a hunk → staged intermediate content (worktree
  minus sibling's loading-state lines, restored to HEAD's
  `CircularProgressIndicator`), then worktree restored to the combined state.
- 2 files (file_detail, upload_file): pure mine, staged wholesale.
- Verified before commit: `git diff --cached | grep FCircularProgress` →
  none; exactly 19 `AppBar(` removals in the cached diff; worktree still
  holds all of 51.5's uncommitted work after commit.
- The full-suite run (below) was on the combined worktree (my headers +
  sibling's CPI swaps) — the state that will exist once 51.5 commits.

## 5. Verification evidence

- `grep -rE 'AppBar\(' lib --include='*.dart'` (anchored
  `[^A-Za-z]AppBar\(`) → **0 hits**.
- `flutter analyze` → **No issues found** (6.7s, post-change).
- `dart format --set-exit-if-changed .` → clean (after formatting my 14
  files; the 2 extra files `dart format .` flagged were the sibling's
  unformatted 51.5 edits — left unstaged, not mine to format-commit).
- `flutter test` (full suite, combined worktree) → **550 passed + 5 skipped,
  0 failed** ("All tests passed!", 3:16). Baseline from 51.7: 550+5 — no
  regression, no new cases (per D3 container swaps add none).
- CRLF convention preserved: CR-byte counts on the 4 CRLF files stable
  (476/443/537/661) — only intended lines changed; `git diff --check`
  trailing-whitespace flags are the known CRLF-convention signal (per skill
  reference), not churn.
- Header semantics surface: no widget test or journey asserts on
  `AppBar`/back-button finders (verified by grep across `test/` and
  `integration_test/`); titles and `Semantics(header: true)` wrappers moved
  verbatim.

## 6. Escalations

None fired. No ADR needed (no Material-only affordance required; the colored
band was expressible via the style delta). No Doc 07 change (FHeader
root/nested usage matches its header pattern and the 9 pre-existing exemplars).

## 7. Definition of done

- [x] All 19 inventory AppBar sites migrated; anchored grep zero.
- [x] Existing screen tests green (full suite 550+5, no finder updates needed).
- [x] `flutter analyze` 0; format clean; `flutter test` green with
      count+delta (550+5, +0).
- [x] Findings written; PLAN progress row updated (51.3 → Done, commit
      `59f595f`).

## 8. Handoff

51.5 (CPI) is in flight by a sibling — its uncommitted work is preserved in
the worktree. Remaining open substeps: 51.6 (material-import sweep; needs
51.2–51.5), 51.8 (46.4 regression coverage), 51.9 (dead files), 51.10
(close). The sibling's restructure of loading states (collapsed
`FScaffold(child: Center(...))` onto one line) means 51.6's import sweep will
see those files formatted differently than HEAD — no action needed, just
awareness.
