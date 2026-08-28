# mine-flow — STEP-45.7: Benchmark E2E + route-registration/deep-link (NR-006 / CF-097)

**Recommended model:** Gemini 3.1 Pro (may add a `router.dart` route change; needs judgment + user check-in).

> **How to run:** *"run substep 45.7"*. Self-contained; runnable cold.

## Context

Benchmark feature journey plus resolution of **NR-006** and **CF-097**: `AppRoutes.benchmarkForm`
is declared in `router.dart:77` but never registered as a `GoRoute` — the form is reached via
`Navigator.push` outside the shell, so it is not deep-linkable and drops the sidebar. Read
`Upcoming Prompts/mine-flow-STEP-45-PLAN.md`. **This substep may add a router code change** — surface
the fix to the user before implementing (STEP-46 flagged it as a behavior decision).

## Read these first
- `Upcoming Prompts/mine-flow-STEP-45-PLAN.md`.
- `Code/mine-flow-app/lib/app/router.dart` — benchmark route registration (258-265) + the dead
  `benchmarkForm` constant (77); compare with `equipmentCheckForm`/`attendanceForm` which ARE registered.
- `Code/mine-flow-app/lib/features/benchmark/` and `benchmark_list_screen.dart` (the `Navigator.push`).
- STEP-46 findings — **NR-006** (deep-link on web), **CF-097** (route constant unregistered),
  CF-033 (CRS/UTM zone never persisted), CF-034 (no validation; coords discarded; double-submit),
  CF-077 (integer keypad on coord fields) — remediated in 46.4; confirm at runtime.
- `Code/mine-flow-app/lib/core/utils/crs_utils.dart` (STEP-36).

## Scope

Owns `integration_test/journeys/benchmark_journey_test.dart` and, if the runtime confirms NR-006/
CF-097, the `router.dart` change to register the `form` route under `benchmark-db`.

## Your task

1. **Benchmark journey:** login → create a benchmark with CRS/UTM zone + coordinates → assert CRS
   and coords persist (guards CF-033/034) → edit → list reflects it.
2. **Route/deep-link (NR-006):** on the **web** build, attempt to open `/operations/benchmark-db/form`
   directly (URL) and via the in-app button. Confirm whether it deep-links and whether the shell
   persists.
3. **If NR-006 confirms the CF-097 gap** (form not URL-addressable / drops shell): register a `form`
   child `GoRoute` under `benchmark-db` (matching `equipmentCheckForm`/`attendanceForm`) and navigate
   via it. **Present this change to the user first**; then add a widget/route test asserting the
   route resolves and renders the form within the shell.

Target `EditableText` finders; coord keypad decimal+signed (CF-077/CF-035). Staging creds absent →
**Unverified** with reason.

## Verification
- Benchmark journey passes on Chrome + `Pixel_6a` (or Unverified w/ reason).
- If the route was registered: route/widget test asserts `benchmarkForm` resolves within the shell.
- `flutter analyze` 0 / format clean. Commit on the STEP-45 branch.

## Keeping the docs true (always)
- A router change may touch `architecture/03-architecture-overview.md` navigation notes; note for
  45.15. Record NR-006 outcome (resolved vs carried-forward) for the findings reconciliation.

## Definition of done
- [ ] Benchmark create/edit/list journey passes (or Unverified w/ reason).
- [ ] NR-006/CF-097 resolved (route registered + test) or explicitly carried forward as a named risk.
- [ ] analyze 0 / format clean; files documented.

## Next
Run substep 45.8 (Data Bucket E2E + real Drive upload) in a fresh chat.
