# mine-flow — STEP-55.11 RESIDUAL-2 FINDINGS (B-fix lane)

**Date:** 2026-10-01
**Branch / head:** `step-0055-cohesive-ui-rebuild` @ `afe14d6` (pushed; local == origin)
**Baseline before this lane:** `d0f3bfc`, CI run `36176012366` att 2 = `failure`
(E2E Web + Android both red).
**Executed by:** Hermes/Claude Opus 4.8 (parent session).
**Scope:** CI run 133 E2E remediation items B1–B5 from
`mine-flow-STEP-55.11-RESIDUAL-2-PROMPT.md`. Item 6 (zone RLS/FK) escalated to
owner — see §6.

Every fix is RED→GREEN pinned where a unit/widget tier can express it; the
journey-only items (B3/B4) are fixture hardening verified by analyze + the full
focused suite, and their true proof is the next CI run (`36891797012`, pending
at time of writing).

## Commits (this lane)

| Commit | Item | Summary |
|---|---|---|
| `0d1b449` | B2 | `routeObserver` typed `RouteObserver<PageRoute<void>>`; subscribe sites guarded `route is PageRoute<void>`; popups no longer fire the dirty-dismiss guard. |
| `a3d6b06` | B1 | daily-log submit autosaves the current **draft** then promotes via `submitDailyLog`; no longer throws "only a draft can be submitted" after a cached autosave. |
| `85d1994` | B5 | `TimelineCubit.loadData` guards both post-await emits with `if (isClosed) return;`. |
| `afe14d6` | B3+B4 | attendance read-back matches id→unique-remark→userId and the edit remark is unique-per-run (cross-leg collision proof); equipment journey polls for the form sheet to close before `appRouter.go`. |
| `5b6d395` | B4-toast-UX | equipment submit-success toast pinned to `FToastAlignment.bottomCenter` — a real UX defect (ForUI's touch default `topCenter` covered the top filter button for its 5s). Kept, but NOT the B4 filter-tap fix (see `03180ec`). Attendance journey gains `ensureVisible` before the sick-choice tap and the reason-field `enterText` (run-138 off-screen flake). |
| `03180ec` | B4 | **The actual fix:** removed the journey's second `appRouter.go()` after submit, which raced the form's own success navigation and left the route's modal scope (the `AppResponsiveSheet` `ColoredBox` scrim) mounted over the history screen; mirror the green daily-log pattern (poll form gone, let exit animation settle). |

## Findings per item

### B1 — daily-log submit write path (P0 product) — FIXED
- **Root cause (confirmed):** `_onSubmitDailyLog` called
  `autoSaveDraft(log.copyWith(status: submitted))` then `submitDailyLog(id)`.
  On the normal journey a debounced autosave has already cached a DRAFT row, so
  the 48.23-re-run-5 monotonic guard (`max(incoming, cached)`) promoted the
  cached row to `submitted` on that call; `submitDailyLog` then read a non-draft
  row and threw. Web passed vacuously (≥800px side-panel left assertions
  tappable); Android failed at `:209` (`Semua (0)`).
- **Fix:** autosave `currentState.log` (still draft → persists field edits as a
  draft), then `submitDailyLog(currentState.log.id)` performs the single
  promotion. The submitted entity is used only for the emitted UI state.
- **Evidence:** new real-repository bloc test
  `test/features/daily_log/presentation/daily_log_submit_real_repo_test.dart`
  (RED pre-fix: "only a draft can be submitted"; GREEN after). Updated the
  48.23-re-run-5 bloc pin's `verify` to `autoSaveDraft(any()).called(1)` (the
  submit flow's own draft persist) — the concurrent-drop contract is unchanged.
  Repository suite, daily_log widget suite, bloc suite all green.
- **Web vacuous-pass note:** the web daily_log journey's step-10 poll still
  needs a hard sheet-closed assertion to prevent future vacuous passes — called
  out in the prompt (item 1); the step-10 hardening is NOT in this lane's diff
  and remains a follow-up for the web-drive journey file.

### B2 — popup-route dismiss over-fire (P0 shared primitive) — FIXED
- **Root cause (confirmed in SDK source):** `routeObserver` was
  `RouteObserver<ModalRoute<void>>`. `RouteObserver.didPush`
  (`flutter/.../routes.dart:2500`) only forwards `didPushNext` when both routes
  are of its type `R`. A Material `DropdownButtonFormField` opens
  `_DropdownRoute` (`material/dropdown.dart:483` — a `PopupRoute`, hence a
  `ModalRoute`), so it matched `R`, fired `didPushNext` on the still-mounted
  dirty sheet, and raised the non-dismissible discard dialog over the dropdown
  (inventory journey red, both platforms).
- **Fix:** narrow `R` to `PageRoute<void>` (`PopupRoute` does NOT extend
  `PageRoute`); guard every `subscribe` site with `route is PageRoute<void>`
  (AppResponsiveSheet, attendance_screen, daily_log_list_screen). Page-to-page
  `didPopNext` (55.5/55.6 list refresh) still fires.
- **Evidence:** new widget regression
  `test/widget/sheet_popup_dismiss_regression_test.dart` (RED pre-fix: discard
  dialog appeared; GREEN after). m2 adversarial stress suite, interaction-
  primitives suite, router suite all green.

### B5 — TimelineCubit emit-after-close (P2) — FIXED
- **Root cause:** `loadData`/`refresh` await two repo reads; close before they
  resolve throws "Cannot emit new states after calling close" (CI deep_link
  "failed after test completion").
- **Fix:** `if (isClosed) return;` before both post-await emits.
- **Evidence:** new close-before-reads-resolve test in
  `timeline_cubit_test.dart` (`completes`, no throw); existing cubit tests green.

### B3 — attendance cross-leg staging race (test-infra) — FIXED
- **Root cause:** concurrent web/android CI legs share one staging DB; the
  step-7 read-back keyed on `userId` matched the sibling leg's same-day row, and
  the step-9 edit remark was a CONSTANT (`'Izin resmi shift pagi'`) so the
  sibling's edit poisoned the read-back.
- **Fix:** `findMutated` matches id → unique-per-run remark → userId (last
  resort); the step-9 edit remark is now `'...${millisecondsSinceEpoch}'`,
  matching the step-5 sick remark. No product change; legs NOT serialized.
- **Evidence:** analyze clean; the collision only manifests under parallel CI,
  so the true proof is run `36891797012`.

### B4 — equipment journey go-race (journey) — FIXED
### B4 — equipment journey filter tap blocked (journey) — **RESOLVED (2026-10-02)**

**Diagnosis trail (kept honest — three theories, two wrong):**

1. **Toast theory — WRONG.** Pinned the submit toast to
   `FToastAlignment.bottomCenter` (`5b6d395`) on the theory that ForUI's
   touch default `topCenter` put the toast over the filter button. A local
   Pixel_6a run **with the toast pinned to the bottom still reproduced the
   identical absorbing chain at the identical top point `(340, 209)`** — so
   the toast was never the interceptor. The toast pin is KEPT anyway: a top
   toast over the history screen is a real UX defect (a user cannot reach
   the top filter button during its 5s), and it costs nothing.
2. **Lingering CustomTransitionPage barrier — the mechanism, but the first
   fix for it was wrong.** The route is `opaque:false` with a transparent
   `barrierColor` that still absorbs. The journey's poll for the
   `EquipmentCheckFormScreen` **widget** reported "gone" while the route's
   modal scope was still mounted over the history screen.
3. **What actually fixed it (`03180ec`):** the journey fired a **second**
   `appRouter.go(AppRoutes.equipmentCheck)` right after submit, racing the
   form's own success navigation (`_handleClose` → `context.go`). Removed
   the second `go()` — mirror the green daily-log journey step 10 exactly:
   poll for the form to leave the tree, then boundedly pump to let the exit
   animation settle. No second navigation.

**Evidence:** the frontmost object in every hit-test chain is the
`AppResponsiveSheet`'s own full-screen `ColoredBox` barrier
(`app_interaction_primitives.dart:454`, a `Positioned.fill` +
`GestureDetector(opaque)` + `ColoredBox` dimming scrim), i.e. the form
sheet itself still mounted — not the toast, not a go_router barrier.

- **Local verification (Pixel_6a, swiftshader):** equipment journey green,
  **zero hit-test warnings**; attendance journey green. A temporary probe
  (scratch, removed) confirmed at tap time: `AppResponsiveSheet` count 0,
  `EquipmentCheckFormScreen` 0, `EquipmentHistoryScreen` 1.
- **CI verification (run 139, `37003629360`, head `03180ec`):** equipment
  journey ✅ and attendance journey ✅ — both **green on Android for the
  first time in this lane** (both were ❌ in run 138). Web stayed green.
  This is the authoritative dual-platform proof for B4 + the attendance
  ensureVisible fix.
- **The Android *job* still reports `failure`, but for an unrelated,
  pre-existing reason:** the only remaining failure is
  `design_review_capture_test.dart:208` (the 25-cell screenshot matrix,
  0/25 captures) — identical single failure in run 138, file untouched by
  this lane's commits, and already a known deferred item (substep 48.13,
  "2/25 PNGs / 23 screenshot timeouts"). It is NOT in the B-fix lane's
  scope.
- **Superseded:** `68313f2`/`cdf6888`/`1f05804` (toast-wait attempts) and
  the "modal barrier" diagnosis. `afe14d6` (sheet-close poll) is kept —
  correct, independent guard.
- **Honest caveat:** the submit success path is async (bloc → repository →
  sync queue), so a slower renderer can still land the history screen with
  the route's exit animation mid-flight. The settle pumps are bounded, not
  gated on the barrier being gone; if CI's timing is slower still, the
  robust follow-up is to poll for the **route** (not the widget) being gone
  via `appRouter.routeInformationProvider.value.uri` before tapping.



### B6 (prompt item 6) — zone RLS/FK — ESCALATED, owner chose SEED
- Staging `zones` is empty and foremen have no INSERT policy, so a daily-log
  sync referencing a locally-created zone dies on FK `daily_logs_zone_id_fkey`
  (23503) / RLS (42501).
- **Owner decision (2026-10-01):** seed a stable staging zone via a SEPARATE
  schema STEP (drafted for review, NOT run in this lane). Draft:
  `Upcoming Prompts/mine-flow-STEP-56-DRAFT-staging-zone-seed.md`.
- Until that STEP lands, the daily-log **create-zone** staging round-trip stays
  **Unverified**. No policy/migration/`supabase/**` change was made here.

## Boundaries honored
- No schema/SQL/RLS/`supabase/**` edits; no CI workflow edits; no secrets/PII
  printed; no `.env` values read.
- All eight touched tracked files verified LF-clean (0 CR in committed blobs),
  except journey/test files already CRLF-by-convention at HEAD (attendance
  459→483 CR added lines keep the file's own CRLF convention; equipment is
  LF). `git diff --cached --check` clean on all commits.

## Verification ledger (local)

| Gate | Result |
|---|---|
| `flutter analyze lib/` | No issues |
| sheet_popup_dismiss_regression (B2) | RED→GREEN |
| daily_log_submit_real_repo (B1) | RED→GREEN |
| timeline_cubit close guard (B5) | GREEN |
| daily_log repo + bloc + widget suites | GREEN |
| m2 adversarial + interaction-primitives + router | GREEN |
| attendance_screen widget suite | GREEN |

**Pending:** CI run `36891797012` (head `afe14d6`) is the authoritative
dual-platform E2E verdict for B1–B5; B3/B4 can only be proven there (parallel
legs / real emulator). Watcher: `.step55.11-ci-watch.sh`.
