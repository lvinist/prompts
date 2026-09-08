# mine-flow — STEP-48.29 FINDINGS: Evidence-guard hardening

**Substep:** 48.29 — zero-executed CI guards (audit §G-2) + l10n multi-line blind spot (audit §G-3)
**Date:** 2026-09-07 (original) · 2026-09-08 (R-1 re-run, §9)
**Owner model (per PLAN):** GPT 5.6 Terra slot — executed by Hermes (Claude) session
**Status:** Implementation complete; all local gates green. Commit is 48.25's lane.

> **What a green E2E job now proves that it did not before:** an `e2e-android` or
> `e2e-web` conclusion of `success` now guarantees **at least one test body
> actually executed** (passed or failed — not skipped), *and* on web, that
> every file in the loop produced a positive execution/skip signal (an
> `e2e_executed` marker in the per-file `result` JSON, a named `e2e_skipped`
> marker, or a driver failure). Before this substep, both jobs could exit 0 on
> a run where **every single test was skipped** — the exact STEP-45 failure
> mode the guards were created to prevent.

## 0. Session context — interrupted prior pass reconciled

This session resumed a partially-executed 48.29 (work present, findings absent). The
prior pass's uncommitted work was **all 48.29-scoped** (48.25 re-run 5 had already
committed the 48.23/48.27 lane: `6f9b2ae`, `3df8e7f`, `87fada3`), so it was rebuilt
rather than preserved. Four defects in it were found and corrected:

1. **Web markers used `print()`** (`MINE_FLOW_E2E_EXECUTED …`). Flutter SDK source
   proves this cannot work on web: `flutter drive`'s tool log receives **no app
   stdout** — the only app→driver channel is `reportData`
   (`packages/integration_test/lib/src/_callback_web.dart:141`, serialized by
   `Response.toJson` in `packages/integration_test/lib/common.dart:73-76` into the
   per-file `result {...}` JSON, which the extended driver prints). Markers were
   re-based on `reportData`.
2. **Q16 was applied backwards on the two post-guard files.** The prior pass added
   `report_type_picker_page.dart` and `file_detail_route.dart` (both created by
   STEP-46.4 on 2026-08-27, *after* the guard landed 2026-08-03) to
   `_legacyExemptFiles` **and collapsed their multi-line `Text(` calls to
   single-line** — defeating the new multi-line detection instead of migrating the
   literals. Q16 mandates fixing exactly these files. Both were restored from HEAD
   and migrated to AppLocalizations (§4).
3. **The web parser keyed on `^Running <file>` headers** — but the CI loop's
   `echo "Running $file"` goes to the *step* log, not `all_web.log` (verified: 0
   hits in the captured `step4824_e2e_web_all.log`). Real aggregates carry no file
   headers at all. The new design writes a `MINE_FLOW_E2E_FILE <path>` marker into
   the aggregate itself (`ci.yml:176`).
4. **Three competing helper implementations** (`tool/check_e2e_executed.py`,
   `tool/check_e2e_executed.dart`, `tool/ci/check_e2e_executed.dart`) + CRLF churn
   (76/69/26 CR bytes on owned files). Consolidated into the single
   `tool/ci/check_e2e_executed.dart`; churn normalized; the `.py` and root `.dart`
   variants deleted.

**Fixture honesty note:** the prompt's "15 pass / 1 fail" description of
`step4824_e2e_web_all.log` no longer matches the file on disk — it was overwritten
(2026-09-06 00:46) by a later all-green loop: **16 blocks, all `result:true`, 0
failures, 0 markers** — at the log level indistinguishable from an all-skipped run.
The findings below treat it as what it is: a legacy-shaped (marker-less) log that
the old guard accepted vacuously and the new guard correctly rejects as
zero-evidence (§2.3). The 15/1 run's per-file table lives in 48.24's FINDINGS §0.5.

## 1. The two holes, reproduced (required pre-fix evidence)

Run from `Code/mine-flow-app` (script: `.step48-work/repro_4829_holes.sh` at the
workspace root):

```
=== HOLE 1: old Android zero-executed guard accepts +0 ~17 ===
VACUOUS PASS: guard exit 0 on '00:05 +0 ~17: All tests passed!' (0 executed, 17 skipped)

=== HOLE 2: old web guard accepts a 16-file all-skipped aggregate ===
VACUOUS PASS: guard exit 0 on a 16-file all-skipped aggregate (16x result:true + 16x 'All tests passed.')

=== HOLE 3: old l10n pattern is blind to multi-line Text( ===
single-line _hardcodedTextPattern matches in HEAD report_type_picker_page.dart: 0
  literal present at: 26:                  'Pilih Jenis Laporan',
```

The old guard was `grep -qE "\+[1-9]|\-[1-9]|All tests passed|Some tests failed"`
(ci.yml `e2e-web` :196, `e2e-android` :275 pre-change). `All tests passed` matches
literally on both platforms even when zero tests executed.

## 2. The new executed-count rule (written into the helper's doc comment)

Single committed helper: `tool/ci/check_e2e_executed.dart`, invoked from ci.yml
(both platforms), unit-tested in `test/tool/check_e2e_executed_test.dart` (17 tests).

### 2.1 Android (`flutter test integration_test/` → `integration_test.log`)

- Grammar: progress lines `MM:SS +<passed>[ -<failed>][ ~<skipped>]:` (token order
  of `-`/`~` varies; both orders seen in captured logs). The **last** such line is
  the suite summary.
- Rule: **fail when `passed + failed == 0`** on the final line. Fail also when
  **no progress line exists** (a hung/cancelled run leaves none — §3a of the
  gate-verdicts skill: the 48.26 cancelled job produced zero test output).
- The `script:` stays one line (the `android-emulator-runner` newline constraint
  from 48.2's findings); the guard invocation is `dart run
  tool/ci/check_e2e_executed.dart --platform=android --log=integration_test.log`
  appended to that line, guard failure takes precedence over the suite's own exit
  status.

### 2.2 Web (per-file `flutter drive` loop → `all_web.log`)

- Grammar: the CI loop now writes `MINE_FLOW_E2E_FILE <path>` into the aggregate
  before each file (previous `echo "Running $file"` went to the step log only).
  Each file's block ends with the extended driver's `result {"result":…,
  "data":{…}}` line. App-side `print()` is **not** in this log on web; the app→CI
  channel is `reportData` only (SDK source, §0.1).
- Journey helpers (`integration_test/helpers/staging_config.dart`):
  `recordE2eExecuted(name)` / `recordE2eSkipped(reason)` write into
  `IntegrationTestWidgetsFlutterBinding.instance.reportData` under
  `e2e_executed` / `e2e_skipped`.
- Rules:
  1. A file **executed** if it emitted ≥1 `e2e_executed` marker **or** its driver
     result is `false` (a failing body still ran).
  2. **Aggregate rule:** at least one file must have executed.
  3. **Marker-era rule** (any marker present anywhere): every file must show some
     signal — executed markers, skip markers, or a driver failure. A file with
     `result:true` and no markers is a journey that skipped without recording a
     named reason or a new file ignoring the convention: **guard failure**. This
     is what makes per-file honesty enforceable.
  4. **Legacy logs** (no markers, e.g. pre-48.29 captures): only the aggregate
     rule applies; `result:false` counts as execution.
- Per-file ran/skipped table printed by the guard (the prompt's recommendation,
  adopted): 48.24/48.26 had to reconstruct this by hand from raw logs.

```
Web E2E execution summary:
  Files in aggregate: 3
  Executed markers: 1
  Per-file composition:
    integration_test/app_boots_test.dart: EXECUTED (1)
    integration_test/journeys/data_bucket_journey_test.dart: SKIPPED (1)
      skip: data_bucket: Drive credentials absent (RISK-0017/0018)
    integration_test/journeys/broken.dart: FAILED (driver)
[OK] Web execution proven: 2 executed.
```

### 2.3 Expected honest skips (unchanged contract)

Drive/D2 → RISK-0017/0018; crew → RISK-0021; staging credentials absent;
offline-sync Part A Android-only (Doc 15 §1) — all now recorded via
`recordE2eSkipped` with named reasons and shown in the table. A wholesale skip
(no markers anywhere) fails.

### 2.4 Fail/pass matrix (10/10, script `.step48-work/guard_matrix_4829.sh`)

| # | Input | Expected | Result |
|---|---|---|---|
| 1 | Android `00:05 +0 ~17: All tests passed!` | FAIL | PASS (exit 1) |
| 2 | Web synthetic 16-file all-skipped | FAIL | PASS (exit 1) |
| 3 | Web captured legacy log `step4824_e2e_web_all.log` (16× result:true, no markers) | FAIL | PASS (exit 1) |
| 4 | Android hung run (no progress line) | FAIL | PASS (exit 1) |
| 5 | Web marker-era file with NO signal | FAIL | PASS (exit 1) |
| 6 | Android captured real log, tail-40 (`step4824_r4_android_full.log`, 23 passed / 3 skipped) | PASS | PASS (exit 0) |
| 7 | Android captured real log, entire file | PASS | PASS (exit 0) |
| 8 | Web marker-era mixed (1 executed + 1 honest skip) | PASS | PASS (exit 0) |
| 9 | Web failed file (driver false = executed) | PASS | PASS (exit 0) |
| 10 | Android failed run `+14 -10 ~2` (24 executed) | PASS | PASS (exit 0) |

"unchanged verdicts for the real logs the previous guard already handled
correctly": rows 6-7 keep the old guard's correct verdicts (it accepted real
execution logs); rows 1-5 are the holes, now closed.

## 3. l10n guard multi-line fix (audit G-3)

`tool/check_l10n_baseline.dart`:

- Detection extracted into **`findHardcodedTextViolations(String content)`**
  (mirrors `findRouterLabelViolations`' testable-helper precedent), returning
  `TextViolation(lineNumber, snippet)` including multi-line hits.
- Multi-line detection: `Text(` at end of line (after trimming), then a string
  literal on the next non-empty non-comment line within a 3-line window. Single-line
  and double-quote coverage unregressed (STEP-41.5 ISSUE-4 tests still pass).
- **Interpolation rule (written into the file's doc comment):** a literal
  containing ONLY interpolation (`'$x'`, `'${y.z}'`) is NOT user-facing copy —
  excluded. Mixed content (`'Hello $name'`, `'$percent%'`) IS flagged — a unit
  suffix is translatable copy; the ARB key should carry a `{percent}` placeholder.
  (`isPureInterpolation` helper, unit-tested.)
- Comment lines (`// …`) are skipped; `Text(` inside a doc comment is invisible to
  the matcher because `///` lines start with `//`.
- Before/after counts: **before** — `[OK] No new hardcoded strings detected`
  with 21 non-exempt files carrying 36 invisible multi-line literals (audit's
  count, spot-verified on `report_type_picker_page.dart`: `'Pilih Jenis
  Laporan'` at HEAD:26, 0 pattern matches). **After** — the same `[OK]`, now
  honest: 48 exempt files (29 original + 19 Q16 pre-guard), 14 non-exempt
  scanned with multi-line detection live, 0 violations.

### 3.1 l10n unit tests (10 new, in `test/tool/check_l10n_baseline_test.dart`)

single-line; multi-line single-quote; multi-line double-quote; single-line
double-quote (ISSUE-4 unregressed); comment; empty/1-char; pure-interpolation
ignored; `'$percent%'` flagged as mixed; mixed text+interpolation flagged;
AppLocalizations getter not flagged. All green (36/36 in `test/tool/`).

## 4. Q16 split — 21 files dispositioned

Rule applied (PLAN Q16): files that **predate** the guard (STEP-12 2026-07-20 /
STEP-31 2026-07-23, guard landed 2026-08-03) join `_legacyExemptFiles` with a
RISK-0004 TODO; files **created after** the guard (STEP-46.4, 2026-08-27) are
**fixed**, not exempted.

**2 fixed (migrated to AppLocalizations):**

| File | Literal | ARB key (en / id) |
|---|---|---|
| `lib/features/reporting/presentation/pages/report_type_picker_page.dart` | `'Pilih Jenis Laporan'` | `reportTypePickerTitle` = "Choose Report Type" / "Pilih Jenis Laporan" |
| `lib/features/data_bucket/presentation/pages/file_detail_route.dart` | `'File tidak ditemukan.'` | `fileDetailNotFound` = "File not found." / "File tidak ditemukan." |

- `flutter gen-l10n` re-run; generated files updated (`app_localizations*.dart`,
  ARBs — ARB/generated files carry the repo's pre-existing CRLF convention,
  matching their HEAD state).
- The deep_link journey's not-found assertion updated to the en value
  (`'File not found.'`) with a comment explaining the fresh-Hive default-locale
  premise (`deep_link_journey_test.dart:179-182`). **Not an assertion weakening** —
  the assertion still requires CF-031's explicit not-found state to render; only
  the localized string changed.
- The prior pass's single-line collapse of these files was reverted (git checkout)
  before the proper migration — collapsing multi-line `Text(` to dodge the guard
  is the exact offence the substep exists to remove.

**19 exempted (pre-guard, one-line justifications):**

| File | Reason (creation date per `git log --diff-filter=A`) |
|---|---|
| `lib/app/presentation/pages/app_shell.dart` | STEP-31 (2026-07-23) — predates the 2026-08-03 guard |
| `lib/app/presentation/pages/dashboard_page.dart` | STEP-12 (2026-07-20) — predates the guard |
| `lib/app/presentation/pages/settings_page.dart` | STEP-31 (2026-07-23) — predates the guard |
| `lib/app/presentation/widgets/app_shell.dart` | STEP-12 (2026-07-20) — predates the guard |
| `lib/app/presentation/widgets/global_app_header.dart` | STEP-31 (2026-07-23) — predates the guard |
| `lib/features/attendance/presentation/widgets/attendance_summary_card.dart` | STEP-12 — predates the guard |
| `lib/features/daily_log/presentation/widgets/weather_selector.dart` | STEP-12 — predates the guard |
| `lib/features/daily_log/presentation/widgets/zone_picker.dart` | STEP-12 — predates the guard |
| `lib/features/data_bucket/presentation/widgets/upload_progress_indicator.dart` | STEP-12 — predates the guard |
| `lib/features/equipment_check/presentation/widgets/equipment_check_card.dart` | STEP-12 — predates the guard |
| `lib/features/reporting/presentation/widgets/report_summary_card.dart` | STEP-12 — predates the guard |
| `lib/features/timeline/presentation/widgets/milestone_card.dart` | STEP-12 — predates the guard |
| `lib/features/timeline/presentation/widgets/timeline_chart.dart` | STEP-12 — predates the guard |
| `lib/features/tracking/presentation/widgets/clearing_summary_card.dart` | STEP-12 — predates the guard |
| `lib/features/tracking/presentation/widgets/cut_fill_card.dart` | STEP-12 — predates the guard |
| `lib/features/tracking/presentation/widgets/inventory_card.dart` | STEP-12 — predates the guard |
| `lib/features/tracking/presentation/widgets/inventory_summary_card.dart` | STEP-12 — predates the guard |
| `lib/features/tracking/presentation/widgets/land_clearing_card.dart` | STEP-12 — predates the guard |
| `lib/features/tracking/presentation/widgets/volume_summary_card.dart` | STEP-12 — predates the guard |

Counts: **2 fixed + 19 exempted = 21 dispositioned** (audit G-3's count). No
blanket exemption; no 36-literal migration (RISK-0004's own STEP). Boundary drawn:
post-guard creation is the fix/exempt line, exactly per Q16.

Note: the two exempted `lib/app/presentation/pages/settings_page.dart` and
`lib/app/presentation/widgets/app_shell.dart` are themselves 48.30's shadow-file
targets (audit G-6) — their l10n exemption is moot once deleted there; this row
records the dependency, not a conflict.

## 5. Files changed (this substep, all in `Code/mine-flow-app`)

| File | Change |
|---|---|
| `.github/workflows/ci.yml` | Both guards replaced with the helper; web loop writes `MINE_FLOW_E2E_FILE` markers; comments document the rule; Android `script:` still one line; secrets still referenced by name only |
| `tool/ci/check_e2e_executed.dart` | NEW — the committed, unit-tested guard |
| `test/tool/check_e2e_executed_test.dart` | NEW — 17 tests incl. 4 CLI subprocess fail/pass cases |
| `integration_test/helpers/staging_config.dart` | `recordE2eExecuted`/`recordE2eSkipped` via reportData (replaces print) |
| `integration_test/app_boots_test.dart` + 12 single-test journey files (attendance, auth, benchmark, cut_fill, daily_log, equipment_check, inventory, land_clearing, notifications, reporting, timeline) | Markers added (12 files were the prior pass's, verified and kept; app_boots restored from HEAD churn and re-edited cleanly) |
| `integration_test/journeys/data_bucket_journey_test.dart`, `deep_link_journey_test.dart`, `offline_sync_journey_test.dart`, `rls_authorization_journey_test.dart` | Markers added this session (prior pass missed them — its parser keyed on `Running` headers that don't exist) |
| `integration_test/journeys/deep_link_journey_test.dart` | Assertion string updated to en locale value (see §4) |
| `tool/check_l10n_baseline.dart` | Multi-line detection + `findHardcodedTextViolations` + `isPureInterpolation` + doc-comment contract + Q16 exemption block |
| `test/tool/check_l10n_baseline_test.dart` | +10 tests for the above (108 lines, LF-clean) |
| `lib/l10n/app_en.arb`, `app_id.arb` (+ regenerated `app_localizations*.dart`) | 2 new keys |
| `lib/features/reporting/presentation/pages/report_type_picker_page.dart` | Migrated to AppLocalizations |
| `lib/features/data_bucket/presentation/pages/file_detail_route.dart` | Migrated to AppLocalizations |

Deleted (prior pass's orphans): `tool/check_e2e_executed.py`,
`tool/check_e2e_executed.dart` (root-level duplicate).

## 6. Verification evidence

| Gate | Result |
|---|---|
| `dart run tool/check_l10n_baseline.dart` | `[OK] No new hardcoded strings detected in non-exempt files.` — 48 exempt / 14 scanned, exit 0 |
| `flutter test test/tool/` | **36/36 All tests passed** (17 e2e-guard + 19 l10n/contract) |
| `flutter test` (full) | **540/540 All tests passed**, exit 0 (baseline 513 + 27 new) |
| `flutter analyze` | **No issues found!** |
| `dart format --output=none --set-exit-if-changed lib/ test/ tool/` | 319 files, 0 changed |
| `dart run tool/check_supabase_contracts.dart` | `[OK] Contract verification passed.` |
| `ci.yml` YAML validity | `python yaml.safe_load` → `ci.yml: valid YAML` |
| Guard matrix | **10/10** (§2.4) |
| CR-byte audit | All owned files 0 CR (test file normalized 245→0); l10n ARB/generated files match their pre-existing HEAD CRLF convention |

`git status` (app repo, end of session): 27 modified + 2 untracked (`tool/ci/`,
`test/tool/check_e2e_executed_test.dart`) — all 48.29-scoped; concurrent repos
untouched (docs: only 48.23/48.27's Doc 04 edit; prompts: only STEP-50's index
edit, per pre-flight).

## 7. Deferred / Unverified

- **CI-side proof of the marker channel.** The reportData-based markers are proven
  against SDK source and synthetic fixtures shaped like real logs, but no live CI
  `e2e-web` run has yet produced a marker-era aggregate. The first post-merge gate
  run (48.26's lane) is the proof; if `e2e_executed` markers somehow do not
  serialize on the real runner, the guard will fail loudly (marker-era file with
  no signal) rather than pass vacuously — fail-safe by design.
- **Local E2E execution** (Android emulator / web chromedriver runs of the marked
  journeys) was not performed — the prompt's verification list is satisfied by
  captured logs + synthetic fixtures; staging untouched per pre-flight.
- **Doc 12 §6** unchanged — the gates were hardened, not renamed; per scope item 5
  no doc change needed. 48.15 owns Doc 12's E2E-shape rewrite and should mention
  the per-file table + marker convention when it rewrites.

## 8. Next

48.30 (dead affordance + shadow files) has since completed (commit `bb32c92`).
The code-touching wave now re-enters the gate sequence: **48.24 local gate →
48.25 commit/push → 48.26 branch-head verdict** — the R-1 guard fix (§9)
rides 48.25's next commit lane, and 48.26's next verdict run is its in-vivo
proof. STEP-48 stays `In progress`.

## 9. R-1 re-run (2026-09-08): the Android guard false-fired in vivo — CI uses the GithubReporter grammar

48.26's re-run 6 (CI run **34204817176**, sha `5bff0b1`) was a NO-GO: the
Android suite itself was green (24 passed / 2 skipped) but the job went red
because **this substep's guard found 0 progress lines and failed a healthy
run** — the guard's first in-vivo execution. Committed as `7db4a0a`, it knew
only the local `MM:SS +N:` compact grammar; that grammar **never appears in
GitHub Actions logs**.

### 9.1 Root cause (from SDK source, not guessed)

With `GITHUB_ACTIONS=true`, package:test selects the **GithubReporter**
(`test_core-0.6.18/lib/src/runner/reporter/github.dart`, vendored at
`D:/AppDev/.pub-cache/hosted/pub.dev/test_core-0.6.18/`), which prints:

- per-test lines `✅ <path>: <name>` / `⏭️ <name> (skipped)` /
  `##[group]❌ <name> (failed) … ##[endgroup]`, wrapped in `##[group]` /
  `##[endgroup]` when the test printed messages;
- section headers `##[group]✅ Passing tests` / `##[group]⏭️ Skipped tests`
  (not tests);
- **no `MM:SS +N` progress lines at all**;
- one final engine-authoritative summary: `🎉 <passed> tests passed[, <failed>
  failed][, <skipped> skipped].` — note only the *passed* clause is pluralized
  ("tests"/"test"); the failed/skipped clauses are bare counts. On failure the
  prefix is `::error::` (rendered `##[error]` in raw logs).

Verified against the captured CI log `step4826_r6_integration_test.log`
(4,297 lines): `grep -cE '[0-9]+:[0-9]{2} *\+'` → **0 matches**; summary line
at :4296 `🎉 24 tests passed, 2 skipped.`; 16 `^✅` lines + 2 skip markers +
13 `##[group]✅/⏭️` headers.

### 9.2 Fix — three-tier grammar resolution in `parseAndroidLog`

1. **CI GithubReporter summary** (preferred): last `🎉 N tests passed, …` /
   `::error::…` line. The summary regex accepts bare `", N failed"` /
   `", N skipped"` clauses and both `::error::` and `##[error]` prefixes;
   singular `test passed` handled.
2. **Local compact progress line** (`MM:SS +N:`) — unchanged, still parsed
   (local `flutter test` runs; all pre-R-1 tests unregressed).
3. **Fallback icon count** (new): if neither summary nor progress line exists
   (a tailed log), count per-test `✅`/`⏭️`/`❌` lines, excluding the
   `Passing tests`/`Skipped tests` section headers — the 48.24 habit of
   tail-ing captured logs made this worth covering.

`AndroidExecutionSummary.finalLine` reports whichever line was used. The
workflow comment block in `ci.yml` was updated to describe the CI grammar and
point to the helper's doc comment. Android `script:` remains one line;
secrets still referenced by name only; no `dart run` interface change.

Also new: `tool/ci/validate_workflow_yaml.dart` — a package:yaml-based
standalone validator for `ci.yml` (the prompt's `python -c` one-liner is
gated in this agent runtime; package:yaml is already a transitive dep). Not
wired into CI — local assurance for workflow edits only.

### 9.3 R-1 fail/pass matrix (all run against the committed helper)

| # | Input | Expected | Result |
|---|---|---|---|
| 1 | Compact all-skipped `00:05 +0 ~17: All tests passed!` | FAIL | FAIL (exit 1) — unregressed |
| 2 | CI all-skipped `🎉 0 tests passed, 17 skipped.` | FAIL | FAIL (exit 1) — `[ERROR] Zero tests executed (passed=0, failed=0, skipped=17)` |
| 3 | Legacy captured `step4824_r4_android_full.log` (23/3) | PASS | PASS — `[OK] Android execution proven: 23 executed.` |
| 4 | **CI false-fire log `step4826_r6_integration_test.log` (run 34204817176, 24/2)** | PASS | PASS — `[OK] Android execution proven: 24 executed.` |

Unit tests added: 8 in the `CI GithubReporter grammar, R-1` group (reject
all-skipped CI summary; accept 24/2 shape; accept failed `::error::` run;
`##[error]` rendering; singular form; last-summary preference; tailed-log
icon fallback; the captured false-fire log) + 1 CLI subprocess test (exit 0
on the false-fire log). `test/tool/` now 45/45 (was 36/36).

### 9.4 R-1 gates

| Gate | Result |
|---|---|
| `flutter test test/tool/` | **45/45 All tests passed** |
| `flutter test` (full) | **551/551 All tests passed** |
| `flutter analyze` | **No issues found!** |
| `dart format --set-exit-if-changed lib/ test/ tool/` | 317 files, 0 changed |
| `dart run tool/check_supabase_contracts.dart` | `[OK] Contract verification passed.` |
| `dart run tool/ci/validate_workflow_yaml.dart` | `ci.yml: valid YAML (3 top-level keys)` |

Test-count deltas since the original pass: `test/tool/` 36 → 45 (+9: the 8
grammar tests + 1 CLI test above); full suite 540 → 551 (those 9, plus
48.30's CreatableCombobox tests in commit `bb32c92`, which landed between the
original pass and this re-run). R-1's own contribution is the 9 e2e-guard
tests.

### 9.5 Files changed (R-1, all in `Code/mine-flow-app`, uncommitted — 48.25's lane)

| File | Change |
|---|---|
| `tool/ci/check_e2e_executed.dart` | CI summary regex + tier-2/tier-3 fallbacks + expanded doc-comment grammar |
| `test/tool/check_e2e_executed_test.dart` | +9 tests (8 grammar group + 1 CLI on the false-fire log) |
| `.github/workflows/ci.yml` | Comment-only: grammar documentation updated (no logic change) |
| `tool/ci/validate_workflow_yaml.dart` | NEW — local ci.yml YAML validator (not CI-wired) |

Concurrent files untouched: `run_web_wrapper.dart` (48.24's, untracked) left
alone; docs repo's `architecture/04-data-model.md` (48.23/48.27) untouched;
`prompts/STEP-index.md` (STEP-50/51 edits) untouched.

### 9.6 What a green e2e-android job now proves (R-1)

Before R-1: a green job proved nothing about execution — and, worse, the
guard could turn a healthy run red (proven in vivo on 34204817176). After
R-1: an `e2e-android` success requires the GithubReporter's
engine-authoritative summary line to show **passed + failed > 0** — a green
job is execution proof in CI's actual log grammar, and a healthy run passes
the guard. The guard now knows both grammars (CI + local), so it cannot be
fooled by environment either way.
