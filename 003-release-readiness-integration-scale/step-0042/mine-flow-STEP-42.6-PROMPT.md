# mine-flow — STEP-42.6: Seed Data Audit & Patch

> **How to run:** Tell your agent: **"Read and run `Upcoming Prompts/mine-flow-STEP-42.6-PROMPT.md`."**
> This substep is self-contained — executable cold in a fresh chat.

## Context

`supabase/seed.sql` was written in STEP-3 against the original schema. Since then, three STEPs added new tables and columns that the seed does not cover: STEP-33 (BCM/LCM columns + `material_type` on `cut_fill_records`; `clearing_method` on `land_clearing_records`), STEP-36 (new `benchmark_records` table), and STEP-38 (`AttendanceFormPage` which exercises a second distinct attendance row). This substep audits the gap and patches the seed, then re-seeds staging.

**Known state (as of completion of 42.4 — can run in parallel with 42.5):**
- `supabase/config.toml` linked to staging project.
- Staging already seeded once (STEP-42.1) with the original `seed.sql`.
- Supabase CLI installed.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-42-PLAN.md`
- `.throughstone/local-user.md`
- `Code/mine-flow-app/supabase/seed.sql` ← you will patch this
- `Code/mine-flow-app/supabase/migrations/20260723_step_33_1_data_model_polish.sql` ← new columns
- `Code/mine-flow-app/supabase/migrations/` (all 5 files — audit column names)
- `Code/mine-flow-docs/architecture/04-data-model.md`

## Scope

**Own:** Read migrations to identify new columns/tables since the seed was written; patch `supabase/seed.sql` with well-formed synthetic rows; re-seed staging; confirm all 8 feature tables are populated in the dashboard.

**Do not:** Change migration files. Change application code. Add real or production data. Remove existing seed rows (only add).

## Your task

### 1. Audit new columns and tables since STEP-3

Read the two migrations added after the original seed:
- `20260723_step_33_1_data_model_polish.sql` — record every new column added to existing tables.
- `20260723_step_34_1_drop_geospatial_file_lat_lon.sql` — record any columns dropped (do not include dropped columns in seed rows).

Also check: does a `benchmark_records` table exist in the migrations? If yes, note the full column list required for an INSERT. If no, note that and skip the benchmark seed row.

### 2. Patch `supabase/seed.sql`

Add the following synthetic rows (adjust column lists to match what you found in step 1):

**A. Additional `cut_fill_records` row (with STEP-33 columns):**
```sql
-- Additional cut/fill row with STEP-33 material_type and BCM/LCM columns
INSERT INTO public.cut_fill_records (id, site_id, daily_log_id, zone_id, cut_volume, fill_volume, elevation_change, measured_by, material_type, bcm_volume, lcm_volume)
VALUES
    ('f2222222-ffff-2222-ffff-222222222222', '00000000-0000-0000-0000-000000000001', 'e1111111-eeee-1111-eeee-111111111111', 'b2222222-bbbb-2222-bbbb-222222222222', 800.00, 200.00, -0.75, '22222222-2222-2222-2222-222222222222', 'Overburden', 760.00, 880.00)
ON CONFLICT (id) DO NOTHING;
```
(Adjust column names and types to match the actual migration. If `bcm_volume`/`lcm_volume`/`material_type` do not exist, skip them and note why.)

**B. Additional `land_clearing_records` row (with STEP-33 `clearing_method`):**
```sql
INSERT INTO public.land_clearing_records (id, site_id, daily_log_id, zone_id, area_cleared_ha, vegetation_type, cleared_by, clearing_method)
VALUES
    ('g2222222-gggg-2222-gggg-222222222222', '00000000-0000-0000-0000-000000000001', 'e1111111-eeee-1111-eeee-111111111111', 'b2222222-bbbb-2222-bbbb-222222222222', 1.20, 'Grassland', '22222222-2222-2222-2222-222222222222', 'Manual')
ON CONFLICT (id) DO NOTHING;
```

**C. Second `attendance_records` row (exercises AttendanceFormPage):**
```sql
INSERT INTO public.attendance_records (id, site_id, user_id, date, status, remarks, logged_by)
VALUES
    ('c2222222-cccc-2222-cccc-222222222222', '00000000-0000-0000-0000-000000000001', '22222222-2222-2222-2222-222222222222', CURRENT_DATE, 'present', 'Foreman attendance record', '11111111-1111-1111-1111-111111111111')
ON CONFLICT (id) DO NOTHING;
```

**D. `benchmark_records` row (STEP-36 — only if table exists in migrations):**
```sql
-- Add a benchmark record if the table exists (STEP-36)
INSERT INTO public.benchmark_records (id, site_id, name, easting, northing, elevation, crs_code, created_by)
VALUES
    ('j1111111-jjjj-1111-jjjj-111111111111', '00000000-0000-0000-0000-000000000001', 'BM-001 PIT Rusia', 453210.50, 9812345.75, 125.30, 'EPSG:32748', '22222222-2222-2222-2222-222222222222')
ON CONFLICT (id) DO NOTHING;
```
(Adjust column list to match STEP-36 migration schema exactly. If the table does not exist, skip and note it.)

### 3. Re-seed staging

```bash
# From Code/mine-flow-app/:
supabase db seed --file supabase/seed.sql
```

Record the output and any errors. If there are column-mismatch errors, adjust the INSERT statements to match the actual schema and re-run.

### 4. Verify in Supabase dashboard

Check the following tables for at least the listed row counts:

| Table | Min rows expected |
|-------|------------------|
| `public.users` | 3 |
| `public.zones` | 2 |
| `public.attendance_records` | 2 |
| `public.equipment_checks` | 1 |
| `public.daily_logs` | 1 |
| `public.cut_fill_records` | 2 |
| `public.land_clearing_records` | 2 |
| `public.inventory_items` | 2 |
| `public.geospatial_files` | 1 |
| `public.benchmark_records` | 1 (if table exists) |

Record actual row counts as evidence.

### 5. Commit the patched seed

```bash
# From Code/mine-flow-app/:
git add supabase/seed.sql
git commit -m "feat(STEP-42.6): patch seed.sql for STEP-33/36/38 schema additions"
git push
```

## Verification

- `supabase db seed` exits 0 with no errors.
- Supabase dashboard confirms expected row counts in all feature tables.
- No real or production data inserted — all rows use static synthetic UUIDs and test values.
- `git diff HEAD~1 supabase/seed.sql` shows only additions, no removals of existing rows.
- `flutter analyze` still clean; `flutter test` still 434+ tests, 0 failures.

## Definition of done

- [ ] Migrations audited; new columns and tables identified and documented.
- [ ] `supabase/seed.sql` patched with rows for: second `cut_fill_records` (STEP-33 cols), second `land_clearing_records` (STEP-33 cols), second `attendance_records`, `benchmark_records` (if table exists).
- [ ] `supabase db seed` exits 0; no errors.
- [ ] Staging dashboard confirms all 8+ feature tables populated with expected row counts.
- [ ] Patched seed committed and pushed on `step-0042-staging-pipeline`.

## Next

After committing, start a fresh chat and run **substep 42.7**: `Upcoming Prompts/mine-flow-STEP-42.7-PROMPT.md`.
