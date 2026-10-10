# mine-flow — STEP-60 PLAN: Dependency & Security Maintenance Sweep

**Phase:** Phase 3 — Release Readiness, Integration & Scale (post-milestone follow-up lane)
**Owner:** Hermes (frontier orchestration; subagents execute, parent verifies)
**Status:** Planned
**Date:** 2026-10-10
**Branch:** `step-0060-dependency-security-sweep` (app + docs repos)
**Repos (projection):** `mine-flow-app`, `mine-flow-docs`, `prompts`

> Close out the dependency/security maintenance rows the STEP-50/53 reviews left in
> `monitoring`: RISK-0007 (hive_ce maintenance trajectory), RISK-0009 (Flutter
> semantics-regression pin retest), RISK-0020 (SDK-pinned transitive drift), plus a
> general `pub outdated`/advisory sweep. Ground state as of 2026-10-10: **Flutter
> stable = 3.47.7 (2026-10-08)** — the RISK-0009 "stable ≥3.48" retest trigger has NOT
> fired, so that row is verdict/recording work unless execution-day check changes it.

## Motivation

These rows were last verified at STEP-53 (2026-09-10); a month has passed and the owner
wants the batch to end with a clean dependency/risk posture record. The work is
inventory → bounded verification → honest verdict; the strongest tier owns the final
risk verdict because mis-stating a dependency/security posture is a silent record
corruption.

## Decisions already locked

- **Owner posture: fix forward** — on upgrade regressions, migrate to latest libs;
  don't roll back SDK pins.
- Tiering per the model-assignment rule: inventory = fast; compatibility/lockfile = mid;
  final evidence/risk verdict = strongest.
- hive_ce keep/migrate decision authority is ADR-0001 — changing it is an ADR-level
  owner decision, not an executor choice; this STEP only re-verifies and records.
- No production touch; no `.env` printing; upgrade-and-verify only.

## Substeps

| # | Title | Produces | Depends on | Open questions |
|---|-------|----------|------------|----------------|
| 60.0 | Dependency inventory + advisory scan | `pub outdated` snapshot; hive_ce release status; Flutter/forui release check; advisory scan results | — | none |
| 60.1 | Bounded compatibility/lockfile work (only if 60.0 finds actionable drift) | Patch/minor updates within constraints; lockfile; focused suites green; or a no-op record | 60.0 | which updates are safe (bounded by pubspec constraints) |
| 60.2 | Risk verdicts + register update + close | RISK-0007/0009/0020 verdicts evidence-cited; risks.yml updates; STEP close | 60.1 (or 60.0 if no-op) | none |

## Test plan

| Test tier / surface | Substep(s) | Tests | Run timing | Command / gate |
|---------------------|------------|-------|------------|----------------|
| Static gates | 60.0–60.2 | analyze/format/l10n/contract guards | per substep | exit 0 |
| Full regression | 60.2 (only if 60.1 changed deps) | full `flutter test` | final verification | full suite |
| CI gate | 60.2 (only if deps changed) | full workflow at head | final | CI run green at exact head sha |

If 60.0 finds nothing actionable, 60.1 records a no-op (stated reason) and 60.2 runs on
static gates alone — a maintenance STEP whose honest verdict is "nothing to do" is a
valid outcome, not a failure.

## Ground rules

- Orchestration as prior STEPs; parent verifies parent-side.
- 60.1 executes only within existing pubspec constraints (patch/minor drift); a
  constraint-widening upgrade (e.g. Flutter SDK, forui major, hive_ce major) is an
  owner decision parked with options, never auto-applied. RISK-0009's trigger
  (stable ≥3.48) re-checked live at 60.0: if it HAS fired by execution day, the forui
  unpin-retest becomes a real 60.1 item with the full test matrix; if not, record
  not-fired with the fetched version.
- hive_ce: re-verify maintenance status (last release date, changelog); keep/migrate
  stays per ADR-0001 unless the evidence demands escalation → park for owner.
- One commit per lane; findings per substep.

## Definition of done

- [ ] 60.0 inventory recorded with live-fetched versions/dates (not memory).
- [ ] 60.1 either landed safe updates with green gates, or recorded a no-op with reason.
- [ ] RISK-0007/0009/0020 verdicts written with evidence; risks.yml updated; the batch's
      final dependency/risk posture is honest and complete.
- [ ] STEP close sequence run (index/PLAN/archive/prompts push) per owner policy.
