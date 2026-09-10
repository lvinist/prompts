# mine-flow — STEP-51.4: `Scaffold` → `FScaffold` (24 files, 37 sites)

> **How to run:** Tell your agent *"run substep 51.4"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.
>
> **Assigned model: Gemini 3.7 Flash High.** Mechanical container swap with an unambiguous
> signal: analyzer, existing tests, and a grep count that must reach zero. The 3 existing
> `FScaffold` uses are the reference. Volume (37 sites) is not judgement risk.

## Context

STEP-51 sweeps the residual Material widgets STEP-46 left behind (CF-087). This substep
migrates all `Scaffold(` sites to forui 0.26's `FScaffold`. **Depends on 51.2** — the
`ScaffoldMessenger`/snackbar interplay must already be retired there. Read the PLAN and
**51.1's findings** — the inventory is your work list. Baseline: `flutter test` green at
the 51.2-close count.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-51-PLAN.md` (decisions D2/D3, ground rules)
- `Upcoming Prompts/mine-flow-STEP-51.1-FINDINGS.md` (the inventory)
- `Upcoming Prompts/mine-flow-STEP-51.2-FINDINGS.md` (what 51.2 did to
  `ScaffoldMessenger` — read before touching shared files)
- Root `.throughstone/local-user.md`
- `Code/mine-flow-docs/architecture/07-ui-design-system.md`
- forui scaffold source: `D:/AppDev/.pub-cache/hosted/pub.dev/forui-0.26.0/lib/src/widgets/scaffold.dart`
- Existing reference: `grep -rn "FScaffold" lib --include='*.dart'` (3 sites)
- `Code/mine-flow-app/README.md`

## Scope

**Owns:** every `Scaffold(` site in `lib/` per the 51.1 inventory; updating existing tests
that match on `Scaffold`.

**Does NOT touch:** other Material families (51.3/51.5 already own theirs — if they've run,
their files are already converted; don't re-edit); import cleanup (51.6); any behaviour
change — a container swap must be visually and behaviourally neutral per D3.

## Your task

1. **Migrate all 37 sites** to `FScaffold`, following the 3 existing uses as reference.
   Known trap (STEP-48.22 hit it twice): the "Material ancestor" class of errors — some
   children expect a Material ancestor; if `FScaffold` drops it, an exception fires at
   runtime that the analyzer cannot see. **Run the widget tests per file as you go**, not
   only at the end.
2. **Watch the 51.2 boundary:** if 51.2 left a `ScaffoldMessenger` use that only existed
   for snackbars, it should already be gone; if you find one it missed (e.g. inside a
   `Scaffold` body), report it in findings — don't expand your scope into toast logic.
3. **Update existing tests** matching on `Scaffold`/`ScaffoldMessenger` finders — update
   what they look for, not what they prove.

## Verification

- `grep -rE '[^F]Scaffold\(' lib --include='*.dart'` → **0 hits** (or justified survivors).
- `flutter analyze` → 0; `dart format --set-exit-if-changed` → clean.
- `flutter test` full suite → green, count+delta stated (expect no new cases).
- Especially: no `MediaQuery`/Material-ancestor runtime exceptions in test output.

## Keeping the docs true

Doc 07 compliance — no doc change expected.

## Definition of done

- [ ] All inventory Scaffold sites migrated; grep zero (or justified survivors).
- [ ] `flutter analyze` 0, format clean, full `flutter test` green with count+delta.
- [ ] No Material-ancestor exceptions in test output.
- [ ] Findings `Upcoming Prompts/mine-flow-STEP-51.4-FINDINGS.md`; PLAN row updated.

## Escalation (to Opus 4.8 — record in findings if fired)

- A Material-ancestor failure whose fix is not the known pattern (not a simple
  wrapper/widget swap).
- Any behaviour difference you cannot classify as test-defect vs application-defect.
- The same fix failing twice.

## Next

Tell the user the next open substep — 51.6 waits on 51.2–51.5 all being done. In a
**fresh chat**.
