# mine-flow — STEP-48.20: Staging Fixture & Seed Alignment

> **How to run:** tell your agent *"run substep 48.20"*. Self-contained — runnable cold.
> A scoped Supabase personal access token (`sbp_…`) may be needed to reseed staging — ask the user.

**Assigned model: Gemini 3.1 Pro High.** Bounded reasoning against written authorities: `seed.sql`,
the RLS policy file, `app_constants.dart`, and Doc 04. The one genuinely interesting call is the
`42501` RLS refusal — deciding whether the policy is right and the test is wrong, or the reverse.
**Escalate to Opus 4.8** for any refusal where a role that *should* be permitted is denied (that is
security-shaped), and **ask the user** before deleting or overwriting existing staging rows.

## Why this substep exists

Branch-head CI run [`33327930159`](https://github.com/lvinist/mine-flow-app/actions/runs/33327930159)
failed both E2E jobs. A whole class of those failures is not a code bug — the schema is fine and the
queries are fine, but the **data the journeys run against is wrong**:

```
22P02  invalid input syntax for type uuid: ""            /rest/v1/zones
23503  insert or update on table "daily_logs" violates foreign key constraint
       "daily_logs_zone_id_fkey"  —  Key is not present in table "zones"
22P02  invalid input syntax for type uuid: "KRU-001"     /rest/v1/attendance_records
22P02  invalid input syntax for type uuid: "KRU-002"     /rest/v1/attendance_records
42501  new row violates row-level security policy for table "zones"
```

Read together they tell one story. A zone write goes out with an **empty-string id**, Postgres rejects
it, so the zone never exists, so the daily log's `zone_id` FK fails. Separately, attendance is written
with crew identifiers `KRU-001`/`KRU-002` where the column is `uuid`. And a zone insert is refused
outright by RLS.

Underneath all of it sits a mismatch that was already handed forward by 48.1 and never settled:

| | Value |
|---|---|
| `lib/core/constants/app_constants.dart:55` | `defaultSiteId = 'f47ac10b-58cc-4372-a567-0e02b2c3d479'` |
| `supabase/seed.sql` | every row seeded under `00000000-0000-0000-0000-000000000001` |

Ten journeys call repositories with `siteId: defaultSiteId`. The seeded data lives under a different
site. So list assertions find nothing — for reasons that have nothing to do with the code under test.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — the 2026-08-31 amendment, decision **D7**, and
  question **Q10** (which carries the recommendation for the site-id mismatch).
- **`Upcoming Prompts/mine-flow-STEP-48.16-FINDINGS.md`** — your scope: the `BH-nnn` rows classified
  **fixture-drift** are yours, and only those.
- `Upcoming Prompts/mine-flow-STEP-48.17-FINDINGS.md` — **hard dependency.** The new
  `timeline_milestones` / `benchmarks` tables and their RLS policies exist now; seed data for them may
  be needed, and their policies constrain who can write.
- `Upcoming Prompts/mine-flow-STEP-48.0-FINDINGS.md` — records the three staging accounts created
  (`supervisor@`, `foreman@`, and a `crew@` account whose secrets were never set) and the seed
  revision used at the time.
- `Upcoming Prompts/mine-flow-STEP-48.1-FINDINGS.md` — where the `defaultSiteId` ≠ seed `site_id`
  problem was first handed forward.
- root `.throughstone/local-user.md` — Experience level 2, Explanatory.
- **`Code/mine-flow-app/supabase/seed.sql`** — all of it. Note it uses static UUIDs; confirm whether
  it is idempotent (`ON CONFLICT … DO NOTHING`) before you re-run it against staging.
- **`Code/mine-flow-app/supabase/migrations/20260718000002_rls_policies.sql`** — the authorization
  truth. For `zones`: `supervisor_zones_all` grants `FOR ALL` to `current_user_role() = 'supervisor'`;
  `zones_read_active` grants **SELECT only** to `foreman` and `crew`. So a non-supervisor cannot
  insert a zone, by design.
- `Code/mine-flow-app/lib/core/constants/app_constants.dart` — `defaultSiteId` and its neighbours.
- `Code/mine-flow-app/integration_test/helpers/staging_config.dart` — which credentials exist
  (`TEST_USER_*`, `TEST_SUPERVISOR_*`, `TEST_FOREMAN_*`; **no** `TEST_CREW_*`) and the
  `hasPerRoleAccounts` / `hasCrewAccount` gates.
- `Code/mine-flow-app/integration_test/helpers/login_helper.dart` — which role each journey logs in
  as. This determines whether a `42501` is expected.
- `Code/mine-flow-docs/architecture/09-environments.md` — staging parity and seeding posture.
- `Code/mine-flow-docs/registries/risks.yml` — **RISK-0021** (partial RLS matrix, crew leg
  unverified). Your work may bear on it; recommend, do not edit.

## Your task

### 1. Settle the site-id mismatch (Q10)

The PLAN recommends changing the **seed** to use `defaultSiteId` and leaving the constant alone: the
constant is referenced by shipped app code and by Hive-cached rows on real devices, while seed data is
disposable fixture data. Follow that unless you find a concrete reason not to — and if you do, state
it and ask the user before diverging.

Whichever way it goes, it must be **one** value end to end: `seed.sql`, any E2E-specific seed you add,
and every journey's `siteId:` argument. Grep for both UUID literals across the whole repo and prove no
straggler remains.

If you change the seed's site, check every FK'd row in `seed.sql` — users, zones, attendance,
equipment checks, daily logs, inventory — moves with it. A half-migrated seed is worse than the
mismatch.

### 2. Find the source of the empty-string UUID

`22P02 … uuid: ""` on `/rest/v1/zones` is a *write* carrying `id: ''` or `zone_id: ''`. That is not
seed data — something in the app or the journey constructs a zone with an empty id. Trace it:

- which journey was running when it fired (the Android log's `❌` grouping tells you);
- which code path builds that zone — look at the `CreatableCombobox` "add new zone" flow the daily-log
  and cut/fill journeys use, and at `zone_model.dart`'s `fromJson`/`toJson` defaults.

Then decide the classification honestly. If the **app** can write an empty-string id, that is an
app-defect and belongs to 48.22/48.23 — hand it over with evidence rather than papering over it with
seed data. If the **journey** builds it, fix the journey. Say which it was; do not fix the symptom in
the seed if the cause is in `lib/`.

Same for `KRU-001`/`KRU-002`: those look like human-readable crew codes used where a `users.id` UUID
belongs. Find who supplies them — a journey fixture, or the app mapping a display code into an id
field. The second is a data-integrity defect and is 48.23's class.

### 3. Resolve the `42501` zone-insert refusal

Determine which role the failing journey authenticated as. Then:

- **refusal is correct** — a foreman or crew user tried to insert a zone, and
  `20260718000002_rls_policies.sql` deliberately allows only supervisors. The **test** is wrong: it
  should either log in as supervisor for that step, or assert the refusal as expected behaviour. An
  RLS policy doing its job is evidence the security model works — record it as such, and consider
  whether the journey should assert it deliberately (that would strengthen RISK-0021's coverage).
- **refusal is wrong** — a supervisor was refused, or a role the data model says should be able to
  create zones cannot. That is **security-shaped**: escalate to Opus 4.8 and the user. Do not "fix"
  it by loosening a policy. Changing an RLS policy is a security posture change and needs an explicit
  decision, not a green test.

Record which it was, with the role and the policy name quoted.

### 4. Make the fixtures fit for purpose

Decide and document how E2E fixture data is provisioned. Options, in order of preference:

1. **Reuse `seed.sql`** if it is idempotent and sufficient — simplest, single source of truth.
2. **Add an E2E-specific seed file** (e.g. `supabase/e2e-seed.sql`) if the journeys need rows
   `seed.sql` should not carry. Document it in `architecture/09-environments.md` if it becomes part of
   the staging procedure.
3. Have journeys create their own fixtures at setup — only where a journey genuinely needs a fresh
   row, and only with real UUIDs (`Uuid().v4()`, as `offline_sync_journey_test.dart` already does
   after 48.10 hit this same class).

Requirements either way:

- every identifier is a **real UUID**; no empty strings, no `KRU-001`-style codes;
- every FK points at a row that exists;
- rows exist under the *one* site id settled in step 1;
- the seed is **idempotent** so a re-run does not fail on conflict or duplicate rows;
- the seed revision (a commit sha or a dated note) is recorded in your findings so results are
  reproducible — 48.0 set that precedent.

### 5. Apply to staging and verify from the database

Ask the user for a scoped `sbp_…` token if you need to reseed.

```bash
export SUPABASE_ACCESS_TOKEN=sbp_…              # session only; never written to a file
supabase seed buckets --linked                  # cheap auth check
supabase db query --linked --file supabase/seed.sql
```

Known quirks in this project: `supabase db seed` no longer exists in the v2 CLI; `[db.seed] sql_paths`
in `config.toml` applies to local `db reset` only and does **not** push to remote; `--file -` (stdin)
does not work — write a temp file under `$LOCALAPPDATA/Temp` and pass a native-readable path; and only
the **last** statement's result set is surfaced, so aggregate verification into one `SELECT`:

```sql
SELECT jsonb_pretty(jsonb_object_agg(t, c ORDER BY t)) AS counts FROM (
  SELECT 'users' t, count(*)::int c FROM public.users
  UNION ALL SELECT 'zones',           count(*)::int FROM public.zones
  UNION ALL SELECT 'daily_logs',      count(*)::int FROM public.daily_logs
  UNION ALL SELECT 'attendance',      count(*)::int FROM public.attendance_records
  UNION ALL SELECT 'inventory_items', count(*)::int FROM public.inventory_items
  UNION ALL SELECT 'equipment_checks',count(*)::int FROM public.equipment_checks
) s;
```

Also count rows **under the settled site id** specifically — a global count of 2 zones proves nothing
if both sit under the wrong site.

**Safety boundary:** additive and idempotent operations only. If reaching a clean fixture state seems
to require `DELETE` or `TRUNCATE` against staging, **stop and ask the user** — staging holds data other
substeps' evidence rests on. Never read or print `.env`. Never echo the token. Remind the user to
revoke it afterwards.

### 6. Re-run the affected journeys

Run the journeys 48.16 assigned you (daily log, cut/fill, attendance, RLS at minimum) locally against
the reseeded staging and record ran-vs-skipped counts per file. `22P02` and `23503` must be gone. A
`42501` may legitimately remain if you concluded the refusal is correct — in that case the journey
should now *assert* it rather than crash on it.

## Verification

- One site id used consistently across `seed.sql`, any E2E seed, and every journey; grep proves no
  straggler.
- The empty-string-UUID source identified and classified — fixed here if fixture, handed over with
  evidence if app-defect.
- `KRU-001`/`KRU-002` source identified and classified the same way.
- The `42501` resolved with the role and policy name quoted, and a stated verdict on whether the
  refusal is correct.
- Staging row counts verified **by query**, including counts scoped to the settled site id; output
  quoted.
- Seed idempotency confirmed by running it twice.
- Seed revision recorded.
- `flutter analyze` 0; `dart format` clean; `flutter test` green (Hive `setUpAll` flake diagnosed
  isolated, not waved).
- Assigned journeys re-run; `22P02`/`23503` gone; counts recorded.
- No RLS policy weakened. No staging row deleted without explicit user approval.

## Scope

**In scope:** fixture and seed data, the site-id reconciliation, identifier validity, the RLS-refusal
verdict, and journey-side fixture construction.

**Not in scope:** migrations or schema DDL (48.17), read-query column names (48.18), write-path key
sets (48.19), finder repair (48.21), UI defects (48.22), persistence/offline defects (48.23),
`risks.yml` status edits, and creating new staging **accounts** or secrets (that was 48.0; if the crew
leg still lacks `TEST_CREW_*`, record it and leave RISK-0021 open).

## Keeping the docs true

If the staging seeding procedure changes, `architecture/09-environments.md` must say so — update it
and bump its Version Log. If `architecture/04-data-model.md` disagrees with the fixture reality, fix
the doc, not the data model's meaning. An RLS policy change would need an ADR and is out of scope
here.

## Definition of done

- [ ] Site-id mismatch settled per Q10; one value end to end; grep evidence in findings.
- [ ] Empty-string UUID source found, classified, and either fixed or routed with evidence.
- [ ] `KRU-001`/`KRU-002` source found, classified, and either fixed or routed.
- [ ] `42501` verdict recorded with role + policy name; escalated if a permitted role was refused.
- [ ] Fixture provisioning approach chosen and documented; seed idempotent; revision recorded.
- [ ] Staging reseeded and verified by query, including per-site counts; output quoted.
- [ ] Assigned journeys re-run locally; `22P02`/`23503` gone; counts recorded.
- [ ] `flutter analyze` 0, `dart format` clean, `flutter test` green.
- [ ] `architecture/09-environments.md` updated if the procedure changed (Version Log bumped).
- [ ] `mine-flow-STEP-48.20-FINDINGS.md` written; PLAN progress table updated.
- [ ] Committed on `step-0048-runtime-evidence`; user reminded to revoke the Supabase token.

## Next

Tell the user the next action is *"run substep 48.21"* (journey finder repair) in a **fresh chat**.
Flag anything you handed to 48.22 or 48.23, and note whether the crew RLS leg is still credential-blocked.
