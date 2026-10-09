# mine-flow — STEP-57.1 FINDINGS: Doc 06 Threat Review + ADR-0020 (Foreman Zone-Insert Policy)

> Substep of STEP-57 (Staging Zone Seed & Foreman Zone-Insert Policy). Branch: `step-0057-zone-insert-policy` in `Code/mine-flow-docs`.
> **Output contract:** This file is authored evidence for the owner gate at the end of 57.1. STEP-57.2 follows immediately after parent verification.

## Summary

STEP-57.1 (Doc 06 threat review + ADR for the owner-locked foreman zone-INSERT policy) is complete. The owner pre-answered all three design questions on 2026-10-10 (~02:20), recorded in `.step56-60-overnight-orchestration-state.md` §Owner decisions. This substep faithfully records those answers as an **Accepted** ADR (citing the owner decision block + date), writes the Doc 06 §7 threat review analyzing the approved design's residual risks honestly (not rubber-stamping), and adds RISK-0031 for the residual unmoderated-creation risk. **No code changes, no migrations, no SQL applied.** The policy + `created_by` column + trigger ship in STEP-57.2.

## Evidence

### 1. ADR number verification (non-duplicate)

- **Command:** `ls adr/ADR-*.md | sort` + `grep -oE '^\|[[:space:]]*ADR-[0-9]+' adr/README.md | grep -oE 'ADR-[0-9]+' | sort | uniq -d`
- **Result:** ADR-0001 through ADR-0019 exist on disk and in registry. ADR-0020 is the next free number. Duplicate scan: empty. ✅
- **New file:** `adr/ADR-0020-foreman-zone-insert-policy.md` — Status: Accepted, Date: 2026-10-10.
- **Registry row added:** `adr/README.md` line 66: `| ADR-0020 | Foreman Zone-Insert Policy (Site-Scoped, Server-Authoritative) | Accepted | 2026-10-10 |`
- check.sh item 5 (ADR registry matches files on disk): **PASS** (20 ADR(s)). ✅

### 2. Client-side zone-creation surface (verified at app HEAD)

Traced the full call chain from UI to sync enqueue at app HEAD (branch `step-0057-zone-insert-policy` is docs-only; app repo is read-only):

| Step | File | Line | What happens |
|------|------|------|--------------|
| 1 | `lib/features/daily_log/presentation/widgets/zone_picker.dart` | 121 | `CreatableCombobox.onCreateNew: (name) => _handleCreateZone(context, name)` |
| 2 | `lib/features/daily_log/presentation/widgets/zone_picker.dart` | 178–185 | `_handleCreateZone` calls `ZoneCubit.createZone(name: name, siteId: siteId)` |
| 3 | `lib/features/zone/presentation/bloc/zone_cubit.dart` | 89–106 | `createZone` builds `ZoneEntity` with UUIDv4 (client-generated), `siteId` (defaults to `defaultSiteId`), `name`, `category=null`, `description=null`, `createdAt`/`updatedAt=DateTime.now()`; no `created_by` field in `ZoneEntity` |
| 4 | `lib/features/zone/data/repositories/zone_repository_impl.dart` | 43–57 | `saveZone` writes to local Hive (`localDataSource.saveZone(model)`), then calls `syncQueueManager.enqueueMutation(entityType: 'zones', action: SyncAction.update, payloadJson: model.toJson(), timestamp: model.updatedAt ?? DateTime.now())` |
| 5 | `lib/core/offline/sync_queue_manager.dart` | 195 | No zone-specific sync registrar exists — the drain falls through to `_defaultSupabaseSync` |
| 6 | `lib/core/offline/sync_queue_manager.dart` | 225–262 | `_defaultSupabaseSync` does LWW check on `updated_at` (lines 240–250), then `await client.from(tableName).upsert(payload)` (line 262) — executes `INSERT .. ON CONFLICT DO UPDATE` |
| 7 | `lib/core/data/models/zone_model.dart` | 39–50 | `ZoneModel.toJson()` carries: `id`, `site_id`, `name`, `category` (if non-null), `description` (if non-null), `created_at`, `updated_at`, `deleted_at` — **no `created_by`** |
| 8 | `lib/core/constants/app_constants.dart` | 55 | `defaultSiteId = 'f47ac10b-58cc-4372-a567-0e02b2c3d479'` |

**Key finding:** The sync path uses `action: SyncAction.update` (not `create`) for new zones (`zone_repository_impl.dart:53`). This means the sync upsert is `INSERT .. ON CONFLICT DO UPDATE` — the foreman needs both INSERT and UPDATE RLS privileges on `zones`. This is why Q2 (UPDATE policy scoped to own rows) is required, not just Q1 (INSERT policy).

### 3. Existing zones policies (migration `20260718000002_rls_policies.sql`)

- `supervisor_zones_all` (line 58–60): `FOR ALL TO authenticated USING (current_user_role() = 'supervisor')` — permissive, supervisors have full access.
- `zones_read_active` (line 63–65): `FOR SELECT TO authenticated USING (deleted_at IS NULL AND current_user_role() IN ('foreman', 'crew'))` — read-only for foremen and crew.
- **No INSERT policy for foremen exists** — this is the RISK-0030 root cause.
- `current_user_role()` (lines 9–12): `SECURITY DEFINER` helper, reads from `public.users WHERE id = auth.uid() AND deleted_at IS NULL`. The proposed `current_user_site_id()` mirrors this exactly.
- **Schema** (`20260718000001_core_schema.sql:58–67`): `zones` table has `id`, `site_id`, `name`, `category`, `description`, `created_at`, `updated_at`, `deleted_at` — **no `created_by` column**.

### 4. check.sh gate

```
Throughstone check — /d/AppDev/mine_flow
1. Duplicate STEP numbers (prompts/STEP-index.md)     [PASS]
2. Duplicate ADR numbers (adr/README.md)              [PASS]
3. Statuses valid                                      [PASS]
4. Architecture docs carry Version / Status / Version Log [PASS]
5. ADR registry matches ADR files on disk              [PASS] (20 ADR(s))
6. Legacy local user profile fields                    [PASS]
7. Workspace-root hygiene (multi-repo only)            [WARN] (pre-existing)
8. Architecture-session template numbering             [PASS]
9. Conditional-session template contract               [PASS]
10. Registry YAML parses and has no control-byte/CR corruption
    [WARN] PyYAML unavailable for per-file check (pre-existing — owner authorized fix in STEP-58.1 Q1)
    [PASS] all 3 registry YAML file(s) parse and contain no control-byte/CR corruption

Summary: 0 fail(s), 4 warning(s) — RESULT: OK
```

### 5. YAML verification (manual, bypassing check.sh's PyYAML gap)

- **Command:** `python -c "import yaml; data = yaml.safe_load(open('registries/risks.yml')); ..."`
- **Result:** YAML parses. 31 risk rows (RISK-0001 through RISK-0031). RISK-0030 updated mitigation with approach-B acceptance + ADR-0020 ref. RISK-0031 added as `open` / `medium` / `security`. ✅

### 6. EOL verification

| File | Convention | Working-tree | Git-stored |
|------|-----------|-------------|------------|
| `architecture/06-security-threat-model.md` | CRLF | 76 CRLF, 0 lone CR | LF (autocrlf) |
| `adr/README.md` | CRLF | 66 CRLF, 0 lone CR | LF (autocrlf) |
| `adr/ADR-0020-*.md` | CRLF (matches sibling ADRs) | 1 CRLF per line, 0 lone CR | LF (autocrlf) |
| `registries/risks.yml` | bare-LF (git convention) | 855 CRLF, 0 lone CR, 0 bare LF | LF (autocrlf) |
| `Upcoming Prompts/mine-flow-STEP-57.1-FINDINGS.md` | bare-LF (matches sibling FINDINGS) | 0 CR | LF |

All files: 0 lone CR, 0 form-feed bytes. ✅ (Note: with `core.autocrlf=true`, git normalizes CRLF→LF on commit; the working-tree CRLF is the checkout artifact, not the stored convention.)

### 7. `git diff --check`

```
(empty output) — clean ✅
```
No whitespace errors, no CRLF-in-diff issues.

## Options considered (recorded in ADR-0020)

| # | Decision | Chosen | Reasoning | Alternatives |
|---|----------|--------|-----------|--------------|
| Q1 | INSERT WITH CHECK scope | **Site-scoped** (`site_id = current_user_site_id()`) | Multi-tenant readiness (Doc 04 §1); prevents cross-site zone injection | A. Role-only (rejected: leaks site isolation)<br>B. No WITH CHECK (rejected: no defense in depth) |
| Q2 | Upsert/UPDATE handling | **`created_by` column + server-side trigger + own-rows UPDATE** | Sync uses `INSERT..ON CONFLICT DO UPDATE` (zone_repository_impl.dart:53, sync_queue_manager.dart:262); foreman needs UPDATE on rows they create | A. Broad foreman UPDATE (rejected: can overwrite supervisor zones, loses audit)<br>B. Client INSERT-only sync (rejected: breaks shared upsert contract) |
| Q3 | Crew access | **Foreman-only** (crew stays read-only) | Crew has no operational need to create zones; all CreatableCombobox surfaces are foreman-facing | A. Crew create-with-moderation (deferred: out of MVP scope) |

## Three Q dispositions

| Q | Answer (owner-locked 2026-10-10, ~02:20) | Status |
|---|------------------------------------------|--------|
| Q1 | Site-scoped: new `current_user_site_id()` helper (SECURITY DEFINER) + policy `FOR INSERT TO authenticated WITH CHECK (current_user_role() = 'foreman' AND site_id = current_user_site_id())` | **Accepted** — recorded in ADR-0020 §Decision Q1 |
| Q2 | `created_by UUID` column + `BEFORE INSERT` trigger (`created_by = auth.uid()`, unspoofable) + foreman UPDATE policy scoped to own rows (`created_by = auth.uid()`) | **Accepted** — recorded in ADR-0020 §Decision Q2 |
| Q3 | Foreman-only; crew stays read-only | **Accepted** — recorded in ADR-0020 §Decision Q3 |

All three were answered in `.step56-60-overnight-orchestration-state.md` §Owner decisions (lines 10–19). The ADR cites this decision block as the acceptance authority.

## Parked-owner-gate status

The original 57.1 prompt described a "park-gate" where the ADR would park for owner approval before 57.2. The overnight orchestration state (§Owner decisions, 2026-10-10 ~02:20, Q5) **superseded** this: "run STEP-57 to completion overnight — ADR records these answers (may be written Accepted citing this decision block)." The owner explicitly authorized Q5 (run to completion) and Q4 (staging apply). Therefore:

- The ADR is written **Accepted** (not Proposed) — the owner is the authority and pre-accepted on 2026-10-10.
- This substep does NOT stop/park for owner review before 57.2.
- 57.2 follows immediately after parent verification.

## Definition of done

- [x] Doc 06 threat-review section (§7) + v-log bump to v0.4.0
- [x] ADR-0020 written as **Accepted** (owner pre-answered 2026-10-10; cites the decision block)
- [x] ADR-0020 row added to `adr/README.md` registry
- [x] RISK-0030 mitigation updated (approach A delivered + approach B accepted/ADR-0020 cited); revisit_trigger updated
- [x] RISK-0031 added (residual: foreman-created zones unmoderated at creation)
- [x] FINDINGS complete
- [x] No migration/SQL applied; no app changes
- [x] Records state is owner-locked (not executor-inferred)
- [x] check.sh: 0 fail(s)
- [x] `git diff --check`: clean
- [x] Duplicate ADR scan: clean (ADR-0020 is unique)
- [x] EOL preserved per file convention
- [x] Not pushed (per task scope)

## Files created/modified

| File | Action | EOL |
|------|--------|-----|
| `adr/ADR-0020-foreman-zone-insert-policy.md` | Created (new) | CRLF (matches sibling ADRs) |
| `adr/README.md` | Added ADR-0020 registry row | CRLF (preserved) |
| `architecture/06-security-threat-model.md` | Added §7 + v-log bump (v0.3.0→v0.4.0) | CRLF (preserved) |
| `registries/risks.yml` | Updated RISK-0030 mitigation/revisit_trigger/refs; added RISK-0031 | LF (preserved) |
| `Upcoming Prompts/mine-flow-STEP-57.1-FINDINGS.md` | Created (new) | LF (matches sibling FINDINGS) |

## Notes / caveats

- The owner's orchestration state file states the ADR "records these answers" and "may be written Accepted citing this decision block" — this subagent followed that instruction rather than the prompt's default "park-gate" (Proposed). The 57.1 prompt §3 explicitly says to write the ADR as Accepted citing the owner decision block.
- RISK-0031's `category: security` and `severity: medium` are a project judgment: unmoderated zone creation is bounded by the 100-user MVP ceiling and supervisor FOR ALL visibility, but could grow into data-quality/audit concerns at scale.
- The `current_user_site_id()` helper and `created_by` column do NOT exist at HEAD — they are proposed in ADR-0020 and ship in STEP-57.2. This substep is design-only.
- PyYAML was unavailable inside check.sh's subshell (wrong Python interpreter), producing pre-existing WARN-level messages. The owner authorized installing PyYAML in STEP-58.1 (Q1). I verified YAML validity manually using the interpreter that has PyYAML installed. No control-byte or CR corruption exists in any registry file.
