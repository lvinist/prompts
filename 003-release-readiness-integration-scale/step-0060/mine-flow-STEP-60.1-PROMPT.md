# mine-flow — STEP-60.1: Bounded Compatibility / Lockfile Work (or Recorded No-Op)

> **How to run:** "run substep 60.1". Cold-runnable.
> **Assigned model tier: mid** (bounded compatibility work; constraint-widening is an
  owner decision that parks, never auto-applies).

## Context

Act on 60.0's inventory: apply only safe, constraint-compatible updates, or record an
honest no-op. STEP PLAN: `Upcoming Prompts/mine-flow-STEP-60-PLAN.md`;
inventory: `Upcoming Prompts/mine-flow-STEP-60.0-FINDINGS.md`.

## Read these first

- 60.0 FINDINGS (the actionable list + parked advisories).
- `pubspec.yaml` constraints (the boundary of "safe").
- STEP-53's precedent (`step-0053` archive: how the last drift sweep was run + verified).

## Scope

**Owns:** patch/minor updates within existing constraints (e.g. go_router 18.0.x,
file_picker, lucide, build_runner drift); lockfile regen; focused suites + static gates
after; or the no-op record. App branch `step-0060-dependency-security-sweep`.

**Does NOT touch:** constraint-widening upgrades (Flutter SDK, forui major/minor-pin
changes, hive_ce major — park with options for the owner), product code beyond what a
dependency bump strictly requires, production.

## Your task

1. From 60.0's actionable list: classify each item safe-in-constraints vs
   needs-owner-decision. Safe items: bump + `flutter pub upgrade --major-versions` is
   NOT the default — prefer targeted `pub upgrade <pkg>` within constraints.
2. Apply safe updates; run `flutter pub get`; verify lockfile diff is the expected
   packages only.
3. Gates: `flutter analyze`, format on touched, focused suites for features the bumped
   packages touch (e.g. go_router → router tests; file_picker → data bucket), l10n +
   contract guards. Full suite runs in 60.2 if deps changed.
4. If nothing is safe-actionable: write the no-op record with per-item reasons (this is
   a valid outcome).
5. One lane commit (`60.1`); FINDINGS: bumps applied (from→to), lockfile delta, gates,
   parked owner-decision items with options.

## Verification

- Lockfile diff confined to named packages; no constraint edits in pubspec (verify:
  `git diff pubspec.yaml` empty or exactly the intended lines).
- Gates green; focused suites green; parked items have options + tradeoffs, not silence.
- If no-op: every actionable 60.0 item has a recorded reason.

## Definition of done

- [ ] Safe updates landed with green gates, or no-op recorded with reasons.
- [ ] Owner-decision items parked with options.
- [ ] Lane committed; FINDINGS complete.

## Next

Report to parent. Next: 60.2 (risk verdicts + register update + STEP close).
