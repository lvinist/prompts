# mine-flow — STEP-51.3: `AppBar` → ForUI header (14 files, 19 sites)

> **How to run:** Tell your agent *"run substep 51.3"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.
>
> **Assigned model: Gemini 3.1 Pro High.** Headers carry navigation affordances (back,
> actions, titles) that existing screen tests assert on; each site needs judgement about
> which FHeader variant fits and how finders must move. Bounded by Doc 07 and the 51.1
> inventory, but the finder/test surface is not mechanical.

## Context

STEP-51 sweeps the residual Material widgets STEP-46 left behind (CF-087). This substep
migrates all `AppBar(` sites to forui 0.26's header family (`FHeader` root/nested,
`FHeaderAction` — the 9 existing `FHeader` uses in `lib/` are the established reference
pattern). Read the PLAN and **51.1's findings** — the inventory there is your work list.
Baseline: `flutter test` **553 passed** (plus any delta from earlier 51.x substeps).

## Read these first

- `Upcoming Prompts/mine-flow-STEP-51-PLAN.md` (decisions D2/D3, ground rules)
- `Upcoming Prompts/mine-flow-STEP-51.1-FINDINGS.md` (the inventory — your work list)
- Root `.throughstone/local-user.md`
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` (Doc 07 — header pattern)
- `Code/mine-flow-docs/architecture/12-test-strategy.md`
- forui header source: `D:/AppDev/.pub-cache/hosted/pub.dev/forui-0.26.0/lib/src/widgets/header/`
- Existing reference uses: `grep -rn "FHeader" lib --include='*.dart'` (9 sites)
- `Code/mine-flow-app/README.md`

## Scope

**Owns:** every `AppBar(` site in `lib/` per the 51.1 inventory; updating existing screen
tests that find/match on `AppBar` or its back button.

**Does NOT touch:** the `Scaffold` bodies these AppBars sit in (51.4 — but note the
interaction: an `FScaffold` may require a header, not an `AppBar` slot; if 51.4 has already
run, follow its pattern); other Material families; import cleanup (51.6).

## Your task

1. **Migrate all 19 sites** to the header pattern the existing `FHeader` uses establish
   (root vs nested header per navigation depth). Preserve: title, back affordance (or its
   deliberate absence on root screens), and every trailing action; keep semantics labels
   stable where they exist — STEP-48's E2E journeys assert on semantics labels, so a
   renamed label can silently break the CI gate.
2. **Update existing screen tests** that find `AppBar`, back buttons, or titles. Known trap
   (inherited, STEP-48): scope form finders to the screen, not `.at(0)` — 48.22 lost two
   sessions to a desktop header search field matching first.
3. **No new tests required per D3** unless a header introduces new behaviour (e.g. an action
   that did not exist before) — container swaps must not break existing tests.

## Verification

- `grep -rE 'AppBar\(' lib --include='*.dart'` → **0 hits** (or justified survivors).
- `flutter analyze` → 0; `dart format --set-exit-if-changed` → clean.
- `flutter test` → green, count+delta stated (expect no new cases; existing must pass).
- If any widget test or the E2E journey surface asserts on header semantics, list which and
  confirm they still match.

## Keeping the docs true

Doc 07 compliance — no doc change expected. If a screen genuinely needs a Material-only
app-bar affordance, escalate (ADR-shaped), don't improvise.

## Definition of done

- [ ] All inventory AppBar sites migrated; grep zero (or justified survivors).
- [ ] Existing screen tests green; any finder updates listed in findings.
- [ ] `flutter analyze` 0, format clean, `flutter test` green with count+delta.
- [ ] Findings `Upcoming Prompts/mine-flow-STEP-51.3-FINDINGS.md`; PLAN row updated.

## Escalation (to Opus 4.8 — record in findings if fired)

- A semantics-label change STEP-48's journeys depend on (E2E gate risk).
- A navigation affordance FHeader cannot express.
- Test-defect vs application-defect you cannot classify; same fix failing twice.

## Next

Tell the user the next open substep — 51.4 waits on 51.2 (not on this); 51.5/51.7/51.8/51.9
depend only on 51.1. In a **fresh chat**.
