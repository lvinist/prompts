# mine-flow — STEP-48.1: Journey-Integrity Repair Audit (no fake greens)

> **How to run:** tell your agent *"run substep 48.1"*. Self-contained — runnable cold.

**Assigned model: Claude Opus 4.8.** This is one of only three substeps in STEP-48 that justify the
heaviest tier, and the reason is the nature of the work: you are deciding, file by file, whether an
assertion is real evidence or theatre. The easy path — editing a test until it goes green — launders a
regression into a passing suite, which is exactly how STEP-45 produced fifteen `Done` rows over zero
evidence. Q4's rule (app-contradicts-doc = bug; doc-stale = drift) requires a judgement call on nearly
every conflict you find. Be adversarial about your own output; the rest of the STEP rests on this
substep being right.


## Context

Read `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` first, then
`Upcoming Prompts/mine-flow-STEP-48.0-FINDINGS.md` (this substep requires **GATE: PASSED**).

STEP-45 authored fifteen `integration_test` files. Eleven carry real assertions. **Four do not,
and one of those is actively dangerous:**

| File | Problem |
|---|---|
| `integration_test/journeys/deep_link_journey_test.dart` | Its second test prints "Unverified…" and then asserts `expect(true, isTrue)` with the comment *"We pass the test gracefully to allow CI to proceed"*. This is a **fake green** — the instant 48.2 points CI at this file, it reports a pass for work that was never done. |
| `integration_test/journeys/data_bucket_journey_test.dart` | Zero assertions. Body is a comment list and `// Stub for the rest of the journey`. |
| `integration_test/journeys/rls_authorization_journey_test.dart` | Zero assertions. The single-user path — the only path that can run — does nothing but `markTestSkipped`. |
| `integration_test/helpers/login_helper.dart` | Docstring: *"Roles are wired in 45.12; currently stubbed to use the default staging credentials."* |

This substep is the firewall between STEP-48 and a repeat of STEP-45. Before a single journey is
run for evidence, every file must be incapable of reporting a pass it did not earn.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — the honesty gate in "Ground rules", and Q4.
- `Upcoming Prompts/mine-flow-STEP-48.0-FINDINGS.md` — credentials, seed state, host state.
- root `.throughstone/local-user.md` — Experience level 2, Explanatory.
- `Code/mine-flow-docs/architecture/12-test-strategy.md` v1.2 — the E2E tier's intent.
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` — the canonical UI contract. You
  need it for Q4: when a test's expectation and the app disagree, this doc decides who is wrong.
- `Code/mine-flow-docs/coding-standards/README.md` — docstrings on everything you write.
- `Code/mine-flow-app/README.md`, `Code/mine-flow-app/integration_test/helpers/*.dart`.
- `Code/mine-flow-docs/registries/risks.yml` — **RISK-0009**: finders must target
  `find.byType(EditableText)`, never `TextField` (flutter/flutter#191095 under forui 0.26).

## Scope

**In scope:** auditing all 16 files under `integration_test/` (15 journeys + `app_boots_test.dart`)
plus the 4 helpers for placeholder assertions, pass-by-default paths, and stubbed bodies;
repairing them so each either asserts something real or skips honestly; completing the
`login_helper` role wiring if 48.0 produced per-role accounts.

**Not in scope:** running the journeys for evidence (48.3–48.12 own that), CI workflow edits
(48.2), the design review (48.13), risk rows (48.14), doc edits (48.15). **Google Drive is out
of STEP-48's scope entirely** (PLAN decision D2) — `data_bucket_journey_test.dart` is made
*honest*, not *complete*.

## Your task

### 1. Audit every file for dishonest paths

Read all 16 test files and all 4 helpers. For each, record in your findings:

- assertion count and whether the assertions are meaningful (`expect(true, isTrue)`,
  `expect(1, 1)`, or asserting on a literal you just wrote are **not** meaningful);
- whether there is any path that reaches the end of the test body without asserting anything;
- whether `markTestSkipped` is followed by `return` (correct) or by code that then passes anyway;
- whether finders use `TextField` anywhere (RISK-0009 violation) instead of `EditableText`;
- whether the file has a `// Stub` / `// If credentials were provided, we would:` body.

Grep helpers to start from, then read the files — do not rely on grep alone:

```bash
cd Code/mine-flow-app
grep -rn "expect(true\|expect(1, 1\|isTrue)" integration_test/
grep -rn "Stub\|we would:\|TODO\|placeholder" integration_test/
grep -rn "byType(TextField)" integration_test/
grep -rln "markTestSkipped" integration_test/
```

### 2. Fix `deep_link_journey_test.dart` — the fake green

Delete the `expect(true, isTrue)` pass-by-default. Replace that second test with either:

- **a real deep-link test** — direct-load and reload of each top-level route and one `:id` route,
  asserting the route resolves and the app shell (sidebar) persists, plus the auth-redirect
  behaviour; or
- **an honest gated skip** — `if (!isStagingConfigured) { markTestSkipped('Unverified: <reason> —
  supply SUPABASE_URL / SUPABASE_ANON_KEY / TEST_USER_EMAIL / TEST_USER_PASSWORD via
  --dart-define'); return; }` followed by the real body.

Since 48.0 has produced credentials, **write the real body.** Substep 48.11 owns *running* it and
closing RISK-0006; your job is that the file contains a genuine test. Note that the first test in
that file (`'Deep link to unauthenticated route redirects to login'`) calls `app.main()` directly
rather than the `pumpApp` harness and asserts `find.text('Login')` — check that against the actual
login screen, which uses the Indonesian label `'Masuk'` (see `auth_journey_test.dart`). If
`'Login'` does not appear in the widget tree, that assertion is broken and would fail for the
wrong reason; fix it to match the real UI.

### 3. Make `data_bucket_journey_test.dart` honest

Drive credentials are **deliberately out of scope** (D2), so this journey cannot be completed.
Make it correct anyway:

- keep the gated skip, but make the reason specific and actionable — name
  `GOOGLE_DRIVE_SERVICE_ACCOUNT_EMAIL` / `GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY`, cite RISK-0017 and
  RISK-0018, and state that STEP-48 deliberately defers them;
- remove the unreachable `pumpApp` / `loginAsStagingUser` calls sitting after the guard with a
  `// Stub for the rest of the journey` comment — dead code that looks like coverage;
- **if** any part of the data-bucket flow can be exercised without Drive (navigating to the
  bucket screen, listing existing `geospatial_files` rows from staging, the file-picker
  validation path, the 50 MB client-side limit check), split the file the way
  `offline_sync_journey_test.dart` does: **Part A** gated on Drive, **Part B** unconditional
  against staging. That converts a zero-evidence file into partial real evidence. Recommended.

### 4. Make `rls_authorization_journey_test.dart` honest for the single-user case

Currently: no per-role accounts → `markTestSkipped` → zero evidence. Restructure:

- **Part A (per-role matrix)** — keep gated on `hasPerRoleAccounts`. If 48.0 created the three
  accounts, this now runs; if not, it skips with a specific reason naming the four
  `TEST_FOREMAN_*` / `TEST_SUPERVISOR_*` defines.
- **Part B (single-user, unconditional when `isStagingConfigured`)** — assert what one
  authenticated user genuinely proves: that RLS is *on*, that reads permitted by the user's role
  succeed, and that at least one operation the role must **not** be allowed to perform is refused
  with a `PostgrestException` (code `42501` or a policy message). Read
  `supabase/migrations/20260718000002_rls_policies.sql` and pick a denial that is unambiguous for
  the role 48.0 assigned.

Note the existing Part A bug: its foreman-delete check wraps the call in `try/catch` and does
**nothing** if no exception is thrown — so an RLS hole would pass silently. Assert the denial
positively (`expect(() async => …, throwsA(isA<PostgrestException>()))` or equivalent), do not
merely log when it happens.

### 5. Complete `login_helper.dart`

`loginAsStagingUser(tester, role:)` already branches on `hasPerRoleAccounts`. Verify it against
the accounts 48.0 actually created:

- if all three exist, remove the "currently stubbed" docstring and confirm each role's define
  pair is read correctly;
- if only the shared user exists, keep the fallback but make the docstring **state the truth** —
  that `role:` is accepted and ignored, so no caller mistakes a `role: 'foreman'` call for
  role-specific coverage.

Also confirm the helper's early `if (!isStagingConfigured) return;` cannot make a caller think a
login succeeded. A silent return that leaves the test on the login screen, followed by
assertions that happen to pass, is the same class of defect as a fake green. Consider making it
throw or requiring callers to guard first.

### 6. Sweep the remaining eleven journeys

They have real assertions but have never run, so treat them as unproven. For each, check:

- RISK-0009 compliance (`EditableText`, not `TextField`);
- Indonesian UI labels — the app's buttons are labelled `'Masuk'`, etc.; an assertion on an
  English string will fail for the wrong reason;
- STEP-46 moved a great deal of UI (97 findings remediated) and STEP-38 extracted
  `AttendanceFormPage` to a standalone route. Assertions written before those changes may target
  screens that no longer exist.

**Apply Q4's rule when a test and the app disagree:** if the app contradicts
`architecture/07-ui-design-system.md`, that is a **bug** — record it as a finding and hand it to
the owning journey substep; if the doc is stale, that is doc drift and belongs to 48.15. **Do not
silently rewrite an assertion to match whatever the app currently does** — that launders a
regression into a green test.

You may make mechanical corrections here (wrong finder type, wrong string literal, a screen that
moved). Anything requiring a judgement call about correct behaviour goes in the findings file for
its journey substep to decide with real runtime output in hand.

### 7. Write the findings file

`Upcoming Prompts/mine-flow-STEP-48.1-FINDINGS.md`:

- a per-file table: 20 rows (16 tests + 4 helpers) with assertion count, verdict
  (`clean` / `repaired` / `honest-skip` / `needs-runtime-decision`), and what changed;
- every fake-green or stub removed, named explicitly;
- the list of expectation-vs-app conflicts handed forward, each tagged with its owning substep;
- confirmation that no file can now report a pass without asserting something real.

## Verification

- `grep -rn "expect(true" integration_test/` returns **nothing**.
- `grep -rn "byType(TextField)" integration_test/` returns nothing.
- No test body reaches its end without either an assertion or a `markTestSkipped` + `return`.
- `flutter analyze` → 0 issues.
- `dart format --set-exit-if-changed .` → clean.
- `flutter test` → still green (448 passing as of STEP-47; the
  `test/integration/attendance_daily_log_sync_test.dart` Hive `setUpAll` flake is known —
  re-run it in isolation to confirm flake, and say so; never wave a red suite through).
- The journeys are **not** run for evidence here. If you run one while iterating, label the
  output as iteration, not evidence — CI on the branch head is authoritative (PLAN decision D1).

## Keeping the docs true

Repairing tests should not change an architecture decision. If it does — for example if the
single-user RLS Part B reveals that the policies do not behave as
`architecture/06-security-threat-model.md` describes — **do not edit the doc here**. Record it and
hand it to 48.12 (for the finding) and 48.15 (for the doc). New/changed functions get docstrings
per `coding-standards/README.md`. Any deferral you create or make explicit goes to 48.14, which
owns `registries/risks.yml`.

## Definition of done

- [ ] All 16 test files and 4 helpers audited, results tabulated in the findings file.
- [ ] `deep_link_journey_test.dart`'s `expect(true, isTrue)` fake green **removed** and replaced
      with a real gated test body.
- [ ] `data_bucket_journey_test.dart` honest: specific skip reason citing RISK-0017/0018, dead
      post-guard code removed, Part B added if any non-Drive coverage is possible.
- [ ] `rls_authorization_journey_test.dart` restructured into gated Part A + unconditional
      single-user Part B; the silent-pass `try/catch` denial check asserts positively.
- [ ] `login_helper.dart` role wiring completed or its limitation stated truthfully in the
      docstring; no path lets a caller mistake a skipped login for a successful one.
- [ ] Remaining eleven journeys swept for RISK-0009 finders, Indonesian labels, and
      post-STEP-38/46 screen changes; judgement calls handed forward, not silently rewritten.
- [ ] `flutter analyze` 0 issues, `dart format` clean, `flutter test` green (flake diagnosed).
- [ ] `Upcoming Prompts/mine-flow-STEP-48.1-FINDINGS.md` written.
- [ ] Committed on `step-0048-runtime-evidence` with a message naming the substep.

## Next

Tell the user the next action is *"run substep 48.2"* (CI gate expansion + evidence artifacts) in
a **fresh chat**, and update 48.1's status in the STEP PLAN.
