# mine-flow — STEP-60.0: Dependency Inventory & Advisory Scan

> **How to run:** "run substep 60.0". Cold-runnable.
> **Assigned model tier: fast** (mechanical inventory with clear gates; no judgment
  calls — findings park for the mid-tier verdict substep).

## Context

The batch's maintenance STEP starts with a live inventory: what's outdated, what's
released upstream, what advisories exist. Everything is recorded; nothing is changed.
STEP PLAN: `Upcoming Prompts/mine-flow-STEP-60-PLAN.md`.

## Read these first

- `pubspec.yaml` + `pubspec.lock` (current pins: go_router ^18.0.0, hive_ce ^2.19.3/
  hive_ce_flutter ^2.3.4, forui ^0.26.0, SDK >=3.12.0 <4.0.0).
- `registries/risks.yml` RISK-0007/0009/0020 (what the verdicts must answer).
- `reports/2026-08-13-flutter-dependency-ci-audit.md` (the original audit baseline).

## Scope

**Owns:** (a) `flutter pub outdated --json` (or equivalent) snapshot to scratch;
(b) live upstream checks: hive_ce pub.dev release status + changelog date, Flutter
stable channel version (the RISK-0009 trigger check), forui releases post-0.26;
(c) advisory scan (pub.dev / OSV-style check for pinned packages; note how the check
was run); (d) FINDINGS. Branch `step-0060-dependency-security-sweep` (app repo, docs
side as needed). No dependency changes.

**Does NOT touch:** pubspec files, lockfile, code, registries.

## Your task

1. Snapshot `flutter pub outdated` full output (scratch file + summary in FINDINGS).
2. Live-fetch: hive_ce latest version + release date (pub.dev API), Flutter stable
   release (the releases JSON), forui versions after 0.26.0. Record fetch dates.
3. Compare against RISK-0007's >6-months trigger and RISK-0009's stable-≥3.48 trigger:
   fired / not-fired, with the fetched evidence.
4. Advisory scan of current pins; record method + any hits (hits park for 60.1/60.2 —
   no auto-fixing here).
5. FINDINGS: inventory tables + trigger verdicts + parked advisory items.

## Verification

- All version/date claims carry a fetch source + date (no memory claims).
- `git status` clean in all repos (inventory is read-only; scratch output lives in
  `Upcoming Prompts/`).
- Trigger verdicts derived from the fetched numbers, quoted in FINDINGS.

## Definition of done

- [ ] Outdated snapshot + upstream status + advisory scan recorded with sources.
- [ ] RISK-0007/0009 trigger verdicts stated with live evidence.
- [ ] FINDINGS parked for 60.1/60.2; no changes made.

## Next

Report to parent. Next: 60.1 (bounded compatibility work or no-op record).
