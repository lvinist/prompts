# mine-flow — STEP-48.6: Inventory & Equipment Check Runtime Evidence (settles 45.6)

> **How to run:** tell your agent *"run substep 48.6"*. Self-contained — runnable cold.

**Assigned model: Gemini 3.7 Flash High.** These two journeys are the most heavily asserted in the
suite, but their likely failures are mechanical: finders left over from the STEP-37 Material purge
(`ElevatedButton`, `Card`, `TextButton` no longer exist here) and layout changes from STEP-38.4/38.7.
`architecture/07-ui-design-system.md` decides every widget-expectation conflict, so the work is
checklist-shaped. **Escalate to Opus 4.8** if a quantity or unit mismatch appears in what lands in
staging (a data-integrity question, not a finder fix), if a control is genuinely unreachable at the
emulator viewport (that would be a STEP-38.7 regression), or if you cannot tell a stale finder from a
real defect.


## Context

Read `Upcoming Prompts/mine-flow-STEP-48-PLAN.md`, then the 48.0/48.1/48.2 findings and
`mine-flow-STEP-48.3-FINDINGS.md` — **48.3 (auth) must be Verified first.**

STEP-45 row 45.6: `Deferred — inventory_journey_test.dart, equipment_check_journey_test.dart
authored; not run → STEP-48`. These are the two most heavily-asserted journeys in the suite
(equipment check 30 assertions, inventory 21), so they are the most likely to surface real drift —
and the most likely to fail on stale finders. Read both files fully before running anything.

Recent UI history that bears directly on them: **STEP-37.1** purged Material widgets from the
equipment-check feature (`ElevatedButton`→`FButton`, `Card`→`Container`, `TextButton`→`FButton`
across `equipment_check_form_screen.dart`, `sop_checklist_item_card.dart`,
`equipment_check_card.dart`). **STEP-38.7** fixed an overflow that made controls unreachable on
narrow mobile. **STEP-38.4** merged inventory's Jumlah + Satuan into a single row. Assertions
written against the pre-purge widget tree will not find `ElevatedButton` or `Card` — that is
expected, and correcting them is a legitimate test fix.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — honesty rule, D1, Q4.
- `…-48.0/1/2/3-FINDINGS.md` — 48.0's seed record matters (inventory items and equipment must
  exist in staging or list assertions fail for environmental reasons).
- root `.throughstone/local-user.md` — Experience level 2, Explanatory.
- `Code/mine-flow-docs/architecture/04-data-model.md` — `inventory_items`, `equipment_checks`,
  their stock/quantity semantics and soft-delete behaviour.
- `Code/mine-flow-docs/architecture/07-ui-design-system.md` — the ForUI-only component contract
  STEP-37 enforced. This is the authority when a test expects a Material widget.
- `Code/mine-flow-docs/architecture/15-native-app-architecture.md` §2 — offline-first writes.
- `Code/mine-flow-app/integration_test/journeys/inventory_journey_test.dart`,
  `equipment_check_journey_test.dart`.
- `Code/mine-flow-app/lib/features/inventory/`, `lib/features/equipment_check/`.
- `Code/mine-flow-app/supabase/migrations/20260718000002_rls_policies.sql` — role-scoped policies
  on both tables.
- `Code/mine-flow-docs/registries/risks.yml` — RISK-0009 (`EditableText`, never `TextField`),
  RISK-0004 (Indonesian labels), RISK-0003 (Phase 2 UI spacing/colour drift deferred — cosmetic
  drift you notice here may already be a known, accepted deferral rather than a new finding).

## Scope

**In scope:** running both journeys against staging until each passes or a real defect is found and
fixed; recording the evidence.

**Not in scope:** other feature areas, the design review (48.13 — resist fixing cosmetic issues you
spot; note them and hand them over), risk rows (48.14), docs (48.15).

## Your task

### 1. Run each journey

```bash
cd Code/mine-flow-app
flutter test integration_test/journeys/inventory_journey_test.dart -d emulator-5554 \
  --dart-define=SUPABASE_URL="$SUPABASE_URL" --dart-define=SUPABASE_ANON_KEY="$SUPABASE_ANON_KEY" \
  --dart-define=TEST_USER_EMAIL="$TEST_USER_EMAIL" --dart-define=TEST_USER_PASSWORD="$TEST_USER_PASSWORD" \
  --dart-define=APP_ENV=staging
```

Then `equipment_check_journey_test.dart`. Web iteration via `flutter drive` (see 48.3). Secrets
from the shell environment only — never inline a literal.

### 2. Triage honestly

- **Material-widget expectations** (`ElevatedButton`, `Card`, `TextButton`, `MaterialBanner`): the
  app is correct and the test is stale — STEP-37 removed them deliberately per
  `architecture/07-ui-design-system.md`. Update the finder to the ForUI equivalent. If you find any
  Material widget still in these features' trees, that is a **STEP-37 miss** — a real finding.
- **Narrow-viewport failures:** STEP-38.7 fixed an equipment-check overflow. If a control is
  unreachable at the emulator's viewport, check whether the fix regressed before assuming a test
  bug — `tester.ensureVisible` masking a genuine overflow would hide the exact class of defect
  STEP-38.7 fixed. Note which you concluded and why.
- **Quantity / stock arithmetic:** inventory writes numeric quantities. Verify what lands in
  staging matches what was entered and what `architecture/04-data-model.md` specifies (units,
  precision). A silent unit mismatch is a data-integrity defect, not cosmetic.
- **SOP checklist state:** equipment check persists per-item checklist results. Confirm the
  persisted shape round-trips — create, reload from staging, and assert the same state.
- **Empty lists** → check 48.0's seed record; environment problem, not a code defect.
- **RLS refusals** → compare against the policy file before calling it a bug.
- **Cosmetic spacing/colour drift** → check RISK-0003 before raising it as new; if it is already
  covered there, note it for 48.13/48.14 rather than fixing it here.

Never delete an assertion to get green. If an app defect is real, fix the root cause, check sibling
call paths, add a regression test at the cheapest tier that catches it.

### 3. Authoritative CI evidence

Commit, push to `step-0048-runtime-evidence`, confirm both journeys **execute and pass** in
`e2e-web` and `e2e-android`, and record the run URL plus real executed/skipped/failed counts. (CI
logs without `gh`: PAT from `git credential fill` as a Bearer token; `/actions/jobs/<id>/logs` 302s
to Azure Blob which rejects the auth header — follow `redirect_url` bare.)

### 4. Record it

`Upcoming Prompts/mine-flow-STEP-48.6-FINDINGS.md`: per-journey verdict (Verified with URL +
counts, or Deferred with named blocker + trigger); every defect classified test-vs-app with fix and
regression test; any Material-widget survivors found (STEP-37 misses); the narrow-viewport
conclusion with reasoning; cosmetic observations handed to 48.13.

## Verification

- Both journeys **execute** on both platforms in a CI run on the branch head, counts quoted; or an
  honest per-journey Deferred.
- Persisted inventory quantities and equipment-check checklist state confirmed to round-trip
  correctly against staging.
- `flutter analyze` → 0 issues; `dart format --set-exit-if-changed .` → clean.
- `flutter test` → green (the `attendance_daily_log_sync_test.dart` Hive flake is known: re-run
  isolated to confirm, and say so; never wave a red suite through).
- Any app fix carries a regression test.
- No secret value in any log, report, or commit.

## Keeping the docs true

A test expecting a Material widget does **not** justify editing
`architecture/07-ui-design-system.md` — the doc is the contract and STEP-37 enforced it. If
`architecture/04-data-model.md` is stale about quantity/unit semantics, hand it to 48.15 with the
section and correction. Docstrings on anything you write (`coding-standards/README.md`). Risk rows
to 48.14.

## Definition of done

- [ ] Both journeys observed **executing** against staging on both platforms in CI.
- [ ] Per-journey verdict recorded: Verified with URL + counts, or Deferred with a named blocker.
- [ ] Inventory quantity and equipment-check checklist state confirmed to round-trip via staging.
- [ ] Any surviving Material widget in these features reported as a STEP-37 miss.
- [ ] Narrow-viewport behaviour assessed against STEP-38.7's fix, conclusion recorded with reasoning.
- [ ] Every defect classified and root-caused; sibling paths checked; regression tests added.
- [ ] `flutter analyze` 0 issues, `dart format` clean, `flutter test` green (flake diagnosed).
- [ ] `Upcoming Prompts/mine-flow-STEP-48.6-FINDINGS.md` written.
- [ ] Committed on `step-0048-runtime-evidence`.

## Next

Tell the user the next action is *"run substep 48.7"* (Benchmark journey + NR-006) in a **fresh
chat**, and update 48.6's status in the STEP PLAN.
