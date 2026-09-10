# mine-flow — STEP-51.2: `SnackBar` → `FToast`/`FToaster` (13 files, 35 sites)

> **How to run:** Tell your agent *"run substep 51.2"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.
>
> **Assigned model: Gemini 3.1 Pro High.** Behaviour-carrying migration: toasts have
> dismiss/timeout/action semantics, so each site needs judgement about what the replacement
> must preserve and what a test should assert. Bounded by Doc 07 and the 51.1 inventory, but
> not mechanical.

## Context

STEP-51 sweeps the residual Material widgets STEP-46 left behind (CF-087). This substep
migrates all `SnackBar`/`showSnackBar` usage to forui 0.26's `FToast`/`FToaster`. Read the
PLAN (`Upcoming Prompts/mine-flow-STEP-51-PLAN.md`) and **51.1's findings**
(`Upcoming Prompts/mine-flow-STEP-51.1-FINDINGS.md`) — the inventory table there is your
work list; do not re-derive it. Baseline at start: `flutter test` **553 passed**.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-51-PLAN.md` (decisions D2/D3, ground rules)
- `Upcoming Prompts/mine-flow-STEP-51.1-FINDINGS.md` (the inventory — your work list)
- Root `.throughstone/local-user.md`
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` (Doc 07 — toast pattern)
- `Code/mine-flow-docs/architecture/12-test-strategy.md` (test tiers)
- forui toast source: `D:/AppDev/.pub-cache/hosted/pub.dev/forui-0.26.0/lib/src/widgets/toast/`
- `Code/mine-flow-app/README.md`

## Scope

**Owns:** every `showSnackBar(` / `SnackBar(` site in `lib/` (51.1's inventory, SnackBar
family); one shared toast-host wiring; widget tests for behaviour-carrying migrations;
retiring `ScaffoldMessenger` snack-bar uses that ride along with this family.

**Does NOT touch:** `AppBar`, `Scaffold`, `CircularProgressIndicator` families (51.3/51.4/
51.5); `flutter/material.dart` import removal beyond what this family's files need (51.6
finishes that); CF-043 (51.7); any test not related to toasts/snackbars.

## Your task

1. **Wire the toast host once.** Establish the app's `FToaster` host per Doc 07's pattern
   (and forui 0.26's API — read the pub-cache source, don't guess). One place, not 13.
2. **Migrate all 35 sites** in the inventory. For each: replace `showSnackBar`/`SnackBar`
   with `FToast`/`FToaster` semantics, preserving duration, action callbacks (e.g. "Undo"),
   and error/info variants. Where a site used `ScaffoldMessenger.of(context)`, retire that
   use in the same commit.
3. **Widget tests where behaviour changes** (D3). At minimum: a toast appears after the
   triggering action; an action callback fires; dismissal behaves (duration or manual).
   Follow the existing toast/widget-test patterns under `test/` — search for how the 13
   already-cited CF-id tests are written.
4. **Update existing tests that matched on SnackBar** — they were asserting on Material;
   update what they look for, not what they prove (ground rule: never weaken an assertion to
   pass).

## Verification

- `grep -rE 'showSnackBar\(|[^w]SnackBar\(' lib --include='*.dart'` → **0 hits** (or every
  survivor justified in a code comment and listed in findings).
- `flutter analyze` → 0 issues; `dart format --set-exit-if-changed` → clean.
- `flutter test` → green; state the count and delta vs 553 (new toast tests add cases).
- Full-suite run required, not just the touched files — toast changes can break unrelated
  screen tests that trigger feedback messages.

## Keeping the docs true

Doc 07 §3/§6 already names ForUI as the vocabulary — this is compliance, no doc change
expected (D5). If you find a toast behaviour ForUI cannot express, **stop and escalate** —
that's an ADR-shaped decision (documented Material exception), not yours to make silently.
Record any accepted deferral in `registries/risks.yml` only if the user approves it.

## Definition of done

- [ ] All inventory SnackBar sites migrated; grep count zero (or justified survivors).
- [ ] Toast host wired once.
- [ ] New/updated widget tests pass, citing the CF id they guard where applicable.
- [ ] `flutter analyze` 0, format clean, `flutter test` green with count+delta stated.
- [ ] Findings file `Upcoming Prompts/mine-flow-STEP-51.2-FINDINGS.md` written; PLAN row updated.

## Escalation (to Opus 4.8 — record in findings if fired)

- A failing test you cannot classify as test-defect vs application-defect.
- A toast behaviour forui 0.26 cannot express (ADR-shaped).
- The same fix failing twice — stop, diagnose, escalate rather than iterating.
- Any temptation to mark a site "migrated" the grep still counts.

## Next

Tell the user: *"run substep 51.4"* (Scaffold→FScaffold, Flash — it depends on this
substep's `ScaffoldMessenger` retirement) — in a **fresh chat**. 51.3/51.5/51.7/51.8 may run
in parallel if not already done.
