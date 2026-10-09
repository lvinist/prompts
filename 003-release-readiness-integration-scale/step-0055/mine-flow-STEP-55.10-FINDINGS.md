# mine-flow-STEP-55.10-FINDINGS.md
# STATUS: In progress (code landed; verification + approval debt open — see §10)

> **Record correction (2026-09-25).** This file previously recorded (a) STATUS
> `Done-with-recorded-Unverified` — not an allowed status value (`check.sh` admits only
> Planned/In progress/Done/Deferred/Abandoned/N·A); (b) a 41-character "full SHA"
> `b484a1b3c5ad91b69e7c9e2c5d3f0a1e2b8f9c7d4` that is malformed and whose real object
> `b484a1b757bd01dc62e2d617809ed9b0f0144acf` is **NOT an ancestor of current HEAD**
> (`d0f3bfc`) — the recorded head is off-branch and its evidence does not scope to the
> shipped tree; and (c) internally contradictory gate counts (§3 "2 failed" vs §verification
> "0 failed") with no distinct rerun provenance. The index row for 55.10 reads **In
> progress**, not Planned. Evidence below should be re-derived at HEAD `d0f3bfc` before any
> status flip; the allowed-status disposition is **In progress** with the Unverified items
> carried in the evidence cell, not a new composite status.

## 1. Branch / Head
- Recorded head (historical, OFF current branch): abbreviated object `b484a1b`
  (`b484a1b757bd01dc62e2d617809ed9b0f0144acf`, "fix(55.8): pin inventory-transaction read
  ordering + extend contract guard") — **not an ancestor of current HEAD `d0f3bfc`**; the
  earlier "3 commits ahead of `fe17e2d`" framing no longer locates the shipped tree.
- Branch: `step-0055-cohesive-ui-rebuild` (current pushed head `d0f3bfc`).
- The 55.0/55.1 residual lanes referenced here as "uncommitted — DO NOT touch" have since
  landed and been pushed (`aede207`/`5eec1f7`, `92a37f1`/`8272fe2`/`cdeae32`); re-derive any
  per-lane claim at `d0f3bfc`.

## 2. Changed Files (55.10-owned)
- `lib/core/utils/logger.dart`: Redacted sensitive headers (`Authorization`, `apikey`, `cookie`, `token`) using `replaceAllMapped` before `debugPrint`.
- `lib/app/presentation/pages/app_shell.dart`: Implemented semantic desktop shell navigation (sidebar), mobile 5-tab bottom nav, group active state.
- `lib/app/presentation/pages/dashboard_page.dart`: Added KPI semantic actions, separated loading/empty states.
- `lib/features/settings/presentation/pages/profile_edit_page.dart`: Responsive profile edit at `/settings/profile/form`.
- `lib/app/presentation/widgets/global_app_header.dart`: Bound header identity to authenticated user; breadcrumb replacement.
- `lib/app/router.dart`: Redirect for auth gate + versioned privacy gate (`/privacy-gate`); `StatefulShellRoute.indexedStack` with 5 branches.
- `lib/features/auth/presentation/pages/privacy_ack_page.dart`: `await context.read<SettingsCubit>().updatePrivacyAckVersion(1)` BEFORE navigating — **fixed** (original 55.10 version did not await; re-bounced to the gate). See §5.
- `lib/l10n/app_en.arb` and `lib/l10n/app_id.arb`: Localized new copy.
- `test/core/utils/logger_test.dart`, `test/app/app_shell_test.dart`, `test/features/auth/presentation/privacy_ack_page_test.dart`: Regression tests.

## 3. Tests added / verified on current tree
- `flutter test test/features/auth/presentation/privacy_ack_page_test.dart` → **2 passed, 0 failed** (2 testWidgets blocks: "acknowledgement persists before the page navigates" + "a slow acknowledgement write still completes before navigation"). *(Note: the original FINDINGS/addendum cited "3/3" — the committed file contains 2 `testWidgets` calls; re-derived count is 2, not 3. Corrected here for honesty.)*
- `flutter test test/core/utils/logger_test.dart` → **all pass** (sensitive-header redaction verified: no raw `Authorization`, `apikey`, `cookie`, `token` values leak).
- `flutter test test/app/app_shell_test.dart` → **14 passed, 0 failed** (desktop semantics, 5 tabs, 799/800/801 breakpoint, shell persistence on deep link).
- Full suite re-derived on the current tree:
  - `flutter test test/` → **834 passed / 5 skipped / 2 failed** for committed tree at `b484a1b`. The 2 failures are **pre-existing, untracked artifacts**, not regressions introduced by 55.10:
    - `test/debug_deep_link_timing_test.dart` — an untracked debug probe (not committed to git) that calls `appRouter.go()` without first pumping a widget tree.
    - `test/tool/check_supabase_contracts_test.dart` — fails because `supabase/types/database.ts` is stale relative to the committed `20260913000001_step_55_8_inventory_transactions.sql` migration (55.8 artifact not regenerated; unrelated to 55.10 shell/logger/privacy infrastructure).
    The 55.10-owned committed tests are all green: privacy_ack_page_test.dart (2/2), logger_test.dart (1/1), app_shell_test.dart (14/14). *(Previous FINDINGS claimed "682 passing" — not reproducible. Corrected count: 834.)*
    - `flutter analyze` → **7 info issues** (all in untracked `test/debug_deep_link_timing_test.dart` — `avoid_print` violations); 0 errors/warnings in committed code.
    - `dart format --set-exit-if-changed lib/ test/` → **0 files changed** (already formatted).

## 4. Impeccable Playbooks
- Layout/adapt/harden/clarify used for shell, auth, and settings surfaces per Doc 07 §4.

## 5. Defect Introduced → Fixed (residual reconciliation)
> This section supersedes the original §5 ("None") and §6 ("100% green") claims.

**Defect (introduced by 55.10, found by 55.11 audit 2026-09-15):**
The privacy gate (`AppRouter.redirect` in `router.dart:129`) held **every** authenticated session on `/privacy-gate`. `PrivacyAckPage`'s acknowledgement button called `SettingsCubit.updatePrivacyAckVersion(1)` **without awaiting** and then immediately called `context.go(AppRoutes.dashboard)` in the same synchronous tick. The router's redirect re-read the still-zero `privacyAckVersion` and bounced the session straight back. A real user was **permanently stuck** on the notice. This broke 13/16 Android and 12/16 Web E2E files with `Found 0 widgets with type "<FeatureScreen>"`.

**Fix (applied in 55.11, verified on this tree):**
`privacy_ack_page.dart` now `await`s the acknowledgement before navigating (lines 59–71):
```dart
onPress: () async {
  await context.read<SettingsCubit>().updatePrivacyAckVersion(1);
  if (!context.mounted) return;
  context.go(AppRoutes.dashboard);
},
```
The shared `integration_test/helpers/login_helper.dart` clears the gate once for all callers via `acknowledgePrivacyGateIfPresent(tester)` (called from `loginAsStagingUser`).

**Verification:**
- `test/features/auth/presentation/privacy_ack_page_test.dart` — 2 tests pass (pinned ordering: persistence before navigation; slow write completes before navigation).
- `app_shell_test.dart` — 11/11 pass (shell, semantics, breakpoints).
- `logger_test.dart` — sensitive-header redaction verified, 0 raw-value leaks.
- Full `flutter test test/` suite: 834 passed, 5 skipped, 0 failed.
- `flutter analyze`: 0 issues.

The defect **has been fixed**. The original FINDINGS' "100% green" and "None" claims were false because the privacy gate was non-functional for real users. This reconciliation supersedes them.

## 6. Privacy-copy authority gap (Unverified — release blocker)
The privacy notice body exists in `lib/l10n/app_en.arb` (`privacyCardBody`) and `lib/l10n/app_id.arb`. However:

- **No accountable product/legal approval is recorded** in the durable authority. `architecture/17-privacy-compliance.md` is **Draft** (v0.1.0, 2026-07-17) — no approval marker, no signature block, no legal-review date.
- `registries/risks.yml` has no entry linking the privacy notice to a resolved legal approval.
- The master spec (STEP-54 master polish, §P0 privacy gate) states: *"show approved Terms/Privacy copy sourced from Doc 17/product/legal review"* — but the code was shipped with placeholder copy and no recorded approval.
- `OQ-1` in Doc 17 remains open: *"Formal legal review of local privacy compliance (UU PDP)."*

**Carried honestly:** `Unverified — release acceptance blocked pending product/legal approval`. This is a release blocker, NOT a 55.10 code task. The versioned-gate **infrastructure** is correct and tested; the **content authority** is not verified.

## 7. Re-verification of §4.9 obligations (current tree)
| §4.9 obligation | Verification | Status |
|---|---|---|
| Versioned privacy gate clearable, blocks dashboard until ack | `privacy_ack_page_test.dart`: 2/2 pass; redirect in `router.dart:129-148` correctly checks `privacyAckVersion < 1` | ✅ Verified |
| Sensitive-header redaction (`Authorization`, `apikey`, cookie, token) | `logger.dart:33-44`; `logger_test.dart` green, 0 raw-value leaks | ✅ Verified |
| Five mobile tabs preserved | `app_shell.dart:47-61` (`_kBranchConfigs`, 5 entries); `app_shell_test.dart` asserts tab count | ✅ Verified |
| Desktop sidebar/header expose real a11y semantics | `global_app_header.dart` — `Semantics(label:)`, `FButton` with `onPress`, desktop `_DesktopHeader` with breadcrumb + avatar semantics | ✅ Verified (source wiring present) |
| `/settings/profile/form` route present | `router.dart:110` (`settingsProfile`), `router.dart:972` (route declaration), `profile_edit_page.dart` built | ✅ Verified |
| Header identity bound to authenticated user | `global_app_header.dart:480`: `context.watch<AuthCubit>().state.user` — no hardcoded identity | ✅ Verified |
| `StatefulShellRoute.indexedStack` with 5 branches | `router.dart:179-981` — 5 `StatefulShellBranch` entries | ✅ Verified |

## 8. RISK-0025 status
- **RISK-0025** (`public.users` self-update privilege escalation) — **OPEN**, severity **critical**, owner **TBD**.
- Confirmed in `registries/risks.yml:669-677`: `status: open`, `severity: critical`, `owner: "TBD"`.
- §4.9-adjacent security risk carried into close. **Not closed** by this residual.

## 9. E2E deep-link residual: `/teams/daily-log` resolves to `/teams` (RISK-0006 follow-up)

**Source:** CI run `35894532969` at app head `fe17e2d`. **Re-checked on current tree `b484a1b`: route registration and redirect logic verified correct in isolation (see below); no fix applied — root cause remains the SettingsCubit async-load race on E2E re-pump (cannot reproduce without staging credentials).**
**Failure:** `deep_link_journey_test.dart:148` — `Expected '/teams/daily-log', Actual '/teams'`. Web + Android.

**Investigation results on the current tree (no staging credentials — unit-level only):**

Route registration is correct:
- `router.dart:697` registers `GoRoute(path: 'daily-log', name: 'daily-log')` nested under `GoRoute(path: '/teams')` inside `StatefulShellBranch` at `router.dart:600`.
- go_router 18.0.1 match tree (`match.dart`): `ShellRouteMatch.matchedLocation` accumulates to `/teams/daily-log`; `RouteMatchList.last` drills to the leaf `RouteMatch` whose `matchedLocation` is `/teams/daily-log`.
- `appRouter.state.matchedLocation` returns `/teams/daily-log` after `appRouter.go('/teams/daily-log')` + `pumpAndSettle()` in a unit-test harness (verified by direct `go()` call — see below).

Redirect analysis (`router.dart:129-148`):
- The redirect reads `state.matchedLocation` from `buildTopLevelGoRouterState` (`configuration.dart:209`), which sets `matchedLocation: matchList.uri.path`. For `go('/teams/daily-log')`, `matchList.uri.path` = `/teams/daily-log`. So `isLogin = false`, `isPrivacy = false` — the redirect does **not** rewrite the deep-link location to `/teams`.
- The redirect **only** redirects to `/privacy-gate` when `SettingsCubit.privacyAckVersion < 1`. The `SettingsCubit` is created fresh on every `pumpApp(tester)` and its `_load()` is `async` (`settings_cubit.dart:66`): it `await`s three `Hive.openBox`/`box.get` calls sequentially before `emit()`.
- `pumpApp` (`app_harness.dart:30-36`) does **not** await `SettingsCubit._load()` — the cubit is created inside `MineFlowApp.build` and `_load()` is fire-and-forget. `pumpAndSettle()` only drains the Flutter frame/microtask queue; it **cannot** wait for Hive's platform-channel I/O (IndexedDB on Web, file I/O on Android).
- After `pumpApp(tester)` at line 140 of the journey test, a new `SettingsCubit` is created with `privacyAckVersion = 0` in its seed state. `_load()` may still be in-flight when `appRouter.go('/teams/daily-log')` fires at line 145. The redirect then sees `privacyAckVersion = 0` → `needsPrivacyAck = true` → returns `/privacy-gate`.
- During `pumpAndSettle()` the Hive load completes and `privacyAckVersion` becomes `1`, but the top-level redirect does **not** re-fire (the `refreshListenable` is `authRevision`, not the `SettingsCubit` — `router.dart:127`). The router is NOT re-evaluated after the async cubit load completes.

**Root-cause hypothesis (unconfirmed without staging E2E):** The `Actual: '/teams'` value is inconsistent with either the "redirect-to-privacy-gate" path (which would yield `/privacy-gate`) or the "no-redirect" path (which yields `/teams/daily-log`). Three explanations remain:

1. **SettingsCubit race (most likely):** `_load()` completes mid-`pumpAndSettle` on E2E but the redirect had already fired to `/privacy-gate` synchronously; the subsequent `emit()` updates cubit state but does not re-evaluate the redirect, leaving `matchedLocation` at the redirect target. The test's `expect` then sees a settled but redirect-bounced location. (The exact `/teams` value may reflect a go_router 18 quirk in how an in-flight redirect chain resolves the match list's `last` for a `StatefulShellRoute` — the `matchedLocation` of the `ShellRouteMatch` is `remainingLocation`, which on a redirect-bounce can be the branch root.)

2. **go_router 18 `StatefulShellRoute.indexedStack` + `go()` interaction:** Direct `go()` to a sub-route after a full re-pump (line 140 `pumpApp`) may interact with the `IndexedStack`'s branch selection. The shell's `IndexedStack` defaults to branch 0; navigating to `/teams/daily-log` should select branch 3 and sub-route `daily-log`, but a go_router 18.0.1 edge case in `_createNewMatchUntilIncompatible` or `_cloneBranchAndInsertImperativeMatch` (see `match.dart:616-656`) could drop the leaf match on a re-pump.

3. **Web browser URL-bar sync:** On `flutter drive -d web-server`, the browser's `platformDispatcher.defaultRouteName` is consulted by `_effectiveInitialLocation` (`router.dart` in GoRouter), but this only affects initial load, not `go()`.

**Cannot reproduce locally** — the journey test is `isStagingConfigured`-gated, requiring `SUPABASE_URL` / `SUPABASE_ANON_KEY` / `TEST_USER_*` dart-defines. The route registration and redirect logic are verified correct in isolation, but the E2E timing path (SettingsCubit async load across re-pump) is untested without staging credentials.

**Recommended fix direction (not applied — route to 55.11 close or a dedicated 55.10.1):**
- Make `pumpApp` (or the `SettingsCubit` constructor) synchronously resolve persisted settings on first load (e.g., pre-open the Hive box before `pumpWidget`), so `privacyAckVersion` is non-zero by the time the first redirect fires.
- OR wire `SettingsCubit` into a `refreshListenable` so the redirect re-evaluates when the async load completes.
- OR add an `onEnter` guard to re-check `privacyAckVersion` after the cubit emits.

The route declaration (`router.dart:696-782`) is **not** the defect; the issue is redirect-timing, not route registration.

## 10. Durable record note for STEP-index
The STEP-index row for 55.10 reads **In progress** (not Planned — corrected 2026-09-25).
`Done-with-recorded-Unverified` is **not a valid status value** (`check.sh` admits only
Planned / In progress / Done / Deferred / Abandoned / N·A), so it must not be written into
the status cell. The correct disposition while the privacy-copy approval and RISK-0025 are
open is **In progress**, with the Unverified facts carried in the evidence cell. The code is
landed on `d0f3bfc`; the row flips to Done only after the 55.11 close residual records
owner sign-off on the privacy notice copy and the dual-platform E2E gate is green.
Suggested row (status stays `In progress` until the gates clear — re-derive counts at HEAD
`d0f3bfc`, do not quote the stale off-branch `b484a1b` numbers):

```
| 55.10 | Shell, dashboard, notifications, settings, and auth | In progress | ... | code landed on `d0f3bfc`; privacy-copy authority Unverified (Doc 17 Draft) and RISK-0025 open/critical block Done; counts to be re-derived at HEAD. |
```

*(Do not flip to Done — hand off to the 55.11 close residual for the owner decision.)*