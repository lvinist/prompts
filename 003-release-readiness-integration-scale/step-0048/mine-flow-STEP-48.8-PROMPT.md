# mine-flow — STEP-48.8: Reporting / PDF Runtime Evidence (settles 45.9)

> **How to run:** tell your agent *"run substep 48.8"*. Self-contained — runnable cold.

**Assigned model: Gemini 3.1 Pro High.** Two things need care rather than raw power: proving NR-001's
control lock without a timing-fragile assertion, and staying off RISK-0014's legacy formula. Both have
written authorities (the risk row, ADR-0012). **Escalate to Opus 4.8** if you cannot make the lock
assertion deterministic — a flaky assertion on the one STEP-45 fix that was real is worse than no
assertion, because it will be waved through later — or if the reporting path turns out to differ from
what RISK-0014 describes.


## Context

Read `Upcoming Prompts/mine-flow-STEP-48-PLAN.md`, then the 48.0/48.1/48.2 findings and
`mine-flow-STEP-48.3-FINDINGS.md` — **48.3 (auth) must be Verified first.**

STEP-45 row 45.9 is the one row in the whole STEP-45 table with a partial win:
`Deferred — Partial: code Done, E2E Unverified. NR-001 genuinely resolved (config controls locked
during generation — real code change); reporting_journey_test.dart authored but not run → STEP-48`.

So NR-001 was the **only** one of STEP-46's six Needs-Runtime findings actually fixed, and the fix
was real code — `ReportConfigPage` locks its controls while a report generates. What was never done
is proving it at runtime. `reporting_journey_test.dart` (7 assertions) asserts exactly that:
`DateRangeSelector.enabled` and `ZonePicker.enabled` are both `false` during generation.

**The trap in this substep.** RISK-0014 (`open`, medium) records that
`reporting_remote_datasource.dart` still queries the legacy `cut_volume_m3` / `fill_volume_m3`
columns and computes `net_volume_m3 = cut − fill` — *"the very formula ADR-0012 rejected as
meaningless"* — so a generated cut/fill PDF and the screen it was generated from can disagree on the
headline volume. That is **known, accepted, and deliberately deferred** to a future reporting STEP.
Your job is to verify report generation *works* and that NR-001's lock holds, **not** to assert the
numbers are correct, and **not** to fix RISK-0014 here. Asserting a corrected formula that has not
shipped would encode a fiction.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — honesty rule, D1, Q4.
- `…-48.0/1/2/3-FINDINGS.md` — 48.0's seed record matters: a report over an empty date range proves
  little.
- root `.throughstone/local-user.md` — Experience level 2, Explanatory.
- `Code/mine-flow-docs/registries/risks.yml` — **RISK-0014** verbatim (do not assert against it, do
  not fix it, confirm it still describes reality); RISK-0009 (`EditableText` finders); RISK-0004
  (Indonesian labels — the UI says `'Buat Laporan'`, `'Cetak'`).
- **`Code/mine-flow-docs/adr/ADR-0012-volume-and-land-clearing-metrics.md`** — so you can state
  precisely which surface is corrected and which is not.
- `Code/mine-flow-docs/architecture/12-test-strategy.md` v1.2.
- `Code/mine-flow-app/integration_test/journeys/reporting_journey_test.dart`.
- `Code/mine-flow-app/lib/features/reporting/` — `ReportConfigPage`,
  `reporting_remote_datasource.dart`, the PDF generation path.
- `Code/mine-flow-app/lib/features/daily_log/presentation/widgets/zone_picker.dart` and
  `lib/features/reporting/presentation/widgets/date_range_selector.dart` — both take an `enabled`
  flag; that flag is NR-001's fix.

Note what the existing test does: it navigates via `appRouter.go(AppRoutes.cutFill)`, finds the
report button by **semantics label** (`find.bySemanticsLabel('Buat Laporan Cut/Fill')`), taps
Generate, then asserts the two `enabled` flags are `false` **after a single `tester.pump()`** — i.e.
during the loading state. It then `pumpAndSettle()`s and expects `'Cetak'` to appear. The attendance
report leg is wrapped in an `if (finder.evaluate().isNotEmpty)` guard, so it silently does nothing
when the button is absent — flag that as a soft spot: a conditional block that can vanish is weak
evidence. Consider asserting the button exists rather than skipping it silently.

## Scope

**In scope:** running `reporting_journey_test.dart` against staging on both platforms; confirming
NR-001's control lock holds at runtime; confirming a report actually generates end-to-end.

**Not in scope:** fixing RISK-0014's legacy volume formula (its revisit trigger names a future
reporting STEP), other feature areas, the design review (48.13), risk rows (48.14), docs (48.15).

## Your task

### 1. Run the journey

```bash
cd Code/mine-flow-app
flutter test integration_test/journeys/reporting_journey_test.dart -d emulator-5554 \
  --dart-define=SUPABASE_URL="$SUPABASE_URL" --dart-define=SUPABASE_ANON_KEY="$SUPABASE_ANON_KEY" \
  --dart-define=TEST_USER_EMAIL="$TEST_USER_EMAIL" --dart-define=TEST_USER_PASSWORD="$TEST_USER_PASSWORD" \
  --dart-define=APP_ENV=staging
```

Web iteration via `flutter drive` (see 48.3). Secrets from the shell environment only.

### 2. Prove NR-001 at runtime

This is the substantive question: STEP-45 claims the fix shipped; nothing has ever confirmed it
against a running app. Verify that while generation is in flight:

- `DateRangeSelector.enabled == false` and `ZonePicker.enabled == false`;
- the Generate button cannot be tapped again to start a second concurrent generation;
- when generation completes, the controls are re-enabled (the test does not currently check this —
  a lock that never releases is also a defect; add the assertion).

Be careful with the timing. `tester.pump()` once may or may not land inside the loading window
depending on how fast staging answers. If the assertion is timing-fragile, make it deterministic
(e.g. assert on the bloc/cubit state that drives `enabled`, or pump in a controlled loop) rather
than sprinkling delays. A flaky lock assertion is worse than none, because it will be waved through
later.

### 3. Confirm generation actually completes

The test expects `'Cetak'` to appear after `pumpAndSettle()`. Confirm a real PDF was produced —
check the success view and, if the feature exposes a file path or byte count, assert on it. "The
success label rendered" is thin evidence that a document exists.

Strengthen the attendance-report leg: replace the silent `if (finder.evaluate().isNotEmpty)` guard
with a real assertion that the button exists, or state in your findings why it must stay
conditional.

### 4. Handle RISK-0014 correctly

Confirm the reporting datasource still uses the legacy columns and the `cut − fill` formula. If it
does, record that RISK-0014 remains accurate and hand it to 48.14 unchanged. If it has since been
fixed, say so with evidence — that would let 48.14 close a risk. **Either way, do not add an
assertion claiming the corrected formula is in place unless you have verified it is.** If you can
cheaply assert the *current documented* behaviour (legacy basis) without encoding it as desirable,
prefer leaving it unasserted and documented over freezing the wrong formula into a test.

### 5. Triage the rest honestly

Semantics-label drift, Material-widget expectations from before STEP-37, route changes from
STEP-38.1's Laporan icon-button work — legitimate test fixes; record each. Real app defects get a
root-cause fix, a sibling-path check, and a regression test. Never delete an assertion to get green.

### 6. Authoritative CI evidence

Commit, push to `step-0048-runtime-evidence`, confirm the journey **executes and passes** in
`e2e-web` and `e2e-android`, and record the run URL plus real counts. (CI logs without `gh`: PAT
from `git credential fill` as a Bearer token; `/actions/jobs/<id>/logs` 302s to Azure Blob which
rejects the auth header — follow `redirect_url` bare.)

### 7. Record it

`Upcoming Prompts/mine-flow-STEP-48.8-FINDINGS.md`: journey verdict (Verified with URL + counts, or
Deferred with named blocker + trigger); a dedicated **NR-001 confirmation** section — this is the
one STEP-45 fix that was real, and this is its first runtime proof; whether the lock releases after
completion; evidence that a PDF genuinely generated; RISK-0014's current accuracy for 48.14; any
timing-fragility you had to engineer around.

## Verification

- Journey **executes** on both platforms in a CI run on the branch head, counts quoted; or an honest
  Deferred.
- NR-001's control lock confirmed **during** generation and confirmed to **release** after.
- Evidence that a report document was actually produced, not just a success label.
- No assertion encodes RISK-0014's legacy formula as correct behaviour.
- `flutter analyze` → 0 issues; `dart format --set-exit-if-changed .` → clean.
- `flutter test` → green (the `attendance_daily_log_sync_test.dart` Hive flake is known: re-run
  isolated to confirm, and say so).
- Any app fix carries a regression test.
- No secret value in any log, report, or commit.

## Keeping the docs true

If report generation's real behaviour differs from what the architecture docs describe, hand it to
48.15 with section and correction — do not edit docs here. ADR-0012 is accepted; never amend it to
match the reporting path's drift (that drift is RISK-0014's business). Docstrings on anything you
write. Risk rows to 48.14.

## Definition of done

- [ ] `reporting_journey_test.dart` observed **executing** against staging on both platforms in CI.
- [ ] Verdict recorded: Verified with URL + counts, or Deferred with a named blocker.
- [ ] **NR-001 confirmed at runtime** — controls locked during generation and re-enabled after.
- [ ] Real evidence a report document was generated.
- [ ] Attendance-report leg strengthened or its conditional guard justified.
- [ ] RISK-0014's continued accuracy confirmed for 48.14; not fixed, not asserted as fixed.
- [ ] Every defect classified and root-caused; sibling paths checked; regression tests added.
- [ ] `flutter analyze` 0 issues, `dart format` clean, `flutter test` green (flake diagnosed).
- [ ] `Upcoming Prompts/mine-flow-STEP-48.8-FINDINGS.md` written.
- [ ] Committed on `step-0048-runtime-evidence`.

## Next

Tell the user the next action is *"run substep 48.9"* (Timeline & Notifications) in a **fresh
chat**, and update 48.8's status in the STEP PLAN.
