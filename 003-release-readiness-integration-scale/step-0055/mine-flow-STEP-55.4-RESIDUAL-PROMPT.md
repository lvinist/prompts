# mine-flow — STEP-55.4 RESIDUAL: CRS recovery localization, projection test coverage, findings evidence, runtime audit

> **How to run:** Tell your agent "run 55.4 residual fix only". Execute cold in a fresh chat.
>
> **Assigned model: Gemini 3.1 Pro High.** Same tier as 55.4 — CRS/projection validation is the P0
> data-integrity boundary this substep owns.

## Context

Benchmark integrity landed in commit `ee7de94` on `step-0055-cohesive-ui-rebuild`. The P0 core is
real and correct: `_computeLatLon` in `benchmark_bloc.dart:356-383` rejects NaN/infinite and
out-of-range results and returns null, and `_onSubmitBenchmark` (`:586-636`) emits a
`BenchmarkError` instead of saving when `computedLatitude`/`computedLongitude` are null — there is
no `0.0, 0.0` fallback on the submit path. The routes exist (`benchmark-form`,
`benchmark-detail`, `benchmark-edit` in `router.dart:526-587`), the inspector is read-only
(`AppResponsiveSheetMode.readOnlyInspector`, Edit only via `_openEdit`), and the list opens
`ReportType.benchmark` contextually (`benchmark_list_screen.dart:87`).

The audit (2026-09-21, this file) left four residuals. Fix only those.

## Residual scope (exact — nothing else)

1. **`FC-54.4-008` CRS recovery copy is not localized.** The recovery message
   `'Proyeksi gagal: Koordinat berada di luar batas (out-of-bounds) atau salah zona (zone
   mismatch). Pastikan CRS/Datum sesuai dengan Easting/Northing.'` is a hardcoded Indonesian string
   duplicated in **two** places — `benchmark_bloc.dart:604` and `benchmark_form_screen.dart:521`.
   The STEP-55 PLAN ground rule "New user-facing strings go through localization" and spec §4.3
   item 4 both demand localization. Note the string does satisfy the *content* requirement (it
   names datum and out-of-bounds/zone-mismatch recovery), so this is a localization debt, not a
   copy gap. Add an ARB key (`crsProjectionFailure` / similar) to `app_id.arb` + `app_en.arb`,
   consume it in both sites, and remove both literals. The three benchmark presentation files are
   on the `_legacyExemptFiles` list in `tool/check_l10n_baseline.dart` — **migrate them off that
   list as part of this fix** (remove the three `lib/features/benchmark/presentation/...` entries,
   lines ~52-54) so the guard actually enforces the new strings. Re-run the guard.
2. **`FC-54.4-001` test coverage gap: malformed / non-finite / out-of-zone input.** The only
   projection-rejection test is `benchmark_bloc_test.dart` "returns Error when submitting with
   invalid projection coordinates" — and it *seeds* `computedLatitude: null` directly rather than
   driving `_computeLatLon` to null from bad input. Spec §4.3 item 1 requires tests that "cover
   out-of-zone and malformed values". Add `crs_utils_test.dart` + bloc cases that actually feed
   malformed/non-finite/out-of-zone Northing/Easting/CRS combinations and assert the computed
   result is null and the submit is refused (no persistence). Cover: an unknown CRS identifier
   (already throws `ArgumentError` in `CrsUtils` — assert the bloc's `catch (_) => null` path),
   extreme out-of-zone easting/northing for a valid zone, and a hemisphere/zone mismatch.
3. **Cold-route tests for benchmark are missing.** `test/app/router_test.dart` has cold
   create/edit tests for cut-fill and equipment-check but **none** for benchmark
   (`AppRoutes.benchmarkForm` / `benchmarkDetail(id)` / `benchmarkEdit(id)` — no `benchmark` route
   test exists in that file beyond the scaffold's `path: 'benchmark-db'` stub). Spec §4.3 item 2
   requires "cold edit route fetches by ID". Add the parity tests: create route parses no params,
   detail and edit routes resolve `:id` from the path **without** `extra`, and the
   `existingBenchmark`-from-`extra` fast path stays distinct from the fetch-by-ID path
   (`benchmark_form_screen.dart:39-42` and `benchmark_inspector_screen.dart:33-37` both branch on
   extra-vs-id — assert both).
4. **`FC-54.4-009` runtime audit stays Unverified at this lane** (same 55.11 deferral as 55.2/55.3).
   Add mechanical coverage only (empty/error states, the invalid-projection panel render path, IME
   on the form, 48dp targets on the delete/action controls, direct URLs, light/dark where the
   harness allows). Do not claim runtime verification you did not run.
5. **Findings hygiene.** `mine-flow-STEP-55.4-FINDINGS.md` is three bullets with no test counts, no
   commands, no file list, and a claim "Tests passed completely" — it does not meet the PLAN's
   per-substep evidence contract (items 1-7). Supersede it with a dated "Residual fix (55.4)"
   section carrying the exact commands and counts from items 1-3 above. Do not delete the original
   section.

## Read first

- `Upcoming Prompts/mine-flow-STEP-55-PLAN.md` (evidence contract + ground rules)
- Master spec §4.3 (all 7 items), §2.5 (D4), §2.6 (D5 route table), §3.1 (D6)
- `Upcoming Prompts/mine-flow-STEP-55.4-PROMPT.md`, `mine-flow-STEP-55.4-FINDINGS.md`
- `lib/features/benchmark/presentation/bloc/benchmark_bloc.dart` (`_computeLatLon` 356-383,
  `_onSubmitBenchmark` 586-636, `_onCreateBenchmark` 431-448)
- `lib/features/benchmark/presentation/pages/benchmark_form_screen.dart` (~490-530 error panel),
  `benchmark_inspector_screen.dart`, `benchmark_list_screen.dart`
- `lib/core/utils/crs_utils.dart`, `lib/app/router.dart` (benchmark routes 526-587)
- `tool/check_l10n_baseline.dart` (exempt list 49-54 + the scan logic), `lib/l10n/app_id.arb`,
  `lib/l10n/app_en.arb`
- `test/features/benchmark/**`, `test/app/router_test.dart` (extend), `test/features/benchmark/core/utils/crs_utils_test.dart`

## Pre-flight (do not skip)

1. `git status --short --branch` + `git log --oneline -5` in `Code/mine-flow-app`. The shared branch
   `step-0055-cohesive-ui-rebuild` moved during the audit window (now at `fa9ab71`, which landed
   the 55.2/55.3 residual lane). Pull before branching; preserve any untracked scratch
   (`.step55.11*` scripts, `run_web_wrapper.dart`, `m2_challenger_stress_test.dart`) and never
   stash/reset/absorb another lane's dirt.
2. Check `prompts/STEP-index.md` row 55.4 status before you start; the audit did not flip it.
   Follow the collaboration runbook's flip rule if you begin work.

## Likely files (ownership boundary)

- ALLOWED: `benchmark_bloc.dart` (localization only — do not touch the validation logic),
  `benchmark_form_screen.dart`, `benchmark_inspector_screen.dart`, `benchmark_list_screen.dart`
  (only if a string moves), `lib/l10n/app_id.arb` + `app_en.arb` + generated localization files,
  `tool/check_l10n_baseline.dart` (exempt-list removal only), `test/features/benchmark/**`,
  `test/app/router_test.dart`, `Upcoming Prompts/mine-flow-STEP-55.4-FINDINGS.md` (append).
- FORBIDDEN: any CRS/projection *algorithm* change (that is a schema/policy escalation — see
  Boundaries), other features, `router.dart` route shapes (test only), `supabase/**`.

## Tests and verification

- `flutter test test/features/benchmark/ test/app/router_test.dart`
- `dart format --output=none --set-exit-if-changed <touched files>`
- `flutter analyze`
- `dart run tool/check_l10n_baseline.dart` — must now scan the three benchmark files as
  non-exempt and report `[OK]`.
- `dart run tool/check_supabase_contracts.dart` (expect pass; no schema change here).
- Record exact commands + counts. ONE commit `fix(55.4): ...`, benchmark-owned hunks only.

## Boundaries and escalation

- No CRS/datum policy change, no silent clamping, no fake coordinate history, no schema migration,
  no persistence before validation. The validation logic is already correct — do not restructure
  it to add tests; add tests that exercise it.
- Escalate any precision/round-trip disagreement in `crs_utils` (the existing round-trip test is
  the reference), or if removing the legacy l10n exemptions surfaces pre-existing violations in the
  benchmark files that a pure localization fix cannot cover (report them; do not mass-migrate
  unrelated strings in this lane).
- Never print secrets.

## Definition of done

- The CRS recovery string is a single localized key consumed in both sites; the three benchmark
  presentation files are off the legacy-exempt list and the guard is green with them scanned.
- Malformed/out-of-zone/non-finite projection inputs are proven rejected by tests that drive
  `_computeLatLon`, not by seeding null state.
- Benchmark cold create/detail/edit routes have router-test parity with cut-fill and
  equipment-check, covering both the extra fast path and the fetch-by-ID path.
- Runtime audit honestly deferred with mechanical coverage added.
- FINDINGS has a dated "Residual fix (55.4)" section with commands and counts; gates green.

## Next

Report the exact replacement evidence-cell line for index row 55.4 — including whether the row is
now flippable to Done (do **not** flip it yourself). Then run the 55.5 residual lane in a fresh
chat; the four lanes (55.4-55.7) are independent at the file level but all touch `lib/l10n/` and
`tool/check_l10n_baseline.dart` — serialize, don't interleave.


---

## E2E residual routed from 55.11 (2026-09-23) — benchmark edit-route push

**Source:** CI run `35894532969` at app head `fe17e2d`, `web-e2e-driver-log`.
**Failure:** `benchmark_journey_test.dart:189` — `expect(find.byType(BenchmarkFormScreen), findsOneWidget)` fails with `Found 0 widgets with type "BenchmarkFormScreen"` on Web **and** Android.

**Not a stale finder** (do not swap the finder — it is correct). The journey:
1. taps the list card → reaches `BenchmarkInspectorScreen` ✅ (asserted at `:182`, passes)
2. taps `Key('benchmark_edit_button')` ✅ (`:183-186`, passes)
3. expects `BenchmarkFormScreen` at `:189` ❌ — the edit route does not land on the form.

**Root cause to investigate:** the inspector's `_openEdit` does `context.pushNamed('benchmark-edit', pathParameters:{'id':…}, extra:…)` (`benchmark_inspector_screen.dart:74-80`). The `benchmark-edit` route (`router.dart:566-588`, path `:id/form`) is a `CustomTransitionPage` with `opaque:false` — under the test the pushed form may not be materialising, or the inspector route (also `opaque:false`, fade transition) is still on top. Verify the pushed form route actually builds `BenchmarkFormScreen` in the test env; check whether the non-opaque transition + `pumpAndSettle` timing leaves the form unmounted, and whether the inspector's `.then()` reload races the push.

**Scope:** benchmark edit-navigation only. Fix in `lib/features/benchmark/**` or the `benchmark-edit` route. Re-run `flutter test integration_test/journeys/benchmark_journey_test.dart` (credential-gated; verified in CI). Do not touch other journeys.
