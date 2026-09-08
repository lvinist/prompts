# mine-flow — STEP-48.3: Auth & Session Runtime Evidence (settles 45.3)

> **How to run:** tell your agent *"run substep 48.3"*. Self-contained — runnable cold.

**Assigned model: Gemini 3.1 Pro High.** The gating journey. It has a written authority to check
against (`architecture/16-identity-auth.md`, `architecture/06-security-threat-model.md`), so the
judgement is bounded — but it is the first live exercise of `flutter_secure_storage` v11 (RISK-0008)
and it touches session tokens. **Escalate to Opus 4.8** immediately if a failed login leaves any token
behind, if session restore misbehaves in a way that could indicate a v11 key-migration problem, or if
you cannot classify a failure as test-defect vs app-defect. Security-shaped results are an escalation
trigger by default, not a judgement call to make alone.


## Context

Read `Upcoming Prompts/mine-flow-STEP-48-PLAN.md`, then the findings from 48.0 (credentials),
48.1 (journey repairs), and 48.2 (CI targets + the per-journey triage table from the first real
CI run).

This is the **gating journey**. Every other journey calls `loginAsStagingUser`, so until auth is
proven at runtime, no other evidence is trustworthy. STEP-45's index row 45.3 reads
`Deferred — auth_journey_test.dart authored & committed; never run against staging (no
credentials) → STEP-48`. This substep settles it.

`integration_test/journeys/auth_journey_test.dart` is the best-formed of the fourteen: 16
assertions, no stubs, and it covers invalid login, real login, session restore across a re-pump,
and logout with session clearing. It asserts against `SecureStorageService` directly as well as
the widget tree, so it proves persistence, not just navigation.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — the honesty rule; decision D1 (CI authoritative).
- `Upcoming Prompts/mine-flow-STEP-48.0-FINDINGS.md`, `…-48.1-FINDINGS.md`, `…-48.2-FINDINGS.md`.
- root `.throughstone/local-user.md` — Experience level 2, Explanatory.
- `Code/mine-flow-docs/architecture/16-identity-auth.md` — the auth model this journey must match.
- `Code/mine-flow-docs/architecture/06-security-threat-model.md` — session handling, token storage.
- `Code/mine-flow-docs/architecture/12-test-strategy.md` v1.2 — E2E tier and gates.
- `Code/mine-flow-app/integration_test/journeys/auth_journey_test.dart` and
  `integration_test/helpers/{app_harness,login_helper,staging_config}.dart`.
- `Code/mine-flow-app/lib/features/auth/` — `AuthCubit`, `AuthState`, the repository.
- `Code/mine-flow-app/lib/core/security/secure_storage_service.dart`.
- `Code/mine-flow-docs/registries/risks.yml` — **RISK-0008** (flutter_secure_storage v9→v11 skip,
  `monitoring`): this journey is the first real exercise of v11 key handling against a live
  backend. If session restore misbehaves, RISK-0008 is a prime suspect. **RISK-0009** — finders
  target `EditableText`, never `TextField`.

## Scope

**In scope:** running `auth_journey_test.dart` against staging on both platforms until it passes
or a real defect is identified and fixed; recording the evidence.

**Not in scope:** other journeys (48.4–48.12), the design review (48.13), risk-register edits
(48.14), doc edits (48.15). Do not repair unrelated journeys you happen to notice — note them and
move on.

## Your task

### 1. Run it locally first, to iterate

```bash
cd Code/mine-flow-app
flutter test integration_test/journeys/auth_journey_test.dart -d emulator-5554 \
  --dart-define=SUPABASE_URL="$SUPABASE_URL" \
  --dart-define=SUPABASE_ANON_KEY="$SUPABASE_ANON_KEY" \
  --dart-define=TEST_USER_EMAIL="$TEST_USER_EMAIL" \
  --dart-define=TEST_USER_PASSWORD="$TEST_USER_PASSWORD" \
  --dart-define=APP_ENV=staging
```

Values come from your shell environment — never inline a literal secret into a command that lands
in a log or a file.

Web iteration uses `flutter drive` (`flutter test … -d chrome` is unsupported on 3.47.x):

```bash
flutter drive --driver=test_driver/integration_test.dart \
  --target=integration_test/journeys/auth_journey_test.dart \
  -d web-server --browser-name=chrome --dart-define=…
```

### 2. Triage what happens, honestly

Three outcomes, three responses:

- **Passes.** Good — but confirm it *executed*. `~1` / "1 skipped" is not a pass. Quote the real
  counts.
- **Fails on a test defect** — a stale finder, an English label where the UI says `'Masuk'`, a
  timing issue needing `pumpAndSettle`. Fix the test. Record what was wrong and why the fix is a
  test fix, not a behaviour change.
- **Fails on a real app defect.** This is a finding. Fix the **root cause**, check sibling call
  paths for the same flaw, and add a regression test at the cheapest tier that catches it
  (usually a widget or unit test under `test/`, not only the E2E). Do not weaken the E2E
  assertion to get green — deleting an assertion is the same offence as fabricating evidence.

Watch specifically for:

- **Session restore.** The test re-pumps the app and expects the session to survive. On a live
  backend this exercises `flutter_secure_storage` v11 key handling (RISK-0008) and Supabase token
  refresh. A failure here is significant, not cosmetic.
- **Invalid login.** It asserts the app stays on the login screen and no token is stored. If a
  failed login leaves any token behind, that is a **security finding** — escalate it in your
  findings and reference `architecture/06-security-threat-model.md`.
- **`storage.clearAll()` at test start.** Confirm this does not clobber anything the user cares
  about on a real device. On the emulator it is fine; note it if a physical device is ever used.

### 3. Get the authoritative CI evidence

Local runs are iteration only (PLAN decision D1). Commit and push to
`step-0048-runtime-evidence`, then confirm `e2e-web` and `e2e-android` both **execute** this
journey and report it passing. Record the run URL, job names, and the executed/skipped/failed
counts verbatim.

CI logs without `gh`: the PAT is in Git Credential Manager (`printf
'protocol=https\nhost=github.com\n\n' | git credential fill`) and works as a Bearer token;
`/actions/jobs/<id>/logs` 302s to Azure Blob, which rejects the GitHub auth header — capture the
`redirect_url` and fetch it bare.

### 4. Record the evidence

`Upcoming Prompts/mine-flow-STEP-48.3-FINDINGS.md`:

- verdict: **Verified** (with CI run URL + counts, per platform) or **Deferred** (with the
  blocking reason and a revisit trigger). Nothing in between.
- every defect found, classified test-defect vs app-defect, with the fix and its regression test;
- any security-relevant observation (token left behind, session not cleared on logout);
- whether RISK-0008's v11 key handling behaved correctly against a live backend — this is the
  first real evidence either way, and 48.14 needs it.

## Verification

- `auth_journey_test.dart` **executes** on both platforms in a single CI run on the branch head,
  with counts quoted. Or an honest Deferred with a named blocker.
- `flutter analyze` → 0 issues; `dart format --set-exit-if-changed .` → clean.
- `flutter test` → green. The `test/integration/attendance_daily_log_sync_test.dart` Hive
  `setUpAll` flake is known: it fails intermittently full-suite and is green in isolation. Re-run
  it isolated to confirm flake, and say so. Never wave a red suite through.
- Any app fix carries a regression test at the appropriate tier.
- No secret value in any log, report, or commit.

## Keeping the docs true

If runtime auth behaviour differs from `architecture/16-identity-auth.md` or
`architecture/06-security-threat-model.md`, **do not edit the doc here**. Decide which side is
wrong: app contradicts a correct doc → a bug, fix it and record the finding; doc is stale → hand
it to 48.15 with the specific section and what it should say. New/changed functions get
docstrings (`coding-standards/README.md`). Deferrals and risk updates go to 48.14.

## Definition of done

- [ ] Journey observed **executing** (not skipping) against staging on Android and web in CI.
- [ ] Verdict recorded: Verified with run URL + counts, or Deferred with a named blocker and a
      revisit trigger.
- [ ] Every defect classified and fixed at its root cause; regression tests added.
- [ ] Any security-relevant observation escalated explicitly.
- [ ] RISK-0008's live-backend behaviour recorded for 48.14.
- [ ] `flutter analyze` 0 issues, `dart format` clean, `flutter test` green (flake diagnosed).
- [ ] `Upcoming Prompts/mine-flow-STEP-48.3-FINDINGS.md` written.
- [ ] Committed on `step-0048-runtime-evidence`.

## Next

48.4, 48.5, 48.6, 48.7, 48.8, 48.9, 48.10, and 48.12 all depend on this substep and are otherwise
independent of each other. Tell the user the next action is *"run substep 48.4"* in a **fresh
chat**, note that the feature-area substeps can be run in any order once auth is green, and update
48.3's status in the STEP PLAN.

**If auth could not be verified, stop.** Every other journey logs in first; running them would
produce a cascade of failures with a single root cause. Tell the user plainly and leave the
remaining substeps unstarted.
