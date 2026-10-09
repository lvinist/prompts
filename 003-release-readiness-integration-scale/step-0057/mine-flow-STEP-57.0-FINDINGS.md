# mine-flow — STEP-57.0 FINDINGS: RISK-0030 Reconciliation & Approach-A Verification

> Substep of STEP-57 (Staging Zone Seed & Foreman Zone-Insert Policy). Branch: `step-0057-zone-insert-policy` in `Code/mine-flow-docs`.

## Summary

Approach A (idempotent staging zone seed) was delivered in a prior session at app commit `be682b7` (master). STEP-57.0 re-derives the on-disk evidence from git, live-verifies the seeded row on staging via authenticated REST, and reconciles `registries/risks.yml` RISK-0030 to record A-delivered while keeping status `open` (approach B pending).

## 1. On-disk verification (migration at be682b7)

**Command:** `git -C Code/mine-flow-app log --oneline -- supabase/migrations/20261008000001_step_56_staging_zone_seed.sql`

**Result:**
```
be682b7 feat(56): idempotent staging zone seed for the daily-log E2E round-trip (RISK-0030)
```

**Migration content** (`git show be682b7:supabase/migrations/20261008000001_step_56_staging_zone_seed.sql`):
- File path: `Code/mine-flow-app/supabase/migrations/20261008000001_step_56_staging_zone_seed.sql`
- Data-only (no DDL), idempotent: `ON CONFLICT (id) DO NOTHING`
- Fixed UUID: `6e60b2e2-0000-4000-8000-000000005656`
- Site UUID: `f47ac10b-58cc-4372-a567-0e02b2c3d479`
- Name: `Pit Alpha`, category: `extraction`

**Cross-check with app constants** (`lib/core/constants/app_constants.dart`):
```
Line 55: const String defaultSiteId = 'f47ac10b-58cc-4372-a567-0e02b2c3d479';
```
The migration's `site_id` column matches `defaultSiteId` exactly. ✅

## 2. Live staging probe (REST, via .env credentials)

**Method:** Authenticated as `TEST_USER_EMAIL` against Supabase Auth (`POST /auth/v1/token?grant_type=password`), then `GET /rest/v1/zones?id=eq.6e60b2e2-0000-4000-8000-000000005656`. Credentials loaded from `.env` into shell variables; no secrets printed.

**Probe command (values redacted):**
```
curl -s -m 15 "https://<project>.supabase.co/rest/v1/zones?id=eq.6e60b2e2-0000-4000-8000-000000005656" \
  -H "apikey: <ANON_KEY>" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Accept: application/json"
```

**Response (only id + name + created_at; no PII):**
```json
[
  {
    "id": "6e60b2e2-0000-4000-8000-000000005656",
    "site_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "name": "Pit Alpha",
    "category": "extraction",
    "description": "Seeded E2E zone (STEP-56): stable FK target for daily-log staging round-trip",
    "created_at": "2026-10-07T21:54:53.52364+00:00",
    "updated_at": "2026-10-07T21:54:53.52364+00:00",
    "deleted_at": null
  }
]
```

**Live probe verdict:** Row present. ✅ The seed is applied on staging. `created_at` = `2026-10-07T21:54:53.52364+00:00` (UTC).

## 3. RISK-0030 patch

**Command:** `git -C Code/mine-flow-docs diff --stat registries/risks.yml`

**Diff:**
```
registries/risks.yml | 15 +++++++++-----
 1 file changed, 10 insertions(+), 5 deletions(-)
```

**Changes:**
- `mitigation`: Updated to record "Approach A delivered" with migration filename, commit `be682b7`, fixed UUID, site_id, staging live-verified date (2026-10-10), and row `created_at`. Approach B decision remains pending.
- `status`: Stays `open` (Approach B not yet implemented). ✅
- EOL audit (parent-corrected 2026-10-10): risks.yml is a **bare-LF file by
  convention** (parent `3e6b9ea^`: 809 LF / 0 CRLF → `3e6b9ea`: 814 LF / 0 CRLF; the
  5 new lines are LF-terminated, matching). The original line here claimed "814 CRLF"
  — a mislabel of the convention; **no EOL churn was introduced** (parent-verified via
  blob byte counts). ✅
- YAML parses via `yaml.safe_load`: 30 risk rows, RISK-0030 status `open`. ✅

**Verification results:**
- `git diff --check`: clean ✅
- check.sh: 0 fail(s), 1 warning (pre-existing workspace-root hygiene) ✅
- YAML parses ✅
- EOL convention preserved (bare-LF file stayed bare-LF; parent-verified) ✅

## 4. Commit / branch

- **Branch:** `step-0057-zone-insert-policy` (created from `main`, which was clean at step-0056-phase3-release-notes — the concurrent session's untracked working-tree changes were NOT staged).
- **Commit SHA:** `3e6b9ea`
- **Files staged:** `registries/risks.yml` only (no app code, no migrations, no STEP-index.md)
- **Not pushed:** per task scope. ✅

## 5. Definition of done

- [x] risks.yml updated with A-delivered evidence; RISK-0030 still open (B pending)
- [x] FINDINGS carries disk + live evidence; no values/secrets printed
- [x] Committed on `step-0057-zone-insert-policy` (docs repo), not pushed

## Evidence artifacts

| Evidence | Source |
|---|---|
| Migration at be682b7 | `git show be682b7:supabase/migrations/20261008000001_step_56_staging_zone_seed.sql` |
| defaultSiteId cross-check | `Code/mine-flow-app/lib/core/constants/app_constants.dart:55` |
| Staging row live probe | Authenticated REST GET `zones?id=eq.6e60b2e2-…` |
| RISK-0030 mitigation patch | `git diff registries/risks.yml` (commit `3e6b9ea`) |
| check.sh gate | `scripts/check.sh` → 0 fail(s) |
