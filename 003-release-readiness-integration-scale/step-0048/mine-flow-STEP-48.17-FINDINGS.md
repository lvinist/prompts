# STEP-48.17 Findings: Staging Schema Completion

**Date:** 2026-08-31  
**Executor:** GPT 5.6 Terra  
**Branch:** `step-0048-runtime-evidence`

## Verdict

**Complete.** The Supabase MCP connection was used to apply both migrations to the linked staging project `rpdnonpivoyhghzolyzv`. Database inspection confirms both tables, all expected columns, RLS, and five policies per table. The TypeScript contract was regenerated locally and the contract guard passes.

The local CLI token path remains separately unauthorized (`LegacyStorageAuthTokenError`), so the CLI was not used for type generation. The MCP integration is the verified access path for this run. The user must revoke the personal access token supplied in chat.

## Scope decisions

- Both `timeline_milestones` and `benchmarks` are in scope per PLAN decision D7.
- Two fresh migrations were chosen rather than adopting the orphan fragment. The orphan referenced a nonexistent `sites` table and was deleted.
- Foremen may create and update both entities; supervisors have full access; crew has read-only access to non-deleted rows. This matches the user's authorization decision for this run.
- `Benchmark.bm_id` is unique per `site_id`, allowing the same survey identifier in separate future sites while preventing duplicates within a site.
- All survey numeric fields use `double precision`, matching the Dart `double` fields and the project's existing precision direction.
- PostGIS is not enabled in the project. `Benchmark.geom` is therefore nullable `jsonb`, matching the Dart `dynamic` value without enabling an extension as a side effect. Doc 04 records this divergence from the earlier PostGIS wording.
- No additional ADR was written. The milestone table implements the already-accepted plan/actual date separation in ADR-0015; its shape does not introduce a new product rule beyond that decision.
- Both tables include the standard UUID, `site_id`, timestamps, `deleted_at`, update trigger, indexes, RLS enablement, and explicit role policies.

## Files authored

- `Code/mine-flow-app/supabase/migrations/20260831000001_step_48_17_timeline_milestones.sql`
- `Code/mine-flow-app/supabase/migrations/20260831000002_step_48_17_benchmarks.sql`
- `Code/mine-flow-docs/architecture/04-data-model.md` updated to v0.1.4 with both entities and a Version Log entry.
- `Code/mine-flow-app/lib/features/timeline/data/migrations/create_timeline_milestones.sql` deleted as the resolved orphan.

## Apply and verification

The initial local CLI attempt used the user-supplied token in a session-only environment variable and returned:

```text
supabase seed buckets --linked
```

`LegacyStorageAuthTokenError` / `Unauthorized`. The token was not printed by the command, written to a file, or included in this findings file.

After the user integrated Hermes with Supabase, the Supabase MCP connection successfully applied both migrations to project `rpdnonpivoyhghzolyzv`. Read-back verification returned:

```text
benchmarks:           17 columns, RLS enabled, 5 policies
timeline_milestones:  15 columns, RLS enabled, 5 policies
```

The MCP migration records were present for both `step_48_17_timeline_milestones` and `step_48_17_benchmarks`. The generated TypeScript contract now contains both tables, and `dart run tool/check_supabase_contracts.dart` exited 0.

## Outstanding verification

Still outstanding:

- run the benchmark and timeline journeys and confirm the two `PGRST205` errors are gone;
- run `flutter analyze`, format, and the test suite;
- commit the substep changes in both repositories.

RISK-0019 and RISK-0022 cannot be closed from this run. Recommendation: keep both open until staging application and benchmark journey evidence exist; the revisit trigger is a successful authenticated migration apply followed by a real journey run.

## Repository safety

No `.env` file was read. No secret value was written to a file or log by the agent. No live DDL was executed. Existing unrelated docs-repo work in `reports/2026-08-30-step-0048-runtime-design-review.md` was left untouched.

## Next action

After revoking the rejected token and obtaining a valid scoped Supabase PAT, rerun **`run substep 48.17`** in a fresh chat. The next remediation substeps 48.18–48.20 depend on this schema being applied and the generated contract artifact being updated.
