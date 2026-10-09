# mine-flow — STEP-55.7 RESIDUAL: wire the supervisor-only delete control to the authenticated session, runtime audit, findings evidence

> **How to run:** Tell your agent "run 55.7 residual fix only". Execute cold in a fresh chat.
>
> **Assigned model: Gemini 3.7 Flash High.** Same tier as 55.7 — the migration surface is bounded
> and the verdicts are exact, but the residual is an authorization control, not cosmetics.

## Context

The Equipment Check migration is complete and clean by static measures: `ExpansionTile` is gone
(detail is route-backed at `/teams/equipment-check/:id`), the detail screen fetches by ID and
renders a read-only inspector (`mobileFullPage: true` on narrow, right inspector on wide), the form
is an `AppResponsiveSheet` with a `_isDirty` D4 guard and an access-denied panel, PASS/FAIL are
labelled `SizedBox(height: 48, child: FButton(...))` with dual icon+text, foreman identity comes
from the session (never the URL), and the report is contextual. 27 focused tests pass, `flutter
analyze` is clean, and the live test suite was re-run during this audit (8/8 green).

**But the supervisor-only delete control is silently dead in production.** The audit (2026-09-21,
this file) left three residuals. Fix only those.

## Residual scope (exact — nothing else)

1. **P1 — `authCubit` is an undefined identifier in the detail screen, so the supervisor-only
   delete footer silently never renders in production.**
   `lib/features/equipment_check/presentation/pages/equipment_check_detail_screen.dart:237` reads
   `final user = authCubit?.state.user;` — but `authCubit` is not a field, parameter, local, or
   import of that file. It resolves only because `auth_cubit.dart:16` declares a **process-wide
   global** `AuthCubit? authCubit;` (set once in `main.dart:60`). That global is genuinely the
   intended production source of session state (`currentUserId()`, `isAuthorizedSite()`, and the
   router all read it), so this is not a compile error — `dart analyze` reports "No issues found".
   The defect is that `main.dart` sets the global but **never provides the cubit into the widget
   tree**, and the detail screen never reads it from the tree either. Net effect today:
   `authCubit?.state.user` is whatever the global happens to hold, and the delete footer's
   `isSupervisor` gate is unverified against the actual authenticated session in a routed context.
   Proven by this audit: temporarily making the test file stop seeding the global (only for the
   probe, then reverted) flipped 4 of 8 tests from pass to fail — including
   "hides delete action for non-supervisor viewers" and "destructive delete action triggers
   confirmation" — proving the tests assert the *global*, not the screen's own wiring.

   Fix it to read the authenticated session through the tree the way the rest of the app does:
   either (a) resolve `AuthCubit` via `context.read<AuthCubit>()` — `MineFlowApp` provides it at
   the root (`app.dart:34-37`, create: `authCubit ?? AuthCubit(...)`) and `equipment_check_form_screen.dart`
   already uses `currentUserId()` from the same auth module — or (b) accept the global but then
   **the screen must obtain it explicitly and the test must not be the only thing seeding it**.
   Option (a) is preferred: it makes the session source explicit and testable per-widget. Keep
   `authCubit?.state.user` semantics for the fallback case where the widget is pumped outside the
   app root (the smoke path), matching `MineFlowApp`'s own no-op fallback.

   Then make the test honest: `test/widget/equipment_check_detail_screen_test.dart` currently sets
   the global in `setUp` and emits a supervisor `AuthState` (line ~63) — the *only* reason the
   delete tests pass. After the fix, provide the `AuthCubit` through `BlocProvider<AuthCubit>` in
   `buildTestWidget` (the production wiring) and assert the supervisor/foreman cases against the
   provided cubit, with the global left unset. Mirror the pattern already used by
   `test/widget/equipment_check_form_test.dart:249-256` (which sets the global for the
   session-derived foreman-identity case — convert that one too if it can read from the tree).
2. **`FC-54.7-007` runtime audit stays Unverified at this lane** (same 55.11 deferral as 55.2-
   55.4). Add mechanical coverage only: contrast of the PASS/FAIL badges, long-list (15-30 item)
   focus/reading order and semantics, 48dp targets on the checklist controls and filter buttons,
   sheet single-scroll-owner behavior, full-page mobile detail geometry, the not-found and
   access-denied panels, and the report dialog preserving list state. Do not claim runtime
   verification you did not run.
3. **Findings hygiene.** `mine-flow-STEP-55.7-FINDINGS.md` is the most thorough of the 55.x set,
   but it claims its "zero `ElevatedButton`, `Card`, or `TextButton`" purge test as an Impeccable
   result — it is a widget-tree assertion, not an Impeccable playbook output, and the file admits
   `impeccable` was never runnable in its environment. Supersede with a dated "Residual fix
   (55.7)" section that (a) records the `authCubit` defect and its root cause in the project's
   standard defect-table shape (symptom / root cause / fix), (b) carries the exact commands and
   counts from item 1, and (c) corrects the Impeccable-playbook attribution. Do not delete the
   original section.

## Read first

- `Upcoming Prompts/mine-flow-STEP-55-PLAN.md` (evidence contract + ground rules)
- Master spec §4.6 (all 6 items), §2.5 (D4), §5 (D7 verdicts)
- `Upcoming Prompts/mine-flow-STEP-55.7-PROMPT.md`, `mine-flow-STEP-55.7-FINDINGS.md`
- `lib/features/equipment_check/presentation/pages/equipment_check_detail_screen.dart`
  (screen constructor 32-49, view constructor 66-76, authCubit read 237, footer gating 248, the
  not-found panel ~190-201 and access-denied panel ~204-222)
- `lib/features/auth/presentation/bloc/auth_cubit.dart` (global `authCubit` 16, `currentUserId`
  19, `isAuthorizedSite` 24-34), `lib/features/auth/presentation/bloc/auth_state.dart`
- `lib/app/app.dart` (root `BlocProvider<AuthCubit>` 34-37 + the `_NoopAuthRepository` fallback),
  `lib/main.dart:60` (the global assignment)
- `lib/features/equipment_check/presentation/pages/equipment_check_form_screen.dart` (the
  session-derived-foreman pattern at 50-56, `currentUserId()` — the reference wiring)
- `lib/app/router.dart` (equipment-check routes 873-940; the detail route does **not** pass an
  authCubit and does not need to once the screen reads it from the tree)
- `test/widget/equipment_check_detail_screen_test.dart` (setUp ~61-96, `buildTestWidget` ~99-126),
  `test/widget/equipment_check_form_test.dart` (249-256)

## Pre-flight (do not skip)

1. `git status --short --branch` + `git log --oneline -5` in `Code/mine-flow-app`. The shared
   branch `step-0055-cohesive-ui-rebuild` moved during the audit window (now at `fa9ab71`, which
   landed the 55.2/55.3 residual lane). Pull before branching; preserve untracked scratch
   (`.step55.11*` scripts, `run_web_wrapper.dart`, `m2_challenger_stress_test.dart`,
   `tool/verify_test_driver_adversarial.dart`) and never stash/reset/absorb another lane's dirt.
2. `dart analyze lib/features/equipment_check/presentation/pages/equipment_check_detail_screen.dart`
   will report clean *before* your fix — that is the trap, not a green light. The defect is a
   global-identifier resolution, which the analyzer cannot see.
3. This lane owns `equipment_check_detail_screen.dart` and the two equipment test files. No other
   55.x lane touches them.

## Likely files (ownership boundary)

- ALLOWED: `equipment_check_detail_screen.dart` (auth read + footer wiring only), optionally
  `equipment_check_form_screen.dart` if the same wiring is simplified, `app.dart` / `main.dart`
  only if the root provider needs adjusting (prefer not to — the provider already exists),
  `test/widget/equipment_check_detail_screen_test.dart`, `test/widget/equipment_check_form_test.dart`,
  `Upcoming Prompts/mine-flow-STEP-55.7-FINDINGS.md` (append).
- FORBIDDEN: SOP checklist content or domain meanings, the route shapes, other features,
  `supabase/**`, `lib/l10n/**` (no new strings should be needed — the delete control already has
  `l10n.equipmentCheckDeleteRecord` / `equipmentCheckDeleteConfirmMessage`).

## Tests and verification

- `flutter test test/widget/equipment_check_detail_screen_test.dart test/widget/equipment_check_form_test.dart test/widget/equipment_history_screen_test.dart test/unit/equipment_check_* test/integration/equipment_check_sync_test.dart`
- `dart format --output=none --set-exit-if-changed <touched files>`
- `flutter analyze`
- `dart run tool/check_l10n_baseline.dart` (expect pass; the equipment files are on the legacy-
  exempt list — that is **not** license to add new hardcoded strings)
- `dart run tool/check_supabase_contracts.dart` (expect pass; no schema change here)
- Record exact commands + counts. ONE commit `fix(55.7): ...`, equipment-owned hunks only.

## Boundaries and escalation

- No SOP checklist/content changes, URL user ID trust, mobile bottom-sheet detail, local expansion
  detail, or color-only status — all already satisfied; do not regress them.
- Do not replace the global `authCubit` wholesale; it is load-bearing for the router's redirect
  (`authRevision`) and for `currentUserId()`/`isAuthorizedSite()`. The fix is how the *screen*
  obtains the session, not where the session lives.
- Escalate if reading `AuthCubit` from the tree is impossible in the detail route's context (it
   should not be — `MineFlowApp` provides it above the router), or if the same global-resolution
   pattern appears in other detail/inspector screens (grep `authCubit?.state` across `lib/` and
   report the list rather than fixing them all in this lane — those are other owners' lanes).
- Never print secrets.

## Definition of done

- The supervisor-only delete footer reads the authenticated session through the widget tree (or an
  explicitly-obtained source), not a bare global identifier that only tests seed.
- The detail/form tests assert the role gating against the provided `AuthCubit`, with the global
  left unset; the 8/8 + 9/9 suites stay green.
- Runtime audit honestly deferred with mechanical coverage added.
- FINDINGS has a dated "Residual fix (55.7)" section with the defect table, commands, and counts;
  the Impeccable-playbook attribution is corrected.
- Gates green.

## Next

Report the exact replacement evidence-cell line for index row 55.7 — including whether the row is
now flippable to Done (do **not** flip it yourself). Then tell the user the 55.4-55.7 residual set
is complete and to review all four FINDINGS addenda plus the 55.6 database-migration handoff (the
only item in the set that changes shared infrastructure and needs the user's `supabase login`).


---

## E2E residual routed from 55.11 (2026-09-23) — equipment_check SOP `Bad state: No element`

**Source:** CI run `35894532969` at app head `fe17e2d`.
**Failure:** `equipment_check_journey_test.dart:207` — `Bad state: No element` (Web + Android). Line 207 is `await tester.ensureVisible(filterFlaggedBtn)` / the SOP-inspection region around the flagged-status filter — an iterable's `.single`/`.first`/`firstWhere` found no element (a finder or a data query returned empty where exactly one was expected).

**Investigate:** which `.single`/`.first` throws — the `Key('filter_status_flagged')` finder (`:206`) resolving to zero widgets, or a repository/list query. 55.7 rebuilt the equipment detail on a ForUI long-SOP sheet + history screen; confirm the flagged-status filter control and the `EquipmentCheckCard`/`EquipmentHistoryScreen` render with the expected keys after the migration.

**Scope:** equipment_check history/filter surface only, `lib/features/equipment_check/**`. Re-run `flutter test integration_test/journeys/equipment_check_journey_test.dart` (credential-gated; verified in CI).
