# mine-flow — STEP-7.2: Cut/Fill Volume Tracking UI & State

> **How to run:** Tell your agent *"run substep 7.2"* (or *"read and run this file"*).

## Context
This is substep 7.2 of STEP-7 (Tier 2 - Field Tracking & Measurement). In this substep, you will implement the UI screens and state management for Cut/Fill Volume Tracking.

## Read these first
- `overview.md`
- `Code/mine-flow-docs/architecture/07-ui-design-system.md`
- `Upcoming Prompts/mine-flow-STEP-7-PLAN.md`
- `Code/mine-flow-app/README.md`

## Scope
- BLoC / State Management (`lib/features/tracking/presentation/bloc/cut_fill/`):
  - `cut_fill_bloc.dart`, `cut_fill_event.dart`, `cut_fill_state.dart`: Events to load records, add cut/fill record, and state management for loading, success, failure.
- Presentation Screens & Widgets (`lib/features/tracking/presentation/pages/cut_fill/`):
  - `cut_fill_summary_screen.dart`: Overview dashboard of cumulative cut, fill, and net earthwork volume per zone with visual progress indicators.
  - `cut_fill_entry_screen.dart`: Form for foremen to record cut volume (m³), fill volume (m³), select Zone, select measurement date, and add operational notes. Includes auto-calculation of net volume ($net = cut - fill$).
  - `cut_fill_history_list.dart`: Historical record list showing previous entries, timestamps, and logged-by user.

## Your task
1. Implement `CutFillBloc` handling loading, submission, and validation.
2. Build `CutFillEntryScreen` with responsive form validation (validating positive numeric inputs for cut/fill, zone selection).
3. Build `CutFillSummaryScreen` displaying total volumes, net balance, and historical breakdown.
4. Apply mine-flow UI Design System styling (dark mode support, clear visual telemetry cards for cut vs fill volumes).

## Verification
- Widget and screen components render properly without overflow errors.
- BLoC events trigger appropriate state transitions.

## Definition of done
- [ ] `CutFillBloc` implemented and tested with mock repository.
- [ ] `CutFillEntryScreen` built with form validation and auto-net-calculation.
- [ ] `CutFillSummaryScreen` and historical list built and styled.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user to *"run substep 7.3"* in a fresh chat.
