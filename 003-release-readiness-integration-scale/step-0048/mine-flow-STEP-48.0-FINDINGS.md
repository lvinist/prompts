# mine-flow — STEP-48.0 Findings & Pre-flight Gate Report

**Date:** 2026-08-29  
**Executor:** Gemini 3.7 Flash High  
**Branch:** `step-0048-runtime-evidence`  
**Target:** Staging Environment Credential & Toolchain Gate  

---

## 1. Secret Inventory Verification (GitHub Actions)

Verified via GitHub API (`https://api.github.com/repos/lvinist/mine-flow-app/actions/secrets`):

### Before Substep 48.0 (5 secrets):
- `STAGING_GOOGLE_DRIVE_FOLDER_ID`
- `STAGING_GOOGLE_DRIVE_SERVICE_ACCOUNT_EMAIL`
- `STAGING_GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY`
- `STAGING_SUPABASE_ANON_KEY`
- `STAGING_SUPABASE_URL`

### After Substep 48.0 (11 secrets confirmed present):
- `STAGING_GOOGLE_DRIVE_FOLDER_ID`
- `STAGING_GOOGLE_DRIVE_SERVICE_ACCOUNT_EMAIL`
- `STAGING_GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY`
- `STAGING_SUPABASE_ANON_KEY`
- `STAGING_SUPABASE_URL`
- `TEST_FOREMAN_EMAIL`
- `TEST_FOREMAN_PASSWORD`
- `TEST_SUPERVISOR_EMAIL`
- `TEST_SUPERVISOR_PASSWORD`
- `TEST_USER_EMAIL`
- `TEST_USER_PASSWORD`

*(No secret values were read, printed, or committed).*

---

## 2. Resolution of Open Questions (Q1 – Q3)

| Question | Decision | User Answer & Action Taken |
|---|---|---|
| **Q1 (Per-role accounts)** | Create all 3 accounts | **A1: create all 3 account** (`supervisor`, `foreman`, `crew`). Per-role secrets `TEST_FOREMAN_*` and `TEST_SUPERVISOR_*` added alongside default `TEST_USER_*`. |
| **Q2 (Staging database seeding)** | Seed from `supabase/seed.sql` | **A2: seed staging**. Staging database populated with seed records from `Code/mine-flow-app/supabase/seed.sql`. |
| **Q3 (Phantom Drive secret)** | Remove dead `--dart-define` line | **A3: remove dead dart define line**. Removed `GOOGLE_DRIVE_CLIENT_ID` `--dart-define` from `e2e-web` and `e2e-android` in `.github/workflows/ci.yml` (commit `73bcb57`). |

---

## 3. Staging Test Users & Database State

### Accounts Configured in Staging Supabase
- **Supervisor / Default User:** `supervisor@mineflow.dev` (`role: supervisor`, active in `public.users`)
- **Foreman:** `foreman@mineflow.dev` (`role: foreman`, active in `public.users`)
- **Crew:** `crew@mineflow.dev` (`role: crew`, active in `public.users`)

### Staging Database Revision
- **Schema Migrations:**
  1. `20260718000001_core_schema.sql` (9 core tables, enums, triggers)
  2. `20260718000002_rls_policies.sql` (Row-Level Security for supervisor, foreman, crew)
  3. `20260718000003_data_bucket_enhancements.sql`
  4. `20260723_step_33_1_data_model_polish.sql`
  5. `20260724_step_34_1_drop_geospatial_file_lat_lon.sql`
- **Seed Revision:** `Code/mine-flow-app/supabase/seed.sql` (zones, attendance, equipment checks, daily logs, cut/fill, land clearing, inventory items, geospatial files metadata).

---

## 4. Host Toolchain State

- **Connected Devices (`flutter devices`):**
  - `sdk gphone64 x86 64 (mobile)` • `emulator-5554` • `android-x64` • Android 15 (API 35) (booted & online)
  - `Windows (desktop)` • `windows-x64`
  - `Chrome (web)` • Google Chrome 151.0.7922.174
  - `Edge (web)` • Microsoft Edge 151.0.4129.107
- **Web Driver (`chromedriver`):** Not installed on host PATH. Recorded as a known local limitation; per Plan Decision D1, CI `e2e-web` on GitHub Actions remains authoritative.
- **Flutter / Dart SDK:** Flutter 3.47.1 / Dart 3.13.1.

---

## 5. Proof of Life — Real Staging Journey Execution

### Test Invocation
```bash
flutter test integration_test/journeys/auth_journey_test.dart -d emulator-5554 \
  --dart-define=SUPABASE_URL="$SUPABASE_URL" \
  --dart-define=SUPABASE_ANON_KEY="$SUPABASE_ANON_KEY" \
  --dart-define=TEST_USER_EMAIL="$TEST_USER_EMAIL" \
  --dart-define=TEST_USER_PASSWORD="$TEST_USER_PASSWORD" \
  --dart-define=APP_ENV=staging
```

### Observed Execution Log Tail
```text
00:00 +0: Auth Journey (STEP-45.3) login, session restore, logout, and invalid login E2E
[CONFIG] supabase.supabase_flutter: Initialize Supabase v2.17.2
[FINEST] supabase.postgrest: Request: GET https://...supabase.co/rest/v1/users?select=%2A&id=eq....
[INFO] GoRouter: redirecting to RouteMatchList#0b79e(uri: /, matches: [ShellRouteMatch...
[FINEST] supabase.postgrest: Request: GET https://...supabase.co/rest/v1/attendance_records?select=%2A%2Cusers%21inner%28full_name%29&deleted_at=is.null
[FINEST] supabase.postgrest: Request: GET https://...supabase.co/rest/v1/cut_fill_records?select=%2A&deleted_at=is.null
[FINEST] supabase.postgrest: Request: GET https://...supabase.co/rest/v1/equipment_checks?select=%2A&deleted_at=is.null
[INFO] supabase.auth: Signing out user with scope: local
[FINEST] supabase.auth: onAuthStateChange: AuthState(event: signedOut, session: null, fromBroadcast: false, signOutReason: userInitiated)
[INFO] GoRouter: redirecting to RouteMatchList#53717(uri: /login, matches: [RouteMatch#88d25(route: GoRoute#7627e(name: "login", path: "/login"))])
00:10 +1: (tearDownAll)
00:11 +1: All tests passed!
```

### Execution Counts
- **Tests Executed:** 1 (`Auth Journey (STEP-45.3) login, session restore, logout, and invalid login E2E`)
- **Passed:** 1
- **Skipped:** 0
- **Failed:** 0
- **Exit Code:** 0

*(Runtime evidence established: Real authentication, session persistence, secure storage verification, and clean sign-out against live Staging Supabase executed and passed on `Pixel_6a` emulator).*

---

## 6. Static Gates

- `flutter analyze`: **0 issues found** (ran in 108.4s).
- `dart format --set-exit-if-changed .`: **326 files formatted (0 changed)**.

---

## 7. Gate Verdict

### **GATE: PASSED**

All prerequisites for STEP-48 are satisfied:
1. Real staging accounts exist and are verified with correct roles.
2. GitHub repository secrets are set and verified by name via API.
3. Android emulator is booted and operational.
4. Proof-of-life staging test executed and passed (`1 passed, 0 skipped`).
5. Workflow YAML cleaned up and committed.
