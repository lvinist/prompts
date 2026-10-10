# mine-flow — STEP-60 Findings: Dependency & Security Maintenance Sweep (Combined)

**Date:** 2026-10-10
**Executor:** Hermes subagent (vc/deepseek-v4.1)
**Status:** Conditional close (branches local, owner review gates merge)

---

## Batch-End Summary: STEPs 56–60

| STEP | Title | Status | Evidence |
|---|---|---|---|
| STEP-56 | Phase-3 Close-Out: Release Notes & User-Facing Docs | **Done** (closed 2026-10-10, owner-approved) | Release notes v1.3.0 drafted (`f5275da`); Phase-3 README STEP-55 row (`67d766d`); gap list recorded. Docs branch merged to main. |
| STEP-57 | Staging Zone Seed & Foreman Zone-Insert Policy | **Done** (closed 2026-10-10, owner-approved push/merge) | App merged at `63deed7`; CI run 38030561898 ALL-GREEN (lint/test, APK, E2E Web+Android incl. daily_log journey); RISK-0030 closed (`f317ee3`). Known behavior: foreman soft-delete 403 recorded. |
| STEP-58 | Doc-Drift, Risk-Register Sweep & Workspace Hygiene | **Done** (closed 2026-10-10) | 16/16 docs triple-agreement; 31-row risk sweep (RISK-0026 closed via parent-run staging audit 124/124 rows); PyYAML installed; PR #206 rechecked (open). Docs branch merged. |
| STEP-59 | OS Process-Death Restoration for All Form Features | **Done** (closed 2026-10-10) | 973 passed / 5 skipped / 0 failed at `4c74e87`; analyze 0 issues; format clean; l10n + contract guards exit 0; restoration matrix 7/7 green (80 focused tests); merged at `8394778`; CI run 38049230677 ALL-GREEN. CI correction `d975d13` cited. |
| STEP-60 | Dependency & Security Maintenance Sweep | **In progress** (conditional close) | 60.0 inventory + 60.1 lockfile bump + 60.2 verdicts complete. Branch local; merge PENDING owner review. |

---

## STEP-60 Execution Record

### 60.0 — Dependency Inventory & Advisory Scan

**Status:** Complete (read-only; no changes made).

**Source:** `mine-flow-STEP-60.0-FINDINGS.md`

Key findings:
- `flutter pub outdated --json` snapshot: 81 packages (17 direct, 63 transitive). Full JSON saved to `.step60.0-pub-outdated.json`.
- **hive_ce:** latest = 2.20.2 (pub.dev API, published 2026-10-06). Maintenance trajectory restored: 2.20.0 (09-12), 2.20.1 (09-27), 2.20.2 (10-06).
- **hive_ce_flutter:** latest = 2.4.0 (pub.dev API, published 2026-09-27).
- **forui:** latest = 0.27.4 (pub.dev API, published 2026-10-04). Pinned at ^0.26.0 — 0.27.x is out-of-constraint (pre-1.0 minor = breaking).
- **Flutter stable:** v3.47.7 (Flutter releases JSON, published 2026-10-08T23:29:50Z). Local install: 3.47.1.
- **Advisory scan:** No advisories on any checked package (pub.dev API `isCurrentAffectedByAdvisory` = false for all).

**Trigger verdicts:**
- RISK-0007 (>6 months no hive_ce release): **RESOLVED** — active maintenance restored.
- RISK-0009 (Flutter stable ≥3.48): **NOT FIRED** — stable is 3.47.7 (< 3.48).

### 60.1 — Bounded Compatibility / Lockfile Work

**Status:** Complete. 19 packages upgraded (lockfile-only, no pubspec.yaml changes).

**Source:** `mine-flow-STEP-60.1-FINDINGS.md`

Upgrades applied (all within existing `^` constraints):
- **hive_ce:** 2.19.3 → 2.20.2 (owner-locked, RISK-0007)
- **hive_ce_flutter:** 2.3.4 → 2.4.0
- **go_router:** 18.0.1 → 18.0.2
- **flutter_secure_storage:** 11.1.0 → 11.2.0
- **file_picker:** 12.2.0 → 12.3.0
- **supabase_flutter:** 2.17.2 → 2.18.2 (supabase 2.16.1 → 2.16.4)
- **image_picker:** 1.2.3 → 1.2.4
- **pdf:** 3.13.0 → 3.13.1
- **printing:** 5.15.0 → 5.15.1
- **lucide_icons_flutter:** 3.1.19 → 3.1.24
- **package_info_plus:** 10.2.1 → 10.2.2
- **url_launcher:** 6.3.2 → 6.3.3
- **battery_plus:** 7.1.1 → 7.1.2
- **googleapis_auth:** 2.3.3 → 2.3.4
- (+ 6 transitive co-upgrades: file_picker_darwin, file_picker_platform_interface,
  gotrue, realtime_client, storage_client, windows_file_picker)

**Owner-decision items parked (NOT applied):**
- forui 0.26 → 0.27.4: out-of-constraint (^0.26.0; pre-1.0 minor = breaking)
- connectivity_plus, http, googleapis: out-of-constraint
- Flutter SDK upgrade: owner decision to not widen SDK constraints
- _test_l10n_guard_temp_* directories: owner-declined sweep — left untouched

**Commit:** `cd1a197` on branch `step-0060-dependency-security-sweep` (app repo).

**Gates (all green at branch head `cd1a197`):**
| Gate | Command | Result |
|---|---|---|
| `flutter analyze` | — | No issues found! ✅ |
| `dart format` | `dart format --output=none --set-exit-if-changed lib/ test/` | 365 files, 0 changed ✅ |
| L10n guard | `dart run tool/check_l10n_baseline.dart` | 21 scanned, 47 exempt, 0 violations ✅ |
| Contract guard | `dart run tool/check_supabase_contracts.dart` | Contract verification passed ✅ |
| Full test suite | `flutter test` | 973 passed, 5 skipped, 0 failed ✅ |
| `git diff pubspec.yaml` | — | Empty ✅ |

**Note:** First full-suite run showed 1 flaky failure in
`attendance_daily_log_sync_test.dart` ("Timestamp conflict resolution" — expected
2 processed items, got 1). Re-ran in isolation: 3/3 passed. Re-ran full suite:
973/5/0. The failure was a timing race in the test's 100ms delay, not a dependency
regression.

### 60.2 — Risk Verdicts, Register Update & Close

**Status:** Complete (conditional close — branch stays local).

**Actions completed:**
1. ✅ RISK-0007 verdict: trigger RESOLVED, active maintenance restored, lockfile at 2.20.2.
2. ✅ RISK-0009 verdict: trigger NOT fired (stable 3.47.7 < 3.48), forui pin kept.
3. ✅ RISK-0020 verdict: 19 upgrades applied, SDK-pinned residuals unchanged.
4. ✅ `registries/risks.yml` updated with STEP-60 evidence (docs main, committed +
   pushed at `798a752`).
5. ✅ `prompts/STEP-index.md` STEP-60 row flipped to "In progress" with conditional-close
   evidence cell.
6. ✅ `check.sh` duplicate STEP scan: 0 duplicates.

**What is NOT done (owner review gates these):**
- App branch `step-0060-dependency-security-sweep` merge — **PENDING owner review**.
- STEP-60 index flip to "Done" — will happen after merge approval.
- Archive to `prompts/003.../step-0060/` — **PENDING** (owner does after merge approval).
- PLAN flip + checklist completion — **PENDING** (owner does after merge approval).

---

## Remaining Owner Decisions (for morning review)

1. **Approve step-0060 branch merge** — branch `step-0060-dependency-security-sweep`
   is local with all gates green at `cd1a197`. Diff is lockfile-only (19 packages).
2. **STEP-60 final index flip + archive** — after merge, flip index row to Done,
   archive PLAN + FINDINGS + snapshots to `prompts/003.../step-0060/`.
3. **Flutter SDK upgrade decision** — local install is 3.47.1; upstream stable
   is 3.47.7. Not applied (SDK upgrade is an owner decision, not an auto-bump).
4. **forui 0.27.x upgrade** — out of constraint until the pin is widened (requires
   RISK-0009 trigger to fire, i.e., Flutter stable ≥3.48).
5. **Parked transitive upgrades** — connectivity_plus (7.3.1→7.3.2), http (1.6.0→1.7.1),
   googleapis (17→19) are all out of the current `^` constraint; awaiting owner decision
   on constraint widening at the next dependency STEP.

---

## Branch Evidence Cells

| Repo | Branch | Head | Pushed? |
|---|---|---|---|
| mine-flow-app | step-0060-dependency-security-sweep | `cd1a197` | NO (local only) |
| mine-flow-docs | main | `798a752` | YES (risks.yml verdicts) |
| prompts | main | PENDING (STEP-index update) | YES (pending) |