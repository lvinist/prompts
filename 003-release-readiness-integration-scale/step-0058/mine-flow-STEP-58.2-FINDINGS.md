# STEP-58.2 FINDINGS: Risk-Register Row-by-Row Sweep

**Date:** 2026-10-10
**Branch:** `step-0058-doc-drift-registry-sweep`
**Commit:** `560ed48` (sweep HEAD)
**App repo HEAD verified:** `fc4b984` (`Code/mine-flow-app`, branch `step-0057-zone-insert-policy`)

## Row Counts

| Metric | Count |
|---|---|
| Rows swept | 31 (RISK-0001..0031) |
| Flipped to closed | 0 |
| Flipped to other status | 1 (RISK-0026: open → monitoring) |
| Kept open/monitoring, evidence current | 24 |
| Kept open with true-up | 2 (RISK-0025, RISK-0030) |
| Parked for owner | 1 (RISK-0026 — data-review criterion unmet) |

## Per-Row Verdicts

### Flipped

| Row | Before | After | Reason |
|---|---|---|---|
| RISK-0026 | open | monitoring | Validation + fallback removal + regression tests met at HEAD `dea5c58` (in `fc4b984` history); data-review criterion unmet (requires staging DB access). Evidence trued up with STEP-55.4 FINDINGS reference. |

### True-up Only (no status change)

| Row | Status | Evidence trued up |
|---|---|---|
| RISK-0025 | open | Verified migration `20261004000001` + trigger `guard_users_self_update` present at HEAD; staging verification confirmed; production remains blocked per owner. |
| RISK-0030 | open | Cherry-picked STEP-57.0/57.2/57.3 evidence into risks.yml: Approach A (staging seed) + Approach B (ADR-0020 policy, staging apply, role-matrix, tests) all verified at HEAD `fc4b984`. CI gate parked per owner Q5. |
| RISK-0031 | open | **Added to register** (was referenced in Doc 06 §7 and STEP-57.4 FINDINGS but missing from risks.yml). Residual: foreman-created zones unmoderated at creation. |

### No Change (criteria not met, evidence current)

RISK-0001, RISK-0004, RISK-0005, RISK-0007, RISK-0008, RISK-0009, RISK-0010, RISK-0011,
RISK-0012, RISK-0013, RISK-0014, RISK-0015, RISK-0016, RISK-0017, RISK-0018, RISK-0019,
RISK-0020, RISK-0021, RISK-0023, RISK-0024, RISK-0027, RISK-0028, RISK-0029.

RISK-0002, RISK-0003, RISK-0006, RISK-0022 — already closed, evidence unchanged.

## Key Evidence

### RISK-0026 (benchmark projection — flipped to monitoring)
- App HEAD `fc4b984` includes commit `dea5c58` (`fix(55.4): localize CRS recovery string, add projection rejection + cold-route tests`) — verified via `git merge-base --is-ancestor dea5c58 fc4b984` (exit 0).
- `benchmark_bloc.dart:607-610`: `_onSubmitBenchmark` blocks null computed lat/lon with `kBenchmarkProjectionFailureMessage`.
- `benchmark_bloc.dart:363-390`: `_computeLatLon` rejects Infinity/NaN/out-of-range → returns null.
- No fallback to 0.0, 0.0 in persistence path (grep confirmed).
- Tests: `crs_utils_test.dart` (9 tests) + `benchmark_bloc_test.dart` (rejection tests) — 78/78 passed per STEP-55.4 FINDINGS.
- **Data review NOT evidenced:** No SQL query, migration, or script auditing existing benchmark records for unintended 0.0, 0.0 values was found on disk. `seed.sql` explicitly notes no benchmark seed rows are included (so seeding can't produce sentinel values). This criterion requires live staging/production DB access.

### RISK-0025 (privilege escalation — stays open)
- Migration `20261004000001_step_55_user_profile_permissions.sql` present at HEAD.
- `guard_users_self_update` trigger + allow-list (name, phone, emergency_contact_name, emergency_contact_phone) verified.
- `reports/2026-10-08-step-0055-follow-up-correction.md` confirms production remains blocked.

### RISK-0030 (foreman zones RLS — stays open)
- Cherry-picked STEP-57 evidence from commits `3e6b9ea`, `f202da9`, `33eb300` (on `step-0057-zone-insert-policy` branch).
- Migration `20261010000001_step_57_foreman_zones_insert.sql` at app commit `fc4b984`.
- Staging apply + live role-matrix verified (foreman INSERT 201, supervisor-row deny, crew/anon 42501).
- RLS tests +2, database.ts regenerated, contract guard exit 0.
- daily_log journey GREEN locally on Web + Android at `fc4b984`.
- CI gate PARKED per owner Q5 — stays open until CI passes at merged head.

### RISK-0031 (added)
- Referenced in Doc 06 §7 (`architecture/06-security-threat-model.md`) and STEP-57.1/57.4 FINDINGS.
- Was NOT present in risks.yml on sweep branch — added via cherry-pick of `f202da9`.
- Residual: foreman-created zones have no name-category uniqueness or moderation gate.

## PyYAML

- Installed: `pip install pyyaml` → PyYAML 6.0.3 available in the miniconda environment.
- `check.sh` registry YAML check: **PASS** (all 3 registry YAML files parse, no control-byte/CR corruption).

## Sweep Policy Compliance

- RISK-0026: Three of four close criteria met on disk; data-review criterion not evidenced → **parked** for owner (judgment call).
- RISK-0030: CI criterion explicitly parked per owner Q5 → status stays open, evidence trued up.
- No row closed without its own close criteria verifiably met on disk.
- No app code modified (read-only grep + git log only).

## Owner-Parked List

1. **RISK-0026 data review:** Audit existing benchmark records for unintended 0.0, 0.0 sentinel values — requires staging DB query access.
2. **RISK-0030 CI gate:** Daily_log Android journey must pass in CI at merged head (owner Q5).
3. **RISK-0005 fl_chart:** Pre-flight review of any future fl_chart major version bump (no bump pending).
4. **RISK-0009 forui:** Consider dropping workarounds when stable Flutter >=3.48 ships with PR #191587 (not yet shipped).
