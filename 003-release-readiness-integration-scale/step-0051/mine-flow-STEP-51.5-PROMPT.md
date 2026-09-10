# mine-flow — STEP-51.5: `CircularProgressIndicator` → `FCircularProgress` (22 files, 25 sites)

> **How to run:** Tell your agent *"run substep 51.5"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.
>
> **Assigned model: Gemini 3.7 Flash High.** Mechanical swap with an unambiguous signal:
> analyzer, existing tests (loading-state finders), and a grep count that must reach zero.

## Context

STEP-51 sweeps the residual Material widgets STEP-46 left behind (CF-087). This substep
migrates all `CircularProgressIndicator(` sites to forui 0.26's `FCircularProgress`
(`FProgress`/`FDeterminateProgress` exist too — pick by whether the site conveys progress
value or indeterminate loading). Read the PLAN and **51.1's findings** — the inventory is
your work list. Baseline: `flutter test` green at the running 51.x count.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-51-PLAN.md` (decisions D2/D3, ground rules)
- `Upcoming Prompts/mine-flow-STEP-51.1-FINDINGS.md` (the inventory)
- Root `.throughstone/local-user.md`
- `Code/mine-flow-docs/architecture/07-ui-design-system.md`
- `Code/mine-flow-docs/architecture/12-test-strategy.md`
- forui progress source: `D:/AppDev/.pub-cache/hosted/pub.dev/forui-0.26.0/lib/src/widgets/progresses/`
- `Code/mine-flow-app/README.md`

## Scope

**Owns:** every `CircularProgressIndicator(` site in `lib/` per the 51.1 inventory; updating
loading-state tests that match on the widget type.

**Does NOT touch:** other Material families; import cleanup (51.6); any loading-behaviour
logic (spinners stay where they are, show/hide conditions unchanged).

## Your task

1. **Migrate all 25 sites.** Indeterminate loading → `FCircularProgress`; sites bound to a
   progress value → `FDeterminateProgress`. Preserve sizing/semantics where tests or
   screen-reader labels depend on them.
2. **Update loading-state tests** that `find.byType(CircularProgressIndicator)` — switch to
   the new type. Never weaken what the test proves (still asserts loading state is shown
   when expected).

## Verification

- `grep -rE 'CircularProgressIndicator\(' lib --include='*.dart'` → **0 hits** (or
  justified survivors).
- `flutter analyze` → 0; `dart format --set-exit-if-changed` → clean.
- `flutter test` full suite → green, count+delta stated (expect no new cases).

## Keeping the docs true

Doc 07 compliance — no doc change expected.

## Definition of done

- [ ] All inventory sites migrated; grep zero (or justified survivors).
- [ ] Loading-state finders updated; full `flutter test` green with count+delta.
- [ ] `flutter analyze` 0, format clean.
- [ ] Findings `Upcoming Prompts/mine-flow-STEP-51.5-FINDINGS.md`; PLAN row updated.

## Escalation (to Opus 4.8 — record in findings if fired)

- A determinate-progress semantics the ForUI widget cannot express.
- Test-defect vs application-defect you cannot classify; same fix failing twice.

## Next

Tell the user the next open substep — 51.6 waits on 51.2–51.5 all done. In a **fresh chat**.
