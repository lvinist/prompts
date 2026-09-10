# mine-flow — STEP-51.5 FINDINGS: `CircularProgressIndicator` → `FCircularProgress` (25 sites, 22 files)

**Substep:** 51.5 — mechanical CPI sweep
**Date:** 2026-09-09
**Owner model (per PLAN):** Gemini 3.7 Flash High
**Status:** Complete — 25/25 sites migrated, all gates green, committed `69c6b44`.
**Branch:** `step-0051-ui-debt-closure`; started from `b706f9c` (51.4), landed on top of `59f595f` (51.3).

## 1. Concurrency note (read first)

This substep ran **concurrently** with two sibling sessions in the same worktree:

- **51.4** (`Scaffold`→`FScaffold`) was mid-sweep when 51.5 started; it committed
  `b706f9c` (35 sites/24 files) while 51.5 was reading the pub-cache API. 51.5's baseline
  was therefore re-run on that head: **`flutter analyze` 0 issues; `flutter test` 550 passed
  + 5 skipped, 0 failed** (logs `step51_5_analyze_baseline.log` / `step51_5_test_baseline.log`
  at the workspace root).
- **51.3** (`AppBar`→`FHeader`) went mid-sweep **while 51.5 was editing**, touching several of
  the same files (`daily_log_form_screen`, `inventory_item_entry_screen`,
  `land_clearing_entry_screen`, `cut_fill_form_screen`, `equipment_history_screen`,
  `notification_list_page`, `timeline_page`, `attendance_screen`, …). Per the shared-file
  commit-boundary procedure, 51.5 staged **only its own hunks** (reconstructed from HEAD
  content, not `git add -p`), and **waited for 51.3 to commit before committing** at the
  user's direction. 51.3's hunks are excluded from 51.5's commit by construction; any that
  appear in `git show <51.5-commit>` would be a mis-staging defect to be fixed by a
  compensating commit, not history rewrite.

## 2. Inventory reconciliation

51.1's inventory table (§3.4) listed 25 sites across 22 files with line numbers as of the
51.1 head. Re-derived on `b706f9c`: **25 sites / 22 files, exact match**, with line drift of
−2 to +15 lines (51.2/51.4 edits shifted positions; re-located by content grep, per the
PLAN's "hedge volatile references" rule).

All 25 sites are **indeterminate** loading spinners — no site binds a `value:`/progress
fraction, so **zero `FDeterminateProgress` conversions**; the target is uniformly
`FCircularProgress` (pub-cache-verified at
`D:/AppDev/.pub-cache/hosted/pub.dev/forui-0.26.0/lib/src/widgets/progresses/circular_progress.dart`).

## 3. Migration mapping (site → target)

| Group | Sites | Target | Rationale |
|---|---|---|---|
| Plain loader | 17 | `const Center(child: FCircularProgress())` | Default `.md`, theme colour (`mutedForeground`) — pure visual swap |
| Sized list-loader | 4 (`daily_log_list`, `cut_fill_list`, `inventory_dashboard`, `land_clearing_list` — 28×28 `SizedBox` + `strokeWidth: 2.5`) | `const Center(child: FCircularProgress(size: .lg))` | ForUI `.lg` (Desktop 18px / Touch 20px) ≈ the 28px-boxed Material default; size token replaces manual sizing per Doc 07 §3 |
| In-button, default colour | 2 (`login_page`, `report_config_page` — 20×20 + `strokeWidth: 2`) | `FCircularProgress(size: .sm)` in the kept 20×20 `SizedBox` | `.sm` (14/16px); `SizedBox` kept for stable button height |
| In-button, explicit colour | 2 (`attendance_form` submit, `equipment_check_form` submit — `primaryForeground` on primary button) | `FCircularProgress(size: .sm, style: .delta(iconStyle: .delta(color: theme.colors.primaryForeground)))` | Colour preserved: WCAG contrast on the primary button was the point (CF-075 precedent); `.sm` matches the 20px box |
| Tiny inline | 1 (`auto_save_indicator` — 12×12, explicit `fgColor`) | `FCircularProgress(size: .xs, style: .delta(iconStyle: .delta(color: fgColor)))` | `.xs` (12/14px); explicit colour kept to match the row's text/icon colour |
| Fixed-height strip | 1 (`zone_picker` — 40px `SizedBox`) | `FCircularProgress()` default inside the kept `SizedBox(height: 40)` | Strip reserves layout space; default size matches previous `strokeWidth: 2` rendering |

API evidence (all in the pinned 0.26.0 pub cache): `FCircularProgress({size, style,
semanticsLabel, icon})`; `size:` is `FCircularProgressSizeVariant` (`.xs/.sm/.md/.lg/.xl`,
default `.md`); `style:` is `FCircularProgressStyleDelta` — `.delta(iconStyle:
IconThemeDataDelta)` per `src/theme/delta/icon_theme_data.dart`; default style =
`IconThemeData(color: colors.mutedForeground, size: typography.body.<variant>.fontSize)`.
Dot-shorthand is valid under the repo's SDK `>=3.12.0`; forui's own source uses it.

## 4. Tests

- `grep CircularProgressIndicator test integration_test --include='*.dart'` → **0 hits** —
  no existing test asserts on the widget type, so **no loading-state finders needed
  updating** (the prompt's task 2 is a no-op, not a skipped duty).
- Behaviour flag per 51.1: **no** (pure visual swap, D3) → **no new tests authored**;
  the full suite must not regress (gates below).

## 5. Gates (all green, 2026-09-09)

- [x] grep-to-zero: `grep -rE 'CircularProgressIndicator\(' lib --include='*.dart'` → **0 hits**
      (`FCircularProgress` count 25 — exactly the inventory total).
- [x] `dart format --set-exit-if-changed` → 2 files reflowed to single-line form (my own sites);
      re-run clean. CR audit: no convention flips (CRLF files stayed CRLF; the −2 CR deltas on
      five CRLF files equal my 3-lines→1-line swaps; `auto_save_indicator.dart` LF-churn caught
      and undone pre-commit — final diff 4+/1−).
- [x] `flutter analyze` → **No issues found** (61s; log `step51_5_analyze.log`).
- [x] `flutter test` full suite → **550 passed + 5 skipped, 0 failed** — identical to the
      51.4-head baseline (no regressions, no new cases; log `step51_5_test.log`).
- [x] Commit `69c6b44` — 22 files, 37 insertions / 74 deletions, **CPI-shaped hunks only**
      (verified: 51.3's earlier commit `59f595f` carries zero `FCircularProgress` insertions;
      51.5's commit carries zero `FHeader`/header-shaped insertions). `git diff --check`
      "trailing whitespace" flags on `login_page.dart`/`daily_log_form_screen.dart` are the
      documented CRLF-convention signal, not defects.
- [x] PLAN progress row updated (51.5 Done, evidence this file + `69c6b44`).

## 6. Concurrency ledger (what stayed dirty and why)

- `test/features/tracking/presentation/cut_fill_form_screen_test.dart` — **not 51.5's**:
  one real content line (a CF-014 citation = 51.8's lane) plus CRLF-on-disk churn vs an
  LF-convention HEAD. Left dirty for its owning substep per the boundary rule.
- `prev_changes.diff` (workspace-root scratch, 51.2's pre-commit backup) — still present at
  the app repo root; flagged for the 51.10 close-out's workspace hygiene sweep.

## 7. Definition of done

- [x] All inventory sites migrated; grep zero (no survivors, none justified needed).
- [x] Loading-state finders: none existed (§4); full suite green with count+delta stated
      (550+5skip, delta 0).
- [x] `flutter analyze` 0, format clean.
- [x] Findings (this file) + PLAN row updated.

## 8. Handoff

With 51.2/51.3/51.4/51.5 all Done, **51.6 (Material-import sweep & residue check) is
unblocked** — its dependency was 51.2–51.5. 51.9 (dead-file disposition) and 51.10
(verification & close) remain. Note for 51.6: the residue check's grep must anchor
`[^A-Za-z]` per the containment-trap lesson (e.g. `FScaffold(` contains `Scaffold(`);
71→fewer `flutter/material.dart` importers expected, with the four families now at zero.
Run in a fresh chat.
