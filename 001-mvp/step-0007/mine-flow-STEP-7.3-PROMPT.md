# mine-flow — STEP-7.3: Land Clearing Area Tracking UI & State

> **How to run:** Tell your agent *"run substep 7.3"* (or *"read and run this file"*).

## Context
This is substep 7.3 of STEP-7 (Tier 2 - Field Tracking & Measurement). In this substep, you will implement the UI screens and state management for Land Clearing Area Tracking.

## Read these first
- `overview.md`
- `Code/mine-flow-docs/architecture/07-ui-design-system.md`
- `Upcoming Prompts/mine-flow-STEP-7-PLAN.md`

## Scope
- BLoC / State Management (`lib/features/tracking/presentation/bloc/land_clearing/`):
  - `land_clearing_bloc.dart`, `land_clearing_event.dart`, `land_clearing_state.dart`: Events to load records, record cleared area, filter by zone/date.
- Presentation Screens & Widgets (`lib/features/tracking/presentation/pages/land_clearing/`):
  - `land_clearing_summary_screen.dart`: Overview dashboard of cumulative cleared area (m² and converted hectares) per zone.
  - `land_clearing_entry_screen.dart`: Form for logging cleared area, selecting clearing method (e.g. bulldozer, excavator, manual tree felling), zone selection, and terrain notes.
  - `land_clearing_history_list.dart`: List of past land clearing activity logs.

## Your task
1. Implement `LandClearingBloc` managing state for land clearing entry and list loading.
2. Build `LandClearingEntryScreen` with input validation (numeric area cleared, dropdown for clearing method, zone selection).
3. Build `LandClearingSummaryScreen` showing cumulative cleared area with unit toggle/display (m² / Hectares: 1 ha = 10,000 m²).
4. Integrate with mine-flow design system cards and telemetry styling.

## Verification
- UI components render without overflow errors.
- Unit conversions (m² to ha) calculate correctly.

## Definition of done
- [ ] `LandClearingBloc` implemented.
- [ ] `LandClearingEntryScreen` created with form validation.
- [ ] `LandClearingSummaryScreen` created with area breakdown.

## Next
**Before finishing this task, you MUST do the bookkeeping:**
1. Open `prompts/STEP-index.md` and change the Status of Substep 7.3 from `Planned` to `Done`. Update the Output / Deliverables column with the paths you created.
2. Open `Upcoming Prompts/mine-flow-STEP-7-PLAN.md` and check off `[x] Substep 7.3` in the Definition of done section.
3. Finally, tell the user to *"run substep 7.4"* in a fresh chat.
