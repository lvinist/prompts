# mine-flow — STEP-48.17: Staging Schema Completion — `timeline_milestones` and `benchmarks`

> **How to run:** tell your agent *"run substep 48.17"*. Self-contained — runnable cold.
> **You will need a scoped Supabase personal access token (`sbp_…`) from the user.** Ask for it when
> you reach the apply step; do not proceed without it and do not look for one on disk.

**Assigned model: GPT 5.6 Terra.** This is the only substep in the remediation wave that mutates a
**live database holding committed data**, and a careless `ALTER`/`DROP` is the one irreversible
action in the wave. It also decides the durable shape of two entities and writes them into Doc 04,
so a wrong shape becomes the architecture. The judgement is bounded — Doc 04, the existing migration
conventions, and the app's own models state the expected answer — which is why it is Terra rather
than Opus. **Escalate to Opus 4.8 or stop and ask the user** if any change you are about to apply is
not purely additive, or if the entity shape appears to contradict an accepted ADR.

## Why this substep exists

Branch-head CI run [`33327930159`](https://github.com/lvinist/mine-flow-app/actions/runs/33327930159)
failed both E2E jobs. Among the causes, two are not bugs but **absences** — the application queries
two tables that no migration has ever created:

```
PGRST205  Could not find the table 'public.timeline_milestones' in the schema cache
PGRST205  Could not find the table 'public.benchmarks' in the schema cache
```

Both are full features in the shipped app — blocs, screens, routes, sync registrars, local and
remote datasources:

- `lib/features/benchmark/data/datasources/benchmark_remote_datasource.dart` — `from('benchmarks')`,
  full CRUD plus a realtime subscription.
- `lib/features/timeline/data/datasources/timeline_remote_datasource.dart` —
  `from('timeline_milestones')`, CRUD plus soft delete.

`Benchmark` is already described in `architecture/04-data-model.md` §1 with its full field list.
`TimelineMilestone` appears in **no** architecture doc at all. Neither has a migration. This is
schema debt that every runtime path has been hiding until real journeys ran.

**PLAN decision D7 (user, 2026-08-31):** both entities are in scope. Author real migrations, apply
them to staging, regenerate the contract artifact, and record them in Doc 04.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — the 2026-08-31 amendment, decisions **D5** and
  **D7**, questions **Q8** and **Q9**.
- `Upcoming Prompts/mine-flow-STEP-48.16-FINDINGS.md` — your inbound work items. 48.16's register
  assigns you specific `BH-nnn` rows; those are your scope, not the whole failure list.
- root `.throughstone/local-user.md` — Experience level 2, Explanatory.
- **`Code/mine-flow-docs/architecture/04-data-model.md`** — §1 Entity Model (the `Benchmark` row is
  already there, verbatim: `id`, `bm_id`, `northing`, `easting`, `ortho_height`, `code`, `orde`,
  `geom`, `latitude`, `longitude`, `ellips_height`, `status`), §2 Ownership, §4 PII & Sensitive Data
  (Benchmark is marked internal confidential), §5 Consistency & Evolution, and the Version Log.
- **`Code/mine-flow-app/supabase/migrations/20260718000001_core_schema.sql`** — the conventions every
  new table must match: `id UUID PRIMARY KEY DEFAULT gen_random_uuid()`, `site_id UUID NOT NULL
  DEFAULT '00000000-0000-0000-0000-000000000001'`, `created_at`/`updated_at TIMESTAMPTZ NOT NULL
  DEFAULT NOW()`, `deleted_at TIMESTAMPTZ` for soft delete, and a
  `CREATE TRIGGER … EXECUTE FUNCTION public.update_updated_at_column()` per table.
- **`Code/mine-flow-app/supabase/migrations/20260718000002_rls_policies.sql`** — every existing table
  is `ENABLE ROW LEVEL SECURITY` with role policies built on `public.current_user_role()`
  (`supervisor` full access; `foreman`/`crew` scoped reads). Your tables must follow suit.
- `Code/mine-flow-app/supabase/migrations/20260723_step_33_1_data_model_polish.sql` — how a later
  migration is named and structured in this project.
- `Code/mine-flow-app/lib/features/benchmark/data/models/benchmark_model.dart` and
  `lib/features/timeline/data/models/timeline_milestone_model.dart` — **the authoritative column
  list**: read every key in `fromJson`/`toJson`. The migration must cover exactly what the app
  reads and writes.
- `Code/mine-flow-app/lib/features/timeline/data/migrations/create_timeline_milestones.sql` — an
  **orphan, never-applied** fragment. See Q9.
- `Code/mine-flow-app/tool/check_supabase_contracts.dart` — read it before you commit anything. It
  fails if migrations changed without a regenerated `supabase/types/database.ts`, and it rejects a
  stub by content (`export type Database` **and** `__InternalSupabase`, ≥2000 bytes).
- `Code/mine-flow-docs/registries/risks.yml` — **RISK-0019** and **RISK-0022** (benchmark deferred
  against staging, missing table). Their status may change because of your work; supply a
  close-or-re-justify recommendation, but leave the register edits to 48.14's successor / 48.25's
  reconciliation as the PLAN routes them.

## Decisions already made for you

- **Q8 — both entities are in scope** (user). Author the migrations; add both to Doc 04 §1.
  Judgement still yours: does `TimelineMilestone`'s shape encode a *product rule* — target vs actual
  value, target/start/end dates, a status vocabulary — that deserves an **ADR** alongside
  **ADR-0015** (plan/actual date+zone separation)? If yes, write it; if it is merely a table, a Doc
  04 Version Log entry suffices. Say which you chose and why.
- **Q9 — prefer a fresh migration.** The orphan fragment references a `sites` table that exists in
  **no** migration (`site_id` is a bare `UUID` with a default everywhere else in this schema), so
  adopting it as-is would fail. Write a fresh migration under `supabase/migrations/` following the
  house conventions, then **delete the orphan** so no future reader mistakes it for applied schema.
  If you keep it instead, say why in the findings.

## Your task

### 1. Derive each table from the app's own model

For each entity, list every JSON key the model reads and writes, then map it to a column with a
deliberate type. Do not guess types from names — read how the Dart code uses the value.

For `benchmarks`, note in particular:

- `bm_id` is a **natural identifier** (`Text`) distinct from the UUID primary key. Decide whether it
  is unique, and per-site or global.
- `northing`, `easting`, `ortho_height`, `latitude`, `longitude`, `ellips_height` are all
  `double` in Dart. Choose `double precision` or `NUMERIC(p,s)` and justify it — survey coordinates
  care about precision, and `20260723_step_33_1` already moved this project toward
  `double precision` for volumes.
- `geom` is `dynamic` in Dart and Doc 04 calls it "PostGIS geometry". **Check whether PostGIS is
  actually enabled** in this project before declaring a `geometry` column; if it is not, a nullable
  `jsonb` or `text` is the honest choice and the divergence from Doc 04 must be recorded. Do not
  enable an extension as a side effect of this substep.
- `crs_identifier` exists in the model with a default of `'UTM Zone 51S'` and is the subject of
  **ADR-0014 (persist CRS identifier)** — read that ADR and make the column match its decision.
- `status` is a free `String` in Dart, and `deleteBenchmark` implements soft delete by setting
  `status = 'deleted'` rather than writing `deleted_at`. Decide whether to add `deleted_at` for
  consistency with every other table, and if you do, note that the app's delete path does **not**
  currently use it — that is a finding for 48.18/48.19's class of work, not a silent fix here.

For `timeline_milestones`, the model's keys are your contract. Cross-check the orphan fragment's
column list against `timeline_milestone_model.dart` and use the model where they disagree — the
model is what runs.

### 2. Write the migrations

One new file per entity (or one combined file if you prefer — say which and why), named in the
existing style, e.g. `supabase/migrations/20260831000001_step_48_17_timeline_milestones.sql`.

Each must include:

- the `CREATE TABLE` with house-convention columns (`id`, `site_id` with default, timestamps,
  `deleted_at`);
- the `update_updated_at_column` trigger;
- indexes for the columns the app filters and orders on — read the datasources: timeline filters
  `site_id`, `zone_id`, `deleted_at` and orders by `target_date`; benchmarks filter `status` and
  order by `created_at`;
- `ALTER TABLE … ENABLE ROW LEVEL SECURITY` **plus policies**. This is not optional: every other
  table in this schema has RLS, and a table with RLS enabled and no policy is unreadable, while a
  table without RLS is readable by every authenticated user. Mirror the role model in
  `20260718000002` — `supervisor` full access via `public.current_user_role() = 'supervisor'`,
  `foreman`/`crew` scoped reads — and state explicitly which roles may write. **If you are unsure
  whether foremen should create benchmarks or milestones, ask the user rather than guessing**: this
  is an authorization decision, and guessing wrong either blocks a real workflow or opens a write
  path that should not exist.
- FK references only to tables that exist (`public.users`, `public.zones`). There is no `sites`
  table.

Make the migrations **idempotent where the house style allows** (`IF NOT EXISTS` on tables and
indexes) so a re-run is safe.

### 3. Apply to linked staging

Ask the user for a scoped Supabase personal access token. Then, in one session:

```bash
export SUPABASE_ACCESS_TOKEN=sbp_…          # session only; never write it to a file
supabase seed buckets --linked              # cheap auth check: JSON counters on success
```

Apply the migrations. `supabase db push --linked` is the intended route; if it is unavailable or
misbehaves, `supabase db query --linked --file <path>` executes raw SQL and is the verified fallback
in this project. Two known quirks: `--file -` (stdin) does **not** work — write a temp file under
`$LOCALAPPDATA/Temp` and pass a native-readable path; and only the **last** statement's result set
is surfaced, so aggregate verification into a single `SELECT`.

Verify from the database, not from the command's exit code:

```sql
SELECT jsonb_pretty(jsonb_object_agg(t, c ORDER BY t)) AS present FROM (
  SELECT 'timeline_milestones' t,
         (SELECT count(*)::int FROM information_schema.tables
          WHERE table_schema='public' AND table_name='timeline_milestones') c
  UNION ALL SELECT 'benchmarks',
         (SELECT count(*)::int FROM information_schema.tables
          WHERE table_schema='public' AND table_name='benchmarks')
) s;
```

Then confirm the columns and the policies exist — query `information_schema.columns` and
`pg_policies` for both tables and record the result. "The push exited 0" is not evidence.

**Safety boundary, non-negotiable:** additive DDL only — `CREATE TABLE`, `CREATE INDEX`,
`CREATE POLICY`, `ALTER TABLE … ENABLE ROW LEVEL SECURITY`, `ADD COLUMN`. If you find yourself
writing `DROP`, `TRUNCATE`, `DELETE`, or an `ALTER … TYPE` on an existing populated column, **stop
and ask the user.** Never read or print `.env` values. Never echo the token. Remind the user to
revoke the token when you are done, because it transited the chat.

### 4. Regenerate the contract artifact

```bash
supabase gen types --lang typescript --linked > supabase/types/database.ts
```

Then run the guard and read its output:

```bash
cd Code/mine-flow-app && dart run tool/check_supabase_contracts.dart
```

It must exit 0 **and** the regenerated file must contain both new tables. Do not hand-edit the
artifact; the guard exists because a stub was once committed here. If typegen is unavailable, that is
a blocker to report — not something to work around by writing types yourself.

### 5. Update Doc 04

- Add a `TimelineMilestone` bullet to §1 Entity Model in the same style as the neighbours, with its
  field list.
- Amend the `Benchmark` bullet if your migration's real shape differs from what §1 claims — in
  particular if `geom` is not PostGIS geometry.
- Check §4 (PII & Sensitive Data): Benchmark is already marked internal confidential; decide whether
  milestones need a classification row.
- Bump the **Version:** header and append a Version Log row (`v0.1.4`, date, `STEP-48.17`, change).
  The doc is at v0.1.3.
- Do **not** hand-edit root `DESIGN.md` / `PRODUCT.md` — they are generated.

### 6. Confirm the journeys can now proceed

You are not closing the benchmark or timeline journeys — 48.24/48.25 run them. But before you finish,
run the two affected journeys once locally and record what happens: the `PGRST205` errors must be
gone. If a *different* error appears (a wrong column name, a missing seed row), that is expected —
record it and confirm 48.16's register already routes it to 48.18/48.19/48.20. If it routes to a
substep that has already run, say so.

## Verification

- Both tables exist in staging, confirmed by an `information_schema` query whose output you quote.
- Every column the app's models read or write exists, with types you can defend.
- RLS is enabled on both tables **and** each has at least one policy; `pg_policies` output quoted.
- `supabase/types/database.ts` regenerated, contains both tables, and
  `dart run tool/check_supabase_contracts.dart` exits 0.
- `flutter analyze` → 0 issues; `dart format --set-exit-if-changed .` → clean; `flutter test` green
  (the `attendance_daily_log_sync_test.dart` / `equipment_check_sync_test.dart` Hive `setUpAll` flake
  is known — re-run isolated to confirm, and say so).
- The two journeys no longer produce `PGRST205`, evidenced by a local run.
- Doc 04 updated with a Version Log bump.
- The orphan `create_timeline_milestones.sql` resolved (deleted, or kept with a stated reason).
- No secret value in any commit, log, or file. `git status` shows no `.env` and no token.

## Scope

**In scope:** the two migrations, their RLS policies and indexes, applying them to staging, the type
regeneration, Doc 04, an ADR if the entity shape warrants one, and the orphan fragment.

**Not in scope:** fixing wrong column names in datasources (48.18) or models (48.19), seed/fixture
data (48.20), any UI or test repair, `risks.yml` edits, and any schema change to an existing table
beyond an additive column your two entities genuinely require.

## Definition of done

- [ ] `supabase/migrations/` contains committed migrations creating `public.timeline_milestones` and
      `public.benchmarks` in house style.
- [ ] Both tables have RLS enabled with explicit, justified role policies.
- [ ] Both applied to linked staging; existence, columns, and policies verified by query, output
      quoted in the findings.
- [ ] `supabase/types/database.ts` regenerated by `supabase gen types`; contract guard exits 0.
- [ ] Doc 04 §1 carries both entities; Version bumped to v0.1.4 with a Version Log row.
- [ ] ADR written, or a recorded decision that none is needed (Q8).
- [ ] Orphan `lib/features/timeline/data/migrations/create_timeline_milestones.sql` resolved (Q9).
- [ ] `PGRST205` gone from a local run of the benchmark and timeline journeys; any new error routed.
- [ ] `flutter analyze` 0, `dart format` clean, `flutter test` green.
- [ ] Close-or-re-justify recommendation written for RISK-0019 and RISK-0022.
- [ ] `mine-flow-STEP-48.17-FINDINGS.md` written; PLAN progress table updated.
- [ ] Committed on `step-0048-runtime-evidence` in both `mine-flow-app` and `mine-flow-docs`.
- [ ] User reminded to revoke the Supabase access token.

## Next

Tell the user the next action is *"run substep 48.18"* (datasource column-name reconciliation) in a
**fresh chat**, and that 48.18–48.20 all depend on the schema you just landed. If 48.16's register
assigned nothing to one of them, say so.
