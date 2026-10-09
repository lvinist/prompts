# mine-flow — STEP-55.4: Benchmark Integrity, Inspector, and Polish

> **How to run:** Tell your agent “run substep 55.4”. Execute cold in a fresh chat.
>
> **Assigned model: Gemini 3.1 Pro High.** The work is bounded, but projection validation is a P0 data-integrity boundary and must not be reduced to cosmetic form migration.

## Context
Fix benchmark coordinate trust first, then migrate Benchmark DB to shared create/edit/inspect/report patterns.

## Read first
STEP-55 PLAN; prior findings; master spec §§2, 3, 4.3, 5–7; Doc 07; Docs 04/11/12 and relevant ADRs; app README/ARCHITECTURE; benchmark form/list/BLoC/entity/model/repository/datasources/CRS utils/router/tests; STEP-54.4/54.10a findings.

## Impeccable
Run context once. Use `harden` for malformed/out-of-zone/not-found/backend failures, `layout` for dense coordinate inspection and sheet hierarchy, native `adapt` for IME/mobile inspector, and bounded `polish`.

## Task
1. **P0 first:** make projection failure a typed validation result; null/non-finite/out-of-zone/malformed computed coordinates cannot submit and can never fall back to `0.0, 0.0`.
2. Add unit/repository regression tests before form polish. Preserve valid precision and governing CRS semantics.
3. Implement create `/operations/benchmark-db/form`, detail `/:id`, edit `/:id/form`; cold ID routes fetch without `extra`.
4. Use responsive form sheets with D4 and a read-only inspector for coordinates, CRS/datum, order, status, and metadata; explicit Edit only.
5. Improve localized CRS recovery copy with datum and actionable out-of-bounds/zone mismatch guidance.
6. Replace report push with bound benchmark dialog.
7. Replace residual FAB/refresh/dropdowns and provide labelled >=48dp delete/action targets.

## Tests and verification
Cover valid projection boundaries/precision; malformed/out-of-zone/non-finite/null; no persistence on failure; no `0,0` fallback; cold routes and invalid/unauthorized IDs; inspector/read/edit flow; dirty guard; report state; empty/error/retry; IME; targets/semantics/text scale/themes.

Run benchmark unit/data/BLoC/widget/router suites, format, analyze, Supabase contract guard if persistence changes, and bounded Web/Android runtime checks. Write `mine-flow-STEP-55.4-FINDINGS.md` tracing `FC-54.4-001..009` and `FC-54.10a-014`.

## Boundaries
No CRS/datum policy change, silent clamping, fake coordinate history, schema migration without docs/contract evidence, or persistence before validation. Escalate any precision/round-trip disagreement or ambiguous accepted coordinate domain.

## Definition of done
Invalid projections are impossible to persist; route-backed form/inspector/report flows satisfy shared contracts; tests and static/runtime gates pass honestly.

## Next
Run substep 55.5 in a fresh chat.
