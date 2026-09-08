# mine-flow — STEP-48.9: Timeline & Notifications Runtime Evidence (settles 45.10)

> **How to run:** tell your agent *"run substep 48.9"*. Self-contained — runnable cold.

**Assigned model: Gemini 3.7 Flash High.** Mostly mechanical: finders stale after the STEP-37.2/37.3
Material purge (`Card`, `TextButton`, `MaterialBanner` are gone from these features), plus read-state
and ordering round-trips with clear right answers in `architecture/04-data-model.md`. **Escalate to Opus
4.8** if a transient-widget assertion cannot be made deterministic without a delay hack, or if a
notification read flag updates locally but not server-side — that is a real persistence defect, not a
finder fix.


## Context

Read `Upcoming Prompts/mine-flow-STEP-48-PLAN.md`, then the 48.0/48.1/48.2 findings and
`mine-flow-STEP-48.3-FINDINGS.md` — **48.3 (auth) must be Verified first.**

STEP-45 row 45.10: `Deferred — timeline_journey_test.dart, notifications_journey_test.dart
authored; not run → STEP-48`. Timeline carries 16 assertions, Notifications 12.

Both features were touched by the Material purge: **STEP-37.2** converted `milestone_card.dart`
(`Card`→`Container`, preserving `InkWell`), and **STEP-37.3** converted
`notification_list_page.dart` (`TextButton`→`FButton`) and `notification_banner.dart`
(`MaterialBanner`→`Container` + `FButton`). Assertions written against the pre-purge tree will not
find those Material widgets — correcting the finder is a legitimate test fix, and finding a
*surviving* Material widget is a STEP-37 miss worth reporting.

Notifications is the trickier of the two: notification state (read/unread, dismissal) is
server-backed, and a banner is transient by nature. Timing-fragile assertions on a transient widget
are a real hazard here — a test that passes only because the pump landed in the right millisecond
will be waved through as a flake later.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — honesty rule, D1, Q4.
- `…-48.0/1/2/3-FINDINGS.md` — 48.0's seed record matters: timeline milestones and notification rows
  must exist in staging or list assertions fail environmentally.
- root `.throughstone/local-user.md` — Experience level 2, Explanatory.
- `Code/mine-flow-docs/architecture/04-data-model.md` — timeline/milestone and notification tables,
  read-state columns, soft delete.
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` — the ForUI-only component contract
  STEP-37 enforced; the authority when a test expects a Material widget.
- `Code/mine-flow-docs/architecture/10-observability.md` — if notifications tie into any logging or
  alerting expectations, this is where they are recorded.
- `Code/mine-flow-app/integration_test/journeys/timeline_journey_test.dart`,
  `notifications_journey_test.dart`.
- `Code/mine-flow-app/lib/features/timeline/`, `lib/features/notifications/`.
- `Code/mine-flow-app/supabase/migrations/20260718000002_rls_policies.sql` — role-scoped policies.
- `Code/mine-flow-docs/registries/risks.yml` — RISK-0009 (`EditableText` finders), RISK-0004
  (Indonesian labels), RISK-0003 (accepted Phase 2 UI spacing/colour drift — check before raising
  cosmetic findings as new).

## Scope

**In scope:** running both journeys against staging until each passes or a real defect is found and
fixed; recording the evidence.

**Not in scope:** other feature areas, the design review (48.13 — note cosmetic issues, do not fix
them), risk rows (48.14), docs (48.15).

## Your task

### 1. Run each journey

```bash
cd Code/mine-flow-app
flutter test integration_test/journeys/timeline_journey_test.dart -d emulator-5554 \
  --dart-define=SUPABASE_URL="$SUPABASE_URL" --dart-define=SUPABASE_ANON_KEY="$SUPABASE_ANON_KEY" \
  --dart-define=TEST_USER_EMAIL="$TEST_USER_EMAIL" --dart-define=TEST_USER_PASSWORD="$TEST_USER_PASSWORD" \
  --dart-define=APP_ENV=staging
```

Then `notifications_journey_test.dart`. Web iteration via `flutter drive` (see 48.3). Secrets from
the shell environment only.

### 2. Triage honestly, with extra care on timing

- **Material-widget expectations** (`Card`, `TextButton`, `MaterialBanner`): the app is correct and
  the test is stale per STEP-37 — update the finder. A *surviving* Material widget in either feature
  is a STEP-37 miss and a real finding.
- **Transient-widget assertions.** If the test asserts a notification banner is visible, make the
  assertion deterministic: assert on the state that drives visibility (bloc/cubit state, or the
  presence of the backing row) rather than racing a timed dismissal. If you cannot make it
  deterministic, say so plainly in the findings rather than shipping a coin-flip.
- **Read-state persistence.** Marking a notification read should round-trip: change it, reload from
  staging, assert it stayed changed. A read flag that only updates locally is a real defect.
- **Timeline ordering.** Milestones have dates; assert the order the UI renders matches what
  `architecture/04-data-model.md` specifies, not merely that items appear.
- **Empty lists** → check 48.0's seed record; environment problem, not a code defect.
- **RLS refusals** → compare against the policy file before calling it a bug.
- **Cosmetic drift** → check RISK-0003 before raising it as new; hand cosmetics to 48.13.

Never delete an assertion to get green. Real app defects get a root-cause fix, a sibling-path check,
and a regression test at the cheapest tier that catches them.

### 3. Authoritative CI evidence

Commit, push to `step-0048-runtime-evidence`, confirm both journeys **execute and pass** in
`e2e-web` and `e2e-android`, and record the run URL plus real executed/skipped/failed counts. (CI
logs without `gh`: PAT from `git credential fill` as a Bearer token; `/actions/jobs/<id>/logs` 302s
to Azure Blob which rejects the auth header — follow `redirect_url` bare.)

### 4. Record it

`Upcoming Prompts/mine-flow-STEP-48.9-FINDINGS.md`: per-journey verdict (Verified with URL +
counts, or Deferred with named blocker + trigger); every defect classified test-vs-app with fix and
regression test; any surviving Material widgets (STEP-37 misses); an explicit note on any assertion
you had to make deterministic and how; read-state and ordering results.

## Verification

- Both journeys **execute** on both platforms in a CI run on the branch head, counts quoted; or an
  honest per-journey Deferred.
- Notification read-state confirmed to round-trip through staging.
- Timeline ordering confirmed against the documented model.
- No timing-fragile assertion left in place without either a determinism fix or an explicit note.
- `flutter analyze` → 0 issues; `dart format --set-exit-if-changed .` → clean.
- `flutter test` → green (the `attendance_daily_log_sync_test.dart` Hive flake is known: re-run
  isolated to confirm, and say so; never wave a red suite through).
- Any app fix carries a regression test.
- No secret value in any log, report, or commit.

## Keeping the docs true

A test expecting a Material widget does not justify editing
`architecture/07-ui-design-system.md` — the doc is the contract. If
`architecture/04-data-model.md` or `architecture/10-observability.md` is stale about notification or
milestone semantics, hand it to 48.15 with the section and correction. Docstrings on anything you
write (`coding-standards/README.md`). Risk rows to 48.14.

## Definition of done

- [ ] Both journeys observed **executing** against staging on both platforms in CI.
- [ ] Per-journey verdict recorded: Verified with URL + counts, or Deferred with a named blocker.
- [ ] Notification read-state round-trip verified; timeline ordering verified.
- [ ] Any surviving Material widget reported as a STEP-37 miss.
- [ ] Timing-fragile assertions made deterministic or explicitly flagged.
- [ ] Every defect classified and root-caused; sibling paths checked; regression tests added.
- [ ] `flutter analyze` 0 issues, `dart format` clean, `flutter test` green (flake diagnosed).
- [ ] `Upcoming Prompts/mine-flow-STEP-48.9-FINDINGS.md` written.
- [ ] Committed on `step-0048-runtime-evidence`.

## Next

Tell the user the next action is *"run substep 48.10"* (offline/sync Part A against staging — the
field-critical journey) in a **fresh chat**, and update 48.9's status in the STEP PLAN.
