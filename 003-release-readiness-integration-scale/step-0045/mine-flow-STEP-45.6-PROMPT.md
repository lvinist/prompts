# mine-flow — STEP-45.6: Inventory & Equipment Checks E2E journeys

**Recommended model:** Gemini 3.7 Flash High (pattern journeys; concrete guards CF-017/019/054).

> **How to run:** *"run substep 45.6"*. Self-contained; runnable cold.

## Context

Tier-2 inventory + Tier-1 equipment-check journeys. Depends on 45.3. Read
`Upcoming Prompts/mine-flow-STEP-45-PLAN.md`.

## Read these first
- `Upcoming Prompts/mine-flow-STEP-45-PLAN.md`.
- `Code/mine-flow-app/lib/features/tracking/` (inventory) and `lib/features/equipment_check/`.
- STEP-46 findings — CF-017 (SOP checklist defaults all PASS), CF-019 (inventory delete no
  confirm/gate), CF-039 (no validation; serial optional), CF-054 (quantity silently
  discarded/negative) — remediated; confirm at runtime.

## Scope

Owns `integration_test/journeys/inventory_journey_test.dart` and `equipment_check_journey_test.dart`.

## Your task

1. **Inventory:** login → add an item (auto-predict name, STEP-33) → stock-adjust (assert quantity
   validated, not silently discarded/negative — guards CF-054) → attempt delete and assert the
   confirm/role gate (guards CF-019) → list reflects state.
2. **Equipment checks:** login → open an SOP inspection → submit with a **genuine non-default**
   checklist state (at least one non-PASS) and assert it persists as entered, not all-PASS default
   (guards CF-017) → history reflects it.

Target `EditableText` finders. Staging creds absent → **Unverified** with reason.

## Verification
- Both journeys pass on Chrome (and `Pixel_6a` if booted), or Unverified w/ reason.
- `flutter analyze` 0 / format clean. Commit on the STEP-45 branch.

## Definition of done
- [ ] Inventory + equipment-check journeys pass (or Unverified w/ reason).
- [ ] CF-017/019/054 runtime guards present.
- [ ] analyze 0 / format clean; files documented.

## Next
Run substep 45.7 (Benchmark E2E + route-registration/deep-link) in a fresh chat.
