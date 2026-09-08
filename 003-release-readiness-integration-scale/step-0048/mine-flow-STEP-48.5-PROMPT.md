# mine-flow — STEP-48.5: Cut/Fill & Land Clearing Runtime Evidence (settles 45.5)

> **How to run:** tell your agent *"run substep 48.5"*. Self-contained — runnable cold.

**Assigned model: Gemini 3.1 Pro High.** The substantive question is whether the in-app volume numbers
match ADR-0012 while RISK-0014's reporting path is still documented as wrong — you must assert the
former and pointedly *not* assert the latter. ADR-0012 and the risk row are the written authorities, so
the judgement is bounded. **Escalate to Opus 4.8** if runtime numbers appear to contradict ADR-0012:
an accepted ADR is superseded deliberately, never retrofitted to match drifted code, and that call is
not this substep's to make alone.


## Context

Read `Upcoming Prompts/mine-flow-STEP-48-PLAN.md`, then the 48.0/48.1/48.2 findings and
`mine-flow-STEP-48.3-FINDINGS.md` — **48.3 (auth) must be Verified first.**

STEP-45 row 45.5: `Deferred — cut_fill_journey_test.dart, land_clearing_journey_test.dart
authored; not run → STEP-48`. Cut/Fill carries 10 assertions, Land Clearing 8 — the two thinnest
of the eleven "real" journeys, so scrutinise whether they actually cover their feature before
accepting a green run as meaningful evidence.

**This area has a live, documented contradiction you must not paper over.** `ADR-0012` corrected
the earthworks volume semantics (bank-equivalent net via `VolumeNormalizer`; BCM/LCM relabelled)
across the entity, blocs, dashboard, and summary cards. **RISK-0014 (`open`) records that the
reporting export path was NOT aligned** — `reporting_remote_datasource.dart` still queries the
legacy `cut_volume_m3` / `fill_volume_m3` columns and computes `net = cut − fill`, the very formula
ADR-0012 rejected as meaningless. So a report and the screen it was generated from can disagree on
the headline volume.

The journey's own header comment says it *"asserts current documented volume semantics"*. Get this
right: assert the **corrected ADR-0012 semantics on the in-app surfaces**, and do **not** assert
that the reporting path is correct — it is documented as still wrong. Asserting a fix that has not
shipped encodes a fiction in the test suite.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — honesty rule, D1, Q4.
- `…-48.0/1/2/3-FINDINGS.md` — especially 48.0's seed record (zones must exist).
- root `.throughstone/local-user.md` — Experience level 2, Explanatory.
- **`Code/mine-flow-docs/adr/ADR-0012-volume-and-land-clearing-metrics.md`** — the authority on
  what the numbers mean. Read it before writing or judging a single assertion.
- `Code/mine-flow-docs/registries/risks.yml` — **RISK-0014** verbatim (reporting path still on the
  legacy formula, `open`); RISK-0009 (`EditableText` finders); RISK-0004 (Indonesian labels).
- `Code/mine-flow-docs/architecture/04-data-model.md` — `cut_fill_records`,
  `land_clearing_records`, and which volume columns are current vs legacy.
- `Code/mine-flow-docs/architecture/15-native-app-architecture.md` §2 — offline-first writes.
- `Code/mine-flow-app/integration_test/journeys/cut_fill_journey_test.dart`,
  `land_clearing_journey_test.dart`.
- `Code/mine-flow-app/lib/features/tracking/` — forms, list screens, `VolumeNormalizer`.
- `Code/mine-flow-app/supabase/migrations/` — the `20260723_step_33_1_data_model_polish.sql` and
  core-schema volume columns.

Relevant recent UI history: **STEP-38.2** fixed the BCM/LCM label-and-unit mix-up, moved these
forms to a 2-column layout, removed the steppers, and switched Zona and Metode Clearing to a
`CreatableCombobox`. **STEP-38.4** changed the Land Clearing Plan/Actual tab layout. Assertions
written before those changes may target controls that no longer exist.

## Scope

**In scope:** running both journeys against staging until each passes or a real defect is found and
fixed; verifying the in-app volume semantics match ADR-0012 at runtime.

**Not in scope:** fixing RISK-0014's reporting path (that is its own follow-up STEP per its revisit
trigger — "next reporting STEP"), the reporting journey itself (48.8), other feature areas, the
design review (48.13), risk rows (48.14), docs (48.15).

## Your task

### 1. Run each journey

```bash
cd Code/mine-flow-app
flutter test integration_test/journeys/cut_fill_journey_test.dart -d emulator-5554 \
  --dart-define=SUPABASE_URL="$SUPABASE_URL" --dart-define=SUPABASE_ANON_KEY="$SUPABASE_ANON_KEY" \
  --dart-define=TEST_USER_EMAIL="$TEST_USER_EMAIL" --dart-define=TEST_USER_PASSWORD="$TEST_USER_PASSWORD" \
  --dart-define=APP_ENV=staging
```

Then `land_clearing_journey_test.dart`. Web iteration via `flutter drive` (see 48.3). Secrets from
the shell environment only.

### 2. Verify the volume semantics deliberately

Beyond "does it pass", answer these and record the answers:

- Does the value the app **persists** to staging use the current columns (`bcm_volume` /
  `lcm_volume` per ADR-0012), or the legacy ones?
- Does the value the app **displays** (dashboard, summary card, list row) match the
  `VolumeNormalizer` bank-equivalent net, not `cut − fill`?
- The journey exercises the CF-035 / CF-040 zero-and-negative-elevation guards. Confirm at runtime
  that invalid input is rejected cleanly rather than persisting a nonsense row.

If the app's in-app numbers disagree with ADR-0012, that is a **real defect** — ADR-0012 is
accepted, and an accepted ADR is not overturned by an implementation that drifted. Fix the root
cause, check sibling call paths (both features share the normalizer), add a regression test.

If you find the reporting path's legacy formula while you are here: **that is RISK-0014, already
known and deliberately deferred.** Do not fix it in this substep and do not assert against it.
Confirm the risk row still describes reality and hand any update to 48.14.

### 3. Triage the rest honestly

- Control drift from STEP-38.2/38.4 (steppers gone, `CreatableCombobox` for Zona, tab layout) is a
  legitimate test fix — record it.
- Empty zone list → check 48.0's seed record; environment problem, not a code defect.
- RLS refusal → compare against `20260718000002_rls_policies.sql` before calling it a bug.

Never delete an assertion to get green.

### 4. Authoritative CI evidence

Commit, push to `step-0048-runtime-evidence`, confirm both journeys **execute and pass** in
`e2e-web` and `e2e-android`, and record run URL plus real counts. (CI logs without `gh`: PAT from
`git credential fill` as a Bearer token; `/actions/jobs/<id>/logs` 302s to Azure Blob which rejects
the auth header — follow `redirect_url` bare.)

### 5. Record it

`Upcoming Prompts/mine-flow-STEP-48.5-FINDINGS.md`: per-journey verdict (Verified with URL +
counts, or Deferred with named blocker + trigger); the **volume-semantics findings** as a dedicated
section, since they are the substantive question here; every defect classified test-vs-app with fix
and regression test; confirmation of RISK-0014's current accuracy for 48.14.

## Verification

- Both journeys **execute** on both platforms in a CI run on the branch head, counts quoted; or an
  honest per-journey Deferred.
- The in-app volume values are explicitly confirmed against ADR-0012 — not just "the test passed".
- No assertion claims the reporting path is corrected while RISK-0014 is `open`.
- `flutter analyze` → 0 issues; `dart format --set-exit-if-changed .` → clean.
- `flutter test` → green (the `attendance_daily_log_sync_test.dart` Hive flake is known: re-run
  isolated to confirm, and say so; never wave a red suite through).
- Any app fix carries a regression test.
- No secret value in any log, report, or commit.

## Keeping the docs true

If runtime behaviour contradicts ADR-0012, the app is wrong — **never amend an accepted ADR to
match drifted code** (an ADR is superseded or amended deliberately, not retrofitted). If
`architecture/04-data-model.md` describes the volume columns staler than reality, hand it to 48.15
with the exact section and correction. Docstrings on anything you write. Risk rows to 48.14.

## Definition of done

- [ ] Both journeys observed **executing** against staging on both platforms in CI.
- [ ] Per-journey verdict recorded: Verified with URL + counts, or Deferred with a named blocker.
- [ ] In-app volume semantics verified against ADR-0012 at runtime and reported explicitly.
- [ ] CF-035 / CF-040 elevation guards confirmed to reject invalid input at runtime.
- [ ] RISK-0014's continued accuracy confirmed and handed to 48.14; its reporting path **not**
      fixed here and **not** asserted as fixed.
- [ ] Every defect classified and root-caused; sibling paths checked; regression tests added.
- [ ] `flutter analyze` 0 issues, `dart format` clean, `flutter test` green (flake diagnosed).
- [ ] `Upcoming Prompts/mine-flow-STEP-48.5-FINDINGS.md` written.
- [ ] Committed on `step-0048-runtime-evidence`.

## Next

Tell the user the next action is *"run substep 48.6"* (Inventory & Equipment Check) in a **fresh
chat**, and update 48.5's status in the STEP PLAN.
