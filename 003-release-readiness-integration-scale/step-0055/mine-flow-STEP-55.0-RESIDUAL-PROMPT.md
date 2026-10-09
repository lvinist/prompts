# mine-flow — STEP-55.0 RESIDUAL: wire remaining dismiss triggers

> **How to run:** Tell your agent "run 55.0 residual fix only". Execute cold in a fresh chat.
>
> **Assigned model: Hermes/Claude Opus 4.8.** Same tier as 55.0 — the dismissal contract compounds across every feature.

## Context

55.0 is Done and the shared primitives exist on branch `step-0055-cohesive-ui-rebuild` in `mine-flow-app` (`9dad444`, plus later 55.11 hardening). The audit (2026-09-19, recorded in `prompts/STEP-index.md` row 55.0) found three residuals. This lane fixes **only the first** — the unwired dismiss triggers. It does **not** redo the foundation, migrate features, or adopt the popover in feature lists (that belongs to the 55.2/55.3 lanes).

## Residual scope (exact — nothing else)

From the index row 55.0:

1. Wire `drag`, `browserNavigation`, and `parentNavigation` dismiss triggers through the one `AppDismissController` path. Today all eight `AppDismissReason`s are *defined* in `lib/core/presentation/widgets/app_interaction_primitives.dart` but only close/barrier/escape/systemBack/cancel are *wired*. Every wired path must keep: one guard, exactly one route pop, non-dismissible dirty dialog while dirty, blocked + announced while busy.
2. Prove the `AppFilterPopover` adoption contract is ready for the feature lanes (focused test + one-paragraph adoption recipe in FINDINGS). Do **not** edit feature list files here — CF/LC adoption is owned by 55.2/55.3.
3. Runtime captures stay **Unverified** (Impeccable binary absent; consolidated audit is 55.11's lane). Record that, do not invent visual evidence.

## Read first

- `Upcoming Prompts/mine-flow-STEP-55-PLAN.md` (ground rules, evidence contract)
- `Code/mine-flow-docs/reports/2026-09-11-step-54-master-polish-spec.md` §§2.4–2.7 (D4 dirty guard, D5 adapter, shared acceptance tests)
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` §4.1 (sheet/dirty contract)
- `Upcoming Prompts/mine-flow-STEP-55.0-FINDINGS.md` (baseline: what 55.0 proved)
- `Code/mine-flow-app/lib/core/presentation/widgets/app_interaction_primitives.dart` (current triggers)
- `Code/mine-flow-app/test/core/presentation/widgets/app_interaction_primitives_test.dart` (extend, don't rewrite)

## Pre-flight (do not skip)

1. `git status --short --branch` + `git log --oneline -5` in `Code/mine-flow-app`. Confirm you are on `step-0055-cohesive-ui-rebuild`. Confirm `prompts/` is on `main`.
2. Preserve everything dirty/untracked — especially the 55.11 lane files (`.step55.11h-run-web.sh`, `.step55.11i-run-android.sh`, `run_web_wrapper.dart`, `test/widget/m2_challenger_stress_test.dart`, `tool/verify_test_driver_adversarial.dart`). Never stash, reset, absorb, or commit them. Stop and report ownership if the tree differs from this picture.

## Likely files (ownership boundary)

- ALLOWED: `lib/core/presentation/widgets/app_interaction_primitives.dart`, `test/core/presentation/widgets/app_interaction_primitives_test.dart`, `Upcoming Prompts/mine-flow-STEP-55.0-FINDINGS.md` (append only).
- FORBIDDEN: `lib/features/**`, `lib/app/router.dart`, `lib/l10n/**`, docs, index. If a trigger truly needs a caller-side hook outside the shared file, leave that call site dirty, record the exact file:line as a handoff, and stop — do not absorb another lane.

## Tests and verification

Extend the existing test file (new cases, same style): each newly-wired reason in clean/dirty/busy states; rapid-repeat dismissal still approves exactly once (the 55.11 one-shot latch must keep holding); popover apply/reset/cancel already covered — add only what the adoption contract needs. Then run:

- `flutter test test/core/presentation/widgets/app_interaction_primitives_test.dart`
- `dart format --output=none --set-exit-if-changed <touched files>`
- `flutter analyze`

Record exact commands + counts. No new dependency, no schema, no l10n change expected — if one proves necessary, stop and escalate instead of inventing it.

## Boundaries and escalation

- No feature migration, no router edit, no visual restyle, no new package.
- Stop (don't retry a third time) if the same trigger fails twice, if `PopScope`/navigator locking fights the one-shot latch, or if a trigger needs an architecture change. Record the blocker as Unverified.
- Never print `.env` or secret values.

## Definition of done

- `drag` / `browserNavigation` / `parentNavigation` each reach `AppDismissController.requestDismiss` and behave per clean/dirty/busy contract; focused + static gates pass; FINDINGS has a dated "Residual fix 2026-09-19 (55.0)" section with commands/counts, the popover adoption recipe, and the Unverified runtime note.

## Next

Report the exact replacement evidence-cell line for index row 55.0 (do **not** edit the index or flip any status yourself). Tell the user to run the 55.1 residual in a fresh chat.
