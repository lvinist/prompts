# mine-flow — STEP-55.6 RESIDUAL: apply the hazard/approval migration to the live database, regenerate the contract artifact, approval-dialog Material purge, findings evidence

> **How to run:** Tell your agent "run 55.6 residual fix only". Execute cold in a fresh chat.
>
> **Assigned model: Hermes/Claude Opus 4.8.** Same tier as 55.6 — this lane carries a real
> data-integrity P0 (unapplied migration) plus authorization semantics; silent errors here corrupt
> safety and approval records.

## Context

The Daily Log contract is genuinely well built. The migration
`supabase/migrations/20260912000001_step_55_6_daily_log_hazard_contract.sql` is real and
substantial: the four hazard columns with a coherence CHECK (severity required iff present, notes/
action meaningful only when present), a `SECURITY DEFINER` `BEFORE UPDATE` trigger
(`enforce_daily_log_transition`) that enforces exactly draft→submitted→approved, supervisor-only
approval with `approved_by IS DISTINCT FROM auth.uid()` rejection, approved-row immutability, and
foreman RLS rescoped to own-draft rows. The Dart side matches: `HazardAssessment.isValid` +
`normalized()`, `approveDailyLog` rejecting non-submitted/duplicate, `_onApproveDailyLog` in the
BLoC, and `Doc 04` v0.1.8 records the contract with a version-log bump. Test coverage is strong
(14 hazard contract tests + 18 repository tests + 9 widget tests covering role tabs, hazard-blocks-
submit, and read-only submitted records).

**But the migration was never applied to the live database**, so every hazard-bearing write fails
at the server. The audit (2026-09-21, this file) left four residuals. Fix only those.

## Residual scope (exact — nothing else)

1. **P0 — apply the migration to the live/staging Supabase database.** Verified by the audit:
   `GET /rest/v1/daily_logs?select=hazard_state` returns
   `42703 column daily_logs.hazard_state does not exist`, and an insert carrying `hazard_state`
   fails `PGRST204 Could not find the 'hazard_state' column of 'daily_logs' in the schema cache`.
   The 55.8 migration `20260913000001_step_55_8_inventory_transactions.sql` is **also** unapplied
   (`inventory_transactions` is absent from the live schema cache) — it is 55.8's lane to confirm,
   but a `db push` applies both at once, so coordinate or run the push and report both. Follow
   `Code/mine-flow-docs/runbooks/staging-provision.md` Step 3: `supabase login` →
   `supabase link --project-ref <STAGING_PROJECT_REF>` → `supabase db push` (idempotent; skips
   already-applied migrations) → verify with `supabase migration list --linked` that every local
   migration shows applied. **Then re-prove the columns live** by re-running the REST probes from
   the audit (`?select=hazard_state`, plus `hazard_severity`/`hazard_notes`/`hazard_action`) and
   paste the responses into the FINDINGS addendum. If `supabase login` credentials are not present
   in this session, that is an owner escalation — stop and ask the user, do not work around it.
2. **Regenerate `supabase/types/database.ts`.** The committed artifact is **stale**: its
   `daily_logs.Row` lists 13 columns and **omits all four hazard columns**, even though the
   migration that added them has been committed since 2026-09-13. The contract guard
   (`tool/check_supabase_contracts.dart`) passes because it only checks the artifact's shape and
   migration/artifact *commit* pairing — it cannot detect that the artifact disagrees with the
   actual database. Fix it the documented way:
   `supabase gen types --lang typescript --linked > supabase/types/database.ts`, then confirm the
   four hazard columns are present in the regenerated file. (Note: the STEP-48.17 artifact was
   regenerated correctly — the stale-detection gap is specific to post-48.17 migrations.)
3. **Contract-guard hardening (small).** `check_supabase_contracts.dart` should fail when a
   committed migration's new columns are absent from the artifact. A minimal, honest version: for
   each `ALTER TABLE ... ADD COLUMN` / `CREATE TABLE` in committed migrations, check the artifact
   names that table and those columns. If a full parser is disproportionate, add a targeted
   regression check for the four hazard columns on `daily_logs` with a comment naming the 2026-09-21
   incident — the point is that this exact silent drift must not pass twice. Keep it mechanical;
   do not invent a general schema-diff engine.
4. **Approval-confirm dialog is still Material (P2).** `daily_log_list_screen.dart:169-191` builds a
   Material `AlertDialog` with `TextButton`/`FilledButton` for the `Setujui Log` confirmation.
   Spec §4.5 item 9 (`FC-54.6-009`) requires no unbounded Material form control remains, and the
   file already carries the "Material: no ForUI equivalent" header — but ForUI `FDialog` (or the
   shared `confirmDestructiveAction` helper already used by the delete path on the same screen,
   `:374-386`) covers this case. Migrate to the shared helper or `FDialog` preserving: the named
   record/date/foreman confirmation text (`'Setujui log {date} dari {foremanName}? ...'`), the
   `barrierDismissible: false` behavior, and the confirm→`ApproveDailyLogEvent` wiring with
   `supervisorId ?? currentUserId()` (never a URL-supplied id). Pin with a widget test.
5. **`FC-54.6-010` runtime/authorization audit stays Unverified at this lane** (same 55.11
   deferral). Add mechanical coverage only: role tab defaults/counts, supervisor-only approval
   visibility, duplicate/wrong-state rejection surfaces, offline queued/failed truth, deep links,
   IME, long text, 48dp, focus, both themes. Do not claim runtime verification you did not run.
   Roles unavailable in the harness stay `Unverified`.
6. **Findings hygiene.** `mine-flow-STEP-55.6-FINDINGS.md` is 5 short sections with no test counts,
   no commands, no file list, and no schema evidence — it does not meet the PLAN's per-substep
   evidence contract (items 1-7), and its "All tests passed" claim is unverifiable as written.
   Supersede it with a dated "Residual fix (55.6)" section carrying the exact commands, the
   `migration list --linked` output, the REST probe responses, and the test counts. Do not delete
   the original section.

## Read first

- `Upcoming Prompts/mine-flow-STEP-55-PLAN.md` (evidence contract + ground rules + "No outbound
  transmission of source, secrets, PII, or runtime data")
- Master spec §4.5 (all 11 items), §3.1 (D6), §5 (D7 verdicts)
- `Upcoming Prompts/mine-flow-STEP-55.6-PROMPT.md`, `mine-flow-STEP-55.6-FINDINGS.md`
- `supabase/migrations/20260912000001_step_55_6_daily_log_hazard_contract.sql`,
  `supabase/migrations/20260913000001_step_55_8_inventory_transactions.sql`,
  `supabase/types/database.ts` (daily_logs Row at line 229), `supabase/config.toml`
- `Code/mine-flow-docs/runbooks/staging-provision.md` (Steps 2-4), `architecture/04-data-model.md`
  (v0.1.8 entry — already correct; no doc change needed once the DB matches it)
- `lib/features/daily_log/presentation/pages/daily_log_list_screen.dart` (approval dialog 169-191,
  role-tab strip 434-473, supervisor gating `:366-369`), `daily_log_form_sheet.dart`
  (`_flushPendingSave` 147-168), `presentation/bloc/daily_log_bloc.dart` (`_onApproveDailyLog` 454+)
- `lib/features/daily_log/domain/entities/hazard_assessment.dart`,
  `data/repositories/daily_log_repository_impl.dart` (`approveDailyLog` 206-240)
- `lib/core/presentation/widgets/confirm_destructive_action.dart` (the shared helper to reuse)
- `tool/check_supabase_contracts.dart` (the guard to harden)
- `test/unit/hazard_assessment_test.dart`, `test/unit/daily_log_repository_test.dart`,
  `test/widget/daily_log_screen_test.dart`, `test/features/daily_log/**`

## Pre-flight (do not skip)

1. `git status --short --branch` + `git log --oneline -5` in `Code/mine-flow-app`. The shared
   branch `step-0055-cohesive-ui-rebuild` moved during the audit window (now at `fa9ab71`, which
   landed the 55.2/55.3 residual lane). Pull before branching; preserve untracked scratch
   (`.step55.11*` scripts, `run_web_wrapper.dart`, `m2_challenger_stress_test.dart`) and never
   stash/reset/absorb another lane's dirt.
2. Confirm `supabase login` works and which project `config.toml`'s `project_id` resolves to
   before pushing anything to a database. The audit confirmed the live project answers REST on the
   `.env` `SUPABASE_URL` and that the hazard columns are absent there.
3. This lane touches `supabase/**` and `tool/**` — no other 55.x lane does, so it will not
   conflict, but the `db push` must be coordinated with the user (it changes a shared database).

## Likely files (ownership boundary)

- ALLOWED: `supabase/types/database.ts` (regenerate), `tool/check_supabase_contracts.dart`
  (hardening), `lib/features/daily_log/presentation/pages/daily_log_list_screen.dart` (dialog
  migration only), `test/widget/daily_log_screen_test.dart` (extend),
  `Upcoming Prompts/mine-flow-STEP-55.6-FINDINGS.md` (append).
- FORBIDDEN: editing migration SQL files (they are immutable history — the drift is in the
  database, not the files), the hazard entity/DTO/repository/BLoC internals (they passed audit
  clean), other features, `lib/l10n/**` unless a new visible string proves necessary.

## Tests and verification

- `flutter test test/unit/hazard_assessment_test.dart test/unit/daily_log_repository_test.dart test/widget/daily_log_screen_test.dart test/features/daily_log/`
- `dart format --output=none --set-exit-if-changed <touched files>`
- `flutter analyze`
- `supabase migration list --linked` — every local migration applied (the audit's evidence command)
- REST re-probes of `daily_logs.hazard_state`/`hazard_severity`/`hazard_notes`/`hazard_action`
- `dart run tool/check_supabase_contracts.dart` — must still pass, and must now catch the
  hazard-column-absence case if the artifact is stale again.
- Record exact commands + counts. ONE commit `fix(55.6): ...` (plus the regenerated artifact —
  it is part of the same logical change), daily-log/supabase-owned hunks only.

## Boundaries and escalation

- No Kanban, arbitrary transitions, client-only authorization, hazard UI without persistence,
  mutable approved log, invented user identity, or secret/PII artifacts — all already satisfied at
  the client; do not regress them.
- The trigger and RLS tightening in the migration are the server-side enforcement; do not weaken
  them to make a test pass. If a row's `hazard_state` default interacts badly with existing data
  on push, stop and report rather than editing the migration.
- Escalate (do not work around): missing `supabase login` credentials; a `db push` that reports a
  conflict or partial application; any disagreement between the regenerated artifact and the REST
  probes; or if the approval dialog migration breaks the confirm-named-record copy.
- Never print secrets — the REST probes must not include the anon key or any token.

## Definition of done

- The hazard/approval migration is applied to the live database and proven by REST probes (and
  `migration list --linked`); the 55.8 migration is applied or explicitly assigned to its lane.
- `supabase/types/database.ts` regenerated and carries the four hazard columns.
- The contract guard fails on this exact staleness pattern in the future.
- The approval-confirm dialog uses the shared ForUI helper with semantics and wiring preserved.
- Runtime/authorization audit honestly deferred with mechanical coverage added.
- FINDINGS has a dated "Residual fix (55.6)" section with commands, migration output, and counts.

## Next

Report the exact replacement evidence-cell line for index row 55.6 — including whether the row is
now flippable to Done (do **not** flip it yourself; the 55.6 row currently reads Done but its
evidence cell omits the migration-drift incident and must be updated). Then run the 55.7 residual
lane in a fresh chat — its P1 is a supervisor-only control that silently never appears in
production.


---

## E2E residual routed from 55.11 (2026-09-23) — daily_log list visibility

**Source:** CI run `35894532969` at app head `fe17e2d`.
**Failure:** Web `daily_log_journey_test.dart:170` — `Found 0 widgets with type "DailyLogCard"`; Android `:169` — `DailyLogListScreen` not found (`Expected: exactly one matching candidate`).

The journey logs in **as foreman** (`role:'foreman'`, `:55`), creates a structured daily log, then at `:166-170` navigates to `AppRoutes.dailyLog` and expects `DailyLogListScreen` + at least one `DailyLogCard`. The created log is not visible in the list.

**Not a stale finder.** Two candidate causes to disambiguate on-device / in-test:
1. **Role-gating** — 55.6 made the list role-aware (foremen create, supervisors review). Confirm the foreman's freshly-created log renders as a `DailyLogCard` in the foreman's own list view, and that `DailyLogListScreen` mounts for the foreman role at all (Android shows the *screen* missing, which points at a route/role guard, not just an empty list).
2. **Read-back lag** — the route-hosted form leaves the list mounted beneath; confirm the list re-fetches after the sheet pops (the same `RouteAware`/`didPopNext` pattern attendance needed in 55.5).

**Scope:** daily_log list visibility + role view only, `lib/features/daily_log/**`. Re-run `flutter test integration_test/journeys/daily_log_journey_test.dart` (needs `TEST_FOREMAN_*` staging creds; verified in CI).


---

## E2E residual re-route from 55.11 (2026-09-24) — daily_log is NOT a flake: order-dependent list-mount failure

**Source:** CI runs `35996412883` (`e5d10a7`) and `36015384410` (`9d29896`).
**Failure:** `daily_log_journey_test.dart:169` — `Found 0 widgets: DailyLogListScreen`
(`Expected: exactly one matching candidate`). Web.

**Adjudication corrected — this is a REAL reproducible failure, not a flake.**
It passed once at `58a52c5` (run `35980569440`), then failed **twice** with
byte-identical daily_log code at `e5d10a7` and `9d29896` (the intervening commits
touch only ci.yml, offline_sync, and 55.8 schema — never daily_log). Two
consistent failures on unchanged code = order-dependent / environmental, but
deterministic — not random noise. The earlier "suspected flake" call is
withdrawn.

### CORRECTION 2026-09-24 (diagnosis pass) — the "full-suite ordering" theory above is WRONG. Ignore it.

Two facts overturn the ordering theory:

1. **Web runs each journey as its OWN isolated `flutter drive` process.** The CI
   web loop is `for file in integration_test/app_boots_test.dart
   integration_test/journeys/*_test.dart; do flutter drive --target=wrapper …`
   — a fresh app boot per journey, no shared in-process state. "State leaking
   from a preceding journey" is IMPOSSIBLE on web. (The `9d29896`→`c982c55`
   commit `c982c55` double-pop guard already targeted the right area but did NOT
   fix the symptom.)

2. **The failure is at `:169` (step 10), NOT `:66` (step 2).** Step 2 has the
   identical `expect(find.byType(DailyLogListScreen), findsOneWidget)` and it
   PASSES — the list mounts fine after login. Everything from `:66`→`:168` runs
   without throwing (form opens, submit at `:139` succeeds, repo readback
   `:143-157` passes). The screen is only absent at `:169`, which runs AFTER the
   submit → form-sheet auto-close → `appRouter.go(dailyLog)` re-navigation at
   `:166`.

**Corrected root-cause direction: a single-journey, deterministic post-submit
navigation race.** After submit, the form sheet's success path
(`daily_log_form_sheet.dart:219-229`) schedules `Future.delayed(600ms) →
_handleClose() → context.pop()`. The test meanwhile calls
`appRouter.go(AppRoutes.dailyLog)` at `:166`. The `c982c55` guard
(`_formRoute?.isCurrent != true`) tried to suppress the stale pop but the symptom
is unchanged — the delayed close still races the test's `.go`, and the net result
is the navigator is NOT showing `DailyLogListScreen` at `:169`. Investigate the
close-vs-renavigate ordering: either the delayed `_handleClose` still pops the
list route (guard insufficient / `isCurrent` true at fire time), or the test's
`.go(dailyLog)` at `:166` is itself swallowed/superseded by the pending close.
Consider having the sheet signal close completion the test can await, or drop the
delayed-close entirely and let the test drive the navigation deterministically.

**LOCAL-REPRO BLOCKER (must resolve before a fix can be verified locally):** this
journey needs `TEST_FOREMAN_EMAIL` / `TEST_FOREMAN_PASSWORD` — absent from `.env`
(only USER + SUPERVISOR present), so it `markTestSkipped`s locally instead of
running. Either add foreman staging creds to `.env` (passed only via
`--dart-define`, never printed) to reproduce locally, or verify the fix in CI
only. Do NOT claim a local verification without foreman creds.

**Scope:** daily_log post-submit close/renavigate race,
`lib/features/daily_log/presentation/pages/daily_log_form_sheet.dart` +
`daily_log_journey_test.dart:166-169`. Reproduce with foreman creds (web
`flutter drive` single journey is enough — it is NOT an ordering bug). Re-run in
CI to confirm.


### UPDATE 2026-09-25 (local repro + fix attempt — timer theory DISPROVEN, corrected hypothesis below)

Foreman creds are now in `.env` (`TEST_FOREMAN_EMAIL=foreman@mineflow.dev`,
password = supervisor's) so this journey RUNS locally instead of skipping.
A local web-drive repro harness exists: start `chromedriver --port=4444`, write
`run_web_wrapper.dart` importing this journey, then `flutter drive
--driver=test_driver/integration_test.dart --target=run_web_wrapper.dart -d
web-server --browser-name=chrome` with the `--dart-define`s from `.env`.
Reproduces `:169 Found 0: DailyLogListScreen` every run.

**HARD EVIDENCE (in-test `matchedLocation` probe at `:167`, since reverted):**
after submit + the app's post-submit close, `appRouter.state.matchedLocation ==
`/teams`` with `DailyLogListScreen count = 0` and `DailyLogFormSheet count = 0`.
The navigation lands on **`/teams` — one level ABOVE the list** (`/teams/daily-log`).

**Bisection fact:** if the test waits for the sheet to fully close BEFORE issuing
its own `appRouter.go(dailyLog)`, `:169` passes and the failure moves forward to
`:203` (`find.text(testSummary)` = 0 — a SECOND, separate list-visibility defect
the race was hiding).

**Timer-cancel fix ATTEMPTED and FAILED (do not repeat it):** I converted the
`Future.delayed` success-close (`daily_log_form_sheet.dart:219-229`) into a stored
`Timer` cancelled in `deactivate()`. Analyzer clean, but the drive re-run was
UNCHANGED (`loc=/teams list=0`). Reverted. **Conclusion: this is NOT merely a
timer-vs-go() race — cancelling the pending close does not fix it.**

**CORRECTED HYPOTHESIS — the close pops ONE LEVEL TOO HIGH (stack-depth /
double-pop), not a timing race.** The create form is pushed as a CHILD of
`/teams/daily-log` (`daily_log_list_screen.dart:190 _openCreateForm →
context.pushNamed('daily-log-form')`), so a single `pop()` should return to the
list at `/teams/daily-log`. Instead it lands on `/teams`. Something pops twice
or the stack is not what the route hierarchy implies. Candidates to instrument
next (log the router stack + whether each fires):
- Does `_handleClose` run more than once? (success listener may re-fire on a
  second `DailyLogFormState` emission — `successMessage` stays non-null, the same
  class as attendance ATT-02's `_hasClosed` latch in the close report §2. A
  one-shot latch on the close is the likely fix, NOT a timer cancel.)
- Does `AppResponsiveSheet.onDismissApproved` ALSO fire a close in addition to
  the success-timer close (two close paths → two pops)?
- Is the form route actually a child of `/teams/daily-log` at runtime, or is it
  mounted on the root navigator (so pop returns to `/teams`)?
Instrument `_handleClose` call count + `context.canPop()` + the GoRouter
location BEFORE and AFTER each pop. Fix is almost certainly a **one-shot close
latch** (pop exactly once) — mirror the attendance ATT-02 `_hasClosed` idiom —
then separately fix the `:203` list-visibility.

**LOCAL VERIFICATION IS NOW POSSIBLE** (foreman creds + web-drive harness). Do
not hand this back as CI-only — reproduce and confirm the fix locally before
push. Budget for a full web-drive cycle (~4-6 min per run; the drive can hang if
a prior dart process is left alive — `taskkill /F /IM dartaotruntime.exe` and
shut down chromedriver between runs).
