# mine-flow — STEP-45.5: Cut/Fill & Land Clearing E2E journeys

**Recommended model:** Gemini 3.1 Pro (RISK-0014 semantic subtlety — assert current documented semantics only).

> **How to run:** *"run substep 45.5"*. Self-contained; runnable cold.

## Context

Tier-2 field-measurement journeys. Depends on 45.3. **Sensitive to RISK-0014** — the reporting/
tracking datasource is still on legacy cut/fill columns with `net = cut − fill`; do **not** assert
a corrected semantic that has not shipped. Read `Upcoming Prompts/mine-flow-STEP-45-PLAN.md` (Q3).

## Read these first
- `Upcoming Prompts/mine-flow-STEP-45-PLAN.md` — Q3 (canonical semantics for assertions).
- `Code/mine-flow-app/lib/features/tracking/` (cut/fill + land clearing).
- `Code/mine-flow-docs/registries/risks.yml` — **RISK-0014** (legacy columns).
- STEP-46 findings — CF-013 (Ha not converted + plan+actual sum), CF-014 (BCM/LCM conflated),
  CF-035/CF-040 (edit drops zero/negative elevations), CF-043 (free-text into enumerated method),
  CF-044 (Plan/Actual tabs share date/zone) — remediated; confirm at runtime.

## Scope

Owns `integration_test/journeys/cut_fill_journey_test.dart` and `land_clearing_journey_test.dart`.

## Your task

1. **Cut/Fill:** login → create an entry with BCM/LCM + material type (STEP-33 columns) → persist to
   staging → edit (including a zero/negative-adjacent elevation to guard CF-035/040) → list reflects
   it. Assert **only the current documented** volume semantics (per Q3/RISK-0014); flag any drift for 45.15.
2. **Land Clearing:** login → create a plan and an actual entry via the Plan/Actual tabs → assert
   the tabs keep independent date/zone (guards CF-044) → method via combobox (guards CF-043) →
   area shown with correct unit handling (guards CF-013) per current documented behavior.

Target `EditableText` finders. Staging creds absent → **Unverified** with reason.

## Verification
- Both journeys pass on Chrome (and `Pixel_6a` if booted), or Unverified w/ reason.
- `flutter analyze` 0 / format clean. Commit on the STEP-45 branch.

## Keeping the docs true (always)
- If runtime volume/area semantics contradict a doc or RISK-0014's description, record for 45.15
  (may update RISK-0014 status), don't silently assert the "correct" number.

## Definition of done
- [ ] Cut/fill + land-clearing journeys pass (or Unverified w/ reason), asserting current documented semantics.
- [ ] CF-035/040/043/044 runtime guards present.
- [ ] analyze 0 / format clean; files documented.

## Next
Run substep 45.6 (Inventory & Equipment Checks E2E) in a fresh chat.
