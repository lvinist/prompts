# mine-flow — STEP-48.27: Post-gate schema, reporting & synchronization contract remediation

> **How to run:** tell your agent *"run substep 48.27"*. Self-contained — runnable cold in a fresh chat.
>
> This is a post-gate remediation substep inside STEP-48. It does not close STEP-48, change
> `prompts/STEP-index.md`, archive the STEP, or authorize Phase 4.

## Context

STEP-48.26 run `33953949570` on `c73a00e` was **NO-GO**: Android was green, but the branch-head
web gate had one red daily-log assertion. The daily-log race is already assigned to 48.23 and has
an in-flight fix; do not duplicate or absorb that work here.

A read-only implementation audit of `c73a00e` found a separate class of defects that the earlier
48.18–48.20 claims did not fully cover:

- timeline aggregation reads obsolete value keys and silently returns zeroes;
- reporting reads obsolete database value/status keys;
- timeline milestone creation can send null into `NOT NULL` timestamp columns;
- benchmark sync re-enters the local-first repository, can leave replacement queue items pending,
  and does not participate in the explicit `updated_at`/LWW contract;
- equipment refresh unconditionally overwrites newer local state;
- delete paths bypass remote timestamp comparison;
- timestamp normalization is incomplete in equipment and Data Bucket paths.

The authoritative current behavior is the checked-in schema and architecture contract, not stale
presentation-map names or earlier findings prose.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — D1, D2, D7, the remediation-wave table,
  the honesty rule, and the 48.26 NO-GO handoff.
- `Upcoming Prompts/mine-flow-STEP-48.26-FINDINGS.md` — current branch-head evidence and residual
  register. Read the current top record, not only the retained historical sections.
- `Upcoming Prompts/mine-flow-STEP-48.18-FINDINGS.md`, `48.19-FINDINGS.md`, and
  `48.20-FINDINGS.md` — earlier claims this substep must verify rather than assume.
- `Code/mine-flow-app/README.md` — app setup and test commands.
- `Code/mine-flow-docs/architecture/04-data-model.md` — current entity/column/timestamp contract.
- `Code/mine-flow-docs/architecture/12-test-strategy.md` — required test tiers and CI bar.
- `Code/mine-flow-docs/architecture/15-native-app-architecture.md` §2 — offline/LWW behavior.
- `Code/mine-flow-app/supabase/migrations/20260718000001_core_schema.sql` — actual core columns,
  defaults, constraints, and trigger use.
- `Code/mine-flow-app/supabase/migrations/20260831000001_step_48_17_timeline_milestones.sql`
  and `20260831000002_step_48_17_benchmarks.sql` — new entity schemas.
- `Code/mine-flow-app/supabase/migrations/20260901000001_step_48_20_updated_at_respects_client.sql`
  and `20260902000001_step_48_21_notes_columns.sql`.
- `Code/mine-flow-app/supabase/types/database.ts` — generated contract; do not hand-edit.
- `Code/mine-flow-app/supabase/seed.sql` and `lib/core/constants/app_constants.dart` — fixture
  and `defaultSiteId` contract.
- `Code/mine-flow-app/lib/features/timeline/data/repositories/timeline_repository_impl.dart`.
- `Code/mine-flow-app/lib/features/reporting/data/datasources/reporting_remote_datasource.dart`.
- `Code/mine-flow-app/lib/core/services/pdf_service.dart`.
- `Code/mine-flow-app/lib/features/timeline/data/models/timeline_milestone_model.dart` and
  `data/datasources/timeline_remote_datasource.dart`.
- `Code/mine-flow-app/lib/features/benchmark/data/{models,repositories,datasources,sync}`.
- `Code/mine-flow-app/lib/features/equipment_check/data/{models,repositories,datasources,sync}`.
- `Code/mine-flow-app/lib/features/data_bucket/data/{models,repositories,datasources,sync}`.
- `Code/mine-flow-app/lib/features/attendance/data/{repositories,datasources,sync}`,
  `daily_log/data/{repositories,datasources,sync}`, and
  `tracking/data/{repositories,datasources,sync}` for sibling comparison.
- Relevant existing tests under `test/unit`, `test/features`, and `test/integration`.

## Pre-flight and concurrency boundary

Inspect all three repositories before editing. At planning time the workspace may contain concurrent
48.23 work:

- `Code/mine-flow-app`: daily-log repository/BLoC/tests for the web race.
- `Code/mine-flow-docs`: `architecture/04-data-model.md` timestamp/status contract amendment.
- `prompts`: STEP-50's in-flight `STEP-index.md` edit.

Do not reset, stash, stage, commit, reformat, or absorb those changes. If the daily-log or Doc 04
work is still dirty, preserve it and either wait for its owner/48.25 handoff or work only in files
that do not overlap. Report the exact pre-existing files in findings.

Do not read or print `.env` values, tokens, passwords, or credential contents. Do not mutate staging
or remote state in this substep unless the user explicitly supplies the required scoped operation;
prefer local tests and static contract checks. Never fabricate remote migration or runtime evidence.

## Scope

### In scope

1. **Timeline/reporting contract repair**
   - Make timeline aggregation consume the actual database-shaped keys (`bcm_volume`,
     `lcm_volume`, `actual_area`) after the datasource query returns them.
   - Make reporting consume actual schema keys while preserving presentation-map compatibility only
     at an explicit boundary.
   - Correct equipment status mapping to `is_operational`.
   - Remove obsolete source-column fallbacks where they imply live database support.
   - Update the PDF/report fixtures and regression tests so they use the real contract.

2. **Timeline milestone write contract**
   - Omit null `created_at`/`updated_at` fields so PostgreSQL defaults can apply, or explicitly
     provide valid UTC timestamps when the client owns them.
   - Add a model/datasource regression test for a newly created milestone payload.

3. **Benchmark sync and LWW**
   - Ensure a drained benchmark mutation goes directly to the remote datasource or an equivalent
     non-re-enqueuing path.
   - Ensure benchmark payloads participate in the client-supplied `updated_at` contract and remote-newer
     comparison.
   - Add tests proving a drain does not create a second pending mutation and that remote-newer rows
     win.

4. **Sibling synchronization sweep**
   - Add the missing refresh LWW/tombstone protection for equipment if the audit finding is confirmed.
   - Sweep equipment and Data Bucket timestamp writers for UTC serialization.
   - Sweep delete paths for the same LWW class. If a delete needs a broader shared abstraction or
     product decision, stop and record the exact decision needed rather than applying an inconsistent
     partial fix.
   - Do not weaken conflict assertions or silently accept stale-write behavior.

5. **Architecture truth**
   - If the implementation changes the documented data/timestamp contract, update
     `Code/mine-flow-docs/architecture/04-data-model.md` with a Version Log bump, only after the
     concurrent 48.23 Doc 04 edit is reconciled. Preserve historical STEP findings.
   - Do not edit generated `supabase/types/database.ts` manually; run and verify the contract guard.

### Out of scope

- The daily-log autosave/submit fix already owned by 48.23.
- The CI screenshot path/matrix remediation, integration timeout hardening, and browser reload
  evidence; these remain separate follow-up work and must be named as still open.
- New product entities, new migrations, staging seed mutation, broad refactors, or dependency changes.
- Changing `prompts/STEP-index.md` or closing/archive bookkeeping.

## Your task

1. Re-derive each audit finding against current source and classify it as confirmed defect,
   already fixed, stale finding, or unverified. Quote the relevant schema and source path/line.
2. Build a compact defect register before editing. Group by shared mechanism: stale schema-key
   reads, null/default write payloads, benchmark queue recursion/LWW, refresh clobber, and delete/
   timestamp contract.
3. Implement the smallest root-cause fixes in dependency order. Do not fix only the originally
   named line; sweep the defect class and justify every remaining legacy/presentation key.
4. Add lower-tier regression tests that fail on the unfixed tree and pass on the fixed tree:
   - database-shaped timeline/reporting mapping fixtures;
   - milestone create payload null/default behavior;
   - benchmark direct-drain/no-re-enqueue and remote-newer LWW;
   - equipment refresh stale-snapshot protection;
   - UTC timestamp serialization and delete/update timestamp behavior where changed.
5. Record any item that cannot be safely fixed without an architecture/product decision as
   `Deferred`/Unverified with a named owner and revisit trigger. Do not turn it into a green test.
6. Produce `Upcoming Prompts/mine-flow-STEP-48.27-FINDINGS.md` with:
   - confirmed/rejected/unverified counts;
   - exact file:line evidence;
   - each fix and its regression test;
   - sibling sweep results;
   - commands and real outputs;
   - remaining screenshot/CI/deep-link gaps;
   - clean handoff to 48.24 → 48.25 → 48.26.

## Verification

Run the relevant focused tests after each fix, then all applicable gates:

```bash
cd Code/mine-flow-app
flutter test test/unit/timeline_repository_impl_test.dart \
  test/features/reporting/presentation/pages/report_config_page_test.dart \
  test/features/benchmark/data/sync/benchmark_sync_registrar_test.dart \
  test/features/benchmark/data/repositories/benchmark_repository_impl_test.dart \
  test/unit/equipment_check_repository_test.dart \
  test/features/tracking/data/repositories/tracking_repository_impl_test.dart
flutter test test/integration/sync_queue_manager_test.dart \
  test/integration/attendance_daily_log_sync_test.dart \
  test/integration/equipment_check_sync_test.dart
flutter analyze
 dart format --output=none --set-exit-if-changed lib/ test/
dart run tool/check_supabase_contracts.dart
```

Remove the leading space before `dart format` if running the block in a shell that treats it
specially. Use the repository's actual test paths if a named test does not exist; record that
fact rather than inventing a replacement.

Required evidence:

- No obsolete database-source keys remain in production reads unless explicitly documented as an
  internal presentation-map boundary.
- All changed serializers emit the real schema keys and valid UTC timestamps.
- Benchmark drain has no local-first re-entry or pending-mutation loop.
- Stale refresh snapshots cannot overwrite newer local rows for the covered entities.
- Contract guard, analyzer, formatter, focused tests, and full `flutter test` pass.
- No `.env` or secret value was read or printed.

## Keeping the docs true

This substep changes implementation-level data/sync behavior. If the current architecture contract
already describes the behavior, update code/tests only. If the timestamp or delete semantics change,
update Doc 04 and bump its Version Log after reconciling the concurrent 48.23 edit. Do not rewrite
historical STEP findings or mark the design-review evidence complete.

## Definition of done

- [ ] Every audit finding in this prompt is classified with current source evidence.
- [ ] Timeline/reporting/database-shaped key drift is fixed or explicitly deferred with an owner.
- [ ] Timeline milestone create payload respects PostgreSQL defaults/NOT NULL constraints.
- [ ] Benchmark draining is direct/non-re-enqueuing and participates in LWW, with regression tests.
- [ ] Equipment refresh and timestamp/delete sibling sweep is complete or has named deferrals.
- [ ] All changed code has lower-tier regression coverage.
- [ ] `flutter analyze` passes with 0 issues.
- [ ] `dart format --set-exit-if-changed lib/ test/` passes.
- [ ] `dart run tool/check_supabase_contracts.dart` passes.
- [ ] Focused tests and the full `flutter test` suite pass, with any known flake isolated and recorded.
- [ ] No secrets were read, printed, or committed.
- [ ] Findings file written; current dirty files preserved and listed.
- [ ] Remaining screenshot/CI/deep-link gaps are explicitly handed forward.

## Next

After this substep, run **substep 48.24** in a fresh chat for the local full-gate re-run. Then run
48.25 to commit/push and 48.26 for the authoritative branch-head CI verdict. STEP-48 remains
`In progress` until 48.26 is GO and 48.15 completes the docs-true close.
