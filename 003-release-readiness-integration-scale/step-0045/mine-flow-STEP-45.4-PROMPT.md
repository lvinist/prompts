# mine-flow — STEP-45.4: Attendance & Daily Logging E2E journeys

**Recommended model:** Gemini 3.7 Flash High (straightforward CRUD journeys following the 45.3 template).

> **How to run:** *"run substep 45.4"*. Self-contained; runnable cold.

## Context

Feature journeys for the two Tier-1 field-entry features. Depends on 45.3 (`loginAsStagingUser`).
Read `Upcoming Prompts/mine-flow-STEP-45-PLAN.md`.

## Read these first
- `Upcoming Prompts/mine-flow-STEP-45-PLAN.md`.
- `integration_test/helpers/` (45.1) + `auth_journey_test.dart` (45.3) for the login pattern.
- `Code/mine-flow-app/lib/features/attendance/` and `lib/features/daily_log/`.
- STEP-46 findings — CF-006 (empty foremanId hides logs), CF-007 (log persisted with empty author),
  CF-008 (draft leak on shared device), CF-009 (empty surveyor attribution) — remediated; confirm at runtime.

## Scope

Owns `integration_test/journeys/attendance_journey_test.dart` and `daily_log_journey_test.dart`.
Not the offline path (45.11 exercises the same features offline).

## Your task

1. **Attendance:** login → create an attendance record for a crew member → assert it persists to
   staging with the correct author/recorder attribution (not empty, not hardcoded). Edit it; confirm
   the update. List reflects it.
2. **Daily log:** login → create a daily structured log → assert it persists with the correct author
   (guards CF-006/007) and is visible in the list (not hidden by empty foremanId). Confirm no draft
   leaks across a simulated user switch (guards CF-008) if feasible in-harness; else note for 45.14.
3. Use the zone `CreatableCombobox` where the daily-log form requires a zone (STEP-33).

Target `EditableText` finders. If staging creds absent → **Unverified** with reason.

## Verification
- Both journeys pass on Chrome (and `Pixel_6a` if booted), or Unverified w/ reason.
- `flutter analyze` 0 / format clean. Commit on the STEP-45 branch.

## Keeping the docs true (always)
- Runtime attribution behavior diverging from the data-model doc → note for 45.15.

## Definition of done
- [ ] Attendance + daily-log create/edit/list journeys pass (or Unverified w/ reason).
- [ ] Correct-attribution assertions present (CF-006/007/009 guards).
- [ ] analyze 0 / format clean; files documented.

## Next
Run substep 45.5 (Cut/Fill & Land Clearing E2E) in a fresh chat.
