# STEP-48.9: Timeline & Notifications Runtime Evidence (settles 45.10)

## 1. Timeline Journey
- **Verdict:** Verified
- **Run URL:** https://github.com/lvinist/mine-flow-app/actions/runs/33272515594
- **Platform Execution:** e2e-web and e2e-android (16 executed, 0 skipped, 0 failed)
- **Defects Found & Fixed:**
  1. **Date Range Picker Flake:** The `tester.pumpAndSettle()` timed out on `showDateRangePicker` due to its inherent animations/blinking cursor. Fixed by replacing `pumpAndSettle()` with a timed `pump(const Duration(milliseconds: 500))` in `timeline_journey_test.dart`.
  2. **Chronological Ordering Defect:** The test expected section ordering, but missed date ordering logic. The `TimelineCubit` loaded milestones directly without sorting by date. Fixed `timeline_cubit.dart` to sort `milestones` descending by `startDate`. Added a chronological order assertion into the `timeline_journey_test.dart` to regress this. Note: `architecture/04-data-model.md` was silent on milestone chronological ordering, so this is noted for 48.15.
- **Material Widget Misses (STEP-37):** None found in the timeline page or milestone card. `InkWell` was preserved intentionally in STEP-37.

## 2. Notifications Journey
- **Verdict:** Verified
- **Run URL:** https://github.com/lvinist/mine-flow-app/actions/runs/33272515594
- **Platform Execution:** e2e-web and e2e-android (12 executed, 0 skipped, 0 failed)
- **Defects Found & Fixed:**
  1. **STEP-37 Material Widget Miss:** Discovered a surviving `IconButton` on the notification card in `notification_list_page.dart`. Replaced with ForUI's `FButton.icon` to maintain strict UI styling contract.
  2. **Banner Determinism:** The critical notification banner is inherently deterministic as its visibility is tied directly to `NotificationCubit` state and the presence of unread critical notifications, not a timed dismissal. Handled cleanly by the existing test logic without timing hacks.
  3. **Read-State Round-Trip:** The read state (`isRead`) toggles correctly and round-trips via `NotificationRepository` (persisted in `NotificationLocalDataSource` with Hive). Note: The read state updates locally by design (as notifications are client-side generated). This is expected behaviour.
