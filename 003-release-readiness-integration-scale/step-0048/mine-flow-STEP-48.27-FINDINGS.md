# STEP-48.27 Findings — Post-gate schema, reporting & synchronization contract remediation

**Date:** 2026-09-05 (re-run 1: 2026-09-08)
**Status:** Execution complete — application fixes and focused verification complete; full suite handed to 48.24. **Re-run 1 complete (2026-09-08):** the TZ-dependent test-fixture defect assigned by 48.26 re-run 5 §0.7 is fixed and verified under both TZs — see "Re-run 1 record" below; the original 2026-09-05 record follows it unchanged.
**Owner:** Hermes / Claude Opus 4.8
**Branch:** `step-0048-runtime-evidence`
**Parent:** STEP-48, substep 48.27
**Source audit:** read-only audit of `mine-flow-app` `c73a00e`; the execution record below describes the resulting uncommitted fixes.

## Re-run 1 record (2026-09-08)

**Assignment source:** 48.26 re-run 5, §0.7 item 1 (findings `mine-flow-STEP-48.26-FINDINGS.md` §0, run `34192851645` on `f14885e`, NO-GO structural). Register rows **R-1** (geospatial `:110`/`:134`) and **R-2** (timeline `:114`): three TZ-dependent test-fixture assertions from this substep's own committed lane `3df8e7f` — fixtures built local `DateTime`s while expectations hardcoded UTC+7-derived strings, so they passed every local gate on this UTC+7 host and failed on CI's UTC runner (first-probe exposure: the strings do not exist at `c73a00e`).

**Pre-flight state (re-verified on disk, not from memory):** `mine-flow-app` at `f14885e`, clean except untracked `run_web_wrapper.dart` (48.24's named loop residue — preserved, never committed); `0	0` ahead/behind `origin`. Concurrent lanes intact and untouched: `mine-flow-docs` carries 48.23 re-run 5's uncommitted `architecture/04-data-model.md` note on `step-0048-runtime-evidence`; `prompts` carries STEP-50's `STEP-index.md` edit on `step-0050-phase3-check-in`. The original prompt's first-pass scope (R-1–R-10 contract remediation) landed in `3df8e7f` and was **not** reopened; this re-run's scope is exactly the gate's assignment.

### Fix (2 fixture sites, 3 assertions, no assertion weakened)

| Site | Before | After |
|---|---|---|
| `test/features/data_bucket/data/models/geospatial_file_model_test.dart:46` | `acquisitionDate: DateTime(2026, 7, 15)` (local) | `DateTime.utc(2026, 7, 15)` |
| same file `:114` | `json['acquisition_date'] == '2026-07-14T17:00:00.000Z'` | `'2026-07-15T00:00:00.000Z'` |
| same file `:139` | `hiveJson['acquisitionDate'] == '2026-07-14T17:00:00.000Z'` | `'2026-07-15T00:00:00.000Z'` |
| `test/unit/timeline_repository_impl_test.dart:108` | `startDate: DateTime(2026, 8, 31, 7)` (local) | `DateTime.utc(2026, 8, 31, 7)` |
| same file `:118` | `json['start_date'] == '2026-08-31T00:00:00.000Z'` | `'2026-08-31T07:00:00.000Z'` |

Per the gate's fix shape: input and expectation now share one explicit `DateTime.utc` anchor instead of a local-clock accident; each expectation still asserts the full serialized string (strengthened, not weakened — the literal changed from a UTC+7-derived value to the anchor's true UTC instant). Application code untouched: 48.26 re-run 5 §0.4.2 already proved app serialization correct (the same commit's positive UTC tests pass on CI); the defect was confined to these test-fixture sites.

### Verification — the gate's discriminator, both legs quoted

| Gate | Result | Log |
|---|---|---|
| Focused pair, default TZ | `All tests passed!` (11/11), exit 0 | `step4827_r1_focused_defaultTZ.log` |
| Focused pair, `TZ=UTC` | `All tests passed!` (11/11), exit 0 | `step4827_r1_focused_tzUTC.log` |
| **Full suite, default TZ** | **`01:34 +542: All tests passed!`, exit 0** | `step4827_r1_fullsuite_defaultTZ.log` |
| **Full suite, `TZ=UTC`** | **`01:08 +542: All tests passed!`, exit 0** | `step4827_r1_fullsuite_tzUTC.log` |
| `flutter analyze` | `No issues found! (ran in 5.4s)` | — |
| `dart format --output=none --set-exit-if-changed lib/ test/` | `Formatted 314 files (0 changed)`, exit 0 | — |
| `dart run tool/check_supabase_contracts.dart` | `[OK] Contract verification passed.`, exit 0 | `step4827_r1_contracts.log` |

The `TZ=UTC` full suite at **542/542** is the discriminator the gate demanded — at `f14885e` the identical command fails exactly the 3 assigned assertions (`539 +3`), so this run proves the class is closed and no hidden tail exists behind it. Both runs executed in the foreground shell (per the wave's environment-poisoning rule; the logs carry the suite's own exit codes, not a pipe's). An earlier background-shell pair produced identical 542/542/exit-0 results on both legs; the foreground re-runs superseded them as the quoted evidence.

### Scope discipline

No commit, no push — **48.25's lane** per 48.26 §0.7 item 2. No application code, `ci.yml`, migration, staging row, doc, or `prompts/STEP-index.md` row touched. The two modified test files are the only tracked changes (`git status --short`: ` M` on exactly those two + the known untracked `run_web_wrapper.dart`); both are LF (0 CR bytes, `tr -dc '\r' | wc -c`). Evidence logs at the workspace root: the five `step4827_r1_*` files named above.

**Next:** 48.25 (commit + push this fix; optional owner decision on 48.29's web-guard exit-capture one-liner riding the same push) → 48.26 (re-run 6 branch-head gate; predictions stand: `test` 542/3/0, Android 24/0/2, web 16/16 of 21 executed, build-android success).

---

## Purpose

This substep was added after the STEP-48.26 branch-head audit found production paths that still
contradict the checked-in Supabase schema and the Doc 04 / Doc 15 client timestamp contract. It is
separate from the daily-log autosave/submit race, which is owned by 48.23 re-run 5.

The substep must fix or explicitly defer the following classes:

1. stale database-key reads in timeline aggregation and reporting;
2. null/default timestamp payloads for timeline milestone creation;
3. benchmark queue re-entry and missing LWW timestamp participation;
4. equipment refresh snapshot clobber;
5. non-UTC timestamp writers and delete paths that bypass the LWW contract.

## Initial audit register

| ID | Finding | Evidence | Initial class | Owner / disposition |
|---|---|---|---|---|
| R-1 | Timeline aggregation reads `cut_volume_m3`, `fill_volume_m3`, and `area_cleared_ha` while the schema uses `bcm_volume`, `lcm_volume`, and `actual_area`; null fallback silently produces zeroes | `lib/features/timeline/data/repositories/timeline_repository_impl.dart:72-104`; `supabase/types/database.ts:156-227,475-543` | Confirmed production defect | 48.27 |
| R-2 | Timeline repository regression fixture uses the obsolete presentation keys and cannot detect R-1 | `test/unit/timeline_repository_impl_test.dart:55-78` | Confirmed test-contract defect | 48.27 |
| R-3 | Reporting reads obsolete cut/fill keys and equipment `status` | `lib/features/reporting/data/datasources/reporting_remote_datasource.dart:74-84,206-215` | Confirmed production defect | 48.27 |
| R-4 | Timeline milestone create payload can include null `created_at` / `updated_at` despite `NOT NULL` columns with defaults | `lib/features/timeline/data/models/timeline_milestone_model.dart:118-135`; migration `20260831000001...sql:16-19` | Confirmed production defect | 48.27 |
| R-5 | Benchmark drain calls a local-first repository, which enqueues another mutation during queue processing | `lib/features/benchmark/data/sync/benchmark_sync_registrar.dart:51-57`; `benchmark_repository_impl.dart:48-63` | Confirmed synchronization defect | 48.27 |
| R-6 | Benchmark payload/model lacks explicit `updated_at` and registrar-side remote-newer comparison | `benchmark_model.dart:68-90`; `benchmark_repository_impl.dart:48-63` | Confirmed LWW contract defect | 48.27 |
| R-7 | Equipment refresh unconditionally writes fetched rows over local cache | `lib/features/equipment_check/data/repositories/equipment_check_repository_impl.dart:134-140` | Confirmed synchronization defect | 48.27 |
| R-8 | Equipment/Data Bucket timestamp serialization and several delete paths do not consistently carry UTC/client `updated_at` | equipment DTO `:89-105`; Data Bucket model/repository `:70-88`, `:94-113`; tracking deletes `tracking_remote_datasource.dart:53-58,86-91,119-124` | Confirmed contract drift; sweep required | 48.27 |
| R-9 | Delete paths and the core default handler do not compare remote timestamps before applying deletes; fetch errors may fall through to upsert | `lib/core/offline/sync_queue_manager.dart:229-268`; feature registrars' delete branches | Confirmed / architecture-sensitive | 48.27; Q14 if abstraction change is required |
| R-10 | Design-review screenshot path, complete Android capture matrix, integration timeouts, and browser reload remain open | `test_driver/integration_test.dart:11-16`; `.github/workflows/ci.yml:212-218,285-291`; `design_review_capture_test.dart:188-213`; deep-link journey `:21-26` | Confirmed but out of scope here | Separate follow-up; do not mark STEP-48 complete |

Counts before execution: **9 confirmed/current rows, 1 out-of-scope evidence row**. Reclassify each
against the source at execution time; do not preserve a finding that is stale.

## Locked boundaries

- The daily-log fix currently in `Code/mine-flow-app/lib/features/daily_log/...` is concurrent
  48.23 work. Do not modify or stage those files.
- The Doc 04 edit currently in `Code/mine-flow-docs/architecture/04-data-model.md` is concurrent
  48.23 work. Re-read it before deciding whether another documentation amendment is needed.
- `prompts/STEP-index.md` has a pre-existing STEP-50 edit. Do not modify it in this substep.
- No secrets, `.env` values, access tokens, or credential contents may be read or printed.
- No staging mutation is part of this prompt. Static/mocked/local evidence is not remote evidence.
- Do not hand-edit generated `supabase/types/database.ts`.
- Do not weaken an assertion to make a test pass.

## Files expected to change, subject to pre-flight confirmation

Application repository:

- timeline repository/model/datasource tests;
- reporting datasource and report/PDF tests;
- timeline milestone model/datasource tests;
- benchmark model/repository/remote datasource/sync registrar and tests;
- equipment repository/DTO and tests;
- Data Bucket timestamp model/repository tests;
- shared queue/delete behavior tests only if the root-cause fix is safe and within Q14.

Docs repository:

- `architecture/04-data-model.md` only if the current concurrent Doc 04 amendment does not already
  cover the exact status/delete contract and a Version Log bump is required.

No files are changed by this planning record alone.

## Required verification

At execution time, run focused tests for every changed subsystem, then:

```bash
cd Code/mine-flow-app
flutter analyze
dart format --output=none --set-exit-if-changed lib/ test/
dart run tool/check_supabase_contracts.dart
flutter test
```

Required assertions include:

- database-shaped timeline/reporting fixtures use actual schema keys;
- report presentation maps are explicit and do not masquerade as database columns;
- new milestone payloads omit nullable client timestamps or supply valid UTC values;
- benchmark queue drain does not enqueue a replacement mutation;
- benchmark remote-newer rows win and benchmark writes carry explicit timestamps;
- equipment refresh preserves a newer local row and tombstone;
- changed timestamp serializers emit UTC values;
- delete behavior is either LWW-safe or explicitly deferred with Q14's owner/revisit trigger.

## Definition of done

- [x] R-1 through R-9 re-derived and classified against current source.
- [x] Confirmed timeline/reporting key drift fixed and database-shaped tests pass.
- [x] Timeline milestone create payload respects PostgreSQL defaults/constraints.
- [x] Benchmark drain is direct/non-re-enqueuing and participates in LWW.
- [x] Equipment refresh and timestamp sibling sweep complete or explicitly deferred.
- [x] Delete/LWW behavior is fixed or Q14 is recorded as a named follow-up; no silent bypass remains.
- [x] Focused tests, analyzer, formatter, and contract guard pass; full-suite timing flakes are isolated and handed to 48.24.
- [x] Concurrent 48.23 and STEP-50 work preserved and listed.
- [x] Remaining screenshot/CI/deep-link gaps are explicitly handed forward.
- [x] This findings file is updated with actual commands/results before the substep is marked Done.

## Execution findings

**Re-derived classification:** R-1/R-2/R-3/R-4/R-5/R-6/R-7/R-8 confirmed and fixed in the app. R-9 is deferred as architecture-sensitive: the shared queue hard-delete path and Data Bucket/Tracking delete contracts need a shared tombstone/delete LWW decision; equipment delete remote-newer comparison remains deferred because its queue payload carries only `id`. R-10 remains out of scope and open.

**Pre-existing concurrent files preserved:** `lib/features/daily_log/data/repositories/daily_log_repository_impl.dart`, `lib/features/daily_log/presentation/bloc/daily_log_bloc.dart`, `test/unit/daily_log_repository_test.dart`, and untracked `test/features/daily_log/presentation/daily_log_bloc_test.dart`. No generated types, migrations, docs, prompts, or secrets were changed.

**Fixes and regression coverage:** timeline now reads `bcm_volume`, `lcm_volume`, and `actual_area`; its fixture uses those schema keys. Reporting reads the schema keys and derives the presentation `status` from `is_operational` while retaining report-facing map keys at the explicit boundary. Milestone serializers omit null server-managed timestamps and UTC-normalize supplied timestamps. Benchmark models/entities carry `updatedAt` through Supabase/Hive/domain serialization; repository mutations stamp UTC; the registrar receives the remote datasource, compares remote-newer rows, and writes directly without repository re-enqueue. Equipment serializers stamp UTC and refresh filters older remote rows/local tombstones. Data Bucket serializers and mutation stamps are UTC-normalized.

**Verification evidence:**

- Initial RED: the schema-key timeline fixture failed with `actual 0.0` vs `expected 100.0`; the benchmark timestamp test initially failed to compile because `updatedAt` was absent. These were corrected before the final focused run.
- Focused command (timeline, milestone payload, benchmark model/registrar/LWW, equipment model/repository, Data Bucket serialization, PDF service): **56 tests passed — `All tests passed!`**. PDF tests emit pre-existing `dart_pdf` Helvetica Unicode warnings for the em dash; no test failed.
- `flutter analyze`: **No issues found!**
- `dart format --output=none --set-exit-if-changed lib/ test/`: passes after formatting (315 files, 0 changed on the final check).
- `dart run tool/check_supabase_contracts.dart`: **`[OK] Contract verification passed.`**
- Full `flutter test`: two complete runs reached **512 passed / 1 failed**; each failed in a different previously documented order-dependent sync timing test (`sync_queue_manager_test.dart` retry-count assertion, then `attendance_daily_log_sync_test.dart` timestamp-conflict assertion). Both failing files passed immediately in isolation (**8/8** and **3/3** respectively), and neither file nor its production path was changed by 48.27. The full-suite rerun remains 48.24's gate, so this substep records the flake evidence rather than claiming a clean full-suite pass.
- Line-ending audit: all 48.27-owned touched files were normalized to LF (0 CR bytes); `git diff --check` passes when the preserved concurrent 48.23 daily-log files are excluded. The sole remaining `git diff --check` finding is the pre-existing CRLF worktree state of `daily_log_repository_impl.dart`, which this substep did not modify or normalize.

## Remaining deferrals and handoff

Q14: owner is the shared offline-sync architecture owner; revisit when the delete/tombstone contract is explicitly chosen. Do not change `SyncQueueManager._defaultSupabaseSync` hard delete, invent generic tombstone payloads, or repair Data Bucket drain recursion until `GeospatialFile` has a deletion field and its contract is approved. Tracking delete timestamp comparison is likewise deferred. The fail-open shared-manager LWW fetch remains unchanged. Screenshot path/matrix, integration timeout, browser reload, and deep-link evidence remain separate follow-up gaps. Next: 48.24 local full-gate rerun, then 48.25 commit/push, then 48.26 branch-head verdict.

## Next

After 48.27 completes, run **48.24** in a fresh chat for the local full-gate re-run, then 48.25
for commit/push and 48.26 for the authoritative branch-head CI verdict. STEP-48 remains `In progress`.
