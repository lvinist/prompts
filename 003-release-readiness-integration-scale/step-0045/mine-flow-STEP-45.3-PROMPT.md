# mine-flow — STEP-45.3: Auth & session E2E journey

**Recommended model:** Gemini 3.1 Pro (defines the reusable journey pattern + `loginAsStagingUser`; security-adjacent).

> **How to run:** *"run substep 45.3"*. Self-contained; runnable cold.

## Context

Third substep of STEP-45; first feature journey. Uses the harness from 45.1. All later journeys
(45.4–45.14) depend on this because they log in first. Read
`Upcoming Prompts/mine-flow-STEP-45-PLAN.md`.

## Read these first
- `Upcoming Prompts/mine-flow-STEP-45-PLAN.md`.
- `integration_test/helpers/` (45.1) — `app_harness`, `staging_config`, `login_helper`.
- `Code/mine-flow-app/lib/features/auth/` — data/domain/presentation for login/session/logout.
- `Code/mine-flow-app/lib/app/router.dart` — route definitions, redirects, auth guard.
- STEP-46 findings `prompts/003-release-readiness-integration-scale/step-0046/mine-flow-STEP-46.3-FINDINGS.md` — CF-001..005 (auth foundation: no real auth, hardcoded creds prefill, logout doesn't signOut) — remediated in STEP-46; this journey confirms they hold at runtime.
- `Code/mine-flow-docs/architecture/16-identity-auth.md`, `06-security-threat-model.md`.

## Scope

Owns: `integration_test/journeys/auth_journey_test.dart` and any `login_helper` completion needed
for real staging sign-in. Does **not** touch the per-role RLS matrix (that's 45.12).

## Your task

Write an E2E journey that, against staging:
1. **Real login** — enter valid staging credentials, submit, land on the dashboard. Assert the
   session token is stored (secure storage) and the user identity is the signed-in user, not a
   hardcoded default (guards CF-002/CF-005).
2. **Session restore** — relaunch the app (re-pump harness) and assert the session persists without
   re-login.
3. **Logout** — trigger logout, assert `signOut` was actually called and the session/token is
   cleared and the app returns to login (guards CF-004).
4. **Invalid login** — wrong credentials surface an error state, no session created (guards CF-003).

Target `EditableText` finders (RISK-0009). Complete `loginAsStagingUser(tester, role)` so later
journeys reuse it. If staging creds are absent, mark the journey **Unverified** with the reason.

## Verification
- `flutter test integration_test/journeys/auth_journey_test.dart -d chrome --dart-define=...` passes (or Unverified w/ reason); also run on `Pixel_6a` if booted.
- `flutter analyze` 0 issues; format clean.
- Name the test file; commit on the STEP-45 branch.

## Keeping the docs true (always)
- If auth runtime behavior diverges from `architecture/16-identity-auth.md`, note for 45.15 and
  update the doc (Version Log) or raise an ADR.

## Definition of done
- [ ] Auth journey covers login / session-restore / logout / invalid-login and passes (or Unverified w/ reason).
- [ ] `loginAsStagingUser` helper complete and reused-ready.
- [ ] analyze 0 / format clean; new files documented.

## Next
Run substep 45.4 (Attendance & Daily Logging E2E) in a fresh chat.
