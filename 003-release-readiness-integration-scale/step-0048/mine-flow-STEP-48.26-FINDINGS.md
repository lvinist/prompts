# mine-flow — STEP-48.26 Findings: Branch-Head CI Gate Run & Verdict

**Date:** 2026-09-08 (re-run 7)
**Executor:** GPT 5.6 Terra lane (per PLAN model assignment; executing agent Hermes)
**Branch:** `step-0048-runtime-evidence`
**Head sha:** `d53fb7e21f2299eb6b65a3aa4e72dc48d851a1eb`
**Run:** [`34225431645`](https://github.com/lvinist/mine-flow-app/actions/runs/34225431645) — attempt 1, `push`, completed **`success`**
**Supersedes:** the 2026-09-08 re-run 6 record (run `34204817176`, sha `5bff0b1`), **retained unmodified below as §0a** (its registers R-1/R-2 are the two defects this run discharges); re-run 5 (`34192851645`, `f14885e`) now in §0b; re-run 4 (`33953949570`, `c73a00e`) in §1–§17; re-run 3 (`33879989164`, `9288168`) in §11; re-run 2 (`33734562106`, `310fea5`) in §12; re-run 1 (`33626548011`, `78bd12d`) in §13; the 2026-09-01 first pass (`33480009094`, `2b2fa3f`) in §14. Every retained register is kept intact, because other findings cite those row ids by name.

---

## §0. Re-run 7 record (2026-09-08) — **GO**

### §0.1 Verdict: **GO — all four required jobs success, executed counts non-zero on both platforms, every skip explained**

The close criterion, quoted verbatim from the PLAN (Definition of done / Test plan final gate):

> A single CI run on the branch head with `test`, `build-android`, `e2e-web`, `e2e-android` all
> success **and** non-zero executed journey counts; URL and counts quoted in the close.

Every clause is satisfied by run `34225431645` on sha `d53fb7e21f2299eb6b65a3aa4e72dc48d851a1eb`:

- **`test` — success.** `🎉 548 tests passed, 5 skipped.` (553 total, **0 failed**). The 5 skips are all 48.29's guard-tool fixture guards in `test/tool/check_e2e_executed_test.dart` (workspace-root captured logs not in the repo): the 3 carried from re-run 6 plus **2 new CI-grammar fixtures** written from the false-fire log (`run 34204817176`) — in-kind, honest, predicted up to the +2 fixture skips.
- **`build-android` — success.** `✓ Built build/app/outputs/flutter-apk/app-debug.apk` (Gradle `assembleDebug`, 316 s).
- **`e2e-android` — success.** `🎉 24 tests passed, 2 skipped.` — 0 `❌` groups, **17/17 APK installs**, and the guard now reads the CI grammar correctly: `Final progress line: 🎉 24 tests passed, 2 skipped.` → **`[OK] Android execution proven: 24 executed.`** Re-run 6's R-1 (guard false-fire) is **fixed and confirmed in vivo** — the exact line re-run 6's §0.7 said the next gate "must verify … exists, not just the job conclusion".
- **`e2e-web` — success.** **16/16 files green** (`result {"result":"true"}` ×16, `"result":"false"` ×0) with **22 `e2e_executed` markers** across 16 files and the guard's `[OK] Web execution proven: 22 executed.` — **R-2 (web attendance `:223`) is fixed and confirmed in vivo**: `attendance_journey_test.dart: EXECUTED (1)` with `result:true`, the first fully-green web loop at a branch-head gate (48.24 re-run 7 predicted exactly this).

**Predictions scorecard (48.24 §0c.4 / 48.25 §0):** `test` 553/3/0 → **553 total ✓** (548 executed + 5 fixture-guard skips, 0 failures); Android 24/0/2 with job success + `[OK] Android execution proven` → **exact ✓**; web 16/16 (22 executed markers) with R-2's attendance `:223` green → **exact ✓**; build success → **✓**. Every prediction landed.

**48.15 may now re-run** and close STEP-48 against this run. STEP-48's index row was not touched here (48.15's lane).

### §0.2 Precondition (sha identity, push, local gates)

| Check | Result |
|---|---|
| `git fsck --full` on `Code/mine-flow-app` | Clean (exit 0; only harmless dangling objects) |
| `HEAD` | `d53fb7e21f2299eb6b65a3aa4e72dc48d851a1eb` |
| `origin/step-0048-runtime-evidence` | `d53fb7e…` — **equal to HEAD**; `git rev-list --left-right --count` → `0 0` |
| Working tree | Clean except untracked `run_web_wrapper.dart` (the standing scratch file — never committed, correctly) |
| Push (prompt DoD asks for it) | `Everything up-to-date` — 48.25 re-run 8 already pushed `5bff0b1..d53fb7e` fast-forward; the push itself triggered run `34225431645` |
| `?head_sha=d53fb7e…` | **`total_count: 1`** — the run for this sha exists, is complete, and is unique; used as handed forward (no second run forced) |

**Local gates re-derived on the exact tree this session** (not carried from 48.25): contract guard `[OK] Contract verification passed.` exit 0 · `flutter analyze` → `No issues found! (ran in 23.0s)` · `dart format --output=none --set-exit-if-changed lib/ test/ tool/` → `Formatted 318 files (0 changed)` · `dart format` idempotent. The full unit suite was proven by 48.25 re-run 8 on this identical tree (553/553, `0 0` ahead/behind — no commit since) and re-proven by CI's `test` job this run (553 total, 0 failed).

### §0.3 Job results

| Job | id | Conclusion | Window (UTC) |
|---|---|---|---|
| `Lint, analyze & test` (`test`) | 102058271675 | **success** | 12:19:30 → 12:22:17 |
| `Build Android APK (smoke check)` | 102059148196 | **success** | 12:22:21 → 12:28:27 |
| `E2E Tests (Android)` (`e2e-android`) | 102059148267 | **success** | 12:22:19 → 12:49:15 (26m56s) |
| `E2E Tests (Web)` (`e2e-web`) | 102059148175 | **success** | 12:22:19 → 12:49:33 (27m14s) |
| `Deploy to Staging` / `Deploy to Production` | — | skipped (not part of the gate) | — |

Both E2E jobs ran to completion with real durations (the §3c cascade and §3a hang shapes are both excluded); Android 17/17 APK installs match every healthy baseline.

### §0.4 Per-file, per-platform table

Android (from `##[group]` ✅/❌/⏭️ markers; the `❌` column is 0 for every file):

| Journey file | Android ✅/❌/⏭️ | Web | Skip reason (verbatim, where a skip exists) | Expected? |
|---|---|---|---|---|
| `app_boots_test.dart` | 1/0/0 | EXECUTED (1), `result:true` | — | yes |
| `design_review_capture_test.dart` | 1/0/0 | not in web loop (not a journey) | — | yes (Android-only harness file) |
| `attendance_journey_test.dart` | 1/0/0 | **EXECUTED (1), `result:true`** | — | **yes — R-2 green, first CI proof** |
| `auth_journey_test.dart` | 1/0/0 | EXECUTED (1) | — | yes |
| `benchmark_journey_test.dart` | 1/0/0 | EXECUTED (1) | — | yes |
| `cut_fill_journey_test.dart` | 1/0/0 | EXECUTED (1) | — | yes |
| `daily_log_journey_test.dart` | 1/0/0 | EXECUTED (1) | — | yes |
| `data_bucket_journey_test.dart` | 2/0/0 | EXECUTED (1) | web skip: `staging or Drive credentials absent (RISK-0017/0018, decision D2)` | yes (D2) |
| `deep_link_journey_test.dart` | 2/0/0 | EXECUTED (2) | — | yes |
| `equipment_check_journey_test.dart` | 1/0/0 | EXECUTED (1) | — | yes |
| `inventory_journey_test.dart` | 1/0/0 | EXECUTED (1) | — | yes |
| `land_clearing_journey_test.dart` | 1/0/0 | EXECUTED (1) | — | yes |
| `notifications_journey_test.dart` | 1/0/0 | EXECUTED (1) | — | yes |
| `offline_sync_journey_test.dart` | 6/0/0 | EXECUTED (5) | web skip: `Android-only per Doc 15 §1 (platform limitation, not a defect)` | yes (Q12) |
| `reporting_journey_test.dart` | 1/0/0 | EXECUTED (1) | — | yes |
| `rls_authorization_journey_test.dart` | 2/0/1 | EXECUTED (2) | Android skip: `RLS Authorization Journey — Part A: per-role matrix (STEP-45.12) crew policies behave as documented` / web skip: `crew credentials absent (RISK-0021)` | yes (RISK-0021) |
| `timeline_journey_test.dart` | 1/0/0 | EXECUTED (1) | — | yes |

Android totals: **24 ✅ / 0 ❌ / 2 ⏭️** (framework summary agrees with the marker counts). Web totals: **16/16 files `result:true`, 22 executed markers, 3 named skips** (guard per-file table quoted above). **Zero journey failures on either platform; zero unexplained skips.**

### §0.5 Evidence quality

1. **The guard's CI grammar (R-1) is proven in vivo, both platforms.** Android: `Final progress line: 🎉 24 tests passed, 2 skipped.` → `[OK] Android execution proven: 24 executed.` (exit 0, job green — the OK polarity). Web: `[OK] Web execution proven: 22 executed.` (16 files, per-file table with named skips verbatim). The firing polarity was already proven by re-run 6's false-fire; the wiring defect class is fully discharged.
2. **Executed counts non-zero, independently corroborated (Android):** 337 `/rest/v1/` request lines prove live staging traffic; `on_conflict=user_id%2Cdate` ×4 and `Remote wins` ×3 (the LWW/onConflict contract behaviors); `23505`/`22P02`/`23503` → **0 hits** (the invalid-UUID/FK/unique-conflict classes stay fixed); `42501` ×6 = the adjudicated correct RLS refusal (48.20 Q10). **Zero opaque failures**: `Multiple exceptions` → 0 in both logs.
3. **The `test` job's 5 skips** — all in `test/tool/check_e2e_executed_test.dart`, all workspace-root fixture guards (`skipped` because the captured logs are not in the repo). Two of the five are new: fixtures written from the false-fire log itself (`run 34204817176`) — the R-1 unit pins that the re-run ordered. Honest, in-kind.
4. **Vacuous-pass spot-checks (delta-scoped):** `git diff --name-status 5bff0b1..d53fb7e` touches **0 `integration_test/` files** (the delta is `ci.yml`, guard tool+test, attendance repository+test — exactly the two committed lanes 48.25 re-run 8 recorded). Checked on the current tree anyway: the single `expect(true` textual hit is the docstring in `deep_link_journey_test.dart:3` documenting the fake green STEP-48.1 removed; all **23 real `markTestSkipped` sites are followed by `return;`** (a 24th textual hit is a `fail()` message in `helpers/login_helper.dart:88` quoting the guard idiom, not a call).
5. **Honest limit, held open (§3b continuity): the screenshot artifacts are still empty on both platforms.** Android captured 1 of 24 cells fail-safe (23 `Warning: takeScreenshot(…) timed out after 1s`); both jobs warn `No files were found with the provided path: screenshots/. No artifacts will be uploaded.` The gate-wedging defect is fixed and the suite is green, but the **design-review coverage the capture harness exists to underwrite still does not exist** — the 73 committed design-review PNGs remain 1×1 placeholders. This does not affect the four-job criterion (screenshots are not a gate clause); it must be carried into 48.15's close as an open, honestly-stated gap (48.22's design-review coverage claim narrows to "harness exists, artifacts not yet produced").
6. **No journey hogs the budget**: web per-file slots all land in the ~95-s band (12:24 → 12:49 for 16 files); Android 26m56s for 17 installs, both within every healthy baseline.

### §0.6 Totals against every prior gate

| | `33327930159` | `33480009094` | `33626548011` | `33734562106` | `33879989164` | `33953949570` | `34192851645` | `34204817176` | **This run `34225431645` (`d53fb7e`)** |
|---|---|---|---|---|---|---|---|---|---|
| Android | 14/10/2 | 15/9/2 | 0 (cancelled) | 20/4/2 | 23/1/2 | 24/0/2 success | skipped | 24/0/2 (job red: guard) | **24/0/2, job success** |
| Web | 6/10 | 8/8 | 10/6 | 12/4 | 15/1 | 15/1 | skipped | 15/1 | **16/16, job success** |
| `test` | success 457 | success 487 | success 489 | success 498 | success 505 | success 505 | failure 536+3+3 | success 539+3+0 | **success 548+5+0 (553)** |

The wave's terminal state: every defect class the register ever carried is green at the branch head — the last two residuals (R-1 guard grammar, R-2 web attendance read-back) were the only deltas since `5bff0b1` and both are confirmed fixed by this run.

### §0.7 GO consequences

**48.15 may now re-run** (docs-true sweep, index correction & close), quoting run `34225431645`, sha `d53fb7e21f2299eb6b65a3aa4e72dc48d851a1eb`, and the counts above. Reconciliation checklist for 48.15, gathered from the wave's handoffs:

- **Doc 09 §4's "harness only" note vs the real E2E shape** (Doc 12) — the dual-platform gate now exists and is green; the docs must say what actually runs.
- **Doc 04's Version Log** — 48.17 and 48.23 (re-run 5) both wrote contract notes (LWW `updated_at` writer obligation; daily-log status contract); confirm both are recorded and current.
- **Design-review report coverage claim** (48.22's handoff): narrow honestly — the harness exists and runs green, but screenshot artifacts are empty (§0.5 item 5); the coverage claim cannot extend to Android and is not even web-real yet.
- **RISK-0006/0011/0014/0015/0016/0019/0021/0022/0023 close-or-re-justify recommendations** produced by the wave — re-weigh each against this run's evidence (RISK-0021 crew leg still skipped on both platforms: credential-gated, honest).
- **The STEP-45 rows that can now cite real evidence** (journey-level: 15/15 web, 17 targets Android) **and those that cannot** (Drive upload D2, crew RLS leg, screenshot-backed design review).
- **Staging hygiene**: the staging token revocation the user owns (handed forward since 48.21/48.23) and the wave's staging write residue (e.g. the `name='150'` rows 48.22 diagnosed) are still open user-side items; name them in the close.
- **STEP-48's index row and archive** — 48.15's lane, untouched here.

No re-runs are ordered. 48.27 and 48.30's lanes were already CI-confirmed at `5bff0b1` and the delta to `d53fb7e` does not touch them; 48.28's roadmap-claims lane is a docs-repo concern for 48.15 to reconcile.

### §0.8 Not done here (scope discipline)

No defect was fixed. No application code, test, `ci.yml`, migration, staging row, `risks.yml` status, architecture doc, `prompts/STEP-index.md` row, or archive was touched. STEP-48's index row and status are untouched (the close is 48.15's). The only writes are this findings file (§0; §0a = re-run 6 retained intact; §0b = re-run 5; §1–§17 = re-run 4), the PLAN's 48.26 progress row (replaced), and evidence-only amendments to the PLAN's 48.29 and 48.24 progress rows (status cells left alone). No staging query was issued. No secret value appears anywhere; the PAT used for the API reads was taken from Git Credential Manager and never echoed. Evidence retained at the workspace root: `step4826_r7_test_job.log`, `step4826_r7_build_job.log`, `step4826_r7_android_job.log`, `step4826_r7_web_job.log`.

**Prompt erratum, carried from all prior passes:** the prompt's Definition of done asks for "`mine-flow-STEP-48.25-FINDINGS.md` written". That file is 48.25's and already exists; this substep's record is this file.

### §0.9 Definition of done (re-run 7)

- [x] Branch head verified pushed (`Everything up-to-date`); sha recorded and matched to the run's `head_sha` via `?head_sha=` → `total_count: 1` (§0.2).
- [x] A single CI run identified with all four required jobs' ids, conclusions, and windows (§0.3).
- [x] Per-file/per-platform counts extracted: Android from the `##[group]` markers + framework summary; web from the guard's per-file table + `result{}` JSON (§0.4).
- [x] Run totals stated against all eight prior gates (§0.6).
- [x] Executed counts confirmed non-zero on both platforms; both zero-executed guards ran, read the CI grammar, and passed — `[OK] Android execution proven: 24 executed.` and `[OK] Web execution proven: 22 executed.` quoted (§0.1, §0.5).
- [x] Every skip explained and matched to a findings file/decision id: Android 2 (RISK-0021 crew, D2 Drive), web 3 (D2, Doc 15 §1/Q12, RISK-0021), `test` 5 fixture guards — zero unexplained skips (§0.4, §0.5).
- [x] Zero residual failures — nothing to classify or assign.
- [x] Vacuous-pass and `markTestSkipped`-followed-by-`return` spot-checks done, delta-scoped (§0.5 item 4).
- [x] Explicit **GO** verdict, with the close criterion quoted verbatim (§0.1).
- [x] On GO: the reconciliation checklist for 48.15 written out (§0.7).
- [x] `mine-flow-STEP-48.26-FINDINGS.md` written (re-run 7 record; all prior records retained); PLAN progress table updated (48.26 row replaced; 48.29 and 48.24 rows amended with evidence only).
- [x] STEP-48's index row and status untouched — verified after writing (§0.10).

### §0.10 Post-write verification

- `Code/mine-flow-app`: `git status --short` clean except untracked `run_web_wrapper.dart`; HEAD still `d53fb7e`, equal to `origin` — this substep wrote nothing into the app repo.
- `Code/mine-flow-docs` / `prompts`: sibling-lane states re-checked and left alone (any remaining modifications are other STEP lanes recorded in their own rows).
- Docs hub `scripts/check.sh` run after writing; fail/warn counts quoted in the session record (the workspace-root evidence logs produce the pre-existing hygiene WARN, unchanged in kind).

---

## §0a. Re-run 6 record (2026-09-08) — retained unmodified

### §0.1 Verdict: **NO-GO — two red jobs: one guard false-fire, one real web journey failure**

The close criterion, quoted verbatim from the PLAN (Definition of done / Test plan final gate):

> A single CI run on the branch head with `test`, `build-android`, `e2e-web`, `e2e-android` all
> success **and** non-zero executed journey counts; URL and counts quoted in the close.

This run fails the criterion on the jobs clause only — and for the first time in the wave, **the failure is not what it appears to be on the jobs dashboard**:

- **`test` — success.** `🎉 539 tests passed, 3 skipped.` (542 total; the 3 skips are 48.29's guard-tool fixture guards, §0.4.3.) **Re-run 5's R-1/R-2 (TZ-dependent fixtures) are fixed and confirmed on CI** — exactly the predicted 542/3/0.
- **`build-android` — success.** `✓ Built build/app/outputs/flutter-apk/app-debug.apk`.
- **`e2e-android` — failure, but every test passed.** `🎉 24 tests passed, 2 skipped.` — 0 failures, 17/17 APK installs, zero `❌` groups. The job is red **solely because 48.29's zero-executed guard false-fired**: it parsed the redirected `integration_test.log`, found `Final progress line: (none)`, counted 0 executed, and exited 1 — on a log that contains **358** matches for the old guard's own loose pattern. The guard's Android grammar (`MM:SS +<passed>:` compact progress lines) does not exist in CI's log **at all** (0 hits for `All tests passed`, `Some tests failed`, `~2:`, any `MM:SS +N` line): CI's `flutter test` under `GITHUB_ACTIONS=true` emits the GitHub-annotations reporter (`##[group]✅/❌/⏭️` per test, `🎉 N tests passed, M skipped.` summary). The guard was unit-tested against local-format logs; this is its **first in-vivo run** (re-run 5's `needs:` cascade skipped both E2E jobs), and the first in-vivo run falsified its grammar.
- **`e2e-web` — failure, one real journey failure.** 15 of 16 files green; `attendance_journey_test.dart` red at `:223` (step-8 list read-back, §0.5).

**Executed counts: non-zero on both platforms** (Android 24 passed + 0 failed = 24 executed; web 22 `e2e_executed` markers across 16 files + 1 driver failure). The criterion's non-zero clause passes; the four-jobs-success clause fails. **STEP-48 stays `In progress`. Phase 4 stays shut. 48.15 may not re-run.**

### §0.2 Precondition (sha identity, push, local gates)

| Check | Result |
|---|---|
| `git fsck --full` on `Code/mine-flow-app` | Clean — only harmless dangling objects |
| `HEAD` | `5bff0b16c2bb3b0317d76ce9e7ea3c78616db79e` |
| `origin/step-0048-runtime-evidence` | `5bff0b1…` — **equal to HEAD**; `git rev-list --left-right --count` → `0 0` |
| Working tree | Clean except untracked `run_web_wrapper.dart` (48.24's named loop residue, never committed — correctly) |
| Push (prompt DoD asks for it) | `Everything up-to-date` — 48.25 re-run 7 already pushed `f14885e..5bff0b1` fast-forward |
| `?head_sha=5bff0b16…` | **`total_count: 1`** — the run for this sha exists, is complete, and is unique; used as handed forward (no second run forced) |

**Local gates re-derived on the exact tree this session** (not carried from 48.25): contract guard `[OK]` exit 0 · `flutter analyze` → `No issues found! (ran in 22.9s)` · `dart format --output=none --set-exit-if-changed lib/ test/ tool/` → `Formatted 317 files (0 changed)`, exit 0.

### §0.3 Job results

| Job | id | Conclusion | Window (UTC) |
|---|---|---|---|
| `Lint, analyze & test` (`test`) | 101991742961 | **success** | 08:30:01 → 08:32:52 |
| `Build Android APK (smoke check)` | 101992590017 | **success** | 08:32:54 → 08:38:17 |
| `E2E Tests (Android)` (`e2e-android`) | 101992590022 | **failure** (guard false-fire; suite 24/0/2 green) | 08:32:54 → 08:57:44 (24m50s) |
| `E2E Tests (Web)` (`e2e-web`) | 101992590072 | **failure** (1 of 16 files red) | 08:32:54 → 09:00:32 (27m38s) |
| `Deploy to Staging` / `Deploy to Production` | — | skipped (not part of the gate) | — |

Both E2E jobs ran to completion with real durations (§3c's cascade and §3a's hang shapes both excluded); 17/17 Android APK installs match all healthy baselines.

### §0.4 Evidence quality — the marker channel is now proven in vivo, and the guard wiring with it

1. **48.29's reportData marker channel: first in-vivo CI proof — a win.** The web guard's own output (job log, `Web E2E execution summary`) shows **16 files in aggregate, 22 executed markers**, and the per-file table with named skips verbatim: `data_bucket_journey_test.dart: staging or Drive credentials absent (RISK-0017/0018, decision D2)` · `offline_sync_journey_test.dart: Android-only per Doc 15 §1 (platform limitation, not a defect)` · `rls_authorization_journey_test.dart: crew credentials absent (RISK-0021)`. Re-run 5's §0.5 item 2 ("in-vivo proof still owed") is **discharged**.
2. **The `5bff0b1` exit-propagation fix is proven in vivo, both polarities.** The web guard ran, printed `[OK] Web execution proven: 22 executed.`, and the job then failed on the journey (`exit $fail`) — the OK path propagates. The Android guard fired (exit 1) and the job went red — the firing path propagates. Ironically, the false-fire is what proves the wiring.
3. **The false-fire's mechanism, from the artifact the guard parsed.** The job log's `cat integration_test.log` dump (lines 594–4890, extracted to `step4826_r6_integration_test.log`, 4,297 lines) contains GitHub-annotation format throughout and **zero** compact-reporter progress lines: `grep -c 'All tests passed'` → **0**; `~2:` → **0**; no `MM:SS +N:` line exists (the 358 loose-pattern hits are incidental — UUIDs, version strings). The old pre-48.29 inline grep would have passed this log on its loose pattern; the new grammar-correct guard rejects it because its grammar describes the **local** reporter, not CI's. Re-run 4's android job was green with 363 progress lines in its artifact **because the old inline grep was still in `ci.yml` at `c73a00e`** (`git show c73a00e:.github/workflows/ci.yml | grep -c check_e2e_executed` → 0); the committed guard has never previously run against a live CI log.

### §0.4.3 The `test` job's 3 skips — honest, in-kind predicted

All three are 48.29's guard-tool fixture guards in `test/tool/check_e2e_executed_test.dart` (workspace-root captured logs not in the repo — same as re-run 5 §0.4.3). Verbatim shape: `⏭️ … parses the captured real Android log from the workspace root (skipped)` · `… parses the captured real web aggregate from the workspace root (skipped)` · `… CLI PASSES (exit 0) on the captured real Android log tail (skipped)`. Legitimate; zero unexplained skips.

### §0.5 Residual register

| # | Failure | Class | Was it known? | Assignment |
|---|---|---|---|---|
| **R-1** | `e2e-android` job red on an all-green suite: guard `Final progress line: (none)` → `Passed: 0, Failed: 0` → `[ERROR] Zero tests executed` | **guard defect (grammar vs reporter mismatch)** — `parseAndroidLog` matches only the local compact reporter; CI emits GitHub annotations. First in-vivo exposure. | Known-possible, now proven: 48.29's own deferred item "first in-vivo proof still owed" | **Re-run 48.29** — teach `parseAndroidLog` the CI grammar (`##[group]✅/❌/⏭️ <path>: <name>` per-test markers + `🎉 <n> tests passed, <m> skipped.` / `Some tests failed.` summaries), keep the local grammar working, pin both with unit tests against **captured CI-format logs** (`step4826_r6_integration_test.log` is a ready fixture at the workspace root). No guard rule may be weakened: the all-skipped (`+0 ~17`) rejection must still pass. |
| **R-2** | Web `attendance_journey_test.dart:223` step-8 list read-back: `Expected: exactly one matching candidate / Actual: Found 0 widgets with text containing Izin sakit shift pagi 1788856612032` after the bounded 50×100 ms poll expired | **web-only UI read-back failure — list does not reflect the saved row within 5 s of pumping.** Android passes the same journey at this sha. The poll (48.24 re-run 6) is present and **insufficient on web** — an expired bounded poll is evidence the list is never refreshed (or the row never built), not that it is slow. | Sibling known (48.24's Android `:209`, fixed by the poll); **web instance new** — first red at this line on web in the wave (gates 1–4's attendance web failures were the *other* assertion, `:225` AttendanceFormPage mount, fixed by 48.22 re-run 5 and green since) | **Re-run 48.24** — diagnose web-side before fixing: (a) the bloc refresh path (subscription vs single load — the data-bucket staleness class), (b) below-the-fold/lazy-build at the web viewport (48.21's insertion-order class; its sweep explicitly left attendance's `getAll()` unsorted as "justified-not-applied" — re-weigh under this evidence), (c) scroll-into-view before asserting. Do not lengthen the poll as the first move. |

**Zero opaque failures** on either platform: `Multiple exceptions` → 0 in both logs; the one journey failure carries a decoded assertion and `file:line`. **No journey hogs the budget.** **Database error-code absence holds on Android**: `23505`/`22P02`/`23503` → 0 hits, `42501` ×6 = the adjudicated correct RLS refusal (48.20 Q10); 344 `/rest/v1/` request lines prove live staging traffic. Web forwards no app traffic (standing asymmetry); execution proven by the marker channel + the decoded failure payload instead.

### §0.6 Totals against every prior gate

| | `33327930159` | `33480009094` | `33626548011` | `33734562106` | `33879989164` | `33953949570` | `34192851645` | **This run `34204817176` (`5bff0b1`)** |
|---|---|---|---|---|---|---|---|---|
| Android | 14/10/2 | 15/9/2 | 0 (cancelled) | 20/4/2 | 23/1/2 | 24/0/2 success | skipped | **24/0/2 — suite green, job red (guard false-fire)** |
| Web | 6/10 | 8/8 | 10/6 | 12/4 | 15/1 | 15/1 | skipped | **15/1** |
| `test` | success 457 | success 487 | success 489 | success 498 | success 505 | success 505 | failure 536+3+3 | **success 539+3+0 (542)** |

The journey surface is **unchanged from `33953949570`** — Android 24/0/2 and web 15/1 are identical counts, with the web failure moved from daily-log (`:136`, now green a 2nd consecutive CI gate after 48.23 re-run 5's fix) to attendance (`:223`). Re-run 5's predictions score: `test` 542/3/0 ✅, Android 24/0/2 ✅ (suite), build ✅, **web 16/16 ❌ (15/1)** — the predicted fully-green web loop did not materialise; the miss is R-2.

### §0.7 NO-GO consequences — substeps to re-run, in order

1. **48.29** (Terra) — re-run for R-1: fix the guard's Android grammar (both reporters), unit-pinned against captured CI-format logs. Ordered **first** because it is structural: until fixed, the gate **cannot** go green even on an all-passing suite.
2. **48.24** — re-run for R-2: web attendance step-8 read-back, diagnose-then-fix per §0.5.
3. **48.25** — commit + push both lanes; hand the triggered run id forward.
4. **48.26** — re-run 7: fresh branch-head gate and verdict.

48.27 and 48.30 need no re-run (their lanes are CI-confirmed green this run). **Predictions for the next gate:** `test` 542+ (48.29's new grammar pins add tests) / Android 24/0/2 with **job success** (guard fixed) / web 16/16 **only if** 48.24's R-2 fix lands — 15/1 otherwise. An honest next-gate reading must check the guard's `[OK] Android execution proven` line exists, not just the job conclusion.

### §0.8 Not done here (scope discipline)

No defect was fixed. No application code, test, `ci.yml`, migration, staging row, `risks.yml` status, architecture doc, `prompts/STEP-index.md` row, or archive was touched. STEP-48's index row and status are untouched. The only writes are this findings file (§0; §0a = re-run 5 retained intact; §1–§17 = re-run 4), the PLAN's 48.26 progress row (replaced), and an evidence-only amendment to the PLAN's 48.29 progress row (status cell left alone). No staging query was issued. No secret value appears anywhere; the PAT used for the API reads was taken from Git Credential Manager and never echoed. Evidence retained at the workspace root: `step4826_r6_test_job.log`, `step4826_r6_build_job.log`, `step4826_r6_android_job.log`, `step4826_r6_web_job.log`, `step4826_r6_integration_test.log` (the guard's actual input, extracted), `step4826_r6_contract.log`, `step4826_r6_analyze.log`, `step4826_r6_format.log`.

**Prompt erratum, carried from all prior passes:** the prompt's Definition of done asks for "`mine-flow-STEP-48.25-FINDINGS.md` written". That file is 48.25's and already exists; this substep's record is this file.

### §0.9 Definition of done (re-run 6)

- [x] Branch head verified pushed (`Everything up-to-date`); sha recorded and matched to the run's `head_sha` via `?head_sha=` → `total_count: 1` (§0.2).
- [x] A single CI run identified with all four required jobs' ids, conclusions, and windows (§0.3).
- [x] Per-file/per-platform counts extracted: Android from the `##[group]` markers + framework summary; web from the guard's per-file table + `result{}` JSON (§0.4, §0.5).
- [x] Run totals stated against all seven prior gates (§0.6).
- [x] Executed counts confirmed non-zero on both platforms; **the Android zero-executed guard FIRED — on a fully-green suite** — and is itself R-1 (a false-fire, recorded as its own defect class, not a vacuous pass).
- [x] Every skip explained: Android 2 (RLS crew RISK-0021, data_bucket D2 RISK-0017/0018 — verbatim in the marker table and `##[group]⏭️` blocks), web 3 named marker skips (same decisions), `test` 3 fixture guards (§0.4.3). Zero unexplained skips.
- [x] Every residual failure classified and assigned (§0.5: R-1 → 48.29, R-2 → 48.24).
- [x] Vacuous-pass and `markTestSkipped`-followed-by-`return` spot-checks: the `c73a00e..5bff0b1` integration_test delta adds **0** active `markTestSkipped` sites (its single textual hit is `recordE2eSkipped`'s docstring) and **0** `expect(true` sites.
- [x] Explicit verdict with the close criterion quoted verbatim (§0.1).
- [x] NO-GO: substeps to re-run listed in order with named defects, fix shapes, and verification requirements; next-gate predictions stated (§0.7).
- [x] `mine-flow-STEP-48.26-FINDINGS.md` written (re-run 6 record; all prior records retained); PLAN progress table updated (48.26 row replaced; 48.29 row amended with evidence only).
- [x] STEP-48's index row and status untouched — verified after writing (§0.10).

### §0.10 Post-write verification

- `Code/mine-flow-app`: `git status --short` clean except untracked `run_web_wrapper.dart`; HEAD still `5bff0b1`, equal to `origin` — this substep wrote nothing into the app repo.
- `Code/mine-flow-docs` / `prompts`: sibling-lane states re-checked and left alone (any remaining modifications are other STEP lanes recorded in their own rows).
- Docs hub `scripts/check.sh` run after writing; fail/warn counts quoted in the session record (the workspace-root evidence logs produce the pre-existing hygiene WARN, unchanged in kind).

---

## §0b. Re-run 5 record (2026-09-08) — retained unmodified

### §0.1 Verdict: **NO-GO — structural: this gate returned no E2E evidence at all**

The close criterion, quoted verbatim from the PLAN (Definition of done / Test plan final gate):

> A single CI run on the branch head with `test`, `build-android`, `e2e-web`, `e2e-android` all
> success **and** non-zero executed journey counts; URL and counts quoted in the close.

This run fails that criterion on **every** clause the previous gate had already satisfied:

- **0 of the 4 required jobs are `success`.** `Lint, analyze & test` (the `test` job) **failed** inside its "Run tests" step; `Build Android APK (smoke check)`, `E2E Tests (Android)` and `E2E Tests (Web)` were **`skipped`** (`needs: test`, `ci.yml:77/:125/:226`) — the dependency cascade, not a timeout.
- **Executed journey counts: zero on both platforms.** No E2E job started, so this is an evidence hole of a *different* kind than re-run 1's §3a hang: not "one job hung", but "the gate's foundation job failed and the wave's journey surface was never measured".
- This is the wave's 7th gate and the **first with a red `test` job**. It is also the shortest (2m44s total).

It is equally **not** the familiar NO-GO shape: unlike gates 1–4 and 6, there are **zero journey-level failures to assign** — the failure is fully upstream, fully classified, and byte-identically reproducible locally (§0.4). **STEP-48 stays `In progress`. Phase 4 stays shut. 48.15 may not re-run.**

### §0.2 Precondition (sha identity, push, local gates)

| Check | Result |
|---|---|
| `git fsck --full` on `Code/mine-flow-app` | Clean — 3 harmless dangling objects (`dangling commit 7c28a90e…`, `69f5970d…`, `dangling blob 7b9bd39f…`; the blob unchanged from every prior pass) |
| `HEAD` | `f14885e4b954ab7f8acd877cafb76fc04ce6824c` |
| `origin/step-0048-runtime-evidence` | `f14885e4b954ab7f8acd877cafb76fc04ce6824c` — **equal to HEAD** |
| `git ls-remote origin refs/heads/step-0048-runtime-evidence` | `f14885e4b954ab7f8acd877cafb76fc04ce6824c` — equal (remote re-read, not inferred) |
| `git rev-list --left-right --count origin/…...HEAD` | `0	0` — neither ahead nor behind |
| Working tree | Clean except untracked `run_web_wrapper.dart` — 48.24's handoff names it loop residue regenerated by every local web run; **not committed, correctly** |
| Push (prompt DoD asks for it) | `Everything up-to-date` — 48.25 re-run 6 already pushed `bb32c92`+`7db4a0a`+`f14885e` as `87fada3..f14885e` fast-forward |
| `?head_sha=f14885e4…` | **`total_count: 1`** — the run for this sha exists, is complete, and is unique; used as handed forward (no second run forced, no re-push) |

**Local gates re-derived on the exact tree this session** (not carried from 48.24/48.25): `dart run tool/check_supabase_contracts.dart` → `[OK] Contract verification passed.` · `flutter analyze` → `No issues found! (ran in 9.8s)` · `dart format --output=none --set-exit-if-changed lib/ test/ tool/` → `Formatted 317 files (0 changed)`, exit 0.

### §0.3 Job results

| Job | id | Conclusion | Window (UTC) |
|---|---|---|---|
| `Lint, analyze & test` (`test`) | 101954282396 | **failure** (step "Run tests") | 06:00:45 → 06:03:26 |
| `Build Android APK (smoke check)` (`build-android`) | 101954846916 | **skipped** (`needs: test`) | — |
| `E2E Tests (Android)` (`e2e-android`) | 101954846776 | **skipped** (`needs: test`) | — |
| `E2E Tests (Web)` (`e2e-web`) | 101954847188 | **skipped** (`needs: test`) | — |
| `Deploy to Staging` | 101954847203 | skipped (not part of the gate) | — |
| `Deploy to Production` | 101954284234 | skipped (not part of the gate) | — |

Job names at `f14885e` are byte-identical to `c73a00e` (`git show <sha>:ci.yml` both list `Lint, analyze & test` / `Build Android APK (smoke check)`) — the renamed-looking set in the jobs API is not new; only the guard implementation inside the E2E jobs changed (48.29's lane, §0.5). All pre-"Run tests" steps in the `test` job were green: contract guard, l10n guard, format, analyze — the failure is the suite itself.

### §0.4 The `test` job failure — three TZ-dependent test fixtures, reproduced byte-identically

Framework summary line (job log line 1086): **`##[error]536 tests passed, 3 failed, 3 skipped.`** Total **542** — exactly 48.24 re-run 6's predicted suite size (its local run: 542/542, including these 3 guard-tool tests executing against the captured logs; CI skips them, §0.4.3).

| # | Failing test | Verbatim payload | Frame |
|---|---|---|---|
| 1 | `test/features/data_bucket/data/models/geospatial_file_model_test.dart` — `GeospatialFileModel Serialization JSON serialization should preserve snake_case field name mapping` | `Expected: '2026-07-14T17:00:00.000Z'` / `Actual: '2026-07-15T00:00:00.000Z'` | `geospatial_file_model_test.dart 110:9` |
| 2 | same file — `GeospatialFileModel Serialization Hive JSON serialization should preserve camelCase field names` | `Expected: '2026-07-14T17:00:00.000Z'` / `Actual: '2026-07-15T00:00:00.000Z'` | `geospatial_file_model_test.dart 134:7` |
| 3 | `test/unit/timeline_repository_impl_test.dart` — `new milestone payload omits null server-managed timestamps` | `Expected: '2026-08-31T00:00:00.000Z'` / `Actual: '2026-08-31T07:00:00.000Z'` | `timeline_repository_impl_test.dart 114:5` |

#### §0.4.1 Residual register

| # | Failure | Class | Was it known? | Assignment |
|---|---|---|---|---|
| **R-1** | Geospatial expectations at `:110` and `:134` fail on a UTC host | **test defect (TZ-dependent fixture)** — first-probe exposure of 48.27's own committed lane | No — first CI appearance; neither expectation string exists at `c73a00e` (`git show c73a00e:<file> | grep -c '17:00:00'` → **0**); the wave's five prior gates never executed these tests | **Re-run 48.27** |
| **R-2** | Timeline expectation at `:114` fails on a UTC host | **same class, same commit (`3df8e7f`)** — one owner, one class | No | **Re-run 48.27** (same re-run covers both rows) |

#### §0.4.2 Mechanism — derived from source, then proven by reproduction

48.27's `3df8e7f` rewrote these tests' expectations to UTC-suffixed strings and made `created_at`/`updated_at` dynamic via `fixedDateStr` (`DateTime.parse('2026-07-15T00:00:00Z').toUtc()` — environment-independent, passes on any host), **but left two fixture sites building local `DateTime`s**:

- `geospatial_file_model_test.dart:20/:44` — `acquisitionDate: local` where `local = DateTime(2026, 7, 15)`; the expectations hardcode `acquisition_date`/`acquisitionDate == '2026-07-14T17:00:00.000Z'`.
- `timeline_repository_impl_test.dart:106` — `startDate: DateTime(2026, 8, 31, 7)`; the expectation hardcodes `start_date == '2026-08-31T00:00:00.000Z'`.

On this **UTC+7** host those local instants serialize to exactly the hardcoded strings (2026-07-15 00:00+07 = 14T17:00Z; 2026-08-31 07:00+07 = 31T00:00Z) — every local gate in the wave passed for that accident. On CI's **UTC** runner they serialize to `2026-07-15T00:00:00.000Z` / `2026-08-31T07:00:00.000Z` and fail.

**Reproduction, byte-identical (the classification's decisive evidence):** on the exact tree,
`TZ=UTC flutter test test/features/data_bucket/data/models/geospatial_file_model_test.dart test/unit/timeline_repository_impl_test.dart` → **exit 1**, all three failures with the CI log's verbatim Expected/Actual pairs (`step4826_r5_tz_utc_repro.log`); default-TZ run of the same files → **exit 0, 11/11 passed** (`step4826_r5_tz_discriminator.log`). The failures are environment-dependent, **not** a flake: deterministic under UTC, green under UTC+7.

**Class enumeration is complete (no hidden tail):** `TZ=UTC flutter test` on the full 542-test suite → **`01:35 +539 -3: Some tests failed.`** — exactly these 3 tests, no others (`step4826_r5_fullsuite_tzUTC.log`). Fixing the two fixture sites (3 assertions) is the entire class; once fixed, a `TZ=UTC` full suite at 542/542 is a complete local pre-gate proof.

**App serialization is correct:** the same commit's positive UTC tests (`toJson and toHiveJson serialize client timestamps as UTC`, both round-trip tests, the minimal-record and null-fields tests) **pass on CI**. No application defect; the defect is confined to two test-fixture sites' hardcoded expectation strings.

#### §0.4.3 The 3 skips — honest, in-kind predicted

All three are in `test/tool/check_e2e_executed_test.dart` (48.29's guard-tool suite), each an explicit fixture guard:

```dart
final logFile = File('../../step4824_r4_android_full.log');
if (!logFile.existsSync()) {
  markTestSkipped('Captured Android log not available');
```

The captured evidence logs live at this workspace root only — they are not in the repository, so CI cannot have them. Predicted in kind by 48.24's §0b (its fixtures are workspace-root logs). Legitimate; zero unexplained skips.

### §0.5 Guard findings — recorded, not fixed (a `ci.yml` change would move the head)

1. **e2e-web guard exit code is swallowed (latent wiring defect at `f14885e`).** The loop runs `dart run tool/ci/check_e2e_executed.dart --platform=web --log=all_web.log` and then unconditionally `exit $fail` — the guard's exit code is never captured. If the guard fired while every journey file passed, the job would still go green. The **Android** wiring is correct (`guard=$?; if [ $guard -ne 0 ]; then exit $guard; fi; exit $status`). No effect on this run (job never started). Owner decision for the **next** head: mirror the Android capture, or fold the guard's status into `fail`. Route to 48.29's lane as an amendment; do not fix here.
2. **48.29's marker channel (`MINE_FLOW_E2E_FILE` aggregate markers + reportData `e2e_executed`/`e2e_skipped`) remains unproven on live CI** — both E2E jobs were skipped. The guard's committed unit tests cover the captured-log matrix; first in-vivo proof is still owed by the next gate that actually runs E2E.
3. Re-run 4 §8 items 1–4 (explicit `timeout:` on 16/17 integration files; the `screenshots/` upload-path mismatch; `failureDetails` printing; the capture harness inside the Android gate glob) are **unchanged and unre-verified** — no E2E ran. None withdrawn.

### §0.6 Totals against the prior gates — with the honest caveat

| | `33327930159` (`90a995c`) | `33480009094` (`2b2fa3f`) | `33626548011` (`78bd12d`) | `33734562106` (`310fea5`) | `33879989164` (`9288168`) | `33953949570` (`c73a00e`) | **This run `34192851645` (`f14885e`)** |
|---|---|---|---|---|---|---|---|
| Android | 14/10/2 | 15/9/2 | 0 executed (cancelled) | 20/4/2 | 23/1/2 | 24/0/2 — job success | **skipped — 0 evidence** |
| Web | 6/10 | 8/8 | 10/6 | 12/4 | 15/1 | 15/1 | **skipped — 0 evidence** |
| `test` | success 505-and-prior ladder: 457/487/489/498/505 | | | | | success 505 | **failure 536+3+3 = 542** |

The last gate with executed journey evidence remains `33953949570` (Android 24/0/2, web 15/1, `test` 505). This run **supersedes it as the branch-head gate without measuring the journeys** — nothing in it contradicts those results, and nothing in it advances them. The `test` total 542 reconciles exactly with 48.24 re-run 6's local suite (its 3 extra executions vs CI are the guard-tool fixture tests that need the workspace-root logs).

### §0.7 NO-GO consequences — substeps to re-run, in order

1. **48.27** (Opus 4.8) — re-run for R-1/R-2: make the two fixture sites host-independent. Fix shape: anchor both fixtures to UTC explicitly — `acquisitionDate: DateTime.utc(2026, 7, 15)` with expectation `'2026-07-15T00:00:00.000Z'`, and timeline `startDate: DateTime.utc(2026, 8, 31, 7)` with expectation `'2026-08-31T07:00:00.000Z'` (or derive the string from the same `DateTime.utc` instance — the point is input and expectation must share one anchor instead of sharing a local-clock accident). No assertion may be weakened. **Verification requirement (this gate's new discriminator):** default-TZ full suite **542/542** **and** `TZ=UTC flutter test` → **542/542** (on this host's git-bash the `TZ=UTC` env prefix works — proven in §0.4.2). Sweep instruction: the full-suite TZ=UTC run already proves the class is exactly these sites; no further grep is required, but the re-run must quote both suite totals.
2. **48.25** (Opus 4.8) — commit 48.27's fix and **push**; hand the auto-triggered run id forward. Optional owner decision to take there (not ordered): 48.29's web-guard wiring one-liner (§0.5 item 1) could ride in the same push — it is a `ci.yml` change and must be a deliberate owner choice.
3. **48.26** (this substep) — new branch-head CI gate and fresh verdict.

**Predictions for the next gate** (48.24's re-run-6 predictions, adjusted only by this gate's new information): `test` **542 passed / 3 skipped / 0 failed** (the 3 fixture-guard skips are CI-structural) · Android **24 passed / 0 failed / 2 skipped** · web **16/16 with 21 executed** · `build-android` success. 48.24 does **not** need to re-run before 48.25: nothing in this gate's delta touches the journey surface, and its local journey evidence stands; the final journey proof still comes from the next CI gate.

48.20's Q10 adjudication, 48.22's deep-link `Deferred`, and the screenshot-content defect are re-weighed-not-re-run (§9); none gained evidence this run. **48.15 must not run until items 1–3 are complete and all four jobs are green with non-zero executed counts.**

### §0.8 Not done here (scope discipline)

No defect was fixed. No application code, test, `ci.yml`, migration, staging row, `risks.yml` status, architecture doc, `prompts/STEP-index.md` row, or archive was touched. STEP-48's index row and status are untouched. The only writes are this findings file (§0; §1–§17 = the re-run 4 record retained intact), the PLAN's 48.26 progress row (replaced), and evidence-only amendments appended to the PLAN's 48.27 and 48.29 progress rows (status cells left alone).

No staging query was issued. No secret value appears anywhere; the PAT used for the API reads was taken from Git Credential Manager and never echoed. Evidence retained at the workspace root: `step4826_r5_test_job.log` (test job, 1,113 lines), `step4826_r5_tz_discriminator.log`, `step4826_r5_tz_utc_repro.log`, `step4826_r5_fullsuite_tzUTC.log`, `step4826_r5_analyze.log`, `step4826_r5_format.log`.

**Prompt erratum, carried from all prior passes:** the prompt's Definition of done asks for "`mine-flow-STEP-48.25-FINDINGS.md` written". That file is 48.25's and already exists; this substep's record is this file.

### §0.9 Definition of done (re-run 5)

- [x] Branch head verified pushed (push attempted per prompt: `Everything up-to-date`); sha recorded and matched to the run's `head_sha` via `?head_sha=` → `total_count: 1`; remote re-read via `ls-remote` (§0.2).
- [x] A single CI run identified with all four required jobs' ids, conclusions, and windows (§0.3).
- [x] Per-file/per-platform counts: **not extractable — both E2E jobs skipped; recorded as the evidence hole it is, not folded into a red count** (§0.1, §0.6). The `test` job's per-test failures are tabulated with verbatim payloads and frames (§0.4).
- [x] Run totals stated against all six prior gates with the executed-vs-skipped asymmetry named explicitly (§0.6).
- [x] Executed counts: **zero on both platforms — the criterion's non-zero clause fails independently of any verdict reading.** Guard-not-fired checks are vacuous this run (nothing ran); recorded as such instead of claimed.
- [x] Every skip's verbatim reason quoted (the 3 `markTestSkipped` fixture guards, quoted; the 5 skipped jobs explained by `needs:`) and reconciled (§0.3, §0.4.3); `markTestSkipped`-followed-by-`return` spot-checks: the integration delta adds **0** new `markTestSkipped` call sites (the delta's single hit is the new helper's docstring) and **0** new `expect(true` (§0.8 evidence).
- [x] Every residual failure classified (test defect, TZ-dependent fixture; first-probe exposure) and assigned — 48.27, with the mechanism derived from source **and** proven by byte-identical `TZ=UTC` reproduction plus a complete class sweep (§0.4).
- [x] Explicit verdict with the close criterion quoted verbatim (§0.1).
- [x] NO-GO: substeps to re-run listed in order with named defects, fix shape, and verification requirement; predictions for the next gate stated (§0.7).
- [x] `mine-flow-STEP-48.26-FINDINGS.md` written (re-run 5 record; re-run 4 retained intact in §1–§17; earlier passes in §11–§14); PLAN progress table updated (48.26 row replaced; 48.27/48.29 rows amended with evidence only — status cells untouched).
- [x] STEP-48's index row and status untouched — verified after writing (§0.10).

### §0.10 Post-write verification

- `Code/mine-flow-app`: `git status --short` clean except untracked `run_web_wrapper.dart` (48.24's named loop residue, never committed); HEAD still `f14885e`, equal to `origin` — this substep wrote nothing into the app repo.
- `Code/mine-flow-docs`: on `step-0048-runtime-evidence` with one modification, `architecture/04-data-model.md` — that is **48.23 re-run 5's uncommitted Doc 04 note** (its lane, recorded in its PLAN row), present before this session and untouched here.
- `prompts`: still on `step-0050-phase3-check-in` with only its pre-existing `STEP-index.md` modification (STEP-50's lane) — no STEP-48 row edited.
- `Code/mine-flow-docs/scripts/check.sh`: **0 fails, 1 warning** — the pre-existing workspace-root hygiene WARN listing the wave's evidence logs (including this session's `step4826_r5_*` files), unchanged in kind from re-run 4.

---

## 1. Verdict: **NO-GO** *(retained re-run 4 record begins here; §1–§17 are the 2026-09-05 record, kept intact)*

The close criterion, quoted verbatim from the PLAN (Definition of done / Test plan final gate):

> A single CI run on the branch head with `test`, `build-android`, `e2e-web`, `e2e-android` all
> success **and** non-zero executed journey counts; URL and counts quoted in the close.

**Three of the four required jobs are `success`. One is not:**

- `test` — **success** (`🎉 505 tests passed.`)
- `build-android` — **success** (`✓ Built build/app/outputs/flutter-apk/app-debug.apk`)
- `e2e-android` — **success** — `🎉 24 tests passed, 2 skipped.` **Zero failures. This is the first green `e2e-android` job of the entire wave.**
- `e2e-web` — **failure** — 15 of 16 journey files green, 1 red.

One red job is still short of the literal criterion, so: **STEP-48 stays `In progress`. Phase 4 stays shut. 48.15 may not re-run.** Ordered re-runs in §10.

What changed, stated precisely rather than softened:

- **Both of the previous gate's register rows are fixed and confirmed on CI.** Previous R-1 (offline-sync last-write-wins leg) now passes on Android — and the registrar's skip branch actually logs on CI for the first time in the wave (§9). Previous R-2 (web attendance cannot mount `AttendanceFormPage` on the second `context.push`) is **green on web**, retiring an error string that had survived three consecutive web gates.
- **Android went from 23/1/2 to 24/0/2 and flipped the job conclusion to `success`.** That is the whole platform clean, not a count nudge.
- **The single web failure is not new and not a surprise — it is a class this wave has repeatedly declined to own.** `daily_log_journey_test.dart:136` fails `Expected: LogStatus:<LogStatus.submitted> / Actual: LogStatus:<LogStatus.draft>`. That is 48.23's **failure B** verbatim, the cell left `Deferred` across four gates "pending a deliberate re-assertion". This run **is** that deliberate re-assertion, and it came back red.

**48.24's re-run-4 classification of this exact failure as a flake with "no re-run ordered" is overruled here, with evidence** (§8, R-1; §4a). Its own local web loop reproduced the signature hours earlier on the same code; the mechanism is a real interleaving in the app, derivable from three named source sites; and the gate's rule from re-run 3 — every red per-file row gets a register id and an owner — applies to it.

---

## 2. Precondition check (48.25's push, and sha identity)

| Check | Result |
|---|---|
| `git fsck --full` on `Code/mine-flow-app` | Clean — `dangling commit 69f5970d…`, `dangling blob 7b9bd39f…` (both harmless; the blob is unchanged from every prior pass) |
| `HEAD` | `c73a00eab799dae717e47f1c1b1d1e327fa858eb` |
| `origin/step-0048-runtime-evidence` | `c73a00eab799dae717e47f1c1b1d1e327fa858eb` — **equal to HEAD** |
| `git ls-remote --heads origin step-0048-runtime-evidence` | `c73a00eab799dae717e47f1c1b1d1e327fa858eb` — equal (remote re-read, not inferred from the local ref) |
| `git rev-list --left-right --count origin/…...HEAD` | `0	0` — neither ahead nor behind |
| Working tree | Clean (`git status --short` prints nothing) |
| 48.25's two re-run-4 commits present | `cf9e8ca` (48.23 R-1: explicit client `updated_at` + premise guards + 7 pins) and `c73a00e` (48.22 R-2 re-run 5: step-8a SnackBar drain), on top of `9288168` |
| `mine-flow-docs` | Branch `step-0048-runtime-evidence`, clean, `41cfbb6` (Doc 04 v0.1.6) — untouched |
| `prompts` | Branch `step-0050-phase3-check-in` with `STEP-index.md` modified — **STEP-50's lane, untouched here** |

**Run/sha match:** run `33953949570` reports `head_sha = c73a00eab799dae717e47f1c1b1d1e327fa858eb`, `head_branch = step-0048-runtime-evidence`, `run_attempt = 1`, `event = push`. Byte-equal to local HEAD. A `?head_sha=` query returns `"total_count": 1` — it is the **only** run for this sha — and `?branch=` confirms it is the newest of 44 runs on the branch. It is the run 48.25's push auto-triggered (`ci.yml` runs `on: push`), used as handed forward. **No second run was forced and no push was attempted here** (48.25's lane).

**Diff scope of the two new commits** (`git diff --name-status 9288168..c73a00e`): four files, all test-side — `integration_test/journeys/attendance_journey_test.dart`, `integration_test/journeys/offline_sync_journey_test.dart`, `test/unit/daily_log_model_test.dart`, and the new `test/features/daily_log/data/sync/daily_log_sync_registrar_test.dart`. **`git diff --stat 9288168..c73a00e -- lib/` is empty:** no application code changed since gate 3. That matters for §8 — the daily-log failure cannot be a regression introduced by this wave round, because the daily-log feature, its bloc, its repository and its journey file are byte-identical to the sha where the same file passed on web.

**Local gates re-derived on this exact tree before the run was read** (not carried from 48.24/48.25): `flutter analyze` → `No issues found! (ran in 23.1s)`; `dart format --output=none --set-exit-if-changed .` → `Formatted 339 files (0 changed)`, exit 0; `dart run tool/check_supabase_contracts.dart` → `[OK] Contract verification passed.`, exit 0.

## 3. Job results

| Job | id | Conclusion | Window (UTC) |
|---|---|---|---|
| `Lint, analyze & test` | 101273733268 | **success** | 07:57:34 → 08:00:08 |
| `Build Android APK (smoke check)` | 101274030710 | **success** | 08:00:10 → 08:05:48 |
| `E2E Tests (Android)` | 101274030722 | **success** | 08:00:10 → 08:27:54 (27m44s) |
| `E2E Tests (Web)` | 101274030761 | **failure** (step 8, `Run E2E tests on Chrome (driver)`) | 08:00:10 → 08:27:41 (27m31s) |
| `Deploy to Staging` | 101277525332 | skipped (not part of the gate — `github.ref != master`) | — |
| `Deploy to Production` | 101273733542 | skipped (not part of the gate — not a release event) | — |

`test` job internals, all green:
`[OK] Contract verification passed.` · `[OK] No new hardcoded strings detected in non-exempt files.` ·
`Formatted 314 files (0 changed) in 1.45 seconds.` (CI formats `lib/ test/`; the local 339 covers the whole tree) ·
`flutter analyze` → `No issues found! (ran in 28.9s)` · `flutter test` → **`🎉 505 tests passed.`**

That 505 matches 48.24's and 48.25's local totals exactly (498 at gate 3 + 48.23's 7 new sync-registrar/DTO pins, four of which are visible by name in the job log), with **zero failures** — `Some tests failed` absent, the order-dependent Hive `setUpAll` / drain-window flake silent for the sixth consecutive gate. `build-android`: `Running Gradle task 'assembleDebug'... 301.8s`.

Terminal lines: Android `🎉 24 tests passed, 2 skipped.` and no `##[error]`; Web `##[error]Process completed with exit code 1.` (the loop's `exit $fail`).

Both E2E jobs again emit `##[warning]No files were found with the provided path: screenshots/. No artifacts will be uploaded.` — see §7 on what that does and does not say.

## 4. Executed counts — totals against every prior gate

| | `33327930159` (`90a995c`) | `33480009094` (`2b2fa3f`) | `33626548011` (`78bd12d`) | `33734562106` (`310fea5`) | `33879989164` (`9288168`) | **This run `33953949570` (`c73a00e`)** |
|---|---|---|---|---|---|---|
| Android | 14 passed, 10 failed, 2 skipped | 15 passed, 9 failed, 2 skipped | 0 executed — cancelled, no output | 20 passed, 4 failed, 2 skipped | 23 passed, 1 failed, 2 skipped | **24 passed, 0 failed, 2 skipped — job `success`** |
| Web | 6 true / 10 false | 8 / 8 | 10 / 6 | 12 / 4 | 15 / 1 | **15 true / 1 false** |
| `test` job | success | success, 457 | success, 487 | success, 489 | success, 498 | success, **505** |
| APK installs (Android) | 17 | 17 | **0** | 17 | 17 | **17** |

Every baseline column was re-parsed from its own job log with the same parser in this session, not carried over from earlier findings' prose. Android emoji-derived per-file totals: `(14,10,2)` · `(15,9,2)` · no framework line at all · `(20,4,2)` · `(23,1,2)` · **`(24,0,2)`** — and this run's parser output **agrees with the framework summary line** `🎉 24 tests passed, 2 skipped.` Web: 6/8/10/12/15/**15** files `result:"true"`, 16 files run every time.

**Executed counts: non-zero on both platforms.**

- **Android:** 17 target files, 26 cases, all 17 with per-file result groups (§6.1).
- **Web:** all 16 target files ran; 15 emitted `All tests passed.`, 1 emitted `result {"result":"false", …}` with a fully decoded failure payload.

**Zero-executed guards — both verified:**

- `e2e-web`'s guard did not fire: the only occurrence of `Error: Zero tests executed across all files.` in the job log is the workflow's own script text (line 405). Its condition was satisfied by 15 `All tests passed` hits in `all_web.log` (31 lines match the guard's full regex).
- `e2e-android`'s inline guard was **reached and satisfied**: `flutter test` returned, so the `if ! grep -qE …` ran against a log containing **363** matching progress lines (measured on the uploaded artifact, which is exactly the file the guard greps) and did not fire. Its three occurrences in the job log remain script text (action-input echo, group echo, `sh -c` command echo).

**Independent confirmation that real tests ran against live staging:**

- **Android:** **341** `/rest/v1/` request lines, real per-row UUID round-trips, and one genuine PostgreSQL error code — `42501` (6 hits, `new row violates row-level security policy for table "zones"` — the *correct refusal* 48.20 adjudicated under Q10, not a defect). **`23505`, `22P02`, `23503`, `PGRST204`, `PGRST205` are all absent** (`grep` → 0 each): every SQL-error class this wave fixed stayed fixed. Positive traces of the two newest fixes are in the log by name: `POST …/attendance_records?on_conflict=user_id%2Cdate` (×4) and `?on_conflict=site_id%2Cbm_id` (×6), plus 59 `Successfully synced` drains.
- **Web:** the `flutter drive` job log carries **no** PostgREST traffic (0 hits for `/rest/v1/`, and `all_web.log` has 0 hits for `supabase` either) — the web driver forwards none of the app's console output. That asymmetry has held at every gate. The web evidence that the app really executed against staging is instead: (a) 15 files' `All tests passed.`; (b) the one failure's fully decoded framework exception with a real `integration_test/journeys/daily_log_journey_test.dart 136:9` frame, reached only after a live login, a live save and a live repository read-back; (c) per-file slot durations spread across the job's own 08:00–08:27 window (§6.2).

### 4a. What the local gate predicted, and where it was wrong

48.24's re-run 4 measured the same code locally and reported **Android 23 passed / 3 skipped / 0 failed** and **web 15 pass / 1 fail**, with the 1 being this same daily-log `:136` status assertion.

- Its Android prediction was **directionally right and numerically conservative**: CI executed one more case (24 vs 23) with one fewer skip, because the `TEST_FOREMAN_*` credentials that are absent locally exist as repository secrets. CI is the stricter measurement, as at previous gates.
- Its web count was **exactly right**: 15/1, same file.
- Its **classification** of that 1 as "flake, NOT a regression … no re-run ordered" is where the gate diverges. The supporting claim "CI green on this file 3 consecutive gates" does not survive a re-parse of the prior gate logs. Web `daily_log_journey_test.dart` as a *file* was red at four of the five prior gates; the `LogStatus.submitted` assertion specifically was **red on web at `33327930159` and `33480009094`** (both logs carry `Actual: LogStatus:<LogStatus.draft>` with the frame at `:134`), green on web at `33626548011` and `33734562106` (those runs failed later, at `:143` / `:145`, in the BH-020 nav class) and green at `33879989164`. So the honest history of this assertion on web is **red, red, green, green, green, red — red in 3 of 6 gates**, and `Actual: LogStatus.draft` has appeared **0 times in every Android log of the wave**.

A ~50 % failure rate on one platform and 0 % on the other is not a flake to wave through; it is the signature of a timing-sensitive race whose window is wider on web. §8 R-1 pins the mechanism in source.

## 5. A-1 (the Android gate hang) — still resolved, and the platform is now fully green

The re-run-1 gate's decisive finding was structural: one file hung, `IntegrationTestWidgetsFlutterBinding.defaultTestTimeout = Timeout.none` (Flutter SDK `packages/integration_test/lib/integration_test.dart:435`, re-verified this session) meant nothing inside the framework could abort it, and when the 60-minute job timeout fired the log was empty. 48.22's `036bea2` fixed the real mechanism (`takeScreenshot` awaits a frame that `testWidgets` never renders). That fix holds, proved with the same four instruments that proved the hole:

- **Install count matches file count** — `grep -c 'Installing build/app'` → **17 for 17 targets**, identical to all four healthy baselines, against the hung run's 0.
- **Artifact runs to the job's end** — `android-e2e-log`'s `integration_test.log` is **433,002 bytes / 4,361 lines** with a stored mtime of **08:27**, matching the job's completion at 08:27:54 UTC. The hung run's artifact was 1,667 bytes frozen at 12:01 against a 12:51 cancel.
- **A real framework summary line exists** and agrees with the parser's emoji-derived totals (§4).
- **The inline zero-executed guard was reached and satisfied** (363 matching progress lines), not merely "not fired".

`design_review_capture_test.dart` passed again — and again produced no usable evidence (§7).

## 6. Per-file counts — both platforms

### 6.1 Android (`flutter test integration_test/`, 17 targets, 26 cases) — **0 failures**

| Journey file | P/F/S | Verbatim failure or skip reason (excerpt) | Expected per findings? |
|---|---|---|---|
| `app_boots_test.dart` | **1/0/0** | — | Yes |
| `design_review_capture_test.dart` | **1/0/0** | — (`design-review captures (1/24)`; 23 bounded 1 s timeouts) | Yes — A-1 stays fixed (§5); capture *content* still absent (§7) |
| `journeys/attendance_journey_test.dart` | **1/0/0** | — | Yes |
| `journeys/auth_journey_test.dart` | **1/0/0** | — | Yes |
| `journeys/benchmark_journey_test.dart` | **1/0/0** | — | Yes |
| `journeys/cut_fill_journey_test.dart` | **1/0/0** | — | Yes |
| `journeys/daily_log_journey_test.dart` | **1/0/0** | — | Yes — and note it is the **web** copy of this file that fails (§6.2, §8) |
| `journeys/data_bucket_journey_test.dart` | 1/0/**1** | Part A skipped: `Unverified: Google Drive service-account credentials absent — supply GOOGLE_DRIVE_SERVICE_ACCOUNT_EMAIL and GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY (plus GOOGLE_DRIVE_FOLDER_ID) via --dart-define to verify. STEP-48 defers this deliberately (PLAN decision D2): NR-004 … RISK-0017 … NR-005 … RISK-0018 …` | Yes — D2, predicted |
| `journeys/deep_link_journey_test.dart` | **2/0/0** | — | Yes — both cases green; the DISPOSED-teardown overflow did not fire again |
| `journeys/equipment_check_journey_test.dart` | **1/0/0** | — | Yes |
| `journeys/inventory_journey_test.dart` | **1/0/0** | — | Yes |
| `journeys/land_clearing_journey_test.dart` | **1/0/0** | — | Yes |
| `journeys/notifications_journey_test.dart` | **1/0/0** | — | Yes |
| `journeys/offline_sync_journey_test.dart` | **6/0/0** | — | **Newly green** — previous R-1 fixed; 5/1/0 → 6/0/0, the LWW leg now passes (§9) |
| `journeys/reporting_journey_test.dart` | **1/0/0** | — | Yes |
| `journeys/rls_authorization_journey_test.dart` | 2/0/**1** | Part A crew leg skipped: `Unverified: crew staging credentials absent — STEP-48.0 created the crew@mineflow.dev account in staging but published no TEST_CREW_* repository secrets, so the crew leg of the RLS matrix cannot run. Supply TEST_CREW_EMAIL / TEST_CREW_PASSWORD via --dart-define to verify. No other role is substituted, because a supervisor or foreman session would silently invalidate every crew assertion.` | Yes — RISK-0021, predicted |
| `journeys/timeline_journey_test.dart` | **1/0/0** | — | Yes |

**Android delta vs `33879989164`:** `++` offline_sync (5/1/0 → 6/0/0) · `--` none · skips unchanged at 2. Net 23 → **24 passed, 1 → 0 failed**, job conclusion `failure` → **`success`**.

### 6.2 Web (`flutter drive` per-file loop, 16 targets)

| Journey file | Web | Slot end (UTC) | min | Verbatim failure reason (excerpt) |
|---|---|---|---|---|
| `app_boots_test.dart` | **pass** | 08:02:30 | 1.5 | — |
| `journeys/attendance_journey_test.dart` | **pass (was fail)** | 08:04:17 | 1.8 | — (previous R-2 fixed) |
| `journeys/auth_journey_test.dart` | **pass** | 08:05:52 | 1.6 | — |
| `journeys/benchmark_journey_test.dart` | **pass** | 08:07:34 | 1.7 | — |
| `journeys/cut_fill_journey_test.dart` | **pass** | 08:09:29 | 1.9 | — |
| `journeys/daily_log_journey_test.dart` | **fail** | 08:11:10 | 1.7 | `Expected: LogStatus:<LogStatus.submitted>` / `Actual: LogStatus:<LogStatus.draft>` @ `daily_log_journey_test.dart 136:9`, test `login, create structured daily log with zone CreatableCombobox, assert attribution (CF-006/007), list visibility, and draft isolation (CF-008) E2E` |
| `journeys/data_bucket_journey_test.dart` | **pass** | 08:12:44 | 1.6 | — |
| `journeys/deep_link_journey_test.dart` | **pass** | 08:14:30 | 1.8 | — |
| `journeys/equipment_check_journey_test.dart` | **pass** | 08:16:12 | 1.7 | — |
| `journeys/inventory_journey_test.dart` | **pass** | 08:18:08 | 1.9 | — |
| `journeys/land_clearing_journey_test.dart` | **pass** | 08:19:52 | 1.7 | — |
| `journeys/notifications_journey_test.dart` | **pass** | 08:21:24 | 1.5 | — |
| `journeys/offline_sync_journey_test.dart` | **pass** | 08:22:51 | 1.5 | Part A returns early on web via `markTestSkipped` + `return` (Doc 15 §1 / 48.23 Q12); Part B runs |
| `journeys/reporting_journey_test.dart` | **pass** | 08:24:25 | 1.6 | — |
| `journeys/rls_authorization_journey_test.dart` | **pass** | 08:26:04 | 1.6 | — |
| `journeys/timeline_journey_test.dart` | **pass** | 08:27:39 | 1.6 | — |

**Web delta vs `33879989164`:** `++` attendance · `--` daily_log. Net **15 → 15 true**, composition changed. Per-file web outcomes across all six gates, for the two files that moved:

| File | `90a995c` | `2b2fa3f` | `78bd12d` | `310fea5` | `9288168` | **`c73a00e`** |
|---|---|---|---|---|---|---|
| `attendance_journey_test.dart` | false | false | false | false | false | **true** |
| `daily_log_journey_test.dart` | false | false | false | false | true | **false** |

Attendance is the cleaner story: **five consecutive red gates, now green** — 48.22's re-run-5 SnackBar-drain fix is confirmed at the tested surface, and the `Found 0 widgets with type "AttendanceFormPage"` string that survived three gates is gone from the run entirely.

Two structural properties held again: every web file finished in **1.5–1.9 minutes** (no journey hogs the budget), and `Multiple exceptions (N)` appears **0 times** in either log, so the one residual carries a decoded assertion and a `file:line` and needs no local re-run to classify. `design_review_capture_test.dart` is not in the web loop's glob (`integration_test/app_boots_test.dart integration_test/journeys/*_test.dart`), so the capture matrix runs on Android only in CI.

## 7. Skip audit and vacuous-pass checks

**Two skips, both the predicted ones**, quoted verbatim in §6.1 from the Android job's `##[group]⏭️ Skipped tests` blocks: `data_bucket_journey_test.dart` Part A (Drive credentials → D2 / 48.14 / RISK-0017+0018) and `rls_authorization_journey_test.dart` Part A crew leg (`TEST_CREW_*` → RISK-0021 / 48.12). Both are the `2 skipped` in the framework summary. **Zero unexplained skips.** The supervisor and foreman legs of the RLS matrix **pass** on CI where the foreman leg skips locally — CI remains the stricter measurement.

Web structurally cannot report skips (`flutter drive` emits one per-file `result{}` and no skip markers), so the offline-sync Part A and data-bucket Part A web skips are invisible in that log by construction. Verified in source on the pushed tree instead, with a statement-aware audit that walks each `markTestSkipped(` call to its closing paren at depth 0 and then requires the next non-blank, non-comment statement (`.scratch-tmp/step4826_r4_skipaudit.py`, enumerating 21 `.dart` files under `integration_test/`):

- `markTestSkipped` **call statements**: **23**. Immediately followed by `return;`: **23**. Violations: **0.**
- A naive fixed-window grep reports 6 false positives here (long reason strings push `return;` past a 5-line window, plus one mention inside a doc string in `helpers/login_helper.dart:88`). The statement-aware count is the correct one; recording the discrepancy so a future pass does not "discover" a regression that is a parser artefact.
- `expect(true, …)` active sites: **0**.

**Assertion-count check on the files that moved** — `grep -c 'expect('` at `9288168` versus HEAD: attendance **21 → 22** (+1, 48.22's `findsNothing` drain guard), offline-sync **34 → 36** (+2, 48.23's server-side premise guards), daily-log **20 → 20**. Nothing was removed or loosened; the newly-green attendance and offline-sync files each got *stricter*.

**Carried-forward evidence defect, re-verified and unchanged.** All **73** PNGs under `Code/mine-flow-docs/reports/design-review/step-0048/` are **68 bytes**, hex-confirmed `PNG … IHDR 00000001 00000001` (1×1), and **none** carries an `android-` prefix. Hold two facts together:

- **A-1 is fixed** — the capture harness can no longer wedge the gate (§5).
- **Android design-review capture still produces nothing usable** — `design-review captures (1/24)` with 23 `Warning: takeScreenshot(...) timed out after 1s` lines (identical to gate 3's 23), and both E2E jobs report `No files were found with the provided path: screenshots/`, so the `android-screenshots` / `web-screenshots` artifacts are empty. Worth naming the structural reason: nothing in the repository ever writes to `screenshots/` — `test_driver/integration_test.dart`'s `onScreenshot` writes to `../mine-flow-docs/reports/design-review/step-0048/`, while `ci.yml:217` and `ci.yml:290` upload `screenshots/`. The two paths have never agreed. The harness *fails safe*, which is what the gate required of it; the design-review coverage it was meant to underwrite does not exist. Recorded as a finding, not fixed; nothing here was deleted or overwritten.

## 8. Residual failure — classification and assignment

Exactly one red per-file row, and per this gate's own re-run-3 rule it gets a register id and an owner.

| # | Failure | Class | Was it known? | Assignment |
|---|---|---|---|---|
| **R-1** | Web daily-log journey, step 9 read-back: `Expected: LogStatus:<LogStatus.submitted> / Actual: LogStatus:<LogStatus.draft>` @ `daily_log_journey_test.dart:136`. Web only; Android passes the same line and has **never** produced this actual in any gate of the wave. | **app defect (concurrency), with a test-hardening half** — not a flake, and not a regression: `git diff --stat 9288168..c73a00e -- lib/` is empty, so no application byte changed since the gate where this file passed on web | **Yes — known, register-documented, and deliberately left unowned.** It is 48.23's **failure B** verbatim (`Deferred` "pending a deliberate re-assertion" across four gates), the class 48.21 re-run 3 handed forward as a "one-off status flake (owner 48.23/48.22)", and the row 48.24 re-run 4 called R-1 while ordering **no re-run**. Red on web at 3 of 6 gates; reproduced in 48.24's own local web loop on this code. | **Re-run 48.23** (owns persistence/offline-integrity, and failure B is literally this assertion). Fix the app, then the harness; do **not** weaken the assertion. |

**Mechanism, derived from source rather than guessed** — three sites, all read this session at HEAD:

1. `daily_log_form_screen.dart:95–101` — `_debouncedAutoSave()` arms a **500 ms** `Timer` that dispatches `AutoSaveDraftEvent`. It is armed by the notes field's `onChanged` (`:377–379`) and the summary field's (`:347–351`).
2. `daily_log_form_screen.dart:389–405` — the submit button's `onPress` dispatches `NotesChangedEvent` then `SubmitDailyLogEvent`. It does **not** cancel `_autoSaveDebounce`. Only `dispose()` (`:113`) cancels it.
3. `daily_log_bloc.dart:24–25` registers both handlers with **no transformer**, so `bloc` 9.2.1's default applies — `Bloc.transformer` is documented "By default all events are processed concurrently" (`bloc-9.2.1/lib/src/bloc.dart:50–61`). `_onAutoSaveDraft` (`:188–194`) guards only on `currentState.log.status != LogStatus.draft`; `_onSubmitDailyLog` (`:223–248`) emits `isSubmitting: true` **with the log still `draft`**, then awaits two repository calls before emitting `log: updatedLog` (status `submitted`). Throughout both awaits the autosave guard passes.
4. `daily_log_repository_impl.dart:120–137` — `autoSaveDraft()` **forces `status: LogStatus.draft`** on whatever it is handed and writes it to the Hive cache with a fresh `updatedAt`. Submit itself calls it at `:247` (harmless, it is followed by `submitDailyLog(id)` at `:248` which writes `submitted`), but a *concurrent* autosave firing after `:248` re-stamps the row back to `draft`. The journey then reads `getDailyLogs()` (`:54–93`), which is a local-cache read — so the last local write wins and the assertion sees `draft`.

The journey's timing makes this reachable, and reachable more often on web: `enterText` at `:112` arms the timer, `pumpAndSettle()` at `:113` typically settles in well under 500 ms, the tap lands at `:119` with the timer still pending, and `pumpAndSettle(const Duration(seconds: 2))` at `:120` then covers the moment it fires. Web's slower Hive/IndexedDB and network round-trips widen the interval between `:247` and the post-`:248` write, which is why the platform asymmetry is stable rather than coincidental.

This is also **why the existing lower-tier pin cannot catch it**: 48.23's failure-B regression test asserts submit→`submitted` persists in cache and payload, sequentially. Nothing models a concurrent `AutoSaveDraftEvent`. The re-run must add a pin that dispatches `AutoSaveDraftEvent` while `SubmitDailyLogEvent` is in flight and asserts the cache ends `submitted` — per the PLAN's test plan, the defect must be catchable without a staging round-trip.

**Class sweep already done for the re-run's benefit** (so the prompt carries the site list, not just the line):

- `grep -rn "Timer(const Duration(milliseconds" lib/` → 4 debounce sites. Only **one** dispatches a write event: daily-log's `AutoSaveDraftEvent`. `equipment_history_screen.dart:85` and `data_bucket/.../search_bar_widget.dart:46` debounce *reads*; `inventory_item_entry_screen.dart:186` debounces a `pop`. So the "debounced write racing a submit" class has exactly one member today.
- `grep -rn "isSubmitting)" lib/features/*/presentation/bloc/*.dart` with an `if`/`return` → **0 hits.** No handler anywhere guards on `isSubmitting`. Four blocs carry the flag (`attendance`, `auth`, `daily_log`, `equipment_check`), so the *shape* is latent elsewhere even though no other bloc currently has a competing debounced writer.
- `grep -rn "status: LogStatus" lib/features/*/data/repositories/*.dart` → the only repository that force-writes a status is `daily_log_repository_impl.dart:113` (`getDraftLogForForeman`'s filter) and `:123` (the `autoSaveDraft` force). The force at `:123` is the one that turns a benign late write into a status downgrade.

Candidate fixes are **not** equivalent, and the substep must say which it chose: cancelling the debounce in the submit handler fixes this widget only; guarding `_onAutoSaveDraft` on `isSubmitting || isSubmitted` fixes the bloc against any dispatcher; making `autoSaveDraft` refuse to downgrade a non-draft row fixes the persistence contract itself. The last is the strongest and the one the class sweep points at — an autosave should never be able to un-submit a log — but it changes a repository contract, so it needs its own pin and a Doc 04 note.

**Nothing was accepted because "most things pass."** One row, one owner, one named class.

**Gate-observability items, recorded not acted on** (48.26 fixes nothing, and a `ci.yml` change would move the branch head the gate must measure):

1. **16 of 17 integration files still carry no explicit `timeout:`** (`grep -L 'timeout: const Timeout'` → only `design_review_capture_test.dart` is bounded). The "one file can consume the whole 60-minute budget" class is narrowed to one file, not eliminated. Unchanged from gate 3.
2. `ci.yml`'s screenshot uploads point at `screenshots/`, which nothing writes (§7). The gate uploads nothing where it claims to upload evidence — a one-line path fix, but an owner decision because it moves the head.
3. `test_driver/integration_test.dart` still does not print the full `failureDetails` payload. Latent; it did not bite (0 opaque failures).
4. `design_review_capture_test.dart` is not a journey yet sits inside the Android gate glob. Moving it to an explicit non-gating invocation would decouple design-review evidence from the release gate. Owner decision.
5. **Re-run-3's procedural rule proved its worth in the negative direction this round.** The rule was "every red per-file row gets a register id or an explicit sentence why not". 48.24 *did* give this failure a register id — and then ordered no re-run on a flake argument whose supporting count was wrong. Strengthen the rule: a red row may be dismissed as a flake only with the per-gate history of that exact assertion re-parsed from the logs, and never when its mechanism is reachable in source.

## 9. Earlier Deferred items this run gives new evidence about (re-weigh, do not reopen blind)

- **Previous register R-1 (offline-sync LWW leg @ `:365`), owned by 48.23 — fixed, confirmed on CI.** `offline_sync_journey_test.dart` is **6/0/0** on Android (was 5/1/0), and the registrar's skip branch logs for the first time in any gate: `[WARNING] DailyLogSyncRegistrar: Conflict for daily log [f42f657e-…]: remote (2026-09-05 08:13:11.121725Z) is newer than queued mutation (2026-09-05 08:13:09.116373Z). Remote wins.` — 3 hits, against **0** at gate 3. The two-second gap between the stamps is exactly the explicit client `updated_at` the fix added, and both server-side premise guards passed (the conflict was real, not vacuous). The contract note for 48.15 stands: **a writer that must participate in LWW has to send its own `updated_at`.**
- **Previous register R-2 (web attendance cannot mount `AttendanceFormPage` @ `:225`), owned by 48.22 — fixed, confirmed on CI.** Web attendance is green after five consecutive red gates, the error string is absent from the run, and the file's assertion count went **up** (21 → 22). 48.22's diagnosis — the save's SnackBar layer winning the hit-test at the FAB centre on the desktop-web surface, expiring faster on Android — is supported: the fix is test-side and the platform asymmetry it predicted is exactly what disappeared.
- **48.23 failure B (daily-log `submitted` vs `draft`), `Deferred` — its deliberate re-assertion has now happened and it FAILED.** This is the one re-weigh that changes an outcome rather than adding evidence: four gates of "passes on both platforms, status cell stays Deferred pending a deliberate re-assertion" ended with a red on web. It becomes this run's **R-1** (§8), with a mechanism, not a flake note. **The status cell is not edited by this substep** — 48.23 owns that once its fix lands.
- **48.22's deep-link DISPOSED-teardown overflow, `Deferred` — did not fire again.** Green on web and 2/0/0 on Android for the fifth consecutive platform-pass. Status unchanged (the render object was never identified and the named unblock was never run); five passes are further evidence it is intermittent, not deterministic. **Do not mark it fixed.**
- **48.20's Q10 verdict (`42501` on `zones` is a correct refusal).** Six `42501` lines, all `zones`, and every affected journey passes. Adjudication holds; not a residual failure.
- **A-1 (Android gate hang), owned by 48.22 — stays fixed** (§5), with the design-review *content* defect still open and still separate (§7).
- **The Hive `setUpAll` / drain-window unit flake — silent for the sixth consecutive gate** (505/505, no `Some tests failed`). Still worth no status change, but the streak is now long enough to be worth quoting in 48.15's close.

## 10. NO-GO consequences — substeps to re-run, in order

1. **48.23** (Opus 4.8) — **R-1.** The daily-log autosave/submit interleaving that can re-stamp a submitted log back to `draft`. Its prompt must carry: the verbatim `Expected: LogStatus:<LogStatus.submitted> / Actual: LogStatus:<LogStatus.draft>` payload and the `daily_log_journey_test.dart 136:9` frame; the four source sites in §8 (`daily_log_form_screen.dart:95–101`, `:389–405`; `daily_log_bloc.dart:24–25`, `:188–194`, `:223–248`; `daily_log_repository_impl.dart:120–137`); `bloc`'s concurrent-by-default transformer as the enabling fact; the class sweep results (one debounced writer, zero `isSubmitting` guards anywhere, one status-forcing repository write); the requirement to add a **concurrency** pin at the lowest tier that can catch it (dispatch `AutoSaveDraftEvent` mid-submit, assert the cache ends `submitted`); the instruction to say **which** of the three candidate fixes it chose and why; and the fact that `git diff -- lib/` since `9288168` is empty, so this is not a regression to bisect. It must **not** weaken `:136`, and it must verify on **web** at the tested surface, since Android has never reproduced it.
2. **48.24** (Flash 3.7) — local full-gate re-run on the resulting tree. Confirm a **complete** Android suite (17/17 installs, a framework summary line) and the web loop, per-file. Given §4a, it must also re-parse this gate's log rather than re-asserting a flake verdict from prose, and it must run the daily-log web file **more than once** if it wants to argue timing.
3. **48.25** (Opus 4.8) — commit and **push** the branch head, then hand the auto-triggered run id forward. This substep will not cross into that lane; three consecutive passes have proved the routing works.
4. **48.26** (this substep) — new branch-head CI run and a fresh verdict, under the strengthened rule in §8 item 5.

48.22's deep-link `Deferred`, 48.20's Q10 adjudication, and 48.13/48.22's screenshot-content defect are re-weighed, not re-run (§7, §9). Nothing in this list belongs to 48.15. **48.15 must not run until items 1–4 are complete and all four jobs are green.**

Distance to GO, stated plainly: `test`, `build-android` and `e2e-android` are green, `e2e-web` is red on one assertion in one file, and that assertion has a named mechanism and an owner. This is the smallest gap the gate has reported.

## 11. Re-run 3 record (2026-09-04, retained)

Run [`33879989164`](https://github.com/lvinist/mine-flow-app/actions/runs/33879989164) on sha `928816838d73fbda25af41064a8645075395ef54` (verified byte-equal to local HEAD and `origin`; fsck clean; sixteen wave commits present; `?head_sha=` → `total_count: 1`). Verdict **NO-GO**. `test` **success** (`🎉 498 tests passed.`) · `build-android` **success** · `e2e-android` **failure** (`23 passed, 1 failed, 2 skipped`) · `e2e-web` **failure** (15 of 16 green). Deltas: Android 20/4/2 → 23/1/2; web 12 → 15 true; zero regressions. A-1 confirmed still fixed (17/17 installs, 435 KB / 4,393-line artifact, guard reached and satisfied with 362 progress lines). `23505`, `22P02`, `23503`, `PGRST204`, `PGRST205` all absent; `42501`×6 = the adjudicated `zones` refusal; `Multiple exceptions` 0. Skips 2, both predicted. Its register, cited elsewhere by row id:

| Row | Defect | Outcome at `c73a00e` |
|---|---|---|
| R-1 | Offline-sync Part A LWW leg: server row keeps the stale queued edit @ `offline_sync_journey_test.dart:365`; test-defect (stale premise — `20260901000001` removed the `NOW()` stamping the setup relied on) → 48.23 | **Fixed** — Android `offline_sync` 6/0/0, registrar skip branch logs 3× on CI, premise guards pass (`cf9e8ca`) |
| R-2 | Web attendance cannot mount `AttendanceFormPage` on the second `context.push` @ `attendance_journey_test.dart:225`; fix-completeness with an ownership gap (three gates, no register row, no owner) → 48.22 | **Fixed** — web attendance green, string absent run-wide, assertions 21 → 22 (`c73a00e`) |

It also recorded the procedural finding that every red per-file row must get a register id or an explicit reason why not — §8 item 5 strengthens it after 48.24 satisfied the letter and not the spirit.

## 12. Re-run 2 record (2026-09-03, retained)

Run [`33734562106`](https://github.com/lvinist/mine-flow-app/actions/runs/33734562106) on sha `310fea5855e26af2b7fec573498f94e72bd0c7b4`. Verdict **NO-GO**. `test` **success** (`🎉 489 tests passed.`) · `build-android` **success** · `e2e-android` **failure** (`20 passed, 4 failed, 2 skipped`) · `e2e-web` **failure** (12 of 16 green).

Its headline was **A-1 resolved**: the Android job that had produced *zero* evidence completed in 22m25s with 17/17 APK installs and a real framework summary line. It also raised a **pre-flight blocker and routed it rather than absorbing it**: at first invocation HEAD was `bc10180`, **ahead 3** with 4 dirty files and `total_count: 0` runs for every unpushed sha, plus a CRLF regression in `036bea2` inflating a 7-line change to 459 lines; both went to 48.25, which fixed and pushed `78bd12d..310fea5`.

Its residual register, with outcomes: **R-1** cut/fill unique-notes read-back @ `:235` — **fixed** (48.21's newest-first read contract, `1b4bd2a`) · **R-2** offline-sync Part A undrainable, `attendance_records` upsert with no `onConflict` vs `UNIQUE (user_id, date)` → `23505` @ `:279` — **fixed** (`?on_conflict=user_id%2Cdate`, `2389a31`) · **R-3** daily-log summary not on `DailyLogListScreen` @ `:145` — **fixed** · **R-4** inventory decrement not persisted @ `:193`, web `Saved inventory item not found` @ `:139` — **fixed** (`9f8805d` + `9288168`/`formScope`) · **(unassigned)** web attendance `Found 0 widgets with type "AttendanceFormPage"` @ `:225`, listed in its per-file table with **no register row and no owner** — became re-run 3's R-2 and is **fixed** at `c73a00e`.

## 13. Re-run 1 record (2026-09-02, retained)

Run [`33626548011`](https://github.com/lvinist/mine-flow-app/actions/runs/33626548011) on sha `78bd12dd3253f5749b37620b013f52a1e92747cb`. Verdict **NO-GO**. `test` **success** (487 tests) · `build-android` **success** · `e2e-web` **failure** (10 true / 6 false) · `e2e-android` **cancelled**.

The dominant finding was structural: `e2e-android` hit `timeout-minutes: 60` inside `flutter test integration_test/` and produced **zero** test output. The artifact was **1,667 bytes** with mtime **12:01 UTC** against a **12:51** cancel, and **0 APK installs** against 17/17 in the healthy baselines, so file #1 never completed. `defaultTestTimeout = Timeout.none` meant nothing in the framework could abort it; the inline zero-executed guard sits after `flutter test` in the same `sh -c` and was **never reached**. The hung file was *inferred* (not proven) to be `design_review_capture_test.dart`; a `rerun-failed-jobs` was considered and declined with reasons recorded. Its register: A-1 (the hang, **fixed** by `036bea2`), R-1 web attendance `:223` (Android fixed; web unfixed → §12's unassigned row → re-run 3's R-2, now **fixed**), R-2 web benchmark `pumpAndSettle` 11.5 min (**fixed**), R-3 web cut/fill read-back `:231` (→ §12's R-1, **fixed**), R-4 daily-log `DailyLogListScreen` never mounts / BH-020 (**fixed**), R-5 web deep-link `Multiple exceptions (2)` (**did not fire**; underlying Deferred open), R-6 web inventory opaque (**scoping fixed**; the defect behind it → §12's R-4, **fixed**).

## 14. First-pass record (2026-09-01, retained)

Run [`33480009094`](https://github.com/lvinist/mine-flow-app/actions/runs/33480009094) on sha `2b2fa3f81ba4e902e4db8def3878aea343d5e22d`. Verdict **NO-GO**: `test` **success** (457 tests, contract + l10n guards OK), `build-android` **success**, `e2e-web` **failure** (8 true / 8 false), `e2e-android` **failure** (`15 passed, 9 failed, 2 skipped`). Executed counts non-zero, zero-executed guard did not fire, both skips legitimate and predicted (Drive/D2 → RISK-0017/0018; crew RLS leg → RISK-0021), each verbatim-quoted, each `markTestSkipped` followed by `return;`; `expect(true` = 0. Real progress vs `33327930159` (Android 14 → 15 passed; web 6 → 8 green): `PGRST205` and all `Too many elements` / `No element` finder errors gone. Its register, still the reference other findings cite:

| Row | Defect | Assigned to |
|---|---|---|
| R-1 | BH-019 Material-ancestor still live at `date_range_selector.dart:124` (8 `DropdownButton*` sites in `lib/`) | 48.22 — **fixed** (`FSelect`; reporting journey green on both platforms) |
| R-2 | BH-015 `RenderFlex` class at `cut_fill_card.dart:33`, `land_clearing_card.dart:30/:34` | 48.22 — **swept** (7 card widgets; 4 previously unnamed) |
| R-3 | Android capture: `No GoRouter found in context` (`design_review_capture_test.dart:80`) | 48.22 — **fixed** (`appRouter`); superseded by A-1, itself fixed |
| R-4 | Data-bucket Part B renders 0 `FileCard` though staging holds the re-sited seed row | 48.20 + 48.22 — **fixed** (`watchFiles`; green both platforms) |
| R-5 | Empty-string UUIDs reaching `zones` (`22P02` → `23503`) and `benchmarks` | 48.20 — **fixed** (`Uuid().v4()`; `22P02`/`23503` absent from this run too) |
| R-6 | BH-009/010 `KRU-001/002/003` non-UUID roster; attendance remark not shown | 48.20 — **fixed** (real site roster; attendance green on both platforms at `c73a00e`) |
| R-7 | Cut/fill `OB / Waste` unfindable; land-clearing save tap misses | 48.21 — **fixed** (generics-aware combobox finders; both green) |
| R-8 | Web-only opaque `inventory` `Multiple exceptions`, Android green | classified by 48.24, **fixed**; "unclassifiable" retired |

## 15. Not done here (scope discipline)

No defect was fixed. No application code, test, migration, staging row, `risks.yml` status, architecture doc, `prompts/STEP-index.md` row, or archive was touched. STEP-48's index row and status are untouched. The only writes are this findings file, the PLAN's 48.26 progress row, and evidence-plus-assignment amendments to the PLAN's 48.22 / 48.23 / 48.24 progress rows (**status cells left alone** in all three).

No staging query was issued. Every claim above is derived from the six gates' CI job logs, this run's `android-e2e-log` and `web-e2e-driver-log` artifacts, the repository at `c73a00e`, the Flutter SDK and `bloc` 9.2.1 sources, and the committed migrations. No secret value appears anywhere; CI's `***` masking is preserved verbatim in every quoted line, and the PAT used for the API reads was taken from Git Credential Manager and never echoed.

Evidence retained under `$LOCALAPPDATA/Temp/step4826_r4/`: this run's four job logs (`job_101273733268`, `job_101274030710`, `job_101274030722`, `job_101274030761`), all five prior gates' E2E job logs re-fetched for re-parsing (`hist_*.log`, `base_*.log`, `gate2_web.log`), and both artifacts unzipped (`art/integration_test.log` 433,002 bytes / 4,361 lines; `art/all_web.log` 45,625 bytes). Two read-only helpers were added to `.scratch-tmp/`: `step4826_r4_audit.py` (skip/vacuous/timeout enumeration) and `step4826_r4_skipaudit.py` (the statement-aware `markTestSkipped` + `return;` walk that corrects the fixed-window false positives).

**Safety-net status:** 48.25's retired-tree backups do not exist and were not needed; `git fsck --full` is clean and `origin` holds every wave commit. Nothing was deleted.

**Prompt erratum, carried from all four prior passes:** the prompt's Definition of done asks for "`mine-flow-STEP-48.25-FINDINGS.md` written". That file is 48.25's and already exists; this substep's record is this file.

## 16. Definition of done

- [x] Branch head verified pushed by 48.25 (no push attempted here); sha recorded and matched to the run's `head_sha`, remote re-read via `ls-remote`, uniqueness proved by `?head_sha=` → `total_count: 1` (§2).
- [x] A single CI run identified with all four required jobs' ids, conclusions, and windows (§3).
- [x] Per-file counts extracted from job logs for **both** platforms; both tables complete (§6). Android's emoji-derived totals cross-checked against the framework summary line.
- [x] Run totals stated against **all five** prior gates with deltas, each re-parsed from its own log in this session (§4), plus the local-gate comparison and where it was wrong (§4a).
- [x] Executed counts confirmed non-zero on both platforms; web zero-executed guard confirmed not fired; Android guard confirmed reached and satisfied (§4).
- [x] A-1 confirmed still resolved with install count, artifact size/mtime, framework line, and guard state (§5).
- [x] Every skip's verbatim reason quoted and reconciled to D2 / RISK-0021; zero unexplained skips; statement-aware source audit 23/23 `markTestSkipped` + `return;`, 0 violations, 0 active `expect(true`; assertion counts checked on every file that moved (§7).
- [x] Vacuous-pass spot-check done; the 73 vacuous 1×1 committed screenshots and the empty screenshot artifacts re-recorded as a live defect, with the `screenshots/` path mismatch newly named (§7).
- [x] The residual failure classified, mechanism derived from source, class swept, and assigned to one owner; the prior round's flake dismissal overruled with re-parsed per-gate history (§8, §4a).
- [x] Explicit verdict with the close criterion quoted verbatim (§1).
- [x] NO-GO: substeps to re-run listed in order with named defects (§10); earlier Deferred items re-weighed rather than reopened, and the one whose deliberate re-assertion has now fired identified as such (§9).
- [x] `mine-flow-STEP-48.26-FINDINGS.md` written (re-run 4 record; prior passes retained in §11–§14 with their registers intact); PLAN progress table updated (48.26 row replaced; 48.22/48.23/48.24 rows amended with evidence and, for 48.23, the new assignment — status cells untouched).
- [x] STEP-48's index row and status untouched — verified after writing.
- [x] Docs-hub `scripts/check.sh` run; fail/warn counts quoted in §17.

## 17. Post-write verification

- `Code/mine-flow-app`: `git status --short` clean, HEAD still `c73a00e`, equal to `origin` — this substep wrote nothing into the app repo.
- `Code/mine-flow-docs`: clean at `41cfbb6`, untouched.
- `prompts`: still on `step-0050-phase3-check-in` with only its pre-existing `STEP-index.md` modification (STEP-50's lane) — no STEP-48 row edited.
- `Code/mine-flow-docs/scripts/check.sh`: **0 fails, 1 warning** — the pre-existing workspace-root hygiene WARN listing this STEP's evidence logs, unchanged in kind by this substep.

## Next

Run **`run substep 48.23`** in a **fresh chat**, scoped to **R-1**: the daily-log autosave/submit interleaving that can re-stamp a submitted log back to `draft` on web. Hand it this run's URL, sha `c73a00e`, the verbatim `Expected: LogStatus:<LogStatus.submitted> / Actual: LogStatus:<LogStatus.draft>` payload with the `daily_log_journey_test.dart 136:9` frame, §8's four source sites and class sweep, and the instruction that Android cannot reproduce it — verification has to be on web. Then **48.24 → 48.25 → 48.26**. STEP-48 remains `In progress` and Phase 4 remains closed.
