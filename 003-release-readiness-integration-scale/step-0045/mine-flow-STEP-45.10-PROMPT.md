# mine-flow — STEP-45.10: Timeline & Notifications E2E journeys

**Recommended model:** Gemini 3.7 Flash High (read-mostly journeys; simplest of the feature set).

> **How to run:** *"run substep 45.10"*. Self-contained; runnable cold.

## Context

Tier-3 timeline + notifications journeys. Depends on 45.3. Read
`Upcoming Prompts/mine-flow-STEP-45-PLAN.md`.

## Read these first
- `Upcoming Prompts/mine-flow-STEP-45-PLAN.md`.
- `Code/mine-flow-app/lib/features/timeline/` and `lib/features/notifications/`.
- STEP-46 findings — CF-046 (severity colors identical; title contrast), CF-067 (Berjalan/Selesai
  badges same color) — remediated; confirm at runtime. Notification rule engine wired in STEP-11.5.

## Scope

Owns `integration_test/journeys/timeline_journey_test.dart` and `notifications_journey_test.dart`.

## Your task

1. **Timeline:** login → timeline renders staging data across the date range → milestone cards
   display with correct status badges (guards CF-067).
2. **Notifications:** login → notification list + persistent banner render → dismiss a notification
   and dismiss-all → assert state clears. If feasible, trigger a rule-engine notification end-to-end
   (e.g. an action that fires a rule) and assert it appears with correct severity styling (CF-046).

Target `EditableText` finders. Staging creds absent → **Unverified** with reason.

## Verification
- Both journeys pass on Chrome (and `Pixel_6a` if booted), or Unverified w/ reason.
- `flutter analyze` 0 / format clean. Commit on the STEP-45 branch.

## Definition of done
- [ ] Timeline + notifications journeys pass (or Unverified w/ reason).
- [ ] analyze 0 / format clean; files documented.

## Next
Run substep 45.11 (Field-critical offline/sync full journey) in a fresh chat.
