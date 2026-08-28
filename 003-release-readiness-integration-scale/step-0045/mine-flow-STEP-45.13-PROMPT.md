# mine-flow — STEP-45.13: `go_router` v16→v17 deep-link validation

**Recommended model:** Gemini 3.1 Pro (routing/redirect/shell-persistence reasoning across every route; touches RISK-0006).

> **How to run:** *"run substep 45.13"*. Self-contained; runnable cold.

## Context

Closes the STEP-43 deferral: `go_router` was upgraded v15→v17 and full E2E deep-link validation was
explicitly deferred to STEP-45 (RISK-0006). This substep drives direct-load/reload of every route on
the web build and confirms shell persistence, redirects, and no observer regressions. Depends on 45.7
(which may register the benchmark form route). Read `Upcoming Prompts/mine-flow-STEP-45-PLAN.md`.

## Read these first
- `Upcoming Prompts/mine-flow-STEP-45-PLAN.md`.
- `Code/mine-flow-app/lib/app/router.dart` — all routes, `StatefulShellRoute`, redirects, auth guard.
- `Code/mine-flow-docs/registries/risks.yml` — **RISK-0006** (go_router v17 route API audit) and
  **RISK-0009** (semantics regression, informs finders).
- `Code/mine-flow-docs/reports/2026-08-25-step-0043-upgrade-report.md` — the v16→v17 change notes
  (observer-only breaking change) and the deferred deep-link item.

## Scope

Owns `integration_test/journeys/deep_link_journey_test.dart` (web) and the RISK-0006 status update.

## Your task

1. On the **web** build, direct-load (via URL) and reload every top-level route and each `:id` route
   (e.g. a data-bucket file detail `/…/:id`), asserting the route resolves, the shell persists, and
   auth redirects behave (unauthenticated deep-link → login → back to target after login).
2. Confirm no `ShellRoute` observer regression from the v17 `notifyRootObserver` change (the codebase
   has no custom `NavigatorObserver`s per RISK-0006 — assert nothing broke).
3. Include the benchmark form route if 45.7 registered it.
4. **Update RISK-0006** status (monitoring → closed, or note remaining gaps) citing this STEP.

Staging creds absent → **Unverified** with reason (auth-guarded routes need a session).

## Verification
- Deep-link journey passes on Chrome (or Unverified w/ reason).
- RISK-0006 status updated in `registries/risks.yml`.
- `flutter analyze` 0 / format clean. Commit on the STEP-45 branch (test) and docs branch (risk).

## Definition of done
- [ ] Every top-level + `:id` route direct-load/reload verified on web (or Unverified w/ reason).
- [ ] No observer regression; RISK-0006 status updated.
- [ ] analyze 0 / format clean; file documented.

## Next
Run substep 45.14 (Runtime Impeccable design review) in a fresh chat.
