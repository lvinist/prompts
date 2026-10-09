# mine-flow — STEP-55.11 RESIDUAL-2: CI run 133 E2E remediation (daily-log submit path, popup-route dismiss over-fire, cross-leg attendance race, equipment go-race, timeline emit guard)

> **How to run:** Tell your agent "run 55.11 residual-2". Execute cold in a fresh chat.
>
> **Assigned model: Hermes/Claude Opus 4.8.** Strongest tier: this lane carries a P0
> write-path regression that every local gate is blind to, a shared-navigation
> primitive change (route observer), and the STEP-55 gate's close evidence.

## Context

CI runs 36156534137 (`afead08`, #132) and 36176012366 (`d0f3bfc`, #133) both failed
E2E: Android 19 passed / 4 failed / 2 skipped; Web 15 / 1. The `d0f3bfc` observer
revert fixed only deep_link. Local artifacts: `.step55.6-ci/` (`android/`, `web/`,
`prev_android/`, `prev_web/`, `r125/`, `r133/`). Read them before theorizing — every
claim below is pinned to a log line or a local probe.

## Root causes (verified 2026-09-26, this analysis)

1. **[P0 product] daily_log submit always throws after any prior autosave.**
   `DailyLogBloc._onSubmitDailyLog` calls `autoSaveDraft(log.copyWith(status:
   submitted))` then `submitDailyLog(id)`. The 48.23 monotonic guard makes the
   submit-time autosave write `submitted` into the cache; the 55.6 strict-machine
   guard in `submitDailyLog` then throws `only a draft can be submitted (current
   status: submitted)`. Probe (real Hive + real repository): submit threw on the
   journey-mirrored sequence. The 48.23 unit test passes only via the null-cached
   path; widget tests mock the repository — every local gate is blind. Web passes
   VACUOUSLY (≥800px side-panel leaves the list tappable with the sheet still open);
   Android fails at `:209` (`Semua (0)`, no form pop in the router log).
2. **[P0 product/test-blocker] AppResponsiveSheet.didPushNext over-fires on popup
   routes.** Material `DropdownButtonFormField` pushes `_DropdownRoute` (a
   PopupRoute) onto the branch navigator; go_router 18 merges root observers into
   branch navigators, so BOTH observer placements see it. The dirty sheet opens the
   non-dismissible AppDirtyDismissDialog ON TOP of the dropdown. Hit-test evidence:
   `Unsaved changes` swallowing the category tap, identical in runs 125/131/132/133,
   both platforms. This blocks the inventory journey (android + web) and is wrong
   UX for real users.
3. **[Test-infra] attendance cross-leg staging race.** Web leg finishes its step-9
   edit (constant remark `Izin resmi shift pagi`) ~11 min before android's step-7
   read-back (run 132: 15:54:20Z vs 16:05:45Z; same-day rows, same staging DB).
   Android's backfill pulls the web row and `findMutated`'s userId fallback returns
   it. Run 125 shows the identical signature.
4. **[Journey race] equipment_check**: `appRouter.go` fires while the dirty form
   sheet is still mounted (success listener hasn't run — the async read-back pumps no
   frames); PopScope vetoes the go() and the dirty dialog blocks the filter taps
   (`:206`/`:208` hit-test shows the barrier). The D4 veto is designed behavior;
   the journey must wait for the sheet.
5. **[P2 latent] TimelineCubit.loadData can emit after close** (run 132 deep_link
   `failed after test completion`). `d0f3bfc` removed the CI repro but the unguarded
   emits remain.
6. **[Escalation — owner decision] Foreman-created zones never reach staging.**
   Staging `zones` is EMPTY (verified); foremen have no zones INSERT policy (42501),
   so every daily-log sync referencing a locally-created zone dies on
   `daily_logs_zone_id_fkey` (23503). Do NOT change policies or migrations in this
   lane.

## Residual scope (exact — nothing else)

1. **Daily-log submit write path (P0).** In `daily_log_bloc.dart`
   `_onSubmitDailyLog`: persist field edits as DRAFT first, then promote —
   `await _repository.autoSaveDraft(currentState.log.copyWith(updatedAt: now))`
   (still draft), then `await _repository.submitDailyLog(id)` (promotes, spread-copy
   preserves the just-written fields incl. hazard). `updatedLog` (submitted) is used
   only for the emitted state. Pin with a repository regression test that mirrors
   the CACHED-draft path (the probe sequence: autosave(draft) → submit flow →
   expect success; the current code fails this — write the test RED first), and a
   bloc test against a REAL repository (not a mock) driving summary→hazard→submit.
   Note in findings that web daily_log CI green was vacuous (sheet never closes;
   wide layout lets assertions pass) — the web journey's step-10 poll must gain a
   hard assertion that the sheet actually closed (fail-fast with bloc state), so
   this class can never pass vacuously again.
2. **Popup-route dismiss over-fire (P0, shared primitive).** Change
   `lib/core/navigation/route_observer.dart` to `RouteObserver<PageRoute<void>>`
   (RouteObserver filters non-R routes in didPush), sweep every
   subscribe/unsubscribe site (attendance_screen, daily_log_list_screen,
   AppResponsiveSheet, AppDetailInspector, fixture pages) with a
   `route is PageRoute<void>` guard before subscribing (no throws on dialog-hosted
   routes). Popup pushes (dropdown menus, showDialog popovers, the dirty dialog
   itself) stop firing didPushNext; page-level didPushNext/didPopNext (the 55.5/55.6
   list-refresh contract) must keep working — pin with: (a) widget test: dirty sheet
   + open a Material dropdown above it → NO AppDirtyDismissDialog; (b) existing
   route/list-refresh tests and the m2 adversarial stress suite stay green.
3. **Attendance journey cross-leg hardening.** Make the step-9 edit remark
   unique-per-run (timestamp suffix, like the sick remark). Rework `findMutated`:
   id match first, then remarks==uniqueRemark, userId last. Step-7's read-back
   filters by uniqueRemark. Do NOT touch the product; do NOT serialize the CI legs.
4. **Equipment journey go-race.** Before `appRouter.go(AppRoutes.equipmentCheck)`
   (journey `:197`), poll for the form sheet to be gone (bounded 50×100ms, mirroring
   daily_log step 10) and assert absence with a reason carrying the bloc state —
   fail fast if the submit path regresses instead of failing opaquely at the filter.
5. **TimelineCubit emit guard (P2).** Guard each emit in `loadData` (and `refresh`)
   with `if (isClosed) return;` after awaits. One-line + test optional (a
   load-then-close unit test is cheap and honest).
6. **Zone RLS/FK escalation — STOP AND ASK.** Present the owner the options:
   seed a stable staging zone (migration/runbook — schema gate), grant foreman
   INSERT on zones (policy change), or defer with the truth recorded in findings
   (daily-log staging round-trip stays unprovable for the create-zone path). Do not
   pick one. Record the staging zones-empty REST probe as current evidence.

## Read first

- `.step55.6-ci/r133/android.log` + `web.log`, `r125/`, `android/`, `prev_android/`
  (the hit-test overlays, `Semua (0)`, FK/RLS warnings, absence of a form-pop router
  event in the daily-log journey)
- `lib/features/daily_log/presentation/bloc/daily_log_bloc.dart`
  (`_onSubmitDailyLog` ~:387), `data/repositories/daily_log_repository_impl.dart`
  (`autoSaveDraft` monotonic guard ~:139, `submitDailyLog` guard ~:166),
  `test/unit/daily_log_repository_test.dart` (48.23 test — null-cached path only)
- `lib/core/presentation/widgets/app_interaction_primitives.dart`
  (didPushNext ~:289, `_requestDismiss`, PopScope ~:420),
  `lib/core/navigation/route_observer.dart`,
  go_router 18 `route.dart` (`_MergedNavigatorObserver`, `notifyRootObserver`)
- `integration_test/journeys/daily_log_journey_test.dart` (:161–209),
  `attendance_journey_test.dart` (:95–330, :435),
  `equipment_check_journey_test.dart` (:160–210),
  `inventory_journey_test.dart` (category retry :103–135)
- `lib/features/timeline/presentation/bloc/timeline_cubit.dart`

## Pre-flight (do not skip)

1. `git status --short --branch` + `git log --oneline -5`. The branch may carry a
   concurrent lane's commits (d0f3bfc as of 2026-09-26); pull before starting.
   `lib/l10n/app_localizations*.dart` were dirty with pure CRLF churn (HEAD 0 CR →
   disk 872/414/416) — classify and preserve; do not absorb or revert other lanes'
   files. Do NOT run `dart format` on `.arb` files.
2. Kill stale `dart.exe`/`dartaotruntime.exe` before any flutter run (a probe left
   processes alive 2026-09-26; chromedriver IPv6-bind conflict is the known symptom).
3. Local web-drive harness exists (`.step55.6-run-web-daily_log.sh`,
   chromedriver 4444, `--dart-define`s from `.env`; foreman creds are present —
   never print them). Web drive ≈4–6 min/run. Inventory/equipment/attendance can be
   reproduced the same way via a wrapper.

## Likely files (ownership boundary)

- ALLOWED: `lib/features/daily_log/presentation/bloc/daily_log_bloc.dart`,
  `lib/core/navigation/route_observer.dart` + the subscribe sites it types
  (attendance_screen, daily_log_list_screen, app_interaction_primitives),
  `lib/features/timeline/presentation/bloc/timeline_cubit.dart`,
  `integration_test/journeys/{daily_log,attendance,equipment_check}_journey_test.dart`,
  `test/unit/daily_log_repository_test.dart` (+ the new cached-draft regression),
  a new real-repository bloc test, `test/widget/` sheet-dropdown regression test.
- FORBIDDEN: migrations/SQL, RLS policies, `supabase/**`, the hazard
  entity/DTO/repository internals (they passed audit), other features' product code,
  `lib/l10n/**` (no new visible strings in this lane), CI workflow files.

## Tests and verification

- RED-first: new repository regression (cached-draft submit) must fail before the
  bloc fix and pass after; commit the fix and the test together.
- `flutter test test/unit/daily_log_repository_test.dart test/features/daily_log/
  test/widget/daily_log_screen_test.dart test/widget/attendance_screen_test.dart`
  + the new files; `flutter analyze`; `dart format --set-exit-if-changed` (dart files
  only); the l10n baseline guard if any string moved (none should).
- Local web-drive: daily_log (must now assert the sheet actually closed), inventory
  (dropdown no longer triggers the dirty dialog), equipment (poll before go).
- CI is the final gate: push, then read the new run's per-journey results; a
  passing run requires BOTH platforms' inventory + android daily_log/attendance/
  equipment green. Record run id + head sha in findings.

## Boundaries and escalation

- No schema/policy/migration changes; no CI workflow edits; no secret/PII output;
  never print `.env` values.
- Escalate (do not work around): the zone RLS/FK decision (item 6); any disagreement
  between local and CI results after the fixes; if the observer retype breaks a
  route-aware consumer you cannot reconcile.

## Definition of done

- Submit-after-cached-draft is pinned RED→GREEN; web daily_log journey asserts real
  sheet closure (no vacuous pass).
- Dirty sheet + popup route no longer opens the discard dialog; page-level
  didPopNext/didPopNext contracts still pass (55.5/55.6 tests).
- Attendance journey is collision-proof against concurrent CI legs.
- Equipment journey waits out the sheet; timeline cubit cannot emit after close.
- Zone RLS/FK decision recorded with owner's answer; findings + index rows updated
  (55.6/55.7/55.8/55.9/55.0 evidence cells point at the fixing commits); CI run for
  the new head is green on both E2E legs or failures are honestly adjudicated.
