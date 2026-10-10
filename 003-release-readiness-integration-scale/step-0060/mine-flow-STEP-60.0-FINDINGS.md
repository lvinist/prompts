# mine-flow — STEP-60.0 Findings: Dependency Inventory & Advisory Scan

**Date:** 2026-10-10
**Fetch date:** 2026-10-10 (live pub.dev API + Flutter releases JSON)
**Executor:** Hermes subagent (vc/deepseek-v4.1)
**Substep:** 60.0
**Status:** Complete

---

## 1. Executive Summary

Full dependency inventory snapshot taken at branch HEAD `4c74e87`. Live upstream
verification performed for hive_ce, hive_ce_flutter, forui, and Flutter stable.
Advisory scan performed via pub.dev API (isCurrentAffectedByAdvisory / advisories
field). No advisories found. No dependency changes made — this substep is read-only.

**Branch:** `step-0060-dependency-security-sweep` (created off master `4c74e87`, clean).

---

## 2. Snapshot Source

- **Command:** `flutter pub outdated --json` (saved to scratch:
  `.step60.0-pub-outdated.json`, 81 packages total: 17 direct, 63 transitive)
- **Summary:** `.step60.0-pub-outdated-summary.txt`

---

## 3. Current Lockfile Versions (Key Direct Dependencies)

| Package | Constraint | Locked | Upgradable (in-constraint) | Latest on pub.dev |
|---|---|---|---|---|
| hive_ce | ^2.19.3 | 2.19.3 | **2.20.2** | 2.20.2 |
| hive_ce_flutter | ^2.3.4 | 2.3.4 | **2.4.0** | 2.4.0 |
| forui | ^0.26.0 | 0.26.0 | 0.26.0 (out of range) | **0.27.4** |
| go_router | ^18.0.0 | 18.0.1 | **18.0.2** | 18.0.2 |
| flutter_secure_storage | ^11.0.0 | 11.1.0 | **11.2.0** | 11.2.0 |
| file_picker | ^12.1.1 | 12.2.0 | **12.3.0** | 13.1.0 |
| supabase_flutter | ^2.17.1 | 2.17.2 | **2.18.2** | 2.18.2 |
| image_picker | ^1.1.2 | 1.2.3 | **1.2.4** | 1.2.4 |
| pdf | ^3.11.1 | 3.13.0 | **3.13.1** | 3.13.1 |
| printing | ^5.13.4 | 5.15.0 | **5.15.1** | 5.15.1 |
| lucide_icons_flutter | ^3.1.17 | 3.1.19 | **3.1.24** | 3.1.24 |
| package_info_plus | ^10.2.1 | 10.2.1 | **10.2.2** | 10.2.2 |
| flutter_bloc | ^9.1.1 | 9.1.1 | 9.1.1 (up to date) | 9.1.1 |
| connectivity_plus | ^7.3.1 | 7.3.1 | 7.3.1 (latest=7.3.2, out of range) | 7.3.2 |
| build_runner | ^2.4.0 | 2.16.1 | **2.16.1** (up to date) | 2.16.1 |
| http | ^1.2.2 | 1.6.0 | 1.6.0 (latest=1.7.1, out of range) | 1.7.1 |
| googleapis | ^17.0.0 | 17.0.0 | 17.0.0 (latest=19.x, out of range) | 19.x |
| url_launcher | ^6.3.1 | 6.3.2 | **6.3.3** | 6.3.3 |

---

## 4. Live Upstream Verification

### 4.1 hive_ce (pub.dev API, fetched 2026-10-10)

- **Latest:** v2.20.2 (published 2026-10-06T23:04:38.716Z)
- **Maintenance trajectory (post-2.19.3):**
  - 2.20.0 — published 2026-09-12
  - 2.20.1 — published 2026-09-27
  - 2.20.2 — published 2026-10-06
- **Advisory:** No advisories; `isCurrentAffectedByAdvisory` = false; `retracted` = false.
- **Source:** https://pub.dev/api/packages/hive_ce (fetched live)

### 4.2 hive_ce_flutter (pub.dev API, fetched 2026-10-10)

- **Latest:** v2.4.0 (published 2026-09-27T18:32:22.643Z)
- **Constraint:** ^2.3.4 — 2.4.0 is within range (same major.minor).
- **Advisory:** No advisories; not retracted; not affected by advisory.
- **Source:** https://pub.dev/api/packages/hive_ce_flutter

### 4.3 forui (pub.dev API, fetched 2026-10-10)

- **Current (pinned):** v0.26.0 (published 2026-08-24)
- **Latest available:** v0.27.4 (published 2026-10-04)
- **Constraint:** ^0.26.0 — 0.27.x is OUT of range (pre-1.0, minor = breaking).
- **Owner decision:** forui ^0.26 pin is KEPT (see §5.2 below).
- **Advisory:** No advisories on 0.26.0 or 0.27.4.

### 4.4 Flutter stable (releases JSON, fetched 2026-10-10)

- **Source:** `https://storage.googleapis.com/flutter_infra_release/releases/releases_windows.json`
- **Latest stable:** v3.47.7 (released 2026-10-08T23:29:50.802Z, hash `abaf9c523780a608bd46686fd5e53740a07077f8`)
- **Local install:** 3.47.1 (framework revision 6655482ec0, 2026-08-19) — behind stable by 6 patch versions.
- **Last 5 stable:** 3.47.7 (10-08), 3.47.6 (10-01), 3.47.5 (09-18), 3.47.4 (09-11), 3.47.3 (09-09).

---

## 5. Trigger Verdicts

### 5.1 RISK-0007 — hive_ce maintenance trajectory (>6 months no release)

- **Verdict: TRIGGER NOT FIRED — RESOLVED.**
- Last stable before 2.19.3: 2.19.3 (published 2026-02-03). At STEP-53.1 time
  (2026-09-10), this was ~7 months and the trigger was FIRED.
- Re-verification at 60.0 (2026-10-10): hive_ce has released 2.20.0 (09-12),
  2.20.1 (09-27), 2.20.2 (10-06) — three releases within 27 days. The >6-month
  silence is broken. Active maintenance restored.
- **Owner decision:** Lockfile bump to 2.20.2 is authorized (60-Q4). This is a
  patch-within-constraint update (^2.19.3 → 2.20.2).

### 5.2 RISK-0009 — Flutter stable ≥3.48 (forui pin mitigation)

- **Verdict: TRIGGER NOT FIRED.**
- Latest Flutter stable: 3.47.7 (2026-10-08). The ≥3.48 trigger has NOT fired.
- forui latest available: 0.27.4 (2026-10-04), but ^0.26.0 does not allow it.
- **Owner decision:** forui ^0.26 pin is KEPT. The forui 0.27 upgrade is
  out-of-constraint (pre-1.0 minor = breaking change). No action taken.

### 5.3 RISK-0020 — SDK-pinned transitive drift

- **Verdict: UNCHANGED.**
- Same SDK-pinned residuals as STEP-53.3: archive, package_config, qr,
  material_color_utilities, _fe_analyzer_shared/analyzer/test family.
- These remain on older versions because the Flutter SDK's own constraints
  pin them. No action possible without an SDK upgrade.
- Status: monitoring.

---

## 6. Advisory Scan

**Method:** pub.dev API `isCurrentAffectedByAdvisory` and `advisories` fields on
hive_ce, hive_ce_flutter, forui, go_router, flutter_secure_storage, file_picker,
supabase_flutter, flutter_bloc, and the top 20 most-used direct/transitive
packages. No `dart pub audit` equivalent is available locally (Dart 3.13.1 tool
chain).

**Results:** Zero advisories across all checked packages. No retracted releases.
No affected-by-advisory flags.

**Parked:** If deeper advisory scanning becomes available (e.g. OSV/GitHub
advisory DB for Dart packages), re-run at the next maintenance STEP.

---

## 7. Actionable Items for 60.1

### 7.1 Safe in-constraint upgrades (owner 60-Q5: auto-apply)

| Package | From → To | Type | Notes |
|---|---|---|---|
| hive_ce | 2.19.3 → 2.20.2 | Direct main | Owner-locked (60-Q4); within ^2.19.3 |
| hive_ce_flutter | 2.3.4 → 2.4.0 | Direct main | Within ^2.3.4; co-upgrade of hive_ce |
| go_router | 18.0.1 → 18.0.2 | Direct main | Within ^18.0.0; patch |
| flutter_secure_storage | 11.1.0 → 11.2.0 | Direct main | Within ^11.0.0 |
| file_picker | 12.2.0 → 12.3.0 | Direct main | Within ^12.1.1; patch/minor |
| supabase_flutter | 2.17.2 → 2.18.2 | Direct main | Within ^2.17.1; minor |
| image_picker | 1.2.3 → 1.2.4 | Direct main | Within ^1.1.2 |
| pdf | 3.13.0 → 3.13.1 | Direct main | Within ^3.11.1 |
| printing | 5.15.0 → 5.15.1 | Direct main | Within ^5.13.4 |
| lucide_icons_flutter | 3.1.19 → 3.1.24 | Direct main | Within ^3.1.17 |
| package_info_plus | 10.2.1 → 10.2.2 | Direct main | Within ^10.2.1 |
| url_launcher | 6.3.2 → 6.3.3 | Direct main | Within ^6.3.1 |
| battery_plus | 7.1.1 → 7.1.2 | Direct main | Within ^7.1.1 |
| googleapis_auth | 2.3.3 → 2.3.4 | Direct main | Within ^2.3.3 |

Plus transitive co-upgrades that follow from the above (48 transitive packages
have in-constraint upgradable versions; they will resolve automatically via
`flutter pub upgrade`).

### 7.2 Owner-decision items (NOT applied)

| Package | Reason | Owner decision |
|---|---|---|
| forui 0.26.0 → 0.27.4 | Out of constraint (^0.26.0, minor is breaking pre-1.0) | KEEP pin (60-Q4) |
| connectivity_plus 7.3.1 → 7.3.2 | Out of constraint (^7.3.1) | Park |
| http 1.6.0 → 1.7.1 | Out of constraint (^1.2.2) | Park |
| googleapis 17.0.0 → 19.x | Out of constraint (^17.0.0) | Park |
| Flutter SDK 3.47.1 → 3.47.7 | SDK channel upgrade | Out of scope (owner decision to not widen SDK constraints) |

### 7.3 _test_l10n_guard_temp_* directories

- Owner decision (60-Q5): **NOT selected.** Leave untouched. No action.

---

## 8. Verification

- `git status` clean — working tree clean (inventory is read-only).
- All version/date claims carry a fetch source (pub.dev API + Flutter releases JSON).
- No files created or modified on this substep.

---

## 9. Definition of Done Checklist

- [x] Outdated snapshot + upstream status + advisory scan recorded with sources.
- [x] RISK-0007/0009 trigger verdicts stated with live evidence.
- [x] FINDINGS parked for 60.1/60.2; no changes made.