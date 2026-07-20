# mine-flow — STEP-3.1: Supabase SQL Schema Migrations & RLS Policies

> **How to run:** Tell your agent *"run substep 3.1"* (or *"read and run this file"*).

## Context
This is the first substep of [mine-flow-STEP-3-PLAN.md](file:///d:/AppDev/mine_flow/prompts/001-mvp/step-0003/mine-flow-STEP-3-PLAN.md).
In this substep, we establish the core PostgreSQL database schema for Supabase, configure Row-Level Security (RLS) policies for user authorization roles (`supervisor`, `foreman`, `crew`), and add audit logging triggers.

## Read these first
- [overview.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/overview.md) — Project brief
- [04-data-model.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/04-data-model.md) — Data model, entities, UUIDs, `site_id`, retention
- [16-identity-auth.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/16-identity-auth.md) — Identity provider, RBAC roles, multi-tenancy
- [06-security-threat-model.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/06-security-threat-model.md) — Security posture & RLS enforcement rules
- [README.md](file:///d:/AppDev/mine_flow/Code/mine-flow-app/README.md) — Target app repository details

## Scope
- **In Scope:**
  - `supabase/migrations/20260718000001_core_schema.sql`: Tables for `users`, `zones`, `attendance_records`, `equipment_checks`, `daily_logs`, `cut_fill_records`, `land_clearing_records`, `inventory_items`, and `geospatial_files`.
  - Primary key `id` (UUID), foreign keys, timestamps (`created_at`, `updated_at`), soft delete (`deleted_at`), and `site_id` multi-tenancy column.
  - `supabase/migrations/20260718000002_rls_policies.sql`: Row-Level Security policies enforcing role privileges (`supervisor` full access, `foreman` logging access, `crew` self-attendance access).
  - Seed SQL script (`supabase/seed.sql`) for dev testing (default site, supervisor/foreman accounts).
- **Out of Scope:**
  - Client-side Dart models (handled in Substep 3.3).
  - Supabase Edge Functions (handled in Substep 3.2).

## Your task
1. Create `supabase/migrations/20260718000001_core_schema.sql` in `d:/AppDev/mine_flow/Code/mine-flow-app/`:
   - Enums: `user_role` ('supervisor', 'foreman', 'crew'), `attendance_status` ('present', 'absent', 'sick', 'leave'), `equipment_type` ('gnss', 'total_station', 'drone'), `log_status` ('draft', 'submitted', 'approved').
   - Tables with standard fields (`id UUID PRIMARY KEY DEFAULT gen_random_uuid()`, `site_id UUID NOT NULL DEFAULT '00000000-0000-0000-0000-000000000001'`, `created_at`, `updated_at`, `deleted_at`).
   - Audit trail trigger function to update `updated_at` on modification.
2. Create `supabase/migrations/20260718000002_rls_policies.sql`:
   - Enable RLS on all operational tables (`ALTER TABLE ... ENABLE ROW LEVEL SECURITY;`).
   - Helper function `auth.user_role()` returning the logged-in user's role from `public.users`.
   - Create RLS policies for SELECT, INSERT, UPDATE, DELETE for each role.
3. Create `supabase/seed.sql` with mock initial data for testing.

## Verification
- Validate syntax of SQL migration files.
- Check that all 9 entities from [04-data-model.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/04-data-model.md) are fully represented with correct UUID data types and foreign key relationships.

## Keeping the docs true
- If schema adjustments are required during SQL drafting, update [04-data-model.md](file:///d:/AppDev/mine_flow/Code/mine-flow-docs/architecture/04-data-model.md) Version Log accordingly.

## Definition of done
- [x] `supabase/migrations/20260718000001_core_schema.sql` written with all 9 core entities and foreign key constraints.
- [x] `supabase/migrations/20260718000002_rls_policies.sql` written with RLS enabled on all tables and policies defined for `supervisor`, `foreman`, and `crew`.
- [x] `supabase/seed.sql` created with initial seed data.

## Next
Update status in STEP-3 PLAN, then tell the user to proceed to *"run substep 3.2"* in a fresh chat.
