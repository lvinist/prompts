# mine-flow — STEP-55.11 RESIDUAL-3 PROMPT — capture-harness fix, runtime evidence matrix, and close-path reconciliation

**Assigned model:** Hermes/Claude Opus 4.8 (same tier as 55.11 — this lane decides
whether runtime evidence honestly supports the close verdict; silent-failure risk).
**Date drafted:** 2026-10-03, by Hermes parent session. Every fact below was
re-derived on disk at app head `03180ec` on the drafting date — re-locate line
numbers and re-verify run facts at execution time; the branch can move mid-session
(pull first).
**Branches:** app+docs `step-0055-cohesive-ui-rebuild`; `prompts/main`.

## Why this exists

RESIDUAL-2 (B-fix lane, `mine-flow-STEP-55.11-RESIDUAL-2-FINDINGS.md`) closed all
five E2E product/fixture defects and is CI-verified: **run 139 (`37003629360`,
head `03180ec`)** — Web E2E green (16/16 journey files `"result":"true"` in the
`web-e2e-driver-log` artifact), **Android journeys green (23 passed / 2 skipped**;
both skips documented: `rls_authorization` Part-A crew policies, `data_bucket`
Drive-dependent), Lint/analyze + APK build green. The Android **job** is red for
exactly one unrelated, pre-existing reason: the design-review capture matrix. This
lane fixes that harness, produces the runtime evidence the deferred FC items need,
and reconciles the close path. It does not re-open any B item.

## The one remaining red gate (evidence, already pulled)

- Run 139 Android capture leg wrote **2/25 PNGs** — `android-login-phone-light-en.png`
  (67,183 B) + `android-dashboard-phone-light-id.png` (131,059 B), verified inside
  the run's `android-screenshots` artifact — and logged **23×
  `Warning: takeScreenshot(<name>) timed out after 5s`**, then the matrix `expect`
  at `integration_test/design_review_capture_test.dart:208` failed
  ("All 25 matrix cells must produce valid screenshots on android-").
- **Deterministic across three independent runs**: 2026-09-14 audit (2/24), run 138,
  run 139 (2/25) — identical 2-then-nothing signature.
- **All 23 timeout warnings in run 139 share one wall-clock second**
  (`12:27:15.53x`): the per-cell 5s deadlines are NOT being consumed in real time —
  the loop's `Future.any([capture, delayed(100ms)])` polling either starves the
  event loop or all captures resolve/fail en masse after one long stall.
- The **web** matrix showed the same stall on 2026-09-14 (23 timeouts after
  login/dashboard), and the current web CI job does not drive the capture test at
  (its drive loop = app_boots + journeys only). Same signature on two different
  capture backends ⇒ the defect class is the **shared harness**
  (`_captureScreenshot` helper + binding completion semantics), not a route,
  platform, or product defect. Fix it ONCE in the harness, not per-platform.

## Residual scope (exact — nothing else)

1. **Local repro + root cause — NO blind CI pushes.** The loop-discipline rule
   applies: this failure has survived 4+ CI runs; do not add a fifth guess.
   Reproduce on **web first** (cheaper, no emulator), driving ONLY
   `integration_test/design_review_capture_test.dart` via a scratch
   `flutter drive -d web-server` invocation (pattern: existing
   `.step55.11h-run-web.sh`; runner stays untracked). Add temporary
   instrumentation (cell index, wall clock around each capture, whether the
   `takeScreenshot` future EVER resolves). Candidate mechanisms to falsify, in
   order:
   a. The capture future only completes when a genuinely scheduled engine frame
      rasterizes; login (post-`convertFlutterSurfaceToImage`/post-login frames)
      and cell 1 (post-login animations) had dirty frames, and from cell 2 on a
      fully-settled tree schedules none — the loop's `tester.pump(100ms)` may not
      produce an engine-level frame the capture waits on.
   b. Event-loop starvation: `Future.any` + `DateTime.now()` busy-loop inside
      testWidgets preventing the capture completer from running (consistent with
      all 23 warnings in one second).
   c. Surface-conversion invalidation on Android
      (`convertFlutterSurfaceToImage` + `tester.view.physicalSize` changes) —
      weaker, since the web leg skips conversion and still stalls.
   Record the falsification trail in FINDINGS; delete instrumentation before commit.

2. **Fix once in the shared harness** (`integration_test/design_review_capture_test.dart`
   `_captureScreenshot`, and only there). Keep intact: the 68-byte-placeholder and
   PNG-magic validation, the anti-clobber protected-steps list, and the
   `SCREENSHOT_DESTINATION_DIR`/args resolution in `test_driver/integration_test.dart`.
   If the root cause proves to be product `lib/**` rendering, STOP and present it —
   do not fix product code inside this lane.

3. **Full-matrix verification locally on BOTH platforms.** Android via the
   existing single-journey runner pattern (`.step55.11i-run-android.sh`, Pixel_6a),
   web via flutter drive. Require 25/25 valid PNGs per platform (login + 24 cells;
   Android prefixed `android-`). Then push ONCE and read CI run ≥140: the Android
   job must be green INCLUDING the capture leg; web journeys must stay green.

4. **Produce + archive the runtime evidence matrix.** Copy the real captures into
   `Code/mine-flow-docs/reports/design-review/step-0055/` on the docs STEP branch,
   with a dated matrix-index markdown (per-cell file, size, platform). Adjudicate
   from the captures and record per-FC verdicts in the close addendum:
   - FC-54.2-007 (Cut & Fill runtime audit — captures/contrast/targets)
   - FC-54.3-007 (Land Clearing runtime audit)
   - FC-54.5-004 / FC-54.5-013 (Attendance runtime audit)
   Anything not provable from captures (cold-start/refresh, reduced-motion, IME,
   authenticated-shell AX, hardware screen-reader) stays **Unverified** with the
   blocker named — do not infer a pass from a green screenshot.
   Also run the web matrix (item 3's web leg is that evidence — the CI web job
   never produces it).

5. **Web daily-log step-10 hardening (owed by RESIDUAL-2 B1).** Add the hard
   sheet-closed assertion to `integration_test/journeys/daily_log_journey_test.dart`
   step 10: bounded poll, then `expect` the `DailyLogFormSheet` route is gone with
   a reason carrying `appRouter` location, so the journey cannot pass vacuously.
   Cite: RESIDUAL-2-FINDINGS B1 "Web vacuous-pass note". Fixture-only; no lib edits.

6. **Close-path bookkeeping (mechanical reconciliation, all in this lane):**
   - Restore the 3 dirty gen-l10n files to HEAD (`git checkout --
     lib/l10n/app_localizations*.dart`) ONLY after re-proving `git diff -w` is
     empty (pure CRLF/EOL churn from the 2026-10-02 local gen-l10n run; zero
     content delta) and copying them aside into scratch first.
   - PLAN progress rows: 55.6 "OPEN DEFECT: cached-draft autosave-vs-submit
     collision" → superseded (B1 `a3d6b06` + RED→GREEN test + run-139 journey
     green); 55.7 Semantics note → equipment journey green in 139, no Semantics
     assert remains (verify); 55.9 → B5 `85d1994`; 55.10 C12 cross-reference →
     55.10-FINDINGS §5 already reconciled it.
   - Index rows: 55.1 — the row says the dialog-test matrix + `originFiltersSnapshot`
     are "still to add" but both are ON DISK as of 2026-10-03
     (`test/features/reporting/presentation/widgets/app_contextual_report_dialog_test.dart`,
     8 testWidgets: prefill, unsupported-filters, loading-dupe, error/retry, focus
     trap/return, barrier; `originFiltersSnapshot` in
     `app_contextual_report_dialog.dart:27,41,55`) — verify at HEAD and correct the
     row. 55.2/55.3 — record FC-54.X-007 verdicts from item 4. 55.8 — point at the
     ordering-test pin + extended contract guard (its statics are a SEPARATE lane:
     `mine-flow-STEP-55.8-RESIDUAL-2-PROMPT.md` — do not absorb them here).
     55.10 stays **In progress** (owner gates open). 55.3 findings' wrong
     FC-prefix: correct via a dated addendum, never rewrite the original section.
   - Commit the prompts STEP-index edit (the current 2-hunk diff is accurate
     through run 139 — re-verify against disk before committing), `git diff --check`,
     duplicate STEP-number scan, push to origin/main per the shared-trunk recipe.
   - Deep-link `/teams/daily-log → /teams` (55.10-FINDINGS §9): verify
     `deep_link_journey_test` results across runs 138+139 (green in 139 both
     platforms). If consistently green, record §9 as not-reproduced-since with the
     last red run named — do NOT claim it fixed. Keep §9's hardening
     recommendation (sync privacy-ack resolution before first redirect /
     refreshListenable) as a parked owner decision.
   - Disposition of the stray docs artifacts — untracked
     `reports/design-review/step-0055/2026-09-14-web-login-1258x566.png` and the
     preserved clobber set in `Upcoming Prompts/.step55.11c-step0048-clobber/` —
     is superseded-by-new-captures: record it in the close addendum as an
     owner-notebook item; do not delete silently.

7. **Honest close verdict.** Append a dated RESIDUAL-3 addendum to
   `Code/mine-flow-docs/reports/2026-09-19-step-0055.11-close-report.md`:
   final gates (run id + head sha, per-leg), capture-matrix counts, and the
   carried-conditions list — privacy-copy approval Unverified; RISK-0025
   (open/critical); RISK-0030 pending the STEP-56 seed decision; 55.8 remote
   contract (a)–(e) Unverified (no staging credentials); `database.ts` regen
   blocked on unapplied migration `20260913000001` (owner-gated
   `supabase db push --linked`). Verdict is **conditional** or **NO-GO** — never
   "unconditional". The STEP row flips to Done ONLY per the owner's call on the
   decision cluster below.

## Read first

- `Upcoming Prompts/mine-flow-STEP-55.11-RESIDUAL-2-FINDINGS.md` (commits + run-139 facts)
- `Upcoming Prompts/mine-flow-STEP-55.11-FINDINGS.md` §Runtime evidence inventory,
  §Remaining blockers, §Approval gate
- `Upcoming Prompts/mine-flow-STEP-55.11-RESIDUAL-PROMPT.md` (superseded items 1–7)
- `Code/mine-flow-docs/reports/2026-09-19-step-0055.11-close-report.md` (retracted close)
- Doc 07 (UI canon) + master spec FC-54.2-007 / FC-54.3-007 / FC-54.5-004,013
- The throughstone design-review-runtime-evidence reference (capture routes,
  stop-conditions, port cleanup)

## Pre-flight (do not skip)

1. `git status --short --branch` + `git log --oneline -5` in app and docs; pull the
   shared branch if it moved. Expected app head ≥ `03180ec`.
2. Preserve ALL untracked scratch (`.step55.*` scripts/JSON, runners,
   `run_web_wrapper.dart`, `test/widget/m2_challenger_stress_test.dart`,
   `tool/verify_test_driver_adversarial.dart`) — never stash/reset/absorb/commit.
   The gen-l10n restore in item 6 is the ONLY worktree mutation allowed here and
   only after the emptiness proof + copy-aside.
3. Serialize device runs: one emulator/web-drive at a time; clean up ports and
   emulator state between runs (runtime-evidence reference).

## Likely files (ownership boundary)

ALLOWED: `integration_test/design_review_capture_test.dart`,
`integration_test/journeys/daily_log_journey_test.dart` (step-10 assertion only),
scratch runners (untracked), `Code/mine-flow-docs/reports/design-review/step-0055/`
+ close-report addendum, `Upcoming Prompts/` PLAN/finding addenda, `prompts/STEP-index.md`
+ `mine-flow-STEP-55-PLAN.md` rows.
FORBIDDEN: product `lib/**`, `supabase/**`, `.github/workflows/**`, ARB files,
`test_driver/integration_test.dart` protections, the STEP-56 draft, other lanes'
scratch.

## Tests and verification

- Local web matrix 25/25 + local Android matrix 25/25 (exact commands + counts in
  findings; PNG sizes per cell).
- Focused suites if any journey file was touched: the daily_log web-drive journey.
- Static: `flutter analyze`; `dart format --set-exit-if-changed` on touched `.dart`
  only (never `.arb`).
- CI run ≥140: Android job green INCLUDING capture leg; web job green. Record run
  id + head sha + per-leg results. Evidence standard: per-cell PNG bytes on disk,
  `e2e_executed` marker semantics for drive runs — no aggregate claims.

## Boundaries and escalation

- No CI workflow edits; no remote mutations; no secrets/PII; never print `.env`.
- Escalate (do not work around): a product-`lib/` root cause for the stall; any
  disagreement between local and CI after the fix; a capture matrix that cannot
  reach 25/25 on both platforms within 2 diagnostic iterations.
- Findings addenda are appended, never replacing.

## Definition of done

Harness fixed once with the falsified root cause named; both platforms 25/25
locally; CI ≥140 Android job green including the capture leg and web green;
capture matrix archived in docs with per-FC adjudications (Unverified items
named); step-10 hardening landed; PLAN + index rows reconciled (55.1 corrected,
55.2/55.3 verdicts recorded, 55.6/55.7/55.9 superseded-defect notes cleared,
55.10 unchanged); prompts index committed + pushed; close-report addendum carries
the conditional verdict + carried conditions; decision cluster answered and
recorded.

## Owner decision cluster (present in chat as ONE gate, then stop)

1. **Privacy-copy posture (55.10):** approve the ARB notice copy as final /
   provide replacement copy / keep release-blocked. (Implementation cannot claim
   approval; row stays In progress until answered.)
2. **RISK-0025** (public.users self-update role escalation, critical, open):
   authorize a remediation lane now / accept-and-carry into close with trigger /
   defer. Do not silently close it.
3. **STEP-56 zone seed** (`mine-flow-STEP-56-DRAFT-staging-zone-seed.md`, owner
   already chose SEED in principle): run it / defer; until then the daily-log
   create-zone staging round-trip stays Unverified (RISK-0030).
4. **`supabase db push --linked`** for migration `20260913000001` + `database.ts`
   regeneration (production remote mutation): authorize / defer.
5. **STEP-55 row disposition** once 1–4 are answered: conditional close (Done with
   named carried conditions) / stay In progress with the enumerated list.

## Next

Execute only after the owner points this lane (or a delegate) at it. Report the
run-≥140 evidence table + decision-cluster answers; do not flip the STEP row
without them.
