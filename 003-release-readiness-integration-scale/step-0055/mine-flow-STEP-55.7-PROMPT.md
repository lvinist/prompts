# mine-flow — STEP-55.7: Equipment Check Migration and Polish

> **How to run:** Tell your agent “run substep 55.7”. Execute cold in a fresh chat.
>
> **Assigned model: Gemini 3.7 Flash High.** The SOP and D7 behavior are already defined; this is a bounded migration onto shared components with exact long-list and status checks.

## Context
Replace inline expansion detail with a route-backed inspection surface and migrate the long SOP form/report without changing checklist policy.

## Read first
STEP-55 PLAN; prior findings; master spec §§2–3, 4.6, 5–7; Doc 07; Docs 04/11/12/15; equipment files/tests, router, report APIs; STEP-54.7 findings.

## Impeccable
Run context once. Use native `adapt` for long Android detail/full-page and sheet/IME/back, `layout` for checklist reading order, `harden` for partial/error/offline states, then bounded `polish`.

## Task
- Add create `/teams/equipment-check/form?siteId=<id>` and detail `/teams/equipment-check/:id`; site context must be authorized and authenticated foreman identity must not come from URL.
- Migrate long SOP create flow to responsive sheet with one clear scroll owner, D4, durable route context, safe areas/IME.
- Replace inline `ExpansionTile` detail: Web read-only right inspector; Android route-backed full page. Fetch by ID and show all checklist results, remarks, metadata, inspector, timestamp.
- Standardize PASS/FAIL and status bands with shared semantic badge and labelled >=48dp controls, never color-only.
- Replace report push with equipment contextual dialog while preserving search/equipment/status state.
- Remove actionable Material residuals without changing SOP items or domain meanings.

## Tests and verification
Cover authorized/unauthorized site context; identity derivation; cold detail/not-found; platform detail override; long 15–30 item order/semantics; D4/back/drag/IME/scroll; PASS/FAIL mappings; report state; offline/error/empty; 48dp/2x text/themes/focus. Run focused equipment/router/report/shared suites, format/analyze/guards, Web + Pixel_6a bounded runtime inspection. Write `mine-flow-STEP-55.7-FINDINGS.md` tracing `FC-54.7-001..007`.

## Boundaries
No SOP checklist/content changes, URL user ID trust, mobile bottom-sheet detail, local expansion detail, or color-only status. Escalate authorization/data-order mismatches or repeated failure.

## Definition of done
SOP entry and inspection are route-backed, platform-correct, guarded, accessible, state-preserving, tested, and polished.

## Next
Run substep 55.8 in a fresh chat.
