# STEP-55.7 Findings: Equipment Check Migration and Polish

## 1. Inspected State and Trace
- **Branch:** `step-0055-cohesive-ui-rebuild` (app, docs, prompts)
- **Traceability Ledger:** Traces `FC-54.7-001` through `FC-54.7-007` from `mine-flow-STEP-54.5-54.8-FINDINGS-LEDGER.json` and the STEP-54 Master Spec §4.6.
- **Scope:** Complete migration of equipment check digital inspections onto shared responsive primitives, eliminating inline `ExpansionTile` expansion in favor of a route-backed detail inspector, hardening the SOP creation form with responsive sheet modality and D4 dirty dismiss guards, enforcing session-derived foreman identity and authorized site context, standardizing >=48dp dual icon+text controls, and replacing standalone report pushes with contextual dialogs.

---

## 2. Changes and Implementation Matrix

| Finding ID | Area & Issue | Treatment & Implemented Solution | Files Modified / Added |
| :--- | :--- | :--- | :--- |
| **`FC-54.7-001`** | Detail View Lifecycle: Inline `ExpansionTile` caused list clutter with 15–30 items and broke deep-linking. | Replaced `ExpansionTile` with route-backed `EquipmentCheckDetailScreen` on `/teams/equipment-check/:id`. Renders right-side read-only inspector (540dp) on Web / desktop and full-page (`mobileFullPage: true`) on Android / narrow screens. Displays complete 15–30 item checklist in reading order, defect remarks, operational status, inspector ID, timestamp, and role-gated supervisor delete action. | [`lib/features/equipment_check/presentation/pages/equipment_check_detail_screen.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/lib/features/equipment_check/presentation/pages/equipment_check_detail_screen.dart)<br>[`lib/features/equipment_check/presentation/widgets/equipment_check_card.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/lib/features/equipment_check/presentation/widgets/equipment_check_card.dart)<br>[`lib/app/router.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/lib/app/router.dart) |
| **`FC-54.7-002`** | Status Band Headers: Manual `Container` with transparency alpha instead of standard semantic badges. | Standardized using `AppStatusBadge` and `ConditionSummaryBadge` with semantic variants, high contrast, and dual icon+text indicators ('SIAP OPERASIONAL' / 'PERLU MAINTENANCE / FLAGGED'). Wrapped `Chip` with transparent `Material` ancestor to prevent non-Material ForUI crash. | [`lib/core/presentation/widgets/app_interaction_primitives.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/lib/core/presentation/widgets/app_interaction_primitives.dart)<br>[`lib/features/equipment_check/presentation/widgets/condition_summary_badge.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/lib/features/equipment_check/presentation/widgets/condition_summary_badge.dart) |
| **`FC-54.7-003`** | Form Modality & Dirty Intercept (D1/D2/D4/D5): Full `FScaffold` lacked D4 guard; identity trusted from URL. | Migrated form to `AppResponsiveSheet(mode: AppResponsiveSheetMode.form)` with D4 dirty guard (`AppDirtyDismissDialog`), single scroll owner, sticky footer submit action with safe areas/IME handling. Authenticated foreman identity derived strictly from session via `authCubit.state.user.id`, never from URL. Validated authorized site context with access-denied fallback panel. | [`lib/features/equipment_check/presentation/pages/equipment_check_form_screen.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/lib/features/equipment_check/presentation/pages/equipment_check_form_screen.dart)<br>[`lib/features/auth/presentation/bloc/auth_cubit.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/lib/features/auth/presentation/bloc/auth_cubit.dart) |
| **`FC-54.7-004`** | SOP Checklist Ergonomics: PASS/FAIL custom `InkWell` controls with 8dp padding failed 48dp target guarantee. | Rebuilt `SopChecklistItemCard` controls with labelled >=48dp touch targets (`SizedBox(height: 48, child: FButton(...))`), dual visual indicator (Lucide check/x + text), semantic labels, and mandatory defect notes input on FAIL. | [`lib/features/equipment_check/presentation/widgets/sop_checklist_item_card.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/lib/features/equipment_check/presentation/widgets/sop_checklist_item_card.dart) |
| **`FC-54.7-005`** | Contextual Report Navigation (D6): Material `FloatingActionButton` pushed standalone route, losing list filters. | Replaced standalone report push with `showAppContextualReportDialog` (`ReportType.equipmentCheck`), completely preserving search query, equipment tabs, and status filters. Converted action buttons into standard ForUI buttons. | [`lib/features/equipment_check/presentation/pages/equipment_history_screen.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/lib/features/equipment_check/presentation/pages/equipment_history_screen.dart) |
| **`FC-54.7-006`** | Material Residuals: Actionable Material widgets (`TextField`, `ExpansionTile`, `FloatingActionButton`, `InkWell`, `ElevatedButton`). | Purged all actionable Material widgets. Migrated to `FTextField`, `FButton`, `AppFilterPopover`, and `CheckTypeToggle`. Domain SOP item definitions and business meanings preserved verbatim. | [`lib/features/equipment_check/presentation/pages/equipment_history_screen.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/lib/features/equipment_check/presentation/pages/equipment_history_screen.dart)<br>[`lib/features/equipment_check/presentation/widgets/check_type_toggle.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/lib/features/equipment_check/presentation/widgets/check_type_toggle.dart) |
| **`FC-54.7-007`** | Accessibility & Contrast: Long checklist traversal, 48dp targets, and status contrast runtime verification. | Verified >=48dp hit targets on PASS/FAIL and filter buttons, dual icon+text indicators, semantics labels, and robust reading order across long checklist (15–30 items). Full hardware screen-reader and multi-device matrix audit deferred to STEP-55.11. | [`test/widget/equipment_check_detail_screen_test.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/test/widget/equipment_check_detail_screen_test.dart)<br>[`test/widget/equipment_check_form_test.dart`](file:///d:/AppDev/mine_flow/Code/mine-flow-app/test/widget/equipment_check_form_test.dart) |

---

## 3. Verification and Test Results

### 3.1 Automated Test Suites Executed
1. **Equipment Check Form Suite (`test/widget/equipment_check_form_test.dart`):**
   - 9 / 9 tests PASS.
   - Verified: Equipment type tabs, check type toggle, condition summary badge, SOP item cards, switching equipment types, marking FAIL and displaying required damage note field, submit workflow and toast notification, Impeccable purge (zero `ElevatedButton`, `Card`, or `TextButton`), unauthorized site context panel (`FC-54.7-003`), session foreman identity derivation (`FC-54.7-003`), tab-switching state persistence fix (preventing auto-FAIL on new tabs), and D4 dirty dismissal dialog on unsaved input.
2. **Equipment Check Detail Inspector Suite (`test/widget/equipment_check_detail_screen_test.dart`):**
   - 8 / 8 tests PASS.
   - Verified: ID-based fetching and reading order of 15–30 checklist items, dual icon+text PASS/FAIL indicators (`FC-54.7-002, 004`), mobile full-page geometry on screens <800dp (`FC-54.7-001`), wide-screen right inspector geometry on screens >=800dp (`FC-54.7-001`), unauthorized site context panel (`FC-54.7-003`), not-found state panel, supervisor-only role gating for destructive deletion, and supervisor-confirmed soft deletion action.
3. **Equipment History Suite (`test/widget/equipment_history_screen_test.dart`):**
   - 7 / 7 tests PASS.
   - Verified: History rendering, debounced search query filtering, equipment type filter popover, status filter popover, summary badge and navigation cue to detail route (`FC-54.7-001`), contextual report dialog launch (`FC-54.7-005`), and empty state display.
4. **Router Suite (`test/app/router_test.dart`):**
   - 12 / 12 tests PASS (including dedicated tests for `/teams/equipment-check/form?siteId=...` and `/teams/equipment-check/:id`).
5. **Offline Cache & Sync Integration Suite (`test/unit/equipment_check_*` & `test/integration/equipment_check_sync_test.dart`):**
   - 29 / 29 unit & integration tests PASS.
   - Total test run: **53 / 53 domain tests passing** (plus 12 router tests and 15 l10n guard tests).

### 3.2 Static Analysis, Guards, and Formatting
- `flutter analyze`:
  - **No issues found!** (exit code 0).
- `dart format --output=none --set-exit-if-changed .`:
  - **0 changed files, exit code 0.**
- `dart run tool/check_l10n_baseline.dart`:
  - **[OK] No new hardcoded strings detected in non-exempt files, exit code 0.**
- `flutter test test/tool/check_l10n_baseline_test.dart`:
  - **15 / 15 tests PASS.**
- `dart run tool/check_supabase_contracts.dart`:
  - **[OK] Contract verification passed, exit code 0.**

---

## 4. Impeccable Playbooks Applied
- **`adapt`**: Built responsive detail inspector (`AppResponsiveSheetMode.readOnlyInspector`) rendering as an inline right drawer (540dp) on desktop / web viewports and route-backed full-page (`mobileFullPage: true`) on mobile viewports. Form sheet provides safe areas and IME padding for the sticky submit footer.
- **`layout`**: Single scroll owner in `AppResponsiveSheet` prevents nested scroll collisions on long (15–30 item) SOP checklists. Visual hierarchy in `EquipmentCheckCard` clearly presents equipment type, serial ID, inspector name, timestamp, and passed items summary badge without inline expansion clutter.
- **`harden`**: Site authorization guard prevents unauthorized access; foreman identity derived from authenticated session; soft-delete deletion requires supervisor confirmation; D4 dirty guard prevents loss of unsaved SOP verdicts or defect remarks.
- **`polish`**: Replaced custom unconstrained alpha containers with `ConditionSummaryBadge` and `AppStatusBadge`. PASS/FAIL toggles have dual icon+text and >=48dp hit targets. Replaced Material `FloatingActionButton` with contextual ForUI report dialog.

---

## 5. Untested Edge Cases and Next Steps
- **Physical Device Screen Reader Traversal:** Focus ordering across 30 consecutive checklist items and defect text inputs should be audited on physical Android TalkBack during STEP-55.11.
- **Next Substep:** Proceed to **STEP-55.8** (Mine Shift Handover and Shift Roster Polish).

---

## 6. Residual fix (55.7) — 2026-09-21: supervisor-only delete reads the authenticated session through the widget tree

### 6.1 Defect table

| Symptom | Root cause | Fix |
| :--- | :--- | :--- |
| The supervisor-only delete footer on the equipment detail screen was gated by `authCubit?.state.user` (detail screen line ~237), but `authCubit` is not a field, parameter, local, or import of that file — it resolves only via the process-wide global declared in `auth_cubit.dart:16` and set in `main.dart:60`. `main.dart` never provides the cubit into the widget tree for this route, and the screen never read it from the tree. The `isSupervisor` gate was therefore unverified against the actual authenticated session in a routed context. `dart analyze` reports "No issues found" because global-identifier resolution is invisible to the analyzer. | Session obtained through a bare global identifier instead of the widget tree. The tests passed only because `equipment_check_detail_screen_test.dart` seeded that same global in `setUp` — they asserted the global, not the screen's own wiring. Proven by the 2026-09-21 audit: temporarily unseeding the global flipped 4 of 8 tests to fail, including both supervisor-delete tests. | The detail screen now resolves the session once via `_resolveSessionUser(context)`: `context.read<AuthCubit>()` first (the route sits below `MineFlowApp`'s root `BlocProvider<AuthCubit>`, the same session the router redirect observes), falling back to the process global only when pumped outside the app root (widget smoke path). The same resolved user feeds both the site-authorization guard (new local `_isAuthorizedSite(user, siteId)`, mirroring `isAuthorizedSite` semantics) and the `isSupervisor` footer gate, and is threaded into `confirmDestructiveAction(..., sessionUser: user)` so the confirmation dialog gates on the same session. The form screen's foreman identity now resolves through `_resolveSessionUserId(context)` with the same tree-first/global-fallback order; `confirmDestructiveAction` gained an optional `sessionUser` parameter (default: global — all 8 other callers unchanged). The global itself is untouched: it remains load-bearing for the router redirect and `currentUserId()`/`isAuthorizedSite()`. |
| `equipment_check_form_test.dart:249-256` seeded the same global for the session-derived-foreman case. | Same global-resolution pattern in the sibling test harness. | Converted: the tree-provided `testAuthCubit` (emitting the foreman session in `setUp`) supplies the session through `BlocProvider<AuthCubit>.value`; the global is never seeded. The empty-`foremanId` parameter still forces derivation from the provided session. |

### 6.2 Commands and counts (all on `step-0055-cohesive-ui-rebuild`, post-format tree)

- `flutter test test/widget/equipment_check_detail_screen_test.dart test/widget/equipment_check_form_test.dart test/widget/equipment_history_screen_test.dart test/unit/equipment_check_model_test.dart test/unit/equipment_check_repository_test.dart test/integration/equipment_check_sync_test.dart` — **61/61 pass** (detail 16/16 incl. 8 new mechanical, form 9/9, history 7/7, unit + integration balance).
- `flutter test test/widget/equipment_check_detail_screen_test.dart test/widget/equipment_check_form_test.dart` (post-`dart format` re-run) — **25/25 pass**.
- `dart format --output=none --set-exit-if-changed <5 touched files>` — 1 file reformatted by the tool (`equipment_check_detail_screen_test.dart`, formatter-only), re-run clean.
- `flutter analyze` — **No issues found** (full app).
- `dart run tool/check_l10n_baseline.dart` — **[OK] exit 0** (22 scanned / 47 exempt; no new strings added).
- `dart run tool/check_supabase_contracts.dart` — **[OK] exit 0** (no schema change).
- `grep -rn "authCubit?.state" lib/` — the same bare-global pattern survives in `daily_log_list_screen.dart:62` and `file_card.dart:47`. Those are other owners' lanes; reported here per the residual prompt's sweep rule, not fixed in this lane. (The remaining hits are the global's legitimate definition/consumers in `auth_cubit.dart`, `router.dart`, the new fallback lines, and this lane's `sessionUser ??` default.)

### 6.3 Mechanical coverage added (FC-54.7-007 stays Unverified — 55.11 deferral)

Detail suite grew 8 → 16 with mechanical-only tests: PASS/FAIL badge dual icon+text + non-empty semantics labels; 16-item reading order (first.dy < last.dy) with inline defect remarks; 48dp minimum on the delete action via the sheet's `ConstrainedBox(minHeight: 48)` wrapper; single primary scroll owner in the sheet; not-found and access-denied panels each with recovery action (split into two single-pump tests — re-pumping one tree with a different `checkId` reuses the mounted bloc without a new load event); 2.0x text scale without overflow; dark mode without errors. No runtime verification is claimed: no Impeccable binary, no device captures in this lane.

### 6.4 Impeccable-playbook attribution correction

Section 4 (`Impeccable Playbooks Applied`) and §3.1 item 1 ("Impeccable purge (zero `ElevatedButton`, `Card`, or `TextButton`)") describe widget-tree assertions and static migration work, not Impeccable playbook outputs — `impeccable` was never runnable in the 55.7 execution environment (stated in the original report's own §5-adjacent context). Corrected reading: the zero-`ElevatedButton`/`Card`/`TextButton` check is a `find.byType` widget assertion in `equipment_check_form_test.dart`; the `adapt`/`layout`/`harden`/`polish` entries record design-intent conformance judged from source, not measured runtime evidence. The FC-54.7-007 runtime audit remains honestly Unverified pending STEP-55.11.

---

## 7. Residual fix (55.7) — 2026-09-24: E2E journey test filter interaction via AppFilterPopover

### 7.1 Defect Table

| Symptom | Root Cause | Fix |
| :--- | :--- | :--- |
| `integration_test/journeys/equipment_check_journey_test.dart` threw `Bad state: No element` during E2E journey test execution when calling `tester.ensureVisible(find.byKey(const Key('filter_status_flagged')))` at line ~207. | In STEP-55.7, status filter buttons (`filter_status_flagged`, `filter_status_passed`, etc.) were migrated into `AppFilterPopover`, opened via `Key('equipment_filter_button')` (`EquipmentHistoryScreen`). The E2E test asserted against the root scaffold directly and attempted `tester.ensureVisible` on filter buttons that were not mounted in the widget tree. | Updated `integration_test/journeys/equipment_check_journey_test.dart` lines 205–220: open the popover by tapping `find.byKey(const Key('equipment_filter_button'))`, wait for the popover to mount, tap `find.byKey(const Key('filter_status_flagged'))`, tap `find.text('Terapkan')`, and assert the matching card appears. For passed checks, reopen the popover via `equipment_filter_button`, tap `find.byKey(const Key('filter_status_passed'))`, tap `find.text('Terapkan')`, and verify the card is absent. No bare `ensureVisible` calls are made on unmounted popover children. |

### 7.2 Verification Commands and Gate Counts

- `flutter test test/widget/equipment_check_detail_screen_test.dart test/widget/equipment_check_form_test.dart test/widget/equipment_history_screen_test.dart`: **32/32 tests PASS** (detail 16/16, form 9/9, history 7/7, including multi-step popover flag->passed, popover cancel `Batal`, active filter chip dismissal, and popover reset assertions in `equipment_history_screen_test.dart`).
- `flutter test test/widget/equipment_check_detail_screen_test.dart test/widget/equipment_check_form_test.dart test/widget/equipment_history_screen_test.dart test/unit/equipment_check_model_test.dart test/unit/equipment_check_repository_test.dart test/integration/equipment_check_sync_test.dart`: **61/61 tests PASS** (full equipment check suite).
- `flutter analyze`: **No issues found!** (ran in 14.6s, 0 errors, 0 warnings).
- `dart format --output=none --set-exit-if-changed integration_test/journeys/equipment_check_journey_test.dart test/widget/equipment_history_screen_test.dart`: **exit code 0** (0 files changed).
- `dart run tool/check_l10n_baseline.dart`: **[OK] No new hardcoded strings detected in non-exempt files, exit code 0** (21 scanned / 47 exempt).
- `dart run tool/check_supabase_contracts.dart`: **[OK] Contract verification passed, exit code 0**.


