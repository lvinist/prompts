# mine-flow — STEP-48.12: Live RLS Evidence, Single-User Scope (settles 45.12)

> **How to run:** tell your agent *"run substep 48.12"*. Self-contained — runnable cold.

**Assigned model: Gemini 3.1 Pro High.** Security-adjacent but well-bounded: the policy file states
exactly what each role may do, so the right assertion is determinable by reading it. The care needed is
in asserting a **refusal** positively and in stating the partial-vs-full boundary precisely. **Escalate
to Opus 4.8** if an operation the policy forbids actually **succeeds** — that is a security defect and
its handling (no ad-hoc policy edits, a dedicated remediation STEP) is not this substep's call — or if
you are unsure whether the single-user evidence is strong enough to update the S0 report's row as
anything other than partial.


## Context

Read `Upcoming Prompts/mine-flow-STEP-48-PLAN.md`, then the 48.0 findings (**which accounts and
roles actually exist** — that determines this substep's whole scope), 48.1 (which restructured this
journey), 48.2, and 48.3.

STEP-45 row 45.12: `Deferred — rls_authorization_journey_test.dart authored; no per-role staging
accounts; STEP-44 S0 deferred row updated to Unverified → STEP-48 (partial: single test user only)`.

This substep has **two obligations**, not one:

1. Produce whatever live RLS evidence the available accounts allow.
2. **Update the STEP-44 S0 security report's deferred row in place.** That report
   (`Code/mine-flow-docs/reports/security/2026-08-26-step-0044-s0-security-baseline-report.md`,
   line ~46) contains this row:

   > *Live RLS behavior test (via integration tests) — Unverified (STEP-45.12): test written
   > (`rls_authorization_journey_test.dart`) but skipped because per-role staging credentials
   > (`TEST_FOREMAN_EMAIL`, etc.) were not provided. Cannot verify full matrix (users, zones,
   > attendance_records, etc.) for foreman/supervisor roles. — Owner: STEP-45 owner — Test passes
   > when staging credentials are supplied*

   Archived reports are normally immutable, but a security report's **deferred row** is explicitly
   designed for the consuming STEP to update with the live result. This is the one in-place edit
   STEP-48 is authorised to make. Update that row and nothing else in that report.

That same S0 report also records, at "Area Detail: RLS / Authorization Behavior (44.2)", that **all
9 tables** carry RLS (`users`, `zones`, `attendance_records`, `equipment_checks`, `daily_logs`,
`cut_fill_records`, `land_clearing_records`, `inventory_items`, `geospatial_files`) and that a
static review found **no coverage gaps**. So the static side is done; what has never happened is
anyone observing a policy actually refuse an unauthorised operation at runtime.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — honesty rule, D1, **Q1** (per-role accounts).
- `…-48.0-FINDINGS.md` — the authoritative answer to Q1 and the role assigned to each account.
- `…-48.1-FINDINGS.md` — how this journey was restructured (Part A gated on `hasPerRoleAccounts`,
  Part B unconditional single-user) and the silent-pass `try/catch` fix.
- root `.throughstone/local-user.md` — Experience level 2, Explanatory.
- **`Code/mine-flow-docs/reports/security/2026-08-26-step-0044-s0-security-baseline-report.md`** —
  the whole RLS section, and the deferred row you must update.
- `Code/mine-flow-docs/architecture/06-security-threat-model.md` — the authorization model.
- `Code/mine-flow-docs/architecture/16-identity-auth.md` — roles and session handling.
- **`Code/mine-flow-app/supabase/migrations/20260718000002_rls_policies.sql`** — read it fully.
  `public.current_user_role()` reads `public.users.role`; the enum is
  `('supervisor', 'foreman', 'crew')`. Policies differ sharply: supervisors get broad access,
  foremen get scoped write access, crew are largely restricted to their own rows.
- `Code/mine-flow-app/integration_test/journeys/rls_authorization_journey_test.dart`.
- `Code/mine-flow-docs/registries/risks.yml` — RISK-0013 (S0 operations cluster), RISK-0010
  (staging provisioned via ClickOps).

## Scope

**In scope:** running the RLS journey with the accounts that exist; asserting at least one genuine
policy **refusal** at runtime; updating the S0 report's live-RLS deferred row; recommending what
stays deferred.

**Not in scope:** writing new RLS policies or migrations (a policy gap would be a finding and its own
STEP), other feature areas, the design review (48.13), `risks.yml` edits (48.14 applies them; you
supply evidence and a recommendation), other doc edits (48.15).

## Your task

### 1. Establish what is actually testable

From 48.0's findings, determine which accounts exist and what role each carries in `public.users`.
Two cases:

- **All three roles exist** → the full matrix is in scope. Run Part A. This is the good outcome and
  it lets a long-deferred security gate close properly.
- **Only a shared user exists** → the matrix stays **partial**. Part A skips honestly; Part B carries
  the whole burden. Say so explicitly and recommend the deferral in your findings.

Confirm each account's `public.users.role` value directly — an auth user without a matching
`public.users` row fails every policy check, and that failure looks exactly like an RLS bug.

### 2. Run the journey

```bash
cd Code/mine-flow-app
flutter test integration_test/journeys/rls_authorization_journey_test.dart -d emulator-5554 \
  --dart-define=SUPABASE_URL="$SUPABASE_URL" --dart-define=SUPABASE_ANON_KEY="$SUPABASE_ANON_KEY" \
  --dart-define=TEST_USER_EMAIL="$TEST_USER_EMAIL" --dart-define=TEST_USER_PASSWORD="$TEST_USER_PASSWORD" \
  --dart-define=APP_ENV=staging
  # plus the four TEST_FOREMAN_* / TEST_SUPERVISOR_* defines if those accounts exist
```

Secrets from the shell environment only.

### 3. Assert a refusal, positively

**This is the crux.** Proving reads succeed proves almost nothing about RLS — an unprotected table
also lets reads succeed. The evidence that matters is a **denial**: an operation the role must not be
permitted, refused by the database.

The original Part A wrapped its foreman-delete check in `try/catch` and did **nothing** if no
exception was thrown — meaning an RLS hole would have passed silently. 48.1 was asked to fix that.
Verify the fix and assert positively:

```dart
await expectLater(
  () => client.from('<table>').delete().eq('id', '<some-id>'),
  throwsA(isA<PostgrestException>()),
);
```

Pick the denial from `20260718000002_rls_policies.sql` that is **unambiguous** for the role you are
authenticated as. Check the exception carries a policy-related code (`42501`) or message rather than
failing for an unrelated reason such as a bad id or a network error — a test that passes because the
row did not exist proves nothing.

If an operation that policy forbids **succeeds**, that is a **security defect**: report it
prominently, do not fix policies ad hoc in this substep (a policy change needs its own migration and
review), and recommend a dedicated remediation STEP.

### 4. State precisely what one user proves

If the matrix is partial, be exact about the boundary. Something like: *"Verified: RLS is enforced
for role X on tables A, B, C — reads permitted by policy succeed and operation Y is refused with
42501. Unverified: the foreman and crew policy paths, and cross-role isolation (whether role X can
see role Z's rows), because those accounts do not exist."* Vague partial claims are how a gate gets
treated as closed when it is not.

### 5. Update the S0 report's deferred row

Edit the single row at ~line 46 of
`Code/mine-flow-docs/reports/security/2026-08-26-step-0044-s0-security-baseline-report.md` to state
the live result, referencing this substep and the CI run. Change **only that row** — the rest of that
report is immutable history. Do not touch the other Deferred rows (Ownership, Repository hygiene,
SBOM) — they belong to their own triggers.

### 6. Authoritative CI evidence

Commit, push to `step-0048-runtime-evidence`, confirm the journey **executes** in `e2e-web` and
`e2e-android`, and record the run URL plus real counts. (CI logs without `gh`: PAT from `git
credential fill` as a Bearer token; `/actions/jobs/<id>/logs` 302s to Azure Blob which rejects the
auth header — follow `redirect_url` bare.)

### 7. Record it

`Upcoming Prompts/mine-flow-STEP-48.12-FINDINGS.md`:

- which accounts and roles existed, and therefore what was in scope;
- verdict: Verified (with the precise boundary from step 4) or Deferred with a named blocker;
- the **refusal evidence** — table, operation, role, exception code/message;
- the exact S0 report row before and after;
- any security defect found, escalated prominently, with a recommendation for its own STEP;
- a recommendation for 48.14: what RLS-related deferral (if any) should be a `risks.yml` row with a
  revisit trigger, given that RISK-0015…0019 are STEP-45's carry-forwards and a partial matrix is a
  *new* deferral needing its own row.

## Verification

- Journey **executes** on both platforms in a CI run on the branch head, counts quoted; or an honest
  Deferred.
- **At least one policy refusal asserted positively**, with a policy-related exception code/message —
  not merely logged, not merely swallowed by a `try/catch`.
- The partial-vs-full scope boundary stated precisely.
- The S0 report's live-RLS row updated; no other row in that report touched.
- `flutter analyze` → 0 issues; `dart format --set-exit-if-changed .` → clean.
- `flutter test` → green (the `attendance_daily_log_sync_test.dart` Hive flake is known: re-run
  isolated to confirm, and say so).
- No secret value in any log, report, or commit. Account **emails** may be recorded; passwords never.

## Keeping the docs true

If runtime RLS behaviour contradicts `architecture/06-security-threat-model.md` or
`architecture/16-identity-auth.md`, that is significant — decide which side is wrong, record the
finding, and hand any doc correction to 48.15 with the section named. A policy gap is a **bug plus a
migration**, not a doc edit. Docstrings on anything you write. `risks.yml` edits to 48.14.

## Definition of done

- [ ] Accounts and roles confirmed against `public.users`; testable scope established.
- [ ] Journey observed **executing** against staging on both platforms in CI; verdict with URL +
      counts.
- [ ] At least one policy **refusal** asserted positively with a policy-related exception.
- [ ] The precise verified / unverified boundary written out — no vague partial claim.
- [ ] STEP-44 S0 report's live-RLS deferred row updated in place; nothing else in that report changed.
- [ ] Any security defect escalated prominently with a recommendation for a dedicated STEP.
- [ ] A recommendation written for 48.14 covering any new RLS deferral row.
- [ ] `flutter analyze` 0 issues, `dart format` clean, `flutter test` green (flake diagnosed).
- [ ] `Upcoming Prompts/mine-flow-STEP-48.12-FINDINGS.md` written.
- [ ] Committed on `step-0048-runtime-evidence`.

## Next

Tell the user the next action is *"run substep 48.13"* (runtime Impeccable design review with
automated screenshots) in a **fresh chat**, and update 48.12's status in the STEP PLAN.
