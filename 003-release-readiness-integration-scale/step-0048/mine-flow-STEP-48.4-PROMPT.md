# mine-flow — STEP-48.4: Attendance & Daily Log Runtime Evidence (settles 45.4)

> **How to run:** tell your agent *"run substep 48.4"*. Self-contained — runnable cold.

**Assigned model: Gemini 3.1 Pro High.** Not a mechanical run: the CF-006/007/009 attribution guards
mean a wrong answer here writes a shift record against the wrong person, and the RLS-vs-defect
distinction needs the policy file read properly. `architecture/04-data-model.md` is the authority, so
the judgement is bounded. **Escalate to Opus 4.8** if attribution is wrong (that is a data-integrity
defect with sibling write paths to check), or if the known
`test/integration/attendance_daily_log_sync_test.dart` flake cannot be cleanly distinguished from a
real regression in these two features.


## Context

Read `Upcoming Prompts/mine-flow-STEP-48-PLAN.md`, then the 48.0/48.1/48.2 findings and
`mine-flow-STEP-48.3-FINDINGS.md` — **48.3 (auth) must be Verified before this substep runs.**
Every journey here logs in first.

STEP-45 row 45.4 reads `Deferred — attendance_journey_test.dart, daily_log_journey_test.dart
authored; not run → STEP-48`. Two journeys, both with substantial assertions
(attendance 19, daily log 20) that have never executed.

Attendance carries extra risk: **STEP-38.6 extracted `AttendanceFormPage` to a standalone route**
(`/teams/attendance/form`), and STEP-40.2 had to migrate two widget tests to the new screen for
exactly that reason. `attendance_journey_test.dart` imports **both** `AttendanceFormPage` and
`AttendanceScreen`, so verify it targets the current navigation shape rather than the pre-STEP-38
one. Its header comment names guards CF-006 / CF-007 / CF-009 (author/recorder attribution) — that
attribution logic is what makes this journey worth running against a real backend rather than a
mock: the recorded author must be the authenticated staging user, not a client-side guess.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — honesty rule, decision D1 (CI authoritative), Q4.
- `…-48.0-FINDINGS.md` (seed state matters here — the crew roster comes from staging data),
  `…-48.1-FINDINGS.md` (repairs and handed-forward conflicts), `…-48.2-FINDINGS.md` (CI triage),
  `…-48.3-FINDINGS.md`.
- root `.throughstone/local-user.md` — Experience level 2, Explanatory.
- `Code/mine-flow-docs/architecture/04-data-model.md` — `attendance_records`, `daily_logs`,
  their author/recorder columns and soft-delete semantics.
- `Code/mine-flow-docs/architecture/15-native-app-architecture.md` §2 — offline-first,
  last-write-wins. Both features write through the sync queue.
- `Code/mine-flow-docs/architecture/12-test-strategy.md` v1.2.
- `Code/mine-flow-app/integration_test/journeys/attendance_journey_test.dart`,
  `daily_log_journey_test.dart`.
- `Code/mine-flow-app/lib/features/attendance/`, `lib/features/daily_log/`.
- `Code/mine-flow-app/supabase/migrations/20260718000002_rls_policies.sql` — `attendance_records`
  has role-scoped policies; the staging user's role determines what it may write. If 48.0 assigned
  a role whose policy forbids the write this journey attempts, the failure is **RLS working
  correctly**, not a bug. Check the policy before calling it a defect.
- `Code/mine-flow-docs/registries/risks.yml` — RISK-0009 (`EditableText` finders), RISK-0004
  (Indonesian strings hardcoded in ~28 legacy files — expect Indonesian labels).

## Scope

**In scope:** running both journeys against staging until each passes or a real defect is
identified and fixed; recording the evidence.

**Not in scope:** other feature areas, the offline/sync Part A journey (48.10 owns it even though
these features use the sync queue), the design review (48.13), risk rows (48.14), docs (48.15).

## Your task

### 1. Run each journey, one at a time

```bash
cd Code/mine-flow-app
flutter test integration_test/journeys/attendance_journey_test.dart -d emulator-5554 \
  --dart-define=SUPABASE_URL="$SUPABASE_URL" --dart-define=SUPABASE_ANON_KEY="$SUPABASE_ANON_KEY" \
  --dart-define=TEST_USER_EMAIL="$TEST_USER_EMAIL" --dart-define=TEST_USER_PASSWORD="$TEST_USER_PASSWORD" \
  --dart-define=APP_ENV=staging
```

Then the same for `daily_log_journey_test.dart`. Web iteration uses `flutter drive` (see 48.3).
Secrets come from the shell environment; never inline a literal.

### 2. Triage honestly

- **Navigation drift** (most likely): assertions written before STEP-38.6/STEP-46 may target
  screens that moved. Fixing a finder or a route is a legitimate test fix — record it.
- **Empty-data failures:** if the crew roster or zone list is empty because staging was not
  seeded, that is an environment problem, not a code defect. Re-check 48.0's seed record, fix the
  environment, and re-run. Do not "fix" the test by removing the assertion.
- **Attribution failures (CF-006/007/009):** if the recorded author is not the authenticated
  staging user, that is a **real defect with data-integrity consequences** — a shift record
  attributed to the wrong person. Fix the root cause, check the sibling write paths in
  `daily_log` and the other features for the same flaw, and add a regression test.
- **RLS refusals:** compare against the policy file first. A refusal that matches policy means the
  journey's expectation is wrong for this user's role — note it and, if the role is the blocker,
  hand the role-matrix question to 48.12.

Never delete an assertion to get green.

### 3. Authoritative CI evidence

Commit, push to `step-0048-runtime-evidence`, and confirm both journeys **execute and pass** in
`e2e-web` and `e2e-android`. Record the run URL and the real executed/skipped/failed counts.
(Reading CI logs without `gh`: PAT from `git credential fill`, Bearer token;
`/actions/jobs/<id>/logs` 302s to Azure Blob which rejects the auth header — follow the
`redirect_url` bare.)

### 4. Record it

`Upcoming Prompts/mine-flow-STEP-48.4-FINDINGS.md`: per-journey verdict (**Verified** with run URL
and counts, or **Deferred** with a named blocker and revisit trigger), every defect classified
test-vs-app with its fix and regression test, and whether runtime write/sync behaviour matched
`architecture/15-native-app-architecture.md` §2 (state "no divergence" explicitly if so — 48.15
needs that either way).

## Verification

- Both journeys **execute** on both platforms in a CI run on the branch head, with counts quoted;
  or an honest Deferred per journey.
- `flutter analyze` → 0 issues; `dart format --set-exit-if-changed .` → clean.
- `flutter test` → green. Note: `test/integration/attendance_daily_log_sync_test.dart` is the
  **known flake** (Hive `setUpAll`, intermittent full-suite, green isolated) and it covers exactly
  these two features. If it fails, re-run isolated and say which it was; a genuine regression here
  would be easy to mistake for the flake and vice versa. Do not wave it through either way.
- Any app fix carries a regression test.
- No secret value in any log, report, or commit.

## Keeping the docs true

If the data written at runtime does not match `architecture/04-data-model.md` (column semantics,
soft delete, attribution), decide which side is wrong: app contradicts a correct doc → bug, fix
and record; doc stale → hand to 48.15 with the section and the correction. Docstrings on anything
you write (`coding-standards/README.md`). Risk rows are 48.14's.

## Definition of done

- [ ] Both journeys observed **executing** against staging on both platforms in CI.
- [ ] Per-journey verdict recorded: Verified with URL + counts, or Deferred with a named blocker.
- [ ] Every defect classified and root-caused; sibling write paths checked for the same flaw;
      regression tests added.
- [ ] Runtime sync/write behaviour compared against Doc 15 §2, with divergence or "no divergence"
      stated explicitly.
- [ ] `flutter analyze` 0 issues, `dart format` clean, `flutter test` green with the
      attendance/daily-log flake correctly diagnosed.
- [ ] `Upcoming Prompts/mine-flow-STEP-48.4-FINDINGS.md` written.
- [ ] Committed on `step-0048-runtime-evidence`.

## Next

Tell the user the next action is *"run substep 48.5"* (Cut/Fill & Land Clearing) in a **fresh
chat**, note that 48.4–48.10 and 48.12 are independent of each other once auth is green, and update
48.4's status in the STEP PLAN.
