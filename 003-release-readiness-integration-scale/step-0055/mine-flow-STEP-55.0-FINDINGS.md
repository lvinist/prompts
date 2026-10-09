# STEP-55.0 Findings — Shared Responsive Interaction Foundation

**Date:** 2026-09-11  
**STEP status:** In progress  
**App branch:** `step-0055-cohesive-ui-rebuild`  
**Docs branch:** `step-0055-cohesive-ui-rebuild`  
**Prompts revision:** `main` at `f71f433` after STEP-55 status was flipped and pushed

## Pre-flight

- All three worktrees were clean before the substep started; `git pull --ff-only` reported up to date for app, docs, and prompts.
- Duplicate STEP scan: none. The only active/planned overlap was STEP-55 itself, covering `mine-flow-app`, `mine-flow-docs`, and `prompts`.
- Baseline gates passed before implementation: `dart format --output=none --set-exit-if-changed .`, `flutter analyze`, and full `flutter test` (550 tests, 5 skipped at baseline).
- App/docs branches were created as required. Prompts remains on shared `main`; its STEP-55 row is now `In progress` and the status update was pushed.

## Delivered

- Added `AppResponsiveSheet`, with wide right-sheet and narrow bottom-sheet geometry at the 800dp boundary, a modal scrim, body-only scroll, fixed header/footer, and a 48dp labelled close control.
- Added one `AppDismissController` contract covering every declared close reason, clean/dirty/busy decisions, and a localized non-dismissible dirty discard dialog.
- Added `AppDetailInspector`, `AppFilterPopover`, `AppCalendarDialog`, `AppStatusBadge`, `AppSyncStatusBadge`, `AppAccessibleIconButton`, `AppStatePanel`, and `AppPlatformSelect`.
- Added URL helper contracts for durable record ID validation and closing a form/detail while retaining query/list state.
- Added a minimal `__interaction-fixture` route and route-backed form fixture. It exists only to prove the shared contract; no production feature was migrated.
- Added Indonesian-first and English localization strings, regenerating the committed localization output.

## Verification

- Focused: `flutter test test/core/presentation/widgets/app_interaction_primitives_test.dart` — **9 passed**.
- Full: `dart format --output=none --set-exit-if-changed .` — passed; `flutter test` — **559 passed, 5 skipped**; `flutter analyze` — passed.
- Guards: `dart run tool/check_l10n_baseline.dart` and `dart run tool/check_supabase_contracts.dart` — passed.
- No new dependency, schema, or architecture/ADR/risk change was required.

## Impeccable and runtime evidence

- `impeccable context` could not be run: the `impeccable` executable is not installed/on PATH in this environment. No `init`, `document`, or `extract` command was run.
- Runtime Web and Pixel_6a capture is **Unverified**: it was not possible to run authenticated app capture without credentials, and the Impeccable launcher is unavailable. The fixture and widget tests validate geometry and semantics mechanically; production runtime evidence remains required during feature migrations and consolidated audit 55.11.
- The full test suite emits existing PDF-font warnings for U+2014; it still passes and is unrelated to this substep.

## Changed files

- `mine-flow-app/lib/core/presentation/widgets/app_interaction_primitives.dart`
- `mine-flow-app/lib/app/presentation/pages/app_interaction_fixture_page.dart`
- `mine-flow-app/lib/app/router.dart`
- `mine-flow-app/test/core/presentation/widgets/app_interaction_primitives_test.dart`
- `mine-flow-app/lib/l10n/app_{id,en}.arb` and generated localization files

## Next handoff

Run **substep 55.1** in a fresh chat. It must use the shared modal/dismissal contract without duplicating it, and build the contextual report dialog architecture.


---

## Residual fix 2026-09-19 (55.0)

**Scope:** residual item 1 only — wire the three unwired dismiss triggers (`drag`, `browserNavigation`, `parentNavigation`) through the one `AppDismissController` path. No feature migration, router edit, l10n change, or new dependency. Owned files: `lib/core/presentation/widgets/app_interaction_primitives.dart`, `test/core/presentation/widgets/app_interaction_primitives_test.dart` (both were already present in the dirty worktree from a prior session; this pass completed verification and fixed one harness-timing test assertion).

### What is now wired

- **`drag`** — a visible `_DragHandle` on the mobile bottom sheet (`!isWide && !mobileFullPage`, D2). `onVerticalDragEnd` requests dismiss when fling velocity > 300 px/s or cumulative drag > 100dp, routing through `_requestDismiss(AppDismissReason.drag)`. Busy state nulls the gesture callbacks (blocked). Semantic label on the handle.
- **`browserNavigation`** — `PopScope.onPopInvokedWithResult` now branches on `kIsWeb`: web prevented-pop (browser back/forward) → `AppDismissReason.browserNavigation`; native → `AppDismissReason.systemBack`. Same single guarded path.
- **`parentNavigation`** — the sheet state is now `RouteAware`, subscribed to the app's global `routeObserver` (already registered in `lib/app/router.dart:129`, `navigatorObservers: [routeObserver]`). `didPushNext()` requests dismiss when a route is pushed above the open sheet (guard may show the dirty dialog, sheet still mounted). `deactivate()` adds a last-chance observability signal (`onRequestClose(parentNavigation)`) for declarative GoRouter stack replacement that `PopScope` never sees — signal only, not a veto, since the element is already deactivating.

Every wired path keeps the invariant: one guard (`AppDismissController.requestDismiss`), exactly one route pop (one-shot latch `_hasApproved`/`_isDismissing` in `_dismiss()`, STEP-55.11), non-dismissible dirty dialog while dirty, blocked + announced while busy.

### Verification (2026-09-19)

- `flutter test test/core/presentation/widgets/app_interaction_primitives_test.dart` — **23 passed** (was 9 at 55.0 baseline; +14 residual cases: drag clean/dirty/busy + rapid-repeat one-shot, `drag`/`browserNavigation`/`parentNavigation` clean/dirty/busy through the controller, popover adoption contract).
- `dart format --output=none --set-exit-if-changed lib/core/presentation/widgets/app_interaction_primitives.dart test/core/presentation/widgets/app_interaction_primitives_test.dart` — **0 changed**.
- `flutter analyze <the two touched files>` — **No issues found**.
- CR-byte count on both owned files — **0** (LF preserved); `git diff --check` — clean.

**One test assertion fixed this pass:** the clean-drag widget case used `tester.fling(...)`, which leaves residual pointer velocity that tears down the drag-handle element before the deferred (`addPostFrameCallback`) approval callback runs — so `onDismissApproved` saw `mounted=false` and the count stayed 0 (false failure). Root-caused by instrumenting `_dismiss()` (post-frame fired with `mounted=false` on fling, `mounted=true` on the equivalent close-button path). Replaced with `tester.drag(handleFinder, Offset(0, 200))` (past the 100dp cumulative threshold, no residual velocity), which keeps the element mounted across the frame boundary and exercises the real approval path. The gesture-recognizer difference is a harness artifact, **not** a product defect: in production `onDismissApproved` is the host route-pop. Source was not changed for this — only the owned test.

### AppFilterPopover adoption recipe (for 55.2/55.3 — not applied here)

A feature list adopts the shared popover without duplicating dismissal or layout logic: wrap the feature's filter controls (zone selector, chips) as the `child:` of an `AppFilterPopover`, wire its `onApply`/`onReset`/`onCancel` to the feature BLoC/cubit (apply and cancel `Navigator.of(context).pop()` the popover; reset mutates filter state and leaves it open), and open it with `showAppFilterPopover(context: context, builder: (_) => AppFilterPopover(...))` from the list's filter affordance. The popover owns layout, the `Terapkan`/`Reset filter`/`Batal` labelled actions, and the semantic container. Proven by the `popover adoption contract: apply/reset/cancel are reachable` widget test (open → child visible → reset increments in place → apply closes → re-open → cancel closes). Feature list files (`ZoneFilterDropdown` + chips) are **not** edited here; CF/LC adoption is owned by 55.2/55.3.

### Runtime evidence — Unverified

Runtime Web / Android captures remain **Unverified**: the Impeccable binary is absent in this environment and the consolidated visual audit is 55.11's lane. The focused widget + controller tests validate geometry, gesture thresholds, the dismiss contract, and semantics mechanically. No visual evidence invented.

### Handoff — index row 55.0 evidence cell

Do not edit the index here. Proposed replacement evidence-cell text for row 55.0 (residual item 1 resolved; items 2 and 3 remain owned by 55.2/55.3 and 55.11):

> Shared D1–D5 sheet, dirty-dismiss, inspector, filter/calendar, status/state/accessibility primitives and route tests. Residual (audit 2026-09-19): drag/browser/parent-navigation dismiss triggers now wired through the one AppDismissController path (focused 23/23, format/analyze clean, 2026-09-19); AppFilterPopover feature-list adoption still pending (owned by 55.2/55.3 — lists still ZoneFilterDropdown + chips); runtime captures remain Unverified (Impeccable binary absent; deferred to 55.11).

Next: run the **55.1 residual** in a fresh chat.

---

## Residual fix 2 (55.0) — 2026-09-23

**Scope:** RESIDUAL-2 only — localize the `_DragHandle` semantic label. The 2026-09-21 review found the drag-handle label was a hardcoded Indonesian string (`'Seret ke bawah untuk menutup'`) at `app_interaction_primitives.dart:549`, contrary to the PLAN's "new user-facing strings go through localization" rule. It escaped detection because `tool/check_l10n_baseline.dart` does not scan `lib/core/presentation/` — a detection blind spot, not authorization. No feature migration, router edit, guard-scope change, or new package.

### Delivered

- Added `sheetDragHandle` key: `lib/l10n/app_id.arb` (`"Seret ke bawah untuk menutup"`) and `lib/l10n/app_en.arb` (`"Drag down to close"`).
- Regenerated localization output via `flutter gen-l10n` — `String get sheetDragHandle` now present in `app_localizations.dart` (abstract), `app_localizations_id.dart`, `app_localizations_en.dart`.
- Swapped the `_DragHandle` hardcoded label to the file's existing fallback pattern: `Localizations.of<AppLocalizations>(context, AppLocalizations)?.sheetDragHandle ?? 'Seret ke bawah untuk menutup'` — identical in shape to the `sheetBarrierLabel`/`sheetClose` fallbacks in the same file.
- Pinned it: new test case `drag handle semantic label resolves via l10n` asserting `tester.getSemantics(handleFinder).label == 'Seret ke bawah untuk menutup'` under the Indonesian-first host (extended, not rewritten).

### Verification (2026-09-23)

- `flutter test test/core/presentation/widgets/app_interaction_primitives_test.dart` — **24 passed** (was 23; +1 l10n label case).
- `dart format --output=none --set-exit-if-changed` on the two owned `.dart` files + the three regenerated l10n `.dart` files — **0 changed**.
- `flutter analyze` on the two owned files and `lib/l10n/` — **No issues found**.
- `dart run tool/check_l10n_baseline.dart` — **[OK]** (22 non-exempt scanned; note it does not scan `lib/core/` — the proof the string is localized is the ARB key + resolved-label test, not the guard).
- CR-byte audit: owned non-generated `.dart` source files are LF (disk-CR=0, HEAD-CR=0). The two ARB files and three generated l10n `.dart` files are committed-CRLF **by convention** — disk adds exactly one CR per new line vs HEAD (app_id 212→213, app_en 148→149); `git diff --check`'s "trailing whitespace" flags on those files are the CRLF-convention signal, not churn. Diff stat: `7 files changed, 46 insertions(+), 3 deletions(-)`, ARB delta is exactly the two new key lines.

### Lesson recorded

The l10n baseline guard scans only `lib/app/presentation` + `lib/features`; `lib/core/presentation/` is a blind spot where new hardcoded user-facing strings pass mechanically. Widening the guard's scan scope is a separate owner decision (explicitly FORBIDDEN in this lane), so the durable proof of localization here is the ARB key plus the resolved-label test.

### Handoff — index row 55.0 evidence cell (do NOT edit index / flip status here)

Proposed evidence-cell addition for row 55.0:

> Residual-2 (2026-09-23): `_DragHandle` semantic label localized via new `sheetDragHandle` ARB key (id/en) + regenerated l10n; label resolution pinned (focused 24/24, format/analyze/l10n-guard clean). l10n guard's `lib/core/` blind spot recorded as a detection limitation.

Committed as `fix(55.0): localize drag-handle semantic label via sheetDragHandle`. Next: run the **55.1 residual-2** in a fresh chat.
