# mine-flow — STEP-51.1 FINDINGS: Register re-scope & sweep inventory (gate)

**Substep:** 51.1 — the STEP's honesty gate
**Date:** 2026-09-09
**Owner model (per PLAN):** Hermes/Claude Opus 4.8
**Status:** Complete — no application-code changes; durable record corrected, inventory built.
**Branch:** `step-0051-ui-debt-closure` cut from `64b054a` (master synced, clean). Index row
flipped to `In progress` and pushed (`4f69cf9`). Register appendix committed and pushed
(`6e6a65d`).

## 1. Lifecycle & bookkeeping (done first)

- `mine-flow-app`: `master` clean at `64b054a`, synced with origin → cut
  `step-0051-ui-debt-closure`. No code changes on it (this substep owns none).
- `prompts/`: on `main`, pulled, clean → STEP-51 row flipped `Planned`→`In progress`, committed
  (`STEP-51 In progress`), duplicate scan empty, pushed (`4f69cf9`).
- Register appendix appended to
  `prompts/003-release-readiness-integration-scale/step-0046/mine-flow-STEP-46.3-FINDINGS.md`
  and pushed (`6e6a65d`). **Append-only proven:** `git diff` shows 85 insertions / 0 deletions
  (the file is CRLF-convention; the appendix was appended via byte-safe `cat` after a
  whole-file LF rewrite was caught and reverted — see §7).

## 2. Count reconciliation — PLAN pre-flight vs re-derived (branch head, 2026-09-09)

| Claim | PLAN (2026-09-09) | Re-derived | Verdict |
|---|---|---|---|
| `showSnackBar(` | 35 sites / 13 files | **35 / 13** | match |
| `SnackBar(` ctor | 35 (naive grep 70) | 35 (naive reads 70) | match — trap confirmed |
| `Scaffold(` | 24 files | **24 files / 35 sites** (naive grep 27 files/38 — `FScaffold(` inflation) | match |
| `AppBar(` | 14 files / 19 sites | **14 / 19** (naive 27 files incl. noise) | match |
| `CircularProgressIndicator(` | 22 files / 25 sites | **22 / 25** | match |
| `FScaffold(` existing reference uses | 3 | **3** (settings, report_config, report_type_picker) | match |
| `FHeader` existing uses | 9 | **9** (7 `FHeader(` root-style + 2 `FHeader.nested`) | match |
| Material importers | 71 (audit: 73) | **71 of 238** lib files | match; total files drifted 240→238 |
| `Icons.` | 0 | **0** (anchored `[^A-Za-z]Icons\.`; naive reads 282 = all `LucideIcons.`) | match |
| CF ids cited under `test/` | 13 | **13** | match |
| CF ids under `integration_test/` | 23 | **23** | match |
| `TODO(STEP-46.4)` markers | 0 | **0** | match |
| Tiered findings | **84** (80 Widget) | **82** (75 Widget, 3 Widget/bloc, 1 Widget/integration, 1 Widget/route, 1 Static guard, 1 `flutter analyze`); no-test lines **15** (13 "No test feasible" + 2 "No automated contrast") | **PLAN off by 2** — it counted CF-075/076's contrast lines as tiered. Corrected in the appendix. |
| Dead files "all 7 already deleted by 48.30" | claimed deleted | **FALSE — see §5.** All 10 real files still exist on disk. | **PLAN pre-flight error** |

Baseline gates at branch head (no code changed this substep): `flutter analyze` — **No issues
found** (143s). `flutter test` — **548 passed + 5 skipped, 0 failed** ("All tests passed!",
2:18). The prompt's "expect 553 passed" and STEP-50's "553/553" count the 5 guard-fixture skips
differently (548 executed-green + 5 skipped = 553 accounted); no deviation to fix — recorded as
the count-grammar note for 51.10.

## 3. Sweep inventory (D2/D3) — 114 Material call sites

ForUI 0.26.0 targets verified in `D:/AppDev/.pub-cache/hosted/pub.dev/forui-0.26.0/lib/src/widgets/`:
`toast/toast.dart` (`FToast`), `toast/toaster.dart` (`FToaster`), `scaffold.dart` (`FScaffold`),
`progresses/circular_progress.dart` (`FCircularProgress`), `header/` (`FHeader` root variant =
start-aligned title; `FHeader.nested` = centre-aligned; both exist and are already used in-repo).

Behaviour flag per D3: **yes** = dismiss/timeout/callback semantics change (widget test
required); **no** = pure container swap (existing tests must not regress).

### 3.1 `showSnackBar`/`SnackBar` → `FToast`/`FToaster` — 35 sites, 13 files (51.2)

All sites are behaviour-flag **yes** (toast dismissal/duration/action semantics replace
snackbar's; 51.2 writes widget tests wherever dismissal/duration/action is asserted).

| File (lib/…) | `showSnackBar(` lines |
|---|---|
| core/presentation/widgets/confirm_destructive_action.dart | 18 |
| features/attendance/presentation/pages/attendance_form_page.dart | 64, 73 |
| features/attendance/presentation/pages/attendance_screen.dart | 94, 114 |
| features/benchmark/presentation/pages/benchmark_form_screen.dart | 126, 130, 493 |
| features/daily_log/presentation/pages/daily_log_form_screen.dart | 130, 138 |
| features/data_bucket/presentation/pages/file_detail_page.dart | 61, 329, 339, 352, 364 |
| features/data_bucket/presentation/pages/upload_file_page.dart | 169, 193, 223, 233, 245, 285, 293 |
| features/data_bucket/presentation/widgets/file_card.dart | 49 |
| features/equipment_check/presentation/pages/equipment_check_form_screen.dart | 121, 134 |
| features/settings/presentation/pages/settings_page.dart | 371 |
| features/tracking/presentation/pages/cut_fill_form_screen.dart | 117, 152, 160 |
| features/tracking/presentation/pages/inventory_item_entry_screen.dart | 79, 168, 176 |
| features/tracking/presentation/pages/land_clearing_entry_screen.dart | 120, 153, 161 |

(Each site pairs with a `SnackBar(` ctor at an adjacent line — 35 ctor uses in the same 13
files. `ScaffoldMessenger` uses retire with this family; 51.4 depends on 51.2 for ordering.)

### 3.2 `AppBar` → `FHeader` root/nested — 19 sites, 14 files (51.3)

Behaviour flag **no** for title-only AppBars (pure container swap); **verify** for the eight
sites with leading back/action affordances (callbacks preserved, finders change — existing
screen tests + journeys assert on semantics, watch them).

| File (lib/…) | `AppBar(` lines |
|---|---|
| features/attendance/presentation/pages/attendance_screen.dart | 139 |
| features/benchmark/presentation/pages/benchmark_form_screen.dart | 143, 158 |
| features/benchmark/presentation/pages/benchmark_list_screen.dart | 79 |
| features/daily_log/presentation/pages/daily_log_form_screen.dart | 164, 226 |
| features/daily_log/presentation/pages/daily_log_list_screen.dart | 138 |
| features/data_bucket/presentation/pages/file_detail_page.dart | 81 |
| features/data_bucket/presentation/pages/upload_file_page.dart | 61 |
| features/equipment_check/presentation/pages/equipment_check_form_screen.dart | 107 |
| features/equipment_check/presentation/pages/equipment_history_screen.dart | 126 |
| features/notifications/presentation/pages/notification_list_page.dart | 53 |
| features/timeline/presentation/pages/timeline_page.dart | 94 |
| features/tracking/presentation/pages/cut_fill_form_screen.dart | 186, 248 |
| features/tracking/presentation/pages/inventory_item_entry_screen.dart | 205, 286 |
| features/tracking/presentation/pages/land_clearing_entry_screen.dart | 187, 240 |

Reference pattern already in-repo: 7 `FHeader(` uses (settings, report_config,
report_type_picker, data_bucket_list, cut_fill_list, inventory_dashboard, land_clearing_list —
mostly wrapped in `PreferredSize(kToolbarHeight)`) and 2 `FHeader.nested` (attendance_form,
upload_file).

### 3.3 `Scaffold` → `FScaffold` — 35 sites, 24 files (51.4)

Behaviour flag **no** (pure container swap) — except `app_shell.dart:268` (shell root; watch
the "Material ancestor" class 48.22 hit twice) and the two `file_detail_route.dart` sites (48/55,
route-level scaffold wrapping — verify nested-scaffold behaviour).

| File (lib/…) | `Scaffold(` lines |
|---|---|
| app/presentation/pages/app_shell.dart | 268 |
| app/presentation/pages/dashboard_page.dart | 33 |
| app/presentation/pages/group_landing_page.dart | 41 |
| features/attendance/presentation/pages/attendance_form_page.dart | 83 |
| features/attendance/presentation/pages/attendance_screen.dart | 136 |
| features/auth/presentation/pages/login_page.dart | 73 |
| features/benchmark/presentation/pages/benchmark_form_screen.dart | 140, 155 |
| features/benchmark/presentation/pages/benchmark_list_screen.dart | 76 |
| features/daily_log/presentation/pages/daily_log_form_screen.dart | 155, 161, 223 |
| features/daily_log/presentation/pages/daily_log_list_screen.dart | 135 |
| features/data_bucket/presentation/pages/data_bucket_list_page.dart | 63 |
| features/data_bucket/presentation/pages/file_detail_page.dart | 78 |
| features/data_bucket/presentation/pages/file_detail_route.dart | 48, 55 |
| features/data_bucket/presentation/pages/upload_file_page.dart | 60, 309 |
| features/equipment_check/presentation/pages/equipment_check_form_screen.dart | 104 |
| features/equipment_check/presentation/pages/equipment_history_screen.dart | 123 |
| features/notifications/presentation/pages/notification_list_page.dart | 50 |
| features/timeline/presentation/pages/timeline_page.dart | 91 |
| features/tracking/presentation/pages/cut_fill_form_screen.dart | 177, 183, 245 |
| features/tracking/presentation/pages/cut_fill_list_screen.dart | 91 |
| features/tracking/presentation/pages/inventory_dashboard_screen.dart | 74 |
| features/tracking/presentation/pages/inventory_item_entry_screen.dart | 196, 202, 283 |
| features/tracking/presentation/pages/land_clearing_entry_screen.dart | 178, 184, 237 |
| features/tracking/presentation/pages/land_clearing_list_screen.dart | 90 |

Reference: 3 existing `FScaffold(` uses (settings_page:37, report_config_page:51,
report_type_picker_page:20) — note two of those files also appear above with legacy `Scaffold(`
counts excluded; settings/report pages are the migration exemplars.

### 3.4 `CircularProgressIndicator` → `FCircularProgress` — 25 sites, 22 files (51.5)

Behaviour flag **no** (pure visual swap). Trap: loading-state tests matching on widget type
must be updated to `FCircularProgress` (update what they look for, not what they prove).

| File (lib/…) | lines |
|---|---|
| features/attendance/presentation/pages/attendance_form_page.dart | 120, 284 |
| features/attendance/presentation/pages/attendance_screen.dart | 228 |
| features/auth/presentation/pages/login_page.dart | 161 |
| features/benchmark/presentation/pages/benchmark_form_screen.dart | 144 |
| features/benchmark/presentation/pages/benchmark_list_screen.dart | 131, 272 |
| features/daily_log/presentation/pages/daily_log_form_screen.dart | 156 |
| features/daily_log/presentation/pages/daily_log_list_screen.dart | 208 |
| features/daily_log/presentation/widgets/auto_save_indicator.dart | 56 |
| features/daily_log/presentation/widgets/zone_picker.dart | 60 |
| features/data_bucket/presentation/pages/data_bucket_list_page.dart | 170 |
| features/data_bucket/presentation/pages/file_detail_route.dart | 49 |
| features/equipment_check/presentation/pages/equipment_check_form_screen.dart | 146, 285 |
| features/equipment_check/presentation/pages/equipment_history_screen.dart | 308 |
| features/notifications/presentation/pages/notification_list_page.dart | 82 |
| features/reporting/presentation/pages/report_config_page.dart | 162 |
| features/timeline/presentation/pages/timeline_page.dart | 146 |
| features/tracking/presentation/pages/cut_fill_form_screen.dart | 178 |
| features/tracking/presentation/pages/cut_fill_list_screen.dart | 176 |
| features/tracking/presentation/pages/inventory_dashboard_screen.dart | 150 |
| features/tracking/presentation/pages/inventory_item_entry_screen.dart | 197 |
| features/tracking/presentation/pages/land_clearing_entry_screen.dart | 179 |
| features/tracking/presentation/pages/land_clearing_list_screen.dart | 177 |

**Inventory total: 35 + 19 + 35 + 25 = 114 sites across 27 distinct files** (the PLAN's "~116
across ~30 files" was close; the exact per-family file sets overlap).

## 4. 46.4 coverage matrix (D4) — all 97 findings accounted for

Re-derived covered seed (`grep -roE 'CF-[0-9]+' test --include='*.dart' | cut -d: -f2 | sort -u`):
13 ids — CF-001, CF-002, CF-003, CF-005, CF-015, CF-017, CF-029, CF-032, CF-056, CF-059,
CF-063, CF-078, CF-079 (citing files listed in the register appendix).

The prompt's "84 tiered, buckets sum to 84" premise was off by two (§2): true tiered = 82, and
one covered id (CF-056) carries a no-test line. The matrix therefore accounts for **all 97**:
**covered 13 · will cover 57 · not covered 27 = 97.** Among the 82 tiered: covered 12, will
cover 57, not covered 13 = 82.

**Will cover (57)** — behaviour-carrying per D3/D4 (validation, gating, data flow, callbacks,
dismiss/timeout), 51.8 writes each with its CF id in a comment:

CF-004, CF-006, CF-007, CF-008, CF-009, CF-010, CF-011, CF-012, CF-013, CF-014, CF-016,
CF-018, CF-019, CF-020, CF-021, CF-022, CF-023, CF-024, CF-025, CF-026, CF-027, CF-028,
CF-030, CF-031, CF-033, CF-034, CF-035, CF-036, CF-037, CF-038, CF-039, CF-040, CF-041,
CF-042, CF-043, CF-044, CF-045, CF-047, CF-048, CF-049, CF-050, CF-051, CF-053, CF-054,
CF-055, CF-058, CF-060, CF-066, CF-068, CF-069, CF-070, CF-071, CF-073, CF-074, CF-077,
CF-084, CF-097.

(Note CF-043's test is authored by 51.7 as part of the structural fix; 51.8 verifies the
citation rather than duplicating. CF-084's reduced-motion/duration assertions are the one
"will cover" that is performance-shaped — 51.8 may reduce it to the no-throw-on-dispose
assertion if timer-based duration assertions prove flaky, recording the reduction.)

**Not covered (27)** — one-line reasons:

| IDs | Reason |
|---|---|
| CF-046, CF-067 | Colour-resolution asserts (badge/severity palettes) — visual token compliance, no behaviour; Doc 07 token review covers it. |
| CF-052, CF-082 | Chip selected-variant/scroll-cue asserts — visual state rendering, no behaviour. |
| CF-064 | Focus-indicator decoration — visual; keyboard activation already covered by interaction tests elsewhere. |
| CF-065 | Spacer/layout geometry — visual. |
| CF-072 | Label-clipping at 360dp — visual layout; the resolved-names half rides CF-069/CF-070's tests. |
| CF-080, CF-081, CF-083 | Layout geometry (reachability, width constraint, overflow) — visual; surface already exercised by existing screen tests. |
| CF-085 | Motion-duration budget — manual/visual per its own tier line ("manual for the rest"). |
| CF-087 | This STEP's own scope — analyzer gate + the behaviour tests 51.2–51.5/51.7 write ARE its tier; no separate test. |
| CF-090 | Hardcoded version string — static copy; optional per its own tier line, low value. |
| CF-057, CF-061, CF-062 | "No test feasible" per register (static copy consistency). |
| CF-075, CF-076 | "No automated contrast test feasible" per register (pixel rendering); static token half verified in 51.6's import sweep. |
| CF-086, CF-088, CF-089, CF-091, CF-092, CF-095, CF-096 | "No test feasible" per register (visual/token/cosmetic/format). |
| CF-093 | "No test feasible if removed" — the dead plumbing was removed; nothing to test. |
| CF-094 | "No test feasible — refactor; verify responsive behaviour manually." |

(CF-056 is counted in **covered** despite its no-test line — it is cited in
`login_page_test.dart` twice.)

## 5. Dead-file dispositions (D6) — **the PLAN's premise was false; 51.9 is a real deletion job**

The PLAN's pre-flight claimed "all 7 candidate files already deleted by 48.30; 51.9 reduces to
verify-and-record." **Wrong.** 48.30's own findings (§4) only *recommended* deletion in
STEP-51 — it deleted just the two shadowing files (`lib/app/presentation/pages/settings_page.dart`,
`lib/app/presentation/widgets/app_shell.dart`, commit `bb32c92`). The PLAN's verification
checked the audit's literal top-level paths (`lib/tracking.dart`, `lib/notification_badge.dart`,
…) — which **never existed**: the audit's greps hit basename noise (e.g.
`features/benchmark/domain/entities/benchmark.dart` for "benchmark.dart"), the same trap 48.30
documented. All the real files still exist on the branch head.

True unreferenced set (verified with `^(import|export|part)` grammar across
`lib test integration_test`, exact-path — basename-noise-proof):

| File | Disposition for 51.9 |
|---|---|
| `lib/features/tracking/tracking.dart` (barrel, 19 lines) | Delete — 0 imports anywhere. |
| `lib/features/benchmark/benchmark.dart` (barrel) | Delete — 0 imports (all `benchmark.dart` hits resolve to `entities/benchmark.dart`). |
| `lib/features/data_bucket/data_bucket.dart` (barrel, 2 lines) | Delete — 0 imports outside itself. |
| `lib/features/tracking/data/data.dart`, `.../domain/domain.dart` | Delete together with their barrel (only importer is the dead barrel). |
| `lib/features/data_bucket/data/data.dart`, `.../domain/domain.dart` | Delete together with their barrel. |
| `lib/features/data_bucket/data/models/hive/geospatial_file_hive_adapter.dart` | Delete-or-merge decision: **duplicate `GeospatialFileModelAdapter` class** (typeId 13 here vs the registered core typeId 7 in `lib/core/offline/adapters/model_adapters.dart:115`; `hive_service.dart` registers only typeId 7). Never registered, never imported except via the dead `data/data.dart` barrel. |
| `lib/features/notifications/presentation/widgets/notification_badge.dart` | 48.30: "keep pending product intent — or delete if notifications confirms no planned use." 51.9 asks the owner; default delete. |
| `lib/features/reporting/presentation/widgets/report_type_card.dart` | Same — reporting uses the migrated report-type picker page; default delete. |
| `lib/app/presentation/models/app_nav_model.dart` (28 lines: `AppNavItem`, `AppNavGroup`) | **New finding — not in 48.30's list.** Unreferenced since STEP-30.1 (the shell defines its own `_SidebarItemConfig`/`_SidebarSection` at `app_shell.dart:60–83`); dead model duplicate. Default delete. |

Also carried for 51.9 (from 48.30 §3): `tool/check_l10n_baseline.dart:86–87` still lists the two
48.30-deleted shadow paths in `_legacyExemptFiles` (inert; guard prints 46 exempt). One-line
cleanup opportunity in the same lane.

**D6 is corrected accordingly:** 51.9 = delete the 3 barrels + 4 barrel-twin files + resolve the
duplicate adapter + owner decision on the 2 product-intent widgets + the new `app_nav_model.dart`
+ l10n-guard entry cleanup — then verify. The PLAN's pre-flight bullet has been amended (see §7).

## 6. CF-043 confirmation

Two independent `CreatableCombobox<String>` writing `record.method` confirmed at
`land_clearing_entry_screen.dart:372` and `:485` (the prompt's :373/:486 drifted by one —
re-locate on branch head), both fed by `_clearingMethods` (`:98`). 48.30 already made the
widget selection-only (`onCreateNew == null` → no create tile), so the structural remainder for
51.7 is exactly the register's ask: one shared control, both tabs editing one normalised value,
widget test asserting it. Related recorded decision (48.30 §1): empty-state copy for the merged
control — Doc 07 has no empty-state pattern; if 51.7 adds copy it must pass the l10n guard.

## 7. Process notes & escalations

- **CRLF near-miss on the register:** the first appendix write normalized the whole CRLF file to
  LF (946-line diff). Caught by the append-only verification, reverted via `git checkout --`,
  re-appended byte-safe (`cat` of a CRLF-converted scratch file). Final diff: 85 insertions,
  0 deletions. Lesson: `write_file` rewrites whole files — never use it on a CRLF-convention
  archived file; append via shell.
- **Two approval-gated script calls timed out** (register parsing; CRLF count) — re-derived the
  same data through grep/awk pipelines instead. No result depends on the blocked calls.
- **PLAN amended (docs-true):** the false D6 pre-flight bullet now states the truth and points
  at this findings file; a Substep progress table was added (51.1 → Done).
- No ADR needed (D5 holds: every family has its ForUI 0.26 equivalent, verified in pub cache).
  No risks.yml changes — the only new debt-shaped item (duplicate Hive adapter class) is
  dispositioned in §5 and owned by 51.9.

## 8. Definition-of-done check

- [x] Branch `step-0051-ui-debt-closure` cut; index row `In progress`, pushed (`4f69cf9`).
- [x] Register appendix appended (85 insertions / 0 deletions proven); CF-087/CF-043/46.4 truth
      recorded; pushed (`6e6a65d`).
- [x] Sweep inventory complete: 114 sites, per-family tables with lines, ForUI targets
      (pub-cache-verified) and behaviour flags.
- [x] Coverage matrix complete: 97/97 accounted (13 covered + 57 will-cover + 27 reasons);
      prompt's "84" premise corrected to the honest 82 tiered.
- [x] Dead-file dispositions recorded — with the D6 premise falsification and the real
      deletion list for 51.9.
- [x] Findings file written; PLAN progress row updated + false pre-flight corrected.
- [x] Baselines recorded: `flutter analyze` 0 issues; `flutter test` 548 passed + 5 skipped
      (the 553 baseline with skip-grammar reconciled).

## 9. Handoff

Next: **"run substep 51.2"** (SnackBar→FToast, Gemini 3.1 Pro) in a fresh chat. 51.3/51.5/51.7/
51.8/51.9 also depend only on 51.1 and are parallelizable; 51.4 must follow 51.2
(ScaffoldMessenger ordering). 51.10 closes. Escalation-worthy items for successors: the
duplicate `GeospatialFileModelAdapter` (data-integrity-shaped — 51.9 must not leave both
registered), and any Material-ancestor failures in 51.4's shell swap (48.22 precedent).
