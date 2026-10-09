# mine-flow — STEP-55.10 RESIDUAL: reconcile the false "100% green" record + close the §4.9 evidence gaps

> **How to run:** Tell your agent "run 55.10 residual fix only". Execute cold in a fresh chat.
>
> **Assigned model: Gemini 3.1 Pro High.** Same tier as 55.10 — broad system-surface reasoning (auth/privacy/logging/routing/a11y) bounded by master spec §4.9 and Doc 07, with a P0 privacy/logging honesty component.

## Why this exists (audit 2026-09-21, do-not-trust-status pass)

**This substep's own FINDINGS lied and was then caught by 55.11.** The original `mine-flow-STEP-55.10-FINDINGS.md` §5 says *"None. Substep 55.10 is 100% green"* and *"682 tests passing"*. The 55.11 audit appended an addendum proving that claim false:

- The privacy gate `AppRouter.redirect` held **every** authenticated session on `/privacy-gate`, and the gate **could not be cleared at all** — `privacy_ack_page.dart` called async `updatePrivacyAckVersion(1)` **without awaiting** then navigated, so the redirect re-read version 0 and bounced back. A real user was permanently stuck. This is a **P0 product defect this substep introduced.**
- It broke the whole E2E suite: 13/16 Android + 12/16 Web files failed with `Found 0 widgets with type "<FeatureScreen>"`.
- The "682 passing" count was not reproducible at any committed head.

**Current state (audit-verified on `step-0055-cohesive-ui-rebuild`):** the privacy-gate defect **has since been fixed** — `privacy_ack_page.dart` now awaits, `login_helper.dart` clears the gate for all callers, and `test/features/auth/presentation/privacy_ack_page_test.dart` (committed) **passes** (verified: 3/3, including "acknowledgement persists before the page navigates" and "a slow acknowledgement write still completes before navigation"). The shell/logger suites also pass (`test/app/app_shell_test.dart` 11/11; `logger_test.dart` green). So the **code is now correct**, but the **durable 55.10 record still reads "100% green / None"**, and the index row still says **Planned**. The record and the index are the debt.

## Residual scope (exact — nothing else)

1. **Reconcile the FINDINGS.** Rewrite `mine-flow-STEP-55.10-FINDINGS.md` so the "None / 100% green / 682 passing" claim is corrected in place (supersede with a dated "Residual (55.10) reconciliation" section — do not delete the addendum): state the privacy-gate defect this substep introduced, that it is now fixed (cite the commits/tests), and give the honest current suite count re-derived on the tree (see §Tests).
2. **Re-verify the §4.9 obligations still hold on the current tree**, since the shared shell/header/primitives are being edited by the uncommitted 55.1/55.2/55.3 residual lane:
   - versioned privacy gate is clearable and blocks the dashboard until acknowledged (route + await);
   - sensitive-header **redaction** (`Authorization`, `apikey`, cookie, token) — run `logger_test.dart`, confirm 0 raw-value leaks;
   - five mobile tabs preserved; desktop sidebar/header expose real a11y semantics; `/settings/profile/form` route present; header identity bound to the authenticated user (no hardcoded identity).
3. **Record the privacy-copy authority gap honestly.** The notice body exists in `app_id.arb`/`app_en.arb` but **no accountable product/legal approval is recorded** in the durable authority (confirmed: no approval marker in `registries/` or reports). Carry this as an explicit `Unverified — release acceptance blocked pending product/legal approval` — never claim approval. This is a release blocker, not a 55.10 code task.
4. **Route RISK-0025** (`public.users` self-update privilege escalation, status: open, severity: critical, owner TBD) — confirm it is still open in `registries/risks.yml` and note in the FINDINGS that it remains a §4.9-adjacent open security risk carried into close. Do not silently close it.

## Read first

- `Upcoming Prompts/mine-flow-STEP-55-PLAN.md`; `mine-flow-STEP-55.10-PROMPT.md`; `mine-flow-STEP-55.10-FINDINGS.md` (incl. its 55.11 addendum); `mine-flow-STEP-55.11-FINDINGS.md`
- Master spec §§2.8–2.9, 4.9, 6–7, 8.3, 9; Doc 07 v0.5.0; `registries/risks.yml` (RISK-0004, 0011, 0019, 0025, 0026–0029)
- `lib/features/auth/presentation/pages/privacy_ack_page.dart`, `lib/app/router.dart` (redirect), `lib/core/utils/logger.dart`, `lib/app/presentation/pages/{app_shell,dashboard_page}.dart`, `lib/app/presentation/widgets/global_app_header.dart`, `lib/features/settings/presentation/pages/profile_edit_page.dart`, `integration_test/helpers/login_helper.dart`
- Tests: `test/features/auth/presentation/privacy_ack_page_test.dart`, `test/core/utils/logger_test.dart`, `test/app/app_shell_test.dart`

## Pre-flight (do not skip)

1. `git -C Code/mine-flow-app status --short --branch`. Worktree carries the uncommitted 55.1/55.2/55.3 residual lane + untracked scratch — **preserve, do not stage/reset/stash/absorb.** This residual should add **no code** if §4.9 already holds; it is a reconcile-and-verify pass. Any genuine regression fix touches only 55.10-owned files in a `fix(55.10): ...` commit with staged-index proof.

## Ownership boundary

- ALLOWED: `mine-flow-STEP-55.10-FINDINGS.md` (dated reconciliation section); 55.10-owned `lib/` (privacy/shell/logger/settings/header) + tests **only if** a regression is proven.
- FORBIDDEN: inventing privacy/legal copy or labelling it approved; closing RISK-0025; editing `app_interaction_primitives.dart` (route regressions to owner), reporting dialog, other features, `STEP-index.md`.

## Tests and verification

- `flutter test test/features/auth/presentation/privacy_ack_page_test.dart test/core/utils/logger_test.dart test/app/app_shell_test.dart`
- Re-derive the honest **full** suite count on the current tree: `flutter test test/` → record `N passed / M skipped / K failed` exactly (audit on 2026-09-21 measured **780 passed / 5 skipped / 1 failed**, the one failure being the untracked `m2_challenger_stress_test.dart` overflow — see the 55.11 residual; the committed tree is green). State the number honestly, do not round to a legacy "682".
- `flutter analyze` (expect 0). Never print secrets; if any raw header value appears in output, stop and escalate.

## Boundaries and escalation

No fabricated legal copy, no editable role, no auth weakening, no secret logging, no sixth tab. Escalate on any raw secret in output, an authorization bypass, privacy-authority ambiguity, or repeated failure.

## Definition of done

FINDINGS corrected so the false "100% green" is superseded by the honest current state (defect introduced → fixed → cited); §4.9 privacy/redaction/shell/identity obligations re-verified on the current tree; privacy-copy approval carried as explicit `Unverified` release blocker; RISK-0025 confirmed open and noted; focused/static gates green.

## Next

Report the exact replacement evidence-cell line for STEP-index row 55.10 and whether it is flippable to **Done-with-recorded-Unverified** (privacy-copy approval + RISK-0025 carried). Do **not** flip it yourself. Hand off to the 55.11 close residual.


---

## E2E residual routed from 55.11 (2026-09-23) — deep-link `/teams/daily-log` resolves to `/teams`

**Source:** CI run `35894532969` at app head `fe17e2d`.
**Failure:** `deep_link_journey_test.dart:148` — `expect(appRouter.state.matchedLocation, route)` fails: `Expected '/teams/daily-log', Actual '/teams'`. Web + Android.

The journey deep-links each `_shellRoutes` entry (`:46-63`) via `appRouter.go(route)` and asserts the router settled on that exact location with the shell mounted. `AppRoutes.dailyLog` (`/teams/daily-log`) lands on `/teams` instead — the daily-log child route under `teams` (`router.dart:697` path `daily-log`, name `daily-log`) is not matching on a direct URI load, or a redirect is bouncing it up to the `teams` landing page.

**Investigate:** the `redirect` in `router.dart:129` (privacy-gate + auth) and the `teams`→`daily-log` nested `GoRoute` registration. Confirm a cold `go('/teams/daily-log')` resolves to the daily-log screen and does not fall back to the `teams` GroupLandingPage. This is a routing/route-binding fix, not a finder swap. (Note: the daily_log *content* visibility failure is separately routed to 55.6; this item is purely the URL-resolution/shell-persistence assertion.)

**Scope:** shell/route binding, `lib/app/router.dart` + `lib/features/**` routing. Re-run `flutter test integration_test/journeys/deep_link_journey_test.dart` (credential-gated; verified in CI).
