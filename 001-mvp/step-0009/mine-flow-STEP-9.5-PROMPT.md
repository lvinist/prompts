# mine-flow — STEP-9.5: Integration, Polish & Test Verification

> **How to run:** Tell your agent *"run substep 9.5"* (or *"read and run this file"*).
> A substep is self-contained — it must be executable cold in a fresh chat.

## Context

This is the final substep for Tier 3 features. Substeps 9.1–9.4 built the core logic and UI for Reports, Timeline, and Notifications.
**Goal:** Wire everything into the main app initialization (`AppInitializer`, `router.dart`), add it to the dashboard, and write the verifying test suite.

## Scope

**This substep owns:**
1. Router (`app/router.dart`) and Dashboard updates.
2. Initializer (`app_initializer.dart`, `hive_service.dart`) wiring.
3. Unit and Widget Tests for all 9.x features.
4. Ensuring `flutter test` and `flutter analyze` pass clean.

## Your task

### Task 1: Wire Routes and Dashboard

**File: `lib/app/router.dart`**
Add constants to `AppRoutes`: `reports`, `reportConfig`, `timeline`, `notifications`.
Add GoRoute configurations referencing the pages built in 9.2, 9.3, 9.4. Ensure `ReportConfigPage` takes a `ReportType` from `state.extra`.

**Update `_DashboardPlaceholder`** (or create actual Dashboard if missing):
Update the dashboard grid to include navigation to "Laporan", "Timeline Pekerjaan", and "Notifikasi". Include the `NotificationBanner` widget at the top of the `Scaffold` body if a critical notification is present in the `NotificationCubit`.

### Task 2: App Initializer & Hive Service

**File: `lib/core/init/app_initializer.dart`**
Inject `ReportingRemoteDataSource`, `ReportingRepositoryImpl`, `PdfService`.
Inject `TimelineRemoteDataSource`, `TimelineRepositoryImpl`.
Inject `NotificationRuleEngine`, `NotificationLocalDataSource`, `NotificationRepositoryImpl`.
Make sure these are provided to the Cubits (or added to `AppServices`).

**File: `lib/core/offline/hive_service.dart`**
Register adapter Type IDs 14 (TimelineMilestone) and 15, 16, 17 (Notification enums/models). Open the new boxes (`timeline_milestones_box`, `notifications_box`).

### Task 3: Write Comprehensive Tests

**Reporting Tests:**
Create `test/core/services/pdf_service_test.dart` asserting that generating a PDF with empty data returns a non-empty `Uint8List`.
Create `test/features/reporting/presentation/bloc/report_cubit_test.dart` using `blocTest`. Verify `selectReportType` updates selected type and `generateReport` yields Loading then Success.

**Timeline Tests:**
Create `test/features/timeline/presentation/bloc/timeline_cubit_test.dart` verifying initial loading of milestones.

**Notification Tests:**
Create `test/features/notifications/data/services/notification_rule_engine_test.dart` verifying that calling it after 3 PM generates the critical equipment check notification.

*(Provide exact test implementations using `mocktail` for dependencies).*

### Task 4: Polish & Run
Execute:
```bash
flutter analyze
flutter test
```
Fix any resulting errors.

## Definition of Done
- [ ] Routes wired and accessible from the dashboard.
- [ ] Dependencies injected.
- [ ] Tests written and passing.
- [ ] `flutter analyze` and `flutter test` are perfectly clean.

## Next
After successful verification, close STEP-9 in `prompts/STEP-index.md` (mark as Done) and create the final `mine-flow-STEP-10-PLAN.md` to begin End-to-End Integration.
