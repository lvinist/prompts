# mine-flow — STEP-11.3: Notification Rules Implementation

> **How to run:** Tell your agent *"run substep 11.3"* (or *"read and run this file"*).

## Context
During STEP-9, the `NotificationRuleEngine` was created, but only Rule 1 (Equipment Check) was fully implemented. Rules 2, 3, and 4 were stubbed out with `TODO` markers. We need to complete the implementation of these rules by injecting the necessary repositories and wiring up the logic.

## Read these first
- `lib/features/notifications/data/services/notification_rule_engine.dart`
- `lib/features/tracking/domain/repositories/tracking_repository.dart`
- `lib/features/attendance/domain/repositories/attendance_repository.dart`
- `lib/features/timeline/domain/repositories/timeline_repository.dart`

## Scope
Complete the `evaluateRules` method in `NotificationRuleEngine` so that all four rules are fully operational.

## Your task
1. **Refactor `NotificationRuleEngine`**: 
   - Add a constructor that injects the required repositories: `TrackingRepository` (for inventory), `AttendanceRepository` (for attendance records), and `TimelineRepository` (for milestones).
2. **Implement Rule 2 (Low Inventory Warning)**:
   - Query the inventory items from `TrackingRepository`.
   - For each item where `quantityOnHand < minThreshold`, generate a warning notification.
3. **Implement Rule 3 (Missing Attendance)**:
   - Query today's attendance records from `AttendanceRepository`.
   - If the list of records is empty (or specific expected crew members are missing, depending on the repository methods available), generate a warning notification.
4. **Implement Rule 4 (Overdue Milestone)**:
   - Query milestones from `TimelineRepository`.
   - For any milestone where `targetDate` has passed and it is not 100% complete, generate an info notification.
5. **Update Dependency Injection**:
   - Ensure that wherever `NotificationRuleEngine` is instantiated (likely in a `Provider` or `BlocProvider` setup in `lib/features/notifications/` or `lib/app/`), the new constructor arguments are properly passed.
6. **Remove all `TODO` comments** related to these rules in the engine.

## Verification
- Run `flutter analyze` to ensure there are no new warnings.
- Run `flutter test` to ensure that you haven't broken any existing DI setups or notification tests.

## Keeping the docs true  (always)
- None required for this implementation completion.

## Definition of done
- [ ] `NotificationRuleEngine` constructor injects necessary repositories.
- [ ] Rules 2, 3, and 4 are fully implemented.
- [ ] `TODO` comments are removed.
- [ ] DI configuration is updated to pass the new dependencies.
- [ ] Tests pass cleanly.

## Next
When this substep is done, update its status in the STEP PLAN, then tell the user the next action: *"run substep 11.4"*, in a **fresh chat**.
