# mine-flow — STEP-45.9: Reporting / PDF E2E over a real dataset (NR-001)

**Recommended model:** Gemini 3.1 Pro (NR-001 progress/cancel decision + RISK-0014 sensitivity).

> **How to run:** *"run substep 45.9"*. Self-contained; runnable cold.

## Context

Reporting journey plus resolution of **NR-001**: whether PDF generation over a real dataset is slow
enough to need a progress/cancel affordance, and whether mid-run config changes corrupt output. Read
`Upcoming Prompts/mine-flow-STEP-45-PLAN.md`. A UI change here (progress/cancel) should be surfaced
to the user first. **Respect RISK-0014** — assert current documented reporting semantics, not
un-shipped corrections.

## Read these first
- `Upcoming Prompts/mine-flow-STEP-45-PLAN.md`.
- `Code/mine-flow-app/lib/features/reporting/` and `lib/core/services/pdf_service.dart`.
- `report_config_page.dart` (S23) — the generate flow.
- STEP-46 findings — **NR-001** (PDF over real dataset; no cancel/progress; mid-run config change),
  CF-030 (Reports no nav entry / shell drop), CF-073 (date-range label desyncs), CF-074 (zone filter
  raw free-text ID), CF-075 (Buat Laporan low contrast) — remediated; confirm at runtime.
- `Code/mine-flow-docs/registries/risks.yml` — **RISK-0014** (legacy cut/fill columns; net = cut − fill).

## Scope

Owns `integration_test/journeys/reporting_journey_test.dart` and any progress/cancel UI change
NR-001 warrants.

## Your task

1. **Generate each report type** over the largest available staging dataset; measure duration.
2. **Mid-run behavior (NR-001):** attempt navigate-away during generation (confirm the cubit/result
   behavior) and a config change mid-run; determine whether output can mismatch config.
3. **Decide + implement (if warranted):** a progress indicator and/or cancel affordance, and locking
   config controls during generation. Present the decision to the user before implementing; add a test.
4. Confirm CF-030 (Reports reachable via nav, stays in shell) and CF-073 (date-range label) hold at runtime.
5. Assert only current documented reporting semantics (RISK-0014); flag drift for 45.15.

Staging creds/dataset absent → **Unverified** with reason.

## Verification
- Reporting journey passes on Chrome + `Pixel_6a` (or Unverified w/ reason).
- Any progress/cancel change has a test.
- `flutter analyze` 0 / format clean. Commit on the STEP-45 branch.

## Keeping the docs true (always)
- Record NR-001 outcome for 45.15; RISK-0014 status may update if reporting semantics were touched.

## Definition of done
- [ ] Reporting journey (each report type) passes (or Unverified w/ reason).
- [ ] NR-001 resolved (progress/cancel decided + implemented w/ test) or carried forward.
- [ ] analyze 0 / format clean; files documented.

## Next
Run substep 45.10 (Timeline & Notifications E2E) in a fresh chat.
