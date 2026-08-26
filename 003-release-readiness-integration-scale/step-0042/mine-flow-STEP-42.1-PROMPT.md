# mine-flow — STEP-42.1: Supabase CLI Install, Link & Migrations

> **How to run:** Tell your agent: **"Read and run `Upcoming Prompts/mine-flow-STEP-42.1-PROMPT.md`."**
> This substep is self-contained — executable cold in a fresh chat.

## Context

STEP-42 provisions the staging environment and wires the CI promotion pipeline. Its PLAN is at `Upcoming Prompts/mine-flow-STEP-42-PLAN.md`. This is the first substep: connect to the already-provisioned staging Supabase project, apply migrations, seed synthetic data, and commit `supabase/config.toml`.

**Known state (as of 2026-08-09):**
- `Code/mine-flow-app` is on `master` (STEP-41 merged). 434 tests passing. `flutter analyze` clean.
- `supabase/config.toml` does **not** exist — blocked by missing CLI in STEP-41.
- `supabase/migrations/` has 5 SQL files (last: `20260723_step_34_1_drop_geospatial_file_lat_lon.sql`).
- `supabase/seed.sql` exists (version 20260718 — gaps to be patched in substep 42.6).
- Supabase CLI is **not** installed. Install it before any `supabase` command.
- The staging Supabase project **already exists** — do not create a new one.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-42-PLAN.md`
- `.throughstone/local-user.md`
- `Code/mine-flow-app/README.md`
- `Code/mine-flow-app/supabase/seed.sql`
- `Code/mine-flow-docs/architecture/08-infrastructure-deployment.md`
- `Code/mine-flow-docs/architecture/09-environments.md`

## Scope

**Own:** Install Supabase CLI; link existing staging project; apply migrations; run seed; commit `config.toml`; confirm staging URL reachable.

**Do not:** Generate Dart types (substep 42.2). Set GitHub Secrets (substep 42.3). Change any application code. Access `.env` or print secrets.

## Your task

### 0. Branch setup

```powershell
# In prompts/ (on main):
cd D:\AppDev\mine_flow\prompts
git pull
# Add STEP-42 substep table row to STEP-index.md (In progress), commit, push:
# | STEP-42 | Staging Environment & Promotion Pipeline | Gemini 3.1 Pro High | In progress | ...
git add STEP-index.md
git commit -m "reserve(STEP-42): mark In progress"
git push

# Cut the step branch in both repos:
cd D:\AppDev\mine_flow\Code\mine-flow-app
git checkout -b step-0042-staging-pipeline

cd D:\AppDev\mine_flow\Code\mine-flow-docs
git checkout -b step-0042-staging-pipeline
```

### 1. Install Supabase CLI

```powershell
# Option A — Scoop (recommended on Windows):
scoop install supabase

# Option B — download the .msi from:
# https://supabase.com/docs/guides/local-development/cli/getting-started

# Verify:
supabase --version
```

Record the installed version.

### 2. Link the existing staging project

You need the **Project Reference ID** (not the URL):
- Supabase Dashboard → Project Settings → General → Reference ID (looks like: `abcdefghijkl`).

```bash
# From Code/mine-flow-app/:
supabase link --project-ref <STAGING_PROJECT_REF>
```

This generates `supabase/config.toml`. Inspect it and confirm it contains the project ref.

### 3. Apply migrations

```bash
# From Code/mine-flow-app/:
supabase db push
```

This applies all 5 migrations idempotently. Record the output — list the migrations shown as applied.

### 4. Seed synthetic data

```bash
# From Code/mine-flow-app/:
supabase db seed --file supabase/seed.sql
```

Record the output. Confirm no errors.

### 5. Verify staging reachable

In the Supabase dashboard, confirm:
- The `public.users` table has 3 rows (Alex Supervisor, Frank Foreman, Charlie Crew).
- The `public.zones` table has 2 rows.
- At least one row exists in `public.attendance_records`.

Record what you see (table names + row counts) as evidence.

### 6. Commit `config.toml`

```bash
# From Code/mine-flow-app/:
git add supabase/config.toml
git commit -m "feat(STEP-42.1): add supabase config.toml linking staging project"
git push -u origin step-0042-staging-pipeline
```

## Verification

- `supabase --version` → a valid version string.
- `supabase/config.toml` exists and contains `project_id` (the staging ref). No secrets.
- `supabase db push` output lists all 5 migrations as applied.
- `supabase db seed` exits 0 with no errors.
- Staging dashboard confirms seeded rows in `users` (3), `zones` (2), `attendance_records` (≥1).
- `git status --porcelain` in `mine-flow-app` shows only committed changes.
- `flutter analyze` still clean (no code changes made).

## Definition of done

- [ ] Supabase CLI installed and version recorded.
- [ ] `supabase/config.toml` committed on `step-0042-staging-pipeline`.
- [ ] All 5 migrations applied to staging; output recorded.
- [ ] `supabase/seed.sql` seeded; staging dashboard confirms rows in expected tables.
- [ ] Staging URL confirmed reachable (dashboard accessible).
- [ ] Worktrees clean; `flutter analyze` still passes.

## Next

After committing, start a fresh chat and run **substep 42.2**: `Upcoming Prompts/mine-flow-STEP-42.2-PROMPT.md`.
