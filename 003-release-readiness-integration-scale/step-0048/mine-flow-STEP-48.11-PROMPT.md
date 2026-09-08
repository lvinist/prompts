# mine-flow — STEP-48.11: Deep-Link Validation & RISK-0006 (settles 45.13)

> **How to run:** tell your agent *"run substep 48.11"*. Self-contained — runnable cold.

**Assigned model: Gemini 3.1 Pro High.** Route enumeration and per-route verification is systematic
work with `router.dart` as ground truth. The judgement that matters is the harness-limitation statement:
an in-process driver is not a cold browser load, and RISK-0006 must not be closed on evidence that
overstates what was proven. **Escalate to Opus 4.8** if a route loses its shell or fails to resolve
(a real go_router v18 regression affecting a whole class of routes), or if you cannot decide between
closing RISK-0006 and narrowing it.


## Context

Read `Upcoming Prompts/mine-flow-STEP-48-PLAN.md`, then the 48.0/48.1/48.2 findings,
`mine-flow-STEP-48.3-FINDINGS.md`, and `mine-flow-STEP-48.7-FINDINGS.md` (its NR-006 work overlaps
this substep — reuse its conclusions rather than re-deriving them). **48.1 and 48.3 must both be
complete**: 48.1 owned removing this file's fake green, 48.3 owned auth.

STEP-45 row 45.13: `Deferred — deep_link_journey_test.dart authored; RISK-0006 remains open (E2E
unverified) → STEP-48`.

**RISK-0006** (`open`, medium) is the row to settle: *"go_router upgraded to v18; route API changes
audited (E2E unverified)"*. Its description records that go_router went ^15.1.2 → ^17.3.0 in
STEP-43 and → ^18.0.0 in STEP-47.1, that v16→v17 breaking changes were limited to `ShellRoute`
observer notification behaviour (the new `notifyRootObserver` property), and that *"Full E2E
deep-link validation was attempted in STEP-45.13 but remains unverified because staging credentials
are absent."* Its mitigation reads *"Integration test stub created in STEP-45.13; will skip until
creds are provided"* and its revisit trigger is *"Before production release, when staging
credentials are available."* Both conditions are now met.

**What this file was.** Before 48.1 repaired it, `deep_link_journey_test.dart` contained the worst
artefact in the suite: a test that printed "Unverified…" and then asserted `expect(true, isTrue)`,
commented *"We pass the test gracefully to allow CI to proceed, noting the gap in RISK-0006."* If
48.1's findings do not confirm that is gone, **stop and fix it before anything else** — the whole
point of STEP-48 is that this pattern never ships again.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — honesty rule, D1.
- `…-48.0/1/2/3-FINDINGS.md` and `…-48.7-FINDINGS.md`.
- root `.throughstone/local-user.md` — Experience level 2, Explanatory.
- `Code/mine-flow-docs/registries/risks.yml` — **RISK-0006** verbatim.
- `Code/mine-flow-docs/adr/ADR-0018-*` — the STEP-47 dependency posture that took go_router to v18.
- `Code/mine-flow-docs/architecture/03-architecture-overview.md`,
  `architecture/07-ui-design-system.md` — the shell/navigation contract.
- `Code/mine-flow-docs/architecture/16-identity-auth.md` — the auth redirect rules a deep link must
  respect.
- `Code/mine-flow-app/integration_test/journeys/deep_link_journey_test.dart` (post-48.1).
- `Code/mine-flow-app/lib/app/router.dart` — every route, `AppRoutes`, the shell branches, the
  redirect logic. Enumerate the routes from here; do not guess them.
- `Code/mine-flow-app/lib/app/presentation/pages/app_shell.dart`.

Route history to keep in mind: **STEP-38.5** corrected the Benchmark route to
`/operations/benchmark-db`, added the sidebar entry, and title-cased breadcrumb segments.
**STEP-38.6** extracted `AttendanceFormPage` to a standalone `/teams/attendance/form` route. Route
groups are `/operations`, `/teams`, `/tools`.

## Scope

**In scope:** validating deep-link behaviour across **all** top-level routes and each `:id` route;
confirming shell persistence and auth-redirect behaviour; producing the evidence that closes or
re-justifies RISK-0006.

**Not in scope:** the benchmark form specifically (48.7 settled NR-006 — cite it, do not redo it),
the sidebar active-state finding NR-003/RISK-0016 (48.13 owns it, though your route work will inform
it), other feature areas, risk-row edits (48.14 applies them; you supply evidence and a
recommendation), docs (48.15).

## Your task

### 1. Enumerate the real route set

Read `lib/app/router.dart` and list every route: top-level, group (`/operations`, `/teams`,
`/tools`), and every `:id` parameterised route. Write the list into your findings. The test must
cover the routes that **exist**, not a remembered subset.

### 2. Verify each route deep-links correctly

For each route, prove three things:

1. **Resolves** — the intended screen renders, not a 404, an error page, or a silent redirect to a
   default.
2. **Shell persists** — `AppShell` (sidebar) is still in the tree for routes that belong inside it.
   This is the `ShellRoute` behaviour go_router v17 changed (`notifyRootObserver`), and it is
   precisely what RISK-0006 is about.
3. **Auth redirect** — unauthenticated access to a guarded route goes to login; after login the user
   lands somewhere sensible (ideally the originally requested route, if that is the documented
   intent — check `architecture/16-identity-auth.md` before asserting it).

For `:id` routes, use an id that actually exists in staging (from the seed, per 48.0) so a failure
means "routing is broken", not "the row is missing".

**Reload behaviour on web** matters most. Direct-load and, where the harness allows, reload each
route via `flutter drive`:

```bash
flutter drive --driver=test_driver/integration_test.dart \
  --target=integration_test/journeys/deep_link_journey_test.dart \
  -d web-server --browser-name=chrome --dart-define=…
```

### 3. State the harness's limits honestly

`integration_test` drives the app **in-process**, so `appRouter.go(...)` is not identical to a
browser cold-loading a URL. It is the closest achievable proxy and it does exercise the router's
redirect and shell logic — but it does not prove the web server serves that path or that a hard
refresh rehydrates state.

Say exactly which of the three checks above were proven by real navigation and which rest on the
in-process proxy. If a genuine cold load cannot be exercised, **that limitation goes in the findings
and in the RISK-0006 recommendation** — a narrowed, honest risk row is a better outcome than a
closure that overstates the evidence.

### 4. Check the first test's assertion

Before 48.1, the file's first test called `app.main()` directly (bypassing the `pumpApp` harness) and
asserted `find.text('Login')`. The login screen's button is labelled `'Masuk'` (Indonesian — see
`auth_journey_test.dart` and RISK-0004). If `'Login'` does not appear in the tree, that assertion
fails for the wrong reason. Confirm 48.1 fixed it; if not, fix it here and note it.

### 5. Triage honestly

Route drift from STEP-38.5/38.6 is a legitimate test fix. A route that genuinely fails to resolve or
loses the shell is a **real go_router v18 regression** — exactly what RISK-0006 predicted. Fix the
root cause in `router.dart`, check every sibling route for the same misconfiguration (this is a
class of bug, not a one-off), and add a regression test. Never delete an assertion to get green.

### 6. Authoritative CI evidence

Commit, push to `step-0048-runtime-evidence`, confirm the journey **executes and passes** in
`e2e-web` and `e2e-android`, and record the run URL plus real counts. Web is the important surface
here. (CI logs without `gh`: PAT from `git credential fill` as a Bearer token;
`/actions/jobs/<id>/logs` 302s to Azure Blob which rejects the auth header — follow `redirect_url`
bare.)

### 7. Record it, with a RISK-0006 recommendation

`Upcoming Prompts/mine-flow-STEP-48.11-FINDINGS.md`:

- the enumerated route list with a per-route result table (resolves / shell persists / auth redirect);
- journey verdict: Verified with URL + counts, or Deferred with a named blocker and trigger;
- an explicit **harness-limitation** statement;
- an explicit recommendation for 48.14: **close RISK-0006** (with evidence refs) or **re-justify**
  it with a narrowed description and a new trigger. Do not edit `risks.yml` yourself;
- any `ShellRoute` / `notifyRootObserver` observations, since that is the specific v17 change
  RISK-0006 flagged;
- anything useful to 48.13 about sidebar active-state on group routes (NR-003 / RISK-0016).

## Verification

- **No `expect(true, isTrue)` anywhere under `integration_test/`.** Verify with a grep and say so.
- Every route from `router.dart` covered, with a recorded result.
- Journey **executes** on both platforms in a CI run on the branch head, counts quoted; or an honest
  Deferred.
- Harness limitations stated; nothing claimed that the in-process driver cannot prove.
- `flutter analyze` → 0 issues; `dart format --set-exit-if-changed .` → clean.
- `flutter test` → green (the `attendance_daily_log_sync_test.dart` Hive flake is known: re-run
  isolated to confirm, and say so).
- Any router fix carries a regression test.
- No secret value in any log, report, or commit.

## Keeping the docs true

If the real route set differs from what `architecture/03-architecture-overview.md` or the router
documentation describes, hand it to 48.15 with the section and correction. If the auth-redirect
behaviour differs from `architecture/16-identity-auth.md`, decide which side is wrong and record it.
Docstrings on anything you write. Risk rows to 48.14.

## Definition of done

- [ ] Every route enumerated from `router.dart` and covered with a recorded per-route result.
- [ ] Resolution, shell persistence, and auth redirect each verified (or explicitly unproven with a
      reason) per route.
- [ ] Journey observed **executing** on both platforms in CI; verdict recorded with URL + counts.
- [ ] The `expect(true, isTrue)` fake green confirmed absent from the whole suite.
- [ ] Harness-limitation statement written — no overclaiming about cold browser loads.
- [ ] Explicit close-or-re-justify recommendation for **RISK-0006** written for 48.14.
- [ ] Any router regression root-caused, sibling routes checked, regression test added.
- [ ] `flutter analyze` 0 issues, `dart format` clean, `flutter test` green (flake diagnosed).
- [ ] `Upcoming Prompts/mine-flow-STEP-48.11-FINDINGS.md` written.
- [ ] Committed on `step-0048-runtime-evidence`.

## Next

Tell the user the next action is *"run substep 48.12"* (live RLS evidence) in a **fresh chat**, and
update 48.11's status in the STEP PLAN.
