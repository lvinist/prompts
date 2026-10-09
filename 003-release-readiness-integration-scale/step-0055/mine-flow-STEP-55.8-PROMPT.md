# mine-flow — STEP-55.8: Inventory Transaction Integrity and Polish

> **How to run:** Tell your agent “run substep 55.8”. Execute cold in a fresh chat.
>
> **Assigned model: Gemini 3.1 Pro High.** A P0 atomic immutable ledger and idempotency contract require data-layer reasoning, while UI/detail/report behavior is explicitly specified.

## Context
Fix inventory history truth before displaying it. Every adjustment must persist an immutable transaction atomically with stock, then the UI may expose route-backed history and shared form/report patterns.

## Read first
STEP-55 PLAN; prior findings; master spec §§2–3, 4.7, 5–9; Docs 04, 06, 11, 12, 15; ADRs/risks; inventory files under `features/tracking/**`, Supabase migrations/types/policies, sync architecture/tests, router/report APIs; STEP-54.8 findings.

## Impeccable
Run context once. Use `harden` for atomic failure/idempotency/offline/numeric/empty history states, `layout` for stock history and dialogs, native `adapt` for Android full detail/IME, then bounded `polish`.

## Task
1. **P0 first:** define/persist immutable adjustment transactions: item ID, signed delta, required reason, authenticated actor, server timestamp, idempotency key. Quantity update + ledger insert must share one transaction/RPC; failures change neither; retries cannot duplicate.
2. Add migration/RPC/RLS/generated contract and data/domain/offline behavior with tests before history UI. Never fabricate prior transactions.
3. Add list `/teams/inventory`, create `/form`, detail `/:id`, edit `/:id/form`; fetch item/history by ID; preserve category/list position.
4. Web history detail uses right inspector; Android uses full page. Show current item and ordered immutable ledger before explicit Edit/Adjust.
5. Migrate item create/edit to responsive sheets with D4/D5.
6. Preserve stock-adjustment dialog and current/next preview; add transactional persistence without turning it into a page.
7. Differentiate out-of-stock from low/reorder using icon+text+semantics and tested thresholds.
8. Use contextual inventory report; replace residual Material fields/FABs and provide labelled >=48dp adjust/delete actions.
9. Keep current module placement and Inventory BLoC boundary.

## Tests
Migration/RPC atomicity, rollback, idempotent retry, authorization/RLS, signed delta/reason/actor/timestamp, concurrent adjustment behavior, history ordering/immutability, no fabricated legacy rows; route reconstruction/unauthorized/not-found; create/edit dirty guard; adjustment preview/error; stock thresholds; report/category retention; numeric IME; full-page mobile detail; focus/semantics/targets/themes.

Run migration/contract/data/domain/BLoC/widget/router suites, Supabase guard, format/analyze. Use staging only with approved non-production credentials; otherwise record remote execution Unverified. Produce `mine-flow-STEP-55.8-FINDINGS.md` tracing `FC-54.8-001..011`.

## Boundaries
No visual history before truthful persistence, no client-side two-write pseudo-transaction, no mutable/deletable ledger, no module refactor, no production remote mutation. Update docs/ADR/risk for the new contract.

Escalate if atomic RPC design, RLS actor attribution, offline idempotency, or legacy-history treatment is ambiguous; or if the same remediation fails twice.

## Definition of done
Stock adjustment is atomic/idempotent/auditable; route-backed history and forms are platform-correct; focused/static/contract gates pass with honest remote evidence.

## Next
Run substep 55.9 in a fresh chat.
