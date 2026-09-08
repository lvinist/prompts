# mine-flow — STEP-48.18: Datasource Column-Name Reconciliation

> **How to run:** tell your agent *"run substep 48.18"*. Self-contained — runnable cold.

**Assigned model: Gemini 3.1 Pro High.** Real reasoning is needed — you are deciding, per query,
whether the *database* or the *query* is wrong — but a written authority bounds every call: the
migration files say what columns exist, `architecture/04-data-model.md` says what should exist, and
**ADR-0012** governs the volume semantics. That is why this is the mid tier. **Escalate to Opus 4.8**
if a mismatch cannot be resolved without contradicting an accepted ADR, or if fixing a read path
would silently change a number a report or dashboard already shows a user.

## Why this substep exists

Branch-head CI run [`33327930159`](https://github.com/lvinist/mine-flow-app/actions/runs/33327930159)
failed both E2E jobs. Two of the errors are **read paths querying columns that do not exist**:

```
42703  column cut_fill_records.measurement_date does not exist
```

The real column is `measured_at`, created in `20260718000001_core_schema.sql`. Two datasources ask
for `measurement_date` anyway:

- `lib/features/timeline/data/datasources/timeline_remote_datasource.dart:71-72` —
  `.gte('measurement_date', …).lte('measurement_date', …)`
- `lib/features/reporting/data/datasources/reporting_remote_datasource.dart:63-64,72` — the same
  filter plus `.order('measurement_date')`

The same file has a sibling of the same bug that has **not fired yet** because the timeline journey
died on the first query:

- `timeline_remote_datasource.dart:80-81` filters `land_clearing_records` on `date`. The real column
  is `cleared_at` (`20260718000001`).
- `timeline_repository_impl.dart:73` reads `r['measurement_date']` and `:89` reads `r['date']` from
  the returned rows and calls `.substring(0, 10)` on them — a **hard cast on a null**, so these will
  throw rather than degrade once the query succeeds.

There is a third, quieter class in the same file. `reporting_remote_datasource.dart:74-75` reads
`row['cut_volume_m3']` and `row['fill_volume_m3']` with `as num?` and a `?? 0.0` fallback. Neither
column has ever existed — `20260718000001` created `cut_volume`/`fill_volume`, and
`20260723_step_33_1_data_model_polish.sql` **dropped** them in favour of `bcm_volume`/`lcm_volume`.
So this path does not error; it silently reports **zero volume** for every row, and then computes
`net_volume_m3 = cut − fill` — the exact formula **ADR-0012** rejected as meaningless. This is the
already-registered **RISK-0014**. Read that risk row before you touch the file.

Note the shape of that bug, because it is the reason this substep exists at all: a nullable read with
a fallback turns a schema mismatch into **wrong data instead of an error**. Those are worse than the
crashes, and they do not appear in a CI log.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — the 2026-08-31 amendment and the honesty rule.
- **`Upcoming Prompts/mine-flow-STEP-48.16-FINDINGS.md`** — your scope. 48.16's `BH-nnn` register
  assigns you specific rows and lists unfired same-class instances. Work that list, not your
  intuition about what else might be wrong.
- `Upcoming Prompts/mine-flow-STEP-48.17-FINDINGS.md` — **48.17 is a hard dependency.** The
  `timeline_milestones` and `benchmarks` tables must exist before your queries can be verified.
  48.17's findings also record any column-shape decision you must match.
- root `.throughstone/local-user.md` — Experience level 2, Explanatory.
- **`Code/mine-flow-app/supabase/migrations/`** — all files, in order. This is the only authority on
  what columns exist. Read `20260718000001_core_schema.sql` for the originals and
  `20260723_step_33_1_data_model_polish.sql` for the renames (`cut_volume`/`fill_volume` →
  `bcm_volume`/`lcm_volume` + `material_type`; `area_cleared_ha` → `plan_area`/`actual_area`;
  `vegetation_type` → `method`), and `20260724_…` for the geospatial drops.
- **`Code/mine-flow-docs/adr/ADR-0012-volume-and-land-clearing-metrics.md`** — bank-equivalent net
  via `VolumeNormalizer`; the `cut − fill` formula is explicitly rejected.
- **`Code/mine-flow-docs/registries/risks.yml`** — **RISK-0014** verbatim. It says the reporting path
  was *deliberately deferred* to a reporting STEP. Respect that: see "Scope" below.
- `Code/mine-flow-docs/architecture/04-data-model.md` — the entity/column authority; note it does not
  enumerate columns for every entity, so the migrations win on specifics.
- `Code/mine-flow-app/lib/features/tracking/data/models/cut_fill_model.dart` — a good example of the
  **tolerant read** pattern this project uses: `json['measured_at'] ?? json['measurement_date']`.
  That tolerance is fine on a *read of a returned row*; it is not a substitute for querying the right
  column name, because Postgres rejects the filter before any row comes back.

## Your task

### 1. Enumerate every remote query in the app

Not just the two failing files. For each `.from('…')` call chain in `lib/`, list every column named
in `.select()`, `.eq()`, `.gte()`, `.lte()`, `.order()`, `.filter()`, `.inFilter()`, `.isFilter()`,
and every key read out of the returned rows. Then diff that against the actual migration columns.

```bash
grep -rn "from('" lib/ --include=*.dart
```

Produce a table: file:line · table · column referenced · exists? · how it fails (error / silent
null). Silent-null rows matter as much as the erroring ones.

### 2. Decide, per mismatch, which side is wrong

- **query wrong, schema right** — the column has a different real name (`measured_at`,
  `cleared_at`). Fix the query. This is the common case.
- **schema wrong, query right** — the app needs a column the data model genuinely calls for and no
  migration provides. **This is not yours to add**; hand it to 48.17's owner or the user with the
  evidence, because a migration is a schema decision and 48.17 owns the token and the safety
  boundary.
- **both wrong** — the query names a column that never existed *and* the value it wants is computed
  differently now (the `cut_volume_m3` case). See step 4.

Do not "fix" a mismatch by adding a fallback that hides it. `json['a'] ?? json['b']` on a **returned
row** is an acceptable compatibility read; `.gte('a', …)` on a column that does not exist is always a
bug.

### 3. Fix the read paths and their consumers

Correct the queries, and then follow the value through. Specifically:

- `timeline_repository_impl.dart:73` and `:89` cast the date field with
  `(r['measurement_date'] as String).substring(0, 10)` — an unguarded cast. Once the query returns
  rows keyed `measured_at`/`cleared_at`, these must read the right key **and** stop crashing on null.
  Decide whether a null date should skip the row or default, and say why.
- Check every other consumer of the rows you re-keyed. A query fix that leaves the repository reading
  the old key converts a Postgres error into a null-pointer crash — a lateral move, not a fix.

### 4. RISK-0014 — scope discipline

`reporting_remote_datasource.fetchCutFillData` is registered as deliberately deferred tech debt
(RISK-0014), and re-implementing ADR-0012's `VolumeNormalizer` net in the reporting path is a
**reporting STEP's** job, not yours. But it currently queries a **non-existent column**
(`measurement_date`) in the filter, which is your class of defect and blocks the reporting journey.

Do this: fix the column names so the query executes, and leave the volume *formula* alone. Then
record the residual precisely — the report will now return real rows with `cut_volume_m3` and
`fill_volume_m3` still resolving to `0.0` from missing columns, which means **reports will show zero
volumes**. That may be worse than erroring, so it needs a judgement:

- if a zero-volume report is misleading enough to be a release blocker, say so and recommend RISK-0014
  be re-severitied or pulled forward — do not quietly ship it;
- if the reporting path is unreachable in the MVP flow, evidence that and leave it deferred.

Either way, write the recommendation into your findings and amend RISK-0014's description with what
you verified at runtime. **Do not change its status yourself** — the register reconciliation owns
that.

Watch for the same silent-fallback class elsewhere in that file: `minimum_stock` is read from
`inventory_items`, whose real column is `min_threshold`. Sweep it.

### 5. Pin each fix with a test

A column-name bug is invisible to a widget test and only fires against real Postgres, which is why it
survived to a branch-head run. Add unit tests that assert the **query shape** — mock or fake the
Supabase client and assert the emitted filter/order column names, or at minimum assert the
repository's mapping against a fixture row keyed with the real column names. Follow the existing test
conventions in `test/features/…` rather than introducing a new mocking approach.

Aim for: if someone renames a column in a migration and forgets a datasource, a `flutter test` run
tells them.

## Verification

- Every remote query in `lib/` audited; the audit table is in your findings.
- Every mismatch either fixed, or handed to a named owner with evidence.
- No unguarded cast left on a date/number read from a re-keyed row.
- New unit tests fail if the column names regress; you have run them and seen them pass.
- `flutter analyze` → 0 issues; `dart format --set-exit-if-changed .` → clean.
- `flutter test` → green. The `attendance_daily_log_sync_test.dart` / `equipment_check_sync_test.dart`
  Hive `setUpAll` flake is known: re-run isolated to confirm and say so; never wave a red suite
  through.
- The timeline and reporting journeys run locally without `42703`, with the counts recorded. If they
  fail for a *different* reason, confirm 48.16's register routes it elsewhere and name the substep.
- RISK-0014's runtime status recorded with a recommendation; its status cell untouched.

## Scope

**In scope:** column names in remote **read** queries and the consumers of those rows; the unfired
same-class instances 48.16 listed; tests pinning them.

**Not in scope:** write-path `toJson()` maps (48.19 — `item_name`, `equipment_checks.status`,
`vegetation_type`), new migrations or any staging mutation (48.17), seed/fixture data (48.20), finder
repair (48.21), UI defects (48.22), persistence defects (48.23), `risks.yml` status edits,
re-implementing ADR-0012's net-volume formula in reporting (a later reporting STEP).

## Keeping the docs true

If a mismatch reveals that `architecture/04-data-model.md` describes a column the schema does not
have — or vice versa — that is doc drift: fix the doc and bump its Version Log. If the app contradicts
an accepted ADR, that is a **bug and a finding**, not a licence to edit the ADR. New or changed
functions get docstrings; comment the *why* wherever a compatibility read remains.

## Definition of done

- [ ] Full remote-query audit table written (file:line · table · column · exists · failure mode).
- [ ] `timeline_remote_datasource.dart` queries `measured_at` and `cleared_at`.
- [ ] `reporting_remote_datasource.dart` queries real columns; `minimum_stock` mismatch resolved.
- [ ] `timeline_repository_impl.dart` reads the correct keys with no unguarded cast.
- [ ] Every unfired same-class instance from 48.16's list fixed or explicitly routed.
- [ ] Unit tests added that catch a column-name regression; run and passing.
- [ ] `flutter analyze` 0, `dart format` clean, `flutter test` green (flake diagnosed).
- [ ] Timeline + reporting journeys run locally; `42703` gone; counts recorded.
- [ ] RISK-0014 runtime status and recommendation recorded; register status not edited here.
- [ ] `mine-flow-STEP-48.18-FINDINGS.md` written; PLAN progress table updated.
- [ ] Committed on `step-0048-runtime-evidence`.

## Next

Tell the user the next action is *"run substep 48.19"* (write-path dual-key purge) in a **fresh
chat**. Note that 48.19 touches `land_clearing_model.dart`, which you may also have edited — flag any
file you changed that 48.19 will reopen.
