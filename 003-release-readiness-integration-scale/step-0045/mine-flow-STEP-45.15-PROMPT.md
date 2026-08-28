# mine-flow — STEP-45.15: Findings reconciliation, docs, risks & STEP close

**Recommended model:** Gemini 3.1 Pro (high-stakes: findings reconciliation, doc/ADR/risk updates, multi-repo merge, archive).

> **How to run:** *"run substep 45.15"*. Self-contained; runnable cold. Final substep of STEP-45.

## Context

Closes STEP-45: reconciles all runtime findings, updates the architecture docs and risk register,
runs the full dual-platform verification gate, merges, and archives. Depends on 45.2–45.14. Read
`Upcoming Prompts/mine-flow-STEP-45-PLAN.md` and the throughstone-workflow skill's closure recipe.

## Read these first
- `Upcoming Prompts/mine-flow-STEP-45-PLAN.md` — the full STEP + Definition of Done.
- All 45.x runtime outcomes recorded in the journey commits and the 45.14 report.
- `prompts/003-release-readiness-integration-scale/step-0046/mine-flow-STEP-46.3-FINDINGS.md` —
  NR-001..006, to mark each resolved or carried-forward.
- `Code/mine-flow-docs/architecture/12-test-strategy.md` (§1 "few E2E", §5 E2E tier, §6 CI gates —
  to bump), `10-observability.md`, `09-environments.md`.
- `Code/mine-flow-docs/templates/adr-template.md` and `adr/README.md` (reserve the ADR number like a STEP number).
- `Code/mine-flow-docs/registries/risks.yml` — RISK-0006/0009/0011/0014.
- `Code/mine-flow-docs/METHOD.md` §6 (keeping docs true), §10 (next-action resolver).

## Scope

Owns the findings reconciliation, doc/ADR/risk updates, final verification, merges, and archive.
Does not write new journeys (that's 45.3–45.14).

## Your task

1. **Reconcile NR-001…006:** for each, record in the STEP-45 report whether it was resolved (with the
   code fix + test reference) or explicitly carried forward as a named `registries/risks.yml` row with
   a revisit trigger. **None may be left silent.** Register any new runtime findings the same way.
2. **Test-strategy doc + ADR:** bump `architecture/12-test-strategy.md` Version Log to reflect the
   expanded E2E tier (all Tier-1/2 features) and the **dual-platform (Chrome + `Pixel_6a`) E2E CI
   gate** (update the §6 gate list and the §1/§5 "few E2E tests" framing). Reserve and write an **ADR**
   recording the scope-expansion decision (E2E on both platforms as a gate). Update
   `architecture/10-observability.md`/`09-environments.md` if the E2E evidence location changed.
3. **Risk register:** update RISK-0006 (go_router deep-link — from 45.13), RISK-0009 (still open/note),
   RISK-0011 (privacy notice runtime status — from 45.14), RISK-0014 (reporting semantics — from
   45.5/45.9), plus any new rows from carried-forward NR items and 45.8 large-file guard.
4. **Full verification gate:** run the entire `integration_test` suite on **both** Chrome and
   `Pixel_6a`; run the existing `flutter test` unit/integration suite; `dart format --set-exit-if-changed
   lib/ test/ integration_test/`; `flutter analyze` (0 issues); `flutter build apk --debug` and
   `flutter build web --release` smoke builds. Record real results. Blockers → Unverified with reason,
   not a claimed pass.
5. **STEP review:** standard PR/code review across the STEP-45 branches + doc-drift check.
6. **Merge** app → docs → prompts (per the PLAN's merge order); verify each merge is a fast-forward
   or clean.
7. **Archive:** gather all `Upcoming Prompts/mine-flow-STEP-45-*` files (PLAN + 15 prompts +
   DECISIONS + the design-review report reference) into
   `prompts/003-release-readiness-integration-scale/step-0045/`; fill the STEP-45 substep table in
   `prompts/STEP-index.md`; flip STEP-45 → **Done**. Update the phase `003-…/README.md` summary row.
8. **Say what's next:** run `./doctor.sh status` and report the next action (likely a Check-in STEP —
   last check-in was STEP-40, and STEP-45 close will be ~5 STEPs later, still within headroom, but
   flag it if the resolver suggests one).

## Verification
- All DoD items in the STEP-45 PLAN are checkable and checked (or the blocker is Unverified with reason).
- Full dual-platform E2E + existing suites + static gates + build smoke all green (or documented blockers).
- Dup scan clean; `git diff --check` passes on `prompts`.

## Definition of done
- [ ] NR-001…006 each resolved-or-carried-forward with evidence; new findings registered.
- [ ] `architecture/12-test-strategy.md` bumped + ADR for the E2E expansion; observability/environments touched if needed.
- [ ] RISK-0006/0009/0011/0014 updated; new risks added for carried-forward items.
- [ ] Full dual-platform verification gate run with real results recorded.
- [ ] STEP review passed; branches merged app→docs→prompts.
- [ ] STEP-45 archived to `prompts/003-release-readiness-integration-scale/step-0045/`; index Done; phase README updated.
- [ ] Next action reported via `./doctor.sh status`.

## Next
STEP-45 complete. Start a fresh chat for the next action from `./doctor.sh status`.
