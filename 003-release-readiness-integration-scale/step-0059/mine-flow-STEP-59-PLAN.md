# mine-flow — STEP-59 PLAN: OS Process-Death Restoration for All Form Features (FC-54.5-013)

**Phase:** Phase 3 — Release Readiness, Integration & Scale (post-milestone follow-up lane)
**Owner:** Hermes (frontier orchestration; subagents execute, parent verifies)
**Status:** Done
**Date:** 2026-10-10
**Branch:** `step-0059-os-restoration-forms` (app + docs repos)
**Repos (projection):** `mine-flow-app`, `mine-flow-docs`, `prompts`

> Extend OS process-death state restoration from the landed attendance lane
> (`27e5c5c`: shell+branch restorationScopeIds, restorationId on all 17 hand-rolled
> CustomTransitionPages, versioned draft snapshot) to every form feature: cut/fill,
> land clearing, daily log, equipment check, benchmark, inventory, and data bucket
> metadata forms. Owner decision 2026-10-10: extend to ALL form features.

## Motivation

FC-54.5-013's investigation (close addendum) proved restoration feasible but cross-cutting;
the owner scoped it to all form features. Field reality: Android process death mid-form
currently loses an in-progress entry everywhere except attendance. The route/scope layers
already exist app-wide (`restorationScopeId` set on app-root, app-router, app-shell, all 5
branches; `restorationId` on all 17 custom pages) — the remaining work is per-feature
draft-state snapshot/restore: versioned draft data registered with restoration buckets,
applied on `AttendanceFormRestoreRequested`-style reload events, proven by
`tester.restartAndRestore()` round-trips.

## Decisions already locked

- **Owner 2026-10-10:** all form features, not attendance-only.
- Attendance is the reference implementation (`lib/features/attendance/presentation/pages/attendance_form_sheet.dart`
  + its restore-requested reload pattern + 2 router + 8 roundtrip tests) — mirror it,
  don't reinvent.
- Three-layer scope rule (go_router): shell `restorationScopeId`, per-branch
  `restorationScopeId`, and per-page `restorationId` — all present; new pages must
  carry `restorationId` explicitly (hand-rolled `CustomTransitionPage` does NOT
  inherit it).
- Test-shape rule: the faithful process-death simulation is `tester.restartAndRestore()`;
  `getRestorationData`/`restoreFrom` trips go_router's one-time registration assertion —
  a red from that pattern is a harness artifact, not a product defect.
- Draft snapshots are versioned + minimal (attendance snapshots status+remarks only;
  roster/auth reloaded fresh) — same minimal-surface philosophy per feature.
- Verify the pinned go_router version from the LOCKED pub cache (`flutter pub cache list`
  resolves PUB_CACHE), not the default cache dir.

## Substeps

| # | Title | Produces | Depends on | Open questions |
|---|-------|----------|------------|----------------|
| 59.0 | Restoration inventory + per-feature draft-state design | Inventory of every form surface + draft fields worth snapshotting; per-feature restore design (parked for owner only if a feature's data model makes snapshots ambiguous) | — | per-feature field selection (see Q1) |
| 59.1 | Cut/fill + land clearing draft restoration | Versioned draft snapshots + restore for both tracking forms; restartAndRestore roundtrip tests | 59.0 | none |
| 59.2 | Daily log + equipment check draft restoration | Same pattern both features | 59.0 | none |
| 59.3 | Benchmark + inventory + data-bucket draft restoration | Same pattern three features | 59.0 | none |
| 59.4 | Cross-feature verification, docs, and close | Full suite + analyzer + focused restoration matrix; Doc 03/15 v-log bumps; index/archive bookkeeping | 59.1–59.3 | none |

**Q1 (resolve per feature at 59.0, bounded judgment, park if ambiguous):** which fields
are draft-state worth snapshotting (user-entered form inputs + selected entity ids) vs
reloaded fresh (reference data, auth, rosters). Attendance's precedent: snapshot the
user's *entry*, reload the *context*.

## Test plan

| Test tier / surface | Substep(s) | Tests | Run timing | Command / gate |
|---------------------|------------|-------|------------|----------------|
| Unit / widget (restoration) | 59.1–59.3 | Per-feature draft snapshot round-trip (save→restore equality), restore-requested reload, version-mismatch fallback (fresh state) | per substep | focused feature suites |
| Router/integration | 59.1–59.3 | `restartAndRestore` roundtrips per feature: URL + sheet + unsaved draft survive | per substep | router_test additions |
| Full regression | 59.4 | Full `flutter test` + `flutter analyze` + format/l10n/contract guards | final verification | full local suite + CI gate at head |

## Ground rules

- Orchestration as prior STEPs; parent verifies each substep parent-side.
- One commit per substep lane; `dart format` on touched .dart files only; l10n
  guard's `lib/core/presentation/` blind spot — any new user-facing string there needs
  ARB key + widget test, not a guard pass.
- If a feature's draft model is genuinely ambiguous (e.g. data-bucket file metadata
  half-uploaded), park that feature's restore with FINDINGS and continue others
  (failure policy).
- Branch stays local until owner review (batch push policy); CI gate runs at head after
  the owner-approved push, or per parent decision at execution time.

## Definition of done

- [x] Every form feature (7 surfaces) has versioned draft restoration with passing `restartAndRestore` roundtrips (or a parked FINDINGS with the named ambiguity — data-bucket file bytes and equipment UI selectors parked per 59.0 §10A).
- [x] Restoration docs updated (Doc 15 native-app-architecture §8) with v-log bumps (v0.3.0); index/substep table/PLAN/archive reconciled.
- [x] Full suite + gates green at the verified head `cdd66b9`; STEP archived per close sequence. CI watcher armed on merged master head `8394778` by parent.
