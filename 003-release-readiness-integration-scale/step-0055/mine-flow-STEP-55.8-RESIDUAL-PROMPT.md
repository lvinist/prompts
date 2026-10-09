# mine-flow — STEP-55.8 RESIDUAL: Inventory remote-contract evidence + index reconciliation

> **How to run:** Tell your agent "run 55.8 residual fix only". Execute cold in a fresh chat.
>
> **Assigned model: Gemini 3.1 Pro High.** Same tier as 55.8 — the residual is a P0 remote data-contract evidence gap (atomicity/RLS/idempotency) plus bookkeeping, bounded by written authority.

## Why this exists (audit 2026-09-21, do-not-trust-status pass)

The 55.8 **code is on disk and its focused/static gates are green**, but the STEP-index row still reads **Planned** and the durable evidence has a hole the FINDINGS file half-admits. Audit facts, verified on `step-0055-cohesive-ui-rebuild`:

- Landed commits: `16e31bd` (feat inventory) + `aa04996` (out-of-stock/low-stock follow-up).
- Migration `supabase/migrations/20260913000001_step_55_8_inventory_transactions.sql` exists — immutable `inventory_transactions` table + `adjust_inventory` RPC.
- Routes `/teams/inventory`, `/:id`, `/:id/form` present in `lib/app/router.dart`.
- Screens present: `inventory_dashboard_screen.dart`, `inventory_history_screen.dart`, `inventory_item_entry_screen.dart`, `stock_adjustment_dialog.dart`.
- Focused suite **PASS** (34 tests): `inventory_bloc_test.dart`, `inventory_dashboard_screen_test.dart`, `inventory_history_screen_test.dart`, `inventory_item_entry_screen_test.dart`, `tracking_repository_impl_test.dart`.
- `flutter analyze` exit 0; Supabase contract guard `[OK]`.
- Inventory E2E journey already migrated to `find.widgetWithText(FButton, 'Tambah Item')` (was `FloatingActionButton`).

**The gap:** every "atomicity / rollback / idempotent-retry / RLS actor attribution / concurrent adjustment / no-fabricated-legacy-rows" claim is currently pinned only at the **client/repository-mock** layer (`idempotencyKey` is passed through and mocked). The migration SQL's real transactional semantics against Supabase are **Unverified** — the 55.8 FINDINGS §6 concedes this as "shallow verification". The 55.8 prompt required these be exercised on staging *or explicitly recorded Unverified*; right now they are neither exercised nor cleanly recorded, and the index row is stale.

## Residual scope (exact — nothing else)

1. **Remote contract evidence.** If approved non-production staging credentials are available (`.env` staging keys; load without printing values, assert only presence/length), exercise against staging: (a) one `adjust_inventory` call updates quantity + inserts exactly one ledger row atomically; (b) an induced failure changes neither table; (c) a retry with the same idempotency key does **not** duplicate the ledger row; (d) RLS attributes the row to the authenticated actor and blocks a cross-tenant write; (e) no fabricated/legacy rows were seeded. Record exact evidence. **If staging credentials are absent, record every one of (a)–(e) as `Unverified — remote execution requires approved staging credentials` in the FINDINGS** — do not claim them from mock tests, and do not mutate production.
2. **Ledger immutability + ordering** — confirm the migration grants no UPDATE/DELETE on `inventory_transactions` to the app role (read the SQL policy block and quote it), and that history renders in server-timestamp order. Pin the ordering with a widget/data test if not already covered.
3. **FINDINGS reconciliation.** Append a dated "Residual (55.8) — remote evidence" section to `mine-flow-STEP-55.8-FINDINGS.md` that (a) separates client-mock coverage from remote coverage, (b) states the (a)–(e) dispositions honestly, (c) does not overwrite the original section.
4. **Report the index-row replacement line** for STEP-55 row 55.8 (see Next). Do **not** flip the row yourself and do **not** touch the STEP-55.11 close — 55.11 is a separate residual.

## Read first

- `Upcoming Prompts/mine-flow-STEP-55-PLAN.md`; `Upcoming Prompts/mine-flow-STEP-55.8-PROMPT.md`; `Upcoming Prompts/mine-flow-STEP-55.8-FINDINGS.md`
- Master spec §§2–3, 4.7; ADR-0012 (volume/derived-semantics precedent for schema sweeps); `registries/risks.yml`
- `supabase/migrations/20260913000001_step_55_8_inventory_transactions.sql`, `supabase/types/database.ts`
- `lib/features/tracking/{data,domain,presentation}/**` inventory paths; `lib/app/router.dart` (inventory routes only)
- `references/remote-supabase-ops.md` and `references/staging-gated-e2e-journeys.md` in the throughstone-workflow skill

## Pre-flight (do not skip)

1. `git -C Code/mine-flow-app status --short --branch` + `git log --oneline -5`. The worktree currently carries an **uncommitted 55.1/55.2/55.3 residual lane** (reporting dialog, `app_interaction_primitives.dart`, `land_clearing_*`) plus untracked scratch (`.step55.11*`, `run_web_wrapper.dart`, `m2_challenger_stress_test.dart`). **Preserve all of it byte-for-byte — it is another lane's work. Do not stage, reset, stash, or absorb it.** Your changes are inventory-only and must be committed as their own `fix(55.8): ...` commit with staged-index proof (`git diff --cached --name-status` shows only inventory files + FINDINGS).
2. Confirm `dart-define`/staging credential presence without echoing values before attempting any remote step.

## Ownership boundary

- ALLOWED: the migration SQL (read-only unless a policy fix is proven necessary — if so, a new migration, never edit the applied one), inventory `lib/features/tracking/**` files, inventory router hunks (staged-index proof), inventory tests, `mine-flow-STEP-55.8-FINDINGS.md` (append dated section).
- FORBIDDEN: reporting dialog, `app_interaction_primitives.dart`, land_clearing, any other feature, `STEP-index.md` (report the line only), the 55.11 close report.

## Tests and verification

- `flutter test test/features/tracking/presentation/inventory_bloc_test.dart test/features/tracking/presentation/inventory_history_screen_test.dart test/features/tracking/presentation/inventory_dashboard_screen_test.dart test/features/tracking/presentation/inventory_item_entry_screen_test.dart test/features/tracking/data/repositories/tracking_repository_impl_test.dart`
- `flutter analyze` (expect 0); `dart run tool/check_supabase_contracts.dart` (expect `[OK]`).
- Record exact commands + counts. No production remote mutation. Never print secrets.

## Boundaries and escalation

No client-side two-write pseudo-transaction, no mutable/deletable ledger, no module refactor, no fabricated legacy rows, no editing an applied migration. Escalate if RLS actor attribution or offline idempotency is ambiguous, if staging cannot be reached safely, or if the same remediation fails twice.

## Definition of done

Remote contract items (a)–(e) are either exercised on approved staging with recorded evidence or honestly marked `Unverified`; ledger immutability/ordering confirmed; FINDINGS carries a dated residual section separating mock from remote coverage; inventory-only commit with staged-index proof; focused/static/contract gates green.

## Next

Report the exact replacement evidence-cell line for STEP-index row 55.8 and whether it is now flippable to **Done** (or Done-with-recorded-Unverified-remote). Do **not** flip it yourself. Tell the user the 55.8 residual is complete and hand off to the 55.11 close residual.


---

## E2E residual routed from 55.11 (2026-09-23) — inventory save-tap not reaching the button (REAL product defect)

**Source:** CI run `35894532969` at app head `fe17e2d`.
**Failure:** `inventory_journey_test.dart:221` — `Expected: true, Actual: <false>` with the journey's own message: *"After the save tap the form is still open with no snackbar — the tap did not reach the button (web hit-test)."* Web **and** Android.

**This is NOT a test-fixture issue — treat as a real user-facing interaction/geometry defect.** The save button in the inventory item sheet is not receiving the tap: the tap is being absorbed by an overlay, an off-screen/covered button, or a hit-test region mismatch (the same class as an overlay barrier eating pointer events). On web the hit-test is stricter, which is why it surfaces there too.

**Investigate:** the inventory item sheet's save button — is it inside the `AppResponsiveSheet` footer (which now caps footer height per `8d5e8bc`)? Is it below the fold / behind the barrier / not `ensureVisible`d before the tap? Confirm on-device whether a real user can save. If the button is genuinely reachable and only the test needs `ensureVisible`/scroll, that is a fixture fix; if the tap is truly absorbed, that is product work.

**Scope:** inventory save flow, `lib/features/inventory/**` (+ the item sheet). Re-run `flutter test integration_test/journeys/inventory_journey_test.dart` (credential-gated; verified in CI). Flag to owner whether this needs an on-device confirmation before deciding fixture-vs-product.


---

## E2E residual re-route from 55.11 (2026-09-24) — inventory save-tap STILL red after the FToast re-anchor

**Source:** CI run `36015384410` at head `9d29896` (which includes the 55.8-UI
commit `06dc9ec` "anchor inventory save-tap gate on FToast").
**Failure UNCHANGED:** `inventory_journey_test.dart:228` — `Expected: true,
Actual: <false>` — *"After the save tap the form is still open with no toast —
the tap did not reach the button (web hit-test)."* Web + Android.

**The `06dc9ec` re-run did not fix the defect — it only changed what the test
asserts** (snackbar → FToast). The underlying failure is identical: **the save
tap is genuinely not reaching the button on web.** This is a REAL product /
geometry defect, not a finder/assertion problem. Re-anchoring the gate on FToast
was a misdiagnosis of the root cause.

**Investigate the button's reachability, not the assertion:**
- The save button lives in the inventory item sheet's `AppResponsiveSheet`
  footer. STEP-55.11 commit `8d5e8bc` changed the mobile sheet height
  (`textScale > 1.3 ? 1.0 : 0.85`) and footer layout — check whether the save
  button is below the fold / behind the barrier / not `ensureVisible`d before
  the tap on the web viewport specifically.
- The committed `inventory_item_entry_save_test.dart` widget test PASSES (mobile
  0.85 footer reachable) — so the widget-level layout is fine in isolation; the
  E2E web hit-test is where the tap is absorbed. The gap is between the widget
  test's assumptions and the real web-rendered sheet.
- **Confirm on-device whether a real user can actually save an inventory item on
  web.** If the tap is truly absorbed, this is a shippable-blocking product bug,
  not a test fix. Report the on-device result before deciding fixture-vs-product.

**Scope:** inventory save flow reachability, `lib/features/tracking/**` (inventory
bloc/sheet) + the journey. Re-run `flutter drive ... inventory_journey_test.dart`
(credential-gated; verified in CI). Do NOT re-anchor the assertion again — fix
the tap reaching the button.
