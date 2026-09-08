# mine-flow — STEP-48.7: Benchmark Journey + NR-006 Route Registration (settles 45.7, RISK-0019)

> **How to run:** tell your agent *"run substep 48.7"*. Self-contained — runnable cold.

**Assigned model: Gemini 3.1 Pro High.** This substep closes a named risk (RISK-0019), which means the
hard part is not running the test but stating honestly what the in-process `flutter drive` harness did
and did not prove about a cold browser deep-link. It also checks CRS/coordinate round-tripping, where a
silent corruption would be a serious data-integrity defect. **Escalate to Opus 4.8** if coordinates or
CRS do not round-trip cleanly, or if you are unsure whether the available evidence justifies closing
RISK-0019 versus narrowing it — an overstated closure is worse than an honest re-justification.


## Context

Read `Upcoming Prompts/mine-flow-STEP-48-PLAN.md`, then the 48.0/48.1/48.2 findings and
`mine-flow-STEP-48.3-FINDINGS.md` — **48.3 (auth) must be Verified first.**

STEP-45 row 45.7: `Deferred — benchmark_journey_test.dart authored; NR-006 not settled →
RISK-0019 → STEP-48`.

This substep carries a **named risk to close**. **RISK-0019** (`monitoring`, medium,
"BenchmarkForm deep-link / route-registration (NR-006)") states: *"STEP-46 finding NR-006 requires
deep-linking to `/operations/benchmark-db/form` on web to ensure shell persistence. Test skipped in
STEP-45 due to missing staging credentials."* Its revisit trigger — *"When staging credentials and
web E2E testing are available"* — is exactly the condition 48.0 and 48.2 created. There is no
excuse left for deferring it.

Context on the route: **STEP-38.5** corrected the Benchmark route to `/operations/benchmark-db` and
added the sidebar entry, after breadcrumb/segment work. NR-006 is about whether deep-linking
*directly* to the form (rather than navigating to it) resolves and keeps the app shell — i.e.
whether the route is properly registered inside the shell branch rather than as a top-level route
that replaces it.

`benchmark_journey_test.dart` (13 assertions) already imports `appRouter`, `AppShell`,
`BenchmarkFormScreen`, and `BenchmarkListScreen`, and its header comment names the CF-033/CF-034
coordinate-and-CRS persistence guards plus NR-006 / CF-097. The scaffolding is there; it has simply
never run.

## Read these first

- `Upcoming Prompts/mine-flow-STEP-48-PLAN.md` — honesty rule, D1, Q4.
- `…-48.0/1/2/3-FINDINGS.md`.
- root `.throughstone/local-user.md` — Experience level 2, Explanatory.
- `Code/mine-flow-docs/registries/risks.yml` — **RISK-0019** verbatim (this substep closes or
  re-justifies it); RISK-0006 (go_router v18, deep links — 48.11 owns it, but the two overlap:
  share findings); RISK-0009 (`EditableText` finders).
- `Code/mine-flow-docs/architecture/03-architecture-overview.md` and
  `architecture/07-ui-design-system.md` — the app-shell/navigation contract.
- `Code/mine-flow-docs/architecture/04-data-model.md` — the benchmark table, coordinate and CRS
  columns.
- `Code/mine-flow-app/integration_test/journeys/benchmark_journey_test.dart`.
- `Code/mine-flow-app/lib/app/router.dart` — route definitions, shell branches, `AppRoutes`.
- `Code/mine-flow-app/lib/features/benchmark/` — form, list, and `lib/core/utils/crs_utils.dart`
  (STEP-36.1 delivered the CRS utilities).

## Scope

**In scope:** running `benchmark_journey_test.dart` against staging on both platforms; settling
NR-006 with real web deep-link evidence; recording whether RISK-0019 can close.

**Not in scope:** the general deep-link sweep across all routes and RISK-0006 (48.11 owns that —
this substep covers the benchmark form specifically), other feature areas, the design review
(48.13), editing risk rows (48.14 applies the change; you supply the evidence and recommendation),
docs (48.15).

## Your task

### 1. Run the journey

```bash
cd Code/mine-flow-app
flutter test integration_test/journeys/benchmark_journey_test.dart -d emulator-5554 \
  --dart-define=SUPABASE_URL="$SUPABASE_URL" --dart-define=SUPABASE_ANON_KEY="$SUPABASE_ANON_KEY" \
  --dart-define=TEST_USER_EMAIL="$TEST_USER_EMAIL" --dart-define=TEST_USER_PASSWORD="$TEST_USER_PASSWORD" \
  --dart-define=APP_ENV=staging
```

Secrets from the shell environment only.

### 2. Settle NR-006 properly — on web

NR-006 is a **web** finding. Android's in-process `appRouter.go(...)` is not the same thing as a
browser loading a URL cold, so an Android pass does **not** close RISK-0019. Use `flutter drive`:

```bash
flutter drive --driver=test_driver/integration_test.dart \
  --target=integration_test/journeys/benchmark_journey_test.dart \
  -d web-server --browser-name=chrome --dart-define=…
```

What must be proven, explicitly:

1. Navigating to `/operations/benchmark-db/form` **resolves** to `BenchmarkFormScreen` — not a 404,
   not a redirect to the list.
2. The **app shell persists** — `AppShell` (sidebar) is still in the widget tree, i.e. the form is
   inside the shell branch and did not replace it.
3. The **auth redirect** behaves: hitting that URL unauthenticated goes to login, and after login
   the user lands somewhere sensible.

Note the harness limitation honestly: `integration_test` under `flutter drive` drives the app
in-process, so `appRouter.go()` plus a shell-presence assertion is the closest achievable proxy for
a cold browser load. If a genuine cold URL load cannot be exercised by this harness, **say so** and
state precisely what was and was not proven — then decide whether RISK-0019 can close on the
available evidence or must be re-justified with a narrower, honest description. Do not claim a cold
deep-link was verified if it was not.

### 3. Verify the CRS / coordinate persistence guards

CF-033 / CF-034: create a benchmark with coordinates and a CRS, save, reload from staging, and
assert both round-trip unchanged. CRS handling is easy to get subtly wrong (axis order, datum,
precision loss) and a silent coordinate corruption in a mining benchmark database is a serious
data-integrity defect, not a cosmetic one. Check `lib/core/utils/crs_utils.dart` behaviour against
what is persisted.

### 4. Triage honestly

Route drift from STEP-38.5, stale finders, Material-widget expectations from before STEP-37 — all
legitimate test fixes; record each. A real app defect gets a root-cause fix, a sibling-path check,
and a regression test. Never delete an assertion to get green.

### 5. Authoritative CI evidence

Commit, push to `step-0048-runtime-evidence`, confirm the journey **executes and passes** in both
`e2e-web` and `e2e-android`, and record the run URL plus real counts. (CI logs without `gh`: PAT
from `git credential fill` as a Bearer token; `/actions/jobs/<id>/logs` 302s to Azure Blob which
rejects the auth header — follow `redirect_url` bare.)

### 6. Record it, with a RISK-0019 recommendation

`Upcoming Prompts/mine-flow-STEP-48.7-FINDINGS.md`:

- journey verdict: Verified with run URL + counts, or Deferred with a named blocker and trigger;
- a dedicated **NR-006 / RISK-0019** section: what was proven, on which platform, by what
  mechanism, and what remains unproven;
- an explicit recommendation for 48.14: **close RISK-0019** (with the evidence reference) or
  **re-justify it** with a narrowed description and a new trigger. Do not edit `risks.yml` yourself;
- CRS/coordinate round-trip results;
- anything relevant to RISK-0006 for 48.11 to reuse.

## Verification

- Journey **executes** on both platforms in a CI run on the branch head, counts quoted; or an
  honest Deferred.
- NR-006 settled with **web** evidence, and the harness's limitations stated plainly.
- Coordinates and CRS confirmed to round-trip through staging unchanged.
- `flutter analyze` → 0 issues; `dart format --set-exit-if-changed .` → clean.
- `flutter test` → green (the `attendance_daily_log_sync_test.dart` Hive flake is known: re-run
  isolated to confirm, and say so).
- Any app fix carries a regression test.
- No secret value in any log, report, or commit.

## Keeping the docs true

If the benchmark route's real registration differs from what
`architecture/03-architecture-overview.md` or the router documentation describes, hand it to 48.15
with the section and correction. If CRS handling diverges from `architecture/04-data-model.md`,
same. Docstrings on anything you write. `registries/risks.yml` edits belong to 48.14 — you supply
evidence and a recommendation, not the edit.

## Definition of done

- [ ] `benchmark_journey_test.dart` observed **executing** against staging on both platforms in CI.
- [ ] Verdict recorded: Verified with URL + counts, or Deferred with a named blocker.
- [ ] NR-006 settled with web evidence; what was proven and what was not stated explicitly.
- [ ] An explicit close-or-re-justify recommendation for **RISK-0019** written for 48.14.
- [ ] CF-033 / CF-034 coordinate and CRS round-trip verified against staging.
- [ ] Every defect classified and root-caused; sibling paths checked; regression tests added.
- [ ] `flutter analyze` 0 issues, `dart format` clean, `flutter test` green (flake diagnosed).
- [ ] `Upcoming Prompts/mine-flow-STEP-48.7-FINDINGS.md` written.
- [ ] Committed on `step-0048-runtime-evidence`.

## Next

Tell the user the next action is *"run substep 48.8"* (Reporting / PDF) in a **fresh chat**, and
update 48.7's status in the STEP PLAN.
