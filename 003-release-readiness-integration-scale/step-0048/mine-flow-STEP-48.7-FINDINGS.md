# STEP-48.7 Findings: Benchmark Journey + NR-006

## Journey Verdict
**Deferred**. 
**Blocker**: The `benchmarks` table does not exist in the Staging database.
During the local Android test run, the Supabase Postgrest client returned: `Could not find the table 'public.benchmarks' in the schema cache, code: PGRST205`.
Upon investigation, there is no `benchmarks` table defined in `supabase/migrations/` or `supabase/types/database.ts`. It appears the migration for the Benchmark feature (STEP-36.1) was never authored.
**Trigger**: When the `benchmarks` table migration is created and applied to Staging.

## NR-006 / RISK-0019
**Recommendation**: **Re-justify RISK-0019**.
The `benchmark_journey_test.dart` uses `appRouter.go(AppRoutes.benchmarkForm)` which is an in-process route push. While it proves the router can resolve the path within the app shell, it **does not** prove a cold URL load from a fresh browser session (a true deep-link), due to harness limitations of `flutter drive`.
Since we cannot verify a true cold browser load with this harness, RISK-0019 should be narrowed to state that in-process deep-linking works, but true cold-start web deep-linking remains unverified pending a different testing approach.

## CRS / Coordinate Round-Trip (CF-033 / CF-034)
**Deferred**.
Cannot verify against Staging because the `benchmarks` table does not exist. 

## Defects Fixed
- **Off-screen tap warning**: Fixed a test defect where `tester.tap` on the `CRS` and `Status` dropdowns failed because the widgets were off-screen in `benchmark_journey_test.dart`. Added `tester.ensureVisible` prior to tapping the dropdowns and their items.

### Current resolution (STEP-48.15, 2026-09-08)

The benchmark migration was applied and the benchmark journey executed and passed in branch-head run `34225431645` (web and Android). The substep is **Done** for benchmark staging/runtime coverage. RISK-0019 remains open only for true browser cold-start/reload deep-link evidence, which this in-process harness cannot prove.


- Commit pushed to `step-0048-runtime-evidence`.
- CI will fail or timeout due to `SyncQueueManager` getting stuck retrying the failed sync against the missing `benchmarks` table.
