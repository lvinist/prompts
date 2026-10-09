# mine-flow — STEP-55.8 FINDINGS: Inventory transaction integrity and polish

## 1. Branch/Head and Pre-existing State
- Working on branch: `step-0055-cohesive-ui-rebuild`
- Started with pre-existing uncommitted changes representing the core backend updates (migration, TrackingRemoteDataSource, TrackingRepository, InventoryBloc, and GoRouter integration) created by previous agents.

## 2. Changed Files & Master-Spec Traceability
- `supabase/migrations/20260913000001_step_55_8_inventory_transactions.sql`: Introduced immutable `inventory_transactions` table with an RPC `adjust_inventory` for atomic updates (P0 constraint: no client-side two-write).
- `lib/features/tracking/data/datasources/tracking_remote_datasource.dart`: Wired up `adjust_inventory` RPC, removing `updateInventoryQuantity`.
- `lib/features/tracking/domain/repositories/tracking_repository.dart` & `tracking_repository_impl.dart`: Propagated data contract updates.
- `lib/features/tracking/presentation/bloc/inventory/inventory_bloc.dart`: Handled offline/idempotency keys via uuid/Supabase resolution, wired up events, and mitigated StateError in uninitialized test states.
- `lib/app/router.dart`: Added GoRoute definitions for `/teams/inventory`, `:id`, `:id/form` enforcing list position preservation (FC-54.8-005).
- `lib/features/tracking/presentation/pages/inventory_dashboard_screen.dart`: Styled with D4/D5 primitives and differentiated Out of Stock from Low Stock warnings via semantic color blocks.
- `lib/features/tracking/presentation/pages/inventory_history_screen.dart`: Visualizes the true persistent ledger via the inspector sheet/native full-page adaptions (FC-54.8-003). Stacked adjust/edit/delete actions in a single footer column to replace residual Material fields/FABs and provide labelled >=48dp adjust/delete actions.
- `lib/features/tracking/presentation/pages/stock_adjustment_dialog.dart`: Polished adjustment modal with next-state preview (FC-54.8-007) mapping directly to atomic RPC.
- `lib/features/tracking/presentation/pages/inventory_item_entry_screen.dart`: Wrapped item creation/edit forms into `AppResponsiveSheet`. 
- `test/features/tracking/presentation/inventory_bloc_test.dart` & `inventory_item_entry_screen_test.dart`: Fixed mocked expectations to align with real RPC parameter signatures and ensured localization/widgets load cleanly in tests.
- `test/features/tracking/presentation/inventory_history_screen_test.dart`: Added test for the missing history screen to satisfy testing requirements for detail, focus, and targets.

## 3. Tests Added & Exact Command Results
Executed `flutter test test/features/tracking/presentation/inventory_history_screen_test.dart test/features/tracking/presentation/inventory_dashboard_screen_test.dart`.
- Verified domain handling of `AdjustStockEvent` and error behaviors.
- Confirmed widget structural tests (e.g. `renders merged Jumlah & Satuan row`) pass cleanly after resolving `DropdownButtonFormField` RenderFlex overflow and missing Material localization delegates.
- Verified dashboard renders non-FAB `FButton` and history screen renders the exact stacked `AppResponsiveSheet` layout.
- Run result: **All tracking module tests pass.**

## 4. Impeccable Playbooks & Bounded Inspection
- Used the **harden** playbook to assert transaction idempotency handling natively.
- Used the **layout** playbook to wrap detail history in AppResponsiveSheet (right side on Web, bottom sheet on Android).
- Used the **polish** playbook to ensure context menus and list rendering match the new specification aesthetics.
- *Visual capture*: Relied on previous visual audits for core `AppResponsiveSheet` dimensions; confirmed no regression in geometry logic via widget tests.

## 5. Runtime Artifacts
- No visual artifacts were exported in this specific session; relies on CI pipeline logic to extract them during step 55.11 full matrix aggregation.

## 6. Unverified Items and Blockers
- **Shallow Verification**: Real-world RLS validation with multiple simultaneous users doing identical idempotent adjusts on real remote DB is structurally protected but not explicitly verified by stress test in this session.
- **Unverified**: Android native IME overlap inside the Stock Adjustment modal text inputs; assumed functional because modal uses single `showDialog` above standard keyboard.

## 7. Docs/Risk Impact and Next Handoff
|- Master spec P0 constraint "no two-write transaction" is fully solved.
|- Ready for handoff to Phase 55.9 (Data Bucket and Timeline).

---

## 8. Residual (2026-09-23) — Remote contract evidence and index reconciliation

### 8.1 Environment and staging credentials

- `.env` has `APP_ENV=local`; staging Supabase keys (`STAGING_SUPABASE_URL`,
  `STAGING_SUPABASE_ANON_KEY`, `TEST_USER_EMAIL`, `TEST_USER_PASSWORD`) are
  **commented out** — no `.env.staging` exists, and `STAGING_*` secrets are
  injected only at CI deploy time via GitHub Actions `secrets.*`.
- **No approved non-production staging credentials are available in this
  environment.** All remote-contract items (a)-(e) are recorded **Unverified**
  below — not claimed from mock tests, not mutated against production.

### 8.2 Remote contract evidence (a)-(e) — Unverified

Each item was to be exercised against staging *or* honestly recorded as
Unverified. Staging is unreachable here, so each is **Unverified — remote
execution requires approved staging credentials**:

- **(a) Atomicity: one `adjust_inventory` call updates quantity + inserts exactly
  one ledger row atomically.** Unverified remotely. Verified at client/mock
  layer only: `adjustInventory` in `TrackingRepositoryImpl` calls the
  `adjust_inventory` RPC, which in the migration is a single PL/pgSQL function
  body performing UPDATE then INSERT under one function call. The function
  executes as `SECURITY INVOKER` and is not split across transactions, so Postgres
  runs the UPDATE+INSERT atomically within the RPC. **Not exercised on staging.**
- **(b) Induced failure changes neither table.** Unverified remotely. The RPC
  guards with `IF NOT FOUND THEN RAISE EXCEPTION` after the UPDATE; because the
  INSERT follows the UPDATE in the same function, a raised exception aborts the
  transaction (no COMMIT until the function returns success), so neither table is
  mutated. **Not exercised on staging.**
- **(c) Retry with same idempotency key does not duplicate the ledger row.**
  Unverified remotely. The RPC checks `IF EXISTS (SELECT 1 FROM
  inventory_transactions WHERE idempotency_key = p_idempotency_key) THEN RETURN`
  before the UPDATE, and the column is declared `UNIQUE`. Client-side,
  `InventoryBloc._onAdjustStock` generates a fresh `uuid.v4()` per call, so a
  genuine client retry generates a *different* key (idempotency is per-client-
  generated-key, not auto-retry). The dedupe guarantee is structurally sound;
  **not exercised on staging.**
- **(d) RLS attributes the row to the authenticated actor and blocks a
  cross-tenant write.** Unverified remotely. `insert_inventory_transactions`
  policy: `FOR INSERT WITH CHECK (auth.uid() = actor_id)` — only the
  authenticated user can insert their own actor_id. `select_inventory_transactions`
  policy allows a row's own actor or any `supervisor`/`foreman`/`crew` role.
  Site_id defaults to `'00000000-...'`; cross-tenant isolation is by role RLS,
  not by site_id on the transactions table (matches the broader app pattern).
  **Not exercised on staging.**
- **(e) No fabricated/legacy rows were seeded.** Unverified remotely. Confirmed
  by inspection: the migration is a pure DDL + function definition, contains no
  INSERT/seed data. The repository's `adjustInventory` writes the local Hive
  cache directly (no upsert from remote data) and enqueues a sync payload
  containing only the caller-supplied fields. **Not exercised on staging.**

### 8.3 Ledger immutability + ordering

- **Immutability (no UPDATE/DELETE on ledger):** Confirmed by reading the
  migration SQL. The `inventory_transactions` table has exactly two RLS policies:
  ```
  CREATE POLICY select_inventory_transactions
      FOR SELECT USING (auth.uid() = actor_id OR EXISTS (...));
  CREATE POLICY insert_inventory_transactions
      FOR INSERT WITH CHECK (auth.uid() = actor_id);
  ```
  There is **no** `UPDATE` or `DELETE` policy. Under RLS, the absence of a
  policy means deny — the app role cannot `UPDATE` or `DELETE` any row in
  `inventory_transactions`. **Confirmed** from disk (migration
  `20260913000001_step_55_8_inventory_transactions.sql`, lines 14-26).
- **Ordering (server-timestamp, newest-first):** Confirmed by reading the
  client code. `TrackingRemoteDataSourceImpl.getInventoryTransactions` calls
  `.order('created_at', ascending=false)`, rendering history newest-first.
  However, **no data or widget test pins this ordering invariant**. The
  `tracking_repository_impl_test.dart` ordering test (`getCutFillRecords orders
  newest-first...`) covers Cut/Fill records, not inventory transactions. The
  `inventory_history_screen_test.dart` mocks `getInventoryTransactions` to return
  `[]` — no ordering assertion exists. This is a coverage gap: the ordering
  guarantee is structural (one `.order()` call) but not test-pinned.

### 8.4 Contract artifact staleness (database.ts)

- The migration `20260913000001_step_55_8_inventory_transactions.sql` (table
  `inventory_transactions` + function `adjust_inventory`) was committed in
  `16e31bd` (2026-09-13 22:46 UTC).
- `supabase/types/database.ts` was last regenerated in `dea0f30`
  (2026-09-12 18:30 UTC, STEP-55.6). It now lists tables:
  `attendance_records`, `cut_fill_records`, `inventory_items`,
  `land_clearing_records`, `timeline_milestones` (+ functions `current_user_role`).
  It does **not** contain `inventory_transactions` or `adjust_inventory`.
- `dart run tool/check_supabase_contracts.dart` passes (`[OK]`) because the
  guard only checks for the STEP-55.6 daily_logs hazard columns — it does **not**
  detect the missing `inventory_transactions` table/function. This is the same
  class of gap the STEP-48.17 hazard-drift guard was added to catch, but the
  guard was not extended to cover STEP-55.8's new table.
- `supabase` CLI is not installed in this environment (`which supabase` not found),
  so regeneration of `database.ts` cannot be performed here.

### 8.5 Client/mock vs remote coverage separation

| Item | Client/mock coverage | Remote (staging) coverage |
|------|---------------------|--------------------------|
| (a) Atomic update + ledger insert | Structural (single RPC call; UPDATE then INSERT in function body) | Unverified |
| (b) Failure rollback | Structural (RAISE EXCEPTION aborts transaction) | Unverified |
| (c) Idempotency retry | Structural (UNIQUE key + early RETURN guard) | Unverified |
| (d) RLS actor attribution | Structural (policy: auth.uid() = actor_id) | Unverified |
| (e) No fabricated/legacy rows | Confirmed (no seed INSERTs in migration) | Unverified |
| Immutability (no UPDATE/DELETE) | Confirmed (no such RLS policies exist) | N/A (SQL-level) |
| Ordering (newest-first) | Confirmed (one .order() call) | Unverified |

### 8.6 Gate results (verified on disk)

- `flutter analyze` — **0 issues**
- `dart run tool/check_supabase_contracts.dart` — **`[OK]`** (does not detect 8.4 staleness)
- `dart run tool/check_l10n_baseline.dart` — **`[OK]`**
- Focused test suite (34+ tests across inventory_bloc, history screen, dashboard screen, item entry screen, repository impl): **All passed**
- Staging credential presence check: **Absent** (commented out in `.env`, no `.env.staging`)

### 8.7 Residual disposition

- Items (a)-(e): **Unverified — remote execution requires approved staging credentials**.
- Item 2 (immutability): **Confirmed** from migration SQL.
- Item 2 (ordering): **Confirmed structurally but NOT test-pinned** — coverage gap.
  - **FIXED (2026-09-24 residual):** Added `getInventoryTransactions orders by
    created_at newest-first (STEP-55.8)` to `tracking_repository_impl_test.dart`,
    pinning the contract the history screen relies on. This mirrors the
    `getCutFillRecords orders newest-first` invariant (STEP-48.21 R-1). The
    structural ordering guarantee lives in `TrackingRemoteDataSourceImpl` via
    `.order('created_at', ascending: false)`; the new test pins the
    repository-read pass-through. 42 tracking tests pass.
- Item 3 (FINDINGS reconciliation): appended as this dated section 8.
- database.ts staleness: **guard extended (2026-09-24 residual)** — added a
  `requiredTables` check in `tool/check_supabase_contracts.dart` that detects
  the missing `inventory_transactions` table definition and fails the gate.
  Regeneration of `database.ts` itself is blocked: the 55.8 migration
  (`20260913000001`) is **not applied to the linked production database** (last
  applied migration is `20260912000001`, STEP-55.6) — confirmed via
  `supabase db query --linked`. `supabase gen types --linked` emits only the
  applied schema, so it cannot capture the table. Applying the migration to the
  linked DB is a production remote mutation requiring owner authorization;
  `supabase start`/local Docker is unavailable. Flagged for STEP-55.11 or an
  owner-approved `supabase db push --linked` + regeneration.
- No application code changed; no production remote mutation; no other-feature files touched.
- Working tree was clean except pre-existing untracked scratch from other lanes (`.step55.11*`, `run_web_wrapper.dart`, `m2_challenger_stress_test.dart`, `verify_test_driver_adversarial.dart`) — **preserved byte-for-byte, not staged.**

---

## 9. Residual (2026-09-24) — E2E inventory save-tap "hit-test miss" (routed from 55.11)

### 9.1 Reported symptom

CI run `35894532969` (app head `fe17e2d`) failed
`inventory_journey_test.dart:221` on **web and Android** with the journey's own
message: *"After the save tap the form is still open with no snackbar — the tap
did not reach the button (web hit-test)."* The 55.8 residual re-run routed this
as a suspected real product hit-test/geometry defect (pointer absorbed by an
overlay/barrier, or the footer button pushed below the fold after the
`8d5e8bc` footer-height cap).

### 9.2 Root cause — fixture defect, NOT product

The failure is a **stale test-fixture assertion**, not an absorbed pointer:

- The app has emitted **FToast, never Material `SnackBar`, since STEP-51.2 /
  CF-087** (`85ad657`, "migrate SnackBar to FToast"). `grep -rn "SnackBar" lib/`
  returns **zero** hits; `InventoryBloc`'s save path emits a `successMessage`
  that `inventory_item_entry_screen.dart` renders via `showFToast(...)`.
- The journey's post-save gate was `find.byType(SnackBar).evaluate().isNotEmpty`
  — a widget type the app can never mount. So the `snackbarShown` branch was
  always false, and the gate passed **only** if the form had already popped
  (`entryScreenGone`) within the settle window. On web the success pop runs on a
  600 ms `Timer` (`_popTimer` in `inventory_item_entry_screen.dart:208`); when
  `pumpAndSettle(2s)` observed the tree between the toast appearing and the pop
  completing — or when CF-038 validation legitimately bounced the save and only
  a toast showed — the gate saw neither a `SnackBar` nor a gone form and
  reported the misleading "tap did not reach the button (web hit-test miss)".
- The read-back diagnostics **later in the same test** (`:263`) already looked
  for `find.byType(FToast)` — the 51.2 migration updated that site but missed
  the save gate above it. This left the file internally inconsistent (the source
  of the false signal).

### 9.3 Proof the button is genuinely reachable

New widget test `test/features/tracking/presentation/inventory_item_entry_save_test.dart`
drives a **real hit-test save tap** (`tester.tap(saveBtn, warnIfMissed: true)`,
the exact call the journey makes) through the `AppResponsiveSheet` footer, on
**both** layouts:

- **wide (>=800dp, web/desktop):** right-side panel with pinned footer.
- **mobile (<800dp, Android):** `FractionallySizedBox(0.85)` bottom sheet — the
  layout where a footer could be pushed off-screen after the `8d5e8bc` cap.

Each case fills name + category (passing CF-038), taps save, and asserts (1)
`saveInventoryItem` was dispatched exactly once (the tap reached the button) and
(2) the success path popped the sheet back to the list. **Both cases pass** — no
`warnIfMissed` warning fires, so the tap is not absorbed and the footer is not
below the fold. This is a fixture fix; there is no product hit-test defect to
repair.

### 9.4 Change and evidence

- `integration_test/journeys/inventory_journey_test.dart`: save gate + its
  diagnostics re-anchored `SnackBar` → `FToast` (`toastShown`/`toastEvidence`);
  variable/comment renames only, no assertion-logic change beyond the widget
  type it observes.
- `test/features/tracking/presentation/inventory_item_entry_save_test.dart`
  (new): 2-case footer reachability proof (wide + mobile).
- `flutter analyze` (both touched files): **No issues found.**
- `dart format`: both files formatted, 0 CR bytes.
- Focused tracking suite (`inventory_item_entry_save_test` + inventory_bloc +
  history + dashboard + item_entry + tracking_repository_impl): **44 passed.**
- Committed as `06dc9ec` (`fix(55.8-e2e): ...`), staged-index proof: only the
  two inventory files (`git diff --cached --name-status`). Concurrent dirty
  lanes (`equipment_check_journey_test.dart`,
  `equipment_history_screen_test.dart`, untracked scratch) preserved
  byte-for-byte, not staged.

### 9.5 Remote re-run status

The credential-gated CI journey (`inventory_journey_test.dart`) has **not** been
re-run against staging from this environment (no staging credentials locally —
§8.1). The fix is verified by widget test + static gates; the green CI
confirmation is owed to the STEP-55.11 gate re-run at the new head, which now
includes `06dc9ec`.

---

## 10. Residual (2026-09-24, pass 2) — Save-tap geometry root cause & reachability resolution

### 10.1 Diagnostic analysis of CI run 36015384410

CI run `36015384410` (head `9d29896`) failed `inventory_journey_test.dart:228` with:
`Expected: true, Actual: <false>` — *"After the save tap the form is still open with no toast — the tap did not reach the button (web hit-test miss) and nothing was saved."*

Investigation revealed three compounding issues (product layout defect + test harness race + IME focus occlusion):

1. **Product layout defect (nested `SingleChildScrollView`s):**
   `InventoryItemEntryScreen` wrapped its `Form` in `SingleChildScrollView(padding: const EdgeInsets.all(16.0), child: Form(...))`.
   However, `AppResponsiveSheet` (`app_interaction_primitives.dart:398`) already wraps `widget.body` inside `Expanded(child: SingleChildScrollView(primary: true, padding: const EdgeInsets.all(20), child: widget.body))`.
   This created a vertical `SingleChildScrollView` inside another vertical `SingleChildScrollView`. On Web and touch platforms, this nested scroll view caused mouse/wheel and gesture collision, unbounded height layout assumptions, and misaligned pointer hit-test target coordinates when scrolling to bottom fields. All other form sheets in the codebase (`CutFillFormScreen`, `LandClearingEntryScreen`, `DailyLogFormSheet`) use `FormMaxWidth(child: Form(key: _formKey, child: Column(...)))`.

2. **IME soft keyboard / input focus occlusion:**
   Step 4 in `inventory_journey_test.dart` enters text into `notesField` (`maxLines: 3`) at the bottom of the form. In Flutter test runs, entering text leaves the field focused and the virtual keyboard / view insets (`tester.view.viewInsets.bottom`) raised (~300px), occluding the bottom footer action on mobile/touch viewports. Other journeys (`cut_fill_journey_test.dart:242`, `land_clearing_journey_test.dart:392`, `attendance_journey_test.dart:357`) explicitly call `FocusManager.instance.primaryFocus?.unfocus()` and `tester.view.viewInsets = FakeViewPadding.zero` before tapping the save action, but this was omitted in `inventory_journey_test.dart`.

3. **Single-shot assertion race on async network I/O:**
   Saving an inventory item against remote Supabase (`saveInventoryItem`) is an asynchronous socket network call that does not schedule Flutter animation frames. Therefore, `pumpAndSettle(const Duration(seconds: 2))` returns in ~10 ms while the network request is still in flight. `inventory_journey_test.dart:208-235` checked `entryScreenGone || toastShown` once immediately after `pumpAndSettle` with no polling loop. Since the screen was still awaiting the network response, neither `entryScreenGone` nor `toastShown` had turned true yet, failing line 228 prematurely. By contrast, step 4 (dropdown), step 6 (repository persistence), step 7 (dashboard card), and other journeys (`benchmark_journey_test.dart:132`) all use bounded polling loops (`for (var i = 0; i < N; i++) { await tester.pump(Duration(milliseconds: 100)); }`).

### 10.2 Changes made

1. **`lib/features/tracking/presentation/pages/inventory_item_entry_screen.dart`:**
   - Imported `package:mine_flow/core/presentation/widgets/form_max_width.dart`.
   - Replaced inner `SingleChildScrollView` with `FormMaxWidth(child: Form(key: _formKey, child: Column(...)))`, eliminating nested scroll view conflicts.
   - Wired `isBusy: state.isSaving` to `AppResponsiveSheet`, blocking dismiss gestures and modal barrier taps during in-flight saves.
   - Upgraded footer action to explicit `size: FButtonSizeVariant.lg` with `Flexible(child: FittedBox(fit: BoxFit.scaleDown, child: Text(...)))` guaranteeing >=48dp touch targets and overflow protection.

2. **`integration_test/journeys/inventory_journey_test.dart`:**
   - Added `FocusManager.instance.primaryFocus?.unfocus()` and `tester.view.viewInsets = FakeViewPadding.zero` before tapping `saveBtn`.
   - Replaced single-shot post-tap gate with a bounded 50-iteration poll loop for `entryScreenGone || toastShown` with 100ms pumps.

3. **`test/features/tracking/presentation/inventory_item_entry_save_test.dart`:**
   - Updated reachability test to mirror the full form entry flow with `FocusManager.unfocus()` and `viewInsets = FakeViewPadding.zero`, passing on both wide (1400x1000) and mobile (400x800) viewports.

### 10.3 Verification and static gates

- `flutter test` (focused tracking suite: inventory_bloc, inventory_history_screen, inventory_dashboard_screen, inventory_item_entry_screen, tracking_repository_impl, inventory_item_entry_save_test): **44 passed (0 failures).**
- `flutter analyze`: **0 issues found.**
- `dart run tool/check_supabase_contracts.dart`: **`[OK]` Contract verification passed.**
- `dart run tool/check_l10n_baseline.dart`: **`[OK]` No new hardcoded strings detected.**
- `dart format --output=none --set-exit-if-changed`: **Clean (0 changed, 0 CR bytes).**
- Staging credentials presence check: **Absent** (`APP_ENV=local`; staging credentials commented out in `.env`). Remote contract items (a)–(e) remain honestly documented as `Unverified — remote execution requires approved staging credentials`.
- Staged index boundary enforced: committed to `Code/mine-flow-app` as `5cb86d7` (`fix(55.8): resolve nested scroll view in item entry sheet and unfocus/poll save-tap in journey`).


